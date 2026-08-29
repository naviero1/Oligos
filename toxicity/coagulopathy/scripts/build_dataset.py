#!/usr/bin/env python3
"""Build the OligoTox-Coagulopathy tables from the staged extraction records.

    python3 toxicity/coagulopathy/scripts/build_dataset.py

Reads  toxicity/coagulopathy/sources/extraction/*.json  (one file per source bundle,
each the literal output of the extraction round, committed so the build is
reproducible from a clean checkout)
Writes toxicity/coagulopathy/data/{sources,oligos,modifications,measurements}.csv

The script is deterministic and does no network I/O. It assigns stable identifiers,
merges compounds that appear in more than one source, computes the control-referenced
ratio where one is derivable, and assigns the ordinal grade STRICTLY by the published
rule recorded in each row's grade_basis. It never invents a value: anything the sources
did not report stays NOT_REPORTED.
"""
import csv, json, glob, os, re, sys
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(ROOT, "sources", "extraction")
DATA = os.path.join(ROOT, "data")

NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"

# ---------------------------------------------------------------- value parsing
_NUM = re.compile(r"^\s*[<>~≈]?\s*(-?[\d,]+(?:\.\d+)?)")

def central(v):
    """Central value of a printed cell. '96 ± 9' -> 96.0; '31 seconds (range 30-33)' -> 31.0.
    Returns None when the cell carries no leading number (prose, NOT_REPORTED, '>>100')."""
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", NR, NA):
        return None
    s = s.replace("−", "-").replace("×", "x")
    m = _NUM.match(s)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None

def censored(v):
    return bool(re.match(r"^\s*[<>]", str(v).strip()))

# Units whose printed value IS ALREADY a ratio to the matched control.
RATIO_UNITS = {
    "INR": 1.0,
    "fold_change": 1.0,
    "fold": 1.0,
    "ratio": 1.0,
    "%_of_control": 100.0,
    "%_of_baseline": 100.0,
    "percent_of_control": 100.0,
}

def ratio_unit_divisor(unit):
    u = (unit or "").strip()
    if u in RATIO_UNITS:
        return RATIO_UNITS[u]
    if "fraction of the" in u.lower() and "control" in u.lower():
        return 1.0
    return None

def derive_ratio(row):
    """Control-referenced ratio, or (None, reason). Never guesses a denominator."""
    val_raw, unit = row.get("readout_value"), row.get("readout_unit")
    if str(row.get("readout_is_qualitative")).lower() == "true":
        return None, "qualitative_row"
    if censored(val_raw):
        return None, "value_is_censored"
    v = central(val_raw)
    if v is None:
        return None, "no_numeric_value"
    d = ratio_unit_divisor(unit)
    if d is not None:
        return (v / d), "value_is_already_control_referenced"
    c = central(row.get("control_value"))
    if c is None:
        return None, "no_matched_control_value"
    if c == 0:
        return None, "control_value_is_zero"
    return (v / c), "value_over_matched_control"

# ---------------------------------------------------------------- grading rubric
# CTCAE v5.0 (NCI, 27 Nov 2017) laboratory criteria. Only the readouts CTCAE actually
# defines are graded here; everything else is left NOT_REPORTED rather than graded by a
# threshold invented for this dataset.
PROLONGATION = {"aPTT", "PT", "INR", "TT", "ACT", "aPTT_ratio", "PT_INR"}
FIBRINOGEN = {"fibrinogen"}

CTCAE_CITE = "CTCAE_v5.0_control_referenced"

def grade(row, ratio):
    """(grade, basis). Grade only where a published criterion applies to this readout."""
    name = (row.get("readout_name") or "").strip()
    if ratio is None:
        if str(row.get("effect_direction")) == "no_change" and name in (PROLONGATION | FIBRINOGEN):
            return "0", "source_states_measured_no_change_on_a_CTCAE_graded_readout"
        return NR, "no_control_referenced_ratio_derivable"
    if name in PROLONGATION:
        if ratio <= 1.0:   return "0", CTCAE_CITE + ":prolongation_ratio<=1.0"
        if ratio <= 1.5:   return "1", CTCAE_CITE + ":prolongation_>1.0-1.5x"
        if ratio <= 2.5:   return "2", CTCAE_CITE + ":prolongation_>1.5-2.5x"
        return "3", CTCAE_CITE + ":prolongation_>2.5x"
    if name in FIBRINOGEN:
        if ratio >= 1.0:   return "0", CTCAE_CITE + ":fibrinogen_not_decreased"
        if ratio >= 0.75:  return "1", CTCAE_CITE + ":fibrinogen_<1.0-0.75x"
        if ratio >= 0.50:  return "2", CTCAE_CITE + ":fibrinogen_<0.75-0.5x"
        return "3", CTCAE_CITE + ":fibrinogen_<0.5x"
    return NR, "readout_has_no_published_CTCAE_criterion"

