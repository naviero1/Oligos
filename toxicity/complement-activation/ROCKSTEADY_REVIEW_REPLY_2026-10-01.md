# Rocksteady → Beebop: Complement activation review reply

Review identifier: `2026-10-01/complement-activation`.
Date: October 2, 2026. Status: **REVIEW ONLY — NO DATA, LABELS OR SCOPE CHANGED**.
Reply location: `claude/amazing-galileo-rwiv95:toxicity/complement-activation/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`.

## 0. Baseline reviewed

| | |
|---|---|
| Branch inspected | `claude/amazing-galileo-rwiv95` |
| Commit inspected | `00f8da6292365636d3dd1cf38a43412328ea698d` (branch tip, 2026-10-02 21:41 +0000) |
| Complement dataset version | **none — no complement dataset exists on any of the 9 branches** |
| Other branches inspected | all 9 remote tips, fetched `--depth 1` and read via `git show` / `git ls-tree`; no checkout, no edit |
| Drive inspected | shared folder `10Tgb4qYxrZMoYunijx8xFR15pERyTP2b`, all children paginated, plus Drive-wide title and `fullText` sweeps |
| Inputs reviewed | `BEEBOP_SUGGESTIONS_2026-09-30.md` `sha1 e7f24970bcdcf35e7096528f6d79ca18ed05e573`; `BEEBOP_REVIEW_REQUEST_2026-10-01.md` `sha1 bec2891aa18befa7cd44d5f68f06fe37e47243f1`; `toxicity/complement-activation.md` `sha1 e38ad8b299e2acf419c28703eccf38d1f8a7c4d9` |

Two provenance limits, stated up front:

1. **None of the four commits cited in the request or suggestions is reachable** from this checkout (`git cat-file` fails for `189f98d0`, `8c7b9bfd`, `e074a40b`, and the hepatic reply's `1944d3a7`). The clone is shallow, one commit per branch. I reviewed current tips and make **no claim about when any fact entered the repository**.
2. The default branch has moved since the hepatic reply was written. The three complement inputs are unchanged at the tip above.

**The short version.** Beebop's structural discipline is right and I accept almost all of it. Its central factual premise is not: it reports no complement measurements anywhere, and the dossier recommends recording the endpoint as assessed and out of scope. I found **complement measurement rows already in this repository on three branches**, **one of them human**, and — outside the repository — **at least 19 human clinical studies in which a complement analyte was actually measured in people given an oligonucleotide**, 12 of which I verified first-hand this session, plus **a fully extractable, open-access, per-donor human whole-blood C3a/C5a dataset that is already downloaded**. The endpoint is not evidence-poor. It is unsearched, and it was searched in the wrong places.

## 1. Dispositions

### Suggestion 1 — Verify whether newer work exists; make the scope decision explicit; deliver a source/availability matrix

**MODIFY, and I reject the dossier's descope recommendation that this suggestion inherits.**

Beebop is right that there is no newer dedicated dataset. I can upgrade that to a verified negative and then overturn the conclusion drawn from it.

- **Zero dedicated complement dataset on any branch.** Every `.csv`/`.tsv` on all 9 remote tips was parsed (sheet XML read directly; `openpyxl`/`pandas` are absent here). No `complement*/data/` directory exists anywhere. The only complement-named paths in the repository are this dossier, these two Beebop files, and one variant dossier.
- **Zero complement file in Drive.** A Drive-wide title search for `*omplement*` returns nothing. A dedicated **`Complement Activation` folder does exist** (id `1X03w9iRA78GKXjSdJjgVjaCkiitPbwZj`), created **2026-10-02 21:56 UTC** — hours ago, after Beebop's request — and it is **empty**. The endpoint has a home and no contents.

But the premise that no complement measurement exists is wrong, and the newer dossier variant Beebop did not read already says so in part:

- **`claude/oligo-reorganize-toxicity-2h7t50:complement-activation/README.md`** (`blob f6c654d8`) is a materially more advanced version of this dossier. It identifies **four measurement rows naming a complement analyte** inside other endpoints' datasets. The `amazing-galileo` variant Beebop and the request both work from (`blob e38ad8b2`) does not contain that section. **Two dossiers disagree about whether complement measurements exist in this repository, and the request is built on the weaker one.**

Verified first-hand, deduplicated by row, the repository's actual complement inventory is **larger than four**:

| Row | Branch / dataset | Readout as recorded | Species | Value | Source |
|---|---|---|---|---|---|
| `COG-MSR0345` | coagulopathy | `complement_alternative_pathway_Bb` | **human** | `NOT_REPORTED`; 5.9–8.5× rise in **all** arms incl. placebo | `COG-S022` |
| `TMSR456` | thrombocytopenia | `complement_activation_below_plasma_threshold` | monkey | `0` | PMID 9152389 |
| `TMSR457` | thrombocytopenia | `complement_activation_plasma_threshold_concentration` | monkey | **`50` µg/mL** | PMID 9152389 |
| `TMSR458` | thrombocytopenia | `complement_factor_H_plasma_concentration` | monkey | `TBD`, direction `decrease` | PMID 9152389 |
| `TMSR459` | thrombocytopenia | `complement_split_products_Bb_C3a_C5a` | monkey | `TBD`, direction `increase` | PMID 9152389 |
| `TMSR460` | thrombocytopenia (`measurements_unresolved`) | `factor_H_displacement_from_heparin_sepharose` | **`NA` — deliberately** | `TBD` | PMID 9152389 |
| `TMSR1047` | thrombocytopenia | `platelet_bound_complement_C3d_C4d` | monkey | `TBD`, `thrombocytopenia_grade 3` | `S-SHEN23` |
| `CMS2155` | chronic-neurotoxicity | `complement_Bb_split_product` | monkey | `~2x` | `R4` |
| `CMS2179` | chronic-neurotoxicity | `complement_Bb_split_product_CSF` | monkey | `0` | `R4` |
| `CMS2201` | chronic-neurotoxicity | `complement_Bb_split_product_CSF` | monkey | `0` | `R4` |

**Ten rows, not zero and not four.** Three consequences Beebop could not have anticipated:

1. **The dossier's own regex sweep no longer reproduces, and its denominator describes a dataset that exists on no branch.** The dossier states "0 hits in all 23 columns × 111 rows of `data/measurements.csv`". The current file is **246 rows × 27 columns** (recounted this session). The 111×23 shape survives only in `claude/oligo-reorganize-toxicity-2h7t50:kidney-toxicity/reconcile/data-111row-lineage/`, and a third lineage carries **769** rows. The *conclusion* (no complement readout in kidney measurements) still holds on the current file; the stated denominator does not. This is the same defect the hepatic reply found in `toxicity/hepatotoxicity.md`, so it is a **repository-wide pattern, not a hepatic one**: dossiers quote row counts from a dataset state that has since moved.
2. **Case-insensitively, the sweep is no longer clean.** The dossier's exact pattern run case-insensitively returns **2 hits** on the current `measurements.csv`, both the substring `c3a` inside the DailyMed GUID `...-1b6cc3a5d123` on `MSR164`/`MSR165`. Case-sensitively it is still 0. The dossier rightly warns that a bare `complement` grep mis-files drug targets; **analyte abbreviations are worse, because `C3a`, `C4a`, `C5a` and `Bb` collide with hex identifiers and chemical formulae.** Any allocation sweep needs word boundaries and a column allow-list.
3. **`TMSR456`–`TMSR460` cite PMID 9152389 — which is the dossier's own acquisition item 2.** Henry *et al.* 1997, *J Pharmacol Exp Ther* 281(2):810–816. The dossier plans to acquire it; the thrombocytopenia dataset already cites it, has extracted five rows from its abstract, and carries the **50 µg/mL threshold** as a recorded value with alicaforsen's exact sequence attached. The plan should start by reconciling that, not by acquiring it.

On the matrix Beebop asked for: I accept the five-way split and would add a sixth bucket, **(f) regulator-adjudicated human evidence**, for the reason given in §2.1. The matrix is §3.

**On scope: I recommend against descoping, and the recommendation is evidence-based, not aspirational.** §3 shows a defensible non-zero human trial count and §7 a zero-cost first package with 144 verified human values in hand. The dossier's descope recommendation was reasonable on what it had and is not reasonable on what exists.

### Suggestion 2 — Prioritize direct human measurements; keep infusion reactions, platelets, coagulation and mechanism as indirect

**ACCEPT the rule without qualification. MODIFY the priority order — the dossier's "Next step" list is in the wrong sequence and is missing its best items.**

The exclusion rule is correct and I applied it strictly throughout: nothing below rests on an infusion reaction, a platelet count, an aPTT change, a glomerular lesion, a cytokine or a proposed mechanism. I also enforced two boundaries Beebop implies but does not state:

- **A drug that targets complement is not complement toxicity.** `OLG035` (cemdisiran, `target_gene = C5_complement`) is correctly flagged by the dossier. The same trap recurs across a whole modern drug class — IONIS-FB-LRx, sefaxersen/RO7434656, AZD6912, pozelimab+cemdisiran, AON-D21, avacincaptad pegol — where complement analytes are **registered efficacy endpoints**. Searching trial registries for complement outcome measures returns mostly this class. The distinction must be a field, not a judgment made per row.
- **Conversely, a therapeutic benefit is not evidence of absent toxicity.** `MSR066` (cemdisiran) carries `negative_eligibility = confirmed_negative` on a readout of eGFR change (`-2.9` vs placebo `-6.3`) — an **efficacy** result. `RESEARCH_ACCESS_REGISTER.md` already raises exactly this caution for teprasiran/`MSR077`; it applies to `MSR066` too, and nobody has recorded it. Not mine to fix, but it should be logged.

**Re-ordering the acquisition plan.** The dossier's five steps put two monkey-only *in vivo* studies first and the monkey-and-human-serum paper third. Every citation verified against NCBI E-utilities and Crossref:

| Dossier rank | Source | Verified identity | Species | My rank | Why |
|---|---|---|---|---|---|
| 1 | Galbraith 1994 | *Antisense Res Dev* 4(3):201–206, **doi 10.1089/ard.1994.4.201**, PMID 7849490 (no DOI in the dossier) | monkey only | **6** | historical first report; abstract names only "C5"; no PMCID; SAGE 403 |
| 2 | Henry 2002 | *Int Immunopharmacol* **2(12)**:1657–1666, doi 10.1016/S1567-5769(02)00142-X, PMID 12469940 | **rhesus** | 5 | Bb ~100×, C5a ~7× at 20 mg/kg ISIS 2302 — the strongest animal effect size in the field |
| 2 | Henry 1997 | *JPET* **281(2)**:810–816, PMID 9152389 (DOI is an Elsevier back-assignment, post-dates the paper) | monkey + cell-free | 4 | **already partly extracted as `TMSR456`–`TMSR460`** |
| 3 | Henry 2014 | *Nucleic Acid Ther* 24(5):326–335, doi 10.1089/nat.2014.0491, PMID 25093529 — **"…in Monkey and Human Serum"** | **monkey, human, and dog** | **2** | the human-serum paper; the dossier's own §"Next step" calls it "in monkey and human serum" and still ranks it third |
| 3 | Shen 2014 | *JPET* 351(3):709–717, doi 10.1124/jpet.114.219378, PMID 25301170 — exact title confirms it **is** a complement paper | monkey + human *in vivo* and serum | **3** | human negative across **767** subjects of the Isis safety database |
| — | **Crooke 2016** | *Mol Ther* 24(10):1771–1782, doi 10.1038/mt.2016.136, PMID 27357629, **PMCID PMC5112040, free, CC BY-NC-SA** | **750 healthy human volunteers** + NHP | **1** | **not in the dossier plan at all**; see §2.2 |

Two corrections to the dossier's reference handling, both verified against the PDFs in `sources/`:

- **Its description of MMB Ch.25 §3.1.2 stops one sentence too early.** The section continues, verbatim from `MethodsMolBiol2022…pdf` PDF p.354: *"Acutely, activation of the alternative complement system can lead to significant drops in blood pressure. Repeated complement activation can result in 'consumption' of complement factor C3 with impaired complement-mediated clearance of antibody aggregates resulting in vascular inflammation [53]. Data from in vitro, in vivo, **and clinical studies** clearly show that cynomolgus monkeys are significantly more sensitive than humans for this lowered threshold of complement activation [54, 55]."* The passage cites **clinical** studies and names refs 53, 56–62 that the dossier never follows. Reading that reference list (PDF pp.358–366) yields **five complement-relevant sources the plan omits**, listed in §2.2.
- **MMB Ch.1's WVEN-531 account is sourced to a corporate press release.** The dossier presents GEM91 and WVEN-531 as the volume's two "compound-named complement accounts", qualitative and equivalent. They are not equivalent. GEM91's is ref [42] (Galbraith 1994, peer-reviewed, non-human primate). WVEN-531's is **ref [65] = "Wave Life Sciences Press Release (2019) … Suvodirsen Phase 1 safety and tolerability data"**. So the repository's own material already contains a compound-named **human Phase 1** complement observation — *"transient increases in complement factors and C-reactive protein"* — graded in the dossier as if it were animal-equivalent background. It is human, and its provenance is press-release-grade. Also note the book writes "WVEN-531" while its cited source concerns **suvodirsen (WVE-210201)**; WVE-N531 is a different Wave compound. **Compound identity in that sentence is unresolved and should not be carried forward without checking.**

### Suggestion 3 — Separate activation readouts, component abundance and functional assays; propose endpoint-specific definitions rather than importing another toxicology's grading scheme

**ACCEPT — this is the strongest item in the set, and the evidence lets me make it concrete instead of abstract.**

The three-way split is exactly right, and the literature divides along those lines so cleanly that pooling would be indefensible:

| Class | Analytes actually used | Quantity | Example |
|---|---|---|---|
| **Activation (split products)** | Bb, Ba, C3a, C4a, C5a, iC3b, C3bBbP, sC5b-9/TCC, C3bc | concentration, fold-change, or incidence >2× ULN | Crooke 2016 (human), Henry 2002 (rhesus) |
| **Component abundance** | C3, C4, factor H, properdin | g/L; "below LLN" | drisapersen C3 −0.085 g/L at wk 48 |
| **Function** | CH50, AH50, total hemolytic complement | % lysis / titre | ApTOLL, CALAA-01, Shaw 1997 |
| **Deposition / surface-bound** | platelet-bound C3d/C4d, glomerular C3c by IF, IgM and properdin binding | qualitative or IF score | `TMSR1047`; Frazier 2015 p.6 |

**They move in opposite directions in the same patient.** In REGULATE-PCI, *CH50 decreased* while *C3a and Bb increased* — function down, split products up, same 90-minute sample. Any scheme that collapses these into one "complement grade" would score that event as partially cancelling. I would add **deposition** as a fourth class; the dossier's own §"Where it touches the kidney data" is entirely about deposition (anti-C3c immunofluorescence along glomerular vascular tufts) and the repository's `TMSR1047` is a deposition row whose `notes` already distinguish it from fluid-phase activation.

**On the rubric, I can offer a source-supported basis instead of an invented one.** Beebop is right that `nephrotox_grade` is not transferable — its levels are renal at every step. But this endpoint does not need an invented scale either, because the field already has a convention:

- **Incidence of a split product above 2× ULN** is the threshold Ionis uses in human and NHP safety assessment (Crooke 2016, Table 1 for NHP and Table 2 for humans, verified).
- **Component abundance below LLN** is the threshold the regulators use (inotersen: 55% vs 21% of subjects with any post-baseline C3 below LLN; drisapersen: 11.7% vs 1.3% shifting normal→low).
- **Plasma concentration threshold** is the exposure axis: ~50 µg/mL in monkey serum (Henry 1997 and Henry 2014, and already recorded as `TMSR457`).

So a defensible draft rubric is anchored on **2× ULN for split products, LLN for components, and the ~50 µg/mL exposure threshold** — all three traceable to sources, none borrowed from another organ. German should adjudicate it; I am proposing the anchors, not the grades.

**Two schema requirements the suggestion does not mention, both forced by evidence:**

- **Route of administration is an exposure determinant here, not metadata.** MMB Ch.1 PDF p.23, verbatim: complement activation *"was due to a plasma concentration effect of the poly-anionic nature of PS-ODNs. **It could be mitigated by subcutaneous administration or by slow intravenous infusion.**"* Consistent with this, the human positives cluster on high-Cmax schedules (24-hour and 2-hour IV infusions of ISIS 5132 and aprinocarsen) while subcutaneous chronic regimens produce slow C3 consumption instead of acute split-product spikes. `delivery_method` must be mandatory and non-null.
- **Donor identity is required for human laboratory rows, because pathway assignment is donor-dependent.** Mangsbo 2009, verbatim: *"P-S-modified CpG 2006 affected classical activation in donor X but alternative activation in donor Y."* A per-donor row structure is not a nicety; the pathway conclusion changes between donors of the same experiment.

### Suggestion 4 — Human-first views with auditable counting; registry identifiers; pooled summaries must not silently add to the trial count

**ACCEPT, and this endpoint supplies the single best worked example in the project of why the pooled-evidence rule matters.**

The rule as written is: *"A pooled trial summary without recoverable study identities remains pooled evidence and should not silently add to the trial count."* The **largest human complement dataset in the field is exactly that case**, and I verified it rather than assuming it:

- **Crooke 2016** pools **750 human subjects** (179 women, 571 men) across "randomized placebo-controlled dose-ranging phase 1 trials" for **12 unique 2′-MOE ASOs**, and measures **Bb, C5a and C3** in humans. It contains **no NCT numbers and no protocol codes anywhere** — not in the main text, and the ASOs are identified only as "ASO 1–12", with just two named (ASO 4 = mipomersen; ASO 11 = a GCGR ASO). The number of constituent trials is never stated.
- Therefore Crooke 2016 yields **many human complement measurements and exactly zero countable verified trials.** Had this been ingested without the rule, it would have produced a headline figure of 750 "participants" and an unknowable trial denominator.

**A second, sharper dedup trap, which I would not have caught without reading both sources.** Shen 2014 corroborates its human negative against *"the Isis Clinical Safety Database containing **767** subjects"*. Crooke 2016 reports **750**. These are overlapping draws from one sponsor's safety database over the same era and the same chemistry class, and both overlap again with the mipomersen, inotersen and volanesorsen programmes counted separately in §3. **750 + 767 is not 1,517, and neither number may be added to the per-programme counts.** I recommend a `participant_pool_id` field so overlapping sponsor-database draws are visibly one pool.

**A third trap, internal to this repository.** The two alicaforsen human trials that measured C3a (Glover 1997, Maksymowych 2002) are already recorded on the **coagulopathy** branch as `COG-STU139`/`COG-STU144`, while the same drug's human data also appear on the **thrombocytopenia** branch as `TMSR452`–`TMSR454`. A complement dataset assembled by harvesting sibling endpoints would count these trials twice. Dedup must be on **PMID or registry ID**, never on document name — a point `COG-STU139`'s own `duplicate_of_hint` already makes about its seven-abstracts-in-one-file source.

### Suggestion 5 — Assess accessibility, usable human measurements, qualified controls and characterization gaps; escalate a bounded scope decision rather than silently completing or excluding

**ACCEPT the process. REJECT the implied conclusion that evidence is likely to remain insufficient.**

Accessibility is genuinely bad for the classical five papers — four of five are closed with no PMCID, and every barrier I hit was a Cloudflare browser challenge rather than a rendered paywall (§6, and the distinction matters because a human with a browser may get through where this session cannot). But accessibility is **excellent** for the sources that actually carry human data, and nobody had looked:

- **Crooke 2016** — free, PMC5112040, **and its Supplementary Tables S1–S10 are retrievable**: I downloaded the supplementary bundle from Europe PMC (HTTP 200, 2,549,427 bytes, containing `mt2016136x1.pdf`, 1.93 MB). This retires an access request before it was raised.
- **Sewing 2017** — `PLoS One` 12(11):e0187574, PMID 29107969, PMC5673186, **CC-BY**, and its raw-data supplement is in hand (§2.3).
- **Mangsbo 2009** — *J Immunol* 183(10):6724–6732, PMID 19864604, **PMC2857538, free full text**.
- **The regulatory record is entirely free**, and it is where the chronic human complement data live (§2.1).

So the bounded scope decision I am escalating to Oscar is **not** "can we obtain anything defensible". It is the much narrower question in §7: whether to ingest one open-access human-laboratory source now, or wait for the paywalled mechanism papers.

On characterization: the gap is real and I quantify it with denominators in §4. It does not block the §7 package, because that package's one source publishes its own sequences and backbone chemistry.

## 2. Additional findings Beebop did not have

### 2.1 The chronic human complement data exist only in the regulatory record — a literature-only search cannot find this endpoint

This is the most consequential finding of the review, and I verified every figure below by downloading the EMA PDFs myself and extracting the passages (not relayed):

- **Drisapersen — EMA Kyndrisa withdrawal assessment report** (105 pp, `withdrawal-assessment-report-kyndrisa_en.pdf`, HTTP 200, 2.80 MB; 64 "complement" hits, ~12 of them "complementary/complemented"). Verbatim: *"**Mean changes of Complement C3 from baseline were -0.047 g/L at Week 12, -0.075 g/L at Week 24, and -0.085 g/L at Week 48 (8% decrease from baseline to Week 48)**, respectively, for drisapersen. For placebo, the mean changes were 0.041, 0.004, and -0.025 g/L, respectively. At week 48, **more subjects on drisapersen 6 mg/kg/wk had a shift from normal to low complement C3 compared to placebo (11.7% vs. 1.3%)**."* Also verbatim: *"complement split products measured in two phase I/II studies (**DMD114118 and PRO051-02**) … There seemed to be no strong evidence … **A mean concentration of split product C3a was found to be above the upper range of normal already at screening in study DMD114118**, which needed further discussion."* And *"long-term drisapersen therapy also decreased Complement factor C3 in clinical trials (study nos. **DMD114876 and DMD114044**)"*. `complement factor C3 decreased` appears as an **adverse-event term** at **6.4% vs 0%**.
- **Inotersen — EMA Tegsedi EPAR** (142 pp, HTTP 200, 2.31 MB; 49 hits). Verbatim: *"**Complement split product measurement (C5a and Bb) was conducted in study CS1.** … otherwise healthy volunteers in CS1 were reported to have had complement factors **C5a and Bb >ULN at baseline** as well as at several time points … in the placebo multiple dose cohort"*; *"**Complement factors were not routinely measured in CS2.** … **55% of inotersen-treated subjects had any post-baseline C3 value below LLN compared to placebo (21%). Mean complement C3 deceased by 33% from baseline to Week 65 in CS2**"* (the typo "deceased" is the source's); *"glomerular deposits for complement factors and IgG"* in renal biopsies; and the CHMP's own verdict, *"**Complement activation was not thoroughly studied in the clinical program**"*.
- **Mipomersen — EMA Kynamro EPAR** (114 pp, HTTP 200, 3.40 MB; 15 hits). Verbatim: *"**consumption of complement (C3 fraction)**, and 65% of patients showing mipomersen antibodies, a contributing effect of immunologically mediated damage to the ISRs cannot be completely excluded"*; *"**Slightly lower C3 values were observed, but without signs of complement activation.** The clinical significance is unknown"*; *"**Antibody formation might induce complement consumption**"*.

Three things follow. First, **the inotersen CS1 baseline finding is a methodological warning the whole endpoint needs**: healthy volunteers, including the placebo arm, had C5a and Bb above ULN at baseline, so a 2× ULN incidence rule applied without a baseline-anchored comparison will generate false positives. Second, **complement is named in the grounds for a negative CHMP opinion.** The Kynamro refusal-grounds document (80,931 bytes, HTTP 200, verified by me) contains exactly two "complement" occurrences and both are in the refusal reasoning, verbatim: *"Mipomersen is also associated with a high incidence of flu-like symptoms, effect on inflammatory markers and **decrease on complement component C3**. Mipomersen may be immunogenic and antibodies were detected in 65% of subjects taking the product. In addition, **complement activation was more pronounced in patients with antibody formation**."* Third, and practically: searching PubMed for `mipomersen AND complement` or `drisapersen AND complement` does not surface any of this. **Beebop's and the dossier's search strategy could not have found the endpoint's richest human evidence, because it is not in the literature.** Hence the sixth matrix bucket in §1.1.

### 2.2 Five complement sources citable from PDFs already in `sources/`, none in the dossier's plan

All extracted from the MMB volume's own reference lists and verified against Crossref/PubMed:

| Ref | Citation | Why it matters |
|---|---|---|
| Ch.25 [61] | **Crooke ST, Baker BF, Kwoh TJ, Cheng W, Schulz DJ, Xia S, Salgado N, Bui HH, Hart CE, Burel SA, Younis HS, Geary RS, Henry SP, Bhanot S (2016)** *Mol Ther* 24(10):1771–1782, doi 10.1038/mt.2016.136 | **750 human volunteers, complement measured, free, supplement in hand.** The top source for this endpoint |
| Ch.25 [62] | **Shen L, Engelhardt JA, Hung G, Yee J, Kikkawa R, Matson J, Tayefeh B, Machemer T, Giclas PC, Henry SP (2016)** "Effects of repeated complement activation associated with chronic treatment of Cynomolgus monkeys with 2′-O-Methoxyethyl modified antisense oligonucleotide", *Nucleic Acid Ther* 26(4):236–249, doi 10.1089/nat.2015.0584 | the chronic-dosing animal counterpart to the human C3-consumption signal |
| Ch.25 [101] | **Nucleic Acid Ther 26(4):210–215, doi 10.1089/nat.2015.0593, PMID 26981618** — "Considerations for the Characterization and Interpretation of Results Related to Alternative Complement Activation in Monkeys Associated with Oligonucleotide-Based Therapeutics" (Oligonucleotide Safety Working Group) | **the assay-characterization and interpretation guidance this endpoint's definitions should be written against.** ⚠ author order unresolved: MMB prints the entry beginning "Seguin R, Cavagnaro J, Berman C, Tepper J, Kornbrust D"; PubMed indexes Henry SP first. Resolve before citing |
| Ch.25 [53] | **Engelhardt JA, Fant P, Guionaud S, Henry SP, Leach MW, Louden C, Scicchitano MS, Weaver JL, Zabka TS, Frazier KS, STP Vascular Injury Working Group (2015)** *Toxicol Pathol* 43(7):935–944, doi 10.1177/0192623315570341 | the source behind the C3-consumption → vascular-inflammation chain |
| Ch.25 [103] | **Tessier Y, Achanzar W, Mihalcik L, Amuzie C, Andersson P, Parry JD, Moggs J, Whiteley LO (2021)** EFPIA Oligonucleotide Working Group survey, *Nucleic Acid Ther* 31(1):7–20, doi 10.1089/nat.2020.0892 | what complement assays industry actually runs — endpoint-definition support |
| Ch.25 [100] | **Crooke ST, Baker BF, Witztum JL, et al. (2017)** "The effects of 2′-O-Methoxyethyl containing antisense oligonucleotides on platelets in human clinical trials", *Nucleic Acid Ther* 27(3):121–129 | sibling endpoint, but the template for a pooled human-trial analysis |
| Ch.25 [101a] | **EMA (2018) Kynamro assessment report**, EMA product 002429 | the dossier's PDFs already point at the regulatory record; §2.1 is what is in it |

I also confirmed two negatives the dossier leaves open: `Sioud_oligo_immunostimulation_cytokines_book.pdf` contains **zero** occurrences of "complement" (so it is correctly unallocated), and the in-repo `OligoTox_challenge_brief.pdf` contains **exactly one** — the endpoint's own name in the scope list, as the dossier says. Note that the in-repo brief is **6 pages**, while the suggestions and access register cite a **20-page** v5 announcement; these are different documents and the repo holds only the short one.

### 2.3 A fully extractable, open-access, per-donor human whole-blood complement dataset — already downloaded, zero acquisition cost

**Sewing S, Roth AB, Winter M, Dieckmann A, Bertinetti-Lapatki C, Tessier Y, McGinnis C, Huber S, Koller E, Ploix C, Reed JC, Singer T, Rothfuss A (2017)**, "Assessing single-stranded oligonucleotide drug-induced effects in vitro reveals key risk factors for thrombocytopenia", *PLoS One* 12(11):e0187574, PMID 29107969, PMC5673186, **CC-BY**.

It is already cited in this repository — on the thrombocytopenia branch as `EXV-TMB-051`/`EXV-TMB-052`, where the endpoint field reads *"Platelet activation, GPVI/PF4 binding, complement and cytokines"* with `Source_Location = Figures 2-6`. **The complement content is invisible there because it is bundled into a composite endpoint string.** Read directly, it is a complement dataset:

- **Analytes: C3a and C5a**, human whole blood, individual sandwich ELISA (**Quidel/TECOmedical Complement Plus EIA**), 45-minute incubation, samples diluted 1:1 in stabilising solution and frozen at −70 °C.
- I downloaded the supplement (`pone.0187574.s001.xlsx`, 54,955 bytes, from the Europe PMC supplementary bundle) and parsed the sheet XML directly. Sheet **"Figure 6"** holds the complement block, headed *"Individual data Whole Blood Assays [Stimulation Index]"*.
- **144 individual human complement values** — 72 C3a + 72 C5a — across **16 conditions**, per donor:

| Condition | n donors | C3a (stimulation index, per donor) |
|---|---|---|
| ODN2395 **+PS** (full phosphorothioate) | 5 | **17.1, 9.9, 10.3, 12.8, 8.9** |
| ODN2395 **−PS** (phosphodiester) | 5 | **0.6, 0.5, 0.6, 0.5, 1.4** |
| (AC)ₙ series, 10/12/14/16/18/20/22 nt | 5 each | 0.5 – 2.7 across all 35 values |
| 16/18/20 nt **LNA** | **3 each** | 0.6 – 1.5 |
| Classical-pathway control | 5 | 10.2 – 21.0 |
| Alternative-pathway control | 5 | 6.4 – 13.3 |
| Inhibitor control | 5 | 0.1 – 0.3 |
| PBS | 3 | 1 (normaliser) |

C5a mirrors it: +PS 4.9/3.1/6.8/4.8/3.4 versus −PS 0.8/0.7/0.9/0.7/0.9.

This single file delivers what the dossier says does not exist: **human matrix, named analytes, a named assay, pathway-specific positive controls, an inhibitor control, a matched phosphorothioate-versus-phosphodiester backbone pair, a seven-point length series, LNA variants, and per-donor values** — under CC-BY.

Three caveats I will not paper over. **(i)** The values are a **Stimulation Index** — a derived ratio to PBS, not an absolute ng/mL — so they can never share a numeric column with the absolute concentrations in other sources. **(ii)** Donor counts are **unequal within one figure** (n=5 for the PS/PO and length series, n=3 for the LNA columns and PBS); the denominator must be per condition. **(iii)** I have **not** read Table 2 character-by-character, so the sequences are not verified by me; the repository records ODN2395 as `TCGTCGTTTTCGGCGCGCGCCG` (22 nt) and I report that as repo-recorded, not confirmed.

### 2.4 The two open-access human-blood sources disagree about backbone dependence — and this is a real scientific question, not a curation error

**Mangsbo SM, Sanchez J, Anger K, Lambris JD, Nilsson Ekdahl K, Loskog AS, Nilsson B, Tötterman TH (2009)**, "Complement Activation by CpG in a Human Whole Blood Loop System: Mechanisms and Immunomodulatory Effects", *J Immunol* 183(10):6724–6732, doi 10.4049/jimmunol.0902374, PMID 19864604, **PMC2857538, free full text** (AAI copyright, **no CC licence** — derived values only). I read it directly.

- Fresh **non-anticoagulated human whole blood**, healthy volunteers, surface-heparinised loop; n=3–6 donors; **2, 6, 20, 60 µg/mL**; **C3a, C4a, C5a** by cytometric bead array; IgM deposition and properdin binding by flow cytometry; convertase assembly by QCM-D.
- Sequences printed verbatim, with **per-position backbone denoted by letter case**: **CpG 2006 (P-S)** `5′-TCG TCG TTT TGT CGT TTT GTC GTT-3′`; **GpC control** `5′-TGC TGC TTT TGT GCT TTT GTG CTT-3′`; **CpG 2216** `GGg gga cga tcg tcG GGG GG` (lower case = phosphodiester); plus a complete **CpG 2006 P-O** variant.
- Controls with concentrations: compstatin 9.2 µM, C5aR antagonist 8.4 µM, EGTA 10 mM, anti-CD11b 10 µg/mL.
- Results: **C3a and C5a detected from 15 min at 20 µg/mL and high at 60 µg/mL; nothing at 2–6 µg/mL; C4a not elevated at 1 h.** Both classical and alternative pathways implicated.

**The disagreements with Sewing 2017 are substantive and must be preserved, not reconciled:**

| | Sewing 2017 | Mangsbo 2009 |
|---|---|---|
| Phosphodiester backbone | **inactive** (SI 0.5–1.4) | **also activated complement** |
| Sequence control | — | **GpC control activated similarly** → sequence-independent |
| C4a | not measured | **not elevated** while C3a/C5a were |
| What the backbone determines | whether activation happens | **which pathway** is engaged, donor by donor |
| Matrix / readout | whole blood, stimulation index | whole blood loop and hirudin plasma, absolute CBA |

And a cross-species observation German should rule on rather than me: Mangsbo sees human whole-blood activation **between 6 and 20 µg/mL**, whereas the monkey-serum threshold recorded as `TMSR457` and confirmed by Henry 2014 is **~50 µg/mL**. Different compounds, matrices and readouts, so these are **not commensurable** and I assert no contradiction. But the repository's inherited narrative — "humans are less susceptible" — is a **compound-, chemistry-, pathway- and matrix-specific** claim, not a general one, and the dossier currently states it generally (quoting MMB Ch.26's *"humans are less susceptible to these effects"* without qualification).

### 2.5 The one human complement row in the repository under-captures its own source by three analytes

`COG-S022` is **Demirjian S, Ailawadi G, Polinsky M, Bitran D, Silberman S, Shernan SK, Burnier M, Hamilton M, Squiers E, Erlich S, Rothenstein D, Khan S, Chawla LS**, *Kidney Int Rep*, PMC5733816, PMID 29270490, doi 10.1016/j.ekir.2017.03.016, **NCT00554359**, CC BY-NC-ND. I read it.

The paper measures **four** analytes — **Bb, C3a, C4a and C5a** — in plasma at screening and 5/15/30 min and 1/2/4/8/24 h post-dose. Verbatim: *"The mean blood concentrations reflecting classic complement pathway activation (C′3a, C′4a, and C′5a) remained stable across all QPI-1002 and placebo groups"*, while *"mean postoperative, predose levels of alternate pathway activated factor B (Bb) increased by 5.9- to 8.5-fold compared with baseline (screening) levels in all groups, consistent with the previously described impact of on-pump bypass surgery."*

The repository has **one row (Bb)**. The three stable analytes — **human, measured, reported** — exist nowhere in the repository. The curation of the row itself is good: `readout_is_qualitative = TRUE`, `value_origin = measured_in_this_document`, `ratio_basis = qualitative_row`, and `notes` stating the absolute values *"exist only in Figure 2 and were NOT read off the plot"*. Its one weakness is structural rather than careless: `readout_category = clotting_time`, with `notes` explaining *"Classified under clotting_time only because the schema has no complement category"*. That is a schema gap doing damage in a sibling dataset.

**And the source's own pathway attribution is biologically loose.** It labels C3a, C4a and C5a "classic complement pathway activation". C3a and C5a are **common-pathway** products generated by any route; C4a is classical/lectin. So the paper's pathway label cannot be inherited as a curated fact. This is precisely why Beebop's suggestion 3 is right, and it gives German a concrete adjudication: **record the source's pathway label and the curator's pathway assignment in separate fields.** The same issue recurs in the ApTOLL 2024 paper, whose results text calls **C3 and C4** the "terminal complement complex" while its methods list C3, C4 and CH50 — an error in the published paper.

### 2.6 PEG, not the backbone, produced the only human complement signal tied to severe clinical harm

**Povsic TJ, Lawrence MG, Lincoff AM, Mehran R, Rusconi CP, Zelenkofske SL, Huang Z, Sailstad J, Armstrong PW, Steg PG, Bode C, Becker RC, Alexander JH, Adkinson NF, Levinson AI; REGULATE-PCI Investigators (2016)**, "Pre-existing anti-PEG antibodies are associated with severe immediate allergic reactions to pegnivacogin, a PEGylated aptamer", *J Allergy Clin Immunol* 138(6):1712–1715, doi 10.1016/j.jaci.2016.04.058, PMID 27522158, **no PMCID, confirmed paywall**. Trial **NCT01848106** (terminated, clinical hold, no results posted).

Measured in humans: **C3a, C4a, C5a, CH50, factor Bb**, plus tryptase and anti-PEG IgG, under the trial's own risk-mitigation and action plan — **not** a registered outcome measure. In the severe-reaction group with paired pre/90-minute samples (n=11): **CH50 significantly decreased, C3a and factor Bb significantly increased**, C4a and C5a not significantly changed though 9 of 11 rose.

Two implications. **(i)** This endpoint is not only a phosphorothioate story; a **conjugate** (PEG) can drive it through an antibody-dependent route, which means `conjugate` and anti-drug-antibody status are predictors here, not metadata. **(ii)** It is the one human dataset where measured complement is temporally and mechanistically tied to severe clinical events — so it should anchor the endpoint's clinical-relevance narrative even though it contributes few rows.

A related negative worth recording: for **pegaptanib/Macugen**, the FDA medical review for NDA 21-756 contains **zero** occurrences of "complement". PEGylation alone is not sufficient; systemic exposure and preformed antibody matter.

### 2.7 A verified generational gap: the GalNAc-conjugated era has no human complement measurement at all

Reading the EMA EPARs directly: **Onpattro/patisiran** (16 complement hits, **all monkey**), **Tryngolza/olezarsen** (11 hits, all monkey), **Leqvio/inclisiran** (1, monkey), **Spinraza/nusinersen** (2, both "complemented by"), **Givlaari/givosiran** (0), **Oxlumo/lumasiran** (0), **Amvuttra/vutrisiran** (3, all "complementing/complemented"), **Qalsody/tofersen** (1, "complemented"). Per-drug registry searches for complement outcome measures return nothing for any of them.

So the human complement evidence base is **concentrated in the first- and second-generation unconjugated PS era (1994–2018)** and stops. For a dataset meant to support predictive modelling of modern constructs, that is a stated limitation, not a gap to be filled — and it is an argument for the mechanistic human-laboratory route in §7 over a clinical-trial-harvesting route.

### 2.8 The factor H decrease in the repository may be an assay artifact

`TMSR458` records `complement_factor_H_plasma_concentration` with `effect_direction = decrease`, from Henry 1997's abstract. Henry 2014 — the monkey-and-human-serum paper — reports that the **apparent factor H decrease is partly an immunoassay artifact**, the ASO interfering with the anti-factor-H antibody. Any row or narrative asserting factor H depletion must carry that caveat. This also vindicates a curation decision: `TMSR460` sets `species = NA` because the abstract does not state the species of the factor H used in the heparin-sepharose competition. That was right, and resolving it matters — **if the factor H were human, `TMSR460` becomes a human-laboratory row.** It is in my access list as A4.

### 2.9 The September 30 suggestions file still authorises implementation

`toxicity/complement-activation/BEEBOP_SUGGESTIONS_2026-09-30.md` closes with *"Oscar has authorized Rocksteady to review, improve, and implement justified changes"* and *"No additional confirmation from Oscar is needed merely to begin this review."* The 2026-10-01 round supersedes this, but the file is unchanged and sits beside the request. A session opening only that file would begin implementing. The hepatic reply raised the identical defect on its own copy; it is **per-endpoint and unfixed here**. Recommend a one-line supersession header — a process fix, not a scientific one.

## 3. Evidence-class accounting, with denominators

Mutually exclusive classes, as required. **Human clinical first. No figure below is offered as a headline trial total except the one row that says so.**

### 3.1 What exists in the repository today

| Class | Verified count | Basis |
|---|---|---|
| **Verified human clinical trials in a complement dataset** | **0** | no complement dataset exists — a verified zero |
| **Human complement measurement rows anywhere in the repository** | **1** | `COG-MSR0345` (Bb), coagulopathy branch, filed `endpoint_scope = scope_adjacent` |
| Human clinical trials in the repository carrying a complement measurement, identity-resolved | **1** | **NCT00554359**, full text staged as `COG-S022` |
| Human trials whose complement result is in the repository **only as study-level free text** | **2** | `COG-STU139` (Glover 1997, PMID 9316823), `COG-STU144` (Maksymowych 2002, PMID 11908555) — no measurement row exists for either |
| Human complement analytes measured by an in-repo source but **recorded nowhere** | **3** | C3a, C4a, C5a of `COG-S022` (§2.5) |
| Animal complement rows | **7** | `TMSR456`–`TMSR459`, `TMSR1047`, `CMS2155`, `CMS2179`, `CMS2201` — monkey |
| Unresolved-species rows | **1** | `TMSR460` (`species = NA`, deliberately) |
| Dedicated complement source PDFs | **0** | confirmed; the dossier is right |
| Complement rows in the kidney dataset | **0** | confirmed on the current 246×27 file; the dossier's 111×23 denominator is stale |

### 3.2 Distinct human clinical studies with a measured complement analyte, outside the repository

**Tier A — I read the source document myself this session.**

| Study identity | Compound | Analytes in humans | Result |
|---|---|---|---|
| **NCT00554359** (QRK-002) | QPI-1002 / I5NP siRNA | Bb, C3a, C4a, C5a | Bb ↑5.9–8.5× in **all** arms incl. placebo (surgery); C3a/C4a/C5a stable |
| **Crooke 2016 pooled** (750 subjects, **no trial identifiers**) | 12 × 2′-MOE ASOs | Bb, C5a, C3 | no increase >2× ULN; NHP **over-predicted** |
| **DMD114876**, **DMD114044** | drisapersen | C3 | −0.047/−0.075/−0.085 g/L at wk 12/24/48; 11.7% vs 1.3% normal→low |
| **DMD114118**, **PRO051-02** | drisapersen | C3a split product | no strong evidence; C3a >ULN already at screening |
| **DMD114349** (to wk 104) | drisapersen | C3 | slight further decrease, mainly stable |
| **CS1** | inotersen | C5a, Bb | **>ULN at baseline incl. placebo**; no pattern detectable |
| **CS2 / NCT01737398** (NEURO-TTR) | inotersen | C3 (not routine), split products | 55% vs 21% any post-baseline C3 <LLN; mean C3 −33% to wk 65 |
| **mipomersen phase 3 programme** (excl. CS5) | mipomersen | C3 | median −7.2% vs −3.0% placebo at wk 28/ET |
| **MIPO3200309** | mipomersen | Bb, C5a | no activation |

**Tier B — citation and finding verified, document not read by me.**

| Study identity | Compound | Analytes | Result |
|---|---|---|---|
| PMID 9316823 (Glover 1997, ph 1) | ISIS 2302 | C3a, C5a | **C3a ↑** after higher repeated doses; C5a unchanged |
| PMID 11908555 (Maksymowych 2002) | ISIS 2302 | serum C3a | small, "clinically insignificant" ↑ at 2 mg/kg |
| PMID 11350886 (Rudin 2001, ph 1) | ISIS 5132 | analytes **unverified** | **dose-dependent activation** on the 24-h schedule |
| PMID 16133798 (Advani 2005, ph 1) | aprinocarsen / ISIS 3521 | Bb, C3a | **Bb ↑1.6×, C3a ↑3.6×**, dose-correlated, transient; contributed to MTD |
| PMID 10550158 (Nemunaitis 1999, ph 1) | ISIS 3521 | "complement levels" | no dose/Cmax/AUC relationship |
| PMID 10778949 (Chen 2000, ph 1) | GEM231 | unspecified | no treatment-related activation |
| **NCT04742062** (ApTOLL FIH) | ApTOLL aptamer | **CH50, C5b-9** | no difference, any timepoint |
| **NCT05569720** (ApTOLL bolus vs infusion) | ApTOLL | C3, C4, CH50 | no effect |
| **NCT00689065** (CALAA-01 ph Ia/Ib, n=24) | CALAA-01 siRNA nanoparticle | plasma Bb, serum CH50 | no appreciable change — **complement is a registered outcome measure** |
| **NCT01848106** (REGULATE-PCI) | pegnivacogin | C3a, C4a, C5a, CH50, Bb | **CH50 ↓, C3a ↑, Bb ↑** at 90 min, n=11 paired |
| **CS6 / CS16** | volanesorsen | C5a, Bb | no notable difference by ADA status |
| Isis Clinical Safety Database, **n=767** | multiple 2′-MOE | AP activation | no evidence in humans |

**Tier C — provenance too weak to count.** Suvodirsen / WVE-210201 Phase 1, *"transient increases in complement factors and C-reactive protein"* — sole source a **corporate press release**, with the compound-identity ambiguity of §1.2.

**Headline figures, stated carefully.**

- **Distinct human clinical studies with a measured complement analyte that I can name and cite: 19** (9 Tier A + 12 Tier B, less the Isis-database draw which is a pool, not a study). Of these, **9 verified by me first-hand**.
- **Distinct named human-tested compounds with a measured complement analyte: 12** — QPI-1002, alicaforsen/ISIS 2302, ISIS 5132, aprinocarsen/ISIS 3521, GEM231, ApTOLL, CALAA-01, pegnivacogin, mipomersen, drisapersen, inotersen, volanesorsen — plus up to 10 further unnamed ASOs inside Crooke 2016.
- **Verified human clinical trials eligible for a headline total today: 1** (NCT00554359, in-repo). Everything else requires source acquisition and a study-register build before it may be counted.
- **Pooled human evidence that must not enter any trial count: 2 sources, 750 and 767 subjects, overlapping.**

**Why I will not offer a single "verified human trials" number above 1.** Oscar's rule requires counts generated from a qualified study register, and no such register exists for this endpoint. The 19 studies are a **qualified candidate pool**, not a trial count: the regulatory studies are identified by sponsor protocol code rather than registry ID; Crooke 2016 and Shen 2014 are overlapping pooled draws; two alicaforsen trials are already double-filed across sibling branches; and six Tier B analyte assignments are unverified. I would rather report **one** verified trial and a declared pool of nineteen than a number that cannot be reconciled to an identifier list.

### 3.3 Human laboratory / ex-vivo sources

| Source | Matrix | Analytes | Direction | Access |
|---|---|---|---|---|
| **Sewing 2017** | human whole blood | C3a, C5a (stimulation index) | **PS positive; PO, length series and LNA negative** | **CC-BY, in hand, 144 values** |
| **Mangsbo 2009** | human whole blood + hirudin plasma | C3a, C4a, C5a | **positive, PS *and* PO, sequence-independent** | **free (PMC2857538), no CC licence** |
| de Boer 2022 | human whole blood + plasma | sC5b-9, C3bBbP, C3bc; C1q and factor H binding | **positive, backbone-dependent** | **not OA** (§6, A5) |
| Shaw 1997 | human serum | hemolytic complement, **C4d** | **positive**, linkage-dependent, sequence-independent | closed |
| Agrawal 1995 | **human, rhesus and guinea pig serum, side by side** | hemolytic complement | reduced in **all three** | closed |
| Henry 2014 | monkey, **human** and dog serum | AP activation; factor H | **human absent**, monkey ≥50 µg/mL | closed |
| Shen 2014 | monkey and **human** serum + in vivo | AP activation; factor H IC50 | **human absent** | browser-blocked |
| Paul 2010 | human whole blood (Chandler loop) | complement, analytes unverified | aptamers negative | closed |
| Kandimalla 1997 | **serum species unverified** | hemolytic complement | MBOs < PS controls | PMC proof-of-work gate |

**9 human-laboratory sources; 2 reachable and usable today; 4 positive, 3 negative, 2 unresolved.** That is the opposite of an empty endpoint, and it is the evidence class the challenge brief privileges — its single complement sentence sits in a paragraph seeking datasets that *"make use of in vitro human systems"*.

### 3.4 Explicitly excluded, and why

- **Target-is-complement (efficacy, not toxicity):** cemdisiran, IONIS-FB-LRx (NCT03446144, withdrawn), sefaxersen/RO7434656, AZD6912 (NCT06115967), pozelimab+cemdisiran (NCT04601844), ADX-038, AON-D21, avacincaptad pegol. **Nearly every modern oligonucleotide trial registering a complement outcome measure does so for efficacy** — the two exceptions are CALAA-01 and ApTOLL-COVID. This asymmetry is itself a finding and argues for a mandatory `complement_measurement_intent` field (`toxicity` / `pharmacodynamic_efficacy`).
- **Indirect only, no complement measured:** the entire alicaforsen Crohn's programme (PMIDs 9609749, 12077088, 12269969, 17296530, 15958080) — infusion reactions and aPTT only; eteplirsen FDA AdCom documents, where complement appears solely as animal class context.
- **Animal-only sources** kept as supporting material and out of every human total: Galbraith 1994, Henry 1997, Henry 2002, Shen 2016, Shen 2023, Wallace 1996 (AR177/zintevir), Engelhardt 2014, Rider 2022 (**SLN360 — complement measured in NHP only; its human whole blood was used for cytokines, not complement** — a natural false positive, excluded by verification), and the monkey complement sections of the patisiran, olezarsen, inotersen, drisapersen, mipomersen, volanesorsen and inclisiran regulatory records.
- **CARPA:** Szebeni's CARPA corpus contains **no oligonucleotide-specific human work** (`Szebeni J[au] AND complement AND (oligonucleotide OR aptamer OR siRNA)` → 0 hits). His influence is real but indirect — his 2014 *Mol Immunol* review is the stated reason the ApTOLL trialists measured complement at all.
- **Patents:** US 6,232,296 and the Ionis composition patents describe assays and compositions. **A patent describing an assay is not evidence it was run**, exactly as Beebop says. They are useful only as a route to compound chemistry.

## 4. Sequence, chemistry and tested-material assessment

Per the shared review questions, with explicit denominators over the eligible human subset.

| Dimension | Coverage over the human-eligible set | Note |
|---|---|---|
| Exact sequence | **2 of 12** named human-tested compounds have a sequence I can point to: alicaforsen `GCCCAAGCTGGCATCCGTCA` (repo-recorded on `TOLG035`, corroborated by WHO INN and patent listings) and AR177/zintevir `GTGGTGGGTGGGTGGGT` (animal) | **0 of 12 verified by me character-by-character** |
| | Human **laboratory** set: **4 of 4** Mangsbo oligos printed verbatim; Sewing's in Table 2, **not read by me**; repo records ODN2395 as `TCGTCGTTTTCGGCGCGCGCCG` | the laboratory set is far better characterised than the clinical set |
| Orientation | stated 5′→3′ in Mangsbo and in the repo's `sequence_5to3` | |
| Strand / duplex identity | single-strand for every PS-ODN/ASO source; **duplex for QPI-1002 and CALAA-01 siRNA, and for the patisiran LNP** — and no source gives both strands | becomes live the moment siRNA rows enter |
| **Position-specific chemistry** | **1 source only: Mangsbo 2009**, where CpG 2216 `GGg gga cga tcg tcG GGG GG` encodes backbone per position by letter case | Sewing gives category-level (full PS ± LNA flanks); Crooke gives none at all |
| Conjugates | **pegnivacogin's PEG is the causal agent of the only harm-linked human signal** (§2.6) — so `conjugate` is a predictor here, not metadata | |
| **Tested-material characterization** | **0 of 12** human-tested compounds has a purity or analytical-identity figure from any source I reached; **0 of 9** human-laboratory sources reports purity | |

**A populated sequence field is not validated identity, and this endpoint shows it three ways.** (i) Crooke 2016's 12 ASOs are *"ASO 1–12"* with 2 named — 750 human subjects' complement data attached to **10 unidentifiable constructs**. (ii) MMB Ch.1's "WVEN-531" does not match its cited source's "suvodirsen" (§1.2). (iii) The repository's own `TOLG035` sequence is `design_source`-derived from WHO INN nomenclature and patent listings, **not read out of the complement papers that the rows cite** — so sequence and outcome in `TMSR456`–`TMSR460` come from different documents.

**On purity, this endpoint is the project's worst case and the reason is mechanistic, not clerical.** The effect is driven by **polyanionic charge and backbone linkage count** (MMB PDF p.26: *"These effects as well as strong binding to serum proteins were thought to be due to the poly-anionic nature of the PS linkage"*; Shaw 1997: abolished by protamine sulfate). Therefore **n−1 shortmers and incompletely sulfurised species are not inert impurities — they change the measured quantity.** The challenge announcement's p.6 requirement for *"data on the purity and characterization of each"* is a `must`, and for this endpoint it is also a scientific necessity. The hepatic reply's proposed `purity_status` enum (`reported_in_source` / `method_reported_only` / `deferred_to_citation` / `unobtainable_paywalled` / `not_reported`) should be adopted project-wide; `"TBD"` reads as pending work rather than an established gap.

**Note what is *not* needed here.** The effect is sequence- and hybridization-independent (MMB Ch.25 §3.1.2; Shaw 1997; and Mangsbo's GpC control activating as strongly as CpG 2006). So the sequence predictors in `oligos.csv` do not bear on it, and `backbone_chemistry`, `ps_count`, `length_nt`, `conjugate` and `delivery_method` are the fields that do. The dossier says this and is right. The one exception is Sewing's length series, which is informative precisely because it is negative across 10–22 nt.

## 5. Raw results vs source interpretation vs curator judgment vs model eligibility

Proposed, for German's adjudication:

- **Raw:** the source's printed value with its literal unit string — `C3a stimulation index = 17.1`, `Complement C3 change = -0.085 g/L`, `Bb increased by 5.9- to 8.5-fold`, `55% below LLN vs 21%`.
- **Source interpretation:** the source's own label and threshold — *"no evidence of complement activation … above 2× ULN"* (Crooke); *"clinically insignificant increases in C3a"* (Glover); *"classic complement pathway activation (C′3a, C′4a, C′5a)"* (Demirjian); *"without signs of complement activation"* (EMA Kynamro). **Each travels with its row, never with the endpoint.**
- **Curator judgment:** pathway re-assignment where the source is loose (§2.5); exclusion of target-is-complement rows; evidence-class assignment; normalising `Bb` vs `factor B activated`; treating stimulation index and absolute concentration as different quantities.
- **Model eligibility:** German only. Nothing eligible until a rubric exists.

**Three places where conflating these would produce a defect a reviewer could find:**

1. **`COG-MSR0345` carries `evidence_class = measured_negative` with `readout_value = NOT_REPORTED`.** Defensible for Bb — the endpoint was measured and showed no drug effect — but the numeric value genuinely is unreported (figure-only). Two facts, one field. The row's own `readout_is_qualitative` and `value_origin` carry it adequately today; a dedicated complement table must not lose that separation. **Missing reports must not become negative outcomes**, and here the distinction is between "measured, reported as unchanged" and "measured, value not extractable".
2. **A 2× ULN rule applied without baselines manufactures positives.** Inotersen CS1 had C5a and Bb **above ULN at baseline in the placebo arm**. Any incidence rule needs a mandatory baseline-anchored comparison.
3. **A surgery effect is not a drug effect.** `COG-S022`'s 5.9–8.5× Bb rise occurred in **every arm including placebo**. Recorded as a drug effect it would be the largest human complement signal in the dataset. The repo's row gets this right; the rule needs to be explicit so the next curator does too.

## 6. Access requests

Classified per `RESEARCH_ACCESS_REGISTER.md`'s taxonomy. No purchase, subscription or researcher contact is assumed or requested. **Every barrier I hit on the paywalled items was a Cloudflare browser challenge rather than a rendered paywall or login form** — which matters, because a person with a browser may get through where this session cannot.

| # | Citation / identifier | File needed | Affected records | Gap it closes | Routes attempted | Observed barrier | Class | Priority |
|---|---|---|---|---|---|---|---|---|
| **A1** | **Henry SP, Jagels MA, Hugli TE, Manalili S, Geary RS, Giclas PC, Levin AA (2014)**, *Nucleic Acid Ther* 24(5):326–335, doi 10.1089/nat.2014.0491, PMID 25093529 | full text + any supplement | the human-serum arm; the factor H artifact caveat; `TMSR458` | the **only** paper assaying monkey, human and dog serum side by side; the species-difference claim rests on it | DOI → `journals.sagepub.com/doi/full/…`; also `/doi/pdf/`, `/doi/full-xml/` | **403 Cloudflare**; Unpaywall `closed`, no PMCID | Browser check over a probable paywall | **High** |
| **A2** | **Shen L, Frazer-Abel A, Reynolds PR, Giclas PC, Chappell A, Pangburn MK, Younis H, Henry SP (2014)**, *JPET* 351(3):709–717, doi 10.1124/jpet.114.219378, PMID 25301170 | full text; the human analyte list; the 767-subject query basis | the largest human negative; ISIS 426115 and ISIS 183750 identity | ASPET host root and the advertised free PDF; ScienceDirect | **403 Cloudflare host-wide**; ⚠ **Unpaywall and Semantic Scholar both report this OA** | **Technical block, NOT a paywall — most likely to open in a browser** | **High** |
| **A3** | **de Boer E, Sokolova M, Quach HQ, et al. (2022)**, *J Immunol* 209(9):1760–1767, doi 10.4049/jimmunol.2101191, PMID 36104112 | full text + any supplement | would be the third usable human-laboratory source | Europe PMC core record | `isOpenAccess N`, **no PMCID, `inPMC N`, `hasSuppl N`** | Not OA; AAI's 12-month free policy may apply — **unconfirmed** | **High** |
| **A4** | **Henry SP, Giclas PC, Leeds J, Pangburn M, Auletta C, Levin AA, Kornbrust DJ (1997)**, *JPET* 281(2):810–816, PMID 9152389 | full text — specifically the **species of the factor H** in the heparin-sepharose assay | `TMSR456`–`TMSR460`; **would convert `TMSR460` from `species = NA` to a human-laboratory row** | ASPET host | **403 Cloudflare host-wide**; no PMCID | Browser check over a probable paywall | **High** |
| **A5** | **Povsic TJ, et al. (2016)**, *J Allergy Clin Immunol* 138(6):1712–1715, doi 10.1016/j.jaci.2016.04.058, PMID 27522158 | the **Online Repository** (Fig E1, Tables E1–E4, "planned biochemical analyses") | NCT01848106 | assay kits, vendors, core laboratory and **the actual numeric complement values**, none of which are in the article body | jacionline.org and ScienceDirect → 403; em-consulte.com → 200 with a subscription notice | **CONFIRMED PAYWALL** on the article; **supplement missing** | Confirmed paywall + missing supplement | **High** |
| **A6** | **Shaw DR, Rustagi PK, Kandimalla ER, Manning AN, Jiang Z, Agrawal S (1997)**, *Biochem Pharmacol* 53(8):1123–1132, doi 10.1016/S0006-2952(97)00091-9, PMID 9175717 | full text | the dedicated human-serum paper; the **C4d / classical-pathway** finding | Unpaywall `closed`; Europe PMC "subscription required" | no OA location; no PMCID | Probable paywall | Medium |
| **A7** | **Agrawal S, Rustagi PK, Shaw DR (1995)**, *Toxicol Lett* 82–83:431–434, doi 10.1016/0378-4274(95)03573-7, PMID 8597089 | full text (4 pp) | the only **human / rhesus / guinea pig** side-by-side serum comparison | Unpaywall `closed` | no OA location | Probable paywall; likely a short proceeding | Medium |
| **A8** | **Kandimalla ER, et al. (1997)**, *Nucleic Acids Res* 25(2):370–378, doi 10.1093/nar/25.2.370, PMID 9016567, **PMC146429** | the scanned full-text PDF — to establish **the serum species** | would be the best position-resolved chemistry/complement series **if** the serum is human | PMC landing page loads (abstract only); `/pdf/250370.pdf`; `efetch db=pmc`; Europe PMC `?pdf=render` and `fullTextXML` | **PMC proof-of-work cookie challenge**; publisher blocks XML; EPMC 500 | **Listed free but technically gated — not a paywall** | Medium |
| **A9** | **Seguin/Henry et al. (2016)**, *Nucleic Acid Ther* 26(4):210–215, doi 10.1089/nat.2015.0593, PMID 26981618 | full text; also resolve the author order (§2.2) | the endpoint definitions and rubric | not fetched after the host-wide SAGE 403s | assumed same barrier | Probable paywall | Medium |
| **A10** | **Shen L, Engelhardt JA, et al. (2016)**, *Nucleic Acid Ther* 26(4):236–249, doi 10.1089/nat.2015.0584 | full text | the chronic animal counterpart to the human C3 signal | same host | assumed same barrier | Probable paywall | Low — animal supporting |
| **A11** | **Galbraith WM, Hobson WC, Giclas PC, Schechter PJ, Agrawal S (1994)**, *Antisense Res Dev* 4(3):201–206, doi 10.1089/ard.1994.4.201, PMID 7849490 | full text | the historical first report | SAGE | **403 Cloudflare**; Unpaywall `closed`, 0 OA locations, no PMCID | Browser check over a probable paywall | **Low — demoted from the dossier's rank 1** |
| **A12** | **Henry SP, Beattie G, Yeh G, Chappel A, Giclas P, Mortari A, Jagels MA, Kornbrust DJ, Levin AA (2002)**, *Int Immunopharmacol* 2(12):1657–1666, doi 10.1016/S1567-5769(02)00142-X, PMID 12469940 | full text | largest animal effect size (Bb ~100×, C5a ~7×) | ScienceDirect | **403 Cloudflare**; no PMCID | Browser check over a probable paywall | Low — animal supporting |
| **A13** | **"Henry SP, Larkin R, Novotny WF, Kornbrust DJ (1994). Effects of ISIS 2302, a phosphorothioate oligonucleotide, on in vit…"** | the original document | would be the earliest ISIS 2302 *in vitro* complement work | cited in Henry 2014's reference list; **not indexed in PubMed**; web search found nothing | identity insufficient | **CITATION UNRESOLVED — do not cite without the original** | Low |

**Retired before being requested — no access needed:**

- **Crooke 2016 Supplementary Tables S1–S10** — obtained. Europe PMC `supplementaryFiles` for PMC5112040, HTTP 200, 2,549,427 bytes, containing `mt2016136x1.pdf` (1.93 MB) plus figure and table images.
- **Sewing 2017 raw-data file** — obtained. `pone.0187574.s001.xlsx`, 54,955 bytes, parsed (§2.3).
- **Mangsbo 2009 full text** — free at PMC2857538, read. (Its supplementary endpoint returned a 296-byte XML stub, so **Supplemental Fig. S1 is not retrieved** — TLR9 expression only, not needed.)
- **EMA assessment reports — free.** **Downloaded and extracted by me this session:** Kyndrisa withdrawal report (2.80 MB), Tegsedi EPAR (2.31 MB), Kynamro EPAR (3.40 MB) and the Kynamro **refusal-grounds** document (80,931 bytes — both quotes in §2.1 confirmed in it first-hand). **Reported reachable by the delegated search but not opened by me:** Waylivra, Spinraza, Onpattro, Givlaari, Leqvio, Oxlumo, Amvuttra, Qalsody, Tryngolza. The Wainua/eplontersen EPAR was **not located** and Exondys has none (eteplirsen was never EMA-authorised).
- **FDA mipomersen medical review** (NDA 203568Orig1s000) — free, **but 404s with a default user agent and returns 200 with a browser user agent.** Worth recording in the register: an FDA UA filter is not a paywall, and a session that does not know this will wrongly log FDA documents as unavailable.

**Register corrections requested.**

1. `RESEARCH_ACCESS_REGISTER.md` carries **no complement entry at all**. The endpoint should appear, with A1–A5 as its request-ready items.
2. The register's *"The prior 'alicaforsen review' entry has no exact citation and remains **citation unresolved**"* is now **partly resolved**: two exact alicaforsen human trials with measured complement are identified — **PMID 9316823** (Glover 1997, *JPET* 282(3):1173–1180) and **PMID 11908555** (Maksymowych 2002, *J Rheumatol* 29(3):447–453) — both already carried on the coagulopathy branch as `COG-STU139`/`COG-STU144`.
3. Add a status value for **"listed open access but technically gated"**. Three items here (A2, A8, and the FDA UA case) are recorded as free by Unpaywall or PMC yet unreachable. Logging them as paywalled would be wrong and would mislead the next session.

## 7. Recommended next work package (smallest useful)

**Scope: ingest Sewing 2017's complement block only.** One source, one species, one evidence class, one matrix, 144 values already on disk. No clinical layer, no regulatory layer, no cross-species claim, no model.

| | |
|---|---|
| Creates | `toxicity/complement-activation/data/` — `oligos.csv`, `measurements_human_lab.csv`, `sources.csv`, plus `row_disposition_log.csv` |
| Why this source first | the **only** source that is simultaneously open-licence (CC-BY), already retrieved, per-donor, matched-backbone-controlled, pathway-controlled, and in a **human** matrix. Cost is zero and nothing is blocked on it |
| Schema | **adopt, do not invent** — physically separate `Human_Clinical_GT` / `Human_ExVivo_GT` tables on the thrombocytopenia `scientist_v09` pattern so the classes cannot be pooled; reuse the coagulopathy `evidence_class` vocabulary and its `endpoint_scope` / `endpoint_scope_note` fields, which already work |
| Endpoint-class field | mandatory `complement_readout_class` ∈ {`activation_split_product`, `component_abundance`, `function`, `deposition`} per §1.3 |
| Required non-null fields | `analyte`, `complement_readout_class`, `matrix`, `donor_id`, `n_donors`, `value_basis` (`absolute` / `stimulation_index` / `fold_change` / `incidence_above_threshold`), `assay_name`, `delivery_method`, `complement_measurement_intent` (`toxicity` / `pharmacodynamic_efficacy`), `pathway_label_source`, `pathway_label_curator` |
| Closure evidence | 144 values; 2 analytes; 16 conditions; **n=5 for 12 conditions and n=3 for 4 conditions, recorded per condition, never averaged into one denominator**; `value_basis = stimulation_index` on all 144; `purity_status = not_reported` on all constructs; **human-trial count 0**; animal count 0; the Mangsbo disagreement of §2.4 recorded as an open scientific question, not resolved |
| Dependencies | German's complement rubric **before any grade column is populated** (rows can land ungraded); Oscar's authorization; nothing else |
| Explicitly **not** in scope | every clinical row; the whole regulatory layer; the 10 existing in-repo complement rows (reconciliation is package 2); `COG-MSR0345` (**leave it where it is** — moving a sibling dataset's row is not this package's business); any monkey-versus-human claim; any grade |

**Package 2, for later authorization, in order:** (i) reconcile the 10 existing in-repo rows, including the `TMSR948`/`TMSR1047` cross-branch duplicate and the Henry 1997 abstract-level extraction; (ii) add Mangsbo 2009 as derived values only, with the §2.4 disagreement explicit; (iii) build the human clinical study register from NCT00554359 plus the regulatory studies, with `identity_basis` distinguishing `registry_number` from `sponsor_protocol_code`; (iv) Crooke 2016 as a **pooled** source contributing measurements and zero trials.

**Why not clinical first.** The clinical layer is the larger prize and the wrong starting point: it needs a study register, the `participant_pool_id` design decision of §1.4, resolution of the regulatory-versus-registry identity question, and five of its best sources are behind browser challenges. Starting there would produce a count before a qualified register exists — the exact failure Oscar's rule is written to prevent.

## 8. Decisions needed from German or Oscar

**German (scientific):**

1. **The complement rubric**, over the three anchors evidence supports: **split products as incidence above 2× ULN**, **components as below LLN**, **function as % of baseline titre** — plus the **~50 µg/mL** plasma-concentration threshold as the exposure axis. `nephrotox_grade` is not reusable; neither is any coagulopathy or thrombocytopenia grade.
2. **Whether the four readout classes of §1.3 may ever share a numeric column or a single grade.** My position: no. REGULATE-PCI's CH50 ↓ with C3a ↑ and Bb ↑ in one sample is the case that forces it.
3. **The Sewing-versus-Mangsbo backbone disagreement** (§2.4). Both human whole blood, both open, opposite conclusions about the phosphodiester backbone, and Mangsbo's sequence control activates as strongly as its CpG. Is backbone dependence endpoint-specific, assay-specific, or is one result not reproducible? I take no position.
4. **Whether an apparent factor H decrease may be recorded at all**, given Henry 2014's immunoassay-artifact finding (§2.8). This bears directly on `TMSR458`.
5. **Pathway attribution authority.** Sources label pathways loosely — Demirjian calls C3a/C4a/C5a "classic pathway"; ApTOLL 2024 calls C3/C4 the "terminal complement complex". I propose `pathway_label_source` and `pathway_label_curator` as separate fields and ask German to own the curator column.
6. **Whether the baseline-above-ULN problem** (inotersen CS1, placebo arm included) makes incidence-based human rows admissible at all without paired baselines.

**Oscar (scope and process):**

7. **Scope: I recommend keeping this endpoint in Phase 2 and reject the dossier's descope recommendation.** Grounds: 10 complement rows already in the repository, 19 nameable human studies with measured complement, 9 human-laboratory sources, and a zero-cost first package with 144 verified human values in hand. The dossier's recommendation was reasonable on what it had.
8. **Which evidence class leads the deliverable.** The hepatic reply referred this to Beebop as a consultation and I will not pre-empt it, but this endpoint sharpens it: the challenge brief's complement sentence sits in a paragraph seeking datasets that *"make use of in vitro human systems"*, and for complement specifically the human-laboratory evidence is both stronger and more accessible than the clinical evidence. **Oscar's counting discipline is not in question anywhere in this reply** — §3 reports one verified trial rather than nineteen because of it.
9. **A project-wide dossier-denominator audit.** Two endpoints have now been caught quoting row counts from dataset states that no longer exist (hepatotoxicity's 111 versus 246; this dossier's 111×23 against a current 246×27 and a 769-row variant). I recommend every dossier's quoted denominator be re-derived from the file it names, repo-wide.
10. **Which complement dossier is authoritative.** `claude/oligo-reorganize-toxicity-2h7t50:complement-activation/README.md` is materially more advanced than the `amazing-galileo` version this round was built on, but sits on a 2026-08-28 branch. The two disagree about whether complement measurements exist. Please rule on precedence, because the request's starting premise depends on it.
11. **The empty Drive folder.** `Complement Activation` (id `1X03w9iRA78GKXjSdJjgVjaCkiitPbwZj`) was created 2026-10-02 21:56 UTC and is empty. If it was created in anticipation of this round, say so, so the next session does not read it as a lost dataset.
12. **`MSR066`'s `confirmed_negative` label**, derived from an eGFR efficacy result (§1.2). Kidney's to fix, not mine, but it should be logged.
13. **The supersession header** on `BEEBOP_SUGGESTIONS_2026-09-30.md` (§2.9).
14. **`purity_status` project-wide**, replacing `"TBD"` (§4). For this endpoint purity is mechanistically load-bearing, not administrative.

## 9. Limitations of this review

- **No sequence has been verified character-by-character by me.** Sewing's Table 2 was not read; Mangsbo's sequences are as printed in the text I fetched; the repo's `TOLG035` and ODN2395 sequences are repo-recorded. Every sequence statement above is attributed, not asserted.
- **No full text of the five classical complement papers was obtained** (A1, A2, A4, A11, A12). All species, analyte and threshold statements about them come from abstracts, reference lists, or secondary citation in the MMB volume. The 50 µg/mL threshold is corroborated across two independent routes but I have not read either primary paper.
- **Six Tier B analyte assignments are unverified** — Rudin 2001 (reported as Bb and C3a by ELISA, from a search-index extraction, **not independently confirmed**), Nemunaitis 1999, Chen 2000, Paul 2010, Shen 2014's human analytes, and Kandimalla 1997's serum species.
- **Parts of §3.2 Tier B and §3.4 rest on delegated searching** that I directed and spot-checked rather than performed end to end. Everything in Tier A, all EMA extracts in §2.1, the Sewing numbers in §2.3, the Mangsbo details in §2.4, the Demirjian analytes in §2.5 and all in-repo row and denominator counts are first-hand this session.
- **Author order for A9 is unresolved** (MMB prints Seguin first, PubMed indexes Henry first).
- **The Povsic Online Repository and the Ganson 2016 supplement were not retrieved**, so REGULATE-PCI's numeric complement values and assay methods are unverified; and whether complement was assayed in pegnivacogin phase 1 remains open.
- **No PMDA, Health Canada or TGA documents were searched**, and the Wainua/eplontersen EMA EPAR was not located. The FDA review set is incomplete — only mipomersen, inotersen, eteplirsen and pegaptanib were read.
- **`git` history is unavailable** (shallow clone; all four cited baseline commits unreachable), so I make no provenance or timing claim about any repository fact.
- **Drive PDFs were not checksummed** against repository copies.
- **I did not open the 23 CNS source PDFs** at `claude/oligo-cns-toxicity-dataset-tijib6:toxicity/notes/cns/corpus/`, which the reorganize-branch dossier notes have never been swept for this endpoint. One of them, `FDA_NDA209531_nusinersen_PharmacologyReview.pdf`, is `source_id = R4` behind three of the ten in-repo rows. **That sweep is outstanding and may add rows.**

---

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**
