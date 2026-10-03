# Rocksteady: corrections to my own 2026-10-03 filings

Correction record for `2026-10-03/cns`. Issued the same day as the filings it
corrects, before German rules on G-1 and before the checkpoint.

All five corrections run **against** the position I filed. Four were found by an
adversarial sweep I commissioned over the Crank/Beebop directives and then
verified myself from committed trees; one I found while checking an unrelated
claim. The figures I had published are named, the measured values replace them,
and the affected documents are patched in the same commit.

| # | What I published | Measured truth | Where |
|---|---|---|---|
| C-1 | "B grades **0** in-vitro rows, so B is §E-compliant where A is not" | B grades **23 of its 34 human** in-vitro rows; the 0 is true only of its 1,825 animal rows | comparison §4 — patched |
| C-2 | §3 "the decisive difference, and it favours A", built on 13 graded molecules | **all 13 are graded only on in-vitro rows**, so a §E withdrawal takes A's human-lab count 13 → **0** | comparison §3 — dependency now published |
| C-3 | "**0 of my 592 records** have per-position chemistry"; "PMDA is the **only identified route**" | **159 of 592** already carry positional chemistry in `notes`. It is a parse, not an acquisition | §3 below |
| C-4 | "45 rows across seven distinct EMA source_refs" | **47 rows across 9** distinct source_refs | §4 below |
| C-5 | "Changing the value is a rights reclassification and **therefore Oscar's**" | Crank typed the licence table "**a correction, not a decision**" — I wrongly parked it | §4 below |

Plus one retraction of reasoning rather than of a figure, in §5.

---

## 1. C-1 — I was wrong about B, in B's favour

I wrote that B leaves its in-vitro rows ungraded and concluded "B is §E-compliant
on exactly the point where A is not." Measured on B's committed tree: B grades
**23 of its 34 human in-vitro rows** (19 at grade 0, 4 at grade 2, 9 of 13
oligos, `grade_status = provisional`). Only its 1,825 *animal* in-vitro rows are
ungraded.

The conclusion survives on a better basis, and the better basis is the one §E
turns on. B's 23 grades each name the author statement they rest on —
`grade_basis` reads "authors state the compound was non-toxic in this system"
(19) and "authors state a significant toxicity or viability loss in this system"
(4). §E allows precisely that: binary calls are curator-derived "**unless the
source explicitly defines them**." B's are source-defined; **A's 297 are
curator-derived against a rubric with no in-vitro branch.**

So the difference is not that B declines to grade in-vitro rows. It is that B
records what each grade rests on and A has no field in which to record it.

## 2. C-2 — A's whole claim to the priority lane sits inside the rows I reported as defective

All 13 of A's qualified human-laboratory molecules (`CNS546`, `CNS549`, `CNS564`,
`CNS565`, `CNS566`, `CNS567`, `CNS570`, `CNS572`, `CNS573`, `CNS574`, `CNS577`,
`CNS581`, `CNS583`) are graded **only** on in-vitro rows — verified per molecule,
every one has `study_type` ∈ {`in_vitro`} exclusively. All 116 `human_laboratory`
rows are `in_vitro`.

The Challenge's declared priority is human in-vitro evidence. A's entire claim to
that lane therefore sits inside the 297 rows I myself reported as a §E
violation. **If German withdraws those grades, A's human-laboratory
qualified-molecule count is 13 → 0 and the section I headed "the decisive
difference, and it favours A" is void.** If German adopts §E's own remedy and
relabels them experimental response severity, the molecules survive but not on
the clinical scale.

I filed a comparison arguing A's advantage on a dimension my own §4 could void,
and did not state the consequence. It is now stated in the document German will
read, with the direction of the dependency: **the §E ruling logically precedes
G-1.**

## 3. C-3 — per-position chemistry is not absent; I had not looked in the right field

This is the correction that changes what I owe, and it reverses an escalation I
made to Crank yesterday — I asked to be assigned PMDA acquisition on the grounds
that it was "the only identified route to a mandatory field for my endpoint" and
that "0 of my 592 records" carry per-position chemistry.

**159 of 592 oligo records (26.9%) already carry positional chemistry, in the
`notes` field, sourced and cited:**

| encoding found in `notes` | records |
|---|---:|
| `linkage=` — phosphorothioate/phosphodiester **by position** (e.g. `sososssssssssssosos`) | **157** |
| `chemistry_code=` — sugar **by position** (e.g. `eeeeeddddddddddeeeee`, e=2′-MOE, d=DNA, k=cEt) | **60** |
| full gapmer notation (`mCes Aeo Ges Geo Aes Tds …`) | 1 (`CNS013`, tofersen) |
| **union** | **159** |

They are overwhelmingly the ISIS/Ionis series from patent sequence listings
(`CNS039`–`CNS272`) plus tofersen. Tofersen alone carries the positional data
**four times over from independent sources**: the WHO INN systematic name, the
FDA QALSODY label §11 DESCRIPTION, US10385341's notation, and the EMA EPAR
`EMA/276404/2024` §2.4.1.1 transcription.

So MQR field 3 fails as a **column**, not as **evidence**, on 27% of the roster.
Promoting it needs a parse of data already committed — no acquisition, no new
source, no network. Creating the columns is a schema act and therefore Oscar's;
measuring and reporting the coverage was always mine, and I should have done it
before escalating.

**PMDA is still worth doing** — it is an independent regulator specification for
nusinersen and it reaches the 433 records that have nothing — but it is no longer
the *only* route and no longer the first thing to do. The first thing is the
parse. I am withdrawing the urgency I attached to the PMDA ask, not the ask.

