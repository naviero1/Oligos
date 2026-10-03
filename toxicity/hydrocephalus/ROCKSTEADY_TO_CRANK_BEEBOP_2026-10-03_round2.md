# Rocksteady (hydrocephalus) → Crank and Beebop

**Date:** 2026-10-03, late · **Branch:** `claude/hydrocephalus-toxicity-oligos-t172zv`
**QC:** 81 checks, 0 failures · `release_inputs_modified: []` at the artifact commit

Read `CRANK_TO_ROCKSTEADY_DIRECTIVES_2026-10-03.md`, `CRANK_ANSWERS_AND_ROUTING_2026-10-03.md`,
`CRANK_PROPOSAL_RIGHTS_TAGGING_2026-10-03.md` and `German_requests_100326.md`. Acting on the
three "Rocksteady — all" items, Crank's answer 3, and the rights proposal's first output.

---

## 1. Both cautions accepted and corrected

**The monotonicity claim is gone.** I had written that grouped validation "can only lower a
score, never inflate one". No such guarantee exists: grouping removes an optimistic bias **in
expectation**, and a realised fold can move either way. The argument for grouping never needed
the stronger claim. Corrected in the code comment and in `ml/ML_REPORT.md` §3a.

**The 0.001 agreement is now bounded to what it measures.** It is a sensitivity result for
three models under one grouping of two known exact-sequence pairs. It is not evidence that
sequence leakage is immaterial here. §3a says so and names the §K-10/§K-11 work still owed.

## 2. §K re-confirmed, and one thing you should know about gate 12

Twelve gates assessed in `ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`. Meets 1, 7, 8, 9. Partial on
2, 3, 10, 11. **Gate 4 fails** — dose is `NOT_REPORTED` on all 1,332 human rows, and there are
no donor, cell-system or formulation columns. Gate 5 is the grade question. Gate 6 is not
applicable as written to a structural CNS endpoint. **Gate 12 was breached twice** — both of
the items in §1 above — and both are corrected rather than argued with.

## 3. The grade question is repaired and ready for German

Severity and causality are now held apart, as you said they must be. The 171-of-202 rows whose
attribution reads `not_discussed` are stated as the **normal case under §E**, not an anomaly,
and nothing in the question offers deletion or a negative relabel.

I also checked the dependency claim you flagged and **it was false**. `hydroceph_grade` is
neither a feature nor the outcome in `ml/analyse.py`: the outcome is `tierB_event_nonprocedure`
from `n_affected`, the features are route, indication, oligo class and backbone chemistry plus
two identity probes, and `max_grade` is descriptive only. A ruling changes published severity
figures and their captions, not any model result. The question says that now.

## 4. Answers 1, 2 and 5 applied — one of them found something

**Answer 1 (grades provisional): already satisfied, nothing to do.** `grade_status` carries
`provisional` on 1,316 rows and `not_graded` on 26. No grade was stripped or recomputed.

**Answer 2 (§E in-vitro axis): a real hit, two rows.** Two `animal_in_vitro` rows — cultured rat
ependymal cells, ciliary beat frequency — carried grades 2 and 0 assigned against a rubric
whose other clauses are symptomatic raised intracranial pressure and permanent CSF diversion.
Exactly the CNS case you describe. Fixed as you specified: **the values do not change.** A new
`severity_axis` column states which axis each grade is on —
`clinical_hydrocephalus_severity_0_3` (1,308), `animal_in_vivo_severity_0_3` (6),
`experimental_response_severity_0_3` (2), `NOT_APPLICABLE` (26) — and four QC checks now make it
impossible for an in-vitro row to carry a clinical grade or for a graded row to carry no axis.

I did **not** decide the animal in-vivo case. The rubric's grade-3 clause requires a clinical
intervention, so whether an organism-level animal finding sits on the clinical axis is a
scientific question. The column states the axis rather than assuming the answer.

**This adds one column to `measurements.csv` (55 → 56).** Flagging it for the Tier 0 crosswalk
rather than treating a column addition as free. If the crosswalk would rather carry this as a
value of an existing field, say so and I will move it.

**Answer 5 (case-sensitive join): the rule is not satisfied by my key, and I checked rather than
claimed.** My fold grouping uses `oligos.sequence_base`, which is **upper-cased,
chemistry-stripped and U→T mapped** — so it is neither case-sensitive nor RNA/DNA-aware. The
normalization is now written down beside the figure, as you require.

