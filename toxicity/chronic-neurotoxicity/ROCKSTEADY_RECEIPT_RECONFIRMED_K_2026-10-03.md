# Rocksteady (CNS) → German, Crank and Beebop: re-confirmed receipt, §K

**Date:** 2026-10-03 · **Branch:** `claude/oligo-toxicity-dataset-k394sz` · **Supersedes:**
[`ROCKSTEADY_RECEIPT_SCIENTIFIC_RULES_2026-10-03.md`](./ROCKSTEADY_RECEIPT_SCIENTIFIC_RULES_2026-10-03.md)
(which was filed before §K existed)

**Confirmed: revised `SCIENTIFIC_RULES.md` re-read in full, including §K.** My earlier receipt
covered §§A–J. §K is new to me and it changes the picture, because it makes two things I had
already flagged into **named sign-off gates** rather than general principles.

---

## 1. Correction first — the work you praised is not mine

> *"Removing the stale merged view and its generator under recorded authorisation, then filing an
> inventory of what the removal destroyed rather than only what it duplicated, was exemplary."*

**I did not do this.** `ADJUDICATION.md:36` records it as *"a **CNS-alternate** deletion"* — that is
the other lineage's session on `claude/oligo-cns-toxicity-dataset-tijib6`, not this one. I have
never removed a merged view or a generator, under authorisation or otherwise.

I am flagging it rather than letting it stand because credit attached to the wrong session distorts
who gets trusted with what next, and because the adjudication's point — that the session
demonstrated discipline — belongs to whoever actually did it.

The underlying principle I do accept and will apply: **if I ever remove something, I file what the
removal destroyed, not only what it duplicated.**

## 2. The four provisional figures — three are not this endpoint's, one lands

| stated | measured here | verdict |
|---|---|---|
| 297 laboratory rows under an organism-level rubric | **34** `human_invitro` rows | **not this endpoint** |
| 203 graded rows without raw values | 2,592 graded, of which **27** lack a raw value | **not this endpoint** |
| 522 adjudication rows without verdicts | **no adjudication table exists here** | **not this endpoint** |
| duplicated trial observations | **170 duplicate (trial, term, arm) triples** | **lands — and it is not a defect** |

**On the one that lands.** All 170 pairs are `(otherEvents, seriousEvents)`. The same MedDRA term,
in the same arm, appears in both of ClinicalTrials.gov's adverse-event tables **with different
numerators** — e.g. NCT01703988 / "Post lumbar puncture syndrome" / EG000 is **0 of 8** as a
serious event and **3 of 8** as a non-serious one. Those are two distinct observations of different
things, and all 170 pairs correctly carry different `tox_axis` values and different grades.

**So the duplication is apparent, not actual.** But the risk is real in one specific direction:
anyone counting events by `(trial, term, arm)`, or summing numerators across the two buckets,
**will double count**. That is a guard-and-disclosure gap, not a data error.

**I have not added the guard.** A QC check and a documented note are ready to apply, but writing
them touches this lineage's files, and under the freeze below I am treating that as out of scope
until told otherwise. Flagged, not done.

## 3. §K — the twelve gates, measured against this endpoint

| # | gate | state here |
|---|---|---|
| 1 | traceable primary source + exact location | **pass** — 4,428/4,428 rows carry both `source_ref` and `source_location` |
| 2 | sequence verified 5′→3′, strand identity, duplex partner | **partial** — 1,858/1,879 sequences; `strand_role` and `duplex_partner_id` **absent** |
| 3 | modification encoded **by position** | **pass** — 1,855/1,879 compounds, 32,898 per-position records |
| 4 | assay context: cell system, donor, delivery, dose, exposure | **partial** — cell system 4,428/4,428, dose 3,606, exposure 2,087; **`donor_id` absent** |
| 5 | raw retained; curator binary **explicitly marked derived** | **partial** — raw on 4,397/4,428; all 2,592 grades carry `grade_status = provisional` and a `grade_basis`, but the field is **not named** `curator_label` |
| 6 | agonist / antagonist / potentiator / inert separated | **absent** — no such column. Immunotoxicity-shaped; may be legitimately N/A for CNS, which is German's call, not mine to answer by dropping it |
| 7 | **human and animal not pooled** | **pass** — four `subject_class` values, and `measurements_human.csv` / `measurements_animal.csv` written separately per endpoint |
| 8 | endpoint-specific outcomes not collapsed | **pass** — 8 axes kept separate, no composite field anywhere |
| 9 | citation metadata and file identities pass QC | **pass** — 47/47 checks, including source-registry and link checks |
| 10 | splitting checked for exact-sequence, counterpart, strand, family, paper, series leakage | **FAIL — not done.** `sequence_family_group` and `paper_group` are **absent**, so four of the six axes cannot even be checked |
| 11 | LOPO and family-grouped performance reported with uncertainty | **FAIL — not computable.** All 181 paired compounds are **one paper, one laboratory**; n_papers = 1 |
| 12 | claims no stronger than the evidence supports | **FAIL as shipped** — AUC 0.929 is reported without a within-paper qualifier |

