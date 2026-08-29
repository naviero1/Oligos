# Coagulopathy — endpoint dossier

**Status:** `background-only` · **Register:** [`./README.md`](./README.md) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Coagulopathy is the fifth endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md)); in oligonucleotide safety it is, per the in-repo characterisation quoted below (MMB 2434 Ch.25 §3.1.2, PDF p.354), prolongation of coagulation time at high plasma Cmax of phosphorothioate-backbone ASOs. This project curated kidney toxicity only. Nothing was extracted for this endpoint, no source was acquired for it, and its entire footprint in the repository is three passages inside one multi-endpoint book held for a different reason.

## Status

| | Value |
|---|---|
| Oligos | 0 |
| Measurement rows | 0 |
| Dedicated source PDFs | 0 |
| `source_id`s | 0 |
| Extraction status | not started; no primary source acquired |
| Graded column and rubric | none — `nephrotox_grade`'s rubric ([`schema.md`](kidney/schema.md), "`nephrotox_grade` rubric (0–3)") is renal and not transferable |

The sweep used throughout this file is `coagul|aPTT|prothrombin|clotting|anticoagul|fibrinogen|thromboplastin` — laboratory clotting descriptors only. It deliberately omits `thrombin`, which matches on-target pharmacology (see "Not this endpoint"), and `bleeding|h[ae]morrhag`, the two commonest clinical descriptors of the endpoint; adding the latter pair adds exactly one file to the table below — 2 hits on PDF p.7 of [`sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf`](_shared/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf), both describing thrombocytopenic bleeding — alongside 1 further hit in the MMB volume and 109 in the general-toxicology textbook, and no per-compound coagulation value anywhere.

Over all 23 columns × 111 rows of [`data/measurements.csv`](kidney/data/measurements.csv) it returns 0 hits, and over all 17 columns × 65 rows of [`data/oligos.csv`](kidney/data/oligos.csv) also 0; the nearest near-miss is `OLG028`'s `target_gene` `SERPINC1_antithrombin`, which only a bare `thrombin` grep catches. The reason nothing is attributable here is not the column list — `readout_name` (`schema.md:55`) is a free string, and `is_kidney_specific` (`schema.md:61`) exists precisely to flag non-kidney rows — but the scope: `is_kidney_specific` is `TRUE` on all 111 rows, with no `FALSE` row in the table.

## Sources allocated

No PDF in `sources/` was acquired for this endpoint. The same sweep over all 18 acquired PDFs returns hits in three files; the other 15 return zero.

