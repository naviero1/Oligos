# Beebop → Rocksteady: kidney gap-closure proposals

Date: 2026-09-30. Status: proposals for independent review and justified implementation; not scientific sign-off.

Oscar asked for a human-first presentation, counting only verified, deduplicated human clinical trials in headline trial totals and moving animal evidence to a separate supporting section. Please apply your intelligence to verify these findings against your latest work, challenge or improve the proposals, and implement changes you can substantiate. Preserve source records and provenance; document disagreements instead of mechanically accepting my assessment. German's scientific review should govern outcome interpretation and control eligibility.

## Observed baseline and provenance

Read-only inspection of branch `claude/amazing-galileo-rwiv95`, commit `8c7b9bfd7145f5f6af6e746793a2ef931380bcac`, found:

| Evidence | Observed count | Meaning |
|---|---:|---|
| Oligo records | 65 | Identity/design records; 55 have sequences |
| Human clinical measurements | 42 | Clinical evidence rows, **not 42 verified trials** |
| Human laboratory measurements | 67 | Distinct, prominent human-cell evidence |
| Animal laboratory measurements | 81 | Supporting appendix only |
| Animal in-vivo measurements | 56 | Supporting appendix only |
| Human–animal bridge records | 15 | Compounds appearing on both sides; not 15 validated translation assays |

Sources: `data/oligos.csv`, `data/measurements.csv`, `data/human_animal_bridge.csv`, `STATUS.md`, `CLINICAL_VALIDATION.md`, and `schema.md`. These are a dated baseline, not assumed current counts. Of the 42 clinical rows, 29 are marked `measured_and_reported`; 13 have other ascertainment states: three `not_measured`, two `not_reported_in_source`, eight `cannot_determine`. All 65 purity fields remain unreported. Scientific grades are described as provisional. The previous audit did not independently verify every original paper.

## Priority 1 — Establish actual human-trial coverage and a clean presentation

Please build a study register connecting each clinical measurement to its underlying study, source type, trial identifier when available, population, exposure, follow-up, renal endpoint, and exact source location. A regulatory label summarizing several studies is not itself a trial. A review, case report, or unresolvable pooled statement should stay visible as clinical supporting evidence without incrementing the verified-trial total.

Resolve aliases, secondary publications, extensions, and pooled analyses without double counting participants or trials. State your rule for counting extension studies and trials lacking registry identifiers. Use primary-publication metadata if sufficient; otherwise record the trial count as unresolved rather than inventing identifiers.

Suggested workbook order: summary of verified human trials; clinical measurements linked to those trials; other human clinical evidence; human laboratory evidence; identity/characterization and source tables; animal appendix; optional human–animal bridge appendix. Headline figures should separately report verified unique trials, human clinical measurements, and unique compounds. Human laboratory observations remain important to phase two but are not human clinical trials. Unknown or mixed-species rows do not enter human counts without row-level evidence.

**Closure check:** every counted trial has a traceable study identity and deduplication decision; the displayed total is reproducible; all animal rows are excluded. Avoid a positive trial-count claim until the register supports it.

## Priority 2 — Resolve negative-label eligibility before model use

Keep the 13 unsupported clinical negatives as evidence records, but exclude them from confirmed-negative modeling views pending source verification and adjudication. Recording the warning field alone does not prevent a downstream model from treating a retained numerical grade of zero as a negative.

Please recheck the remaining 29 records too: an endpoint measured for efficacy, generic renal monitoring guidance, or a label's absence statement does not automatically establish a measured safety negative in the actual trial. Retrieve available trial protocols, reports, and relevant supplements to distinguish monitoring recommendations from the assessments actually performed. Capture population exclusions and observation windows; absence of detected injury within one selected population is not universal renal safety.

Propose a derived eligibility field and reason rather than silently overwriting source assertions. Preserve original reported outcomes, separate normalized interpretations, and route disputed regrading to German. Avoid interpreting a change in statistical significance as a quantified reduction in confounding; compare effect sizes and ascertainment distributions if assessing that issue.

**Closure check:** no `not_measured`, `not_reported_in_source`, or `cannot_determine` row enters the confirmed-negative subset. Every accepted negative has an explicit measured endpoint, relevant exposure/window, source location, and review decision.

## Priority 3 — Keep quantitative endpoints comparable

The patent tables use different reference denominators: the human-cell table reports percentages of saline control, while the rat-cell table reports percentages of compound 1-1 reference. Please preserve denominator, raw value, uncertainty, delivery method, dose, duration, and assay context. Do not pool these values merely because both are percentages. Separate functional change, biomarker response, viability, and clinical renal injury unless a justified mapping is approved.

Review the provisional grading thresholds against controls and endpoint biology with German. The bridge's maximum-grade comparison can confound species with dose, assay, follow-up, source, and clinical ascertainment. Identify genuinely paired experimental comparisons separately from cross-study compound overlap; describe the latter as hypothesis-generating.

**Closure check:** incompatible normalizations cannot silently combine; a bridge verdict identifies its source measurements and limitations, and unsupported human negatives cannot produce claims that animals overpredict toxicity.

## Priority 4 — Close characterization and release-document gaps

Replace the absolute claim that purity “cannot be curated” with the narrower supported statement that it was not reported in the sources reviewed. Search targeted available supplements, analytical descriptions, and batch records; list unresolved material and proposed author/manufacturer requests for Oscar's approval rather than sending messages autonomously. Record batch linkage, method, purity value/range, and source wherever recoverable. Published reference sequence identity is distinct from analytical characterization of tested material.

Reconcile stale schema counts, clinical-validation text, generated tables, and submission narratives against the accepted release. Regenerate derived files through the existing scripts, expanding validation only where needed to check the new eligibility/counting rules. Keep documented unknowns explicit and do not describe missing requirement content as fulfilled merely because a column exists.

A useful near-term opportunity is a compact, well-qualified human renal evidence set with clearly linked mechanistic cell assays. That is more defensible than treating all 246 observations as interchangeable training examples.

## Rocksteady response requested

Create an adjacent `ROCKSTEADY_RESPONSE_KIDNEY.md` containing:

1. Baseline reviewed: branch/commit, data versions, and corrected counts.
2. Proposal dispositions: accepted / modified / rejected, reasoning, and evidence.
3. Implemented changes: files and resulting behavior; preserved historical records.
4. Verified human trial count and counting rule; separate human measurement, compound, and laboratory counts; animal appendix counts.
5. Additional findings and better approaches you identified.
6. Remaining scientific decisions for German and unresolved source access or characterization needs.
7. Verification performed, unresolved limitations, and readiness conclusion.

Please complete justified improvements, identify meaningful uncertainties, and explain the result so Oscar can review the scientific and presentation decisions.


## Posting and scope note

Posted to `claude/amazing-galileo-rwiv95`, path `toxicity/kidney/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.
