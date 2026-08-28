# Cross-cutting artifacts

Artifacts that serve **no single endpoint**: source material spanning several of the eight
Challenge endpoints, and endpoint-neutral tooling. Filing any of it under one endpoint would
either duplicate it or hide it from the endpoints it also serves. One artifact belongs to no
endpoint at all (§3).

Four endpoints carry data — [kidney-toxicity](../kidney-toxicity/README.md) (769 measurements),
[thrombocytopenia](../thrombocytopenia/README.md) (1,786),
[chronic-neurotoxicity](../chronic-neurotoxicity/README.md) (2,393) and
[hydrocephalus](../hydrocephalus/README.md) (147); 5,095 in total. They were curated
independently on four branches that were never merged until this pass, so each arrived with its
own schema, its own grade column and its own methodology. Nothing in this folder is a shared
rubric, and no shared rubric exists — see §4.

Endpoint dossiers: [kidney-nephrotoxicity](../kidney-toxicity/README.md) ·
[hepatotoxicity](../hepatotoxicity/README.md) · [complement-activation](../complement-activation/README.md) ·
[coagulopathy](../coagulopathy/README.md) · [thrombocytopenia](../thrombocytopenia/README.md) ·
[immunotoxicity](../immunotoxicity/README.md) · [chronic-neurotoxicity](../chronic-neurotoxicity/README.md) ·
[hydrocephalus](../hydrocephalus/README.md)

## 1. Cross-cutting source material

[`sources/`](sources/) holds four multi-endpoint PDFs (below), the legacy kidney source registry
(§1.5), and [`sources/cns/`](sources/cns/), the retrieved corpus serving both CNS endpoints (§1.6).

