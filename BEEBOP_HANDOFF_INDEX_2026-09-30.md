# Beebop to Rocksteady: toxicity review proposals

Date: 2026-09-30. Requested by Oscar Penny. Status: suggestions delivered for independent review and justified implementation; no claim that changes have been implemented or scientifically approved.

## Read the proposal for your endpoint

Rocksteady, please use your own intelligence to verify Beebop's findings against your latest work, challenge or improve the proposed methods, identify missing opportunities, and implement changes you can substantiate. Preserve source lineage and the team's scientific adjudication process. In the response file requested by your proposal, explain what you accepted, modified, rejected, deferred, or found already complete, with evidence, changed files, counts, and validation. These are collaborative proposals, not a rigid substitute for your judgment.

Oscar will prompt each Claude Code session to check this communication. No polling or messaging automation has been created. If your current checkout is another branch, read the linked proposal on the named branch without overwriting uncommitted work. Reconcile newer local work before applying any dated finding.

| Endpoint | Proposal | Branch |
|---|---|---|
| Kidney toxicity | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/toxicity/kidney/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/amazing-galileo-rwiv95` |
| Immunotoxicity | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/toxicity/immunotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/amazing-galileo-rwiv95` |
| Hepatotoxicity | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/toxicity/hepatic/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/amazing-galileo-rwiv95` |
| Complement activation | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/toxicity/complement-activation/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/amazing-galileo-rwiv95` |
| Thrombocytopenia | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/oligo-challenge-data-4um5mi/thrombocytopenia/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/oligo-challenge-data-4um5mi` |
| Coagulopathy | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/coagulopathy-oligos-toxicity-ap70gf/toxicity/coagulopathy/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/coagulopathy-oligos-toxicity-ap70gf` |
| Chronic neurotoxicity | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/oligo-toxicity-dataset-k394sz/toxicity/chronic-neurotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/oligo-toxicity-dataset-k394sz` |
| Acute neurotoxicity (supporting module) | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/oligo-toxicity-dataset-k394sz/toxicity/acute-neurotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/oligo-toxicity-dataset-k394sz` |
| Hydrocephalus | [Read suggestions](https://github.com/naviero1/Oligos/blob/claude/hydrocephalus-toxicity-oligos-t172zv/toxicity/hydrocephalus/BEEBOP_SUGGESTIONS_2026-09-30.md) | `claude/hydrocephalus-toxicity-oligos-t172zv` |

The immunotoxicity and complement folders were created for these proposals on the default branch because no dedicated populated branch was identified. Hepatotoxicity uses the existing `toxicity/hepatic/` folder. Please cross-reference any newer team work before proposing a new data pipeline. The acute module is supporting material, not a ninth equally required challenge toxicity.

## Oscar's firm presentation and counting requirements

1. Present human clinical trials first. Headline clinical-trial totals include only verified, deduplicated actual human clinical trials; do not substitute measurement rows, papers, participants, labels, cases, spontaneous reports, or animal experiments for trials.
2. Distinguish verified unique trials, endpoint-evaluable trials, outcome records, and unique compounds. Count the same trial once across its registry, papers, labels, and repeated outcomes. Do not sum overlapping participant denominators.
3. Keep human laboratory and ex-vivo evidence separate and prominent. They are not clinical trials, but are particularly relevant to phase two. Clinical data alone are not equivalent to human laboratory data.
4. Move animal evidence to separate supporting tables or an appendix and exclude it from human totals and default human-outcome summaries. Do not silently delete source data. Mixed/unknown-origin records remain unresolved until supported.
5. Let Rocksteady's evidence-based judgment improve the proposed implementation. Preserve German's role in scientific labels, controls, model eligibility, and final claims. Do not fabricate negatives, purity values, sequences, trial identifiers, or missing outcomes.

## Common gaps to review

- Different branches and Drive exports hold different versions; bind each accepted dataset, source inventory, figures, and documents to a release identifier.
- A source file or completed narrative does not establish scientifically qualified data or challenge compliance.
- Missing characterization should remain explicit, with a targeted recovery or clarification plan; recording `NOT_REPORTED` alone does not meet a missing requirement.
- Trial counts must be generated from a qualified study register. Baseline counts in the proposals are record counts unless explicitly stated otherwise.
- Do not add broad and scientist-governed thrombocytopenia inventories as independent data, or double-count nervous-system and dedicated hydrocephalus records.

## Required response

Use the response filename requested in the endpoint proposal and record: baseline/commit reviewed; proposal disposition and rationale; additional discoveries; implementation files; verified before/after counts by evidence class; checks performed; limitations; and decisions requiring scientific review. Published suggestions are not proof that Rocksteady has read them or completed the changes.

[Official challenge announcement](https://ncats.nih.gov/sites/default/files/2026-01/NIH-Challenge-Announcement-OligoTox-Open-Data-Challenge-Final-v5-508.pdf) · [Shared source folder](https://drive.google.com/drive/folders/10Tgb4qYxrZMoYunijx8xFR15pERyTP2b)
