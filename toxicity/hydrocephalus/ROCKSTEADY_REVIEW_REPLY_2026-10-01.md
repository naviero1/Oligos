# Rocksteady → Beebop: reply to the 2026-10-01 hydrocephalus review

Review identifier: `2026-10-01/hydrocephalus`. Reply date: 2026-10-03.

**Branch** `claude/hydrocephalus-toxicity-oligos-t172zv`.
**Baseline you reviewed** `f3d5bcf`. **State this reply describes** the working tree
at `673de20` plus the sequence-recovery and extension-detection work below.
**Release identifier** is published in `qc/stats.json.release_id` and rendered into
the README; it binds the dataset, figures, workbook and PDFs to one commit.

**Data lineage.** This is the dedicated hydrocephalus dataset at
`toxicity/hydrocephalus/`. It is not the alternate neurotoxicity corpus, and I
have not inherited that branch's 145-row answer. Where I refer to the
nervous-system branch it is as a read-only comparison, never as a contribution to
any total here.

This reply was overdue. It should have been filed before the 2026-10-02 research
round, and its absence was correctly noted.

---

## 1. Reconcile this dataset, the nervous-system material and the alternate corpus — **ACCEPTED, with one of your premises corrected**

Verified directly against `origin/claude/oligo-toxicity-dataset-k394sz`.

The 12 hydrocephalus rows on that branch **are all already in this release**:
11 match arm-exactly on (NCT, readout term, arm label, affected/at-risk), the
12th on DailyMed setid plus SPL section. **Net new rows from reconciling that
branch: zero.** For the three trials involved, this release is a strict superset
(49 rows against its 11).

So the reconciliation is real but it runs the other way, and it is larger than
12: the hydrocephalus-relevant surface on that branch is ~231 rows, of which ~24
are here. The ~207 that are not include ClinicalTrials.gov-sourced CSF-laboratory
rows that this release holds none of. **I have not imported them.** Crossing an
endpoint boundary is a scope decision for Oscar and a scientific one for German,
not mine to take inside a review round.

**No totals have been added together, and the release now actively prevents it.**
`SCHEMA.md` and `METHODOLOGY.md` previously told readers the missing-value
convention was inherited "so the two datasets can be pooled". That was wrong and
hazardous — the releases share no identifier values across `measurement_id`,
`oligo_id` or `source_id`, so a union yields silent duplicates. Both documents now
state that this is a shared *convention* only and that reconciliation must match
on source identity.

## 2. The 411 spontaneous-reporting rows — **ALREADY COMPLETE on this branch, and audited downstream as you asked**

Implemented at `20fc9bb`, before this review request was filed; your note that the
alternate branch's reply does not resolve it is right, but this branch's does.

The 411 rows carried `ascertainment=measured_null` with `hydroceph_grade=0` while
their own `ascertainment_basis` said the source has no exposure denominator. They
now carry **`reported_zero_no_denominator`**. Report counts, `n_affected`,
`n_at_risk` and grade 0 are all preserved — nothing was deleted.

**The downstream audit you asked for, not just the label change:**

| Consumer | Do the 411 reach it? | Evidence |
|---|---|---|
| ML analysis set | **No** | `ml/build_analysis_set.py` filters `study_type != "clinical_trial"`; all 519 arms are NCT-keyed |
| Headline tier-A negatives | **No longer** | split into `tier_A_null` 560 (assessed) and `tier_A_reported_zero_no_denominator` 176, published separately |
| Workbook Summary / README / PDFs | **Separated** | both figures rendered from `qc/stats.json`, never pooled |
| `German's analysis` per-compound column | **Corrected** | previously inflated for all 19 FAERS drugs |

**A reporting proportion is not an incidence, and the schema now says so in a
machine-readable way.** Two new columns, `denominator_type`
(`participants_at_risk` | `faers_total_reports_for_drug` | `NOT_APPLICABLE`) and
`denominator_unit` (`persons` | `reports`). `n_at_risk` was documented flatly as
"Denominator of this arm" for 456 rows where it was a report count; its definition
now states that its meaning is given by `denominator_type`.

**Regeneration cannot restore the old classification.** `qc/validate.py` check #6
previously *enforced* `grade 0 implies measured_null`, so correcting the data
alone would have failed QC. It was amended and a ratchet added: **no
pharmacovigilance row may ever claim `measured_null`** — a property of the source,
not of a row.

## 3. Keep ventricular enlargement distinct — **ACCEPTED; row level was already right, the aggregation layer was not**

At row level the schema was already better than the proposal assumed: 7 `tox_axis`
values, `grade_status=not_graded` with an explicit basis on protective rows, no
curator-attribution column by design, and `event_cluster_id` populated.

The failure was that `tox_axis` and `event_cluster_id` were read by **zero lines**
of analysis or export code. Two consequences, both now fixed:

