# Rocksteady → Beebop: Complement activation research report

Research round: `2026-10-02/complement-activation`.
Date: October 3, 2026. Status: **RESEARCH ONLY — NO DATASET, LABEL, SCHEMA, ADJUDICATION OR MODEL CHANGED.**
Reply location: `claude/amazing-galileo-rwiv95:toxicity/complement-activation/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md`.

## 0. Baseline, and what was actually done

| | |
|---|---|
| Branch | `claude/amazing-galileo-rwiv95` |
| Commit at which this report's inventory is pinned | `e4eb59e770bdd54af9fdf14654bf0660abc4677b` |
| Review snapshot addressed | `6c5797a2590e163aa8ce9fab7f3437117a9aa0e0`, as Beebop's request specifies |
| Dedicated complement dataset | **still none — 0 ingested rows.** This round created no dataset. |
| Search coverage | **20 of 20** compendium resources logged; 14 genuinely searched, 4 blocked, 5 judged inapplicable with justification (one resource is both searched and inapplicable) |
| Primary sources verified first-hand this round | 9 full texts, 4 regulatory assessment reports, 2 supplementary data files |
| Work banked | `research-staging/working/` — six machine-readable files, committed so a restart cannot destroy them again |

**A process failure to disclose up front.** My first attempt at this round was a 54-agent workflow. This container has **4 CPUs**, so its concurrency cap is **2**; the run was effectively serial, and a container restart killed it with **52 of 54 agents unfinished**. Two sweeps survived in the journal and were recovered. I re-planned into small banked batches. The loss is mine, not the environment's: I sized the work for a concurrency that does not exist here. Everything below is from the re-planned batches plus the two recovered sweeps.

**Seven corrections to the 2026-10-01 reply.** Beebop found three. This round found four more, and two further ones emerged while writing. All are recorded in §7. The reply was directionally right that the endpoint is evidence-rich and wrong in most of its specific counts.

## 1. Proposal dispositions

### Proposal 1 — Prioritize Sewing 2017 S1 Figure 6 and Mangsbo 2009; separate donors, replicates, analytes, controls and ratios; coordinate with thrombocytopenia's existing file and checksum

**ACCEPT in full, and executed.** Every sub-clause was right, including the two I would not have thought of.

- **The unit discipline is correct and I can sharpen it.** The 144 cells are **2 analytes × 16 conditions × 3–5 donors**, triplicate wells already averaged before the ratio is formed. Beyond Beebop's point: **6 of the 144 are PBS normalisers fixed at exactly 1.000 with zero variance**, so only **138 values across 15 conditions** carry information. The PBS column is the denominator, not an observation.
- **Shared acquisition honoured.** The file is the same one behind thrombocytopenia's `EXV-TMB-051`/`EXV-TMB-052` on `claude/oligo-challenge-data-4um5mi`. One acquisition, two endpoints. Committed once, with `sha256 cd4d4b092e112982cb3ab56e6de88101d523933dcf147185c20a829a71f6a3fc` recorded so that branch can reconcile against identical bytes. No duplicate download.
- **Verified negative worth having:** complement appears in **only** sheet `Figure 6` of the six-sheet workbook. The other five sheets contain no complement analyte. So 144 is the file's complete complement content, not a sample of it.

**What verification found that changes the plan — a defect in the source itself.** Table 2's legend reads *"\* phosphothioate backbone; **bold letters: locked nucleic acid**"* (the misspelling is the authors'). **There is no bold anywhere in Table 2's sequence column.** Confirmed three independent ways: the publisher JATS XML contains zero `<bold>` elements in Table 2; the PDF embeds no bold monospace font, page 7 using only `CourierNewPSMT` regular; and the publisher's table image shows no bold glyph. Consequently `(AC)8 LNA` is **character-identical** to `(AC)8`, and likewise for the 18- and 20-mers.

**The legend is orphaned, so Table 2 alone cannot say which positions are LNA.** The 3-wing gapmer placement is recoverable only from prose — Methods: *"had three flanking LNA modifications on each side"*; Results: *"flanking three nucleotides of (AC)8, (AC)9 and (AC)10"* — and must be carried as a **flagged inference**, never presented as transcribed. This matters because Phase 2 requires "the location of all chemical modifications in each oligo" as a *must*: for 3 of this source's 12 constructs that location is **inferred, not readable**. My 2026-10-01 characterisation of Sewing's chemistry as "category-level" was too generous.

Verified Table 2, triple-sourced and arithmetically validated on all 12 rows (length = base count; asterisks = length − 1 for the 11 PS oligos, 0 for the one phosphodiester):

| Name as printed | nt | Sequence |
|---|---:|---|
| `ODN2395_Thio` | 22 | `T*C*G*T*C*G*T*T*T*T*C*G*G*C*G*C*G*C*G*C*C*G` |
| `ODN2395` | 22 | `TCGTCGTTTTCGGCGCGCGCCG` |
| `(AC)5` … `(AC)11` | 10,12,14,16,18,20,22 | `A*C*` repeats, fully phosphorothioated |
| `(AC)8/9/10 LNA` | 16,18,20 | character-identical to the non-LNA rows — see above |

The repository's recorded ODN2395 sequence `TCGTCGTTTTCGGCGCGCGCCG` is **confirmed character-for-character**. Two naming corrections: Table 2 writes `ODN2395_Thio` with an underscore while the running text uses a space, and **"ODN2395-PO" is my own paraphrase appearing nowhere in the paper** — the real pair is `ODN2395_Thio` (PS) and `ODN2395` (phosphodiester), identical bases, backbone the only difference. A clean backbone-isolating pair, attributed by the authors to Flierl U et al., *J Exp Med* 2015;212(2):129–37, PMID 25646267.

The 16 supplement labels now map to named constructs, validated against the figure axis categories and reconciling to exactly 144 values: `+ PS`→`ODN2395_Thio`; `- PS`→`ODN2395`; `10`…`22`→`(AC)5`…`(AC)11`; `16/18/20 LNA`→`(AC)8/9/10 LNA`; **`Class. Path.`→HAGG (heat-aggregated gamma globulin, TECOmedical)**; **`Alt. Path.`→Zymosan (Sigma)**. One label is unresolved: **`Inhib.` — its position and its 0.1–0.5 SI are certain, its reagent identity is never stated.**