# ---------------------------------------------------------------- load
def norm_name(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())

def norm_seq(s):
    s = str(s or "").strip().upper()
    s = re.sub(r"[^ACGTU]", "", s)
    return s if len(s) >= 8 else ""

_SEQ_RUN = re.compile(r"^[ACGTUacgtu][ACGTUacgtu\s\-]*")
_LEAD_INT = re.compile(r"^\s*(\d+)")

def split_sequence(cell):
    """A sequence cell must hold a sequence and nothing else.

    Returns (sequence, note). Extraction sometimes appended prose ("+ 3' inverted dT
    (case-normalised ...)") or printed two strands of a duplex in one cell. The leading
    contiguous nucleotide run is the sequence; everything after it is preserved verbatim
    as a note. A cell with NO leading run (a duplex written 'sense 5'-...; antisense
    5'-...') has no single 5'->3' base string, so the sequence is NOT_APPLICABLE and the
    whole printed cell is kept as the note."""
    raw = str(cell or "").strip()
    if raw in ("", NR, NA):
        return (raw or NR), ""
    m = _SEQ_RUN.match(raw)
    if not m:
        return NA, raw
    seq = re.sub(r"[^ACGTU]", "", m.group(0).upper())
    rest = raw[len(m.group(0)):].strip()
    if len(seq) < 8:
        return NA, raw
    return seq, rest

def split_length(cell):
    """(declared_length, note). Keeps a leading integer, preserves any qualifying prose."""
    raw = str(cell or "").strip()
    if raw in ("", NR, NA):
        return NR, ""
    m = _LEAD_INT.match(raw)
    if not m:
        return NR, raw
    rest = raw[m.end():].strip(" .;:-")
    return m.group(1), rest

def load():
    bundles = []
    for f in sorted(glob.glob(os.path.join(EXTRACT, "*.json"))):
        with open(f) as fh:
            d = json.load(fh)
        d["_bundle"] = os.path.basename(f)[:-5]
        bundles.append(d)
    if not bundles:
        sys.exit(f"no extraction records in {EXTRACT}")
    return bundles

