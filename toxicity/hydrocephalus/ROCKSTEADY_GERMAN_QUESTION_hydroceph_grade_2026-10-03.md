# For German's decision queue — hydrocephalus

Prepared by Rocksteady (hydrocephalus), **revised 2026-10-03** after Beebop
corrected the first draft. Formatted to fold into `German_requests_100326.md`.
Branch `claude/hydrocephalus-toxicity-oligos-t172zv`. Figures measured from the
committed tree.

**What changed in revision.** The first draft conflated two separate decisions —
how severe an event was, and whether the drug caused it — and then offered
rulings that would have deleted severity information because causality was
absent. It also claimed the ML outcome rests on this column, which is false. Both
are corrected below. The question that remains is one of **interpretation**, not
of deletion.

---

## N. Hydrocephalus — how should `hydroceph_grade` be interpreted and marked

**Why.** `SCIENTIFIC_RULES.md` §A states no agent may assign toxicity labels, and
§K-5 requires that curator-derived labels be **explicitly marked derived**. This
endpoint's severity column is curator-derived. The question is not whether it may
exist, but what it is and how it must be presented so no reader takes it for an
adjudicated finding.

**Where the rule comes from.** §A and §K of `SCIENTIFIC_RULES.md`, Crank's
derivation published at Oscar's direction. §K states it reproduces the twelve
sign-off gates from your immunotoxicity validation memo §9. I have not seen that
memo — it is Drive-only. If the derivation has overstated either rule, this
question narrows or dissolves.

**Context — the column, and the two things it does not conflate.**
`hydroceph_grade` is an ordinal 0–3 **severity** scale defined in `SCHEMA.md`,
graded on clinical/structural consequence — grade 3 means a CSF-diversion
procedure was performed, not that a drug caused it.

| | Rows |
|---|---:|
| Rows carrying a grade | 1,316 of 1,342 |
| grade 0 / 1 / 2 / 3 | 1,114 / 101 / 79 / 22 |
| Positive severity calls (1–3) | 202 |
| `grade_status` = `provisional` | 1,316 — all of them |
| Rows with a `grade_basis` naming the rule applied | 1,316 — all of them |

**Severity and causality are held in different columns, and that is deliberate.**
`attribution_as_stated` records what the **source** said about cause and is never
written by the grade. Of the 202 positive severity rows, **31** carry
`drug_attributed`; the other **171** carry `not_discussed` — the source reported
an event and did not opine on cause.

I previously presented that 171 as evidence of curator overreach. **It is not.**
Recording that an event was severe, while recording that no causal claim was
made, is the correct behaviour under §E's author-versus-curator separation. The
171 are not unattributed toxicity labels; they are severity observations with
causality explicitly left open.

**Where the column actually propagates — stated precisely, because the first
draft got this wrong.**

- It **does** drive published headline counts: `tier_A_positive` (62),
  `tier_A_null` (560), `grade3_rows` (22), the per-compound `German's analysis`
  sheet, and the narrative's severity prose.
- It **does not** enter the predictive analysis in any way. The modelled outcome
  is `tierB_event_nonprocedure`, derived from `n_affected` counts on tier-B rows
  with the procedure axis excluded. The model's features are delivery route,
  indication, oligo class and backbone chemistry, plus two identity leakage
  probes. `max_grade` is carried into `ml/analysis_set.csv` as a descriptive
  column and is neither a feature nor the outcome. Verified at HEAD.

So a ruling here changes the **published severity figures and how they are
labelled**. It does not change any model result.

**Needed — an interpretation ruling, in three parts.**

1. **What is this column?** A curator-derived provisional severity index, or
   something you would call a toxicity label? The name reads as the latter; the
   construction and the row-level marking are the former.
2. **Is `grade_status = provisional` sufficient marking under §K-5**, or does a
   curator-derived label need something stronger — a renamed column, an explicit
   `curator_derived` flag, or presentation only alongside
   `attribution_as_stated`?
3. **How should severity-without-attribution be presented?** The 171 rows are the
   normal case, not an anomaly. Should published severity counts be reported
   split by attribution (31 source-attributed / 171 attribution-not-discussed) so
   a reader cannot read a severity total as a causal total?

**What I am explicitly not asking for.** Deletion of the 171, or their relabelling
as negatives. Both would destroy sourced severity observations because a separate
question — causality — is unanswered, and that is the conflation this revision
removes.

**Blocks.** Not blocking acquisition or description. It blocks: how the severity
figures may be captioned in the narrative; whether `tier_A_positive` may be
published as a single number; and the §K-5 compliance statement. Nothing has been
changed pending your ruling.

**My own read, offered to save you time and carrying no weight.** Part 1: a
curator-derived provisional severity index. Part 2: `provisional` is probably
necessary but not sufficient, because the column *name* carries more authority
than the marking removes. Part 3: splitting published severity counts by
attribution looks cheap and strictly more informative. I have not acted on any
of this.