Method fields now pinned: **Quidel/TECOmedical Human Complement Plus EIA, C3a Cat. A015 and C5a Cat. A025**; Versamax reader, Softmax Pro 5.2; 195 µL whole blood + 5 µL of 40× stock, triplicate, 37 °C/5% CO₂, **complement sampled at 45 min**, blood used within 3 h. **Stimulation Index = treated ÷ that same donor's PBS vehicle control** — established empirically, since PBS is exactly 1.000 with zero variance for both analytes. **No absolute concentration is printed anywhere**, so the native unit is UNVERIFIED and these values must never be recorded as ng/mL.

An unreconciled discrepancy to carry: Methods says *"the 3 donors"*, the Figure 6 legend says *"n = 5"*, and the supplement holds a mix of 3 and 5. The paper never explains it. **Treat per-condition n from the supplement as authoritative.**

### Proposal 2 — Follow COG-MSR0345 to NCT00554359, Figure 2 and the other three analytes; distinguish surgical from drug effect; research the two alicaforsen PMIDs and regulatory monitoring with explicit observation windows

**ACCEPT, with the surgical-confound point strengthened, and one part I could not complete.**

Confirmed first-hand from `PMC5733816`: the trial measures **four** analytes — Bb, C3a, C4a, C5a — in plasma at screening and 5/15/30 min and 1/2/4/8/24 h. Three are recorded nowhere in the repository.

**Beebop's confound warning is right and sharper than stated.** The Bb rise is not merely "also in placebo" — it is *pre-dose*: *"mean **postoperative, predose** levels of alternate pathway activated factor B (Bb) increased by 5.9- to 8.5-fold compared with baseline (screening) levels **in all groups**, consistent with the previously described impact of on-pump bypass surgery."* The elevation is established **before study drug is given**. So this is not a drug effect with a placebo comparator; it is a **surgical effect measured across a drug/placebo split**, and the only drug-attributable statement available is the absence of a between-group difference. Recorded as such.

Also confirmed: the source's own pathway label is biologically loose — it calls C3a, C4a and C5a *"classic complement pathway activation"*, when C3a and C5a are common-pathway products. **Source pathway label and curator pathway assignment must be separate fields.** The same defect recurs in the ApTOLL 2024 paper, whose results text calls C3 and C4 the "terminal complement complex".

**Not completed:** the Figure 2 numbers. They exist only in the figure, and I will not digitise a plot — that manufactures precision the source does not publish. The analyte list, timepoints, direction and verbatim result are captured; the values are not available and should be recorded as `figure_only`.

The two alicaforsen studies are resolved as citations (Glover 1997 PMID 9316823, *JPET* 282(3):1173–1180; Maksymowych 2002 PMID 11908555, *J Rheumatol* 29(3):447–453) but **both remain abstract-level** — neither full text was obtained, so analyte detail, assay and denominators stay UNVERIFIED. Regulatory monitoring windows are in §2 and the register.

### Proposal 3 — Reconcile every proposed clinical study in an identifier-level register; the headline 19 does not reconcile; pooled 750/767 cannot substitute for named trials

**ACCEPT without reservation. Beebop is right, the 19 was wrong, and the register surfaced a structural problem neither of us had.**

The arithmetic failure is confirmed: three table rows each carried two named studies and three entries were pools. **21 named studies + 3 pooled sources**, not 19. §3 rebuilds it properly.

**The structural finding: zero registry identifiers in the regulatory record.** A regex for `NCT\s?0?\d{7,8}` over the full text of all four EMA assessment reports returns **0 hits in each**:

| Document | Pages | NCTs | Identification used |
|---|---:|---:|---|
| Kyndrisa (drisapersen) withdrawal AR | 105 | **0** | `DMD1140xx`, `PRO051-0x` |
| Tegsedi (inotersen) EPAR | 142 | **0** | `ISIS 420915-CSn` |
| Kynamro (mipomersen) EPAR | 114 | **0** | `ISIS 301012-CSn`, `MIPO35xxxxx` |
| Waylivra (volanesorsen) EPAR | 121 | **0** | `CSn`; animal `304801-ASnn` |

The regulatory record holds **the only chronic human complement data in the field** and identifies every study by **sponsor protocol code alone**. Those codes satisfy Oscar's "documented stable study identifier" basis, but **cross-linking them to a registry is a separate, unperformed step**, and until it is done no regulatory study can be reconciled against a registry-derived count. This is a real dependency.

It also corrected the rosters: **drisapersen has ten named studies**, not the five or six I listed — `DMD114117` (71 mentions) and `DMD115501` were missed entirely. **Inotersen has three, not two**: the EPAR's own abbreviation list defines `CS1` = Clinical Study 1, **`CS2` = Parent Study**, **`CS3` = OLE Study** — a **parent/extension pair that must never be summed**, which is exactly the extension-counting convention Beebop asked for. Volanesorsen's complement comparison has **no stated denominator** (the `3 of 8` and `18 of 23` figures I had leaned on are platelet counts). And mipomersen's study-level attribution is **FDA-sourced** while its EMA statements attach to no named study — two regulators, two attributions, which my reply did not distinguish.

**On planned versus reported monitoring, which Beebop asked me to separate:** the registry sweep found this distinction is load-bearing. `NCT05071300` (eplontersen, Phase 3) carries complement in a **primary** outcome measure but has **no results posted**; `NCT05276297` (bepirovirsen) names complement activation only inside an **AESI description**, which is an adverse-event term, not an analyte measurement. Neither is a reported measurement. Against that, `NCT02363946` and `NCT03728634` are **registered complement outcomes with results posted** — see §3.

### Proposal 4 — Correct the sequence denominator; AR177 cannot count toward twelve human compounds; keep administered sequence mandatory alongside chemistry, conjugate, formulation, concentration and characterization; sequence independence is not established

**ACCEPT all four clauses. The denominator correction is conceded, and I withdraw the sequence-independence claim — though the evidence for it got stronger, not weaker, which I report rather than hide.**

AR177/zintevir is an animal construct and had no business in a human denominator: **1 of 12**, not 2 of 12. Conceded in the published addendum.

On the mandatory field list, this round adds two items from evidence rather than principle. **Formulation**: ARC-520's delivery excipient is a masked hepatocyte-targeted polymeric amine (NAG-MLP), and CALAA-01 is a cyclodextrin-polymer nanoparticle — in both, formulation is a candidate complement driver independent of the oligonucleotide. **Anticoagulant**: see §6; of six human complement sources, three do not report it, one contradicts itself, and those that do report use agents that themselves perturb complement.

**On sequence independence I accept Beebop's instruction and withdraw the dataset-level claim — and must report that the human evidence has since strengthened.** Two independent human-blood sources now carry explicit sequence controls and both find the control as active as the CpG:

- **Mangsbo 2009**, Figure 1 title verbatim: *"**CpG- and GpC-induced** complement activation results in increased levels of C3a and C5a"*; Discussion: *"The expression was complement-dependent rather than oligo sequence-specific as demonstrated by a similar up-regulation with GpC."*
- **de Boer 2022**, verbatim: *"GpC-A, -B and -C changed sC5b-9, C3bBbP and C3bc to the same extent as CpG-A, -B and -C, **indicating a DNA-backbone-dependent effect**."*

So the position I now hold is Beebop's, for Beebop's reason plus a stronger one: Phase 2 exists to let sequence and modification data support prediction, and its dataset "must contain the sequences of all oligos tested, as well as the location of all chemical modifications". A dataset that declares the primary predictor irrelevant in its own narrative undercuts its submission. **Record the full sequence and per-position chemistry for every construct, carry sequence-independence as per-row source-reported interpretation, and let the distribution speak.** German adjudicates whether it generalises.

### Proposal 5 — Keep activation fragments, component consumption, functional activity and tissue deposition separate; preserve matrix, anticoagulant, handling, donor, baseline, assay and timepoint; serum and whole blood are not interchangeable; thresholds need German

**ACCEPT entirely. This round produced three new exhibits for it, and one of them resolves a contradiction I had flagged.**

**Exhibit 1 — a second instance of split products up while function goes down.** Beyond REGULATE-PCI's CH50↓ with C3a↑ and Bb↑, the Kyndrisa report states for monkeys: *"the complement system was activated (**complement split factors C3a and Bb**), but the **concomitantly decreased total complement activity** suggests functional impairment of the cascade."* Two independent instances. Activation and function cannot share a column or a grade.

**Exhibit 2 — matrix is analyte-specific within a single study.** ARC-520, verbatim: *"Venous blood samples were collected and processed to produce **serum** (for complement CH50 analysis) **or plasma** (for split products-Bb analysis)."* One trial, two matrices, chosen per analyte. "Serum vs whole blood are not interchangeable" understates it — serum vs plasma is not interchangeable *within one study*.

**Exhibit 3 — the apparent Sewing/Mangsbo contradiction largely dissolves on method-level reading, and de Boer resolves the rest.** My 2026-10-01 §2.4 framed these as contradicting each other on backbone dependence. With all three read at method level:

| | Sewing 2017 | Mangsbo 2009 | de Boer 2022 |
|---|---|---|---|
| Matrix | whole blood, plasma for ELISA | whole-blood loop + hirudin plasma | whole blood + plasma |
| Anticoagulant | **"anticoagulant-sprayed" — identity not reported** | heparinised surface **+ soluble heparin 0.5 U/mL**; EDTA 10 mM stop | **lepirudin 50 µg/mL**; EDTA 10 mM stop |
| Analytes | C3a, C5a | C3a, C4a, C5a | sC5b-9, C3bBbP, C3bc |
| Readout | Stimulation Index (ratio) | absolute, CBA | absolute |
| PS backbone | **activates** | **activates** | **activates** (CpG-B, CpG-C) |
| Phosphodiester / non-PS | **inactive** | activates, **via the classical pathway** | CpG-A (mixed PO/PS) **inactive** |
| Sequence control | not tested | **activates equally** | **activates equally** |

The three agree that **PS backbone activates and sequence does not matter**. They differ only on whether a non-PS backbone can activate, and Mangsbo's answer is pathway-specific — its own Results heading reads *"Phosphorodiester CpG activates complement via the classical pathway while phosphorothioate CpG utilizes either the classical or alternative pathway **depending on blood donor**."* So the live scientific question is not "do they contradict" but **"under what matrix, concentration and time can a phosphodiester backbone engage the classical pathway"**, plus the donor-dependence of pathway choice. That is a much better-posed question for German, and I restate it as such in §7. Note de Boer's CpG-C **is** ODN 2395, Sewing's compound — so the two agree on the same molecule.

Also confirmed for the record: **C4a was NOT elevated** in Mangsbo at 1 h, and no other C4a timepoint was reported, so any C4a claim at 15 min or 6 h is UNVERIFIED. Analyte-level resolution matters; "anaphylatoxins" cannot be collapsed.

**On thresholds, I accept the instruction and narrow my earlier position.** No threshold enters the dataset this round. Phase 2 asks for measured values, their distribution and positive/negative controls — not a graded label. One point of record stands: **2× ULN is Crooke's *human* Table 2 convention and "below LLN" is the EMA *human* reports' convention**; only the ~50 µg/mL figure is animal-derived, and that one must never become a human rule. Calling all three "animal exposure cutoffs" would mislead a later reader about provenance. German owns the rubric at modelling time, which the Work-Plan schedules per endpoint as "Finish ML".

### Proposal 6 — Prioritize the inaccessible Henry 2014, Shen 2014, de Boer 2022 and Povsic 2016 including supplements; distinguish technical blocking from paywalls; verify entitlement and price rather than copying assumed categories; phrase any conjugate-era absence as a bounded search result

**ACCEPT, and this proposal was the most valuable of the six because its last clause caught a real error of mine.**

**de Boer 2022 is obtained** — a green open-access accepted manuscript under CC-BY 4.0, via a non-obvious route after the publisher host, the AAI legacy hosts and two institutional PDF links all returned Cloudflare 403. It is now our **third usable human-laboratory source** and the one that settles the backbone question. Details in §5.

**Henry 2014 and Shen 2014 are no longer blocking**, for a reason I would have missed without reading the regulatory record: the Tegsedi EPAR **summarises both, with citations**, verbatim —

> *"The potential for complement system activation appears to predominate in monkeys, because the **binding of ASOs to complement factor H (CFH)** has been demonstrated, which releases the inhibition of constitutive activation of the alternative complement pathway (**Henry et al., 2014**). Monkeys are more sensitive than humans to this stimulation because of the **~3-fold higher inhibitory capacity of 2'-MOE ASOs to monkey CFH** compared to the CFH of other species (**Shen et al., 2014**). As the inotersen exposure was at least 3-fold higher in monkeys than in patients at the recommended therapeutic dose, the CHMP considers that the potential for complement system activation in humans is minor."*

The mechanism and the species figure are now citable from a **free, regulator-adjudicated** source. The primaries are still wanted for analyte-level detail, assay methods and any sequences, but they move from *blocking* to *desirable*. Note the EPAR frames the 3-fold as the ASO's inhibitory capacity *against* monkey CFH; that is not word-for-word how a secondary summary framed it, so the EPAR is quoted as the EPAR and the two framings are not blended.

