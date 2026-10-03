# Rocksteady: receipt re-confirmed against §K, and four dispositions

Addendum to [`ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`](./ROCKSTEADY_RULES_RECEIPT_2026-10-03.md).
Issued on Oscar's instruction to re-confirm against the revised `SCIENTIFIC_RULES.md`.

| | |
|---|---|
| **Version I originally received** | blob `bebe077b83`, 10,993 B — read from `origin/claude/crank-phase2-oversight`, which **still carries that older copy** |
| **Revised version** | blob `b85d50d49e`, 12,954 B, on `origin/claude/amazing-galileo-rwiv95` |
| **What changed** | **§K only.** I diffed the two files in full: the revision is 31 inserted lines, §K "German's scientist sign-off gates", placed between §I and §J. **No other section was altered by a single character.** So §§A–J as I answered them stand unamended, and my original receipt is not stale except as §K extends it. |
| **Branch / commit** | `claude/oligo-cns-toxicity-dataset-tijib6` @ `0ecce02`, clean tree |
| **Note for whoever maintains the rules file** | the crank oversight branch is one revision behind. A session reading the rules there, as I did on 2026-10-03, will not see §K. |

§K states that the **Minimum Qualified Record "is their cross-endpoint
generalization, and is derived from them rather than invented"**, which answers a
question I had put to Beebop about which field list is operative: the MQR's seven
fields descend from these twelve gates, so the twelve are the authority and the
seven are the restatement.

---

## 1. §K's twelve gates, audited against my corpus

Measured at `0ecce02` over 2,538 measurements and 592 oligo records.

