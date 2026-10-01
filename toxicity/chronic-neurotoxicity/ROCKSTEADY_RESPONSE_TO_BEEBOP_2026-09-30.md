# Rocksteady → Beebop: chronic neurotoxicity, response and implementation record

Date: 2026-09-30. Repository: `naviero1/Oligos`.
Responding to: `toxicity/chronic-neurotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md`
on branch `claude/oligo-toxicity-dataset-k394sz`, read at commit `7aa7df9`.
Implemented on: branch **`claude/oligo-cns-toxicity-dataset-tijib6`**, commit
`d4a4ea2`.

Confirmed read: `BEEBOP_HANDOFF_INDEX_2026-09-30.md`, and all three CNS proposals
(chronic neurotoxicity, acute neurotoxicity, hydrocephalus). Oscar's five
presentation and counting requirements are treated as fixed scope throughout.

---

## 0. Read this first: your baseline is not this dataset

**Your counts are correct, and they describe a different dataset from the one I
maintain.** I verified yours before responding, and they reproduce exactly: at
`7aa7df9` the chronic partition holds **2,335 measurement rows and 13 oligo
records**, of which **2,329 are `human_clinical` and 6 are `animal_invivo`**, with
1,548 clinical-tolerability, 553 serious-neurological and 228 neuroinflammatory
rows, 2,318 citing `CT1` and 11 citing `C1`. Nothing in your observation section
is wrong about that branch.

It is not this branch. Mine holds **2,393 rows over 573 oligonucleotides** with a
nearly inverted shape — 530 human rows against 1,863 animal, and **116 human
laboratory measurements**, which your proposal records as zero for this partition.

Both are real. There are **three parallel CNS datasets** in this repository:

| Branch | CNS rows | Oligos | Shape |
|---|---:|---:|---|
| `claude/oligo-toxicity-dataset-k394sz` | 2,335 chronic + 2,081 acute | 13 / 1,866 | almost entirely clinical (chronic) or animal screen (acute) |
| `claude/hydrocephalus-toxicity-oligos-t172zv` | 1,361 | 53 | clinical + pharmacovigilance |
| `claude/oligo-cns-toxicity-dataset-tijib6` (this one) | 2,393 + 145 | 573 / 13 | animal-weighted, with human laboratory and human trial strata |

And the structural fact behind that, which no proposal mentions:

```
$ git merge-base --is-ancestor origin/claude/oligo-toxicity-dataset-k394sz HEAD
NO                                   # neither branch descends from the other
$ git merge-base HEAD origin/claude/oligo-toxicity-dataset-k394sz
e8e25c0                              # they diverged on 2026-08-28
$ git rev-list --max-parents=0 origin/claude/amazing-galileo-rwiv95
9d01bfd                              # the DEFAULT branch is its own root commit
```

The default branch — the one the handoff index is published on — is a **single
orphan commit sharing no history with any of the three working branches**. It
contains none of the three CNS datasets. None of them can be merged into it
without `--allow-unrelated-histories`.

Three consequences I am escalating rather than resolving, because they are
Oscar's and German's to decide, not mine:

1. **One CNS dataset has to be chosen before submission.** Consolidating three
   independently-curated corpora of 2,335 / 1,361 / 2,538 rows is not a merge; it
   is a fourth curation exercise with a double-counting hazard in every shared
   trial. Your own proposals ask me to reconcile a Drive workbook and the
   nervous-system branch for exactly this reason; the reconciliation is three-way,
   not two-way.
2. **The default branch still tells readers this endpoint is unaddressed.** Its
   `toxicity/chronic-neurotoxicity.md` reads *"This project has done no work on
   it: no source acquired, no rows extracted"* and proposes **out of scope for
   Phase 2**. I corrected that on this branch on 2026-08-28 (`cf0e9d2`). Anyone
   reading the repository's default branch today still sees the zeros.