**On price and entitlement: nothing was verified, so nothing is recorded.** No price, subscription offer or entitlement was displayed anywhere in this round. Every access status in §5 is recorded as a **block type**, never as a price. No account was created, nothing was purchased, no author or sponsor was contacted.

**On the bounded-search clause — Beebop was right and I was wrong.** My §2.7 asserted that the GalNAc-conjugated generation has **no** human complement measurement at all. That was generalised past the EMA documents I had actually checked. **PMID 30570431 / `PMC6386089`** is an integrated clinical assessment of GalNAc3-conjugated 2′-MOE ASOs in healthy volunteers that **measures Bb and C5a**. Verified first-hand. The claim cannot survive it and is withdrawn. Phrasing matters exactly as Beebop said: the defensible statement is *"of the nine EMA assessment reports listed in §4, none reports a human complement measurement"* — a bounded result naming its documents.

## 2. Current inventory at commit `e4eb59e`

### 2.1 In the repository

| Class | Count | Basis |
|---|---:|---|
| Dedicated complement dataset rows | **0** | nothing ingested; this round was research only |
| Complement measurement rows anywhere in the repo | **10** | 1 human + **8 animal** + 1 unresolved species — corrected from the reply's "7 animal" |
| Human complement rows | **1** | `COG-MSR0345` (Bb), coagulopathy branch, `endpoint_scope = scope_adjacent` |
| Human trials in-repo with measured complement, identity-resolved | **1** | `NCT00554359`, full text staged as `COG-S022` |
| Human complement results in the repo only as study-level free text | **2** | `COG-STU139`, `COG-STU144` — no measurement row exists for either |
| Analytes measured by an in-repo source but recorded nowhere | **3** | C3a, C4a, C5a of `COG-S022` |
| Dedicated complement source PDFs | **0** → **1** | Sewing 2017 S1 now committed under CC-BY |
| Complement rows in the kidney dataset | **0** | confirmed on the current 246 × 27 file |

### 2.2 Human clinical studies with a measured complement analyte, by identifier basis

Classes are mutually exclusive. **No total below is offered as a headline trial count** except the one row that says so.

**A. Registry-identified (NCT), complement measured and reported — 6**
`NCT00554359` QPI-1002 (Bb, C3a, C4a, C5a) · `NCT01872065` ARC-520 (Bb plasma, CH50 serum) · `NCT04742062` ApTOLL (CH50, C5b-9) · `NCT05569720` ApTOLL (C3, C4, CH50) · `NCT00689065` CALAA-01 (Bb, CH50) · `NCT01848106` REGULATE-PCI (C3a, C4a, C5a, CH50, Bb)

**B. Registry-identified, complement a registered outcome WITH RESULTS POSTED — 2, both new this round**
- **`NCT02363946`** ARC-AAT (Arrowhead RNAi), Phase 1, TERMINATED, **`hasResults = TRUE`**; secondary outcome *"Mean Percentage Change in Circulating Blood Levels of Complement Factors 2 Hours Post-Dose"*. Diphenhydramine 50 mg given 2 h pre-dose.
- **`NCT03728634`** Ionis Phase 1/2, COMPLETED, **`hasResults = TRUE`**; primary outcome description states *"Laboratory parameters included measurement of blood chemistry, hematology, coagulation, **complement**, or urinalysis parameters"*.

These are the highest-value unexploited items in the whole endpoint: **registered complement outcomes with posted registry results** means extractable numbers with a registry identifier attached. **Neither has been extracted.**

**C. Registry-identified, complement registered but no results posted — 2** · `NCT05071300` eplontersen Phase 3 (complement in a **primary** outcome) · `NCT05293236` ApTOLL COVID-19, TERMINATED

**D. Complement named only as an AESI term, not an analyte — 1** · `NCT05276297` bepirovirsen. **Not a measurement.** Recorded to prevent a later session scoring it as one.

**E. Publication-identified, no registry (pre-registration era) — 7** · Glover 1997 · Maksymowych 2002 · Rudin 2001 (ISIS 5132) · Advani 2005 (aprinocarsen) · Nemunaitis 1999 · Chen 2000 (GEM231) · LJP 394 PMID 9034989

**F. Sponsor-protocol-identified (regulatory record only) — 11** · drisapersen `DMD114876`, `DMD114044`, `DMD114118`, `PRO051-02`, `DMD114349` · inotersen `CS1`, `CS2` (parent), `CS3` (OLE) · mipomersen `MIPO3200309` + phase 3 programme excluding `CS5` · volanesorsen `CS6`/`CS16`

**G. Pooled, NOT countable as trials — 3** · Crooke 2016, 750 subjects, no identifiers · GalNAc3 integrated, 392 randomised / 350 analysed, **zero NCTs and zero protocol codes** (`grep -c` = 0 on both full text and the 53-page supplement) · Isis Clinical Safety Database, 767 subjects

**H. Provenance too weak to count — 1** · suvodirsen/WVE-210201 Phase 1, sole source a corporate press release

**Headline figures, stated with their criteria.**
- **Verified human trials with a measured, reported complement analyte and a recoverable identifier: 8** (A + B).
- Named human studies with a measured complement analyte across all identifier bases: **26** (A+B+E+F), of which **11 exist only in the regulatory record** and **none of those 11 carries a registry identifier**.
- **Countable toward a headline trial total today: still only the 8 of A + B**, because no qualified study register exists yet and E and F need the identifier work of §3.
- **Pooled participants that must never be summed: 750, 767 and 350.** Overlap is real (all Ionis-era 2′-MOE) and **unquantifiable from the sources**; they are non-additive and I make no combined figure.

⚠ **An unresolved discrepancy I will not paper over.** One verifier stated Crooke 2016 pooled "52 trials and >2,600 subjects"; I verified **750** first-hand from `PMC5112040`. The figures may describe different denominators or different papers. **Neither is used until reconciled.**

### 2.3 Human laboratory — the count falls from 9 to 7, and usable sources rise from 2 to 3

The reply's 9 was inflated by counting one research programme five times. Verified: PMID 9873494 (Kandimalla 1998), PMID 9175717 (Shaw 1997), PMID 8597089 (Agrawal 1995), PMID 9016567 (Kandimalla 1997 *NAR*) and PMID 8931938 (Yu 1996) are **one Hybridon/UAB cluster** — same authors, same laboratory, same hemolytic assay lineage, near-identical titles, same two endpoints. Assume dependence.

