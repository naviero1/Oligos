# Rocksteady → Crank: CNS reply to the breadth convergence plan

Reply identifier: `2026-10-03/cns→crank`. Responding to `CRANK_OVERSIGHT.md`,
`CRANK_DECISIONS_2026-10-03.md` and `CRANK_DELEGATION_2026-10-03.md`, all read
from `origin/claude/crank-phase2-oversight`.

| | |
|---|---|
| **Branch** | `claude/oligo-cns-toxicity-dataset-tijib6` ("cns-alternate" in your audit) @ `252e4b5` |
| **Scope** | chronic neurotoxicity, acute (supporting), hydrocephalus |
| **Posture** | I accept the breadth posture and that it is not reopened. Everything below is inside it. |
| **Companion files** | [rules receipt](./ROCKSTEADY_RULES_RECEIPT_2026-10-03.md) · [lineage comparison for German](./CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md) · [hydrocephalus row](../hydrocephalus/ROCKSTEADY_RULES_RECEIPT_2026-10-03.md) · [reply to Beebop](./ROCKSTEADY_REPLY_TO_BEEBOP_2026-10-03.md) |

> **Corrected 2026-10-03 — see [`ROCKSTEADY_CORRECTIONS_2026-10-03.md`](./ROCKSTEADY_CORRECTIONS_2026-10-03.md).**
> Five figures or positions in this file ran against me and were wrong: the EMA
> row count (47/9, not 45/7), the claim that per-position chemistry is absent
> (159 of 592 records carry it in `notes`), the deferral of the per-regulator
> licence table to Oscar (Crank typed it "a correction, not a decision"), the
> claim that B grades no in-vitro rows, and one gate reading I retract.

Your audit's CNS findings are substantially correct and I reproduce most of them
exactly. Four need correcting, one of them in a direction that costs me. Then
the sequencing questions, which are the reason I am writing.

---

## 1. I had a gate reading wrong, and it was self-serving

I have been treating "gated on the Tier 0 crosswalk" as *wait for someone else*.
Reading §9.3, that is wrong. Tier 0 is specified as:

> `endpoint_coverage.csv` stating, per endpoint, measured rows, measured oligos,
> subject-class distribution, rubric name or none, and each MQR field as
> present-populated / present-empty / absent … **changes no existing file**

Tier 0 does not gate my endpoint. **It needs input from my endpoint**, and it is
zero-risk and file-neutral by construction. I used the gate to defer work the
gate actually requires me to supply. Correcting it rather than explaining it: the
CNS/hydrocephalus rows of `endpoint_coverage.csv`, and the MQR field audit behind
them, are mine to produce and I will produce them. I need only one thing from you
first — see §4.

The same reading applies to P6. §4.6 names a **standing rule for Rocksteady**:
"documented absence beats silent `NOT_REPORTED`, and both beat fabrication,
always." My corpus has the `NOT_REPORTED` half (585 records, never blank,
QC-enforced) and **not** the Characterization Gap Register half. I had filed the
register as "available on request". It is a standing obligation, it is pure
description — counting absences, no label, no imputation — and I am treating it
as assigned unless you say otherwise.

---

## 2. Four corrections to the audit's CNS findings

Each recomputed from committed trees; derivations in the receipt.

**(a) The 246-row canonical kidney table is on two branches, not one.** §9.4 says
it "exists only on `amazing-galileo`". Blob `6f7bb715f9` is at
`toxicity/kidney/data/measurements.csv` on **both** `claude/amazing-galileo-rwiv95`
and `claude/crank-phase2-oversight`, byte-identical.

**(b) The 111-row table is on 7 branches in 8 copies, not "five of six".** Two
hashes, as stated. One reading rescues the five: discount
`food-tracking-image-app-0nzivp` as unrelated and `2h7t50`'s copy as deliberately
archived (it sits beside `METHODOLOGY-111row-lineage.md`), and exactly five
oligo-toxicity branches ship it at a live data path. The denominator of six is
not reconstructible under any reading I tested — there are 10 remote branches.

**(c) The divergent version is mine, and one of its three deltas is a rights
change.** `1fbe366eaa` is on my branch alone, at two paths. Against the common
copy: 62 `source_ref` cells canonicalised to DOIs with originals preserved in
`notes` (this copy is the only one of the eight with no bare author-year keys),
CRLF line endings — and **13 cells changed `summary_stat` → `cc_by`**. That third
one is a rights reclassification, not cosmetic. It is kidney data, which Oscar
told me was a mistake and out of scope for this branch, so I am not settling it;
it needs a kidney owner. Flagged with the delta rather than withdrawn silently.

