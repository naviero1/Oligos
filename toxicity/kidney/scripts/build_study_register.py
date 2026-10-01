#!/usr/bin/env python3
"""Build the clinical study register: what the 42 clinical rows actually rest on.

Oscar's requirement is that a headline human total counts **verified, deduplicated
human clinical trials** -- not measurement rows, papers, labels, cases or
participants. The dataset counts rows, so "42 human clinical" has been true as
stated and misleading as read. This register resolves each clinical row to its
underlying study and makes the trial count reproducible.

COUNTING RULES (stated so the total can be checked, and so disagreement lands on
the rule rather than the arithmetic):

 R1. A trial counts ONCE however many rows, publications, labels or outcomes
     reference it.
 R2. An extension, longer follow-up or secondary publication of the same trial is
     the SAME trial. ENVISION baseline + ENVISION 24-month = one trial.
 R3. A regulatory label is NOT a trial. A label summarises one or more studies
     without identifying which, so a label-only row cannot increment the trial
     count -- it is real clinical evidence of a weaker kind.
 R4. A case report is NOT a trial.
 R5. A review or editorial is NOT a trial, even when it discusses trials.
 R6. A pooled cross-trial analysis is NOT one trial and its component trials are
     not individually identified; it is counted in its own class.
 R7. A study with neither a name nor a registry identifier is UNRESOLVED and does
     not increment the verified count. No identifier is ever invented.

SOURCE ACCESS is three-valued, not boolean. An adversarial review of the first
version of this register found the boolean flag was doing too much work: it was set
TRUE for documents the project's own SOURCES_TO_ACQUIRE.md lists as unretrieved,
because reading a web-fetched page and holding the PDF had been conflated.

  document_in_hand   the primary trial report is held locally under sources/
  fetched_and_read   the primary trial report was fetched and read in this project,
                     but no local copy is held (a weaker tier: the read passed
                     through a summarisation layer)
  not_read           neither

A trial enters the headline VERIFIED count only when it is BOTH class `trial` AND
its access is `document_in_hand` or `fetched_and_read` AND the document read is the
trial report itself. That last clause matters: PMC12369710, previously credited as
the read source for SEQUOIA, is a secondary paper in Annals of Medicine and Surgery
reporting the trial's findings -- not the trial report -- so under R5 it makes
MSR078 review_derived, not a verified trial.

Usage:  python scripts/build_study_register.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "data", "measurements.csv")
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")
OUT = os.path.join(ROOT, "data", "clinical_study_register.csv")

# Per-row attribution. Every entry is a judgement about what the cited source IS,
# made from the source_ref/source_table already in the data and, where marked
# read=True, from having opened the document in this project.
#   study_key : the deduplication key. Rows sharing a key are the same study.
#   evidence_class : trial | label_derived | case_report | review_derived |
#                    pooled_analysis | unresolved
#   access : document_in_hand | fetched_and_read | not_read (see docstring)
A = {
 # --- named / registered trials -------------------------------------------------
 "MSR001": ("NEURO-TTR", "trial", "NEJM 2018 NEJMoa1716793; phase 3 inotersen", "not_read"),
 "MSR005": ("vanPoelgeest2013_SPC5001_ph1", "trial", "Br J Clin Pharmacol phase 1", "not_read"),
 "MSR006": ("vanPoelgeest2013_SPC5001_ph1", "trial", "same phase 1 study as MSR005 (R1)", "not_read"),
 "MSR007": ("vanPoelgeest2013_SPC5001_ph1", "trial", "same phase 1 study as MSR005 (R1)", "not_read"),
 "MSR009": ("ENVISION", "trial", "NEJM 2019 NEJMoa1913147; phase 3 givosiran", "not_read"),
 "MSR010": ("ENVISION", "trial", "ENVISION 24-month follow-up = same trial (R2)", "not_read"),
 # Reclassified on review: the value was read out of the SmPC, not the APPROACH report.
 # Shares source_id A8 with MSR013, which is label_derived from the same SmPC. The NCT
 # is a pointer, not evidence of class (R3).
 "MSR012": ("LABEL_volanesorsen_Waylivra", "label_derived",
            "value from EMA SmPC sec 4.4/4.8; NCT02658175 is a pointer, APPROACH report not retrieved",
            "not_read"),
 "MSR017": ("DMD114673", "trial", "drisapersen study DMD114673; Janssen2019 PMC6796739 PDF held in sources/", "document_in_hand"),
 "MSR018": ("DMD114673", "trial", "same study as MSR017 (R1)", "document_in_hand"),
 "MSR019": ("DMD114673", "trial", "same study as MSR017 (R1)", "document_in_hand"),
 "MSR040": ("PROMOVI", "trial", "eteplirsen PROMOVI", "not_read"),
 # Reclassified on review: no trial document cited -- label + NCBI Bookshelf monograph +
 # a bare trial-name token. Own prior retrieval found eGFR reported as efficacy/eligibility.
 "MSR045": ("LABEL_lumasiran_Oxlumo", "label_derived",
            "Oxlumo label + NBK588653 monograph; ILLUMINATE-B is a bare name token, report not retrieved",
            "fetched_and_read"),
 "MSR046": ("PHYOX3", "trial", "nedosiran PHYOX3", "not_read"),
 # Reclassified on review: only document is the Amvuttra PI; own CLINICAL_VALIDATION
 # records this row UNSUPPORTED on that label. Mirrors MSR044 (patisiran), same shape.
 "MSR047": ("LABEL_vutrisiran_Amvuttra", "label_derived",
            "Amvuttra prescribing information; HELIOS-A is a bare name token, report not retrieved",
            "fetched_and_read"),
 "MSR056": ("Mongersen_ph2_NEJM2015", "trial", "NEJM 2015 phase 2", "not_read"),
 "MSR065": ("OCEANa-DOSE", "trial", "olpasiran phase 2", "not_read"),
 "MSR066": ("Cemdisiran_ph2_IgAN", "trial",
            "CJASN 2024 phase 2 IgAN primary report; PMC11020434 fetched and read, no local copy",
            "fetched_and_read"),
 "MSR067": ("Donidalorsen_ph3_NEJM2024", "trial", "NEJM 2024 phase 3", "not_read"),
 # Reclassified on review: the one resolvable citation (PMC9804925) is a phase 1
 # healthy-volunteer study, contradicting this row's population=chronic_HBV_patients;
 # "B-Clear_NEJM" carries no DOI/PMID/NCT. Unresolved per R7 rather than counted.
 "MSR068": ("UNRESOLVED_bepirovirsen_BClear", "unresolved",
            "PMC9804925 is a phase 1 healthy-volunteer study, not B-Clear; B-Clear has no resolvable citation",
            "not_read"),
 "MSR077": ("Teprasiran_ph2_Circ2021", "trial", "Circulation 2021 phase 2", "not_read"),
 # Reclassified on review: PMC12369710 is a secondary paper in Annals of Medicine and
 # Surgery reporting SEQUOIA's findings, not the trial report. R5 applies.
 "MSR078": ("REVIEW_fazirsiran_SEQUOIA_secondary", "review_derived",
            "PMC12369710 is a secondary report in Annals of Medicine and Surgery, not the SEQUOIA trial report",
            "fetched_and_read"),
 "MSR079": ("TRANSLATE-TIMI70", "trial", "vupanorsen phase 2b", "not_read"),
 # --- label-derived: the label summarises studies, is not itself a trial (R3) ----
 "MSR002": ("LABEL_inotersen_211172", "label_derived", "FDA label sec 5.2", "not_read"),
 "MSR003": ("LABEL_inotersen_211172", "label_derived", "FDA label sec 5.2", "not_read"),
 "MSR011": ("LABEL_nusinersen_Spinraza", "label_derived", "label sec 5.3 cites Study 1+2, not resolved individually", "not_read"),
 "MSR013": ("LABEL_volanesorsen_Waylivra", "label_derived", "EMA SmPC", "not_read"),
 "MSR014": ("LABEL_mipomersen_203568", "label_derived", "FDA label sec 5 + EPAR", "not_read"),
 "MSR015": ("LABEL_mipomersen_203568", "label_derived", "open-label extension via label; study not identified", "not_read"),
 "MSR016": ("LABEL_inclisiran_Leqvio", "label_derived", "label sec 6", "not_read"),
 "MSR042": ("LABEL_tofersen_Qalsody", "label_derived", "label warnings; read directly", "fetched_and_read"),
 "MSR043": ("LABEL_eplontersen_Wainua", "label_derived", "label clinical AE", "not_read"),
 "MSR044": ("LABEL_patisiran_Onpattro", "label_derived", "prescribing information; read directly", "fetched_and_read"),
 "MSR049": ("LABEL_pegaptanib_Macugen", "label_derived", "FDA label 021756", "not_read"),
 "MSR055": ("LABEL_fitusiran_Qfitlia", "label_derived", "FDA label 219019", "not_read"),
 "MSR160": ("LABEL_golodirsen_Vyondys53", "label_derived", "DailyMed SPL sec 5.2; read directly", "fetched_and_read"),
 "MSR162": ("LABEL_casimersen_Amondys45", "label_derived", "DailyMed SPL sec 5.2; read directly", "fetched_and_read"),
 "MSR164": ("LABEL_viltolarsen_Viltepso", "label_derived", "DailyMed SPL sec 5.1; read directly", "fetched_and_read"),
 # --- not trials (R4, R5, R6, R7) -----------------------------------------------
 "MSR004": ("CASE_inotersen_FSGS_AJKD2022", "case_report", "single-patient biopsy case", "not_read"),
 "MSR030": ("REVIEW_Wu2022", "review_derived", "review restating the nusinersen label", "fetched_and_read"),
 "MSR063": ("REVIEW_pelacarsen_ClinKidneyJ", "review_derived", "editorial; verified to report no renal endpoint", "fetched_and_read"),
 "MSR058": ("POOLED_Crooke2018_2MOE", "pooled_analysis", "pooled across unidentified 2'-MOE trials (R6)", "not_read"),
 "MSR064": ("UNRESOLVED_zilebesiran_KARDIA", "unresolved", "source_ref 'KARDIA_trials' is not a citation (R7)", "not_read"),
}


def main():
    OL = {r["oligo_id"]: r for r in csv.DictReader(open(OLIGOS, newline=""))}
    rows = [r for r in csv.DictReader(open(MEAS, newline="")) if r["study_type"] == "clinical"]

    missing = [r["measurement_id"] for r in rows if r["measurement_id"] not in A]
    extra = [k for k in A if k not in {r["measurement_id"] for r in rows}]
    if missing or extra:
        raise SystemExit(f"attribution out of sync — unattributed {missing}, stale {extra}")

    out = []
    for r in sorted(rows, key=lambda x: x["measurement_id"]):
        key, cls, why, access = A[r["measurement_id"]]
        ol = OL[r["oligo_id"]]
        out.append({
            "measurement_id": r["measurement_id"],
            "study_key": key,
            "evidence_class": cls,
            "counts_toward_trial_total": "TRUE" if cls == "trial" else "FALSE",
            "source_access": access,
            "counts_as_verified": "TRUE" if (cls == "trial" and access != "not_read") else "FALSE",
            "oligo_id": r["oligo_id"],
            "oligo_name": ol["oligo_name"],
            "population": r["system_model"],
            "renal_endpoint": r["readout_name"],
            "reported_value": r["readout_value"],
            "nephrotox_grade": r["nephrotox_grade"],
            "renal_endpoints_measured": r["renal_endpoints_measured"],
            "source_ref": r["source_ref"],
            "source_locus": r["source_table"],
            "attribution_basis": why,
        })

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    # ---- derived counts, by class, deduplicated on study_key ----
    def keys(cls):
        return {r["study_key"] for r in out if r["evidence_class"] == cls}
    trials = keys("trial")
    read_trials = {r["study_key"] for r in out if r["counts_as_verified"] == "TRUE"}

    print(f"wrote {OUT}: {len(out)} clinical rows attributed\n")
    print("CLINICAL EVIDENCE, deduplicated by study")
    print(f"  distinct trials identified          {len(trials):>3}")
    print(f"    of which the report was read      {len(read_trials):>3}   <- headline VERIFIED trial count")
    print(f"    identified but not yet read       {len(trials - read_trials):>3}   <- acquisition worklist")
    for cls, label in [("label_derived", "distinct labels (not trials)"),
                       ("case_report", "case reports"),
                       ("review_derived", "reviews/editorials"),
                       ("pooled_analysis", "pooled cross-trial analyses"),
                       ("unresolved", "unresolved citations")]:
        print(f"  {label:<35}{len(keys(cls)):>3}")
    print(f"\n  clinical measurement rows           {len(out):>3}  (NOT a trial count)")
    print(f"  unique compounds with clinical data {len({r['oligo_id'] for r in out}):>3}")
    print(f"\n  verified trials, by name: {', '.join(sorted(read_trials))}")
    print(f"  unread trials, by name:   {', '.join(sorted(trials - read_trials))}")


if __name__ == "__main__":
    main()
