# For German's decision queue — hydrocephalus

Prepared by Rocksteady (hydrocephalus) 2026-10-03, formatted to fold into
`German_requests_100326.md`. Branch `claude/hydrocephalus-toxicity-oligos-t172zv`,
release `hydrocephalus-3d76b77`. Figures measured from the committed tree, not
reported from a prior document.

Raised by the session that built the column, against itself. Nobody asked for it.

---

## N. Hydrocephalus — is the `hydroceph_grade` curator rubric permissible at all

**Why.** `SCIENTIFIC_RULES.md` §A states that no agent may **assign toxicity
labels**. This endpoint's central column is an agent-assigned ordinal toxicity
severity label. If §A is read strictly, the column should not exist in the form
it does, and it is the column every downstream figure, the ML outcome and the
narrative rest on. I cannot resolve this myself — §A also forbids agents
resolving scientific conflicts — so it is escalated rather than defended.

**Where the rule comes from.** `SCIENTIFIC_RULES.md` is a derivation prepared by
Crank at Oscar's direction, published on `claude/crank-phase2-oversight`. Its §A
states it derives the agent contract from your definition of the AI role as
**dormant raw-transfer**, activated only once a verified local structured source
exists with a recorded checksum, and lists the five prohibitions. The derivation
cites two of your documents: the *OligoTox Immunotoxicity Scientific Validation
& ML Correction Memo* (v0.1, 24 Aug 2026) and *OligoTox Thrombo Scientific
Governance and Model Readiness* (v0.9). I have not seen either — they are in
Drive and not visible from this repository. **If the derivation has overstated
§A, this question dissolves and the answer is simply "the derivation is wrong",
which is useful to know on its own.**

**Context — what the column actually is.** `hydroceph_grade` is an ordinal 0–3
severity scale defined by a rubric in `SCHEMA.md` §"`hydroceph_grade` rubric
(0–3)", graded on clinical/structural consequence:

| | Rows |
|---|---:|
| Rows carrying a grade | 1,316 of 1,342 |
| grade 0 | 1,114 |
| grade 1 | 101 |
| grade 2 | 79 |
| grade 3 | 22 |
| **Rows with a positive severity call (1–3)** | **202** |
| `grade_status` = `provisional` | **1,316 — all of them** |
| Rows with a `grade_basis` stating how the grade was reached | 1,316 — all of them |

**The part that matters.** Of the **202** rows carrying a positive severity call,
only **31** have the source itself attributing the event to the drug
(`attribution_as_stated = drug_attributed`). The other **171** sit at
`not_discussed`: the source reported an event, and the **curator** — not the
source — placed it on a severity scale. That is the operation §A names.

Mitigations already in place, offered as facts rather than as a defence:
- every graded row carries a `grade_basis` naming the rule applied;
- every grade is marked `provisional`, none `adjudicated`;
- the source's own attribution is held separately in `attribution_as_stated` and
  is never overwritten by the grade (§E's author-versus-curator separation);
- grade 0 requires `ascertainment = measured_null`, and spontaneous-report
  silence was moved out to `reported_zero_no_denominator` precisely so it could
  not masquerade as an assessed negative.

**Needed — one of four rulings.**

1. **Permitted as built.** The rubric stands, `provisional` is the right marker,
   and §A's prohibition is aimed at unmarked or adjudicated labelling. Nothing
   changes.
2. **Permitted but must be renamed and demoted.** The column is a *curator-derived
   provisional severity index*, not a toxicity label, and must be presented as
   such everywhere, including as the ML outcome's basis.
3. **Permitted only where the source attributes.** Keep the 31 source-attributed
   rows graded; move the other 171 positive calls to `UNKNOWN` / `HOLD` pending
   your adjudication. This would reduce the graded positive set by **85%** and
   materially change the headline figures.
4. **Not permitted.** The column is withdrawn from the published dataset and
   retained only as an internal annotation.

**Blocks.** Not blocking acquisition or description, which continue. It does
block: any claim that the release's severity figures are scientifically
adjudicated; the tier-A positive counts as published; and the interpretation of
the ML outcome, which is defined on tier-B events rather than on grade but is
reported beside the grade distribution. Rulings 3 and 4 would change published
numbers, so I am holding any change until you decide rather than pre-empting one.

**My own read, offered only because withholding it would waste your time.**
Ruling 2 looks closest to the facts: the column behaves like a provisional
curator index, is already marked as one row-by-row, and keeps author attribution
separate — but it is *named* like a toxicity label and is read as one. I have no
standing to choose, and I have not acted on this view.
