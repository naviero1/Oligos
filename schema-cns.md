# Schema — OligoTox-CNS dataset

Companion to `schema.md` (the kidney dataset). Same two-table normalized design,
same conventions, so the two datasets can be **unioned or compared** without
re-mapping: `data/cns_oligos.csv` uses the **identical 17-column layout** as
`data/oligos.csv`, and `data/cns_measurements.csv` extends the measurement layout
with CNS-specific context columns.

All files are UTF-8 CSV with a header row. Missing/unknown values are the literal
string `TBD` (never guessed, never blank-as-zero). Booleans are `TRUE`/`FALSE`.

---

## Endpoint scope — and why it is scoped this way

The NCATS OligoTox challenge brief names its toxicities of interest as:

> Hepatotoxicity, kidney toxicity, thrombocytopenia, complement activation,
> coagulopathy, immunotoxicity, **chronic neurotoxicity**, and **hydrocephalus**.
> *Given the availability of large data sets focused on acute neurotoxicity,
> specifically alterations of neuronal electrical activity, submissions focused on
> this topic will be considered a lower priority than other toxicities of interest.*

This dataset is therefore built **chronic-neurotoxicity-first and
hydrocephalus-first**. Acute neurotoxicity is still captured — it is a real,
strongly sequence-dependent oligonucleotide signal and one of the most
informative predictors available — but every row declares which bucket it falls
in via `endpoint_domain` and `challenge_priority`, so a consumer can filter the
deprioritized acute-electrophysiology material out in one predicate rather than
having it silently inflate the record count.

---

## Table 1 — `data/cns_oligos.csv`

One row per **unique oligonucleotide** (identity + design predictors). Column
layout is identical to the kidney dataset's `data/oligos.csv`.

| Column | Type | Description / controlled vocabulary |
|--------|------|-------------------------------------|
| `oligo_id` | string PK | Stable ID, e.g. `CNS001`. Never reused. CNS-prefixed so IDs never collide with the kidney table's `OLG###`. |
| `oligo_name` | string | Common/INN name, e.g. `tofersen`, `nusinersen`, `tominersen`. |
| `aliases` | string | `;`-separated alternates, e.g. `BIIB067;ISIS 666853`. |
| `oligo_class` | enum | `ASO_gapmer` \| `siRNA` \| `GalNAc_siRNA` \| `splice_switching_ASO` \| `PMO` \| `aptamer` \| `other`. |
| `target_gene` | string | Intended molecular target (e.g. `SOD1`, `SMN2`, `HTT`, `MAPT`), or `NA`. |
| `indication` | string | Disease/indication, free text. |
| `developer` | string | Sponsor/developer. |
| `max_phase` | enum | `approved` \| `approved_EMA` \| `phase_3` \| `phase_3_discontinued` \| `phase_2` \| `phase_2_discontinued` \| `phase_1` \| `phase_1_discontinued` \| `preclinical` \| `research_panel` \| `named_patient` (n-of-1 / expanded access) \| `class_review`. |
| `length_nt` | int | Oligonucleotide length in nucleotides. |
| `backbone_chemistry` | enum | `full_PS` \| `PS_PO_mix` \| `full_PO` \| `PMO_neutral` \| `mixed` \| `TBD`. |
| `sugar_modifications` | string | `;`-separated, e.g. `2'-MOE;DNA_gap`, `2'-OMe`, `cEt`, `LNA`, `2'-F`, `morpholino`. |
| `gapmer_design` | string | Wing-gap-wing motif if applicable, e.g. `5-10-5_MOE`, `3-10-3_cEt`; else `NA` (uniformly modified SSOs, siRNA, PMO). |
| `conjugate` | enum | `none` \| `GalNAc` \| `lipid` \| `peptide` \| `PEG` \| `divalent` \| `other`. |
| `ps_count` | int | Number of phosphorothioate linkages, or `TBD`. |
| `sequence_5to3` | string | 5′→3′ sequence. **`TBD` unless from a redistribution-permitted source. Never guessed.** Case is significant in gapmer rows (uppercase = 2′-MOE/cEt/LNA wing, lowercase = DNA gap). |
| `design_source` | string | Source for the design metadata (DOI / patent / label / WHO INN list). |
| `notes` | string | Free text. |

---

