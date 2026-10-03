# Item 1 — Harmonized schema proposal

**Status: PROPOSAL FOR GERMAN'S RATIFICATION. Not an approved schema or a migration instruction.**  
Prepared by Beebop • 2026-10-03 • Package checkpoint: 2026-10-10  
Scientific ratification: German García-Fresco. Engineering review: Oscar Penny.

## Basis and requested decision

This proposal generalizes the canonical-oligo-to-observation model already specified in
[SCIENTIFIC_RULES.md, pinned source](https://github.com/naviero1/Oligos/blob/e9d4f6da4f455f0c39f2405f31a18779f34a5a2d/SCIENTIFIC_RULES.md).
Source commit: `e9d4f6da4f455f0c39f2405f31a18779f34a5a2d`; source blob:
`b85d50d49ecd2ca9da841f2f0af2973626517a5c`.

Sections B–D supply the architecture, named fields and evidence lanes. Sections A and E–J
constrain transfer, missingness, interpretation and release. Section K permits a proposal based
on this derived reference. German's underlying primary governance documents were not re-read
for this proposal; no final scientific authority is claimed.

**Decision requested:** ratify the two-table logical design and the field placements below,
with amendments where needed. Oscar can then review the physical implementation. Ratification
of this design does not ratify any existing record, establish a canonical neurotoxicity lineage,
or authorize migration, scientific admission, model training or release.

**Nonblocking source discrepancy:** the delegation describes 38 fields, but the pinned section C
enumerates **35 required field names**: 8 identity/chemistry + 3 characterization + 12
exposure/system + 10 outcome/adjudication + 2 grouping. All 35 are preserved below.
`is_LNA` (is locked nucleic acid) is an example of a secondary flag, not a 36th required field.
The three additional names implied by “38” are not supplied. Confirm the count or supply those
names during ratification; this proposal does not invent replacements. Engineering additions
below are explicitly separate from that count.

## 1. Architecture and record grain

Two core scientific tables remain the center of the design:

| Core table | One row represents | Proposed key and relationship |
|---|---|---|
| `canonical_oligo` | One construct record preserving exact sequence, strand identity and position-specific chemistry. Before identity adjudication, separate source construct records remain separate provisional entries. | `construct_record_id`, a stable opaque record key, not proof of equivalence. |
| `experimental_observation` | One observed measurement at the grain **oligo × chemistry × strand state × dose × time × donor / cell system × delivery condition × endpoint**, with source row, replicate or reported aggregate retained. | `observation_id` plus a reference to `construct_record_id`. Many observations may reference one construct record. |

An oligo-level summary is a downstream view, not the primary evidence record (§B).
Different measured endpoints, doses, times, delivery conditions, donors and replicates stay
distinguishable. A source-reported aggregate remains an aggregate: no individual donors,
measurements or replicate rows are manufactured. Repeated reports of the same experiment are
flagged for review, not automatically counted as independent evidence.

No existing endpoint is re-grained by this proposal. An endpoint requiring a change of biological
grain must record that exception for German. The foreign key links a measurement to a construct
record; it does not equate a reference substance with the material administered in a particular
experiment.

**Construct boundaries (§G):** shared base sequence does not justify merging records that differ
by sugar/base/linkage position, strand, conjugate, stereochemistry or formulation. Formulation
remains explicit on observations; grouping records never erases that distinction. A
`sequence_family_group` is for leakage control, not construct equivalence. Candidate family
relations remain unadjudicated until approved.

Supporting provenance, characterization and review records may be linked or nested in a physical
implementation. They preserve the lineage of the two core tables; they do not replace the model
with a new scientific architecture.

## 2. Field dictionary — all 35 section C fields

“Construct” means `canonical_oligo`; “Observation” means
`experimental_observation`. Types and placements are **engineering proposals**, subject to
ratification. Every listed field must exist in the proposed interface even when its reported
value is missing. Missing is not zero, false, a negative label, or permission to infer a value.

| # | Exact field | Placement | Proposed representation and constraint |
|---|---|---|---|
| 1 | `sequence_5to3` | Construct | Source-preserved sequence text with orientation-verification evidence. Preserve case and annotations where meaningful; no destructive normalization. |
| 2 | `strand_role` | Construct | Source-described role. Ambiguous strand identity remains unresolved. |
| 3 | `duplex_partner_id` | Construct | Reference to a separate partner construct record where applicable; unresolved or unreported partners stay explicit. |
| 4 | `backbone_by_linkage` | Construct | Source-backed linkage-position representation, retaining strand and positional convention. No substitution of a molecule-level flag. |
| 5 | `sugar_mod_by_position` | Construct | Source-backed residue-position representation, preserving partial coverage and unknown positions. |
| 6 | `base_mod_by_position` | Construct | Source-backed residue-position representation, preserving partial coverage and unknown positions. |
| 7 | `terminal_modifications` | Construct | Source-described end, chemical identity and attachment where reported. Unspecified terminals are not assumed unmodified. |
| 8 | `gap_length_nt` | Construct | Reported gap length in nucleotides with its source. No inference from letter case or a broad chemistry class without an approved derivation. |
| 9 | `purity_pct` | Observation / linked tested-material characterization | Reported number or source expression with percent unit, batch/material scope and source; otherwise `NOT_REPORTED`. No construct-wide default. |
| 10 | `identity_method` | Observation / linked tested-material characterization | Reported identity method and material scope; otherwise `NOT_REPORTED`. A method description is not proof of complete identity confirmation. |
| 11 | `endotoxin_level` | Observation / linked tested-material characterization | Reported value/expression and unit, method and material scope where supplied; no assumed zero. |
| 12 | `formulation` | Observation | Reported formulation, preserving distinctions between administered materials. |
| 13 | `delivery_agent` | Observation | Reported delivery agent and context. Absence of a statement is not “none.” |
| 14 | `anticoagulant` | Observation | Reported anticoagulant; missing or contextual nonapplicability kept explicit, not guessed. |
| 15 | `dose_value` | Observation | Reported number or expression, including bounds; paired with `dose_unit` and dose basis. |
| 16 | `dose_unit` | Observation | Source unit, including per-body-mass or concentration basis. No undocumented conversions. |
| 17 | `exposure_time_h` | Observation | Hours only when supplied or converted under a separately approved, documented rule. Original time value/unit retained; no conversion executed here. |
| 18 | `cell_system` | Observation | Source-described system. Clinical population details live in accompanying condition metadata; a clinical row does not invent a cell assay. |
| 19 | `cell_subset` | Observation | Source-described subset where reported; not inferred from a generic cell-system name. |
| 20 | `species` | Observation | Source-reported species. Mixed systems retain their composition and require lane review. |
| 21 | `donor_id` | Observation | Source-provided donor token, scoped to the source; pooled or unreported donors do not receive invented individual identities. |
| 22 | `donor_class` | Observation | Source-described donor/population class. |
| 23 | `sample_state` | Observation | Reported sample state, including source-specific processing conditions. |
| 24 | `endpoint_name` | Observation | Specific measured endpoint, retaining source wording. Distinct outcomes remain separate. |
| 25 | `raw_value` | Observation | Exact reported continuous value, count, range, bound or expression; retain aggregation and denominator context. |
| 26 | `raw_unit` | Observation | Reported unit or scale; no conversion of fold change into clinical severity. |
| 27 | `author_interpretation` | Observation | Source-attributed author interpretation, distinct from project adjudication; exact location retained. |
| 28 | `curator_label` | Observation | Existing scientist-approved label or unresolved state, with origin and derivation metadata. Agents assign no new toxicity labels. |
| 29 | `immunomodulatory_direction` | Observation | Preserve reported/scientist-approved agonist, antagonist, potentiator, inert-low-response, mixed or unknown distinctions where applicable. No invented cross-endpoint equivalents. |
| 30 | `receptor_pathway` | Observation | Source-supported pathway and evidence context; absence of measurement is not absence of pathway activity. |
| 31 | `mechanism_evidence_type` | Observation | Reported evidence basis, separately attributed from a curator's interpretation. |
| 32 | `clinical_anchor` | Observation | Source-linked clinical observation or reference where present; not automatic validation of a laboratory result. |
| 33 | `evidence_confidence` | Observation | Preserve reported/existing adjudicated value and its author or rubric; new assignments require German. No implicit model-eligibility score. |
| 34 | `sequence_family_group` | Construct, exposed on observation views | Candidate or adjudicated grouping with decision provenance. No silent construct merge. |
| 35 | `paper_group` | Observation | Primary-paper grouping reference; linked secondary reports stay traceable and do not create independent experiments. |

For characterization, a separate linked material record is preferred when several observations
used the **same source-confirmed batch**. The three characterization fields remain exposed in
the observation interface. An unlinked substance or batch claim stays in supporting evidence
with linkage unresolved; it must not be broadcast across observations. Conflicting batches
remain separate records.

## 3. Proposed engineering support — not additional scientific findings

These additions make the required lineage auditable. They are proposed field groups, not a
delivered crosswalk, control inventory, endpoint scorecard or source inventory.

| Field group | Proposed contents | Derivation / purpose |
|---|---|---|
| Record identity | `construct_record_id`, `observation_id`, original endpoint record key, original row/arm/replicate or aggregate key | §B: distinguish a source record from an adjudicated construct and preserve measurement grain. |
| Material scope | `material_record_id`, batch/lot as reported, material-to-observation linkage evidence | §§F–G: avoid transferring analytical characterization between unverified batches. |
| Source lineage | Primary-source identifier, citation, source web address, local-file checksum, file version/commit, sheet/table/figure/page and exact row/cell location | §§A/B, gates 1 and 9: trace each transferred value to the verified source artifact. Multiple field-level sources are allowed. |
| Reported context | Original dose/time text and units, route, population/eligibility, exposure schedule, arm, numerator/denominator, replicate/aggregation description where supplied | §B and gate 4: retain reported clinical and laboratory context without manufacturing finer-grained observations. |
| Evidence lane | `evidence_lane`: proposed human-clinical, human-laboratory/ex-vivo, animal, unresolved; retain system details separately | §D and gate 7: separate evidence populations. Mixed or ambiguous systems remain unresolved pending review. |
| Evidence state | `evidence_state`: held, staged, admitted; decision reference for any admission | Existing project distinction; an artifact's availability is separate from scientific acceptance. |
| Interpretation lineage | Interpretation record, author-versus-curator origin, derivation reference, scientific decision reference, model-eligibility decision reference | §B and gate 5: preserve the chain from observation through interpretation to any eventual model row. |
| Controls and thresholds | Source control identifiers, source-defined threshold, reported control role, scientist disposition reference | §E: represent control evidence without assigning control status or constructing an inventory in this pass. |
| Grouping support | Laboratory, experimental series, matched pair and counterpart/strand relationships, with source and adjudication state | §G and gate 10: permit later leakage review beyond paper/family alone. |
| Missingness and conflicts | Field name, reported-value status, gap-register reference, conflict reference, applicability decision reference | §§E–F: distinguish unreported, unresolved and explicitly adjudicated nonapplicable cases. |
| Raw chemistry evidence | Exact source representation, source positional convention, raw stereochemistry payload and source reference | §§C/G: preserve information while chemistry interpretation and stereochemistry rulings remain pending. |

**Position handling:** the proposed normalized interface would use one-based residue positions
and directed linkages from residue i to i+1, always qualified by strand and the source convention.
That is a proposed encoding convention, not permission to transform data. Circular, branched,
partially specified or otherwise incompatible structures remain explicit exceptions.
Unreported positions remain unknown; no position map is completed by inference.

Data from GSRS (Global Substance Registration System) stays raw and unparsed pending German's
stereochemistry ruling, as directed by the existing
[decision record](https://github.com/naviero1/Oligos/blob/5db8dddb7eef893dff7da8fca1edabdf0f340ed6/CRANK_DECISIONS_2026-10-03.md).
No normalized stereochemistry mapping, stereoisomer pooling or ingestion is performed here.

## 4. Missingness, evidence lanes and qualification

The proposed interchange contract accepts a reported value **or an explicit status**, rather
than coercing missing numeric fields to zero. For absent analytical identity or purity,
`NOT_REPORTED` remains the field value under §F, accompanied by a Characterization Gap Register
entry stating what is missing, why, what was attempted, and what would close the gap.
A future numeric storage implementation must preserve that exact status in a companion field
and round-trip it without loss; its choice is for Oscar after ratification.

Nonapplicability requires an attributed rationale and scientist-approved disposition; it is not
an agent shortcut for empty required fields. Contradictory source values are retained with an
exception reference. No “typical,” molecule-level or other-batch characterization fills a gap.

Human clinical, human laboratory/ex-vivo and animal observations are kept separate. Animal
laboratory and animal living-system evidence remain distinguishable in the system context;
neither is reported as human evidence. Completeness/directness tiers are separate from toxicity,
safety, qualification and model eligibility (§D).

The companion [MQR (Minimum Qualified Record) proposal](BEEBOP_MQR_PROPOSAL_2026-10-03.md)
maps all twelve sign-off gates. Structural validation cannot turn a row into scientifically
admitted data. A complete row does not bypass split, performance, claim or release review.

## 5. Proposed checks and implementation boundary

After ratification, mechanical validation should check:

1. Both core tables and all 35 named section C fields are represented; no field is dropped by an endpoint adapter.
2. Record references resolve, or an unresolved exception is retained. Matching sequence text alone never collapses construct records.
3. Every transferred field can resolve to a source location and verified file identity; conflicting or absent evidence is explicit.
4. Reported dose/time units, strand, position conventions, donor/aggregate scope and distinct endpoints survive transfer.
5. Missing analytical characterization round-trips as `NOT_REPORTED` with its gap entry; no zero substitution or propagation across batches occurs.
6. Author interpretations, derived labels, evidence lanes and scientific/model-eligibility decisions remain distinguishable.
7. Candidate grouping and raw stereochemistry remain unchanged pending scientific decisions.

These are proposed checks, not a statement that any endpoint currently passes them.
The activation rule in §A still applies: a verified local structured source with recorded
checksum must exist before agent row transfer into a locked staging schema.

**Ratification choices within item 1:** confirm/amend table grain and field placement; resolve the
35-versus-38 naming discrepancy; confirm batch-scoped characterization and missingness encoding;
confirm the proposed support metadata and position convention. Existing scientific rulings,
including stereochemistry and authoritative neurotoxicity lineage, remain separate dependencies.

This pass produces this proposal and item 2 only. No dataset, label, source acquisition,
crosswalk, release, or work item 3–12 is executed. The October 10 checkpoint is unchanged.

