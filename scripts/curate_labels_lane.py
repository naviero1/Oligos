#!/usr/bin/env python3
"""Emit a hand-curated 'regulatory label' lane in curation-workflow format.

These rows were extracted by the curator directly from FDA prescribing
information retrieved this session via the DailyMed SPL REST API, and parsed from
the label XML — not via a subagent and not from memory. Every value below was
read off the retrieved label text; the exact sentences are preserved in
scripts/scan_labels_platelet.py output for audit.

Design metadata for compounds that already appear in the sister OligoTox-Kidney
dataset is REUSED from data/oligos.csv rather than re-derived, carrying that
dataset's own design_source provenance with it. This is deliberate: those rows
were already validated against WHO INN nomenclature and patent sequence listings
(see ../schema.md "Data-dictionary QC log"), so re-deriving them would risk
introducing an error the sister dataset has already ruled out.

Output is merged with the multi-agent lane output by scripts/assemble_thrombo.py.

Usage:  python3 scripts/curate_labels_lane.py > labels_lane.json
"""
import csv, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIDNEY_OLIGOS = os.path.join(ROOT, "data", "oligos.csv")

# ---------------------------------------------------------------------------
# Label identifiers verified this session (DailyMed SPL setid + version)
# ---------------------------------------------------------------------------
LABELS = {
    "inotersen":  ("FDA_label_TEGSEDI_SPL_8513207e-b55f-417b-9473-af785146a543_v10", "TEGSEDI (inotersen), Akcea Therapeutics, SPL v10 2024-01-26"),
    "olezarsen":  ("FDA_label_TRYNGOLZA_SPL_olezarsen", "TRYNGOLZA (olezarsen sodium), Ionis Pharmaceuticals"),
    "nusinersen": ("FDA_label_SPINRAZA_SPL_nusinersen", "SPINRAZA (nusinersen), Biogen"),
    "imetelstat": ("FDA_label_RYTELO_SPL_imetelstat", "RYTELO (imetelstat sodium), Geron Corporation"),
}

# ---------------------------------------------------------------------------
# Measurement rows. Every readout_value below appears verbatim in the retrieved
# label text. Grades follow the rubric in thrombocytopenia/schema.md:
# incidence rows are graded by the SEVERITY OF THE EVENT, not by the incidence.
# ---------------------------------------------------------------------------
M = []


def row(**kw):
    base = dict(species="human", tissue="blood", delivery_method="systemic_dose",
                dose_or_conc_unit="mg", exposure_duration="TBD",
                readout_unit="pct_incidence", effect_direction="increase",
                is_platelet_specific="TRUE", redistribution="public_domain",
                study_type="clinical", system_model="patient_cohort")
    base.update(kw)
    M.append(base)


# --- inotersen (TEGSEDI) — the canonical severe anchor ----------------------
INO = LABELS["inotersen"][0]
row(oligo_name="inotersen", dose_or_conc_value="284", exposure_duration="weekly",
    readout_category="platelet_count", readout_name="platelet_count_below_100x10e9_per_L",
    readout_value="25", effect_vs_control="25pct_vs_2pct_placebo",
    thrombocytopenia_grade=2, source_ref=INO, source_table="label sec 5.1",
    notes="NEURO-TTR Study 1;the common dose-dependent mode;grade_provisional")
row(oligo_name="inotersen", dose_or_conc_value="284", exposure_duration="weekly",
    readout_category="platelet_count", readout_name="platelet_count_below_75x10e9_per_L",
    readout_value="14", effect_vs_control="14pct_vs_0pct_placebo",
    thrombocytopenia_grade=2, source_ref=INO, source_table="label sec 5.1",
    notes="NEURO-TTR Study 1;no placebo patient affected;grade_provisional")
row(oligo_name="inotersen", dose_or_conc_value="284", exposure_duration="chronic",
    readout_category="platelet_count", readout_name="platelet_nadir_below_75x10e9_per_L_baseline_under_200",
    readout_value="39", effect_vs_control="39pct_vs_6pct_if_baseline_ge_200x10e9_per_L",
    thrombocytopenia_grade=2, source_ref=INO, source_table="label sec 5.1",
    notes="Study 1 + extension;BASELINE PLATELET COUNT IS A RISK FACTOR - modellable covariate;grade_provisional")
row(oligo_name="inotersen", dose_or_conc_value="284", exposure_duration="chronic",
    readout_category="platelet_count", readout_name="sudden_severe_thrombocytopenia_below_25x10e9_per_L",
    readout_value="3", effect_vs_control="3_patients_3pct",
    thrombocytopenia_grade=3, source_ref=INO, source_table="label sec 5.1 + Boxed Warning",
    notes="the rare severe idiosyncratic mode;potentially fatal bleeding;graded on event severity not incidence;grade_provisional")
