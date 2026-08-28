# OligoTox — Curated Per-Measurement Oligonucleotide Toxicity Datasets

A curated, openly-releasable, **per-measurement** resource of oligonucleotide toxicity
observations, built for the **NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data
Challenge, Phase 2** (Data Generation Phase). It now spans **four datasets — 5,095
measurements — across four of the Challenge's eight named endpoints**, with the
remaining four endpoints documented rather than populated.

The deliverable is a **dataset**, not a model: openly-releasable, well-documented and
reproducible, which is what NCATS scores. Every row is traceable to a source and a locus
within it; missing values are the literal string `TBD` and are never guessed or imputed.

---

## The Challenge's toxicities of interest

Quoted verbatim from the Challenge brief
([`_shared/sources/OligoTox_challenge_brief.pdf`](_shared/sources/OligoTox_challenge_brief.pdf),
page 1):

> Toxicities of interest include:
> Hepatotoxicity, kidney toxicity, thrombocytopenia, complement activation,
> coagulopathy, immunotoxicity, chronic neurotoxicity, and hydrocephalus.

The same page deprioritizes one adjacent topic explicitly:

> Given the availability of large data sets focused on acute neurotoxicity, specifically
> alterations of neuronal electrical activity, submissions focused on this topic will be
> considered a lower priority than other toxicities of interest.

Acute neurotoxicity is therefore **not** an endpoint folder here. Acute rows exist inside
`chronic-neurotoxicity/` — they are the matched in-vitro arm of in-vivo panels on the same
molecules — but every row declares its bucket through `endpoint_domain` and
`challenge_priority`, so the deprioritized class can be dropped with one predicate.

---

## Toxicity register

One row per named endpoint, in the brief's own order. Counts are recomputed from the CSVs
in each folder.

| Endpoint | Status | Oligos | Measurements | Source PDFs held |
|---|---|---:|---:|---|
| [hepatotoxicity/](hepatotoxicity/) | sources-acquired-not-extracted | 0 | 0 | 5, in `hepatotoxicity/sources/` |
| [kidney-toxicity/](kidney-toxicity/) | delivered | 71 | 769 | 7, in `kidney-toxicity/sources/` |
| [thrombocytopenia/](thrombocytopenia/) | delivered | 252 | 1,786 | 0 archived; sources were retrieved online and registered in [`thrombocytopenia/SOURCES.md`](thrombocytopenia/SOURCES.md) |
| [complement-activation/](complement-activation/) | background-only | 0 | 0 | 0 dedicated |
| [coagulopathy/](coagulopathy/) | background-only | 0 | 0 | 0 dedicated |
| [immunotoxicity/](immunotoxicity/) | sources-acquired-not-extracted | 0 | 0 | 1, in `immunotoxicity/sources/` |
| [chronic-neurotoxicity/](chronic-neurotoxicity/) | delivered | 573 | 2,393 | 0 in-folder; 23 in [`_shared/sources/cns/`](_shared/sources/cns/) |
| [hydrocephalus/](hydrocephalus/) | delivered | 13 | 147 | 0 in-folder; the same `_shared/sources/cns/` corpus |
| **Total** | **4 delivered** | **909** | **5,095** | **13 in endpoint folders, 23 in `_shared/sources/cns/`** |

Reading the totals correctly:

- **The PDF column counts source documents only.** 42 PDFs sit on disk; the 41 counted here
  are 13 in endpoint folders, 23 under `_shared/sources/cns/`, 4 multi-endpoint reference
  works in `_shared/sources/`, and 1 in `_unallocated/`. The 42nd is the built findings deck
  at `kidney-toxicity/presentation/OligoTox-Kidney.pdf`, which is an output, not a source.
- **909 is a sum across four separate oligo tables, not 909 distinct molecules.** An oligo
  is a compound identity, not a toxicity observation, so the same molecule may legitimately
  appear in more than one endpoint's `oligos.csv`. The 5,095 measurement rows *are* disjoint.
- Four further PDFs in [`_shared/sources/`](_shared/sources/) serve several endpoints at
  once and are counted under none; one off-topic PDF sits in
  [`_unallocated/`](_unallocated/).
- `background-only` means no dedicated source was acquired and nothing was extracted; the
  endpoint's only footprint is passages inside multi-endpoint reference material held for
  other reasons. Each such folder's README records exactly what and where.

### Composition of the four delivered datasets

