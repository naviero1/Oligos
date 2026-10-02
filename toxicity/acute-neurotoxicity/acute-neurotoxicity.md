# Acute neurotoxicity — endpoint dossier

**Status:** `delivered` · **Not on the Challenge's endpoint list** · **Register:** [`../README.md`](../README.md) · **Data:** [`./data/`](./data/) · **Shared CNS pipeline:** [`../_shared/cns/`](../_shared/cns/)

This folder holds the acute axis of the CNS curation: **2,081 measurements**. It exists
because the data exists and has to be filed somewhere honest — **not** because the Challenge asks
for it.

## 1. Read this before citing anything here

The brief's page 1, quoted at [`../README.md`](../README.md#scope-authority), states that
submissions focused on acute neurotoxicity, *"specifically alterations of neuronal electrical
activity"*, are **lower priority** than the eight listed toxicities. A previous revision of the
register drew the consequence explicitly: *"Acute neurotoxicity therefore has no dossier here."*

**This folder reverses that**, and the reversal is a filing decision, not a scope claim. The
curation produced 2,081 rows on this axis; leaving them undossiered would have meant either
discarding them or hiding them inside another endpoint's folder. Both are worse than filing them
under their own name with the caveat attached.

Nothing here counts toward the brief's endpoint coverage. The two listed CNS endpoints are
[`../chronic-neurotoxicity/`](../chronic-neurotoxicity/) (6 rows) and
[`../hydrocephalus/`](../hydrocephalus/) (1 row).

## 2. Status

| Item | Count |
|---|---:|
| Measurement rows | **2,047** |
| Oligonucleotides | **1,866** |
| Per-position modification records | **32,478** |
| `source_id`s | 5 — H1, HV1, HV2, HV3, K1 |
| Sequences published | 1,851 / 1,866 — see `../_shared/cns/docs/CHARACTERIZATION_COVERAGE.md`, which keeps the human and animal subsets apart |
| Graded rows | 245 — 0/1/2/3 = 74 / 81 / 39 / 51 |
| Ungraded rows | 1,825 — the in vitro readout is continuous and the source defines no severity bands |
| Human rows | **34** — all human *in vitro* (hiPSC forebrain neurons, cortical organoids, SH-SY5Y), from HV1–HV3. **Zero clinical.** |
| Verified human clinical trials | **0** — `data/trials.csv` is present and empty, which is the claim, not an omission |

### What is in here

| `tox_axis` | Rows | What it is |
|---|---:|---|
| `acute_neuronal_excitability` | 1,825 | spontaneous calcium oscillations, rat cortical neurons — *literally* the phrase the brief deprioritises |
| `acute_behavioural` | 222 | 0–20 tolerability score, ≤1 h after ICV dosing |
| `invitro_human_neural_toxicity` | 28 | **human** iPSC neurons, cortical organoids and SH-SY5Y — viability, apoptosis and neurite readouts |
| `invitro_human_context_not_toxicity` | 6 | human rows that measure **uptake or off-target expression, not injury**. Carried for context and never graded |

**This folder is now purely acute.** An earlier revision also held the general clinical CNS adverse
events, because they mapped to no listed endpoint. They have since moved to
[`../chronic-neurotoxicity/`](../chronic-neurotoxicity/): trial adverse events are collected across
chronic exposure, which makes them the human arm of a **listed** endpoint rather than a residual
here.

**This folder nonetheless holds the module's only human laboratory data.** An earlier revision of
this dossier stated in three places that the endpoint was entirely animal. That was wrong from the
moment sources HV1–HV3 were ingested, and it was wrong about exactly the data class the Challenge
prioritises. The human rows are *in vitro*, never clinical: `data/trials.csv` exists here and is
empty, which states a verified human clinical-trial count of **zero in this module** — not that no
such trials exist in the world.

## Human versus animal

| file | rows |
|---|---:|
| [`data/measurements_human.csv`](./data/measurements_human.csv) | 34 — all `human_invitro` |
| [`data/measurements_animal.csv`](./data/measurements_animal.csv) | 2,047 |

## 3. Sources allocated

