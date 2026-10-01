#!/usr/bin/env python3
"""Gate which grade-0 rows may be used as negatives, without overwriting source data.

Beebop's Priority 2 makes a point I had missed. I added `renal_endpoints_measured`
to flag unsupported negatives, but the numeric `nephrotox_grade` stayed 0 on those
rows -- so a model reading the grade column picks them up as negatives regardless
of the flag. A warning column does not gate anything.

Beebop also challenged my 29 `measured_and_reported` rows. Auditing them narrows
the issue usefully: 21 of the 29 are POSITIVE findings (grade >= 1), where
"measured" is trivially true. Only 8 assert a negative, and two of my own
classifications there do not survive scrutiny:

  * MSR045 lumasiran -- I recorded in CLINICAL_VALIDATION.md that eGFR appears as
    efficacy / eligibility stratification rather than a safety assessment, then
    classified the row `measured_and_reported` anyway. That is inconsistent with
    my own finding.
  * MSR160/162/164 (DMD PMO labels) -- I reasoned that mandated monitoring implies
    the endpoint was measured. It does not: monitoring guidance is forward-looking
    advice to prescribers. The labels do assert "kidney toxicity was not observed
    in the clinical studies", which is a statement about study findings, but there
    is no reported endpoint table behind it. Stronger than silence, weaker than a
    measured result -- it needs its own class rather than being promoted.

So negative eligibility is graded, and the strongest tier additionally requires
that the primary study source was actually read (from the study register):

  confirmed_negative            safety endpoint measured, quantitative result
                                reported, primary source read
  asserted_negative_regulatory  a label asserts no finding in the studies, with no
                                endpoint table behind it
  efficacy_derived_negative     renal endpoint reported, but for efficacy or
                                eligibility rather than safety
  not_eligible_negative         not_measured / not_reported_in_source /
                                cannot_determine
  positive_finding              grade >= 1; not a negative, eligibility n/a

Source assertions are preserved. `nephrotox_grade` is untouched. Two derived
columns are added:

  negative_eligibility       the class above, with the reason in `notes`
  nephrotox_grade_modeling   equals nephrotox_grade EXCEPT it is blank on rows
                             whose negative is not confirmed -- so a modeller
                             using this column cannot silently train on an
                             unsupported zero. Missing, not zero.

Every regrade here is a curation proposal for German's scientific review, not a
settled scientific judgement.

Usage:  python scripts/add_negative_eligibility.py && python scripts/build_merged.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "data", "measurements.csv")
REG = os.path.join(ROOT, "data", "clinical_study_register.csv")

# explicit downgrades, with the reason recorded per row
DOWNGRADE = {
    "MSR045": ("efficacy_derived_negative",
               "eGFR reported as efficacy/eligibility stratification not safety assessment; "
               "AE table lists only injection-site reaction and abdominal pain"),
    "MSR160": ("asserted_negative_regulatory",
               "label asserts not observed in clinical studies; monitoring guidance is "
               "prescriber advice not evidence of assessment; no endpoint table"),
    "MSR162": ("asserted_negative_regulatory",
               "label asserts not observed in clinical studies; monitoring guidance is "
               "prescriber advice not evidence of assessment; no endpoint table"),
    "MSR164": ("asserted_negative_regulatory",
               "label asserts not observed in clinical studies; monitoring guidance is "
               "prescriber advice not evidence of assessment; no endpoint table"),
    "MSR016": ("asserted_negative_regulatory",
               "label section 6 absence statement; no reported renal endpoint table"),
}


def main():
    read_studies = set()
    if os.path.exists(REG):
        for r in csv.DictReader(open(REG, newline="")):
            if r["primary_source_read"] == "TRUE":
                read_studies.add(r["measurement_id"])

    with open(MEAS, newline="") as fh:
        rd = csv.DictReader(fh)
        fields, rows = list(rd.fieldnames), list(rd)
    for col in ("negative_eligibility", "nephrotox_grade_modeling"):
        if col not in fields:
            fields.insert(fields.index("nephrotox_grade") + 1, col)

    counts, gated = {}, []
    for r in rows:
        grade = r["nephrotox_grade"]
        mid = r["measurement_id"]
        prov = r["renal_endpoints_measured"]

        if grade != "0":
            cls, why = "positive_finding", "grade>=1; not a negative"
        elif r["study_type"] != "clinical":
            # assay rows: the experiment measured the endpoint by construction
            cls, why = "confirmed_negative", "in-vitro/in-vivo assay readout at tested exposure"
        elif prov != "measured_and_reported":
            cls, why = "not_eligible_negative", f"ascertainment is {prov}"
        elif mid in DOWNGRADE:
            cls, why = DOWNGRADE[mid]
        elif mid not in read_studies:
            cls, why = ("asserted_negative_regulatory",
                        "reported negative but primary study source not yet read in this project")
        else:
            cls, why = "confirmed_negative", "safety endpoint measured and reported; primary source read"

        r["negative_eligibility"] = cls
        eligible = cls in ("positive_finding", "confirmed_negative")
        r["nephrotox_grade_modeling"] = grade if eligible else ""
        if not eligible:
            gated.append(mid)
        tag = f"negative_eligibility_{cls}:{why}"
        if tag not in r["notes"]:
            r["notes"] = f"{r['notes']};{tag}" if r["notes"].strip() else tag
        counts[cls] = counts.get(cls, 0) + 1

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print("negative_eligibility assigned:")
    for k in ("positive_finding", "confirmed_negative", "asserted_negative_regulatory",
              "efficacy_derived_negative", "not_eligible_negative"):
        print(f"  {k:<32}{counts.get(k, 0):>4}")
    print(f"\nrows with nephrotox_grade_modeling BLANK (cannot train as negatives): {len(gated)}")
    clin = [r for r in rows if r["study_type"] == "clinical"]
    cg = [r for r in clin if r["nephrotox_grade"] == "0"]
    conf = [r for r in cg if r["negative_eligibility"] == "confirmed_negative"]
    print(f"clinical grade-0 rows: {len(cg)}; of those CONFIRMED negatives: {len(conf)}"
          f" -> {[r['measurement_id'] for r in conf]}")


if __name__ == "__main__":
    main()