| | kidney-toxicity | thrombocytopenia | chronic-neurotoxicity | hydrocephalus |
|---|---|---|---|---|
| Measurements × columns | 769 × 23 | 1,786 × 23 | 2,393 × 26 | 147 × 26 |
| Oligos × columns | 71 × 21 | 252 × 17 | 573 × 17 | 13 × 17 |
| Oligos with a `sequence_5to3` other than `TBD` | 66 / 71 | 193 / 252 | 458 / 573 | 6 / 13 |
| — of which an actual sequence string (excluding `NA`) | 64 / 71 | 192 / 252 | 458 / 573 | 6 / 13 |
| Distinct `target_gene` values (raw) | 35 | 62 | 43 | 9 |
| — excluding the `TBD` / `NA` placeholders | 34 | 60 | 41 | 8 |
| Distinct `source_id`s | 17 | 43 | 94 | 44 |
| Graded column | `nephrotox_grade` | `thrombocytopenia_grade` | `neurotox_grade` | `neurotox_grade` |
| Grade 0/1/2/3 | 372 / 140 / 151 / 106 | 756 / 466 / 372 / 192 | 1,183 / 577 / 513 / 120 | 63 / 14 / 54 / 16 |
| Study type | in_vitro 677 · animal_invivo 53 · clinical 39 | clinical 852 · in_vitro 482 · animal_invivo 424 · ex_vivo 28 | animal_invivo 1,684 · clinical 414 · in_vitro 295 | clinical 133 · animal_invivo 12 · in_vitro 2 |
| Dominant species | human 635 · rat 110 | human 1,291 · mouse 175 · monkey 174 | mouse 1,011 · rat 612 · human 530 | human 133 · rat 10 |
| Dominant delivery | gymnotic_free_uptake 677 · systemic_dose 87 | systemic_dose 1,264 · direct_addition 496 | intrathecal 1,019 · intracerebroventricular 1,008 | intrathecal 115 |

Each dataset documents itself in full — grading rubric, extraction method, verification
status, limitations — in its own folder:
[`thrombocytopenia/README.md`](thrombocytopenia/README.md),
[`chronic-neurotoxicity/README.md`](chronic-neurotoxicity/README.md),
[`hydrocephalus/README.md`](hydrocephalus/README.md),
[`kidney-toxicity/METHODOLOGY.md`](kidney-toxicity/METHODOLOGY.md).
`hydrocephalus/` carries its own README but inherits the CNS methodology and schema from
`chronic-neurotoxicity/`; it does not duplicate them.

---

## Repository layout

**The rule is one folder per toxicity.** Each endpoint's data, sources, scripts and
documentation live under that endpoint's own root-level folder, and **no folder mixes two
endpoints' measurements**. A reader who wants one endpoint needs exactly one directory.

| Path | Contents |
|---|---|
| [`kidney-toxicity/`](kidney-toxicity/) | `data/` `sources/` `scripts/` `presentation/` `reconcile/` · `METHODOLOGY.md` `schema.md` `SOURCES.md` |
| [`thrombocytopenia/`](thrombocytopenia/) | `data/` `scripts/` · `README.md` `METHODOLOGY.md` `schema.md` `SOURCES.md` |
| [`chronic-neurotoxicity/`](chronic-neurotoxicity/) | `data/` `scripts/` `notes/` · `README.md` `README-CNS.md` `METHODOLOGY-CNS.md` `schema-cns.md` `SOURCES-CNS.md` `VERIFICATION-CNS.md` `NEXT-STEPS-CNS.md` |
| [`hydrocephalus/`](hydrocephalus/) | `data/` `scripts/` · `README.md` (schema and methodology inherited from `chronic-neurotoxicity/`) |
| [`hepatotoxicity/`](hepatotoxicity/) | `sources/` (5 PDFs) · `README.md` |
| [`immunotoxicity/`](immunotoxicity/) | `sources/` (1 PDF) · `README.md` |
| [`complement-activation/`](complement-activation/) | `README.md` |
| [`coagulopathy/`](coagulopathy/) | `README.md` |
| [`_shared/`](_shared/) | Material serving **no single endpoint**: `sources/` (4 multi-endpoint PDFs, plus `cns/` with the retrieved CNS corpus), `scripts/`, `README.md` |
| [`_unallocated/`](_unallocated/) | Material belonging to **no endpoint at all** — currently one off-topic PDF, kept visible rather than deleted or misfiled |

`_shared/` exists because filing a multi-endpoint source under one endpoint would either
duplicate it or hide it from the endpoints it also serves. `_unallocated/` exists so that
"nothing here needs this" is a recorded state rather than an inference from absence.

Every delivered dataset uses the same two-table design — `data/oligos.csv` (one row per
unique oligo, identity plus design predictors) joined on `oligo_id` to
`data/measurements.csv` (one row per oligo × model × delivery × dose × readout) — with a
denormalized analysis view generated alongside them. The two normalized tables are always
the source of truth; the merged view is regenerated by script and never hand-edited.

---

## How this repository came together

Four Claude Code sessions produced work on **separate branches that were never merged into
each other**. This pass consolidated them into the folder-per-toxicity structure above:

| Branch | Became | Contributed |
|---|---|---|
| `claude/oligo2-sequences-and-patent-mining` | `kidney-toxicity/` | 769 measurements, 37 commits |
| `claude/oligo-challenge-data-4um5mi` | `thrombocytopenia/` | 1,786 measurements, 63 commits |
| `claude/oligo-cns-toxicity-dataset-tijib6` | `chronic-neurotoxicity/` + `hydrocephalus/` | 2,540 measurements, 56 commits |
| `claude/amazing-galileo-rwiv95` (default) | `kidney-toxicity/reconcile/`, `REVIEW-2026-08.md` | the superseded 111-row kidney lineage and the August 2026 review |

**The two kidney lineages.** The default branch carried 111 kidney measurements; the
`oligo2` branch carried 769. The 769-row set is a verified **strict superset**: all 111
`measurement_id`s are present plus 658 more, and its `oligos.csv` adds four columns
(`sequence_sense_5to3`, `sequence_source`, `sequence_redistribution`,
`purity_characterization`). Exactly 21 shared rows differ, all `source_id = N3`, on species,
system model, dose and exposure duration. The 769-row values are the correct ones: the
*Measuring In Vivo Nephrotoxicity* section of US 11,105,794 binds its Table 1 to "Purpose
bred Wistar Han Crl:WI(Han) male rats" dosed 40 mg/kg on days 1 and 8 with necropsy on day
15 — rat, not the mouse/7-day/`TBD` tuple the 111-row lineage recorded. Shipping the 769-row
set therefore resolves the headline blocker (B1) of `REVIEW-2026-08.md`.

**The CNS partition.** The CNS curation was one corpus of 2,540 rows serving two named
endpoints. It was split by its own `challenge_priority` column: the 147 `high_hydrocephalus`
rows to `hydrocephalus/`, the remaining 2,393 to `chronic-neurotoxicity/`. The partition is
disjoint and exhaustive (147 + 2,393 = 2,540) and is reproduced by
[`_shared/scripts/split_cns_by_endpoint.py`](_shared/scripts/split_cns_by_endpoint.py). Each
side's `oligos.csv` is filtered to the oligos its own measurements reference, so each folder
is a self-contained two-table dataset.

---

## Open reconciliation work

Consolidation moved files into the right folders. It did not harmonize what is inside them.

1. **Two kidney documentation lineages remain unreconciled.** The superseded 111-row lineage
   is preserved at [`kidney-toxicity/reconcile/`](kidney-toxicity/reconcile/)
   (`data-111row-lineage/`, `METHODOLOGY-111row-lineage.md`, `schema-111row-lineage.md`)
   **because its documentation contains later analysis — the clinical-validation work — that
   the `oligo2` documentation does not.** The data question is settled (ship the 769-row set);
   the documentation question is not. Merging the clinical-validation material into
   [`kidney-toxicity/METHODOLOGY.md`](kidney-toxicity/METHODOLOGY.md) and
   [`kidney-toxicity/schema.md`](kidney-toxicity/schema.md), then retiring the lineage copies,
   is open work.
2. **There is no unified toxicity rubric.** Each dataset carries its own schema file and its
   own graded column — `nephrotox_grade` ([`kidney-toxicity/schema.md`](kidney-toxicity/schema.md)),
   thrombocytopenia grading ([`thrombocytopenia/schema.md`](thrombocytopenia/schema.md)),
   `neurotox_grade` ([`chronic-neurotoxicity/schema-cns.md`](chronic-neurotoxicity/schema-cns.md),
   which also governs `hydrocephalus/`). All are 0–3, but they are three independently written
   rubrics anchored to three different clinical literatures. **A grade 2 does not mean the same
   thing across endpoints, and the tables must not be unioned on grade.**
3. **The column layouts have diverged.** Measurements are 23 columns for kidney and
   thrombocytopenia and 26 for the CNS-derived pair; oligos are 21 columns for kidney and 17
   for the other three. A cross-endpoint union needs an explicit mapping that does not yet exist.
4. **Verification coverage is uneven.** Thrombocytopenia and CNS report per-block adversarial
   verification in their own documentation; the kidney set does not carry an equivalent pass.

---

## Governance, licensing and review

- **[`PADP.md`](PADP.md)** — Public Access & Dissemination Plan: licensing, archival DOI
  deposit, and the U.S. Government continuity provisions the Challenge requires. Written for
  the kidney dataset and now covering all four; its title still says *OligoTox-Kidney*.
- **[`LICENSE`](LICENSE)** — CC BY 4.0 for the curated tables and documentation. Per-row
  redistribution rights are tracked separately in each dataset's `redistribution` column,
  because source licences differ row by row; filter on it before reusing raw values.
- **[`REVIEW-2026-08.md`](REVIEW-2026-08.md)** — strict adversarial review, August 2026.
  **Scope caveat:** it was written against the 111-row kidney lineage only, before the other
  three branches were discovered, so its kidney findings still apply except B1 (resolved
  above) and its claims that thrombocytopenia, chronic neurotoxicity and hydrocephalus have
  zero rows are wrong — they describe the single branch it could see.
- **[`_shared/README.md`](_shared/README.md)** — what each cross-cutting source is and which
  endpoints it serves.