| File | Hits (pages) | Bearing on this endpoint | `source_id` | Rows |
|---|---:|---|---|---:|
| [`sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](kidney/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) | 7 (4) | The only real material — three passages, below. The remaining page, PDF p.111, is a chapter reference list citing coagulation factors as *therapeutic targets* for splicing rescue. | none | 0 |
| [`sources/reference/OligoTox_challenge_brief.pdf`](_shared/reference/OligoTox_challenge_brief.pdf) | 1 (1) | The word "coagulopathy" in the page-1 endpoint list. Scope authority, not evidence. | none | 0 |
| [`sources/reference/CasarettDoull_Toxicology_textbook.pdf`](_shared/reference/CasarettDoull_Toxicology_textbook.pdf) | 195 (75) | General toxicology. Only 2 of those 75 pages also carry `oligonucleotide` or `antisense`: PDF p.1178 (prose on snake-venom nucleases, on a page that also tabulates hemostatically active venom components) and p.1467 (the alphabetical index). Not oligonucleotide coagulopathy content. Count is for the seven-term pattern above; [`./cross-cutting.md`](./cross-cutting.md), section 1.2 "Casarett & Doull", reports 143 for bare `coagul`. | none | 0 |

Both reference files are allocated to [`./cross-cutting.md`](./cross-cutting.md); so is the MMB volume, despite its filing under `sources/kidney/`.

## What the in-repo material says

All three passages are in Methods in Molecular Biology 2434, indexed per chapter at [`./cross-cutting.md`](./cross-cutting.md), section 1.4 "Methods in Molecular Biology 2434 — misfiling finding". Page references are PDF indices, with the printed book page verified from the page footer. Quotations restore the 2′ prime, which the PDF text layer renders as `20-`; nothing else inside quotation marks is altered.

**Ch.25 (Andersson) §3.1.2, PDF p.354 = book p.359**, headed "Sequence and Hybridization Independent Effects: Coagulation Time and Complement Activation", opens:

> A couple of toxicities that are dependent on plasma Cmax but independent of both hybridization and sequence can be observed at relative high doses of PS backbone ASOs. This includes prolongation of coagulation time and activation of the alternative complement system.

The section then develops the complement half only, closing that "Both these effects are driven by the plasma Cmax levels" and are transient. That sentence and that clause are the whole of the coagulation content: class-level, directional, naming no compound, dose or value. The complement half of the same section is owned by [`./complement-activation.md`](./complement-activation.md).

**Ch.1 (Gait and Agrawal), PDF p.23 = book p.9** carries the only compound-named coagulation observation in the repository's oligonucleotide-specific material: "the subcutaneous administration of GEM91 in humans caused flu-like symptoms, swelling of the draining lymph nodes, prolongation of activated partial thromboplastin time (aPTT), and thrombocytopenia [29]. … However, intravenous delivery had minimal effect on these parameters." No aPTT value and no dose is given, and GEM91 appears nowhere in `data/oligos.csv` (0 matches). The same sentence is the shared locus with [`./thrombocytopenia.md`](./thrombocytopenia.md). Its citation [29] — Agrawal S (1992), *Trends Biotechnol* 10(5):152–158, read verbatim from PDF p.38 — is not held in `sources/` and was not retrieved.

**Ch.1, PDF p.26 = book p.12** attributes the effect to chemistry: "dose-dependent activation of complement and prolongation of aPTT were found to be unwanted side effects of PS-ODNs", ascribed to "the poly-anionic nature of the PS linkage", with "significantly less side effects when PS-ORN or 2′-OMe-PS-ASO" were used. This is the passage that connects the endpoint to the present dataset, whose `backbone_chemistry` is `full_PS` for 45 of 65 oligos and `PS_PO_mix` for 15 more — but it supplies no per-compound value and changes nothing in the data.

## Not this endpoint

Three oligos act on the coagulation or complement cascades **by design**. Those targets are on-target pharmacology, not toxicity observations, and each compound's single row is a renal grade-0 `renal_safety` / `no_signal` clinical row from `source_id = WS`: `OLG028` fitusiran (`SERPINC1_antithrombin`, `MSR055`), `OLG036` donidalorsen (`KLKB1_prekallikrein`, `MSR067`), `OLG035` cemdisiran (`C5_complement`, `MSR066` — the false positive shared with [`./complement-activation.md`](./complement-activation.md)). All three grades are soft: each row carries `grade_provisional` in `notes`, and `MSR055` and `MSR067` are among the six absence claims `data/clinical_validation_2026-08.md:72-74` presumes suspect until the source is retrieved (only `MSR066` is checked and **CONFIRMED**, `:37`). The rows belong to the kidney endpoint, whose treatment of the `WS` tier and of that validation is in [`./kidney/kidney-nephrotoxicity.md`](./kidney/kidney-nephrotoxicity.md), section 6 "Known issues". Any automated allocation keyed on a bare `thrombin` grep will mis-file `OLG028` here.

## Known issues

- The file holding this endpoint's entire material is misfiled. The 416-page MMB 2434 volume sits in `sources/kidney/`, inside the tier `sources/SOURCES.md:195` describes as "strict-kidney primary sources & reviews", and its entry at `:200` reads "(book; contains the renal-tox-in-mice chapter, NBK584232)". Nothing in `sources/SOURCES.md` leads a reader to Ch.25; only this register does. Finding and recommendation at [`./cross-cutting.md`](./cross-cutting.md), section 1.4 "Methods in Molecular Biology 2434 — misfiling finding"; not acted on.
- `sources/SOURCES.md` keys sections to the two endpoints that have material — `KIDNEY-SPECIFIC` (`:28`) and `HEPATOTOX FALLBACK` (`:83`) — and files the rest by folder. Its `reference/` tier (`:207`) is described as "background reviews / textbooks / project docs (NOT per-row data)", the right shelf for material of this kind, but there is no bucket for an endpoint that was assessed and not extracted, so such a decision has no addressable entry.
- Verification scope: all hit counts and page references here come from the PDFs' text layers. Figure content was not examined.

## Not done, and why

| Not done | Cause |
|---|---|
| No rows, oligos or `source_id` | No in-repo document carries a per-compound coagulation value. The one substantive passage is a safety-assessment methods chapter writing at class level. |
| No scope decision recorded outside this file | `kidney/METHODOLOGY.md` and `kidney/SOURCES.md` contain 0 hits for the pattern above; the only hit in `../README.md` is the eight-endpoint list this reorganization added. This dossier **recommends** recording it as assessed and out of scope for Phase 2; that decision has not been taken or propagated. |
| No primary source acquired | `sources/SOURCES.md` names none. One weak lead sits inside a file already on disk (Crooke 2016, below), unretrieved and of unverified relevance. |

## Next step

1. Retrieve Crooke ST, Baker BF, Kwoh TJ, et al. (2016), "Integrated safety assessment of 2′-O-Methoxyethyl chimeric antisense oligonucleotides in NonHuman primates and healthy human volunteers", *Mol Ther* 24(10):1771–1782, doi 10.1038/mt.2016.136 — MMB Ch.25 reference [61], PDF p.361. It is the only lead the sweep above surfaced. Whether it reports per-compound coagulation times is **unverified**; the expectation rests on its title alone. Read individually from p.361, none of Ch.25 §3.1.2's ten citations [53]–[62] is titled as a coagulation study: [53] is drug-induced vascular injury, [54], [55] and [62] are complement mechanism, [56]–[60] are pharmacokinetics, [61] is the integrated safety assessment.
2. The MMB relocation and per-chapter index, which would make Ch.25 §3.1.2 citable from here, are owned and tracked at [`./cross-cutting.md`](./cross-cutting.md), section 1.4 "Methods in Molecular Biology 2434 — misfiling finding"; not restated as an action here.
3. Record the out-of-scope decision in `sources/SOURCES.md`, which currently has no place to put it.
4. Only if a source is ever acquired: add a coagulation-specific graded column with its own written rubric. Do not extract into `nephrotox_grade`.
