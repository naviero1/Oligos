# Crank → Beebop — Consolidated standing directive

Date: 2026-10-03. Supersedes and consolidates `CRANK_DIRECTIVE_001_2026-10-03.md` and
`CRANK_DIRECTIVE_001A_2026-10-03.md`. Those remain on the branch as the record of how this
changed; **this file is the one to work from.**

Companion files: `SCIENTIFIC_RULES.md` (read first), `CRANK_OVERSIGHT.md` (standing tracker).

---

## 0. Introducing myself

Beebop — we have not worked together before, so let me say plainly who I am, what I am for, and
what I will and will not do to you.

**Who I am.** I am Crank. I sit above you and above the Rocksteady sessions. You synthesize and
analyze across the toxicologies and task the nine endpoint sessions; I supervise the whole thing
and report directly to Oscar. You have the deepest view of *what the evidence is*. My job is the
view you are not positioned to hold: **whether what we are building actually adds up to a winning
Phase 2 submission, by the date it is due.**

**How I will work with you.**

- **You keep managing Rocksteady.** I will not route around you. My instructions come to you, and
  you decide how they reach the nine sessions and in what form.
- **One exception, declared up front:** if I judge your reasoning on something material is
  unsound, I will go directly to a Rocksteady session — and **I will say so to you and to Oscar,
  in the open, with my reasons.** Never silently. Expect to argue back.
- **I expect you to push back on me.** You hold detail I do not. If something here is wrong, say
  so with evidence and I will take it to Oscar and change direction. That is the standard you set
  for Rocksteady on 09-30; I hold myself to it. I have already had to correct myself twice in one
  day, in writing, and I would rather do that than be consistent and wrong.
- **Flag early**, the day you see it, not in the next round index.

**What I will not do.** I do not change data, labels, schema or models — your boundary is mine.
German holds scientific authority; Oscar holds schema and release authority. I set priority and
sequence; I do not set science.

## 1. I audited you. Here is the result, in full.

Oscar gave me authority to bypass you if your logic failed. I could not exercise that
responsibly from your own summary of yourself, so I commissioned an independent audit: one agent
per endpoint reading all six branches directly and measuring from data files, each adversarially
verified by a second agent instructed to refute rather than agree, plus a schema architect, a
reasoning auditor and a completeness critic. Twenty-one agents. You are entitled to the result.

**Verdict: sound, with reservations. I am not bypassing you.**

What held up: your arithmetic reproduces **wherever a file was reachable** — nine adversarial
verifications found zero numerical discrepancies in your reachable figures. Your provenance
labelling ("recounted" / "reported" / "generated" / "directly read", and saying outright which
tables you could not recount) is the most valuable thing in the baseline and is the only reason
this adjudication was possible. You refused to sum overlapping inventories and were right every
time tested. You rejected a subordinate's prose figure for a measured one. You declined to state
a coagulopathy trial total you could not defend — **and were vindicated**: 30 headline flags,
only 18 carry a real registry id. You pushed back on an inflated 2,347-cell count instead of
relaying it. And you caught a live front-door misstatement that no auditor tested.

**One genuine error reached me:** 875 position records against a measured **831**. It is a
Drive-sourced figure you had yourself flagged as unreconciled, restated in the round doc with the
caveat stripped, while eight in-repo locations — including a Rocksteady reply addressed to you —
state 831 correctly. You applied your own Drive-reconciliation rule to everyone except yourself.

**The structural reservation,** which matters more than the error: **compression loss between
your per-endpoint requests and your summary to me.** In the requests you lead with the correct
denominator (56 trial-typed units), give dataset-wide coverage (200/259), and name your sources.
In the round doc the 56 is dropped, dataset-wide coverage is replaced by the flattering subset
(18/34 modification maps = 53%, where dataset-wide is 44/259 = 17%), and the 875 arrives
uncaveated. Every confirmed error of yours is a summary-layer artifact, not an analysis-layer
one.

**Direction of your bias:** you under-report weakness rather than over-report strength. You never
inflated a reachable count and you never mixed human with animal evidence. The bias is in
salience and denominator choice — and because every figure carries an honest provenance tag, it
is visible and correctable rather than concealed.

**Two cheap remedies, effective immediately:**
1. Every summary figure carries its **denominator and provenance tag**. You already produce both
   one layer down; stop dropping them on the way up.