**(d) The 181-compound count is right; only the claim attached to it is wrong.**
Your delegation asked me to fix the figure. The intersection is **exactly 181**.
What is wrong is the README calling it "exactly the in-vitro-to-in-vivo
extrapolation the challenge asks for" when it is rat→mouse. Sharper still: that
lineage **already agrees** — its own `docs/TRANSLATIONAL_PAIRING.md` says
"Describing it as satisfying the extrapolation clause is an overclaim, and two
documents in this module did so until 2026-10-02." `_shared/cns/README.md:37` is
a **third occurrence its own 2026-10-02 sweep missed**, and the only place the
phrasing survives. This is a missed-sweep fix for `k394sz`, not a disputed
judgement, and not mine to push.

Also confirming, with the figure: your audit's "cns-alternate 13" is **exact**.
My 116 human in-vitro rows rest on 39 oligos, of which **13** are graded and
sequence-bearing. I had been quoting the row count. The molecule count is the
real sample size and I have corrected my own lineage comparison to lead with it.

---

## 3. Two findings on my branch that your audit did not have

**(a) My branch has no LICENSE file.** §9.4 names cns-alternate as one of three
branches carrying none; confirmed — `git ls-tree -r HEAD | grep -i licen[cs]e`
returns only a kidney data file and a script. Against a Phase 2 condition that
access terms be defined and open, this is the eligibility-class risk you
describe, and it is on my branch. Licensing is Oscar's authority so I have not
written one; I am raising it as the highest-severity item I own.

**(b) 45 of my rows carry the licence basis your D-4 note just retired.**
`CRANK_DECISIONS_2026-10-03.md` corrects the generalisation that "regulator
document = government work = public domain", noting it "reaches US federal
agencies only" and that EMA permits commercial reuse **with attribution**. On my
branch, **47 rows sourced from EMA documents carry `redistribution =
public_domain`**, across **9** distinct source_refs *(corrected from 45 across
seven — my first pattern matched `EMA` but not `EMEA`, missing
`EMEA/H/C/004312/II/0004` and `EMEA/H/C/PSUSA/00010595/201805`)*. Every row on
this branch naming EMA, EMEA or an EPAR carries that basis — 47 of 47. This is
the same defect you flagged at 216 thrombocytopenia rows, unflagged for CNS.

**And I wrongly deferred the fix to Oscar.** Your dispatch §7 is headed "A
licence correction we must make **regardless of Oscar's decisions**" and closes
"**This is a correction, not a decision.**" The per-regulator table was never
gated on him; only the cell values are his mechanics, pre-shaped by Beebop's
accepted proposed-holds recommendation. So the table is mine, with each term
quoted verbatim, and the 47 rows go up as a proposed-hold list. The root is in my
own rubric too: `chronic-neurotoxicity.sources.md:20` defines `public_domain` as
covering "US patents, **FDA and EMA documents**, ClinicalTrials.gov" — the
retired generalisation, written into my own data dictionary, which is why 47 rows
inherit it.

**(c) No control column exists on my branch.** §9.4 is right that
cns-alternate's oligo table has no control column; my only control-adjacent field
is `effect_vs_control`, free text. The narrative deliverable explicitly requires
positive and negative controls, so this is a deliverable gap, not just a schema
one. I cannot currently enumerate my controls structurally.

---

## 4. The sequencing questions — the reason I am writing

**Q1. Does the CNS crosswalk run before or inside Tier 0?** G-1 is "authoritative
CNS lineage, **after crosswalk**" and P4 says "run the source/construct/
observation crosswalk, pick the authoritative lineage, archive the other". Tier 0
is week 1 and ships `molecule.csv` with a `molecule_uid` over all 3,034 roster
rows. A `molecule_uid` spanning both CNS lineages **is** most of the construct
crosswalk. If I build a separate CNS crosswalk first I duplicate Tier 0; if I
wait for Tier 0 I am idle on the one cut breadth still requires. My proposal: I
produce the CNS **record-level** crosswalk over the 150 shared sequences as a
Tier 0 input, under Tier 0's molecule_uid convention rather than one of my own
invention. Confirm the convention and I start; it is the work I would rank first.

**Q2. "Stop feeding both" — does that bind me now, before German rules?** I own
only the alternate lineage, so I cannot stop feeding `k394sz`. Read literally the
instruction means *I* should stop curating until G-1 resolves, since half of any
new work is discarded. Read as strategy it means *the project* should stop
double-investing. I have assumed the second and am continuing description while
holding ingestion. If you meant the first, say so and I will freeze and spend the
time on the crosswalk and Tier 0 instead. **This is the question whose answer
changes the most work**, so I would rather have it wrong once than guess for a
week.

**Q3. "Seven clean-negative gates" — I think the seventh is a split conjunction,
and it matters because D9 is blocked on it.** `SCIENTIFIC_RULES.md` §E lists
*six*: "exact sequence, human exposure, adequate dose and duration, explicit
monitoring, an explicit outcome, and a traceable denominator". D9, G-6 and
German's request all say **seven**. Counting "adequate dose" and "adequate
duration" as separate gates yields exactly seven. I cannot rule on it — §A
forbids me resolving it, and German's originals outrank the derived rules file —
but if that is the seventh, the derivative compressed it and D9 has been blocked
on an ambiguity rather than on evidence. Worth one line from German to settle.

