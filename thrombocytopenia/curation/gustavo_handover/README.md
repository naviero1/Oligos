# Handover to Gustavo — thrombocytopenia inputs

**From:** Rocksteady/thrombocytopenia · **Commit:** `706e364` · **2026-10-03**
**Why this exists:** Crank's delegation records that nothing in it reaches Gustavo, because Crank has
no channel to him — and flags that as a gap rather than an oversight. Oscar authorised packaging
these for relay. Oscar is the relay; I have no channel either.

**Nothing in Gustavo's Google Drive was read, written, moved or altered in building this.** Everything
here is in this repository. The two scientist workbooks were read from local copies already retrieved
earlier in this session; no Drive file was touched.

---

## Read this first: the model card you own already exists

`curation/scientist_v09/Model_Card_v0.9.csv` is German's, and it is close to complete. It already
fixes the model name, scientific status (**CONDITIONALLY APPROVED FOR RESTRICTED PROOF OF CONCEPT**),
objective, unit of analysis, **candidate N = 16**, the three scaffold families, the primary target,
the feature list, the validation scheme (grouped by sequence / scaffold / matched pair / publication
/ series, **no random row split**), the model comparators, the metrics, the **four required
sensitivity analyses**, the permitted claim, the prohibited claim, the key limitations, deployment
(none) and the scientist gate.

So the task is **executing against a card that exists**, not drafting one. If you draft from scratch
you will almost certainly contradict it somewhere, and German approves all wording before
dissemination.

## The nine lanes, and which are actually open

From `Model_Readiness_v0.7.csv`. Statuses are German's, verbatim:

| Lane | Status | Training permission |
|---|---|---|
| MR-TMB-001 human mechanistic platelet-interaction | CONDITIONALLY READY | **proof-of-concept training permitted** |
| MR-TMB-002 matched-sequence treatment-context | READY FOR DESCRIPTIVE | descriptive + context features |
| MR-TMB-003 treatment-aware clinical risk | DESIGN READY; **TRAINING DEFERRED** | architecture and description only |
| MR-TMB-004 sequence-only clinical classifier | **BLOCKED** | **no final training** |
| MR-TMB-005 pooled 2′MOE class/dose baseline | READY WITH LIMITATIONS | descriptive baseline |
| MR-TMB-006 severe phenotype-2 case series | CASE-SERIES ONLY | structured case series |
| MR-TMB-007 coagulation/bleeding/thrombosis | SEPARATE MODULE | descriptive/mechanistic |
| MR-TMB-008 therapeutic correction / intended pharmacology | SUPPORT/ONTOLOGY READY | control and ontology use only |
| MR-TMB-009 public derivative export | PROVISIONALLY READY FOR TECHNICAL QA | internal team QA only |

**Only MR-TMB-001 permits training of any kind**, and only as proof of concept. Every lane carries a
prohibited claim; four are worth memorising because they are the easy mistakes:

- *Do not claim prediction of clinical thrombocytopenia* (001)
- *Do not balance the dataset by manufacturing negatives* (004)
- *Do not merge phenotype 2 with moderate phenotype 1* (006)
- *Do not merge aPTT prolongation with thrombocytopenia* (007)

## What I am handing you, and what it is for

`manifest.csv` lists all 16 files with byte count and a sha256 prefix, so you can confirm you have
the same version I had. Nothing is duplicated into this folder — the paths are live, which avoids the
drift that has already bitten this endpoint three times.

**Mine, ready to use:**
- `data/controls_inventory.csv` — 31 control records over 26 compounds. Phase 2 requires the
  narrative to open with positive/negative controls, and this is the only endpoint with real arms.
  Each row carries its **prohibited** use as well as its permitted one.
- `data/study_counts.csv` + `data/toxicity_denominator_audit.csv` — the trial ladder and the
  four-test audit behind it. **Quote 19, not 56 and not 1,002.**