## Table 2 — `data/cns_measurements.csv`

One row per **oligo × model/subject × CNS region × delivery × dose × readout**.
A single oligo at a single dose measured for NfL *and* ventricular volume =
**two rows**.

| Column | Type | Description / controlled vocabulary |
|--------|------|-------------------------------------|
| `measurement_id` | string PK | Stable ID, e.g. `CMS001`. |
| `oligo_id` | string FK | → `cns_oligos.oligo_id`. |
| `study_type` | enum | `in_vitro` \| `animal_invivo` \| `clinical`. |
| `species` | enum | `human` \| `monkey` \| `rat` \| `mouse` \| `multi_species` \| `NA`. |
| `system_model` | string | Cell line / model / subject, e.g. `hiPSC_motor_neuron`, `hiPSC_cortical_neuron`, `hiPSC_microglia`, `hiPSC_astrocyte`, `human_neural_progenitor`, `cerebral_organoid`, `SH-SY5Y`, `primary_cortical_neuron`, `CNS_invivo`, `patient_cohort`, `patient_case`. |
| `cns_region` | enum | `whole_brain` \| `cortex` \| `hippocampus` \| `cerebellum` \| `brainstem` \| `striatum` \| `spinal_cord` \| `DRG` \| `ventricle` \| `CSF` \| `meninges` \| `optic_nerve` \| `peripheral_nerve` \| `systemic` \| `NA`. |
| `delivery_method` | enum | `intrathecal` \| `intracerebroventricular` \| `intracisternal` \| `intraparenchymal` \| `intravitreal` \| `systemic_dose` \| `gymnotic_free_uptake` \| `transfection` \| `lipofection` \| `TBD`. |
| `dose_or_conc_value` | float | Numeric concentration or dose, or `TBD`. |
| `dose_or_conc_unit` | enum | `uM` \| `nM` \| `ug/mL` \| `mg/kg` \| `mg` (total dose) \| `ug` \| `fold_Cmax` \| `NA`. |
| `exposure_duration` | string | e.g. `72h`, `14d`, `28wk`, `chronic`; or `TBD`. |
| `endpoint_domain` | enum | **CNS-specific.** `chronic_neurotoxicity` \| `hydrocephalus` \| `acute_neurotoxicity` \| `neuroinflammation` \| `neurodegeneration` \| `neurobehavioral` \| `cytotoxicity` \| `csf_biomarker` \| `clinical_neuro_ae`. |
| `challenge_priority` | enum | **CNS-specific.** `high_chronic_neurotox` \| `high_hydrocephalus` \| `medium` \| `low_acute_electrophysiology`. Encodes the brief's explicit deprioritization so it is filterable, not buried. |
| `readout_category` | enum | `functional` \| `injury_biomarker` \| `viability` \| `accumulation` \| `histopathology` \| `imaging` \| `behavioral` \| `clinical_neuro_outcome` \| `electrophysiology` \| `transcriptomic`. |
| `readout_name` | string | e.g. `NfL_CSF`, `NfL_plasma`, `GFAP`, `Iba1`, `AIF1_mRNA`, `CSF_WBC`, `CSF_total_protein`, `ventricular_volume`, `hydrocephalus_incidence`, `spinal_cord_degeneration`, `DRG_neuron_degeneration`, `neuronal_necrosis`, `microgliosis`, `astrogliosis`, `acute_neurotoxicity_score`, `motor_function_score`, `ataxia`, `tremor`, `hypoactivity`, `papilledema`, `intracranial_pressure`, `myelitis`, `radiculitis`, `aseptic_meningitis`, `brain_weight`, `neurite_length`, `viability_ATP`, `caspase3`, `TUNEL`. |
| `readout_value` | float/string | Reported value, or `TBD` if qualitative-only. |
| `readout_unit` | string | e.g. `pg/mL`, `% of control`, `fold_change`, `pct_incidence`, `n_of_N`, `score_0_to_5`, `mL`, `cells/uL`, `IC50_uM`; or `NA`. |
| `effect_direction` | enum | `increase` \| `decrease` \| `no_change` \| `TBD`. |
| `effect_vs_control` | string | Quantified effect vs control (e.g. `3.2x`, `-45%`, `12pct_vs_2pct_placebo`), else `TBD`. |
| `neurotox_grade` | int 0–3 | Graded label (rubric below). |
| `reversibility` | enum | `reversible` \| `partially_reversible` \| `irreversible` \| `not_assessed` \| `TBD`. Central to separating transient acute effects from **chronic** neurotoxicity. |
| `is_cns_specific` | bool | `TRUE` = strict-CNS row; `FALSE` = non-CNS/systemic comparator row (flagged, e.g. a negative-control systemic oligo with no CNS exposure). |
| `source_id` | string | → entry in `sources/SOURCES-CNS.md`. |
| `source_ref` | string | DOI / PMID / patent number / NCT number / FDA application number. |
| `source_table` | string | Exact locus, e.g. `Table 2`, `Fig 3B`, `label sec 5.1`, `Claim 7`, `Supp Table S1 row 14`. |
| `redistribution` | enum | `public_domain` \| `cc_by` \| `derived_features_only` \| `summary_stat` \| `verify`. |
| `notes` | string | Free text (e.g. `resolved without discontinuation`, `grade_provisional`). |

