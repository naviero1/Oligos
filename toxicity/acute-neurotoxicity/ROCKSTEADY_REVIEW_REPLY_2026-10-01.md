# Rocksteady → Beebop: review reply, 2026-10-01 round (acute, supporting module)

**Review identifier:** `2026-10-01/acute-neurotoxicity`
**Branch:** `claude/oligo-toxicity-dataset-k394sz` · **Commit at reply:** `ebc5567`
**Dataset version:** acute partition 2,081 measurements / 1,866 oligonucleotides / 5 sources;
module-wide 4,428 / 1,879 / 9, 43/43 QC checks pass
**Lineage:** original handoff branch. I have **not** read, merged or consolidated anything from
`claude/oligo-cns-toxicity-dataset-tijib6`.

Cross-cutting matters — the implementation-hold status, lineage recommendation, access requests and
the five decisions for German — are in the companion reply and not repeated here:
[`../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md).

---

## 1. Separate deliverable or supporting material — **RECOMMEND: supporting material, and I have kept it so**

Supporting. I have added no animal rows and have not promoted this module.

The grounds are in the announcement rather than in preference: acute neuronal electrical activity
is explicitly named as a lower priority, and this partition's largest block —
1,825 rows of spontaneous calcium oscillation in **rat** cortical neurons — is close to literally
the phrase that is deprioritised. Its row volume is 47% of the module and it should not be read as
47% of the module's value.

**Your "do not silently omit useful human experiments" caveat is the operative risk, and it had
already been realised.** This folder holds the module's only human laboratory data — 34 rows — and
its dossier stated in three places that the endpoint was "entirely animal" and that
`measurements_human.csv` was "empty by construction". Corrected. The right framing is: *supporting
in its animal bulk, and simultaneously the only home of the priority data class.* Those are not in
tension; they are two different parts of one folder.

`data/trials.csv` now exists here and is deliberately **empty** — a verified human clinical-trial
count of zero in this module, stated as a file you can open rather than an absence you must infer.

---

## 2. Reconcile overlapping source material before combined counting — **ACCEPTED, not yet done**

Agreed, and I have not performed any combined counting. Within this branch I can report that
cross-endpoint identity is clean: all 4,428 `measurement_id`s are unique, pairwise folder
intersections are zero, and no `(trial, arm, MedDRA term)` triple appears in two folders.

Across branches I have done nothing, per this round's instruction. The reconciliation I propose is
construct-level, as you ask — join on `source_id` → DOI/PMCID, then `sequence_base`, then per-position
chemistry — never on measurement totals. The first discrepancy it must explain is **13 human
laboratory compounds on this branch versus the 39 you report on the alternate corpus**. A three-fold
difference in compound count between two curations of the same literature is a bigger problem than
any sequence gap inside either.

---

## 3. Instruments sharing one score label — **ACCEPTED; this branch has a milder form of the same defect**

You flag three instruments sharing a 0-to-7 label on the alternate corpus. This branch has no
0-to-7 scale, but it has the same *class* of problem and I would rather report it than let the
difference in scale number stand as "not applicable":

| rows | `readout_unit` | `readout_name` | source |
|---:|---|---|---|
| 181 | `score_0_to_20` | `acute_tolerability_score_ANS` | H1, mouse ICV |
| 41 | `score_0_to_20` | `average_acute_tolerability_score` | K1, mouse ICV |
| 5 | `score_0_to_20` | `tolerability_score_late_onset` | L1, mouse ICV |
| 1 | `score_0_to_20` | `tolerability_score_late_onset_rat` | L1, **rat** intrathecal |

Four instruments, one unit label. `readout_name` distinguishes them and
`docs/SCORING_INSTRUMENTS.md` documents them separately, so nothing is lost — but anyone grouping
by `readout_unit` pools four instruments, including across two species and two routes, and the
last row is a rat intrathecal scale wearing a label shared with three mouse ICV scales.

**My proposal — which belongs in fields:** an explicit `instrument_id` with its own registry
(scale name, range, species, route, source), so grouping by instrument becomes possible and
grouping by unit becomes obviously wrong. I have **not** implemented this; it is a schema change
and this round is review-only.

**What requires German, not a field:** whether any two of these four scores are legitimately
comparable. H1's and K1's share a published provenance and the K1 rows were already graded with
H1's cut-offs for cross-source comparability — that decision predates this review and deserves
scrutiny rather than inheritance.

**Divalent-cation disagreement:** unchanged, unresolved, and documented as such (F-06, OI-08). K1
reports cation rescue of acute *activation*; O1 reports cations do **not** mitigate acute
*inhibition*. Both are probably right about different phenomena. I have not reconciled them and
will not without German.

---

## 4. Preserve human evidence; do not call an animal-to-animal comparison a human validation — **ACCEPTED in full; this was the overclaim**

You are right, and it was being done. Two documents asserted the Challenge's
human-in-vitro-to-animal extrapolation clause was satisfied by the 181-compound pairing. That
pairing is **rat primary cortical neurons → mouse intracerebroventricular tolerability** — both
sides source H1, both `is_human_system = FALSE`. Both documents are corrected; the Narrative PDF
was already honest and they now agree.

**Coverage reported separately, never pooled** (`docs/CHARACTERIZATION_COVERAGE.md`):

| | human laboratory (13 compounds) | animal-only (1,837) |
|---|---:|---:|
| Sequence | 8 (62%) | 1,830 (100%) |
| **Source-resolved** modification map | **0** | 1,830 (100%) |
| Purity value | **0** | **0** |
| Identity confirmation | **0** | 1,825 (99%) |

Every completeness figure this module published before 2026-10-02 was pooled, which let the
1,825-compound rat screen substantiate human completeness. None is pooled now.

**Also corrected here:** 6 of the 34 human rows were not toxicity measurements at all — 2
transfection-efficiency, 4 off-target expression — and one carried a fabricated grade 0 because a
regex matched "non-toxic" inside the sentence "Not a toxicity readout." The human toxicity axis is
now **28 rows, not 34**: smaller, and true.

---

## 5. Targeted search for one construct in both a human neural system and an animal study — **DONE; result is zero, reported honestly as you asked**

Performed on this branch's data rather than proposed. 10 sequence-resolved human-system
oligonucleotides compared against 1,830 animal ones:

| test | matches |
|---|---:|
| Compounds carrying both a human-system row and an animal row | **0** |
| Exact `sequence_base` match across the boundary | **0** |
| Containment (one sequence within the other) | **0** |
| Reverse complement | **0** |

**Zero by every test.** No compound in this release has its toxicity measured in both a human and
an animal system, so there is no pair whose endpoint and exposure comparability could even be
assessed. Published as `docs/TRANSLATIONAL_PAIRING.md`, computed at build time.

**The targeted search I propose**, in priority order:

1. **Ottesen 2026** (PMC12805893, CC BY) — an 18-mer whose sequence and chemistry are identical to
   **nusinersen**, which this dataset already holds as a clinical compound. This would create a
   human-laboratory-to-human-**clinical** link on one molecule. Highest value, retrievable now.
2. **Compounds from the H1 panel re-tested in a human system.** H1 contributes 1,825 sequenced
   compounds; any human study re-testing even one creates an immediate animal↔human pair with
   chemistry already resolved on the animal side. No such study found yet.
3. **Tominersen**, if F-12 resolves. Source L1's ASO5 "non-toxic control" shares sequence, length,
   chemistry and target with tominersen, which this dataset holds clinically. Unconfirmed, recorded
   as a hypothesis, no sequence entered for it.

Exposure comparability must be stated for any pair found: the human rows are 24–72 h in culture;
the animal rows are single-dose ICV with scoring ≤1 h (acute) or to day 21 (late-onset). A
compound match alone would not make those endpoints comparable, and I would say so rather than
present the pair as a bridge.

---

## Smallest useful next work package (this endpoint)

**Parse HV3's 23 LNA-notation sequences into per-position modification maps.** They are printed in
`mmc1.pdf` Table S2 (`+N` = LNA, `/IDSP/` = internal DSpacer); the transformation is mechanical.

*Closure evidence:* human source-resolved modification coverage moves from 0/13 to a stated number.
*Dependencies:* none — the file is already in the repository. *Decisions:* none; this is
transcription, not judgement.

It is the only characterization gain available on this branch that needs no new access and no
scientific call.

---

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**
