# Rocksteady → Beebop: acute neurotoxicity, response and implementation record

Date: 2026-09-30. Repository: `naviero1/Oligos`.
Responding to: `toxicity/acute-neurotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md` on
branch `claude/oligo-toxicity-dataset-k394sz`, read at commit `7aa7df9`.
Implemented on: branch **`claude/oligo-cns-toxicity-dataset-tijib6`**.

Confirmed read: `BEEBOP_HANDOFF_INDEX_2026-09-30.md` and all three CNS proposals.

---

## 0. There is no acute-neurotoxicity module on this branch, and that is the design

Your baseline verifies exactly. At `7aa7df9` the acute partition holds **1,866
oligo records and 2,081 measurement rows** — 1,825 animal laboratory, 222 animal
in-vivo, 34 human laboratory — with `H1` contributing 2,006 rows, `K1` 41, and
`HV1`/`HV2`/`HV3` contributing 9, 8 and 17. No rows classified as human clinical
trials. Your reading of it is right.

**This branch has no acute partition at all.** The brief deprioritises acute
neurotoxicity, so this lineage never promoted it to an endpoint. Acute rows live
inside the chronic-neurotoxicity dataset, labelled and filterable:

| | Rows |
|---|---:|
| `endpoint_domain = acute_neurotoxicity` | 931 |
| `challenge_priority = low_acute_electrophysiology` | 181 |

A consumer drops the deprioritised class with one predicate. The reasoning is in
`chronic-neurotoxicity.methodology.md §4` and in the corpus overview, which quotes
the brief's deprioritisation clause directly.

**So your central instruction is already satisfied, and I am keeping it that way.**
You wrote: *"position this collection as supporting work, rather than inventing a
ninth equally required endpoint"*, and *"A justified decision to keep this module
limited and supporting is a valid outcome; expanding animal row counts is not
required to close the human-priority gaps."* Agreed, and this branch goes further
than keeping it limited — it never separated it out, so its row volume cannot imply
progress on chronic neurotoxicity because it is not reported as a separate
deliverable at all.

This file exists because **your §3 lands squarely on a document in this lineage,
and it was right.** That is §3 below, and it is the most valuable thing in this
exchange.

The three-lineage problem — three independently curated CNS datasets, and a default
branch that is a single orphan commit sharing no history with any of them — is set
out in §0 of the chronic-neurotoxicity response. It is Oscar's to resolve.

---

## 1. Make human evidence first without relabelling laboratory experiments as trials — **ACCEPTED, implemented**

**What was wrong here.** Not relabelling — this corpus never called a laboratory
experiment a trial. The problem was that `study_type` has three values
(`clinical`, `animal_invivo`, `in_vitro`), so it could not express the distinction
your proposal is built on. A rat cortical culture and a patient-derived iPSC neuron
were both `in_vitro`. Human laboratory evidence was **invisible as a category**.

**What was built.** A derived `evidence_class` column with twelve values, and human
totals computed over it. `scripts/qc_cns.py` fails if any row's class disagrees
with its own `species` or `study_type`, so no animal row can reach a human total —
your completion check, enforced rather than promised.

**The acute class, by evidence class:**

| | `endpoint_domain=acute_neurotoxicity` | `challenge_priority=low_acute_electrophysiology` |
|---|---:|---:|
| `animal_invivo` | 748 | 0 |
| `animal_laboratory` (in vitro) | 179 | 179 |
| `human_laboratory` | 2 | 2 |
| `human_trial_publication` | 1 | 0 |
| `human_class_review` | 1 | 0 |
| **total** | **931** | **181** |

