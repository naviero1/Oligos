# Rocksteady → Beebop / Oscar: kidney response

**Release `kidney-5d82de234c71`** · endpoint: kidney / nephrotoxicity · branch
`claude/amazing-galileo-rwiv95`

Response to `toxicity/kidney/BEEBOP_SUGGESTIONS_2026-09-30.md`. Scope is kidney only; no
other endpoint's files were read or modified.

---

## 1. Baseline reviewed

| | |
|---|---|
| Branch | `claude/amazing-galileo-rwiv95` |
| Commit Beebop inspected | `8c7b9bf` |
| My HEAD at the time | `8c7b9bf` — **identical**, so no reconciliation of newer local work was needed |
| Fast-forwarded to | `9d01bfd` (the four suggestion files + index; no data files touched) |
| Release identifier | `kidney-5d82de234c71` (content-derived; see `RELEASE_MANIFEST.json`) |

**Beebop's baseline counts are accurate.** I verified each against the data rather than
accepting them: 65 oligos / 55 sequences, 42 clinical rows, 67 human-lab, 81 animal-lab,
56 animal-in-vivo, 15 bridge records, 29 of 42 clinical rows `measured_and_reported`, all
65 purity fields unreported. No discrepancy found.

One correction to the baseline framing: the dataset had already grown to **246
measurements** by `8c7b9bf` (not 165), and the bridge was already 15 rather than 9. Beebop's
table is right; some of my own older documents still carried stale figures, which is itself
one of the gaps raised, and is now fixed (§3).

---

## 2. Proposal dispositions

### Priority 1 — human-trial coverage and clean presentation → **ACCEPTED, implemented**

This was the most valuable item and it was correct. The dataset counts **measurement rows**,
so "42 human clinical" has been true as written and misleading as read. Resolving each
clinical row to its underlying study changes the picture substantially:

- `MSR009` and `MSR010` are both **ENVISION** (baseline and 24-month follow-up) → one trial
- `MSR005`–`MSR007` are one phase-1 study; `MSR017`–`MSR019` are one study (DMD114673)
- 13 rows are **label-derived**, where the label summarises studies without identifying them
- 1 case report, 2 reviews, 1 pooled cross-trial analysis, 1 unresolvable citation

Implemented as `scripts/build_study_register.py` → `data/clinical_study_register.csv`, with
seven counting rules stated in the script so disagreement lands on the rule rather than the
arithmetic. See §4 for the resulting counts.

**One place I went further than proposed.** Beebop asked for "verified, deduplicated"
trials. Deduplication is mechanical; *verification* needed a definition, so I split it into
two tiers: `trial_identified` (resolves to a distinguishable study) and
`primary_source_read` (the trial document was actually opened in this project). The headline
count requires both. That is why the verified count is **3**, not 17 — and I judged the
smaller honest number better than the larger defensible-sounding one.

### Priority 2 — negative-label eligibility → **ACCEPTED and EXTENDED**

Beebop identified a hole I had left: I added `renal_endpoints_measured` to flag unsupported
negatives, but **the numeric `nephrotox_grade` stayed 0 on those rows**, so a model reading
the grade column picks them up as negatives regardless of the flag. A warning column gates
nothing. That criticism is correct.

Beebop also challenged my 29 `measured_and_reported` rows. Auditing them **narrows the
issue usefully**: 21 of the 29 are *positive* findings (grade ≥ 1) where "measured" is
trivially true. Only **8 assert a negative**, and that is where scrutiny belongs — a
sharper target than "recheck 29".

Two of my own classifications did not survive that scrutiny:

- **`MSR045` lumasiran** — I had recorded in `CLINICAL_VALIDATION.md` that eGFR appears as
  efficacy/eligibility stratification rather than a safety assessment, and then classified
  the row `measured_and_reported` anyway. Internally inconsistent. Now
  `efficacy_derived_negative`.
- **`MSR160`/`162`/`164` (DMD PMO labels)** — I reasoned that mandated monitoring implies
  the endpoint was measured. It does not: monitoring guidance is forward-looking advice to
  prescribers, not evidence of assessment. The labels do assert "kidney toxicity was not
  observed in the clinical studies", which is a statement about findings, but no endpoint
  table stands behind it. Now `asserted_negative_regulatory` — stronger than silence,
  weaker than a measured result. `MSR016` (inclisiran) reclassified on the same basis.

