# Schema — OligoTox-Hydrocephalus

Data dictionary, controlled vocabularies and the grading rubric for the
**hydrocephalus** endpoint of the NIH/NCATS Oligonucleotide Toxicity (OligoTox)
Open Data Challenge, Phase 2.

Three normalized UTF-8 CSV tables. `oligos` and `measurements` join on `oligo_id`;
both carry `source_id` into `sources`.

| File | Grain | Key |
|---|---|---|
| `data/oligos.csv` | one row per oligonucleotide — identity and design predictors | `oligo_id` (PK) |
| `data/measurements.csv` | one row per oligo × population/model × route × dose × readout × arm | `measurement_id` (PK), `oligo_id` (FK) |
| `data/sources.csv` | provenance registry | `source_id` (PK) |

`data/hydrocephalus_merged.csv` is a **generated** denormalized join of the first
two, produced by `scripts/build_merged.py`. It is never hand-edited.

---

## Missing-value convention

Inherited from the sibling **OligoTox-CNS** release so the two datasets can be
pooled. Three distinct states, never collapsed:

| Literal | Meaning |
|---|---|
| `NOT_REPORTED` | The source does not report this value. It has **not** been estimated, imputed, or filled from background knowledge. |
| `NOT_APPLICABLE` | The field has no meaning for this row (e.g. a comparator arm for a single-arm case report). |
| *(empty cell)* | The field does not apply to this table's row type. |

Booleans are `TRUE`/`FALSE`. No value is ever guessed. See `METHODOLOGY.md`
§"No-fabrication policy".

---

## Endpoint definition and tiers

This dataset's endpoint is **hydrocephalus and the CSF-dynamics disturbances that
produce or accompany it**. Because "hydrocephalus" alone is a rare, hard endpoint
that would yield too few rows to model, the dataset records a second, wider tier —
explicitly labelled, never silently pooled.

| `endpoint_tier` | Definition | Examples |
|---|---|---|
| **A** | The core endpoint: a ventricular or CSF-volume outcome. | hydrocephalus (communicating or obstructive), ventriculomegaly, ventricular volume change, CSF hypersecretion, shunt or external ventricular drain placement |
| **B** | CSF-dynamics adjacent: a pressure, composition or flow disturbance on the causal path to, or clinically bundled with, tier A. | raised intracranial pressure, papilloedema, aseptic/chemical meningitis, CSF protein or white-cell rise, post-lumbar-puncture syndrome, choroid-plexus or ependymal injury |

Tier C — general CNS or neurological adverse events with no ventricular, pressure,
or CSF readout — is **out of scope and contributes no rows**. Route of
administration is not evidence of this endpoint: an intrathecally dosed compound
with only a renal or hepatic readout does not belong here.

**Any analysis that pools tier A with tier B must say so.** `endpoint_tier` exists
precisely so the pooling is a stated choice rather than an accident.

---

## Table 1 — `data/oligos.csv`

Column names and vocabularies are kept **compatible with OligoTox-CNS
`oligos.csv`** so that the two endpoint tables can be concatenated.