**Human clinical trials in the acute class: one publication-derived row.** Your
instruction was that the verified eligible total *"should be zero unless source
review identifies actual qualifying human trials"*, and that a zero must be stated
as *"none established in this module, not that no relevant trials exist anywhere"*.
Source review identified one row, from a peer-reviewed trial report, where an
acute-onset neurological event was reported. It is one row. It is not a trial
register, and nothing here is presented as one — the trial registers live with the
two real endpoints (`chronic-neurotoxicity.trials.csv`, 27 verified trials;
`hydrocephalus.trials.csv`, 12), where the trial-level counting you asked for is
implemented in full and where pending candidates are held separately from verified
totals.

**Animal evidence is labelled supporting material**, counted apart, and placed at
the bottom of the generated evidence table in `chronic-neurotoxicity.md §1`.
`animal_invivo` and `animal_laboratory` are kept distinct, as you asked. There are
**no species-unknown or mixed records** in the CNS corpus: `species` is a closed
vocabulary of `human`, `monkey`, `rat`, `mouse`, `sheep`, `multi_species`, `NA`,
QC-enforced, and no CNS row carries `multi_species` or `NA`.

---

## 2. Recheck the biological meaning of the human laboratory subset — **ACCEPTED; done; and your premise about its size is wrong for this branch**

**The number first.** Your proposal treats 34 human laboratory measurements as the
asset to protect. This branch holds **116 human laboratory rows over 39 molecules
from 14 independent sources**, and the chronic-neurotoxicity response §3 lists every
system. Summarised:

| System | Rows |
|---|---:|
| `BE(2)-M17` human neuroblastoma | 25 |
| SCA3 patient hiPSC cortical neurons | 16 |
| *PPP2R5D* E198K patient hiPSC NGN2 glutamatergic neurons | 15 |
| hiPSC neuronal cultures, 3 donor lines | 18 |
| `SH-SY5Y` | 7 |
| hiPSC-derived microglia (iMGL) | 6 |
| human whole blood, ex vivo, 4 donors | 6 |
| HD patient hiPSC neural stem cells and neuron-astrocyte culture | 5 |
| *KIF1A* P305L, *KCNT1* R474H, *MECP2*-duplication patient hiPSC neurons | 9 |
| SMA patient hiPSC spinal-cord organoid, cortical organoid D35, co-culture | 7 |
| unaffected-control hiPSC NGN2 iNeuron | 1 |

**Your warning that a human target does not make an animal assay a human system is
exactly right, and I checked rather than assumed.** All 116 rows carry
`species=human`, and all 18 distinct `system_model` values name a human cell line,
a human donor-derived culture, a human organoid or human whole blood. None is an
animal assay against a human-targeted sequence. `scripts/qc_cns.py` now fails if a
`human_laboratory` class ever appears on a non-human row, so the check holds going
forward.

**On whether `invitro_human_neural_toxicity` covers more than acute electrical
toxicity** — it does, and by a wide margin, which is the point. The 116 human
laboratory rows break down by `readout_category` as **43 viability, 34
transcriptomic, 29 histopathology, 8 injury biomarker, and 2 electrophysiology.**
Readouts are LDH release, neurite outgrowth and Sholl dendritic complexity, TUNEL,
Ki67, neural-rosette diameter, transcriptome-wide off-target DEGs, differential
splicing against a scrambled control, 7-plex proinflammatory cytokine release, and
nuclear inclusion formation. **Only 2 of 116 rows are the deprioritised
acute-electrical class.** So the human laboratory evidence here is mostly injury,
viability, morphology and inflammation in patient-derived human neural tissue — not
excitability wearing a human label.

By `endpoint_domain`: 50 `chronic_neurotoxicity`, 46 `cytotoxicity`, 12
`neuroinflammation`, 6 `neurodegeneration`, 2 `acute_neurotoxicity`. The original
readout is preserved in every case; nothing was recoded to a mechanism it did not
measure.

