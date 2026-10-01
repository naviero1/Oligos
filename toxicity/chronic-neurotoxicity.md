# Chronic neurotoxicity

**Status:** `delivered` · **Register:** [`./README.md`](./README.md) · **Corpus documentation:** [`chronic-neurotoxicity.corpus-overview.md`](./chronic-neurotoxicity.corpus-overview.md)

Chronic neurotoxicity is the seventh endpoint on the Challenge's list of toxicities of interest, quoted verbatim from the brief at [`./README.md`](./README.md#scope-authority). It is **curated and delivered**: 2,393 graded per-measurement rows over 573 oligonucleotides, drawn from 89 distinct source documents.

> **This file previously said the opposite.** Until 2026-08-28 it recorded the endpoint as `not-addressed` — "no source acquired, no rows extracted" — and proposed **out of scope for Phase 2** as its deliverable. That was an accurate description of one branch (the 111-row kidney lineage) and a wrong description of the project: the CNS curation was carried out on a separate branch that the review could not see. The recommendation is withdrawn, and §4 below preserves what the original sweeps did and did not establish, since that record is still useful.

**Review correspondence:** Beebop's 2026-09-30 proposals and the response recording each disposition are at [`chronic-neurotoxicity/ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`](./chronic-neurotoxicity/ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md). Its §0 records that this branch is one of three parallel CNS lineages.

## 1. What this endpoint holds — human evidence first

Phase 2 asks for human-relevant data, so the table below is ordered by the
strength of the human claim each class of evidence supports, and animal evidence
sits at the bottom as supporting material. The ordering is not cosmetic: it is
enforced by a column. `evidence_class` splits what `study_type` conflates — that
column has three values, so a rat cortical culture and a patient-derived iPSC
neuron are both "in vitro", and a registry-posted trial table, a label's pooled
safety summary and a single case report are all "clinical". Human totals are
computed over `evidence_class`, and [`scripts/qc_cns.py`](./scripts/qc_cns.py)
fails if any row's class disagrees with its own `species` or `study_type`, so
"no animal row contributes to a human total" is checked rather than promised.

<!-- BEGIN generated:evidence -->

| Evidence class | Rows | Molecules | Sources | What it is |
|---|---:|---:|---:|---|
| Human trial — registry-posted results | 133 | 11 | 20 | arms and denominators as posted |
| Human trial — peer-reviewed report | 100 | 11 | 16 | registry identity verified separately; see the register |
| Human trial — sponsor or conference report | 62 | 4 | 8 | no posted table, no peer review |
| **Human laboratory** — in vitro / ex vivo | 116 | 39 | 14 | patient-derived iPSC neurons, organoids, microglia, whole blood |
| Human — label / SmPC / EPAR, pooled | 101 | 10 | 13 | pools a development programme; never one trial |
| Human — postmarketing signal assessment | 1 | 1 | 1 | no exposure denominator |
| Human — case report or case series | 3 | 2 | 3 | one patient each, however serious |
| Human — cross-compound review or atlas | 14 | 3 | 2 | aggregates other studies' compounds |
| Animal in vivo | 1,684 | 512 | 23 | supporting material |
| Animal laboratory — in vitro | 179 | 143 | 2 | supporting material |
| **Human — all classes** | **530** | — | — | 22% of the endpoint |
| **Animal — all classes** | **1,863** | — | — | 78%, supporting material |

Molecule counts do **not** sum down that column: one molecule can carry rows in several bands. Row counts do sum.

**Human clinical trials, counted as trials.** From [`chronic-neurotoxicity.trials.csv`](./chronic-neurotoxicity.trials.csv), one row per trial, never per measurement.

| | Count |
|---|---:|
| Verified unique human trials | **27** |
| …with an endpoint-evaluable outcome | 27 |
| …flagged by their own source as an extension or roll-over protocol | 5 |
| …also contributing rows to the other CNS endpoint | 10 |
| Pending candidates — a trial report naming no registry entry | 19 |
| Human trial-derived measurement rows | 295 |
| Unique compounds across the verified trials | 18 |
| Human laboratory / ex-vivo measurement rows | 116 |

Pending candidates are excluded from the verified total on purpose. A publication reporting a trial establishes the trial, but its registry identifier has to come from a document — supplying one from recall would be exactly the fabricated trial identifier this dataset refuses to contain.

**Which hydrocephalus claim each row makes.** The endpoint is not one thing, and `endpoint_domain` cannot carry the distinction — it has a single `hydrocephalus` value, and its use in this corpus drifted by extraction lane. `hydroceph_tier` is derived from the readout instead, so it is lane-independent.

| Tier | Rows | What it is |
|---|---:|---|
| `pressure_or_composition` | 2 | raised intracranial or CSF opening pressure, CSF volume, outflow resistance, DTI-ALPS — supports a mechanism, is not a confirmed hydrocephalus event |
| `related_clinical_sign` | 1 | papilloedema and optic findings — a pressure sign, recorded separately because the two dissociate |

