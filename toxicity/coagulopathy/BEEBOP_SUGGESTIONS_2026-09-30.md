# Coagulopathy: proposals for Rocksteady's scientific review

**From:** Beebop · **Date:** September 30, 2026 · **Status:** Recommendations for review, not a scientific sign-off.

Rocksteady, please challenge and improve these recommendations using your own analysis and the latest source evidence. Implement justified changes within the user's authorized scope, preserve provenance and scientist decisions, and document what you accept, modify, reject, or defer. Refer changes to biological interpretation and training eligibility for scientific review. These proposals are meant to complement your work.

## Evidence baseline and limits

Read-only inspection of branch `claude/coagulopathy-oligos-toxicity-ap70gf`, commit `54f69aacfc140259dfcdf74264d8bb5d913eb91f`, found:

| Evidence inventory | Observed value | Interpretation |
|---|---:|---|
| Compounds / measurements | 218 / 2,685 | Distinct grains; neither is a trial count |
| Human-classified records | 1,183 | 749 clinical, 236 laboratory, 198 ex-vivo plasma |
| Animal / undetermined records | 1,476 / 26 | Separate supporting and unresolved evidence |
| `on_target_effect=TRUE` | 1,790 | Intended pharmacology flag, not automatic adverse toxicity |
| `unintended_toxicity=TRUE` | 630 | Existing curation flag requiring source review |
| Sequence entries / modification coverage | 104/218; 1,039 positions across 52 compounds | Coverage, not proof of material identity |
| Purity values | 0/218 | All `NOT_REPORTED` |
| Grade status | All 2,685 provisional | Includes ungraded rows; no final scientific grading approval implied |

Counts come from `data/oligos.csv`, `data/measurements.csv`, and `data/modifications.csv`. The earlier audit reported a Drive workbook at 213 compounds/2,388 measurements; this is a prior comparison requiring reconciliation, not a second dataset to add. This inspection checks structure and documentation, not every original experiment.

## Priority 1 — Separate intended coagulation effects from harmful outcomes

The existing two-axis design is useful: intended pharmacology and unintended toxicity can coexist. Please preserve it, but qualify each claim by source support. Anticoagulant activity, a prolonged clotting assay, reduced target-factor activity, bleeding, and thrombosis answer different questions. An intended effect can also cause harm; conversely, a desired laboratory change is not automatically an adverse outcome.

Proposed primary groups: source-supported adverse bleeding/thrombotic events; unintended laboratory coagulation disturbances; intended pharmacodynamic effects; measured endpoint-specific negatives; baseline/reference measurements; and unresolved observations. Preserve numerical measurements regardless of classification. Add an explicit evidence basis, reviewer status, and uncertainty for inferred `unintended_toxicity` decisions.

Review combination treatments, antidotes, background anticoagulants, population bleeding risks, and exposure context. Do not attribute a combination-arm outcome solely to the oligonucleotide. Cross-reference platelet-mediated bleeding with thrombocytopenia without duplicating the underlying trial in consolidated totals.

**Acceptance:** A reader can derive the actual adverse-outcome subset independently of the 2,685-row inventory. Both flags may remain true when justified. False flags do not become evidence of safety. No intended-pharmacology record becomes a toxicity positive solely through its target or assay direction.

## Priority 2 — Count actual human trials and order evidence accordingly

Please introduce a deduplicated study registry linked to source documents and measurement rows. `study_type=clinical` currently provides 749 records; this is not 749 clinical trials. Distinguish interventional trials, observational studies, case reports, labels, regulatory summaries, pooled analyses, and spontaneous reporting. Count only verified actual human trials containing relevant endpoint evidence in headline trial totals.

Suggested study identifiers include registry number where available and an auditable internal identifier when older trials lack one. Link arms, cohorts, compound identities, treatment combinations, enrolled/analyzed denominators, dose, timing, outcomes, and source locations. Deduplicate the same trial across its publication, registry results, and regulatory report; do not count pooled analyses as additional trials or sum overlapping participant populations.

