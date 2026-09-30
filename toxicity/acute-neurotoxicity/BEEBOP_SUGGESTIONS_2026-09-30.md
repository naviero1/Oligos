# Beebop → Rocksteady: acute neurotoxicity supporting-module proposals

Date: 2026-09-30. Repository: `naviero1/Oligos`. Baseline: branch `claude/oligo-toxicity-dataset-k394sz`, commit `7aa7df9`; endpoint `toxicity/acute-neurotoxicity/` and shared material under `toxicity/_shared/cns/`.

Rocksteady, please independently verify these findings, improve the proposals with your own judgment, and implement justified changes. Your contribution should include challenges to my assumptions and additional opportunities, not simply following this list. Oscar's fixed request is human-first presentation, human-only clinical-trial totals, and animal evidence separated as supporting material. The methods proposed here remain open to improvement.

## Observed baseline and intended role

The inspected acute partition has **1,866 oligo records and 2,081 measurement rows**: **1,825 animal laboratory measurements**, **222 animal in-vivo measurements**, and **34 human laboratory measurements**. Its study-type field contains laboratory and animal experiments, with **no rows presently classified as human clinical trials**. Source `H1` contributes 2,006 rows; `K1` contributes 41; human sources `HV1`, `HV2`, and `HV3` contribute 9, 8, and 17 respectively.

This is useful supporting science, but its row volume should not imply equivalent progress on chronic neurotoxicity. The phase-two brief gives acute neuronal electrical toxicity lower priority. Please position this collection as supporting work, rather than inventing a ninth equally required endpoint or diverting effort from the priority human evidence gaps.

## 1. Make human evidence first without relabeling laboratory experiments as trials

Please show a small human clinical-trial coverage section first. Its verified eligible total should be **zero unless source review identifies actual qualifying human trials**. State that this means none established in this module, not that no relevant trials exist anywhere. Record identified-but-unverified trial candidates separately, excluded from the verified total.

Immediately follow with the human laboratory section, preserving the 34 measurements and distinguishing unique compounds, independent experiments/studies, doses, timepoints, and replicate structure. Human in-vitro and ex-vivo studies are valuable evidence; neither is a clinical trial. If a clinical source is later added, verify its trial identity and consolidate its registry, papers, and label summaries under one trial key before counting it. Clinical case reports and spontaneous reports remain separate evidence types.

Move the 2,047 animal measurements to supporting tables or an appendix, retaining sequence and source links. Keep animal laboratory and animal in-vivo counts distinct. Species-unknown or mixed records require review and are excluded from human totals until resolved.

**Completion check:** the human clinical-trial total is computed only from verified trial records; all 34 currently classified human laboratory rows remain separately visible; no animal row contributes to a human total.

## 2. Recheck the biological meaning of the human laboratory subset

Please verify species and model identity from primary source methods, including cell provenance, differentiation state, endpoint, exposure duration, dose, formulation, comparator, replicate count, and sequence/chemistry linkage. A human sequence target or an oligo intended for human treatment does not make an animal assay a human system.

The existing `invitro_human_neural_toxicity` axis may cover mechanisms broader than acute electrical toxicity. Review whether each human experiment measures neuronal excitability, viability, neurite changes, inflammatory responses, intended target activity, or another effect. Preserve the original readout and avoid equating intended biological activity with injury.

Ask German to adjudicate disputed endpoint assignments and severity mappings. Where exposure or outcome supports another endpoint, propose a shared evidence record with endpoint-specific qualification; do not duplicate the experiment or automatically move every human row into chronic neurotoxicity.

**Completion check:** every accepted human experiment has a traceable source locus and endpoint eligibility rationale; uncertain records remain flagged rather than assigned a fabricated grade.

## 3. Describe translational pairing accurately

The shared documentation highlights 181 compounds paired between a rat laboratory assay and mouse in-vivo tolerability. This is animal-to-animal pairing. It should not be described as an established bridge from human laboratory systems to animal outcomes.

Please identify actual shared compounds between the human and animal experiments, comparing full sequences, modification positions, route, dose, formulation, exposure, and outcome. Classify each proposed link as exact compound, related analogue, or mechanistic context. Different endpoints or unmatched chemistry require explicit caveats; sequence similarity alone does not establish predictive transfer.

Where sufficiently matched data exist, propose a bounded exploratory analysis. Otherwise present the pairing gap and the highest-value sources needed to close it. Review the queued human sources for usable quantitative outcomes rather than counting unextracted sequence lists as completed experiments.

## 4. Resolve documentation, characterization, and model-readiness discrepancies

The shared readme still describes an older 1,839-oligo/2,065-measurement release and says no human laboratory data were found, while its open-items file records the later 34 human measurements. Regenerate current scope and counts from the accepted endpoint tables and clearly mark archived consolidated versions. Do not silently combine historic releases.

Please report sequence and chemistry coverage separately for human and animal subsets; the large animal screen cannot substantiate human completeness. Recover purity and material-characterization evidence where available and distinguish a purification method from a reported purity value. Preserve missing values honestly.

For retained predictive analyses, explain the narrow chemistry/source distribution and use evaluation groups that keep correlated compounds, studies, and repeat measurements together. A strong animal-screen result should remain an animal-screen result. Document provisional grading and the unresolved source disagreement about divalent-cation rescue rather than presenting a settled mechanism.

**Completion check:** all generated summaries agree with the human-first tables; claims state their species, endpoint, and independent sample size; the phase-two contribution and remaining characterization gaps are explicit.

## Requested response and implementation record

Please return a dated acceptance/modification/rejection record with supporting evidence, your additional proposals, changed files, before/after counts, validation results, and outstanding decisions for German or Oscar. Preserve original evidence and document transformations. A justified decision to keep this module limited and supporting is a valid outcome; expanding animal row counts is not required to close the human-priority gaps.


Please use the adjacent filename `ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md` for the requested response, with separate entries for each proposal and your additional findings.


## Posting and scope note

Posted to `claude/oligo-toxicity-dataset-k394sz`, path `toxicity/acute-neurotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.

Requirements reference: [official OligoTox challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Confirm current organizer guidance before final submission. The dataset's human laboratory relevance and mandatory characterization requirements remain distinct from the requested human clinical-trial presentation order.
