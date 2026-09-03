# Methodology — OligoTox-Kidney Dataset

Methodology and provenance documentation for the **OligoTox-Kidney** dataset, a
curated, openly-releasable, per-measurement dataset of oligonucleotide
**kidney toxicity / nephrotoxicity** for the NIH/NCATS Oligonucleotide Toxicity
(OligoTox) Open Data Challenge, **Phase 2 (Data Generation Phase)**.

> **Nature of the dataset.** This is an **in-silico curation** of pre-existing,
> publicly reported data — not wet-lab-generated data. The "materials and
> methods" below therefore describe **source identification, extraction,
> harmonization, grading, provenance, and quality control**, i.e. how the
> dataset was *assembled and computationally processed*, in the spirit of the
> Phase 2 methodology requirement.

Snapshot at this revision: **65 oligonucleotides · 159 measurements · 35 target
genes · all strict-kidney** (`is_kidney_specific = TRUE`).

---

## 1. Scope and design decisions

- **Endpoint:** kidney toxicity / nephrotoxicity (a named OligoTox endpoint of interest).
- **Granularity:** **strict-kidney, per-measurement.** One row =
  oligo × cell-model/subject × delivery × concentration/dose × readout.
- **Coverage goal:** span all therapeutic oligonucleotide modalities, study
  types (in-vitro / animal / clinical), and the full toxicity-severity range,
  including **negative controls**.
- **Driving domain fact:** oligonucleotide nephrotoxicity is frequently
  **functional, not cytotoxic** — phosphorothioate ASOs accumulate in proximal
  tubule epithelial cells via megalin/cubilin endocytosis, producing reversible
  low-molecular-weight proteinuria (impaired albumin/α1-microglobulin/RAP
  reabsorption) **without loss of viability**. The schema therefore captures
  functional and injury-biomarker readouts (KIM-1, NGAL, clusterin, cystatin C,
  A1M, lysosomal load), not viability alone.

## 2. Data model

Two normalized UTF-8 CSV tables joined on `oligo_id` (full data dictionary,
controlled vocabularies, and the grading rubric are in **`schema.md`**):

| File | Grain | Key |
|------|-------|-----|
| `data/oligos.csv` | one row per unique oligo (identity + design predictors) | `oligo_id` (PK) |
| `data/measurements.csv` | one row per oligo × model × delivery × dose × readout | `measurement_id` (PK), `oligo_id` (FK) |

Missing/unknown values are the literal string `TBD` (never guessed, never
imputed as zero).

## 3. Source identification and prioritization

Sources were prioritized **kidney-first** and catalogued in `SOURCES.md`
with stable identifiers, redistribution status, and acquisition state. Three tiers:

1. **Strict-kidney primary sources** — e.g. Janssen et al. 2019 (drisapersen,
   ciPTEC; PMC6796739); Sandelius et al. 2020 (urinary kidney biomarker panel;
   PMID 33084520); van Poelgeest 2013 (SPC5001); the Wu et al. marketed-ASO
   nephrotoxicity review (PMC10174585).
2. **Regulatory / clinical anchors** — FDA/EMA labels, prescribing information,
   and pivotal-trial publications for marketed/clinical oligonucleotides.
3. **Hepatotoxicity panels (fallback, flagged non-kidney)** — Dieckmann 2018,
   Burdick 2014, Hagedorn 2013; retained for chemistry/design diversity only and
   would be flagged `is_kidney_specific = FALSE`. *(None ingested as rows yet.)*

## 4. Data acquisition and extraction

Three extraction paths were used, each recorded per row via `source_id`:

1. **Local full-text extraction.** Primary-source PDFs supplied by the team were
   parsed with **PyMuPDF** (text + tables). Per-measurement values, doses,
   sequences, and figure/table loci were transcribed by hand into the schema.
   *(e.g. `N2` drisapersen → MSR017–026; `K1` Sandelius → MSR031–039.)*
