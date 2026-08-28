# Kidney toxicity

Per-measurement curation of oligonucleotide **nephrotoxicity** — 71 oligonucleotides,
**769 graded measurements**, 35 target genes, every row `is_kidney_specific = TRUE`. An
in-silico curation of publicly reported data; no wet-lab work was performed.

Data dictionary: [`schema.md`](schema.md) · assembly and grading rules: [`METHODOLOGY.md`](METHODOLOGY.md) · source registry: [`SOURCES.md`](SOURCES.md).

## Status

| | |
|---|---|
| Measurements | 769 (`data/measurements.csv`, 23 columns) |
| Oligonucleotides | 71 (`data/oligos.csv`, 21 columns) |
| Merged analysis table | 769 × 43 (`data/oligotox_kidney_merged.csv`, generated) |
| Target genes | 35 |
| Sequences filled | 66 of 71 carry a `sequence_5to3` other than `TBD` (2 of those are `NA` — class-level pooled entries that are not a single molecule); 5 remain `TBD` |
| Source identifiers in use | 17 |
| Local source PDFs | 7 in [`sources/`](sources/) |
| Grades | provisional throughout — no subject-matter sign-off |
| Model-ready | **No.** See *Known issues and open work* |

## Why the endpoint is curated this way

Oligonucleotide nephrotoxicity is frequently **functional rather than cytotoxic**.
Phosphorothioate ASOs accumulate in proximal tubule epithelial cells through
megalin/cubilin-mediated endocytosis and impair reabsorption of low-molecular-weight
proteins — reversible proteinuria (α1-microglobulin, RAP) **with no loss of cell
viability**. A viability-only screen under-calls this phenotype.

Three consequences run through the schema:

- **Readouts are functional and injury-biomarker first.** 322 rows are `functional` and 166
  `injury_biomarker`, against 228 `viability`. The dominant readouts are ATP (221), EGF in
  supernatant (211), KIM-1 protein (123), EGFR mRNA (76) and KIM-1 mRNA (27).
- **The grade rubric separates functional from structural injury.** Grade 1 is explicitly
  *mild, functional, reversible, no viability loss*; grade 2 requires injury-biomarker
  elevation or histopathology. Rubric and in-vitro thresholds: [`schema.md`](schema.md).
- **The grain is one row per condition, not per compound.** One oligo at one concentration read out by
  both KIM-1 and viability is two rows, so a functional-positive / viability-negative pair on the same
  agent is representable. `tissue` is `proximal_tubule` on 696 rows and `kidney` on 73.

## Data files

| Path | Grain | Key |
|---|---|---|
| [`data/oligos.csv`](data/oligos.csv) | one row per unique oligonucleotide (identity + design predictors) | `oligo_id` |
| [`data/measurements.csv`](data/measurements.csv) | one row per oligo × model × delivery × dose × readout | `measurement_id`, FK `oligo_id` |
| [`data/oligotox_kidney_merged.csv`](data/oligotox_kidney_merged.csv) | denormalized join, generated — not canonical | `measurement_id` |
| [`data/patent_excluded_rows.json`](data/patent_excluded_rows.json) | 262 patent rows held out of the graded tables, with the reason for each | — |
| [`data/clinical_validation_2026-08.md`](data/clinical_validation_2026-08.md) | audit of the clinical rows against their cited sources | — |

Regenerate the merged table with `python scripts/build_merged.py`
([`scripts/build_merged.py`](scripts/build_merged.py)); never hand-edit it. Missing values are
the literal string `TBD`, never guessed and never imputed as zero.

The 262 held-out rows fall in eight classes: non-kidney systems (123), vehicle/untreated controls
(41), on-target pharmacology rather than toxicity (33), patent composite scores (20), small-molecule
reference nephrotoxicants (20), an ambiguous compound header not guessed at (15), absolute-unit
rows (8), nulls (2).

## Distributions

**Oligonucleotides (n = 71).** Class: ASO_gapmer 46 · GalNAc_siRNA 12 · splice_switching_ASO 4 · PMO 4 ·
siRNA 2 · other 2 · aptamer 1. Backbone: full_PS 51 · PS_PO_mix 15 · PMO_neutral 4 · mixed 1. Conjugate:
none 54 · GalNAc 16 · PEG_5prime 1. Stage: research_panel 36 · approved 18 · phase_3 6 · phase_2 5 ·
phase_3_discontinued 3 · phase_1 1 · approved_EMA 1 · class_review 1.

**Measurements (n = 769).**

| Field | Distribution |
|---|---|
| `nephrotox_grade` | 0: 372 · 1: 140 · 2: 151 · 3: 106 |
| `study_type` | in_vitro 677 · animal_invivo 53 · clinical 39 |
| `species` | human 635 · rat 110 · mouse 9 · multi_species 8 · monkey 7 |
| `delivery_method` | gymnotic_free_uptake 677 · systemic_dose 87 · intrathecal 3 · intravitreal 1 · oral 1 |
| `readout_category` | functional 322 · viability 228 · injury_biomarker 166 · clinical_renal_outcome 27 · histopathology 24 · accumulation 2 |
| `redistribution` | public_domain 705 · summary_stat 64 |

The corpus is dominated by in-vitro patent panels: `PTEC_TERT1` supplies 499 rows, `primary_rat_PTEC` 81, `primary_human_PTEC` 78.

## Sources

Seven PDFs are committed in [`sources/`](sources/). Six back rows; one is background.

