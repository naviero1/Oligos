# Chronic neurotoxicity

Chronic neurotoxicity is the seventh endpoint on the Challenge's list of toxicities of interest, quoted verbatim from the brief at [`README.md`](./README.md#scope-authority). **This project has done no work on it:** no source acquired, no rows extracted, and the endpoint is named in no file in `data/`, `sources/`, `scripts/` or the deck (a case-insensitive grep for `neurotox|neurodegener|hydrocephal|CNS toxicity` over the curated corpus returns nothing; it now appears only in `README.md`, `REVIEW-2026-08.md` and this directory, all added by this reorganization). No scope decision was recorded either — `sources/SOURCES.md` holds no section, note or exclusion statement for it. This dossier supplies the missing statement: **out of scope for Phase 2**, on the grounds in §2 and §5.

## 1. Status

| Item | Count | Basis |
|---|---:|---|
| Oligos | 0 | No oligo row carries a neurological toxicity observation — §3 |
| Measurement rows | 0 | All 111 rows in `data/measurements.csv` are kidney; no neurological readout exists |
| `source_id`s | 0 | All 16 `source_id`s in use belong to [kidney](./kidney/kidney-nephrotoxicity.md) |
| Source PDFs held | 0 | No PDF in `sources/` is a neurotoxicity source — §2 |
| Extraction status | not started | Nothing to extract from |

## 2. Sources allocated

**None.** All 18 PDFs in `sources/` were swept with the case-insensitive pattern `neurotox|neurodegener|hydrocephal|neuroinflamm|neuronal` over their full text layers. Fifteen return zero hits, including all five hepatotox sources, both Frazier reviews, and every kidney PDF except the MMB volume treated below. Three return hits; none is a source for this endpoint, and all three are already allocated in [`cross-cutting.md`](./cross-cutting.md).

