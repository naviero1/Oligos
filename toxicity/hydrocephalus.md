# Hydrocephalus — endpoint dossier

**Status:** `delivered` · **Dataset:** [`./hydrocephalus/`](./hydrocephalus/README.md) · **Register:** [`./README.md`](./README.md) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md#scope-authority)). Until this pass it was `not-addressed`: zero rows, zero oligos, zero `source_id`s, no dedicated source, and no scope decision on record. It now carries a dataset of its own — **1,324 measurement rows over 50 oligonucleotides from 189 sources** — in [`./hydrocephalus/`](./hydrocephalus/README.md).

The previous version of this dossier set three conditions for advancing the endpoint and judged that meeting them would produce "a second dataset, not an extension of this one." That judgement was correct and has been followed: the new dataset has its own graded column, its own rubric, its own vocabularies and its own tables. **Nothing in `../data/`, `../schema.md`, `../METHODOLOGY.md`, `../sources/` or `../scripts/` was changed.** The renal dataset and this one sit side by side and are joined by nothing.

## Status

| | Value |
|---|---:|
| Oligonucleotides described | 50 |
| — of which carry at least one measurement | 44 |
| Measurement rows | 1,324 |
| — tier A (ventricular / CSF-volume outcome) | 797 |
| — tier B (CSF pressure, composition, flow, procedure) | 527 |
| Tier-A rows with a positive finding | 61 |
| Tier-A rows that are explicit measured negatives | 735 |
| Grade-3 (severe) rows | 22 |
| Distinct sources | 189 |
| Oligonucleotides with a published sequence | 10 of 50 |
| Per-position modification records | 202, over 10 oligonucleotides |
| Oligonucleotides with a known length | 10 of 50 |
| QC checks run / failed | 44 / 0 |

Every figure above is computed by the dataset's QC suite into `qc/stats.json` and rendered into its `README.md`. They are **transcribed** here and will drift if the dataset changes; [`./hydrocephalus/README.md`](./hydrocephalus/README.md) is authoritative.

## How the three conditions were met

| Condition set by the previous dossier | How it was met |
|---|---|
| "acquiring a primary source" | 53 sources across six modalities: ClinicalTrials.gov posted adverse-event tables, ClinicalTrials.gov pre-specified MRI outcome measures, openFDA FAERS, US DailyMed labels, EU EMA Summaries of Product Characteristics, and primary full-text literature including a disease-epidemiology cohort. Every payload is committed under `hydrocephalus/sources/raw/`, so the dataset rebuilds offline. |
| "adding CNS terms to the `tissue` and `readout_category` vocabularies" | Deliberately **not** done. Adding CNS terms to the renal vocabularies would have modified the delivered kidney dataset. The new dataset declares its own `cns_compartment` and `readout_category` vocabularies instead, leaving the renal ones untouched. |
| "the sequences of all oligos tested, as well as the location of all chemical modifications in each oligo" (Phase 2 brief) | Partly. [`data/modifications.csv`](./hydrocephalus/data/modifications.csv) gives the location of every modification for the two intrathecal ASOs whose labels state their motif in words, and the base at every position of the four sequenced siRNA duplexes — 122 position rows. Sequences and full per-position maps for nusinersen, tofersen, tominersen, inotersen, eplontersen and volanesorsen were recovered from the WHO INN Recommended lists by deterministic parse of the INN chemical name, validated against each label's molecular formula and, for tofersen, its stated 15-phosphorothioate/4-phosphodiester split. Still open for the double-stranded siRNAs and the morpholinos (OI-02). |
| "the methods used to purify and characterize oligo identity" (Phase 2 brief) | Recorded as `NOT_REPORTED` throughout, from evidence: a full-text sweep of all 16 committed US labels finds no drug-substance purity, purification or identity statement in any of them. The same finding as the sibling CNS release. |
| "writing a separate graded column with its own rubric" | `hydroceph_grade` (0–3), with a rubric written in ventricular and CSF terms at [`SCHEMA.md`](./hydrocephalus/SCHEMA.md). It is not a reuse of `nephrotox_grade` and is not transferable to it. |

## What changed since the `not-addressed` sweep

