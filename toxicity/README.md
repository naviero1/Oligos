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
([`sources/reference/OligoTox_challenge_brief.pdf`](../sources/reference/OligoTox_challenge_brief.pdf),
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

Counts recomputed from [`data/oligos.csv`](../data/oligos.csv) (65 rows × 17 columns) and
[`data/measurements.csv`](../data/measurements.csv) (111 rows × 23 columns). "Source PDFs
held" counts only PDFs filed to that endpoint alone; the 4 multi-endpoint reference PDFs are
excluded here and listed in the cross-cutting file instead.

**Two endpoints are now delivered, by two independent datasets that share no table.** The
kidney rows live in `../data/`; the hydrocephalus rows live in
[`./hydrocephalus/data/`](./hydrocephalus/README.md), with their own schema, their own graded
column and their own source registry. The last two columns of the table below are therefore
about `../data/measurements.csv` only, and read `n/a` for hydrocephalus — its sources reach
its own registry, not that file. Nothing about the kidney dataset changed when hydrocephalus
was added, which is the point of keeping them apart.

| Endpoint | Status | Oligos | Measurement rows | Source PDFs held | `source_id`s reaching `measurements.csv` |
|---|---|---:|---:|---:|---|
| [Kidney toxicity (nephrotoxicity)](./kidney-nephrotoxicity.md) | delivered | 65 | 111 | 7 | 16 — WS, N3, M1, N2, K1, REV, A1–A10 |
| [Hepatotoxicity](./hepatotoxicity.md) | sources-acquired-not-extracted | 0 | 0 | 5 | none — N1 is registered in `sources/SOURCES.md` but yields 0 rows |
| [Immunotoxicity / immunostimulation](./immunotoxicity.md) | sources-acquired-not-extracted | 0 | 0 | 1 | none |
| [Thrombocytopenia](./thrombocytopenia.md) | background-only | 0 | 0 | 0 | none |
| [Complement activation](./complement-activation.md) | background-only | 0 | 0 | 0 | none |
| [Coagulopathy](./coagulopathy.md) | background-only | 0 | 0 | 0 | none |
| [Chronic neurotoxicity](./chronic-neurotoxicity.md) | not-addressed | 0 | 0 | 0 | none |
| [Hydrocephalus](./hydrocephalus.md) | **delivered — separate dataset** | 34 | 904 | 0 | n/a — 52 sources in its own registry, [`hydrocephalus/data/sources.csv`](./hydrocephalus/data/sources.csv) |
| **Total** | — | **99** | **1,015** | **13** | **16** into `../data/measurements.csv`; 52 into the hydrocephalus registry |

`sources/` holds 18 PDFs in total: the 13 endpoint-dedicated files counted above, 4
cross-cutting reference files, and 1 off-topic file in `sources/_unrelated/`.

Row counts for the single populated endpoint, by `source_id`: WS 36, N3 21, M1 11, N2 10,
K1 9, A4 5, REV 4, A1 3, A3 3, A8 2, A9 2, A2 1, A5 1, A6 1, A7 1, A10 1. Five of those 16
(N2, N3, M1, K1, REV) correspond to a PDF held locally; the other 11 (WS and A1–A10) have no
local PDF and are allocated to the endpoint by `source_id` alone. Distributions, per-source
oligo counts and the local-PDF mapping are in
[`kidney-nephrotoxicity.md`](./kidney-nephrotoxicity.md).

## How to read the status values

| Status | Meaning |
|---|---|
| `delivered` | Rows are extracted, curated and present in `data/`. The endpoint has a dataset. |
| `sources-acquired-not-extracted` | Primary PDFs are held in `sources/` and per-oligo material inside them has been identified, but no rows have been extracted into `data/`. |
| `background-only` | No dedicated source was acquired. The endpoint appears only inside multi-endpoint reference material held for other reasons. |
| `not-addressed` | No dedicated source, no row, no doc section, no slide, and no scope decision on record. At most an incidental passage inside a volume held for another endpoint. Listed so the allocation is exhaustive against the brief's eight-item list. |

Two dossiers now describe datasets — kidney and hydrocephalus — and they are peers. The other
six describe source inventories and extraction backlogs; they are deliberately short, and they
are not peers of the two populated files.

`delivered — separate dataset` means the endpoint has its own tables, schema, grading rubric
and source registry in a subdirectory of this one, and contributes no row to `../data/`. It is
the shape any further endpoint should take, for the reason given in the next section.

## What this reorganization changed

**Terminology used throughout these dossiers.** The **curated corpus** means the dataset and its
documentation as they stood before this reorganization: [`data/`](../data/), [`sources/`](../sources/),
[`scripts/`](../scripts/), [`METHODOLOGY.md`](../METHODOLOGY.md), [`schema.md`](../schema.md),
[`PADP.md`](../PADP.md) and [`PRESENTATION.md`](../PRESENTATION.md). The **index layer** means what this
pass added: this directory, [`../REVIEW-2026-08.md`](../REVIEW-2026-08.md), and the register section
added to [`../README.md`](../README.md). A statement such as "no file in the curated corpus mentions
this endpoint" is scoped to the former, so it stays true as the index layer grows.

The dossiers are a new index layer. Nothing else moved:
[`data/`](../data/), [`schema.md`](../schema.md), [`METHODOLOGY.md`](../METHODOLOGY.md),
[`sources/`](../sources/) and [`scripts/`](../scripts/) were not restructured, renamed or
edited, and they remain the source of truth. Where a dossier and a data file disagree, the
data file wins.

Three facts about the data model that this index makes visible rather than changes:

- **All 111 measurement rows are kidney.** `is_kidney_specific` is `TRUE` on 111 of 111
  rows; no `FALSE` row exists. The column carries no information in the current dataset.
- **`nephrotox_grade` is single-endpoint by construction.** Its distribution is 0 → 27,
  1 → 30, 2 → 39, 3 → 15, and its 0–3 rubric in [`schema.md`](../schema.md) is written
  entirely in renal terms. It is not transferable: a second endpoint requires its own graded
  column and its own written rubric, not a reuse of this one.
- **`data/oligotox_kidney_merged.csv` (111 × 39) is generated,** by
  [`scripts/build_merged.py`](../scripts/build_merged.py), as a denormalized join of the two
  CSVs above. It is not a third dataset and is not curated independently.

Because both the endpoint flag and the grade column are kidney-shaped, a seven-endpoint
register cannot be produced by re-slicing the existing tables. That is why six of the eight
dossiers still report zero rows rather than a subset — and why the seventh,
[hydrocephalus](./hydrocephalus.md), was built as a separate dataset in
[`./hydrocephalus/`](./hydrocephalus/README.md) rather than as new rows here. It declares its
own `hydroceph_grade` with its own rubric, its own CNS vocabularies, and its own provenance
registry, and it changed no file in `../data/`, `../schema.md`, `../sources/` or
`../scripts/`.

## Related files

- [`cross-cutting.md`](./cross-cutting.md) — artifacts that serve no single endpoint: the
  Challenge brief, the general-toxicology and multi-endpoint reference PDFs, the source
  registry, the root documents, and the endpoint-neutral scripts.
- [`../README.md`](../README.md) — project front door, scope and record counter.
- [`../METHODOLOGY.md`](../METHODOLOGY.md) — the Phase 2 methodology deliverable, including
  the no-fabrication policy these dossiers are written under.
- [`../schema.md`](../schema.md) — data dictionary, controlled vocabularies, grading rubric.
- [`../sources/SOURCES.md`](../sources/SOURCES.md) — the source registry and `source_id`
  definitions.
- [`../PADP.md`](../PADP.md) — Public Access & Dissemination Plan.
- [`../PRESENTATION.md`](../PRESENTATION.md) — the deck, which covers the kidney endpoint
  only.
