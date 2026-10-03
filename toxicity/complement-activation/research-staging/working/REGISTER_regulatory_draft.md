# Regulatory-record clinical register — complement activation (working draft)

Compiled 2026-10-03 by Rocksteady. **All entries below were extracted first-hand this session** from EMA assessment reports downloaded and parsed locally with `pdftotext -layout`. Not yet published; working input to `ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md`.

## Decisive finding: zero registry identifiers

**None of the four EMA assessment reports contains a single NCT number.** A regex for `NCT\s?0?\d{7,8}` over all four full texts returns **0 hits** in each:

| Document | Pages | NCT numbers | Study identification used instead |
|---|---:|---:|---|
| Kyndrisa (drisapersen) withdrawal AR | 105 | **0** | `DMD1140xx`, `DMD11xxxx`, `PRO051-0x` |
| Tegsedi (inotersen) EPAR | 142 | **0** | `ISIS 420915-CSn`, short form `CSn` |
| Kynamro (mipomersen) EPAR | 114 | **0** | `ISIS 301012-CSn`, short form `CSn`, `MIPO35xxxxx` |
| Waylivra (volanesorsen) EPAR | 121 | **0** | `CSn`, animal studies `304801-ASnn` |

Consequence for counting: the regulatory record holds the **only chronic human complement data in the field**, and it identifies every study by **sponsor protocol code, never by registry number**. Under Oscar's rule these qualify on the "documented stable study identifier with its evidence" basis — but cross-linking them to ClinicalTrials.gov is a **separate, unperformed mapping step**, and until it is done no regulatory study may be reconciled against a registry-derived count. This is a real dependency, not a formality.

## Study rosters as printed

Occurrence counts are from the full text and indicate prominence, not importance.

- **Drisapersen** — `DMD114044` (79), `DMD114117` (71), `DMD114876` (64), `DMD114349` (57), `DMD114673` (38), `PRO051-02` (15), `DMD115501` (10), `DMD114118` (6), `DMD110117` (2), `PRO051-01` (2). **Ten studies — more than the five or six named in the 2026-10-01 reply.** `DMD114117` and `DMD115501` were not previously recorded at all.
- **Inotersen** — three studies, and the EPAR's own abbreviation list defines them: **`CS1` = Clinical Study 1**; **`CS2` = Parent Study (`ISIS 420915-CS2`)**; **`CS3` = OLE Study (`ISIS 420915-CS3`)**. `CS2`/`CS3` are a **parent/extension pair and must never be summed**. `CS3` carries 211 mentions and was not recorded in the 2026-10-01 reply at all. Note two stray occurrences of `ISIS 430915-CS2/CS3` against nine-plus of `ISIS 420915` — almost certainly a typo in the source document; flagged, not corrected.
- **Mipomersen** — `ISIS 301012-CS1` … `-CS12` plus `MIPO3500108`. The EPAR's complement statements sit **nowhere within 700 characters of any study code**, so the EMA document alone does not attribute them to a named study.
- **Volanesorsen** — clinical `CS6` (148), `CS16` (95), `CS7` (53), `CS2` (24), `CS1` (15), `CS13` (7), `CS4` (4); animal `304801-AS01` … `-AS16`.

## Per-programme complement entries

### Drisapersen
- **Attribution, verbatim:** "long-term drisapersen therapy also decreased Complement factor C3 in clinical trials (study nos. **DMD114876 and DMD114044**; see clinical AR for further evaluation)."
- **Quantified, verbatim:** "Mean changes of Complement C3 from baseline were **-0.047 g/L at Week 12, -0.075 g/L at Week 24, and -0.085 g/L at Week 48 (8% decrease from baseline to Week 48)** … For placebo, the mean changes were 0.041, 0.004, and -0.025 g/L … At week 48, more subjects on drisapersen 6 mg/kg/wk had a **shift from normal to low complement C3 compared to placebo (11.7% vs. 1.3%)**."
  - ⚠ **Attribution caveat:** the quantified passage occurs in a clinical section whose nearest study code is `DMD114349`, while the explicit "study nos." attribution naming `DMD114876`/`DMD114044` sits in the nonclinical AR. The quantified figures are described elsewhere as covering the ambulant placebo-controlled studies. **Which study or pooled set the numbers belong to needs a closer read before any row is keyed to a study.** Do not assume.
- **Split products:** "complement split products measured in two phase I/II studies (**DMD114118 and PRO051-02**) … There seemed to be no strong evidence … A mean concentration of split product **C3a was found to be above the upper range of normal already at screening in study DMD114118**."
- **Adverse-event term:** `complement factor C3 decreased` at **6.4% vs 0%**.
- **Animal, and a four-class case:** "the complement system was activated in monkeys (**complement split factors C3a and Bb**), but the **concomitantly decreased total complement activity** suggests functional impairment of the cascade." Split products up while function down, in one study — a second independent instance of the pattern after REGULATE-PCI, and further evidence that activation and function cannot share one column or one grade.

### Inotersen
- **CS1, verbatim and fuller than previously recorded:** "Complement split product measurement (**C5a and Bb**) was conducted in study CS1 … otherwise healthy volunteers in CS1 were reported to have had complement factors **C5a and Bb >ULN at baseline** as well as at several time points during the study **in the placebo multiple dose cohort**, in the inotersen single dose and in the multiple dose cohorts. No specific pattern could be detected and **complement factors were often measured at a single time point only**, probably in line with biological variation or secondary to acute phase response. Assessment of complement factors in study CS2 is clearly hampered by the **irregularity of measurements applied** and the overall low number of subjects."
  - This is a **regulator-stated data-quality verdict**: irregular sampling, frequent single timepoints, baseline abnormalities in both arms. It bears directly on model eligibility and should travel with any inotersen row.
