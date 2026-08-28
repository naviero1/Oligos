# Immunotoxicity / immunostimulation

Innate immune activation by an oligonucleotide itself — cytokine and interferon induction driven by backbone
chemistry and sequence motifs rather than by target knockdown. It is the sixth endpoint named in the Challenge
brief's list, quoted verbatim in the repository register, [`../README.md`](../README.md). **No immunotoxicity
dataset was built.** One dedicated PDF is held — Sioud 2005, a per-siRNA immunostimulation screen — now under
[`sources/`](./sources), and nothing has been taken from it. Four sibling endpoints do carry data —
kidney-toxicity (769 measurements), thrombocytopenia (1786), chronic-neurotoxicity (2393), hydrocephalus (147)
— and two of them hold cytokine-induction rows as adjacent readouts inside their own endpoints (§4). This file
records what the Sioud PDF holds and where those scattered immune readouts sit.

## 1. Status

| | Value |
|---|---|
| Oligos | 0 — `immunotoxicity/` holds no `data/` directory |
| Measurement rows | 0 |
| Local source PDFs | 1 dedicated, under [`sources/`](./sources); 2 cross-cutting PDFs in `../_shared/sources/` carry a section |
| `source_id`s reaching any `measurements.csv` | none; no `source_id` has ever been assigned to this endpoint |
| Extraction status | not started; no grading rubric written for this endpoint |
| Mentions in the kidney lane's own docs | 2 — a grep for `sioud\|immunostim\|immunotox\|cytokine\|interferon\|TLR\|inflammat` across `../kidney-toxicity/` returns `SOURCES.md:205` (the registry entry) and `presentation/PRESENTATION.md:349` (the word "inflammation", glossing glomerulonephritis). The endpoint is named as an endpoint only in [`../README.md`](../README.md) and `../REVIEW-2026-08.md`. |
| Immune readouts elsewhere in the repository | 55 measurement rows — 47 in `../thrombocytopenia/data/measurements.csv`, 8 in `../chronic-neurotoxicity/data/measurements.csv` (§4) |
| Deck coverage | none — `../kidney-toxicity/presentation/PRESENTATION.md:349` uses "inflammation" only to gloss glomerulonephritis inside the renal rubric |

## 2. Work done

Acquisition and filing only. The PDF was uploaded and entered in the kidney lane's registry at
`../kidney-toxicity/SOURCES.md:205` as `(immunostimulation; off-endpoint)`. No `source_id` was assigned, no table
was read into any `data/`, no rubric was written, and no scope statement in the repository records a decision —
inclusion or exclusion — for this endpoint (§5 item 2). That one-word label is the whole of the reasoning on file.

## 3. Sources allocated

Paths verified by directory listing; page counts, titles, DOIs and headings read from the files.

| File | Pages | `source_id` | State | Rows | What it carries |
|---|---:|---|---|---:|---|
| [`sources/Sioud_oligo_immunostimulation_cytokines_book.pdf`](./sources/Sioud_oligo_immunostimulation_cytokines_book.pdf) | 12 | none | acquired | 0 | Per-siRNA immunostimulation screen; Tables 1 and 2 |
| `../_shared/sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf` | 12 | none (cross-cutting) | acquired | 0 | Section "HYBRIDIZATION-INDEPENDENT PROINFLAMMATORY EFFECTS (CHALLENGE #1)", PDF p.4 |
| `../_shared/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf` | 416 | none (cross-cutting) | acquired | 0 | Ch.25 §3.1.3, PDF pp.354–355 |

**The dedicated file is misnamed.** Its `_book` suffix is wrong: PDF p.1 gives the title
*"Induction of Inflammatory Cytokines and Interferon Responses by Double-stranded and Single-stranded
siRNAs is Sequence-dependent and Requires Endosomal Localization"*, sole author Mouldy Sioud, footer
`doi:10.1016/j.jmb.2005.03.013`, `J. Mol. Biol. (2005) 348, 1079–1090`. It is a 12-page primary research
article holding per-oligo material — the opposite of the "background reviews / textbooks / project docs (**NOT
per-row data**)" that `../kidney-toxicity/SOURCES.md:203` reserves the `reference/` tier for. Consolidation moved
the file into this endpoint's own `sources/`, which fixes the filing; the filename and the registry entry are
still wrong. Only the endpoint word in that entry (`immunostimulation`) is right.

**What it would yield.** Table 1 (PDF p.2, "Sequences of the siRNAs used in this study") prints 32 numbered
siRNAs with sense strand and target gene — all 21-mers with a `TT` 3′ overhang, e.g. `1
GGCCUUCCUACCUUCAGACTT` Mouse TNF-a. Table 2 (PDF p.10) adds four sequences H1–H4 in two printed columns
under "Sequences of siRNAs targeting human TNF-a"; Figure 8 tests those four as *inhibitors* of
siRNA-27-induced TNF-a, so their own immunostimulatory potential is not reported. Normalized (`U`→`T`) and
compared whole and `TT`-trimmed against the 462 distinct sequence strings held across all four populated
endpoints' `oligos.csv` files (66 of them the kidney set's, from 64 filled `sequence_5to3` values, 59
distinct), all 36 give **zero matches** — extraction would add new oligos, not annotate existing ones.

