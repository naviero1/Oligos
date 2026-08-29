# Chronic neurotoxicity

**Status:** `delivered` · **Register:** [`./README.md`](./README.md) · **Corpus documentation:** [`../README-CNS.md`](./chronic-neurotoxicity.corpus-overview.md)

Chronic neurotoxicity is the seventh endpoint on the Challenge's list of toxicities of interest, quoted verbatim from the brief at [`./README.md`](./README.md#scope-authority). It is **curated and delivered**: 2,393 graded per-measurement rows over 573 oligonucleotides, drawn from 89 distinct source documents.

> **This file previously said the opposite.** Until 2026-08-28 it recorded the endpoint as `not-addressed` — "no source acquired, no rows extracted" — and proposed **out of scope for Phase 2** as its deliverable. That was an accurate description of one branch (the 111-row kidney lineage) and a wrong description of the project: the CNS curation was carried out on a separate branch that the review could not see. The recommendation is withdrawn, and §4 below preserves what the original sweeps did and did not establish, since that record is still useful.

## 1. Status

| Item | Count | Basis |
|---|---:|---|
| Measurement rows | **2,393** | `challenge_priority != high_hydrocephalus` in the 2,540-row CNS corpus |
| Oligos | **573** | distinct `oligo_id` referenced by those rows |
| Oligos with a published sequence | **458 / 573** | rest are `TBD`; never reconstructed |
| Distinct `source_ref` documents | **89** | canonical identifiers — DOI, PMID, PMCID, US patent, NCT, FDA/EMA document |
| Distinct `source_id`s | **94** | |
| Distinct target genes | **41** | |
| Rows carrying a verifier verdict | **228** | adversarial verification, [`../VERIFICATION-CNS.md`](./chronic-neurotoxicity.verification.md) |
| Extraction status | complete for this pass | 12 extraction lanes, [`../notes/cns/extractions/`](./notes/cns/extractions/) |

Grades — provisional on all rows, pending subject-matter review:

| `neurotox_grade` | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Rows | 1,183 | 577 | 513 | 120 |

| Study type | animal in vivo | clinical | in vitro |
|---|---:|---:|---:|
| Rows | 1,684 | 414 | 295 |

## 2. Where the data and its documentation live

The CNS curation was carried out as **one corpus of 2,540 measurements serving both CNS endpoints the brief names**, partitioned by its own `challenge_priority` column: `high_hydrocephalus` (147 rows) belongs to [`./hydrocephalus.md`](./hydrocephalus.md), everything else (2,393) here. The partition is disjoint and exhaustive.

| Artifact | Path |
|---|---|
| Measurements | [`../data/cns_measurements.csv`](./chronic-neurotoxicity.measurements.csv) (2,540 × 26, corpus) |
| Oligos | [`../data/cns_oligos.csv`](./chronic-neurotoxicity.oligos.csv) (592 × 17, corpus) |
| Analysis view (generated) | [`../data/oligotox_cns_merged.csv`](./notes/cns/corpus/oligotox_cns_merged.csv) |
| Schema, vocabularies, 0–3 rubric | [`../schema-cns.md`](./chronic-neurotoxicity.schema.md) |
| Methodology | [`../METHODOLOGY-CNS.md`](./chronic-neurotoxicity.methodology.md) |
| Verification record | [`../VERIFICATION-CNS.md`](./chronic-neurotoxicity.verification.md) |
| Source registry (generated) | [`../sources/SOURCES-CNS.md`](./chronic-neurotoxicity.sources.md) |
| Gap analysis / what to generate next | [`../NEXT-STEPS-CNS.md`](./chronic-neurotoxicity.next-steps.md) |

The rubric concern the earlier version raised was real and is resolved: `nephrotox_grade` is renal and not transferable, so this endpoint has its **own** graded column, `neurotox_grade`, with its own written rubric in [`../schema-cns.md`](./chronic-neurotoxicity.schema.md), plus CNS-specific columns (`cns_region`, `endpoint_domain`, `challenge_priority`, `reversibility`). `cns_oligos.csv` keeps the identical 17-column layout as the kidney oligo table so the two datasets union without re-mapping.

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

The methodological lesson is recorded in [`../NEXT-STEPS-CNS.md`](./chronic-neurotoxicity.next-steps.md): an endpoint sweep bounded by the local library measures the library, not the literature, and should say which it is measuring.

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