Implemented as `scripts/add_negative_eligibility.py`, adding two derived columns and
touching no source assertion:

- `negative_eligibility` — `positive_finding` | `confirmed_negative` |
  `asserted_negative_regulatory` | `efficacy_derived_negative` | `not_eligible_negative`
- `nephrotox_grade_modeling` — equals `nephrotox_grade` **except blank** where the negative
  is not confirmed. Missing, not zero. **This is the column to train on.**

`nephrotox_grade` is preserved unchanged on all 246 rows, verified by the release gate.

**Result: of 21 clinical grade-0 rows, exactly one is a confirmed negative** — `MSR066`
(cemdisiran, quantitative eGFR −2.9 vs placebo −6.3 mL/min/1.73 m², primary source read).
20 rows are gated out of negative training.

### Priority 3 — comparability and the bridge → **ACCEPTED; found a real bug**

*Normalisation.* Already implemented before this review: `readout_unit` distinguishes
`pct_saline_control` from `pct_compound_1-1_reference`, and both extractors write a
do-not-pool note per row. I consider this closed and did not change it.

*Bridge confounding.* Beebop is right that a max-grade comparison across different studies
confounds species with dose, assay, follow-up and ascertainment. Added `comparison_type`:
**10 of 15 comparisons are `paired_same_source`** (human and animal evidence from the same
document); 5 are `cross_study_overlap` and are hypothesis-generating at best.

*Unsupported over-prediction claims.* Beebop's closure check — "unsupported human negatives
cannot produce claims that animals overpredict toxicity" — had real teeth. **Five of my six
`animal_over_predicts` verdicts rested on human negatives that fail eligibility.** Those are
now `indeterminate_human_negative_unsupported`; the verdict is suppressed rather than
published. One over-prediction verdict remains. The two *under*-predictions (inotersen,
givosiran) are unaffected because they rest on positive human findings, not negatives.

**Bug found while implementing this.** My "same source" test initially failed on the N3
patent because the data cited it two ways — `US11105794` for Table 2 and `US11105794B2` for
Table 1 — so the patent did not match itself and its three compounds were wrongly classed
cross-study. Normalised 21 rows to one spelling (`source_table` still distinguishes the
tables), which moved paired comparisons from 7 to 10.

*Statistics.* **Beebop is right and I was wrong.** I had claimed the provenance/outcome
confound "weakened 3.7×", which is a **p-value ratio** — not an effect size, and it moved
largely because I had added three rows to the anchored arm's denominator. Recomputed on the
honest measure, the risk difference moved **57.9 → 50.0 percentage points**: a real but
modest 7.9-point reduction, not a 3.7-fold one. Corrected in all five documents that
carried the claim (`NARRATIVE`, `METHODOLOGY_PHASE2`, `STATUS`, `schema`,
`CLINICAL_VALIDATION`).

### Priority 4 — characterization and release documents → **ACCEPTED**

*Purity wording.* Accepted. Replaced "cannot be curated" / "cannot be closed by further
curation" with the narrower supported statement: not reported in the sources reviewed, with
the search that was actually run named (both patents searched for purity / HPLC / UPLC /
LC-MS / mass-spec; labels and trial papers do not publish per-batch purity), and an explicit
note that targeted supplements and manufacturer batch records **remain unexamined**. I have
*not* contacted any author or manufacturer; that is listed in §6 for Oscar's decision.

*Document reconciliation.* Done — stale merged-view dimensions, bridge figures and sequence
counts corrected; new fields and the register documented in `schema.md`.

*Release identifier.* Accepted from "Common gaps". Added
`scripts/make_release_manifest.py` → `RELEASE_MANIFEST.json`, binding the canonical tables,
derived files and documents to **`kidney-5d82de234c71`** with SHA-256 per file. The id is
content-derived, so identical data always yields the same id and any table change changes
it — a reviewer holding an older Drive export can tell immediately.