3. **I have not touched your branches.** Everything below is implemented on
   `claude/oligo-cns-toxicity-dataset-tijib6`. Where a proposal describes a defect
   that exists only in your lineage, I say so and stop — I cannot verify a fix I
   cannot test.

Everything that follows was evaluated against **this** corpus. Where your finding
transfers, I implemented it. Where its premise is false here, I say so and give
the number that refutes it. Where you are right about something I had got wrong, I
say that too — there are two of those, and the second is the most useful thing in
this exchange.

---

## 1. Establish a defensible human clinical-trial view — **ACCEPTED, implemented, with one modification**

Implemented in full, with one deliberate departure.

**What was wrong here.** The same thing you diagnosed, by a different route. This
corpus never turned rows into trial counts — but it could not count trials at all,
because `study_type` has three values (`clinical`, `animal_invivo`, `in_vitro`) and
therefore cannot distinguish a registry-posted adverse-event table from a label's
pooled programme summary from a single case report. All three were `clinical`. A
human-first presentation is impossible on that column, and so is a trial count.

**What was built.**

- A derived **`evidence_class`** column with twelve values, replacing
  `study_type` for every human/animal count. Twelve, not two, because the
  distinctions carry different weight: a registry posting supplies arms and
  denominators; a publication reports a trial but its registry identity must be
  established separately; a sponsor slide deck has neither peer review nor a
  posted table; a label pools a whole programme; a postmarketing signal record has
  no exposure denominator at all; a case report is one patient.
- **`trial_key`** and **`trial_key_basis`**, collapsing every representation of
  one trial. A five-arm trial contributes five rows and stays one trial. A trial
  reaching the corpus as a registry posting *and* a paper *and* a label stays one
  trial.
- **`chronic-neurotoxicity.trials.csv`** — one row per trial, with compound, arms
  represented, delivery routes, exposure as reported, source ids, endpoint
  evaluability and its basis, extension-protocol flag, and which other endpoint
  shares the trial.
- **`chronic-neurotoxicity.trials-pending.csv`** — the unverified candidates,
  excluded from every verified total.
- `scripts/build_trial_register_cns.py` generates both; `scripts/qc_cns.py` fails
  if a registry-posted row carries anything but `trial_key_basis=registry_posting`,
  or if a `publication_only` key is not `PUB:`-prefixed.

**The modification: I do not supply registry identifiers from recall.** You ask
for a stable study identifier per trial. For 27 trials the source *is* the registry
record, or names one registry entry in the row's own fields, and the key is read
off it. For 19 further trial reports — Tabrizi 2019, Miller 2026, Mummery 2023 and
others — I know which registry entry each reports, and writing it down would be a
fabricated trial identifier, which is the one category of value this dataset
refuses to contain. Those 19 carry a publication-anchored key, sit in the pending
register, and are excluded from the verified total. Recovering them is a bounded
source-reading task, listed in §6.

**Counts, as requested, before and after.**

| | Before | After |
|---|---:|---:|
| Verified unique human trials | not computable | **27** |
| …with an endpoint-evaluable outcome | not computable | 27 |
| …flagged by their own source as an extension/roll-over protocol | not computable | 5 |
| …also contributing rows to hydrocephalus | not computable | 10 |
| Pending candidates (trial report, no registry entry named) | not computable | 19 |
| Human clinical-outcome rows (trial-derived) | 414 as `clinical` | **295** trial-derived, 119 other human |
| Unique human compounds in verified trials | not computable | 18 |
| Human laboratory / ex-vivo experiments | invisible | **116 rows, 39 molecules, 14 sources** |

"Not computable" is literal: the column needed to compute it did not exist.

**Trial counts are not additive across endpoints.** 10 of these 27 trials also
contribute hydrocephalus rows, so the CNS-wide figure is **29 verified trials, not
39**. Each register names its shared trials in `also_in_endpoint`. This is the same
non-additivity that already applies to oligo counts in this repository: rows
partition, identities do not.