| Source | Matrix | Anticoagulant | Analytes | Direction | Access |
|---|---|---|---|---|---|
| **Sewing 2017** | whole blood | **not reported** | C3a, C5a (SI) | PS positive; PO, length series, LNA negative | **CC-BY, in hand** |
| **Mangsbo 2009** | whole-blood loop + hirudin plasma | heparin surface + **0.5 U/mL** | C3a, C4a, C5a | positive; PO via classical; GpC equal | **free, no CC licence** |
| **de Boer 2022** | whole blood + plasma | **lepirudin 50 µg/mL** | sC5b-9, C3bBbP, C3bc | CpG-B/C positive, CpG-A negative; GpC equal | **obtained, CC-BY** |
| Henry 2014 | monkey, **human**, dog serum | not reached | AP activation, factor H | human absent | confirmed paywall |
| Shen 2014 | monkey and **human** serum + in vivo | not reached | AP activation, factor H IC50 | human absent | technical block |
| Paul 2010 | whole blood, Chandler loop | UNVERIFIED | UNVERIFIED | aptamers negative | closed |
| **Hybridon/UAB cluster** (5 papers) | human serum | UNVERIFIED | hemolytic complement, C4d | positive, linkage-dependent | closed |

**7 independent sources; 3 reachable and usable today, up from 2.** Separately, one **grey-literature** human dataset was found and is held apart from the seven: AACR 2025 Abstract 7276 (doi `10.1158/1538-7445.am2025-7276`) with EUROTOX companion LP-31 — ex vivo fresh circulating human whole blood, **6 donors**, 1/5/25 µM, **C3a and C5a**, in which **imetelstat at 25 µM significantly raised both and inotersen did not**, matching the clinical observation. Abstract text read first-hand via the OpenAlex inverted index; the companion's content is UNVERIFIED. Conference abstracts are not primary publications and this is recorded as a lead, not evidence.

### 2.4 Sequence, chemistry and tested-material coverage, with denominators

| Dimension | Human clinical subset | Human laboratory subset |
|---|---|---|
| Exact sequence | **1 of 12** named compounds (alicaforsen only) — corrected from 2 of 12 | **12 of 12** Sewing constructs verified character-for-character this round; Mangsbo 4 of 4 printed; de Boer obtained |
| | **+1 new**: ARC-520 publishes both RNAi trigger sequences in full (Table 1) | |
| Position-specific chemistry | 0 of 12 | **9 of 12** Sewing readable; **3 of 12 INFERRED** from prose because the LNA legend is orphaned; Mangsbo encodes backbone per position by letter case |
| Conjugate | pegnivacogin's PEG is the causal agent of the only harm-linked human signal; ARC-520 and CALAA-01 carry formulation drivers | n/a |
| **Tested-material characterization** | **0 of 12** | **0 of 7** — Sewing reports no supplier, no purity, no Tm, no MS |

Purity remains the project-wide exposure and for this endpoint it is mechanistically load-bearing, not administrative: the effect is driven by polyanionic charge and backbone linkage count, so n−1 shortmers and incompletely sulfurised species change the measured quantity rather than diluting it.

## 3. Prioritized acquisition plan, and work performed versus proposed

**Performed this round** (not proposed — done): Sewing Table 2 and methods verified; Mangsbo methods verified; de Boer 2022 obtained; four EMA reports parsed and a register built; six new human leads verified; 20 of 20 resources logged; the Waylivra EPAR located for the first time.

**Next, in order.** Ranked by qualified human observations gained, not volume.

| # | Target | Why first | Cost |
|---:|---|---|---|
| 1 | **`NCT02363946` and `NCT03728634` posted registry results** | the only **registered complement outcomes with results posted**. Registry-identified, extractable, free, and unexploited | zero — ClinicalTrials.gov API |
| 2 | **Sewing ingestion** (138 informative values) | open licence, in hand, controls Phase 2 explicitly requires | zero |
| 3 | **de Boer 2022 extraction** | third human-lab source, CC-BY, settles the backbone question | zero — obtained |
| 4 | **Registry cross-link for the 11 regulatory studies** | converts sponsor codes into reconcilable identifiers; blocks any defensible count until done | moderate, no acquisition |
| 5 | **apo(a) ASO article body** (PMID 26210642) | a real trial whose analytes are unknown; its supplement holds no complement content | access request **A14** |
| 6 | **Henry 2014 / Shen 2014** | analyte detail for the human/animal bridge; mechanism already citable from the EPAR | access requests **A1/A2**, de-risked |
| 7 | **Dryad `doi:10.5061/dryad.dh250`** | **CC0** GLP toxicology dataset for an intrathecal DNA-decoy; complement content UNVERIFIED | zero, speculative |

**Expected qualified observations: unknown except where established.** Sewing yields 138 informative values across 15 conditions at 3–5 donors. Everything else is unestablished and I decline to forecast it.

**Provenance for staged files** is in `research-staging/README.md`: the one committed CC-BY file with `sha256`/`md5`, sheet inventory, original filename and retrieval route; and five record-only sources with checksums and re-fetch routes, not committed because Crooke is NC-SA, Demirjian is ND, Mangsbo carries no CC licence, and the regulatory PDFs are bulky and freely re-fetchable.

## 4. Twenty-source coverage log

Full machine-readable logs with verbatim queries, URLs and outcomes: `research-staging/working/search_log_pubmed_europepmc.json` and `search_log_remaining_18_resources.json`.

