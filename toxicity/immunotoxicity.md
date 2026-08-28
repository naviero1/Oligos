# Immunotoxicity / immunostimulation

Innate immune activation by an oligonucleotide itself — cytokine and interferon induction driven by
backbone chemistry and sequence motifs rather than by target knockdown. It is the sixth endpoint named in
the Challenge brief's list, quoted verbatim in [`README.md`](./README.md). **This project extracted no
immunotoxicity data.** One dedicated PDF is held — Sioud 2005, a per-siRNA immunostimulation screen — but
it is filed under `sources/reference/` and labelled off-endpoint, so real immunotoxicity material is
shelved as background. This file records what that PDF holds and that nothing has been taken from it.

## 1. Status

| | Value |
|---|---|
| Oligos in [`data/oligos.csv`](../data/oligos.csv) | 0 |
| Measurement rows in [`data/measurements.csv`](../data/measurements.csv) | 0 |
| Local source PDFs | 1 dedicated, under `sources/reference/`; 2 cross-cutting PDFs carry a section |
| `source_id`s reaching `measurements.csv` | none; no `source_id` has ever been assigned to this endpoint |
| Extraction status | not started; no grading rubric written for this endpoint |
| Mentions in the curated corpus | 2 — a grep of `*.md` for `sioud\|immunostim\|immunotox\|cytokine\|interferon\|TLR\|inflammat` over `data/`, `sources/`, `scripts/`, `METHODOLOGY.md`, `schema.md`, `PADP.md` and `PRESENTATION.md` returns `sources/SOURCES.md:209` (the registry entry) and `PRESENTATION.md:349` (the word "inflammation", glossing glomerulonephritis). The endpoint is also named in `README.md` and `REVIEW-2026-08.md`, both added by this reorganization. |
| Deck coverage | none — `PRESENTATION.md:349` uses "inflammation" only to gloss glomerulonephritis inside the renal rubric |

## 2. Work done

Acquisition and filing only. The PDF was uploaded and entered in the registry at `sources/SOURCES.md:209`
as `(immunostimulation; off-endpoint)`. No `source_id` was assigned, no table was read into `data/`, no
rubric was written, and neither of the repository's two scope statements records a decision — inclusion or
exclusion — for this endpoint (§5 item 2). That one-word label is the whole of the reasoning on file.

## 3. Sources allocated

Paths verified by directory listing; page counts, titles, DOIs and headings read from the files.

| File | Pages | `source_id` | State | Rows | What it carries |
|---|---:|---|---|---:|---|
| `sources/reference/Sioud_oligo_immunostimulation_cytokines_book.pdf` | 12 | none | acquired | 0 | Per-siRNA immunostimulation screen; Tables 1 and 2 |
| `sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf` | 12 | none (cross-cutting) | acquired | 0 | Section "HYBRIDIZATION-INDEPENDENT PROINFLAMMATORY EFFECTS (CHALLENGE #1)", PDF p.4 |
| `sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf` | 416 | none (cross-cutting) | acquired | 0 | Ch.25 §3.1.3, PDF pp.354–355 |

**The dedicated file is misnamed and misfiled.** Its `_book` suffix is wrong: PDF p.1 gives the title
*"Induction of Inflammatory Cytokines and Interferon Responses by Double-stranded and Single-stranded
siRNAs is Sequence-dependent and Requires Endosomal Localization"*, sole author Mouldy Sioud, footer
`doi:10.1016/j.jmb.2005.03.013`, `J. Mol. Biol. (2005) 348, 1079–1090`. It is a 12-page primary research
article holding per-oligo material — the opposite of the "background reviews / textbooks / project docs
(**NOT per-row data**)" that `sources/SOURCES.md:207` reserves `sources/reference/` for. Only the endpoint
word in the registry entry (`immunostimulation`) is right.

**What it would yield.** Table 1 (PDF p.2, "Sequences of the siRNAs used in this study") prints 32 numbered
siRNAs with sense strand and target gene — all 21-mers with a `TT` 3′ overhang, e.g. `1
GGCCUUCCUACCUUCAGACTT` Mouse TNF-a. Table 2 (PDF p.10) adds four sequences H1–H4 in two printed columns
under "Sequences of siRNAs targeting human TNF-a"; Figure 8 tests those four as *inhibitors* of
siRNA-27-induced TNF-a, so their own immunostimulatory potential is not reported. Normalized (`U`→`T`) and
compared whole and `TT`-trimmed against the 55 filled `sequence_5to3` values in `data/oligos.csv` (53
distinct; two values appear twice), all 36 give **zero matches** — extraction would add new oligos, not
annotate existing ones.

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

**Cross-cutting sections.** Two acquired multi-endpoint PDFs, indexed in
[`cross-cutting.md`](./cross-cutting.md), carry immunotoxicity-relevant sections. Both loci are already
cited by sibling dossiers for other endpoints — Ch.25 §3.1.3 in [`thrombocytopenia.md`](./thrombocytopenia.md),
sections 3 "Sources allocated" and 4 "Data", for its TCP passage; Frazier 2015 PDF p.4 in
[`complement-activation.md`](./complement-activation.md), section "Sources allocated", for complement — but
neither reads them for the proinflammatory content this endpoint owns. Frazier 2015 PDF p.4 names
proinflammatory effects as the first of the review's three challenges and states that
*"the preclinical proinflammatory lesions of greatest concern are related to
glomerulonephritis (as described subsequently) and vasculitis associated with some types of ASO
administration in monkeys."* MMB 2434 Ch.25 §3.1.3 (PDF pp.354–355) summarises proinflammatory
manifestations and design rules. It is adjacent to Ch.25 §3.1.2, which [`cross-cutting.md`](./cross-cutting.md)
section 1.4 "Methods in Molecular Biology 2434 — misfiling finding" allocates to
[`complement-activation.md`](./complement-activation.md) and [`coagulopathy.md`](./coagulopathy.md);
§3.1.3 is read here, not substituted for it.

