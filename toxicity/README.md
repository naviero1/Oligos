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
CNS: [`cns/data/`](cns/data/) (1,839 oligos × 45; 2,065 measurements × 36; plus a 32,569-row
per-position modification table). The CNS rows below count only what is allocated to each
endpoint, **not** the module's totals — see the note under the table. "Source PDFs held" counts
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
| [Chronic neurotoxicity](./chronic-neurotoxicity.md) | delivered (thin) | 5 | 6 | 1 | 1 — L1 |
| [Hydrocephalus](./hydrocephalus.md) | delivered (single row) | 1 | 1 | 0 | 1 — C1 |
| **Total** | — | **71** | **118** | **14** | **18** |

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

Two datasets are described here: [kidney](./kidney/kidney-nephrotoxicity.md), and the CNS module
at [`cns/`](cns/), indexed by [chronic neurotoxicity](./chronic-neurotoxicity.md) and
[hydrocephalus](./hydrocephalus.md). The remaining five dossiers describe source inventories and
extraction backlogs; they are deliberately short, and they are not peers of the kidney file.

**The CNS module's totals do not belong to any endpoint on the brief's list.** It holds 2,065
CNS measurements, of which **6 are chronic neurotoxicity and 1 is hydrocephalus**; 2,047 (99.1%)
sit on the *acute* axis — "alterations of neuronal electrical activity" — which the brief
deprioritises and which therefore still has no dossier here. Quoting the module's size as
coverage of a listed endpoint would overstate it by roughly two orders of magnitude. The
allocation is set out in
[`chronic-neurotoxicity.md` §2](./chronic-neurotoxicity.md#2-the-allocation-problem--read-before-quoting-the-modules-size).

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

Three facts about **the kidney data model** that this index makes visible rather than changes. They are scoped to [`kidney/data/`](kidney/data/); the CNS module has its own schema, its own graded column and its own controlled vocabularies:

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
own written rubric ([`cns/docs/SCHEMA.md`](cns/docs/SCHEMA.md)), exactly as the earlier revisions
of both CNS dossiers said it would have to be.

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