2. **Secondary-source / review extraction.** Aggregating reviews (`REV` = Wu et
   al.) were used for marketed-drug renal findings, cross-checking primary data.
3. **`WS` (WebSearch-derived).** Because this environment's network policy blocks
   outbound full-text fetch, label/trial figures that were not supplied as files
   were taken from **search-engine summaries of the specific FDA/EMA label,
   clinical trial, or nonclinical paper named in each row's `source_ref`**. These
   are flagged `source_id = WS` and should be **verified against the cited
   primary source before publication.**
4. **WHO INN nomenclature derivation.** The WHO *Recommended INN* lists spell out
   every residue of a named oligonucleotide longhand
   (`2'-O-methyl-P-thiocytidylyl-(3'→5')-…`), so the base sequence is recoverable
   by deterministic parse rather than transcription. Lists were fetched as PDFs,
   text-extracted, and parsed by `scripts/fill_inn_sequences.py`. Two properties
   make this safer than reading a sequence off a table:
   - **Direction is explicit.** INN writes one strand with `(3'→5')` linkages
     (listed 5'→3') and its partner with `(5'→3')` linkages (listed 3'→5', hence
     reversed on output). Mis-handling this silently yields a *reversed* strand —
     the single most dangerous failure mode here — so the parser was validated by
     reproducing **givosiran** and **inclisiran**, already in this table from INN
     List 76, character-for-character before any new row was written.
   - **Results are self-checking.** Every duplex filled this way was required to
     show its guide strand as the exact reverse complement of its sense strand
     (ignoring 3′ overhangs), and residue counts were cross-checked against the
     published molecular formula where the phosphorus count fixes the length
     (e.g. viltolarsen `P20` → 21 nt; alicaforsen `P19S19` → 20 nt).

   Note that path 3's network restriction was specific to earlier sessions; direct
   fetch of `cdn.who.int` and PMC succeeded in the session that added path 4.

> **No-fabrication policy (strict).** `sequence_5to3` and any toxicity
> `readout_value` are **never invented or recalled from memory**. A sequence is
> filled only when an explicit string is returned by a credible source (e.g.
> inotersen, corroborated independently by the vutrisiran guide strand);
> otherwise it remains `TBD`. Compounds lacking published renal data were
> **omitted**, not padded.

## 5. Harmonization and controlled vocabularies

All categorical fields use the controlled vocabularies enumerated in `schema.md`.
The dictionary is reconciled to the data after each ingestion round (see the
**Data-dictionary QC log** in `schema.md`); vocabulary added during curation
(e.g. `delivery_method ∈ {intrathecal, intravitreal, oral}`, `conjugate = PEG`,
`species = multi_species`) is documented there rather than left implicit.

## 6. Toxicity grading

Each measurement carries an ordinal **`nephrotox_grade` (0–3)** assigned from the
reported endpoint per the rubric in `schema.md` (0 = no signal; 1 = mild/
functional/reversible, no viability loss; 2 = moderate injury-biomarker/
histopathology; 3 = severe AKI/glomerulonephritis/renal failure). Grades are
currently flagged **`grade_provisional`** in `notes`, pending scientific sign-off.

## 7. Independent (predictor) variables and their distribution

Design predictors hypothesized to drive nephrotoxicity, per `oligos.csv`
(n = 65 oligos):

| Variable | Distribution |
|----------|--------------|
| **Modality** (`oligo_class`) | ASO gapmer 40 · GalNAc-siRNA 12 · splice-switching ASO 4 · PMO 4 · siRNA 2 · 1st-gen PS-DNA (`other`) 2 · aptamer 1 |
| **Backbone** | full-PS 45 · PS/PO-mix 15 · PMO-neutral 4 · mixed 1 |
| **Conjugate** | none 48 · GalNAc 16 · PEG 1 |
| **Development stage** | approved 19 · research panel 30 · phase 3 (incl. discontinued) 9 · phase 2 5 · phase 1 1 · class-level 1 |
| **Sequence available** | 55 / 65 (rest `TBD`, never guessed — 6 proprietary, 2 class-level aggregates, 2 Ionis code compounds without an INN) |
| **Target genes** | 35 distinct |