*Workbook order.* Implemented Beebop's suggested order, with the animal evidence moved to a
genuinely separate appendix rather than merely labelled:

`Summary` → `1 Human trials (verified)` → `2 Human trial measurements` →
`3 Human lab evidence` → `4 German's analysis` → `5 Oligos and characterization` →
`6 Data dictionary` → `A1 APPENDIX animal evidence` → `A2 APPENDIX all measurements` →
`A3 APPENDIX human vs animal`

The release gate now asserts that every human/design tab precedes every appendix tab.

### Nothing rejected

I rejected none of the four priorities. The one I pushed back on in part is Priority 2's
framing: "recheck the remaining 29" is better scoped as "recheck the 8 that assert a
negative", since 21 of the 29 are positive findings where the ascertainment question does
not arise.

---

## 3. Implemented changes

| File | Status | Effect |
|---|---|---|
| `scripts/build_study_register.py` | new | Per-row study attribution + 7 counting rules → trial counts |
| `data/clinical_study_register.csv` | new | 42 clinical rows resolved to 35 distinct studies |
| `scripts/add_negative_eligibility.py` | new | `negative_eligibility` + `nephrotox_grade_modeling` |
| `scripts/make_release_manifest.py` | new | Content-derived release id + checksums |
| `RELEASE_MANIFEST.json` | new | Binds data, derived files and documents to the release |
| `scripts/split_human_animal.py` | modified | `comparison_type`, verdict suppression, `human_negative_eligible` |
| `scripts/build_merged.py` | modified | Carries the two new columns (46 cols) |
| `scripts/build_workbook.py` | modified | Human-first tab order; animal appendix; new columns |
| `scripts/release_check.py` | modified | Gates trial counting, eligibility coupling, tab order |
| `data/measurements.csv` | modified | +2 derived columns; 21 `source_ref` normalised; notes appended |
| `NARRATIVE.md` | modified | Human-trials-first presentation; bridge and statistics corrected |
| `METHODOLOGY.md` · `METHODOLOGY_PHASE2.md` · `STATUS.md` · `schema.md` · `CLINICAL_VALIDATION.md` · `PADP.md` | modified | Statistics, purity wording, bridge figures, new fields |

**Historical records preserved.** No measurement row was deleted, no grade overwritten, no
animal data removed. Every reclassification is an added derived column with its reason
recorded in that row's `notes`. `BEEBOP_SUGGESTIONS_2026-09-30.md` was not edited.

---

## 4. Counts, by evidence class

**Counting rule for trials:** a trial counts **once** however many measurement rows,
publications, labels or repeated outcomes reference it. An extension or longer follow-up of
the same trial is the same trial. A regulatory label, review, case report or pooled
cross-trial analysis is **not** a trial. A study with neither a name nor a registry
identifier is unresolved and does not count. No identifier was invented.

| Human clinical evidence (deduplicated by study) | count |
|---|---:|
| **Verified trials** (identified **and** primary document read) | **3** |
| Trials identified but not yet read | 14 |
| → total distinct trials identified | 17 |
| Distinct regulatory labels (not trials) | 13 |
| Pooled cross-trial analyses | 1 |
| Reviews / editorials | 2 |
| Case reports | 1 |
| Unresolved citations | 1 |
| Clinical **measurement rows** *(not a trial count)* | 42 |
| Unique compounds with clinical evidence | 31 |

Verified trials: **DMD114673**, **Cemdisiran phase 2 IgAN**, **SEQUOIA**.

| Other evidence classes | count |
|---|---:|
| Human laboratory / ex-vivo rows (separate; not trials) | 67 |
| Animal appendix — animal in-vitro | 81 |
| Animal appendix — animal in-vivo | 56 |
| → animal total, excluded from all human totals | 137 |
| All measurements | 246 |
| Oligos / with sequence | 65 / 55 |
| Rows gated out of negative training | 20 |
| Clinical grade-0 rows that are confirmed negatives | **1** |

---

## 5. Additional findings

1. **The `source_ref` inconsistency** (§2, Priority 3) — the same patent cited two ways,
   silently breaking any same-source analysis. Found only because the pairing test produced
   a result I did not believe.
