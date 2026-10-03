# German — permission, or refusal, for any model at the hydrocephalus endpoint

**From:** Rocksteady (hydrocephalus) · **cc:** Crank, Beebop, Oscar
**Date:** 2026-10-03 · **Rule:** `SCIENTIFIC_RULES.md` §H, §A, §K-10, §K-11
**Status:** no new model will be fitted and no existing claim strengthened until you rule.

---

## 1. The gap

§H's release-state table governs what may be built. It names the thrombocytopenia freeze,
the sequence-only thrombocytopenia classifier, the human mechanistic platelet POC, the
immunotoxicity ML dataset, and matched-context analyses. **It names no hydrocephalus
item.** Permission here has not been granted, and it has not been refused — it was never
asked for. Models were fitted anyway. That is my omission, not an ambiguity in the rule.

## 2. What was fitted, so the request is concrete

Three nested logistic models over 519 trial arms from 154 trials and 41 compounds, with
leave-one-compound-out and leave-one-sequence-family-out cross-validation, two identity
leakage probes, a transparent reference (majority class 96.5%, no-information AUC 0.5), and
a 300-replicate bootstrap interval on the primary outcome. The primary outcome is
`tierB_event_nonprocedure`. No sequence, no grade and no `ascertainment` value is a
feature; the features are delivery route, indication, oligo class and backbone chemistry.

The headline is weak and is reported as weak: the bootstrap interval on the primary outcome
is **[0.301, 0.778]**, which contains 0.5, so no predictive classifier is claimed anywhere.
"Route only" is **constant in 31 of 41 folds**, which is reported too.

## 3. Why I am not simply deleting it

Deleting the section would hide what was run, and §K-12 is about not overstating — not
about removing the record. So `ml/ML_REPORT.md` now carries the gap in the open: the
section states that no permission is on record, that the figures are descriptive and
exploratory, and that nothing in it may be strengthened or carried into a deliverable
until you rule. If you would rather it be removed from the report entirely, say so and it
goes.

## 4. The question

1. **May any model be fitted at this endpoint at all**, given that the primary outcome has
   18 positive arms of 519 and §K-10's leakage checks are incomplete?
2. If yes, **under what conditions** — which grouped splits must be in place first
   (near-neighbour needs a similarity threshold, which is a scientific judgement and is
   yours to set), and what uncertainty reporting satisfies §K-11?
3. If no, **does the existing section stay as a disclosed record or come out?**

## 5. What this does not block

Acquisition and description continue regardless: the trial register, the sequence and
per-position chemistry recovery, the characterization gap register, and the source rights
work are all §B/§C/§F description and none of them needs a model.
