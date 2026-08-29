#!/usr/bin/env python3
"""
Curated NONCLINICAL (animal) rows for OligoTox-Hydrocephalus.

These close two gaps the first release recorded as open items: the dataset was
entirely human (OI-03), and it was entirely toxicity-direction, with the
`therapeutic_ventricular_effect` axis declared and used by no row (OI-04).

Both sources are rodent studies in which a defined siRNA changes a ventricular
outcome, in opposite directions:

  N1  A SPAK-targeting siRNA delivered in a lipid nanoparticle PREVENTS
      ventriculomegaly in a kaolin-induced hydrocephalus model. Protective.
  N2  An AQP4-targeting siRNA AGGRAVATES ventriculomegaly in an intraventricular-
      haemorrhage model, against a designed negative-control siRNA. Toxic
      direction, and the first DESIGNED control in the dataset — every other
      negative here is a comparator arm or a reported zero, not a compound built
      to be inactive.

N1 also supplies the dataset's first published sequences. All four SPAK duplexes
are printed in the source's Materials section and each passes the reverse-
complement check between its sense and antisense strands (19-mer cores, TT
overhangs trimmed) — a test that depends on no source being correct and so
catches a plausible-but-wrong transcription that two agreeing documents would
not. The check is re-run by qc/validate.py.

No number is read off a figure. Both sources publish their ventricular
measurements graphically, so `readout_value` is NOT_REPORTED and
`readout_is_qualitative` is TRUE throughout.

Output: data/_nonclinical_measurements.csv
Usage:  python3 scripts/build_nonclinical.py
"""
import csv
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
TODAY = date.today().isoformat()

N1 = dict(
    source_key="Choroid_plexus_siSPAK_LNP_2025_NatCommun",
    source_ref="PMID 40640139; PMC12246246; doi 10.1038/s41467-025-61543-1",
    file="sources/raw/sweep6_PMC12246246_fulltext.xml",
    system=("Kaolin-induced hydrocephalus, male mice; T7-peptide-modified lipid "
            "nanoparticle co-delivering SPAK siRNA and resveratrol, dosed by tail "
            "vein every 24 h from 24 h before intraventricular kaolin until 48 h after"),
    redistribution="summary_stat_only",
)

N2 = dict(
    source_key="AQP4_siRNA_hydrocephalus_2018_MedSciMonit",
    source_ref="PMID 29921834; PMC6042309; doi 10.12659/MSM.907186",
    file="sources/raw/sweep6_PMC6042309_fulltext.xml",
    system=("Intraventricular-haemorrhage hydrocephalus model, rats, autologous "
            "blood injection; AQP4-specific siRNA against a negative-control siRNA; "
            "MRI and haematoxylin-eosin staining on days 1 and 3"),
    redistribution="cc_by_nc",
)

ROWS = [
    dict(src=N1, oligo="SPAK_siRNA4", tier="A", cat="ventricular_morphometry",
         axis="therapeutic_ventricular_effect", route="intravenous",
         readout="ventriculomegaly_prevention", direction="decrease",
         grade="", status="not_graded",
         basis=("NOT GRADED. The measured ventricular effect is PROTECTIVE, and the "
                "0-3 rubric grades severity of harm. Grading a prevented lesion on a "
                "toxicity scale would make a beneficial effect look like an absent "
                "one. tox_axis = therapeutic_ventricular_effect marks the row for "
                "exclusion from any compound-toxicity analysis."),
         asc="measured_positive", attribution="drug_attributed",
         evidence=('"As expected, siR/RSV@TNP fulfilled its function of knocking down '
                   'SPAK expression, relieving inflammation and oxidative stress, '
                   'retrieving blood-CSF barrier integrity, and ultimately preventing '
                   'ventriculomegaly and hydrocephalus in male mice."'),
         loc="Discussion, concluding paragraph; ventricular data published as figures",
         comparator="kaolin-induced hydrocephalus model, untreated and vehicle groups"),
    dict(src=N1, oligo="SPAK_siRNA4", tier="B", cat="csf_dynamics",
         axis="therapeutic_ventricular_effect", route="intravenous",
         readout="CSF_overproduction_reduction", direction="decrease",
         grade="", status="not_graded",
         basis=("NOT GRADED. Protective direction; see the sibling row's basis."),
         asc="measured_positive", attribution="drug_attributed",
         evidence=('"SPAK siRNA restores blood-CSF barrier integrity, reduces CSF '
                   'overproduction, and prevents ..."'),
         loc="Results, blood-CSF barrier section; values published as figures",
         comparator="kaolin-induced hydrocephalus model, untreated and vehicle groups"),
    dict(src=N2, oligo="AQP4_siRNA", tier="A", cat="ventricular_morphometry",
         axis="ventricular_enlargement", route="intracerebroventricular",
         readout="lateral_ventricle_volume", direction="increase",
         grade=2, status="provisional",
         basis=("2 = ventriculomegaly aggravated with accompanying structural injury "
                "(disorganised ependymal layer, impaired blood-brain barrier), in an "
                "animal model with no CSF diversion available "
                "(SCHEMA.md rubric grade 2). Grade 3 is reserved for a permanent "
                "diversion or a fatal/disabling outcome, neither of which is reported."),
         asc="measured_positive", attribution="drug_attributed",
         evidence=('"When AQP4 was silenced, the hydrocephalus was aggravated, and the '
                   'lateral ventricle volumes were increased significantly compared '
                   'with the negative control of siRNA group (Figure 6A, 6B)." '
                   'Conclusions: "silencing AQP4 aggravates hydrocephalus, indicating '
                   'that AQP4 protects against hydrocephalus."'),
         loc="Results, section 'AQP4 siRNA aggravated hydrocephalus'; Figure 6A,6B",
         comparator="negative control siRNA group"),
    dict(src=N2, oligo="AQP4_siRNA", tier="B",
         cat="histopathology_choroid_ependyma", axis="ventricular_enlargement",
         route="intracerebroventricular", readout="ependymal_layer_integrity",
         direction="increase", grade=2, status="provisional",
         basis=("2 = structural injury to the ependymal lining accompanying the "
                "ventricular change (SCHEMA.md rubric grade 2)."),
         asc="measured_positive", attribution="drug_attributed",
         evidence=('"the disorganized ependymal layer induced by hydrocephalus was '
                   'aggravated by AQP4 silencing (Figure 6C)."'),
         loc="Results, Figure 6C (haematoxylin-eosin staining)",
         comparator="negative control siRNA group"),
    dict(src=N2, oligo="negative_control_siRNA", tier="A",
         cat="ventricular_morphometry", axis="ventricular_enlargement",
         route="intracerebroventricular", readout="lateral_ventricle_volume",
         direction="no_change", grade=0, status="provisional",
         basis=("0 = the designed negative-control siRNA is the arm against which the "
                "AQP4 siRNA's ventricular enlargement is measured; the source reports "
                "no ventricular effect attributable to it beyond the haemorrhage model "
                "itself (SCHEMA.md rubric grade 0)."),
         asc="measured_null", attribution="not_discussed",
         evidence=("The source uses this compound as its comparator throughout, "
                   "reporting AQP4-siRNA effects 'compared with the negative control of "
                   "siRNA group'. It is a scrambled/non-targeting siRNA included by the "
                   "authors to control for siRNA delivery per se."),
         loc="Results, section 'AQP4 siRNA aggravated hydrocephalus'; Figure 6A,6B",
         comparator="AQP4 siRNA group"),
]


