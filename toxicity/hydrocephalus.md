# Hydrocephalus — endpoint dossier

**Status:** `delivered` · **Dataset:** [`./hydrocephalus/`](./hydrocephalus/README.md) · **Register:** [`./README.md`](./README.md) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list of toxicities of interest (quoted verbatim in [`./README.md`](./README.md#scope-authority)). Until this pass it was `not-addressed`: zero rows, zero oligos, zero `source_id`s, no dedicated source, and no scope decision on record. It now carries a dataset of its own — **904 measurement rows over 34 oligonucleotides from 52 sources** — in [`./hydrocephalus/`](./hydrocephalus/README.md).

The previous version of this dossier set three conditions for advancing the endpoint and judged that meeting them would produce "a second dataset, not an extension of this one." That judgement was correct and has been followed: the new dataset has its own graded column, its own rubric, its own vocabularies and its own tables. **Nothing in `../data/`, `../schema.md`, `../METHODOLOGY.md`, `../sources/` or `../scripts/` was changed.** The renal dataset and this one sit side by side and are joined by nothing.

## Status

| | Value |
|---|---:|
| Oligonucleotides described | 34 |
| — of which carry at least one measurement | 29 |
| Measurement rows | 904 |
| — tier A (ventricular / CSF-volume outcome) | 382 |
| — tier B (CSF pressure, composition, flow, procedure) | 522 |
| Tier-A rows with a positive finding | 55 |
| Tier-A rows that are explicit measured negatives | 326 |
| Grade-3 (severe) rows | 18 |
| Distinct sources | 52 |
| Oligonucleotides with a published sequence | 4 of 34 — all research reagents; see `METHODOLOGY.md` OI-02 |
| QC checks run / failed | 30 / 0 |

Every figure above is computed by the dataset's QC suite into `qc/stats.json` and rendered into its `README.md`. They are **transcribed** here and will drift if the dataset changes; [`./hydrocephalus/README.md`](./hydrocephalus/README.md) is authoritative.

## How the three conditions were met

| Condition set by the previous dossier | How it was met |
|---|---|
| "acquiring a primary source" | 52 sources across six modalities: ClinicalTrials.gov posted adverse-event tables, ClinicalTrials.gov pre-specified MRI outcome measures, openFDA FAERS, US DailyMed labels, EU EMA Summaries of Product Characteristics, and primary full-text literature including a disease-epidemiology cohort. Every payload is committed under `hydrocephalus/sources/raw/`, so the dataset rebuilds offline. |
| "adding CNS terms to the `tissue` and `readout_category` vocabularies" | Deliberately **not** done. Adding CNS terms to the renal vocabularies would have modified the delivered kidney dataset. The new dataset declares its own `cns_compartment` and `readout_category` vocabularies instead, leaving the renal ones untouched. |
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

**Hydrocephalus is tominersen-specific in the trial record.** Serious hydrocephalus or normal-pressure hydrocephalus adverse events appear in three separate tominersen studies, including **2/263 against 0/264 in the concurrent placebo arm** of GENERATION HD1, with cerebral ventricle dilatation across all three dose arms of the open-label extension. No other intrathecal oligonucleotide programme with posted results — nusinersen, tofersen, BIIB080, BIIB105, WVE-120101, WVE-120102, WVE-003 — reports a tier-A serious event. The others show the pressure and inflammation axes without the ventricular one.

**The mechanism is documented end to end in a single patient.** Rising CSF protein (to 2.64 g/L) and lymphocytosis, then ventricular dilation on serial MRI, then increased resistance to CSF outflow measured directly by lumbar infusion study, then a ventriculoperitoneal shunt — with the authors attributing the sequence to a drug-induced sterile meningitis. This is why the dataset records CSF-composition findings alongside ventricular ones, under an explicit tier label so that the two are never pooled by accident.

**An oligonucleotide sits on both sides of this endpoint.** A SPAK-targeting siRNA prevents ventriculomegaly in a rodent model while an AQP4-targeting siRNA aggravates it — so "oligonucleotide" is not a direction of effect here, and the protective rows are carried on their own `tox_axis` and left ungraded so they cannot be read as absent toxicity.

**The disease is a fourfold confounder.** In the era before nusinersen was approved, SMA patients had a hydrocephalus incidence rate ratio of **4.7 (95% CI 2.4–10.2)** against matched non-SMA controls. Those baseline rows are in the dataset, carrying no compound, on `tox_axis = disease_background_rate`. Any analysis of an SMA-indicated oligonucleotide that omits them will over-attribute.

## Known issues

- **Grades are provisional.** All graded rows ship `grade_status = provisional`; no subject-matter expert has reviewed the rubric or its application.
- **No sequences.** The Challenge's "sequences of all oligos tested" requirement is unmet for this endpoint (`METHODOLOGY.md` OI-02). Design predictors are chemistry- and design-level only.
- **Nonclinical coverage is thin** (OI-03): five rodent rows from two studies, all qualitative because both sources publish their ventricular measurements graphically and this project reads no number off a figure. The dose–response resolution the clinical record cannot give is still missing.
- **Only one designed control** (OI-08): the AQP4 study's scrambled non-targeting siRNA. Every other negative in the dataset is a comparator arm, a reported zero or a silent label — the same weakness a review found in the sibling kidney dataset, now at least recorded in `arm_role` and `ascertainment` rather than glossed.
- ~~253 tier-A negatives rest on an unverified absence argument~~ — **resolved.** 42 CFR 11.48(a)(4)(ii)(A) requires a results submission to table *all* serious adverse events with no frequency threshold, so absence of a tier-A term from a posted serious-adverse-event table is a reported zero for serious events. The regulation is committed and cited per row. Two limits remain in-row: a non-serious ventricular event below the 5 percent threshold of subparagraph (B) would not appear, and none of this evidences that ventricular imaging was done.
- **The counts in this dossier are transcribed**, not regenerated, and will drift if the dataset changes.
- **EMA rows carry `redistribution = verify`.** Reuse terms for EMA product information were not established; the verbatim text is quoted as evidence, but a redistributor should resolve the licence before republishing those eight rows' values.
- **One compound row is a composite** (OI-07): `casimersen_or_golodirsen` covers a trial whose posted table does not separate the two compounds.

## Next step

1. Recover sequences through the WHO INN Recommended lists (OI-02) — the route the sibling kidney dataset already built and validated.
2. Extract nonclinical intracerebroventricular and intrathecal animal rows (OI-03), the only available source of dose–response for this endpoint.
