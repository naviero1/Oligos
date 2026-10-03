#!/usr/bin/env python3
"""Assemble the canonical OligoTox-Thrombocytopenia CSVs from curation-agent output.

Input is a JSON file with the shape produced by the curation workflow:

    {"lanes": [
        {"lane": "<lane key>",
         "oligos":       [ {<oligos.csv fields, keyed by oligo_name>}, ... ],
         "measurements": [ {<measurements.csv fields, oligo_name as FK>}, ... ],
         "verified":     {"verdicts": [
             {"oligo_name":..., "readout_name":..., "verdict":"CONFIRMED|CORRECTED|REJECTED",
              "reason":..., "corrections":[{"field":..., "corrected_value":...}]}, ...]}},
        ...]}

What it does, in order:
  1. Applies the adversarial verifier's verdicts — REJECTED rows are DROPPED,
     CORRECTED rows have the named fields overwritten.
  2. Deduplicates oligos on a normalized `oligo_name`, merging field-by-field and
     preferring a real value over "TBD" (never overwriting one real value with another;
     conflicts are reported).
  3. Deduplicates measurements on the natural key
     (oligo, study_type, system_model, dose, readout_name, source_ref, source_table).
  4. Assigns stable primary keys TOLG### / TMSR### in deterministic sorted order.
  5. Writes thrombocytopenia/data/oligos.csv and measurements.csv.

Rows referencing an oligo that no agent described are NOT silently dropped: a stub
oligo row is created with TBD design fields so referential integrity holds and the
gap is visible rather than hidden.

Usage:  python3 scripts/assemble_thrombo.py <curation_output.json>
"""
import csv, json, os, re, sys, collections

# Paths are anchored to the ENDPOINT folder that owns this script, so all
# thrombocytopenia artefacts stay inside thrombocytopenia/ and nothing is
# written outside it.
ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt",
              "backbone_chemistry", "sugar_modifications", "gapmer_design",
              "conjugate", "ps_count", "sequence_5to3", "modification_map",
              "purity_pct", "purity_method", "design_source", "notes"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "tissue", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "readout_category", "readout_name", "readout_value",
             "readout_unit", "effect_direction", "effect_vs_control",
             "thrombocytopenia_grade", "is_platelet_specific", "subject_class",
             "source_id", "source_ref", "source_table", "redistribution", "notes"]

EMPTY = {"", None, "TBD", "NA", "n/a", "N/A", "null", "None", "unknown"}

# Controlled-vocabulary near-misses. Extraction agents occasionally mistype an enum
# value ("public_documain"), and a single bad cell fails QC for the whole dataset.
# These are corrected here and every correction is REPORTED — the point is to fix
# unambiguous typos without hiding them. Anything not listed still reaches
# qc_thrombo.py and still fails, which is what should happen to a value whose
# intended meaning is not obvious.
VOCAB_FIXES = {
    "redistribution": {
        "public_documain": "public_domain", "public domain": "public_domain",
        "publicdomain": "public_domain", "public_domian": "public_domain",
        "cc-by": "cc_by", "ccby": "cc_by", "cc by": "cc_by",
        "summary_stats": "summary_stat", "summary stat": "summary_stat",
        "derived_features": "derived_features_only",
    },
    "is_platelet_specific": {"true": "TRUE", "false": "FALSE",
                             "True": "TRUE", "False": "FALSE"},
    "effect_direction": {"increased": "increase", "decreased": "decrease",
                         "unchanged": "no_change", "none": "no_change"},
    "backbone_chemistry": {
        # mononucleotide controls have no internucleotide linkage at all; the
        # extractor spelled this out in prose. "NA" is the schema's term for it,
        # and is deliberately distinct from "TBD" (chemistry unknown).
        "NA (mononucleotides, no internucleotide linkage)": "NA",
        "none": "NA", "n/a": "NA",
    },
    "species": {"Gottingen minipig": "minipig", "gottingen minipig": "minipig",
                "Go\u0308ttingen minipig": "minipig", "swine": "minipig", "pig": "minipig"},
    "study_type": {"invitro": "in_vitro", "in vitro": "in_vitro",
                   "exvivo": "ex_vivo", "ex vivo": "ex_vivo",
                   "animal_in_vivo": "animal_invivo", "in_vivo": "animal_invivo"},
}


