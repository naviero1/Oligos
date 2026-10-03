# New human complement leads — verified 2026-10-03

Six leads surfaced by the PubMed and Europe PMC sweeps and verified one agent per lead. Full per-lead
output is in `new_human_leads_verified.json`. **Research only — no dataset, label or adjudication.**

Two of the six carry a `counts_as_verified_trial` flag that **contradicts the verifier's own
reasoning**. I have overruled the flag in favour of the reasoning in both cases, and recorded why.

## Dispositions

| Lead | Identity | Class | Countable trial | Disposition |
|---|---|---|---|---|
| **L1 ARC-520** | Schluep T, Lickliter J, Hamilton J, Lewis DL, Lai CL, Lau JY, Locarnini SA, Gish RG, Given BD (2017) *Clin Pharmacol Drug Dev* 6(4):350–362, doi 10.1002/cpdd.318, PMID 27739230, PMC5516171, **CC BY-NC-ND 4.0**; **NCT01872065** / Heparc-1001 | human_clinical | **YES** | **NEW verified human trial.** Accepted. |
| **L2 GalNAc3 integrated** | PMID 30570431 / PMC6386089, *Nucleic Acid Ther*, **CC BY-NC** | human_clinical | **NO — overruled** | Pooled source. Corrects our §2.7. |
| **L3 apo(a) ASO** | PMID 26210642, *Lancet*; EudraCT 2012-004909-27 | human_clinical | **NO** | Real trial, analytes unknown. Access request. |
| **L4 LJP 394 / abetimus** | PMID 9034989 | human_clinical | **YES, low-strength** | Abstract-only, n=4, severe confounder. |
| **L5 Kandimalla 1998** | PMID 9873494 | human_laboratory | NO | **Not independent — overruled.** Collapses into one cluster. |
| **L6 aptamer corona** | PMID 38044589, *ACS Nano* | **mechanistic_only** | NO | **Excluded** from measurement tables. |

## L1 — ARC-520: a new verified human trial, accepted

**NCT01872065**, Phase 1, COMPLETED, **54 healthy volunteers** (36 active / 18 placebo), 9 cohorts of 6
randomised 4:2, single intravenous dose 0.01–4.0 mg/kg. Publication and registry denominators agree.

- **Analytes, verbatim:** "Venous blood samples were collected and processed to produce serum (for
  complement **CH50** analysis) or plasma (for split products-**Bb** analysis)." Two analytes only.
- **Dual matrix, explicitly stated** — CH50 in serum, Bb in plasma, in one sentence. This is the
  cleanest in-source demonstration we have that matrix is analyte-specific within a single study.
- **Anticoagulant NOT reported** for the complement plasma. The verifier flagged a trap worth
  carrying: the paper *does* name EDTA, but only in the siRNA PK methods. **That EDTA must not be
  carried over to the Bb plasma** — the paper never links them.
- **Assay, vendor, units, LLOQ and reference ranges all NOT REPORTED**, and the omission is specific:
  the paper names vendors for its cytokine panel, PK software and PNA probes.
- **Conditional measurement scheme, verbatim:** "Initially the 0- (pre-) and 0.5-hour postdose samples
  were analyzed, with the remaining samples analyzed if a change from baseline was observed at 0.5
  hours." So for most timepoints, **absence of a result means "not analysed", not "measured and
  normal"** — the suppressed-row trap, inside a single trial.
- **Sequences published in full** (Table 1), for both RNAi triggers AD0009 and AD0010, with 2′-modified
  sugars, deoxy residues, an inverted-dT 3′ cap and a phosphorothioate linkage in the `dTsdT`
  overhang. Verifier's caution: reading `f` as 2′-fluoro is an inference from table notation, not
  stated in prose.
- **Route matters here.** Infusion is given as **rate, not duration**; the rate was cut from 3.5 to
  2 mL/min at the overlapping 2 mg/kg dose "to lessen risk of infusion reaction", and cohorts 7–9 were
  pre-treated with oral diphenhydramine 50 mg. Complement was one of the readouts tracked across that
  de-escalation — so this trial is also evidence on the route/rate mitigation point.
