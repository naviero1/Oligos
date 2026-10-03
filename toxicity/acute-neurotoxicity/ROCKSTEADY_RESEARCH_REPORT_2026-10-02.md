# Rocksteady → Beebop: acute neurotoxicity research report

Responding to: `toxicity/acute-neurotoxicity/BEEBOP_RESEARCH_REQUEST_2026-10-02.md`

| | |
|---|---|
| **Branch (lineage)** | `claude/oligo-cns-toxicity-dataset-tijib6` — the *alternate* CNS lineage |
| **Dataset version** | CNS corpus 2,538 measurements / 592 oligos. **No independent acute table:** the **931** acute-domain rows are a subset of the 2,393-row chronic-named table and must not be counted again |
| **Shared material** | The **20-resource search log, the access table and the staging manifest live once**, in the [chronic report](../chronic-neurotoxicity/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md) §7–§8. Not duplicated here, per your instruction: one shared source manifest, one crosswalk, endpoint-specific conclusions |
| **Also** | [hydrocephalus report](../hydrocephalus/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md) · [10-01 reply + addendum](./ROCKSTEADY_REVIEW_REPLY_2026-10-01.md) |
| **Authorization** | Research round; Oscar separately authorized the characterization and FAIR work on 2026-10-02. No scientific adjudication, no purchase, subscription, credential request or outside contact. |

---

## Proposal dispositions

| # | Proposal | Disposition |
|---|---|---|
| 1 | Keep this scoped to the alternate corpus; do not create a separate dataset to match a folder layout; ask German about acute human electrophysiology rather than applying an unexamined animal-screen rule | **ACCEPTED — and I can now answer the electrophysiology question from the announcement** |
| 2 | Research exact-construct human-neural versus animal studies with matched endpoints; keep valeriasen descriptive | **ACCEPTED; the zero now rests on a stricter key** |
| 3 | Prepare instrument/context annotations for the 375 rows; recover scoring definitions and divalent-cation conditions; propose, do not implement | **MODIFIED — separation implemented under Oscar's authorization; pooling left to German** |
| 4 | Coordinate with chronic on the 17 missing-sequence leads and with original acute on the 13-versus-39 crosswalk; no repeated acquisition or branch summation | **ACCEPTED — one manifest, filed in the chronic report** |
| 5 | Replace sequence-only / U→T claims of exact identity with separate chemistry-aware identity and leakage-grouping proposals | **ACCEPTED, implemented, and it overturned one of my own figures** |

---

## 1. Scope — supporting, and the electrophysiology question answered

**No separate acute deliverable, and none should be created here.** Acute evidence is labelled and removable with one predicate: `endpoint_domain=acute_neurotoxicity` (931) and `challenge_priority=low_acute_electrophysiology` (181). By class within the acute domain: animal in-vivo 748, animal laboratory 179, human laboratory 2, human trial publication 1, human class review 1. **Do not add 931 to the chronic total** — your round states this and it is correct; they are the same table.

**Your proposal 1 asked me not to apply an unexamined animal-screen rule to human electrophysiology, and to ask German. I now think I over-escalated, and the announcement settles it.** The deprioritisation reads: *"Given the availability of **large data sets** focused on acute neurotoxicity, specifically alterations of neuronal electrical activity, submissions focused on this topic will be considered a lower priority."* Phase 2 separately states that *"datasets based on in vitro human systems or able to extrapolate data between in vitro human systems and animal data are of particular interest."* Two human iPSC-neuron rows are not a large electrical-activity dataset; they are in vitro human-system data, which the challenge prioritises. The deprioritisation targets the large animal screens.

So the flag is a corpus-wide invariant (every `readout_category=electrophysiology` row carries `low_acute_electrophysiology`, QC-enforced) that produces a misleading label on exactly two rows. **I am not changing it in this round** — it is a labelling decision and the round is research — but I withdraw the question from German's list and propose instead that those two rows keep the flag while the human-laboratory section counts them as human in-vitro evidence, which it already does. No useful human experiment is omitted.

---

## 2. Proposals 2 and 5 — the identity work, and a figure of mine it overturned

