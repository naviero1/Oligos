# Minimum Qualified Record proposal — 3 October 2026

**PROPOSAL FOR GERMAN'S RATIFICATION — item 2 only.**

**Scientific reviewer:** German García-Fresco. **Engineering reviewer:** Oscar Penny. **Prepared by:** Beebop. **Package due:** 10 October 2026.

This MQR (Minimum Qualified Record) proposal translates the twelve sign-off gates published in `SCIENTIFIC_RULES.md` §K into a reproducible evidence checklist. It proposes a review mechanism; it does not qualify records, authorize training, confer scientific authority, or grant a release. No endpoint records have been adjudicated through this proposal.

**Source pin:** [`SCIENTIFIC_RULES.md`](https://github.com/naviero1/Oligos/blob/e9d4f6da4f455f0c39f2405f31a18779f34a5a2d/SCIENTIFIC_RULES.md), repository `naviero1/Oligos`, default-branch commit `e9d4f6da4f455f0c39f2405f31a18779f34a5a2d`, file blob `b85d50d49ecd2ca9da841f2f0af2973626517a5c`.

That file explicitly identifies itself as Crank's derived reference. German's underlying governance documents remain authoritative and have **not** been independently reviewed for this proposal. Section K now permits proposals derived from this reference. Ratification must resolve any discrepancy with the underlying documents before an authority claim is made.

## 1. Proposed meaning and boundary

An **MQR candidate** is a versioned observation and its linked construct identity, accompanied by evidence for the applicable checklist and an explicit account of unresolved gaps. Calling a record a candidate is an administrative state, not a completeness tier, toxicity label, safety finding, scientific acceptance, or model-eligibility decision.

The primary observation grain remains exactly that in §B:

> oligo × chemistry × strand state × dose × time × donor / cell system × delivery condition × endpoint

Use the two linked primary tables required by §B: a canonical oligo table for identity, sequence and chemistry, and an experimental-observation table for the measured condition and outcome. A named medicine, shared sequence, or sequence-family group does not establish identical administered constructs. Chemistry, strand, conjugate, stereochemistry and formulation differences remain visible. Do not merge records or re-grain existing one-row-per-oligo data through this checklist.

The checklist is an engineering sidecar to those two tables. Its references, decisions and attachments do not introduce a competing biological observation table. All fields required by §C remain in the schema; additional endpoint fields may be proposed. Position chemistry is primary. Molecule-level chemistry flags, composite outcomes and summary rows remain secondary derivations.

## 2. Twelve gates: source text and proposed evidence

The numbered gate wording below reproduces §K; line wrapping is normalized. The gate 8 parenthetical generalization is already supplied by that source. No other gate is replaced or relaxed here. Abbreviations in the quoted source: TLR (Toll-like receptor), QC (quality control) and LOPO (leave-one-paper-out).

### Gates 1–9: record evidence and linked source checks

**1. Every training row has a traceable primary source and exact source location.**

Attach the primary-source identity, source address, acquired-file identity and checksum, and exact table, figure, page, supplement, sheet or row locator. Preserve source-row lineage through every transfer. A review article or a file-level citation alone is insufficient. Proposed structural check: the locator exists and the referenced source and file resolve; scientific adequacy remains reviewable (§§A, B, D, I).

**2. Every sequence is verified 5′→3′, with strand identity and duplex partner where applicable.**

Link `sequence_5to3`, `strand_role` and `duplex_partner_id` to exact sequence evidence and a verification record. Preserve the source representation as well as any documented normalization. Record an unresolved partner or direction as an exception, not an inferred sequence. “Not applicable” for a duplex partner requires a source-supported strand state and review (§§B, C).

**3. Every chemical modification is encoded by position, not only as a molecule-level flag.**

Attach source-backed `backbone_by_linkage`, `sugar_mod_by_position`, `base_mod_by_position`, `terminal_modifications` and relevant `gap_length_nt`, with sequence coordinates and strand associations. Structural validation can flag inconsistent lengths or coordinates; it cannot fill missing modifications. Unknown stereochemistry or uncertain identity remains unresolved, without flattening distinct constructs into one (§§B, C, G).

**4. Assay context includes cell system, donor information, delivery/formulation, dose and exposure time.**

Link the exposure/system fields in §C to source evidence. Preserve dose value and unit, exposure duration, species, biological system or population, sample state, donor information, formulation and delivery conditions. For clinical observations, retain the source's population and exposure description rather than inventing a cell system or donor identifier. German must ratify any endpoint-specific applicability treatment; missing context is disclosed (§§B, C, D).

**5. Raw/continuous outcomes are retained when available; curator-derived binary labels are explicitly marked derived.**

Retain `raw_value`, `raw_unit` and `author_interpretation`, with source thresholds, fold changes and significance when provided. Keep `curator_label` separate and carry its derivation and authorized decision lineage when one exists. This proposal authorizes no new labels. A binary-only source should be identified as such, without fabricating a continuous value (§§A, C, E).

**6. Agonist, antagonist, potentiator and inert/low-response states are separated.**

Preserve the source-supported response state and context through `immunomodulatory_direction` and associated evidence, including mixed or unknown states. Do not treat an antagonist as an ordinary negative, or a non-stimulatory finding as safety. An agent may transfer an existing source statement but cannot infer a scientific classification. Where the terminology does not map directly to an endpoint, flag applicability for German rather than marking an automatic pass (§§A, C, E, J).

**7. Human and animal observations are not pooled as interchangeable ground truth.**

Carry explicit evidence-lane membership: human clinical, human ex vivo/laboratory, or animal. Preserve intended pharmacology separately from adverse toxicity. A mixed or uncertain source must be resolved into supported observations by an authorized decision; it cannot be assigned to a convenient lane. Completeness tiers are scored per lane and never substitute for labels or eligibility (§§B, D, E).

**8. TLR7, TLR8 and TLR9 outcomes are not collapsed prematurely. (Generalizes to: endpoint-specific outcomes are not collapsed into a composite; a composite is a secondary derived field only.)**

Preserve `endpoint_name`, receptor/pathway and measured outcome at the original endpoint grain. Keep platelet count, activation, coagulation, bleeding and thrombosis distinct, as well as receptor- and cytokine-specific measurements. A proposed secondary composite must link to its component observations and derivation; it cannot replace them (§§B, C, E, K).

**9. Citation metadata and file identities pass QC.**

Record the exact source version, identifier, checksum, source-to-file match, locator verification and known correction status. Check §I corrections, including Goodchild 2009 and the Herzner/Hornung misidentification. A successful file download proves neither correct attribution nor row provenance. Unresolved per-row provenance stays excluded from validated training data (§§A, B, I).

### Gates 10–12: dataset, analysis and claims checks

These gates attach to a versioned dataset or analysis and are linked back to each candidate through its proposed use. They are not waived because an individual record is well documented.

**10. Train/test splitting has been checked for exact-sequence, modified/unmodified counterpart, strand, family, paper and experimental-series leakage.**

Attach the dataset snapshot, grouping manifest, split specification, leakage-check output and unresolved collisions. Include laboratory, near-neighbour and matched-pair grouping required by §G, in addition to the dimensions named in this gate. `sequence_family_group` and `paper_group` must exist from the start. Shared grouping must not merge chemically distinct constructs. Random row splitting is prohibited (§§C, G).

**11. LOPO and sequence-family grouped performance are reported with uncertainty.**

For a permitted model, attach both performance reports, uncertainty methods/results, fold populations and failed or degenerate folds. Include transparent null/majority, length-only, chemistry-only and family-only baselines as required by §G. Do not run a prohibited model to complete this checklist. Before a model is authorized and evaluated, this gate remains unassessed and the model claim remains blocked (§§A, G, H).

**12. All major mechanistic and clinical claims are no stronger than the evidence supports.**

Attach a claim-to-evidence record identifying the exact statement, supporting observations, analysis version, limitations and German's disposition. Descriptive findings cannot become clinical prediction or universal causal rules. Document where a proposed claim was narrowed, rejected or deferred. Neither checklist completeness nor an internal performance statistic authorizes clinical accuracy language (§§G, H, J).

## 3. Proposed review record and states

These are **engineering proposals**, not additional scientist-authored gates. Implement one checklist entry per gate and review scope; reuse dataset-level evidence by reference rather than copying it into each observation.

| Proposed field | Required content |
|---|---|
| `checklist_version`, `rules_commit` | This proposal/version and the pinned rules version used. |
| `candidate_id`, `construct_record_id`, `observation_id` | Stable links to the candidate and both primary tables, using the schema proposal's exact construct key; no identity equivalence inferred. |
| `scope_type`, `scope_id`, `scope_version` | Observation, dataset/split, model evaluation or claim; immutable reviewed snapshot. |
| `gate_id`, `criterion_source` | Gate 1–12 and supporting rule sections. |
| `evidence_refs` | Source/file checksum, precise locator and supporting review or analysis attachments. |
| `evidence_status`, `checked_by`, `checked_at` | Administrative evidence state, actor and time. |
| `exception_refs`, `applicability_note` | Missing information, conflicting evidence or proposed applicability treatment. |
| `scientific_disposition`, `decision_ref` | German's recorded decision, scope, conditions and evidence version; absent until supplied. |
| `supersedes_review_id` | Prior review invalidated or replaced after a material change. |

Proposed **administrative evidence states** are `NOT_ASSESSED`, `EVIDENCE_LINKED`, `GAP_DOCUMENTED` and `CONFLICT_OPEN`. `EVIDENCE_LINKED` means attachments exist; it is deliberately not called “passed.” Structural checks may report formatting or reference failures without assigning scientific meaning.

Proposed **scientific dispositions**, recorded only from German's explicit decision, are `PENDING`, `ACCEPTED_FOR_STATED_SCOPE`, `REVISION_REQUIRED` and `NOT_ACCEPTED_FOR_STATED_SCOPE`. These administrative terms do not populate toxicity labels or replace German's own terminology. Any approved exception must retain its exact scope and conditions; an agent cannot manufacture an exception.

Overall candidate states are `DRAFT`, `SUBMITTED_FOR_REVIEW`, `REVISION_REQUIRED` and `REVIEW_RECORDED`. No automatic `QUALIFIED`, `SAFE`, `MODEL_READY` or `RELEASED` state is proposed. A recorded decision must be read at its actual scope. Record acceptance cannot be presented as approval of an unreviewed split, model, claim or release.

## 4. Missingness and controls remain explicit

Under §F, absent analytical identity or purity remains `NOT_REPORTED` unless primary characterization or lot-level records are recovered. Preserve this truth in the relevant field and link a **Characterization Gap Register** entry recording what is missing, why, attempts made and the evidence required to close it. Do not replace absent batch values with typical, inferred or group-level values.

The field value and gap entry satisfy the documentation instruction; **they do not grant a completeness waiver or automatically establish eligibility**. Source-specific batch measurements remain attached to their actual batch and context. Storage typing and missingness representation are addressed in the [harmonized schema proposal](BEEBOP_HARMONIZED_SCHEMA_PROPOSAL_2026-10-03.md), while this checklist checks that missingness is preserved and traceable.

For any proposed control, attach sequence, chemistry, assay and measured-outcome evidence. Unsourced, synthetic or proposed controls belong in a separate design register and cannot enter training rows. This proposal creates no controls and supplies no control inventory.

A proposed clean clinical negative requires the six source requirements in §E: exact sequence, human exposure, adequate dose and duration, explicit monitoring, explicit outcome and traceable denominator. Each must have its own evidence reference. Missing adverse-event text, a reporting threshold or a no-event mention does not establish a negative. Intended pharmacology and therapeutic correction must remain distinguishable from adverse toxicity; scientific assignment remains German's.

## 5. Proposed operating sequence and ratification request

1. Pin the rules, schema and source versions. Confirm a verified local structured source and recorded checksum before row transfer under §A.
2. Link a candidate observation to its exact construct, primary source and source location. Preserve the two-table grain and all required schema fields.
3. Assemble gates 1–9 evidence, structural findings and exceptions. Submit unresolved scientific questions without filling the gaps or assigning labels.
4. Link the candidate's intended use to gates 10–12. If a split, authorized evaluation or claim review does not yet exist, retain `NOT_ASSESSED`; do not claim that all twelve gates have been met.
5. Submit the exact versioned package to German. Record his decision verbatim by reference and implement only its permitted scope. Any changed construct, observation, grouping, analysis or claim requires review of affected evidence and decisions.

**Requested ratification:** confirm this cross-endpoint interpretation, the scope separation without waiver of gates 10–12, the proposed review fields/states, and endpoint applicability treatment—especially assay context and response-state terminology. Confirm how documented characterization gaps affect each permitted use. A separate, explicit model-eligibility or release decision remains necessary wherever German's governance requires it.

Until ratified, this is a complete proposal ready for review. It asserts no newly qualified records, training permission, scientific sign-off or public freeze. Items 3–12 of the delegated package remain outside this working pass.
