# Coagulopathy — endpoint dossier

**Status:** `background-only` · **Register:** [`../README.md`](../README.md) · **Cross-cutting sources:** [`../_shared/README.md`](../_shared/README.md)

Coagulopathy is the fifth endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in the register, [`../README.md`](../README.md)); in oligonucleotide safety it is, per the in-repo characterisation quoted below (MMB 2434 Ch.25 §3.1.2, PDF p.354), prolongation of coagulation time at high plasma Cmax of phosphorothioate-backbone ASOs. Four endpoints in this repository carry data — kidney-toxicity (769 measurements), thrombocytopenia (1786), chronic-neurotoxicity (2393), hydrocephalus (147). This is not one of them: no dataset was built for it and no source was acquired for it. Its narrative footprint is still three passages inside one multi-endpoint book in `../_shared/sources/` held for a different reason — but the thrombocytopenia dataset, built on a branch this dossier could not see, now carries **49 coagulation-readout rows** (§ "Coagulation rows now in the repository").

## Status

| | Value |
|---|---|
| Oligos | 0 |
| Measurement rows | 0 |
| Dedicated source PDFs | 0 |
| `source_id`s | 0 |
| Extraction status | not started; no primary source acquired |
| Graded column and rubric | none of this endpoint's own — the 49 rows below are graded on `thrombocytopenia_grade`; the kidney rubric ([`../kidney-toxicity/schema.md`](../kidney-toxicity/schema.md), "`nephrotox_grade` rubric (0–3)") is renal and not transferable |

The sweep used throughout this file is `coagul|aPTT|prothrombin|clotting|anticoagul|fibrinogen|thromboplastin` — laboratory clotting descriptors only. It deliberately omits `thrombin`, which matches on-target pharmacology (see "Not this endpoint"), and `bleeding|h[ae]morrhag`, the two commonest clinical descriptors of the endpoint; adding the latter pair adds exactly one file to the table below — 2 hits on PDF p.7 of [`../_shared/sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf`](../_shared/sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf), both describing thrombocytopenic bleeding — alongside 1 further hit in the MMB volume and 109 in the general-toxicology textbook, and no per-compound coagulation value in any of those PDFs.

Over all 23 columns × 769 rows of [`../kidney-toxicity/data/measurements.csv`](../kidney-toxicity/data/measurements.csv) it returns 0 hits, and over all 21 columns × 71 rows of [`../kidney-toxicity/data/oligos.csv`](../kidney-toxicity/data/oligos.csv) also 0; the nearest near-miss is `OLG028`'s `target_gene` `SERPINC1_antithrombin`, which only a bare `thrombin` grep catches. The reason nothing is attributable in the kidney lane is not the column list — `readout_name` is a free string, and `is_kidney_specific` exists precisely to flag non-kidney rows — but the scope: `is_kidney_specific` is `TRUE` on all 769 rows, with no `FALSE` row in the table.

## Coagulation rows now in the repository

`../thrombocytopenia/data/measurements.csv` carries **49 rows with `readout_category = coagulation`**, over 8 oligos: 40 clinical (human) and 9 animal (8 monkey, 1 rat). Every one is flagged `is_platelet_specific = FALSE` — recorded, in that lane's own words, as adjacent haematology context beside a platelet series. They grade 0 on 47 rows and 1 on 2, on the `thrombocytopenia_grade` rubric, which measures platelet counts, not clotting.

| Readout family | Rows | Where |
|---|---:|---|
| `prothrombin_time_gt1.2xULN_incidence` | 15 | 13 from Crooke 2016 (`10.1038/mt.2016.136`), monkey and human incidence percentages on `TOLG020`, a pooled 12-ASO panel; 2 from `PMC6386089` on the class pool `TOLG059` |
| `abnormal_APTT_incidence_gt1.4` / `_gt2.5` / `abnormal_PT_incidence_gt1.2` / `APTT_gt1.4xULN_incidence` | 26 | 24 from `CROOKE2017` on the class pool `TOLG014`; 2 from `PMC6386089` on `TOLG059` |
| Per-compound coagulation readouts | 8 | Six sources, five of them regulatory reviews: imetelstat (aPTT and PT prolonged incidence, 26% and 34%, human), inotersen (aPTT/INR/PT; PT prolonged 0%), ISIS 416858 (`factor_XI_activity` 0.2 U/mL), mipomersen (rat `APTT` 26.20 s; monkey PT/aPTT/fibrinogen), volanesorsen (monkey aPTT increased) |

This matters for the dossier's own reasoning below. **Next step 1 asked for Crooke 2016 and called it unverified whether that paper reports coagulation times: it does, and it has already been retrieved** — 13 of its rows are prothrombin-time incidences. It reports them for a pooled 12-ASO panel, not per compound, so the "no per-compound coagulation value" finding survives for that source; the eight per-compound rows in the last line above come from six sources and do overturn it as a claim about the repository. What does not exist is a coagulopathy dataset: 49 rows on a platelet rubric, deliberately flagged non-specific by the lane that collected them, are not one.