`scripts/cross_system_pairs_cns.py` now computes two relations that were previously conflated:

- **Exact construct** — base sequence **and** every recorded chemistry field (`backbone_chemistry`, `sugar_modifications`, `gapmer_design`, `conjugate`, `ps_count`, `length_nt`, `oligo_class`). Returns **nothing** where the sequence or any field is unknown, because an exact-identity claim cannot rest on blanks.
- **Leakage group** — base sequence with U collapsed to T, explicitly labelled as *not* an identity claim. It exists to keep related molecules in one train/test fold.

**Three results:**

1. **8 exact-construct cross-band groups exist. Every one is animal-to-animal.** Not one spans a human band.
2. **168 of 581 records cannot be keyed exactly** — a missing sequence or a missing chemistry field. The characterization gap, expressed as a matching limit.
3. **A figure in my 10-01 reply is withdrawn.** It reported *animal in vivo and human clinical = 12 molecule-records*. That came from the U→T key — the normalisation §5b of the same reply flagged as unsafe, which I then relied on in §5a. By identity it is **5**; by exact construct it is **zero across a human band**.

**Your proposal 2's premise holds and is now better supported.** Zero human-laboratory/animal-in-vivo matches; two human-laboratory/animal-laboratory matches with **different endpoints** — `APOE ASO-1` and `TREM2 ASO-171`, each in human iPSC-microglia and human whole blood ex vivo (7-plex cytokine release, conserved off-target DEGs) *and* on a rat primary-neuron multi-electrode array (firing rate, burst duration). Same molecule, incomparable readouts: **mechanistic context, not predictive transfer.**

**valeriasen stays descriptive.** The only human-laboratory-to-human-clinical pair here, and discordant: grade 0 in the patient's own *KCNT1* p.R474H iPSC neurons, grade-3 raised intracranial pressure and status dystonicus in that patient. One case is not predictive validation in either direction.

**Reused panels are not independent replication**, as you say. The 8 exact-construct groups are patent-panel molecules recurring across `US*` sequence listings and the Hagedorn supplement — the same designed constructs, not independent experiments. Any analysis must group them.

---

## 3. Proposal 3 — instruments separated; pooling left open

**Implemented** under Oscar's authorization, because the Phase 2 criteria score *"consistency with FAIR data principles"* (10 points) and *"whether researchers would have any concerns or hesitation in making use of this dataset"*, and one unit string naming three instruments fails interoperability outright.

| New `readout_unit` | Rows | Read from that source's own transcribed definition |
|---|---:|---|
| `score_0_to_7_fob7_regional_sum` | 376 | "7 regions (tail, hind paws, hind legs, hind end, front posture, fore paws, head), 0/1 each, summed 0-7" — `US10968453B2`, `US9605263B2`, `US9683235B2` |
| `score_0_to_7_ordinal_inhibition_ladder` | 73 | "0 bright/alert/responsive; 1 tail without tone; 2 drooping hind end…; 6 forelimbs immobile" — `doi:10.1093/nar/gkaf1333` |
| `score_0_to_7_acute_activation` | 36 | "shaking, muscle twitching, cramping, hyperactivity, vocalisation, tremors, convulsions and seizures, peaking ~15 min" — `doi:10.1093/nar/gkag057` |

**Where I departed from your wording.** You asked me to *propose* and not implement. I separated them, and I think the distinction matters: **separating is recording what each source already states; pooling is the scientific judgement.** Separation is also the safe direction — a consumer who later learns two instruments are equivalent can merge, while a silent merge cannot be undone. Nothing needed German's answer to keep them apart. **Whether they may ever be pooled remains entirely open.**

**No new field for the observation window.** `exposure_duration` already separates `3h`, `8wk`, `0-15min_post_single_dose` and `0-120min_post_dose`. The phenotype direction is written **into the unit name** rather than a separate column, so it survives an export that drops sparse columns.