# ---------------------------------------------------------------------------
# Cross-source NAME COLLISIONS.
#
# The join key is the compound name, which assumes a name means the same molecule
# everywhere. That assumption broke once, silently, and on the dataset's central
# predictor:
#
#   "ODN 2395" is a standard CpG reagent that is FULLY PHOSPHOROTHIOATE. Sewing
#   2017 uniquely synthesised a phosphodiester variant and named it "ODN2395",
#   reserving "ODN2395_Thio" for the PS form. Every OTHER source using the bare
#   name means the standard PS compound. Merging on the bare name therefore
#   attached 38 rows describing an ACTIVE PS compound to an oligo record asserting
#   ps_count=0 / full_PO — inflating the zero-PS bucket's mean grade and directly
#   undercutting the phosphorothioate hypothesis the dataset exists to test.
#
# Rule: (normalized name, source predicate) -> canonical name. Applied to
# measurements before the join, and every remap is reported.
NAME_DISAMBIGUATION = [
    {
        "name": "odn2395",
        # Sewing (PMC5673186 / journal.pone.0187574) is the ONLY source whose bare
        # "ODN2395" means the phosphodiester variant; it names the PS form
        # explicitly. Any other source means the standard PS reagent.
        "keep_if_source_contains": ["PMC5673186", "0187574"],
        "else_rename_to": "ODN2395_Thio",
        "why": "bare 'ODN 2395' outside Sewing 2017 is the standard fully-PS reagent",
    },
]


# ---------------------------------------------------------------------------
# SYNONYM NAMES — the inverse of a collision: one molecule, two names.
#
# Different papers name the same reagent differently, and joining on the name
# alone splits one compound into two records with the outcome evidence divided
# between them. Each entry below was confirmed by CONTENT, not by the names
# looking similar: identical sequence, identical backbone, identical ps_count,
# and both sources explicitly describing the same variant.
#
#   ODN2395_nonmod (Flierl 2015, 18 rows) == ODN2395 (Sewing 2017, 6 rows)
#     Both are the PHOSPHODIESTER variant of ODN2395:
#     TCGTCGTTTTCGGCGCGCGCCG, full_PO, ps_count 0. Flierl's Methods give
#     "ODN2395 ... with and without PS backbone"; Sewing's Table 2 prints it
#     without thioate marks. Kept separate they would look like two independent
#     negative controls when they are one compound measured twice.
#
# Note this is the OPPOSITE hazard to NAME_DISAMBIGUATION above, which splits one
# name that means two molecules. Both are needed; neither implies the other.
NAME_ALIASES = {
    "odn2395nonmod": "ODN2395",
}


def canonicalize_names(rows):
    """Fold synonym names onto one canonical name. Reports what it folded."""
    folded = collections.Counter()
    for r in rows:
        nk = norm_name(r.get("oligo_name"))
        if nk in NAME_ALIASES:
            was = r["oligo_name"]
            r["oligo_name"] = NAME_ALIASES[nk]
            note = clean(r.get("notes"))
            r["notes"] = ((note if note != "TBD" else "")
                          + f";name_canonicalized_from:{was}"
                          + ";same molecule as the canonical record - identical sequence,"
                            " backbone and ps_count, confirmed by content not by name")
            folded[f"{was} -> {r['oligo_name']}"] += 1
    return folded

def disambiguate(rows, src_field="source_ref"):
    """Remap names that mean different molecules in different sources.

    Applied to BOTH measurements (keyed on `source_ref`) and oligo entries (keyed
    on `design_source`). Doing only the measurements is not enough and was in fact
    the first attempt at this fix: the oligo-level merge unions `aliases` and
    `design_source` by design, so the PS form's identity (`ISIS 818290`,
    `PS-ODN 2395`, the Haematologica table) leaked onto the phosphodiester record
    that asserts ps_count=0. Anyone resolving by alias would then map the PS
    reagent onto the PO record and get the central predictor backwards — the exact
    error the measurement-level remap was meant to prevent.
    """
    fixed = collections.Counter()
    for r in rows:
        nk = norm_name(r.get("oligo_name"))
        for rule in NAME_DISAMBIGUATION:
            if nk != rule["name"]:
                continue
            src = str(r.get(src_field, ""))
            if any(tok in src for tok in rule["keep_if_source_contains"]):
                continue
            r["oligo_name"] = rule["else_rename_to"]
            note = clean(r.get("notes"))
            r["notes"] = ((note if note != "TBD" else "")
                          + f";name_disambiguated:{rule['why']}")
            fixed[f"{rule['name']} -> {rule['else_rename_to']}"] += 1
    return fixed