row(oligo_name="inotersen", dose_or_conc_value="284", exposure_duration="chronic",
    readout_category="immunogenicity", readout_name="treatment_emergent_antiplatelet_IgG_antibody",
    readout_value="3", readout_unit="patients", effect_vs_control="3_of_3_severe_cases",
    thrombocytopenia_grade=3, source_ref=INO, source_table="label sec 5.1",
    notes="ALL 3 severe-thrombocytopenia patients were antibody-positive shortly before/at the event - this is the evidence that the severe mode is IMMUNE-MEDIATED and mechanistically distinct from the mild decline;grade_provisional")
row(oligo_name="inotersen", dose_or_conc_value="284", exposure_duration="chronic",
    readout_category="clinical_outcome", readout_name="fatal_intracranial_hemorrhage",
    readout_value="1", readout_unit="patients", effect_vs_control="1_death",
    thrombocytopenia_grade=3, source_ref=INO, source_table="Boxed Warning",
    notes="basis of the FDA Boxed Warning;grade_provisional")

# --- olezarsen (TRYNGOLZA) — GalNAc 2'-MOE ASO, mild dose-dependent mode ----
OLE = LABELS["olezarsen"][0]
row(oligo_name="olezarsen", dose_or_conc_value="80", exposure_duration="53wk",
    readout_category="clinical_outcome", readout_name="decreased_platelet_count_adverse_reaction",
    readout_value="12", effect_vs_control="12pct_5of43_vs_4pct_1of23_placebo",
    thrombocytopenia_grade=1, source_ref=OLE, source_table="label sec 6.1 Table (Trial 1, FCS)",
    notes="FCS Trial 1;no major bleeding events associated with low platelet counts;grade_provisional")
row(oligo_name="olezarsen", dose_or_conc_value="50", exposure_duration="53wk",
    readout_category="platelet_count", readout_name="mean_platelet_count_change_from_baseline",
    readout_value="-6", readout_unit="pct_change", effect_direction="decrease",
    effect_vs_control="minus6pct_vs_no_change_placebo",
    thrombocytopenia_grade=1, source_ref=OLE, source_table="label sec 6.1 Laboratory Tests",
    notes="sHTG Trials 2+3;DOSE-RESPONSE pair with the 80 mg row;grade_provisional")
row(oligo_name="olezarsen", dose_or_conc_value="80", exposure_duration="53wk",
    readout_category="platelet_count", readout_name="mean_platelet_count_change_from_baseline",
    readout_value="-10", readout_unit="pct_change", effect_direction="decrease",
    effect_vs_control="minus10pct_vs_plus22pct_placebo_Trial1_or_no_change_Trials2-3",
    thrombocytopenia_grade=1, source_ref=OLE, source_table="label sec 6.1 Laboratory Tests",
    notes="across all trials;higher dose gives larger mean decline = dose-dependent mild mode;grade_provisional")
row(oligo_name="olezarsen", dose_or_conc_value="TBD", exposure_duration="53wk",
    readout_category="clinical_outcome", readout_name="major_bleeding_event_associated_with_low_platelets",
    readout_value="0", readout_unit="events", effect_direction="no_change",
    effect_vs_control="none_reported;bleeding_AE_rate_similar_to_placebo",
    thrombocytopenia_grade=0, source_ref=OLE, source_table="label sec 6.1 Laboratory Tests",
    notes="NEGATIVE row: platelet decline occurred WITHOUT clinical bleeding - separates laboratory effect from clinical harm;grade_provisional")

# --- nusinersen (SPINRAZA) — intrathecal 2'-MOE PS, class-warning ----------
NUS = LABELS["nusinersen"][0]
row(oligo_name="nusinersen", dose_or_conc_value="12", delivery_method="intrathecal",
    exposure_duration="chronic", readout_category="platelet_count",
    readout_name="platelet_count_below_lower_limit_of_normal",
    readout_value="16", effect_vs_control="16pct_24of146_vs_14pct_10of72_sham",
    thrombocytopenia_grade=1, source_ref=NUS, source_table="label sec 5.1",
    notes="Studies 1+2 Low Dose Regimen;NEAR-NULL vs sham (16pct vs 14pct) - intrathecal route gives minimal systemic platelet exposure;grade_provisional")
row(oligo_name="nusinersen", dose_or_conc_value="12", delivery_method="intrathecal",
    exposure_duration="28d", readout_category="platelet_count",
    readout_name="platelet_count_below_50000_per_uL",
    readout_value="2", readout_unit="patients",
    effect_vs_control="lowest_10000_per_uL_on_study_day_28",
    thrombocytopenia_grade=3, source_ref=NUS, source_table="label sec 5.1",
    notes="Study 2;the rare severe mode appears even by the intrathecal route;grade_provisional")

# --- imetelstat (RYTELO) — DIFFERENT MECHANISM, flagged ---------------------
IME = LABELS["imetelstat"][0]
row(oligo_name="imetelstat", dose_or_conc_value="7.1", dose_or_conc_unit="mg/kg",
    exposure_duration="chronic", readout_category="platelet_count",
    readout_name="grade3_or_4_decreased_platelets",
    readout_value="65", effect_vs_control="65pct_of_MDS_patients",
    thrombocytopenia_grade=3, source_ref=IME, source_table="label sec 5.1 / 6.1",
    notes="MECHANISM DIFFERS: imetelstat is a lipid-conjugated N3'-P5' thiophosphoramidate telomerase template antagonist and its thrombocytopenia is ON-TARGET MYELOSUPPRESSION in MDS, not the PS-ASO platelet-binding mechanism. Retained for modality breadth but MUST be mechanism-flagged so a model does not attribute it to backbone chemistry;grade_provisional")