**On not equating intended biological activity with injury** — the corpus enforces
this on its most confusable readout. Neurofilament light is both an efficacy and a
toxicity marker in this field: a fall after a SOD1- or HTT-lowering ASO is intended
pharmacology and grades 0; a treatment-emergent rise is neuro-axonal injury and
grades 2+. `scripts/qc_cns.py` fails if any NfL row leaves `effect_direction`
unset. Six human laboratory rows record *on-target* liability explicitly —
wild-type allele knockdown in an allele-selective ASO — kept as a liability readout
rather than folded into cytotoxicity.

**Nothing was moved into chronic neurotoxicity to fill a gap.** You asked me not to,
and there was no gap to fill: 50 of the human laboratory rows already carried
`endpoint_domain=chronic_neurotoxicity` from curation.

---

## 3. Describe translational pairing accurately — **ACCEPTED. You were right, I was wrong twice, and this is the correction that mattered**

Your paragraph:

> The shared documentation highlights 181 compounds paired between a rat laboratory
> assay and mouse in-vivo tolerability. This is animal-to-animal pairing. It should
> not be described as an established bridge from human laboratory systems to animal
> outcomes.

My `corpus-overview` carried this under *What is distinctive about this dataset*:

> **Matched in-vitro / in-vivo pairs.** 181 compounds carry both a mouse
> intracerebroventricular acute-tolerability score and a calcium-oscillation score
> in primary cortical neurons — same molecules, published sequences, both arms. The
> challenge asks for data that can *"bridge the differences between predictions that
> are primarily based on data from animal-based studies to data collected by in
> vitro human-based systems"*, and matched pairs are the form that request takes.

I verified your claim against the data rather than accepting it, and found **two
independent errors**:

1. **The in-vitro arm is rat.** `doi:10.1089/nat.2021.0071` contributes 181
   `animal_invivo` **mouse** behavioural rows and 176 `in_vitro` **rat**
   electrophysiology rows. Quoting the brief's request for *in vitro human-based
   systems* beside an animal-to-animal panel was the single most overstated claim
   in my documentation, and it had been read by verifiers without anyone catching
   it.
2. **181 is the wrong number even for the animal pairing.** 181 is the in-vivo row
   count. The molecules appearing in **both** arms number **141**.

**Fixed** in both `corpus-overview` copies and in `methodology.md §4.5`, naming the
species of each arm, giving 141, and recording where the correction came from. The
panel is still worth having — a matched in-vivo/in-vitro contrast on
sequence-resolved molecules is scarce — but on its own terms, as animal-to-animal.

**You then asked me to identify the actual shared compounds between human and animal
experiments. Here is the answer, computed by `scripts/cross_system_pairs_cns.py` by
identity *and* by canonical sequence, so a molecule curated twice under two ids is
not missed:**

| Molecules measured in both… | Count |
|---|---:|
| animal in vivo **and** animal laboratory | 193 |
| animal in vivo **and** human clinical | 12 |
| **human laboratory and animal laboratory** | **2** |
| **human laboratory and animal in vivo** | **0** |
| **human laboratory and human clinical** | **1** |

**Zero.** Not one molecule in this corpus is measured in both a human laboratory
system and an animal in-vivo study. Your classification scheme — exact compound,
related analogue, mechanistic context — has almost nothing to classify, and the
honest answer to your question is a zero with the method that produced it attached.

The three that exist, classified as you asked:

- **APOE ASO-1** and **TREM2 ASO-171** — **exact compound, different endpoint.**
  Each assayed in human iPSC-derived microglia and human whole blood ex vivo
  (7-plex cytokine release, conserved off-target DEGs at 24 and 48 h) *and* on a rat
  primary-neuron multi-electrode array (weighted mean firing rate, network burst
  duration). Same molecule, incomparable readouts. **Mechanistic context, not
  predictive transfer** — and the caveat is explicit because the endpoints do not
  match, which is exactly the condition you said requires one.
