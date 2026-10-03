# Crank → Beebop — Directive 001: make breadth converge

Date: 2026-10-03. Issued by Crank (supervisory layer) at Oscar's instruction. Relayed by Oscar.
Standing context: `CRANK_OVERSIGHT.md`.

**Authorization boundary unchanged.** This directive sets priority and sequence. It authorizes
no dataset edit, label change, merge, training run or release. German retains scientific
labels, qualification and freeze authority; Oscar retains schema, engineering and release
authority. Research-only boundaries from the 2026-10-01 and 2026-10-02 rounds remain in force
until Oscar authorizes implementation.

---

## Why this directive exists

Beebop, your 09-30 / 10-01 / 10-02 rounds did the hard and correct thing: they established what
we actually have rather than what we claim. The counting discipline — human trials separate
from human laboratory separate from animal, trials counted once, no summed denominators, no
fabricated negatives — is right, and it matches the challenge's own stated priority. Keep it.

Two things now change the shape of the work.

**First, Oscar has set the posture: maximize breadth.** All eight toxicities of interest are
driven toward qualification in parallel. Nothing is demoted to appendix on scope grounds. I had
recommended consolidating to a defensible core; Oscar chose breadth, and that is settled.

**Second, the calendar.** The work plan gives November to the four deliverables and December to
buffer. We are four weeks out.

Together these move the binding constraint. It is no longer discovery — it is **convergence**.
Eight parallel endpoint streams become one submission only if they share one schema, one
counting convention, one missingness convention and one release discipline. Without those,
breadth produces eight incompatible tables and no submission. **From this round, convergence
work outranks new source discovery.** That is the single instruction behind everything below.

---

## P1 — Blocking: harmonize the schema

Nothing else converges until this lands, and every day it is open, eight streams accrue rework.

The obstacle is concrete: the kidney model is kidney-shaped by construction. `is_kidney_specific`
is TRUE on 111 of 111 legacy rows and carries no information; `nephrotox_grade` has a rubric
written entirely in renal terms. A seven-endpoint register therefore **cannot** be produced by
re-slicing the kidney tables, which is exactly why seven dossiers report zero rows rather than a
subset.

Your task: assemble the cross-branch column inventory across all six branches and propose a
harmonized model to Oscar — shared core entities (oligo, construct and chemistry, source,
study/experiment, observation, provenance), **one** shared evidence-class vocabulary, and a
**per-endpoint graded outcome column that each carry their own written rubric**. Do not attempt
to generalize the renal rubric across endpoints; propose per-endpoint rubrics inside a shared
frame. Oscar owns the decision — this is his assigned role. Bring him a proposal, not options.

## P2 — Blocking: publish the Minimum Qualified Record

Breadth cannot mean perfection on eight fronts, so the floor must be explicit, published, and
applied identically everywhere. Propose it this round. My starting draft — improve it:

A row ships only if it carries (1) a resolvable oligo identifier; (2) sequence present **or**
explicitly flagged absent with a reason; (3) modification positions mapped **or** explicitly
flagged absent with a reason; (4) purity/characterization value **or** a documented recovery
attempt plus an explicit missingness reason; (5) an evidence class from the shared vocabulary;
(6) provenance to a registered `source_id` with a locator; (7) an endpoint outcome plus the
rubric it was graded under.

Everything below the floor goes to a labelled staging tier — never in headline counts, never in
the released dataset unlabelled. Carry forward your own warning: reference identity is not
experimental-batch identity, and shared-sequence grouping for leakage prevention must not merge
chemically distinct administered constructs.

## P3 — Critical path: the three thin endpoints get first call

Hepatic, complement and immunotoxicity are the only endpoints that can make breadth fail
outright. Give them bounded, named targets — not open research — and a shorter reporting
cadence than the rest.

- **Hepatic** (0 dedicated rows): drive the nine human-hepatocyte constructs to qualified rows.
  Stage Burdick's 80-construct panel as clearly-labelled animal support. It is not human
  progress and must never be presented as such.
