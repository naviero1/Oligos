# Phase 2 compliance — hydrocephalus endpoint

Maps this endpoint's work to the Challenge's Phase 2 requirements and to the
team's own division of labour, so that what is done, what is missing and who owns
each missing piece can be read in one place.

**Scope:** hydrocephalus only. The kidney and CNS endpoints are separate
deliverables and nothing here touches them.

**Sources of the requirements.** The requirement text is quoted from
`Phase 2 description.docx`; ownership is from `Phase Roles Assignment Plan.docx`;
the schedule is from `Phase 2 Work-Plan.xlsx` — all three in the team's shared
Drive folder `OligoTox Challenge / Phase 2`.

Counts below are transcribed from `qc/stats.json` on the date of the last commit
and will drift; [`README.md`](README.md) is authoritative.

---

## The four required submission parts

| # | Required part | Owner | Status for this endpoint |
|---|---|---|---|
| 1 | **Narrative document**, single PDF ≤ 12 pages | Gustavo | **Not started.** The material for five of its six required sections exists in `README.md` and `METHODOLOGY.md` and is listed below, but no narrative PDF has been written. |
| 2 | **Methodology document**, single PDF ≤ 5 pages, *"including the methods used to purify and characterize oligo identity"* | German | **Draft material exists, not in deliverable form.** [`METHODOLOGY.md`](METHODOLOGY.md) covers curation methods, source-study methods, QC and 9 open items, and §"Purification and identity characterisation" answers the purity clause with evidence. It is Markdown and longer than 5 pages. |
| 3 | **Dataset**: data dictionary + schema, raw data in Excel or similar, *"sequences of all oligos tested, as well as the location of all chemical modifications in each oligo, data on the purity and characterization of each, and any additional metadata"*, under an open licence | Oscar | **Substantially met; two gaps.** Detailed below. |
| 4 | **PADP**, ≤ 5 pages | Gustavo | **Not started for this endpoint.** A kidney-endpoint PADP exists at the repository root; it is not this endpoint's and has not been adapted. |
| — | *Optional*: code documentation, interactive notebooks, tutorials | Oscar | **Code documented, notebooks not started.** Every build step is a documented script; there is no tutorial notebook. |

---

## Part 3 — the dataset, requirement by requirement

This is the part owned by this workstream, so it is broken out in full.

| Requirement (quoted) | Status | Evidence |
|---|---|---|
| "a data dictionary and schema documenting all metadata" | **Met** | [`scripts/data_dictionary.py`](scripts/data_dictionary.py) is the authoritative definition, rendered as the workbook's `data_dictionary` sheet. The QC suite asserts in **both directions** that every column has an entry and every entry is a real column. [`SCHEMA.md`](SCHEMA.md) carries the conceptual schema: tiers, rubric, missing-value convention. |
| "access to the raw data … by including a data file in Excel (or similar format)" | **Met** | `OligoTox-Hydrocephalus_Dataset.xlsx`, 9 sheets, same layout as the sibling CNS release. CSVs in `data/` are the canonical form. |
| "the sequences of all oligos tested" | **Partly met — gap** | **10 of 50** compounds carry a published sequence. Recovered from WHO INN Recommended lists by deterministic parse, validated against each label's molecular formula. Missing for the double-stranded siRNAs, the morpholinos, and 15 compounds that reach the dataset only through the trial registry. See `METHODOLOGY.md` **OI-02**. |
| "the location of all chemical modifications in each oligo" | **Partly met — gap** | [`data/modifications.csv`](data/modifications.csv): **202 rows, one per nucleotide position, over 10 compounds**, giving sugar, base, 5-methylation and phosphorothioate-vs-phosphodiester at every position. Same 40 compounds missing as above. |
| "data on the purity and characterization of each" | **Met, as a negative finding** | `purity_pct` is `NOT_REPORTED` for all 50, from evidence: a full-text sweep of all 16 committed US labels finds no drug-substance purity, purification or identity statement in any of them. Recorded with the sweep as its basis, not left blank. The sibling CNS release reports the same for all 1,839 of its compounds. |
| "any additional metadata" | **Met** | 53 measurement columns, 32 oligo columns, 12 modification columns, 20 source columns — including provenance, ascertainment, attribution and rights on every row. |
| "terms for data access and data use … allowing for open and public access, such as through a creative commons license" | **Partly met — gap** | Rights are tracked **per row** (`redistribution`): 1,290 public domain, 8 CC BY, 3 CC BY-NC, 15 summary-statistic-only, 8 `verify`. But **no LICENSE file exists** in the repository, so the dataset's own licence has not been granted. This blocks the PADP, whose continuity argument rests on an irrevocable grant already being in place. |

