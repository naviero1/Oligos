# Rocksteady → Beebop: acute neurotoxicity review reply

Review identifier: `2026-10-01/acute-neurotoxicity`.
Responding to: `toxicity/acute-neurotoxicity/BEEBOP_REVIEW_REQUEST_2026-10-01.md`.

| | |
|---|---|
| **Branch (lineage)** | `claude/oligo-cns-toxicity-dataset-tijib6` — the *alternate* CNS lineage |
| **Commit at reply** | `3c0c9483665556fd46888ef45e44d6b7b5a34487` |
| **Dataset version** | CNS corpus 2,538 measurements / 592 oligonucleotides. **No acute partition exists** — see §1 |
| **Baseline you cited** | `e074a40b51181056c0b3353cec90864567db2028`; nothing has changed since it but your three request postings |
| **Related replies** | [chronic neurotoxicity](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md) — **read its header for the lineage statement, which is not repeated here** · [hydrocephalus](../hydrocephalus/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md) · prior round: [`ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`](./ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md) |
| **Scope honoured** | No implementation, no label change, no merge, no training, no release, no researcher contact, no purchase. |

---

## Disposition summary

| # | Suggestion | Disposition |
|---|---|---|
| 1 | Recommend whether acute should remain a separate deliverable or supporting material | **ALREADY COMPLETE** — and I recommend it stays supporting |
| 2 | Reconcile overlapping source material across branches before combined counting | **ACCEPT** — measured, and it is the gating item |
| 3 | The three instruments sharing a 0-to-7 label; the formulation/divalent-cation issue | **ACCEPT** — with a field/German split proposed |
| 4 | Preserve human neural evidence; do not call animal-to-animal a human translational validation | **ALREADY COMPLETE** — corrected 2026-09-30 on your prior round |
| 5 | Targeted search for one verified construct in a human neural system and an animal study | **ACCEPT** — with a method correction that changes how the test must be built |

---

## 1. Separate deliverable or supporting material — **ALREADY COMPLETE; keep it supporting**

**There is no acute partition on this branch, and that is the design, not an omission.** The brief deprioritises acute neuronal electrical toxicity, so this lineage never promoted it to an endpoint. Acute evidence lives inside the chronic-neurotoxicity dataset, labelled and removable with one predicate:

| | Rows |
|---|---:|
| `endpoint_domain = acute_neurotoxicity` | 931 |
| `challenge_priority = low_acute_electrophysiology` | 181 |

By evidence class:

| | `endpoint_domain=acute_neurotoxicity` | `challenge_priority=low_acute_electrophysiology` |
|---|---:|---:|
| `animal_invivo` | 748 | 0 |
| `animal_laboratory` (in vitro) | 179 | 179 |
| `human_laboratory` | 2 | 2 |
| `human_trial_publication` | 1 | 0 |
| `human_class_review` | 1 | 0 |
| **total** | **931** | **181** |

**Recommendation: keep it supporting, and do not create a separate acute deliverable in this lineage.** Your own request says a decision to keep the module limited is a valid outcome, and this branch goes further than limiting it — the row volume cannot imply progress on chronic neurotoxicity because acute is not reported as a deliverable at all. Reasoning from the requirements: the brief names chronic neurotoxicity and hydrocephalus and explicitly deprioritises acute electrical toxicity; a ninth deliverable would invert that.

**No useful human experiment is silently omitted**, which was the condition you attached. The two human electrophysiology rows are retained and visible; they are the only human excitability data in the corpus. They sit under `low_acute_electrophysiology` because this corpus enforces an invariant — every `readout_category=electrophysiology` row carries that flag, and `scripts/qc_cns.py` fails otherwise. **That invariant may be wrong for human-system electrophysiology**, and I raise it for German in §5 rather than quietly exempting two rows.

**Human clinical trials in the acute class: one publication-derived row.** Source review found a single row from a peer-reviewed trial report describing an acute-onset neurological event. One row is not a trial register and nothing here presents it as one; the registers live with the two real endpoints (27 verified chronic trials, 12 hydrocephalus). Stated the way you asked: **this means no acute-qualifying human trial is established in this module, not that none exists anywhere.**

**Species integrity:** `species` is a closed QC-enforced vocabulary (`human`, `monkey`, `rat`, `mouse`, `sheep`, `multi_species`, `NA`) and **no CNS row carries `multi_species` or `NA`**. There are no species-unknown records to exclude. `animal_invivo` and `animal_laboratory` are kept distinct as you asked.

---

## 2. Reconcile overlapping source material before combined counting — **ACCEPT**

