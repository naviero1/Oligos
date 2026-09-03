# Clinical-row validation — human trials, August 2026

Validation of the 39 `study_type=clinical` rows against their cited primary sources,
prompted by a structural concern found before any source was opened (§1). Seven of the
13 unverified absence claims were checked directly; results in §2. **Grades in
`measurements.csv` were NOT changed** — recommended reclassifications are recorded here
for review, because relabelling a toxicity dataset is a scientific call, not a curation one.

## 1. The confound that motivated this

Cross-tabulating provenance against outcome across all 39 clinical rows:

|                          | grade ≥2 | grade <2 | total |
|--------------------------|---------:|---------:|------:|
| `WS` (search-derived)    |    **0** |       20 |    20 |
| anchor-sourced           |       11 |        8 |    19 |

- Base rate of grade ≥2 = 11/39 = 28.2%; expected among 20 unverified = **5.6**, observed **0**.
- One-sided Fisher exact **p = 4.5 × 10⁻⁵**.
- 13 of 14 rows whose entire claim is an absence statement (`no_signal`/`none`/`no_change`)
  are `WS`.

Verification status predicts the label almost perfectly. A model trained on this as-is
partly learns *"does this compound have a regulatory paper trail"* rather than renal
biology — and that shortcut inverts on prospective compounds, which have no dossier and
would be scored non-nephrotoxic by construction. That is the wrong error direction for a
safety model.

## 2. What direct source retrieval found

The decisive question per row: does "no signal" mean (a) renal endpoints were **measured
and unremarkable**, (b) renal endpoints were **never measured**, or (c) the **cited source
does not report them**? Only (a) supports a grade of 0.

| mid | drug | verdict | what the source actually shows |
|-----|------|---------|-------------------------------|
| MSR066 | cemdisiran | **CONFIRMED** | eGFR measured: change at wk32 −2.9 (11.1) vs placebo −6.3 (4.8) mL/min/1.73 m². A genuine measured negative, in fact favourable vs placebo. |
| MSR045 | lumasiran | **PARTIAL** | eGFR reported extensively but as *efficacy/eligibility stratification*, not toxicity. AE table (Table 2) lists only injection-site reaction and abdominal pain. Renal function tracked; renal *safety* not assessed. |
| MSR063 | pelacarsen | **REFUTED** | Source states "no excess nephrotoxicity" as a generic claim with no renal endpoint behind it — and the trials **excluded** eGFR <60 and UACR >100 mg/g. The design removes the population where nephrotoxicity would appear. |
| MSR078 | fazirsiran | **REFUTED** | Safety assessments were "TEAEs and changes in FEV1 and DLCO Hb" only. No renal endpoint. Patients with renal dysfunction excluded at enrollment. |
| MSR042 | tofersen | **REFUTED** | Label has no Renal Impairment subsection and no renal endpoint in the AE table. Sole renal mention: "No clinical studies have been conducted to evaluate the pharmacokinetics of tofersen in patients with renal or hepatic impairment." Intrathecal route plausibly explains low renal risk, but that is a mechanistic inference, not a measurement. |
| MSR044 | patisiran | **UNSUPPORTED** | Onpattro label carries no renal endpoint in the AE table; only §8.7 boilerplate dosing and "has not been studied in severe renal impairment or ESRD". |
| MSR047 | vutrisiran | **UNSUPPORTED** | Amvuttra label identical in kind: AE table lists pain in extremity, arthralgia, dyspnea, vitamin A decreased. No renal endpoint. |

**Score: 1 of 7 checked absence claims survives as a measured negative.**

### The mechanism

Whether renal endpoints were measured tracks the **indication**, not the drug's actual
renal risk. Cemdisiran (IgA nephropathy) and lumasiran (primary hyperoxaluria) have renal
indications and renal data. Pelacarsen, fazirsiran, tofersen, patisiran and vutrisiran do
not, and their trials neither measured renal endpoints nor enrolled renally impaired
patients. The negative class is therefore substantially *"nobody looked"* rather than
*"looked and found nothing"* — exactly as the confound predicted.

A second, subtler point for the approved drugs: absence of a renal AE from a label's
adverse-reactions table is **not** a measured negative. AE tables list events above a
frequency threshold, so a real low-frequency renal signal would not appear. Labels cannot
settle these rows; the FDA Pharmacology/Toxicology reviews or the primary trial papers can.

## 3. Recommended reclassification (NOT applied)

Introduce a `renal_endpoints_measured` field with values
`measured_and_reported` / `not_measured` / `not_reported_in_source` / `cannot_determine`,
and set `nephrotox_grade = not_assessed` wherever it is not `measured_and_reported`.

- MSR042, MSR063, MSR078 → `not_assessed` (renal endpoints never measured)
- MSR044, MSR047 → `not_assessed` (not reported in the cited source; resolvable via reviews/trial papers)
- MSR045 → keep 0, annotate as efficacy-derived rather than safety-assessed
- MSR066 → keep 0, and replace `no_signal` with the quantitative value (eGFR −2.9 mL/min/1.73 m²)

The six remaining unchecked absence claims (MSR049 pegaptanib, MSR055 fitusiran,
MSR056 mongersen, MSR064 zilebesiran, MSR067 donidalorsen, MSR079 vupanorsen) should be
presumed suspect until retrieved; four of them are behind sources this environment cannot reach.

**Until this field exists, the dataset should not be used to train a nephrotoxicity model.**
That recommendation rests on the aggregate counts in §1 and the 7 retrievals in §2.

## 4. Method note

Two attempted multi-agent validation runs returned nothing: every parameterized subagent
tool call was rejected by a harness-level permission fault (`updatedInput` stripped of
required parameters; only parameterless tools such as `ListAgents` succeeded). ~2.4M tokens
produced zero retrievals across the two runs. All findings above were obtained by direct
inline retrieval instead, which worked without incident.

## 5. Update — 3 September 2026

Three approved DMD PMOs (golodirsen, casimersen, viltolarsen) were added from their
DailyMed labels, each contributing a human grade-0 row of the **measured** kind: the
labels prescribe the analytes (serum cystatin C, urine dipstick, UPCR — monthly and
quarterly) and then state affirmatively that "kidney toxicity was not observed in the
clinical studies". Endpoints prescribed, result negative — the distinction §2 found
missing from the WS rows.

Effect on the confound: anchor-sourced grade-0 clinical rows **1 → 4**, and the
association weakens from one-sided Fisher **p = 4.5 × 10⁻⁵ to p = 1.65 × 10⁻⁴**. That is
a 3.7× weakening achieved the right way — by adding well-sourced negatives, not by
removing positives. It is **not a resolution**: p = 1.65 × 10⁻⁴ still evidences strong
confounding, the 20 WS rows are unchanged, and the `renal_endpoints_measured` field
recommended in §3 remains unimplemented.

These three also strengthen the extrapolation evidence in the right direction. All three
are now bridge compounds with animal grade 2 against human grade 0, and unlike lumasiran
and vutrisiran their human negatives are supported — so of the 6 current
`animal_over_predicts` verdicts, 3 now rest on measured human negatives rather than
unexamined ones.
