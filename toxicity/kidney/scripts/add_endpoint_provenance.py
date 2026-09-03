#!/usr/bin/env python3
"""Add `renal_endpoints_measured` -- the field that stops grade 0 meaning two things.

CLINICAL_VALIDATION.md established that a nephrotoxicity grade of 0 in this dataset
conflates two situations that are not the same evidence:

    (a) renal endpoints were measured and were unremarkable   -> a real negative
    (b) renal endpoints were never measured, or the cited source does not report
        them                                                  -> not a negative at all

Direct retrieval of 7 unverified absence claims found only one in category (a). The
provenance/outcome confound (0 of 20 search-derived clinical rows reach grade >=2,
against 11 of 22 anchor-sourced) is what that conflation looks like in aggregate.
This field separates them so a model can exclude, weight or impute the (b) rows
instead of training on them as though they were measured negatives.

Values:
    measured_and_reported     the endpoint was assayed and a result is reported
    not_measured              the study did not assess renal endpoints at all
    not_reported_in_source    assessed or not, the cited source does not report it
    cannot_determine          not yet verified against the primary source

ASSIGNMENT RULES (deterministic, so the field can be re-derived, not hand-curated):

 1. Any in-vitro or animal in-vivo row -> measured_and_reported. These rows exist
    because an assay was run and read; the measurement IS the row.
 2. Any clinical row reporting a positive finding (grade >= 1, or a numeric
    readout_value) -> measured_and_reported. A finding cannot be reported without
    having been measured.
 3. Clinical grade-0 rows carry the verdict from the direct source retrievals
    recorded in CLINICAL_VALIDATION.md, where one exists.
 4. Every remaining clinical grade-0 row -> cannot_determine. These are the
    unverified absence claims; the honest value is "not checked", not "negative".

Usage:  python scripts/add_endpoint_provenance.py && python scripts/build_merged.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "data", "measurements.csv")

# rule 3 -- verdicts from the direct retrievals in CLINICAL_VALIDATION.md §2 and §5
VERIFIED = {
    "MSR066": ("measured_and_reported", "eGFR measured, wk32 -2.9 vs placebo -6.3 mL/min/1.73m2"),
    "MSR045": ("measured_and_reported", "eGFR reported but as efficacy/eligibility stratification not safety"),
    "MSR063": ("not_measured", "no renal endpoint; trial excluded eGFR<60 and UACR>100mg/g"),
    "MSR078": ("not_measured", "safety assessments were TEAEs FEV1 DLCO only; renal dysfunction excluded"),
    "MSR042": ("not_measured", "label has no renal endpoint and no renal impairment subsection"),
    "MSR044": ("not_reported_in_source", "Onpattro label AE table carries no renal endpoint"),
    "MSR047": ("not_reported_in_source", "Amvuttra label AE table carries no renal endpoint"),
    "MSR160": ("measured_and_reported", "label mandates cystatin C/UPCR/dipstick then reports negative"),
    "MSR162": ("measured_and_reported", "label mandates cystatin C/UPCR/dipstick then reports negative"),
    "MSR164": ("measured_and_reported", "label mandates cystatin C/UPCR/dipstick then reports negative"),
}


def numeric(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def main():
    with open(MEAS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = list(reader.fieldnames), list(reader)

    if "renal_endpoints_measured" not in fields:
        fields.insert(fields.index("nephrotox_grade"), "renal_endpoints_measured")

    counts = {}
    for r in rows:
        mid = r["measurement_id"]
        if r["study_type"] != "clinical":                        # rule 1
            val, why = "measured_and_reported", "assay_readout_is_the_measurement"
        elif mid in VERIFIED:                                    # rule 3 (before rule 2)
            val, why = VERIFIED[mid]
        elif r["nephrotox_grade"] != "0" or numeric(r["readout_value"]):   # rule 2
            val, why = "measured_and_reported", "positive_or_quantitative_finding_implies_measurement"
        else:                                                    # rule 4
            val, why = "cannot_determine", "unverified_absence_claim_not_checked_against_primary_source"
        r["renal_endpoints_measured"] = val
        tag = f"renal_endpoints_{val}:{why}"
        if tag not in r["notes"]:
            r["notes"] = f"{r['notes']};{tag}" if r["notes"].strip() else tag
        counts[val] = counts.get(val, 0) + 1

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print("renal_endpoints_measured assigned:")
    for k in ("measured_and_reported", "not_measured", "not_reported_in_source", "cannot_determine"):
        print(f"  {k:<24}{counts.get(k, 0):>4}")
    clin = [r for r in rows if r["study_type"] == "clinical"]
    print(f"\nclinical rows only ({len(clin)}):")
    cc = {}
    for r in clin:
        cc[r["renal_endpoints_measured"]] = cc.get(r["renal_endpoints_measured"], 0) + 1
    for k, v in sorted(cc.items()):
        print(f"  {k:<24}{v:>4}")
    unsafe = [r["measurement_id"] for r in clin
              if r["nephrotox_grade"] == "0" and r["renal_endpoints_measured"] != "measured_and_reported"]
    print(f"\ngrade-0 clinical rows NOT supported as measured negatives: {len(unsafe)}")
    print("  " + " ".join(unsafe))


if __name__ == "__main__":
    main()
