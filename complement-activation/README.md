# Complement activation — endpoint dossier

**Status:** `background-only` · **Register:** [`../README.md`](../README.md) · **Cross-cutting sources:** [`../_shared/README.md`](../_shared/README.md)

Complement activation is the fourth endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in the register, [`../README.md`](../README.md)); in oligonucleotide safety it is the classical phosphorothioate class effect, driven by peak plasma concentration rather than by sequence. Four endpoints in this repository carry data — kidney-toxicity (769 measurements), thrombocytopenia (1786), chronic-neurotoxicity (2393), hydrocephalus (147). This is not one of them: no dataset was built for it, no source was acquired for it, and its richest in-repo material still sits inside two multi-endpoint sources in `../_shared/sources/` held for other reasons. Four measurement rows in two of the populated datasets do name a complement analyte, as adjacent readouts of their own endpoints (§ "Complement elsewhere").

## Status

| | Value |
|---|---|
| Oligos | 0 |
| Measurement rows | 0 |
| Dedicated source PDFs | 0 |
| `source_id`s | 0 |
| Extraction status | not started; no primary source acquired |
| Graded column and rubric | none — the kidney rubric ([`../kidney-toxicity/schema.md`](../kidney-toxicity/schema.md), "`nephrotox_grade` rubric (0–3)") is renal and not transferable, and [`../_shared/README.md`](../_shared/README.md) § 4 shows the four existing grade columns are not comparable to each other either |

A regex sweep for `complement|C3a|C5a|CH50|anaphylat|CARPA` over every column of all four datasets returns: 0 hits in 23 × 769 kidney rows; 17 rows of 1786 in thrombocytopenia, 1 of them a `readout_name`; 4 rows of 2393 in chronic-neurotoxicity, 3 of them a `readout_name`; 1 row of 147 in hydrocephalus, a `notes` use of "complementarity".

## "Complement" elsewhere in this repository

Four rows now name a complement analyte, all of them adjacent readouts inside another endpoint's dataset rather than complement-activation records:

| Row | Dataset | Readout | Compound, model | Grade (host rubric) |
|---|---|---|---|---|
| `TMSR948` | thrombocytopenia | `platelet_bound_complement_C3d_C4d` | ISIS 405879, cynomolgus in vivo | `thrombocytopenia_grade` 3 |
| `CMS2155` | chronic-neurotoxicity | `complement_Bb_split_product` | nusinersen, cynomolgus single-dose IT | `neurotox_grade` 0 |
| `CMS2179` | chronic-neurotoxicity | `complement_Bb_split_product_CSF` | nusinersen, cynomolgus 14-week | `neurotox_grade` 0 |
| `CMS2201` | chronic-neurotoxicity | `complement_Bb_split_product_CSF` | nusinersen, cynomolgus 1-year | `neurotox_grade` 0 |

`TMSR948` records complement deposition on the platelet surface as a clearance mechanism and is explicitly distinguished in its own `notes` from fluid-phase alternative-pathway activation; the three nusinersen rows are all negatives (no drug-related Bb increase) graded on a CNS rubric. Four rows, two compounds, one route each: adjacent evidence, not a dataset.

The remaining string matches are false positives for the endpoint:

- **`C5_complement` is a drug target, not a finding.** `OLG035` in [`../kidney-toxicity/data/oligos.csv`](../kidney-toxicity/data/oligos.csv) is cemdisiran (`GalNAc_siRNA`, Alnylam, `max_phase = phase_2`, `indication = IgA_nephropathy_PNH`) and its `target_gene` is `C5_complement`. The drug *inhibits* complement C5. Its single measurement row, `MSR066`, is `study_type = clinical`, `readout_name = renal_safety`, `readout_value = no_signal`, `nephrotox_grade = 0`, `source_id = WS` — a renal row. `TOLG047` in thrombocytopenia is the same case (`target_gene = NA (binds complement component C5 protein)`).
- **"Reverse complement" is a sequence QC check.** `../kidney-toxicity/reconcile/METHODOLOGY-111row-lineage.md:93` and `:180` and `../_shared/scripts/fill_inn_sequences.py:16` use the term for guide/sense strand verification; `OLG035` carries `revcomp_verified_core21` in the 111-row lineage's `oligos.csv`, though not in the shipped 769-row one. `../kidney-toxicity/presentation/PRESENTATION.md:686` uses "complementing". Sixteen `../chronic-neurotoxicity/data/oligos.csv` notes use "complementary strand" for heteroduplex partners.

Any automated allocation keyed on a bare `complement` grep will mis-file all of these here.

## Sources allocated

`complement-activation/` holds no `sources/` directory: no PDF anywhere in the repository was acquired for this endpoint. A multi-endpoint book and a multi-endpoint review, both in `../_shared/sources/` and indexed in [`../_shared/README.md`](../_shared/README.md), carry its material; the book carries it in three separate chapters.