The previous dossier's sweeps stand and are not withdrawn. A case-insensitive `hydrocephal` sweep over the 18 PDFs in `../sources/` still returns 7 hits in 2 files, both reference PDFs, neither of them oligonucleotide evidence; the six textbook occurrences are still small-molecule and infectious teratology. **That finding was about this repository's local PDF library, not about the world.** It showed the library held nothing for this endpoint — true then, true now. The new dataset was built from sources that were never in that library and had to be retrieved.

The prior dossier's first "known issue" was that no scope decision existed anywhere outside itself, and it recommended recording the endpoint as swept and out of scope. That recommendation is now **withdrawn** rather than left standing: the endpoint is in scope and populated.

One material circumstance differed between the two passes. The kidney dataset was assembled in sessions whose egress policy blocked outbound fetch (`../sources/SOURCES.md` network-status note; `../README.md` §"Status & next steps"), which is why its lowest-provenance tier is 36 rows taken from search-engine summaries. That restriction did not apply here: ClinicalTrials.gov, openFDA, DailyMed and Europe PMC were all directly reachable, and **no row in the hydrocephalus dataset comes from a search summary.**

## Sources allocated

No PDF in `../sources/` is allocated to this endpoint; the two files containing the word remain allocated to [`./cross-cutting.md`](./cross-cutting.md), unchanged. This endpoint's sources live under [`./hydrocephalus/sources/raw/`](./hydrocephalus/sources/raw/) and are registered in `./hydrocephalus/data/sources.csv` — **not** in `../sources/SOURCES.md`. The two registries are kept apart for the same reason the two sets of tables are.

The largest sources are the tominersen trial records (NCT03761849 GENERATION HD1; NCT03342053 and NCT03842969, the open-label extensions), the FAERS aggregate across 19 marketed oligonucleotides, the SPINRAZA and QALSODY labels, and two CC BY articles: the index case report and the SMA disease-baseline cohort.

## What the dataset records

Three findings bear on how the rest of this register should be read.

**Ventricular volume was measured, and it rose with dose.** The tominersen phase 1/2a trial made ventricular volume a pre-specified structural-MRI outcome. From screening to day 197 the placebo arm moved 35.58 → 36.46 mL (+2.5%, n=12) while the two highest dose arms moved +13.0% (n=9) and +19.9% (n=10); in the open-label extension the ventricular-volume boundary shift integral rose 46.1% on monthly against 18.8% on bimonthly dosing at 15 months. These are the only rows in either dataset where the ventricles were measured rather than incidentally observed. Group sizes are small and no test statistic is computed.

**Within registered trials the signal is tominersen's alone — but the endpoint is not tominersen-specific.** Serious hydrocephalus or normal-pressure hydrocephalus adverse events appear in three separate tominersen studies, including **2/263 against 0/264 in the concurrent placebo arm** of GENERATION HD1. No other intrathecal programme with posted results reports a tier-A serious event. That is a statement about registered trials only: the two strongest drug-attributed cases in the dataset come from outside that record. In an n-of-1 protocol, **both** infants dosed intrathecally with valeriasen — a different ASO, target, indication and age group — developed ventricular enlargement, one requiring endoscopic third ventriculostomy at a CSF opening pressure of 55 cmH₂O and the other an external drain and then a ventriculoperitoneal shunt; the authors call it "a potential monitorable toxicity of some intrathecal antisense oligonucleotides".

**The two drug-attributed cases support different mechanisms.** The tominersen index case was attributed to a sterile meningitis (CSF protein 2.64 g/L, lymphocytosis); the KCNT1 patients had a negative CSF inflammatory panel and a dose-related working hypothesis, evidenced by a reduced-dose rechallenge delivered without recurrence. The dataset keeps the two apart on `tox_axis` and `event_cluster_id` rather than pooling them into one "hydrocephalus" count.

**The mechanism is documented end to end in a single patient.** Rising CSF protein (to 2.64 g/L) and lymphocytosis, then ventricular dilation on serial MRI, then increased resistance to CSF outflow measured directly by lumbar infusion study, then a ventriculoperitoneal shunt — with the authors attributing the sequence to a drug-induced sterile meningitis. This is why the dataset records CSF-composition findings alongside ventricular ones, under an explicit tier label so that the two are never pooled by accident.