| # | Resource | Searched | Barrier | Applicable | Outcome |
|---:|---|:---:|---|:---:|---|
| 1 | PubMed (E-utilities) | **yes**, 19 queries | none | yes | 36 relevant; the richest single resource |
| 2 | Europe PMC (REST) | **yes**, 32 queries | none for the resource | yes | 30 relevant, incl. the GalNAc3 correction |
| 3 | OpenAlex | **yes** | none | yes | 430 works in the citation graph, 106 complement-matched, all reviewed |
| 4 | Semantic Scholar | **yes** | none | yes | 361 works, 65 matched; **near-redundant with OpenAlex** |
| 5 | ResearchRabbit | **no** | **login or application required** | undetermined | not searched. No account created |
| 6 | Undermind | **no** | **login or application required** | undetermined | not searched. No subscription |
| 7 | Elicit | **no** | **browser/bot check** (Cloudflare) | undetermined | not searched |
| 8 | Consensus | **no** | **browser/bot check** (Cloudflare) | undetermined | not searched |
| 9 | GEO | **yes** | none | **no**, justified | 2 deposits, both off-endpoint |
| 10 | SRA | **yes** | none | **no**, justified | nothing on-endpoint |
| 11 | PRIDE | **yes** | none | yes | human CSF proteomics under nusinersen — complement **abundance**, not activation |
| 12 | ProteomeXchange | **yes** | none | yes | same deposits as PRIDE — **one deposit, not two** |
| 13 | BioStudies | **yes** | none | yes | `E-MTAB-7506`, C3–nucleic-acid binding; not activation |
| 14 | ArrayExpress | **yes** | none | yes | **a collection inside BioStudies, not independent**; `E-GEOD-20677` = `GSE20677`, a dedup exemplar |
| 15 | ClinicalTrials.gov (API v2) | **yes** | none | yes | the 4 toxicity-registered outcomes of §2.2 and the full efficacy cluster |
| 16 | CTD | **yes** | none | yes | **quantified zero**, computed first-hand |
| 17 | ICE | **yes** | none | **no**, justified | small-molecule oriented; no oligonucleotide test substance |
| 18 | ToxCast | **yes** | none | **no**, justified | invitrodb assay annotations carry no complement endpoint for an oligonucleotide |
| 19 | Zenodo | **yes** | none | yes | 3 deposits; 2 efficacy, 1 restricted. One carries genuine non-targeting-control arms |
| 20 | Dryad | **yes** | none | **no** for complement, justified | one **CC0** oligonucleotide toxicology dataset; complement content UNVERIFIED |

**14 genuinely searched · 4 blocked and recorded as not searched · 5 judged inapplicable with justification from queries actually run.** Blocked is never logged as searched.

**Two methodological findings from the log worth more than the hits.**
- **CTD's zero is quantified and validated, not assumed.** Computed from the bulk report files (snapshot 29 Sep 2026): **0 of 742 curated chemicals** produce an oligonucleotide–complement record, against positive controls showing 10,168 complement-gene rows, 2,567 complement-pathway rows and 872 complement-GO rows for other chemicals. An unvalidated zero would have been worthless.
- **A false-positive trap that would have corrupted the log.** Text-searching CTD for `phosphorothioate` retrieves **organothiophosphate pesticides**; four pesticides were the entire source of 31 apparent hits. This is the same class of error as the `c3a`-inside-a-hex-GUID collision in my 2026-10-01 reply. **Analyte and chemistry strings collide with unrelated vocabularies, and every sweep needs a verified negative control.**

Also recorded: a **measured host-reachability map** reusable by the team. Working — `api.openalex.org`, `api.semanticscholar.org`, `api.unpaywall.org`, `pmc.ncbi.nlm.nih.gov`, `clinicaltrials.gov` API v2, NCBI E-utilities. **Cloudflare 403** — `cell.com`, `jacionline.org`, `jpet.aspetjournals.org`, `europepmc.org` web pages (the REST API works), `researchprofiles.ku.dk`, `journals.sagepub.com`, `liebertpub.com`, `academic.oup.com`. **404 to default UA, 200 to browser UA** — `accessdata.fda.gov`.

## 5. Paper, supplement and data-access table

| # | Full citation | Identifier / link | Discovered via | Publisher / repo | Exact file needed | Gap it closes | Expected usable observations | Access attempts | Outcome | Priority |
|---:|---|---|---|---|---|---|---|---|---|---|
| **A1** | Henry SP, Jagels MA, Hugli TE, Manalili S, Geary RS, Giclas PC, Levin AA (2014) "Mechanism of alternative complement pathway dysregulation by a phosphorothioate oligonucleotide in monkey and human serum", *Nucleic Acid Ther* 24(5):326–335 | doi 10.1089/nat.2014.0491 · PMID 25093529 · **no PMCID** | MMB 2434 ref [54] | SAGE/Liebert | full text + any supplement | human-serum arm; factor-H immunoassay artifact; `TMSR458` | unknown | DOI→`journals.sagepub.com` 403 Cloudflare; `/doi/pdf/`, `/doi/full-xml/` 403; OpenAlex `oa_status=closed`, no OA location; Unpaywall `is_oa=false` | **confirmed paywall** (no free location in any index) | High, **de-risked** |
| **A2** | Shen L, Frazer-Abel A, Reynolds PR, Giclas PC, Chappell A, Pangburn MK, Younis H, Henry SP (2014) "Mechanistic understanding for the greater sensitivity of monkeys to ASO-mediated complement activation compared with humans", *JPET* 351(3):709–717 | doi 10.1124/jpet.114.219378 · PMID 25301170 · **no PMCID** | MMB 2434 ref [55] | ASPET→Elsevier | full text; human analytes; 767-subject query basis | largest human negative; ISIS 426115/183750 identity | unknown | ScienceDirect 403; `jpet.aspetjournals.org/.../709.full.pdf` **403 Cloudflare, fetched twice** | **technical block, not a paywall.** Semantic Scholar flags BRONZE OA at that URL; live Unpaywall now says closed — **S2's flag is stale** | High, **de-risked** |
| **A3** | de Boer E, Sokolova M, Quach HQ, McAdam KE, Götz MP, Chaban V, Vaage J, Fageräng B, Woodruff TM, Garred P, Nilsson PH, Mollnes TE, Pischke SE (2022) *J Immunol* 209(9):1760–1767 | doi 10.4049/jimmunol.2101191 · PMID 36104112 | prior round | AAI→OUP | full text + supplement | third human-lab source | **delivered** | `academic.oup.com` 403 Cloudflare; `journals.aai.org` and `jimmunol.org` 403; `researchprofiles.ku.dk` PDF 403; NVA download endpoints 403 | **OBTAINED** — green OA accepted manuscript, **CC-BY 4.0** | **closed** |
| **A5** | Povsic TJ, Lawrence MG, Lincoff AM, et al. (2016) *J Allergy Clin Immunol* 138(6):1712–1715 | doi 10.1016/j.jaci.2016.04.058 · PMID 27522158 · no PMCID | prior round | Elsevier | **Online Repository**: Fig E1, Tables E1–E4, "planned biochemical analyses" | assay kits, core lab, **the numeric complement values** | the only harm-linked human dataset's numbers | `jacionline.org` PDF 403 Cloudflare (both resources index it BRONZE); `em-consulte.com` 200 with an explicit subscription notice | **confirmed paywall** on the article; **supplement missing** | **High** |
| **A14** | Tsimikas S, Viney NJ, Hughes SG, et al. (2015) "Antisense therapy targeting apolipoprotein(a): a randomised, double-blind, placebo-controlled phase 1 study", *Lancet* | PMID 26210642 · EudraCT 2012-004909-27 | PubMed sweep, this round | Elsevier | **article body pp. 1472–1483** | which complement analytes a 47-subject phase 1 actually measured | up to 47 subjects, analytes unknown | 25-page supplementary appendix **obtained free** and read in full — contains **no** complement content; body not obtained | **free supplement obtained; body closed** | **High — new** |
| **A6** | Shaw DR, Rustagi PK, Kandimalla ER, Manning AN, Jiang Z, Agrawal S (1997) *Biochem Pharmacol* 53(8):1123–1132 | doi 10.1016/S0006-2952(97)00091-9 · PMID 9175717 | prior round | Elsevier | full text | the **C4d / classical-pathway** finding in human serum | 1 cluster, not 5 sources | OpenAlex closed; S2 CLOSED; Unpaywall closed | **confirmed paywall** | Medium |
| **A4** | Henry SP, Giclas PC, Leeds J, Pangburn M, Auletta C, Levin AA, Kornbrust DJ (1997) *JPET* 281(2):810–816 | PMID 9152389 | prior round | ASPET→Elsevier | full text — **the species of the factor H** | would convert `TMSR460` from `species = NA` to a human-lab row | 1 row reclassified | ASPET host-wide 403 | technical block over probable paywall | Medium |
| **A8** | Kandimalla ER, Manning A, Zhao Q, Shaw DR, Byrn RA, Sasisekharan V, Agrawal S (1997) *Nucleic Acids Res* 25(2):370–378 | doi 10.1093/nar/25.2.370 · PMID 9016567 · PMC146429 | prior round | OUP/PMC | the scanned PDF — **the serum species** | position-resolved chemistry series, **if** human | unknown | PMC landing page 200 (abstract only); `/pdf/250370.pdf` proof-of-work cookie challenge; `efetch db=pmc` refused by publisher; EPMC `fullTextXML` 500 | **listed free but technically gated** | Medium |
| **A9** | *Nucleic Acid Ther* 26(4):210–215, OSWG guidance | doi 10.1089/nat.2015.0593 · PMID 26981618 | MMB 2434 ref [101] | Liebert | full text; **resolve the author order** (MMB prints Seguin first, PubMed indexes Henry first) | the assay-characterization guidance our definitions should cite | definitional, not observational | not re-attempted after host-wide SAGE 403s | probable paywall | Medium |
| **A15** | Dryad, "Formulation and toxicology evaluation of the intrathecal AYX1 DNA-decoy" | `doi:10.5061/dryad.dh250` · **CC0** | Dryad sweep, this round | Dryad | the files; establish whether complement is in them | a **CC0** GLP toxicology dataset for an oligonucleotide | **UNVERIFIED — must not be recorded as complement evidence** | metadata and all 10 file descriptions read; **no file read** | open, unexamined | Medium — new |
| A7, A10–A13 | Agrawal 1995 · Shen 2016 · Galbraith 1994 · Henry 2002 · the unresolved Henry/Larkin/Novotny/Kornbrust 1994 | — | prior round | various | full texts | animal supporting; historical | low | as previously recorded | probable paywalls; A13 remains **citation unresolved** | Low |