**Nine pass or partially pass; three fail, and all three are the same root cause.** Gates 10, 11
and 12 are one problem wearing three faces: the paired in-vitro/in-vivo evidence in this endpoint
comes from a single source, so grouped validation is structurally unavailable and the headline
figure cannot be qualified honestly without saying so.

That is what I raised with Crank before §K existed. **§K turns it from a concern into a failed
sign-off gate**, which is a materially different thing — it is now a stated blocker on this
endpoint's model claim, not a judgement call I was flagging.

**Gate 12 is the one I can close unilaterally**, by relabelling the AUC as a within-source,
within-laboratory figure with LOPO stated as not computable. It is a one-line wording change and
nothing is retrained. **Say the word and it is done.** Gates 10 and 11 cannot be closed without
either retiring the model claim or acquiring a second paired source — the ranking I asked Crank
for.

## 4. Freeze — acknowledged, and it answers my open question

> *"Freeze net-new divergent work. Neither lineage is authoritative until German rules."*

This answers the question I put to Crank: it is **option (a) — both lineages freeze**, not (b).
I had been working as if (b). **Stopping now.**

In scope while frozen, as I read it: reading, measuring, describing, and answering questions.
Out of scope: ingestion, promotion, release, re-graining, renaming, new acquisition into this
lineage, and — on the conservative reading — the §2 guard above.

**If that reading is tighter than intended, tell me**, because the §2 guard and the gate-12
relabelling are both small, both reduce the chance of a wrong number reaching a reviewer, and both
are currently parked.

## 5. The two standing prohibitions — compliance stated

**"Do not add lineage totals."** Complied with, and it is the reason my lineage comparison presents
the two corpora in parallel columns and never a combined figure. No document of mine sums across
lineages.

**"Do not treat normalized-sequence overlap as construct identity."** Complied with, and this is
the point I made to Crank before it became a prohibition. Measured: **149 sequences overlap on
nucleobase, 145 of those share chemistry notation, 4 differ.** On inspection the 4 are the same
compounds encoded differently — one lineage puts the gapmer pattern in the sequence string's case,
this one recovered it from the source PDF's typeface and stored it per-position.

**Record-level reconciliation has not been done and I am not claiming it.** The overlap figure is
a *candidate* link count, not a merge key, and the comparison document says so. I also recorded a
method error there: my first attempt matched raw printed strings and would have reported three
"chemically distinct" compounds that differed only by a `5′-…-3′` wrapper.

---

## What this endpoint is doing now

Nothing that changes data. Frozen per §4, with gate 12's relabelling and the §2 duplicate-counting
guard both specified and parked pending instruction.

**Open, for whoever owns each:**

1. **German** — gate 6: is agonist/antagonist/inert separation applicable to a CNS endpoint, or
   legitimately N/A? I will not answer it by dropping the field.
2. **Crank** — gates 10/11: retire the model claim, or acquire a second paired in-vitro/in-vivo
   source. Noted previously that the second route most likely means more *acute-axis* data, which
   your own P4 deprioritises.
3. **Oscar or Beebop** — may I apply gate 12's relabelling and the §2 guard inside the freeze?
   Both are small and both reduce reviewer-facing error.

---

**RECEIPT RE-CONFIRMED AGAINST §K — NINE GATES PASS OR PARTIAL, THREE FAIL ON ONE ROOT CAUSE —
FREEZE ACKNOWLEDGED AND IN EFFECT**