**Extractability limit.** Neither table has a toxicity, potency or magnitude column; the cytokine
magnitudes are in the figures, and not all eight carry per-siRNA ELISA data (Figure 5 is a schematic of
intracellular siRNA signaling, Figure 3 is flow cytometry of TLR3, Figure 7(a) of CD83 — though Figure 7(b)
adds an IL-12 comparison of siRNA 27 against control siRNA 32). What is stated in text, on **PDF p.4**
(journal p.1082), is aggregate: *"Specific ELISA on culture supernatants revealed that
around 50% of the tested siRNAs induced the production of TNF-a (Figure 1(a))"*, and, three sentences later
in the same paragraph, *"Only six of the siRNAs examined exhibited a strong immunostimulatory effect, with
siRNA 27 being the most effective under our experimental conditions."* The six are not enumerated in text;
the model is adherent human PBMC, DOTAP-complexed, 18 hours. Per-siRNA numeric values are therefore
figure-bound, and digitisability has not been assessed.

**Cross-cutting sections.** Two multi-endpoint PDFs held in `../_shared/sources/` and indexed in
[`../_shared/README.md`](../_shared/README.md) carry immunotoxicity-relevant sections. Both loci are already cited
by sibling dossiers for other endpoints — Ch.25 §3.1.3 in [`../thrombocytopenia/README.md`](../thrombocytopenia/README.md)
for its TCP passage; Frazier 2015 PDF p.4 in [`../complement-activation/README.md`](../complement-activation/README.md),
section "Sources allocated", for complement — but neither reads them for the proinflammatory content this endpoint
owns. Frazier 2015 PDF p.4 names proinflammatory effects as the first of the review's three challenges and states
that *"the preclinical proinflammatory lesions of greatest concern are related to glomerulonephritis (as described
subsequently) and vasculitis associated with some types of ASO administration in monkeys."* MMB 2434 Ch.25 §3.1.3
(PDF pp.354–355) summarises proinflammatory manifestations and design rules. It is adjacent to Ch.25 §3.1.2, which
[`../_shared/README.md`](../_shared/README.md) § 1.4 "Methods in Molecular Biology 2434 — misfiling resolved"
allocates to [`../complement-activation/README.md`](../complement-activation/README.md) and
[`../coagulopathy/README.md`](../coagulopathy/README.md); §3.1.3 is read here, not substituted for it.

## 4. Data

No dataset in this repository is keyed to this endpoint and `immunotoxicity/` holds no `data/`. Cytokine readouts
do exist in two sibling datasets, in both cases as adjacent readouts collected because they sat beside that
endpoint's own measurement. `../thrombocytopenia/data/measurements.csv` holds 47: `IL-8_release` (26) and
`MCP-1_release` (21), `readout_category = immunogenicity`, human whole blood in vitro, 16 oligos, from
`PMC5673186; doi:10.1371/journal.pone.0187574` and `10.3324/haematol.2020.260059`, all 47 flagged
`is_platelet_specific = FALSE`. `../chronic-neurotoxicity/data/measurements.csv` holds 8:
`proinflammatory_cytokine_release_7plex` (6) and the IL1B/IL6/IL8/IL10/IL12p70/IFNg/TNFa panel (2),
`readout_category = injury_biomarker`, `source_id = S_CNS_IV_MICROGLIA2024`, two oligos (`CNS544`, `CNS584`) in
hiPSC-derived microglia and human whole blood ex vivo. Those 55 rows are the closest the repository comes to this
endpoint and are not an immunotoxicity dataset: each is graded on its host endpoint's rubric
(`thrombocytopenia_grade`, `neurotox_grade`), carries that endpoint's schema and scope flag, and they span 18
oligos rather than a designed sequence series — the sequence-dependence this endpoint is about. The kidney dataset
holds no such readout at all: over its 769 rows, `readout_name` and `readout_category` return zero hits for
`cytokine|interferon|IFN|TLR|IL-?[0-9]|TNF|immunostim|immunogenic|inflammat`.

One kidney observation is immunotoxicity-adjacent but recorded as renal: `MSR067`
(donidalorsen, `OLG036`, clinical, human, `readout_name = renal_safety`, `readout_value = no_signal`,
`nephrotox_grade = 0`, `source_id = WS`) stores `effect_vs_control =
only_injection_site_AEs_no_renal_signal`, restated in `OLG036.notes` as
`renal_negative_only_injection_site_AEs`; MMB Ch.25 §3.1.3 names injection-site reactions among the
clinical manifestations of proinflammatory effects. That is one free-text string in a kidney-negative row,
in a schema with no field able to hold it — not a dataset. It also sits in the clinical population
`../kidney-toxicity/data/clinical_validation_2026-08.md` found confounded.

