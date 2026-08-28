# Methodology — OligoTox-Kidney Dataset

Methodology and provenance documentation for the **OligoTox-Kidney** dataset, a
curated, openly-releasable, per-measurement dataset of oligonucleotide
**kidney toxicity / nephrotoxicity** for the NIH/NCATS Oligonucleotide Toxicity
(OligoTox) Open Data Challenge, **Phase 2 (Data Generation Phase)**.

> **Nature of the dataset.** This is an **in-silico curation** of pre-existing,
> publicly reported data — not wet-lab-generated data. The "materials and
> methods" below therefore describe **source identification, extraction,
> harmonization, grading, provenance, and quality control**, i.e. how the
> dataset was *assembled and computationally processed*, in the spirit of the
> Phase 2 methodology requirement.

Snapshot of the dataset shipped in this folder: **71 oligonucleotides · 769 measurements ·
35 `target_gene` values (34 excluding the `TBD` placeholder) · all strict-kidney**
(`is_kidney_specific = TRUE`).

> **Stale figures below.** Sections 7, 8 and 11 of this document were written against the
> superseded 111-measurement / 65-oligo lineage and their distributions have **not** been
> recomputed against the 769-row data shipped here. Treat every count in those sections as
> historical. The current distributions are in [`README.md`](README.md); the superseded
> lineage is preserved under [`reconcile/`](reconcile/). Recomputing sections 7, 8 and 11 is
> open work.

---

## 1. Scope and design decisions

- **Endpoint:** kidney toxicity / nephrotoxicity (a named OligoTox endpoint of interest).
- **Granularity:** **strict-kidney, per-measurement.** One row =
  oligo × cell-model/subject × delivery × concentration/dose × readout.
- **Coverage goal:** span all therapeutic oligonucleotide modalities, study
  types (in-vitro / animal / clinical), and the full toxicity-severity range,
  including **negative controls**.
- **Driving domain fact:** oligonucleotide nephrotoxicity is frequently
  **functional, not cytotoxic** — phosphorothioate ASOs accumulate in proximal
  tubule epithelial cells via megalin/cubilin endocytosis, producing reversible
  low-molecular-weight proteinuria (impaired albumin/α1-microglobulin/RAP
  reabsorption) **without loss of viability**. The schema therefore captures
  functional and injury-biomarker readouts (KIM-1, NGAL, clusterin, cystatin C,
  A1M, lysosomal load), not viability alone.

## 2. Data model

Two normalized UTF-8 CSV tables joined on `oligo_id` (full data dictionary,
controlled vocabularies, and the grading rubric are in **`schema.md`**):

| File | Grain | Key |
|------|-------|-----|
| `data/oligos.csv` | one row per unique oligo (identity + design predictors) | `oligo_id` (PK) |
| `data/measurements.csv` | one row per oligo × model × delivery × dose × readout | `measurement_id` (PK), `oligo_id` (FK) |

Missing/unknown values are the literal string `TBD` (never guessed, never
imputed as zero).

## 3. Source identification and prioritization

Sources were prioritized **kidney-first** and catalogued in `SOURCES.md`
with stable identifiers, redistribution status, and acquisition state. Three tiers:

1. **Strict-kidney primary sources** — e.g. Janssen et al. 2019 (drisapersen,
   ciPTEC; PMC6796739); Sandelius et al. 2020 (urinary kidney biomarker panel;
   PMID 33084520); van Poelgeest 2013 (SPC5001); the Wu et al. marketed-ASO
   nephrotoxicity review (PMC10174585).
2. **Regulatory / clinical anchors** — FDA/EMA labels, prescribing information,
   and pivotal-trial publications for marketed/clinical oligonucleotides.
3. **Hepatotoxicity panels (fallback, flagged non-kidney)** — Dieckmann 2018,
   Burdick 2014, Hagedorn 2013; retained for chemistry/design diversity only and
   would be flagged `is_kidney_specific = FALSE`. *(None ingested as rows yet.)*

## 4. Data acquisition and extraction

Three extraction paths were used, each recorded per row via `source_id`:

1. **Local full-text extraction.** Primary-source PDFs supplied by the team were
   parsed with **PyMuPDF** (text + tables). Per-measurement values, doses,
   sequences, and figure/table loci were transcribed by hand into the schema.
   *(e.g. `N2` drisapersen → MSR017–026; `K1` Sandelius → MSR031–039.)*
2. **Secondary-source / review extraction.** Aggregating reviews (`REV` = Wu et
   al.) were used for marketed-drug renal findings, cross-checking primary data.
3. **`WS` (WebSearch-derived).** Because this environment's network policy blocks
   outbound full-text fetch, label/trial figures that were not supplied as files
   were taken from **search-engine summaries of the specific FDA/EMA label,
   clinical trial, or nonclinical paper named in each row's `source_ref`**. These
   are flagged `source_id = WS` and should be **verified against the cited
   primary source before publication.**

> **No-fabrication policy (strict).** `sequence_5to3` and any toxicity
> `readout_value` are **never invented or recalled from memory**. A sequence is
> filled only when an explicit string is returned by a credible source (e.g.
> inotersen, corroborated independently by the vutrisiran guide strand);
> otherwise it remains `TBD`. Compounds lacking published renal data were
> **omitted**, not padded.

## 5. Harmonization and controlled vocabularies

