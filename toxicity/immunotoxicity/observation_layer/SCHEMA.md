# Immunotoxicity condition-level observation layer — empty skeleton

Date: 2026-10-03. Status: **empty structure, conformed to Beebop's harmonized schema. Not
populated, not ratified, not migrated.** Built per Crank's instruction ("the condition-level
observation layer is still missing — build that first") and `SCIENTIFIC_RULES.md` §K, which permits
deriving a proposal from the rules for German's ratification without stalling for finality.

## Why this exists

The bottleneck, unchanged: of 141 canonical oligo identifiers, **1** directly matches an observation
identifier, and the 33 `Evidence_Observations` are paper-level narrative, not condition grain. The
condition-level observation table did not exist. This builds its **structure** so that, once German
ratifies Beebop's schema and authorizes population, the target is ready and nobody forks field
names. It holds **zero rows by design**.

## Conformance — no forked field definitions

Both tables are the two-table design in
[`BEEBOP_HARMONIZED_SCHEMA_PROPOSAL_2026-10-03.md`](../../../BEEBOP_HARMONIZED_SCHEMA_PROPOSAL_2026-10-03.md),
itself derived from `SCIENTIFIC_RULES.md` §B–D at pinned commit `e9d4f6d`. Every column is one of
Beebop's placements — the 35 §C fields in their assigned table, plus Beebop's named engineering
support groups (record identity, material scope, source lineage, reported context, evidence lane,
evidence state, interpretation lineage, controls/thresholds, grouping support, missingness/conflicts,
raw chemistry evidence). **No field name was invented here.** If Beebop's proposal changes under
German's ratification, these headers change to match; they do not lead.

| File | Rows | Columns | Grain |
|---|---:|---:|---|
| `canonical_oligo.csv` | 0 | 20 | one construct record (identity + position chemistry); key `construct_record_id`, an opaque record key, **not** an equivalence claim |
| `experimental_observation.csv` | 0 | 68 | one measurement at **oligo × chemistry × strand × dose × time × donor/system × delivery × endpoint**; key `observation_id`, FK `construct_record_id` |

## Derivability of the existing 33 observations — `derivability_map.csv`

Every current `Evidence_Observation` classified by what blocks its decomposition into condition
rows. This is **description, not decomposition**: no row was created, nothing re-grained.

| Blocker class | Count | What would unblock (all gated) |
|---|---:|---|
| `GROUP_COMPARISON` | 31 | split into per-construct conditions, each needing its own sourced measurement |
| `AGGREGATE_NARRATIVE` | 1 | figure digitization or a source-defined per-construct qualitative result (OBS-029, Sioud 32-siRNA panel) |
| `SINGLE_NO_NUMERIC` | 1 | a sourced numeric value or an explicit qualitative endpoint |

**Condition-grain rows derivable now: 0.** Not because the structure is missing — it now exists —
but because populating is gated (German, scientific) and every current observation is an aggregate
or group summary, not a condition-grain measurement. The acquired supplements change this prospect:
Yoshida S1 (~39 numeric outcomes, mean/SD/n=3) and Valentin S2 (80 ASOs, per-position chemistry,
four receptor readouts) are the first sources that could yield real condition rows **when
population is authorized** — but that authorization is German's, and the grain is his to ratify.

## Gates — explicit

- **Not populated.** Zero rows. Populating is ingestion → gated on German.
- **Nothing re-grained.** The existing one-row-per-oligo catalog is untouched (§B: flag, do not
  re-grain). This adds an empty parallel structure; it does not convert the old one.
- **Not ratified.** Beebop's schema is a proposal awaiting German; these headers inherit that status.
- **No identity merges.** `construct_record_id` is opaque; `sequence_family_group` is candidate and
  unadjudicated (§G) — in particular the ODN2006 cluster stays unmerged pending German.
