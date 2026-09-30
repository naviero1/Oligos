# Beebop → Rocksteady: hydrocephalus gap-closing proposals

Date: 2026-09-30. Repository: `naviero1/Oligos`. Baseline: branch `claude/hydrocephalus-toxicity-oligos-t172zv`, commit `19fb6a6`, endpoint `toxicity/hydrocephalus/`.

Rocksteady, please independently verify these findings against your latest sources, complement them with your own analysis, and implement changes you judge justified. Treat this as an evidence-backed proposal for collaboration. Please challenge errors or suggest better solutions, recording acceptance, modification, or rejection with reasons. Oscar's human-first evidence presentation and human-only clinical-trial counting requirements remain fixed; you can improve how they are implemented.

## Observed baseline

The inspected release contains **1,361 measurement rows and 53 oligo-table records**, versus 1,329 measurements in the previously inspected Drive workbook. Two oligo-table records are non-compound controls/background; therefore 53 should not automatically be described as 53 compounds. Thirteen records have sequences and position-resolved chemistry; three constructs carry a published purity range of 90–97%. There are no human laboratory measurements in this release.

Study classifications include **789 `clinical_trial` rows, 456 pharmacovigilance rows, 88 regulatory-label rows, 15 clinical-case rows, three background-epidemiology rows, eight animal in-vivo rows, and two animal laboratory rows**. These are observations, not unique trial counts. Existing human/animal views help, but the human view still combines evidence types that must not become a single clinical-trial denominator.

## 1. Correct reporting zeros before using them as toxicity negatives

**411 pharmacovigilance rows are labeled `ascertainment=measured_null` and grade zero.** Their own `ascertainment_basis` states that the voluntary reporting system has no exposure denominator and that absence of a reaction term reflects reporting behavior as well as clinical absence. This is an internal semantic conflict, not merely missing documentation.

Please preserve the original report count while assigning a source-appropriate ascertainment category, such as reporting-zero/unknown-clinical-status. Remove eligibility as experimentally confirmed negative unless independent evidence establishes it. Update the generator and validation rules so regeneration cannot restore the misleading classification.

The same rows use `n_at_risk` for total reports naming the drug. Please separate report totals from exposed-person denominators, with explicit denominator type and unit. A reporting proportion must never be exported or modeled as clinical incidence. Positive spontaneous reports also need report counts distinguished from verified unique cases and causal attribution.

**Completion check:** none of the 411 reporting-zero records automatically supplies a measured-negative label; denominator semantics survive exports; affected summaries and model subsets are rebuilt. Check downstream eligibility rather than assuming every flagged source row entered the existing model.

## 2. Rebuild human trial totals and review trial negatives

Make a deduplicated, verified human clinical-trial register the first displayed section, followed by human laboratory/ex-vivo evidence and other human evidence in separate sections. Keep animal studies in an appendix. Count actual underlying trials once across registry entries, papers, regulatory summaries, and follow-up publications. Preserve trial arms and repeated outcomes as separate observations without inflating the trial total. Mark overlapping extension cohorts.

Please distinguish identified trials from trials with evaluable hydrocephalus outcomes. A registry record with no results cannot establish endpoint coverage. A missing adverse-event term, reporting threshold, or incomplete safety table does not universally establish a measured negative. Review each current trial-derived negative against posted tables, assessment method, collection window, reporting threshold, and denominator. Explicit zero-event reporting and protocol-assessed imaging outcomes should retain their different evidence bases.

**Completion check:** every headline trial has source-supported identity and eligibility; all negatives have traceable ascertainment; registry/publication duplicates share a trial key. Case reports, labels, background studies, spontaneous reports, and animal experiments contribute zero to trial totals. Human laboratory evidence may legitimately remain zero.

## 3. Preserve distinct endpoints and attribution

The schema already separates ventricular enlargement, pressure/composition disturbances, procedure complications, disease background, and therapeutic effects. Please verify that every export and analysis honors these distinctions. A pressure-related event or meningitis can support a mechanistic hypothesis without being a confirmed hydrocephalus event. A therapeutic reduction in ventricular enlargement is not automatically a nontoxicity control.

Retain source attribution separately from curator inference and from severity. Evaluate disease, age, delivery procedure, treatment, monitoring intensity, and background risk as competing explanations. Preserve matched comparator arms, and use existing event-cluster identifiers to prevent one episode becoming several independent events. Seek German's adjudication for disputed ascertainment, endpoint tiers, and provisional grades.

## 4. Reassess modeling after qualification

Review `ml/build_analysis_set.py`, its generated analysis set, and the report after label corrections. Compare results before and after strict negative eligibility, endpoint separation, and overlapping-cohort controls. Keep related trial/compound records grouped during evaluation. Treat route and indication as potential confounders and ascertainment predictors, not automatically sequence-toxicity mechanisms.

The current report interprets a below-chance compound-identity score as confirming correct validation. Please investigate that claim; below-chance performance alone does not establish a sound split or leakage protection. Report the evaluation design and diagnostic evidence directly. Avoid generalizing predictive claims beyond the sparse sequence-resolved subset.

## 5. Reconcile versions and characterize the usable subset

Reconcile the additional 32 measurements against the older Drive workbook. Also reconcile the 12 hydrocephalus measurements in the nervous-system branch using stable study/event/measurement identifiers. Do not add overlapping releases or events together.

Generate human-subset completeness for sequence, position-level chemistry, purity, material identity, dose, duration, and source access. Preserve the published purity range rather than inventing exact per-construct values. Reference identity is not proof of experimental-batch characterization. Prioritize recovery of human-relevant characterization and direct human laboratory sources, while reporting unavailable evidence honestly.

## Requested response and implementation record

Please add a dated accepted/modified/rejected response for each proposal, your additional findings, source evidence, changed files, and reproducible before/after trial, outcome, compound, and qualified-negative counts. Include scientific questions for German and remaining blockers with owners. Regenerate the workbook and narrative from the accepted data, preserving raw evidence and a reversible change log so Oscar can review the resulting changes.


Please use the adjacent filename `ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md` for the requested response, with separate entries for each proposal and your additional findings.


## Posting and scope note

Posted to `claude/hydrocephalus-toxicity-oligos-t172zv`, path `toxicity/hydrocephalus/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.

Requirements reference: [official OligoTox challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Confirm current organizer guidance before final submission. The dataset's human laboratory relevance and mandatory characterization requirements remain distinct from the requested human clinical-trial presentation order.
