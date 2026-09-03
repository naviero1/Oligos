# OligoTox-Kidney — Narrative Document

**NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge, Phase 2 (Data Generation)**
**Endpoint: kidney toxicity / nephrotoxicity**

*Phase 2 narrative deliverable. Target length ≤ 12 pages when rendered to PDF.*

---

## 1. Executive summary

**OligoTox-Kidney** is an openly-licensed, per-measurement dataset of oligonucleotide
**kidney toxicity**. It contains **246 measurements across 65 unique oligonucleotides**
spanning **35 target genes**, every row traceable to a named source table, figure or
label section, and every row strict-kidney (`is_kidney_specific = TRUE` on 246/246).

The dataset is an **in-silico curation** of published and public-domain data. No wet-lab
work was performed. Its contribution is not new bench measurement but **harmonisation**:
values that exist today only as scattered patent tables, label sections and supplementary
files, reduced to one schema with one grading rubric and per-row provenance, so they can
be trained on and audited.

### Composition

| `subject_class` | rows | share |
|---|---:|---:|
| `animal_invitro` (rat primary PTEC) | 81 | 32.9% |
| `human_invitro` (primary human PTEC, PTEC-TERT1, ciPTEC, 3D-RPTEC, tubule-on-chip) | 67 | 27.2% |
| `animal_invivo` (rat, mouse, monkey) | 56 | 22.8% |
| `human_clinical` (trials, labels, case reports) | 42 | 17.1% |

**109 of 246 rows (44.3%) are human**, and **67 are human in-vitro** — the category the
Phase 2 announcement names as of particular interest. A further 81 rows are animal
in-vitro on the *same assay and compounds*, which is what makes the human↔animal
extrapolation analysis in §5 possible.

### Controls

We distinguish **designed controls** from **negative observations**, because conflating
them overstates the evidence:

- **Designed negative control.** Patent compound **1-1** (`OLG045`), a scrambled-sequence
  ASO the source explicitly designates *innocuous* and uses as its normalisation
  reference. It appears in 25 rows and grades **0 in every one**. Two independent grading
  rubrics were *anchored* on it (§4.3), so it functions as a control in the strict sense.
- **Designed positive anchors.** **SPC5001** / patent compound **3-1** (`OLG002`/`OLG047`)
  — a known human nephrotoxin that caused acute tubular necrosis in a clinical trial — and
  patent compound **4-1** (`OLG048`), the source's *high*-toxicity reference. **Inotersen**
  (`OLG001`) anchors the severe clinical end (grade 3, crescentic glomerulonephritis).
- **Negative observations, not controls.** The remaining grade-0 rows are compounds
  measured at a non-toxic exposure. They are evidence, but they were not *designed* as
  controls, and §3 explains why some of them are weaker evidence than they appear.

### Headline numbers

- 65 oligonucleotides · 246 measurements · 35 target genes · 15 bridging oligos
- Sequences for **55/65**; the 10 gaps are structural, not clerical (§4.4)
- Grade distribution 0/1/2/3 = **97 / 58 / 60 / 31** — a genuinely graded label, not a
  rare-event problem
- Modalities: ASO gapmer 40 · GalNAc-siRNA 12 · splice-switching ASO 4 · PMO 4 · siRNA 2 ·
  1st-gen PS-DNA 2 · aptamer 1
- Licence **CC BY 4.0**, with per-row `redistribution` status retained

---

## 2. Main findings and conclusions

### 2.1 Animal-to-human translation is bidirectional, not one-way

The received wisdom is that animal renal toxicology **over-predicts** human effects for
2′-MOE ASOs. Our 15 bridging oligos — those carrying evidence on both sides of the
human/animal divide — do not support that as a rule:

| concordance | oligos |
|---|---:|
| concordant | 7 |
| animal over-predicts | 6 |
| **animal under-predicts** | **2** |

