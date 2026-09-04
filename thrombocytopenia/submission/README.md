# Phase 2 submission package — OligoTox-Thrombocytopenia

The four parts the Challenge requires, for the **thrombocytopenia / platelet-toxicity**
endpoint. Nothing here covers another endpoint.

| Part | File | Pages | Limit |
|---|---|---:|---:|
| 1. Narrative document | [`narrative.pdf`](narrative.pdf) | 9 | 12 |
| 2. Methodology document | [`methodology.pdf`](methodology.pdf) | 4 | 5 |
| 3. Public Access & Dissemination Plan | [`padp.pdf`](padp.pdf) | 3 | 5 |
| — Supporting: **Data Sources & Provenance** | [`sources.pdf`](sources.pdf) | 15 | none |
| 4. Dataset | [`OligoTox-Thrombocytopenia_dataset.xlsx`](OligoTox-Thrombocytopenia_dataset.xlsx) — single workbook — plus [`../data/`](../data/) CSVs and [`../schema.md`](../schema.md) | — | none |

The announcement allows the dataset "either by including a data file in Excel (or
similar format) or a document with instructions … on how to access and download
the raw data". Both are provided: a **single workbook** with every table on its
own sheet for reviewer convenience, and the canonical CSVs in the repository,
which remain the source of truth.

## The sources document

`sources.pdf` documents **every source behind the dataset**: 70 distinct sources
across six databases, each with its full citation, the database it came from, a
**clickable resolving link**, its rights class, how many rows it contributed
(human and animal separately), and how many distinct loci within it were cited.
It is generated from `data/measurements.csv`, so it cannot list a source the
dataset no longer uses or omit one it does.

| Database | Sources | Rows |
|---|---:|---:|
| Peer-reviewed literature (Europe PMC / PMC / doi.org) | 38 | 1,211 |
| FDA — Drugs@FDA review documents | 12 | 271 |
| EMA — EPAR assessment reports and SmPCs | 8 | 216 |
| USPTO patents (Google Patents) | 6 | 241 |
| FDA — prescribing information (DailyMed) | 4 | 14 |
| ClinicalTrials.gov posted results | 2 | 6 |

## Rebuilding the PDFs

Sources are HTML with a shared stylesheet carrying `{{placeholders}}`; every number
is substituted from the live dataset at render time, so a document cannot quote a
stale figure. Rendering is headless Chromium — no proprietary toolchain. The script
fails if a placeholder has no value, or if a document exceeds its page limit:

```
scripts/render_submission.py
```

## What part 4 comprises

| File | Content |
|---|---|
| `../data/oligos.csv` | oligonucleotides — identity and design predictors, incl. sequence, per-residue modification map, PS count, purity fields |
| `../data/measurements.csv` | graded per-measurement records with per-row provenance and rights |
| `../data/germans_analysis.csv` | **German's analysis** — one row per compound: oligo · sequence · modification · toxicity, worst-first |
| `../data/measurements_human.csv` | human rows, **denormalised** so sequence and toxicity grade sit beside every row |
| `../data/measurements_animal.csv` | animal rows, same denormalised shape |
| `../data/bridge_human_animal.csv` | compounds characterised on **both** sides — the extrapolation set |
| `../data/oligotox_thrombo_merged.csv` | generated denormalised analysis view |
| `../data/model_demo_results.json` | predictive-model demonstration results |
| `../schema.md` | data dictionary, controlled vocabularies, 0–3 grade rubric |
| `../SOURCES.md` | source registry with per-source redistribution class |
| `../curation/` | raw extractions, verification verdicts, source sweep |

Licence: **CC-BY 4.0**. Rights are tracked per row so a consumer can filter to
exactly the records they may lawfully reuse.