### Datasets "of particular interest" to the sponsor

> "Datasets based on in vitro human systems or able to extrapolate data between in
> vitro human systems and animal data are of particular interest."

**This is the release's weakest point and it is structural.** The dataset is
**1,319 human rows, 5 animal rows and 0 in vitro rows**. It cannot currently
support in vitro-to-animal extrapolation, because it contains neither an in vitro
arm nor a substantial animal arm.

What it does support, and should be argued on instead:

- **Human clinical evidence at scale** — 757 trial rows from 155 registered
  trials, with denominators and comparator arms.
- **A route contrast** — intrathecal against systemically dosed oligonucleotides,
  so the delivery hypothesis is testable rather than assumed.
- **Confounder separation** — disease background rate, delivery-procedure
  complication and drug effect on separate `tox_axis` values.

Closing the in vitro gap is a **German** item under the roles plan ("Define the in
vitro human systems and ensure the dataset can extrapolate between human and
animal models"). A hunt for human in vitro choroid-plexus, ependymal and
blood-CSF-barrier oligonucleotide studies is in progress; if that literature does
not exist, the honest submission position is to say so and argue the human
clinical scale instead.

---

## Material already written for the narrative document

The narrative is Gustavo's to write, but five of its six required sections have
their content assembled here. Listed so it can be lifted rather than re-derived.

| Required narrative section | Where the material is |
|---|---|
| "executive summary of the dataset(s) generated, and **positive/negative controls** included" | `README.md` §"Dataset at a glance" and §"What makes this endpoint hard". Controls: 735 tier-A explicit measured negatives; placebo and sham comparator arms; `disease_background_rate` rows carrying no compound; `delivery_procedure_complication` rows; one designed scrambled non-targeting siRNA; two protective-direction rows. |
| "summary of the main findings and conclusions" | `README.md` §"What the data shows" — eight findings, each traceable to rows and loci. |
| "how data were produced … experimental design, data acquisition and **computational processing**" | `METHODOLOGY.md` §3 (five retrieval modalities) and §4 (seven extraction components, three of them deterministic parsers). Every payload committed under `sources/raw/`. |
| "how indicators and predictor variables … were measured, their **distribution**, and the distribution of predictor variables amongst tested oligos" | `README.md` generated block: 12 distribution tables, rendered from `qc/stats.json`. Predictor distributions across compounds are in `data/oligos.csv`. |
| "how the results address a **gap** in the publicly available data" | `../hydrocephalus.md` — the endpoint was `not-addressed` in this repository and, per the team's Phase 1 analysis, is unaddressed by every Phase 1 winning team. |
| "how the data could be used to develop a **predictive model**" | `METHODOLOGY.md` §8 states what the dataset supports and what it does not, plainly. **This is the section with the least material**, and it is the one the ML step is meant to produce. |

---

## Against the work plan

The plan's October block for this endpoint is *Data prep → Finish ML → Write up
report*; the four documents are the November block.

| Step | Status |
|---|---|
| Data prep | **Done**, and extended past the original scope: 1,324 rows, 50 compounds, 189 sources, 155 trials, 44 QC checks. |
| **Finish ML** | **Not started.** This is the next step in the plan's own order, and it is what the narrative's predictive-model section needs. |
| Write up report | Not started. |

---

## Gap list, in priority order

1. **No LICENSE file.** Cheapest to fix, blocks the PADP, and the repository has
   intended CC-BY since the kidney release without ever granting it. *(Decision
   needed — it is a rights grant, not a curation choice.)*
2. **No ML analysis.** Next in the work plan's own order; supplies the narrative's
   weakest section.
3. **No in vitro rows**, against a stated sponsor interest. Hunt in progress;
   may end in a documented absence.
4. **Sequences and modification maps for 40 of 50 compounds** (OI-02): duplex
   siRNAs, morpholinos, and the registry-only compounds.
5. **Animal arm is 5 rows** (OI-03), so human-to-animal extrapolation is not
   supported either.
6. **No narrative, methodology or PADP PDF** for this endpoint — Gustavo and
   German's deliverables, listed here for completeness rather than as this
   workstream's backlog.
7. **100 verified sources retrieved but unextracted**, in
   [`notes/source_backlog.md`](notes/source_backlog.md).