- **CS2, verbatim:** "Complement factors were not routinely measured in CS2 … **55% of inotersen-treated subjects had any post-baseline C3 value below LLN compared to placebo (21%). Mean complement C3 deceased by 33% from baseline to Week 65 in CS2** (however, based on a low number of subjects with any measures)." ("deceased" is the source's typo.)
- **Additional analysis not previously recorded:** "TEAEs potentially related to complement activation were evaluated using an **unspecific MedDRA query of hypersensitivity**. No significant difference was noted between treatments." This is an AE-proxy analysis, not a measurement — it must not be recorded as a complement measurement.
- **Tissue deposition, CS2/CS3:** "additional immunological contribution of inotersen evident by **glomerular deposits for complement factors and IgG**"; "**Two subjects presented with reduced complement C3**."
- **CHMP verdict:** "Complement activation was not thoroughly studied in the clinical program."

### Inotersen EPAR as a free proxy for the two paywalled primaries
The Tegsedi EPAR summarises, with citations, the central findings of **Henry 2014** and **Shen 2014** — the two confirmed-inaccessible papers at the top of the access list — verbatim:

> "The potential for complement system activation appears to predominate in monkeys, because the **binding of ASOs to complement factor H (CFH)** has been demonstrated, which releases the inhibition of constitutive activation of the alternative complement pathway (**Henry et al., 2014**). Monkeys are more sensitive than humans to this stimulation because of the **~3-fold higher inhibitory capacity of 2'-MOE ASOs to monkey CFH compared to the CFH of other species** (**Shen et al., 2014**). As the inotersen exposure was at least 3-fold higher in monkeys than in patients at the recommended therapeutic dose, the CHMP considers that **the potential for complement system activation in humans is minor**."

This **materially de-risks access items A1 and A2**: the mechanism and the ~3-fold species figure are now citable from a free, regulator-adjudicated source. The primaries are still wanted for analyte-level detail, assay methods and any sequences — but they move from *blocking* to *desirable*. Note the EPAR phrases the 3-fold as the ASO's inhibitory capacity *against* monkey CFH; that is not word-for-word how a secondary summary of Shen 2014 framed it, so **quote the EPAR as the EPAR and do not blend the two framings**.

### Volanesorsen
- **Verbatim:** "There were no notable differences in the levels of platelet count (IM-positive: 38%; 3 of 8), IM negative (78%; 18 of 23) for confirmed platelet counts < 140,000 /mm3), ALT, AST, creatinine clearance, hsCRP, **complement C5a, and complement Bb** between ADA-positive patients and antibody-negative patients."
- ⚠ **Denominator caution:** the `3 of 8` and `18 of 23` figures are **platelet** counts. The EPAR states **no denominator for the complement comparison**, so the number of patients in whom C5a and Bb were actually measured is **UNVERIFIED**. The 2026-10-01 reply's phrasing — "measured in human phase 3 patients (CS6/CS16)" — is not supported at that precision; what is supported is that C5a and Bb were analysed by ADA status within the `CS6`/`CS16` immunogenicity assessment.
- **Animal:** monkey `304801-AS11` (39 wk) reports **Complement C3** at the top dose; `304801-AS02` (13 wk) reports **Complement Bb** from ≥8 mg/kg. "Complement activation is seen in monkeys, a known effect of antisense oligonucleotides and considered **species specific**."

### Mipomersen — a provenance split worth preserving
The Kynamro EPAR's complement statements ("consumption of complement (C3 fraction)"; "Slightly lower C3 values were observed, but without signs of complement activation"; "Antibody formation might induce complement consumption") are **not attributable to a named study from the EMA document alone**. The study-level attribution — phase 1 `MIPO3200309` measuring Bb and C5a with no activation, and intact C3 measured in the phase 3 trials excluding `CS5` with a median change of −7.2% vs −3.0% placebo — comes from the **FDA medical review for NDA 203568Orig1s000**, a different document by a different regulator.

Two regulators, two attributions, one drug. Any mipomersen row must carry which regulatory document it came from; they are not interchangeable and must not be merged into one source.

The **Kynamro refusal-grounds document** (10 pp, verified first-hand) contains exactly two complement occurrences, both in the refusal reasoning: "Mipomersen is also associated with a high incidence of flu-like symptoms, effect on inflammatory markers and **decrease on complement component C3** … In addition, **complement activation was more pronounced in patients with antibody formation**."

## Corrections this register forces to the 2026-10-01 reply

1. Drisapersen has **ten** named studies in the EPAR, not the five or six listed; `DMD114117` and `DMD115501` were missed entirely.
2. Inotersen has **three** studies, not two: `CS3` (the open-label extension) was missed, and `CS2`/`CS3` form a parent/extension pair that must not be summed.
3. Volanesorsen's complement denominator is **unverified**, not "phase 3 patients".
4. The mipomersen study attribution is **FDA-sourced, not EMA-sourced** — the reply did not distinguish them.

## Retrieval notes for the shared access register

- The EMA document host rate-limits (HTTP 429); retry with backoff succeeds.
- `accessdata.fda.gov` returns **404 to a default user agent and 200 to a browser user agent**. Not a paywall. A session that does not know this will wrongly log FDA reviews as unavailable.
- The Waylivra EPAR is at `ema.europa.eu/en/documents/assessment-report/waylivra-epar-public-assessment-report_en.pdf` (HTTP 200, 2,601,099 bytes, 121 pp) — previously unlocated.
