# Hydrocephalus — endpoint dossier

**Status:** `delivered` · **Register:** [`./README.md`](./README.md) · **Corpus documentation:** [`hydrocephalus.corpus-overview.md`](./hydrocephalus.corpus-overview.md)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md#scope-authority)). It is **curated and delivered**: 145 graded per-measurement rows over 13 oligonucleotides, drawn from 40 distinct source documents.

> **This file previously said the opposite.** Until 2026-08-28 it recorded the endpoint as `not-addressed` — "nothing was acquired, extracted or decided… zero rows, zero oligos, zero `source_id`s" — and recommended recording it as out of scope. That was an accurate description of one branch (the 111-row kidney lineage) and a wrong description of the project. The recommendation is withdrawn; §"What the original sweep established" preserves the part of the record that still holds.

**Review correspondence:** Beebop's 2026-09-30 proposals and the response recording each disposition are at [`hydrocephalus/ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`](./hydrocephalus/ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md). Its §0 records that this branch is one of three parallel CNS lineages.

## Status — human evidence first

Phase 2 asks for human-relevant data, so the table below is ordered by the
strength of the human claim each class of evidence supports, and animal evidence
sits at the bottom as supporting material. `evidence_class` is what makes that
ordering real: `study_type` has three values, so it cannot tell a registry-posted
trial table from a label's pooled safety summary or from a single case report,
and all three were previously counted together as "clinical". For this endpoint
that conflation mattered most of all, because almost all of its evidence is
clinical and the kinds are not interchangeable.

<!-- BEGIN generated:evidence -->

| Evidence class | Rows | Molecules | Sources | What it is |
|---|---:|---:|---:|---|
| Human trial — registry-posted results | 63 | 4 | 16 | arms and denominators as posted |
| Human trial — peer-reviewed report | 13 | 3 | 5 | registry identity verified separately; see the register |
| Human trial — sponsor or conference report | 8 | 1 | 2 | no posted table, no peer review |
| Human — label / SmPC / EPAR, pooled | 12 | 2 | 7 | pools a development programme; never one trial |
| Human — postmarketing signal assessment | 1 | 1 | 1 | no exposure denominator |
| Human — case report or case series | 15 | 3 | 6 | one patient each, however serious |
| Human — observational cohort, exposed | 12 | 2 | 2 | outside a trial protocol |
| Human — disease background, unexposed | 7 | 1 | 3 | no oligonucleotide given; a baseline rate, not an effect |
| Animal in vivo | 12 | 6 | 4 | supporting material |
| Animal laboratory — in vitro | 2 | 2 | 1 | supporting material |
| **Human — all classes** | **131** | — | — | 90% of the endpoint |
| **Animal — all classes** | **14** | — | — | 10%, supporting material |

Molecule counts do **not** sum down that column: one molecule can carry rows in several bands. Row counts do sum.

**Human clinical trials, counted as trials.** From [`hydrocephalus.trials.csv`](./hydrocephalus.trials.csv), one row per trial, never per measurement.

| | Count |
|---|---:|
| Verified unique human trials | **12** |
| …with an endpoint-evaluable outcome | 12 |
| …flagged by their own source as an extension or roll-over protocol | 5 |
| …also contributing rows to the other CNS endpoint | 10 |
| Pending candidates — a trial report naming no registry entry | 7 |
| Human trial-derived measurement rows | 84 |
| Unique compounds across the verified trials | 4 |
| Human laboratory / ex-vivo measurement rows | 0 |

The human-laboratory row is **zero, and stated rather than hidden**: no in vitro or ex vivo human experiment in this corpus measures this endpoint. Nothing was reclassified to fill it.

Pending candidates are excluded from the verified total on purpose. A publication reporting a trial establishes the trial, but its registry identifier has to come from a document — supplying one from recall would be exactly the fabricated trial identifier this dataset refuses to contain.

**Which hydrocephalus claim each row makes.** The endpoint is not one thing, and `endpoint_domain` cannot carry the distinction — it has a single `hydrocephalus` value, and its use in this corpus drifted by extraction lane. `hydroceph_tier` is derived from the readout instead, so it is lane-independent.

