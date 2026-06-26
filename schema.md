# Schema — OligoTox-Kidney dataset

Two normalized tables joined on `oligo_id`. All files are UTF-8 CSV with a
header row. Missing/unknown values are the literal string `TBD` (never guessed,
never blank-as-zero). Booleans are `TRUE`/`FALSE`.

---

## Table 1 — `data/oligos.csv`

One row per **unique oligonucleotide** (identity + design predictors). These
are the chemistry/sequence/design features hypothesized to drive nephrotoxicity.

| Column | Type | Description / controlled vocabulary |
|--------|------|-------------------------------------|
| `oligo_id` | string PK | Stable ID, e.g. `OLG001`. Never reused. |
| `oligo_name` | string | Common/INN name, e.g. `inotersen`, `drisapersen`. |
| `aliases` | string | `;`-separated alternates, e.g. `IONIS-TTRRx;ISIS 420915`. |
| `oligo_class` | enum | `ASO_gapmer` \| `siRNA` \| `GalNAc_siRNA` \| `splice_switching_ASO` \| `PMO` \| `aptamer` \| `other`. |
| `target_gene` | string | Intended molecular target (e.g. `TTR`), or `NA` for non-hybridizing aptamers. |
| `indication` | string | Disease/indication, free text. |
| `developer` | string | Sponsor/developer. |
| `max_phase` | enum | `approved` \| `phase_3` \| `phase_2` \| `phase_1` \| `preclinical` \| `research_panel`. |
| `length_nt` | int | Oligonucleotide length in nucleotides. |
| `backbone_chemistry` | enum | `full_PS` \| `PS_PO_mix` \| `full_PO` \| `PMO_neutral` \| `mixed` \| `TBD`. |
| `sugar_modifications` | string | `;`-separated, e.g. `2'-MOE;2'-OMe;cEt;LNA;2'-F;morpholino;DNA_gap`. |
| `gapmer_design` | string | Wing-gap-wing motif if applicable, e.g. `5-10-5_MOE`; else `NA`. |
| `conjugate` | enum | `none` \| `GalNAc` \| `lipid` \| `peptide` \| `other`. (Affects renal exposure.) |
| `ps_count` | int | Number of phosphorothioate linkages, or `TBD`. |
| `sequence_5to3` | string | 5′→3′ sequence. **`TBD` unless from a redistribution-permitted source. Never guessed.** |
| `design_source` | string | Source for the design metadata (DOI / patent / label). |
| `notes` | string | Free text. |

---

## Table 2 — `data/measurements.csv`

One row per **oligo × cell-model × delivery × concentration × readout**. A
single oligo at a single concentration measured with KIM-1 *and* viability =
**two rows**.

| Column | Type | Description / controlled vocabulary |
|--------|------|-------------------------------------|
| `measurement_id` | string PK | Stable ID, e.g. `MSR001`. |
| `oligo_id` | string FK | → `oligos.oligo_id`. |
| `study_type` | enum | `in_vitro` \| `animal_invivo` \| `clinical`. |
| `species` | enum | `human` \| `monkey` \| `rat` \| `mouse` \| `NA`. |
| `system_model` | string | Cell line / model / subject, e.g. `ciPTEC`, `HK-2`, `RPTEC_TERT1`, `primary_human_PTEC`, `proximal_tubule_on_chip`, `kidney_invivo`, `patient`. |
| `tissue` | string | `kidney` \| `proximal_tubule` \| `glomerulus` \| `NA`. |
| `delivery_method` | enum | `gymnotic_free_uptake` \| `transfection` \| `conjugate_mediated` \| `systemic_dose` \| `TBD`. |
| `dose_or_conc_value` | float | Numeric concentration or dose, or `TBD`. |
| `dose_or_conc_unit` | enum | `uM` \| `nM` \| `ug/mL` \| `mg/kg` \| `NA`. |
| `exposure_duration` | string | e.g. `72h`, `14d`, `chronic`; or `TBD`. |
| `readout_category` | enum | `functional` \| `injury_biomarker` \| `viability` \| `accumulation` \| `histopathology` \| `clinical_renal_outcome`. |
| `readout_name` | string | e.g. `KIM-1`, `NGAL`, `clusterin`, `cystatin_C`, `albumin_reabsorption`, `A1M`, `RAP_uptake`, `LMW_proteinuria`, `lysosomal_load`, `LDH_release`, `viability_MTT`, `eGFR`, `serum_creatinine`, `proteinuria`, `tubular_degeneration`. |
| `readout_value` | float/string | Reported value, or `TBD` if qualitative-only. |
| `readout_unit` | string | e.g. `% of control`, `fold_change`, `ng/mL`, `mg/mmol_creatinine`, `IC50_uM`; or `NA`. |
| `effect_direction` | enum | `increase` \| `decrease` \| `no_change` \| `TBD`. |
| `effect_vs_control` | string | Quantified effect vs control if available (e.g. `3.2x`, `-45%`), else `TBD`. |
| `nephrotox_grade` | int 0–3 | Graded label (rubric below). |
| `is_kidney_specific` | bool | `TRUE` = strict-kidney row; `FALSE` = hepatotox/other fallback row (flagged). |
| `source_id` | string | → entry in `sources/SOURCES.md` (e.g. `N2`). |
| `source_ref` | string | DOI or patent number. |
| `source_table` | string | Exact locus, e.g. `Table 2`, `Fig 3B`, `Claim 7`, `Supp Table S1 row 14`. |
| `redistribution` | enum | `public_domain` \| `derived_features_only` \| `summary_stat` \| `verify`. |
| `notes` | string | Free text (e.g. `reversible on washout`). |

---

## `nephrotox_grade` rubric (0–3)

| Grade | Definition |
|-------|------------|
| **0** | No renal signal at tested exposure — no change in function, injury biomarkers, or histology. |
| **1** | **Mild / functional, reversible** — e.g. low-MW proteinuria, impaired LMW-protein reabsorption, modest biomarker rise, **no viability loss**. (The characteristic PS-ASO proximal-tubule phenotype.) |
| **2** | **Moderate** — clear injury-biomarker elevation (KIM-1/NGAL/clusterin) and/or histopathology (tubular degeneration/basophilia), or clinically significant proteinuria. |
| **3** | **Severe** — acute kidney injury, glomerulonephritis, renal failure / dialysis, or dose-limiting nephrotoxicity. *(e.g. inotersen.)* |

Grade is assigned per measurement from the reported endpoint; rows for the same
oligo may differ by model/dose. Record the rationale in `notes` when non-obvious.

## Provenance rules

- Every row MUST carry `source_id` + `source_ref` + `source_table`.
- `redistribution` governs whether raw values may be published: patents are
  `public_domain`; journal supplementary data may be `derived_features_only` or
  `summary_stat` — when unsure, use `verify` and resolve before release.
- `sequence_5to3` and any toxicity `readout_value` are **never fabricated**.
  Use `TBD` and fetch the source.
