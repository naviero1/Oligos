# Beebop → Rocksteady: Coagulopathy review

Review identifier: `2026-10-01/coagulopathy`.
Date: October 1, 2026. Status: **REVIEW REQUEST — IMPLEMENTATION ON HOLD**.
Request location: `claude/coagulopathy-oligos-toxicity-ap70gf:toxicity/coagulopathy/BEEBOP_REVIEW_REQUEST_2026-10-01.md`.

## Authorization and purpose

Oscar approved posting this **review-only round** on October 1, 2026. Please use your independent judgment to challenge, improve, or replace these suggestions. This current approval supersedes any earlier wording allowing implementation: **inspect and reply first; changes require Oscar's subsequent approval**.

Please do not implement fixes, change scientific labels, merge datasets, retrain models, or publish a release in response to this request. German retains scientific authority. Oscar retains implementation and scope approval. This round authorizes your written review reply, not external researcher contact, purchases, or subscriptions.

## Starting point

A published response exists. It proposes 30 trials, but six study clusters require review and the study register is not yet linked to measurement rows.

Original branch baseline: `claude/coagulopathy-oligos-toxicity-ap70gf`, commit `c23b7656db54db3c128a912a2990e3b727976253`. The alternate branch baseline, where referenced, is `claude/oligo-cns-toxicity-dataset-tijib6` at `e074a40b51181056c0b3353cec90864567db2028`. Recheck current evidence before agreeing with any reported count or proposed correction.

## Endpoint suggestions for your critique

1. Assess the proposed next priority: link the study register to measurement rows and stable compound identifiers. Explain how to reconcile study totals with the actual human outcome subset and preserve arm, dose, time, and source locations.

2. Review the six flagged study clusters before relying on the 30-trial headline. Propose evidence-based merge/split decisions; trial identity and overlap are source-verification questions, not merely matching rules.

3. Audit species within categories named clinical outcomes. The prior audit found animal records in those categories. Clarify which categories mean human clinical events and which describe animal findings or indirect observations.

4. Review the boundary between intended anticoagulation, unintended laboratory changes, source-reported adverse outcomes, and curator-inferred harm. Identify the highest-priority records requiring German's adjudication.

5. Do not equate a matching numeric value in a paper with verified compound/arm/timing attribution. Propose targeted source-aware checks and characterize human-subset sequence, chemistry, and purity gaps.

## Shared review questions

- For each suggestion, state **accept / modify / reject / already complete**, with evidence and reasoning. Add important gaps or better alternatives that Beebop missed.
- Keep verified, deduplicated human trials separate from clinical measurement rows, publications, human laboratory experiments, and animal support. Human trials appear first; human laboratory evidence stays prominent; animal evidence belongs in a separate supporting view.
- Assess exact sequence, orientation, strand/duplex identity, position-specific chemistry, and tested-material characterization. Report source-verified coverage for the relevant human subset with explicit denominators. A populated sequence is not automatically verified; a shared base sequence is not proof of identical chemistry or tested material.
- Distinguish raw results, source interpretation, curator judgments, and approved model eligibility. Missing reports must not become negative outcomes.
- Recommend the smallest useful next work package, its closure evidence, dependencies, and the decisions for German or Oscar.

## Research sources and access

Use the [source compendium](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/RESEARCH_SOURCE_COMPENDIUM.md) and [access register](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/RESEARCH_ACCESS_REGISTER.md) as references. In your reply, list identified papers or supplements needed to close a specific gap but unavailable to you. Give the exact citation/link, required file, affected records, expected benefit, priority, attempted access routes, and observed barrier. Distinguish confirmed paywalls from login requirements, browser checks, missing supplements, and unresolved citations. Ask Oscar for the specific file when appropriate; do not assume a search-service subscription unlocks publisher content.

## Requested reply

Save your review beside this request as `ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`. Include your branch and commit, dataset version, point-by-point dispositions, evidence links or source locations, any new findings, access requests, recommended next work package, and outstanding scientific decisions. End with **REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**.

Beebop will assess your reasoning and respond after Oscar requests the next check. Agreement is not required; a supported disagreement is useful.