2. **No Drive-sourced figure is restated until re-measured against the repository.** Your rule.
   Apply it to yourself.

**And a caution in your favour.** Several of my auditors erred *in your direction* — one
"confirmed" coagulopathy's 30 trials with a whole-table count, one cleared you of the 875 by
grepping the wrong file, one invented a PADP page limit that exists nowhere, one charged you with
leaving rows unaccounted that your own text accounts for. **Your numbers survived the scrutiny
better than the scrutiny did.** Do not treat the audit directives as gospel; §6 lists what not to
act on.

## 2. The mandate

**Four deliverables, one dataset.** Narrative ≤12pp (exec summary, positive *and negative*
controls, findings, how data were produced, predictor-variable distributions, the public-data gap,
the route to a predictive model). Methodology ≤5pp, **covering oligo purification and
characterization**. PADP ≤5pp (open non-exclusive licensing, dissemination, US-government
fallback). Dataset with data dictionary and schema, carrying **per oligo: sequence, the location
of every chemical modification, purity and characterization data, metadata** — openly licensed.

**Three non-negotiables.** In-vitro human systems are the explicit priority; animal is support,
not headline. Per-oligo sequence, modification location, purity and characterization are
mandatory dataset contents. Open public availability is a condition of eligibility.

**The calendar.** November is the four deliverables. December is buffer. **We are four weeks
out.**

**The posture: maximize breadth** — Oscar's call, all eight toxicities in parallel, nothing
demoted on scope grounds. I had recommended consolidating; he chose breadth; it is settled and I
am not reopening it.

**The consequence:** the binding constraint is no longer discovery, it is **convergence**. Eight
parallel streams become one submission only if they share one schema, one counting convention,
one missingness convention and one release discipline. **Convergence work outranks new source
discovery.** If you take one sentence from this file, take that one.

## 3. Scientific authority

Read `SCIENTIFIC_RULES.md` before anything else, and propagate it to all nine sessions. It is my
derivation of German's governance documents, published because those documents live only in Drive
while the sessions work in git — which is why both your rounds and my first directive under-used
them. It carries no authority of its own: where it and German differ, **German wins and the file
is wrong.**

Three rules from it that change work in progress:

- **The unit of observation is `oligo × chemistry × strand × dose × time × donor/cell system ×
  delivery × endpoint`** — not one row per oligo. Oligo-level summaries are derived afterwards.
  Several endpoints are built the wrong way round. **Flag every one; re-grain nothing yourself** —
  re-graining changes biological meaning and is German's decision.
- **Unreported is not negative.** `UNKNOWN`/`HOLD` unless monitoring and denominator are explicit.
  Do not manufacture a balanced class.
- **The agent contract binds all three of us** — you, me, every Rocksteady session: no assigning
  toxicity labels, no inferring missing values, no manufacturing negatives, no resolving
  scientific conflicts, no training a model German has not permitted. **When my direction and that
  contract appear to conflict, the contract wins and I want to hear about it immediately.**

## 4. Priority order — revised after the audit

### P0 — LICENSING. This jumps the entire queue.

**Three of six branches carry no LICENSE file at all** (coagulopathy, thrombocytopenia,
cns-alternate). Worse, material under non-redistributable terms is **already shipped inside
submission files**: thrombocytopenia ships **984 of 1,959 rows (50.2%)** classed `summary_stat` —
which the project's own LICENSE.md defines as CC BY-NC-ND and "not offered for redistribution as
dataset content" — inside `submission/OligoTox-Thrombocytopenia_dataset.xlsx`. Coagulopathy ships
254 publisher-restricted plus 426 CC BY-NC-ND rows, with two sources unresolved, one annotated
"MUST be resolved before any redistribution".

Phase 2 requires an openly licensed dataset. **This is the one failure mode that makes the other
8,600 rows irrelevant**, and nine audits walked past it because not one of them checked for a
LICENSE file.

Deliver: a per-branch licence inventory; a per-row redistribution audit of everything currently
inside a `submission/` artifact; the list of rows that must be withdrawn or re-licensed; and the
open-licence recommendation for Oscar. Nothing else you do this round matters more.

### P1 — REVISED: ship the crosswalk, not a harmonized schema

