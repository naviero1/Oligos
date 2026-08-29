#!/usr/bin/env python3
"""
Curated literature rows for OligoTox-Hydrocephalus.

Unlike the ClinicalTrials.gov, FAERS and DailyMed components, these rows cannot
be produced by a parser: each comes from prose in a full-text article that a
human read. They are therefore written out here EXPLICITLY, each carrying the
verbatim sentence it was taken from, so that the value and its evidence travel
together and any reader can check one against the other without opening the
article. The full texts are committed under sources/raw/.

Nothing in this file is recalled from memory. Every `evidence` string below was
copied from the retrieved full text of the cited article.

Output: data/_literature_measurements.csv

Usage: python3 scripts/build_literature.py
"""
import csv
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

TODAY = date.today().isoformat()

# --------------------------------------------------------------------------
# L1 — Stoker, Andresen & Barker 2021, Movement Disorders 36(1):263-264.
#      "Hydrocephalus Complicating Intrathecal Antisense Oligonucleotide
#      Therapy for Huntington's Disease". PMID 33125799, PMC7894279.
#      Licence: CC BY 4.0 (open access) -> values may be reproduced.
#
#      A single patient in the tominersen open-label extension (NCT03342053).
#      All four rows describe the SAME patient and the SAME clinical episode:
#      they share event_cluster_id L1-EVT-01 and must never be counted as four
#      independent events.
# --------------------------------------------------------------------------
L1 = dict(
    source_key="Stoker_2021_MovDisord",
    source_ref="PMID 33125799; PMC7894279; doi 10.1002/mds.28359",
    study_type="clinical_case", species="human", strain="NOT_APPLICABLE",
    system_model=("Single case report within the tominersen open-label extension "
                  "(the article names NCT03761849 as the concurrent phase 3; the "
                  "patient was in the phase 1/2a OLE)"),
    is_human_system="TRUE",
    indication_population="Huntington's disease, CAG 42, 54-year-old man",
    arm_label="tominersen 120 mg intrathecal monthly (open-label extension)",
    arm_description=("Had received four doses of intrathecal PLACEBO in the prior "
                     "phase 1/2a trial before starting open-label tominersen"),
    arm_role="exposed",
    cns_compartment="lateral_ventricles", delivery_route="intrathecal_lumbar",
    dose_regimen="monthly intrathecal tominersen",
    exposure_duration="deterioration began after the fifth monthly dose",
    redistribution="cc_by",
)

L1_ROWS = [
    dict(endpoint_tier="A", readout_category="hydrocephalus_event",
         readout_name="communicating_hydrocephalus_diagnosed",
         readout_value="communicating hydrocephalus", readout_unit="diagnosis",
         readout_is_qualitative="TRUE", n_affected=1, n_at_risk="NOT_REPORTED",
         grade=3,
         grade_basis=("3 = hydrocephalus requiring permanent CSF diversion; a "
                      "ventriculoperitoneal shunt was inserted (SCHEMA.md rubric "
                      "grade 3)."),
         tox_axis="ventricular_enlargement",
         attribution="drug_attributed",
         evidence=("\"Here we report for the first time on a patient in receipt of "
                   "this therapy who developed a communicating hydrocephalus that we "
                   "diagnosed as being secondary to a sterile meningitis induced by "
                   "tominersen.\""),
         location="Discussion, paragraph 1"),
    dict(endpoint_tier="A", readout_category="ventricular_morphometry",
         readout_name="ventricular_dilation_on_serial_MRI",
         readout_value="increasing ventricular dilation with periventricular edema",
         readout_unit="qualitative_imaging", readout_is_qualitative="TRUE",
         n_affected=1, n_at_risk="NOT_REPORTED", grade=2,
         grade_basis=("2 = symptomatic ventriculomegaly; the imaging change "
                      "accompanied gait deterioration and preceded shunting "
                      "(SCHEMA.md rubric grade 2). No ventricular volume is "
                      "published, so readout_is_qualitative is TRUE and no number "
                      "was read off the figure."),
         tox_axis="ventricular_enlargement", attribution="drug_attributed",
         evidence=("\"Serial brain magnetic resonance imaging revealed increasing "
                   "ventricular dilation, with periventricular edema, consistent with "
                   "hydrocephalus (Fig. 1C,D).\""),
         location="Case description; Fig. 1C,D"),
    dict(endpoint_tier="B", readout_category="csf_composition",
         readout_name="CSF_total_protein_peak", readout_value="2.64",
         readout_unit="g/L", readout_is_qualitative="FALSE",
         n_affected=1, n_at_risk="NOT_REPORTED", grade=2,
         grade_basis=("2 = the authors diagnosed a sterile meningitis, named at "
                      "SCHEMA.md rubric grade 2. The CSF protein rise is the "
                      "biochemical evidence for that diagnosis."),
         tox_axis="csf_composition_disturbance", attribution="drug_attributed",
         evidence=("\"His clinical deterioration was accompanied by a progressive "
                   "increase in CSF protein, peaking at 2.64 g/L, and a CSF "
                   "lymphocytosis, peaking at 46 cells/mm3 (Fig. 1A,B).\""),
         location="Case description; Fig. 1A"),
    dict(endpoint_tier="B", readout_category="csf_dynamics",
         readout_name="resistance_to_CSF_outflow_lumbar_infusion_study",
         readout_value="increased resistance to CSF outflow",
         readout_unit="qualitative_manometry", readout_is_qualitative="TRUE",
         n_affected=1, n_at_risk="NOT_REPORTED", grade=2,
         grade_basis=("2 = a measured CSF-dynamics abnormality that was symptomatic "
                      "and led to intervention (SCHEMA.md rubric grade 2). This row "
                      "is the direct physiological measurement linking the tier-B "
                      "CSF change to the tier-A ventricular outcome."),
         tox_axis="csf_dynamics",
         attribution="drug_attributed",
         evidence=("\"His gait improved dramatically after a high-volume CSF tap, and "
                   "lumbar infusion studies confirmed increased resistance to CSF "
                   "outflow (Fig. 1E).\""),
         location="Case description; Fig. 1E"),
    dict(endpoint_tier="A", readout_category="shunt_or_drain_intervention",
         readout_name="ventriculoperitoneal_shunt_inserted",
         readout_value="ventriculoperitoneal shunt", readout_unit="intervention",
         readout_is_qualitative="TRUE", n_affected=1, n_at_risk="NOT_REPORTED",
         grade=3,
         grade_basis=("3 = permanent CSF diversion performed (SCHEMA.md rubric "
                      "grade 3)."),
         tox_axis="ventricular_enlargement", attribution="drug_attributed",
         evidence=("\"A ventriculoperitoneal shunt was therefore inserted, and his "
                   "mobility improved to his baseline state. He did not receive any "
                   "further doses of tominersen.\""),
         location="Case description, final sentence"),
]

