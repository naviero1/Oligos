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

Two separate verification tiers, because "verified" must mean something:
  trial_identified        the row resolves to a distinguishable study (name or registry ID)
  primary_source_read     the primary trial document was actually opened and read
                          in this project (not a search summary, not a label
                          restating it)

A trial enters the headline VERIFIED count only when both hold. Trials identified
but not yet read are reported separately as identified-but-unread, which is the
honest state and also the acquisition worklist.

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
#   read : was the PRIMARY study document opened in this project?
A = {
 # --- named / registered trials -------------------------------------------------
 "MSR001": ("NEURO-TTR", "trial", "NEJM 2018 NEJMoa1716793; phase 3 inotersen", False),
 "MSR005": ("vanPoelgeest2013_SPC5001_ph1", "trial", "Br J Clin Pharmacol phase 1", False),
 "MSR006": ("vanPoelgeest2013_SPC5001_ph1", "trial", "same phase 1 study as MSR005 (R1)", False),
 "MSR007": ("vanPoelgeest2013_SPC5001_ph1", "trial", "same phase 1 study as MSR005 (R1)", False),
 "MSR009": ("ENVISION", "trial", "NEJM 2019 NEJMoa1913147; phase 3 givosiran", False),
 "MSR010": ("ENVISION", "trial", "ENVISION 24-month follow-up = same trial (R2)", False),
 "MSR012": ("APPROACH_NCT02658175", "trial", "registry ID present", False),
 "MSR017": ("DMD114673", "trial", "drisapersen study DMD114673", True),
 "MSR018": ("DMD114673", "trial", "same study as MSR017 (R1)", True),
 "MSR019": ("DMD114673", "trial", "same study as MSR017 (R1)", True),
 "MSR040": ("PROMOVI", "trial", "eteplirsen PROMOVI", False),
 "MSR045": ("ILLUMINATE-B", "trial", "lumasiran ILLUMINATE-B", False),
 "MSR046": ("PHYOX3", "trial", "nedosiran PHYOX3", False),
 "MSR047": ("HELIOS-A", "trial", "vutrisiran HELIOS-A", False),
 "MSR056": ("Mongersen_ph2_NEJM2015", "trial", "NEJM 2015 phase 2", False),
 "MSR065": ("OCEANa-DOSE", "trial", "olpasiran phase 2", False),
 "MSR066": ("Cemdisiran_ph2_IgAN", "trial", "CJASN 2024 phase 2", True),
 "MSR067": ("Donidalorsen_ph3_NEJM2024", "trial", "NEJM 2024 phase 3", False),
 "MSR068": ("B-Clear", "trial", "bepirovirsen B-Clear", False),
 "MSR077": ("Teprasiran_ph2_Circ2021", "trial", "Circulation 2021 phase 2", False),
 "MSR078": ("SEQUOIA", "trial", "fazirsiran SEQUOIA", True),
 "MSR079": ("TRANSLATE-TIMI70", "trial", "vupanorsen phase 2b", False),
 # --- label-derived: the label summarises studies, is not itself a trial (R3) ----
 "MSR002": ("LABEL_inotersen_211172", "label_derived", "FDA label sec 5.2", False),
 "MSR003": ("LABEL_inotersen_211172", "label_derived", "FDA label sec 5.2", False),
 "MSR011": ("LABEL_nusinersen_Spinraza", "label_derived", "label sec 5.3 cites Study 1+2, not resolved individually", False),
 "MSR013": ("LABEL_volanesorsen_Waylivra", "label_derived", "EMA SmPC", False),
 "MSR014": ("LABEL_mipomersen_203568", "label_derived", "FDA label sec 5 + EPAR", False),
 "MSR015": ("LABEL_mipomersen_203568", "label_derived", "open-label extension via label; study not identified", False),
 "MSR016": ("LABEL_inclisiran_Leqvio", "label_derived", "label sec 6", False),
 "MSR042": ("LABEL_tofersen_Qalsody", "label_derived", "label warnings; read directly", True),
 "MSR043": ("LABEL_eplontersen_Wainua", "label_derived", "label clinical AE", False),
 "MSR044": ("LABEL_patisiran_Onpattro", "label_derived", "prescribing information; read directly", True),
 "MSR049": ("LABEL_pegaptanib_Macugen", "label_derived", "FDA label 021756", False),
 "MSR055": ("LABEL_fitusiran_Qfitlia", "label_derived", "FDA label 219019", False),
 "MSR160": ("LABEL_golodirsen_Vyondys53", "label_derived", "DailyMed SPL sec 5.2; read directly", True),
 "MSR162": ("LABEL_casimersen_Amondys45", "label_derived", "DailyMed SPL sec 5.2; read directly", True),
 "MSR164": ("LABEL_viltolarsen_Viltepso", "label_derived", "DailyMed SPL sec 5.1; read directly", True),
 # --- not trials (R4, R5, R6, R7) -----------------------------------------------
 "MSR004": ("CASE_inotersen_FSGS_AJKD2022", "case_report", "single-patient biopsy case", False),
 "MSR030": ("REVIEW_Wu2022", "review_derived", "review restating the nusinersen label", True),
 "MSR063": ("REVIEW_pelacarsen_ClinKidneyJ", "review_derived", "editorial; verified to report no renal endpoint", True),
 "MSR058": ("POOLED_Crooke2018_2MOE", "pooled_analysis", "pooled across unidentified 2'-MOE trials (R6)", False),
 "MSR064": ("UNRESOLVED_zilebesiran_KARDIA", "unresolved", "source_ref 'KARDIA_trials' is not a citation (R7)", False),
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
        key, cls, why, read = A[r["measurement_id"]]
        ol = OL[r["oligo_id"]]
        out.append({
            "measurement_id": r["measurement_id"],
            "study_key": key,
            "evidence_class": cls,
            "counts_toward_trial_total": "TRUE" if cls == "trial" else "FALSE",
            "primary_source_read": "TRUE" if read else "FALSE",
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
    read_trials = {r["study_key"] for r in out
                   if r["evidence_class"] == "trial" and r["primary_source_read"] == "TRUE"}

    print(f"wrote {OUT}: {len(out)} clinical rows attributed\n")
    print("CLINICAL EVIDENCE, deduplicated by study")
    print(f"  distinct trials identified          {len(trials):>3}")
    print(f"    of which primary source read      {len(read_trials):>3}   <- headline VERIFIED trial count")
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
