# Beebop → Rocksteady: Chronic neurotoxicity review

Review identifier: `2026-10-01/chronic-neurotoxicity`.
Date: October 1, 2026. Status: **REVIEW REQUEST — IMPLEMENTATION ON HOLD**.
Request location: `claude/oligo-cns-toxicity-dataset-tijib6:toxicity/chronic-neurotoxicity/BEEBOP_REVIEW_REQUEST_2026-10-01.md`.

## Authorization and purpose

Oscar approved posting this **review-only round** on October 1, 2026. Please use your independent judgment to challenge, improve, or replace these suggestions. This current approval supersedes any earlier wording allowing implementation: **inspect and reply first; changes require Oscar's subsequent approval**.

Please do not implement fixes, change scientific labels, merge datasets, retrain models, or publish a release in response to this request. German retains scientific authority. Oscar retains implementation and scope approval. This round authorizes your written review reply, not external researcher contact, purchases, or subscriptions.

## Starting point

The substantive reply is on the alternate neurotoxicity branch. Its reported 26 missing sequences among 39 human laboratory compounds applies to that corpus, not automatically to this original branch.

Original branch baseline: `claude/oligo-toxicity-dataset-k394sz`, commit `d80eac1fc3970c814bd934050a2f17a9c1244a19`. The alternate branch baseline, where referenced, is `claude/oligo-cns-toxicity-dataset-tijib6` at `e074a40b51181056c0b3353cec90864567db2028`. Recheck current evidence before agreeing with any reported count or proposed correction.

This same request is visible on the original handoff branch `claude/oligo-toxicity-dataset-k394sz` and alternate branch `claude/oligo-cns-toxicity-dataset-tijib6`. It is one endpoint review, not two independent work orders. Reply on your active branch, identify the data lineage, and link any other reply rather than duplicating claims. No consolidation is authorized.

## Endpoint suggestions for your critique

1. Prioritize source recovery for the 26 of 39 human laboratory compounds lacking sequences in the alternate corpus. Verify which gaps are recoverable and link exact chemistry and outcomes; report the corresponding denominator for your own branch.

2. Review chronic-versus-acute eligibility at observation level using duration, timing, phenotype, and experimental context. Propose the categories and identify decisions requiring German.

3. Resolve parent/extension links and overlapping study populations before interpreting counts as independent evidence. The accessible tofersen paper identifies parent NCT02623699 and extension NCT03070119; inspect that primary-source lead.

4. Assess the proposed correction to the prior reply's characterization stance: include explicit purity and analytical-identity fields now, even when unknown, so missingness is measurable. Missingness records do not fulfill the requirement. If you disagree, propose a better auditable design.

5. Recommend one authoritative dataset lineage and a source/record crosswalk among branches. Review sponsor summaries and unquantified claims separately from source-resolved outcomes; do not merge lineages in this round.

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
