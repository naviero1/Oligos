#!/usr/bin/env python3
"""
The data dictionary, in one place.

This module is the single definition of what every column in every table means.
It is imported by `scripts/export_xlsx.py`, which renders it as the workbook's
`data_dictionary` sheet, and by `qc/validate.py`, which asserts that **every
column present in every CSV has an entry here and every entry corresponds to a
real column**.

That check exists because of a defect in this release's own history: `SCHEMA.md`
declared `purity_pct`, `purity_method` and `identity_confirmation` while the
builder emitted none of them, and nothing caught it — the same
documentation-versus-data drift the sibling kidney dataset was reviewed for. A
prose schema cannot be enforced. This can.
"""

DICTIONARY = {
    "oligos": {
        "oligo_id": "Primary key. Stable identifier, e.g. HYD-OLG-0001. Never reused.",
        "oligo_name": "Common or INN name; the join key used by the build scripts.",
        "aliases": "Other names, semicolon separated.",
        "oligo_class": "ASO_gapmer | ASO_mixmer | splice_switching_ASO | siRNA | "
                       "divalent_siRNA | PMO | aptamer | vehicle_control | other | "
                       "NOT_APPLICABLE",
        "modality": "single_stranded_ASO | double_stranded_siRNA | vehicle | "
                    "NOT_REPORTED | NOT_APPLICABLE",
        "target_gene": "Intended target gene symbol, or none_no_transcriptome_match "
                       "for scrambles.",
        "indication": "Disease or research context.",
        "developer": "Originating organisation.",
        "max_phase": "Highest development phase reached, or research_panel.",
        "route_of_administration": "Route the compound is dosed by in clinical or "
                                   "study use. Context, not an endpoint claim.",
        "length_nt": "Length in nucleotides. See length_nt_basis for how it was "
                     "established.",
        "length_nt_basis": "stated_in_label | counted_from_published_sequence | "
                           "derived_from_molecular_formula (with the derivation "
                           "spelled out) | NOT_REPORTED.",
        "sequence_5to3_asprinted": "Sequence exactly as printed by the source, "
                                   "preserving any case convention that encodes "
                                   "chemistry. For duplexes this is the antisense "
                                   "(guide) strand; the sense strand is in notes. "
                                   "NEVER guessed.",
        "sequence_base": "Nucleobase sequence, upper case, chemistry stripped.",
        "sequence_source": "Exact document and locus the sequence came from.",
        "backbone_chemistry": "full_PS | mixed_PO_PS | no_PS | PMO_neutral | "
                              "NOT_REPORTED",
        "sugar_modifications": "Sugar chemistry summary, semicolon separated.",
        "modification_pattern": "The design motif in the source's own terms, e.g. "
                                "5-10-5.",
        "gapmer_shape": "gapmer | mixmer | uniform | NOT_APPLICABLE",
        "molecular_formula": "Molecular formula as printed by the label.",
        "molecular_weight": "Molecular weight as printed by the label.",
        "conjugate": "Conjugated moiety, or NOT_REPORTED.",
        "formulation": "Vehicle the compound is dosed in, where the label states it. "
                       "Divalent-cation content is noted because the CNS "
                       "oligonucleotide literature treats it as material.",
        "purity_pct": "Reported purity percentage. NOT_REPORTED for every compound "
                      "in this release: no US label states drug-substance purity.",
        "purity_method": "Purification method, verbatim from the source, or "
                         "NOT_REPORTED.",
        "identity_confirmation": "How identity was confirmed (e.g. RP-UPLC-MS), "
                                 "verbatim, or NOT_REPORTED.",
        "synthesis_platform": "Synthesiser/supplier as stated, or NOT_REPORTED.",
        "design_source_text": "JSON of the verbatim label sentences each parsed "
                              "design value was matched from, so the parse is "
                              "checkable without opening the label.",
        "identity_source": "Document establishing the compound's identity and route.",
        "source_location": "Exact locus within that document.",
        "redistribution": "Rights status governing reproduction of this row.",
        "notes": "Free text.",
    },
    "measurements": {
        "measurement_id": "Primary key, e.g. HYD-MSR-00001.",
        "oligo_id": "Foreign key to oligos.oligo_id.",
        "oligo_name": "Denormalised compound name, for readability.",
        "source_id": "Foreign key to sources.source_id.",
        "study_type": "clinical_trial | clinical_case | pharmacovigilance | "
                      "animal_invivo | in_vitro | background_epidemiology | "
                      "regulatory_label",
        "species": "human | mouse | rat | monkey | pig | multi_species",
        "subject_class": "The human/animal and in vivo/in vitro division, in one "
                         "column: human_in_vivo | human_in_vitro | human_population "
                         "| animal_in_vivo | animal_in_vitro | not_applicable. "
                         "Derived deterministically from (species, study_type) and "
                         "re-derived by the QC suite, which fails on any "
                         "disagreement. human_population marks a population "
                         "incidence rate — human subjects, but no individual dosed "
                         "and no per-subject observation, so it must not be pooled "
                         "with trial rows. Generated views data/measurements_human.csv "
                         "and data/measurements_animal.csv are filters on this "
                         "column.",
        "strain": "Strain, sex and age where stated.",
        "system_model": "Trial design, cohort, animal model or culture system.",
        "is_human_system": "TRUE if measured in a human or human-derived system.",
        "indication_population": "Disease population dosed — the confounding "
                                 "variable for this endpoint.",
        "arm_label": "The trial arm, cohort or group this row describes.",
        "arm_description": "The arm's own description, as the source gives it.",
        "arm_role": "exposed | comparator | disease_background",
        "cns_compartment": "lateral_ventricles | whole_ventricular_system | CSF | "
                           "choroid_plexus | ependyma | subarachnoid_space | "
                           "CSF_and_neuraxis | NOT_APPLICABLE",
        "delivery_route": "intrathecal_lumbar | intracerebroventricular | "
                          "intraparenchymal | intravenous | subcutaneous | "
                          "intravitreal | in_culture_medium | NOT_APPLICABLE",
        "dose_value": "Dose as stated.",
        "dose_unit": "Unit of dose_value.",
        "dose_regimen": "Dosing regimen as stated.",
        "exposure_duration": "Duration of exposure as stated.",
        "timepoint": "When the readout was taken.",
        "endpoint_tier": "A = ventricular/CSF-volume outcome. B = CSF-dynamics "
                         "adjacent (pressure, composition, flow, procedure). Never "
                         "pool the two without saying so.",
        "readout_category": "hydrocephalus_event | ventricular_morphometry | "
                            "shunt_or_drain_intervention | csf_pressure | "
                            "csf_composition | csf_dynamics | procedure_complication "
                            "| histopathology_choroid_ependyma",
        "readout_name": "The specific readout.",
        "readout_term_verbatim": "The source's own term, unnormalised and never "
                                 "spelling-corrected.",
        "readout_value": "The value exactly as reported, or NOT_REPORTED.",
        "readout_unit": "Unit of readout_value.",
        "readout_is_qualitative": "TRUE where the source reports the result only in "
                                  "words or only as a figure. No number is ever read "
                                  "off a figure.",
        "n_affected": "Participants/animals with the event in this arm.",
        "n_at_risk": "Denominator of this arm.",
        "comparator_arm": "What this arm is compared against.",
        "n_affected_comparator": "Events in the comparator arm.",
        "n_at_risk_comparator": "Denominator of the comparator arm.",
        "statistic": "Dispersion, CI or significance AS STATED by the source. This "
                     "dataset computes no inferential statistic of its own.",
        "effect_direction": "increase | decrease | no_change | NOT_APPLICABLE",
        "effect_vs_control": "The comparison as stated, including the comparator "
                             "value.",
        "seriousness": "Regulatory seriousness classification where the source gives "
                       "one.",
        "assessment_type": "How the observation was made (registry assessment type, "
                           "protocol-specified outcome measure, spontaneous report, "
                           "investigator diagnosis).",
        "organ_system": "System organ class where the source assigns one.",
        "source_vocabulary": "Coding vocabulary and version where stated.",
        "hydroceph_grade": "Ordinal severity 0-3. Blank where the readout is "
                           "continuous or protective and not graded.",
        "grade_basis": "The exact rule that produced the grade. A grade with no "
                       "stated basis is a defect.",
        "grade_status": "provisional | expert_confirmed | not_graded",
        "ascertainment": "measured_positive | measured_null | "
                         "reported_threshold_limited | not_assessed. A grade of 0 is "
                         "permitted only where this is measured_null.",
        "ascertainment_basis": "How that was established, citing the source's own "
                               "statement or the governing reporting rule.",
        "attribution_as_stated": "What the SOURCE concluded about causation: "
                                 "drug_attributed | procedure_attributed | "
                                 "disease_attributed | multifactorial | undetermined "
                                 "| not_discussed. Never this dataset's inference.",
        "attribution_evidence": "The source's reasoning, quoted or summarised.",
        "tox_axis": "ventricular_enlargement | csf_pressure_disturbance | "
                    "csf_composition_disturbance | csf_dynamics | "
                    "delivery_procedure_complication | disease_background_rate | "
                    "therapeutic_ventricular_effect",
        "event_cluster_id": "Rows sharing a value describe ONE clinical episode in "
                            "the same subject(s) and must not be counted as "
                            "independent events.",
        "source_ref": "Citation key, DOI, PMID, NCT id, DailyMed set id or API query.",
        "source_location": "Exact locus — a JSON path, a label section with its LOINC "
                           "code, or a table/figure identifier. A category word such "
                           "as 'results' is rejected by the QC suite.",
        "redistribution": "public_domain | cc_by | cc_by_nc | summary_stat_only | "
                          "derived_features_only | verify",
        "notes": "Free text.",
    },
    "modifications": {
        "oligo_id": "Foreign key to oligos.oligo_id.",
        "oligo_name": "Denormalised compound name, for readability.",
        "strand": "single_strand | antisense_guide | sense.",
        "position_5to3": "1-based position from the 5' end. Contiguous 1..n, and n "
                         "must equal oligos.length_nt.",
        "nucleobase": "A | C | G | T | U | NOT_REPORTED.",
        "sugar_chemistry": "2'-MOE | DNA_2prime_deoxy | LNA | morpholino | 2'-OMe | "
                           "2'-F | RNA_2prime_OH | NOT_REPORTED.",
        "base_modification": "e.g. 5-methylcytosine, or NOT_REPORTED.",
        "linkage_3prime": "Linkage to the next nucleotide, terminal_none at the 3' "
                          "end, or NOT_REPORTED.",
        "basis": "How this position was established: "
                 "position_resolved_from_source_motif_statement | "
                 "position_resolved_from_source_uniform_chemistry_statement | "
                 "position_resolved_from_published_sequence.",
        "source_id": "Foreign key to sources.source_id.",
        "source_location": "Exact locus within that source.",
        "notes": "Free text, including what could NOT be resolved and why.",
    },
    "sources": {
        "source_id": "Primary key.",
        "source_key": "Short citation key.",
        "citation": "Full citation.",
        "first_author": "First author, or NOT_APPLICABLE for registry/regulatory "
                        "sources.",
        "year": "Publication or retrieval year.",
        "journal": "Journal, or NOT_APPLICABLE.",
        "doi": "DOI where one exists.",
        "pmid": "PubMed id where one exists.",
        "pmcid": "PubMed Central id where one exists.",
        "nct_id": "ClinicalTrials.gov id where one exists.",
        "url": "Canonical URL.",
        "access": "open_access | public_domain | subscription | api",
        "license": "Licence as stated by the source.",
        "redistribution": "Rights status governing reproduction of values from this "
                          "source.",
        "evidence_tier": "regulatory_primary | registry_results | primary_fulltext | "
                         "primary_supplementary_data | pharmacovigilance_api | "
                         "case_report | epidemiology | review_secondary",
        "retrieved_via": "The exact retrieval route, so any value can be re-fetched.",
        "retrieved_date": "Date of retrieval.",
        "n_oligos": "Oligonucleotides this source contributes. Recomputed, never "
                    "typed.",
        "n_measurements": "Measurement rows this source contributes. Recomputed, "
                          "never typed.",
        "notes": "Free text.",
    },
}