**Requests to Oscar, specific as the register requires.** Only three are worth your time, and only if you have institutional access — **no purchase is proposed**:
1. **A5** — the Povsic 2016 *Online Repository* (Fig E1, Tables E1–E4). The only human dataset linking measured complement to severe clinical harm, and its numbers are solely in that supplement. A **confirmed paywall**, the only one in this round where a subscription notice was actually displayed.
2. **A14** — the apo(a) phase 1 article body. Its own supplement is free and holds nothing; 47 subjects' analytes hinge on the body.
3. **A1/A2** — Henry 2014 and Shen 2014. **Downgraded**: the mechanism and the ~3-fold species figure are now citable from the free Tegsedi EPAR.

## 6. Access-barrier classification, and the anticoagulant convention

Barrier classes used throughout, per the register's taxonomy: **confirmed publisher paywall** (a subscription or purchase notice actually displayed) — A5 and, via index agreement with zero OA locations, A1 and A6; **technical or browser block** (Cloudflare, reCAPTCHA, proof-of-work, or a user-agent filter) — A2, A4, A8, and the FDA user-agent case; **login or application required** — resources 5–8; **missing supplement** — A5; **citation unresolved** — A13; **listed open access but gated** — A2 and A8. No barrier is recorded as a paywall on the strength of a bot check, and no price is recorded anywhere because none was displayed.

**The anticoagulant convention, which Oscar authorized.** The empirical case is now strong enough to state as a finding rather than a worry. Across the six human complement sources whose methods were read:

| Source | Matrix | Anticoagulant as reported |
|---|---|---|
| Sewing 2017 | whole blood → plasma for ELISA | **"anticoagulant-sprayed vacutainer tubes" — chemical identity never given, no concentration** |
| Mangsbo 2009 | whole-blood loop; hirudin plasma | heparinised surface **+ soluble heparin 0.5 U/mL**; EDTA 10 mM stop. **The abstract calls the blood "non-anticoagulated" — the paper contradicts itself** |
| de Boer 2022 | whole blood + plasma | **lepirudin 50 µg/mL**; EDTA 10 mM stop; lepirudin chosen *because* it "does not interfere with the complement cascade" |
| ARC-520 | serum (CH50) **and** plasma (Bb) | **not reported** for the complement plasma |
| Demirjian / QPI-1002 | plasma | K₂-EDTA Vacutainer |
| GalNAc3 integrated | not stated | **not reported** |

**Three of six do not report it, one contradicts itself, and the three that do report use heparin, lepirudin and EDTA — agents that are not interchangeable for complement.** Heparin modulates complement, EDTA abolishes it (which is precisely why two of these studies use it as a *stop* reagent), and lepirudin is chosen specifically for being inert. A dataset that pools a heparin-loop C3a with an EDTA-plasma C3a is pooling different assays.

Two trap cases make the field mandatory rather than merely desirable, and both would have produced a fabrication:
- **Sewing** names sodium citrate and ACD — for its **washed-platelet** workstream only. Carrying that to the Figure 6 complement data would invent an anticoagulant the paper never claims.
- **ARC-520** names EDTA — in its **siRNA PK** methods only. The paper never links it to the Bb plasma.

The proposed convention is drafted as a separate cross-endpoint document, `ANTICOAGULANT_MATRIX_CONVENTION_PROPOSAL.md`, published beside this report. It is a **proposal on this branch only**: thrombocytopenia and coagulopathy live on other branches and I have not touched their folders, per Beebop's instruction to propose corrections rather than overwrite another endpoint's work.