## 8. Dependent (indicator) variables and their distribution

Toxicity indicators per `measurements.csv` (n = 111):

| Variable | Distribution |
|----------|--------------|
| **`nephrotox_grade`** | 0: 27 · 1: 30 · 2: 39 · 3: 15 |
| **Study type** | clinical 39 · animal 53 · in-vitro 19 |
| **Species** | human 58 · rat 29 · mouse 9 · multi-species 8 · monkey 7 |
| **Subject class** (`subject_class`) | human_invitro 67 · animal_invivo 53 · human_clinical 39 |
| **Delivery route** | systemic 87 · gymnotic/free-uptake 19 · intrathecal 3 · intravitreal 1 · oral 1 |
| **Readout category** | functional 35 · clinical renal outcome 27 · histopathology 24 · injury-biomarker 16 · viability 7 · accumulation 2 |
| **Kidney-specific** | TRUE 111 / 111 |

Readouts emphasize the **functional / injury-biomarker** axis (KIM-1, NGAL,
clusterin, cystatin C, A1M, proteinuria) over viability, by design. The dataset
deliberately includes **27 grade-0 negative controls** spanning GalNAc-siRNA,
siRNA, intrathecal ASO, and aptamer modalities — and paired
functional-positive / structural-negative rows on the same agent (e.g.
drisapersen: grade-1 A1M proteinuria alongside grade-0 viability and grade-0
monkey histopathology), which encode the central functional-not-cytotoxic signal.

## 9. Provenance and redistribution

- Every measurement carries `source_id` + `source_ref` + `source_table` (exact
  figure/table/label section/claim).
- `redistribution` is tracked per row: regulatory documents (FDA/EMA) →
  `public_domain`; journal-derived statistics → `summary_stat`; use `verify`
  where rights are unresolved. The 16 source identifiers in use are documented in
  `SOURCES.md`.
- Intended public license: a permissive open license (e.g. CC-BY) for the curated
  tables; underlying third-party full texts are **referenced, not redistributed**.

## 10. Quality control

Automated checks run after every ingestion round:
- **Schema conformance** — every categorical value validated against the
  `schema.md` enums; column-count integrity (17 / 24).
- **Referential integrity** — `measurements.oligo_id` → `oligos.oligo_id`
  (0 orphans); no duplicate primary keys.
- **Range checks** — `nephrotox_grade ∈ {0,1,2,3}`; booleans `TRUE/FALSE`.
- **Sequence policy** — only explicitly-sourced sequences filled; all others `TBD`.
- **Duplex self-consistency** — for every siRNA whose sense strand is recorded in
  `notes`, the stored guide strand must be its exact reverse complement once 3′
  overhangs are trimmed. This check depends on no external source being correct,
  so it catches a plausible-but-wrong sequence that two agreeing documents would
  not. All 6 duplexes added from WHO INN pass.
- **Case is significant** — in gapmer rows case encodes chemistry (uppercase =
  2′-MOE/cEt wings, lowercase = DNA gap). Sequence validators must be
  case-insensitive; a case-sensitive `[ACGUT]+` check will report these correct
  rows as malformed.

## 11. Known limitations

- **The negative class is not yet trustworthy — see [`CLINICAL_VALIDATION.md`](CLINICAL_VALIDATION.md).**
  Provenance and outcome are near-perfectly confounded across the 39 clinical rows: of the
  20 flagged `WS`, **zero** carry `nephrotox_grade ≥2`, against 11/19 among anchor-sourced
  rows (one-sided Fisher **p = 4.5 × 10⁻⁵**). Direct retrieval of 7 of the 13 unverified
  absence claims found only **one** genuine measured negative. Whether renal endpoints were
  measured tracks the *indication*, not the drug: trials of non-renal-indication compounds
  both omitted renal endpoints and excluded renally impaired patients. Until a
  `renal_endpoints_measured` field separates *measured-and-normal* from *never-looked*,
  **this dataset should not be used to train a nephrotoxicity model.**