The two under-predictions are the safety-relevant direction and involve the dataset's most
severe human findings: **inotersen** (human grade 3 crescentic glomerulonephritis against
animal grade 1) and **givosiran** (human 2, animal 1). A screening cascade calibrated on
the assumption that animals over-predict would have under-called both.

This is a bounded finding, and we state the bounds: 15 oligos is not a rule, and 3 of the
6 over-prediction verdicts rest on human grade-0 values that direct source retrieval could
not support (§3). Model the direction as an open question, not a constant.

### 2.2 Human cell systems can be more sensitive than the animal in-vivo grade

Patent compound **3-1** — the same molecule as SPC5001, which caused acute tubular
necrosis and AKI in humans — grades **3 in human in-vitro** against **2 in rat in-vivo**
within a single laboratory's data. The human cell system recovered severity the animal
in-vivo grading did not. That is exactly the translational claim the Challenge is
interested in, demonstrated on a compound whose human outcome is independently documented.

### 2.3 A provenance/outcome confound, quantified — and partly corrected

The most important methodological finding is about the dataset itself. When clinical rows
were cross-tabulated by **how well sourced they were** against **what they concluded**,
provenance predicted outcome almost perfectly: of 20 rows derived from search summaries,
**zero** reached grade ≥2, against 11 of 22 anchor-sourced rows (one-sided Fisher
**p = 4.5 × 10⁻⁵**; expected 5.6 severe among the unverified block, observed 0).

Direct retrieval of the underlying documents for 7 of the unverified absence claims found
**only one** that survived as a measured negative. The rest were cases where renal
endpoints were never measured, or were not reported in the cited source — and in two
instances the trials had *excluded* renally impaired patients at enrolment, so the study
design could not have detected nephrotoxicity.

**A dataset that encodes this without marking it teaches a model to predict "does this
compound have a regulatory paper trail", not renal biology** — and that shortcut inverts
on prospective compounds, which have no dossier and would be scored non-toxic by
construction. That is the wrong error direction for a safety model.

Two corrections were applied. First, three approved drugs with *measured* human negatives
were added (§4.2), weakening the association **3.7×** to p = 1.65 × 10⁻⁴. Second, and more
importantly, the schema now carries **`renal_endpoints_measured`** (§4.5), which separates
"measured and unremarkable" from "never looked". **13 grade-0 clinical rows are explicitly
flagged as not supported as measured negatives.** Consumers can exclude, down-weight or
impute them; they can no longer be mistaken for safety evidence.

We report this prominently rather than quietly fixing it, because the confound is not
unique to us — it is a structural hazard of curating safety data from heterogeneous
sources, and the field would benefit from it being named.

### 2.4 Nephrotoxicity here is functional before it is cytotoxic

145 of 246 rows are injury-biomarker readouts and only 7 are viability. This reflects the
underlying biology: phosphorothioate ASOs accumulate in proximal tubule epithelium via
megalin/cubilin endocytosis and produce reversible low-molecular-weight proteinuria
**without loss of viability**. A viability-only screen under-calls this phenotype. The
schema therefore captures KIM-1, EGF/EGFR, α1-microglobulin, clusterin, cystatin C and
lysosomal load alongside function.

---

## 3. How the data were produced

### 3.1 Design

- **Grain.** One row = oligo × system/subject × delivery × concentration/dose × readout.
  The same oligo at one concentration read on KIM-1 *and* viability is two rows.
- **Two normalised tables**, joined on `oligo_id`: `oligos.csv` (identity and design
  predictors, 65 rows × 20 columns) and `measurements.csv` (outcomes and context, 246 × 25).
  A denormalised analysis view (`oligotox_kidney_merged.csv`, 246 × 44) is **generated,
  never hand-edited**.
- **Strict-kidney scope.** Verified, not asserted: 246/246 rows `is_kidney_specific=TRUE`,
  tissue values only `kidney` (79) and `proximal_tubule` (167), zero hepatic readouts,
  models or sources.

### 3.2 Acquisition paths

Each row records which path produced it via `source_id`:

1. **Local full-text extraction** of primary-source PDFs (drisapersen/ciPTEC, Sandelius
   urinary biomarker panel, Moisan human PTEC panel, two Roche nephrotoxicity patents).
2. **Secondary/review extraction**, used for cross-checking rather than as primary evidence.
3. **Search-summary derivation (`WS`)**, from an early session whose network policy blocked
   full-text fetch. These 36 rows are flagged and are the subject of §2.3.
4. **WHO INN nomenclature derivation** — described in §4.4, and the methodological
   contribution we would most want reused.

### 3.3 Computational processing

Every transformation is a committed, re-runnable script; none of the derived values is
hand-entered. `split_human_animal.py` derives `subject_class` and the bridge view;
`extract_patent_table2.py` and `extract_n4_table5.py` parse the two patent tables;
`fill_inn_sequences.py` derives sequences from INN nomenclature;
`add_endpoint_provenance.py` derives `renal_endpoints_measured`; `build_merged.py`
regenerates the analysis view.

Two extraction hazards are worth recording because they silently produce plausible wrong
answers:

- **Table text layers interleave columns.** Both patent tables extract as a flat number
  stream that cannot be mapped back to (compound, concentration, system, timepoint). Both
  extractors therefore parse the *layout-preserving* text and **check parsed values against
  anchors taken from the printed table** before writing; both refuse to write a partial table.
- **Case encodes chemistry.** In gapmer sequences, upper case marks 2′-MOE/cEt wings and
  lower case the DNA gap. A case-sensitive validator reports these correct rows as
  malformed — ours flagged 22 valid rows before being corrected.

### 3.4 A corrected error, disclosed

During final QC, **21 rows — 19% of the then-dataset** — were found to record a rat study
as a mouse study. The source patent binds its Table 1 to a method section describing
"Wistar Han Crl : WI (Han) male rats", dosing "at 40 mg/kg on days 1 and 8", a "Multiplex
MAP **Rat** Kidney Toxicity Magnetic Bead Panel 2", and sacrifice "on day 15". The rows
said mouse, 7 days, dose unknown. All four statements were verified against the patent
before correction. Species distribution moved from mouse 30 / rat 8 to **rat 29 / mouse 9**,
and 21 rows gained a published dose.

We disclose this because it is the kind of error that survives peer review when a dataset
is presented only as totals, and because it is an argument for the per-row provenance
discipline that caught it.

---

## 4. Indicators, predictors, and their distributions

### 4.1 Dependent variable — `nephrotox_grade` (0–3)

| Grade | Definition | n |
|---|---|---:|
| 0 | No renal signal at tested exposure | 97 |
| 1 | Mild/functional, reversible; no viability loss | 58 |
| 2 | Moderate — clear injury-biomarker rise and/or histopathology | 60 |
| 3 | Severe — AKI, glomerulonephritis, renal failure, dose-limiting | 31 |

Distribution by subject class:

| class | g0 | g1 | g2 | g3 |
|---|---:|---:|---:|---:|
| human_clinical | 21 | 10 | 6 | 5 |
| human_invitro | 33 | 12 | 17 | 5 |
| animal_invitro | 37 | 21 | 12 | 11 |
| animal_invivo | 6 | 15 | 25 | 10 |

All grades carry `grade_provisional` pending subject-matter sign-off.

### 4.2 Readouts

`injury_biomarker` 145 · `functional` 35 · `clinical_renal_outcome` 30 ·
`histopathology` 27 · `viability` 7 · `accumulation` 2. Delivery is
`gymnotic_free_uptake` 148 · `systemic_dose` 93 · `intrathecal` 3 · `intravitreal` 1 ·
`oral` 1. **207 of 246 rows carry a numeric dose or concentration.**

A caveat that applies to five compounds: all three DMD PMO labels warn that **serum
creatinine is unreliable in Duchenne patients** because of reduced skeletal muscle mass.
Creatinine-based renal readouts in DMD populations must be read with that in mind; the
rows added from those labels record cystatin C, UPCR and urine dipstick instead.

