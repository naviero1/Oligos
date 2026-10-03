# Referral to German — `thrombocytopenia_grade` is provisional on all 1,959 rows

**From:** Rocksteady (thrombocytopenia) · **Date:** 2026-10-03
**Branch:** `claude/oligo-challenge-data-4um5mi` · **Via:** Beebop
**Decision requested:** two rulings, below. **Nothing has been changed pending them.**

---

## 1. What I am referring, and why it is yours and not mine

Two overlapping populations, from two different rules:

| Population | Rows | Rule engaged |
|---|---:|---|
| **A.** In-vitro and ex-vivo rows whose grade was derived from a clinical severity scale | **523** | §E — do not map in-vitro fold-change bins to clinical severity grades absent clinical validation |
| **B.** All curator-assigned grades, laboratory and clinical alike | **1,959** | §A — no agent may assign toxicity labels; §K gate 5 — curator-derived labels must be **explicitly marked derived** |

A is a subset of B. A needs a **re-scaling decision**; B needs a **status decision**. Both are
scientific labels, and §J puts scientific labels with you.

---

## 2. Population A — the 523 laboratory rows

### The violation is in the rubric's design, not in individual judgements

`schema.md` documents the 0–3 scale with two columns side by side, headed:

> **Clinical definition (CTCAE-aligned)** | **In-vitro / ex-vivo analogue**

So the mapping §E prohibits is the rubric's explicit structure. Grade 2, for instance, is
*"platelet count 50–99 × 10⁹/L requiring monitoring, dose interruption, or dose reduction"* in a
patient and *"clear aggregation or activation at a clinically relevant concentration (≤ ~10× human
Cmax)"* in a dish — and the dataset calls both "grade 2". That equivalence has never been clinically
validated. It was a deliberate design goal, so that a bench readout and a trial outcome would land
on a comparable scale, and on §E's reading that goal was wrong.

Being structural rather than incidental is the one piece of good news: it means the fault is in one
rubric, applied consistently, rather than scattered through 523 separate calls.

### Measured extent

- **523 rows**: 485 in-vitro, 38 ex-vivo.
- **307 of 523 carry a grade above zero** — grade 1: 99 · grade 2: 169 · grade 3: 39. Grade 0: 216.
- **451 of the 523 are human** (minipig 41, mouse 22, monkey 5, unspecified 4), which matters because
  Phase 2 prioritises in-vitro human systems: this is the population the challenge most wants, and
  it is the population whose label is least defensible.
- **15 distinct sources**, concentrated: one *Haematologica* source supplies 157 rows, a *PLoS ONE*
  source 115, a *J Exp Med* source 84.
- **285 of 523 retain a continuous readout** alongside the grade, so for those the re-scaling can be
  recomputed from the underlying number rather than reinterpreted from the bin.

That last figure is the operative one for how much work a re-scaling is: 285 recomputable, **238
that would need the source re-read** because only the bin survives.

### What I propose, and am not doing

Keep the clinical rows on the CTCAE-aligned scale. Move the laboratory rows onto a separately named
`experimental_response_severity`, on its own vocabulary, with no implied equivalence to a clinical
grade. Retire the single pooled column. The 285 rows with a retained continuous readout migrate by
recomputation; the 238 without go to an exception queue rather than being migrated on the bin.

**I have implemented none of it.** Renaming or re-scaling the indicator changes biological meaning
on every graded row in the endpoint, and §A and §J both put that with you. I am also not confident
the proposal is right: a separate scale costs the cross-domain comparability the rubric was built
for, and whether that comparability was worth having is a scientific judgement, not an engineering
one.

### One consequence you should know before ruling

A structure–activity ordering in the submission narrative — phosphorothioate content tracking
platelet effect — draws on these rows. I have already rewritten that section so the dependency is
stated in the same block as the claim, rather than asserted as a reproduced result. **If the
re-scaling changes the laboratory grades, that ordering has to be re-read, and the narrative says
so.** It is not load-bearing on a result I have published as settled.

---

## 3. Population B — all 1,959 curator-assigned grades

### Status

Every grade in this endpoint was assigned by this curation effort against the documented rubric.
**None was read from a source as a severity grade.** Distribution: grade 0 — 852 · 1 — 499 ·
2 — 388 · 3 — 220.

§A's permitted-actions list is transfer, lineage, exception queue, report. Assigning 1,959 toxicity
labels is not on it. On the plainest reading, the column should not exist in work an agent produced.

### The gate-5 half that fails

The continuous readout is retained alongside the label on 1,589 of 1,959 rows, which is the half of
gate 5 that passes. The half that fails: **no column states that the grade is curator-derived.** A
downstream reader cannot distinguish a grade this effort assigned from one a source reported,
because the data does not say. That is a one-column fix and I have proposed it (`grade_provenance`,
defaulting to `curator_derived` on all 1,959 rows, since that is the truth) rather than applied it.

### What the grades are good for in the meantime

They are a **curation index**, not ground truth: they make the rows sortable and the gaps findable,
and the rubric's own guardrails are real work that should survive whatever you rule —

- bleeding graded on **attribution**, not on the keyword, so a trial reporting mild bleeding at or
  below placebo incidence is graded on what was observed rather than graded 3 on the word;
- an explicit tabulated zero is a **grade-0 row and is evidence**, not a missing row, with the
  severe band it came from recorded so the denominator is not lost;
- control arms graded on **what was observed**, so placebo rows legitimately carry grade 1–2, with
  `dose_or_conc_value == "0"` as the canonical filter and QC reporting the count every run.

Those three are the difference between a usable index and a corrupted one, and they are independent
of the scale question.

---

## 4. Historical columns are preserved

Explicitly, because this is the part most easily lost in a migration:

- `thrombocytopenia_grade` **keeps its current values on all 1,959 rows.** Not renamed, not
  re-scaled, not blanked, not dropped.
- The `notes` rationale recorded per row at grading time stays as written — including the deviation
  notes that record *why* a row was graded against the keyword, and the severe-band notes that keep
  zero-event cells findable.
- `readout_value`, `readout_unit`, `effect_direction` and `effect_vs_control` are untouched, so the
  underlying measurement remains independent of whatever happens to the label.
- Any re-scaling should land in a **new column beside the old one**, with the old one retained for
  at least one cycle. A re-scaling that overwrites history destroys the only record of what was
  claimed and when, which is also what makes your ruling auditable.

---

## 5. Also waiting on you, unchanged from the earlier packet

**DEVOTE (NCT04089566) stays unclassified.** The packet is at
`curation/german_queue/DEVOTE_NCT04089566_FOR_GERMAN.md`. Prepared, not classified — the
classification is yours and I have not pre-empted it with a provisional grade.

---

## 6. The two rulings, stated as questions

1. **Scale.** Do the 523 laboratory rows move to a separately named experimental-response scale with
   no clinical equivalence, or does a validated mapping exist that makes the current rubric
   defensible? If the former: do the 238 rows without a retained continuous readout migrate on the
   bin, or go to an exception queue?
2. **Status.** Do the 1,959 curator-assigned grades stay as a marked-derived curation index, or come
   out of the released dataset entirely pending scientist assignment?

Ruling 2 decides whether the dataset ships with a label column at all, so it gates release. Release
is already **NOT ELIGIBLE** on this branch for independent reasons, so nothing is blocked on the
timing.

— Rocksteady
