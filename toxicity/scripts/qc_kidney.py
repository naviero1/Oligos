#!/usr/bin/env python3
"""Quality-control validator for the OligoTox-Kidney dataset.

The kidney dataset previously had no automated validator — its QC log in
`schema.md` was maintained by hand. This ports the checks that earned their place
in the companion CNS round, where each one caught a real defect:

  1. Column-set conformance for both canonical tables.
  2. Primary-key uniqueness and referential integrity (measurements -> oligos).
  3. Controlled-vocabulary conformance for every enum column.
  4. Range checks (nephrotox_grade in 0..3, booleans, numeric dose fields).
  5. Provenance completeness (source_id + source_ref + source_table on every row).
  6. Endpoint-policy checks the kidney rubric implies.
  7. Sequence sanity: IUPAC bases only, case-insensitively (case encodes
     chemistry, so a case-sensitive check rejects correct rows), with length
     cross-checked against length_nt.
  8. An unverified-provenance census: rows whose source_id is `WS` were derived
     from search summaries rather than full text, and METHODOLOGY.md commits to
     verifying them before release. They are reported, not treated as errors.

Exit status is non-zero if any ERROR is raised. WARNINGs are informational.

Usage:  python scripts/qc_kidney.py
"""
import csv
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")
MEAS = os.path.join(ROOT, "data", "measurements.csv")

TBD = "TBD"

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt",
              "backbone_chemistry", "sugar_modifications", "gapmer_design",
              "conjugate", "ps_count", "sequence_5to3", "design_source", "notes"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "tissue", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "readout_category", "readout_name",
             "readout_value", "readout_unit", "effect_direction",
             "effect_vs_control", "nephrotox_grade", "is_kidney_specific",
             "source_id", "source_ref", "source_table", "redistribution", "notes"]

ENUMS = {
    "oligo_class": {"ASO_gapmer", "siRNA", "GalNAc_siRNA", "splice_switching_ASO",
                    "PMO", "aptamer", "other"},
    "max_phase": {"approved", "approved_EMA", "phase_3", "phase_3_discontinued",
                  "phase_2", "phase_1", "preclinical", "research_panel",
                  "class_review"},
    "backbone_chemistry": {"full_PS", "PS_PO_mix", "full_PO", "PMO_neutral",
                           "mixed", TBD},
    # PEG_5prime is the positional form of the schema's PEG value, in use since
    # the aptamer row records where the PEG sits.
    "conjugate": {"none", "GalNAc", "lipid", "peptide", "PEG", "PEG_5prime",
                  "other", TBD},
    "study_type": {"in_vitro", "animal_invivo", "clinical"},
    "species": {"human", "monkey", "rat", "mouse", "multi_species", "NA"},
    "tissue": {"kidney", "proximal_tubule", "glomerulus", "NA"},
    "delivery_method": {"gymnotic_free_uptake", "transfection",
                        "conjugate_mediated", "systemic_dose", "intrathecal",
                        "intravitreal", "oral", TBD},
    "dose_or_conc_unit": {"uM", "nM", "ug/mL", "mg/kg", "mg", "fold_Cmax", "NA", TBD},
    "readout_category": {"functional", "injury_biomarker", "viability",
                         "accumulation", "histopathology", "clinical_renal_outcome"},
    "effect_direction": {"increase", "decrease", "no_change", TBD},
    "is_kidney_specific": {"TRUE", "FALSE"},
    # cc_by added from the CNS round: a CC-BY source permits reproducing raw
    # values with attribution, which is a materially stronger right than
    # summary_stat and is worth tracking rather than conservatively flattening.
    "redistribution": {"public_domain", "cc_by", "derived_features_only",
                       "summary_stat", "verify"},
}

# Readouts where a RISE is recovery, not injury. Without this the grade-0 check
# fires on rescued phenotypes and trains the curator to ignore its own warnings.
HIGHER_IS_BETTER = ("viability", "reabsorption", "uptake", "egfr", "clearance")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(path, expected_cols, label):
    if not os.path.exists(path):
        err(f"{label}: file missing at {path}")
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        err(f"{label}: no data rows")
        return []
    got = list(rows[0].keys())
    if got != expected_cols:
        missing = [c for c in expected_cols if c not in got]
        extra = [c for c in got if c not in expected_cols]
        err(f"{label}: column mismatch. missing={missing} extra={extra}")
    return rows


def check_enums(rows, label):
    for r in rows:
        rid = r.get("measurement_id") or r.get("oligo_id")
        for col, allowed in ENUMS.items():
            if col not in r:
                continue
            v = (r[col] or "").strip()
            if v and v not in allowed:
                err(f"{label} {rid}: {col}='{v}' not in controlled vocabulary")