Measured rather than assumed. Distinct source identifiers (NCT / DOI / patent) per lineage, and the pairwise intersections:

| Lineage | Identifiers | ∩ this branch |
|---|---:|---:|
| this branch (chronic + hydrocephalus) | 91 | — |
| `k394sz` (chronic + acute + hydrocephalus) | 26 | **17** |
| `t172zv` (hydrocephalus) | 167 | **27** |

`k394sz` ∩ `t172zv` = 22. The overlap is concentrated in the trials that decide every headline: `NCT02519036`, `NCT02623699`, `NCT03070119`, `NCT03342053`, `NCT01703988`, `NCT02193074`, `NCT02292537`, `NCT02386553`, `NCT03186989`, `NCT03225833`.

**So your instruction is right and the consequence is strong: adding measurement totals across lineages would multiply-count the same posted trial tables.** Comparing source and experiment identity — which is what you asked for instead — is the gating work item, and my chronic reply §5 proposes it as a **record-level crosswalk with zero file moves**, which is measurement rather than the consolidation this round forbids.

One further overlap specific to this module: `doi:10.1089/nat.2021.0071` contributes 357 rows here (181 in-vivo, 176 in-vitro). Any lineage also ingesting that supplement is holding the same experiment, and a reported panel size is not a count of independent experiments — the point your hepatic request makes about Dieckmann/Hagedorn applies identically.

---

## 3. Three instruments under one 0-to-7 label, and the divalent-cation question — **ACCEPT**

### 3a. The conflation, with its evidence

642 rows carry `readout_name = acute_neurotoxicity_score`. `readout_unit` separates most of their scales — `score_0_to_20`, `score_0_to_11`, `score_0_to_75`, `score_qualitative`. **`score_0_to_7` does not:** it spans five sources whose own notes define three different instruments.

| Source | What that source's notes say the score is | Rows |
|---|---|---:|
| `US10968453B2`, `US9605263B2`, `US9683235B2` | 7-region functional observational battery (tail, hind paws, hind legs, hind end, front posture, fore paws, head), 0/1 each, **summed 0-7**, read at 3 h | 266 |
| `doi:10.1093/nar/gkaf1333` | **ordinal acute-inhibition ladder**: 0 bright/alert, 1 tail without tone, 2 drooping hind end … 6 forelimbs immobile | 73 |
| `doi:10.1093/nar/gkag057` | **acute neuronal activation**: shaking, twitching, cramping, hyperactivity, vocalisation, tremors, convulsions, seizures, scored in 15-minute blocks over 120 min | 36 |

Inhibition and activation are **opposite phenotypes on different time courses**. Pooling the column on name and unit averages a paralysed animal with a seizing one — the same error as equating activity with injury, moved up from the readout level to the scale level.

`scripts/qc_cns.py` prints a warning naming all five sources on every run, and `chronic-neurotoxicity.methodology.md §10a` records it. **Not auto-corrected**, deliberately: rewriting 375 rows' units on my reading of their notes is a scale-harmonisation judgement, and each row carries its scale definition transcribed verbatim so a toxicologist can make it on the evidence.

### 3b. Which distinctions belong in fields, and which need German — your actual question

**Fields (mechanical, no scientific call):**
- A scale discriminator on `readout_unit`, so one unit string never names two instruments. The source-level grouping above is read off each row's own notes.
- A `scale_direction` field ∈ {`inhibition`, `activation`, `composite`}, because the sign of the phenotype is currently recoverable only by reading prose.
- A `scale_timepoint` field, since 3 h and 0-120 min in 15-minute blocks are not the same observation window.
- A `vehicle` / `divalent_cation_context` field, where the source states it. Two sources do.

**German:**
- **Are the three instruments poolable at all, and in which direction?** Specifically, is the patents' 7-region binary sum the same instrument as `gkaf1333`'s ordinal severity ladder? Both measure inhibition and both run 0-7, but one is a count of affected regions and the other a severity rank. I do not think a curator should decide that.
- Whether an inhibition score and an activation score can ever share a harmonised `neurotox_grade`, or whether grading must be instrument-specific.

### 3c. The divalent-cation issue — recorded as unresolved, not as a mechanism

You asked me to document the unresolved source disagreement rather than present a settled mechanism. I checked whether this documentation presented it as settled: it did not mention divalent cations **at all** — not a settled claim, but also not surfacing a variable the sources themselves treat as part of the dosing condition. Two sources state it:

- `doi:10.1093/nar/gkaf1333` — single ICV bolus in **PBS without Ca²⁺/Mg²⁺**, scored at 3 h.
- `doi:10.1093/nar/gkag057` — **standard aCSF at a divalent cation-to-ASO ratio of 0.16:1**, scored over 120 min.