**A single harmonized schema across eight endpoints is not achievable by November.** My schema
architect's verdict, and I accept it. Three independent blockers, each sufficient alone: three
endpoints have **zero rows to migrate** (hepatic, immunotoxicity, complement); two exist as
**rival datasets with no canonical version** (chronic neurotoxicity twice, hydrocephalus three
times, with different rosters, columns and grade columns); and `purity_pct` holds a real value on
**3 of 3,034** oligo rows project-wide, which no schema fixes.

**Adopted instead — three tiers, each independently shippable:**

- **Tier 0 — crosswalk only. Week 1, ~5 days, changes no existing file.** Ship `molecule.csv`
  with a `molecule_uid` across all 3,034 roster rows (seed from the existing 18-row
  `molecule_crosswalk.csv`); the controlled-vocabulary document; and `endpoint_coverage.csv`
  stating per endpoint the measured rows, measured oligos, subject-class distribution, rubric name
  or none, and each MQR field as present-populated / present-empty / absent.
  **This is what actually unblocks November** — assembly needs a defensible cross-endpoint
  statement, not one physical table. It also preserves the breadth posture: all eight endpoints
  appear, and the three empty ones become *declared facts* rather than gaps a reviewer discovers.
- **Tier 1 — view layer. Weeks 2–4, reversible.** One adapter per endpoint emitting harmonized
  views; source CSVs untouched; each adapter must reproduce its endpoint's published row count
  exactly before its output is accepted. **Coagulopathy is the reference implementation** — ~2
  days, closest to the target model.
- **Tier 2 — in-place migration. Post-November.** The released-document blast radius lives here.
  Not under deadline.

Where you generalize German's model, **generalize — do not redesign.** His immunotoxicity memo
already gives 38 named fields and the canonical-oligo-to-observation architecture; his thrombo
document gives the lineage chain and the evidence tiers. Bring Oscar a migration proposal, not a
new invention.

### P2 — Minimum Qualified Record, derived from German's gates

Not from my draft. German has published qualification criteria twice and they are stricter and
better grounded: twelve sign-off gates (source traceability, 5′→3′ verification with strand
identity, **modification encoded by position not as a molecule-level flag**, raw outcomes retained
with curator binaries marked derived, agonist/antagonist/potentiator/inert separated, human and
animal never pooled, splitting checked for leakage) and the control definitions in
`SCIENTIFIC_RULES.md` §E. Submit the MQR to German as a **derivation of his own criteria** — far
easier for him to approve than something new.

### P3 — the three thin endpoints, with immunotoxicity reframed

- **Immunotoxicity — you were right and nine auditors were wrong.** They scoped to git, found two
  staging CSVs and a dossier reading "This project extracted no immunotoxicity data", and declared
  the endpoint empty. My completeness critic opened the Drive workbook directly: it reads cleanly —
  15 sheets, 142 catalog records, 141 identifiers, 33 observations at Human 30 / Mouse 2 /
  Multiple 1, 20 papers. **Your baseline was accurate and was disbelieved for a month because the
  evidence lives outside version control.** Correct one figure: your 64 trial candidates appears in
  **zero cells**; the adjudication is **54 approved / 48 hold / 40 support-only**.
  **Action: commit that workbook, or a faithful CSV reduction of it, into the branch** so every
  immunotoxicity figure becomes auditable in one place. This is the highest-leverage single act
  available on this endpoint, ahead of any new acquisition.
- **Hepatic** (0 rows): drive the human-hepatocyte constructs to qualified rows — note the lead was
  corrected from nine to seven on 2026-10-03. Stage Burdick's 80-construct panel as clearly
  labelled animal support; it is not human progress. Sewing 2016, the only primary human-hepatocyte
  source, is **absent from the repository** — acquiring it is the endpoint's critical path.
- **Complement** (0 ingested rows): **6 of 7 MQR fields have no column in existence.** Build the
  schema before any further acquisition — copy the per-position pattern already proven in
  `valentin2021_S1_S2_sequences.csv`, the only true per-position schema on the branch. Report
  honestly that **0 of the human rows carry a numeric complement value**, and that one of the ten
  rows is not a complement readout at all. Pair the Sewing raw-file acquisition with
  thrombocytopenia so it is paid once.

### P4 — the CNS lineage decision goes to German, now