**An oligonucleotide sits on both sides of this endpoint.** A SPAK-targeting siRNA prevents ventriculomegaly in a rodent model while an AQP4-targeting siRNA aggravates it — so "oligonucleotide" is not a direction of effect here, and the protective rows are carried on their own `tox_axis` and left ungraded so they cannot be read as absent toxicity.

**The disease is a fourfold confounder.** In the era before nusinersen was approved, SMA patients had a hydrocephalus incidence rate ratio of **4.7 (95% CI 2.4–10.2)** against matched non-SMA controls. Those baseline rows are in the dataset, carrying no compound, on `tox_axis = disease_background_rate`. Any analysis of an SMA-indicated oligonucleotide that omits them will over-attribute.

## Known issues

- **Grades are provisional.** All graded rows ship `grade_status = provisional`; no subject-matter expert has reviewed the rubric or its application.
- **No sequences.** The Challenge's "sequences of all oligos tested" requirement is unmet for this endpoint (`METHODOLOGY.md` OI-02). Design predictors are chemistry- and design-level only.
- **Nonclinical coverage is thin** (OI-03): five rodent rows from two studies, all qualitative because both sources publish their ventricular measurements graphically and this project reads no number off a figure. The dose–response resolution the clinical record cannot give is still missing.
- **Only one designed control** (OI-08): the AQP4 study's scrambled non-targeting siRNA. Every other negative in the dataset is a comparator arm, a reported zero or a silent label — the same weakness a review found in the sibling kidney dataset, now at least recorded in `arm_role` and `ascertainment` rather than glossed.
- ~~253 tier-A negatives rest on an unverified absence argument~~ — **resolved.** 42 CFR 11.48(a)(4)(ii)(A) requires a results submission to table *all* serious adverse events with no frequency threshold, so absence of a tier-A term from a posted serious-adverse-event table is a reported zero for serious events. The regulation is committed and cited per row. Two limits remain in-row: a non-serious ventricular event below the 5 percent threshold of subparagraph (B) would not appear, and none of this evidences that ventricular imaging was done.
- ~~The counts in this dossier are transcribed, not regenerated, and will drift if the dataset changes~~ — **resolved**, after they drifted exactly as predicted. Counts are now rendered into this file from `qc/stats.json` by `scripts/render_docs.py`; the `<!--stat:…-->` markers are generated, not hand-edited.
- **The Phase 2 submission is assembled for this endpoint.** Every requirement is mapped to its status and owner in [`hydrocephalus/PHASE2_COMPLIANCE.md`](./hydrocephalus/PHASE2_COMPLIANCE.md). The dataset, the ML analysis, the narrative, methodology and PADP PDFs, a supplementary source and provenance register, and a CC BY 4.0 LICENSE for the curation layer are all present. The remaining gaps are stated there, not hidden: no human in vitro system, and sequences for only <!--stat:oligos_with_sequence-->13<!--/stat--> of <!--stat:n_oligos-->53<!--/stat--> compounds.
- **Human and animal evidence are split** by `subject_class`, with generated views. The release is <!--stat:n_human_rows-->1,351<!--/stat--> human rows against <!--stat:n_animal_rows-->10<!--/stat--> animal and <!--stat:n_in_vitro_rows-->2<!--/stat--> in vitro — the in vitro rows being an **animal** in-vitro/in-vivo pair on one compound, against a Phase 2 brief that calls in vitro *human* systems a particular interest. That gap is unclosed.
- **100 further verified sources are retrieved but not extracted**, listed in [`hydrocephalus/notes/source_backlog.md`](./hydrocephalus/notes/source_backlog.md) — EudraVigilance, WHO VigiBase, EMA CHMP assessment reports, FDA pharmacology/toxicology reviews, PMDA documents and two patent families among them. This is the release's completeness limit, stated rather than left to be discovered.
- **EMA rows carry `redistribution = verify`.** Reuse terms for EMA product information were not established; the verbatim text is quoted as evidence, but a redistributor should resolve the licence before republishing those eight rows' values.
- **One compound row is a composite** (OI-07): `casimersen_or_golodirsen` covers a trial whose posted table does not separate the two compounds.

## Next step

1. Recover sequences through the WHO INN Recommended lists (OI-02) — the route the sibling kidney dataset already built and validated.
2. Extract nonclinical intracerebroventricular and intrathecal animal rows (OI-03), the only available source of dose–response for this endpoint.