**Mechanistic overlap with the kidney endpoint.** Five kidney rows carry a glomerular lesion name, all stored as
`tissue = kidney` (`../kidney-toxicity/schema.md:53` declares `glomerulus`; zero of 769 rows use it). For the three
glomerulonephritis rows — `MSR001` crescentic_glomerulonephritis, `MSR015` glomerulonephritis, `MSR029`
renal_toxicity_potential_glomerulonephritis — Frazier 2015 p.4 places the lesion inside its
proinflammatory-effects section, so those three rest on a mechanism this endpoint owns. For `MSR004` and
`MSR013` (focal_segmental_glomerulosclerosis), **the immune mechanism is unverified**: "focal segmental"
and "glomerulosclerosis" return zero hits across Frazier 2015 (12 pp.) and Frazier 2022 (7 pp.), the two
reviews supplying this dossier's proinflammatory framing, so neither characterises FSGS as immune-mediated.

## 5. Known issues

1. `../kidney-toxicity/SOURCES.md:205` still registers a filename that misstates the document type (`_book`) for a
   source carrying 32 sequenced siRNAs. The endpoint is off *this project's chosen scope*, not the Challenge's.
2. No scope statement records a decision for this endpoint. `../kidney-toxicity/METHODOLOGY.md:20-22` ("1. Scope
   and design decisions") names kidney toxicity and nothing else, and the other three populated endpoints were
   curated on branches that never saw it. Exclusion here is indistinguishable from oversight.
3. No grading rubric exists and no existing grade column can be reused — the kidney rubric in
   `../kidney-toxicity/schema.md` is renal at every grade including 0, and [`../_shared/README.md`](../_shared/README.md)
   § 4 "The reconciliation problem" establishes that the four 0–3 grades are not comparable to each other.
4. The kidney `is_kidney_specific` flag is `TRUE` on 769 of 769 rows and defines `FALSE` as a "hepatotox/other
   fallback row"; a boolean cannot express a third endpoint, and the other three datasets each carry their own such
   flag (`is_platelet_specific`, `is_cns_specific`) — the same limit four times over.
5. Redistribution is unassessed. Sioud 2005 is Elsevier (PDF p.1: "q 2005 Elsevier Ltd. All rights reserved."), and
   the kidney `redistribution` enum's `derived_features_only` and `verify` classes are used by zero of its 769 rows.

## 6. Not done / blocked

| Not done | Cause |
|---|---|
| Any row ingested | Unrecorded scope decision; the PDF has been on disk since the only commit and its tables were never read |
| Per-siRNA cytokine values | Structural — the magnitudes are in figures, not tables; digitisability unassessed |
| Frazier & Obert 2018, "Drug-induced glomerulonephritis" | Never acquired; known only as reference-list item 5 inside `../kidney-toxicity/sources/Frazier2022_kidney_effects_review_ToxPathol.pdf` |

Acquisition is not the blocker for the 32 sequences: an unrecorded decision, an absent rubric and the lack of any
schema for this endpoint are, with the figure-bound magnitudes limiting numeric values only.

## 7. Next step

1. Rename the PDF on disk to drop `_book` — the "book" defect is in the filename, not in the annotation —
   and update `../kidney-toxicity/SOURCES.md:205` to Sioud 2005, *J. Mol. Biol.* 348:1079–1090, replacing the bare
   "off-endpoint" with what the file holds (32 sequenced siRNAs, Table 1, PDF p.2).
2. Record an explicit scope decision in the register [`../README.md`](../README.md) and at
   `../kidney-toxicity/METHODOLOGY.md:20-22`; the defensible reason is §3's — the per-siRNA cytokine magnitudes are figure-bound and digitisability is unassessed.
3. Assign a `source_id`, and resolve the Elsevier redistribution class before any extraction.
4. Before ingesting any row, this endpoint needs its own two-table dataset under `immunotoxicity/data/` with its own
   graded column and rubric, on the pattern of the four populated endpoints. Do not reuse any existing grade column.
5. Assess whether Figure 1(a) is digitisable — the answer decides whether the yield is 32 sequences with
   two text-stated calls, or 32 with a per-siRNA call each.
6. The `tissue = glomerulus` edit belongs to [`../kidney-toxicity/README.md`](../kidney-toxicity/README.md)
   § "Known issues and open work"; this dossier contributes the mechanistic split in §4, not the edit.
7. Cross-reference the 55 cytokine rows in §4 from their host datasets, which do not name this endpoint.

---

Index: register [`../README.md`](../README.md) · [`../kidney-toxicity/README.md`](../kidney-toxicity/README.md) · [`../hepatotoxicity/README.md`](../hepatotoxicity/README.md) · [`../thrombocytopenia/README.md`](../thrombocytopenia/README.md) · [`../chronic-neurotoxicity/README.md`](../chronic-neurotoxicity/README.md) · [`../hydrocephalus/README.md`](../hydrocephalus/README.md) · [`../_shared/README.md`](../_shared/README.md) · [`../kidney-toxicity/schema.md`](../kidney-toxicity/schema.md) · [`../_shared/sources/SOURCES-kidney-legacy.md`](../_shared/sources/SOURCES-kidney-legacy.md)
