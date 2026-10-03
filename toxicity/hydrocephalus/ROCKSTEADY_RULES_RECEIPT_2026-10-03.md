# Rocksteady → Beebop: hydrocephalus row of the 2026-10-03 delegation

Receipt identifier: `2026-10-03/hydrocephalus`. Companion to the CNS receipt at
[`../chronic-neurotoxicity/ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`](../chronic-neurotoxicity/ROCKSTEADY_RULES_RECEIPT_2026-10-03.md),
which carries the `SCIENTIFIC_RULES.md` confirmation and the rule-by-rule
response for all CNS lanes. This file works only the hydrocephalus row.

| | |
|---|---|
| **Branch** | `claude/oligo-cns-toxicity-dataset-tijib6` @ `ce4d677`, clean tree |
| **My hydrocephalus partition** | `toxicity/hydrocephalus.measurements.csv` — 145 rows, 13 oligos, all 13 measured, 0 orphans |
| **Recomputed from** | committed trees only, at `ce4d677` for my lane and at `origin/…` tips for the other two lineages |
| **Scope** | no label assigned or changed, nothing re-grained, no ingestion/promotion/release. Items 3–5 below are on branches I do not own and are **report-only**. |

---

## 1. "Zero human in-vitro" — confirmed, and it is true of every hydrocephalus lineage

The delegation states this of hydrocephalus. It holds, and it is not a quirk of
one curation:

| lineage | rows | human rows | **human in-vitro** | any in-vitro |
|---|---:|---:|---:|---|
| **mine** (tijib6) | 145 | 131 | **0** | 2 rows, rat |
| `t172zv` (dedicated) | 1,342 | 1,332 | **0** | 2 rows, rat |
| `k394sz` | 12 | 12 | **0** | none at all |

My 131 human rows are entirely clinical: `patient_cohort` (87),
`patient_case` (20), and named cohorts including SMA post-marketing, SOD1/ALS
pooled, and matched non-SMA population controls. My non-human rows are 12 animal
in-vivo (rat 8, mouse 3, monkey 1) plus the 2 rat in-vitro.

**On `t172zv` the gap is stronger than "no human in-vitro", and it is already
disclosed.** An independent recomputation of that branch confirms
`subject_class` = human_in_vivo 1,329 / human_population 3 / animal_in_vivo 8 /
animal_in_vitro 2, with **no `human_in_vitro` value at all** and no "ex vivo"
term anywhere in any of its 11 committed CSVs. Its two in-vitro rows are rat
cultured ependymal cells (`HYD-MSR-01338`, `HYD-MSR-01339`). Further: the compounds
appearing in its human rows (43 distinct `oligo_name` values, of which **41** are
real compound names — `NOT_APPLICABLE` and `placebo_or_sham_control` are the
other two, and 4 of the 41 are pooled multi-compound strings such as
`casimersen; eteplirsen; golodirsen`) and the 6 in its animal rows
(`AQP4_siRNA`, `Gai2_AS_ODN`, `Gai2_mismatch_ODN`, `Gai2_nonsense_ODN`,
`SPAK_siRNA4`, `negative_control_siRNA`) have an **empty intersection** under any
of those counting rules — not one oligo is measured on both sides. Under §D that is correct lane separation, and
it means no bridge of any kind is available, not merely no human in-vitro one.
To that branch's credit the gap is disclosed rather than hidden: its own
`qc/stats.json` already carries `"human_in_vitro_rows": 0`.

**The scientific consequence, stated without resolving it.** For this endpoint
there is no human laboratory model anywhere in the corpus, and the only
mechanistic in-vitro evidence is 2 rat rows. So hydrocephalus is a
clinically-observed endpoint with almost no mechanistic support, and §D forbids
pooling the human and animal evidence to compensate. Any claim that this
endpoint supports in-vitro-to-clinical translation is unsupportable on the
present data. That is a finding, not a label: whether the endpoint is therefore
reportable at all is German's call under §J.

My evidence composition, for the record (`evidence_class`):
human_trial_registry 63 · human_case_report 15 · human_trial_publication 13 ·
human_label_pooled 12 · animal_invivo 12 · human_observational 12 ·
human_trial_sponsor 8 · human_background_epi 7 · animal_laboratory 2 ·
human_postmarketing 1.

