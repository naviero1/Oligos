# Hydrocephalus — endpoint dossier

**Status:** `delivered` · **Register:** [`./README.md`](./README.md) · **Corpus documentation:** [`../README-CNS.md`](../README-CNS.md)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md#scope-authority)). It is **curated and delivered**: 147 graded per-measurement rows over 13 oligonucleotides, drawn from 40 distinct source documents.

> **This file previously said the opposite.** Until 2026-08-28 it recorded the endpoint as `not-addressed` — "nothing was acquired, extracted or decided… zero rows, zero oligos, zero `source_id`s" — and recommended recording it as out of scope. That was an accurate description of one branch (the 111-row kidney lineage) and a wrong description of the project. The recommendation is withdrawn; §"What the original sweep established" preserves the part of the record that still holds.

## Status

| Item | Count | Basis |
|---|---:|---|
| Measurement rows | **147** | `challenge_priority = high_hydrocephalus` in the 2,540-row CNS corpus |
| Oligos | **13** | distinct `oligo_id` referenced by those rows |
| Oligos with a published sequence | **6 / 13** | rest are `TBD`; never reconstructed |
| Distinct `source_ref` documents | **40** | canonical identifiers |
| Distinct `source_id`s | **44** | |
| Rows carrying a verifier verdict | **38** | every hydrocephalus row was sampled for verification |
| Extraction status | complete for this pass | |

| `neurotox_grade` | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Rows | 63 | 14 | 54 | 16 |

| Study type | clinical | animal in vivo | in vitro |
|---|---:|---:|---:|
| Rows | 133 | 12 | 2 |

That shape is the endpoint's central problem, not an artifact of curation: **the evidence is almost entirely clinical.** See *Honest limits* below.

## Derivation

Curated as part of a single CNS corpus of 2,540 measurements serving both named CNS endpoints, partitioned by the corpus's own `challenge_priority` column — `high_hydrocephalus` here, everything else to [`./chronic-neurotoxicity.md`](./chronic-neurotoxicity.md). The partition is disjoint and exhaustive (147 + 2,393 = 2,540). Schema, methodology, verification record and source registry are shared with that dossier and listed there.

Every row carries `endpoint_domain = hydrocephalus` (143) or a directly related clinical neuro event (4), and `challenge_priority = high_hydrocephalus`.

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

The gap analysis in [`../NEXT-STEPS-CNS.md`](../NEXT-STEPS-CNS.md) names the two things that would most strengthen this endpoint, both generation rather than curation: **ventricular volume as a routine endpoint in non-human-primate intrathecal studies** (imaging on animals already being dosed and imaged), and **a human choroid-plexus or ependymal organoid assay** dosed with clinical-stage oligonucleotides.
