# Complement activation — endpoint dossier

**Status:** `background-only` · **Register:** [`./README.md`](./README.md) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Complement activation is the fourth endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md)); in oligonucleotide safety it is the classical phosphorothioate class effect, driven by peak plasma concentration rather than by sequence. This project curated kidney toxicity only. Nothing was extracted for this endpoint, no source was acquired for it, and its richest in-repo material sits inside two multi-endpoint sources held for other reasons; further acquired PDFs mention it only in passing (§ Sources allocated).

## Status

| | Value |
|---|---|
| Oligos | 0 |
| Measurement rows | 0 |
| Dedicated source PDFs | 0 |
| `source_id`s | 0 |
| Extraction status | not started; no primary source acquired |
| Graded column and rubric | none — `nephrotox_grade`'s rubric (`schema.md`, "`nephrotox_grade` rubric (0–3)") is renal and not transferable |

A regex sweep for `complement|C3a|C5a|CH50|anaphylat|CARPA` over all 23 columns × 111 rows of [`data/measurements.csv`](../data/measurements.csv) returns 0 hits.

## "Complement" elsewhere in this repository is not this endpoint

This has to be stated first, because in the repository's own markdown, Python and CSV files every occurrence of the string outside `toxicity/` is a false positive for the endpoint. The acquired PDFs are the opposite case and are handled in § Sources allocated.

- **`C5_complement` is a drug target, not a finding.** `OLG035` in [`data/oligos.csv`](../data/oligos.csv) is cemdisiran (`GalNAc_siRNA`, Alnylam, `max_phase = phase_2`, `indication = IgA_nephropathy_PNH`) and its `target_gene` is `C5_complement`. The drug *inhibits* complement C5. Its single measurement row, `MSR066`, is `study_type = clinical`, `readout_name = renal_safety`, `readout_value = no_signal`, `nephrotox_grade = 0`, `source_id = WS` — a renal row.
- **"Reverse complement" is a sequence QC check.** `METHODOLOGY.md:93` and `METHODOLOGY.md:180` and `scripts/fill_inn_sequences.py:16` use the term for guide/sense strand verification, and `OLG035`'s own `notes` field carries `revcomp_verified_core21`. `PRESENTATION.md:686` uses "complementing".

Those four markdown/Python loci, together with the `OLG035` row of `oligos.csv` and the `MSR066` row of the generated `data/oligotox_kidney_merged.csv`, are every `complement` hit in the curated corpus — and not one of them is a complement-activation finding. Any automated allocation keyed on a bare `complement` grep will mis-file all of them here.

## Sources allocated

No PDF in `sources/` was acquired for this endpoint. A multi-endpoint book and a multi-endpoint review, both allocated to [`./cross-cutting.md`](./cross-cutting.md), carry its material; the book carries it in three separate chapters.

