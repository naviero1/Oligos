# Thrombocytopenia: proposals for Rocksteady's scientific review

**From:** Beebop · **Date:** September 30, 2026 · **Status:** Recommendations for review, not a scientific sign-off.

Rocksteady, please use your independent judgment to verify, challenge, and improve this proposal against your latest work. Implement changes you can justify within the user's authorized scope; explain accepted, modified, rejected, and unresolved recommendations in an adjacent response file. Preserve scientist adjudications and refer changes to biological interpretation or training eligibility for scientific review. A better evidence-backed alternative is welcome.

## Evidence baseline and limits

Read-only inspection of branch `claude/oligo-challenge-data-4um5mi`, commit `0a2fe619f62346dd27edc05a421658afaea560dd`, found:

| Evidence inventory | Observed value | Interpretation |
|---|---:|---|
| `data/oligos.csv` | 259 records | Compound records, not trials |
| `data/measurements.csv` | 1,959 records | Outcomes across several evidence types |
| `subject_class=human_clinical` | 1,002 records | Classification requiring trial-level verification |
| Human laboratory / ex-vivo | 426 / 25 records | Human mechanistic evidence, not clinical trials |
| Animal evidence | 497 records | Supporting evidence only in human-first summaries |
| Mixed species / unspecified | 4 / 5 records | Exclude from human counts pending resolution |
| Sequence field populated | 194/259 | Excluding blank, `TBD`, `NA`, `NOT_REPORTED`, `NOT_APPLICABLE`; validity and identity linkage require separate checks |
| Purity values | 0/259 | All carry `TBD` |

The earlier audit reported a Drive workbook at 254 compounds/1,878 measurements and a separate scientist-governed version 0.9 with 45 construct/product records, 110 human evidence records, 875 modification-position records, and 16 mechanistic candidates. Those Drive claims require version reconciliation before reuse; they were not independently reread for this branch inspection. The scientist-reviewed package reportedly has no qualified sequence-linked clinical negatives. Do not add these inventories together or overwrite its judgments with the larger branch dataset.

## Priority 1 — Make the human clinical-trial count defensible

The existing `scripts/split_human_animal.py` already separates human and animal measurements. That is useful, but its human output combines clinical, laboratory, and ex-vivo evidence. `STATUS.md` also describes older `human_clinical` row totals as “human trials.” Please replace that ambiguity with a study registry and separate views.

Suggested fields: stable study identifier, registry identifier where available, design, eligibility decision and reason, compound identity, intervention arms, participant population, enrolled/analyzed denominator, exposure and follow-up, source locations, and links to every measurement. Use an auditable local study identifier for older trials without a registry number; absence of registration alone need not disqualify an otherwise verified trial.

Match publications, registry results, regulatory reviews, pooled analyses, and labels to underlying trials. One trial reported in four documents is one trial. A pooled report is not an additional trial; include constituent trials in the count only when identifiable and independently supported. Clinical case reports, observational cohorts, spontaneous reports, and unspecified label summaries belong in separate human-supporting views.

**Acceptance:** Headline counts include only verified, deduplicated human trials with relevant platelet outcomes. Show screened trials, endpoint-evaluable trials, unique compounds, outcome records, and participants separately. Never sum overlapping patient denominators. Until verified, publish the trial total as “not yet established,” not 1,002.

## Priority 2 — Preserve scientist authority while reconciling versions

Please compare the broad collection and scientist-governed package using compound/construct identity, sequence and chemistry, source study, exposure, assay, and outcome. Build a crosswalk of retained, duplicate, conflicting, newly proposed, and excluded records. Retain original identifiers and adjudication history.

Keep clinical platelet-count reductions separate from platelet activation, protein binding, immune mechanisms, and other mechanistic readouts. These may support interpretation but are not interchangeable clinical outcomes. A negative needs evidence that the endpoint was assessed under a defined exposure and observation window; silence, absent warning language, and lack of a report are not measured negatives.

**Acceptance:** Every model-eligible row traces to a current scientific disposition. No record excluded or held by the scientist re-enters automatically during merge. If qualified clinical negatives remain absent, explicitly limit the clinical modeling claim; do not manufacture class balance from reporting silence or animal controls.

## Priority 3 — Put human evidence first without discarding animal support

Suggested workbook order: coverage and limitations; verified human trials; clinical-trial outcomes; human laboratory and ex-vivo evidence; other human evidence; unresolved records; animal appendix; cross-species comparison. Preserve canonical source tables and make views reproducible.

The current script computes pooled human-plus-animal maximum/mean grades, sorts `germans_analysis.csv` using pooled severity, and calculates human-versus-animal mean-grade differences. Please review these outputs. They mix heterogeneous ordinal scores, exposure conditions, and evidence types; they do not establish translational performance. Favor explicit endpoint, dose, duration, biological system, and review-status comparisons. Matching a compound across species alone is insufficient validation.

**Acceptance:** No animal record influences the displayed human clinical count, human outcome label, or default human ranking. Mixed/unknown evidence is visible and unassigned. Any retained aggregate severity or bridge statistic has a justified interpretation and clear limitations.

## Priority 4 — Close characterization and source-verification gaps

Prioritize sequence/chemistry confirmation and raw-source recovery for the human trial compounds and scientist-approved mechanistic candidates. Distinguish a reference sequence from demonstrated identity of the material tested. Recover position-specific chemistry, terminal modifications, characterization methods, purity values and basis, and sample/batch links where sources support them. Do not infer analytical purity from a patent sequence or reference identity.

For each unresolved requirement, record the missing item, sources searched, owner, next action, and stopping criterion. Recommend any author/manufacturer outreach for user review rather than initiating contact. Evaluate source content and supplements before declaring purity structurally unobtainable.

**Acceptance:** Priority eligible records have exact source locations for outcomes and identity links, or explicit unresolved flags. Verification means the correct value, compound, arm, exposure, and endpoint were checked together—not merely that a number occurs somewhere in a document.

## Priority 5 — Rebuild qualified outputs and document residual limits

Please regenerate exports and submission documents from the accepted version. `STATUS.md` currently mixes historical counts and completion statements; distinguish documents generated, source verification complete, scientist approval complete, and release eligibility. Reassess the existing model demonstration only after the population is qualified, with trial/source and compound leakage addressed. A smaller defensible collection is preferable to inflated readiness claims.

**Acceptance:** One build reproduces the study registry, inclusion/exclusion ledger, human-first workbook, animal appendix, counts, and matching narrative. Existing structural checks pass; targeted checks prevent duplicated trial counts, animal leakage, unsupported negatives, and reversal of scientist decisions.

## Requested response

Please provide an adjacent `ROCKSTEADY_RESPONSE_TO_BEEBOP.md` with one row per priority: accept/modify/reject/defer, evidence and rationale, files changed, before/after counts at the correct grain, validation performed, and remaining scientific decisions. Add gaps I missed and explain any superior approach. Do not treat publication of this proposal as scientist approval or as evidence that challenge requirements are satisfied.


Supporting source links: [scientist-governed version 0.9 workbook](https://docs.google.com/spreadsheets/d/1ysEdbKPbYR_kGnIQOlJNJijFyiyyowfi/edit); [scientific governance and model-readiness document](https://docs.google.com/document/d/1it5jNVAW5JUous8keFLlnoQr2Iqbwo02/edit).


## Posting and scope note

Posted to `claude/oligo-challenge-data-4um5mi`, path `thrombocytopenia/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.

Requirements reference: [official OligoTox challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Confirm current organizer guidance before final submission. The dataset's human laboratory relevance and mandatory characterization requirements remain distinct from the requested human clinical-trial presentation order.
