#!/usr/bin/env python3
"""Add human-clinical and animal rows for the three approved DMD PMOs.

golodirsen (OLG011), casimersen (OLG012) and viltolarsen (OLG013) are approved
drugs that carried NO measurement rows at all. Their labels were read directly on
DailyMed (accessdata.fda.gov is unreachable from this environment) and all three
share the same structure: a Warnings and Precautions "Kidney Toxicity" subsection
stating that kidney toxicity was seen in ANIMALS, was NOT seen in the human
studies, and that renal function must nonetheless be monitored.

Why these human rows are worth having, when the dataset already has too many
unsupported grade-0s: this is the *measured* kind of negative. The labels mandate
specific analytes -- "Serum cystatin C, urine dipstick, and urine
protein-to-creatinine ratio should be measured before starting ... During
treatment, monitor urine dipstick every month, and serum cystatin C and urine
protein-to-creatinine ratio every three months" -- and then state affirmatively
that "kidney toxicity was not observed in the clinical studies". Endpoints were
prescribed and the result was negative, which is exactly the distinction
CLINICAL_VALIDATION.md found missing from the existing WS grade-0 rows.

One methodological point these labels make explicitly, and which matters for every
DMD row in the dataset (drisapersen, eteplirsen, golodirsen, casimersen,
viltolarsen): "because of the effect of reduced skeletal muscle mass on creatinine
measurements, creatinine may not be a reliable measure of kidney function in DMD
patients". Serum-creatinine-based renal readouts in DMD populations should be read
with that caveat, which is why these rows record cystatin C / UPCR / dipstick as
the monitored analytes rather than creatinine.

The animal rows record the labels' nonclinical statements. They are label-level
summaries, not primary study data -- dose and duration stay TBD and the notes say
so -- but they are citable, and they make all three compounds human/animal bridge
compounds.

Usage:  python scripts/add_dmd_pmo_label_rows.py && python scripts/split_human_animal.py \
        && python scripts/build_merged.py
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "data", "measurements.csv")

MONITORED = "cystatin_C;urine_dipstick;UPCR"
CAVEAT = ("serum_creatinine_unreliable_in_DMD_reduced_muscle_mass_per_label;"
          "monitored_analytes_" + MONITORED)

DRUGS = [
    dict(oid="OLG011", drug="golodirsen", src="A11", section="5.2",
         setid="35c227d1-5b24-44b0-b5d3-f0f6b1c46bd5", brand="Vyondys53",
         animal_species="multi_species",
         animal_note="juvenile_rat_dose_dependent_renal_tubular_effects;mouse_and_rat_kidney_toxicity;"
                     "primate_microscopic_renal_changes"),
    dict(oid="OLG012", drug="casimersen", src="A12", section="5.2",
         setid="e9e5fd44-eeda-4580-bba1-a734828bbcc3", brand="Amondys45",
         animal_species="multi_species",
         animal_note="juvenile_rat_and_mouse_renal_tubular_degeneration_necrosis"),
    dict(oid="OLG013", drug="viltolarsen", src="A13", section="5.1",
         setid="1ffff9a8-6d6a-4dcb-8493-1b6cc3a5d123", brand="Viltepso",
         animal_species="multi_species",
         animal_note="kidney_toxicity_observed_in_animals_label_summary_see_section_8.4"),
]


def main():
    with open(MEAS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = reader.fieldnames, list(reader)
    if any(r["source_id"] in {d["src"] for d in DRUGS} for r in rows):
        print("DMD PMO label rows already present - nothing to do")
        return

    n = max(int(re.sub(r"\D", "", r["measurement_id"])) for r in rows)
    new = []
    for d in DRUGS:
        ref = f"DailyMed_SPL_{d['setid']};{d['brand']}_label"
        base = {c: "" for c in fields}
        base.update(is_kidney_specific="TRUE", tissue="kidney", oligo_id=d["oid"],
                    source_id=d["src"], source_ref=ref, redistribution="public_domain")

        n += 1
        human = dict(base)
        human.update({
            "measurement_id": f"MSR{n}", "study_type": "clinical", "species": "human",
            "subject_class": "human_clinical", "system_model": "DMD_patients",
            "delivery_method": "systemic_dose",
            "dose_or_conc_value": "TBD", "dose_or_conc_unit": "mg/kg",
            "exposure_duration": "TBD",
            "readout_category": "clinical_renal_outcome",
            "readout_name": "kidney_toxicity_monitored",
            "readout_value": "not_observed", "readout_unit": "NA",
            "effect_direction": "no_change", "effect_vs_control": "TBD",
            "nephrotox_grade": "0",
            "source_table": f"Section {d['section']} Warnings and Precautions - Kidney Toxicity",
            "notes": ("renal_endpoints_PRESCRIBED_and_monitored_then_reported_negative;"
                      "label_states_kidney_toxicity_not_observed_in_clinical_studies;"
                      f"{CAVEAT};measured_negative_not_absence_of_reporting;grade_provisional"),
        })
        new.append(human)

        n += 1
        animal = dict(base)
        animal.update({
            "measurement_id": f"MSR{n}", "study_type": "animal_invivo",
            "species": d["animal_species"], "subject_class": "animal_invivo",
            "system_model": "nonclinical_label_summary",
            "delivery_method": "systemic_dose",
            "dose_or_conc_value": "TBD", "dose_or_conc_unit": "mg/kg",
            "exposure_duration": "TBD",
            "readout_category": "histopathology",
            "readout_name": "renal_tubular_toxicity",
            "readout_value": "observed", "readout_unit": "NA",
            "effect_direction": "increase", "effect_vs_control": "TBD",
            "nephrotox_grade": "2",
            "source_table": f"Section {d['section']} Warnings and Precautions - Kidney Toxicity",
            "notes": (f"{d['animal_note']};label_level_nonclinical_summary_not_primary_study_data;"
                      "dose_and_duration_not_given_in_label;grade_provisional"),
        })
        new.append(animal)

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows + new)
    print(f"added {len(new)} rows ({new[0]['measurement_id']}..{new[-1]['measurement_id']})")
    for r in new:
        print(f"  {r['measurement_id']:<8}{r['oligo_id']:<8}{r['subject_class']:<16}"
              f"{r['readout_name']:<26}{r['readout_value']:<14}g{r['nephrotox_grade']}")


if __name__ == "__main__":
    main()
