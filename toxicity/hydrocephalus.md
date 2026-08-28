# Hydrocephalus — endpoint dossier

**Status:** `not-addressed` · **Register:** [`./README.md`](./README.md) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md#scope-authority)). This project curated kidney toxicity only. Nothing was acquired, extracted or decided for this endpoint: zero rows, zero oligos, zero `source_id`s and no dedicated source. No oligonucleotide-specific material of any kind bears on it — of the 18 PDFs in `sources/`, the word occurs in exactly two, both reference PDFs (the brief's own endpoint list and a general-toxicology textbook), itemised below, and in no file in `data/` or `scripts/`. The other `not-addressed` endpoint differs: [`./chronic-neurotoxicity.md`](./chronic-neurotoxicity.md) has one relevant oligonucleotide passage to weigh. This file exists so that the absence is recorded rather than silent.

## Status

| | Value |
|---|---|
| Oligos | 0 |
| Measurement rows | 0 |
| Dedicated source PDFs | 0 |
| `source_id`s | 0 |
| Extraction status | not started; no source acquired and no candidate named anywhere in [`sources/SOURCES.md`](../sources/SOURCES.md) |
| Graded column and rubric | none — see §"Not done, and why" |

## Sources allocated

No PDF in `sources/` was acquired for this endpoint. A case-insensitive `hydrocephal` sweep over the full text of all 18 PDFs under `sources/` returns 7 hits in 2 files; the other 16 return zero.

| File | Hits (pages) | Bearing on this endpoint | `source_id` | Rows |
|---|---:|---|---|---:|
| [`sources/reference/OligoTox_challenge_brief.pdf`](../sources/reference/OligoTox_challenge_brief.pdf) | 1 (1) | The word inside the page-1 endpoint list. Scope authority, not evidence. | none | 0 |
| [`sources/reference/CasarettDoull_Toxicology_textbook.pdf`](../sources/reference/CasarettDoull_Toxicology_textbook.pdf) | 6 (5) | General toxicology, itemised below. Not oligonucleotide content. | none | 0 |

Both files are allocated to [`./cross-cutting.md`](./cross-cutting.md).

The six textbook occurrences, by PDF page: **511** (×2) cyclophosphamide and its metabolites causing hydrocephaly in gestation-day-13 rat embryos; **517** congenital *Toxoplasma gondii* infection in infants; **768** a table row listing tellurium as a neurotoxicant causing hydrocephalus in experimental animals; **1037** tellurium compounds in rats after gestational exposure; **1098** glycol ethers among rodent structural anomalies. None of those five pages carries the word `oligonucleotide` or `antisense` (checked per page). They are small-molecule and infectious teratology, each a bare mention in a malformation list or a table cell; the volume nowhere defines the lesion. No claim in this register traces to them.

## Data

Zero rows, and no column that could hold one. A case-insensitive sweep for `hydrocephal|ventricul|cerebrospinal|intracranial|CSF|imaging|MRI|ultrasound` over all 23 columns × 111 rows of [`data/measurements.csv`](../data/measurements.csv) and all 17 columns × 65 rows of [`data/oligos.csv`](../data/oligos.csv) returns 0 hits in each. `tissue` is enumerated at `schema.md:49` as `kidney | proximal_tubule | glomerulus | NA` and `readout_category` at `schema.md:54` as `functional | injury_biomarker | viability | accumulation | histopathology | clinical_renal_outcome`; both vocabularies are wholly renal. Three rows are dosed into the CSF (`delivery_method = intrathecal`: `MSR011`, `MSR030`, `MSR042`) and all three record a renal readout; they are analysed in [`./chronic-neurotoxicity.md`](./chronic-neurotoxicity.md), not here — route of administration is not evidence of this endpoint.

## Known issues

- **No scope decision is recorded outside this file.** `README.md`, `METHODOLOGY.md` and `sources/SOURCES.md` say nothing about this endpoint. `SOURCES.md`'s 18 sections are all organised around sources acquired or sought — by endpoint bucket (`KIDNEY-SPECIFIC` `:28`, `HEPATOTOX FALLBACK` `:83`), by location (`LOCAL SOURCE FILES` `:189`) and by fetch priority — with no section for an endpoint considered and excluded, so no exclusion is recorded there for this or any other endpoint. This dossier **recommends** recording the exclusion; the decision has not been taken or propagated.
- **The scope authority is only partly authentic** — cite pp.1–3a only ([`cross-cutting.md`, §1.1 "Challenge brief — provenance defect (pp.3b–6)"](./cross-cutting.md#11-challenge-brief--provenance-defect-pp3b6)). This matters here because the page-1 sentence is the only evidence this dossier rests on. Every count above traces to page 1 or to the sweeps; nothing to pages 3b–6.
- **Verification scope:** the PDF counts come from text layers only — figure content was not examined; the CSV counts are full-column sweeps of both data files.

## Not done, and why

| Not done | Cause |
|---|---|
| No rows, oligos or `source_id` | No document in `sources/` reports a hydrocephalus outcome for any oligonucleotide. The seven occurrences of the word are six general-toxicology passages plus the brief's own list entry. |
| No source acquired | Nothing in `sources/SOURCES.md` names a candidate — not in the kidney section (`:28`), the hepatotox section (`:83`), the fetch list (`:152`) or the source-hunting strategy (`:177`). |
| No rubric or schema support | `nephrotox_grade`'s rubric ([`schema.md`](../schema.md), "`nephrotox_grade` rubric (0–3)") is renal and not transferable, and there is no imaging, ventricular-volume or CSF field. Extraction would require new columns, not just new rows. |

## Next step

1. Record hydrocephalus as swept and out of scope for Phase 2, in `sources/SOURCES.md` or `METHODOLOGY.md`. The sweeps above are the evidence that the exclusion is informed rather than inadvertent.
2. Keep this dossier in step with `sources/`: if a hydrocephalus source is ever acquired, the sweeps in §"Sources allocated" must be re-run, since they are the basis for the exclusion.
3. No acquisition is proposed. Advancing this endpoint would require acquiring a primary source, adding CNS terms to the `tissue` and `readout_category` vocabularies, and writing a separate graded column with its own rubric. That is a second dataset, not an extension of this one.
