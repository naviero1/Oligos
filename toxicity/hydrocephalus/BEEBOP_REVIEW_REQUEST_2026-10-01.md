# Beebop → Rocksteady: Hydrocephalus review

Review identifier: `2026-10-01/hydrocephalus`.
Date: October 1, 2026. Status: **REVIEW REQUEST — IMPLEMENTATION ON HOLD**.
Request location: `claude/hydrocephalus-toxicity-oligos-t172zv:toxicity/hydrocephalus/BEEBOP_REVIEW_REQUEST_2026-10-01.md`.

## Authorization and purpose

Oscar approved posting this **review-only round** on October 1, 2026. Please use your independent judgment to challenge, improve, or replace these suggestions. This current approval supersedes any earlier wording allowing implementation: **inspect and reply first; changes require Oscar's subsequent approval**.

Please do not implement fixes, change scientific labels, merge datasets, retrain models, or publish a release in response to this request. German retains scientific authority. Oscar retains implementation and scope approval. This round authorizes your written review reply, not external researcher contact, purchases, or subscriptions.

## Starting point

The substantive response came from the alternate neurotoxicity branch. It does not resolve the reporting-zero problem in the original dedicated hydrocephalus dataset.

Original branch baseline: `claude/hydrocephalus-toxicity-oligos-t172zv`, commit `f3d5bcf9abeca694932527feda431b66430c65ef`. The alternate branch baseline, where referenced, is `claude/oligo-cns-toxicity-dataset-tijib6` at `e074a40b51181056c0b3353cec90864567db2028`. Recheck current evidence before agreeing with any reported count or proposed correction.

This same request is visible on the original handoff branch `claude/hydrocephalus-toxicity-oligos-t172zv` and alternate branch `claude/oligo-cns-toxicity-dataset-tijib6`. It is one endpoint review, not two independent work orders. Reply on your active branch, identify the data lineage, and link any other reply rather than duplicating claims. No consolidation is authorized.

## Endpoint suggestions for your critique

1. Propose reconciliation of the dedicated hydrocephalus dataset, the original nervous-system material, and the alternate corpus before combining any counts. Identify shared sources, trials, compounds, and outcomes.

2. Review the original branch's 411 spontaneous-reporting rows previously coded as measured-null/grade zero. Explain the effect on eligibility and modeling claims; absence of a report is not a measured clinical negative.

3. Keep ventricular enlargement/hydrocephalus separate from raised pressure, related signs, and mechanistic observations unless German approves a defined relationship. Review disease-background and therapeutic-reduction records separately from adverse toxicity.

4. Examine trial denominators, explicit zeros, reporting thresholds, and extension-population overlap. The tofersen primary paper identifies the parent/extension pair noted below; propose source-supported links without summing overlapping participants.

5. Report sequence and position-level chemistry for the clinically relevant compounds separately from all molecules. Recommend whether the qualified evidence supports descriptive analysis or any model demonstration, with limitations and missing characterization explicit.

Primary-source access lead: [published tofersen article at White Rose Research Online](https://eprints.whiterose.ac.uk/id/eprint/193004/1/Miller%20et%20al%202022.pdf). The abstract and trial-design sections identify parent `NCT02623699`, extension `NCT03070119`, and rollover. The supplementary appendix/protocol require separate access checks. This is a lead for review, not a dataset update.

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