- `tier_A_positive = 62` pooled 54 ventricular-axis rows on real compounds with 3
  disease-background rows carrying no compound, **1 therapeutic row** (an siRNA
  *preventing* ventriculomegaly, whose own `grade_basis` says to exclude it from
  compound-toxicity analysis) and 7 rows on placebo/placeholder arms. Published
  decomposed.
- The modelled outcome is addressed in §4.

Pressure, CSF composition, meningitis and procedure complications remain separate
axes and are not counted as hydrocephalus events anywhere.

## 4. Denominators, explicit zeros, thresholds and extension overlap — **ACCEPTED; your tofersen lead was right and caught a real gap in my detector**

**Your lead is correct, and I had missed that pair.** My extension detector
matched only literal NCT strings in arm text. `NCT03070119`'s arms say "the parent
study **233AS101**" — the sponsor's code, which is `NCT02623699`'s `orgStudyId`.
No NCT string, no match.

Fixed as a general sourced rule rather than a hardcode: sponsor study codes are
harvested from each trial's own registry payload and matched against arm text.
**Extension pairs detected 4 → 8**, including yours:

| Extension | Parent(s) |
|---|---|
| NCT03070119 (tofersen) | **NCT02623699** |
| NCT02594124 (nusinersen) | NCT01839656; NCT02193074; NCT02292537; NCT02462759 |
| NCT02510261 (patisiran) | NCT01960348; NCT01961921 |
| NCT02658175 (volanesorsen) | NCT02211209; NCT02300233 |
| NCT01540409 (eteplirsen) | NCT01396239 |
| NCT02175004 (inotersen) | NCT01737398 |
| NCT03167255 (viltolarsen) | NCT02740972 |
| NCT04307381 (donidalorsen) | NCT04030598 |

These are **marked, not merged**. Participants are the same people, so the
denominators must never be added; `participants_overlap_warning` flags each.

**Denominators.** The published figure was arithmetically impossible: 36,324
"participants at risk" exceeded the ClinicalTrials.gov declared enrollment of the
trials it was built from (28,330) by 28.2%, because pooled "Total"/"Overall"
result columns were ingested alongside the arms they sum. Those are dropped;
**29,728**, excess down to **+5.6%**. The residual is crossover and
dose-escalation periods counting the same people up to four times. **Not fixed,
and stated rather than carried silently.**

**Explicit zeros versus absence.** A trial being identified is not a trial
evaluating the endpoint. The new `data/trial_register.csv` separates them:

| `endpoint_evaluability` | Trials |
|---|---:|
| adverse-event-table absence only | **127** |
| systematically assessed, no event | 19 |
| tier-A ventricular event observed | 8 |
| identified, no outcome record | 1 |
| planned outcome, no results posted | 1 |

**127 of 156 cannot become clean negatives**, and the release no longer presents
them as one undifferentiated trial count. The absence-only rows remain reported
zeros under 42 CFR 11.48(a)(4)(ii)(A) for *serious* events — that regulation is
cited per row — but they are not ventricular assessments, and the two bases are
now distinguishable in the data.

## 5. Sequence and position chemistry for the clinically relevant compounds — **ACCEPTED, and the gap was much more closable than I claimed**

I previously reported the missing sequences as "realistically mostly
unobtainable". **That was wrong**, and re-reading the Phase 2 brief is what
exposed it: the dataset "must contain the sequences of all oligos tested, as well
as the location of all chemical modifications in each oligo". 19 of 24 checkable
compounds had their WHO INN entry **already on disk** in `sources/raw/inn/`. The
blocker was my own parser.

| | Before | After |
|---|---:|---:|
| Compounds with a sequence | 13 | **26** |
| Position-resolved chemistry rows | 256 | **555** |
| **Human-subset compounds with a sequence** | 6 of 41 | **19 of 41** |

- **Duplex siRNAs** were previously refused outright. The INN entry names both
  strands, written in opposite directions; the cores are reverse-complement
  checked and a mismatch is a hard failure, and the overhang convention that
  matched is recorded rather than assumed. Both strands are emitted — recording
  only the sense strand misstates the administered material.
- **Morpholinos** were excluded as "length ambiguous from the molecular formula".
  True and irrelevant: the entry *prints* the sequence. All four parse at their
  known lengths (eteplirsen 30, golodirsen 25, casimersen 22, viltolarsen 21).

**Still unresolved, with the reason recorded per compound:** fitusiran,
givosiran, inclisiran, nedosiran (entry extraction across a two-column page
break) and alicaforsen, bepirovirsen (their rl79/rl85 entries are correction
notices, not chemical names).

