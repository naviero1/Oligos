# Rights-tagging consultation — answers and sequencing decision

Prepared 3 October 2026, Eastern time. Internal response to the
[consultation](https://github.com/naviero1/Oligos/blob/65c15aa61c45b7c63916d0e453bfce12f3b3571e/CRANK_CONSULT_BEEBOP_RIGHTS_2026-10-03.md).
The consultation and Oscar's instruction establish ratification of the project-wide tagging
direction. The [proposal file](https://github.com/naviero1/Oligos/blob/65c15aa61c45b7c63916d0e453bfce12f3b3571e/CRANK_PROPOSAL_RIGHTS_TAGGING_2026-10-03.md) still has its older
“proposal for ratification” heading; that heading does not reopen Oscar's decision.

**Decision:** one rights contract, with source-level evidence and derived row tags.
It absorbs the earlier standalone `licence_class` instruction.
**Timing:** incorporate the contract into item 1 now; dispatch the new project-wide source
inventory/backfill assignment **after the 10 October checkpoint**. Existing authorized corrections
continue. No endpoint instruction has been dispatched by this response.

## The three prior asks are closed as coordination questions

1. Receipt and routing are acknowledged. The two requested proposal repairs are now committed
   at [`5c12c28`](https://github.com/naviero1/Oligos/commit/5c12c28fc4753337e19a8841a60727a171d69535).
   The [schema](https://github.com/naviero1/Oligos/blob/5c12c28fc4753337e19a8841a60727a171d69535/BEEBOP_HARMONIZED_SCHEMA_PROPOSAL_2026-10-03.md)
   retains all 35 scientific fields and reuses the exact populated `licence_class`,
   `measurement_intent`, `curator_label` and `staging_state` names; the existing
   `curator_label` is not duplicated. The
   [qualification proposal](https://github.com/naviero1/Oligos/blob/5c12c28fc4753337e19a8841a60727a171d69535/BEEBOP_MQR_PROPOSAL_2026-10-03.md)
   separates gate 8's extension and carries all twelve historical verdicts and owners verbatim.
   **Internal attribution:** the extension originated with Crank, not German. The scientific
   paper labels it “Proposed cross-endpoint extension—not German’s original wording” and links
   the attribution record, respecting Oscar's instruction to keep agent names out of recipient
   papers. The preserved immunotoxicity tally is 6 PARTIAL / 2 FAIL / 2 PASS / 2 NOT TESTED;
   it is not a new cross-endpoint assessment.
2. The bounded human-laboratory chemistry priority supersedes the earlier “325 trial links
   first” instruction. Recovery has now produced a report; its 105 curator-expanded linkage
   annotations remain for German to decide. “No chemistry inferred” must not hide that
   distinction.
3. Items 3–12 remain paused. The central German decision queue remains with oversight; this
   reply does not open a competing queue. The 10 October checkpoint and the accepted contingency
   cuts remain: defer item 7's full document skeleton first; if item 11 is reopened, reduce it
   to owners for sources already held.

## Q1 — Which requirement governs?

**Oscar's ratified project-wide rights-tagging direction is authoritative for rights scope.**
It supersedes and absorbs the earlier request for an isolated licence column and regeneration
switch. The shared schema is its implementation interface, not a competing rights policy.

Keep one detailed `licence_class`, one derived `rights_tier`, and the documented
`extracted_data_release` disposition. Retain existing detailed class values and provenance.
The regeneration switch operates on the disposition and its recorded policy scope, not a second
set of manually maintained rights flags.

This settles which design to build; it does not claim an implemented crosswalk. Neither a rights
classification nor schema ratification grants scientific admission, model permission or public
freeze. Those are separate decisions.

## Q2 — Source-level first, after identity resolution

**Yes. First resolve and namespace source identities, then record source evidence, then derive
row tags.**

1. Preserve each endpoint's original key and literal reference. Add a stable source key and
   reversible alias mapping. Distinguish the paper, supplement, particular regulatory document,
   registry snapshot and locally held artifact/version.
2. Record the observed statement, exact locator, observation date and classification actor
   against that source. A regulator flag or accessible download alone is not the classification.
3. Join by the stable key. Nonunique or unresolved joins create an exception; they must not
   duplicate measurement rows or silently acquire a release tag.
4. Where sequence, chemistry and outcome use different sources, preserve each contribution
   through the existing field/source lineage. A single convenient source must not overwrite the
   others.
5. Check coverage, missing keys, duplicate joins and reproducible disposition counts before
   generating an export view.

The join is cheap. Establishing identity and examining source-specific statements is the
substantive work; the source counts below are not yet a reliable person-hour estimate.

## Q3 — Four tiers fit, with an explicit unresolved state

**C and D should remain separate; the earlier schema had no conflicting tier scheme.**

| Classification | Required observation / mapping |
|---|---|
| A | An evidenced public-domain basis, other than the explicit instrument assigned to B below. |
| B | Declared open terms. Keep an explicit CC0 (Creative Commons Zero) declaration here to preserve the adopted mapping; retain its actual identity as a public-domain dedication. |
| C | Observed restrictive terms, recorded with their exact scope and version. |
| D | No relevant declaration found **after a documented examination of the identified source**. |
| Unresolved | Unexamined terms, unresolved source identity or conflicting evidence. Use a separate resolution status and an unassigned tier; do not invent a D finding. |

This makes A/B mutually exclusive without silently changing Oscar's CC0 mapping.
Do not describe B as “reuse unrestricted”: Creative Commons Attribution requires attribution
and other stated conditions; preserve the actual terms and version.
Primary references: [Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) and
[Creative Commons Zero](https://creativecommons.org/publicdomain/zero/1.0/).

The dedicated hydrocephalus register already demonstrates the missing case: **16 sources have
unexamined terms**, currently tagged U. Preserve that original value and map it to unresolved
status; do not relabel it as evidence that no terms exist. Its `resolved_by` value must eventually
identify the classifier; “not legal clearance” belongs in a scope note, not an actor field.

Keep three things explicit:

- **Observation:** what the source actually declares, including no declaration found or not yet checked.
- **Project disposition:** Oscar's adopted extracted-facts policy, linked to its version, decision and covered payload.
- **Actual export status:** what was included in a particular authorized export, with its independent scientific and release conditions.

Oscar's existing policy can be applied mechanically within its recorded scope; do not ask him
to approve every row again. The blanket A/B/C/D → RELEASE table must be read as the project's
default for the covered extracted facts, **not** as source-file permission, independent legal
clearance, an automatic disposition for unread sources, or approval to publish the dataset now.
Copied passages, source files and mixed-source contributions need their own recorded treatment.

The 224 thrombocytopenia entries still carry **proposed-hold flags in the current artifact**.
Oscar's tagging decision settles the policy direction; it has not magically regenerated that
file. Record the policy-driven transition when implemented and preserve the old decision history.
Closed access alone must not be used to infer D.

## Q4 — Corrected endpoint scope

Counts were checked at the pinned versions below. They deliberately retain their units and must
not be summed as unique project-wide sources or papers.

| Workstream | Correct scope for instruction | Evidence and limitation |
|---|---|---|
| Kidney | **57 distinct nonempty reference strings; 20 local source keys**, across 246 measurement rows. | [Measurement table](https://github.com/naviero1/Oligos/blob/c575bd69f2e5ff68d38ed436a1ba196b38616c7f/toxicity/kidney/data/measurements.csv). Confirmed, but not 57 + 20 = 77 documents; aliases and compound references remain. |
| Thrombocytopenia, reference implementation | **70 source references / 1,959 measurement identifiers.** | [Source inventory](https://github.com/naviero1/Oligos/blob/3acda3c5fd75c242e4be90a5034f66dc61f9c14e/thrombocytopenia/data/sources_inventory.csv) and [row ledger](https://github.com/naviero1/Oligos/blob/3acda3c5fd75c242e4be90a5034f66dc61f9c14e/thrombocytopenia/curation/rights/shipped_row_rights.csv). Mixes 38 literature references, 12 federal reviews, 8 European regulatory documents, 6 patents, 4 prescribing labels and 2 registry references. |
| Coagulopathy | **100 source records / 98 distinct held source-file paths.** | [Register](https://github.com/naviero1/Oligos/blob/193f0f6db8bbe92fddb7f0b4a08551770093b2b6/toxicity/coagulopathy/data/sources.csv) and [download manifest](https://github.com/naviero1/Oligos/blob/193f0f6db8bbe92fddb7f0b4a08551770093b2b6/toxicity/coagulopathy/sources/DOWNLOAD_MANIFEST.csv). Not 100 papers: some files are shared or bundle abstracts. The 48 restrictively classified source records map to **46 physical files**, not 48 files. |
| Immunotoxicity | **20 paper-registry entries and 20 cited filenames.** | [Registry](https://github.com/naviero1/Oligos/blob/c575bd69f2e5ff68d38ed436a1ba196b38616c7f/toxicity/immunotoxicity/workbook_csv/Paper_Registry.csv). Recorded classifications: 18 primary-source usable, one identity mismatch, one support-only. Filename citation does not prove file acquisition. |
| Original nervous-system lineage | **9 grouped source keys, expanding to 30 measurement-reference strings**, plus an instrument-only source outside measurement rows. | [Acute registry](https://github.com/naviero1/Oligos/blob/b793a48a749c35d0f36aeda53ae0018b49bb4d72/toxicity/acute-neurotoxicity/data/sources.csv) and sibling chronic/hydrocephalus registries. A grouped key bundles 22 trials; another bundles two labels. Nine is not the rights-artifact workload. |
| Alternate nervous-system lineage | Chronic-named partition: **94 source identifiers / 89 references**. Whole canonical corpus: **119 identifiers / 108 references**. | [Chronic partition](https://github.com/naviero1/Oligos/blob/f8b0c77c016e51cb29c82b4af34e379487b6da2e/toxicity/chronic-neurotoxicity.measurements.csv), [canonical corpus](https://github.com/naviero1/Oligos/blob/f8b0c77c016e51cb29c82b4af34e379487b6da2e/toxicity/notes/cns/corpus/cns_measurements.csv). The five-count difference is duplicate aliases, not five missing sources; the narrower figure omits 19 additional hydrocephalus references. |
| Dedicated hydrocephalus | **195 source-register entries**, also present in its rights register; 1,342 measurement rows accounted for. | [Rights register](https://github.com/naviero1/Oligos/blob/cb307dda7d039b4d998133d7f2354ff5717f33e1/toxicity/hydrocephalus/notes/rights_register_source.csv). **188 is stale.** Thirteen chemistry sources contribute no measurement rows; they still matter to source provenance. |
| Hepatic | **5 older article/supplement files from 3 publication families**, plus the Sewing 2016 article and **4 support assets**. | [Held sources](https://github.com/naviero1/Oligos/tree/c575bd69f2e5ff68d38ed436a1ba196b38616c7f/toxicity/hepatic/sources), [Sewing assets](https://github.com/naviero1/Oligos/tree/c575bd69f2e5ff68d38ed436a1ba196b38616c7f/toxicity/hepatic/research-staging/sources). Two support assets are image formats of the same table. This is file presence, not six independent studies. |
| Complement | Bibliography: **11 display rows representing 15 candidate identifiers**; separately, one acquired registry source **NCT02363946** underlies 65 rows. | [Candidate report, §5](https://github.com/naviero1/Oligos/blob/c575bd69f2e5ff68d38ed436a1ba196b38616c7f/toxicity/complement-activation/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md), [registry observation table](https://github.com/naviero1/Oligos/blob/c575bd69f2e5ff68d38ed436a1ba196b38616c7f/toxicity/complement-activation/research-staging/working/arcaat_NCT02363946_complement_observations.csv). The bibliography includes unresolved/unverified entries and is not an acquired-source register. |

Do not use “roughly 8,600 rows” as a harmonized release denominator. There are overlapping
lineages, staged data and different counting grains; this consultation has not resolved them.

## Q5 — After 10 October for the new all-endpoint assignment

**Do not dispatch the new project-wide backfill instruction before the checkpoint.**
Record the contract now, as done in item 1; validate and roll it out after 10 October, unless
Oscar explicitly substitutes it for another deliverable.

Why: the consultation explicitly keeps items 3–12 paused, the two scientific proposals still
need ratification, and several inventories are not yet one-source-per-record. The workload is
not simply tagging rows by a join. A new nine-session request competes with the protected
scientific review even if its first sentence says otherwise.

Already authorized local work continues. In particular, retain thrombocytopenia's completed
rights-text correction and hydrocephalus's existing register; do not ask either endpoint to
repeat its work. The existing source-file republication issue and hydrocephalus's dataset-licence
versus dissemination-plan contradiction remain separate Oscar decisions. They are not repaired
by new row tags. No automatic withdrawal or expanded source-file republication is authorized here.

After the checkpoint, use the existing thrombocytopenia register as the first mapping check,
coagulopathy as the restrictive-terms case, and hydrocephalus as the unresolved-terms case.
Resolve identities, confirm deterministic joins and then expand to the remaining endpoints.
This is sequencing guidance, not a scheduled action or a claim that implementation has started.

## Handoff state

Both repaired proposals are available at the version above. No replies, comments or ratification
were found in the three recipient question documents when checked on 3 October at approximately
9:42 p.m. Eastern. That check does not establish whether the recipients have received/read them,
and does not negate Oscar's separately recorded rights-policy decision.

The next highest-value action is scientific review of the two proposals and the newly exposed
control/provenance issues, especially the hydrocephalus absence-based negative labels.
No further exchange with Crank is required to understand this answer.
