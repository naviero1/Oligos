# Beebop suggestions for Rocksteady: complement activation

Date: 2026-09-30. Purpose: independently assess the evidence gap, improve these suggestions, and implement a defensible endpoint plan.

## Request and user requirements

Oscar wants your independent review, not mechanical execution. Please verify the observations below against your latest work, challenge weak assumptions, identify additional opportunities, and implement justified improvements. Accept, modify, reject, or replace each suggestion with an explanation. Scientific labels, endpoint definitions, and claims should respect German's adjudication. This file does not grant final scientific approval to unreviewed labels.

Put human clinical trials first. Headline trial counts must include only verified, deduplicated human clinical trials. Count clinical outcome rows and distinct compounds separately. Papers, case reports, labels, spontaneous reports, animal studies, and laboratory experiments are not interchangeable trial units. Human laboratory and ex-vivo evidence should remain separately prominent because these systems are central to phase two. Animal evidence belongs in separate supporting tables or an appendix, excluded from human totals. Mixed or unknown biological origin stays outside human counts until resolved.

## Starting evidence and uncertainty

- Baseline branch inspected: `claude/amazing-galileo-rwiv95`, commit `8c7b9bfd7145f5f6af6e746793a2ef931380bcac`.
- `toxicity/complement-activation.md` is an evidence/source dossier. I found no populated dedicated complement dataset in the inspected branches or supplied Drive folder.
- Existing material is mainly review and textbook discussion, with some adjacent material in kidney, coagulation, and immune sources. These are acquisition leads, not independent complement measurements.
- The dossier already identifies primary-source candidates, including material described as comparing monkey and human serum. Please verify the titles, identifiers, actual contents, and availability. This review has not independently validated every cited article.
- The work plan schedules complement work in September. The gap is currently the absence of visible qualified data, not the absence of a document titled complement.

## Prioritized suggestions

### 1. Verify whether newer work exists and make the scope decision explicit

Please first look for a newer dataset in your active work, other branches, and shared team material. If found, use it as the starting point and reconcile the obsolete dossier. If no newer work exists, propose a bounded acquisition and extraction plan with a realistic stop condition. The dossier's earlier suggestion to omit this endpoint is a recommendation, not an approved team decision.

Suggested deliverable: a source/availability matrix separating (a) actual human clinical trial outcomes, (b) human serum/plasma or other laboratory experiments, (c) animal evidence, (d) mechanistic background, and (e) inaccessible or unresolved sources. State what useful evidence could be added in the next work cycle. Escalate a scope recommendation to Oscar if no defensible human evidence can be obtained; do not silently call the endpoint complete or excluded.

### 2. Prioritize direct human measurements over adjacent toxicity claims

Start with the primary human-serum or comparative-serum leads already named in the dossier, then look for direct complement measurements in identified human trials. Verify whether a source supplies quantitative outcomes, assay context, dose/concentration, time, relevant controls, and traceable compound identity. Preserve species explicitly when the same paper includes several systems.

Do not infer measured complement activation solely from platelet decline, coagulation changes, infusion reactions, kidney lesions, cytokines, or a proposed mechanism. Such material may be valuable context, but it needs a separate role. A patent describing an assay that could be performed is not evidence that it was performed. A review repeating a primary experiment is not another experiment.

Completion evidence: every included complement outcome is linked to a measured endpoint and exact source location. Indirect observations are identifiable and excluded from direct endpoint totals and training labels.

### 3. Define a schema that preserves assay and exposure meaning

Please propose endpoint-specific tables and have German validate their biological definitions. Retain original readout names, values, units, assay method, control, sample matrix, donor/replicate information where available, exposure, sampling time, and source. Distinguish activation readouts from component abundance and functional assays rather than pooling unlike measurements. Preserve specimen-handling and delivery details when reported and relevant.

Separate administered dose, laboratory concentration, and measured exposure. Do not convert one into another without documented assumptions. Record uncertainty or missingness explicitly. Any grade should be secondary to the source result and scientifically justified for the specific assay; do not inherit a kidney or coagulation grade.

Completion evidence: a data dictionary with biologically distinct outcome classes, independently checkable units, and controls tied to the actual experiment. Do not encode unknown results as zero or define a negative from a missing mention.

### 4. Implement human-first views with auditable counting

For each verified clinical trial, retain a registry identifier where available or a documented stable study identifier with its evidence. Link papers, labels, and repeated timepoints to the same trial. A pooled trial summary without recoverable study identities remains pooled evidence and should not silently add to the trial count. Count distinct trials, distinct human-tested constructs, and outcome records separately. Avoid adding the same patients across timepoints or multiple publications.

Keep human laboratory experiments in their own view and animal work in an appendix. If no human clinical trials qualify, report zero verified trials in the inspected dataset; do not suppress useful human laboratory data or relabel it as clinical. Unknown species and mixed-source summaries need a review queue, not forced human classification.

Completion evidence: headline counts reconcile to the included identifier lists and a row-disposition log. Animal records must not enter human-only summaries or determine the displayed human toxicity score for a compound.

### 5. Establish compound identity and a credible translation claim

Capture exact sequences, strands, position-level chemistry, conjugates, and analytical characterization where sources support them. Identify mixtures or unnamed class-level observations separately from sequence-resolved constructs. Missing purity and experimental identity information must remain visible as unresolved requirement gaps, with a recovery or organizer-clarification plan.

Comparative human/animal evidence could be valuable, but shared compound names alone do not demonstrate translation. Verify matched construct, endpoint, exposure, and assay conditions before describing a comparison as a bridge. Let the data determine whether modeling is justified; a curated mechanistic dataset can be useful without a claimed clinical predictor. Ask German to assess any proposed negative class and all generalization claims.

Completion evidence: construct crosswalk, source-supported chemistry coverage, documented matching limitations, and a qualified modeling or descriptive-analysis subset.

## Packaging and response

Please align the endpoint's narrative, methodology, schema/data dictionary, and Public Access and Dissemination Plan to the accepted scope. Preserve original-source reuse terms and access routes. Report scientific readiness separately from file existence or structural checks.

Respond beside this file as `ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`. Include: latest evidence reviewed; accept/modify/reject/already-complete decisions; your additional findings and alternatives; implemented files; verification results; human trial, human laboratory, animal, and unresolved counts; and scientific or scope decisions for German/Oscar. Explain reasons for nonimplementation rather than forcing a change to satisfy this proposal.

Sources: `toxicity/complement-activation.md` and its cited primary-source leads; [shared Drive](https://drive.google.com/drive/folders/10Tgb4qYxrZMoYunijx8xFR15pERyTP2b); [official challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Recheck current challenge guidance before final submission.


## Posting and scope note

Posted to `claude/amazing-galileo-rwiv95`, path `toxicity/complement-activation/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.