| File | Size | Endpoints served | Role |
|---|---|---|---|
| [`sources/OligoTox_challenge_brief.pdf`](sources/OligoTox_challenge_brief.pdf) | 6 pages | all eight (scope authority) | Defines the endpoint list this register is keyed to. **Cite pp.1–3a only** — §1.1. |
| [`sources/CasarettDoull_Toxicology_textbook.pdf`](sources/CasarettDoull_Toxicology_textbook.pdf) | 1,473 pages | all (background only) | General toxicology definitions. No per-oligo data — §1.2. |
| [`sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf`](sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf) | 12 pages | kidney, hepatotox, thrombocytopenia, complement | Multi-endpoint ASO safety review; dedicated thrombocytopenia section — §1.3. |
| [`sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) | 416 pages | kidney, complement, coagulopathy, hepatotox, CNS delivery | Multi-chapter volume; four Part V chapters serve four endpoints — §1.4. |

All four are registered in [`sources/SOURCES-kidney-legacy.md`](sources/SOURCES-kidney-legacy.md)
at lines 200 (MMB 2434), 208 (Frazier 2015), 210 (Casarett & Doull) and 211 (challenge brief) —
under their old kidney-branch paths, which no longer exist (§1.5).

### 1.1 Challenge brief — provenance defect (pp.3b–6)

Page 1 carries the sentence the whole register depends on, verbatim:

> Toxicities of interest include:
> Hepatotoxicity, kidney toxicity, thrombocytopenia, complement activation,
> coagulopathy, immunotoxicity, chronic neurotoxicity, and hydrocephalus.

Pages 1 to mid-3 read as an authentic NCATS executive summary. From mid-page 3 the
document changes character and **is not usable as evidence**:

- Raw markdown headings survive in the rendered PDF: `### Types of Toxicity` and
  `### Safety Assessment` (p.3), `### Mitigating Toxicity` and `### Key Literature on
  Oligonucleotide Therapeutics and Toxicity` (p.4), `### Accessing the Literature` and
  `### Conclusion:` (p.6).
- The six-item bibliography on pp.4–6 has author fields that are not names — entry 3 is
  attributed to "K. M. S. M. F. B. R. R. R. D. R. K. M. R. R. M. J. M. M. A. A. H.",
  entry 4 to "A. M. A. M. N. H. J. A. G.", entry 6 to "J. M. H. R. L. V. M. P. G. I. A."
- It closes: "If you need further details on a specific study or topic, let me know!"

Cite pp.1–3a as scope authority; cite nothing from pp.3b–6; enter none of its six
bibliography entries into the source registry. Line 211 of
[`sources/SOURCES-kidney-legacy.md`](sources/SOURCES-kidney-legacy.md) registers the file as
"challenge executive summary" with no caveat — annotate that entry.

### 1.2 Casarett & Doull

1,473 pages of general toxicology. Whole-volume keyword profile: immunotox 494,
kidney 650, hepatotox 318, nephrotox 230, complement 143, coagul 143, platelet 176,
thrombocytopeni 52, hydrocephal 6 — but **oligonucleotide 13** and **antisense 7**. It
supplies background organ-toxicity definitions and nothing oligonucleotide-specific; no
row in any endpoint's `measurements.csv` derives from it.

### 1.3 Frazier 2015

Genuinely multi-endpoint over 12 pages: hepatotox 25, kidney 22, platelet 19,
complement 18, thrombocytopeni 16, nephrotox 7, coagul 0. It is structured around three
numbered challenges — #1 (p.4), #2, toxicity unrelated to accumulation (p.5), and a
dedicated section headed **"THROMBOCYTOPENIA (CHALLENGE #3)"** (p.7). Cross-reference it
from kidney, hepatotoxicity, thrombocytopenia and complement-activation; it belongs to
none of them alone.

### 1.4 Methods in Molecular Biology 2434 — misfiling resolved

**Resolved this pass.** The file previously sat in `sources/kidney/`, where its filename
advertised a renal chapter although it is the whole 416-page volume *Antisense RNA Design,
Delivery, and Analysis* (28 chapters, six parts). It now sits at
[`sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf),
under no endpoint, which is where a volume serving four endpoints belongs. The renal chapter is
real, but is one of four in Part V "Safety and Toxicology":

| Chapter | Title (book p.) | Endpoint served |
|---|---|---|
| 24 | Intrathecal Delivery of Therapeutic Oligonucleotides … CNS (p.345) | delivery route; chronic neurotoxicity context |
| 25 | Preclinical Safety Assessment of Therapeutic Oligonucleotides (p.355) | complement activation **and** coagulopathy — §3.1.2 "Effects: Coagulation Time and Complement Activation", PDF p.354 |
| 26 | Preclinical Evaluation of the Renal Toxicity of Oligonucleotide Therapeutics in Mice (p.371) | kidney |
| 27 | Protocol for Isolation and Culture of Mouse Hepatocytes (HCs), Kupffer Cells (KCs), and Liver Sinusoidal Endothelial Cells (LSECs) … (p.385) | hepatotoxicity |

Whole-volume keyword counts confirm the imbalance: antisense 517, oligonucleotide 443,
complement 43, kidney 34, renal 19, hepatotox 5, coagulation 4.

**Still open:** per-chapter indexing. The volume is registered once, as a single kidney-bucket
line, so no registry entry leads a reader to Ch.24, Ch.25 or Ch.27. Until it is indexed per
chapter, this section is the only place those chapters are addressable, and
[`../complement-activation/README.md`](../complement-activation/README.md) and
[`../coagulopathy/README.md`](../coagulopathy/README.md) both point here for that reason.

### 1.5 Legacy kidney source registry

[`sources/SOURCES-kidney-legacy.md`](sources/SOURCES-kidney-legacy.md) is the source registry
written on the original kidney branch. It is kept here, rather than under
[`../kidney-toxicity/`](../kidney-toxicity/), because it registers material now spread across
four folders: the four multi-endpoint PDFs above, the kidney sources at
[`../kidney-toxicity/sources/`](../kidney-toxicity/sources/), the five hepatotoxicity PDFs at
[`../hepatotoxicity/sources/`](../hepatotoxicity/sources/), the Sioud chapter at
[`../immunotoxicity/sources/`](../immunotoxicity/sources/), and the off-topic upload (§3).

Its internal paths — `sources/kidney/`, `sources/hepatotox/`, `sources/reference/`,
`sources/_unrelated/` — describe a directory layout this repository no longer has. Read it as a
provenance record, not as a map. The shipped kidney registry is
[`../kidney-toxicity/SOURCES.md`](../kidney-toxicity/SOURCES.md); the CNS registry is
[`../chronic-neurotoxicity/SOURCES-CNS.md`](../chronic-neurotoxicity/SOURCES-CNS.md); the
thrombocytopenia registry is [`../thrombocytopenia/SOURCES.md`](../thrombocytopenia/SOURCES.md).

### 1.6 CNS retrieved-source corpus (`sources/cns/`)

[`sources/cns/`](sources/cns/) holds the primary material behind both CNS endpoints. It is
cross-cutting for the same reason the CNS dataset was split (§2): the curation was one corpus
serving two named toxicities, so its sources cannot be filed under either one alone. Both
[`../chronic-neurotoxicity/`](../chronic-neurotoxicity/) and
[`../hydrocephalus/`](../hydrocephalus/) draw on it, and neither folder holds sources of its own.

It is a partial corpus, not a complete one. The two CNS datasets cite 119 distinct `source_id`
values between them (94 in chronic-neurotoxicity, 44 in hydrocephalus, overlapping), against 45
files here — most sources were read and cited without a retrieved file being kept. The registry
of record is
[`../chronic-neurotoxicity/SOURCES-CNS.md`](../chronic-neurotoxicity/SOURCES-CNS.md).

46 top-level entries: 45 files plus the `fpo/` subdirectory, which holds 16 further patent HTML
captures — 61 files in all.

| Kind | Count | Notes |
|---|---|---|
| PMC full-text XML (`PMC*.jats.xml`, `PMC*_fulltext.xml`) | 20 | Primary literature |
| WHO INN Recommended List PDFs | 12 | Sequence provenance; two are marked `PARSER-VALIDATION` |
| Article supplements and full texts (Bravo-Hernández 2026, Kuroda 2025, Moazami 2024 ×2, O'Rourke 2026) | 5 | |
| Regulatory reviews (FDA nusinersen, FDA tofersen, EMA Qalsody) | 3 | PDFs |
| US patent PDFs (`US9605263`, `US10138482`, `US10815483`) | 3 | Full text |
| `hagedorn2022_NAT_SupplTableS1_148ASO_ICV_mouse_tolerability.xlsx` | 1 | Source of the 181-row `HAG2022` block |
| `QALSODY_tofersen_label_dailymed.htm` | 1 | Product label capture |
| `fpo/` patent HTML captures | 16 | Free Patents Online renderings, three of which duplicate the PDFs above |

The root register counts this folder as "23" — that is the PDF count only (23 of the 45
top-level files are PDFs).

## 2. Endpoint-neutral tooling

[`scripts/`](scripts/) holds three scripts, none of which belongs to a single endpoint.

| Script | What it does | Documentation status |
|---|---|---|
| [`scripts/paper_search.py`](scripts/paper_search.py) | OpenAlex / Europe PMC / PMC / Crossref search and OA full-text helper | Documented in [`../thrombocytopenia/METHODOLOGY.md`](../thrombocytopenia/METHODOLOGY.md), which names it "shared with the kidney dataset", so the earlier finding that it was documented nowhere no longer holds. No kidney-side document names it. |
| [`scripts/fill_inn_sequences.py`](scripts/fill_inn_sequences.py) | Parses WHO INN chemical nomenclature into oligo sequences | Documented only in the superseded lineage doc [`../kidney-toxicity/reconcile/METHODOLOGY-111row-lineage.md`](../kidney-toxicity/reconcile/METHODOLOGY-111row-lineage.md). The shipped [`../kidney-toxicity/METHODOLOGY.md`](../kidney-toxicity/METHODOLOGY.md) does not mention it. |
| [`scripts/split_cns_by_endpoint.py`](scripts/split_cns_by_endpoint.py) | Reproduces the CNS partition — see below | Documented from [`../README.md`](../README.md) and both CNS folder READMEs. |

**What `split_cns_by_endpoint.py` does.** The CNS curation produced one corpus of 2,540
measurements covering two Challenge endpoints. Every row already declares which one it serves,
through `challenge_priority`, so the script reads the partition off the data rather than
inferring it: rows with `challenge_priority == high_hydrocephalus` are written to
`hydrocephalus/data/`, every other row to `chronic-neurotoxicity/data/`. Each side's
`oligos.csv` is filtered to the oligos its own measurements reference, so each folder becomes a
self-contained two-table dataset; a molecule may legitimately appear in both oligo tables,
because an oligo is a compound identity, not a toxicity observation. The script aborts if any
measurement references an unknown `oligo_id`, and again if the two halves do not sum to the
corpus total. They do: 147 + 2,393 = 2,540, disjoint and exhaustive.

**Not cross-cutting, despite appearances.** `schema.md`, `METHODOLOGY.md` and `build_merged.py`
existed once, on the kidney branch, and were plausibly reusable then. They are not shared now —
each populated endpoint carries its own (§4), and `build_merged.py` writes a kidney-specific
merged table. All three are allocated to [`../kidney-toxicity/`](../kidney-toxicity/).

**Repository-wide documents at the root.** [`../PADP.md`](../PADP.md) (Public Access &
Dissemination Plan) and [`../LICENSE`](../LICENSE) sit above the endpoint folders and are not
listed here, but two notes belong on the record. The earlier finding that PADP asserts a CC-BY
4.0 release while the repository contains no LICENSE file is **resolved** — `LICENSE` now exists
and carries the CC BY 4.0 grant. What remains is scope: PADP's first paragraph still describes
its subject as "the OligoTox-Kidney dataset", and `LICENSE` still names "OligoTox-Kidney
contributors", although the license covers five times as many rows across four endpoints.

## 3. Unallocated

[`../_unallocated/Tipthara2016_urinary_lipidomics_OFFTOPIC.pdf`](../_unallocated/Tipthara2016_urinary_lipidomics_OFFTOPIC.pdf)
— 901,081 bytes, human urinary lipidomics, not oligonucleotide-related. It serves no endpoint on
the Challenge list and supplies no row.
[`sources/SOURCES-kidney-legacy.md`](sources/SOURCES-kidney-legacy.md) lines 212–213 file it
under "off-topic upload, flagged for REMOVAL".

This pass moved it out of the source tree into [`../_unallocated/`](../_unallocated/), which
carries its own [`README.md`](../_unallocated/README.md) recording the judgement. Moving is not
deleting: `git ls-files` still lists the file, so it is still redistributed, still contradicting
`PADP.md` — "Underlying third-party full texts are never redistributed."

**Recommendation: `git rm` it. This has not been done.**

## 4. The reconciliation problem

This section used to ask what would have to change *if* a second endpoint were populated. Three
more endpoints are populated. The question is now retrospective, and the answer is that nothing
was reconciled, because the four datasets were built in parallel on branches that could not see
each other. Each brings a complete, internally coherent schema of its own. Across endpoints
there is no shared rubric, no shared scope flag and no shared column set.

| Endpoint | Schema | Grade column | Scope flag | Flag distribution | Measurement cols |
|---|---|---|---|---|---|
| [kidney-toxicity](../kidney-toxicity/schema.md) | `schema.md` | `nephrotox_grade` | `is_kidney_specific` | TRUE 769, FALSE 0 | 23 |
| [thrombocytopenia](../thrombocytopenia/schema.md) | `schema.md` | `thrombocytopenia_grade` | `is_platelet_specific` | TRUE 1,595, FALSE 191 | 23 |
| [chronic-neurotoxicity](../chronic-neurotoxicity/schema-cns.md) | `schema-cns.md` | `neurotox_grade` | `is_cns_specific` | TRUE 2,289, FALSE 104 | 26 |
| [hydrocephalus](../hydrocephalus/) | none of its own — uses the CNS schema | `neurotox_grade` | `is_cns_specific` | TRUE 146, FALSE 1 | 26 |

What this table makes concrete:

- **The 0–3 grades are not comparable across endpoints.** Each rubric is written in its own
  organ's terms — the kidney rubric grades proteinuria, KIM-1/NGAL/clusterin and dialysis; the
  CNS rubric does not, and cannot. A grade 2 in one dataset asserts nothing about a grade 2 in
  another. Any cross-endpoint severity claim needs a rubric that does not yet exist.
- **Two endpoints share a grade column for a historical reason, not a principled one.**
  `neurotox_grade` spans chronic-neurotoxicity and hydrocephalus because both were split out of
  one corpus. That is the only place two endpoints agree on a column, and it is an artefact of
  provenance.
- **The scope flag is four names for one idea.** `is_kidney_specific` is TRUE for all 769 kidney
  rows and has no FALSE row, so as a boolean it still carries no information; the other three
  flags do discriminate. Reconciling these into one endpoint key is open work.
- **Hydrocephalus has no schema document.** It inherits
  [`../chronic-neurotoxicity/schema-cns.md`](../chronic-neurotoxicity/schema-cns.md) by
  provenance rather than by reference. Nothing in [`../hydrocephalus/`](../hydrocephalus/) states
  which schema governs its columns.

Two kidney presentation assets remain stale in a way that touches this section, because their
subject matter — the data model and the extraction ladder — is infrastructure rather than
kidney-specific content:

| Asset | What it renders | Why it is now wrong |
|---|---|---|
| [`assets/datamodel.svg`](../kidney-toxicity/presentation/assets/datamodel.svg) | "65 drugs", "17 columns", "111 measurements", "23 columns", the field name `nephrotox_grade (0–3)` | The shipped kidney dataset is 71 oligos across 21 columns and 769 measurements across 23. Three of its four figures are wrong, and the diagram presents one endpoint's grade column as *the* grade column. |
| [`assets/extraction.svg`](../kidney-toxicity/presentation/assets/extraction.svg) | "111 graded rows"; source_ids N2, K1, M1, N3, REV, WS | The shipped kidney dataset has 769 rows drawn from 17 source_ids. |

Both are embedded in [`../kidney-toxicity/presentation/PRESENTATION.md`](../kidney-toxicity/presentation/PRESENTATION.md)
(lines 318 and 464) and are baked into the three built decks alongside it —
`OligoTox-Kidney.pdf`, `OligoTox-Kidney.pptx`, `OligoTox-Kidney-editable.pptx`. No rebuild
command exists anywhere in the repository; a grep for `marp|npx|pandoc|libreoffice|soffice`
finds only `marp: true` in the front matter of `PRESENTATION.md` itself. The decks therefore
cannot be regenerated from the repository as it stands.