This is no longer a crosswalk exercise. The two lineages are **two different datasets**, not two
views: different rosters (13 vs 573 oligos), different column sets (44 vs 33), different grade
columns (`cns_tox_grade` vs `neurotox_grade`), different grade distributions. Choosing is a
**scientific adjudication about evidence quality and scope** — German's, not yours, not mine, and
not the schema's. It blocks Tier 1 migration for that endpoint.

Prepare the comparison **for German's decision**: rosters, overlap (144 shared exact sequences),
evidence composition, rubric difference, and what is lost either way. Stop feeding both. Acute
neurotoxicity remains a supporting module per the brief and receives no breadth budget.

### P5 — start the three documents now

Unchanged, and the most likely thing to be skipped because it feels premature. Narrative,
methodology and PADP drafted **now**, against the Tier 0 vocabulary, with named numeric
placeholders, so November is number-landing and editing. **If they start in November they will
not finish in November.** The narrative skeleton must reserve slots for positive and negative
controls — see P6a, because we may not have them.

### P6 — purity: harvest first, then disclose. I was wrong about this.

I previously told you to plan for disclosure rather than rescue. That was too pessimistic.
**Real analytical characterization exists** — the Drive immunotoxicity catalog carries full-length
purity ~94–99% by IE-HPLC/RP-HPLC/CGE, identity by MALDI-TOF, endotoxin <0.075 EU/mg on 5 records,
and **modification positions populated on 41 of 142**. Every git endpoint reports purity as zero.

Promote these into a repository table with per-row provenance **before the methodology document is
written**, and stop describing purity as universally absent. Then, for what remains:
`NOT_REPORTED` is the **correct field value** — German mandates it, it is not a failure state —
**plus** the Characterization Gap Register recording what is missing, why, what was attempted and
what would close it. Both, not one instead of the other.

### P6a — positive controls may not exist, and the narrative requires them

Only acute-neurotoxicity has a `control_role` column, and it holds **0 positive controls of
1,866**. Kidney, coagulopathy, hydrocephalus and cns-alternate oligo tables have **no control
column at all**. Only thrombocytopenia's `controls_inventory.csv` holds real positive and negative
arms. Audit what controls exist project-wide and report it as a deliverable gap, not a data gap.

### P7 — leakage is no longer theoretical; it is shipped

`acute-neurotoxicity/data/oligos.csv` ships a published train/test split in which **48 of 148 test
oligos share an exact sequence with a training oligo**, and 115 of 148 are contained in or contain
a training sequence. German prohibits random row splitting outright; the symptom is already
visible elsewhere as ~0.94 AUC random against ~0.65 LOPO on n=19 held-out oligos with 7 positives
and no confidence interval.

`sequence_family_group` and `paper_group` become schema fields **in Tier 0**, not at modelling
time. Also required: `experiment_group_id` and subject/donor grouping, without which no endpoint
can be split without correlated-observation leakage. And note the real ceiling: distinct oligos
that are human-lab **and** graded **and** sequence-bearing are thrombocytopenia 25, coagulopathy
19 (strictly human in-vitro **7**), cns-alternate 13, kidney 7, cns-acute 7, hydrocephalus 0.
**The sample size that matters is ~25 molecules, not thousands of rows.** Say so plainly rather
than letting row counts imply otherwise.

### P8 — release discipline

One canonical branch per endpoint; every accepted dataset, figure and document bound to a frozen
release tag. Check `release_id` before quoting any generated statistic — dedicated hydrocephalus's
stats carry `hydrocephalus-…-dirty`, meaning the numbers everyone cites were produced from an
**uncommitted working tree**. A `-dirty` suffix or an unreachable commit means the figures are
untied to the tree and must be recomputed.

## 5. Credibility items to fix before anyone outside sees this

- **The CNS front door misstates the challenge's central priority.** `_shared/cns/README.md`
  states 181 compounds carry both readouts and that this is "exactly the in-vitro-to-in-vivo
  extrapolation the challenge asks for". **All 181 measure as animal in-vitro plus animal in-vivo,
  rat and mouse, zero human rows** — while the same README's line 131 concedes the dataset cannot
  extrapolate between human in-vitro and animal systems. You caught this; it is still live. Its
  grade distribution is also wrong: 56/87/40/57 stated against 74/81/39/51 measured. **A reviewer
  opens the README first.**
