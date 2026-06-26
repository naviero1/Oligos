# OligoTox-Kidney — A Curated Nephrotoxicity Dataset for Oligonucleotide Therapeutics

A curated, openly-releasable, per-measurement dataset of **kidney toxicity /
nephrotoxicity** signals for therapeutic oligonucleotides, built for the
**NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge, Phase 2**
(Data Generation Phase; submission window 1 May – 31 Dec 2026).

The deliverable is a **dataset**, not a model: openly-releasable,
well-documented, and reproducible — which is what NCATS scores.

---

## ⚠️ Reconstruction note (2026-06-26)

The original repository contents from the prior working session
(`README.md`, `schema.md`, `data/oligos.csv` with 21 oligos,
`data/measurements.csv` with 22 anchor rows, `sources/SOURCES.md`) were
**never committed or pushed**, so they were lost when that ephemeral
container was reclaimed. The remote (`naviero1/Oligos`) was empty when this
session started.

These scaffolding files (`README.md`, `schema.md`, `sources/SOURCES.md`, and
the **header-only** data CSVs) have been **reconstructed faithfully from the
project specification** and **committed + pushed immediately** so they are now
durably persisted. **No oligo identities, sequences, or toxicity values were
re-invented** — those must be restored from a backup of the prior files or
re-derived from primary sources (see `sources/SOURCES.md`). The current record
counter therefore reflects reality: **0 measurement rows**.

---

## Scope (decided — not under review)

- **Endpoint:** Kidney toxicity / nephrotoxicity (a named OligoTox endpoint of interest).
- **Approach:** In-silico **curation** of existing data (no wet lab).
- **Coverage:** All oligo classes — ASO gapmer, siRNA / GalNAc-siRNA,
  splice-switching ASO / PMO, aptamer.
- **Granularity:** **Strict-kidney, per-measurement.** One row =
  oligo × cell-model × delivery × concentration × readout.
- **Target:** ≥ 100 measurement records.

## Why this design — key domain facts

1. **Oligo nephrotoxicity is often FUNCTIONAL, not cytotoxic.** PS-ASOs
   accumulate in proximal tubule epithelial cells via megalin/cubilin
   endocytosis, causing reversible low-molecular-weight proteinuria
   (impaired albumin / α1-microglobulin / RAP reabsorption) **with no loss of
   viability**. Viability-only readouts under-call this. The schema therefore
   captures **functional and injury biomarkers** (KIM-1, NGAL, clusterin,
   cystatin C), lysosomal load, and proteinuria — not just viability.
2. **Toxicity is driven by sequence + chemistry + design TOGETHER**, not
   chemistry alone — so `oligos.csv` records granular design predictors.
3. **Marketed-drug data alone is too small** (~24 approved oligos, few with
   renal signals). Volume must come from **in-vitro sequence panels** in
   supplementary tables. Most large panels are *hepatotoxicity*; kidney-specific
   data is thinner — hence the kidney-first source prioritization.

## Data model (see `schema.md` for the full dictionary)

Two normalized tables joined on `oligo_id`:

| File | Grain | Key |
|------|-------|-----|
| `data/oligos.csv` | one row per unique oligo (identity + design predictors) | `oligo_id` (PK) |
| `data/measurements.csv` | one row per oligo × cell-model × delivery × concentration × readout | `measurement_id` (PK), `oligo_id` (FK) |

Graded label: **`nephrotox_grade` 0–3** (rubric in `schema.md`). Inotersen
(grade-3 glomerulonephritis) is the canonical severe anchor.

## Record counter

| | Count | Target |
|---|------|--------|
| Unique oligos (`oligos.csv`) | **31** | — |
| Measurement rows (`measurements.csv`) | **58** | **≥ 100** |
| — of which strict-kidney | **58** | majority |
| — of which hepatotox fallback (flagged) | **0** | as needed |
| Grade distribution (0/1/2/3) | 14 / 20 / 18 / 6 | — |
| Oligo classes — gapmer / GalNAc-siRNA / SSO / PMO / LNP-siRNA / aptamer / 1st-gen-PS-DNA | 11 / 8 / 4 / 4 / 1 / 1 / 2 | all |
| Delivery routes (systemic/gymnotic/intrathecal/intravitreal/oral) | 47 / 6 / 3 / 1 / 1 | 5 routes |
| Study types (clinical/animal/in-vitro) | 30 / 22 / 6 | mixed |
| Oligos with sequence (not TBD) | **3** | all |

_Update this table in the same commit whenever rows are added._

> **Provisional anchor rows (2026-06-26):** the 16 seed rows are marketed-oligo
> **clinical/regulatory** renal outcomes re-derived via `WebSearch` with full
> citations (FDA/EMA labels, NEJM, AJKD, Br J Clin Pharmacol, Arch Toxicol,
> Liver Int). Every `nephrotox_grade` is assigned per the `schema.md` rubric and
> flagged `grade_provisional` in `notes` — **pending scientific sign-off**. No
> toxicity values were fabricated; numeric `readout_value`/`sequence_5to3` left
> `TBD` where a primary source is still needed. These are **in-vivo/clinical**
> anchors; the >100-record **in-vitro** volume still requires the `sources/`
> drops (see `sources/SOURCES.md`).
>
> **First primary-source extraction (drisapersen / N2):** rows MSR017–026 and
> OLG008–010 were extracted from the uploaded open-access paper (Janssen 2019,
> PMC6796739) — including 3 published **sequences** and strict-kidney **in-vitro
> ciPTEC** rows that capture the functional-not-cytotoxic phenotype (A1M
> proteinuria grade 1; no viability loss and no tubular damage = grade 0).

## Provenance & licensing

- Every measurement row is traceable to a **source DOI / patent number + table
  or figure** (`source_id`, `source_ref`, `source_table` columns).
- **Redistribution is tracked per row** (`redistribution` column):
  - USPTO patents → **public domain**, values may be reproduced.
  - Journal supplementary tables → may be restricted to **derived features /
    summary statistics only**; check each source's license before copying raw
    values.
- **Sequences are never guessed.** `sequence_5to3` is `TBD` unless taken from a
  redistribution-permitted source.

## Status & next steps

This session's network policy **blocks all outbound web fetch** (org egress
policy denies the CONNECT tunnel to every host — PMC, USPTO, publishers all
return 403; only `WebSearch` summaries are available). Primary-source files
must therefore be **dropped into `sources/` by the user** for local extraction.
See `sources/SOURCES.md` for the exact drop-list and harmonization plan.