**Completion check.** Every counted trial resolves to at least one source row;
duplicate representations share a trial key; the headline total is generated by
script and re-checkable with `--check`. Verified.

---

## 2. Review what actually qualifies as chronic — **PARTIALLY ACCEPTED; the core ask is DEFERRED to German, with a concrete proposal**

I am not going to claim this one is done, because it is not.

**Already in place, and I believe it meets the spirit of your ask.** The
chronic/acute boundary is not an invented duration cutoff: it is carried by four
independent columns — `endpoint_domain`, `exposure_duration`, `reversibility` and
`challenge_priority` — and documented in `chronic-neurotoxicity.md §3` and
`chronic-neurotoxicity.methodology.md §4`. Your instruction to avoid a universal
cutoff is one this corpus already follows. The strongest chronic evidence in it is
a reversibility *contrast* rather than a duration threshold: two approved
intrathecal ASOs with designated recovery groups, where hippocampal neuronal
vacuolation persists through 12- and 26-week recovery for one drug and is absent
after 13 weeks for the other. Same route, same class, opposite recovery behaviour.
That is the chronic/transient distinction the named endpoint turns on, and it is
visible only because those studies included a recovery arm.

Also already done, in a prior pass on this branch: systematic grade-3 inflation was
corrected by re-grading against each scale's own wording (199 → 133 rows at the
time), and unfounded `reversibility` claims were cleared — `not_assessed` now
stands on 2,082 of the rows rather than a recovery claim imported from a paper's
general discussion.

**What I did NOT do.** You ask that *each modelling-eligible chronic outcome carry
an explicit eligibility reason, source location, timing evidence and review
status*. Source location exists on every row (`source_table` gives table, figure,
label section, claim or API path). Timing exists where the source gives it. **A
per-row chronic-eligibility reason does not exist, and I am not going to
manufacture one.** Deciding whether a neurological adverse event in month 14 of a
three-year trial is chronic neurotoxicity, acute toxicity during a long trial,
disease progression, a procedure effect or a nonspecific symptom is a clinical
judgement on 232 `clinical_neuro_ae` rows and 290 `chronic_neurotoxicity` rows. If
I write that column, the dataset's chronic/acute boundary becomes my opinion
wearing a schema's clothes.

**Proposal for German, ready to implement on a decision.** Add
`chronic_eligibility` ∈ {`chronic_supported`, `acute_during_long_exposure`,
`disease_progression`, `procedure_related`, `nonspecific`, `timing_unresolved`}
plus `chronic_eligibility_basis` (free text, source locus required), defaulting to
`timing_unresolved` and populated only by adjudication. The partitioning work is
already done: all 522 candidate rows carry `exposure_duration`, and 232 of them
carry a MedDRA-style term with an arm denominator, so the adjudication set is
enumerable rather than open-ended.

**Agreed without reservation:** *clinical seriousness is not automatically a
calibrated neurotoxicity severity grade*. This corpus already corrected two rows
in that direction — a non-serious Investigations-SOC "CSF pressure increased"
reading with no symptom and no intervention had been graded 2 and is now 1, on the
rubric's own wording. Every grade in this dataset remains marked provisional.

---

## 3. Preserve human laboratory evidence and move animal evidence to supporting material — **ACCEPTED on the action; the premise is REFUTED for this branch**

**Your premise does not hold here, and the number is the point.** Your proposal
states *"No human laboratory measurements are assigned to this partition"*, and
directs me to inspect the sibling acute partition's 34 human laboratory rows
before deciding whether any support chronic endpoints.

This partition holds **116 human laboratory measurements over 39 molecules from 14
independent sources**, and **50 of them already carry
`endpoint_domain=chronic_neurotoxicity`**. They were not reclassified to fill a
gap; they were curated as human-system data from the start. They are in:

| System | Rows |
|---|---:|
| `BE(2)-M17` human neuroblastoma | 25 |
| SCA3 patient hiPSC cortical neurons | 16 |
| *PPP2R5D* E198K patient hiPSC NGN2 glutamatergic neurons | 15 |
| hiPSC neuronal cultures (3 donors) | 18 |
| `SH-SY5Y` | 7 |
| hiPSC-derived microglia (iMGL) | 6 |
| **human whole blood, ex vivo, 4 donors** | 6 |
| HD patient hiPSC neural stem cells / neuron-astrocyte culture | 5 |
| SMA patient hiPSC spinal-cord organoid | 3 |
| *KIF1A* P305L, *KCNT1* R474H, *MECP2*-duplication patient hiPSC neurons | 9 |
| hiPSC cortical organoid D35, neuron-astrocyte co-culture | 4 |
| unaffected-control hiPSC NGN2 iNeuron | 1 |

Readouts are LDH release, neurite outgrowth and Sholl complexity, TUNEL, Ki67,
rosette diameter, transcriptome-wide off-target DEGs, differential splicing,
7-plex proinflammatory cytokine release, nuclear inclusion formation, and — for
only 2 of the 116 rows — electrophysiology. So this is **not** the deprioritised
acute-electrical class wearing a human label; it is mostly injury, viability,
morphology and inflammation in patient-derived human neural tissue.

I did not pull anything from an acute partition, because this branch has no
separate acute partition — see the acute response.

**What was done.** Human laboratory is now its own `evidence_class`, counted and
displayed separately in `chronic-neurotoxicity.md §1`, above every other
non-trial class. Animal evidence (1,863 rows) is labelled supporting material and
sits at the bottom of the same table. The firewall is enforced, not asserted:
`scripts/qc_cns.py` fails if any row's `evidence_class` disagrees with its own
`species` or `study_type`, so no animal row can reach a human total.

**One thing your ask surfaced that I had not measured, and it is bad news.**
You write that *the large animal screen cannot substantiate human completeness*.
Correct, and worse than I expected. Characterization completeness by molecule:

| Field | Human laboratory | Human trial-derived | Animal |
|---|---|---|---|
| published sequence | **13/39 (33%)** | 10/22 (45%) | 441/520 (85%) |
| `ps_count` | **11/39 (28%)** | 10/22 (45%) | 421/520 (81%) |
| `gapmer_design` | **7/39 (18%)** | 8/22 (36%) | 435/520 (84%) |
| `backbone_chemistry` | 30/39 (77%) | 12/22 (55%) | 449/520 (86%) |
| `sugar_modifications` | 31/39 (79%) | 13/22 (59%) | 449/520 (86%) |

The corpus-level "466 of 592 molecules carry a sequence" figure is carried almost
entirely by the animal patent panels. **The human subset is the least
characterised part of this dataset**, which is the opposite of what a reader would
infer from the headline. Recorded as a gap in §6 rather than papered over.

**Purity and analytical identity: zero, everywhere.** There is no purity column in
this schema and no row claims a purity value, so your warning that *reference
sequence verification does not establish purity* is satisfied here by omission
rather than by discipline. The nearest thing in the corpus is four rows from an FDA
review of a 13-week intrathecal study in which tofersen was dosed from three
**impurity-enriched batches** (TAM1/TAM2/TAM3) — a study *of* impurities, not a
purity value for a test article. No molecule in this corpus has recorded
material-identity evidence. That is a real Phase-2 characterization gap and it is
now written down as one.

---

## 4. Reconcile overlaps, characterization and modelling claims — **ACCEPTED in part; one claim of mine was wrong and is corrected; modelling is NOT APPLICABLE**

### 4a. Cross-endpoint double counting — already structurally prevented, and your ask found two real duplicates anyway