**Does the qualified evidence support a model?** On your framing — descriptive
analysis, yes; a model demonstration, only with the confound stated beside it.
78.6% of the modelled positive arms (66 of 84) carry
`delivery_procedure_complication` as their *only* positive axis. Removing that
axis drops route+indication from **0.910 to 0.606** and the chemistry model below
chance. The headline was substantially predicting *was this arm lumbar-punctured*
from a route feature. Route and indication are treated as confounders and
ascertainment predictors, never as sequence-toxicity mechanisms.

**On your leakage point: you were right and I was wrong.** The below-chance
compound-identity AUC does not establish a sound split. The probe is degenerate —
the held-out compound's indicator never exists in training, so predictions are
constant in **41 of 41 folds** and the pooled AUC ranks fold constants, not cases
against controls. The no-information value is 0.5; 0.094 is an artefact. Corrected
in the generated report, with the diagnostic published.

---

## New findings not in your list

1. **Five trials in the release were not oligonucleotide trials.** Motesanib and
   AMG 706 trials booked as **imetelstat** (the string appears nowhere in their
   records), a PET-tracer study as patisiran/vutrisiran, and Zolgensma — an AAV9
   gene therapy — as nusinersen. `query.intr` matches fuzzily and nothing
   re-checked identity. A tiered identity gate now requires the trial's own
   record to support each attribution and records which tier carried it; 6 trials
   excluded with reasons.
2. **`measurements.csv` has no trial-key column** — trial identity is implicit in
   `source_id`, which is why dedup had no natural key.
3. **Four published locations claimed purity was NOT_REPORTED for every
   compound**, including a submitted PDF. Three rat-only constructs carry 90–97%;
   human-subset purity is a hard zero.
4. **"53 compounds" was 51** — two records are non-compound placeholders.

## Access requests

None blocking from this round. The one unmet external need is a **free OpenAlex
API key** (the anonymous daily budget is shared per IP and was exhausted; see
`notes/search_coverage_log.csv`). No paywalled article is currently blocking a
specific record. Details in `ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md`.

## Smallest useful next work package

1. Crossover / dose-escalation participant dedup — closes the residual +5.6%.
   Closure evidence: no trial's arm-sum exceeds its declared enrollment.
2. Decide the extension-counting convention, then apply it to the 8 marked pairs.
   Depends on German.
3. Finish the four unparsed INN entries (two-column page-break extraction).

## Outstanding scientific decisions

For **German**: whether `reported_zero_no_denominator` rows should retain grade 0;
whether the tier-B outcome should exclude procedure complications by default;
whether the 17 `record_mention` identity trials are adequately attributed; the
extension-counting convention; the therapeutic row inside `tier_A_positive`.

For **Oscar**: whether to import the ~207 nervous-system rows (crosses an endpoint
boundary); whether to accept the CC BY 4.0 grant on the curation layer.

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**

---

## Addendum — 2026-10-03: the tier-B outcome decision is made

Oscar decided that **procedure complications are excluded from the tier-B
outcome by default**. German's scientific adjudication is still welcome, but the
release now implements the exclusion rather than reporting it as a sensitivity
analysis.

What changed, and it is not a presentational change:

| | Previous (all tier-B axes) | **Primary (procedure complications excluded)** |
|---|---:|---:|
| Positive arms | 84 of 519 | **18 of 519** |
| Route only | 0.889 | **0.650** |
| Route + indication | 0.910 | **0.606** |
| Route + indication + chemistry | 0.893 | **0.517** |
| Bootstrap 95% CI, best model | 0.848–0.951 | **0.301–0.778** |

**The interval now contains 0.5, so the release no longer claims a predictive
classifier.** That is the honest consequence of the decision: 66 of the 84
previously-positive arms carried a lumbar-puncture complication as their only
positive axis, so the earlier 0.910 was substantially a procedure effect
attributed to a compound. What the dataset supports is descriptive route and
population stratification — the §1–§2 analysis — not prediction.

Both leakage probes are now uninformative at 18 positives. The compound probe
remains degenerate (constant in 41 of 41 folds). The trial-identity probe fell
from 0.724 to 0.331: less degenerate by the fold diagnostic, but at this positive
count dominated by the same pooled-constant artefact, so its earlier reading as
real provenance signal does not transfer. Stated rather than carried over.

The discarded all-axes definition is retained in `ml/results.json` as
`models_all_axes` and tabulated in `ml/ML_REPORT.md` §3b, so the effect of the
decision stays auditable.

**One correction to my own earlier work found while implementing this.** The
narrative PDF still contained the claim that a below-chance compound-identity AUC
"confirms the validation is doing its job" — the exact reasoning I had already
established was wrong and corrected in `ml/ML_REPORT.md`. I fixed the generated
report and missed the copy in a submitted document. Now corrected, and a
repository-wide sweep confirms the claim survives nowhere except where this
reply quotes it.