| File | `source_id` | Rows |
|---|---|---|
| `US11105794_in_vitro_nephrotox_assay_patent.pdf` | `N3` | 431 |
| `US11479818_in_vitro_nephrotox_assay_patent_EGFR.pdf` | `N4` | 248 |
| `Moisan2017_EGF_uptake_nephrotox_ASO_invitro_PMC5363415.pdf` | `M1` | 11 |
| `Janssen2019_drisapersen_reversible_proteinuria_ciPTEC_PMC6796739.pdf` | `N2` | 10 |
| `Sandelius2020_urinary_kidney_biomarker_panel_ASO_tubular_tox_PMID33084520.pdf` | `K1` | 9 |
| `Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf` | `REV` | 4 |
| `Frazier2022_kidney_effects_review_ToxPathol.pdf` | — | 0 (background review) |

The remaining 11 source identifiers have **no local PDF** and account for 56 rows: `WS`
(36 rows, WebSearch-derived label and trial figures) and the clinical/regulatory anchors
`A1` (3), `A2` (1), `A3` (3), `A4` (5), `A5` (1), `A6` (1), `A7` (1), `A8` (2), `A9` (2),
`A10` (1). Each is identified by DOI, patent number or label in [`SOURCES.md`](SOURCES.md);
none of their values were verified against a retrieved full text in this repository.

## Presentation

[`presentation/`](presentation/) holds a Marp deck — [`PRESENTATION.md`](presentation/PRESENTATION.md),
its `assets/` SVGs, and three built binaries (`OligoTox-Kidney.pptx`, `OligoTox-Kidney-editable.pptx`,
`OligoTox-Kidney.pdf`, 6.6 MB together). **Both the source and the built binaries are stale relative to
this dataset**: they were built against the 111-row lineage and still state "65 oligos · 111
measurements", a grade split of 27/30/39/15, and "33 of 65" sequences. None of those figures describe
the 769-row data. The deck must be rebuilt from `data/` before it is shown.

## Known issues and open work

**`reconcile/` — two documentation lineages, not yet merged.** An earlier kidney lineage
carried 111 measurements; this one carries 769, and is a verified strict superset — all 111
`measurement_id`s are present plus 658 more, and its `oligos.csv` adds four columns
(`sequence_sense_5to3`, `sequence_source`, `sequence_redistribution`,
`purity_characterization`). The 111-row lineage is preserved at [`reconcile/`](reconcile/)
— [`data-111row-lineage/`](reconcile/data-111row-lineage/),
[`METHODOLOGY-111row-lineage.md`](reconcile/METHODOLOGY-111row-lineage.md),
[`schema-111row-lineage.md`](reconcile/schema-111row-lineage.md) — because **its
documentation is in places ahead of this folder's**, not behind it: it records a fourth
extraction path (WHO INN nomenclature parsing, with reverse-complement and
phosphorus-count self-checks), a duplex self-consistency QC step, and a per-compound
account of why each remaining sequence is unfilled, none of which appears in
[`METHODOLOGY.md`](METHODOLOGY.md). Conversely only this folder's [`schema.md`](schema.md)
documents the four added columns and the in-vitro grading thresholds. **Merging the two doc
lineages is open work.** Until it is done, `METHODOLOGY.md` §7 and §8 still report the old
65-oligo / 111-measurement distributions and should not be quoted; the distributions above
are recomputed from the CSVs.

**`clinical_validation_2026-08.md` was computed on the 111-row lineage.** Its Fisher exact
test (p = 4.5 × 10⁻⁵), its 11/39 base rate and its 20-vs-19 provenance cross-tabulation all
derive from that dataset and **have not been recomputed on 769**. The clinical stratum is 39
rows in both, so its conclusions are likely to carry — but that is an expectation, not a
result. Its central finding (verification status predicts the label, so a model would partly
learn "does this compound have a regulatory paper trail") and its recommended
`renal_endpoints_measured` field remain **unapplied**: no such column exists in `schema.md`
or the data. On the strength of it, this dataset should not yet train a nephrotoxicity model.

**REVIEW blocker B1 is resolved in this dataset.** [`../REVIEW-2026-08.md`](../REVIEW-2026-08.md)
reports as its headline blocker that 21 patent-derived rows record a rat study as mouse, a
15-day design as 7 days, and drop the published dose. Verified here: the 21 `N3` in-vivo rows
(`MSR91`–`MSR111`) all carry `species = rat`, `system_model = rat_invivo_Wistar_Han_14day`,
`dose_or_conc_value = 40` mg/kg and `exposure_duration = 2_doses_d1_d8_necropsy_d15` —
matching US 11,105,794's "Measuring In Vivo Nephrotoxicity" section, which binds Table 1 to
purpose-bred Wistar Han Crl:WI(Han) male rats dosed 40 mg/kg on days 1 and 8 with necropsy
on day 15. **B1 needs no further action here.**

**The rest of that review still applies.** Its remaining kidney findings — grading,
provenance-locus precision, tissue granularity, the `WS` tier, licensing and deck claims —
are in [`../REVIEW-2026-08.md`](../REVIEW-2026-08.md) and are not restated here. Two caveats
on reading it: it was written against the 111-row lineage only, so its row counts and line
references point at that data; and its claims that other endpoints have zero rows are wrong,
because it could see only one of four branches.

**Smaller items verified in this data.** `system_model` is inconsistently spelled — `PTEC_TERT1` on
499 rows and `PTEC-TERT1` on 8 — which will split naively on grouping. [`SOURCES.md`](SOURCES.md) still
describes a `sources/kidney/` · `hepatotox/` · `reference/` · `_unrelated/` layout; `sources/` is now
flat and holds only the seven PDFs above, the rest having been reallocated to the endpoint folders they
belong to. All grades remain `grade_provisional`.
