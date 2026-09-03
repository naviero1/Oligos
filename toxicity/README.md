# Toxicity register — the project's work indexed by endpoint

This directory indexes the repository by toxicity endpoint: one dossier per endpoint on the
OligoTox Challenge's list, so that a reader can see at a glance what has been done for each
one. Every dossier answers the same questions in the same order — which source PDFs are
held, which `source_id`s actually reach `data/measurements.csv`, how many oligos and
measurement rows exist, where the work lives elsewhere in the repo, and, where the answer is
none, why. The dossiers are an index and an allocation over artifacts that already exist;
they contain no measurement, oligo, sequence or citation of their own.

## Scope authority

The endpoint list is quoted verbatim from the Challenge brief
([`sources/reference/OligoTox_challenge_brief.pdf`](_shared/reference/OligoTox_challenge_brief.pdf),
page 1):

> Toxicities of interest include:
> Hepatotoxicity, kidney toxicity, thrombocytopenia, complement activation,
> coagulopathy, immunotoxicity, chronic neurotoxicity, and hydrocephalus.

The same page states that submissions focused on acute neurotoxicity, specifically
alterations of neuronal electrical activity, will be considered a lower priority than the
other toxicities of interest. Acute neurotoxicity therefore has no dossier here.

*Caveat, stated once and applied throughout:* that PDF is 6 pages. Pages 1 to mid-3 read as
an NCATS executive summary. From mid-page 3 the document changes character — markdown
listicles (`### Types of Toxicity`, `### Safety Assessment`), a six-entry bibliography whose
author fields are initials-only, and a closing offer of further details. Only pages 1–3a are
cited as scope authority anywhere in this register; no claim in it traces to pages 3b–6, and
those six bibliography entries are not treated as references.

## Coverage

Counts are recomputed from **two** datasets, which are separate and are not joined.
Kidney: [`kidney/data/oligos.csv`](kidney/data/oligos.csv) (65 × 17) and
[`kidney/data/measurements.csv`](kidney/data/measurements.csv) (111 × 23).
CNS: three endpoint folders, each holding only its own toxicity —
[`acute-neurotoxicity/data/`](acute-neurotoxicity/data/),
[`chronic-neurotoxicity/data/`](chronic-neurotoxicity/data/) and
[`hydrocephalus/data/`](hydrocephalus/data/). There is deliberately no combined CNS table; the
allocation rule lives in [`_shared/cns/src/endpoints.py`](_shared/cns/src/endpoints.py), and four
QC checks fail if any row sits in the wrong folder. The three share one source tree and one build
pipeline at [`_shared/cns/`](_shared/cns/). "Source PDFs held" counts
only PDFs filed to that endpoint alone; the 4 multi-endpoint reference PDFs are excluded here
and listed in the cross-cutting file instead.

| Endpoint | Status | Oligos | Measurement rows | Source PDFs held | `source_id`s reaching `measurements.csv` |
|---|---|---:|---:|---:|---|
| [Kidney toxicity (nephrotoxicity)](./kidney/kidney-nephrotoxicity.md) | delivered | 65 | 111 | 7 | 16 — WS, N3, M1, N2, K1, REV, A1–A10 |
| [Hepatotoxicity](./hepatotoxicity.md) | sources-acquired-not-extracted | 0 | 0 | 5 | none — N1 is registered in `sources/SOURCES.md` but yields 0 rows |
| [Immunotoxicity / immunostimulation](./immunotoxicity.md) | sources-acquired-not-extracted | 0 | 0 | 1 | none |
| [Thrombocytopenia](./thrombocytopenia.md) | background-only | 0 | 0 | 0 | none |
| [Complement activation](./complement-activation.md) | background-only | 0 | 0 | 0 | none |
| [Coagulopathy](./coagulopathy.md) | background-only | 0 | 0 | 0 | none |
| [Chronic neurotoxicity](./chronic-neurotoxicity/chronic-neurotoxicity.md) | delivered | 13 | 2,335 | 1 | 3 — C1, CT1, L1 |
| [Hydrocephalus](./hydrocephalus/hydrocephalus.md) | delivered | 2 | 12 | 0 | 2 — C1, CT1 |
| **Total (listed endpoints)** | — | **80** | **2,458** | **14** | **21** |
| [Acute neurotoxicity](./acute-neurotoxicity/acute-neurotoxicity.md) — *not on the brief's list* | delivered | 1,832 | 2,047 | 3 | 2 — H1, K1 |

`sources/` holds 18 PDFs in total: the 13 endpoint-dedicated files counted above, 4
cross-cutting reference files, and 1 off-topic file in `sources/_unrelated/`.

Row counts for the kidney endpoint, by `source_id`: WS 36, N3 21, M1 11, N2 10,
K1 9, A4 5, REV 4, A1 3, A3 3, A8 2, A9 2, A2 1, A5 1, A6 1, A7 1, A10 1. Five of those 16
(N2, N3, M1, K1, REV) correspond to a PDF held locally; the other 11 (WS and A1–A10) have no
local PDF and are allocated to the endpoint by `source_id` alone. Distributions, per-source
oligo counts and the local-PDF mapping are in
[`kidney-nephrotoxicity.md`](./kidney/kidney-nephrotoxicity.md).

## How to read the status values