All categorical fields use the controlled vocabularies enumerated in `schema.md`.
The dictionary is reconciled to the data after each ingestion round (see the
**Data-dictionary QC log** in `schema.md`); vocabulary added during curation
(e.g. `delivery_method ∈ {intrathecal, intravitreal, oral}`, `conjugate = PEG`,
`species = multi_species`) is documented there rather than left implicit.

## 6. Toxicity grading

Each measurement carries an ordinal **`nephrotox_grade` (0–3)** assigned from the
reported endpoint per the rubric in `schema.md` (0 = no signal; 1 = mild/
functional/reversible, no viability loss; 2 = moderate injury-biomarker/
histopathology; 3 = severe AKI/glomerulonephritis/renal failure). Grades are
currently flagged **`grade_provisional`** in `notes`, pending scientific sign-off.

## 7. Independent (predictor) variables and their distribution

Design predictors hypothesized to drive nephrotoxicity, per `oligos.csv`
(n = 65 oligos):

| Variable | Distribution |
|----------|--------------|
| **Modality** (`oligo_class`) | ASO gapmer 40 · GalNAc-siRNA 12 · splice-switching ASO 4 · PMO 4 · siRNA 2 · 1st-gen PS-DNA (`other`) 2 · aptamer 1 |
| **Backbone** | full-PS 45 · PS/PO-mix 15 · PMO-neutral 4 · mixed 1 |
| **Conjugate** | none 48 · GalNAc 16 · PEG 1 |
| **Development stage** | approved 19 · research panel 30 · phase 3 (incl. discontinued) 9 · phase 2 5 · phase 1 1 · class-level 1 |
| **Sequence available** | 33 / 65 (rest `TBD`, never guessed) |
| **Target genes** | 35 distinct |

## 8. Dependent (indicator) variables and their distribution

Toxicity indicators per `measurements.csv` (n = 111):

| Variable | Distribution |
|----------|--------------|
| **`nephrotox_grade`** | 0: 27 · 1: 30 · 2: 39 · 3: 15 |
| **Study type** | clinical 39 · animal 53 · in-vitro 19 |
| **Species** | human 58 · mouse 30 · monkey 7 · multi-species 8 · rat 8 |
| **Delivery route** | systemic 87 · gymnotic/free-uptake 19 · intrathecal 3 · intravitreal 1 · oral 1 |
| **Readout category** | functional 35 · clinical renal outcome 27 · histopathology 24 · injury-biomarker 16 · viability 7 · accumulation 2 |
| **Kidney-specific** | TRUE 111 / 111 |

Readouts emphasize the **functional / injury-biomarker** axis (KIM-1, NGAL,
clusterin, cystatin C, A1M, proteinuria) over viability, by design. The dataset
deliberately includes **27 grade-0 negative controls** spanning GalNAc-siRNA,
siRNA, intrathecal ASO, and aptamer modalities — and paired
functional-positive / structural-negative rows on the same agent (e.g.
drisapersen: grade-1 A1M proteinuria alongside grade-0 viability and grade-0
monkey histopathology), which encode the central functional-not-cytotoxic signal.

## 9. Provenance and redistribution

- Every measurement carries `source_id` + `source_ref` + `source_table` (exact
  figure/table/label section/claim).
- `redistribution` is tracked per row: regulatory documents (FDA/EMA) →
  `public_domain`; journal-derived statistics → `summary_stat`; use `verify`
  where rights are unresolved. The 16 source identifiers in use are documented in
  `SOURCES.md`.
- Intended public license: a permissive open license (e.g. CC-BY) for the curated
  tables; underlying third-party full texts are **referenced, not redistributed**.

## 10. Quality control

Automated checks run after every ingestion round:
- **Schema conformance** — every categorical value validated against the
  `schema.md` enums; column-count integrity (17 / 23).
- **Referential integrity** — `measurements.oligo_id` → `oligos.oligo_id`
  (0 orphans); no duplicate primary keys.
- **Range checks** — `nephrotox_grade ∈ {0,1,2,3}`; booleans `TRUE/FALSE`.
- **Sequence policy** — only explicitly-sourced sequences filled; all others `TBD`.

## 11. Known limitations

- **Provisional grades** pending scientific (subject-matter) review.
- **Sequence coverage 33/65**; remaining marketed-oligo sequences are published
  (patents/INN) but were not transcribable from available summaries.
- **`WS` rows** rest on secondary search summaries of primary regulatory/trial
  sources and must be verified before release.
- **Species translation** — animal toxicology is known to *over-predict* human
  renal effects for 2′-MOE ASOs; this is captured explicitly (e.g. the Crooke
  pooled-human entry) and should be modeled, not ignored.
- **In-vitro human-system rows are still under-represented** (19/111); expanding
  these (e.g. the pending in-vitro nephrotoxicity-assay patents and ciPTEC/
  RPTEC-TERT1 panels) is the priority for the next ingestion round.

## 12. Reproducibility

The repository is self-documenting: `README.md` (strategy + live record counter),
`schema.md` (dictionary + QC log), `SOURCES.md` (source registry +
acquisition state), and this file. Extraction used open tooling (PyMuPDF; standard
CSV). Every row is traceable to a citable locus, so any value can be independently
re-verified against its `source_ref`.

## 13. Intended use for predictive modeling

The two-table design exposes granular **sequence + chemistry + design**
predictors against graded, per-condition renal outcomes, supporting models that
predict nephrotoxic potential from oligonucleotide design — including the
clinically important distinction between **reversible functional proteinuria**
and **structural tubular injury**, and the **animal-to-human** translation gap.