## 4. Data

No column in `data/measurements.csv` records an immune or cytokine readout, and no oligo or measurement row
belongs to this endpoint. One observation is immunotoxicity-adjacent but recorded as kidney: `MSR067`
(donidalorsen, `OLG036`, clinical, human, `readout_name = renal_safety`, `readout_value = no_signal`,
`nephrotox_grade = 0`, `source_id = WS`) stores `effect_vs_control =
only_injection_site_AEs_no_renal_signal`, restated in `OLG036.notes` as
`renal_negative_only_injection_site_AEs`; MMB Ch.25 §3.1.3 names injection-site reactions among the
clinical manifestations of proinflammatory effects. That is one free-text string in a kidney-negative row,
in a schema with no field able to hold it — not a dataset. It also sits in the clinical population
`data/clinical_validation_2026-08.md` found confounded.

**Mechanistic overlap with the kidney endpoint.** Five kidney rows carry a glomerular lesion name, all
stored as `tissue = kidney` (`schema.md:49` declares `glomerulus`; zero of 111 rows use it). For the three
glomerulonephritis rows — `MSR001` crescentic_glomerulonephritis, `MSR015` glomerulonephritis, `MSR029`
renal_toxicity_potential_glomerulonephritis — Frazier 2015 p.4 places the lesion inside its
proinflammatory-effects section, so those three rest on a mechanism this endpoint owns. For `MSR004` and
`MSR013` (focal_segmental_glomerulosclerosis), **the immune mechanism is unverified**: "focal segmental"
and "glomerulosclerosis" return zero hits across Frazier 2015 (12 pp.) and Frazier 2022 (7 pp.), the two
reviews supplying this dossier's proinflammatory framing, so neither characterises FSGS as immune-mediated.

## 5. Known issues

1. `sources/SOURCES.md:209` registers a filename that misstates the document type (`_book`), and its
   placement in `sources/reference/` contradicts `:207`'s "NOT per-row data" for a source carrying 32
   sequenced siRNAs. The endpoint is off *this project's chosen scope*, not off the Challenge's.
2. Neither scope statement records a decision for this endpoint. `README.md` § "Scope (decided — not under review)" fixes the kidney scope
   as "decided — not under review"; `METHODOLOGY.md:20-22`, under "1. Scope and design decisions", names
   the same endpoint. Neither names any other, so exclusion is indistinguishable from oversight.
3. No grading rubric exists, and `nephrotox_grade` cannot be reused — `schema.md:74-77` is renal at every
   grade including 0 ([`cross-cutting.md`](./cross-cutting.md) section 4 claims this for grades 1–3 only).
4. `is_kidney_specific` is `TRUE` on 111 of 111 rows and `schema.md:61` defines `FALSE` as a
   "hepatotox/other fallback row"; a boolean cannot express a third endpoint.
5. Redistribution is unassessed. Sioud 2005 is Elsevier (PDF p.1: "q 2005 Elsevier Ltd. All rights
   reserved."), and `schema.md:65`'s `derived_features_only` and `verify` classes are used by zero of 111
   rows, so there is no worked precedent.

## 6. Not done / blocked

| Not done | Cause |
|---|---|
| Any row ingested | Unrecorded scope decision; the PDF has been on disk since the only commit and its tables were never read |
| Per-siRNA cytokine values | Structural — the magnitudes are in figures, not tables; digitisability unassessed |
| Frazier & Obert 2018, "Drug-induced glomerulonephritis" | Never acquired; known only as reference-list item 5 inside `sources/kidney/Frazier2022_kidney_effects_review_ToxPathol.pdf` |

Acquisition is not the blocker for the 32 sequences: an unrecorded decision, an absent rubric and a
renal-only schema are, with the figure-bound magnitudes limiting numeric values only.

## 7. Next step

1. Rename the PDF on disk to drop `_book` — the "book" defect is in the filename, not in the annotation —
   and update `sources/SOURCES.md:209` to Sioud 2005, *J. Mol. Biol.* 348:1079–1090, replacing the bare
   "off-endpoint" with what the file holds (32 sequenced siRNAs, Table 1, PDF p.2).
2. Record an explicit scope decision beside both `README.md` § "Scope (decided — not under review)" and `METHODOLOGY.md:20-22`. The
   defensible reason for exclusion is the one in §3 — the per-siRNA cytokine magnitudes are figure-bound
   and digitisability is unassessed.
3. Assign a `source_id`, and resolve the Elsevier redistribution class before any extraction.
4. Before ingesting any row, add a dedicated graded column with its own rubric in
   [`schema.md`](../schema.md). Do not reuse or rename `nephrotox_grade`.
5. Assess whether Figure 1(a) is digitisable — the answer decides whether the yield is 32 sequences with
   two text-stated calls, or 32 with a per-siRNA call each.
6. The `tissue = glomerulus` edit is tracked in [`kidney-nephrotoxicity.md`](./kidney-nephrotoxicity.md),
   section 6 "Known issues" item 5 and section 8 "Next step" item 6; this dossier contributes the
   mechanistic split in §4, not the edit.

---

Index: [`README.md`](./README.md) · [`kidney-nephrotoxicity.md`](./kidney-nephrotoxicity.md) · [`hepatotoxicity.md`](./hepatotoxicity.md) · [`thrombocytopenia.md`](./thrombocytopenia.md) · [`cross-cutting.md`](./cross-cutting.md) · [`../METHODOLOGY.md`](../METHODOLOGY.md) · [`../schema.md`](../schema.md) · [`../sources/SOURCES.md`](../sources/SOURCES.md)
