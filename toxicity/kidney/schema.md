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
| `sequence_5to3` | string | 5′→3′ sequence. **`TBD` unless from a redistribution-permitted source. Never guessed.** |
| `purity_pct` | float | Reported purity of the tested oligo, %. **`TBD` for all 65** — verified unavailable, not merely unrecorded: both in-repo patents were searched for purity/HPLC/UPLC/LC-MS/mass-spec language and neither reports any, and labels and trial papers do not publish per-batch purity. No wet lab was run, so this cannot be closed by further curation. |
| `purity_method` | string | Analytical method behind `purity_pct` (e.g. `HPLC`, `LC-MS`). `TBD` for all 65, same reason. |
| `identity_confirmation` | enum | **How each oligo's identity was established** — the half of the Phase 2 "purify and characterize oligo identity" requirement a curated dataset can answer. `who_inn_chemical_nomenclature` (residue-by-residue INN parse, reverse-complement and molecular-formula checked) \| `patent_sequence_listing` \| `regulatory_label` \| `peer_reviewed_publication` \| `not_established` (sequence still `TBD`). Derived by `scripts/add_identity_characterization.py`. |
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
| `study_type` | enum | `in_vitro` \| `animal_invivo` \| `clinical`. Note `in_vitro` spans both species — use `subject_class` to separate human from animal cell systems. |
| `species` | enum | `human` \| `monkey` \| `rat` \| `mouse` \| `multi_species` (finding pooled across species) \| `NA`. |
| `subject_class` | enum | **The human/animal divider.** `human_clinical` (human trial) \| `human_invitro` (human cell system) \| `animal_invitro` (non-human cell system, e.g. rat primary PTEC) \| `animal_invivo` (non-human live study). **Derived** from `study_type` + `species` by `scripts/split_human_animal.py`, never hand-entered, so it cannot drift from the columns it summarises. Materialised because the Phase 2 brief makes this division a scoring criterion — datasets "based on in vitro human systems or able to extrapolate data between in vitro human systems and animal data" are of particular interest. |
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
| `renal_endpoints_measured` | enum | **Stops grade 0 meaning two different things.** `measured_and_reported` (endpoint assayed, result reported — a real negative) \| `not_measured` (study never assessed renal endpoints) \| `not_reported_in_source` (cited source does not report them) \| `cannot_determine` (not yet verified against the primary source). Only `measured_and_reported` supports a grade of 0 as evidence of safety. Assigned deterministically by `scripts/add_endpoint_provenance.py`; see `CLINICAL_VALIDATION.md`. |
| `nephrotox_grade` | int 0–3 | Graded label (rubric below). **Read together with `renal_endpoints_measured`** — a grade of 0 on a row that is not `measured_and_reported` means "not established", not "safe". |
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

- **2026-08-03** — Re-ran the US 11,105,794 patent-panel extraction from scratch and
  validated all 21 compounds (`OLG045`–`OLG065`) against the patent's **formal
  SEQUENCE LISTING** rather than the examples table alone. 19 rows match the
  listing base-for-base; `OLG065` confirmed against its raw listing entry
  (`LENGTH : 12`). Filled `OLG046` — its three leading glyphs are unmapped in the
  text layer of **both** patents (render as `???`), recovered as `AAT` from the
  rendered page and confirmed by the listing (SEQ ID NO:2, LENGTH 16). Corrected
  `OLG065.gapmer_design` (`LNA_gapmer` → `2-8-2_MOE`) per the Table 1 footnote
  defining bold-italic lower case as MOE units. Filled `OLG002` (SPC5001), whose
  published sequence proved **identical to `OLG047`**, establishing that the
  patent's PCSK9 compound 3-1 is the clinical nephrotoxin SPC5001; both rows are
  cross-flagged as one molecule.
  **Two extraction hazards recorded for future rounds:** (1) a naive
  `[acgt]`-run regex over the sequence listing silently mis-parses SEQ ID NO:20 —
  the text layer renders the bold-italic `tc` as `to`, so the regex skips it and
  absorbs letters from the following claims text, yielding a plausible but wrong
  14-nt sequence; always confirm against the entry's declared `LENGTH`. (2)
  Judging letter case from rendered pixels is unreliable at x-height — an
  apparent lower-case `c` in SEQ ID NO:1 contradicted four independent printed
  loci reading `AATC`. Case encodes LNA vs. DNA, so resolve it from the text
  layer and corroborating loci, not from a render.
  After this round: all enum/FK/range checks pass; `sequence_5to3` filled for
  **55/65** oligos (9 added by deterministic parse of WHO INN chemical
  nomenclature — see METHODOLOGY §4 path 4).

---