**Which zeros are negatives.** A grade of 0 means four different things, and only two of them are a measured negative.

| | Rows |
|---|---:|
| Grade-0 rows | 1,183 |
| …eligible as a measured negative (`negative_eligible=TRUE`) | 1,135 |
| …**not** eligible | 48 |

The ineligible rows are kept, with their evidence, and excluded from negative counts by one predicate:

- `review_required` — 37 row(s): no ascertainment basis could be established from the row's own source fields
- `threshold_limited_zero` — 4 row(s): the table lists only terms above a frequency cut-off, so the term's absence may be a reporting artefact
- `not_assessed_in_source` — 4 row(s): the source does not report this endpoint at all
- `absence_of_label_warning` — 3 row(s): the finding is a warning *not appearing* in a label, which is a fact about the document

<!-- END generated:evidence -->

### Corpus-level counters

| Item | Count | Basis |
|---|---:|---|
| Measurement rows | **2,393** | `challenge_priority != high_hydrocephalus` in the 2,538-row CNS corpus |
| Oligos | **573** | distinct `oligo_id` referenced by those rows |
| Oligos with a published sequence | **458 / 573** | rest are `TBD`; never reconstructed |
| Distinct `source_ref` documents | **89** | canonical identifiers — DOI, PMID, PMCID, US patent, NCT, FDA/EMA document |
| Distinct `source_id`s | **94** | |
| Distinct target genes | **41** | |
| Rows carrying a verifier verdict | **228** | adversarial verification, [`chronic-neurotoxicity.verification.md`](./chronic-neurotoxicity.verification.md) |
| Extraction status | complete for this pass | 12 extraction lanes, [`notes/cns/extractions/`](./notes/cns/extractions/) |

Grades — provisional on all rows, pending subject-matter review:

| `neurotox_grade` | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Rows | 1,183 | 577 | 513 | 120 |

## 2. Where the data and its documentation live

The CNS curation was carried out as **one corpus of 2,538 measurements serving both CNS endpoints the brief names**, partitioned by its own `challenge_priority` column: `high_hydrocephalus` (145 rows) belongs to [`./hydrocephalus.md`](./hydrocephalus.md), everything else (2,393) here. The partition is disjoint and exhaustive.

| Artifact | Path |
|---|---|
| Measurements | [`chronic-neurotoxicity.measurements.csv`](./chronic-neurotoxicity.measurements.csv) (2,393 × 32) |
| Oligos | [`chronic-neurotoxicity.oligos.csv`](./chronic-neurotoxicity.oligos.csv) (573 × 17) |
| Analysis view (generated) | [`notes/cns/corpus/oligotox_cns_merged.csv`](./notes/cns/corpus/oligotox_cns_merged.csv) |
| Schema, vocabularies, 0–3 rubric | [`chronic-neurotoxicity.schema.md`](./chronic-neurotoxicity.schema.md) |
| Methodology | [`chronic-neurotoxicity.methodology.md`](./chronic-neurotoxicity.methodology.md) |
| Verification record | [`chronic-neurotoxicity.verification.md`](./chronic-neurotoxicity.verification.md) |
| Source registry (generated) | [`chronic-neurotoxicity.sources.md`](./chronic-neurotoxicity.sources.md) |
| Gap analysis / what to generate next | [`chronic-neurotoxicity.next-steps.md`](./chronic-neurotoxicity.next-steps.md) |
| Human clinical-trial register | [`chronic-neurotoxicity.trials.csv`](./chronic-neurotoxicity.trials.csv) |
| Pending trial candidates | [`chronic-neurotoxicity.trials-pending.csv`](./chronic-neurotoxicity.trials-pending.csv) |

The rubric concern the earlier version raised was real and is resolved: `nephrotox_grade` is renal and not transferable, so this endpoint has its **own** graded column, `neurotox_grade`, with its own written rubric in [`chronic-neurotoxicity.schema.md`](./chronic-neurotoxicity.schema.md), plus CNS-specific columns (`cns_region`, `endpoint_domain`, `challenge_priority`, `reversibility`). `cns_oligos.csv` keeps the identical 17-column layout as the kidney oligo table so the two datasets union without re-mapping.

## 3. The chronic/acute boundary

The earlier version correctly noted that the brief distinguishes chronic neurotoxicity from acute alterations of neuronal electrical activity but defines neither, and that adopting the endpoint would require drawing that line. It is drawn in the data rather than in prose: every row declares `endpoint_domain` and `challenge_priority`, so a consumer filters rather than trusts a judgement.

