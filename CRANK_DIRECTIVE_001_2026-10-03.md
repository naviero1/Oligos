# Crank → Beebop — Directive 001: introduction, and making breadth converge

Date: 2026-10-03. Issued directly by Crank at Oscar's instruction.
Standing context: `CRANK_OVERSIGHT.md`, beside this file.

---

## 0. Introducing myself

Beebop — we have not worked together before, so let me say plainly who I am, what I am for,
and what I will and will not do to you.

**Who I am.** I am Crank. I sit above you and above the Rocksteady sessions. You synthesize and
analyze across the toxicologies and task the nine Rocksteady sessions; I supervise the whole
thing and report directly to Oscar. You have the deepest view of *what the evidence is*. My job
is the view you are not positioned to hold: **whether what we are building actually adds up to
a winning Phase 2 submission, by the date it is due.**

**What that means in practice.** I read the challenge's end product — the four deliverables, the
mandatory per-oligo dataset contents, the in-vitro-human priority, the open-licensing condition
— and the work-plan calendar, and I hold your rounds against them. When the evidence work and
the submission diverge, that is mine to catch and correct. I will re-prioritize across
endpoints, and I will tell you when something you are treating as important is not on the
critical path to a deliverable, or when something you are treating as routine is.

**How I will work with you.**

- **You keep managing Rocksteady.** I will not route around you. My instructions come to you,
  and you decide how they reach the nine sessions and in what form — you know those sessions and
  their state better than I do.
- **One exception, declared up front:** if I judge that your reasoning on something material is
  unsound, I will go directly to a Rocksteady session. If I ever do that, **I will say so to you
  and to Oscar, in the open, with my reasons.** I will not do it silently and I will not do it
  to save time. You should expect to be able to argue back.
- **I expect you to push back on me.** Everything below is a judgment about priority and
  sequence, made from above the detail. You hold detail I do not. If a pillar here is wrong, or
  there is a seventh thing that matters more, say so with evidence and I will take it to Oscar
  and change my direction. That is the same standard you set for Rocksteady in your 09-30
  handoff, and I hold myself to it.
- **Flag early, do not wait for a round.** If something is going to break a deliverable, I want
  it the day you see it, not in the next index.

**What I will not do.** I do not change data, labels, schema or models — the same boundary you
operate under. German holds scientific labels, qualification and freeze authority. Oscar holds
schema, engineering and release authority. I set priority and sequence; I do not set science.
Nothing in this directive authorizes a dataset edit, label change, merge, training run or
release.

**One thing I want on the record before I start giving instructions.** Your 09-30, 10-01 and
10-02 rounds did the hard and unglamorous thing: they established what we actually have rather
than what we would like to claim. The counting discipline — human trials separate from human
laboratory separate from animal, trials counted once across registry and papers and labels, no
summed denominators, no fabricated negatives, "work requested is not work completed" stated
outright — is correct, and it happens to match the challenge's own stated priority exactly.
Keep every bit of it. What follows changes *what we point that discipline at*, not the
discipline.

---

## 1. Why this directive exists

Two things now change the shape of the work.

**First, Oscar has set the posture: maximize breadth.** All eight toxicities of interest are
driven toward qualification in parallel. Nothing is demoted to appendix on scope grounds. I had
recommended consolidating to a defensible core; Oscar chose breadth, and that is settled — I am
not reopening it, and neither should you.

**Second, the calendar.** `Phase 2 Work-Plan.xlsx` gives **November to the four deliverables and
December to buffer.** We are four weeks out.

Together these move the binding constraint. It is no longer discovery — it is **convergence**.
Eight parallel endpoint streams become one submission only if they share one schema, one
counting convention, one missingness convention and one release discipline. Without those,
breadth produces eight incompatible tables and no submission at all.

**So: from this round, convergence work outranks new source discovery.** That is the single
instruction behind all six pillars below. If you take nothing else from this directive, take
that sentence.

---

## 2. The six pillars

### P1 — Blocking: harmonize the schema

Nothing else converges until this lands, and every day it stays open, eight streams accrue
rework.

The obstacle is concrete and it is already in your own register: the kidney model is
kidney-shaped by construction. `is_kidney_specific` is TRUE on 111 of 111 legacy rows and
therefore carries no information; `nephrotox_grade` has a rubric written entirely in renal
terms. A seven-endpoint register **cannot** be produced by re-slicing the kidney tables — which
is exactly why seven dossiers report zero rows rather than a subset. That is a data-model fact,
not a backlog.

Assemble the cross-branch column inventory across all six branches and bring Oscar a harmonized
model: shared core entities (oligo, construct and chemistry, source, study/experiment,
observation, provenance), **one** shared evidence-class vocabulary, and **per-endpoint graded
outcome columns, each carrying its own written rubric**. Do not try to generalize the renal
rubric across endpoints — propose per-endpoint rubrics inside a shared frame. Oscar owns the
decision; it is his assigned role. Bring him a proposal, not a menu of options.

### P2 — Blocking: publish the Minimum Qualified Record

Breadth cannot mean perfection on eight fronts, so the floor must be explicit, published, and
applied identically everywhere. Propose it this round. My starting draft — improve it:

A row ships only if it carries (1) a resolvable oligo identifier; (2) sequence present **or**
explicitly flagged absent with a reason; (3) modification positions mapped **or** explicitly
flagged absent with a reason; (4) purity/characterization value **or** a documented recovery
attempt plus an explicit missingness reason; (5) an evidence class from the shared vocabulary;
(6) provenance to a registered `source_id` with a locator; (7) an endpoint outcome plus the
rubric it was graded under.

Everything below the floor goes to a labelled staging tier — never in headline counts, never in
the released dataset unlabelled. Carry forward your own warning verbatim: reference identity is
not experimental-batch identity, and shared-sequence grouping for leakage prevention must not
merge chemically distinct administered constructs.

### P3 — Critical path: the three thin endpoints get first call

Hepatic, complement and immunotoxicity are the only endpoints that can make breadth fail
outright. Bounded, named targets — not open research — and a shorter reporting cadence than the
rest.

- **Hepatic** (0 dedicated rows): drive the nine human-hepatocyte constructs to qualified rows.
  Stage Burdick's 80-construct panel as clearly-labelled animal support. It is not human
  progress and must never be presented as such.
- **Complement** (0 dedicated rows): human whole-blood / serum complement assay files. Pair the
  Sewing raw-file acquisition with thrombocytopenia so that effort is paid once, not twice.
- **Immunotoxicity** (142 catalog records, but **1 identifier literally joins** the 33
  observations, and that result is qualitative): fix compound→observation linkage **before**
  acquiring anything further. A catalog that does not join yields approximately zero trainable
  rows — this is the highest-leverage single fix on the board. Then target raw cytokine and
  receptor outcomes with human donor and assay context for constructs already held or approved.

### P4 — Cut the duplicate CNS lineage

Two parallel nervous-system lineages are duplication, not breadth, and this is the one place
breadth still requires a cut. Run the source/construct/observation crosswalk, recommend the
authoritative lineage to Oscar, archive the other as a frozen lineage. **Stop feeding both
now.** Human-laboratory compound coverage already differs between them (13 original vs 39
alternate identifiers) and no branch totals may be added.

Acute neurotoxicity stays a supporting module — the brief explicitly makes it lower priority. It
does not receive breadth budget.

### P5 — Start the three documents now, in parallel with the data

The highest-leverage deadline move available to us, and the one most likely to be skipped
because it feels premature. Narrative, methodology and PADP get drafted **now**, against the
frozen schema, with named numeric placeholders — so November is number-landing and editing
rather than writing. **If those documents start in November they will not finish in November.**

Produce a placeholder-tagged skeleton for each so every figure we later generate has a named
slot waiting for it. Leads per the roles plan: Gustavo narrative + PADP, German methodology,
Oscar schema/dictionary and the optional notebook. The narrative skeleton must already reserve
slots for every required element: positive and negative controls, predictor-variable measurement
and distribution, the gap in publicly available data, and the route to a predictive model.

### P6 — Make documented missingness the differentiator

Purity coverage is at or near zero on every endpoint measured so far — 0/65 kidney, 0/34
thrombocytopenia, 0/38 coagulopathy, 0/21 original nervous-system, 0/41 hydrocephalus — against
a brief that names purity and characterization as **mandatory** dataset contents. We will not
close that gap completely in four weeks across eight endpoints. So we do the honest thing and
make it an asset rather than a wound.

Build a **Characterization Gap Register**: per oligo — what is missing, why, what was attempted,
what would close it. It satisfies the narrative's required discussion of the gap in publicly
available data, it protects every other claim we make from reading as inflated, and it is a
genuine contribution in its own right. Standing rule for every Rocksteady session, no
exceptions: **documented absence beats silent `NOT_REPORTED`, and both beat fabrication.**

---

## 3. Governance carried forward

- **Release identifiers.** One canonical branch per endpoint; every accepted dataset, source
  inventory, figure and document bound to a frozen release tag. "Different branches hold
  different versions" is a live defect against the dataset deliverable, not a cosmetic one.
- **Counting discipline unchanged** — keep it exactly as you have it, and extend it into the
  shared schema so all eight endpoints express evidence class the same way.
- **Qualification bar.** Under breadth the bar is the MQR floor, not completeness. State that
  plainly in your reporting rather than letting a reader infer a higher bar than we met.

## 4. What I want back from you

1. The harmonized schema proposal for Oscar (P1) and the MQR draft for Oscar and German (P2).
   These two are blocking and they come first.
2. A **Phase 2 Readiness Scorecard**, one page per endpoint: coverage against the four
   deliverables, against the four mandatory per-oligo dataset fields, and the human in-vitro row
   fraction. Under a breadth posture this is a *tracking* instrument, not a tiering one — it
   tells us where to send help, not what to cut.
3. The CNS lineage recommendation with the crosswalk behind it (P4).
4. The three placeholder-tagged document skeletons (P5).
5. **Your disagreements**, with evidence.

Flag immediately, outside the round cadence, if: an endpoint cannot meet the MQR floor at all;
schema harmonization proves infeasible for a specific endpoint; or anything here conflicts with
German's scientific authority. In that last case German wins and I want to hear about it.

---

*Crank. Reporting to Oscar. Directive 001.*