# --------------------------------------------------------------------------
# L2 — Viscidi et al. 2021, Orphanet Journal of Rare Diseases 16:207.
#      "The incidence of hydrocephalus among patients with and without spinal
#      muscular atrophy (SMA): Results from a US electronic health records
#      study". PMID 33962637, PMC8105953. Licence: CC BY 4.0.
#
#      THE CONFOUNDER CONTROL. These rows carry NO drug exposure. The study
#      period (2007-2016) ENDS at nusinersen approval, so the SMA rate here is a
#      disease baseline uncontaminated by the drug.
# --------------------------------------------------------------------------
L2 = dict(
    source_key="Viscidi_2021_OJRD",
    source_ref="PMID 33962637; PMC8105953; doi 10.1186/s13023-021-01822-4",
    study_type="background_epidemiology", species="human", strain="NOT_APPLICABLE",
    system_model=("Retrospective matched-cohort study, US Optum de-identified "
                  "electronic health records, study period 1 Jan 2007 - 22 Dec 2016 "
                  "(i.e. before nusinersen approval)"),
    is_human_system="TRUE",
    arm_description=("Hydrocephalus ascertained by one or more ICD-9/ICD-10 codes for "
                     "any type of hydrocephalus after the index date"),
    cns_compartment="whole_ventricular_system", delivery_route="NOT_APPLICABLE",
    dose_regimen="NOT_APPLICABLE", exposure_duration="NOT_APPLICABLE",
    redistribution="cc_by",
)

L2_ROWS = [
    dict(population="Spinal muscular atrophy, untreated era", arm_label="SMA cases",
         arm_role="disease_background",
         readout_name="hydrocephalus_incidence_rate", readout_value="15.5",
         readout_unit="per_100000_person_months", n_affected=42, n_at_risk=5354,
         statistic="95% CI 11.2-20.9",
         comparator="non-SMA matched controls", n_aff_comp=9, n_risk_comp=5354,
         evidence=("\"There were 5354 SMA cases and an equal number of matched non-SMA "
                   "controls. Incident hydrocephalus events were identified in 42 SMA "
                   "cases and 9 non-SMA controls. Hydrocephalus incidence rates per "
                   "100,000 person-months were 15.5 (95% CI: 11.2-20.9) among SMA cases "
                   "and 3.3 (95% CI: 1.5-6.3) among non-SMA controls.\""),
         location="Abstract, Results"),
    dict(population="Matched non-SMA controls", arm_label="non-SMA matched controls",
         arm_role="disease_background",
         readout_name="hydrocephalus_incidence_rate", readout_value="3.3",
         readout_unit="per_100000_person_months", n_affected=9, n_at_risk=5354,
         statistic="95% CI 1.5-6.3",
         comparator="SMA cases", n_aff_comp=42, n_risk_comp=5354,
         evidence=("\"Hydrocephalus incidence rates per 100,000 person-months were 15.5 "
                   "(95% CI: 11.2-20.9) among SMA cases and 3.3 (95% CI: 1.5-6.3) among "
                   "non-SMA controls.\""),
         location="Abstract, Results"),
    dict(population="SMA versus matched non-SMA controls",
         arm_label="SMA vs non-SMA incidence rate ratio", arm_role="disease_background",
         readout_name="hydrocephalus_incidence_rate_ratio", readout_value="4.7",
         readout_unit="incidence_rate_ratio", n_affected="NOT_APPLICABLE",
         n_at_risk="NOT_APPLICABLE", statistic="95% CI 2.4-10.2",
         comparator="non-SMA matched controls", n_aff_comp="NOT_APPLICABLE",
         n_risk_comp="NOT_APPLICABLE",
         evidence=("\"The incidence rate ratio was 4.7 (95% CI: 2.4-10.2). ... SMA "
                   "patients had an approximately fourfold increased risk of "
                   "hydrocephalus compared with non-SMA controls in the era preceding "
                   "nusinersen treatment.\""),
         location="Abstract, Results and Conclusions"),
]

# --------------------------------------------------------------------------
# L3 — Serious Neurologic Adverse Events in Tofersen Clinical Trials for ALS,
#      Muscle & Nerve (2025). PMID 40017137, PMC12060635.
#      Licence: CC BY-NC-ND -> recorded as summary_stat_only, because the ND
#      term makes reproduction of the underlying table inadvisable; only the
#      figures quoted in the abstract are carried, as summary statistics.
# --------------------------------------------------------------------------
L3 = dict(
    source_key="Tofersen_seriousAE_2025_MuscleNerve",
    source_ref="PMID 40017137; PMC12060635; doi 10.1002/mus.28372",
    study_type="clinical_trial", species="human", strain="NOT_APPLICABLE",
    system_model="Pooled analysis of the tofersen clinical trial programme",
    is_human_system="TRUE",
    indication_population="SOD1 amyotrophic lateral sclerosis",
    arm_label="tofersen 100 mg intrathecal", arm_description="pooled trial participants",
    arm_role="exposed", cns_compartment="CSF_and_neuraxis",
    delivery_route="intrathecal_lumbar", dose_regimen="100 mg intrathecal",
    exposure_duration="trial programme duration", redistribution="summary_stat_only",
)