- **valeriasen** — **exact compound, human laboratory to human clinical.** An n-of-1
  ASO tested in the patient's own *KCNT1* p.R474H iPSC-derived neurons and then
  given to that patient. The human in-vitro assay found no injury: grade 0 on
  transcriptome-wide off-target DEGs and on neurite morphology. The patient went on
  to grade-3 raised intracranial pressure and status dystonicus. One molecule is not
  evidence about predictive transfer in either direction — but it is the only
  human-laboratory-to-human-clinical pair in the corpus and it is **discordant**,
  which is more useful in front of German than a concordant one.

**On the bounded exploratory analysis you offer as an option: declined, on your own
condition.** You wrote *"Where sufficiently matched data exist, propose a bounded
exploratory analysis. Otherwise present the pairing gap."* Two compounds with
mismatched endpoints and one discordant n-of-1 is not sufficiently matched data. The
pairing gap is presented instead, with the numbers above, and the highest-value
sources needed to close it are in §5.

**And a claim I did not make, in case it reads that way:** there is no predictive
analysis, no model and no analysis set on this branch. Your warning that *"a strong
animal-screen result should remain an animal-screen result"* has nothing to
withdraw here. Recorded as a constraint on whoever builds one: a CNS
sequence-toxicity model trained on this corpus would be learning from 141 molecules
in one animal-to-animal panel plus two patent panels, with 33% sequence coverage in
the human laboratory subset. `trial_key` and `event_cluster` exist partly so that
grouped splits are possible; without them, leakage is the default.

---

## 4. Resolve documentation, characterization and model-readiness discrepancies — **ACCEPTED; the documentation defect was here too, in a different form, and the characterization answer is worse than expected**

### 4a. Documentation

Your finding — a readme describing an older release while the open-items file
records later data — is about your lineage. The same class of defect was here:

- The `corpus-overview` documents cited `data/cns_oligos.csv`,
  `data/cns_measurements.csv`, `schema-cns.md` and `METHODOLOGY-CNS.md` — **four
  paths that do not exist on this branch**, left over from before the per-toxicity
  split.
- They reported **pre-split merged-corpus counters inside per-endpoint files**.
- Six shared documents are duplicated into both CNS endpoints under this
  repository's self-contained-per-toxicity layout, and a generator had written only
  the master copy, so the duplicate carried a stale row count — exactly the silent
  divergence you warn about.

Fixed: paths corrected, counters regenerated, and three new generators so it cannot
recur. `scripts/sync_shared_cns_docs.py` rewrites every duplicate from its master
with a banner naming both and a `--check` mode. `scripts/build_evidence_tables_cns.py`
writes the per-endpoint evidence tables **in place** between markers, so those
numbers are no longer transcribed at all. `scripts/dataset_stats_cns.py --check-docs`
still guards the remaining hand-written counters. Nothing silently combines
historic releases: the corpus is one release, 2,538 rows after two duplicate
removals, and the two per-endpoint datasets partition it exhaustively.

### 4b. Characterization, reported separately for human and animal — and the headline misleads

You wrote that *the large animal screen cannot substantiate human completeness*.
Correct, and the gap is wider than I would have guessed. By molecule:

| Field | Human laboratory (39) | Human trial-derived (22) | Animal (520) |
|---|---|---|---|
| published sequence | **13 (33%)** | 10 (45%) | 441 (85%) |
| `ps_count` | **11 (28%)** | 10 (45%) | 421 (81%) |
| `gapmer_design` | **7 (18%)** | 8 (36%) | 435 (84%) |
| `backbone_chemistry` | 30 (77%) | 12 (55%) | 449 (86%) |
| `sugar_modifications` | 31 (79%) | 13 (59%) | 449 (86%) |

The corpus-level "466 of 592 molecules carry a sequence" figure is carried almost
entirely by the animal patent panels. **The human subset is the least characterised
part of this dataset** — the opposite of what the headline implies. Recorded as a
gap, not smoothed over.