| `source_id` | Source | Licence | Rows |
|---|---|---|---:|
| `H1` | Hagedorn PH et al. 2022, *Nucleic Acid Ther* 32(3):151–162 — mouse ICV acute tolerability and a rat primary-neuron calcium assay | **CC BY 4.0** | 2,006 |
| `K1` | Miller BR et al. 2024, *Mol Ther Nucleic Acids* 35(2) — divalent-cation formulation rescue | CC BY-NC | 41 |
| `C1` | FDA prescribing information (tofersen, nusinersen) via DailyMed | public domain | 11 |

`O1` (O'Rourke 2026) contributes measurement instruments but no rows; it is documented in
[`../_shared/cns/docs/SCORING_INSTRUMENTS.md`](../_shared/cns/docs/SCORING_INSTRUMENTS.md).

## 4. Why this data is worth keeping despite the deprioritisation

Every row pairs an oligonucleotide's **design** — sequence plus the position of every chemical
modification — with a **measured outcome**. Five findings follow, each regenerable from
[`./data/`](./data/); full traces in
[`../_shared/cns/FINDINGS.md`](../_shared/cns/FINDINGS.md).

1. **The source table is ~12× larger than the field cites it as.** `H1` is universally cited for
   148 mouse-dosed compounds; its supplementary table holds **1,825**, each with a sequence whose
   case encodes LNA position. Restructuring the whole table is the main contribution here.
2. **Sequence predicts in vivo toxicity better than the in vitro assay does** — AUC **0.888** vs
   **0.735** across the 181 compounds carrying both readouts.
3. **The assay's noise is measurable from the data: CV 17.3%** (one control oligo, 14 independent
   plate runs). That explains finding 2.
4. **Guanine is a graded risk factor, and position beats count** — median mouse score rises 0.3 →
   20 with guanine count; a guanine near the 3′ end is the strongest single sequence warning.
5. **Formulation can override sequence entirely** — added calcium takes the same molecule from
   19.5 to 1.0 on a 0–20 scale, so `formulation_ca_mM` and `formulation_mg_mM` are first-class
   columns rather than a methods note.

A worked baseline (`../_shared/cns/src/baseline_model.py`) reaches **89.5%** accuracy on a
held-out set of 19 compounds against a *different target gene* — reproducing the accuracy the
original authors report, which is also the check that the restructured table is faithful.

## 5. Known issues

- **Not a listed endpoint.** §1. Nothing here counts toward the brief's coverage.
- **The folder holds 11 rows that are not acute neurotoxicity** — §2.
- **The large in vitro arm is rat, not human.** 1,825 of this folder's 2,081 rows are the rat
  primary-neuron calcium screen. 34 rows are human *in vitro* (HV1-HV3, 13 compounds) and none is
  clinical. That layer is thin, and extending it is the module's highest-value work —
  [`../_shared/cns/OPEN_ITEMS.md`](../_shared/cns/OPEN_ITEMS.md) OI-07.
- **Chemistry is narrow** — 1,825 of 1,834 compounds are LNA/DNA full-phosphorothioate
  oligonucleotides from a single study (1,726 gapmers, 99 mixmers).
- **1,825 rows are deliberately ungraded.** Grading a continuous readout for which the source
  defines no severity bands would mean inventing thresholds.
- **Grades are provisional**, pending subject-matter-expert review.
- **One row is one group, not one animal** (group means over 4–6 mice).
- **Publication bias.** The ~40% failure rate in `H1`'s library is a property of a library built
  to interrogate toxicity, not a base rate for CNS oligonucleotides.

## 6. Not done, and next step

| Not done | Cause |
|---|---|
| Human *in vitro* data | **34 rows over 13 compounds** (HV1–HV3), all held in this folder. Still thin against 2,047 animal rows, and the module's largest scientific gap. |
| Chemistry breadth | One chemistry class dominates; the queued `B1` (non-human primate) and `P1` (patent) sources would widen it. |
| Extraction of the queued sources | Five sources gathered, none extracted — [`../_shared/cns/sources/RESEARCH_QUEUE.md`](../_shared/cns/sources/RESEARCH_QUEUE.md). |

Because this endpoint is deprioritised, **adding more acute rows is the lowest-value next step
in the whole CNS programme.** Effort is better spent on
[chronic neurotoxicity](../chronic-neurotoxicity/chronic-neurotoxicity.md), which the brief lists
and which currently has six rows.
