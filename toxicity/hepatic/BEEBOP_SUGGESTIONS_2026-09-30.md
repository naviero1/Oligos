# Beebop suggestions for Rocksteady: hepatotoxicity

Date: 2026-09-30. Purpose: close the phase-two evidence gaps through your independent analysis and justified implementation.

## How to use this proposal

Oscar asks you to review these suggestions with your own intelligence, verify them against your latest work, complement them with findings I missed, and implement the changes you judge justified. Please challenge or replace my proposed methods when evidence supports a better approach. Explain what you accepted, modified, rejected, or found already complete. The implementation details below are proposals, not a substitute for scientific judgment. Preserve German's authority over scientific labels, controls, and final scientific claims.

Oscar's presentation requirement is firm: put human clinical trials first and count only verified, deduplicated human clinical trials in headline trial totals. Do not count individual outcome rows, patients, papers, labels, case reports, spontaneous reports, or animal experiments as trials. Show unique human trial identifiers, clinical outcome records, and distinct compounds as separate quantities. If a trial cannot be identified reliably, flag it as unresolved rather than guessing a count. Keep human laboratory and ex-vivo evidence separately visible because the challenge emphasizes human laboratory systems. Put animal evidence in separate supporting tables or an appendix and exclude it from every human total. Keep mixed-species and unknown-origin records outside human totals until resolved.

## Evidence available to this review

- Inspected default branch: `claude/amazing-galileo-rwiv95`, commit `8c7b9bfd7145f5f6af6e746793a2ef931380bcac`.
- `toxicity/hepatotoxicity.md` is an endpoint dossier. Five files are present in `toxicity/hepatic/sources/`; this is not five independent studies. The dossier identifies overlap between the Dieckmann article and supplements.
- No populated hepatotoxicity-specific measurement table was found in the inspected branches or the supplied shared Drive folder. This is a scoped finding, not proof that no team member has additional work.
- The dossier identifies potential source tables in Burdick 2014 and Dieckmann 2018, a missing Hagedorn 2013 supplement, and human-hepatocyte material in sources currently filed under kidney. Its proposed counts and source descriptions are leads to reverify, not newly validated data.
- The team work plan schedules hepatotoxicity for October. An empty table as of this review should not be presented as a missed October deadline.

## Suggested work, in priority order

### 1. Locate existing team work before rebuilding

Please check the latest branches, Drive material, and your own current working files for a newer hepatic dataset. If one exists, audit and extend it instead of starting another disconnected version. Record the authoritative branch, dataset version, source locations, and any superseded files. Update the endpoint dossier to distinguish acquired sources, extracted records, scientifically qualified records, and final release readiness.

Completion evidence: a short inventory with exact paths, counts from the actual tables, and the selected baseline. If no dataset exists, say so explicitly and create an appropriately scoped dataset rather than inheriting kidney records.

### 2. Build a human-first evidence collection with clear study units

Please prioritize source-resolved human clinical trials with liver outcomes and human laboratory systems. Give clinical trials their own first view; give human laboratory experiments a separate prominent view; retain relevant animal experiments as supporting evidence. A human clinical event is not a human laboratory result. A hepatocyte result should be classified by the actual species and biological system, not by the paper's title or its folder.

For clinical records, proposed fields include trial identifier, treatment arm, population, compound, dose/regimen, duration, endpoint, assessment window, result, units, denominator, comparator, and exact source location. Separate measured liver-injury outcomes, nonspecific adverse-event statements, and background disease. For laboratory records, preserve system, donor/replicate information when reported, delivery conditions, concentrations, times, assay, controls, and numeric outcomes.

Completion evidence: mutually exclusive human-trial, human-laboratory, animal-support, and unresolved views. Human-trial totals must reconcile to an identifier list. Do not invent a trial total from the number of papers or measurements. A verified zero trial count is acceptable if that is what the evidence supports.

### 3. Recover source-level outcomes without counting the same experiment twice

The existing dossier suggests that some Dieckmann values originate in Hagedorn and that the 236-compound panel requires material not currently held. Please verify that lineage before extraction. Treat duplicated article/supplement content as one experimental source. The cited human-hepatocyte figures may offer useful evidence, but first establish whether the readout actually supports liver toxicity, reflects another biological process, or is only a mechanistic observation.

Avoid counting an aggregate statement that 236 compounds were studied as 236 usable labeled records. Recover sequence-linked outcomes and source-defined controls. If digitization is needed, preserve the original image, extraction method, uncertainty, and scientific review instead of presenting approximate values as supplied raw data. Recheck the dossier's concentration units against the original source; extracted text may corrupt micro symbols.

Completion evidence: each included result links to an exact table/figure or structured record, and repeated publications are cross-referenced to the same underlying experiment.

### 4. Link molecular identity and chemistry, preserving unresolved gaps

Please encode sequences, strands, chemical changes by position, conjugates, and analytical characterization where reported. Distinguish a verified published sequence from experimental identity confirmation and purity of the tested material. Recover available supporting characterization or record the limitation; do not assume all purity data are obtainable or that none can be curated. A missing-value code does not itself satisfy the challenge requirement.

The dossier suggests compounds shared with kidney. Cross-reference them only after confirming sequence, chemistry, and construct identity. Preserve the different species, exposure schedules, and endpoints. A shared molecule does not make two experiments a matched cross-organ or cross-species validation pair.

Completion evidence: field-level completeness using eligible compounds as denominators, identity crosswalks, and a documented plan for unresolved required characterization.

### 5. Make labels and model claims follow the evidence

Please propose an endpoint-specific scientific definition and have German adjudicate it. Do not reuse kidney grades or treat an unreported liver event as a measured negative. Separate laboratory effects, enzyme changes, clinically adjudicated injury, and intended target-related effects where relevant. Retain original numeric outcomes and reference ranges before deriving categories. Use study/compound-family grouping if a modeling demonstration becomes justified; a small credible dataset is preferable to an apparently balanced set built from inferred negatives.

Completion evidence: a documented inclusion rule, source-based negative-control definitions, a scientist-reviewed modeling subset, and claims limited to what those records support.

## Phase-two packaging and response

Please align the final data dictionary, methodology, narrative, and Public Access and Dissemination Plan to one accepted dataset version. Review original-source redistribution terms rather than assuming the repository license covers every source file. All documents should report human trial counts separately from laboratory experiments and animal support. The challenge's focus does not require every endpoint to be equally mature; recommend a bounded scope if evidence acquisition proves inadequate.

Respond beside this file as `ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`, with: baseline reviewed; suggestion accepted/modified/rejected/already complete; scientific reason; changes and files; verification results; before/after counts by evidence class; additional discoveries; and decisions needing German or Oscar. Please include better alternatives and remaining limits rather than simply marking tasks complete.

Sources: [shared Drive](https://drive.google.com/drive/folders/10Tgb4qYxrZMoYunijx8xFR15pERyTP2b); `toxicity/hepatotoxicity.md`; `toxicity/hepatic/sources/`; [official challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Recheck current challenge guidance before final submission.


## Posting and scope note

Posted to `claude/amazing-galileo-rwiv95`, path `toxicity/hepatic/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.