L3_ROWS = [
    dict(endpoint_tier="B", readout_category="csf_pressure",
         readout_name="intracranial_hypertension_or_papilledema_serious_AE",
         readout_value="4", readout_unit="events", n_affected="NOT_REPORTED",
         n_at_risk="NOT_REPORTED", grade=2,
         grade_basis=("2 = serious events of raised intracranial pressure and "
                      "papilloedema, named at SCHEMA.md rubric grade 2. The source "
                      "reports EVENTS, not participants, for this subtotal, so "
                      "n_affected is NOT_REPORTED rather than 4."),
         tox_axis="csf_pressure_disturbance", attribution="drug_attributed",
         evidence=("\"Ten participants (approximately 7% of tofersen 100-mg-treated "
                   "trial participants) experienced a total of 12 serious neurologic "
                   "AEs - 4 of myelitis, 2 of radiculitis, 2 of aseptic meningitis, and "
                   "4 of intracranial hypertension (ICH) and/or papilledema.\""),
         location="Abstract, Results"),
    dict(endpoint_tier="B", readout_category="csf_composition",
         readout_name="aseptic_meningitis_serious_AE",
         readout_value="2", readout_unit="events", n_affected="NOT_REPORTED",
         n_at_risk="NOT_REPORTED", grade=2,
         grade_basis=("2 = serious aseptic meningitis, named at SCHEMA.md rubric "
                      "grade 2. Reported as events, not participants."),
         tox_axis="csf_composition_disturbance", attribution="drug_attributed",
         evidence=("\"...2 of aseptic meningitis, and 4 of intracranial hypertension "
                   "(ICH) and/or papilledema. All events but one resolved either "
                   "spontaneously, with dosing interruption/modification, or with "
                   "concomitant therapies.\""),
         location="Abstract, Results"),
    dict(endpoint_tier="A", readout_category="hydrocephalus_event",
         readout_name="hydrocephalus_serious_AE", readout_value="0",
         readout_unit="events", n_affected=0, n_at_risk="NOT_REPORTED", grade=0,
         grade_basis=("0 = a dedicated review of the serious neurologic adverse events "
                      "in the tofersen programme enumerates myelitis, radiculitis, "
                      "aseptic meningitis and intracranial hypertension/papilloedema, "
                      "and names no hydrocephalus (SCHEMA.md rubric grade 0)."),
         tox_axis="ventricular_enlargement", attribution="not_discussed",
         evidence=("\"Ten participants ... experienced a total of 12 serious neurologic "
                   "AEs - 4 of myelitis, 2 of radiculitis, 2 of aseptic meningitis, and "
                   "4 of intracranial hypertension (ICH) and/or papilledema.\" The "
                   "enumeration is exhaustive for serious neurologic AEs and contains "
                   "no hydrocephalus term."),
         location="Abstract, Methods and Results"),
]


