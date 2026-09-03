# Phase 2 submission package — OligoTox-Thrombocytopenia

The four parts the Challenge requires, for the **thrombocytopenia / platelet-toxicity**
endpoint. Nothing here covers another endpoint.

| Part | File | Pages | Limit |
|---|---|---:|---:|
| 1. Narrative document | [`narrative.pdf`](narrative.pdf) | 9 | 12 |
| 2. Methodology document | [`methodology.pdf`](methodology.pdf) | 4 | 5 |
| 3. Public Access & Dissemination Plan | [`padp.pdf`](padp.pdf) | 3 | 5 |
| 4. Dataset | [`OligoTox-Thrombocytopenia_dataset.xlsx`](OligoTox-Thrombocytopenia_dataset.xlsx) — single workbook — plus [`../data/`](../data/) CSVs and [`../schema.md`](../schema.md) | — | none |

The announcement allows the dataset "either by including a data file in Excel (or
similar format) or a document with instructions … on how to access and download
the raw data". Both are provided: a **single workbook** with every table on its
own sheet for reviewer convenience, and the canonical CSVs in the repository,
which remain the source of truth.

## Rebuilding the PDFs

Sources are HTML with a shared stylesheet, rendered by headless Chromium — no
proprietary toolchain:

```
scripts/build_submission.sh
```

## What part 4 comprises

| File | Content |
|---|---|
| `../data/oligos.csv` | 254 oligonucleotides — identity and design predictors, incl. sequence, per-residue modification map, PS count, purity fields |
| `../data/measurements.csv` | 1,878 graded per-measurement records with per-row provenance and rights |
| `../data/measurements_human.csv` | 1,372 human rows |
| `../data/measurements_animal.csv` | 497 animal rows |
| `../data/bridge_human_animal.csv` | 22 compounds characterised on **both** sides — the extrapolation set |
| `../data/oligotox_thrombo_merged.csv` | generated denormalised analysis view |
| `../data/model_demo_results.json` | predictive-model demonstration results |
| `../schema.md` | data dictionary, controlled vocabularies, 0–3 grade rubric |
| `../SOURCES.md` | source registry with per-source redistribution class |
| `../curation/` | raw extractions, verification verdicts, source sweep |

Licence: **CC-BY 4.0**. Rights are tracked per row so a consumer can filter to
exactly the records they may lawfully reuse.