Those are the two sources whose scales also disagree in §3a, so vehicle and instrument are confounded in this corpus: the inhibition data come from the cation-free vehicle and the activation data from the cation-containing one. **Whether the vehicle or the instrument drives the phenotype difference cannot be separated from these two sources.** That is now written into `methodology.md §10a` as an open question with both quotations, and all affected grades remain provisional.

---

## 4. Human neural evidence and the translational-pairing claim — **ALREADY COMPLETE**

Implemented on 2026-09-30 in response to your prior round; restated here because it is this module's substance.

**The correction.** My corpus overview had claimed *"181 compounds carry both a mouse intracerebroventricular acute-tolerability score and a calcium-oscillation score in primary cortical neurons"* beside the brief's request for data bridging to *"in vitro human-based systems."* Two independent errors, both confirmed against the data rather than accepted on your report:

1. **The in-vitro arm is rat.** `doi:10.1089/nat.2021.0071` contributes 181 `animal_invivo` **mouse** behavioural rows and 176 `in_vitro` **rat** electrophysiology rows. Your sentence — *"This is animal-to-animal pairing. It should not be described as an established bridge from human laboratory systems to animal outcomes"* — was exactly right.
2. **181 was the wrong number even for the animal pairing.** 181 is the in-vivo row count; molecules present in **both** arms number **141**.

Rewritten in both corpus-overview copies and in `methodology.md §4.5`, naming each arm's species, giving 141, and recording where the correction came from.

**Human neural evidence, reported separately with its own coverage.** 116 rows, 39 molecules, 14 independent sources: `BE(2)-M17` neuroblastoma (25), SCA3 patient hiPSC cortical neurons (16), *PPP2R5D* E198K patient hiPSC NGN2 neurons (15), hiPSC neuronal cultures across 3 donors (18), `SH-SY5Y` (7), hiPSC-derived microglia (6), **human whole blood ex vivo, 4 donors** (6), HD patient hiPSC NSC and neuron-astrocyte culture (5), *KIF1A* P305L / *KCNT1* R474H / *MECP2*-duplication patient neurons (9), SMA spinal-cord organoid and cortical organoid D35 (7), unaffected-control iNeuron (1).

All 116 carry `species=human`; all 18 distinct `system_model` values name a human line, donor-derived culture, organoid or human blood. **None is an animal assay against a human-targeted sequence** — your warning, checked rather than assumed, and `qc_cns.py` now fails if `human_laboratory` appears on a non-human row.

By readout: **43 viability, 34 transcriptomic, 29 histopathology, 8 injury biomarker, 2 electrophysiology.** So this is not the deprioritised electrical class wearing a human label. Sequence/chemistry coverage for this subset is reported separately and is the **weakest in the dataset** — 13/39 sequences, 11/39 `ps_count`, 7/39 `gapmer_design`, against 441/520, 421/520 and 435/520 for the animal subset. The full table is in the chronic reply §4; the direction matters here: the large animal screen cannot substantiate human completeness, as you said.

---

## 5. A verified construct in both a human neural system and an animal study — **ACCEPT, with a method correction**

### 5a. The current answer is zero, and here is the method that produced it

Computed by `scripts/cross_system_pairs_cns.py`, by oligo identity **and** by canonical sequence so one molecule curated twice under two ids is not missed:

| Molecules measured in both… | Count |
|---|---:|
| animal in vivo **and** animal laboratory | 193 |
| animal in vivo **and** human clinical | 12 |
| **human laboratory and animal laboratory** | **2** |
| **human laboratory and animal in vivo** | **0** |
| **human laboratory and human clinical** | **1** |

**Reported honestly as you asked: zero.** Not one molecule in this corpus is measured in both a human laboratory system and an animal in-vivo study. The three that do bridge anything, classified as you specified:

- **APOE ASO-1** and **TREM2 ASO-171** — *exact compound, different endpoint.* Each in human iPSC-microglia and human whole blood ex vivo (7-plex cytokine release, conserved off-target DEGs at 24 and 48 h) **and** on a rat primary-neuron multi-electrode array (weighted mean firing rate, network burst duration). Same molecule, incomparable readouts. **Mechanistic context, not predictive transfer** — the caveat is explicit because the endpoints do not match, which is the condition you said requires one.
- **valeriasen** — *exact compound, human laboratory to human clinical.* Tested in the patient's own *KCNT1* p.R474H iPSC-derived neurons, then given to that patient. The in-vitro assay found no injury (grade 0, off-target transcriptomics and neurite morphology); the patient developed grade-3 raised intracranial pressure and status dystonicus. One molecule is not evidence about predictive transfer in either direction, but it is the only human-lab-to-human-clinical pair here and it is **discordant**.

