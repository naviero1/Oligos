# Schema — OligoTox-Thrombocytopenia dataset

Two normalized tables joined on `oligo_id`. All files are UTF-8 CSV with a
header row. Missing/unknown values are the literal string `TBD` (never guessed,
never blank-as-zero). Booleans are `TRUE`/`FALSE`.

This schema deliberately **mirrors the OligoTox-Kidney schema** (`../schema.md`)
so the two datasets are joinable on `oligo_id` semantics and share controlled
vocabularies wherever the biology allows. Only the endpoint-specific columns
(`system_model`, `tissue`, `readout_category`, `readout_name`,
`thrombocytopenia_grade`, `is_platelet_specific`) diverge.

---

## Table 1 — `data/oligos.csv`

One row per **unique oligonucleotide** (identity + design predictors). Identical
column set to the kidney dataset — these are the chemistry/sequence/design
features hypothesized to drive toxicity.

| Column | Type | Description / controlled vocabulary |
|--------|------|-------------------------------------|
| `oligo_id` | string PK | Stable ID, e.g. `TOLG001`. Never reused. |
| `oligo_name` | string | Common/INN name, e.g. `inotersen`, `volanesorsen`. |
| `aliases` | string | `;`-separated alternates, e.g. `IONIS-TTRRx;ISIS 420915`. |
| `oligo_class` | enum | `ASO_gapmer` \| `siRNA` \| `GalNAc_siRNA` \| `splice_switching_ASO` \| `PMO` \| `aptamer` \| `other`. |
| `target_gene` | string | Intended molecular target (e.g. `TTR`), or `NA` for non-hybridizing aptamers. |
| `indication` | string | Disease/indication, free text. |
| `developer` | string | Sponsor/developer. |
| `max_phase` | enum | `approved` \| `approved_EMA` \| `phase_3` \| `phase_3_discontinued` \| `phase_2` \| `phase_2_discontinued` \| `phase_1` \| `preclinical` \| `research_panel` \| `class_review`. |
| `length_nt` | int | Oligonucleotide length in nucleotides. |
| `backbone_chemistry` | enum | `full_PS` \| `PS_PO_mix` \| `full_PO` \| `PMO_neutral` \| `mixed` \| `NA` (no internucleotide linkage exists — mononucleotide controls; distinct from `TBD` = unknown) \| `TBD`. |
| `sugar_modifications` | string | `;`-separated, e.g. `2'-MOE;2'-OMe;cEt;LNA;2'-F;morpholino;DNA_gap`. |
| `gapmer_design` | string | Wing-gap-wing motif if applicable, e.g. `5-10-5_MOE`; else `NA`. |
| `conjugate` | enum | `none` \| `GalNAc` \| `lipid` \| `peptide` \| `PEG` \| `other`. |
| `ps_count` | int | Number of phosphorothioate linkages, or `TBD`. **Central predictor for this endpoint** — PS content drives platelet binding. |
| `sequence_5to3` | string | 5′→3′ sequence, bases only. **`TBD` unless from a redistribution-permitted source. Never guessed.** `NA` where no sequence exists (mononucleotide controls). |
| `modification_map` | string | **Per-residue modification notation exactly as printed by the source**, e.g. `mG*mC*mG*mA*…` where `*` marks a phosphorothioate linkage and a leading letter a 2′-modified residue. Phase 2 requires "the location of all chemical modifications in each oligo"; `sequence_5to3` holds bases only, so this column carries the positional detail that would otherwise be normalised away. `TBD` where the source printed no residue-level notation — `gapmer_design` then gives wing/gap boundaries and `sugar_modifications` the chemistries present. |
| `purity_pct` | float | Reported purity, e.g. `95.2`. `TBD` where the source does not state it — **which is the usual case**, see the note below. |
| `purity_method` | string | Method behind `purity_pct` / identity confirmation, e.g. `HPLC`, `LC-MS`, `CE`, `MALDI-TOF`. `TBD` where unstated. |
| `design_source` | string | Source for the design metadata (DOI / patent / label). |
| `notes` | string | Free text. |

---

## Table 2 — `data/measurements.csv`

One row per **oligo × model/subject × delivery × concentration/dose × readout**.
A single oligo at a single dose reporting platelet count *and* P-selectin =
**two rows**.