| Status | Meaning |
|---|---|
| `delivered` | Rows are extracted, curated and present in a `data/` directory. The endpoint has a dataset. |
| `delivered (thin)` | Rows exist and are curated, but too few, or from too few sources, to support a distributional claim. Used where the count would otherwise imply coverage it does not have. |
| `delivered (single row)` | Exactly one curated row. Recorded because it displaces a prior claim of "nothing", not because it is coverage. |
| `sources-acquired-not-extracted` | Primary PDFs are held in `sources/` and per-oligo material inside them has been identified, but no rows have been extracted into `data/`. |
| `background-only` | No dedicated source was acquired. The endpoint appears only inside multi-endpoint reference material held for other reasons. |
| `not-addressed` | No dedicated source, no row, no doc section, no slide, and no scope decision on record. At most an incidental passage inside a volume held for another endpoint. Listed so the allocation is exhaustive against the brief's eight-item list. |

Four endpoints are populated: [kidney](./kidney/kidney-nephrotoxicity.md),
[chronic neurotoxicity](./chronic-neurotoxicity/chronic-neurotoxicity.md),
[hydrocephalus](./hydrocephalus/hydrocephalus.md), and
[acute neurotoxicity](./acute-neurotoxicity/acute-neurotoxicity.md) — the last of which is **not
on the brief's list**. The remaining four dossiers describe source inventories and extraction
backlogs; they are deliberately short, and they are not peers of the kidney file.

**The CNS curation now covers the listed endpoints substantively.** It holds
4,394 measurements: **2,335 chronic neurotoxicity**
(of which 2,329 are human clinical),
**12 hydrocephalus**, and 2,047 acute. That is a change of scale from an
earlier revision, where the two listed endpoints held 7 rows between them, and it came from
ingesting the ClinicalTrials.gov posted adverse-event tables — human data with denominators and
comparator arms.

Acute neurotoxicity — "alterations of neuronal electrical activity" — remains the axis the brief
**deprioritises**. It keeps a folder so the data is filed under its own name rather than discarded
or hidden inside a listed endpoint's folder, but **nothing in it counts toward the brief's
coverage**.

## What this reorganization changed

**Terminology used throughout these dossiers.** The **curated corpus** means the dataset and its
documentation as they stood before this reorganization: [`data/`](kidney/data/), [`sources/`](kidney/sources/),
[`scripts/`](kidney/scripts/), [`METHODOLOGY.md`](kidney/METHODOLOGY.md), [`schema.md`](kidney/schema.md),
[`PADP.md`](kidney/PADP.md) and [`PRESENTATION.md`](kidney/PRESENTATION.md). The **index layer** means what this
pass added: this directory, [`kidney/REVIEW-2026-08.md`](kidney/REVIEW-2026-08.md), and the register section
added to [`../README.md`](../README.md). A statement such as "no file in the curated corpus mentions
this endpoint" is scoped to the former, so it stays true as the index layer grows.

The dossiers are a new index layer. Nothing else moved:
[`data/`](kidney/data/), [`schema.md`](kidney/schema.md), [`METHODOLOGY.md`](kidney/METHODOLOGY.md),
[`sources/`](kidney/sources/) and [`scripts/`](kidney/scripts/) were not restructured, renamed or
edited, and they remain the source of truth. Where a dossier and a data file disagree, the
data file wins.

Three facts about **the kidney data model** that this index makes visible rather than changes. They are scoped to [`kidney/data/`](kidney/data/); the CNS endpoints have their own schema, its own graded column and its own controlled vocabularies:

- **All 111 measurement rows are kidney.** `is_kidney_specific` is `TRUE` on 111 of 111
  rows; no `FALSE` row exists. The column carries no information in the current dataset.
- **`nephrotox_grade` is single-endpoint by construction.** Its distribution is 0 → 27,
  1 → 30, 2 → 39, 3 → 15, and its 0–3 rubric in [`schema.md`](kidney/schema.md) is written
  entirely in renal terms. It is not transferable: a second endpoint requires its own graded
  column and its own written rubric, not a reuse of this one.
- **`data/oligotox_kidney_merged.csv` (111 × 39) is generated,** by
  [`scripts/build_merged.py`](kidney/scripts/build_merged.py), as a denormalized join of the two
  CSVs above. It is not a third dataset and is not curated independently.

Because both the endpoint flag and the grade column are kidney-shaped, a seven-endpoint
register cannot be produced by re-slicing the kidney tables. That is why five of the eight
dossiers still report zero rows rather than a subset — and why the CNS work is a **second
dataset alongside** the kidney one, with its own schema, its own `cns_tox_grade` column and its
own written rubric ([`_shared/cns/docs/SCHEMA.md`](_shared/cns/docs/SCHEMA.md)), exactly as the
earlier revisions of both CNS dossiers said it would have to be.

## Related files

- [`cross-cutting.md`](./cross-cutting.md) — artifacts that serve no single endpoint: the
  Challenge brief, the general-toxicology and multi-endpoint reference PDFs, the source
  registry, the root documents, and the endpoint-neutral scripts.
- [`../README.md`](../README.md) — project front door, scope and record counter.
- [`kidney/METHODOLOGY.md`](kidney/METHODOLOGY.md) — the Phase 2 methodology deliverable, including
  the no-fabrication policy these dossiers are written under.
- [`kidney/schema.md`](kidney/schema.md) — data dictionary, controlled vocabularies, grading rubric.
- [`kidney/SOURCES.md`](kidney/SOURCES.md) — the source registry and `source_id`
  definitions.
- [`kidney/PADP.md`](kidney/PADP.md) — Public Access & Dissemination Plan.
- [`kidney/PRESENTATION.md`](kidney/PRESENTATION.md) — the deck, which covers the kidney endpoint
  only.