| Column | Type | Definition / controlled vocabulary |
|---|---|---|
| `oligo_id` | string PK | Stable identifier, prefixed with the source id, e.g. `T1-OLG-0001`. Never reused. |
| `oligo_name` | string | Common or INN name. |
| `aliases` | string | Other names, `;` separated. |
| `oligo_class` | enum | `ASO_gapmer` \| `ASO_mixmer` \| `splice_switching_ASO` \| `siRNA` \| `divalent_siRNA` \| `PMO` \| `aptamer` \| `vehicle_control` \| `other` |
| `modality` | enum | `single_stranded_ASO` \| `double_stranded_siRNA` \| `vehicle` |
| `target_gene` | string | Intended target gene symbol, or `none_no_transcriptome_match` for scrambles. |
| `indication` | string | Disease or research context. |
| `developer` | string | Originating organisation. |
| `max_phase` | enum | `approved` \| `approved_EMA` \| `phase_3` \| `phase_3_discontinued` \| `phase_2` \| `phase_1` \| `preclinical` \| `research_panel` |
| `length_nt` | int | Length in nucleotides, or `NOT_REPORTED`. |
| `sequence_5to3_asprinted` | string | Sequence **exactly** as printed by the source, preserving any case convention that encodes chemistry. `NOT_REPORTED` unless an explicit string was retrieved. **Never guessed.** |
| `sequence_base` | string | Nucleobase sequence, upper case, chemistry stripped. |
| `sequence_source` | string | Exact document and locus the sequence came from, or `NOT_REPORTED`. |
| `backbone_chemistry` | enum | `full_PS` \| `mixed_PO_PS` \| `no_PS` \| `PMO_neutral` \| `NOT_REPORTED` |
| `sugar_modifications` | string | Sugar chemistry summary, `;` separated, e.g. `2'-MOE;DNA_gap`. |
| `modification_pattern` | string | The design motif in the source's own terms, e.g. `5-10-5_MOE_gapmer`. |
| `gapmer_shape` | enum | `gapmer` \| `mixmer` \| `uniform` \| `NOT_APPLICABLE` |
| `conjugate` | string | Conjugated moiety, or `none`. |
| `route_of_administration` | string | The route the compound is dosed by in its clinical or study use. **Context, not an endpoint claim.** |
| `dose_regimen_asapproved` | string | Approved or trial dosing regimen where stated. |
| `purity_pct` | string | Reported purity percentage, or `NOT_REPORTED`. |
| `purity_method` | string | Purification method, verbatim from the source, or `NOT_REPORTED`. |
| `identity_confirmation` | string | How identity was confirmed, verbatim, or `NOT_REPORTED`. |
| `formulation` | string | Vehicle the oligo was dosed in. |
| `source_id` | string FK | → `sources.source_id`. |
| `source_location` | string | Exact table/figure/section within the source. |
| `notes` | string | Free text. |

---

## Table 2 — `data/measurements.csv`

One row per **oligo × population or model × route × dose × readout × arm**. A
trial that reports hydrocephalus in a treated arm and in its placebo arm yields
**two rows**, so that the comparator is data rather than a footnote.

### Identity and context

| Column | Type | Definition / controlled vocabulary |
|---|---|---|
| `measurement_id` | string PK | e.g. `T1-MSR-00001`. |
| `oligo_id` | string FK | → `oligos.oligo_id`. |
| `source_id` | string FK | → `sources.source_id`. |
| `study_type` | enum | `clinical_trial` \| `clinical_case` \| `pharmacovigilance` \| `animal_invivo` \| `in_vitro` \| `background_epidemiology` |
| `species` | enum | `human` \| `mouse` \| `rat` \| `monkey` \| `pig` \| `multi_species` |
| `strain` | string | Strain, sex and age where stated, or `NOT_APPLICABLE`. |
| `system_model` | string | The trial design, cohort, animal model or culture system. |
| `is_human_system` | bool | `TRUE` if measured in a human or human-derived system. The Challenge prioritises these. |
| `indication_population` | string | The disease population dosed — the confounding variable for this endpoint. |
| `cns_compartment` | string | `lateral_ventricles` \| `whole_ventricular_system` \| `CSF` \| `choroid_plexus` \| `ependyma` \| `subarachnoid_space` \| `CSF_and_neuraxis` \| `NOT_APPLICABLE` |
| `delivery_route` | enum | `intrathecal_lumbar` \| `intracerebroventricular` \| `intraparenchymal` \| `intravenous` \| `subcutaneous` \| `in_culture_medium` \| `NOT_APPLICABLE` |
| `dose_value` / `dose_unit` | float / string | Dose as stated. `NOT_REPORTED` where the source does not give one. |
| `dose_interval` | string | e.g. `Q8W`, `Q16W`, `3 loading doses 14 days apart then Q4M`. |
| `exposure_duration` | string | Duration of exposure as stated. |
| `timepoint` | string | When the readout was taken. |

### The endpoint

