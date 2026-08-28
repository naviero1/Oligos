#!/usr/bin/env python3
"""Quality-control validator for the OligoTox-Thrombocytopenia dataset.

Runs the checks documented in thrombocytopenia/METHODOLOGY.md §Quality control:
  - schema conformance   (column set + controlled-vocabulary enums)
  - referential integrity (measurements.oligo_id -> oligos.oligo_id, no orphans)
  - primary-key uniqueness
  - range checks         (thrombocytopenia_grade in 0..3, booleans TRUE/FALSE)
  - provenance completeness (every row has source_id + source_ref + source_table)
  - sequence policy      (only A/C/G/T/U characters, case-insensitive, or TBD)

Exits non-zero if any hard check fails, so it can gate a commit.

Usage:  python3 scripts/qc_thrombo.py
"""
import csv, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "thrombocytopenia", "data")

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt",
              "backbone_chemistry", "sugar_modifications", "gapmer_design",
              "conjugate", "ps_count", "sequence_5to3", "design_source", "notes"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "tissue", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "readout_category", "readout_name", "readout_value",
             "readout_unit", "effect_direction", "effect_vs_control",
             "thrombocytopenia_grade", "is_platelet_specific", "source_id",
             "source_ref", "source_table", "redistribution", "notes"]

ENUMS = {
    "oligo_class": {"ASO_gapmer", "siRNA", "GalNAc_siRNA", "splice_switching_ASO",
                    "PMO", "aptamer", "other"},
    "backbone_chemistry": {"full_PS", "PS_PO_mix", "full_PO", "PMO_neutral", "mixed", "TBD"},
    "conjugate": {"none", "GalNAc", "lipid", "peptide", "PEG", "other", "TBD"},
    "max_phase": {"approved", "approved_EMA", "phase_3", "phase_3_discontinued",
                  "phase_2", "phase_2_discontinued", "phase_1", "preclinical",
                  "research_panel", "class_review", "TBD"},
    "study_type": {"in_vitro", "ex_vivo", "animal_invivo", "clinical"},
    "species": {"human", "monkey", "rat", "mouse", "dog", "multi_species", "NA", "TBD"},
    "delivery_method": {"direct_addition", "gymnotic_free_uptake", "transfection",
                        "conjugate_mediated", "systemic_dose", "intrathecal",
                        "intravitreal", "oral", "subcutaneous", "TBD"},
    "dose_or_conc_unit": {"uM", "nM", "ug/mL", "mg/kg", "mg", "fold_Cmax", "NA", "TBD"},
    "readout_category": {"platelet_count", "platelet_activation", "platelet_aggregation",
                         "platelet_binding", "megakaryocyte", "immunogenicity",
                         "clinical_outcome", "histopathology", "viability", "coagulation"},
    "effect_direction": {"increase", "decrease", "no_change", "TBD"},
    "is_platelet_specific": {"TRUE", "FALSE"},
    "redistribution": {"public_domain", "cc_by", "derived_features_only",
                       "summary_stat", "verify"},
}

SEQ_RE = re.compile(r"^[ACGTUacgtu]+$")


def load(name):
    path = os.path.join(BASE, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f)), path