| # | Gate | Verdict | Evidence |
|---|---|---|---|
| 1 | Traceable primary source and exact source location on every training row | **MET** | `source_id` + `source_ref` + `source_table` blank on **0 of 2,538**, QC-enforced; **1,734 distinct `source_table`** values, so locations are genuinely per-row, not per-document; 108 distinct `source_ref`, all resolvable |
| 2 | Sequence verified 5′→3′, **with strand identity and duplex partner** where applicable | **FAILS** on the second half | `sequence_5to3` present on 466/592. **No `strand_role`, no `duplex_partner_id`** — strand state is absent from both tables, so siRNA duplexes are unlinked |
| 3 | Every modification encoded **by position** | **FAILS as a column; 26.9% present as evidence** | No positional column exists. **159 of 592 records carry positional chemistry in `notes`** — 157 `linkage=` (PS/PO by position), 60 `chemistry_code=` (sugar by position), tofersen in full notation. A parse, not an acquisition |
| 4 | Assay context: cell system, **donor information**, delivery/**formulation**, dose, exposure time | **PARTIAL** | `system_model` ✓, `dose_or_conc_value`/`_unit` ✓, `exposure_duration` ✓ (free text, mixed units). **No donor field. No formulation field** — `delivery_method` is a route, not an agent or formulation |
| 5 | Raw/continuous outcomes retained; **curator-derived binary labels explicitly marked derived** | **FAILS** on the marking half | `readout_value`/`readout_unit` retained, but **203 of 2,538 (8.0%)** are `TBD` (figure-only sources). **No column marks `neurotox_grade` as curator-derived, though every one of the 2,538 is.** `k394sz` carries `grade_basis` + `grade_status`; I carry neither |
| 6 | Agonist / antagonist / potentiator / inert-low-response separated | **ABSENT** | No `immunomodulatory_direction` or equivalent. I am **not** declaring this inapplicable to CNS — §C says dropping a field because an endpoint finds it inconvenient "is a question for German", and §K says eleven of twelve gates "apply as written to every endpoint" |
| 7 | **Human and animal not pooled** as interchangeable ground truth | **MET** | Lanes separated by `study_type`, `species` and `evidence_class` (12 values) on every row; no pooled row exists; `cross_system_pairs_cns.py` reports pairs and never merges them |
| 8 | Endpoint-specific outcomes not collapsed into a composite; a composite is **a secondary derived field only** | **FAILS** | `endpoint_domain` (9), `readout_name` and `hydroceph_tier` (6) are all kept specific — but **`neurotox_grade` is a single 0–3 composite spanning all 9 domains and all 3 study strata, used as the primary label rather than a secondary derived field.** This is the same defect §E identifies, reached from a second direction |
| 9 | Citation metadata and **file identities** pass QC | **PARTIAL** | Citation metadata is QC-enforced (non-blank triple, enum-checked, 0 errors). **File identity is not QC-verified**: sha256 exists only in `sources/cns/_staging_2026-10-02/MANIFEST.csv` for 3 staged articles; `qc_cns.py` performs no checksum check over the archived corpus |
| 10 | Train/test splitting checked for exact-sequence, counterpart, strand, family, paper and series leakage | **NOT APPLICABLE — and that is the compliant state** | **My branch publishes no split.** No `split_group`, `cv_fold` or train/test column exists in either table, so there is no split to leak. Contrast: `k394sz`'s `acute-neurotoxicity/data/oligos.csv` ships a split in which 48 of 148 test oligos share an exact sequence with a training oligo |
| 11 | **LOPO and sequence-family grouped performance reported with uncertainty** | **NOT APPLICABLE — no performance is claimed** | No AUC, ROC, accuracy or any model-performance figure is published anywhere in my material. The only `AUC` string in my corpus is a **pharmacokinetic** AUC₀₋₂₄ quoted verbatim from FDA NDA 215887 for tofersen, flagged in its own note as carrying a units error in the source. See §2 for the disposition of the 181-compound claim |
| 12 | All major claims **no stronger than the evidence supports** | **MET as of today, after five retractions** | Two of my claims *were* stronger than the evidence: that per-position chemistry was absent (it is 26.9% present) and that the rival lineage grades no in-vitro rows (it grades 23 of 34 human ones). Both retracted in [`ROCKSTEADY_CORRECTIONS_2026-10-03.md`](./ROCKSTEADY_CORRECTIONS_2026-10-03.md) |

**Tally: 3 met, 2 partial, 4 failed, 2 not applicable, 1 absent-and-not-waived.**

Gates **2, 3, 5, 6 and 8** are the live failures. Every one of them is a schema
act to fix — a column that does not exist — and therefore Oscar's under §J, or
German's where it touches what a label *means*. I have added no column and
changed no label.

The two most consequential, because neither is a missing-data problem:

- **Gate 5 and gate 8 both indict `neurotox_grade` itself**, not its coverage.
  It is unmarked as curator-derived, and it is a composite used as a primary
  label. §E reaches the same column from the in-vitro side. Three independent
  rules now converge on one field.
- **Gate 3 is the cheapest to close and I had misreported it.** The positional
  data exists for 159 records in `notes`, sourced and cited; promoting it needs a
  parse of committed data, no acquisition and no network.

---

## 2. Disposition: the 181-compound AUC claim is retired, not rescued

Accepted and recorded. Verified arithmetically before accepting:

- The paired set is **exactly 181** oligos carrying both a rat primary-neuron
  calcium-oscillation score and a mouse in-vivo acute tolerability score.
- All **362** of its measurement rows carry `source_id = H1` and **one single
  `source_ref`: `Hagedorn2022_NAT_10.1089/nat.2021.0071`.**
- Therefore **n_papers = 1**. Leave-one-paper-out requires at least two paper
  folds to form a single held-out partition, so **LOPO is not computable on this
  set at all** — it is undefined, not merely weak.

This makes §K gate 11 unsatisfiable for that set by construction, and §G's
grouped-split requirement inapplicable rather than failed. **The claim is
retired.** I am not acquiring data to rescue the metric: the only data that would
create a second paper fold is further acute-axis material, and acute is the axis
the brief explicitly deprioritises and which P4 states "does not receive breadth
budget."

I note for the record that **no AUC claim was ever published on my branch** — the
figure lives in §G of the rules file as a corpus-wide observation and the paired
set lives on `k394sz`. My corpus-overview already carried the correct caveat on
its leakage groups: they exist "only to keep related molecules in one train/test
fold. It is **not** a claim that the grouped constructs are experimentally
interchangeable, and it must never be reported as an identity count." Nothing to
retract on my side; the retirement is recorded so it cannot be revived here.

---

## 3. Disposition: controls are a deliverable gap, reported as instructed

The narrative deliverable explicitly requires positive **and** negative controls.
Measured state of my branch:

| | |
|---|---|
| control-like records identifiable **by name or alias** | **25** (41 measurement rows) |
| of those, the named Hagedorn negative-control panel | **13** — `CNS309`–`CNS321`, "Hagedorn2022 LNA-ASO Control-001…013" |
| sequences present on those 13 | **13 of 13** |
| their grades | 13 rows at grade 0, 13 at grade 1 — benign-to-mild, consistent with negative controls |
| **positive controls, by design** | **0** |
| **`control_role` column** | **does not exist** |

So Oscar's figure is right: **13 negative, 0 positive.** Two things make it worse
than those numbers suggest, and I report them rather than round them off:

1. **None of it is machine-readable.** With no `control_role` column, the 25 are
   discoverable only by pattern-matching name strings — which is not a schema, it
   is a grep. A consumer cannot filter controls, and a reviewer cannot verify the
   count without repeating my regex.
2. **Three rows among the other 12 control-like records sit at grade 2**
   (`CMS1656`, `CMS2148`, `CMS2150` — a 2′-OMe gap variant, a "standard control
   oligomer" showing nuclear inclusions, an "H40" control). These are *not*
   positive controls: a positive control is high-grade **by design**, and these
   are incidental findings on reagents intended as inert. Calling any of them a
   positive control would be assigning a control role, which is a label and
   therefore German's. **I have not.**

**This is reported as a deliverable gap, not fixed.** Creating `control_role` is
Oscar's schema call; populating it is German's labelling call; and right now
neither half can move, which is why it is a gap rather than a task.

---

## 4. Disposition: net-new divergent work is frozen

Accepted. This resolves, in the literal direction, the question I had put to
Crank as the one that changed the most work. **Frozen as of `0ecce02`:**

- the 522-row chronic-eligibility queue (0 verdicts written, and none will be);
- the 19 + 7 pending-trial rows;
- the Characterization Gap Register **as a per-oligo table over my 592 records** —
  it is keyed on this lineage and discarded if German picks the other;
- the per-position parse of the 159 records, and any new column to hold it;
- the Tier 0 `endpoint_coverage.csv` rows and the MQR audit as deliverables;
- all remaining acquisition: PMDA, the three CC-BY `mmc1.pdf` supplements, the
  Hagedorn purification method, valeriasen conditions. No TGA attempt has ever
  been made or logged on this branch, so nothing is in flight there either.

**Continuing, as the two permitted classes:**

- **The comparison prepared for German** — [`CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md`](./CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md),
  including the §E dependency that takes my human-laboratory count from 13 to 0
  if those grades are withdrawn.
- **Fixes to already-published material** — this addendum; the five corrections;
  the per-regulator licence table and the 47-row proposed hold, which repair a
  defect already shipped in my own data dictionary (`sources.md:20` defines
  `public_domain` as covering "FDA **and EMA** documents"); and the removal notes
  for the deleted merged view.

I am treating the record-level crosswalk over the 150 shared sequences as
**frozen too**, since it is net-new. If it was meant to count as input to the
comparison rather than new work, say so and I will resume it — it is the one item
where I genuinely cannot tell which side of the line Oscar drew, and I would
rather be told than assume in the direction that lets me keep working.

**Acute neurotoxicity remains a supporting module.** Existing model claims and
splits await German's scoped disposition; I hold none of either on this branch,
so there is nothing here for that disposition to act on beyond the retirement in
§2.

---

## 5. One thing §K settles that I had escalated wrongly

I asked Oscar for German's two Drive source documents, giving as a live cost that
§E lists six elements of a clean clinical negative while three other documents
say seven. §K's closing paragraph answers it:

> **On producing work against this file.** A *proposal* may be derived from this
> file and submitted for German's ratification — that is what a proposal is. Only
> an *authority claim* requires his primary documents. Do not stall a proposal
> for want of a source you need only in order to assert finality.

So the ask was wrong in form. I do not need the originals to **propose** that the
seventh gate is "adequate dose" and "adequate duration" counted separately —
which yields exactly seven from §E's own six-item sentence — I need them only to
*declare* it settled, which is not mine to do anyway. **The proposal stands as a
proposal**, in [`ROCKSTEADY_REPLY_TO_CRANK_2026-10-03.md`](./ROCKSTEADY_REPLY_TO_CRANK_2026-10-03.md) §4 Q3,
and I withdraw the request to wait on it.

---

## 6. What this addendum changes

No data file touched: `cns_measurements.csv` 2,538 × 33 and `cns_oligos.csv`
592 × 21 are byte-identical, `qc_cns.py` 0 errors. No label assigned, changed or
withdrawn — the 297 in-vitro grades stay exactly as they are. No column added,
including the five that §K gates 2, 3, 5, 6 and 8 would need. No control role
assigned. No `redistribution` cell changed. Nothing merged, nothing re-grained,
no split created, no performance figure computed or published.

---
_Generated by [Claude Code](https://claude.ai/code)_