SEQ_OK = re.compile(r"^[ACGTUacgtu]+$")
# Per-residue modification notation, e.g.
#   G*C*G*A*C*T*...            (* = phosphorothioate linkage)
#   mG*mC*mG*mA*mC*T*A*...     (leading letter = 2'-modified residue: m/f/d/l/e/k)
# The schema stores the BASE sequence with case encoding chemistry, so the
# annotated form is normalized to bases and preserved verbatim in `notes` rather
# than discarded — the annotation is richer than the column can hold, and throwing
# it away would lose real chemistry information.
ANNOT_RESIDUE = re.compile(r"^[A-Za-z]?([ACGTUacgtu])$")


def normalize_sequence(seq, notes):
    """Return (sequence, notes). Strips per-residue modification notation."""
    s = (seq or "").strip()
    if not s or s == "TBD" or SEQ_OK.match(s):
        return s or "TBD", notes
    if s.upper().startswith("NA"):
        # e.g. "NA (mononucleotides)" — no sequence exists for this entity
        return "NA", (notes or "") + f";sequence_not_applicable:{s}"
    if "*" in s:
        toks = [x for x in s.split("*") if x]
        bases = []
        for x in toks:
            m = ANNOT_RESIDUE.match(x)
            if not m:
                return s, notes          # unrecognized — leave it for QC to flag
            bases.append(m.group(1))
        return "".join(bases), (notes or "") + f";sequence_as_printed:{s}"
    return s, notes

# ---------------------------------------------------------------------------
# SUBJECT CLASS — the human/animal division, derived not hand-entered.
#
# The Phase 2 announcement singles out datasets "based on in vitro human systems
# or able to extrapolate data between in vitro human systems and animal data".
# That axis was previously only implicit, recoverable by joining study_type to
# species. Making it a first-class column means a consumer can split human from
# animal evidence without reconstructing the rule — and, because it is COMPUTED
# from (study_type, species) on every assembly rather than typed by an agent, it
# cannot drift out of agreement with the columns it summarises.
#
# `qc_thrombo.py` re-derives it independently and fails the build on any mismatch.
ANIMAL_SPECIES = {"monkey", "rat", "mouse", "dog", "minipig"}


def derive_subject_class(study_type, species):
    st = (study_type or "").strip().lower()
    sp = (species or "").strip().lower()
    if sp == "human":
        if st == "clinical":
            return "human_clinical"
        if st == "ex_vivo":
            return "human_ex_vivo"
        if st == "in_vitro":
            return "human_in_vitro"
        return "human_other"
    if sp in ANIMAL_SPECIES:
        if st == "animal_invivo":
            return "animal_in_vivo"
        if st == "ex_vivo":
            return "animal_ex_vivo"
        if st == "in_vitro":
            return "animal_in_vitro"
        return "animal_other"
    if sp == "multi_species":
        # a finding pooled across species — deliberately NOT forced to one side
        return "multi_species"
    return "unspecified"

# ---------------------------------------------------------------------------
# SOURCE-REFERENCE CANONICALISATION.
#
# Different extraction agents cite the same source with differently-detailed
# strings — one stops at the DOI, another appends the author-year. Left alone the
# same paper counts as two sources, which inflates a headline number the
# submission documents quote. Rows are therefore grouped by the IDENTIFIERS inside
# the reference (NCT / PMID / PMCID / DOI / patent / NDA / EMEA), and the most
# complete string in each group becomes canonical for all of them.
#
# Grouping is on identifiers, never on string similarity: two papers by the same
# authors in the same year must not be merged just because their citations look
# alike.
SRC_ID_PATTERNS = [
    r"(NCT\d{8})", r"PMID[:\s]*(\d{6,8})", r"(PMC\d{6,8})",
    r"(10\.\d{4,9}/[^\s;,()]+)", r"(US\s?[\d,]{7,12}\s?[AB]\d?)",
    r"(NDA\s?\d{6})", r"(EMEA/H/C/\d+)",
]