| File | Pattern / strict `neurotox` hits | Why it is not a source here |
|---|---|---|
| [`CasarettDoull_Toxicology_textbook.pdf`](_shared/reference/CasarettDoull_Toxicology_textbook.pdf) (1,473 pp.) | 804 / 625 | General toxicology. Only 14 of its pages mention oligonucleotides or antisense at all, and none of those 14 also carries a `neurotox` hit. |
| [`MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](kidney/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) (416 pp.) | 18 / **0** | All 18 hits are `neurodegener` or `neuronal`; most are the CNS as a *therapeutic target* (Batten disease, Parkinson's, neuromuscular and neurodegenerative indications). Two passages touch CNS safety — below. |
| [`OligoTox_challenge_brief.pdf`](_shared/reference/OligoTox_challenge_brief.pdf) (6 pp.) | 4 / 2 | Scope authority naming the endpoint, not evidence about it. Both strict hits are on p.1, inside the authoritative portion (provenance caveat: [`cross-cutting.md`, §1.1 "Challenge brief — provenance defect (pp.3b–6)"](./cross-cutting.md#11-challenge-brief--provenance-defect-pp3b6)). |

Two passages touch CNS safety; neither is oligonucleotide-specific evidence for this endpoint.

**Chapter 24**, "Intrathecal Delivery of Therapeutic Oligonucleotides for Potent Modulation of Gene Expression in the Central Nervous System" (PDF pp.341–349 = book pp.345–353), is allocated to this endpoint as "delivery route; chronic neurotoxicity context" by the chapter table at [`cross-cutting.md`, §1.4 "Methods in Molecular Biology 2434 — misfiling finding"](./cross-cutting.md#14-methods-in-molecular-biology-2434--misfiling-finding). Its Notes (PDF p.348 = book p.352) state that 10 µL injections in adult mice "are well-tolerated and do not cause neuronal loss, astrogliosis, or microgliosis [9]". That is a **procedure and volume** qualification — it names no oligonucleotide, dose or duration, and concerns single injections — so it supports the delivery method, not a chronic-toxicity finding.

**Chapter 25**, "Preclinical Safety Assessment of Therapeutic Oligonucleotides" (Patrik Andersson, chapter head at PDF p.350), §3.2.1 (PDF p.356 = book p.361): the author states that, to the author's knowledge, there is no information on systemically administered ASOs or siRNA "showing activity in vitro or in vivo safety pharmacology studies, including activity on the hERG channel or any other ion channels important for cardiovascular or neuronal function", while noting that direct delivery into heart and CNS "is a different story and could result in functional effects". It reports an **absence of available information**, not a demonstrated negative, and carries no compound, dose, species or value. Ion-channel activity maps to the acute axis the brief deprioritizes ("alterations of neuronal electrical activity", brief p.1); the passage itself uses neither "acute" nor "chronic", so that mapping is this dossier's inference. Neither passage addresses the chronic axis, and neither does anything else the §2 and §3 sweeps reached.

## 3. Data

No file or column in `data/` carries a record for this endpoint. Sweeping all 23 columns × 111 measurement rows and all 17 columns × 65 oligo rows with `neuro|CNS|brain|cerebr|spinal|cognit|ventricul|hydrocephal|axon|myelin|intrathecal|neuron` returns 10 field-level matches across 7 loci. Every one is a renal row, a route string, or a drug-identity field belonging to an oligo indicated for neurological disease — listed so a later sweep does not re-open them as findings.

| Loci | Field | What it is |
|---|---|---|
| `MSR011`, `MSR030` | `delivery_method=intrathecal` | Nusinersen (`OLG004`). Both read out `urine_protein_elevated` (58 and 69 `pct_incidence`), `tissue=kidney`, `nephrotox_grade=1`. **Renal rows; the route is intrathecal because the drug is.** |
| `MSR042` | `delivery_method`, `notes` | Tofersen (`OLG017`). `readout_name=proteinuria`, `readout_value=none`, `nephrotox_grade=0` — the *absence* of a renal finding. Its note `neuro_AEs_predominate_ASO_class_renal_statement` mentions neurological AEs only to explain why the renal signal is not the dominant one. No neurological AE is named, counted or graded. |
| `MSR001`, `OLG001` | `source_table`, `indication`, `design_source` | Inotersen: the NEURO-TTR trial name used as a provenance locus, and the treated disease (hATTR polyneuropathy). All 5 of its rows are `systemic_dose`. |
| `OLG004`, `OLG017` | `indication`, `notes` | Route strings (`intrathecal_delivery`, `intrathecal`); `OLG017`'s note is a *renal* class precaution. `OLG004`'s `indication` is `spinal_muscular_atrophy` — the treated disease, not a toxicity observation. |

The three oligos the sweep matched — `OLG001` inotersen, `OLG004` nusinersen, `OLG017` tofersen — carry 8 measurement rows between them, all kidney. The rule is the regex above, not a clinical judgement: the four hATTR oligos (`OLG018`, `OLG019`, `OLG022`, `OLG023`) and the five DMD oligos (`OLG008`, `OLG011`, `OLG012`, `OLG013`, `OLG016`) are also indicated for neuromuscular or amyloid disease but their `indication` strings contain no pattern term, so they fall outside this list — and no field of theirs matched the sweep either. Two of the three are intrathecally delivered; inotersen is systemic in every row. Their identity and design fields are curated, so the identity layer for them exists; no neurological observation is attached to any of them.

## 4. Known issues that apply here

- The eight-endpoint list existed in the repository only as a PDF; no markdown file quoted or named it, so an endpoint with zero artifacts was indistinguishable from one that was never part of the Challenge (audit finding, `major`). Quoting it at [`README.md`](./README.md#scope-authority) is the fix.
- The same silence covers five of the other six non-kidney endpoints (audit finding, `minor`). Hepatotoxicity is the exception: `sources/SOURCES.md:83`, `:169` and `:216` carry its fallback status, and the root [`README.md` § "Record counter" (the hepatotox-fallback row)](../README.md) records the decision as "not needed".
- The MMB 2434 volume is misfiled under `sources/kidney/` although it is a 416-page multi-chapter book — which is why the §2 sweep had to reach into a kidney-filed file. Finding and fix in [`cross-cutting.md`, §1.4 "Methods in Molecular Biology 2434 — misfiling finding"](./cross-cutting.md#14-methods-in-molecular-biology-2434--misfiling-finding).
- Scope of verification: the sweeps above cover PDF text layers, tables and reference lists. Figure content was not searched.

## 5. Not done, and next step

| Not done | Cause |
|---|---|
| No rows extracted | No source in the repository carries a per-compound neurological readout. The two passages in §2 are an injection-procedure note and a class-level statement about missing information. |
| No source acquired | Deliberate: no candidate was ever entered on the fetch list, and the scope decision above leaves it that way for Phase 2. |
| No grading rubric | The 0–3 rubric in [`schema.md`](kidney/schema.md) is written entirely in renal terms and is not transferable; a second endpoint needs its own graded column and rubric ([`cross-cutting.md`, §4 "What must change if a second endpoint is populated"](./cross-cutting.md#4-what-must-change-if-a-second-endpoint-is-populated)). |
| No chronic/acute boundary defined | The brief distinguishes chronic neurotoxicity from acute alterations of neuronal electrical activity but defines neither. Adopting the endpoint would require drawing that line here. |

No acquisition work is proposed; the deliverable for this endpoint is the scope statement above. If it were ever advanced, the order is: define the chronic/acute boundary, add a neurotoxicity-specific graded column with a written rubric, then acquire a primary source from outside the current library.