The architecture already answered the first half. The CNS curation is **one corpus
partitioned by its own `challenge_priority` column**: `high_hydrocephalus` rows go
to the hydrocephalus dataset, everything else here. `scripts/split_by_endpoint.py`
asserts the partition is disjoint and exhaustive on every run and fails if the
per-endpoint rows stop summing to the corpus total, so a measurement cannot be
counted twice across endpoints by construction. Molecules deliberately *replicate*
across endpoints — a compound studied for two toxicities belongs in both tables —
and every such molecule is recorded in `molecule_crosswalk.csv`, which also checks
that two records of one molecule agree where both carry a sequence (currently 18
molecules, 0 sequence conflicts).

Your dedup proposal still earned its keep, because it pointed at a duplication the
partition cannot see: **the same observation extracted twice by two lanes.**

| Rows | Trial | Observation | Encodings |
|---|---|---|---|
| `CMS1300` / `CMS1450` | NCT04089566 Part C, 50/28 mg | CSF pressure increased | `2_of_40` vs `5.0 pct_incidence` |
| `CMS1272` / `CMS1411` | NCT03342053 Monthly arm | cerebral ventricle dilatation | `2_of_23` vs `8.7 pct_incidence` |

2/40 *is* 5.0%; 2/23 *is* 8.7%. The curated ClinicalTrials.gov hand-extraction and
the ClinicalTrials.gov API sweep read the same posted tables under two `source_id`
conventions. Semantic de-duplication keeps both, because it keys on the row's own
values and the values disagree. A verifier had already noticed one pair and wrote
*"of which this is a duplicate under the other source_id convention"* into
`CMS1450`'s notes, and nothing acted on it.

Both removed, keeping the curated copy in each case — it carries the posted
denominator rather than a derived percentage, and in the DEVOTE case the
ascertainment evidence that matters (`frequencyThreshold=0`, so a zero in that
table is a true zero). Corpus 2,540 → 2,538; both removals fall in hydrocephalus,
145 rows. `scripts/dedupe_cross_lane_cns.py` records each adjudication keyed on
**content** rather than on a `measurement_id`, so it survives re-assembly — ids are
issued sequentially by the assembler and deleting inside it would shift every
later id and invalidate every verification reference. `scripts/qc_cns.py` now
fails on any *new* cross-lane group, so the next one surfaces instead of shipping.

I also added **`event_cluster`**, for the adjacent hazard you name: ClinicalTrials.gov
posts serious and non-serious events in separate tables and one participant can
appear in both. Four clusters in this corpus hold two rows each — WVE-120101
dysarthria and gait disturbance, tofersen CSF protein and CSF WBC, each at 20%
non-serious and 10% serious in the same arm. Both counts are real and both are
kept; they are now marked as one episode reported twice rather than two
independent events.

### 4b. The translational-pairing claim — **you are right, I was wrong twice, and it is fixed**

This is your acute-module §3, and it lands on a file in *this* partition, so I am
answering it here as well as there.

My `corpus-overview` carried this under *What is distinctive about this dataset*:

> **Matched in-vitro / in-vivo pairs.** 181 compounds carry both a mouse
> intracerebroventricular acute-tolerability score and a calcium-oscillation score
> in primary cortical neurons… The challenge asks for data that can *"bridge the
> differences between predictions that are primarily based on data from
> animal-based studies to data collected by in vitro human-based systems"*, and
> matched pairs are the form that request takes.

Two errors, both confirmed by reading the data rather than by accepting your note:

1. **The in-vitro arm is rat.** `doi:10.1089/nat.2021.0071` contributes 181
   `animal_invivo` mouse rows and 176 `in_vitro` **rat** rows. Your sentence —
   *"This is animal-to-animal pairing. It should not be described as an established
   bridge from human laboratory systems to animal outcomes"* — is exactly right, and
   quoting the brief's "in vitro human-based systems" beside an animal-to-animal
   panel was the single most overstated claim in my documentation.
2. **181 is the wrong number even for the animal pairing.** 181 is the in-vivo row
   count. The molecules appearing in **both** arms number **141**.

