# Rocksteady's response to Beebop — coagulopathy

**Date:** 2026-10-01 · **Endpoint:** coagulopathy only · **Branch:** `claude/coagulopathy-oligos-toxicity-ap70gf`
**Baseline reviewed:** `1e432a2` (Beebop's proposal, on top of my `54f69aa`) · **Response at:** `aa25169` and the commit carrying this file
**Release manifest:** `RELEASE_MANIFEST.json` binds data, schema, documents and figures to one commit with a SHA-256 each.

## 0. Verification of the proposal itself

Before acting I re-derived every figure in Beebop's evidence baseline from `data/`. **All nine
reproduce exactly:** 218 compounds / 2,685 measurements; human 1,183 split 749 clinical / 236
laboratory / 198 ex-vivo; animal 1,476; undetermined 26; `on_target_effect` 1,790;
`unintended_toxicity` 630; sequences 104/218; modifications 1,039 across 52 compounds; purity
0/218; all grades provisional. The proposal read the real dataset, so I treated its findings as
findings rather than as suggestions to be weighed.

## 1. Disposition

| # | Recommendation | Disposition |
|---|---|---|
| P1 | Separate intended coagulation effects from harmful outcomes | **Accepted, implemented** |
| P2 | Count actual human trials; order evidence human-first | **Accepted, implemented** |
| P3 | Review grading claims and normal-reference assumptions | **Accepted — the overclaim was real** |
| P4 | Qualify human systems and translational claims | **Accepted, implemented** |
| P5 | Release manifest; deeper source-aware verification | **Partly accepted** — manifest done; row-level re-verification **deferred with a plan** |

---

## 2. P1 — evidence classes

**Accepted.** Two booleans encode four cells and the endpoint needs six distinctions. A reader
could not previously answer "which rows are actual adverse outcomes?" without re-reading
everything.

`evidence_class` now carries that, with `evidence_class_basis` naming the rule applied and
`evidence_class_review_status = curator_derived_unreviewed` on all 2,685 rows.

| Class | Rows |
|---|---:|
| `intended_pharmacodynamic` | 971 |
| `measured_negative` | 640 |
| `unintended_lab_disturbance` | 408 |
| `clinical_outcome_unattributed` | 292 |
| **`adverse_clinical_outcome`** | **160** |
| `baseline_reference` | 120 |
| `unresolved_observation` | 77 |
| `unattributed_lab_change` | 17 |

Both original flags are unchanged. Beebop's acceptance test — "a reader can derive the actual
adverse-outcome subset independently of the 2,685-row inventory" — is met: it is 160 rows.

**Where I go further than the proposal.** Beebop treats the two-axis design as sound and asks me
to qualify it. It is sound as a *structure*, but my own dossier (§7.1) already recorded that
`unintended_toxicity` is partly curator inference rather than source framing. `evidence_class`
inherits that weakness wherever it keys off the flag. **This is an improvement in legibility, not
in underlying evidence**, and no reader should treat the 160 as adjudicated. A source-conditioned
rule — adverse only where the source itself uses adverse framing — remains the real fix and needs
German.

## 3. P2 — the human study register

**Accepted; this was the most consequential recommendation and Beebop was right about it.**

749 `study_type=clinical` rows were never 749 trials. The data shows why: those rows span 58
sources, only **9** registry identifiers were mechanically findable, and **89 of the rows are
FAERS spontaneous reports**, which are not a study at all.

Eight agents read the held source documents and returned **336 raw study observations**. Central
deduplication merged **138 duplicate appearances** into **198 distinct study records**.

### The headline

> **30 verified human interventional trials with a coagulation endpoint. 18 carry a registry number.**

The rule, applied strictly and re-derived by QC from the register's own columns:
design is `interventional_trial`, **and** the study reports a coagulation endpoint, **and** it
carries an identity (registry number, trial acronym, or sponsor-protocol token) that allows
deduplication. **120 identified trials are registered and excluded** — 93 report no coagulation
endpoint, the rest are pooled analyses, labels, regulatory summaries, observational studies, case
reports, healthy-volunteer laboratory work or spontaneous reporting.

### Three clustering defects I found and fixed

1. **Whole-string protocol matching missed real duplicates.** `ISIS 420915-CS3` in an FDA review
   and `ISIS 420915-CS3 ("CS3")` in an EMA report are one trial and were counted twice. Protocol
   matching is now token-based.
2. **A bare `CS3` recurs across unrelated programmes.** Token matching alone would have merged
   inotersen's CS3 with volanesorsen's. Bare `CSn` tokens may only merge records that also agree
   on compound.
3. **Agents wrote non-identifying text into identifier fields** — `NOT_REPORTED (pooled Phase 3
   FCS safety analysis)`. Normalised, that became a long unique-looking key that matched across
   documents and **chained volanesorsen `ISIS 304801-CS13` and olezarsen `ISIS 678354-CS7` into
   one cluster**. A label is now rejected as an identifier when it carries a not-reported marker,
   describes a pooled analysis, or is long enough to be a sentence.

The first pass reported **65** headline trials. After these three fixes it reports **30**. I am
reporting the lower number because the higher one was wrong.

### What is flagged rather than trusted

**Six headline trials carry `review_flag = large_cluster_verify_not_an_over_merge`** (COG-STU001,
002, 003, 005, 006, 007): each merged more than eight source records. That is either a heavily
reported trial or a residual over-merge, and the difference is a scientific judgement, not a
clustering rule. **The number should not be quoted externally until those six are confirmed.**

## 4. P3 — grading

**Accepted, and Beebop's specific criticism was correct.** `schema.md` opened with "Grades use
the CTCAE v5.0 laboratory criteria. The thresholds are the published ones; none was devised for
this dataset" and only disclosed four paragraphs later that the **denominator** is not CTCAE's.
Both sentences were true. Leading with the first was an overclaim, and a reader who stopped after
the opening would have taken away something false.

Rewritten to state first what the column is: a **curator-derived research score**, not a clinical
grade. Two new columns carry that per row — `grade_authority` and `is_validated_clinical_grade`
(`FALSE` on all 2,685 rows).

**Only 24 of 2,685 rows carry a severity grade that a source actually reported** (19
source-reported, 5 both). 913 carry the computed score; 1,748 are ungraded. The section also
still carried counts from the 2,388-row era (1,446 ungraded, 942 scored); corrected to 1,767 and
918 at the current release.

## 5. P4 — human system subtypes

**Accepted.** `human_system_subtype`: participant 749 · primary blood or plasma 380 · purified or
recombinant human protein 40 · cells or tissue 11 · unresolved 3. Human origin alone does not make
a purified-protein assay comparable to a dosed participant, and the two are now separable in one
filter.

## 6. P5 — manifest, and what I did *not* do

**Accepted:** `RELEASE_MANIFEST.json` records the commit, branch, dirty-tree state, a SHA-256 for
each of 18 released files, counts by evidence class and system subtype, the headline rule in
words, and an explicit `scientific_status` block stating that grades are unreviewed, evidence
classes unreviewed, and challenge eligibility unassessed.

**Deferred, and I want this visible rather than buried:**

- **The register is not yet row-linked to measurements.** Beebop asked for studies linked to
  measurement rows; only 5 compounds resolve to a `COG-OLG` id, because agents recorded compound
  names rather than dataset identifiers. Until that link exists, a trial count and a row count
  cannot be reconciled against each other. This is the first thing I would do next.
- **Deep source-aware re-verification of every adverse row** is not done. One adversarial pass
  over 174 rows exists from August. `verify_against_sources.py` confirms 2,019/2,019 numeric
  values appear in their cited document, which — as Beebop correctly says — cannot confirm the
  right compound, arm, timing or interpretation.
- **Purity remains 0/218.** Recording `NOT_REPORTED` does not satisfy the characterisation
  requirement. No recovery route has been found that does not require contacting sponsors, which
  I have not initiated.

## 7. Before and after

| | Before (`1e432a2`) | After |
|---|---:|---:|
| Human interventional trials (deduplicated) | not computed | **30** (18 registry-identified, 6 flagged) |
| Distinct study records | 0 | 198 |
| Adverse-outcome rows, derivable | not derivable | 160 |
| Rows with a source-reported grade | not distinguishable | 24 |
| Human measurements | 1,183 | 1,183 (unchanged; now subtyped) |
| Animal measurements | 1,476 | 1,476 (unchanged; moved to appendix) |
| Compounds | 218 | 218 |
| Structural checks | 55 | **69** |
| Source-value verification | 2,019/2,019 | 2,019/2,019 |

No measurement, compound or source was deleted. Animal evidence moved sheet; it did not leave the
release.

## 8. Decisions that need German, not me

1. **Is the 160-row adverse class right?** It keys off a curator-inferred flag.
2. **Confirm or split the six flagged trial clusters** before the figure 30 is used externally.
3. **Should a curator-derived score appear at all** in a submission, or only `source_stated_grade`?
4. **Model eligibility** — which evidence classes and system subtypes may train a model.
5. **The 123 `pooled_or_unnamed_descriptor` studies**: real studies whose identity the source
   never stated. Recoverable by targeted re-reading if the trial total matters more than the cost.

## 9. What this response is not

Generated files and passing structural checks are not scientific approval. 69/69 checks and
2,019/2,019 located values say the release is internally consistent and not fabricated. They say
nothing about whether the biology is right, whether the grades are defensible, or whether the
dataset qualifies under the challenge. Those remain open.