| Column | Type | Description / controlled vocabulary |
|--------|------|-------------------------------------|
| `measurement_id` | string PK | Stable ID, e.g. `TMSR001`. |
| `oligo_id` | string FK | → `oligos.oligo_id`. |
| `study_type` | enum | `in_vitro` \| `ex_vivo` \| `animal_invivo` \| `clinical`. |
| `species` | enum | `human` \| `monkey` \| `rat` \| `mouse` \| `dog` \| `minipig` (Göttingen minipig — an established regulatory tox species with its own GPVI/PF4 ontogeny data here) \| `multi_species` \| `NA`. |
| `system_model` | string | e.g. `washed_human_platelets`, `human_PRP`, `human_whole_blood`, `CD34_derived_megakaryocytes`, `MEG-01`, `bone_marrow`, `patient_cohort`, `healthy_volunteer`, `cynomolgus_invivo`, `mouse_invivo`. |
| `tissue` | string | `platelet` \| `blood` \| `plasma` \| `bone_marrow` \| `spleen` \| `NA`. |
| `delivery_method` | enum | `direct_addition` (in-vitro spike into platelets/blood) \| `gymnotic_free_uptake` \| `transfection` \| `conjugate_mediated` \| `systemic_dose` \| `intrathecal` \| `intravitreal` \| `oral` \| `TBD`. |
| `dose_or_conc_value` | float *or band string* | Numeric concentration or dose, or `TBD`. **May also carry a dose *band* exactly as printed** (e.g. `>175-275`, `>475`) where the source reports incidence per dose band rather than at a point dose — as the large pooled clinical tables do. Bands are recorded verbatim rather than converted to invented midpoints; a consumer that needs a numeric column should parse or bin these explicitly rather than coercing them silently. |
| `dose_or_conc_unit` | enum | `uM` \| `nM` \| `ug/mL` \| `mg/kg` \| `mg` (total dose) \| `fold_Cmax` \| `NA`. |
| `exposure_duration` | string | e.g. `15min`, `72h`, `13wk`, `chronic`; or `TBD`. |
| `readout_category` | enum | `platelet_count` \| `platelet_activation` \| `platelet_aggregation` \| `platelet_binding` \| `megakaryocyte` \| `immunogenicity` \| `clinical_outcome` \| `histopathology` \| `viability` \| `coagulation`. |
| `readout_name` | string | e.g. `platelet_count`, `platelet_nadir`, `grade4_thrombocytopenia_incidence`, `thrombocytopenia_incidence`, `CD62P_P-selectin`, `PAC-1_binding`, `platelet_aggregation`, `GPVI_binding`, `GPIIbIIIa_binding`, `anti-platelet_antibody`, `PF4_release`, `megakaryocyte_count`, `bone_marrow_megakaryocyte_hyperplasia`, `bleeding_event`, `platelet_microaggregate`. |
| `readout_value` | float/string | Reported value, or `TBD` if qualitative-only. |
| `readout_unit` | string | e.g. `10^9/L`, `% of control`, `fold_change`, `pct_incidence`, `pct_subjects`, `EC50_uM`, `MFI`; or `NA`. |
| `effect_direction` | enum | `increase` \| `decrease` \| `no_change` \| `TBD`. |
| `effect_vs_control` | string | Quantified effect vs control if available (e.g. `3.2x`, `-45%`, `12pct_vs_2pct_placebo`), else `TBD`. |
| `thrombocytopenia_grade` | int 0–3 | Graded label (rubric below). |
| `is_platelet_specific` | bool | `TRUE` = strict platelet/thrombocytopenia row; `FALSE` = adjacent-hematology fallback row (flagged). |
| `subject_class` | enum | **Derived, never hand-entered** — the human/animal division: `human_clinical` \| `human_in_vitro` \| `human_ex_vivo` \| `human_other` \| `animal_in_vivo` \| `animal_in_vitro` \| `animal_ex_vivo` \| `animal_other` \| `multi_species` \| `unspecified`. Computed from `study_type` × `species` at assembly and **independently re-derived by `qc_thrombo.py`**, which fails the build on any disagreement, so it cannot drift from the columns it summarises. Pooled multi-species findings are assigned to **neither** side rather than forced. See `../STATUS.md` for why this axis is called out separately. |
| `source_id` | string | → entry in `SOURCES.md` (e.g. `T1`). |
| `source_ref` | string | DOI, PMID/PMCID, patent number, or regulatory label ID. |
| `source_table` | string | Exact locus, e.g. `Table 2`, `Fig 3B`, `Claim 7`, `label sec 5.1`. |
| `redistribution` | enum | `public_domain` \| `cc_by` \| `derived_features_only` \| `summary_stat` \| `verify`. |
| `notes` | string | Free text (e.g. `recovered_after_discontinuation`). |

---

## `thrombocytopenia_grade` rubric (0–3)

The endpoint has a **bimodal** clinical presentation, and the rubric is built to
preserve that distinction rather than average it away:

- a **common, mild, dose- and plasma-concentration-dependent** decline in
  platelet count that plateaus and is not immune-mediated; and
- a **rare, severe, idiosyncratic immune-mediated** thrombocytopenia with
  anti-platelet antibodies and platelet counts that can fall below 10 × 10⁹/L.