| File | Locus for this endpoint | `source_id` | Rows yielded |
|---|---|---|---|
| [`sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](../sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) | Ch.1 (Gait and Agrawal), PDF pp.23, 24, 26 — GEM91 and WVEN-531, qualitative | none | 0 |
| (same volume) | Ch.25 (Andersson), §3.1.2 "Sequence and Hybridization Independent Effects: Coagulation Time and Complement Activation", PDF p.354 = book p.359 | none | 0 |
| (same volume) | Ch.26, PDF p.367 — drisapersen glomerulopathies attributed to chronic complement activation | none | 0 |
| [`sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf`](../sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf) | PDF pp.4, 6, 7, 9 | none | 0 |

MMB Ch.25 §3.1.2 opens, verbatim:

> A couple of toxicities that are dependent on plasma Cmax but independent of both hybridization and sequence can be observed at relative high doses of PS backbone ASOs. This includes prolongation of coagulation time and activation of the alternative complement system.

One section covers this endpoint and coagulopathy together, which is why [`./coagulopathy.md`](./coagulopathy.md), section "What the in-repo material says", cites the same locus. The passage names no compound and reports no value, and the exposure variable it turns on — plasma Cmax — is representable in `measurements.csv` only relatively, as `dose_or_conc_unit = fold_Cmax` (`schema.md:52`, "multiple of clinical Cmax"), used by `MSR022`, `MSR023` and `MSR024`; no field holds an absolute plasma Cmax.

MMB Ch.1 carries the volume's compound-named complement accounts, all qualitative: GEM91, whose bolus intravenous administration in non-human primates "led to severe hemodynamic changes due to activation of the alternative complement pathway [42]" (PDF p.23 = book p.9); WVEN-531, whose dosing "also led to transient increases in complement factors and C-reactive protein [65]" (PDF p.24); and the chemistry attribution at PDF p.26 = book p.12, "dose-dependent activation of complement and prolongation of aPTT were found to be unwanted side effects of PS-ODNs", which [`./coagulopathy.md`](./coagulopathy.md) already quotes for its aPTT half.

Frazier 2015 is the fullest mechanistic account in the repository and equally unextractable. PDF p.4 attributes ASO-mediated inflammation in monkeys to "activation of the alternative pathway of complement", gives the mechanism (ASO interaction with Factor H, disrupting Factor H's interaction with C3 convertase), and names the assay that would generate this endpoint's data — "in vitro complement fixation assays" — as routine developer screening. PDF p.6 records complement fragments along glomerular vascular tufts by anti-C3c immunofluorescence. PDF p.7 is the clinical bridge: "the potential for clinical glomerular effects from ASO-mediated immunomodulation and especially complement-mediated damage (as in monkey) remains a relevant clinical concern", with mipomersen and drisapersen named as the reported human glomerulonephritis examples. All of it is class-level or per-study, and the file carries no numbered tables.

Four further acquired PDFs mention complement in the endpoint's sense and correctly produced no complement row: [`Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf`](../sources/kidney/Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf) (`source_id = REV`; p.10, PS ASOs "can activate the alternate complement system"), [`Frazier2022_kidney_effects_review_ToxPathol.pdf`](../sources/kidney/Frazier2022_kidney_effects_review_ToxPathol.pdf) (its p.2 complement passages are background on peptide and antibody hypersensitivity, not on ASOs; its ASO sentence is at p.5, read below), and both nephrotoxicity-assay patents, which name C3a and C5a only inside "in some embodiments" claim-scope prose, publish no complement table, and frame the panel as predicting "in vivo immunotoxicity of the drug substance" (`US11105794` p.21) — that passage belongs to [`./immunotoxicity.md`](./immunotoxicity.md), which does not yet carry it. Two more PDFs contain the string and carry nothing for this endpoint: `CasarettDoull_Toxicology_textbook.pdf` (general toxicology, no oligonucleotide complement content — [`./cross-cutting.md`](./cross-cutting.md) section 1.2 "Casarett & Doull") and the challenge brief, whose single p.1 occurrence is the endpoint's own name in the scope list. The only remaining hits anywhere in `sources/` are two `complementary` in Hagedorn 2013, two in Moisan 2017 and one `complemented` in Sandelius 2020 — none in the immune sense.

## Where it touches the kidney data

Frazier 2015, Frazier 2022 and MMB Ch.26 all attribute the glomerular — as opposed to tubular — arm of ASO renal toxicity to complement activation and to greater monkey sensitivity: Frazier 2015 PDF pp.4 and 6, where ASO vasculitis and glomerulonephritis "share a similar pathogenesis in monkeys, related to complement activation and initial injury to the endothelium"; Frazier 2022 PDF p.5, where monkey glomerulopathy and mesangial hyperplasia are "related to monkey sensitivity to complement and enhanced complement responsiveness"; and MMB Ch.26 PDF p.367, where the drisapersen glomerulopathies are "linked to the chronic complement activation and inflammatory effects of the ASO" and over-predicted "since humans are less susceptible to these effects". These are not three independent attestations: all three cite one primary study (Frazier et al. 2014) and two share its author. The repository holds five rows carrying glomerular lesion names and cannot separate them, because `tissue = glomerulus` is declared at `schema.md:49` and used by zero rows; that defect and its fix are owned by [`./kidney-nephrotoxicity.md`](./kidney-nephrotoxicity.md), section 6 "Known issues" item 5 and section 8 "Next step" item 6. Complement activation is the mechanism that makes the split worth making. No row may be created from any of this.

## Known issues

- The brief's eight-endpoint list reaches the repo only as a PDF. `METHODOLOGY.md:22` names kidney as "a named OligoTox endpoint of interest" without reproducing the list, so a reader could not tell that seven other endpoints were named. [`./README.md`](./README.md) now quotes the sentence.
- `sources/SOURCES.md` keys sections only to the two endpoints that have material — `KIDNEY-SPECIFIC` (`:28`) and `HEPATOTOX FALLBACK` (`:83`); other background is filed by folder, with `reference/` described in its `LOCAL SOURCE FILES` tree as "background reviews / textbooks / project docs (NOT per-row data)". There is nowhere in the registry to record an endpoint that was assessed and not extracted.
- The file holding most of this endpoint's in-repo material is misfiled. The 416-page MMB 2434 volume sits in `sources/kidney/` and is registered there as "(book; contains the renal-tox-in-mice chapter, NBK584232)" (`sources/SOURCES.md:200`), so nothing in `sources/SOURCES.md` leads a reader to Ch.1, Ch.25 or Ch.26 — only this register does. Finding and recommendation in [`./cross-cutting.md`](./cross-cutting.md), section 1.4 "Methods in Molecular Biology 2434 — misfiling finding"; not yet acted on.

## Not done, and why

| Not done | Cause |
|---|---|
| No rows, oligos or `source_id` | No in-repo document carries a per-compound complement *value*; MMB Ch.1's two compound-named accounts (GEM91, WVEN-531) are qualitative, and the rest is class-level narrative. |
| No scope decision recorded outside this file | `README.md`, `METHODOLOGY.md` and `sources/SOURCES.md` carry no statement about this endpoint. This dossier **recommends** recording it as assessed and out of scope for Phase 2; that decision has not been taken or propagated. |
| Extraction would need schema work before rows | A `complement_grade` column with its own written rubric, and an absolute plasma-Cmax field: exposure is representable today only relative to Cmax, as `fold_Cmax` (`schema.md:52`, used by `MSR022`–`MSR024`). The effect is also sequence- and hybridization-independent, so the sequence predictors in `oligos.csv` do not bear on it; `backbone_chemistry` is the one that does. |

## Next step

1. Acquire Galbraith WM, Hobson WC, Giclas PC, Schechter PJ, Agrawal S (1994), "Complement activation and hemodynamic changes following intravenous administration of phosphorothioate oligonucleotides in the monkey", *Antisense Res Dev* 4(3):201–206 — MMB Ch.1 reference [42], PDF p.39. It is the study behind Ch.1's GEM91 sentence, the repository's one compound-named in-vivo complement account.
2. Then the two in-vivo monkey studies named in the Frazier 2015 reference list (PDF p.11): Henry et al. (2002), "Complement activation is responsible for acute toxicities in rhesus monkeys treated with a phosphorothioate oligodeoxynucleotide", *Int Immunopharmacol* 2:1657–66 — the study the p.4 attribution rests on — and Henry et al. (1997), "Activation of the alternative pathway of complement by a phosphorothioate oligonucleotide: Potential mechanism of action", *J Pharmacol Exp Ther* 281:810–6.
3. Then the two mechanism papers Ch.25 cites, both listed at MMB PDF p.361: Henry et al. (2014), *Nucl Acid Ther* 24(5):326–335 (ref [54], "in monkey and human serum"), and Shen et al. (2014), *J Pharmacol Exp Ther* 351(3):709–717 (ref [55], the species difference).
4. Move the MMB volume out of `sources/kidney/` and index it per chapter ([`./cross-cutting.md`](./cross-cutting.md), section 1.4 "Methods in Molecular Biology 2434 — misfiling finding"), so Ch.25 §3.1.2 is citable from here and from [`./coagulopathy.md`](./coagulopathy.md).
5. Only after 1–4, write the rubric and add the Cmax field. Do not extract complement rows into `nephrotox_grade`.