### 4.3 Grading rubrics for the quantitative panels

The two patent panels report continuous biomarker values, so grades were thresholded. The
thresholds are **stated and anchored, not free**: in each case the floor is set so that the
source's own innocuous reference compound grades 0 on every one of its cells.

- **Extracellular EGF, % of saline** (human PTEC / PTEC-TERT1): <200 / 200–499 / 500–1499 /
  ≥1500 → 0/1/2/3. Compound 1-1 grades 0 on all 16 cells, and grade then tracks the
  source's own in-vivo classification monotonically (innocuous 16×0; medium 10/3/2/1;
  high 4/4/4/4).
- **EGFR mRNA and KIM-1, % of compound 1-1** (rat primary PTEC): KIM-1 rises with injury
  (<200 / 200–499 / 500–1499 / ≥1500); EGFR falls (>70 / 40–70 / 20–39 / <20). Compound 1-1
  grades 0 on all 9 cells.

The two panels use **different normalisations** — % saline versus % compound 1-1 — recorded
in `readout_unit` and flagged in `notes` so they are never silently pooled.

### 4.4 Design predictors

| Variable | Distribution |
|---|---|
| Modality | ASO gapmer 40 · GalNAc-siRNA 12 · SSO 4 · PMO 4 · siRNA 2 · PS-DNA 2 · aptamer 1 |
| Backbone | full-PS 45 · PS/PO-mix 15 · PMO-neutral 4 · mixed 1 |
| Conjugate | none 48 · GalNAc 16 · PEG 1 |
| Stage | research panel 30 · approved 19 · phase 3 (incl. discontinued) 9 · phase 2 5 · phase 1 1 · class-level 1 |
| Sequence available | **55 / 65** |
| Identity confirmation | patent sequence listing 25 · WHO INN nomenclature 20 · regulatory label 7 · publication 3 · not established 10 |

**Sequence recovery from WHO INN nomenclature.** 20 sequences were recovered by parsing
the residue-by-residue chemical nomenclature WHO publishes for named oligonucleotides
(`2'-O-methyl-P-thiocytidylyl-(3'→5')-…`). This is a deterministic parse rather than a
transcription, and it is self-checking in two ways: INN writes one strand with (3′→5′)
linkages and its partner with (5′→3′), so mishandling direction yields a *reversed* strand
— the parser was validated by reproducing two sequences already in the table
character-for-character before any new row was written — and every duplex was required to
show its guide strand as the exact reverse complement of its sense strand, with residue
counts cross-checked against the published molecular formula where the phosphorus count
fixes the length. We believe this method is reusable by any group needing sequences for
INN-named oligonucleotides.

The 10 remaining gaps are structural: 6 proprietary research compounds whose sponsors never
published sequences, 2 class-level aggregate rows for which a single sequence is not
meaningful, and 2 Ionis development-code compounds that never received an INN.

### 4.5 Provenance variables

`renal_endpoints_measured` — `measured_and_reported` 233 · `cannot_determine` 8 ·
`not_measured` 3 · `not_reported_in_source` 2. This field exists so that a grade of 0 on a
row that is not `measured_and_reported` reads as **"not established"**, never as "safe".

`purity_pct` and `purity_method` are **`TBD` for all 65 oligos**. This is a genuine and
unavoidable limitation of a curation-type dataset, and we verified it rather than assuming
it: both source patents were searched for purity, HPLC, UPLC, LC-MS and mass-spectrometry
language and neither reports any; labels and trial publications do not publish per-batch
purity. What *can* be answered is the identity half of the requirement, and
`identity_confirmation` records for every oligo how its identity was established.

---

## 5. The gap this addresses

Public oligonucleotide toxicity data is dominated by **hepatotoxicity**. Kidney data is
thinner, more scattered, and disproportionately locked in formats that resist reuse —
patent example tables, label sections, supplementary PDFs. Three specific gaps are closed
here.