- **Provisional grades** pending scientific (subject-matter) review.
- **Sequence coverage 55/65.** The 10 remaining `TBD` are, with one exception,
  structurally unfillable rather than merely unretrieved:
  **6 are proprietary and unpublishable** (the Moisan 2017 AON-A/C/D/E series and
  the Sandelius 2020 cEt tool/control ASOs — sequences withheld by their sources),
  **2 are class-level aggregate rows** for which a single sequence is not
  meaningful (`OLG030` Janas GalNAc-siRNA panel, `OLG031` Crooke pooled 2′-MOE),
  and **2 are Ionis development-code compounds** (`OLG025` ISIS 113715,
  `OLG026` ISIS 104838) which never received an INN and so have no entry in the
  WHO nomenclature lists that supplied the rest; their sequences would have to come
  from patent sequence listings, which is the only actionable remainder.
- **Duplicate molecule, retained deliberately.** `OLG002` (SPC5001) and `OLG047`
  (US11105794 compound 3-1) carry an **identical sequence and design** and are the
  same molecule curated from two independent sources (Santaris/Roche clinical vs.
  the Roche assay patent). Both rows are kept so each source's measurements remain
  traceable, but they are cross-flagged in `notes` and **must not be treated as two
  independent compounds when modelling.**
- **`OLG024` (pegaptanib)** carries `length_nt = 28` against a 27-character
  sequence: the 28th residue is a 3′-3′-linked inverted deoxythymidine cap, which
  has no representation in a 5′→3′ string. The length is correct for the molecule;
  the string is the 27-nt aptamer body.
- **`WS` rows** rest on secondary search summaries of primary regulatory/trial
  sources. Verification was **performed, not deferred**, and mostly failed: of 7
  unverified absence claims retrieved directly, 1 survived as a measured negative
  (`CLINICAL_VALIDATION.md`). Treat the remaining `WS` rows as unvalidated.
- **Species translation is bidirectional here, not one-way.** The received wisdom is
  that animal toxicology *over-predicts* human renal effects for 2′-MOE ASOs. The 9
  oligos in `data/human_animal_bridge.csv` that carry both human and animal evidence
  do **not** support that as a blanket rule: 4 concordant, 3 animal-over-predicts,
  and **2 animal-under-predicts** — inotersen (human grade 3 crescentic
  glomerulonephritis against animal grade 1) and givosiran (human 2, animal 1). The
  under-prediction cases are the safety-relevant direction and involve the dataset's
  most severe human findings.
  Two caveats bound this. The bridge set is 9 oligos, too small for a rule. And two
  of the three over-prediction verdicts (lumasiran, vutrisiran) rest on human grade-0
  values that direct source retrieval could not support, so they may reflect an
  unmeasured human endpoint rather than a species difference. Model the direction as
  an open question, not a known constant.
- **In-vitro human-system rows were under-represented** (19/111); the US 11,105,794
  Table 2 extraction (2026-09-03) raised this to **67/159 = 42.1%**, now the largest
  class. Further expansion
  these (e.g. the pending in-vitro nephrotoxicity-assay patents and ciPTEC/
  RPTEC-TERT1 panels) is the priority for the next ingestion round.

## 12. Reproducibility

The repository is self-documenting: `README.md` (strategy + live record counter),
`schema.md` (dictionary + QC log), `SOURCES.md` (source registry +
acquisition state), and this file. Extraction used open tooling (PyMuPDF; standard
CSV). Every row is traceable to a citable locus, so any value can be independently
re-verified against its `source_ref`.

## 13. Intended use for predictive modeling

The two-table design exposes granular **sequence + chemistry + design**
predictors against graded, per-condition renal outcomes, supporting models that
predict nephrotoxic potential from oligonucleotide design — including the
clinically important distinction between **reversible functional proteinuria**
and **structural tubular injury**, and the **animal-to-human** translation gap.