# --------------------------------------------------------------------------
# L4 — European Medicines Agency Summaries of Product Characteristics.
#      Included because the EU and US regulators reached MATERIALLY DIFFERENT
#      positions on the same evidence: the EMA gives hydrocephalus its own
#      subheading under section 4.4 "Special warnings and precautions for use"
#      for nusinersen, whereas the US label mentions it only in section 6.2
#      Postmarketing Experience. A jurisdiction contrast on an identical
#      molecule is a genuine datum about how strong the signal is judged to be.
#
#      Rights: EMA product information is publicly available, but the terms of
#      reuse were not established in this session, so every L4 row is marked
#      redistribution = verify rather than assumed public domain. The verbatim
#      text is quoted as evidence; a redistributor should resolve the licence
#      before republishing these rows' values.
# --------------------------------------------------------------------------
L4_ROWS = [
    dict(oligo="nusinersen", source_key="EMA_SmPC_Spinraza",
         file="sources/raw/sweep4_ema_smpc_spinraza.txt",
         tier="A", cat="hydrocephalus_event", axis="ventricular_enlargement",
         readout="ema_label_statement_hydrocephalus",
         value="communicating hydrocephalus not related to meningitis or bleeding",
         unit="verbatim_label_text", qualitative="TRUE",
         n_aff="NOT_REPORTED", n_risk="NOT_REPORTED", grade=3,
         basis=("3 = the EU label states that some affected patients required a "
                "ventriculo-peritoneal shunt, i.e. permanent CSF diversion "
                "(SCHEMA.md rubric grade 3)."),
         asc="measured_positive",
         evidence=('"Hydrocephalus. There have been reports of communicating '
                   'hydrocephalus not related to meningitis or bleeding in patients '
                   'treated with nusinersen 12 mg in the post-marketing setting. Some '
                   'patients were implanted with a ventriculo-peritoneal shunt. In '
                   'patients with decreased consciousness, an evaluation for '
                   'hydrocephalus should be considered."'),
         loc=("Annex I SmPC section 4.4 Special warnings and precautions for use, "
              "under its own subheading 'Hydrocephalus'")),
    dict(oligo="nusinersen", source_key="EMA_SmPC_Spinraza",
         file="sources/raw/sweep4_ema_smpc_spinraza.txt",
         tier="A", cat="shunt_or_drain_intervention", axis="ventricular_enlargement",
         readout="ema_label_statement_vp_shunt",
         value="ventriculo-peritoneal shunt implantation", unit="verbatim_label_text",
         qualitative="TRUE", n_aff="NOT_REPORTED", n_risk="NOT_REPORTED", grade=3,
         basis="3 = permanent CSF diversion (SCHEMA.md rubric grade 3).",
         asc="measured_positive",
         evidence=('"Some patients were implanted with a ventriculo-peritoneal shunt. '
                   '... The benefits and risks of nusinersen treatment in patients with '
                   'a ventriculo-peritoneal shunt are unknown at present and the '
                   'maintenance of treatment needs to be carefully considered."'),
         loc="Annex I SmPC section 4.4, subheading 'Hydrocephalus'"),
    dict(oligo="tofersen", source_key="EMA_SmPC_Qalsody",
         file="sources/raw/sweep4_ema_smpc_qalsody.pdf",
         tier="B", cat="csf_pressure", axis="csf_pressure_disturbance",
         readout="ema_serious_ICP_or_papilloedema_pct", value="2.7",
         unit="pct_of_participants", qualitative="FALSE",
         n_aff="NOT_REPORTED", n_risk=147, grade=2,
         basis=("2 = serious increased intracranial pressure and/or papilloedema, "
                "named at SCHEMA.md rubric grade 2."),
         asc="measured_positive",
         evidence=('"The serious adverse reactions in tofersen-treated participants '
                   'were myelitis (4.1%), increase intracranial pressure and/or '
                   'papilloedema (2.7%), radiculitis (1.4%) and aseptic meningitis '
                   '(1.4%)." Section 4.4 adds: "Serious cases of increased '
                   'intracranial pressure and/or papilloedema have been reported in '
                   'patients treated with tofersen."'),
         loc="Annex I SmPC sections 4.8 Undesirable effects and 4.4"),
    dict(oligo="tofersen", source_key="EMA_SmPC_Qalsody",
         file="sources/raw/sweep4_ema_smpc_qalsody.pdf",
         tier="B", cat="csf_composition", axis="csf_composition_disturbance",
         readout="ema_serious_aseptic_meningitis_pct", value="1.4",
         unit="pct_of_participants", qualitative="FALSE",
         n_aff="NOT_REPORTED", n_risk=147, grade=2,
         basis="2 = serious aseptic meningitis, named at SCHEMA.md rubric grade 2.",
         asc="measured_positive",
         evidence=('"The serious adverse reactions in tofersen-treated participants '
                   'were myelitis (4.1%), increase intracranial pressure and/or '
                   'papilloedema (2.7%), radiculitis (1.4%) and aseptic meningitis '
                   '(1.4%)."'),
         loc="Annex I SmPC section 4.8 Undesirable effects, Summary of safety profile"),
    dict(oligo="tofersen", source_key="EMA_SmPC_Qalsody",
         file="sources/raw/sweep4_ema_smpc_qalsody.pdf",
         tier="B", cat="csf_composition", axis="csf_composition_disturbance",
         readout="ema_csf_white_blood_cell_increased_pct", value="27.9",
         unit="pct_of_participants", qualitative="FALSE",
         n_aff="NOT_REPORTED", n_risk=147, grade=1,
         basis=("1 = a CSF composition change reported as a common adverse reaction "
                "with no stated symptom or intervention (SCHEMA.md rubric grade 1)."),
         asc="measured_positive",
         evidence=('"The most common adverse reactions reported in tofersen-treated '
                   'participants who received 100 mg (n=147) were pain (68.7%), '
                   'arthralgia (36.7%), fatigue (30.6%), CSF white blood cell increased '
                   '(27.9%), CSF protein increased (26.5%), myalgia (22.4%) and pyrexia '
                   '(20.4%)."'),
         loc="Annex I SmPC section 4.8, Summary of safety profile"),
    dict(oligo="tofersen", source_key="EMA_SmPC_Qalsody",
         file="sources/raw/sweep4_ema_smpc_qalsody.pdf",
         tier="B", cat="csf_composition", axis="csf_composition_disturbance",
         readout="ema_csf_protein_increased_pct", value="26.5",
         unit="pct_of_participants", qualitative="FALSE",
         n_aff="NOT_REPORTED", n_risk=147, grade=1,
         basis=("1 = a CSF composition change reported as a common adverse reaction "
                "with no stated symptom or intervention (SCHEMA.md rubric grade 1)."),
         asc="measured_positive",
         evidence=('"... CSF white blood cell increased (27.9%), CSF protein increased '
                   '(26.5%), myalgia (22.4%) and pyrexia (20.4%)."'),
         loc="Annex I SmPC section 4.8, Summary of safety profile"),
    dict(oligo="tofersen", source_key="EMA_SmPC_Qalsody",
         file="sources/raw/sweep4_ema_smpc_qalsody.pdf",
         tier="A", cat="hydrocephalus_event", axis="ventricular_enlargement",
         readout="ema_label_statement_hydrocephalus", value="NOT_REPORTED",
         unit="verbatim_label_text", qualitative="TRUE",
         n_aff=0, n_risk="NOT_REPORTED", grade=0,
         basis=("0 = the EU label for this product contains no occurrence of the "
                "string 'hydrocephal' anywhere in its 48,316 extracted characters, "
                "while naming four other CNS adverse reactions explicitly "
                "(SCHEMA.md rubric grade 0)."),
         asc="measured_null",
         evidence=("The label names myelitis, radiculitis, increased intracranial "
                   "pressure and/or papilloedema, and aseptic meningitis as serious "
                   "adverse reactions, and no hydrocephalus. A regulator that itemises "
                   "four CNS risks and omits a fifth is a stronger negative than "
                   "silence about the whole organ system."),
         loc="whole Annex I SmPC, full-text sweep for 'hydrocephal' (0 hits)"),
    dict(oligo="inotersen", source_key="EMA_SmPC_Tegsedi",
         file="sources/raw/sweep4_ema_smpc_tegsedi.txt",
         tier="A", cat="hydrocephalus_event", axis="ventricular_enlargement",
         readout="ema_label_statement_hydrocephalus", value="NOT_REPORTED",
         unit="verbatim_label_text", qualitative="TRUE",
         n_aff=0, n_risk="NOT_REPORTED", grade=0,
         basis=("0 = full-text sweep of the EU label returns zero occurrences of "
                "'hydrocephal', 'intracranial pressure', 'papilloedema' and 'aseptic "
                "meningitis' (SCHEMA.md rubric grade 0)."),
         asc="measured_null",
         evidence=("Nothing in the label bears on this endpoint. inotersen is dosed "
                   "subcutaneously, so this row also serves as a route contrast: the "
                   "systemic ASO label is silent where both intrathecal ASO labels are "
                   "not."),
         loc="whole Annex I SmPC, full-text sweep (0 hits for all four concepts)"),
]