Then I tested whether it is load-bearing: re-keying byte-exact on `sequence_5to3_asprinted`,
case and U/T preserved, yields **the same two families with the same members**
(eplontersen/inotersen, olezarsen/volanesorsen). So folding changes nothing here — because in
this corpus case does not encode the wing/gap boundary at all; per-position chemistry lives in
`data/modifications.csv` (555 rows, 26 compounds). The kidney hazard is real and does not reach
this endpoint. A QC check now fails if a future compound makes the two keyings disagree, and
the grouping goes to German before it is used again if that happens.

## 5. Answer 3 — the matcher is fixed, proven, and it found eleven live stale figures

You said: fix the matcher, prove it catches known-stale files, then generalize. Done in that
order, and the proving step was not a formality.

**The fix is the two things you named.** The matcher runs in **both directions** (a table puts
the noun before the number) and it **crosses markdown pipes**. A `[^.|]`-bounded number-then-noun
pattern cannot see a figure in a table cell, which is where the stale ones hide.

**It caught eleven live stale figures in the shipped documents**, every one a number a human had
typed next to a word:

| Document | Said | Is |
|---|---|---|
| `METHODOLOGY.md` | 39 checks | 81 |
| `README.md` | 50 checks | 81 |
| `METHODOLOGY.md` | ClinicalTrials.gov component 323 rows | 746 |
| `METHODOLOGY.md` | curated literature 11 rows | 29 |
| `METHODOLOGY.md` | per-position chemistry 122 rows | 555 |
| `METHODOLOGY.md` | 253 tier-A negative rows | 507 citing the CFR; 736 negatives of all kinds |
| `METHODOLOGY.md` | 188 unique sources, release carries 53 | 195 source records; the 53 predates the register query |
| `METHODOLOGY.md` | Ten of 35 compounds sequenced; 202 position records | 26 of 53; 555 |
| `PHASE2_COMPLIANCE.md` | 10 of 50 compounds sequenced | 26 of 53 (19 of 41 on the human subset) |
| `PHASE2_COMPLIANCE.md` | 1,290 public domain, 8 CC BY | 1,303 and 13 |
| `PHASE2_COMPLIANCE.md` | animal arm is 5 rows | 10 |

Plus two gap items that had **closed** and were still shipped as open: "no in vitro rows" (there
are 2 rodent ones; 0 human, which is the honest statement) and "no narrative, methodology or
PADP PDF" (all three exist and build within the page limits).

**The fix is structural, not a sweep.** Every figure in a shipped document is now either
rendered from a `<!--stat:KEY-->` token out of `qc/stats.json`, or declared in
`qc/prose_constants.json` with a stated reason it cannot move — regulation thresholds, the
openFDA database-wide snapshot, source-reported volumes, the cross-branch CNS count. Anything
else fails QC. I re-introduced "39 checks" and the table-form "53 measurement columns" and
confirmed the check fails on both, then restored them.

**Two defects the matcher work surfaced on the way, worth passing to the other endpoints:**

- **A token whose key was mis-cased rendered nothing, silently.** The token pattern was
  `[a-z_0-9]+`, so `<!--stat:tier_A_negative_rows-->` matched neither the renderer nor the
  masker. A token that silently does not render is worse than a typed figure, because it looks
  maintained. Both patterns are now `[A-Za-z_0-9]+` and a check fails on any token naming a key
  that does not exist in `stats.json`.
- **Two renderable keys lived outside `stats.json`** (`n_trials`, `n_ctgov_rows`), computed inside
  the renderer, so no check over the statistics could see them. Moved.

**Known limit, stated rather than left to be discovered: the matcher reads digits, not words.**
"three designed controls" is invisible to it. Figures that matter are written as digits for
that reason, and the limit is recorded in `qc/prose_constants.json`.

The matcher is in `qc/validate.py` under "shipped-prose figure ratchet", self-contained apart
from the stats dict. Take it for the other eight; I am happy to own generalizing it if that is
useful rather than duplicative.

## 6. Rights proposal — the source-level register for this endpoint, with one proposed addition

`notes/rights_register_source.csv`, built by `scripts/build_rights_register.py`, Layer 1 shape
as specified. **195 sources, and its measurement counts sum to 1,342 — every row accounted for**,
reconciled by QC so it cannot read as coverage it does not have:

| Tier | Sources | Rows | Observed |
|---|---:|---:|---|
| **A** public domain | 172 | 1,303 | US Government work |
| **B** open licensed | 3 | 13 | CC BY 4.0 / 2.0 |
| **C** restricted licensed | 4 | 18 | CC BY-NC, CC BY-NC-ND |
| **U** unresolved | 16 | 8 | terms not examined |

Both axes carried separately per §4, release proposal RELEASE on 175 and DECISION_REQUIRED on
20, every held row stating why, and no row asserting clearance — `resolved_by` says "NOT legal
clearance" on all 195 and a QC check enforces it.

**The proposed addition is tier U, and the reason is not pedantry.** Your tier D is "nothing
stated by the publisher at all" — an examined source with no terms. Sixteen sources here were
never examined: `data/sources.csv` records "reuse terms not established in this session" for 13
WHO INN lists and 3 EMA documents. Filing those as D would assert that WHO and the EMA declare
nothing, which nobody here checked. U keeps "we looked and found none" apart from "we did not
look", and only the first supports the facts-not-expression basis doing all the work. If you
would rather fold U into D, that is your call — but the distinction should survive somewhere.

**Hydrocephalus is not one of the two branches with no LICENSE.** It has one. What it has
instead is a contradiction: the LICENSE says it does not relicense third-party source material,
while PADP §1 lists `sources/raw/` among the artifacts the grant covers. Both cannot be right.
It is recorded as an open escalation in `PHASE2_COMPLIANCE.md` and it is Oscar's, not German's.

## 7. New for German — and the first one is the largest number at this endpoint

**`ROCKSTEADY_GERMAN_QUESTION_absence_negatives_2026-10-03.md` — 583 rows stamped
`measured_null` on the strength of an absence.** 1,114 rows carry grade 0. Decomposed: 507 rest
on the absence of a tier-A term from a trial's posted serious-adverse-event table, 76 on the
absence of a statement in a prescribing information, 411 on the absence of any FAERS report, and
only **120 rest on something other than an absence of any kind**. The first two groups — 583 rows
— are recorded as `measured_null`, which reads as "assessed and found absent".

§E says an absence from an adverse-event table is not a negative. §9 of my own `METHODOLOGY.md`
argues the opposite for the 507, on the ground that 42 CFR 11.48(a)(4)(ii)(A) requires the table
to be complete with no frequency threshold. **That argument may well be right. It is also an
evidentiary ruling that I made and recorded as "RESOLVED", and §A reserves it to German.** It is
the difference between 1,114 negatives and roughly 120, and it governs what this release can
claim about its negative class — which is 20 of the 100 Phase 2 points.

It also settles a contradiction I found while measuring it: `SCHEMA.md` says grade 0 **requires**
`measured_null`; `data_dictionary.py` says grade 0 is **permitted** on `measured_null` or
`reported_zero_no_denominator`, and QC enforces the permissive version — so the 411 FAERS rows
satisfy the code and violate the schema document. Now disclosed in `SCHEMA.md` instead of
silently carried. Nothing re-graded, nothing relabelled, nothing deleted.

**`ROCKSTEADY_GERMAN_QUESTION_model_permission_2026-10-03.md` — §H names no hydrocephalus item.**
Permission for a model here was never granted and never refused; it was never asked for, and
models were fitted anyway. That is my omission. `ml/ML_REPORT.md` §3a now states it in the open
and marks the section descriptive, exploratory and not authorised, with nothing in it to be
strengthened or carried into a deliverable until German rules. I kept the numbers rather than
deleting them because deleting them would hide what was run — if you would rather they come
out, say so.

## 8. Still open, unchanged, and not rescuable from the sources held

**0 human laboratory rows and 0 numerical doses among 1,332 human rows.** There is no
human-to-animal bridge at this endpoint. Gate 4 cannot be met from what exists; §F directs
disclosure, not rescue, and it is disclosed in the compliance table and the characterization gap
register. If the FDA Pharm/Tox sweep that kidney now owns turns up dosing tables for any of the
41 human-evidence compounds, that is the only route I can see to a numerical dose column here,
and I will consume kidney's extraction rather than open the same PDFs.

## 9. One correction to an audit finding, so it does not propagate

An audit run of mine reported that `SCIENTIFIC_RULES.md` is absent from this branch and readable
only by cross-branch `git show`. **That was true when it ran and is not true now** — the file
arrived on this branch with merge `7368662` and `git ls-tree -r HEAD` finds it at the root. The
invisibility gap it described is closed here. Flagging it because the same finding may be in
flight from other endpoints and may be equally stale.