| Column | Type | Definition / controlled vocabulary |
|---|---|---|
| `endpoint_tier` | enum | `A` \| `B`. See §"Endpoint definition and tiers". |
| `readout_category` | enum | `hydrocephalus_event` \| `ventricular_morphometry` \| `shunt_or_drain_intervention` \| `csf_pressure` \| `csf_composition` \| `csf_dynamics` \| `procedure_complication` \| `histopathology_choroid_ependyma` |
| `readout_name` | string | The specific readout, e.g. `hydrocephalus_serious_AE`, `ventricular_volume_change`, `intracranial_pressure_increased_AE`, `papilloedema_AE`, `CSF_protein`, `meningitis_aseptic_AE`, `post_lumbar_puncture_syndrome_AE`, `shunt_placement`. |
| `readout_value` | float/string | The value **exactly** as reported, or `NOT_REPORTED`. |
| `readout_unit` | string | e.g. `participants`, `reports`, `mL`, `pct_change`, `mg/dL`, `cases_per_1000_person_years`. |
| `readout_is_qualitative` | bool | `TRUE` where the source reports the result only in words or only as a figure. **No number is ever read off a figure.** |

### Numerator, denominator and comparator

The single most common defect in a toxicity dataset is a numerator without its
denominator. These five columns are mandatory for every incidence row.

| Column | Type | Definition |
|---|---|---|
| `n_affected` | int | Participants/animals with the event in this arm. |
| `n_at_risk` | int | Participants/animals at risk in this arm — the denominator. |
| `comparator_arm` | string | What this arm is compared against, or `NOT_APPLICABLE` (e.g. single-arm). |
| `n_affected_comparator` | int | Events in the comparator arm. |
| `n_at_risk_comparator` | int | Denominator of the comparator arm. |
| `statistic` | string | Dispersion, CI or significance **as stated by the source**. `NOT_REPORTED` where the source gives none — this dataset computes no inferential statistic of its own. |
| `effect_direction` | enum | `increase` \| `decrease` \| `no_change` \| `NOT_APPLICABLE` |
| `effect_vs_control` | string | The comparison as stated, including the comparator value. |

### Grading

| Column | Type | Definition |
|---|---|---|
| `hydroceph_grade` | int 0–3 | Ordinal severity, rubric below. Blank where the readout is continuous and not graded. |
| `grade_basis` | string | **The exact rule that produced this grade**, quoted or named. A grade with no stated basis is a defect. |
| `grade_status` | enum | `provisional` \| `expert_confirmed` \| `not_graded` |

### Ascertainment and attribution — the two columns this endpoint turns on

A prior review of the sibling kidney dataset found that grade 0 silently conflated
"measured and null" with "nobody looked". For hydrocephalus that conflation would
be fatal, because most sources never image the ventricles at all. These two
columns keep the distinction in the data.

| Column | Type | Definition / controlled vocabulary |
|---|---|---|
| `ascertainment` | enum | `measured_positive` — the endpoint was assessed and found.<br>`measured_null` — the endpoint was actively assessed and **not** found.<br>`reported_threshold_limited` — the source reports adverse events only above a frequency threshold, so absence is not evidence of absence.<br>`not_assessed` — the endpoint was not looked for; the row exists for the exposure context only. |
| `ascertainment_basis` | string | How the above was established, citing the source's own statement (e.g. the AE reporting threshold it declares). |
| `attribution_as_stated` | enum | `drug_attributed` \| `procedure_attributed` \| `disease_attributed` \| `multifactorial` \| `undetermined` \| `not_discussed`. **What the SOURCE concluded**, never this dataset's own inference. |
| `attribution_evidence` | string | The source's stated reasoning, quoted or summarised, with its locus. |
| `tox_axis` | enum | `ventricular_enlargement` \| `csf_pressure_disturbance` \| `csf_composition_disturbance` \| `delivery_procedure_complication` \| `disease_background_rate` \| `therapeutic_ventricular_effect` |

`tox_axis = disease_background_rate` marks rows that carry **no drug exposure at
all** — untreated-population incidence figures. `tox_axis =
therapeutic_ventricular_effect` marks oligonucleotides whose measured ventricular
effect is *protective*. Both are deliberate control classes; both must be excluded
from any "toxicity of exposed compounds" analysis, and `oligo_id` is
`NOT_APPLICABLE` for background rows with no compound.

### Provenance

| Column | Type | Definition |
|---|---|---|
| `source_ref` | string | Citation key, DOI, PMID, NCT id, DailyMed set id, or FAERS query. |
| `source_location` | string | **Exact locus** — `Table 2`, `Fig 3B`, `PI section 5.4`, `adverseEventsModule.seriousEvents["Hydrocephalus"]`. A category word such as `results` is not acceptable. |
| `redistribution` | enum | `public_domain` \| `cc_by` \| `cc_by_nc` \| `summary_stat_only` \| `derived_features_only` \| `verify` |
| `notes` | string | Free text. |

