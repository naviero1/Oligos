# Complement activation — schema and data dictionary

**Status: SCHEMA ONLY. No data ingested under it.** Built 2026-10-03 to satisfy the first instruction of
the Complement row in `CRANK_DELEGATION_2026-10-03.md` ("build the schema before any further
acquisition"). Derived from `SCIENTIFIC_RULES.md` §§B, C, E, F, G and from German's decision queue items
2 and 5. The per-position pattern is copied from
`toxicity/immunotoxicity/research_staging/valentin2021_S1_S2_sequences.csv` as instructed.

**Gated:** ingestion, promotion and release wait on the Tier 0 crosswalk for schema and on German for
anything scientific. **No grade column is defined here**, because no rubric exists and the rubric is
German's.

Where this schema and German's documents differ, **German's documents win and this file is wrong.**

## Architecture — two tables, per §B

§B requires *"a canonical oligo table holding identity, sequence and chemistry, linked to an
experimental-observation table. Keep them separate."*

```
oligo_canonical.csv          construct_uid  (one row per administered construct)
        |
        | construct_uid
        v
observation.csv              observation_uid
                             oligo x chemistry x strand state x dose x time
                             x donor/cell system x delivery condition x endpoint
        |
        | source_id
        v
sources.csv                  source_id, licence_class, redistribution terms
```

**The observation grain is §B's, verbatim, and it is not one row per oligo.** An oligo-level summary is
derived afterwards and is never the curated record. For the one source staged so far, Sewing 2017, that
grain resolves to **analyte × condition × donor** — because its complement panel is single-concentration
(10 µM) and single-timepoint (45 min), so dose and time are constant within it rather than absent.

## Table 1 — `oligo_canonical.csv`

Implemented as `../research-staging/working/sewing2017_constructs_perposition.csv`, 12 constructs,
30 columns. **Chemistry is encoded by position. Molecule-level flags are prohibited as the primary
encoding** (§C).

| Column | Type | Notes |
|---|---|---|
| `construct_uid` | id | an **inventory record identifier**, not a claim of molecular distinctness |
| `construct_identity_state` | enum | `read_from_source_table` · `no_published_sequence_or_position_chemistry` · `UNRESOLVED`. Added 2026-10-03 |
| `canonical_join_status` | enum | `joinable` · `not_joinable_no_canonical_row_exists`. **An observation whose construct has no canonical record must say so, not point at a `construct_uid` that does not exist.** Added 2026-10-03 after a dangling key was found in the `NCT02363946` table |
| `name_as_printed` | text | verbatim from the source, including its own inconsistencies |
| `notation_verbatim` | text | **the source's own notation, preserved** — the valentin pattern's key property |
| `bases_5to3` | text | plain base sequence, asterisks stripped |
| `length_nt` | int | validated: must equal the base count |
| `strand_role` | enum | `single_strand` · `sense` · `antisense` · `NOT_REPORTED` |
| `duplex_partner_id` | id | `NOT_APPLICABLE` for single strands |
| `PS_linkage_after_positions` | int list | 1-based, `;`-delimited. `NONE_phosphodiester` where there are none |
| `n_PS_linkages`, `n_linkages_total` | int | validation pair: full PS ⇒ `n_PS = length − 1` |
| `sugar_mod_by_position` | position list | **`NOT_REPORTED` where the source does not print positions, even when prose implies them** |
| `sugar_mod_provenance` | enum | `read_from_source_table` · `orphaned_legend_in_source` · `derived_from_prose_rule` · `not_reported` |
| `stereochemistry_by_linkage` | position list | present **before** ingestion per German item 5, so a later GSRS pull cannot collapse into a plain `full_PS` |
| `stereochemistry_provenance` | enum | as above |
| `base_mod_by_position` | position list | e.g. 5-methyl-C positions |
| `terminal_modifications` | text | 5′/3′ caps, inverted-dT, conjugates |
| `gap_length_nt` | int | gapmer gap; `NOT_REPORTED` when wings are unreadable |
| `purity_pct` | numeric | `NOT_REPORTED` is **the correct value**, not a failure (§F) |
| `purity_gap_cause` | enum | **`not_reported_by_source` · `withheld_as_confidential` · `deferred_to_citation` · `unobtainable_paywalled`** — German item 2 |
| `identity_method`, `identity_gap_cause` | text / enum | same treatment |
| `endotoxin_level` | numeric | §C |
| `supplier` | text | |
| `sequence_family_group` | id | §G. Required **from the start** |
| `paper_group` | id | §G |
| `source_id`, `source_locus` | id / text | exact table or figure |
| `chemistry_encoding_level` | enum | `per_position` · `molecule_level` · `none`. Makes a §C violation visible rather than silent |
| `staging_state` | enum | `STAGED_NOT_INGESTED` · `INGESTED` · `QUARANTINED` |
| `model_eligibility` | enum | `NOT_ASSESSED_GERMAN` only, until German rules |

## Table 2 — `observation.csv` — defined, deliberately empty

**No row exists.** The 138 informative Sewing values are held pending the crosswalk.

### Endpoint fields — the four classes stay unpoolable

`complement_readout_class` is mandatory and non-null:

| Value | Analytes | Why separate |
|---|---|---|
| `activation_split_product` | Bb, Ba, C3a, C4a, C5a, iC3b, C3bBbP, sC5b-9, C3bc | |
| `component_abundance` | C3, C4, factor H, properdin | |
| `function` | CH50, AH50, total hemolytic complement | |
| `deposition` | platelet-bound C3d/C4d, glomerular C3c, IgM/properdin binding | |

Two independent sources show **split products rising while function falls in the same sample** —
REGULATE-PCI (CH50 ↓, C3a ↑, Bb ↑) and the Kyndrisa monkey data (*"complement split factors C3a and Bb"*
up with *"concomitantly decreased total complement activity"*). A scheme pooling these would score such
an event as partially cancelling. §E's "do not collapse distinct outcomes" applies directly.

`pathway_label_source` and `pathway_label_curator` are **separate columns**. Sources mislabel pathways:
Demirjian calls C3a/C4a/C5a *"classic complement pathway activation"* when C3a and C5a are
common-pathway products, and the ApTOLL 2024 paper calls C3 and C4 the *"terminal complement complex"*.
The curator column is **German's**, per §J.

### Value fields — §E's constraints are schema-level, not advisory

| Column | Notes |
|---|---|
| `raw_value`, `raw_unit` | the source's printed value and its literal unit string |
| `value_basis` | `absolute_concentration` · `stimulation_index` · **`percent_change`** · `fold_change` · `incidence_above_threshold` · `qualitative` |
| | **`percent_change` added 2026-10-03.** The dictionary predated it and `NCT02363946` used it before it was declared — recorded as a defect, not a silent patch. A percentage change from a stated baseline is **not** a fold change and must not be converted into one: `+309%` is a 4.09-fold value, and storing either number under the other's basis would misstate it. |
| `normalisation_denominator` | what a ratio is divided by — for Sewing, the same donor's PBS vehicle control |
| `severity_scale` | **`experimental_response_severity` only.** §E prohibits mapping in-vitro fold-change bins onto CTCAE or any clinical grade without clinical validation |
| `source_threshold`, `source_threshold_basis` | **per-source**, never a project constant. §E: no universal thresholds. 2× ULN and below-LLN live here, with their own provenance |
| `author_interpretation` | the source's own label, verbatim |
| `curator_label` | **German's**. Marked curator-derived unless the source explicitly defines it |

### Exposure and system fields

`formulation` and `delivery_agent` are mandatory, not metadata: ARC-520's masked polymeric amine
(NAG-MLP) and CALAA-01's cyclodextrin nanoparticle are candidate complement drivers independent of the
oligonucleotide. `route` and `infusion_duration_or_rate` are mandatory because the human positives
cluster on high-C<sub>max</sub> schedules, and MMB 2434 Ch.1 records that the effect *"could be mitigated
by subcutaneous administration or by slow intravenous infusion"*. ARC-520 reports **rate, not elapsed
time**, so the field must accept either and say which.

`matrix` is **per analyte, not per study** — ARC-520 used serum for CH50 and plasma for Bb in one
sentence. `anticoagulant`, `anticoagulant_concentration`, `surface_treatment`, `stop_reagent` and
`anticoagulant_provenance` follow the 2026-10-02 convention proposal; §C independently requires
`anticoagulant`, so only the provenance sub-field and the do-not-carry-across-assays rule are additional.

`donor_id` and `donor_class` are mandatory for human-laboratory rows because **pathway assignment is
donor-dependent**: Mangsbo's own Results heading reads *"phosphorothioate CpG utilizes either the
classical or alternative pathway depending on blood donor"*.

### Control fields — §E

`control_role` ∈ `positive_pathway_specific` · `positive_nonspecific` · `vehicle` · `inhibitor` ·
`matched_chemistry` · `sequence_control` · `none`, plus `control_sourced` as a boolean.

**§E: "Unsourced controls are not training rows."** For Sewing that quarantines a named block: the
`Inhib.` condition's reagent is never identified, so `control_sourced = FALSE` and its **10 values**
(5 donors × 2 analytes) cannot enter training. The two pathway controls are sourced — `Class. Path.` =
HAGG (heat-aggregated gamma globulin, TECOmedical), `Alt. Path.` = Zymosan (Sigma) — and are unaffected.

### Evidence lane — §D

`evidence_lane` ∈ `human_clinical` · `human_laboratory` · `animal` · `cell_free` · `unresolved`.
**Never pooled as interchangeable ground truth.** `measurement_intent` ∈ `toxicity` ·
`pharmacodynamic_efficacy` separates intended pharmacology from adverse toxicity — load-bearing here,
because one compound inside the GalNAc3 pooled dataset (ION 696844) **targets complement factor B**,
and Bb is factor B's activation fragment.

`identity_basis` ∈ `registry_number` · `sponsor_protocol_code` · `publication_identifier` ·
`pooled_or_unnamed_descriptor`. This exists because **none of the four EMA assessment reports contains a
single NCT number** — 11 regulatory studies are identified by sponsor protocol code alone.
`participant_pool_id` marks overlapping sponsor-database draws so that 750, 767 and 350 are visibly
non-additive.

## Lineage — §B, end to end

> model row → model-eligibility decision → scientific interpretation → observed measurement →
> experimental/clinical condition → biological system/population → exact oligo construct and position
> chemistry → exact source location and source URL

Every observation row must resolve this whole chain. For Sewing the chain is complete except that
`model_eligibility` is `NOT_ASSESSED_GERMAN` and, for three of twelve constructs, position chemistry
terminates at `NOT_REPORTED`.

## Validation rules enforced at build time

1. `length_nt` equals the `bases_5to3` count — **all 12 pass**.
2. Full-PS constructs satisfy `n_PS_linkages = length_nt − 1` — **11 of 12 pass; `ODN2395` has 0, correctly**.
3. Every position list is 1-based and within `[1, length_nt]`; linkage lists within `[1, length_nt − 1]`.
4. `NOT_REPORTED` may never be replaced by an inferred, typical or group-level value (§F).
5. No row carries a grade column. None is defined.
6. `sequence_family_group` and `paper_group` are non-null on every row (§G).
7. `chemistry_encoding_level` must read `per_position` for any row entering modelling.

## Known §G leakage structure in the staged source

Sewing's 12 constructs reduce to **2 sequence families** and contain **4 base-sequence-identical pairs**:
`ODN2395_Thio`/`ODN2395` (backbone differs) and `(AC)8`, `(AC)9`, `(AC)10` each paired with its LNA
variant (sugar differs, unreadably). Random splitting would place base-identical constructs on both
sides. **These share a leakage group and must remain distinct constructs** — §G's own case.

## What this schema does not settle

Endpoint definitions, the rubric, evidence tiers, model eligibility, the pathway curator column, and
whether `TMSR460` and `TMSR457` belong in the complement row set are **German's**. Schema implementation
and release mechanics are **Oscar's**. This file is a proposal awaiting the Tier 0 crosswalk.