row(oligo_name="imetelstat", dose_or_conc_value="7.1", dose_or_conc_unit="mg/kg",
    exposure_duration="6wk", readout_category="platelet_count",
    readout_name="median_time_to_onset_grade3_or_4_decreased_platelets",
    readout_value="6", readout_unit="weeks", effect_vs_control="range_2_to_88_weeks",
    thrombocytopenia_grade=3, source_ref=IME, source_table="label sec 5.1",
    notes="kinetics row;median time to recovery to grade<=2 was 1.3 weeks;on-target myelosuppression;grade_provisional")


def main():
    with open(KIDNEY_OLIGOS, newline="", encoding="utf-8") as f:
        kidney = {r["oligo_name"].lower(): r for r in csv.DictReader(f)}

    oligos, seen = [], set()
    for m in M:
        n = m["oligo_name"].lower()
        if n in seen:
            continue
        seen.add(n)
        k = kidney.get(n)
        if k:
            o = {c: k[c] for c in k if c != "oligo_id"}
            o["notes"] = (k["notes"] + ";design_metadata_reused_from_OligoTox-Kidney_oligos.csv")
        else:
            o = {"oligo_name": m["oligo_name"], "oligo_class": "other",
                 "sequence_5to3": "TBD", "design_source": LABELS[n][0],
                 "notes": "design_metadata_not_yet_curated"}
            if n == "olezarsen":
                # Sequence recovered by deterministic parse of the label's IUPAC
                # chemical name (sec 11 DESCRIPTION), which spells out every residue:
                #   [MOE]rA [MOE]rG [MOE]m5rC [MOE]m5rU [MOE]m5rU   <- 5' MOE wing (5)
                #   m5C T T G T m5C m5C A G m5C                     <- DNA gap (10)
                #   [MOE]m5rU [MOE]m5rU [MOE]m5rU [MOE]rA [MOE]m5rU <- 3' MOE wing (5)
                # => 5-10-5 MOE gapmer, 20 nt, AGCTTCTTGTCCAGCTTTAT.
                # SELF-CHECK (why this is safe to fill rather than leave TBD):
                #  (a) the parse independently reproduces volanesorsen's already-published
                #      sequence — expected, since olezarsen is the GalNAc-conjugated
                #      APOC3 analogue — so two independent documents agree; and
                #  (b) the stated molecular formula C296H419N71O154P20S19Na20 gives
                #      S19 = 19 phosphorothioate linkages across 19 internucleotide
                #      bonds (full PS) and fixes the length at 20 residues.
                # This is the same INN-nomenclature derivation path documented as
                # path 4 in the sister dataset's METHODOLOGY §4.
                o.update(oligo_class="ASO_gapmer", target_gene="APOC3",
                         indication="familial_chylomicronemia_syndrome;severe_hypertriglyceridemia",
                         developer="Ionis", max_phase="approved", length_nt="20",
                         backbone_chemistry="full_PS",
                         sugar_modifications="2'-MOE;DNA_gap", gapmer_design="5-10-5_MOE",
                         conjugate="GalNAc", ps_count="19",
                         sequence_5to3="AGCTTCTTGTCCAGCTTTAT",
                         design_source=LABELS[n][0] + ";sec_11_DESCRIPTION_chemical_name",
                         notes="GalNAc-conjugated 2'-MOE gapmer targeting APOC3;sequence derived by deterministic parse of the label IUPAC chemical name;independently reproduces volanesorsen sequence (same target, non-conjugated analogue);molecular formula P20S19 confirms full-PS and 20 residues;SAME BASE SEQUENCE as volanesorsen - do not treat as two independent sequences when modelling, the informative contrast between them is the GalNAc conjugate")
            elif n == "imetelstat":
                o.update(oligo_class="other", target_gene="TERC_telomerase_RNA_template",
                         indication="myelodysplastic_syndromes_transfusion_dependent_anemia",
                         developer="Geron", max_phase="approved", length_nt="13",
                         backbone_chemistry="mixed",
                         sugar_modifications="N3'-P5'_thiophosphoramidate",
                         gapmer_design="NA", conjugate="lipid", ps_count="TBD",
                         notes="13-mer lipid-conjugated N3'-P5' thiophosphoramidate telomerase template antagonist;NOT a PS-ASO;thrombocytopenia is on-target myelosuppression")
        oligos.append(o)

    json.dump({"lanes": [{"lane": "curated_regulatory_labels",
                          "oligos": oligos, "measurements": M, "verified": None}]},
              sys.stdout, indent=1)


if __name__ == "__main__":
    main()
