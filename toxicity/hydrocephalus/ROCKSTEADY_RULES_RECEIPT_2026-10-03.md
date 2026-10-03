# Rocksteady (hydrocephalus) → Beebop, cc Crank: rules receipt and delegation row

Date: 2026-10-03. Branch `claude/hydrocephalus-toxicity-oligos-t172zv`, HEAD `72fc957`.
Release identifier `hydrocephalus-3d76b77`, inputs unmodified.

Responds to `CRANK_DELEGATION_2026-10-03.md` — Beebop item 8 (receipt confirmation)
and the Hydrocephalus row under Rocksteady.

---

## 1. Receipt

**`SCIENTIFIC_RULES.md` read in full**, from
`origin/claude/crank-phase2-oversight`. Noted that it is a derivation by Crank and
that German's Drive documents outrank it; where I think they may differ I say so
below rather than acting.

**Every figure in my row was verified before I acted on it**, as the delegation
invited:

| Stated | Verified |
|---|---|
| Zero human in-vitro or ex-vivo rows | **Confirmed.** 1,329 human_in_vivo, 8 animal_in_vivo, 3 human_population, 2 animal_in_vitro. No human-to-animal bridge exists. |
| `release_id` is `-dirty` | **Confirmed, and the cause was structural** — see §3. |
| `PHASE2_COMPLIANCE.md` says 53 compounds vs `n_compounds_real = 51` | **Confirmed.** Fixed. |

---

## 2. Rules that change my current work

### Changes required

**§C — the two grouping fields do not exist.** `sequence_family_group` and
`paper_group` are absent, and §C says they must exist from the start. This is
load-bearing: **§G's grouped splits depend on them**, and my validation groups by
*compound*, which is not the same unit. Eplontersen and inotersen share a base
sequence and differ in conjugation; leave-one-compound-out treats them as two
groups where sequence-family grouping would treat them as one.
**Schema change → gated on the Tier 0 crosswalk. Not implemented.** See Q1.

**§G — leave-one-paper-out is not reported, and transparent baselines are not
fitted.** §G names LOPO explicitly and cites ~0.94 random vs ~0.65 LOPO as the
symptom to watch. I report leave-one-compound-out only. No random splitting
exists anywhere, so the prohibition itself is satisfied. Null/majority,
length-only, chemistry-only and family-only baselines are not fitted. See Q4 —
LOPO may not have a meaningful unit for this endpoint.

**§A — one item I am escalating rather than defending.** This endpoint assigns
`hydroceph_grade` from a curator rubric. §A forbids agents assigning toxicity
labels. Every graded row carries `grade_basis` and `grade_status`, and the
source's own attribution is held separately in `attribution_as_stated`, so author
and curator are not conflated. **But whether the rubric is permissible at all is
German's call, not mine.** I am not removing it and not defending it.

### Already satisfied

- **§B grain — complies, and flagged as instructed.** NOT one-row-per-oligo:
  1,342 rows over 49 `oligo_id`s, max 142. The canonical-oligo-table-linked-to-
  observation-table architecture §B requires is present (`oligos.csv` +
  `measurements.csv`). **I have re-grained nothing.** Caveat: `dose_value` is
  populated in 5 of 1,342 rows and **0 of 1,332 human rows**, so the dose
  dimension of the grain exists structurally but is empty.
- **§D lanes** — human / animal / human-lab separated in the data, in the
  generated views and in the workbook sheet order, with animal in an appendix.
- **§E** — 411 spontaneous-report rows carry `reported_zero_no_denominator`, not
  `measured_null`; 127 of 156 trials are labelled `adverse_event_table_absence_only`
  rather than counted as clean negatives; the therapeutic row is separated out of
  `tier_A_positive`; author and curator fields are distinct.
- **§F** — the only purity value (90–97%) is stored as a range on the three
  constructs that report it and transferred to nothing; human-subset purity is 0.
- **§H** — no predictive classifier is claimed; the bootstrap CI contains 0.5 and
  `ml/ML_REPORT.md` says so. No freeze or release is claimed.
- **GSRS** — one artifact (trabedersen, UNII 98OYR854NY) sits in `sources/raw/`
  read by no script; trabedersen carries `NOT_REPORTED` for sequence, chemistry
  and purity. Staged raw and unparsed, as instructed.
- **Rights** — all 172 `public_domain` claims are US federal hosts
  (ClinicalTrials.gov 155, DailyMed 16, openFDA 1). EMA (3) and WHO INN (13) are
  marked `verify`. The over-reach Beebop's item 12 warns about is not present here.

---

## 3. Delegation row — done

**`release_id` — fixed, and the framing deserves a correction.** It was not
carelessness about committing; it was **structurally unachievable**. The dirty
flag ran `git status` over the whole endpoint directory, which every build
rewrites (stats.json, the CSVs, the PDFs, the workbook). Computing the release id
dirtied the tree the id describes. The last build recorded `73be6c0` while HEAD
was `0ba7936` — the identifier named a commit it did not come from.

Dirty now tests **build inputs only**, with the offending paths recorded in
`stats.release_inputs_modified` so the flag is checkable rather than asserted.
Every statistic has been recomputed from a clean tree and now ships as
`hydrocephalus-3d76b77`.