| Grade | Clinical definition (CTCAE-aligned) | In-vitro / ex-vivo analogue |
|-------|--------------------------------------|------------------------------|
| **0** | No platelet signal at tested exposure — platelet count unchanged, no activation, no bleeding. | No activation, aggregation, or binding above vehicle control at tested concentration. |
| **1** | **Mild / reversible** — platelet count decline that remains ≥ 100 × 10⁹/L (CTCAE grade 1), or a statistically significant but clinically non-actionable mean decline; no intervention. | Platelet **activation marker** rise (CD62P/P-selectin, PAC-1) or binding **without** aggregation, at supra-clinical concentration only. |
| **2** | **Moderate** — platelet count 50–99 × 10⁹/L (CTCAE grade 2–3 lower band), requiring monitoring, dose interruption, or dose reduction; or megakaryocyte/bone-marrow findings in animals. | Clear **aggregation** or activation at a **clinically relevant** concentration (≤ ~10× human Cmax); or dose-dependent megakaryocyte effect. |
| **3** | **Severe** — platelet count < 50 × 10⁹/L, CTCAE **grade 4** (< 25 × 10⁹/L), immune-mediated thrombocytopenia with confirmed anti-platelet antibodies, a **bleeding/haemorrhagic event attributable to thrombocytopenia**, treatment discontinuation for a platelet event, or death. *(e.g. inotersen — boxed warning; volanesorsen — dose-limiting.)* | Aggregation/activation at or below therapeutic plasma concentration, or demonstrated antibody-mediated platelet clearance. |

**Bleeding is graded on attribution, not on the word "bleeding".** Grade 3
requires a haemorrhagic event *attributable to thrombocytopenia*. A trial that
reports mild bleeding events at an incidence **at or below placebo** is
reporting a background rate, not a drug-induced platelet injury, and such rows
are graded on what was actually observed (typically 0–1) with the deviation
stated in `notes`. Grading them 3 on the keyword alone would manufacture severe
events out of a null result — the single easiest way to corrupt this endpoint.

**An explicit zero is grade 0, and it is evidence.** Where a source tabulates a
severe band and reports no events in it, that cell is a grade-0 row, not a
missing row. Such rows record in `notes` which grade the band *would* have
carried had events occurred, so severe-band cells remain findable and the
denominator is not lost.

**Control arms are graded on what was observed, so models must filter them.**
A placebo subject whose platelets genuinely fell below 75 × 10⁹/L *had* that
event, and the rubric grades the observed band regardless of study arm. The
dataset therefore contains **control-arm rows carrying grade 1–2**, correctly.
But a model joining grade to *design features* would read them as the compound
causing an effect at zero dose. **The canonical filter is
`dose_or_conc_value == "0"`**, and `qc_thrombo.py` reports the count on every run
so the hazard stays visible. Placebo rows are retained rather than dropped
because they carry the comparator denominators that make the treated rows
interpretable.

Grade is assigned **per measurement** from the reported endpoint; rows for the
same oligo may differ by model, dose, or readout. Record the rationale in `notes`
when the assignment is non-obvious. Where a source reports an incidence
(e.g. "3 % of patients had grade 4"), the row is graded on the **severity of the
event described**, and the incidence is carried in `readout_value`.

### A note on `purity_pct` / `purity_method`

Phase 2 requires the dataset to carry "**data on the purity and characterization of
each**" oligo. That requirement is written for teams *synthesising* compounds, who
hold HPLC/MS data for everything they made. This dataset is an **in-silico curation
of published results**, and the source literature very rarely reports purity for the
compounds it tests.

The columns exist so that purity is recorded wherever a source *does* state it
(patents sometimes do; some papers state ">90 % by HPLC"), and so the shortfall is
**visible rather than absent** — `qc_thrombo.py` reports coverage of these fields on
every run. They are not populated by inference, and a purity figure will never be
carried over from a different compound, batch, or paper.

---
## Provenance rules

- Every row MUST carry `source_id` + `source_ref` + `source_table`.
- `redistribution` governs whether raw values may be published:
  - `public_domain` — USPTO patents and FDA/EMA regulatory documents. Values may
    be reproduced without restriction.
  - `cc_by` — the source article is Creative Commons Attribution licensed (e.g.
    PLOS, many PMC open-access articles). Raw values **may be reproduced with
    attribution**; this is materially more permissive than `summary_stat` and
    should be used wherever the licence is confirmed rather than assumed.
    Confirm from the article's own licence field (Europe PMC `license`, or the
    article's rights statement) — not from the fact that it is free to read.
  - `derived_features_only` / `summary_stat` — copyrighted journal content where
    only derived features or summary statistics are reproduced under fair use.
  - `verify` — rights unresolved; must be settled before release.
- `sequence_5to3` and any toxicity `readout_value` are **never fabricated**.
  Use `TBD` and fetch the source.

---

## Derived table — `data/oligotox_thrombo_merged.csv` (generated, not canonical)

An analysis-ready **denormalized join** of the two canonical tables on
`oligo_id`, produced by `scripts/build_merged_thrombo.py`. One row per
measurement, carrying design predictors and the graded outcome together.
`data/oligos.csv` and `data/measurements.csv` remain canonical; regenerate this
file after any change and never hand-edit it.