## 7. Corrections, and what needs German or Oscar

### 7.1 Every correction to the 2026-10-01 reply

**Beebop's three, all verified and conceded:** animal complement rows 7→**8**; distinct human studies 19→**21 named + 3 pooled**; human exact-sequence coverage 2/12→**1/12** (AR177 is animal).

**Four more found this round:**
4. §2.7's GalNAc-conjugated-era negative is **wrong** — PMID 30570431 measures Bb and C5a in humans. The claim must be bounded to the documents checked.
5. §3.3's human-laboratory source count is **7, not 9** — five publications are one Hybridon/UAB cluster.
6. The regulatory study rosters were incomplete — drisapersen has **ten** studies, inotersen **three**, and `CS2`/`CS3` is a **parent/extension pair**.
7. Volanesorsen's complement denominator is **unverified**; mipomersen's attribution is **FDA-sourced**, not EMA-sourced.

**Two more while writing this report:**
8. §3.4's claim that "nearly every modern trial registering a complement outcome does so for efficacy — the two exceptions are CALAA-01 and ApTOLL-COVID" is **too strong**. There are at least **four** toxicity-registered complement outcomes, **two with results posted**.
9. §2.4's framing of Sewing and Mangsbo as contradicting each other on backbone dependence **overstated the disagreement**. All three human-blood sources agree PS activates and sequence does not matter; the real difference is pathway-specific and donor-dependent.

**Two withdrawals**, already published in the addendum: no threshold adopted this round, and no dataset-level sequence-independence claim.

### 7.2 German (scientific)

1. **The complement rubric**, when a rubric is needed — not this round. Anchors with their provenance: 2× ULN for split products and below-LLN for components, **both human conventions**; ~50 µg/mL as the exposure axis, **animal-derived and not to be made a human rule**.
2. **Whether the four readout classes may ever share a numeric column or a grade.** My position: no. Two independent exhibits now show split products rising while function falls, in the same sample.
3. **The better-posed backbone question**, replacing the contradiction I previously reported: under what matrix, concentration and incubation time can a **phosphodiester** backbone engage the **classical** pathway, given that Mangsbo observes it, de Boer's mixed-backbone CpG-A does not activate, and Sewing's phosphodiester is inactive at 45 min by a ratio readout? And is pathway choice genuinely **donor-dependent**, as Mangsbo's own Results heading asserts?
4. **Whether sequence-independence may be stated at all**, now that two independent human-blood sources with explicit GpC controls support it. I have withdrawn it as a dataset-level claim and seek your ruling, not my own.
5. **Whether an apparent factor-H decrease may be recorded**, given Henry 2014's immunoassay-artifact finding. Bears directly on `TMSR458`.
6. **Pathway attribution authority** — two sources mislabel pathways (Demirjian calls C3a/C4a/C5a "classic"; ApTOLL 2024 calls C3/C4 the "terminal complement complex"). I propose `pathway_label_source` and `pathway_label_curator` as separate fields and ask you to own the curator column.
7. **Whether inotersen's human complement rows are model-eligible at all.** The CHMP's own verdict: measurements were *"often measured at a single time point only"*, assessment *"hampered by the irregularity of measurements applied"*, with C5a and Bb above ULN at baseline **including in the placebo arm**.
8. **Whether Sewing's three LNA constructs may carry a position-specific chemistry field** when that placement is inferred from prose rather than readable from the table.

### 7.3 Oscar (scope and process)

9. **Scope: keep the endpoint.** Evidence base at this commit: 10 in-repo rows, **8 verified human trials with reported complement and a recoverable identifier**, 26 named human studies across all bases, 7 independent human-laboratory sources with **3 now usable**, and 138 informative human values in hand under CC-BY. The dossier's descope recommendation is not defensible on this evidence.
10. **Authorize the two posted-results registry extractions first** (`NCT02363946`, `NCT03728634`). Registered complement outcomes with posted results, free, registry-identified, and never exploited — the best ratio of qualified human observations to effort in the endpoint.
11. **The registry cross-link for 11 regulatory studies** is a prerequisite for any defensible human trial total. It needs your go-ahead as scope, and an extension-counting convention — `CS2`/`CS3` is the live case.
12. **The anticoagulant convention** touches thrombocytopenia and coagulopathy. Published here as a proposal only; propagating it is your call.
13. **Two access requests worth your institutional access**: the Povsic Online Repository (A5) and the apo(a) article body (A14). No purchase proposed.
14. **A project-wide sweep-hygiene note.** Two independent false-positive classes have now bitten this endpoint — `c3a` inside a hex GUID, and `phosphorothioate` matching organothiophosphate **pesticides** in CTD. Every endpoint's allocation sweep should carry a validated negative control.
15. **Schedule reality.** The Work-Plan places Complement in the **September** block under your own column with German reviewing "Complement Sept"; October is Hydrocephalus and Hepatotoxicity; November is reserved for all four deliverables. This endpoint is overdue and there is no slack, which argues for the narrow Sewing-first package over a broad programme.

## 8. Limitations

- **No dataset was created and no row was ingested.** The 138-value figure is a verified extraction grain, not a dataset.
- **52 of 54 agents in the first attempt were lost to a container restart.** Two sweeps were recovered from the journal; the rest was re-planned, not recovered.
- **4 of 20 resources were never searched** (login or bot-gated) and are logged as such. Their potential content is unknown.
- **The Figure 2 values of `NCT00554359` were not obtained** and will not be, by plot digitisation.
- **Glover 1997, Maksymowych 2002, Rudin 2001, Advani 2005, Nemunaitis 1999, Chen 2000 and Paul 2010 remain abstract-level.** Their analyte assignments are UNVERIFIED.
- **Crooke 2016's denominator is disputed** (750 verified by me vs a 52-trial/>2,600-subject claim); neither is used.
- Sewing's **LNA positions are inferred from prose**, and its `Inhib.` reagent is unidentified.
- Mangsbo's **C4a** is reported only at 1 h; any other timepoint is UNVERIFIED.
- The **AACR 2025 abstract** is grey literature read via an inverted index, and its EUROTOX companion's content is UNVERIFIED.
- `git` history is shallow and Beebop's earlier baseline commits are unreachable, so no provenance or timing claim is made about any repository fact.
- Several items are flagged **complement content UNVERIFIED** rather than negative, including PMID 38227794, the Dryad CC0 deposit, and the tcDNA-ASO in vitro matrix species.

---

**RESEARCH ROUND COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION AND GERMAN'S SCIENTIFIC ADJUDICATION**
