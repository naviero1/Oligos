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
| `max_phase` | enum | `approved` \| `approved_EMA` \| `phase_3` \| `phase_3_discontinued` \| `phase_2` \| `phase_1` \| `preclinical` \| `research_panel` \| `class_review` (class-level/pooled entry). |
| `length_nt` | int | Oligonucleotide length in nucleotides. |
| `backbone_chemistry` | enum | `full_PS` \| `PS_PO_mix` \| `full_PO` \| `PMO_neutral` \| `mixed` \| `TBD`. |
| `sugar_modifications` | string | `;`-separated, e.g. `2'-MOE;2'-OMe;cEt;LNA;2'-F;morpholino;DNA_gap`. |
| `gapmer_design` | string | Wing-gap-wing motif if applicable, e.g. `5-10-5_MOE`; else `NA`. |
| `conjugate` | enum | `none` \| `GalNAc` \| `lipid` \| `peptide` \| `PEG` (e.g. `PEG_5prime`) \| `other`. (Affects renal exposure.) |
| `ps_count` | int | Number of phosphorothioate linkages, or `TBD`. |
| `sequence_5to3` | string | 5′→3′ sequence of the **active / guide strand** (the ASO itself, or an siRNA's antisense strand). **`TBD` unless from a redistribution-permitted source. Never guessed.** `NA` for class-level/pooled entries that are not a single molecule. |
| `sequence_sense_5to3` | string | For **duplexes only**: the 5′→3′ **sense (passenger)** strand. Empty for single-stranded oligos. (Splitting the duplex across two columns keeps `sequence_5to3` a single comparable active strand across all modalities.) |
| `sequence_source` | string | Exact provenance of the **sequence** specifically (e.g. `WHO INN Proposed List 114`, `EMA Givlaari EPAR EMA/CHMP/70703/2020 p15`, `US 11,105,794 B2 SEQ ID NO 2`). Distinct from `design_source`, which covers the rest of the design metadata. |
| `sequence_redistribution` | enum | Rights status of the sequence string: `public_domain` (WHO INN, FDA/EMA regulatory documents, USPTO patents) \| `summary_stat` (journal-derived) \| `verify` (rights or provenance unresolved — e.g. taken from a secondary reproduction of an INN record) \| `NA`. |
| `purity_characterization` | string | Purity / identity-characterization data for the oligo as reported by the source (e.g. HPLC, mass spec), or the literal `not_reported_in_source`. Required by the Phase 2 dataset specification; for an in-silico curation this records what the primary source states rather than newly generated analytics. |
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
| `species` | enum | `human` \| `monkey` \| `rat` \| `mouse` \| `multi_species` (finding pooled across species) \| `NA`. |
| `system_model` | string | Cell line / model / subject, e.g. `ciPTEC`, `HK-2`, `RPTEC_TERT1`, `primary_human_PTEC`, `proximal_tubule_on_chip`, `kidney_invivo`, `patient`. |
| `tissue` | string | `kidney` \| `proximal_tubule` \| `glomerulus` \| `NA`. |
| `delivery_method` | enum | `gymnotic_free_uptake` \| `transfection` \| `conjugate_mediated` \| `systemic_dose` \| `intrathecal` \| `intravitreal` \| `oral` \| `TBD`. |
| `dose_or_conc_value` | float | Numeric concentration or dose, or `TBD`. |
| `dose_or_conc_unit` | enum | `uM` \| `nM` \| `ug/mL` \| `mg/kg` \| `mg` (total dose) \| `fold_Cmax` (multiple of clinical Cmax) \| `NA`. |
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

### In-vitro rubric extension (quantitative dose–response readouts)

The 0–3 rubric above is written for clinical/histopathological endpoints. In-vitro
rows report a **continuous value as % of control** (saline, or the innocuous
reference compound 1-1), so grades are assigned by the explicit, deterministic
thresholds below. Every such row records its value, its direction, and the
resulting grade in `notes`, so any grade can be recomputed from the data.

Two of these thresholds are **the source's own**, not ours: US 11,105,794 B2 /
US 11,479,818 B2 state that toxicity is indicated by *"a 10 fold increase"* in
KIM-1 mRNA and *"a 2 fold increase"* in KIM-1 protein over the innocuous
compound. Those cutoffs are adopted verbatim as the grade-2 boundary.

| Readout | Toxicity direction | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| `ATP` (intracellular) | decrease | ≥85 | 70–84 | 50–69 | <50 |
| `EGFR_mRNA` | decrease | ≥75 | 50–74 | 25–49 | <25 |
| `EGF_supernatant` | **increase** (impaired EGF consumption = tubular dysfunction) | ≤125 | 126–200 | 201–400 | >400 |
| `KIM-1_protein` | increase | <150 | 150–199 | **200**–399 | ≥400 |
| `KIM-1_mRNA` | increase | <300 | 300–999 | **1000**–2999 | ≥3000 |

Bold = the patent's own stated toxicity threshold. All in-vitro grades are
flagged `grade_provisional` pending subject-matter sign-off, consistent with the
rest of the dataset.

**What is deliberately excluded from the graded tables.** On-target pharmacology
(`PCSK9_mRNA` knockdown) is *not* a toxicity readout — the source itself states
the knockdown "does not appear to contribute to the toxicity" — so those rows are
not graded. Vehicle/untreated controls, small-molecule reference nephrotoxicants
(cyclosporine A, staurosporine), non-kidney systems (A549, CACO2, hepatocytes),
and absolute-unit rows are likewise held outside the canonical strict-kidney
tables. All exclusions are retained with their reasons in
`data/patent_excluded_rows.json` rather than discarded silently.

## Provenance rules

- Every row MUST carry `source_id` + `source_ref` + `source_table`.
- `redistribution` governs whether raw values may be published: patents are
  `public_domain`; journal supplementary data may be `derived_features_only` or
  `summary_stat` — when unsure, use `verify` and resolve before release.
- `sequence_5to3` and any toxicity `readout_value` are **never fabricated**.
  Use `TBD` and fetch the source.

---

## Data-dictionary QC log

- **2026-06-26** — Validated every controlled-vocabulary column against the enums
  above. Reconciled the dictionary to the curated data by documenting values that
  arose during extraction: `conjugate=PEG`; `species=multi_species`;
  `delivery_method=intrathecal/intravitreal/oral`; `max_phase=approved_EMA / phase_3_discontinued / class_review`;
  `dose_or_conc_unit=mg / fold_Cmax`. After reconciliation: all rows pass enum
  validation; measurements→oligos FK = 0 orphans; no duplicate IDs; grades ∈ {0,1,2,3}.
  `sequence_5to3` filled for 7/31 oligos (rest `TBD` pending authoritative
  retrieval — never guessed).

---

## Derived table — `data/oligotox_kidney_merged.csv` (generated, not canonical)

An analysis-ready **denormalized join** of the two canonical tables on `oligo_id`,
produced by `scripts/build_merged.py`.

- **Grain / size:** one row per measurement — **111 rows × 39 columns**.
- **Columns:** `measurement_id`, `oligo_id`, then all 15 oligo **design predictors**
  + `notes_oligo`, then all 20 measurement **outcome/context** fields + `notes_measurement`.
  (The two source `notes` columns are disambiguated to `notes_oligo` /
  `notes_measurement`; `oligo_id` appears once.)
- **Purpose:** each row carries the **predictors and the graded outcome together**,
  so downstream EDA / model training needs no join. Supports the challenge's
  "data translatability" dimension.
- **Status:** **generated and derived — not a source of truth.** `data/oligos.csv`
  and `data/measurements.csv` remain canonical; regenerate this file with
  `python scripts/build_merged.py` after any change, and never hand-edit it
  (denormalization repeats each oligo's design across its measurement rows).