I also confirm I have ingested **none** of the three purity figures the dispatch
forbids: `purity_pct` is `NOT_REPORTED` on 585 records and `NOT_APPLICABLE` on 7,
with no numeric value anywhere, and nusinersen `CNS012` is `NOT_REPORTED` — so
the impurity-enriched toxicology-batch figure has not entered my data.

## 4. C-4 and C-5 — the EMA basis: a bigger number, and work I wrongly deferred

**The count.** 47 rows, not 45, across **9** distinct `source_ref` strings, not
seven. My first pass used a pattern that matched `EMA` but not `EMEA`, missing
`EMEA/H/C/004312/II/0004` and `EMEA/H/C/PSUSA/00010595/201805`. Every row on my
branch whose `source_ref` names EMA, EMEA or an EPAR carries
`redistribution = public_domain` — 47 of 47, none on any other basis.

A two-row understatement inside the one escalation that invokes the
denominator-and-provenance discipline is the exact compression failure the
oversight tracker charges elsewhere. Corrected upward, by me, before anyone
asked.

**The root is in my own documentation, not only in the cells.**
`toxicity/chronic-neurotoxicity.sources.md:20` defines the basis as: "`public_domain`
| US patents, **FDA and EMA documents**, ClinicalTrials.gov. Values may be
reproduced without restriction." `hydrocephalus.sources.md` carries the same
line. That sentence *is* the retired generalisation, written into my rubric, and
it is why 47 rows inherit it.

**C-5, the deferral.** I wrote that changing this is "a rights reclassification
and therefore Oscar's". Checked against the primary text, that is wrong about
scope. `CRANK_DISPATCH_SOURCES_2026-10-03.md` §7 is headed "A licence correction
we must make **regardless of Oscar's decisions**" and closes "Build a
per-regulator licence table with each term quoted verbatim, and stop using one
basis string for all of them. **This is a correction, not a decision.**"

So the **table** was never gated on Oscar; only the cell values are his
mechanics, and even those are pre-shaped by Beebop's accepted recommendation of
proposed holds rather than automatic withdrawals. Holding "the rows and the
evidence are ready" was not delivery. The per-regulator licence table with
verbatim terms, and the 47 rows as a proposed-hold list with reasons, are mine
and I am building them. I have changed no cell and withdrawn nothing.

## 5. Retraction of reasoning: the merged-view gate

My receipt argued: "Regenerating it is a build step that writes a data file,
which I read as ingestion rather than description, so I have not run it."

**I retract that reasoning.** The outcome was right — Oscar authorized deleting
the view and its generator, and that is done — but the ground I published was
not. A materialised join of two committed tables introduces no fact and is not
ingestion in the sense the directive uses, where ingestion sits beside
acquisition, promotion and release of **source** material. The honest grounds for
not regenerating were the two I established later: the view carried zero
independent information, and its generator hardcoded column lists whose comments
asserted completeness and had silently stopped being true.

This is the second gate reading I have had to retract today, after Tier 0, and
it is the same pattern: a gate invoked where it did not apply, in the direction
that deferred my own work. I am recording it rather than leaving it to be found,
because published reasoning gets cited as precedent even when the outcome was
correct. For the next occurrence: a harmonized derived view is **Tier 1 adapter
output**, which §9.3 requires to reproduce its endpoint's published row count
before acceptance — not an ingestion question.

## 6. Two things with no owner, raised rather than assumed

Stated under the delegation's own rule: "Every open item has exactly one owner.
No orphans. If you believe something is yours that is not listed under you, say
so rather than assuming."

**The hydrocephalus canonicalization has no owner and no gate row.** The
oversight tracker records that hydrocephalus "exists **three** times", names it
among the three reasons the harmonized schema is unachievable, demands "one
canonical branch per endpoint", and counts hydrocephalus in the achievable
five-endpoint register. But G-1, D3 and P4 are all scoped to the *chronic* CNS
lineages; none names hydrocephalus. So one of the five register slots depends on
a decision with no owner, no gate and no date. **And the multiplicity is four,
not three**: `toxicity/hydrocephalus.*.csv` on tijib6 (145 rows),
`toxicity/hydrocephalus/data/` on t172zv (1,342) and on k394sz (12), and
`hydrocephalus/data/` on oligo-reorganize-toxicity-2h7t50 (147). I am not
claiming the decision — I cannot, it spans three branches I do not own — but it
needs assigning, and whether it is scientific or mechanical is unstated.

**D3's owner is contradicted inside Crank's own documents.** The oversight
tracker's open-decisions table lists "Authoritative CNS lineage after crosswalk"
against **Oscar**; §3, §9 and G-1 in the decisions log put the same question with
**German**, and §J makes scientific adjudication German's. I resolved it silently
by addressing my comparison to German and never said that I had chosen. That was
an open matter treated as decided. One sentence settles it, and if I chose wrong
the comparison is sitting in the wrong queue while Tier 1 stays blocked on it.

For completeness, one more I can only disclaim: **no TGA retrieval has been
attempted or logged on my branch.** The decisions log time-boxes TGA to one
further egress attempt, then stop. Zero effort exists here, so the time-box is
unbreached rather than discharged — if an attempt was made it was made elsewhere.
TGA is not among my acquisition items and I am not claiming it.

---

## 7. What none of this changes

No label assigned, changed or withdrawn — including the 297 in-vitro grades,
which stay exactly as they are pending German. No imputation, no manufactured
negative, no source conflict resolved. No schema column added, including the
per-position columns §3 shows I could now populate from committed data. No
`redistribution` cell changed. Nothing merged across the 150 candidate links.
Nothing written to any branch but my own. `cns_measurements.csv` 2,538 × 33 and
`cns_oligos.csv` 592 × 21 are byte-identical to their state before these
corrections; `qc_cns.py` 0 errors.

---
_Generated by [Claude Code](https://claude.ai/code)_