| File | Locus for this endpoint | `source_id` | Rows yielded |
|---|---|---|---|
| [`../_shared/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](../_shared/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) | Ch.1 (Gait and Agrawal), PDF pp.23, 24, 26 — GEM91 and WVEN-531, qualitative | none | 0 |
| (same volume) | Ch.25 (Andersson), §3.1.2 "Sequence and Hybridization Independent Effects: Coagulation Time and Complement Activation", PDF p.354 = book p.359 | none | 0 |
| (same volume) | Ch.26, PDF p.367 — drisapersen glomerulopathies attributed to chronic complement activation | none | 0 |
| [`../_shared/sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf`](../_shared/sources/Frazier2015_ASO_therapies_review_ToxPathol.pdf) | PDF pp.4, 6, 7, 9 | none | 0 |

MMB Ch.25 §3.1.2 opens, verbatim:

> A couple of toxicities that are dependent on plasma Cmax but independent of both hybridization and sequence can be observed at relative high doses of PS backbone ASOs. This includes prolongation of coagulation time and activation of the alternative complement system.

One section covers this endpoint and coagulopathy together, which is why [`../coagulopathy/README.md`](../coagulopathy/README.md), section "What the in-repo material says", cites the same locus. The passage names no compound and reports no value, and the exposure variable it turns on — plasma Cmax — is representable in the kidney `measurements.csv` only relatively, as `dose_or_conc_unit = fold_Cmax` (`../kidney-toxicity/schema.md:56`, "multiple of clinical Cmax"), used by `MSR022`, `MSR023` and `MSR024`; no field in any of the four schemas holds an absolute plasma Cmax.

MMB Ch.1 carries the volume's compound-named complement accounts, all qualitative: GEM91, whose bolus intravenous administration in non-human primates "led to severe hemodynamic changes due to activation of the alternative complement pathway [42]" (PDF p.23 = book p.9); WVEN-531, whose dosing "also led to transient increases in complement factors and C-reactive protein [65]" (PDF p.24); and the chemistry attribution at PDF p.26 = book p.12, "dose-dependent activation of complement and prolongation of aPTT were found to be unwanted side effects of PS-ODNs", which [`../coagulopathy/README.md`](../coagulopathy/README.md) already quotes for its aPTT half.

Frazier 2015 is the fullest mechanistic account in the repository and equally unextractable. PDF p.4 attributes ASO-mediated inflammation in monkeys to "activation of the alternative pathway of complement", gives the mechanism (ASO interaction with Factor H, disrupting Factor H's interaction with C3 convertase), and names the assay that would generate this endpoint's data — "in vitro complement fixation assays" — as routine developer screening. PDF p.6 records complement fragments along glomerular vascular tufts by anti-C3c immunofluorescence. PDF p.7 is the clinical bridge: "the potential for clinical glomerular effects from ASO-mediated immunomodulation and especially complement-mediated damage (as in monkey) remains a relevant clinical concern", with mipomersen and drisapersen named as the reported human glomerulonephritis examples. All of it is class-level or per-study, and the file carries no numbered tables.

Four further acquired PDFs mention complement in the endpoint's sense and correctly produced no complement row: [`Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf`](../kidney-toxicity/sources/Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf) (`source_id = REV`; p.10, PS ASOs "can activate the alternate complement system"), [`Frazier2022_kidney_effects_review_ToxPathol.pdf`](../kidney-toxicity/sources/Frazier2022_kidney_effects_review_ToxPathol.pdf) (its p.2 complement passages are background on peptide and antibody hypersensitivity, not on ASOs; its ASO sentence is at p.5, read below), and both nephrotoxicity-assay patents, which name C3a and C5a only inside "in some embodiments" claim-scope prose, publish no complement table, and frame the panel as predicting "in vivo immunotoxicity of the drug substance" (`US11105794` p.21) — that passage belongs to [`../immunotoxicity/README.md`](../immunotoxicity/README.md), which does not yet carry it. Two more PDFs contain the string and carry nothing for this endpoint: `CasarettDoull_Toxicology_textbook.pdf` (general toxicology, no oligonucleotide complement content — [`../_shared/README.md`](../_shared/README.md) section 1.2 "Casarett & Doull") and the challenge brief, whose single p.1 occurrence is the endpoint's own name in the scope list. Across the 18 PDFs of the original kidney-lineage source set, the only remaining hits are two `complementary` in Hagedorn 2013, two in Moisan 2017 and one `complemented` in Sandelius 2020 — none in the immune sense. The 23 CNS PDFs later added at `../_shared/sources/cns/` have not been swept for this endpoint; one of them, `FDA_NDA209531_nusinersen_PharmacologyReview.pdf`, is the source (`source_id = R4`) behind three of the four complement rows above.

## Where it touches the kidney data

Frazier 2015, Frazier 2022 and MMB Ch.26 all attribute the glomerular — as opposed to tubular — arm of ASO renal toxicity to complement activation and to greater monkey sensitivity: Frazier 2015 PDF pp.4 and 6, where ASO vasculitis and glomerulonephritis "share a similar pathogenesis in monkeys, related to complement activation and initial injury to the endothelium"; Frazier 2022 PDF p.5, where monkey glomerulopathy and mesangial hyperplasia are "related to monkey sensitivity to complement and enhanced complement responsiveness"; and MMB Ch.26 PDF p.367, where the drisapersen glomerulopathies are "linked to the chronic complement activation and inflammatory effects of the ASO" and over-predicted "since humans are less susceptible to these effects". These are not three independent attestations: all three cite one primary study (Frazier et al. 2014) and two share its author. The kidney dataset holds five rows carrying glomerular lesion names (`MSR001`, `MSR004`, `MSR013`, `MSR015`, `MSR029`) and cannot separate them, because `tissue = glomerulus` is declared at `../kidney-toxicity/schema.md:53` and used by zero of its 769 rows; that defect belongs to [`../kidney-toxicity/README.md`](../kidney-toxicity/README.md) § "Known issues and open work". Complement activation is the mechanism that makes the split worth making. No row may be created from any of this.

## Known issues

- The brief's eight-endpoint list reaches the repo only as a PDF. `../kidney-toxicity/METHODOLOGY.md:22` names kidney as "a named OligoTox endpoint of interest" without reproducing the list, so a reader of that lane alone could not tell that seven other endpoints were named. The register [`../README.md`](../README.md) now quotes the sentence and states which four of the eight are populated.
- `../kidney-toxicity/SOURCES.md` keys sections only to the two endpoints that lane had material for — `KIDNEY-SPECIFIC` (`:28`) and `HEPATOTOX FALLBACK` (`:83`); other background is filed by folder. The same holds of `../thrombocytopenia/SOURCES.md` and `../chronic-neurotoxicity/SOURCES-CNS.md`: each registry is scoped to its own endpoint, so there is nowhere to record an endpoint that was assessed and not extracted.
- The MMB volume's misfiling is **resolved** — it now sits at `../_shared/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`, under no endpoint. What remains open is per-chapter indexing: it is registered once as a single kidney-bucket line, so no registry entry leads a reader to Ch.1, Ch.25 or Ch.26 — only this dossier and [`../_shared/README.md`](../_shared/README.md) § 1.4 "Methods in Molecular Biology 2434 — misfiling resolved" do.

## Not done, and why

| Not done | Cause |
|---|---|
| No rows, oligos or `source_id` | No in-repo document carries a per-compound complement *value*; MMB Ch.1's two compound-named accounts (GEM91, WVEN-531) are qualitative, and the rest is class-level narrative. |
| No scope decision recorded outside this file | No `METHODOLOGY.md` or source registry in any of the four populated endpoint folders carries a statement about this endpoint. This dossier **recommends** recording it as assessed and out of scope for Phase 2; that decision has not been taken or propagated. |
| Extraction would need schema work before rows | A `complement_grade` column with its own written rubric, and an absolute plasma-Cmax field: exposure is representable today only relative to Cmax, as `fold_Cmax` (`../kidney-toxicity/schema.md:56`, used by `MSR022`–`MSR024`). The effect is also sequence- and hybridization-independent, so the sequence predictors in any `oligos.csv` do not bear on it; `backbone_chemistry` is the one that does. |

## Next step

1. Acquire Galbraith WM, Hobson WC, Giclas PC, Schechter PJ, Agrawal S (1994), "Complement activation and hemodynamic changes following intravenous administration of phosphorothioate oligonucleotides in the monkey", *Antisense Res Dev* 4(3):201–206 — MMB Ch.1 reference [42], PDF p.39. It is the study behind Ch.1's GEM91 sentence, the repository's one compound-named in-vivo complement account.
2. Then the two in-vivo monkey studies named in the Frazier 2015 reference list (PDF p.11): Henry et al. (2002), "Complement activation is responsible for acute toxicities in rhesus monkeys treated with a phosphorothioate oligodeoxynucleotide", *Int Immunopharmacol* 2:1657–66 — the study the p.4 attribution rests on — and Henry et al. (1997), "Activation of the alternative pathway of complement by a phosphorothioate oligonucleotide: Potential mechanism of action", *J Pharmacol Exp Ther* 281:810–6.
3. Then the two mechanism papers Ch.25 cites, both listed at MMB PDF p.361: Henry et al. (2014), *Nucl Acid Ther* 24(5):326–335 (ref [54], "in monkey and human serum"), and Shen et al. (2014), *J Pharmacol Exp Ther* 351(3):709–717 (ref [55], the species difference).
4. Index the MMB volume per chapter — the relocation to `../_shared/sources/` is done, the indexing is not ([`../_shared/README.md`](../_shared/README.md) § 1.4) — so Ch.25 §3.1.2 becomes citable from a registry rather than only from here and [`../coagulopathy/README.md`](../coagulopathy/README.md).
5. Read `../_shared/sources/cns/FDA_NDA209531_nusinersen_PharmacologyReview.pdf` for the complement analysis behind `CMS2155`, `CMS2179` and `CMS2201`. Those rows were extracted for a CNS endpoint; the review's complement sections have not been read for this one.
6. Only after 1–5, write the rubric and add the Cmax field. Do not extract complement rows into any existing grade column.