Order outputs: verified human trials and their outcomes; human laboratory/ex-vivo evidence; other human evidence; unresolved evidence; animal appendix; optional cross-species comparison. Report distinct compounds, outcome records, and participants separately.

**Acceptance:** The headline trial total is reproducible from verified unique study identifiers. Until that work is done, mark the count as unestablished. Animal evidence, laboratory experiments, individual reports, and document counts cannot enter that total.

## Priority 3 — Review grading claims and normal-reference assumptions

`schema.md` says the rubric applies clinical thresholds to ratios against matched experimental controls because laboratory normal limits are usually absent. It acknowledges resulting low-end bias. The document also initially describes its thresholds as published criteria without modification. Please reconcile those statements and verify each endpoint-specific threshold against its primary grading authority before retaining the attribution.

Keep source-reported severity, measured value, control comparison, and curator-derived research score as separate fields. A research score using a matched-control denominator is not automatically a validated clinical adverse-event grade. Normal variation, baseline measurements, healthy controls, and genuinely measured nulls require explicit treatment. Review missing values, inequality-censored values, mixed units, and inferred ratios before converting them into grades.

**Acceptance:** Every displayed grade names its basis and approval status. Unvalidated scores are labeled as such and excluded from clinical severity claims. Baselines are not treatment outcomes, and weak near-control differences do not silently become clinical toxicity positives. Preserve any uncertainty rather than choosing the more alarming interpretation.

## Priority 4 — Qualify human systems and translational claims

The existing `species_class` and `species_class_basis` columns appropriately go beyond species labels: some purified systems use human proteins while their `species` field is `NOT_APPLICABLE`. Please preserve that source-backed distinction and add a clear human-system subtype: participant, primary blood/plasma, cells/tissue, or purified/recombinant proteins. Unspecified origin remains unresolved.

Human origin alone does not establish physiological relevance, toxicity prediction, or challenge eligibility. Discuss the limitations of purified-target assays separately from blood/plasma systems. Any human–animal comparison should match compound chemistry, relevant endpoint, exposure, timing, and biological context before supporting extrapolation. Retain these comparisons as supporting work while keeping animal data out of human-only totals.

**Acceptance:** Each human-system assignment is source-traceable; isolated biochemical activity is not presented as a human clinical result. Translational claims identify comparable evidence and validation rather than citing compound overlap alone.

## Priority 5 — Recover characterization, verify sources, and rebuild claims

Prioritize trial-linked and adverse-outcome compounds for sequence and position-specific chemistry recovery, purity/characterization searches, and sample identity linkage. A documented reference sequence is not analytical confirmation of the tested material. Represent strand-specific identity where needed instead of forcing multi-strand constructs into a single sequence field. Track unobtainable items explicitly; propose external inquiries for user review without initiating outreach.

The existing verifier documents whether numeric values appear in source text. This is useful screening but cannot alone confirm the correct compound, arm, outcome, timing, unit, or interpretation. Please prioritize manual/source-aware review of adverse outcomes, negatives, inferred classifications, and provisional scores. Record unresolved supplements and retrieval gaps without counting them as verified.

**Acceptance:** A release manifest ties data, schema, narrative, figures, and source-verification results to the same commit. Rebuild historical counts and overbroad completion claims from the accepted views. Add targeted checks for study duplicates, species leakage, unsupported negatives, and conflation of desired pharmacology with adverse toxicity; rerun the existing structural validation.

## Requested response

Please write adjacent `ROCKSTEADY_RESPONSE_TO_BEEBOP.md`: recommendation; accept/modify/reject/defer; supporting evidence and alternative reasoning; files changed; before/after counts separated by trial, compound, and outcome; validation; unresolved scientist decisions. Include anything this proposal missed. Generated submission files and passed structural checks should be reported separately from scientific approval and challenge eligibility.


## Posting and scope note

Posted to `claude/coagulopathy-oligos-toxicity-ap70gf`, path `toxicity/coagulopathy/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.

Requirements reference: [official OligoTox challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf), especially pages 3, 5–6 and 13–14. Confirm current organizer guidance before final submission. The dataset's human laboratory relevance and mandatory characterization requirements remain distinct from the requested human clinical-trial presentation order.