| Tier | Rows | What it is |
|---|---:|---|
| `ventricular_enlargement` | 88 | ventricular volume, ventriculomegaly, hydrocephalus incidence, macrocephaly — the endpoint itself |
| `pressure_or_composition` | 29 | raised intracranial or CSF opening pressure, CSF volume, outflow resistance, DTI-ALPS — supports a mechanism, is not a confirmed hydrocephalus event |
| `related_clinical_sign` | 16 | papilloedema and optic findings — a pressure sign, recorded separately because the two dissociate |
| `procedure_or_mechanism` | 4 | ependymal damage, cilia loss, meningitis, arachnoiditis — mechanism and procedure effects |
| `disease_background` | 7 | measured in patients given no oligonucleotide: a baseline rate, never an effect of a compound |
| `therapeutic_reduction` | 1 | the compound REDUCED the endpoint — an efficacy result, not a toxicity negative |

**Which zeros are negatives.** A grade of 0 means four different things, and only two of them are a measured negative.

| | Rows |
|---|---:|
| Grade-0 rows | 63 |
| …eligible as a measured negative (`negative_eligible=TRUE`) | 51 |
| …**not** eligible | 12 |

The ineligible rows are kept, with their evidence, and excluded from negative counts by one predicate:

- `disease_background` — 7 row(s): measured in patients given no oligonucleotide — a baseline rate, not a negative for any compound
- `review_required` — 4 row(s): no ascertainment basis could be established from the row's own source fields
- `therapeutic_reduction` — 1 row(s): the compound REDUCED the endpoint — measured, but an efficacy result, not evidence the compound is non-toxic

Rows can qualify under more than one reason, and the list above reports the tier reason first. Counted by `ascertainment` alone, independently of tier:

- `ascertainment = measured` — 6 row(s)
- `ascertainment = review_required` — 6 row(s)

<!-- END generated:evidence -->

### Corpus-level counters

| Item | Count | Basis |
|---|---:|---|
| Measurement rows | **145** | `challenge_priority = high_hydrocephalus` in the 2,538-row CNS corpus |
| Oligos | **13** | distinct `oligo_id` referenced by those rows |
| Oligos with a published sequence | **6 / 13** | rest are `TBD`; never reconstructed |
| Distinct `source_ref` documents | **40** | canonical identifiers |
| Distinct `source_id`s | **44** | |
| Rows carrying a verifier verdict | **38** | every hydrocephalus row was sampled for verification |
| Extraction status | complete for this pass | |

| `neurotox_grade` | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Rows | 63 | 13 | 53 | 16 |

That shape is the endpoint's central problem, not an artifact of curation: **the
evidence is almost entirely clinical, and within that, several different kinds of
clinical.** Twelve verified trials carry it; the remaining human rows are labels,
case reports, an exposed cohort and a disease-background rate, none of which is a
trial. See *Honest limits* below.

## Derivation

Curated as part of a single CNS corpus of 2,538 measurements serving both named CNS endpoints, partitioned by the corpus's own `challenge_priority` column — `high_hydrocephalus` here, everything else to [`./chronic-neurotoxicity.md`](./chronic-neurotoxicity.md). The partition is disjoint and exhaustive (145 + 2,393 = 2,538). Schema, methodology, verification record and source registry are shared with that dossier and listed there.

Every row carries `endpoint_domain = hydrocephalus` (141) or a directly related clinical neuro event (4), and `challenge_priority = high_hydrocephalus`.

## What the data contains

- **The tominersen ventricular-volume ladder** — absolute ventricular volume by dose arm with a concurrent placebo arm, from ClinicalTrials.gov posted results, plus a matching CSF neurofilament ladder. This is the best-anchored finding for the endpoint.
- **The nusinersen post-marketing signal** — the EU safety communication's individual case narratives, the SmPC statement of communicating hydrocephalus with some patients shunted, and a PSUR denominator.
- **Tofersen papilloedema and raised intracranial pressure**, recorded as *separate* readouts from hydrocephalus, because the two dissociate: one drug shows raised pressure with zero hydrocephalus, another shows ventriculomegaly. A model that collapses them learns a relationship that does not exist.
- **The untreated-disease baseline as data, not prose** — spinal muscular atrophy itself carries an incidence-rate ratio of 4.7 (95% CI 2.4–10.2) for hydrocephalus, from a matched cohort whose study window closes before nusinersen approval, so no participant was oligonucleotide-exposed by construction. Every ventriculomegaly row in an SMA patient has to be read against it.
- **A preclinical negative** — hydrocephalus incidence scored as an explicit endpoint in ASO-treated mice, with no change.