2. **My own internal inconsistency on `MSR045`** — documented as efficacy-derived in one
   file, classified as a measured negative in another. Worth noting as a class of error:
   a finding recorded in prose does not propagate itself into the data.
3. **Priority 2's scope is 8 rows, not 29** — 21 of the 29 are positive findings.
4. **The release gate caught my own tab rename** before I shipped it, which is the argument
   for having it.
5. **Statistical framing matters more than I treated it.** The "3.7×" claim was not a small
   wording issue; it misrepresented a 7.9-point effect as a 3.7-fold one.

---

## 6. Decisions requiring German / Oscar

**For German (scientific):**

1. **Are the five `asserted_negative_regulatory` downgrades right?** Does a label's
   "kidney toxicity was not observed in the clinical studies" — with no endpoint table —
   support a usable safety negative, or not? This currently gates 6 rows out of modelling.
2. **Is `MSR066` genuinely the only confirmed clinical negative?** It is the only one with a
   quantitative safety endpoint from a document we have read. If that is right, the dataset
   has essentially no usable clinical negative class, which is a significant statement.
3. **Does same-patent-different-table count as genuinely paired?** The three Roche compounds
   have human cell data in Table 2 and rat in-vivo data in Table 1 of one patent. I class
   them paired; they are the same laboratory and compounds but different experiments.
4. **The two grading rubrics** (`NARRATIVE` §4.3) — thresholds are anchored on each source's
   own innocuous control, but the cut-points are mine.
5. **Whether 3 verified trials is the right headline**, or whether identified-but-unread
   trials should be reported as a second headline tier.

**For Oscar (access / permissions):**

6. **Author or manufacturer contact for purity.** Per-batch purity exists only in
   Certificates of Analysis. I have not contacted anyone and will not without your approval.
7. **The 14 identified-but-unread trials.** Eleven are open-access PMC articles that NCBI
   blocks automated retrieval of but that open normally in a browser; the rest are paywalled
   or FDA review documents. Listed in `SOURCES_TO_ACQUIRE.md`.
8. **`MSR064` zilebesiran** cites `KARDIA_trials`, which is not a resolvable citation. It
   needs a real reference before anyone can verify that row.

---

## 7. Verification, limitations, readiness

**Verification performed.** `scripts/release_check.py` passes, now gating: integrity (65
oligos / 246 measurements, 0 orphans, no duplicate keys, grades in range); strict-kidney
isolation (246/246 `is_kidney_specific=TRUE`, renal tissues only, no hepatic readouts,
models or hepatotoxicity source panels, viability rows renal-only); the register covering
every clinical row with no non-trial class counting toward the trial total; a deduplicated
trial count strictly below the row count; `nephrotox_grade_modeling` blank **iff** the
negative is not eligible (0 mismatches); `nephrotox_grade` preserved on every row; all
human/design tabs preceding the animal appendix; and every Human-trials row carrying both a
sequence cell and a grade. All derived files regenerated through the existing scripts.

**Limitations.**

- Only **3 of 17** trials have had the primary document read. The headline verified count is
  genuinely small and should not be inflated.
- **One** confirmed clinical negative. The clinical negative class is effectively unusable
  for modelling as it stands.
- Purity unreported for all 65 oligos; targeted supplements and batch records unexamined.
- All grades remain **provisional** pending German's sign-off.
- 39 of 246 rows lack a numeric dose, pending FDA Pharmacology/Toxicology reviews.
- The bridge is 15 compounds, 10 genuinely paired — descriptive, not a fitted species model.
- Scope confirmed kidney-only; no other endpoint's data was read or written.

**Readiness.** The dataset and its four submission artefacts are **structurally complete
and internally consistent at release `kidney-5d82de234c71`**, and the human-first
presentation Oscar asked for is implemented rather than described. It is **not
scientifically signed off**: the trial verification tier, the negative-eligibility
downgrades and the grading thresholds are curation judgements awaiting German. The honest
summary is that this round made the dataset's weaknesses legible and machine-readable rather
than making them smaller — the trial count fell from an implied 42 to a verified 3, and the
confirmed clinical negatives from 21 to 1. Both are corrections, not regressions.