Rewritten in both `corpus-overview` copies and in `methodology.md §4.5`, naming the
species of each arm, giving 141, and recording where the correction came from. The
panel is still worth having — a matched in-vivo/in-vitro contrast on
sequence-resolved molecules is scarce — but on its own terms.

**And here is what the corpus can actually claim**, computed by
`scripts/cross_system_pairs_cns.py` rather than asserted, by identity *and* by
canonical sequence so that one molecule curated twice under two ids is not missed:

| Molecules measured in both… | Count |
|---|---:|
| animal in vivo **and** animal laboratory | 193 |
| animal in vivo **and** human clinical | 12 |
| **human laboratory and animal laboratory** | **2** |
| **human laboratory and animal in vivo** | **0** |
| **human laboratory and human clinical** | **1** |

Zero. Not one molecule in this corpus is measured in both a human laboratory system
and an animal in-vivo study. The classification you asked for — exact compound,
related analogue, mechanistic context — has almost nothing to classify, and saying
so is the honest answer to your question.

The three that do exist are worth naming:

- **APOE ASO-1** and **TREM2 ASO-171**, each in human iPSC-derived microglia and
  human whole blood ex vivo *and* on a rat primary-neuron multi-electrode array.
  Exact compound, different endpoint: human readouts are cytokine release and
  off-target DEGs, the rat readout is firing rate and burst duration. A mechanistic
  context pairing, not a predictive one.
- **valeriasen**, an n-of-1 ASO tested in the patient's own *KCNT1* p.R474H
  iPSC-derived neurons and then given to that patient. The human in-vitro assay
  found no injury — grade 0 on off-target transcriptomics and on neurite
  morphology — and the patient went on to grade-3 raised intracranial pressure and
  status dystonicus. One molecule is not evidence about predictive transfer in
  either direction. But it is the only human-laboratory-to-human-clinical pair in
  the corpus, and it is **discordant**, which is a more useful thing to put in front
  of German than a concordant one would have been.

### 4c. Modelling claims — **NOT APPLICABLE to this branch**

You ask me to reassess predictive analyses after eligibility changes, keep
correlated records grouped, and avoid claiming chronic sequence prediction because
the dataset is large. There is **no predictive analysis on this branch** — no
`ml/`, no analysis set, no model, no reported score. The deliverable here is a
dataset, stated as such in the corpus overview. Nothing to reassess, and no claim
to withdraw.

Your warning is nonetheless recorded as a constraint on whoever builds one, because
the numbers above make it sharp: any CNS sequence-toxicity model trained on this
corpus would be learning from **141 molecules in one animal-to-animal panel plus
two patent panels**, with 33% sequence coverage in the human laboratory subset and
18 compounds across 27 human trials. Grouped splits on trial, compound and
publication are not a refinement there; without them the result is leakage.
`event_cluster` and `trial_key` exist partly to make such grouping possible.

### 4d. Documentation consistency — **ACCEPTED, and it was worse than you flagged**

Your acute §4 notes a readme describing an older release. The same class of defect
was here, in a different form: the `corpus-overview` documents cited
`data/cns_oligos.csv`, `data/cns_measurements.csv`, `schema-cns.md` and
`METHODOLOGY-CNS.md` — **four paths that do not exist on this branch**, left over
from before the per-toxicity split — and reported pre-split merged-corpus counters
inside per-endpoint files. Six shared documents are duplicated into both CNS
endpoints under this repository's self-contained-per-toxicity layout, and a
generator had written only the master copy, so the duplicate carried a stale row
count.

Fixed: paths corrected, counters updated, and `scripts/sync_shared_cns_docs.py`
now rewrites every duplicate from its master with a banner naming both, with a
`--check` mode so a stale duplicate fails rather than surprises. The per-endpoint
evidence tables are no longer transcribed at all —
`scripts/build_evidence_tables_cns.py` writes them **in place** between markers in
the dossier, so the numbers in the prose are the numbers in the data by
construction.

---

## 5. Additional findings from my own review, not in your proposal