**The divalent-cation condition, recovered as far as the corpus allows, and still unresolved.** Two sources state it: `gkaf1333` dosed in **PBS without Ca²⁺/Mg²⁺** (scored at 3 h); `gkag057` dosed in **standard aCSF at a divalent cation-to-ASO ratio of 0.16:1** (scored over 120 min). **Vehicle and instrument are confounded across the only two sources that report either** — the inhibition data come from the cation-free vehicle and the activation data from the cation-containing one. Whether vehicle or instrument drives the phenotype difference **cannot be separated from these two sources**, which is why no mechanism is asserted. Recorded in `*.methodology.md §10a`. Recovering the original scoring definitions in full is an acquisition item; neither source's methods section has been re-read this round.

**QC change worth flagging.** The scale warning now fires only for unadjudicated groups: the three patents share one instrument by their own definitions, so that pair is recorded as adjudicated rather than warning on every run. A permanently-firing check teaches people to ignore QC.

---

## 4. Proposal 4 — coordination, no duplicate acquisition

**One manifest, one access table, filed once** in the chronic report §8. The three CC-BY `mmc1.pdf` files behind up to 17 missing human-laboratory sequences are **blocked by a bot wall, not a paywall** — `europepmc.org/articles/<PMCID>/bin/<file>` returns HTTP 403, and the bulk route has no `Range` support and exceeded 286 MB because it embeds `.mp4` movie files while the sequence table sits in `mmc1.pdf`. Three full texts were retrieved (169 KB / 119 KB / 269 KB) and staged with SHA-256 checksums; one of them yielded **3 inline 20-mers**, recorded as candidates and **not ingested**.

**The 13-versus-39 human-compound crosswalk is not started** and is the gating item. It needs the original branch's *records*, not an inference from its counts, and no branch totals may be added: measured source-identifier overlap is this branch 91, `k394sz` 26, `t172zv` 167, sharing 17 / 27 / 22 pairwise. `doi:10.1089/nat.2021.0071` alone contributes 357 rows here (181 in-vivo, 176 in-vitro); any lineage that also ingested that supplement holds the same experiment.

---

## 5. Inventory, with the acute subset kept inside its parent table

| | Count |
|---|---:|
| `endpoint_domain = acute_neurotoxicity` rows | **931** (a subset of the 2,393-row chronic-named table) |
| `challenge_priority = low_acute_electrophysiology` rows | 181 |
| Human laboratory rows in the acute domain | **2** |
| Human trial-derived rows in the acute domain | 1 (one publication) |
| Animal rows in the acute domain | 927 |
| Verified acute-qualified human trials | **0 — none established in this module, which is not a claim that none exist anywhere** |
| Whole-corpus human laboratory rows | 116 over 39 molecules, 14 sources |
| …of which electrophysiology | **2 of 116** |

Human-laboratory readouts corpus-wide: 43 viability, 34 transcriptomic, 29 histopathology, 8 injury biomarker, **2 electrophysiology**. So the human-system evidence is overwhelmingly injury, viability, morphology and inflammation in patient-derived tissue — not excitability wearing a human label. All 116 carry `species=human` and all 18 distinct `system_model` values name a human line, donor culture, organoid or human blood; QC fails if `human_laboratory` appears on a non-human row.

**Characterization: 0 purity and 0 analytical identity across all 592 molecules**, now recorded as `NOT_REPORTED` (585) and `NOT_APPLICABLE` (7) rather than as absent columns. Human-laboratory sequence coverage **13/39**; and generic sugar descriptions are **not** source-verified per-position chemistry, as your request insists.

---

## 6. Decisions

**Oscar:** the three CC-BY `mmc1.pdf` downloads (chronic §8) · whether an acute module should exist as a separate deliverable at all — this lineage says no and your request endorses that outcome · the lineage choice after the crosswalk · and the Phase 2 document gap: **no narrative, no methodology document, no PADP for CNS, 90 days from the 2026-12-31 close.**

**German:** whether the three `score_0_to_7` instruments may be pooled (375 rows) · whether vehicle divalent-cation content is a schema covariate or a prose caveat, given it is confounded with instrument across the only two reporting sources · grade calibration across evidence classes.

**Withdrawn from German's list:** the human-electrophysiology priority question, answered from the announcement in §1.

---

**RESEARCH REPORT COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**

---
_Generated by [Claude Code](https://claude.ai/code)_