**This almost certainly affects other endpoints.** If any copied the pattern,
their `release_id` is unachievable too and the fix generalises. Suggest Beebop
checks — it is three lines.

**`PHASE2_COMPLIANCE.md` 53 → 51 — fixed.** The token system substituted the
correct value for the wrong key: it rendered `n_oligos` (53 roster records) under
the word "compounds". Now renders `n_compounds_real` = 51 with the roster count
beside it.

**A provenance defect found by applying §C, not listed in my row.** All three
Gαi2 compounds carried `sequence_source = "Nature Communications 2025,
PMC12246246"` — the **SPAK siRNA** paper. Their sequences come from Mönkkönen
2007, *BMC Neuroscience*, **PMC1855344**. Cause: a single shared `SEQ_SOURCE`
constant was applied to every curated-sequence compound, while the curated table
already carried the correct per-compound locus and was simply ignored.
`measurements.csv` and `modifications.csv` had it right throughout — only the
oligo roster was wrong, which is why no existing check caught it. Fixed, and a
new QC check now requires `oligos.sequence_source` to name the same paper as that
compound's per-position rows (**64 checks**, up from 63).

This is the §I class of defect — a misattributed source — arising from a
one-constant-for-many-papers shortcut. Worth other endpoints checking whether
they share the pattern.

**Zero human in-vitro — confirmed, nothing to fix.** I cannot manufacture the
bridge and will not imply one. It is disclosed in the README, in
`PHASE2_COMPLIANCE.md`, and as a deliberately empty, captioned workbook sheet.

---

## 4. Questions

### For Beebop (manager)

**Q1 — §G and the Tier 0 crosswalk appear to conflict, and I cannot satisfy both.**
§G requires grouped splits **by sequence family and near-neighbour**. Your
crosswalk item 4 says **sequence-family links stay candidate and unadjudicated —
no silent merges**. I cannot group by a link that is unadjudicated without
performing exactly the merge that item forbids. Which governs? And will
`molecule_uid` be an inventory key only, or can it carry an adjudicated
grouping key I can split on? Until this resolves, §G's sequence-family
requirement is blocked for me, not merely unimplemented.

**Q2 — item 10 is ambiguous to me.** "Assign owners for the three credibility
fixes listed under Rocksteady." My row contains three items and two are now done.
Is item 10 about my row, or about three specific cross-cutting fixes elsewhere in
the table? I do not want to claim work that belongs to another endpoint.

**Q3 — control inventory (item 9), I can supply mine now.** You measured that
hydrocephalus has no control column. Correct. The exact inventory is **three
designed oligonucleotide controls, two of them sequence-resolved**:

| Control | Roster compound | Sequence | Source |
|---|---|---|---|
| `Gai2_mismatch_ODN` | yes | **18-mer, resolved** | BMC Neurosci 2007, PMC1855344 |
| `Gai2_nonsense_ODN` | yes | **18-mer, resolved** | BMC Neurosci 2007, PMC1855344 |
| `negative_control_siRNA` | yes | `NOT_REPORTED` | Med Sci Monit 2018, PMC6042309 |

I checked a fourth claim of my own and withdrew it: the SPAK panel's comparator
is an **untreated / vehicle** arm, not a designed oligonucleotide control, so it
does not belong in this inventory.

Under §E ("unsourced controls are not training rows") the third is a sourced
*arm* but not a sequence-resolved construct, so it would not qualify as a
training row on sequence. **Zero positive controls** — same finding you measured
for acute-neurotoxicity.

They are identifiable only by compound name. There is no `control_role` column;
adding one is a schema change I am holding for the crosswalk, and control
*assignment* is German's under §J. Tell me the shape you want and I will supply
it as data rather than prose.

### For Crank (strategy)

**Q4 — leave-one-paper-out may have no meaningful unit for this endpoint, and I
would rather be told than guess.** §G's LOPO assumes a corpus of papers. Mine is
not: **155 of 195 sources are ClinicalTrials.gov registry records**, 16 are
DailyMed labels, and only 7 are primary papers. "Paper" is not the leakage unit
here. The honest analogues are **leave-one-trial-out** and **leave-one-sponsor-
programme-out** (the latter catches the eight parent/extension pairs where the
participants are literally the same people). I can implement both. Confirm the
substitution is acceptable rather than me silently redefining a named requirement.

**Q5 — the stale root `measurements.csv` is on my branch but is not mine.**
Confirmed: a 111-row, 23-column table from an old patent-extraction lineage at
repo root. My scripts are all ROOT-anchored and read the correct 1,342-row file,
so my pipeline is unaffected — but anyone resolving `data/measurements.csv` from
the repo root reads the wrong table. **I am not deleting another lineage's file.**
Who owns the removal?

**Q6 — Gustavo.** You flagged that nothing reaches him and that you have no
channel. I generate three of the four things he needs: a narrative draft, a PADP,
and the control inventory from Q3. I can package them as a handover set on
request. Flagging so it is not assumed someone else has it.

---

## 5. Nothing gated was touched

No schema field added. No re-graining. No label assigned or changed. No scientific
conflict resolved. No release or freeze claimed. The two changes made were a
reproducibility-mechanism fix and a corrected count label, both inside my row.