- Internal inconsistency recorded: the Discussion says complement was measured "in plasma", which
  contradicts the Methods. The Methods are the specific statement and should govern.
- Delivery excipient is a masked hepatocyte-targeted polymeric amine (NAG-MLP), so **formulation is a
  candidate driver independent of the oligonucleotide** and must be recorded.

## L2 — GalNAc3: our §2.7 claim is wrong, and the source is pooled

**The correction is confirmed first-hand.** Bb and C5a were measured in healthy volunteers dosed with
GalNAc3-conjugated 2′-MOE ASOs. Our §2.7 assertion that the GalNAc-conjugated generation has no human
complement measurement cannot survive it. The EMA-assessment-report route that produced that assertion
simply does not cover this source — it is a sponsor-authored integrated analysis in a journal.

**Why I overrule `counts_as_verified_trial: True`.** The verifier's own reasoning says it "is STILL a
pooled assessment", and recommends counting it as **one dataset, not as 6–8 trials**. I agree, and the
rule is ours: no recoverable trial identity, no countable trial. Specifically —

- **Zero NCT numbers, zero protocol codes** anywhere, verified by `grep -c` returning 0 on both the
  Europe PMC full-text XML and the 53-page supplement. The paper never states how many trials there are.
- **The complement data are themselves pooled across compounds** — every point aggregates "at least 10
  subjects and 3 GalNAc3-conjugated 2′MOE ASOs"; no per-compound complement result is recoverable for
  any of the eight.
- The pooling is **explicitly post hoc** (individual datasets merged into one SAS dataset; ANCOVA with
  trial as a factor), though Bb/C5a were pre-specified safety labs in the component trials.

So: **0 countable trials, a large number of human complement measurements.** Register entry flagged
*pooled, trial identities not recoverable*.

**The confound that matters most.** One of the seven pooled compounds, **ION 696844, targets complement
factor B — and Bb is the activation fragment of factor B.** The paper separates it in no complement
analysis. So for an unknown fraction of the pooled Bb data, complement is an **efficacy** readout
sitting inside what reads as a toxicity null. This is exactly the target-is-complement confound we
warned about, occurring *within* a single pooled human dataset. It must be recorded on the row.

Other mandatory caveats: measurement is narrow (two split products, first dose only, 24 h window,
all-subcutaneous — a weak test of an infusion-associated mechanism); matrix, anticoagulant and assay
entirely unreported; reference ranges partly data-derived (mean ± 2 SD of baselines); and the supplement
contains one ASO-treated and one placebo Bb excursion >2× ULN plus an unadjusted nominal p<0.05 that the
main text does not mention. Denominators differ by analyte and by timepoint (baseline Bb 86 placebo +
262 ASO = 348; C5a 74 + 220 = 294; intermediate timepoints far lower). An unreconciled 10-subject gap
(392 − 32 = 360 vs 350 analysed) is flagged, not resolved.

⚠ **Discrepancy to resolve, not adopt.** This verifier states Crooke 2016 "pooled 52 trials and >2,600
subjects". We verified **750 subjects** first-hand from PMC5112040. The figures may describe different
papers or different denominators. **Neither should be used until reconciled.**

## L5 — the human-laboratory count collapses from 9 to 7

The verifier's dedup finding is the most consequential item in this batch after L2, and I accept it in
full: PMID 9873494 is **not an independent human-laboratory source**. It is the same group, the same
laboratory and the same assay lineage as the sources we already counted separately:

- Kandimalla ER, Shaw DR, Agrawal S (1998) — Hybridon + UAB
- Shaw DR, Rustagi PK, Kandimalla ER, Manning AN, Jiang Z, Agrawal S (1997) *Biochem Pharmacol* 53(8):1123–32 — PMID 9175717
- Agrawal S, Rustagi PK, Shaw DR (1995) *Toxicol Lett* 82–83:431–4 — PMID 8597089
- Kandimalla ER, Manning A, Zhao Q, Shaw DR, Byrn RA, Sasisekharan V, Agrawal S (1997) *Nucleic Acids Res* 25(2):370–378 — PMID 9016567
- Yu D, Iyer RP, Shaw DR, … Agrawal S (1996) *Bioorg Med Chem* 4(10):1685–92 — PMID 8931938

Near-identical titles, the same two endpoints (hemolytic complement + aPTT), and the same Shaw hemolytic
assay at UAB throughout. **Assume dependence, not independence.**

**Revised human-laboratory source count: 7, not 9** — Sewing 2017, Mangsbo 2009, de Boer 2022,
Henry 2014, Shen 2014, Paul 2010, and **one Hybridon/UAB cluster** standing for five publications. Of
the seven, **2 are reachable and usable today** (Sewing, Mangsbo). The cluster's distinct contribution
is a chemistry contrast — PS-DNA worse than PS-RNA / 2′-O-methyl-RNA / 2′-5′-RNA — not a replication.

## L3 and L4 — one access request, one weak signal

**L3, apo(a) ASO (PMID 26210642).** A real randomised, double-blind, placebo-controlled first-in-human
phase 1 in **47 randomised** subjects (206 screened), EudraCT **2012-004909-27**, with complement named
in the prespecified safety panel and a target (apo(a)) that is *not* complement. But the abstract says
only "complement variables" and the **analytes remain UNVERIFIED**. The 25-page supplementary appendix
was obtained free and read in full — it contains **no complement content**. The main article body, the
only place the analytes can be named, was not obtained. Not countable as a complement measurement until
it is. **This is access request A14.**

**L4, LJP 394 / abetimus (PMID 9034989).** Counted, but at the bottom of the evidence ladder. **Four
women with stable SLE**, single 100 mg infusion, **no control arm**; "complement" and "complement split
products" measured but the individual analytes are named nowhere accessible. The drug is verified
genuinely oligonucleotide-based (~90% of its 54 kDa mass is synthetic dsDNA on a triethylene-glycol
platform). **Decisive confounder: SLE patients consume complement from their disease**, so a complement
change in four lupus patients without a control arm cannot be attributed to the drug. Access barrier is
**"article not digitized" — no online version exists anywhere; not a paywall, not a login, not a
CAPTCHA.** The verifier did obtain, free and in full, the companion trial Furie et al. (2001)
*J Rheumatol* 28(2):257–265, PMID 11246659, whose human readouts are C3/C4 component abundance only.

## L6 — excluded, and the exclusion is the finding

PMID 38044589 (*ACS Nano*) is **corona/interactome proteomics with pathway annotation, not a
measurement of complement activation.** No C3a, C5a, Bb or sC5b-9 anywhere. It identifies intact
complement proteins in an aptamer's plasma protein corona and annotates them to a "complement
activation" GO term. **Identification of a complement component in a corona does not establish that
convertase-mediated cleavage occurred.** It must not enter the endpoint's measurement tables. Recorded
because a keyword sweep will surface it again and the next session needs the reasoning, not just the
verdict.

## Running tally of corrections forced to the 2026-10-01 reply

Beebop found three; this round and the regulatory register add four more, all found by us:

4. §2.7's GalNAc-conjugated-era negative is **wrong** (L2).
5. §3.3's human-laboratory source count is **7, not 9** (L5 dedup).
6. The regulatory programmes' study rosters were incomplete and `CS2`/`CS3` is a parent/extension pair
   (see `REGISTER_regulatory_draft.md`).
7. Volanesorsen's complement denominator is unverified, and mipomersen's attribution is FDA-sourced
   rather than EMA-sourced (same file).

Plus one new countable human trial (ARC-520) and one new pooled human source (GalNAc3) that the reply
did not have at all.
