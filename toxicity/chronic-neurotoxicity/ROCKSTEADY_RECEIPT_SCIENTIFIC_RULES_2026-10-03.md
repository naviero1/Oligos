# Rocksteady (CNS) → Beebop: receipt for `SCIENTIFIC_RULES.md`

**Date:** 2026-10-03 · **Branch:** `claude/oligo-toxicity-dataset-k394sz` · **Endpoints:** CNS —
acute-neurotoxicity, chronic-neurotoxicity, hydrocephalus (original lineage)

**Confirmed: `SCIENTIFIC_RULES.md` read in full, and `CRANK_DELEGATION_2026-10-03.md` row
"CNS — both lineages" worked.** Both were read at `claude/amazing-galileo-rwiv95`.

**Correction to the dispatch:** neither file is on this branch. The instruction said "at the
repository root on your current branch"; this branch's root holds only `README.md`. I read them on
the default branch. If sessions are expected to find them locally, they need to be merged down —
publishing a file does not put it on nine branches.

---

## Rules that change this endpoint's work

### §B — unit of observation. **This endpoint is partly one-row-per-oligo. Flagged, not re-grained.**

Measured, rows per distinct (oligo, readout) key:

| source | keys | max rows/key | mean | grain |
|---|---:|---:|---:|---|
| **H1** (Hagedorn) | 2,006 | **1** | **1.00** | **one row per oligo per readout** |
| CT1 | 288 | 32 | 8.09 | observation |
| K1 | 7 | 28 | 5.86 | observation |
| HV3 | 9 | 5 | 1.89 | observation |
| HV1 | 6 | 4 | 1.50 | observation |
| HV2 / L1 / C1 | 8 / 6 / 12 | 1 | 1.00 | one row per oligo per readout |

**H1 is 1,825 of 1,879 compounds and 2,006 of 4,428 rows**, and it is strictly oligo-grained: one
calcium score and one tolerability score per compound, no dose, time or replicate dimension within
a readout. `dose_value` and `exposure_duration` are populated on all 2,006 rows, but they are
constant per readout — a single condition, not a condition axis.

The schema is observation-grained and three sources use it as such. **The limitation is the
source's grain, not the schema's.** Hagedorn publishes one summary score per compound; recovering
condition-level rows would mean re-extracting from data the paper does not print.

**Nothing re-grained.** Per §B that is German's call.

### §G — leakage. **The 0.929 AUC cannot satisfy the grouped-split requirement, and I am relabelling it.**

The baseline model does **not** use a random split — it uses the authors' own published
train/test/validate assignment, which was already a generalisation test rather than a random one.
So the §G prohibition is not violated.

But §G's positive requirement cannot be met here at all:

- **Every one of the 181 compounds comes from one source, one paper, one laboratory** (H1,
  `source_ref` distinct count = 1). **Leave-one-paper-out is not computable**: n_papers = 1.
- `sequence_family_group` and `paper_group` — which §C says must exist from the start — **do not
  exist in this schema**.
- German's stated symptom is ~0.94 on random/held-out against ~0.65 LOPO. **0.929 on a
  within-paper held-out set is exactly that shape**, and this module has no way to produce the
  second number.

**Change:** the AUC must be labelled a within-source, within-laboratory number with LOPO stated as
not computable, wherever it appears. It is currently reported as a held-out AUC without that
qualifier. This is a wording and framing change, not a re-analysis, and I have not retrained or
re-run anything.

### §C — missing schema fields

Absent from this endpoint, verified by column check: `sequence_family_group`, `paper_group`,
`strand_role`, `duplex_partner_id`, `donor_id`, `endotoxin_level`. Also absent as named fields:
`curator_label`, `author_interpretation`, `evidence_confidence`, `donor_class`, `sample_state`,
`delivery_agent`, `anticoagulant`.

Several exist under other names — `cns_tox_grade` is a curator label, `effect_vs_control` carries
author interpretation, `system_model` carries cell system. **§C says adding is fine and dropping is
German's question; it does not say renaming is free.** I am not renaming anything ahead of the
Tier 0 crosswalk, which is where field identity gets settled.

### §E — the grade is a curator label, and 1,539 rows are a manufactured-negative risk

`cns_tox_grade` is assigned by this pipeline, not by the sources. It carries `grade_status =
provisional` and a `grade_basis` string recording the rule — but it is **not named as a curator
label**, and the author's own statement is not stored in a separate `author_interpretation` field.
Per §E ("keep author result and curator label separate") that separation needs to be explicit.