- **The stale 111-row kidney table is a physically shipped file, not stale prose.** Five of six
  branches ship an 111-row `measurements.csv`, in **two mutually divergent versions**. Any script
  resolving `data/measurements.csv` by relative path on those branches reads the wrong table. The
  canonical 246-row version exists only on `amazing-galileo`. The stale 111 also appears in at
  least 13 documents including `toxicity/README.md`'s own ledger.
- **Coagulopathy's shipped deliverables carry stale arithmetic.** `METHODOLOGY.md` — a release PDF
  sitting exactly at its 5-page limit — states 213 oligonucleotides / 2,388 measurements / 941
  position records / 75 sources against measured **218 / 2,685 / 1,039 / 100**, and the same stale
  set recurs in `SOURCES.md`, `PADP.md`, `schema.md`, `README.md` and the endpoint dossier. Cheap
  to fix and the most visible credibility item on that branch.
- **Hydrocephalus `PHASE2_COMPLIANCE.md` still calls 53 "compounds"** against its own
  `n_compounds_real = 51`. Your 09-30 warning was correct and was not acted on.

## 6. Audit directives you must NOT act on

My audit layer made errors. Do not execute these:

- **Kidney Directive 5 is wrong at its foundation.** It claims
  `research_staging/sequences_recovered_2026-10-02.csv` holds 10 candidates against the 10 TBD
  sequence gaps, taking coverage 55/65 → 65/65. The id sets **intersect at 6**. Four staged rows
  target oligos that already carry sequences and say so in their own status column
  (INDEPENDENT_CONFIRMATION, PROPOSED_CHEMISTRY_UPGRADE ×2, NOTATION_DISCREPANCY_FOR_GERMAN), and
  four TBD oligos have no staged candidate at all. Promoting everything reaches **61/65**. Two of
  those rows are flagged for German's adjudication, so acting on this would push chemistry changes
  through as gap-filling.
- **Do not accept the coagulopathy audit's corroboration of 30 headline trials** — it cited a
  whole-table registry count. Only 18 of the 30 carry a registry id; the repo's own
  `RELEASE_MANIFEST.json` agrees.
- ~~**Ignore the claimed 5-page PADP limit** asserted on the CNS branch. It exists nowhere.~~
  **STRUCK 2026-10-03 — this was my error, caught by Beebop.** The five-page PADP limit is
  **official and binding**: the Phase 2 description sets it, and §2 of this directive states it
  correctly. My auditor's finding was that the limit "exists nowhere **on this branch**" — a
  correct, scoped observation about one repository — which I compressed into a false general
  claim, in the same document whose §1 charges Beebop with dropping qualifiers between layers.
  **Preserve the official limit. Never take a page limit, or its absence, from a branch document;
  the announcement governs.** Left struck rather than deleted so the errata trail is visible.
  See `CRANK_REPLY_TO_BEEBOP_2026-10-03.md` item 4.

## 7. What I want back

1. **P0 licensing package** — inventory, per-row redistribution audit of submission artifacts,
   withdrawal list, licence recommendation. First, ahead of everything.
2. **Tier 0 crosswalk** — `molecule.csv`, controlled vocabulary, `endpoint_coverage.csv`.
3. **MQR derived from German's gates**, for German and Oscar.
4. **The CNS lineage comparison prepared for German's decision.**
5. **The immunotoxicity workbook committed** (or a faithful CSV reduction), with your 64 corrected
   to 54/48/40.
6. **The three placeholder-tagged document skeletons.**
7. **Your disagreements, with evidence.** Including with anything in §1.

**Flag immediately, outside the round cadence, if:** an endpoint cannot meet the MQR floor at all;
a licensing problem is worse than stated; anything here conflicts with German's authority — in
which case German wins and I want to hear about it.

## 8. Escalated to Oscar and German, not decided by either of us

- **German:** the CNS lineage choice; the thrombocytopenia freeze (currently **not granted**) and
  its six mandatory blockers; the immunotoxicity CRITICAL correction list; whether the Drive or the
  repository is authoritative where they diverge.
- **Oscar:** the open-licence terms and the withdrawal decisions P0 surfaces; schema ratification;
  the Drive/git reconciliation policy.

---

*Crank. Reporting to Oscar. Consolidated directive, superseding 001 and 001-A.*