# --------------------------------------------------------------------------
# L5 — Nakayama et al. 2026, Nature Medicine 32:1411-1420. "Antisense
#      oligonucleotide-mediated knockdown therapy in two infants with severe
#      KCNT1 epileptic encephalopathy". PMID 41981306, PMC13099374.
#      Licence: CC BY-NC-ND -> summary_stat_only.
#
#      THE SECOND INDEPENDENT DRUG-ATTRIBUTED SIGNAL, and the reason this
#      dataset does not call hydrocephalus a tominersen-specific finding. Two
#      n-of-1 patients dosed with valeriasen (KT777), a different ASO against a
#      different target in a different indication and age group, and BOTH
#      developed the endpoint. The authors state: "We therefore considered the
#      serious adverse events encountered in our two patients to be attributable
#      to dosing of the study drug", and frame it as "a potential monitorable
#      toxicity of some intrathecal antisense oligonucleotides".
#
#      It also differs MECHANISTICALLY from the tominersen index case. There the
#      authors diagnosed a sterile meningitis with CSF protein 2.64 g/L and
#      lymphocytosis; here CSF was negative for inflammatory biomarkers and the
#      authors' working hypothesis is a DOSE-RELATED effect. The reduced-dose
#      rechallenge in patient 2, delivered without recurrence, is the evidence
#      for that and is carried as its own row.
# --------------------------------------------------------------------------
L5 = dict(
    source_key="Nakayama_2026_NatMed_KCNT1",
    source_ref="PMID 41981306; PMC13099374; doi 10.1038/s41591-026-04314-9",
    file="sources/raw/sweep1_kcnt1_aso_infants_PMC13099374.xml",
    redistribution="summary_stat_only",
)

L5_ROWS = [
    # ---- patient 1 ----
    dict(pt="1", cluster="L5-PT1", tier="A", cat="hydrocephalus_event",
         axis="ventricular_enlargement", readout="communicating_hydrocephalus_diagnosed",
         value="severe communicating hydrocephalus with transependymal flow",
         unit="diagnosis", qual="TRUE", n_aff=1, grade=3, asc="measured_positive",
         dose="60 mg every 8 weeks intrathecal (escalated from 40 mg q8w at week 26)",
         time="8 weeks after the 9th intrathecal dose",
         basis=("3 = hydrocephalus requiring a CSF-diversion procedure; an endoscopic "
                "third ventriculostomy with choroid plexus cauterization was performed, "
                "it did not relieve the hydrocephalus, and goals of care were redirected "
                "to palliative care (SCHEMA.md rubric grade 3)."),
         ev=('"Brain and spine imaging was obtained 2 days later and revealed severe '
             'communicating hydrocephalus with T2 white matter changes representing '
             'transependymal flow but no other parenchymal changes." Attribution: "We '
             'therefore considered the serious adverse events encountered in our two '
             'patients to be attributable to dosing of the study drug."'),
         loc="Results, 'Safety and adverse events', patient 1 paragraph"),
    dict(pt="1", cluster="L5-PT1", tier="B", cat="csf_pressure",
         axis="csf_pressure_disturbance", readout="CSF_opening_pressure",
         value="55", unit="cmH2O", qual="FALSE", n_aff=1, grade=2,
         asc="measured_positive",
         dose="60 mg every 8 weeks intrathecal",
         time="at endoscopic third ventriculostomy",
         basis=("2 = measured raised intracranial pressure (SCHEMA.md rubric grade 2). "
                "The grade-3 consequence is carried by the sibling hydrocephalus and "
                "diversion-procedure rows in the same event cluster."),
         ev=('"An endoscopic third ventriculostomy with choroid plexus cauterization was '
             'performed, showing a CSF opening pressure of 55 cm H2O."'),
         loc="Results, 'Safety and adverse events', patient 1 paragraph"),
    dict(pt="1", cluster="L5-PT1", tier="A", cat="shunt_or_drain_intervention",
         axis="ventricular_enlargement",
         readout="endoscopic_third_ventriculostomy_choroid_plexus_cauterization",
         value="endoscopic third ventriculostomy with choroid plexus cauterization",
         unit="intervention", qual="TRUE", n_aff=1, grade=3, asc="measured_positive",
         dose="60 mg every 8 weeks intrathecal", time="after diagnosis",
         basis=("3 = a CSF-diversion procedure was performed (SCHEMA.md rubric "
                "grade 3)."),
         ev=('"No improvement in hydrocephalus was seen over the following 2 days. '
             'After considering ventriculoperitoneal shunt placement, and mindful of the '
             'seriousness of her disease course before experimental therapy, the family '
             'withdrew from the investigational protocol in favor of palliative care."'),
         loc="Results, 'Safety and adverse events', patient 1 paragraph"),
    # ---- patient 2 ----
    dict(pt="2", cluster="L5-PT2", tier="A", cat="ventricular_morphometry",
         axis="ventricular_enlargement", readout="ventricular_size_MRI",
         value="normal ventricular size", unit="qualitative_imaging", qual="TRUE",
         n_aff=0, grade=0, asc="measured_null",
         dose="escalating intrathecal 10, 20, 30, 40 mg", time="day 55",
         basis=("0 = brain MRI performed and reported as unremarkable including normal "
                "ventricular size (SCHEMA.md rubric grade 0). A WITHIN-PATIENT negative "
                "seven days before the same patient's ventricular enlargement, which is "
                "the strongest form of negative in this dataset."),
         ev=('"A brain MRI was unremarkable (including normal ventricular size) '
             '(day 55). Lumbar puncture showed a normal opening pressure of 16 cm H2O."'),
         loc="Results, 'Safety and adverse events', patient 2 paragraph"),
    dict(pt="2", cluster="L5-PT2", tier="B", cat="csf_composition",
         axis="csf_composition_disturbance", readout="CSF_white_cells_and_protein",
         value="WBC 28 cells/mm3; protein 83 mg/dL", unit="mixed", qual="FALSE",
         n_aff=1, grade=1, asc="measured_positive",
         dose="escalating intrathecal 10, 20, 30, 40 mg", time="day 55",
         basis=("1 = mild CSF composition change, described by the source as slightly "
                "elevated and normalising on follow-up, with no intervention "
                "(SCHEMA.md rubric grade 1)."),
         ev=('"CSF WBCs and protein were slightly elevated at 28 cells mm-3 and 83 mg '
             'dl-1, respectively (and follow-up cell counts and protein levels were '
             'normal)."'),
         loc="Results, 'Safety and adverse events', patient 2 paragraph"),
    dict(pt="2", cluster="L5-PT2", tier="A", cat="ventricular_morphometry",
         axis="ventricular_enlargement", readout="ventricular_size_MRI",
         value="mild increase in ventricular size, no evidence of obstruction",
         unit="qualitative_imaging", qual="TRUE", n_aff=1, grade=2,
         asc="measured_positive",
         dose="escalating intrathecal 10, 20, 30, 40 mg", time="days 62 and 64",
         basis=("2 = symptomatic ventricular enlargement leading to intensive-care "
                "transfer and intervention (SCHEMA.md rubric grade 2); the grade-3 "
                "consequence is carried by the drain and shunt rows in the same "
                "event cluster."),
         ev=('"While the initial brain MRI (day 55) had been unremarkable, repeat MRIs '
             'performed on days 62 and 64 showed mild increases in ventricular size. '
             'There was no evidence of obstruction."'),
         loc="Results, 'Safety and adverse events', patient 2 paragraph"),
    dict(pt="2", cluster="L5-PT2", tier="A", cat="shunt_or_drain_intervention",
         axis="ventricular_enlargement", readout="external_ventricular_drain",
         value="extraventricular drain, opening pressure >20 cmH2O",
         unit="intervention", qual="TRUE", n_aff=1, grade=3, asc="measured_positive",
         dose="escalating intrathecal 10, 20, 30, 40 mg", time="day 64",
         basis="3 = an external ventricular drain was placed (SCHEMA.md rubric grade 3).",
         ev=('"Given the hydrocephalus found in patient 1, patient 2 was transferred to '
             'the pediatric intensive care unit for closer neurologic monitoring, where '
             'an extraventricular drain was placed. Opening pressure was >20 cm H2O."'),
         loc="Results, 'Safety and adverse events', patient 2 paragraph"),
    dict(pt="2", cluster="L5-PT2", tier="A", cat="shunt_or_drain_intervention",
         axis="ventricular_enlargement", readout="ventriculoperitoneal_shunt_inserted",
         value="ventriculoperitoneal shunt", unit="intervention", qual="TRUE",
         n_aff=1, grade=3, asc="measured_positive",
         dose="escalating intrathecal 10, 20, 30, 40 mg", time="day 65",
         basis=("3 = permanent CSF diversion performed (SCHEMA.md rubric grade 3)."),
         ev=('"There was persistent drainage through the extraventricular drain, and a '
             'ventriculoperitoneal shunt was placed on day 65. Ventricular dilatation '
             'gradually normalized on serial MR ventriculograms, and she was discharged '
             'to home in stable condition on day 87."'),
         loc="Results, 'Safety and adverse events', patient 2 paragraph"),
    dict(pt="2", cluster="L5-PT2", tier="B", cat="csf_composition",
         axis="csf_composition_disturbance", readout="CSF_inflammatory_biomarkers",
         value="negative", unit="qualitative_panel", qual="TRUE", n_aff=0, grade=0,
         asc="measured_null",
         dose="escalating intrathecal 10, 20, 30, 40 mg", time="after the event",
         basis=("0 = an inflammatory CSF panel was performed and was negative "
                "(SCHEMA.md rubric grade 0). MECHANISTICALLY LOAD-BEARING: the "
                "tominersen index case attributed its hydrocephalus to a sterile "
                "meningitis with CSF protein 2.64 g/L and lymphocytosis, whereas here "
                "the same endpoint occurs with a negative inflammatory panel and a "
                "dose-related working hypothesis. The two cases support different "
                "mechanisms and must not be pooled as one."),
         ev=('"CSF testing was negative for inflammatory biomarkers (albumin, IgG index, '
             'oligoclonal bands and neoptyrin) ... A review of preclinical and clinical '
             'findings led to our working hypothesis that hydrocephalus was a '
             'dose-related clinical side effect."'),
         loc="Results, 'Safety and adverse events', closing paragraph"),
    dict(pt="2", cluster="L5-PT2-RECHALLENGE", tier="A", cat="ventricular_morphometry",
         axis="ventricular_enlargement", readout="reduced_dose_rechallenge_no_recurrence",
         value="no recurrence", unit="qualitative_imaging", qual="TRUE", n_aff=0,
         grade=0, asc="measured_null",
         dose=("reduced: 2 intrathecal doses (10 mg, 15 mg) then 5 intracerebroventricular "
               "doses (3, 3, 6, 6, 9 mg), each 2 months apart"),
         time="after a 2-year hiatus",
         basis=("0 = rechallenge at reduced dose under a revised protocol with periodic "
                "MRI ventriculograms and per-lumbar-puncture opening pressures, "
                "delivered without recurrence of the endpoint (SCHEMA.md rubric "
                "grade 0). This is the dataset's only DECHALLENGE/REDUCED-DOSE "
                "RECHALLENGE row and is the direct evidence for the authors' "
                "dose-related hypothesis."),
         ev=('"A revised protocol was developed, using lower doses, periodic MRI '
             'ventriculograms and opening pressure measurements with each lumbar '
             'puncture. ASO administration for patient 2 resumed after a 2-year hiatus. '
             'Two IT doses (10 mg and 15 mg, spaced 2 months apart) and five ICV doses '
             '(3 mg, 3 mg, 6 mg, 6 mg, 9 mg, spaced 2 months apart) were safely '
             'delivered."'),
         loc="Results, 'Safety and adverse events', closing paragraph"),
]