## What the original sweep established

The original dossier swept the 18 PDFs then in `sources/` for `hydrocephal` and found 7 hits in 2 files, neither an oligonucleotide source. That reading stands for that library. The conclusion drawn from it does not: the sweep measured **the sources held**, not the sources available, and the CNS pass acquired 40 documents bearing on this endpoint that were not in `sources/` at the time.

## Honest limits — this endpoint must not be overstated

- **The mechanistic floor is close to empty.** No published animal study was found in which an oligonucleotide *caused* hydrocephalus. The one apparent exception does not survive reading: an intracerebroventricular antisense against Gαi2 does dilate rat ventricles, but its own base-composition-matched mismatch control produced no effect, the dilatation was strictly unilateral, the molecule is an unmodified phosphodiester DNA 18-mer sharing no chemistry with any clinical ASO, and the effect required continuous minipump infusion where a single bolus did nothing. It supports "knocking down Gαi2 dilates rat ventricles"; it does not support "intrathecal ASOs cause hydrocephalus".
- **No non-human-primate ventricular-volume dataset exists** for any therapeutic oligonucleotide, and no CSF outflow-resistance or ependymal cilia-beat measurement for any modern chemistry.
- **No in vitro model of CSF dynamics** for oligonucleotide toxicity exists in any system — the missing human mechanistic model for a named endpoint. Eighteen further queries confirmed the emptiness is real rather than unsearched.
- **Grey literature is load-bearing.** Some rows rest on sponsor medical-affairs slide decks that cannot be independently re-fetched; they carry `redistribution=verify` and are the weakest evidence here.
- **Grades are provisional** on all 147 rows.

## Next step

The gap analysis in [`../NEXT-STEPS-CNS.md`](./hydrocephalus.next-steps.md) names the two things that would most strengthen this endpoint, both generation rather than curation: **ventricular volume as a routine endpoint in non-human-primate intrathecal studies** (imaging on animals already being dosed and imaged), and **a human choroid-plexus or ependymal organoid assay** dosed with clinical-stage oligonucleotides.

---

## Divided by toxicity, and what is duplicated

This dataset is one slice of the CNS corpus, produced by
[`scripts/split_by_endpoint.py`](./scripts/split_by_endpoint.py). Two things happen
in that split and they are **not** the same operation:

**Measurements divide.** A measurement is an observation of one toxicity, so the
rows partition — disjoint and exhaustive. This toxicity holds **147 measurement
rows**, and across all endpoints the per-toxicity counts sum exactly to the corpus
total. The script fails loudly if they ever stop summing, so the partition cannot
silently drift.

**Oligonucleotides duplicate.** A molecule is a compound *identity*, not an
observation. A drug studied for two toxicities belongs in both tables. This
toxicity's oligo table holds **13 molecules**, of which **5 also appear
under another toxicity** — 5 replicated under the same `oligo_id`, and 0
curated independently elsewhere and therefore carrying a *different* id there.

> **Consequence, because it is the easy mistake to make: oligo counts are not
> additive across toxicities. Row counts are.** Summing the oligo tables
> double-counts every molecule studied for more than one toxicity.

| File | What it is |
|---|---|
| [`hydrocephalus.measurements.csv`](./hydrocephalus.measurements.csv) | this toxicity's 147 graded measurement rows |
| [`hydrocephalus.oligos.csv`](./hydrocephalus.oligos.csv) | the 13 molecules those rows reference |
| [`hydrocephalus.shared-molecules.csv`](./hydrocephalus.shared-molecules.csv) | the 5 molecules also present under another toxicity, with the id they carry there |
| [`molecule_crosswalk.csv`](./molecule_crosswalk.csv) | the same ledger across every toxicity at once |

The crosswalk matters most for the 0 molecules curated independently under two
toxicities: nothing links `OLG###` to `CNS###`, so a model keyed on `oligo_id` would
treat one compound as two. Where both records carry a sequence, the split asserts
they agree base-for-base and **fails** if they do not — a disagreement would mean one
of the two is the wrong molecule. Across the whole repository there are currently
**no such conflicts**.

Cross-cutting artifacts are **duplicated into each toxicity that uses them** rather
than shared from a common folder, so every toxicity here is self-contained.