def main():
    errors, warnings = [], []
    oligos, opath = load("oligos.csv")
    meas, mpath = load("measurements.csv")

    # --- column-set conformance -------------------------------------------------
    if oligos and list(oligos[0].keys()) != OLIGO_COLS:
        errors.append(f"oligos.csv column set mismatch:\n  got {list(oligos[0].keys())}")
    if meas and list(meas[0].keys()) != MEAS_COLS:
        errors.append(f"measurements.csv column set mismatch:\n  got {list(meas[0].keys())}")

    # --- primary-key uniqueness -------------------------------------------------
    for rows, key, label in ((oligos, "oligo_id", "oligos"), (meas, "measurement_id", "measurements")):
        dupes = [k for k, c in collections.Counter(r[key] for r in rows).items() if c > 1]
        if dupes:
            errors.append(f"{label}: duplicate {key}: {dupes[:5]}")

    # --- referential integrity --------------------------------------------------
    known = {o["oligo_id"] for o in oligos}
    orphans = [m["measurement_id"] for m in meas if m["oligo_id"] not in known]
    if orphans:
        errors.append(f"measurements: {len(orphans)} orphan oligo_id refs: {orphans[:5]}")
    used = {m["oligo_id"] for m in meas}
    unused = sorted(known - used)
    if unused:
        warnings.append(f"oligos with no measurement rows: {len(unused)} ({unused[:5]})")

    # --- controlled vocabularies ------------------------------------------------
    for rows, label in ((oligos, "oligos"), (meas, "measurements")):
        for r in rows:
            pk = r.get("oligo_id") or r.get("measurement_id")
            for col, allowed in ENUMS.items():
                if col in r and r[col] and r[col] not in allowed:
                    errors.append(f"{label} {pk}: {col}={r[col]!r} not in controlled vocabulary")

    # --- range checks -----------------------------------------------------------
    for m in meas:
        g = m.get("thrombocytopenia_grade", "")
        if g not in {"0", "1", "2", "3"}:
            errors.append(f"measurements {m['measurement_id']}: grade={g!r} outside 0-3")

    # --- provenance completeness ------------------------------------------------
    for m in meas:
        for col in ("source_id", "source_ref", "source_table"):
            if not m.get(col) or m[col] in {"", "TBD", "NA"}:
                errors.append(f"measurements {m['measurement_id']}: missing provenance {col}")

    # --- provenance STRENGTH (not a failure, but must stay visible) -------------
    # A row citing a paywalled paper's abstract is legitimately sourced — an
    # abstract is a specific, retrievable locus — but it is weaker evidence than a
    # numbered table and must be re-verified against full text before release.
    # Surfacing the count here stops that caveat from being buried in a notes field.
    abstract_only = [m["measurement_id"] for m in meas
                     if "abstract" in (m.get("source_table") or "").lower()]
    if abstract_only:
        warnings.append(
            f"{len(abstract_only)} row(s) cite an abstract rather than a numbered "
            f"table/figure (paywalled full text) — verify before release: "
            f"{abstract_only[:5]}")

    # --- CONTROL-ARM rows carrying a non-zero grade ----------------------------
    # These are correctly graded: the rubric grades the OBSERVED band regardless of
    # study arm, and a placebo subject whose platelets genuinely fell below 75 K/uL
    # did have that event. But a model joining grade to DESIGN FEATURES would read
    # them as the compound causing an effect at zero dose. The canonical filter is
    # `dose_or_conc_value == "0"`; surfacing the count here keeps the hazard visible
    # instead of buried in prose.
    ctrl_nonzero = [m["measurement_id"] for m in meas
                    if str(m.get("dose_or_conc_value", "")).strip() in {"0", "0.0"}
                    and m.get("thrombocytopenia_grade") not in {"0", ""}]
    if ctrl_nonzero:
        warnings.append(
            f"{len(ctrl_nonzero)} CONTROL-ARM row(s) (dose 0) carry grade > 0 — correct "
            f"per the rubric, but MODELS MUST EXCLUDE dose_or_conc_value=='0' before "
            f"joining grade to design features: {ctrl_nonzero[:5]}")

    # --- sequence policy (case-insensitive; case encodes chemistry) -------------
    for o in oligos:
        s = o.get("sequence_5to3", "")
        if s and s != "TBD" and not SEQ_RE.match(s):
            errors.append(f"oligos {o['oligo_id']}: sequence_5to3 has non-ACGTU chars: {s!r}")
        if s and s != "TBD" and o.get("length_nt", "TBD") not in ("TBD", "", str(len(s))):
            warnings.append(
                f"oligos {o['oligo_id']}: length_nt={o['length_nt']} != len(sequence)={len(s)}")

    # --- report -----------------------------------------------------------------
    print(f"oligos.csv        {len(oligos):>4} rows x {len(OLIGO_COLS)} cols   {opath}")
    print(f"measurements.csv  {len(meas):>4} rows x {len(MEAS_COLS)} cols   {mpath}")
    if meas:
        gd = collections.Counter(m["thrombocytopenia_grade"] for m in meas)
        print("grade distribution 0/1/2/3 :",
              " / ".join(str(gd.get(str(i), 0)) for i in range(4)))
        print("study types                :",
              dict(collections.Counter(m["study_type"] for m in meas)))
        print("platelet-specific TRUE     :",
              sum(1 for m in meas if m["is_platelet_specific"] == "TRUE"), "/", len(meas))
        print("distinct sources           :",
              len({m["source_ref"] for m in meas}))
    if oligos:
        withseq = sum(1 for o in oligos if o["sequence_5to3"] not in ("", "TBD"))
        print(f"sequences filled           : {withseq} / {len(oligos)}")
        print("oligo classes              :",
              dict(collections.Counter(o["oligo_class"] for o in oligos)))

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")

    if errors:
        print(f"\nQC FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"\nQC PASSED ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