| `challenge_priority` | Rows (corpus) | Meaning |
|---|---:|---|
| `high_chronic_neurotox` | 1,047 | the named endpoint |
| `high_hydrocephalus` | 147 | the other named endpoint, in its own dossier |
| `medium` | 1,165 | in scope, neither named bucket |
| `low_acute_electrophysiology` | 181 | the readout class the brief deprioritises — 7% of the corpus, filterable in one predicate |

Acute rows are present deliberately: the large panels that pair **sequences** with **graded CNS outcomes** are acute, and they are the modelling payload. The 181 electrophysiology rows are present only as the matched in-vitro arm of an in-vivo panel on the same molecules.

## 4. What the original sweeps established, and what they did not

Preserved because the record remains useful. The original dossier swept the 18 PDFs then in `sources/` and found no per-compound neurological readout among them: two passages touched CNS safety — an injection-procedure note in *Methods in Molecular Biology* 2434 ch. 24 stating that 10 µL murine injections cause no neuronal loss, astrogliosis or microgliosis, and a ch. 25 statement that the author knew of no safety-pharmacology data on systemic ASOs — and neither is oligonucleotide-specific evidence of chronic toxicity. Both readings stand.

What did not follow is the conclusion. **The corpus of sources held at the time was not the corpus of sources available**, and the sweep measured the former. The CNS pass acquired 108 documents that were not in `sources/` when the dossier was written, including FDA nonclinical review documents that had been recorded as unobtainable because `accessdata.fda.gov` returns HTTP 404 to non-browser clients — a bare 404 there was read as absence. Those reviews are among the best chronic-neurotoxicity sources in existence, because they carry per-dose, per-sex, per-timepoint lesion incidences **with recovery groups**.

The methodological lesson is recorded in [`chronic-neurotoxicity.next-steps.md`](./chronic-neurotoxicity.next-steps.md): an endpoint sweep bounded by the local library measures the library, not the literature, and should say which it is measuring.

## 5. Known limitations

- **Grades are provisional** on all 2,393 rows, pending subject-matter review.
- **Recovery is rarely assessed.** `reversibility` is `not_assessed` on the large majority of corpus rows because most sources never looked; 398 rows carry a real recovery assessment, nearly all from regulatory nonclinical reviews.
- **Human in vitro data is thin** — 295 in-vitro rows, and the literature is genuinely close to empty for iPSC microglia and brain organoids, which is a finding rather than an omission.
- **Source concentration.** A few high-yield documents contribute a large share of rows, so errors there propagate; those were prioritised in verification.
- Verification was a stratified sample, not a census: 614 verdicts, 149 refuted, 253 rows corrected.

---

## Divided by toxicity, and what is duplicated

This dataset is one slice of the CNS corpus, produced by
[`scripts/split_by_endpoint.py`](./scripts/split_by_endpoint.py). Two things happen
in that split and they are **not** the same operation:

**Measurements divide.** A measurement is an observation of one toxicity, so the
rows partition — disjoint and exhaustive. This toxicity holds **2,393 measurement
rows**, and across all endpoints the per-toxicity counts sum exactly to the corpus
total. The script fails loudly if they ever stop summing, so the partition cannot
silently drift.

**Oligonucleotides duplicate.** A molecule is a compound *identity*, not an
observation. A drug studied for two toxicities belongs in both tables. This
toxicity's oligo table holds **573 molecules**, of which **15 also appear
under another toxicity** — 5 replicated under the same `oligo_id`, and 10
curated independently elsewhere and therefore carrying a *different* id there.

> **Consequence, because it is the easy mistake to make: oligo counts are not
> additive across toxicities. Row counts are.** Summing the oligo tables
> double-counts every molecule studied for more than one toxicity.

| File | What it is |
|---|---|
| [`chronic-neurotoxicity.measurements.csv`](./chronic-neurotoxicity.measurements.csv) | this toxicity's 2,393 graded measurement rows |
| [`chronic-neurotoxicity.oligos.csv`](./chronic-neurotoxicity.oligos.csv) | the 573 molecules those rows reference |
| [`chronic-neurotoxicity.shared-molecules.csv`](./chronic-neurotoxicity.shared-molecules.csv) | the 15 molecules also present under another toxicity, with the id they carry there |
| [`molecule_crosswalk.csv`](./molecule_crosswalk.csv) | the same ledger across every toxicity at once |

The crosswalk matters most for the 10 molecules curated independently under two
toxicities: nothing links `OLG###` to `CNS###`, so a model keyed on `oligo_id` would
treat one compound as two. Where both records carry a sequence, the split asserts
they agree base-for-base and **fails** if they do not — a disagreement would mean one
of the two is the wrong molecule. Across the whole repository there are currently
**no such conflicts**.

Cross-cutting artifacts are **duplicated into each toxicity that uses them** rather
than shared from a common folder, so every toxicity here is self-contained.