**1,539 of the 2,341 human clinical rows record `numAffected = 0`** and carry curator grade 0.
These are *not* the §E trap of absence-from-table — each has an explicit denominator and explicit
monitoring within a stated collection window, which is stronger. **But they are still a curator
grade on a non-event, and they are 95 % of this module's grade-0 rows.** §E's "do not manufacture a
balanced class" applies directly. They are already flagged by an `incidence_is_zero` column; whether
they may serve as a negative class is German's.

### §F — missingness. **Already compliant, and the calibration matches.**

`purity_pct` is `NOT_REPORTED` for **all 1,879** compounds and `identity_confirmation` for the
human subset — no inferred, typical or group-level value was substituted. German reports zero of 45
thrombo records with usable purity; this endpoint is **zero of 1,879**. `docs/CHARACTERIZATION_COVERAGE.md`
functions as the Characterization Gap Register, with per-field denominators and named recovery
leads, reported separately for human and animal subsets and never pooled.

### §D — tiers. One field needs checking, not changing

The source registry carries `evidence_tier` with values like `primary_supplementary_data`. Those
describe directness of provenance, not quality or eligibility, which is consistent with §D — but
the name invites the §D misreading and should be reviewed at Tier 0.

### §A, §H, §I — no change

- **§A:** nothing here infers or imputes a missing value, manufactures a negative beyond the
  flagged zero-incidence rows, or resolves a scientific conflict. The one unresolved conflict in
  this module (K1 vs O1 on divalent-cation rescue) is documented as unresolved and left so.
- **§H:** this module claims no freeze and no clinical classifier. No sequence-only clinical
  classifier exists here.
- **§I:** none of this endpoint's nine sources is `Peacock_2009`, the misattributed "Hornung 2005",
  Riera-Tur, Fucini or Lenert. The corrections do not touch it.

---

## Crank's figures for my row — verified, two corrections

**1. README 181 overclaim — CONFIRMED, now fixed.** `_shared/cns/README.md:37` read *"which is
exactly the in-vitro-to-in-vivo extrapolation the challenge asks for"*. All 181 are rat in vitro
plus mouse in vivo, zero human rows — Crank is right. **My earlier round fixed a different passage
in the same file and missed this one**, which is the second time that failure mode has caught me
here. Corrected, and the retired figures are now in a QC blocklist that fails the build if they
return.

**2. Grade distribution — Crank's "reads 56/87/40/57" is right; the correction figure needs care.**

| population | measured |
|---|---|
| README's claim | 56/87/40/57 — **matches nothing** |
| Crank's stated correction | 74/81/39/51 |
| **acute folder, all graded** | **74 / 81 / 39 / 51** (n=245) ✓ matches Crank |
| acute folder, animal only | 55 / 81 / 35 / 51 (n=222) |
| module-wide, animal only | 56 / 81 / 37 / 54 (n=228) |
| **module-wide, all graded** | **1,614 / 673 / 130 / 175** (n=2,592) |

Crank's figure is correct **for the acute folder**. The README sentence is a module-level claim, so
substituting it would have replaced one wrong number with a different-population number. I wrote
the module-wide figure, broke out the animal panel, and stated that 1,539 of the grade-0 rows are
non-events — which is the fact the single ratio was hiding.

**3. Shared sequences — I measure 149, Crank states 144.** Method: strip all characters outside
`ACGTU`, upper-case, intersect as sets. 1,686 distinct here against 277 in the alternate,
intersection **149**. Probably a normalisation difference (U/T unification, or collapsing repeated
records). **I have adopted neither figure**; the method is stated so it can be reconciled.

**4. Cross-branch stale file — present on this branch, and it is not mine to fix.** The stale
111-row `measurements.csv` ships here at `toxicity/kidney/data/measurements.csv`, against the
246-row canonical file on `claude/amazing-galileo-rwiv95`. Flagged for the Kidney session and
Cross-branch owner. I have not touched another endpoint's folder.

---

## Done this round

- README claims 2–4 corrected from measurement; stale figures added to the QC freshness blocklist.
- **Lineage comparison prepared for German** — [`CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md`](./CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md).
  Measured, no merge, no recommendation of a winner, and it states that I built one of the two.
  Headline for the decision: **the alternate holds 238 non-human-primate rows and 116 human
  laboratory rows against this lineage's 0 and 34** — neither corpus is a superset of the other.
- 47/47 QC checks pass.

## Gated, not done

Ingestion, promotion, release, re-graining, field renaming, lineage merge or selection, and any
scientific adjudication. The AUC relabelling in §G is a wording change I will make on request; I
have flagged it rather than editing the narrative mid-round.

---

**RECEIPT CONFIRMED — RULES READ — FIVE RULES CHANGE THIS ENDPOINT'S WORK (§B, §C, §E, §G, and §D for review)**