def main():
    bundles = load()
    os.makedirs(DATA, exist_ok=True)

    # ---- sources -----------------------------------------------------------
    src_by_ident, sources = OrderedDict(), []
    src_map = {}                                   # (bundle, local key) -> source_id
    for b in bundles:
        for s in b.get("sources", []):
            ident = (s.get("identifier") or s.get("local_path") or "").strip()
            key = norm_name(ident) or norm_name(s.get("citation"))
            if key not in src_by_ident:
                sid = "COG-S%03d" % (len(sources) + 1)
                rec = {
                    "source_id": sid,
                    "citation": s.get("citation", NR),
                    "identifier": ident or NR,
                    "document_file": (os.path.basename(s.get("local_path", "")).split(" (")[0].strip() or NR),
                    "retrieval_route": s.get("retrieval_route", NR),
                    "licence": s.get("licence", NR),
                    "redistribution": s.get("redistribution", NR),
                    "extraction_bundle": b["_bundle"],
                    "n_oligos": 0, "n_measurements": 0,
                }
                src_by_ident[key] = rec
                sources.append(rec)
            src_map[(b["_bundle"], s.get("source_key"))] = src_by_ident[key]["source_id"]

    # ---- oligos (merged across sources) ------------------------------------
    oligos, by_seq, by_name = [], {}, {}
    olg_map, merges = {}, []
    for b in bundles:
        for o in b.get("oligos", []):
            seq, nm = norm_seq(split_sequence(o.get("sequence_base"))[0]), norm_name(o.get("oligo_name"))
            hit = by_seq.get(seq) if seq else None
            if hit is None and nm:
                hit = by_name.get(nm)
            _seq, _seqnote = split_sequence(o.get("sequence_base"))
            _len, _lennote = split_length(o.get("length_nt"))
            if hit is None:
                oid = "COG-OLG%03d" % (len(oligos) + 1)
                rec = {
                    "oligo_id": oid,
                    "oligo_name": o.get("oligo_name", NR),
                    "aliases": o.get("aliases", NR),
                    "oligo_class": o.get("oligo_class", NR),
                    "modality": o.get("modality", NR),
                    "target_gene": o.get("target_gene", NR),
                    "indication": o.get("indication", NR),
                    "developer": o.get("developer", NR),
                    "max_phase": o.get("max_phase", NR),
                    "length_nt": _len,
                    "length_nt_from_sequence": str(len(_seq)) if _seq not in (NR, NA) else NA,
                    "sequence_5to3_asprinted": o.get("sequence_5to3_asprinted", NR),
                    "sequence_base": _seq,
                    "sequence_note": "; ".join(x for x in (_seqnote, _lennote) if x) or NA,
                    "terminal_modification": NA,
                    "sequence_locus": o.get("sequence_locus", NR),
                    "backbone_chemistry": o.get("backbone_chemistry", NR),
                    "sugar_modifications": o.get("sugar_modifications", NR),
                    "gapmer_design": o.get("gapmer_design", NR),
                    "conjugate": o.get("conjugate", NR),
                    "ps_count": o.get("ps_count", NR),
                    "purity_pct": o.get("purity_pct", NR),
                    "purity_method": o.get("purity_method", NR),
                    "identity_confirmation": o.get("identity_confirmation", NR),
                    "synthesis_platform": o.get("synthesis_platform", NR),
                    "source_ids": src_map.get((b["_bundle"], o.get("source_key")), NR),
                    "n_measurements": 0,
                    "notes": o.get("notes", ""),
                }
                oligos.append(rec)
                if seq: by_seq[seq] = rec
                if nm:  by_name[nm] = rec
                hit = rec
            else:
                sid = src_map.get((b["_bundle"], o.get("source_key")), "")
                if sid and sid not in hit["source_ids"]:
                    hit["source_ids"] += ";" + sid
                # fill gaps only; never overwrite a value already sourced
                for k in ("sequence_5to3_asprinted", "sequence_locus",
                          "backbone_chemistry", "sugar_modifications", "target_gene",
                          "developer", "max_phase", "length_nt", "gapmer_design",
                          "conjugate", "ps_count", "oligo_class", "modality", "indication"):
                    if str(hit.get(k, NR)) in ("", NR) and str(o.get(k, NR)) not in ("", NR):
                        hit[k] = o[k]
                if norm_name(o.get("oligo_name")) != norm_name(hit["oligo_name"]):
                    al = str(hit.get("aliases") or "")
                    if o.get("oligo_name") and o["oligo_name"] not in al:
                        hit["aliases"] = (al + ";" + o["oligo_name"]).strip(";") if al not in ("", NR) else o["oligo_name"]
                merges.append((b["_bundle"], o.get("local_oligo_key"), hit["oligo_id"]))
            olg_map[(b["_bundle"], o.get("local_oligo_key"))] = hit["oligo_id"]

    # ---- measurements ------------------------------------------------------
    measurements, orphans = [], 0
    for b in bundles:
        for m in b.get("measurements", []):
            oid = olg_map.get((b["_bundle"], m.get("local_oligo_key")))
            if oid is None:
                orphans += 1
                continue
            sid = src_map.get((b["_bundle"], m.get("source_key")), NR)
            ratio, how = derive_ratio(m)
            g, basis = grade(m, ratio)
            src = next((s for s in sources if s["source_id"] == sid), None)
            measurements.append({
                "measurement_id": "COG-MSR%04d" % (len(measurements) + 1),
                "oligo_id": oid,
                "source_id": sid,
                "study_type": m.get("study_type", NR),
                "species": m.get("species", NR),
                "system_model": m.get("system_model", NR),
                "matrix": m.get("matrix", NR),
                "delivery_method": m.get("delivery_method", NR),
                "dose_value": m.get("dose_value", NR),
                "dose_unit": m.get("dose_unit", NR),
                "timepoint": m.get("timepoint", NR),
                "exposure_duration": m.get("exposure_duration", NR),
                "n_subjects": m.get("n_subjects", NR),
                "readout_category": m.get("readout_category", NR),
                "readout_name": m.get("readout_name", NR),
                "readout_value": m.get("readout_value", NR),
                "readout_unit": m.get("readout_unit", NR),
                "readout_is_qualitative": str(m.get("readout_is_qualitative", False)).upper(),
                "control_value": m.get("control_value", NR),
                "control_description": m.get("control_description", NR),
                "effect_direction": m.get("effect_direction", NR),
                "effect_vs_control": m.get("effect_vs_control", NR),
                "ratio_to_control": ("%.4g" % ratio) if ratio is not None else NR,
                "ratio_basis": how,
                "coag_tox_grade": g,
                "grade_basis": basis,
                "grade_status": "provisional",
                "severity_stated_by_source": m.get("severity_stated_by_source", NR),
                "on_target_effect": str(m.get("on_target_effect", False)).upper(),
                "unintended_toxicity": str(m.get("unintended_toxicity", False)).upper(),
                "source_locus": m.get("source_locus", NR),
                "redistribution": (src or {}).get("redistribution", NR),
                "verbatim_quote": re.sub(r"\s+", " ", str(m.get("verbatim_quote", ""))).strip(),
                "notes": m.get("notes", ""),
            })

    # ---- modifications -----------------------------------------------------
    mods, mod_orphans = [], 0
    for b in bundles:
        for r in b.get("modifications", []):
            oid = olg_map.get((b["_bundle"], r.get("local_oligo_key")))
            if oid is None:
                mod_orphans += 1
                continue
            mods.append({
                "oligo_id": oid,
                "position": r.get("position", NR),
                "nucleobase": r.get("nucleobase", NR),
                "sugar_mod": r.get("sugar_mod", NR),
                "backbone_linkage_3p": r.get("backbone_linkage_3p", NR),
                "is_5_methyl_C": str(r.get("is_5_methyl_C", False)).upper(),
                "basis": r.get("basis", NR),
            })
    seen = set()
    mods = [m for m in mods if not ((m["oligo_id"], m["position"]) in seen or seen.add((m["oligo_id"], m["position"])))]

    # A 3'-inverted-dT cap or similar terminal residue has no place in a 5'->3' base
    # string, so it cannot own a position row. Lift it to an oligo-level field instead of
    # dropping it, and never silently: the count is reported at the end of the build.
    seq_len = {o["oligo_id"]: len(o["sequence_base"]) for o in oligos
               if o["sequence_base"] not in (NR, NA)}
    by_oid = {o["oligo_id"]: o for o in oligos}
    lifted, kept = 0, []
    for r in mods:
        L = seq_len.get(r["oligo_id"])
        p = int(r["position"]) if str(r["position"]).isdigit() else None
        if L is not None and p is not None and p > L:
            o = by_oid[r["oligo_id"]]
            desc = f"position {p}: {r['nucleobase']}/{r['sugar_mod']} ({r['backbone_linkage_3p']})"
            o["terminal_modification"] = desc if o["terminal_modification"] in (NA, "") else o["terminal_modification"] + "; " + desc
            lifted += 1
        else:
            kept.append(r)
    mods = kept
    mods.sort(key=lambda r: (r["oligo_id"], int(r["position"]) if str(r["position"]).isdigit() else 0))

    # ---- roll-ups ----------------------------------------------------------
    per_o, per_s = defaultdict(int), defaultdict(int)
    for m in measurements:
        per_o[m["oligo_id"]] += 1
        per_s[m["source_id"]] += 1
    o_per_s = defaultdict(set)
    for o in oligos:
        o["n_measurements"] = per_o.get(o["oligo_id"], 0)
        for sid in str(o["source_ids"]).split(";"):
            o_per_s[sid].add(o["oligo_id"])
    for s in sources:
        s["n_measurements"] = per_s.get(s["source_id"], 0)
        s["n_oligos"] = len(o_per_s.get(s["source_id"], ()))

    def write(name, rows):
        p = os.path.join(DATA, name)
        if not rows:
            return p, 0
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
            w.writeheader()
            w.writerows(rows)
        return p, len(rows)

    for nm, rows in (("sources.csv", sources), ("oligos.csv", oligos),
                     ("modifications.csv", mods), ("measurements.csv", measurements)):
        p, n = write(nm, rows)
        print(f"  wrote {os.path.relpath(p, ROOT):<28} {n:>5} rows")

    graded = [m for m in measurements if m["coag_tox_grade"] != NR]
    dist = defaultdict(int)
    for m in graded:
        dist[m["coag_tox_grade"]] += 1
    print(f"\n  merged compounds across sources : {len(merges)}")
    print(f"  terminal caps lifted to oligo   : {lifted}")
    print(f"  orphan measurements dropped     : {orphans}")
    print(f"  orphan modification rows dropped: {mod_orphans}")
    print(f"  graded rows                     : {len(graded)} / {len(measurements)}"
          f"  (0/1/2/3 = {dist['0']}/{dist['1']}/{dist['2']}/{dist['3']})")

if __name__ == "__main__":
    main()