---

## Table 3 — `data/sources.csv`

| Column | Definition |
|---|---|
| `source_id` | Primary key, e.g. `T1`, `C1`, `F1`. |
| `source_key` | Short citation key, e.g. `GENERATION_HD1_NCT03761849`. |
| `citation` | Full citation. |
| `first_author`, `year`, `journal` | Bibliographic fields, or `NOT_APPLICABLE` for registry/regulatory sources. |
| `doi`, `pmid`, `pmcid`, `nct_id`, `url` | Identifiers; empty where none exists. |
| `access` | `open_access` \| `public_domain` \| `subscription` \| `api` |
| `license` | The licence as stated by the source. |
| `redistribution` | Rights status governing reproduction of values from this source. |
| `evidence_tier` | `regulatory_primary` \| `registry_results` \| `primary_fulltext` \| `primary_supplementary_data` \| `pharmacovigilance_api` \| `case_report` \| `epidemiology` \| `review_secondary` |
| `retrieved_via` | The exact retrieval route used, so any value can be re-fetched. |
| `retrieved_date` | Date of retrieval. |
| `n_oligos`, `n_measurements` | Rows this source contributes. Recomputed by the QC suite, never typed. |
| `notes` | Free text. |

---

## `hydroceph_grade` rubric (0–3)

Severity is graded on **clinical/structural consequence**, not on the size of a
number. The rubric is written for this endpoint and is **not** transferable to or
from the sibling `nephrotox_grade` or `cns_tox_grade` columns.

| Grade | Definition |
|---|---|
| **0** | The endpoint was assessed and no ventricular, pressure or CSF-composition abnormality was found. Requires `ascertainment = measured_null`. |
| **1** | **Mild / biochemical or asymptomatic.** A CSF composition change (protein or cell-count rise), or an imaging finding without symptoms, requiring no intervention and resolving spontaneously. |
| **2** | **Moderate / symptomatic, reversible.** Symptomatic raised intracranial pressure, papilloedema, or aseptic/chemical meningitis; ventriculomegaly with symptoms; managed medically or by dose interruption, without a permanent CSF diversion. |
| **3** | **Severe.** Hydrocephalus requiring permanent CSF diversion (shunt or external ventricular drain), a serious adverse event coded as hydrocephalus, or a CSF-dynamics event that is fatal, life-threatening, or causes persistent disability. |

Rules that constrain the rubric, and which the QC suite enforces:

1. **Every graded row must state its `grade_basis`.** Where a grade derives from a
   regulatory seriousness classification rather than from a clinical description,
   `grade_basis` says exactly that.
2. **Grade 0 requires `ascertainment = measured_null`.** A row that was never
   assessed is `not_assessed` with an **empty** grade, not a zero. This is the
   rule the sibling kidney dataset lacked.
3. **The scale is censored by study type.** An `in_vitro` or `csf_composition`
   row cannot reach grade 3, because grade 3 is defined by whole-organism
   intervention. Grades are therefore **not comparable across `study_type`**, and
   any model trained on this column must carry `study_type` as a covariate or
   stratify on it. This is stated here rather than discovered later.
4. **Grade is a property of the measurement, not of the compound.** The same
   oligonucleotide may carry grade 3 in one arm and grade 0 in another.
5. All grades ship `grade_status = provisional` pending subject-matter-expert
   review.

---

## Deliberate limits of this schema

- **It records no disproportionality statistic.** Pharmacovigilance rows carry
  report counts and the drug's total report base; PRR/ROR and their intervals are
  left to the user, because a spontaneous-reporting ratio is an analysis, not a
  measurement, and its denominator assumptions belong to whoever makes them.
- **It records no attribution of its own.** `attribution_as_stated` reproduces
  the source's conclusion. Where a source draws none, the value is `not_discussed`
  and stays that way.
- **It records no number read off a figure.** Where a source publishes a value
  only graphically, `readout_value` is `NOT_REPORTED` and
  `readout_is_qualitative` is `TRUE`.