---

## `neurotox_grade` rubric (0–3)

| Grade | Definition |
|-------|------------|
| **0** | **No CNS signal at the tested exposure** — no behavioural change, no biomarker or imaging change, no histopathology, incidence at or below concurrent control. Negative controls are recorded, not omitted. |
| **1** | **Mild / transient, reversible** — transient acute behavioural signs resolving within hours–days; isolated mild glial marker or CSF-protein elevation; mild CSF pleocytosis; **no neuronal loss and no persisting functional deficit**. |
| **2** | **Moderate** — sustained neuroinflammation (astrogliosis/microgliosis), measurable neuro-axonal injury (treatment-emergent NfL rise), ventriculomegaly without clinical decompensation, or a clinically significant but manageable/resolving neurologic adverse event (aseptic meningitis, radiculitis, myelitis, papilledema). |
| **3** | **Severe** — neuronal degeneration/loss, spinal-cord or DRG degeneration, paralysis, hydrocephalus requiring intervention, moribundity/death, or **dose-limiting or programme-halting** neurotoxicity. |

Grade is assigned **per measurement** from the reported endpoint; rows for the
same oligo may legitimately differ by model, region and dose. Record the
rationale in `notes` when non-obvious.

### Direction matters more here than in any other endpoint

`NfL` is both an efficacy biomarker and a toxicity biomarker in this field. A
**fall** in CSF/plasma NfL after a huntingtin- or SOD1-lowering ASO is a benefit
signal and grades **0**; a **treatment-emergent rise** over baseline is
neuro-axonal injury and grades **2** or higher. `effect_direction` is therefore a
grading input, not decoration, and no NfL row may be filed with
`effect_direction = TBD`.

---

## Provenance rules

- Every row MUST carry `source_id` + `source_ref` + `source_table`.
- `redistribution` governs whether raw values may be published:
  - `public_domain` — US patents, FDA/EMA regulatory documents. Reproduce freely.
  - `cc_by` — the source article is Creative Commons Attribution licensed, which
    permits **unrestricted reproduction of the raw values with attribution**.
    This is a materially stronger right than `summary_stat` and is tracked
    separately rather than being conservatively flattened into it, because it is
    what allows whole per-oligo panels to be republished verbatim in an open
    dataset. Every `cc_by` row's `source_ref` carries the citation that
    attribution requires.
  - `summary_stat` / `derived_features_only` — numbers quoted from a source whose
    licence does not clearly permit bulk reproduction.
  - `verify` — rights unresolved; must be settled before public release.
- `sequence_5to3` and any toxicity `readout_value` are **never fabricated**.
  Use `TBD` and fetch the source.
- Values recalled from model memory are not acceptable provenance. Every number
  must have been read out of a fetched document during curation.

---

## Derived table — `data/oligotox_cns_merged.csv` (generated, not canonical)

An analysis-ready **denormalized join** of the two canonical CNS tables on
`oligo_id`, produced by `scripts/build_merged_cns.py`: one row per measurement
carrying both the design predictors and the graded outcome, so downstream
EDA/model training needs no join. `data/cns_oligos.csv` and
`data/cns_measurements.csv` remain the source of truth; regenerate this file
after any change and never hand-edit it.