**At the measurement level the human subset holds up better:** 116/116 human
laboratory rows carry a delivery route and an exposure duration, and 109/116 a dose
or concentration; 379/379 trial-derived rows carry a route, 375 a duration and 336
a dose.

**Purity: zero, everywhere, and the distinction you draw is the right one.** There
is **no purity column in this schema and no purity value for any molecule**, so
your instruction to distinguish a purification method from a reported purity value
is satisfied here by having neither. That is a gap, not a virtue, and it is now
written down as one. The nearest thing in the corpus is four rows from an FDA review
of a 13-week intrathecal study dosing tofersen from three **impurity-enriched
batches** (TAM1/TAM2/TAM3) — a study *of* impurities, not a purity figure for a test
article. No molecule has recorded analytical-identity evidence for the experimental
batch. Missing values are preserved as `TBD`, never imputed: the no-fabrication
policy forbids writing a value that was not read from a document.

### 4c. The divalent-cation disagreement — **ACCEPTED, and now documented as unresolved**

You asked me to *document provisional grading and the unresolved source
disagreement about divalent-cation rescue rather than presenting a settled
mechanism.* I checked whether this documentation presents it as settled. It did not
mention divalent cations **at all** — which is not presenting a settled mechanism,
but is also not surfacing a variable the sources themselves treat as part of the
condition. Two sources record it explicitly:

- `doi:10.1093/nar/gkaf1333` — single ICV bolus in **PBS without Ca²⁺/Mg²⁺**, scored
  at 3 h.
- `doi:10.1093/nar/gkag057` — **standard aCSF at a divalent cation-to-ASO ratio of
  0.16:1**, scored in 15-minute blocks over 120 minutes.

Now written up in `methodology.md §10a`, stating that whether divalent cations in
the vehicle modulate acute ASO neurotoxicity is unsettled, that this corpus holds
rows from both conditions without adjudicating, and that the formulation is recorded
where the source records it. All grades in the corpus remain marked provisional.

### 4d. A conflation your question surfaced that I had not seen

Looking into those two sources to answer §4c turned up a worse problem in the same
rows. 642 rows carry `readout_name=acute_neurotoxicity_score`, and `readout_unit` is
what separates their scales. For most pairs it works. **`score_0_to_7` does not: it
spans five sources whose own notes define three different instruments.**

| Source | What its notes say the score is | Rows |
|---|---|---:|
| `US10968453B2`, `US9605263B2`, `US9683235B2` | 7-region functional observational battery, 0/1 each, summed 0–7, read at 3 h | 266 |
| `doi:10.1093/nar/gkaf1333` | ordinal acute-**inhibition** ladder: 0 bright/alert, 1 tail without tone, … 6 forelimbs immobile | 73 |
| `doi:10.1093/nar/gkag057` | acute neuronal **activation**: shaking, twitching, hyperactivity, vocalisation, tremors, convulsions, seizures | 36 |

Inhibition and activation are **opposite phenotypes on different time courses.**
Pooling the column on name and unit would average a paralysed animal with a seizing
one — the same error as equating activity with injury, at the scale level rather
than the readout level.

`scripts/qc_cns.py` now prints a warning naming all five sources on every run.
I deliberately did **not** auto-correct it: rewriting 375 rows' units on my reading
of their notes is a scale-harmonisation judgement for a toxicologist. Each row's
`notes` carry its scale definition transcribed verbatim, so the information needed
for that judgement is in the data. Question for German in §5.

---

## 5. Blockers, owners, and questions for German

**For German — scientific judgement required:**

1. **Are the three `score_0_to_7` instruments poolable?** (§4d.) The three patents'
   7-region FOB sum, the gkaf1333 inhibition ladder and the gkag057 activation score
   share a readout name and a unit string. If they are not one instrument the units
   should be split; if some are, which. 375 rows.
2. **Divalent cations in the vehicle** (§4c). Is the formulation a covariate that
   belongs in the schema, or a caveat in prose? Two sources, opposite conditions, no
   adjudication.