BLANK = dict(
    strain="NOT_APPLICABLE", dose_value="NOT_REPORTED", dose_unit="NOT_APPLICABLE",
    timepoint="NOT_REPORTED", seriousness="NOT_REPORTED",
    assessment_type="investigator_diagnosis", organ_system="NOT_APPLICABLE",
    source_vocabulary="NOT_APPLICABLE", n_affected_comparator="NOT_APPLICABLE",
    n_at_risk_comparator="NOT_APPLICABLE", comparator_arm="NOT_APPLICABLE",
    statistic="NOT_REPORTED", readout_term_verbatim="NOT_APPLICABLE",
)


def row(**kw):
    base = dict(BLANK)
    base.update(kw)
    return base


def main():
    os.makedirs(DATA, exist_ok=True)
    rows = []

    # ---- L1: Stoker 2021 -------------------------------------------------
    for i, r in enumerate(L1_ROWS, 1):
        rows.append(row(
            oligo_name="tominersen", source_key=L1["source_key"],
            study_type=L1["study_type"], species=L1["species"],
            system_model=L1["system_model"], is_human_system=L1["is_human_system"],
            indication_population=L1["indication_population"],
            arm_label=L1["arm_label"], arm_description=L1["arm_description"],
            arm_role=L1["arm_role"], cns_compartment=L1["cns_compartment"],
            delivery_route=L1["delivery_route"],
            exposure_duration=L1["exposure_duration"],
            timepoint="after the fifth monthly dose and over the following 3 months",
            endpoint_tier=r["endpoint_tier"], readout_category=r["readout_category"],
            readout_name=r["readout_name"], readout_value=r["readout_value"],
            readout_unit=r["readout_unit"],
            readout_is_qualitative=r["readout_is_qualitative"],
            n_affected=r["n_affected"], n_at_risk=r["n_at_risk"],
            effect_direction="increase",
            effect_vs_control=("within-patient: the same patient received four doses of "
                               "intrathecal placebo in the prior trial without this "
                               "syndrome"),
            hydroceph_grade=r["grade"], grade_basis=r["grade_basis"],
            grade_status="provisional",
            ascertainment="measured_positive",
            ascertainment_basis=("Actively investigated: serial MRI, serial CSF "
                                 "sampling and a lumbar infusion study were performed "
                                 "because of the clinical deterioration."),
            attribution_as_stated=r["attribution"],
            attribution_evidence=r["evidence"],
            tox_axis=r["tox_axis"],
            event_cluster_id="L1-EVT-01",
            source_ref=L1["source_ref"], source_location=r["location"],
            redistribution=L1["redistribution"],
            notes=("Rows L1-EVT-01 (%d of %d) describe ONE patient and ONE clinical "
                   "episode. They are separate measurements of that episode, not "
                   "independent events, and must not be counted as such. Full text "
                   "committed at sources/raw/sweep1_stoker2021_PMC7894279_fulltext.xml. "
                   "Retrieved %s." % (i, len(L1_ROWS), TODAY)),
        ))

    # ---- L2: Viscidi 2021 background incidence ---------------------------
    for r in L2_ROWS:
        rows.append(row(
            oligo_name="NOT_APPLICABLE", source_key=L2["source_key"],
            study_type=L2["study_type"], species=L2["species"],
            system_model=L2["system_model"], is_human_system=L2["is_human_system"],
            indication_population=r["population"], arm_label=r["arm_label"],
            arm_description=L2["arm_description"], arm_role=r["arm_role"],
            cns_compartment=L2["cns_compartment"],
            delivery_route=L2["delivery_route"],
            exposure_duration=L2["exposure_duration"],
            timepoint="study period 2007-01-01 to 2016-12-22",
            endpoint_tier="A", readout_category="hydrocephalus_event",
            readout_name=r["readout_name"], readout_value=r["readout_value"],
            readout_unit=r["readout_unit"], readout_is_qualitative="FALSE",
            n_affected=r["n_affected"], n_at_risk=r["n_at_risk"],
            comparator_arm=r["comparator"], n_affected_comparator=r["n_aff_comp"],
            n_at_risk_comparator=r["n_risk_comp"], statistic=r["statistic"],
            effect_direction="increase", effect_vs_control="see statistic",
            hydroceph_grade="", grade_basis=(
                "NOT GRADED. This row is a population incidence rate, not a per-subject "
                "severity, so the 0-3 rubric does not apply. It exists to give the "
                "drug-exposed rows a disease baseline."),
            grade_status="not_graded",
            ascertainment="measured_positive",
            ascertainment_basis=("Systematic ascertainment by ICD-9/ICD-10 diagnosis "
                                 "code in a 100-million-person EHR database over a "
                                 "defined study window."),
            attribution_as_stated="disease_attributed",
            attribution_evidence=r["evidence"], tox_axis="disease_background_rate",
            event_cluster_id="L2-BASELINE",
            source_ref=L2["source_ref"], source_location=r["location"],
            redistribution=L2["redistribution"],
            notes=("NO DRUG EXPOSURE. The study window ends at nusinersen approval, so "
                   "this is a disease baseline uncontaminated by the drug. Any analysis "
                   "attributing hydrocephalus to an SMA-indicated oligonucleotide must "
                   "be read against these rows. Exclude from compound-level toxicity "
                   "analyses (tox_axis = disease_background_rate). Full text at "
                   "sources/raw/sweep1_sma_hydro_incidence_PMC8105953.xml. Retrieved "
                   "%s." % TODAY),
        ))

    # ---- L3: tofersen serious neurologic AEs -----------------------------
    for r in L3_ROWS:
        rows.append(row(
            oligo_name="tofersen", source_key=L3["source_key"],
            study_type=L3["study_type"], species=L3["species"],
            system_model=L3["system_model"], is_human_system=L3["is_human_system"],
            indication_population=L3["indication_population"],
            arm_label=L3["arm_label"], arm_description=L3["arm_description"],
            arm_role=L3["arm_role"], cns_compartment=L3["cns_compartment"],
            delivery_route=L3["delivery_route"],
            exposure_duration=L3["exposure_duration"],
            timepoint="trial programme", endpoint_tier=r["endpoint_tier"],
            readout_category=r["readout_category"], readout_name=r["readout_name"],
            readout_value=r["readout_value"], readout_unit=r["readout_unit"],
            readout_is_qualitative="FALSE", n_affected=r["n_affected"],
            n_at_risk=r["n_at_risk"],
            statistic="approximately 7% of tofersen 100-mg-treated trial participants "
                      "experienced any of the 12 serious neurologic AEs",
            effect_direction=("no_change" if r["grade"] == 0 else "increase"),
            effect_vs_control="NOT_REPORTED",
            hydroceph_grade=r["grade"], grade_basis=r["grade_basis"],
            grade_status="provisional",
            ascertainment=("measured_null" if r["grade"] == 0 else "measured_positive"),
            ascertainment_basis=("Serious adverse events defined per ICH guidance and "
                                 "diagnosed by investigators on symptoms, examination "
                                 "and diagnostic workup, as stated in the source's "
                                 "Methods."),
            attribution_as_stated=r["attribution"], attribution_evidence=r["evidence"],
            tox_axis=r["tox_axis"], event_cluster_id="L3-TOFERSEN-SAE",
            source_ref=L3["source_ref"], source_location=r["location"],
            redistribution=L3["redistribution"],
            notes=("Licence is CC BY-NC-ND; only abstract-level summary statistics are "
                   "carried and no underlying table is reproduced. Counts are EVENTS, "
                   "not participants. Full text at "
                   "sources/raw/sweep1_tofersen_seriousAE_PMC12060635.xml. Retrieved "
                   "%s." % TODAY),
        ))

    # ---- L4: EMA Summaries of Product Characteristics --------------------
    for r in L4_ROWS:
        rows.append(row(
            oligo_name=r["oligo"], source_key=r["source_key"],
            study_type="regulatory_label", species="human",
            system_model="EMA Annex I Summary of Product Characteristics",
            is_human_system="TRUE",
            indication_population=("spinal_muscular_atrophy" if r["oligo"] == "nusinersen"
                                   else "SOD1_amyotrophic_lateral_sclerosis"
                                   if r["oligo"] == "tofersen"
                                   else "hereditary_transthyretin_amyloidosis"),
            arm_label="EU labelled population", arm_description="NOT_APPLICABLE",
            arm_role="exposed",
            cns_compartment=("NOT_APPLICABLE" if r["oligo"] == "inotersen"
                             else "CSF_and_neuraxis"),
            delivery_route=("subcutaneous" if r["oligo"] == "inotersen"
                            else "intrathecal_lumbar"),
            exposure_duration="NOT_APPLICABLE", timepoint="NOT_APPLICABLE",
            endpoint_tier=r["tier"], readout_category=r["cat"],
            readout_name=r["readout"], readout_value=r["value"],
            readout_unit=r["unit"], readout_is_qualitative=r["qualitative"],
            n_affected=r["n_aff"], n_at_risk=r["n_risk"],
            statistic=("denominator n=147 is stated by the label for its "
                       "common-adverse-reaction sentence; the serious-reaction "
                       "percentages are consistent with the same denominator "
                       "(2.7% x 147 = 4.0; 1.4% x 147 = 2.1) but the label does not "
                       "restate it, so this consistency is corroboration, not a "
                       "denominator the label asserts for those rows."
                       if r["n_risk"] == 147 else "NOT_REPORTED"),
            effect_direction=("no_change" if r["grade"] == 0 else "increase"),
            effect_vs_control="NOT_REPORTED",
            hydroceph_grade=r["grade"], grade_basis=r["basis"],
            grade_status="provisional", ascertainment=r["asc"],
            ascertainment_basis=(
                "A regulatory label states identified risks. It is not a record of "
                "everything looked for and not found, so a silent label is a weaker "
                "negative than a trial-arm zero - except where, as here, the same "
                "label itemises several neighbouring risks and omits this one."),
            attribution_as_stated=("drug_attributed" if r["grade"] else "not_discussed"),
            attribution_evidence=r["evidence"], tox_axis=r["axis"],
            event_cluster_id="NOT_APPLICABLE", source_ref=r["source_key"],
            source_location=r["loc"], redistribution="verify",
            notes=("EMA product information. Rights of reuse were not established in "
                   "this session, so redistribution is 'verify': the verbatim text is "
                   "quoted as evidence and a redistributor should resolve the licence "
                   "before republishing the value. Retrieved document at %s. "
                   "Retrieved %s." % (r["file"], TODAY)),
        ))

    # ---- L5: KCNT1 n-of-1 ASO, two patients ------------------------------
    for r in L5_ROWS:
        rows.append(row(
            oligo_name="valeriasen", source_key=L5["source_key"],
            study_type="clinical_case", species="human",
            system_model=("n-of-1 investigational protocol, patient %s of 2; "
                          "2-year-old girl with de novo KCNT1 p.Arg474His epilepsy of "
                          "infancy with migrating focal seizures" % r["pt"]),
            is_human_system="TRUE",
            indication_population="KCNT1 developmental and epileptic encephalopathy",
            arm_label="valeriasen (KT777), intrathecal",
            arm_description=r["dose"], arm_role="exposed",
            cns_compartment="lateral_ventricles", delivery_route="intrathecal_lumbar",
            dose_value="NOT_REPORTED", dose_unit="NOT_APPLICABLE",
            dose_regimen=r["dose"], exposure_duration="NOT_REPORTED",
            timepoint=r["time"], endpoint_tier=r["tier"],
            readout_category=r["cat"], readout_name=r["readout"],
            readout_value=r["value"], readout_unit=r["unit"],
            readout_is_qualitative=r["qual"], n_affected=r["n_aff"], n_at_risk=2,
            comparator_arm="NOT_APPLICABLE",
            effect_direction=("no_change" if r["grade"] == 0 else "increase"),
            effect_vs_control=("both patients in this two-patient protocol developed the "
                               "endpoint; there is no untreated comparator"),
            hydroceph_grade=r["grade"], grade_basis=r["basis"],
            grade_status="provisional", ascertainment=r["asc"],
            ascertainment_basis=(
                "Actively investigated. After the first patient's event the protocol was "
                "revised to require periodic MRI ventriculograms and an opening-pressure "
                "measurement at every lumbar puncture, so later rows are "
                "protocol-specified rather than incidental."),
            attribution_as_stated=("drug_attributed" if r["grade"] else "not_discussed"),
            attribution_evidence=r["ev"], tox_axis=r["axis"],
            event_cluster_id=r["cluster"], source_ref=L5["source_ref"],
            source_location=r["loc"], redistribution=L5["redistribution"],
            notes=("Licence CC BY-NC-ND: summary statistics and short quoted evidence "
                   "only; no table or figure is reproduced. Sequences and per-position "
                   "chemistry for valeriasen exist in the source's Extended Data Table 1 "
                   "but are published as an IMAGE in which 2'-MOE positions are encoded "
                   "by bold and underline, which does not survive text extraction; they "
                   "are therefore NOT transcribed here (METHODOLOGY.md OI-02). Full "
                   "text at %s. Retrieved %s." % (L5["file"], TODAY)),
        ))

    out = os.path.join(DATA, "_literature_measurements.csv")
    cols = sorted({k for r in rows for k in r})
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("wrote %s: %d rows" % (out, len(rows)))
    for r in rows:
        print("  %-12s tier %s  %-46s %s" % (
            r["oligo_name"][:12], r["endpoint_tier"], r["readout_name"][:46],
            str(r["readout_value"])[:34]))


if __name__ == "__main__":
    main()
