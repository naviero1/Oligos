#!/usr/bin/env python3
"""Assemble the canonical OligoTox-CNS tables from the per-lane extraction JSONs.

Each extraction lane (regulatory, clinicaltrials, hydrocephalus, nonclinical,
in-vitro-human, patents, sequences, clinical programmes) writes
`notes/cns/extractions/<lane>.json` against the contract in
`notes/cns/EXTRACTION_CONTRACT.md`, using placeholder ids. This script merges
them into `data/cns_oligos.csv` and `data/cns_measurements.csv`.

Three things make this more than a concatenation:

1. **Oligo identity resolution.** The same molecule is extracted independently by
   several lanes under different names (tofersen / BIIB067 / ISIS 666853). Records
   are unioned over *specific* identifier tokens drawn from names and aliases, so
   the lanes' independent views of one molecule collapse to a single `CNS###` row.
   Sequence is deliberately NOT a merge key: patents contain genuine design
   variants that share a nucleobase sequence but differ in wing placement
   (ISIS 791656 vs 791657), and merging those would destroy real predictor
   variance.

2. **Conflict surfacing, not conflict hiding.** When two lanes disagree on a
   non-TBD field the winner is chosen by source strength, and the loser is
   recorded verbatim in the merged row's `notes` as `CONFLICT(field)=...`. A
   silently resolved disagreement is indistinguishable from a fabrication once
   it is in the CSV.

3. **Cross-lane measurement de-duplication.** Lanes overlap by design (the
   hydrocephalus lane and the ClinicalTrials lane both mine the tominersen
   trials). Duplicates are collapsed on a semantic key rather than on the
   `source_table` string, which the lanes format differently.

Usage:  python scripts/assemble_cns.py [--report]
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT_DIR = os.path.join(ROOT, "notes", "cns", "extractions")
OUT_OLIGOS = os.path.join(ROOT, "data", "cns_oligos.csv")
OUT_MEAS = os.path.join(ROOT, "data", "cns_measurements.csv")

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt", "backbone_chemistry",
              "sugar_modifications", "gapmer_design", "conjugate", "ps_count",
              "sequence_5to3", "design_source", "notes"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "cns_region", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "endpoint_domain", "challenge_priority",
             "readout_category", "readout_name", "readout_value", "readout_unit",
             "effect_direction", "effect_vs_control", "neurotox_grade", "reversibility",
             "is_cns_specific", "source_id", "source_ref", "source_table",
             "redistribution", "notes"]

TBD = "TBD"
# What counts as "no value". Deliberately narrow: `NA` and `none` are MEANINGFUL
# controlled-vocabulary members in this schema (`cns_region=NA` means the readout
# is not regional, `conjugate=none` means an unconjugated oligo), so treating them
# as blanks would rewrite real data as missing.
EMPTY = {"", "null", "unknown", "tbd"}

# Lane precedence when two lanes disagree on a field. Earlier wins.
# `sequences` leads because it is the only lane that derives sequences by
# deterministic parse of WHO INN nomenclature with a formula-based length check;
# `patents` and `regulatory` follow because their sources are public-domain
# primary documents.
LANE_RANK = ["sequences", "patents", "regulatory", "hydrocephalus",
             "clinicaltrials", "clinical_programs", "nonclinical", "invitro_human"]

# --- Identity resolution ---------------------------------------------------
# Cross-lane merging is done ONLY on tokens that identify a molecule GLOBALLY.
# This is a whitelist, not a blacklist, because the failure modes are wildly
# asymmetric:
#
#   Under-merging leaves one molecule as two rows. Visible, harmless, fixable.
#   Over-merging FUSES TWO DIFFERENT MOLECULES into one row, silently attaching
#   one compound's toxicity measurements to another compound's sequence. That is
#   indistinguishable from fabricated data once it reaches the CSV.
#
# The trap that motivated this: papers label their compounds "ASO1", "ASO3",
# "AON2". Those are paper-local names — O'Rourke's ASO3 and Kuroda's ASO3 are
# unrelated molecules — but they are distinctive-looking enough to fool any
# "has a digit, so it must be an identifier" heuristic.

# Sponsor development codes: 2-6 letters then 3+ digits (isis666853, biib067,
# ion363, rg6042, wve120101, nvp13 is too short and correctly excluded).
SPONSOR_CODE = re.compile(r"^(isis|ion|biib|rg|ro|wve|aln|stk|nvp|amt|gsk|azd|"
                          r"bms|sqz|tak|pf|ly|jnj)\d{3,}$")
# INN stems for oligonucleotide drugs: -rsen/-sen (ASOs), -siran/-ran (siRNAs),
# -mersen, plus the -virsen/-nersen families.
INN_STEM = re.compile(r"^[a-z]{6,}(rsen|nersen|virsen|mersen|sen|siran|ran)$")
# Brand names seen in this domain (regulatory documents use these as the primary
# identifier, so they must merge with the INN).
BRANDS = {"qalsody", "spinraza", "tegsedi", "exondys", "vyondys", "amondys",
          "viltepso", "onpattro", "amvuttra", "givlaari", "oxlumo", "rivfloza",
          "leqvio", "waylivra", "kynamro", "wainua", "tryngolza", "macugen",
          "vitravene", "defitelio", "imetelstat", "qfitlia"}
# Paper-local compound labels that must never be used as merge keys.
PAPER_LOCAL = re.compile(r"^(aso|aon|asos|oligo|cpd|compound|seq|ctrl|control|"
                         r"scr|scramble|scrambled|mm|ms|sso|gapmer|sirna|pmo|"
                         r"parent|variant|test|ref|reference)[a-z]?\d*$")


def norm(s):
    # NB: `str(s or "")` would be wrong here. The lanes emit numbers as JSON
    # numbers, and 0 is falsy in Python, so that idiom silently turns every
    # `neurotox_grade: 0` (and every zero dose, incidence or readout value) into
    # an empty string and then into TBD — erasing exactly the negative-control
    # rows this dataset is built to preserve.
    return re.sub(r"\s+", " ", ("" if s is None else str(s)).strip())


def key_token(s):
    """Normalise an identifier token for matching: casefold, strip punctuation."""
    t = re.sub(r"[^a-z0-9]+", "", str(s or "").lower())
    return t


def is_empty(v):
    return norm(v).lower() in EMPTY


def ident_tokens(o):
    """Globally-identifying tokens for this oligo (from its name and aliases).

    Returns only tokens that pin down a molecule independently of the document it
    was read from: sponsor development codes, INN drug names, and brand names.
    Everything else — above all paper-local labels like ASO1/AON2 — is excluded,
    so two papers' unrelated "ASO3" can never be fused. See the whitelist above.
    """
    out = set()
    raw = [o.get("oligo_name", "")] + re.split(r"[;,|]", str(o.get("aliases", "") or ""))
    for r in raw:
        r = norm(r)
        if not r:
            continue
        t = key_token(r)
        if not t or PAPER_LOCAL.match(t):
            continue
        if SPONSOR_CODE.match(t) or INN_STEM.match(t) or t in BRANDS:
            out.add(t)
    return out


class Union:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def load_lanes():
    lanes = []
    for path in sorted(glob.glob(os.path.join(EXTRACT_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        lane = d.get("lane") or os.path.splitext(os.path.basename(path))[0]
        lanes.append((lane, d))
    return lanes


def rank(lane):
    return LANE_RANK.index(lane) if lane in LANE_RANK else len(LANE_RANK)


def merge_field(field, candidates, notes_sink):
    """candidates: list of (lane, value). Return chosen value; log conflicts."""
    real = [(l, norm(v)) for l, v in candidates if not is_empty(v)]
    if not real:
        return TBD
    distinct = {}
    for l, v in real:
        distinct.setdefault(v, []).append(l)
    if len(distinct) == 1:
        return real[0][1]
    ordered = sorted(real, key=lambda lv: rank(lv[0]))
    winner = ordered[0][1]
    losers = sorted({v for _, v in real if v != winner})
    notes_sink.append(
        "CONFLICT(%s)=chose'%s'(%s)over%s" % (
            field, winner, ordered[0][0],
            "/".join("'%s'" % x for x in losers)))
    return winner


NCT_RE = re.compile(r"\b(NCT\d{8})\b", re.I)
PAT_RE = re.compile(r"\b(US\s?\d{7,8}\s?[AB]\d?)\b", re.I)
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s,;)\]]+)")
PMID_RE = re.compile(r"\bPMID[:\s]*(\d{6,9})\b", re.I)


def canon_source_ref(ref):
    """Reduce a source reference to its canonical identifier.

    Lanes cite the same document in different prose — `NCT03761849` and
    `NCT03761849 (GENERATION HD1), ClinicalTrials.gov posted results` are one
    trial. Left unnormalised this inflates the apparent source count, breaks
    per-source analysis, and — worse — defeats cross-lane de-duplication, since
    the duplicate detector keys on the reference.
    """
    s = norm(ref)
    m = NCT_RE.search(s)
    if m:
        return m.group(1).upper()
    m = PAT_RE.search(s)
    if m:
        return re.sub(r"\s+", "", m.group(1)).upper()
    m = DOI_RE.search(s)
    if m:
        return "doi:" + m.group(1).rstrip(".,;")
    m = PMID_RE.search(s)
    if m:
        return "PMID:" + m.group(1)
    return s


def load_licences():
    """Map DOI -> Creative Commons licence, read from the archived source XMLs.

    Redistribution rights are asserted from the licence statement in the
    document we actually archived, not from an assumption about the journal.
    Only plain CC-BY permits reproducing raw values in a CC-BY dataset; CC-BY-NC
    and CC-BY-ND do not, so those stay at `summary_stat` (facts quoted, not the
    table republished).
    """
    lic = {}
    for path in glob.glob(os.path.join(ROOT, "sources", "cns", "*.xml")):
        try:
            t = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        doi = re.search(r'<article-id pub-id-type="doi">([^<]+)', t)
        if not doi:
            continue
        codes = {a.lower() for a, _ in
                 re.findall(r"creativecommons\.org/licenses/([a-z\-]+)/([0-9.]+)", t)}
        if not codes:
            continue
        # plain "by" only; anything with nc or nd is not bulk-redistributable here
        free = any(c == "by" for c in codes) and not any(
            "nc" in c or "nd" in c for c in codes)
        lic["doi:" + doi.group(1).strip().lower()] = "cc_by" if free else "restricted"
    return lic


def merge_sequence(candidates, notes_sink):
    """Reconcile sequences reported by several lanes for the same molecule.

    Lanes legitimately differ in NOTATION without differing in fact:
      * T vs U for the same nucleobase. A 2'-MOE 5-methyluridine IS thymine at the
        base level; the sugar lives in `sugar_modifications`, so the base letter
        should not carry it.
      * case. In gapmer rows CASE ENCODES CHEMISTRY (upper = MOE/cEt/LNA wing,
        lower = DNA gap), so `CAGGAtacatttctaCAGCT` strictly dominates the same
        string in flat upper case.

    So: compare on canonical bases (upper, U->T). If the bases agree, this is a
    notation difference, not a conflict — keep the most informative spelling (the
    case-encoded one) and record the variants. Only a genuine base-level
    disagreement is reported as a CONFLICT, because that is the one that means
    somebody has the wrong molecule.
    """
    real = [(l, norm(v)) for l, v in candidates if not is_empty(v)]
    if not real:
        return TBD

    def canon(s):
        return re.sub(r"[^ACGT]", "", s.upper().replace("U", "T"))

    groups = defaultdict(list)
    for l, v in real:
        groups[canon(v)].append((l, v))

    if len(groups) > 1:
        ordered = sorted(real, key=lambda lv: rank(lv[0]))
        winner = ordered[0][1]
        losers = sorted({v for _, v in real if canon(v) != canon(winner)})
        notes_sink.append("CONFLICT(sequence_5to3)=chose'%s'(%s)over%s"
                          % (winner, ordered[0][0],
                             "/".join("'%s'" % x for x in losers)))
        return winner

    variants = groups[next(iter(groups))]

    # Most informative spelling: mixed case (chemistry-encoding) beats flat case;
    # then longer (keeps 3' overhangs); then lane precedence.
    def info(lv):
        l, v = lv
        mixed = 1 if (v != v.upper() and v != v.lower()) else 0
        return (mixed, len(v), -rank(l))
    best_lane, best = max(variants, key=info)

    # The case pattern comes from that spelling, but the BASE LETTERS come from the
    # single highest-ranked lane. Sources disagree on T vs U for the same residue —
    # a 2'-MOE 5-methyluridine is thymine as a nucleobase but uridine as a
    # nucleoside — so the choice is a notation convention, and a convention has to
    # be applied UNIFORMLY to be worth anything. Voting per molecule would settle
    # each one independently and leave the table speaking two alphabets, which is
    # precisely the defect this project already carries in its kidney table, where
    # inotersen and eplontersen share a nucleobase sequence, are spelled
    # differently, and therefore do not compare equal to a model.
    # The `sequences` lane wins because its strings are deterministic parses of
    # WHO INN nomenclature with formula-checked lengths — one consistent source of
    # convention rather than a per-molecule editorial choice.
    if len({v.upper() for _, v in variants}) > 1 and \
            len({len(v) for _, v in variants}) == 1:
        authority = min(variants, key=lambda lv: rank(lv[0]))[1]
        best = "".join(
            (authority[i].lower() if ch.islower() else authority[i].upper())
            for i, ch in enumerate(best))

    others = sorted({v for _, v in variants if v != best})
    if others:
        notes_sink.append("sequence_notation_variants(same_bases)=" +
                          "/".join(others) +
                          ";base_letters_resolved_by_majority;case_encodes_chemistry")
    return best


def main():
    lanes = load_lanes()
    if not lanes:
        raise SystemExit("no extraction JSONs found in %s" % EXTRACT_DIR)

    # ---------------- collect oligo records -----------------------------
    records = []          # (lane, oligo dict)
    for lane, d in lanes:
        for o in d.get("oligos", []):
            records.append((lane, o))

    # union-find over identifier tokens
    uf = Union()
    tok_owner = {}
    for i, (lane, o) in enumerate(records):
        uf.find(i)
        for t in ident_tokens(o):
            if t in tok_owner:
                uf.union(tok_owner[t], i)
            else:
                tok_owner[t] = i

    # Secondary rule: identical name AND identical sequence is the same molecule.
    # Both halves are required. Sequence alone would fuse genuine design variants
    # that share a nucleobase sequence but differ in wing placement (ISIS 791656 vs
    # 791657); name alone would fuse two papers' "ASO1". Together they are safe, and
    # they let a lane that re-reports the same compounds from the same panel — for
    # instance the paired in-vitro arm of a study whose in-vivo arm is already in —
    # attach to the existing rows instead of duplicating them.
    pair_owner = {}
    for i, (lane, o) in enumerate(records):
        seq = norm(o.get("sequence_5to3"))
        name = norm(o.get("oligo_name")).lower()
        if is_empty(seq) or not name:
            continue
        k = (name, seq.upper())
        if k in pair_owner:
            uf.union(pair_owner[k], i)
        else:
            pair_owner[k] = i

    groups = defaultdict(list)
    for i, (lane, o) in enumerate(records):
        groups[uf.find(i)].append(i)

    # ---------------- build merged oligos -------------------------------
    # stable ordering: by best lane rank then by name
    def group_sort_key(idxs):
        best = min(rank(records[i][0]) for i in idxs)
        name = min(norm(records[i][1].get("oligo_name", "")).lower() for i in idxs)
        return (best, name)

    ordered_groups = sorted(groups.values(), key=group_sort_key)

    merged_oligos = []
    tmp_to_cns = {}
    conflicts_total = 0
    for n, idxs in enumerate(ordered_groups, start=1):
        cns_id = "CNS%03d" % n
        members = [(records[i][0], records[i][1]) for i in idxs]
        members.sort(key=lambda lo: rank(lo[0]))
        notes_sink = []
        row = {"oligo_id": cns_id}
        for col in OLIGO_COLS[1:]:
            if col in ("aliases", "design_source", "notes", "sequence_5to3"):
                continue
            row[col] = merge_field(col, [(l, o.get(col)) for l, o in members],
                                   notes_sink)
        row["sequence_5to3"] = merge_sequence(
            [(l, o.get("sequence_5to3")) for l, o in members], notes_sink)
        # aliases: union of every name/alias except the chosen primary name
        alias = set()
        for l, o in members:
            for r in [o.get("oligo_name", "")] + re.split(
                    r"[;,|]", str(o.get("aliases", "") or "")):
                r = norm(r)
                if r and r != row["oligo_name"] and not is_empty(r):
                    alias.add(r)
        row["aliases"] = ";".join(sorted(alias)) if alias else "NA"
        # design_source: union, so every contributing document stays cited
        ds = []
        for l, o in members:
            v = norm(o.get("design_source"))
            if v and not is_empty(v) and v not in ds:
                ds.append(v)
        row["design_source"] = " | ".join(ds) if ds else TBD
        # notes: lane-tagged union plus any conflict records
        nt = []
        for l, o in members:
            v = norm(o.get("notes"))
            if v and not is_empty(v):
                nt.append("[%s] %s" % (l, v))
        nt.extend(notes_sink)
        conflicts_total += len(notes_sink)
        if len(members) > 1:
            nt.append("merged_from_lanes=" + ",".join(sorted({l for l, _ in members})))
        row["notes"] = " ;; ".join(nt) if nt else "NA"

        merged_oligos.append(row)
        for l, o in members:
            tmp_to_cns[(l, o["oligo_id"])] = cns_id

    # ---------------- collect + dedupe measurements ---------------------
    licences = load_licences()
    upgraded = 0
    raw = []
    for lane, d in lanes:
        for m in d.get("measurements", []):
            m = dict(m)
            original = norm(m.get("source_ref"))
            canon = canon_source_ref(original)
            if canon != original:
                m["source_ref"] = canon
                m["notes"] = norm(m.get("notes")) + \
                    " ;; source_ref_as_cited=" + original
            lic = licences.get(canon.lower())
            if lic == "cc_by" and m.get("redistribution") in (
                    "summary_stat", "derived_features_only", "verify"):
                m["redistribution"] = "cc_by"
                m["notes"] = norm(m.get("notes")) + \
                    " ;; redistribution_upgraded_to_cc_by_from_archived_licence_statement"
                upgraded += 1
            cns = tmp_to_cns.get((lane, m.get("oligo_id")))
            if cns is None:
                print("WARN dropping %s/%s: oligo_id %r not found in its lane's oligos"
                      % (lane, m.get("measurement_id"), m.get("oligo_id")))
                continue
            raw.append((lane, cns, m))

    def sem_key(cns, m):
        """Semantic identity of a measurement, independent of source_table wording.

        This must carry EVERY field that defines the dataset's grain, or genuinely
        distinct rows collapse into one. The grain is
        oligo x model x region x delivery x dose x readout, and the same readout at
        two timepoints or in two brain regions is two measurements, not a duplicate —
        so `cns_region` and `exposure_duration` belong here just as much as dose does.
        """
        return (cns,
                key_token(m.get("source_ref")),
                key_token(m.get("study_type")),
                key_token(m.get("species")),
                key_token(m.get("system_model")),
                key_token(m.get("cns_region")),
                key_token(m.get("delivery_method")),
                key_token(m.get("dose_or_conc_value")),
                key_token(m.get("dose_or_conc_unit")),
                key_token(m.get("exposure_duration")),
                key_token(m.get("readout_category")),
                key_token(m.get("readout_name")),
                key_token(m.get("readout_value")))

    def richness(m):
        return sum(1 for c in MEAS_COLS if not is_empty(m.get(c)))

    best = {}
    dupes = Counter()
    for lane, cns, m in raw:
        k = sem_key(cns, m)
        if k in best:
            dupes[lane] += 1
            prev_lane, prev_m = best[k]
            # keep the richer row; tie-break on lane precedence
            if (richness(m), -rank(lane)) > (richness(prev_m), -rank(prev_lane)):
                m = dict(m)
                m["notes"] = norm(m.get("notes")) + \
                    " ;; duplicate_of_lane=%s(kept_this)" % prev_lane
                best[k] = (lane, m)
            else:
                prev_m["notes"] = norm(prev_m.get("notes")) + \
                    " ;; duplicate_also_in_lane=%s" % lane
        else:
            best[k] = (lane, m)

    kept = list(best.values())
    # stable order: lane precedence, then original source, then readout
    kept.sort(key=lambda lm: (rank(lm[0]), norm(lm[1].get("source_ref")),
                              norm(lm[1].get("source_table")),
                              norm(lm[1].get("readout_name"))))

    merged_meas = []
    for n, (lane, m) in enumerate(kept, start=1):
        row = {"measurement_id": "CMS%04d" % n,
               "oligo_id": tmp_to_cns[(lane, m["oligo_id"])]}
        for col in MEAS_COLS[2:]:
            v = m.get(col)
            row[col] = TBD if is_empty(v) and col != "notes" else norm(v)
        # `reversibility=NA` is a lane's way of saying recovery was never looked at,
        # which the vocabulary already expresses as `not_assessed`. Fold it in rather
        # than admitting a second spelling of one concept into the dictionary.
        if row["reversibility"] == "NA":
            row["reversibility"] = "not_assessed"
        # keep the originating lane visible for provenance auditing
        row["notes"] = ("[%s] " % lane) + (row["notes"] if row["notes"] else "NA")
        merged_meas.append(row)

    # ---------------- write ---------------------------------------------
    os.makedirs(os.path.dirname(OUT_OLIGOS), exist_ok=True)
    with open(OUT_OLIGOS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OLIGO_COLS)
        w.writeheader()
        for r in merged_oligos:
            w.writerow(r)
    with open(OUT_MEAS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MEAS_COLS)
        w.writeheader()
        for r in merged_meas:
            w.writerow(r)

    # ---------------- report ---------------------------------------------
    print("redistribution upgraded to cc_by from archived licences: %d rows" % upgraded)
    print("lanes            : %d (%s)" % (
        len(lanes), ", ".join("%s:%d/%d" % (l, len(d.get('oligos', [])),
                                            len(d.get('measurements', [])))
                              for l, d in lanes)))
    print("oligo records in : %d  ->  merged: %d  (collapsed %d duplicates)"
          % (len(records), len(merged_oligos), len(records) - len(merged_oligos)))
    print("field conflicts  : %d (recorded in notes as CONFLICT(field)=...)"
          % conflicts_total)
    print("measurements in  : %d  ->  kept: %d  (dropped %d cross-lane duplicates: %s)"
          % (len(raw), len(merged_meas), len(raw) - len(merged_meas),
             dict(dupes) or "none"))
    multi = [r for r in merged_oligos if "merged_from_lanes=" in r["notes"]]
    print("oligos seen by >1 lane: %d" % len(multi))
    for r in multi[:12]:
        print("   %s %s" % (r["oligo_id"], r["oligo_name"]))
    print("wrote %s and %s" % (OUT_OLIGOS, OUT_MEAS))


if __name__ == "__main__":
    main()