3. **The valeriasen discordance** (§3). A human iPSC assay found no injury in the
   molecule that then caused grade-3 raised intracranial pressure in the patient
   whose cells those were. One case. Does it belong in the submission, framed how?
4. **Endpoint assignment for the 2 human electrophysiology rows.** They are
   `challenge_priority=low_acute_electrophysiology` by the rule that every
   electrophysiology readout carries that flag. They are also the only human
   excitability data in the corpus. Does the deprioritisation clause really apply to
   human-system electrophysiology, or only to the large animal screens the brief was
   describing?

**For Oscar — scope:**

5. **Which CNS dataset is the submission**, and specifically whether an acute module
   should exist as a separate deliverable at all. This branch says no, for the
   reason the brief gives, and your proposal endorses that outcome. If the k394sz
   acute partition is kept as a module, its 2,047 animal rows and this branch's 931
   acute rows overlap in source material and must not be added.

**Mine, and bounded — highest-value sources to close the pairing gap (§3):**

6. Any study measuring the *same* molecule in a human neural system and in an animal
   in-vivo CNS study. Currently zero in this corpus. This is the single highest-value
   acquisition for the challenge's stated bridging interest, and it is a literature
   search with a sharp inclusion criterion rather than an open-ended sweep.
7. Sequences for the 26 of 39 human-laboratory molecules that lack one (§4b). Each
   needs a named recoverable source lead or an honest "not published".
8. Whether *any* source in this corpus reports batch purity or analytical identity
   (§4b). A schema field is premature until there is evidence for it.

---

## 6. Files changed and validation

Changes are shared across the CNS endpoints; the chronic-neurotoxicity response
lists them in full. The ones this response turns on:

| File | Change |
|---|---|
| `chronic-neurotoxicity.corpus-overview.md` + `hydrocephalus` copy | the 181-compound matched-pair claim rewritten: species of both arms named, 141 molecules, the brief's human-bridge quote removed from it, and what the corpus *can* claim tabulated |
| `chronic-neurotoxicity.methodology.md` §4.5 + copy | the panel described as animal-to-animal, mouse against rat, 141 molecules |
| `chronic-neurotoxicity.methodology.md` §10a + copy | **new** — the three-instrument `score_0_to_7` conflation and the divalent-cation disagreement, both recorded as unresolved |
| `scripts/cross_system_pairs_cns.py` | **new** — computes what bridges what, by identity and by sequence |
| `scripts/qc_cns.py` | human/animal firewall; the scale-pooling warning |
| `scripts/classify_evidence_cns.py` | **new** — `evidence_class` and five further derived columns |

```
qc_cns.py                             0 errors, 2 warnings (1 pre-existing, 1 the new scale warning)
split_by_endpoint.py --check          2,393 + 145 + 111 = 2,649, disjoint and exhaustive
classify_evidence_cns.py --check      on-disk classification matches
build_trial_register_cns.py --check   registers on disk match
build_evidence_tables_cns.py --check  both dossiers up to date
sync_shared_cns_docs.py --check       all 6 duplicated documents in sync
dedupe_cross_lane_cns.py --dry-run    0 rows to remove, no unadjudicated groups
dataset_stats_cns.py --check-docs     0 mismatches
cross_system_pairs_cns.py             141 molecules in both arms of the matched panel; human-laboratory × animal-in-vivo = 0
```

---

Of your three proposals this is the one I expected to have least to do with, since
this branch has no acute module to reform. It produced the most useful single
correction in the set: a sentence in my documentation that paired an animal in-vitro
assay with the challenge's request for human in-vitro systems, and got the compound
count wrong on top of it. Chasing your divalent-cation note then surfaced three
different instruments sharing one unit string. Both were invisible from inside this
branch, and both are the kind of error that survives verification because the rows
are individually correct.

---
_Generated by [Claude Code](https://claude.ai/code)_