1. **54 grade-0 rows were not negatives.** Your hydrocephalus §1 is about
   spontaneous-reporting zeros. This branch has no pharmacovigilance rows at all,
   so that specific finding does not transfer — but the *category error* was here in
   a different guise, and your framing is what made me go looking. Three rows'
   entire readout was a CNS warning **not appearing** in a label
   (`CNS_warning_absent_from_label`, graded 0). Four cited a label section that
   reports no CNS endpoint at all — and one of those, `CMS1214`, says so in its own
   notes: *"Section 13.1 states carcinogenicity studies have not been conducted…
   no CNS or neurobehavioral endpoint is reported."* An endpoint never assessed was
   standing as evidence of no toxicity. Four more rest on an adverse-event table
   that lists only terms above a frequency cut-off, where absence may be a
   reporting artefact. 43 more could not be resolved from the row's own source
   fields at all. All of them are kept with their evidence and excluded from
   negative counts by one predicate, `negative_eligible=FALSE`. Corpus-wide the
   split is **1,186 grade-0 rows eligible, 60 not** — 48 of the ineligible in this
   partition, 12 in hydrocephalus, where the hydrocephalus response describes two
   further reasons a well-measured zero is still not a negative. `scripts/qc_cns.py` fails if `negative_eligible` ever disagrees with
   `ascertainment`, so regeneration cannot restore the misleading classification —
   which is your completion check, met.
   
   One row deserves separate mention as the clean case: `CMS1215` keeps its
   negative, because the label's clinical-trials-experience section was read in
   full, prints every adverse reaction observed with denominators (n=18 vs placebo
   n=11), and contains no neurologic term. An exhaustive table with a denominator
   is a weak negative; a missing warning is not a negative at all.

2. **The `human_trial_sponsor` tier is thinner than its row count suggests.** 62
   rows come from medical-affairs slide decks, press releases and a conference
   report. 21 of them carry no extractable quantity — "statistically significant
   versus placebo; magnitude not given", "favourable safety profile", "most adverse
   events". They are flagged `ascertainment=review_required` and excluded from
   negatives. I would not put them in front of German as trial evidence without
   that caveat attached.

3. **A trial's extension protocol is flagged, but not linked to its parent.** 5 of
   the 27 trials describe themselves as a roll-over, open-label extension or LTE —
   NCT03842969 is the tominersen roll-over, NCT03070119 the tofersen extension. The
   flag is read from each source's own wording. **No source row names the parent
   trial's registry identifier**, so the parent-child link is not recorded, and I
   will not infer it. Participants in those cohorts overlap their parent studies'
   and their events are not independent. Listed as a blocker in §6.

---

## 6. Blockers, owners, and what German should decide

**For German — scientific judgement required:**

1. **Chronic eligibility per row** (§2). Does `chronic_eligibility` get added, with
   what categories, and who adjudicates the 522 candidate rows? Until then the
   chronic/acute boundary rests on four columns and a documented rationale, not on
   a per-row determination.
2. **Grade calibration across evidence classes.** Is a grade-2 serious adverse
   event in a registry posting the same "2" as a grade-2 histopathology finding in a
   patent panel? Every grade here is marked provisional precisely because I do not
   think that question is settled.
3. **The valeriasen discordance** (§4b). A human iPSC assay found no injury in the
   molecule that then caused grade-3 raised intracranial pressure in the patient
   those cells came from. One case. Does it belong in the submission as a cautionary
   human-to-human pair, and how should it be framed?
4. **The 21 unquantified sponsor rows** (§5.2). Keep as flagged qualitative
   evidence, or drop from the release?

**For Oscar — scope and release decisions:**

5. **Which CNS dataset is the submission** (§0). Three lineages, no shared history
   with the default branch. This is the largest risk in the handoff and no proposal
   addresses it.
6. **The default branch still says this endpoint is unaddressed** (§0.2). It needs
   correcting wherever the team treats as canonical, independently of which dataset
   wins.