**A harmonised kidney corpus with per-row provenance.** 246 measurements under one schema
and one rubric, each traceable to a named table or section, spanning in-vitro human and
animal cell systems, animal in-vivo, and human clinical outcomes.

**Human in-vitro data at usable scale, paired with animal data on the same compounds.**
67 human in-vitro rows and 81 animal in-vitro rows, of which the patent panels supply the
same compounds in **human cells, rat cells, and rat in vivo from a single laboratory** —
three-way comparisons with no cross-study confounding. This is the configuration the
Challenge's extrapolation criterion asks for, and it is rare in public data.

**Two reusable methods.** The INN sequence-recovery procedure (§4.4), and the
`renal_endpoints_measured` distinction (§4.5). The second is the more transferable: any
curated safety dataset assembled from heterogeneous sources is exposed to the same
confound, and most do not carry a field that would reveal it.

---

## 6. Use in predictive modelling

### 6.1 What the dataset supports today

The merged view carries design predictors and graded outcome on the same row, so no join
is required. Reasonable first targets: ordinal prediction of `nephrotox_grade` from
chemistry and design; binary "reaches grade ≥2"; and — the most interesting — **predicting
the human grade from the animal grade** on the bridge set.

### 6.2 How it must be used, to avoid learning the wrong thing

These are not generic caveats; they follow from findings in this dataset.

1. **Filter on `renal_endpoints_measured`.** Rows that are not `measured_and_reported`
   should be excluded or treated as missing-label, never as negatives. Otherwise the model
   learns provenance (§2.3).
2. **Group splits by `oligo_id`, never random row splits.** Compounds contribute up to 25
   rows each; random splitting puts the same molecule on both sides and inflates
   performance.
3. **Do not pool the two normalisations.** % saline and % compound 1-1 are different
   scales; `readout_unit` distinguishes them.
4. **Treat `subject_class` as a first-class feature or a stratifier.** Grade distributions
   differ sharply across the four classes — animal in-vivo is 6/15/25/10, human clinical
   21/10/6/5. A model blind to it will confound assay severity with compound severity.
5. **Expect small-n on the bridge.** 15 oligos supports descriptive translation analysis,
   not a fitted species-correction model.

### 6.3 Honest limits

- Grades are **provisional** pending subject-matter sign-off.
- Purity is absent for every oligo (§4.5).
- 36 `WS` rows remain search-derived; 13 grade-0 clinical rows are flagged unsupported.
- The confound is **reduced, not eliminated** (p = 1.65 × 10⁻⁴).
- 39 rows still lack a numeric dose, mostly awaiting FDA Pharmacology/Toxicology reviews.

We would rather ship a dataset whose weaknesses are enumerated and machine-readable than
one whose totals look cleaner. Every limitation above is either a flagged column value or
a documented row set, so a modeller can act on it programmatically rather than having to
rediscover it.

---

## 7. Access

All data, schema, extraction scripts and documentation are in the project repository under
`toxicity/kidney/`, licensed **CC BY 4.0** (repository-root `LICENSE`), with per-row
`redistribution` status retained for values whose underlying sources carry their own terms.
Source PDFs are included for verification and are not covered by that licence.

| Artefact | Path |
|---|---|
| Oligo design table | `data/oligos.csv` (65 × 20) |
| Measurement table | `data/measurements.csv` (246 × 25) |
| Merged analysis view | `data/oligotox_kidney_merged.csv` (246 × 44, generated) |
| Human/animal bridge view | `data/human_animal_bridge.csv` (15 oligos) |
| Data dictionary & schema | `schema.md` |
| Methodology | `METHODOLOGY.md` (long form), `METHODOLOGY_PHASE2.md` (submission) |
| Validation of the confound | `CLINICAL_VALIDATION.md` |
| Independent strict review | `REVIEW-2026-08.md` |
| Public access plan | `PADP.md` |