def main():
    oligos = load(OLIGOS, OLIGO_COLS, "oligos")
    meas = load(MEAS, MEAS_COLS, "measurements")
    if not oligos or not meas:
        report()
        return

    # --- primary keys -----------------------------------------------------
    for rows, key, label in ((oligos, "oligo_id", "oligos"),
                             (meas, "measurement_id", "measurements")):
        dupes = [k for k, c in Counter(r[key] for r in rows).items() if c > 1]
        if dupes:
            err(f"{label}: duplicate {key}: {dupes[:5]}")

    # --- referential integrity -------------------------------------------
    known = {r["oligo_id"] for r in oligos}
    orphans = [m["measurement_id"] for m in meas if m["oligo_id"] not in known]
    if orphans:
        err(f"measurements: {len(orphans)} orphan oligo_id refs: {orphans[:5]}")
    unused = known - {m["oligo_id"] for m in meas}
    if unused:
        warn(f"oligos: {len(unused)} oligo(s) with no measurement: {sorted(unused)[:5]}")

    check_enums(oligos, "oligos")
    check_enums(meas, "measurements")

    # --- numeric / range / provenance -------------------------------------
    for m in meas:
        mid = m["measurement_id"]
        if m["nephrotox_grade"] not in {"0", "1", "2", "3"}:
            err(f"{mid}: nephrotox_grade='{m['nephrotox_grade']}' not in 0..3")
        d = m["dose_or_conc_value"]
        if d and d not in (TBD, "NA"):
            try:
                float(d)
            except ValueError:
                err(f"{mid}: dose_or_conc_value='{d}' is neither numeric, NA nor TBD")
        for col in ("source_id", "source_ref", "source_table"):
            if not (m[col] or "").strip() or m[col] == TBD:
                err(f"{mid}: provenance column {col} is empty/TBD")

    for o in oligos:
        for col in ("length_nt", "ps_count"):
            v = o[col]
            if v and v not in (TBD, "NA"):
                try:
                    int(v)
                except ValueError:
                    err(f"{o['oligo_id']}: {col}='{v}' is neither an integer nor TBD/NA")

    # --- endpoint policy ---------------------------------------------------
    for m in meas:
        mid = m["measurement_id"]
        rn = m["readout_name"].lower()
        if m["nephrotox_grade"] == "0" and m["effect_direction"] == "increase" \
                and m["readout_category"] in {"injury_biomarker", "histopathology"} \
                and not any(k in rn for k in HIGHER_IS_BETTER) \
                and not re.search(r"placebo|control|untreated|sham|vehicle",
                                  m["effect_vs_control"], re.I):
            warn(f"{mid}: grade 0 with an increase in an injury readout and no "
                 f"control comparison — verify grading")
        # "The source did not report toxicity" is not "the source measured it and
        # found none". Only the second is a negative control.
        if m["nephrotox_grade"] == "0" and m["readout_value"] == TBD \
                and m["effect_direction"] == TBD \
                and re.search(r"method", m["source_table"], re.I):
            err(f"{mid}: grade 0 with no value, no direction and a Methods-section "
                f"locus — this is silence, not a measured negative")

    # --- sequence sanity --------------------------------------------------
    seq_re = re.compile(r"^[ACGTUacgtu]+$")
    filled = 0
    for o in oligos:
        s = (o["sequence_5to3"] or "").strip()
        if not s or s == TBD:
            continue
        filled += 1
        if not seq_re.match(s):
            err(f"{o['oligo_id']}: sequence_5to3 contains non-IUPAC characters")
            continue
        ln = o["length_nt"]
        if ln and ln not in (TBD, "NA"):
            try:
                if int(ln) != len(s):
                    warn(f"{o['oligo_id']}: length_nt={ln} but sequence is {len(s)} nt "
                         f"(check for 3'-caps/overhangs; explain in notes)")
            except ValueError:
                pass

    # --- unverified provenance census -------------------------------------
    ws = [m for m in meas if m["source_id"] == "WS"]
    if ws:
        warn(f"{len(ws)} row(s) carry source_id=WS (derived from search summaries, "
             f"not full text). METHODOLOGY.md commits to verifying these against "
             f"their cited primary source before release.")

    # --- summary ----------------------------------------------------------
    print(f"oligos.csv        : {len(oligos)} oligos")
    print(f"measurements.csv  : {len(meas)} measurements")
    print(f"sequences filled  : {filled}/{len(oligos)}")
    print("grade distribution: " + " ".join(
        f"{g}:{sum(1 for m in meas if m['nephrotox_grade'] == g)}" for g in "0123"))
    print("study types       : " + " ".join(
        f"{k}:{v}" for k, v in Counter(m["study_type"] for m in meas).most_common()))
    print("rights            : " + " ".join(
        f"{k}:{v}" for k, v in Counter(m["redistribution"] for m in meas).most_common()))
    report()


def report():
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