def _source_key(ref):
    ids = set()
    for pat in SRC_ID_PATTERNS:
        for g in re.findall(pat, ref or "", re.I):
            ids.add(g.rstrip(".").rstrip(")").lower())
    return frozenset(ids) if ids else frozenset({(ref or "").lower()[:60]})


def canonicalise_sources(rows):
    """Fold source_ref variants that carry the same identifiers onto one string."""
    groups = collections.defaultdict(set)
    for r in rows:
        groups[_source_key(r.get("source_ref"))].add(r.get("source_ref") or "")
    canon, folded = {}, collections.Counter()
    for k, variants in groups.items():
        if len(variants) < 2:
            continue
        best = max(variants, key=len)          # the most complete citation wins
        for v in variants:
            if v != best:
                canon[v] = best
                folded[f"{v[:48]}... -> {best[:48]}..."] += 1
    for r in rows:
        v = r.get("source_ref")
        if v in canon:
            r["source_ref"] = canon[v]
    return folded

def norm_name(n):
    """Normalize an oligo name to a join key: case- and punctuation-insensitive."""
    return re.sub(r"[^a-z0-9]", "", (n or "").lower())


def clean(v):
    if v is None:
        return "TBD"
    s = str(v).strip().replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s)
    return s if s else "TBD"


def apply_verdicts(lane):
    """Drop REJECTED rows and apply CORRECTED field overwrites. Returns (rows, stats)."""
    meas = lane.get("measurements") or []
    verified = lane.get("verified") or {}
    verdicts = verified.get("verdicts") or []

    # index verdicts by (normalized oligo, readout_name) — the verifier's addressing scheme
    vindex = {}
    for v in verdicts:
        vindex.setdefault((norm_name(v.get("oligo_name")),
                           clean(v.get("readout_name")).lower()), []).append(v)

    kept, stats = [], collections.Counter()
    for row in meas:
        key = (norm_name(row.get("oligo_name")), clean(row.get("readout_name")).lower())
        vs = vindex.get(key) or []
        verdict = None
        for v in vs:
            # consume each verdict once, so N identical rows map to N verdicts
            if not v.get("_used"):
                v["_used"] = True
                verdict = v
                break
        if verdict is None:
            stats["unverified"] += 1
            kept.append(row)
            continue
        d = verdict.get("verdict")
        if d == "REJECTED":
            stats["rejected"] += 1
            continue
        if d == "CORRECTED":
            for c in verdict.get("corrections") or []:
                f = c.get("field")
                if f in MEAS_COLS or f == "oligo_name":
                    row[f] = c.get("corrected_value")
            note = clean(row.get("notes"))
            reason = clean(verdict.get("reason"))[:160]
            row["notes"] = (note if note != "TBD" else "") + f";verifier_corrected:{reason}"
            stats["corrected"] += 1
        else:
            stats["confirmed"] += 1
        kept.append(row)
    return kept, stats


# `max_phase` is by definition the MAXIMUM development stage a compound reached,
# so two sources disagreeing is usually not a conflict at all — it is one source
# being older. Crooke 2017 lists inotersen as phase 1 because it predates the 2018
# approval. Taking the later stage is the semantically correct merge; "keep first"
# would silently under-report every compound that advanced after its oldest source.
PHASE_RANK = {
    "TBD": -1, "research_panel": 0, "preclinical": 1, "phase_1": 2, "phase_2": 3,
    "phase_2_discontinued": 3, "phase_3": 4, "phase_3_discontinued": 4,
    "approved_EMA": 5, "approved": 6, "class_review": 0,
}