- `data/approved_analyses.json` — the matched-contrast outputs, plus the retraction record for the
  classifier I withdrew when it turned out to be MR-TMB-004.
- `data/study_nesting_ledger.csv` — 23 pool/trial overlaps, each proved by arm-size arithmetic.
  Needed before any participant total; denominators here are **not summable**.
- `data/recovery_ledger.csv` — 18 open gaps, 10 critical. This is the Characterization Gap Register.

**Staged and gated — do not model on it yet:**
- `curation/research_staging/sewing2017_condition_level.csv` — 2,347 per-replicate cells with exact
  cell loci, from the Sewing 2017 raw workbook. This is the material your **four required sensitivity
  analyses** need: it contains the alternating-AC family, the CpG controls (ODN 2395 PS/PO) and the
  numeric endpoint values, which are exactly the three subsets the card asks you to remove or
  restrict to. It is **not ingested and not promoted**, gated on German (SRQ-TMB-006) and Oscar.
  Honest accounting: only **163 of the 2,347 cells resolve to a named construct** and 190 are
  controls; a cell is not an observation, and recovering these reconstructs the source's own
  measurements at finer grain rather than replicating anything.

## Three things that will bite you if nobody says them

**1. The classifier is blocked, and I already built it by accident.** An earlier version of this
endpoint shipped a classifier predicting platelet effect from design features at grouped ROC-AUC
0.61–0.69 over 228 compounds. That is MR-TMB-004. It is retracted, the AUCs are withdrawn, and
`data/model_demo_results.json` is now a retraction record so nothing downstream can read a stale
number. The authorized population is **16 constructs**, not 228.

**2. N=16 over 12 independent sequence groups will not support a performance claim.** I checked:
the 16 authorized constructs fall into **12** independent exact-sequence groups. Leave-one-group-out
on 12 groups is dominated by single-group variance. The card's own key limitations say as much
(*N=16; only three major families; ordinal labels partly reconstructed; raw numeric values
incomplete; no external validation*). Report the grouped and LOPO numbers prominently with
uncertainty, and expect them to be weak — `SCIENTIFIC_RULES.md` §G records ~0.94 AUC on random
splits against ~0.65 leave-one-paper-out elsewhere in this corpus, which is the shape of the trap.

**3. A discrepancy for German, not for you to resolve.** The model card lists features including
"2′MOE/LNA/CpG **flags**". `SCIENTIFIC_RULES.md` §C says coarse flags such as `is_LNA` are
"permitted only as secondary derived variables — never as the primary encoding, and never as a
causal feature". The card also lists position-derived chemistry, so this may be compression rather
than conflict. But the rules file instructs that where it and German's documents differ, **German
wins and the rules file is wrong — report the discrepancy rather than following the file.** So:
reported. Please get German's read before you encode features, because position-resolved chemistry
exists for only **44 of 259** compounds dataset-wide and that constrains what a position-encoded
model can even see.

## State of the endpoint, in four numbers

| | |
|---|---:|
| Measurement rows | 1,959 (1,002 human clinical · 451 human laboratory · 497 animal · 9 unresolved) |
| Trials supporting a platelet-toxicity claim | **19** |
| Position-resolved chemistry | **44 / 259** compounds, of which **2** are source-verbatim |
| Qualified clinical negatives | **0** |

Release eligibility: **NOT ELIGIBLE**. Freeze not granted. Five scientific questions are open with
German, including two large ones — whether the CTCAE-aligned grade may stand on 523 laboratory rows,
and whether the 1,959 curator-assigned grades stand at all under the agent contract. Either answer
changes what you can model. Worth knowing before you start rather than after.

## What I would ask of you

If you need anything re-cut — a different grain, a subset, a join — say so and I will produce it.
What I would ask in return is that nothing from the staged folder enters a model before German rules,
and that the trial figure you quote is 19 with its definition attached, so the number does not drift
again between your documents and mine.