- **Complement** (0 dedicated rows): human whole-blood / serum complement assay files. Pair the
  Sewing raw-file acquisition with thrombocytopenia so the effort is paid once, not twice.
- **Immunotoxicity** (142 catalog records, **1 identifier literally joins** the 33 observations,
  and that result is qualitative): fix compound→observation linkage **before** acquiring
  anything further. A catalog that does not join yields approximately zero trainable rows. Then
  target raw cytokine/receptor outcomes with human donor and assay context for constructs
  already held or approved.

## P4 — Cut the duplicate CNS lineage

Two parallel nervous-system lineages are duplication, not breadth, and this is the one place
breadth still requires a cut. Run the source/construct/observation crosswalk, recommend the
authoritative lineage to Oscar, and archive the other as a frozen lineage. Stop feeding both
now. Human-laboratory compound coverage already differs (13 original vs 39 alternate
identifiers) and **no branch totals may be added**.

Acute neurotoxicity stays a supporting module: the brief explicitly makes it lower priority. It
does not receive breadth budget.

## P5 — Start the three documents now, in parallel with the data

This is the highest-leverage deadline move available to us, and it is the one most likely to be
skipped. Narrative, methodology and PADP get drafted **now**, against the frozen schema, with
named numeric placeholders — so that November is number-landing and editing, not writing. If
those documents start in November they will not finish in November.

Produce a placeholder-tagged skeleton for each, so every figure we later generate has a named
slot waiting for it. Leads per the roles plan: Gustavo narrative + PADP, German methodology,
Oscar schema/dictionary and the optional notebook. The narrative skeleton must already reserve
slots for the required elements: positive and negative controls, predictor-variable measurement
and distribution, the public-data gap, and the route to a predictive model.

## P6 — Make documented missingness the differentiator

Purity coverage is at or near zero on every endpoint we have measured — 0/65 kidney, 0/34
thrombocytopenia, 0/38 coagulopathy, 0/21 original nervous-system, 0/41 hydrocephalus — against
a brief that names purity and characterization as mandatory dataset contents. We will not close
that gap completely in four weeks on eight endpoints. So we do the honest thing and make it an
asset.

Build a **Characterization Gap Register**: per oligo — what is missing, why, what was attempted,
what would close it. It satisfies the narrative's required discussion of the gap in publicly
available data, it protects every other claim we make from looking inflated, and it is a real
contribution on its own. Standing rule for every Rocksteady session, no exceptions:
**documented absence beats silent `NOT_REPORTED`, and both beat fabrication.**

---

## Governance to carry forward

- **Release identifiers.** One canonical branch per endpoint; every accepted dataset, source
  inventory, figure and document bound to a frozen release tag. "Different branches hold
  different versions" is a live defect against the dataset deliverable, not a cosmetic one.
- **Counting discipline unchanged** — keep it exactly as you have it, and extend it into the
  shared schema so all eight endpoints express evidence class the same way.
- **Qualification bar.** Under breadth the bar is the MQR floor, not completeness. Say so
  plainly in your reporting rather than letting readers infer a higher bar than we met.

## What I want back from you

1. The harmonized schema proposal for Oscar (P1) and the MQR draft for Oscar and German (P2).
2. A **Phase 2 Readiness Scorecard**, one page per endpoint: coverage against the four
   deliverables, against the four mandatory per-oligo dataset fields, and the human in-vitro row
   fraction. Under a breadth posture this is a *tracking* instrument, not a tiering one — it
   tells us where to send help, not what to cut.
3. The CNS lineage recommendation with the crosswalk behind it (P4).
4. The three placeholder-tagged document skeletons (P5).
5. Your disagreements. If any pillar above is wrong, or if you see a seventh thing that matters
   more, say so with evidence and I will take it to Oscar. These are instructions, not a
   substitute for your judgment — the same standard you set for Rocksteady.

Flag immediately, do not wait for a round, if: an endpoint cannot meet the MQR floor at all;
the schema harmonization turns out to be infeasible for a specific endpoint; or any instruction
here conflicts with German's scientific authority.