def merge_oligo(dst, src, conflicts):
    """Merge src into dst field-by-field, preferring real values over TBD."""
    for col in OLIGO_COLS:
        if col in ("oligo_id",):
            continue
        s = clean(src.get(col))
        d = clean(dst.get(col))
        if s in EMPTY:
            continue
        if d in EMPTY:
            dst[col] = s
        elif d != s:
            if col == "max_phase":
                if PHASE_RANK.get(s, -1) > PHASE_RANK.get(d, -1):
                    dst[col] = s
                continue
            if col in ("aliases", "notes", "design_source", "sugar_modifications"):
                parts = [p for p in (d.split(";") + s.split(";")) if p and p not in EMPTY]
                dst[col] = ";".join(dict.fromkeys(parts))
            elif col == "sequence_5to3":
                # never silently pick a winner between two different sequences
                conflicts.append(f"{dst['oligo_name']}: sequence conflict {d!r} vs {s!r}")
            else:
                conflicts.append(f"{dst['oligo_name']}.{col}: {d!r} vs {s!r} (kept first)")
    return dst


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        payload = json.load(f)

    lanes = payload.get("lanes") or []
    all_stats = collections.Counter()
    oligo_by_key, conflicts = {}, []
    meas_rows = []

    for lane in lanes:
        lname = lane.get("lane", "?")
        disambiguate(lane.get("oligos") or [], src_field="design_source")
        canonicalize_names(lane.get("oligos") or [])
        for o in lane.get("oligos") or []:
            k = norm_name(o.get("oligo_name"))
            if not k:
                continue
            row = {c: clean(o.get(c)) for c in OLIGO_COLS if c != "oligo_id"}
            row["oligo_name"] = clean(o.get("oligo_name"))
            if k in oligo_by_key:
                merge_oligo(oligo_by_key[k], row, conflicts)
            else:
                oligo_by_key[k] = row

        kept, stats = apply_verdicts(lane)
        all_stats.update(stats)
        for m in kept:
            m["_lane"] = lname
            meas_rows.append(m)

    name_fixes = disambiguate(meas_rows)
    alias_fixes = canonicalize_names(meas_rows)
    src_fixes = canonicalise_sources(meas_rows)

    # --- deduplicate measurements on their natural key --------------------------
    seen, deduped = {}, []
    for m in meas_rows:
        nk = (norm_name(m.get("oligo_name")),
              clean(m.get("study_type")).lower(),
              clean(m.get("system_model")).lower(),
              clean(m.get("dose_or_conc_value")).lower(),
              clean(m.get("readout_name")).lower(),
              clean(m.get("source_ref")).lower(),
              clean(m.get("source_table")).lower())
        if nk in seen:
            all_stats["duplicate_dropped"] += 1
            continue
        seen[nk] = True
        deduped.append(m)

    # --- stub any oligo referenced by a measurement but never described ---------
    for m in deduped:
        k = norm_name(m.get("oligo_name"))
        if k and k not in oligo_by_key:
            oligo_by_key[k] = {c: "TBD" for c in OLIGO_COLS if c != "oligo_id"}
            oligo_by_key[k]["oligo_name"] = clean(m.get("oligo_name"))
            oligo_by_key[k]["notes"] = "stub;design_metadata_not_yet_curated"
            all_stats["stub_oligos"] += 1

    # --- handle oligos that no surviving measurement references ------------------
    # Two very different cases hide here, and collapsing them loses real data:
    #
    #  (a) A bare stub — no sequence, no design source. Nothing to learn from and
    #      nothing to predict; dropped.
    #  (b) A fully curated compound with a sourced sequence and design metadata that
    #      simply has no *individual* outcome row, because its source reported a
    #      POOLED outcome across a cohort (e.g. the 16 named ASOs in the Crooke
    #      pooled safety database, whose outcomes are recorded against the
    #      "2'-MOE ASO class pool" pseudo-oligo). These are kept: the sequences are
    #      hard-won, independently length-validated predictors, and the identity of
    #      the compounds making up a pooled cohort is itself information. A modeller
    #      wanting only rows with outcomes gets them from the join, for free.
    #
    # Both counts are reported; qc_thrombo surfaces the kept ones as a warning.
    referenced = {norm_name(m.get("oligo_name")) for m in deduped}
    unreferenced = sorted(k for k in oligo_by_key if k not in referenced)
    dropped_names, kept_unref = [], []
    for k in unreferenced:
        row = oligo_by_key[k]
        substantive = (row.get("sequence_5to3") not in EMPTY
                       or row.get("design_source") not in EMPTY)
        if substantive:
            note = row.get("notes", "")
            row["notes"] = ((note if note not in EMPTY else "")
                            + ";no_individual_measurement_row"
                            + ";outcome_reported_only_at_cohort_level_by_its_source")
            kept_unref.append(row["oligo_name"])
            all_stats["oligo_kept_no_measurements"] += 1
        else:
            dropped_names.append(row["oligo_name"])
            all_stats["oligo_dropped_empty_stub"] += 1
            del oligo_by_key[k]

    # --- assign stable IDs (deterministic: sorted by name) -----------------------
    ordered = sorted(oligo_by_key.items(), key=lambda kv: kv[1]["oligo_name"].lower())
    for i, (k, row) in enumerate(ordered, start=1):
        row["oligo_id"] = f"TOLG{i:03d}"
    keymap = {k: row["oligo_id"] for k, row in ordered}

    # measurements sorted by oligo then source then readout for stable IDs
    deduped.sort(key=lambda m: (keymap.get(norm_name(m.get("oligo_name")), "ZZZ"),
                                clean(m.get("source_ref")).lower(),
                                clean(m.get("source_table")).lower(),
                                clean(m.get("readout_name")).lower()))

    vocab_fixed, seq_fixed = [], []
    os.makedirs(BASE, exist_ok=True)
    with open(os.path.join(BASE, "oligos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OLIGO_COLS)
        w.writeheader()
        for _, row in ordered:
            out = {c: row.get(c, "TBD") for c in OLIGO_COLS}
            raw_seq = out.get("sequence_5to3")
            seq, nts = normalize_sequence(raw_seq, out.get("notes"))
            if seq != raw_seq:
                seq_fixed.append(f"{out['oligo_name']}: {raw_seq[:34]!r} -> {seq!r}")
                out["sequence_5to3"], out["notes"] = seq, nts
                # The announcement requires "the location of all chemical
                # modifications in each oligo". Per-residue notation carries exactly
                # that, and normalising it to bases would throw it away, so the
                # as-printed form is promoted into its own column.
                if out.get("modification_map") in EMPTY and "*" in (raw_seq or ""):
                    out["modification_map"] = raw_seq
            for col, fixes in VOCAB_FIXES.items():
                if col in out and out[col] in fixes:
                    vocab_fixed.append(f"{col}: {out[col]!r} -> {fixes[out[col]]!r}")
                    out[col] = fixes[out[col]]
            w.writerow(out)

    with open(os.path.join(BASE, "measurements.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MEAS_COLS)
        w.writeheader()
        for i, m in enumerate(deduped, start=1):
            row = {c: clean(m.get(c)) for c in MEAS_COLS}
            for col, fixes in VOCAB_FIXES.items():
                v = row.get(col)
                if v in fixes:
                    vocab_fixed.append(f"{col}: {v!r} -> {fixes[v]!r}")
                    row[col] = fixes[v]
            row["measurement_id"] = f"TMSR{i:03d}"
            row["subject_class"] = derive_subject_class(row.get("study_type"),
                                                        row.get("species"))
            row["oligo_id"] = keymap.get(norm_name(m.get("oligo_name")), "TBD")
            if row["source_id"] in EMPTY:
                row["source_id"] = m.get("_lane", "TBD")
            w.writerow(row)

    print(f"oligos.csv        {len(ordered)} rows")
    print(f"measurements.csv  {len(deduped)} rows")
    print("verdicts:", dict(all_stats))
    if src_fixes:
        print(f"canonicalised {sum(src_fixes.values())} source_ref(s) onto a fuller "
              f"citation of the same source:")
        for k, n in src_fixes.most_common(5):
            print(f"    {k}  (x{n})")
    if alias_fixes:
        print("synonym names folded (one molecule, two names):")
        for k, n in alias_fixes.most_common():
            print(f"    {k}  (x{n})")
    if name_fixes:
        print("name disambiguations applied:")
        for k, n in name_fixes.most_common():
            print(f"    {k}  (x{n})")
    if dropped_names:
        print(f"dropped {len(dropped_names)} empty stub oligo(s): {dropped_names[:8]}")
    if vocab_fixed:
        import collections as _c
        cnt = _c.Counter(vocab_fixed)
        print(f"corrected {len(vocab_fixed)} controlled-vocabulary typo(s):")
        for k, n in cnt.most_common(10):
            print(f"    {k}  (x{n})")
    if seq_fixed:
        print(f"normalized {len(seq_fixed)} sequence(s) from per-residue notation "
              f"(original preserved in notes):")
        for x in seq_fixed[:6]:
            print("   ", x)
    if kept_unref:
        print(f"kept {len(kept_unref)} curated oligo(s) with no individual measurement "
              f"(pooled-cohort outcomes): {kept_unref[:8]}")
    if conflicts:
        print(f"\n{len(conflicts)} merge conflict(s) needing review:")
        for c in conflicts[:25]:
            print("  ", c)


if __name__ == "__main__":
    main()