## Sources allocated

`coagulopathy/` holds no `sources/` directory and no PDF anywhere was acquired for this endpoint. The sweep over the 18 PDFs of the original kidney-lineage source set returns hits in three files; the other 15 return zero. The 23 CNS PDFs at `../_shared/sources/cns/` and the sources behind the 49 rows above were not part of that sweep.

| File | Hits (pages) | Bearing on this endpoint | `source_id` | Rows |
|---|---:|---|---|---:|
| [`../_shared/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](../_shared/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) | 7 (4) | The only real material — three passages, below. The remaining page, PDF p.111, is a chapter reference list citing coagulation factors as *therapeutic targets* for splicing rescue. | none | 0 |
| [`../_shared/sources/OligoTox_challenge_brief.pdf`](../_shared/sources/OligoTox_challenge_brief.pdf) | 1 (1) | The word "coagulopathy" in the page-1 endpoint list. Scope authority, not evidence. | none | 0 |
| [`../_shared/sources/CasarettDoull_Toxicology_textbook.pdf`](../_shared/sources/CasarettDoull_Toxicology_textbook.pdf) | 195 (75) | General toxicology. Only 2 of those 75 pages also carry `oligonucleotide` or `antisense`: PDF p.1178 (prose on snake-venom nucleases, on a page that also tabulates hemostatically active venom components) and p.1467 (the alphabetical index). Not oligonucleotide coagulopathy content. Count is for the seven-term pattern above; [`../_shared/README.md`](../_shared/README.md), section 1.2 "Casarett & Doull", reports 143 for bare `coagul`. | none | 0 |

All three files now sit in `../_shared/sources/` and are indexed in [`../_shared/README.md`](../_shared/README.md); the MMB volume's move out of the kidney bucket is the resolved half of § 1.4 there.

## What the in-repo material says

All three passages are in Methods in Molecular Biology 2434, indexed per chapter at [`../_shared/README.md`](../_shared/README.md), section 1.4 "Methods in Molecular Biology 2434 — misfiling resolved". Page references are PDF indices, with the printed book page verified from the page footer. Quotations restore the 2′ prime, which the PDF text layer renders as `20-`; nothing else inside quotation marks is altered.

**Ch.25 (Andersson) §3.1.2, PDF p.354 = book p.359**, headed "Sequence and Hybridization Independent Effects: Coagulation Time and Complement Activation", opens:

> A couple of toxicities that are dependent on plasma Cmax but independent of both hybridization and sequence can be observed at relative high doses of PS backbone ASOs. This includes prolongation of coagulation time and activation of the alternative complement system.

The section then develops the complement half only, closing that "Both these effects are driven by the plasma Cmax levels" and are transient. That sentence and that clause are the whole of the coagulation content: class-level, directional, naming no compound, dose or value. The complement half of the same section is owned by [`../complement-activation/README.md`](../complement-activation/README.md).

**Ch.1 (Gait and Agrawal), PDF p.23 = book p.9** carries the only compound-named coagulation observation in the repository's oligonucleotide-specific material: "the subcutaneous administration of GEM91 in humans caused flu-like symptoms, swelling of the draining lymph nodes, prolongation of activated partial thromboplastin time (aPTT), and thrombocytopenia [29]. … However, intravenous delivery had minimal effect on these parameters." No aPTT value and no dose is given, and GEM91 appears in none of the four `oligos.csv` files (0 matches). The same sentence is the shared locus with [`../thrombocytopenia/README.md`](../thrombocytopenia/README.md). Its citation [29] — Agrawal S (1992), *Trends Biotechnol* 10(5):152–158, read verbatim from PDF p.38 — is not held anywhere in the repository and was not retrieved.

**Ch.1, PDF p.26 = book p.12** attributes the effect to chemistry: "dose-dependent activation of complement and prolongation of aPTT were found to be unwanted side effects of PS-ODNs", ascribed to "the poly-anionic nature of the PS linkage", with "significantly less side effects when PS-ORN or 2′-OMe-PS-ASO" were used. This is the passage that connects the endpoint to the datasets: the kidney set's `backbone_chemistry` is `full_PS` for 51 of 71 oligos and `PS_PO_mix` for 15 more, and every one of the 49 coagulation rows above sits on a PS-backbone compound or class pool. The passage still supplies no per-compound value of its own.

## Not this endpoint

Three oligos act on the coagulation or complement cascades **by design**. Those targets are on-target pharmacology, not toxicity observations, and each compound's single row is a renal grade-0 `renal_safety` / `no_signal` clinical row from `source_id = WS`: `OLG028` fitusiran (`SERPINC1_antithrombin`, `MSR055`), `OLG036` donidalorsen (`KLKB1_prekallikrein`, `MSR067`), `OLG035` cemdisiran (`C5_complement`, `MSR066` — the false positive shared with [`../complement-activation/README.md`](../complement-activation/README.md)). All three grades are soft: each row carries `grade_provisional` in `notes`, and `MSR055` and `MSR067` are among the six absence claims `../kidney-toxicity/data/clinical_validation_2026-08.md:72-74` presumes suspect until the source is retrieved (only `MSR066` is checked and **CONFIRMED**, `:37`). The rows belong to the kidney endpoint, whose treatment of the `WS` tier and of that validation is in [`../kidney-toxicity/README.md`](../kidney-toxicity/README.md) § "Known issues and open work". Any automated allocation keyed on a bare `thrombin` grep will mis-file `OLG028` here.

## Known issues

- The MMB volume's misfiling is **resolved** — it now sits at `../_shared/sources/`, under no endpoint. What remains is that `../kidney-toxicity/SOURCES.md` still registers it once as a kidney-bucket line reading "(book; contains the renal-tox-in-mice chapter, NBK584232)", so no registry entry leads a reader to Ch.25; only this dossier and [`../_shared/README.md`](../_shared/README.md) § 1.4 "Methods in Molecular Biology 2434 — misfiling resolved" do.
- `../kidney-toxicity/SOURCES.md` keys sections to the two endpoints that lane had material for — `KIDNEY-SPECIFIC` (`:28`) and `HEPATOTOX FALLBACK` (`:83`) — and files the rest by folder; its `reference/` tier (`:203`) is described as "background reviews / textbooks / project docs (NOT per-row data)". The thrombocytopenia and CNS registries are likewise scoped to their own endpoints. None has a bucket for an endpoint assessed and not extracted, so such a decision has no addressable entry.
- The 49 rows in § "Coagulation rows now in the repository" are discoverable only by reading another endpoint's data. Nothing in `../thrombocytopenia/` names coagulopathy as an endpoint, and nothing here linked to them until this revision.
- Verification scope: all hit counts and page references here come from the PDFs' text layers. Figure content was not examined.

## Not done, and why

| Not done | Cause |
|---|---|
| No rows, oligos or `source_id` **of this endpoint's own** | The three MMB passages write at class level. The 49 coagulation rows that do exist were curated as thrombocytopenia context, on that endpoint's schema and rubric, and cannot be relabelled without a rubric this endpoint does not have. |
| No scope decision recorded outside this file | `../kidney-toxicity/METHODOLOGY.md` and `../_shared/sources/SOURCES-kidney-legacy.md` contain 0 hits for the pattern above; the only hit in `../README.md` is the eight-endpoint list this reorganization added. This dossier **recommends** recording it as assessed and out of scope for Phase 2; that decision has not been taken or propagated. |
| No primary source acquired *for this endpoint* | No registry names one. The lead this dossier named — Crooke 2016 — was retrieved by the thrombocytopenia lane instead, which is why 13 of its coagulation rows are in the repository under `source_id = workflow:10.1038/mt.2016.136`. |

## Next step

1. ~~Retrieve Crooke ST, Baker BF, Kwoh TJ, et al. (2016), "Integrated safety assessment of 2′-O-Methoxyethyl chimeric antisense oligonucleotides in NonHuman primates and healthy human volunteers", *Mol Ther* 24(10):1771–1782, doi 10.1038/mt.2016.136 — MMB Ch.25 reference [61], PDF p.361.~~ **Done, by another lane.** It does report coagulation times, as pooled-panel prothrombin-time incidences; 13 rows. The reference-list reading behind this step still stands: read individually from MMB PDF p.361, none of Ch.25 §3.1.2's ten citations [53]–[62] is titled as a coagulation study — [53] is drug-induced vascular injury, [54], [55] and [62] are complement mechanism, [56]–[60] are pharmacokinetics, [61] is the integrated safety assessment.
2. Read `../thrombocytopenia/SOURCES.md` for the six sources behind the eight per-compound rows, which are regulatory reviews this dossier never assessed. They, not new acquisition, are the nearest thing to a starting corpus.
3. Index MMB per chapter, so Ch.25 §3.1.2 is citable from a registry rather than only from here; owned at [`../_shared/README.md`](../_shared/README.md) § 1.4, and not restated as an action here.
4. Record the out-of-scope decision — or, given the 49 rows, a decision to build this endpoint from them — in the register [`../README.md`](../README.md), which is the only file scoped to say it.
5. Before any row is claimed for this endpoint: a coagulation-specific graded column with its own written rubric. Do not reuse `thrombocytopenia_grade` or `nephrotox_grade`.
