# Beebop → Rocksteady: chronic neurotoxicity gap-closing proposals

Date: 2026-09-30. Repository: `naviero1/Oligos`. Baseline: branch `claude/oligo-toxicity-dataset-k394sz`, commit `7aa7df9`; endpoint `toxicity/chronic-neurotoxicity/` and supporting material under `toxicity/_shared/cns/`.

Rocksteady, please verify these observations against your current files, use your independent scientific and engineering judgment to improve them, and implement the changes you judge justified. These are proposals, not a request for mechanical compliance. Please challenge an incorrect finding, identify missing work, and record why you accept, modify, or reject each proposal. Oscar's human-first presentation and human-trial counting requirements below are the fixed scope; you may improve the implementation.

## Observed baseline and central gap

The inspected endpoint table has **2,335 measurement rows and 13 oligo records**. Of those measurements, **2,329 are classified `human_clinical` and six `animal_invivo`**. The human rows comprise 1,548 clinical tolerability, 553 serious neurological, and 228 neuroinflammatory records; 2,318 rows refer to source `CT1` and 11 to `C1`. These are measurement counts, **not unique trial counts**. The six animal rows concern late-onset neurodegeneration. No human laboratory measurements are assigned to this partition.

The main gap is endpoint qualification: a neurological adverse-event term in a clinical source does not by itself establish chronic neurotoxicity, a causal drug effect, or an independently measured outcome. The older consolidated Drive workbook and shared documents contain different totals and scope. Please treat them as versions to reconcile, rather than sources of additional independent observations.

## 1. Establish a defensible human clinical-trial view

Please make verified human trials the first displayed evidence section. Create a trial-level register with stable study identifier, source identifiers, interventional-study verification, compound, arms/cohorts, observation period, endpoint assessment method, and links to corresponding measurements. Count each underlying human trial once, consolidating registry entries, publications, follow-up reports, and label summaries. Distinguish a separate extension protocol from duplicate reporting of the same cohort, and flag overlapping participants.

Report separately: (a) verified unique human trials, (b) the subset with usable chronic-neurotoxicity outcomes, (c) human clinical-outcome rows, (d) unique human compounds, and (e) human laboratory/ex-vivo experiments. Do not turn the 2,329 clinical rows, label mentions, case reports, or spontaneous reports into trial totals. Preserve unverified candidates in a pending register excluded from verified totals. A trial without usable endpoint results can be listed as identified, but cannot inflate endpoint-evaluable coverage.

**Completion check:** every counted trial resolves to source evidence; duplicate representations share a trial key; the headline total is generated from the register and reproducible.

## 2. Review what actually qualifies as chronic

Please propose a documented endpoint rubric for German's scientific adjudication. Capture exposure duration, event onset, persistence or reversibility, follow-up, neurological specificity, ascertainment, and source attribution separately. Avoid an invented universal duration cutoff. Where necessary use endpoint-specific criteria and retain the published rationale.

Review the current clinical-tolerability, serious-neurological, and neuroinflammatory groups. Separate source-supported chronic findings from acute events during a long trial, disease progression, procedure effects, nonspecific symptoms, and unresolved timing. Retain uncertain records in a clearly marked evidence layer; do not force them into either chronic positives or negatives. Clinical seriousness is not automatically a calibrated neurotoxicity severity grade.

**Completion check:** each modeling-eligible chronic outcome has an explicit eligibility reason, source location, timing evidence, and review status. Provisional grades remain provisional until adjudicated.

## 3. Preserve human laboratory evidence prominently and move animal evidence to supporting material

The sibling acute partition contains **34 human laboratory measurements**. Inspect their actual exposure and outcomes before deciding whether any additionally support chronic endpoints; do not reclassify them just to fill this gap. Maintain human laboratory and ex-vivo evidence as separately counted, visible sections because phase two emphasizes human laboratory systems. Put the six late-onset animal measurements in an animal appendix with cross-links, excluded from every human count.

Review the existing research queue for prolonged exposure, delayed effects, human neural models, and matched compounds across laboratory and clinical systems. Rank acquisition by direct chronic endpoint relevance and usable sequence/chemistry/outcome linkage, rather than number of rows available. Document a zero eligible-human-laboratory result honestly if that remains the result.

## 4. Reconcile overlaps, characterization, and modeling claims

The nervous-system branch also contains **12 hydrocephalus measurements**. Coordinate stable source/event identifiers with the dedicated hydrocephalus package so a consolidated submission cannot count them twice. Shared source material should remain reusable without creating duplicate experiments.

Generate characterization completeness specifically for the accepted human subset: sequence, per-position chemistry, purity, identity-confirmation evidence, dose, route, and duration. Reference sequence verification does not establish purity or analytical identity of the experimental material. Record missing characterization as missing and propose recoverable source leads; documentation alone does not close that requirement.

Reassess any predictive analysis after eligibility changes. Keep related records from the same trial, compound, and overlapping cohort together when splitting data. Report small numbers of independent compounds/trials and sensitivity to endpoint eligibility. Avoid claiming chronic sequence prediction merely because the consolidated dataset is large.

**Completion check:** all summary files and generated deliverables agree with the selected release; animal exclusions, unresolved records, overlapping cohorts, and endpoint exclusions are explicit.

## Requested response and implementation record

Please add a dated response listing each proposal as accepted, modified, or rejected, with evidence and rationale. Include additional recommendations from your own review; files changed; before/after unique-trial, outcome-row, and compound counts; validation results; and remaining blockers with owners. Identify questions requiring German's scientific judgment. Preserve original evidence and document transformations so Oscar can review the resulting scientific changes.


Please use the adjacent filename `ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md` for the requested response, with separate entries for each proposal and your additional findings.


## Posting and scope note

Posted to `claude/oligo-toxicity-dataset-k394sz`, path `toxicity/chronic-neurotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.

Requirements reference: [official OligoTox challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Confirm current organizer guidance before final submission. The dataset's human laboratory relevance and mandatory characterization requirements remain distinct from the requested human clinical-trial presentation order.