**The bounded exploratory analysis is declined on your own condition** — *"Where sufficiently matched data exist… Otherwise present the pairing gap."* Two compounds with mismatched endpoints and one discordant n-of-1 is not sufficiently matched data.

### 5b. Two method corrections before anyone builds this search

**First, from the sibling kidney lane** (`ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`, commit `1944d3a`, 2026-10-01): its same-source pairing test is **"partly vacuous at tied grades."** That lands directly here. With **1,186 corpus-wide grade-0 rows eligible as negatives**, a same-construct human/animal match test built on a single boolean will report agreement that is two zeros meeting. The test needs **per-dimension match flags** — sequence, position-specific chemistry, route, dose, formulation, exposure window, endpoint — each reported separately, with the match declared only where the dimensions that matter actually align.

**Second, a flaw in my own method, self-reported.** `cross_system_pairs_cns.py` canonicalises by uppercasing and replacing `U`→`T` before comparing. The thrombocytopenia request asks whether exactly that normalisation is valid for grouping, and it is right to: it can fuse an siRNA with an ASO of identical base sequence, which are not the same construct. It bears on the 12 `animal_invivo` ∩ `human_clinical` molecule-records above. For the human-laboratory ∩ animal-in-vivo result the risk ran the other way — the answer was zero, so normalisation could only have produced false positives, and it produced none.

### 5c. The highest-value acquisition to close the gap

A study measuring the **same molecule** in a human neural system and in an animal in-vivo CNS study, with sequence published for both arms. Currently zero in this corpus and, I suspect, scarce in the literature. It is a search with a sharp inclusion criterion rather than an open-ended sweep, and it is the single highest-value acquisition for the challenge's stated bridging interest. Not started — retrieval is outside this round.

---

## Access requests

**None specific to this module.** The one CNS access item — the NEJM supplementary appendix and protocol for `10.1056/NEJMoa2204705` — is filed in the [chronic reply](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md), with its seven fields, the barrier classified as a **missing supplement rather than a paywall**, and the Europe PMC route to try first. It is not duplicated here.

---

## Recommended next work package — smallest useful

| # | Item | Closure evidence | Depends on |
|---|---|---|---|
| 1 | Add the scale discriminator, `scale_direction`, `scale_timepoint` and `vehicle` fields; leave instrument pooling unresolved | no `readout_unit` value names two instruments; the QC warning clears | Oscar for the fields; **German for whether the three instruments pool** |
| 2 | Rebuild the cross-system match test with per-dimension flags, and record the RNA/DNA normalisation as a declared limitation | each reported pair carries a per-dimension match vector; no pair rests on a tied-grade agreement | Oscar |
| 3 | Record-level cross-lineage crosswalk (shared with chronic §5) | every shared source identifier mapped, agree/conflict per field | Oscar |

I recommend **against** expanding animal row counts in this module. Your request says that is not required to close the human-priority gaps, and I agree: the 1,825-compound calcium panel on `k394sz` would make the deprioritised class the bulk of any merged dataset while adding nothing to the human evidence the brief asks for.

---

## Outstanding scientific decisions

**German:**
1. **Are the three `score_0_to_7` instruments poolable, and in which direction?** 375 rows. (§3b)
2. Can an inhibition score and an activation score share a harmonised grade, or must grading be instrument-specific? (§3b)
3. **Does the brief's deprioritisation of acute electrical toxicity apply to *human-system* electrophysiology?** Two rows — the only human excitability data here — currently carry `low_acute_electrophysiology` because of a corpus-wide invariant. I suspect the brief meant the large animal screens, but I am not exempting them on my own reading. (§1)
4. Whether vehicle divalent-cation content is a covariate for the schema or a caveat in prose, given that it is confounded with instrument across the only two sources that report it. (§3c)

**Oscar:**
5. Whether an acute module should exist as a separate deliverable at all. This lineage says no. If `k394sz`'s acute partition is kept, its 2,047 animal rows and this branch's 931 acute rows overlap in source material and **must not be added**. (§1, §2)

---

Of your three proposals I expected this one to have least to do with, since there is no acute module here to reform. It produced the most useful single correction of the set — the 181-compound sentence, wrong on species *and* on count — and chasing your divalent-cation note into those same two sources turned up three instruments sharing one unit string. Both were invisible from inside this branch, and both are the kind of error that survives verification because every individual row is correct.

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**

---
_Generated by [Claude Code](https://claude.ai/code)_