**Mine, and bounded:**

7. Recover registry identifiers for the 19 pending trial candidates by reading each
   publication's registration statement. Moves 19 trials from pending to verified
   without inventing an identifier.
8. Recover parent-trial links for the 5 extension protocols (§5.3), from source.
9. Resolve the 43 corpus-wide `review_required` ascertainments where the source may settle it.
10. Human-subset characterization (§3): 26 of 39 human-laboratory molecules lack a
    published sequence. Each gap needs a named recoverable source lead or an honest
    "not published".
11. Purity and analytical identity are absent for every molecule in the corpus
    (§3). A schema field is pointless until there is evidence to put in it; the task
    is finding whether any source reports batch characterization at all.

---

## 7. Files changed

| File | Change |
|---|---|
| `notes/cns/corpus/cns_measurements.csv` | 7 derived columns; 2 duplicate rows removed (2,540 → 2,538) |
| `chronic-neurotoxicity.measurements.csv` | regenerated by the split (2,393 rows × 32) |
| `hydrocephalus.measurements.csv` | regenerated (147 → 145 rows × 32) |
| `chronic-neurotoxicity.trials.csv` | **new** — 27 verified trials |
| `chronic-neurotoxicity.trials-pending.csv` | **new** — 19 pending candidates |
| `hydrocephalus.trials.csv` / `.trials-pending.csv` | **new** — 12 verified, 7 pending |
| `chronic-neurotoxicity.md`, `hydrocephalus.md` | human-first evidence section, generated in place |
| `*.corpus-overview.md` (both copies) | 181-pair claim rewritten; counters, paths and the grade-0 discussion corrected |
| `*.methodology.md` (both copies) | §4.5 pairing described as animal-to-animal, 141 molecules |
| `*.schema.md` (both copies) | derived columns documented, with the rule `negative_eligible` enforces |
| `*.sources.md` (both copies) | regenerated |
| `README.md` | human-first cross-endpoint table; non-additivity of trial counts stated |
| `scripts/classify_evidence_cns.py` | **new** — derives the 6 columns |
| `scripts/build_trial_register_cns.py` | **new** — the trial registers |
| `scripts/dedupe_cross_lane_cns.py` | **new** — adjudicated cross-lane duplicates |
| `scripts/cross_system_pairs_cns.py` | **new** — what bridges what |
| `scripts/build_evidence_tables_cns.py` | **new** — writes evidence tables in place |
| `scripts/sync_shared_cns_docs.py` | **new** — keeps duplicated docs identical |
| `scripts/qc_cns.py` | 4 new rule families: human/animal firewall, negative eligibility, trial-key integrity, cross-lane duplicates |

## 8. Validation

```
qc_cns.py                           0 errors, 1 pre-existing warning
split_by_endpoint.py --check        2,393 + 145 + 111 = 2,649, disjoint and exhaustive
classify_evidence_cns.py --check    on-disk classification matches
build_trial_register_cns.py --check registers on disk match
build_evidence_tables_cns.py --check  both dossiers up to date
sync_shared_cns_docs.py --check     all 6 duplicated documents in sync
dedupe_cross_lane_cns.py --dry-run  0 rows to remove, no unadjudicated groups
dataset_stats_cns.py --check-docs   0 mismatches
molecule_crosswalk                  18 molecules, 0 sequence conflicts
```

Every pass is idempotent: re-running changes nothing. Original evidence is
preserved — no row's curated values were edited by this work except the two
adjudicated duplicate removals, and the 6 derived columns can be deleted and
regenerated without loss.

---

Thank you for the review. The 181-compound correction in §4b was worth the whole
exchange: it was the most overstated sentence in my documentation, it had been
read by reviewers without anyone catching it, and it was wrong in two independent
ways. §0 is the part I need read back — the three-lineage problem is not something
I can solve from inside one branch.

---
_Generated by [Claude Code](https://claude.ai/code)_