def main():
    rows = []
    for r in ROWS:
        src = r["src"]
        rows.append(dict(
            oligo_name=r["oligo"], source_key=src["source_key"],
            study_type="animal_invivo",
            species=("mouse" if src is N1 else "rat"),
            strain="NOT_REPORTED", system_model=src["system"],
            is_human_system="FALSE",
            indication_population=("kaolin-induced hydrocephalus model" if src is N1
                                   else "intraventricular-haemorrhage hydrocephalus model"),
            arm_label=r["oligo"], arm_description=src["system"][:200],
            arm_role=("comparator" if r["oligo"] == "negative_control_siRNA"
                      else "exposed"),
            cns_compartment="lateral_ventricles", delivery_route=r["route"],
            dose_value="NOT_REPORTED", dose_unit="NOT_APPLICABLE",
            dose_regimen=("every 24 h by tail vein, from 24 h before to 48 h after "
                          "kaolin" if src is N1 else "NOT_REPORTED"),
            exposure_duration="NOT_REPORTED",
            timepoint=("NOT_REPORTED" if src is N1 else "days 1 and 3 after injection"),
            endpoint_tier=r["tier"], readout_category=r["cat"],
            readout_name=r["readout"], readout_term_verbatim="NOT_APPLICABLE",
            readout_value="NOT_REPORTED", readout_unit="NOT_APPLICABLE",
            readout_is_qualitative="TRUE",
            n_affected="NOT_REPORTED", n_at_risk="NOT_REPORTED",
            comparator_arm=r["comparator"], n_affected_comparator="NOT_REPORTED",
            n_at_risk_comparator="NOT_REPORTED",
            statistic=("significance stated by the source; the value is published only "
                       "as a figure and no number was read off it"),
            effect_direction=r["direction"],
            effect_vs_control=("stated in words by the source; see "
                               "attribution_evidence"),
            seriousness="NOT_APPLICABLE", assessment_type="investigator_assessment",
            organ_system="Nervous system disorders",
            source_vocabulary="NOT_APPLICABLE",
            hydroceph_grade=r["grade"], grade_basis=r["basis"],
            grade_status=r["status"], ascertainment=r["asc"],
            ascertainment_basis=("Protocol-driven: the study's purpose was to measure "
                                 "the ventricular consequence of knocking down this "
                                 "target, so the ventricles were imaged by MRI in every "
                                 "animal. Values are published as figures only."),
            attribution_as_stated=r["attribution"],
            attribution_evidence=r["evidence"], tox_axis=r["axis"],
            event_cluster_id=("N1-SPAK" if src is N1 else "N2-AQP4"),
            source_ref=src["source_ref"], source_location=r["loc"],
            redistribution=src["redistribution"],
            notes=("Nonclinical rodent row. Full text committed at %s. Values are "
                   "qualitative because the source publishes them graphically and this "
                   "project reads no number off a figure. Retrieved %s."
                   % (src["file"], TODAY)),
        ))

    out = os.path.join(DATA, "_nonclinical_measurements.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote %s: %d rows" % (out, len(rows)))
    for r in rows:
        print("  %-22s tier %s  %-32s %s  axis=%s" % (
            r["oligo_name"], r["endpoint_tier"], r["readout_name"],
            r["effect_direction"], r["tox_axis"]))


if __name__ == "__main__":
    main()