- **2026-09-03** — Added `subject_class`, the explicit human/animal divider, derived
  from `study_type` + `species` by `scripts/split_human_animal.py` (39 human_clinical /
  19 human_invitro / 53 animal_invivo; 0 disagreements with its source columns). Added
  the derived `data/human_animal_bridge.csv` view (9 oligos with paired human+animal
  evidence). **Corrected the 21 US 11,105,794 Table 1 rows (`MSR91`–`MSR111`, 19% of the
  dataset): species `mouse`→`rat`, `exposure_duration` `7_days`→`15_days`, and
  `dose_or_conc_value` `TBD`→`40` mg/kg** — verified against the patent's own method
  section (p.25), which binds itself to Table 1 ("groups of 4 (table 1, exp. A) or 8
  (table 1, exp. B)"), names "Wistar Han Crl : WI (Han) male rats", a "Multiplex MAP
  **Rat** Kidney Toxicity Magnetic Bead Panel 2", dosing "at 40 mg / kg on days 1 and 8",
  and sacrifice "on day 15". Species distribution moves from mouse 30 / rat 8 to
  **rat 29 / mouse 9**; rows lacking a dose fall from 54 to 33. Merged view grows to 40
  columns. After this round: all enum/FK/range checks pass, 0 orphans, 0 broken
  documentation links.

- **2026-09-03 (b)** — Extracted **US 11,105,794 Table 2**, acquired with the patent in
  June but never mined (`SOURCES.md` recorded it as "not yet extracted"). 48 quantitative
  **human in-vitro** rows (`MSR112`–`MSR159`): compounds 1-1 / 3-1 / 4-1 (`OLG045`,
  `OLG047`, `OLG048`) × 4 concentrations (3/10/30/100 µM) × 2 human systems (primary
  human PTEC, PTEC-TERT1) × 2 timepoints (day 3, day 6), readout `extracellular_EGF` as
  % of saline control under **gymnotic** (naked, untransfected) exposure. The page's
  naive text layer interleaves the columns into an unusable number stream, so
  `scripts/extract_patent_table2.py` re-parses the layout-preserving extraction on every
  run and checks 4 values against the patent's printed table before writing — no number
  is hand-transcribed. Grades assigned by a stated fold-over-saline rubric (<200 / 200–499
  / 500–1499 / ≥1500 → 0/1/2/3) whose floor is anchored so the patent's own innocuous
  control grades 0 in all 16 of its cells; verified, and grade tracks the patent's in-vivo
  class monotonically (innocuous 16×g0; medium 10/3/2/1; high 4/4/4/4). All rows
  `grade_provisional`; raw % and SD retained so any regrade needs no return to the PDF.
  Effect: measurements 111 → **159**; **human in-vitro 19 → 67 (17.1% → 42.1%, now the
  largest class)**; human/animal bridge set 9 → **12 oligos**, the three new ones being
  same-compound/same-lab human-in-vitro-vs-rat-in-vivo pairs with no cross-study
  confounding.

- **2026-09-03 (c)** — Added the three approved DMD PMOs that carried **no rows at all**:
  golodirsen (`OLG011`), casimersen (`OLG012`), viltolarsen (`OLG013`). Labels read
  directly on DailyMed (`accessdata.fda.gov` is unreachable here); all three carry a
  Warnings-and-Precautions "Kidney Toxicity" subsection with the same structure — kidney
  toxicity seen in **animals**, **not** seen in the human studies, and renal monitoring
  nonetheless mandated. 6 rows (`MSR160`–`MSR165`, source_id `A11`–`A13`): one human
  clinical and one animal per drug. New `source_id` values `A11`/`A12`/`A13`;
  `system_model` gains `DMD_patients` and `nonclinical_label_summary`.
  These human grade-0 rows are **measured negatives, not absence of reporting** — the
  labels prescribe the analytes ("serum cystatin C, urine dipstick, and urine
  protein-to-creatinine ratio ... monitor urine dipstick every month, and serum cystatin C
  and UPCR every three months") and then state the result was negative. That is the
  distinction `CLINICAL_VALIDATION.md` found missing from the WS grade-0 rows, and adding
  them **weakened the provenance/outcome confound 3.7×** (one-sided Fisher
  p = 4.5 × 10⁻⁵ → **1.65 × 10⁻⁴**; anchor-sourced grade-0 clinical rows 1 → 4). The
  confound is reduced, not resolved.
  All three labels also warn that "creatinine may not be a reliable measure of kidney
  function in DMD patients" because of reduced skeletal muscle mass — recorded in `notes`,
  and relevant to every DMD row in the dataset (drisapersen, eteplirsen, golodirsen,
  casimersen, viltolarsen). Serum-creatinine-based renal readouts in DMD populations
  should be read with that caveat.
  Effect: measurements 159 → **165**; human_clinical 39 → **42**; animal_invivo 53 → **56**;
  bridge set 12 → **15 oligos**.

- **2026-09-03 (d)** — Final pre-submission round. Extracted **US 11,479,818 Table 5**
  (`N4`, previously unmined): 81 rows, 9 panel compounds × 3 concentrations × 3 biomarkers
  (`EGFR_mRNA`, `KIM-1_mRNA`, `KIM-1_protein`) on **rat primary PTEC**. Values are
  normalised to compound 1-1, **not** saline (`readout_unit = pct_compound_1-1_reference`)
  and must not be pooled with the N3 Table 2 %-saline values. 4 anchors checked against
  the printed table; compound 1-1 grades 0 on all 9 of its cells by construction.
  These are animal *cell* data, which exposed a real defect: `subject_class` previously
  mapped every non-human row to `animal_invivo`. Added **`animal_invitro`**, so the four
  classes are now human_clinical 42 / human_invitro 67 / animal_invitro 81 / animal_invivo 56.
  Added **`renal_endpoints_measured`** to `measurements.csv`, implementing the
  `CLINICAL_VALIDATION.md` recommendation: `measured_and_reported` 233 / `cannot_determine` 8
  / `not_measured` 3 / `not_reported_in_source` 2. **13 grade-0 clinical rows are now
  explicitly flagged as not supported as measured negatives.**
  Added **`purity_pct`**, **`purity_method`** (TBD for all 65 — verified unavailable: both
  patents searched for purity/HPLC/UPLC/LC-MS/mass-spec language, none present) and
  **`identity_confirmation`** (who_inn_chemical_nomenclature 20 / patent_sequence_listing 25
  / regulatory_label 7 / peer_reviewed_publication 3 / not_established 10), answering the
  identity half of the Phase 2 characterization requirement.
  Added a repository-root **`LICENSE`** (CC BY 4.0) with third-party source material
  explicitly excluded and per-row `redistribution` retained.
  Totals: **65 oligos (20 cols) · 246 measurements (25 cols) · 246 merged (44 cols)**,
  0 orphans, all enum/range checks pass.

## Derived table — `data/oligotox_kidney_merged.csv` (generated, not canonical)

An analysis-ready **denormalized join** of the two canonical tables on `oligo_id`,
produced by `scripts/build_merged.py`.

- **Grain / size:** one row per measurement — **165 rows × 40 columns**.
- **Columns:** `measurement_id`, `oligo_id`, then all 15 oligo **design predictors**
  + `notes_oligo`, then all 21 measurement **outcome/context** fields + `notes_measurement`
  (including `subject_class`, so the human/animal split is filterable in the flat view).
  (The two source `notes` columns are disambiguated to `notes_oligo` /
  `notes_measurement`; `oligo_id` appears once.)
- **Purpose:** each row carries the **predictors and the graded outcome together**,
  so downstream EDA / model training needs no join. Supports the challenge's
  "data translatability" dimension.
- **Status:** **generated and derived — not a source of truth.** `data/oligos.csv`
  and `data/measurements.csv` remain canonical; regenerate this file with
  `python scripts/build_merged.py` after any change, and never hand-edit it
  (denormalization repeats each oligo's design across its measurement rows).

## Derived table — `data/human_animal_bridge.csv` (generated, not canonical)

One row per oligo carrying evidence on **both** sides of the human/animal divide,
produced by `scripts/split_human_animal.py`. This is the dataset's direct answer to
the Phase 2 "extrapolate between in vitro human systems and animal data" criterion,
so it is materialised rather than left for each consumer to recompute.

- **Grain / size:** one row per bridging oligo — currently **9 oligos**.
- **Columns:** `oligo_id`, `oligo_name`, `oligo_class`, `sequence_known`,
  `n_human_clinical`, `n_human_invitro`, `n_animal_invivo`, `human_max_grade`,
  `animal_max_grade`, `concordance`, `human_species_models`, `animal_species`.
- **`concordance`:** `concordant` \| `animal_over_predicts` \| `animal_under_predicts`,
  comparing the maximum human grade against the maximum animal grade for that oligo.
- **Read with care.** Concordance inherits the reliability of both grades. Where the
  human grade is an unvalidated 0 (see `CLINICAL_VALIDATION.md`), an
  `animal_over_predicts` verdict may be an artefact of *nobody having measured the
  human endpoint* rather than a true species difference. Two of the three current
  `animal_over_predicts` rows (lumasiran `OLG020`, vutrisiran `OLG022`) rest on
  exactly such grades and must not be cited as species-difference evidence until
  their human endpoints are sourced.