`hydroceph_tier`: ventricular_enlargement 88 · pressure_or_composition 29 ·
related_clinical_sign 16 · disease_background 7 · procedure_or_mechanism 4 ·
therapeutic_reduction 1.

---

## 2. Recomputed from the committed tree, as instructed

All figures in §1 come from `git show <ref>:<path>` against committed blobs, not
from a working tree and not from any previously published summary. My own lane
is clean at `ce4d677` and identical to `origin`, so for this branch "committed"
and "current" coincide; for `t172zv` and `k394sz` I read their `origin` tips.

One previously published figure of mine, restated so the correction is not
buried: I reported hydrocephalus verified-trial sequence coverage as **2 of 4**.
**The truth is 3 of 4** — only inclisiran lacks a sequence. I found that error
myself and am repeating the correction here because the 2-of-4 figure was
subsequently quoted onward without being rechecked.

---

## 3. `PHASE2_COMPLIANCE.md` — the 53-vs-51 split is real, and there is a third number

On `origin/claude/hydrocephalus-toxicity-oligos-t172zv`, at
`toxicity/hydrocephalus/PHASE2_COMPLIANCE.md`:

- **line 43** renders `<!--stat:n_compounds_real-->51<!--/stat-->` — "purity for
  the human-evidence subset is zero of 51 compounds"
- **line 106** renders `<!--stat:n_oligos-->53<!--/stat-->` — "53 compounds"

Both in one document, unreconciled. Recomputing from that branch's committed
data gives a **third** figure neither line reports:

| count | value |
|---|---:|
| records in `oligos.csv` | **53** |
| distinct `oligo_id` carrying ≥1 measurement | **49** |
| oligo records never measured | **4** |
| orphan measurement `oligo_id` | 0 |

So `n_oligos` = 53 is the stored roster, 49 is the measured roster, and 51 is
neither — it sits between them and its derivation is not stated in the document.
A reader cannot tell which population the purity claim on line 43 is about.
Report-only: not my branch, not my file.

---

## 4. `release_id` is `-dirty` — confirmed verbatim, and it is release-blocking

`toxicity/hydrocephalus/qc/stats.json:356` on `t172zv`:

```json
"release_id": "hydrocephalus-73be6c0-dirty"
```

The `-dirty` suffix means the identifier was stamped from a working tree with
uncommitted changes, so it does not bind to a reproducible commit. Three
documents on that branch cite `qc/stats.json.release_id` as the release
identifier — `ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md:5`,
`ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md:11` and
`ROCKSTEADY_REVIEW_REPLY_2026-10-01.md:8` — so the unreproducible identifier is
already load-bearing in published prose. Under §H that blocks promotion, and
release authority is Oscar's under §J. Report-only.

---

## 5. Hydrocephalus data is scattered across four branches in four incompatible shapes

Not asked for, found while recomputing §1, and relevant to whichever lineage is
promoted:

| branch | path | rows |
|---|---|---:|
| `tijib6` (mine) | `toxicity/hydrocephalus.measurements.csv` | 145 |
| `t172zv` | `toxicity/hydrocephalus/data/measurements.csv` | 1,342 |
| `k394sz` | `toxicity/hydrocephalus/data/measurements.csv` | 12 |
| `2h7t50` | `hydrocephalus/data/measurements.csv` | 147 |

Four row counts, four paths, no two alike, and `t172zv` additionally carries five
upstream partials (`_ctgov_`, `_faers_`, `_label_`, `_literature_`,
`_nonclinical_`). The `study_type` vocabularies differ too: mine uses
`clinical`, `t172zv` splits it into `clinical_trial` / `pharmacovigilance` /
`regulatory_label` / `clinical_case` / `background_epidemiology`. That vocabulary
difference is a Tier 0 crosswalk item, not something to paper over at merge
time — flagged, not reconciled.

---

## 6. What I did not do

No grade or label assigned or changed in this lane. No row re-grained. No
imputation, no manufactured negative, no conflict resolved between the four
hydrocephalus lineages. Nothing written to `t172zv`, `k394sz` or `2h7t50`. No
ingestion, promotion or release. The 2-of-4 → 3-of-4 correction in §2 is a
restatement of an error I had already found and published, not a new change to
data.

---
_Generated by [Claude Code](https://claude.ai/code)_