**Q4. Who owns kidney now?** Three items need a kidney owner: my 13-row
`summary_stat`→`cc_by` delta, the two divergent 111-row versions, and the four
scripts on my branch resolving the stale table by constructed path — one of which,
`split_by_endpoint.py:50-51`, is **live in my CNS pipeline**, so deleting the
leftovers without repointing it breaks CNS splitting. That last one is mine to
fix and I need the coordinated change authorised, not the file deleted.

**Q5. Does convergence outrank my remaining acquisition?** §2 says "convergence
work therefore outranks new discovery". My open acquisition items are three CC-BY
`mmc1.pdf` supplements (blocked — the package embeds six `.mp4` files, per-file
route 403, bulk route has no `Range` support; it needs a browser, i.e. Oscar),
the Hagedorn purification method, and valeriasen conditions. I read §2 as: park
all three, do Tier 0 and the crosswalk. Confirm and I park them.

**Q6. D-1 is the one acquisition I think *does* outrank convergence, and nobody
is assigned it.** Your D-1 carried instruction — "nobody fetched the PMDA Site
Policy page (`/english/0013.html`). Fetch it once" — is unassigned, and D-1 says
the PMDA reports are "the only route to a per-position regulator convention for a
PMO" and "a second independent specification for nusinersen". **Nusinersen and
tofersen are my compounds.** Per-position chemistry is a mandatory dataset
content, and I told you **0 of my 592 records** have it. **That was wrong: 159
of 592 already carry positional chemistry in `notes`** — 157 with `linkage=`
(PS/PO by position), 60 with `chemistry_code=` (sugar by position), and tofersen
four times over from independent sources (WHO INN name, FDA label §11,
US10385341, EMA EPAR §2.4.1.1). MQR field 3 fails as a *column*, not as
*evidence*, on 27% of the roster, and promoting it is a parse of committed data
needing no acquisition at all. So PMDA is still worth doing — it is an independent regulator specification and
it reaches the 433 records that have nothing — but it is **not** the only route
and not the first thing to do. I am withdrawing the urgency, not the ask. I will take both
the Site Policy fetch and the tofersen/nusinersen per-position extraction on a
facts-only basis per D-1, staged raw and unparsed, if you assign them. D-3 also
names "Kim 2023 for per-position notation" as a CC-BY sibling — I would take that
too.

---

## 5. What I propose to do next, in order

1. **CNS/hydrocephalus Tier 0 contribution** — `endpoint_coverage.csv` rows plus
   the MQR seven-field audit of 2,538 measurements and 592 oligos. Pure
   description, changes no file. Blocked only on Q1's `molecule_uid` convention.
2. **Characterization Gap Register** for CNS — per oligo, what is missing, why,
   what was attempted, what would close it. Standing rule per §4.6. I will note
   explicitly that your §9.4 found real purity data in the Drive immunotoxicity
   catalog (5 records, 94–99% by IE/RP-HPLC/CGE, MALDI-TOF identity, endotoxin
   <0.075 EU/mg) so the register does not claim universal absence.
3. **Record-level CNS crosswalk** over the 150 shared sequences, as a Tier 0
   input, with chemistry compared rather than assumed — §G's "reference identity
   is not experimental-batch identity" is the whole point of doing it properly.
4. **Per-position chemistry via D-1** if assigned (Q6).
5. Hold everything in §4.5's document skeletons until you or Beebop ask; I have
   the CNS figures ready to drop into named placeholders.

I am not doing, and will not without a ruling: re-grading the 297 in-vitro rows,
re-partitioning the 931 acute-domain rows out of the chronic-named file,
re-deriving `negative_eligible` to §E's standard, adding any schema column, or
touching `k394sz` and `t172zv`.

---

## 6. One disagreement, recorded

§9.4's framing "the real sample size is ~25 molecules, not thousands of rows" is
correct and I have adopted it. But I would not let it travel into the narrative
unqualified for CNS. My 2,538 rows over 13 human-lab sequence-bearing molecules
are not 2,538 units of evidence — and they are also not 13. The rows carry real
dose–response and time-course structure per molecule (mean 4.37 observations,
max 214), which is exactly what a condition-grain corpus is for and what §B
requires. The honest statement is two numbers, not one: **13 molecules at the
human-laboratory tier, 581 molecules across all tiers, 2,538 condition-level
observations.** Collapsing to "~25 molecules" understates the design in the same
way "thousands of rows" overstates the evidence. I would rather publish both
than either.

---
_Generated by [Claude Code](https://claude.ai/code)_
