---
marp: true
title: "OligoTox-Kidney — A Curated Nephrotoxicity Dataset for Oligonucleotide Therapeutics"
description: "Findings, methodology, and sources — for scientific review"
paginate: true
---

# OligoTox-Kidney

### A curated, per-measurement **nephrotoxicity** dataset for therapeutic oligonucleotides

Built for the **NIH / NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge — Phase 2** (Data Generation Phase; submission window 1 May – 31 Dec 2026)

**For scientific review — German (biochemist)**
Snapshot: 65 oligos · 111 measurements · 35 target genes · all strict-kidney

> This deck is a Markdown/Marp presentation. It can be read as a document on GitHub or exported to slides (`marp PRESENTATION.md --pdf`). Every claim traces to a row in `data/` and a source in `sources/SOURCES.md`.

---

## What we are building (and what we are *not*)

- **A dataset, not a model.** NCATS Phase 2 scores an **openly-releasable, well-documented, reproducible dataset**. We are not training a predictor — we are assembling the labelled substrate one could be trained on.
- **Endpoint: kidney toxicity / nephrotoxicity** — one of the named OligoTox endpoints of interest.
- **Method: in-silico curation** of already-published data — no wet lab. The "methods" are *source identification, extraction, harmonization, grading, provenance, and QC*.
- **Granularity: strict-kidney, per-measurement.** One row = **oligo × cell-model/subject × delivery × concentration/dose × readout.**
- **Coverage goal:** span every therapeutic oligo modality and the full severity range (including negative controls). Target **≥ 100 measurement rows — met (111).**

---

## Why kidney, and why this is scientifically non-trivial

The central biology that shaped every design decision:

1. **Oligo nephrotoxicity is frequently *functional*, not *cytotoxic*.**
   Phosphorothioate ASOs are filtered and reabsorbed by **proximal tubule epithelial cells via megalin/cubilin-mediated endocytosis**, accumulating in the lysosomal compartment. This produces **reversible low-molecular-weight proteinuria** (impaired reabsorption of albumin, α1-microglobulin, RAP) **with no loss of cell viability.**
   → **A viability/MTT readout will score these compounds as clean.** That is the trap this dataset is designed to avoid.
2. **Toxicity = sequence + chemistry + design *together*** — not chemistry class alone. Two MOE gapmers of identical chemistry can differ by orders of magnitude in renal signal based on sequence. So we record **granular per-oligo design predictors.**
3. **Marketed-drug data alone is too small** (~19 approved oligos, a minority with renal signal). Volume and mechanistic resolution come from **in-vitro human proximal-tubule panels** and **patent toxicity panels.**

---

## The schema captures the *right* phenotype

Because the injury is functional, the readout vocabulary is deliberately weighted toward **function and injury biomarkers**, not viability:

| Readout category | Rows | Examples |
|---|---:|---|
| **functional** | 35 | LMW proteinuria, A1M/albumin reabsorption, eGFR/creatinine shift, RAP |
| **clinical_renal_outcome** | 27 | proteinuria, AKI, glomerulonephritis on label/trial |
| **histopathology** | 24 | tubular degeneration, basophilic granules, glomerular change |
| **injury_biomarker** | 16 | **KIM-1, NGAL, clusterin, cystatin C**, osteopontin |
| **viability** | 7 | included only to *pair against* functional positives |
| **accumulation** | 2 | tubular drug accumulation |

The dataset deliberately encodes **paired functional-positive / structural-negative rows on the same agent** (e.g. drisapersen: grade-1 A1M proteinuria *alongside* grade-0 viability and grade-0 monkey histopathology) — that pairing *is* the functional-not-cytotoxic signal in machine-readable form.

---

## Data model — two normalized tables

Joined on `oligo_id`; full dictionary + controlled vocabularies + grading rubric in `schema.md`.

| File | Grain | Key | Cols |
|---|---|---|---:|
| `data/oligos.csv` | one row per unique oligo (identity + **design predictors**) | `oligo_id` (PK) | 17 |
| `data/measurements.csv` | one row per oligo × model × delivery × dose × readout (**graded outcomes**) | `measurement_id` (PK), `oligo_id` (FK) | 23 |

**Predictor columns (oligos):** class, target gene, backbone chemistry, sugar modifications, gapmer design, conjugate (GalNAc/PEG), PS count, length, sequence (5′→3′), development stage.

**Outcome columns (measurements):** study type, species, system/model, tissue, delivery, dose/conc, exposure, readout name/value/unit, effect direction vs control, **`nephrotox_grade`**, `is_kidney_specific`, and full provenance (`source_id`, `source_ref`, `source_table`, `redistribution`).

Missing/unknown is the literal `TBD` — **never guessed, never imputed as zero.**

---

## The graded label: `nephrotox_grade` (0–3)

An ordinal severity scale assigned from the reported endpoint (rubric in `schema.md`):

| Grade | Meaning | Canonical anchor |
|:---:|---|---|
| **0** | No renal signal (true negative control) | GalNAc-siRNA, intrathecal ASO, aptamer negatives |
| **1** | Mild / **functional** / reversible — **no viability loss** | drisapersen A1M proteinuria (ciPTEC) |
| **2** | Moderate — injury biomarker ↑ and/or histopathology | tubular basophilic granules; KIM-1/NGAL rise |
| **3** | Severe — AKI / glomerulonephritis / renal failure | **inotersen** (grade-3 GN); **SPC5001** (tubular AKI, FIH) |

> **All grades currently carry a `grade_provisional` flag in `notes`.** Removing that flag is the **scientific sign-off we are asking German to perform** (see final slide). Grades were assigned by rubric, but the rubric→row mapping is exactly where domain judgment is most valuable.

---

## Methodology — three extraction paths (each tagged per row)

Every row records *how* it was obtained via `source_id`:

1. **Local full-text extraction (primary sources).** PDFs supplied by the team parsed with **PyMuPDF** (text + tables); per-measurement values, doses, sequences, and figure/table loci transcribed by hand.
   → `N2` drisapersen, `K1` Sandelius, `M1` Moisan, `N3` patent panel.
2. **Secondary / review extraction.** Aggregating reviews used for marketed-drug renal findings, cross-checked against primary data. → `REV` = Wu et al. 2022.
3. **`WS` (WebSearch-derived).** This environment's network policy **blocks outbound full-text fetch** (org egress denies the CONNECT tunnel; only search summaries are available). Label/trial figures not supplied as files were taken from **search summaries of the specific FDA/EMA label or trial named in that row's `source_ref`**, flagged `source_id = WS`, and marked **to be verified against the primary source before release.**

---

## The rule that governs the whole dataset

> ## ⚠️ No-fabrication policy (strict)
> **`sequence_5to3` and any toxicity `readout_value` are never invented or recalled from memory.**
>
> - A **sequence** is filled only when an explicit string is returned by a credible, redistribution-permitted source — otherwise `TBD`. (e.g. inotersen, corroborated independently against the vutrisiran guide strand.)
> - A **toxicity value** is filled only when reported in the cited source.
> - **Compounds lacking published renal data were omitted, not padded** to hit the count.

This is why sequence coverage is **33/65 and not 65/65** — the remaining 32 are real gaps, honestly marked, not fabricated. For a reviewer, that distinction is the credibility of the whole table.

---

## Papers & sources researched — strict-kidney primary

The scientific backbone — direct nephrotoxicity measurements:

| ID | Source | Contribution | Rows |
|---|---|---|---:|
| **N2** | **Janssen et al. 2019**, *PMC6796739* (drisapersen) | **ciPTEC** human proximal-tubule in-vitro; A1M proteinuria *without* viability loss — the functional phenotype; **3 published sequences** | 10 |
| **N3** | **US 11,105,794 B2** (Roche/patent panel) | Table 1: per-compound LNA/MOE gapmers with **sequence + SEQ ID + in-vivo nephrotox class** — public domain | 21 |
| **M1** | **Moisan et al. 2017**, *PMC5363415* | **RPTEC/TERT1** human tubule panel; ASO uptake / EGF-pathway nephrotox in-vitro | 11 |
| **K1** | **Sandelius et al. 2020**, *PMID 33084520* | Urinary **kidney injury-biomarker** panel (KIM-1/NGAL/clusterin) | 9 |
| **A3** | **van Poelgeest et al. 2013**, *bcp.12738* | **SPC5001** first-in-human — proteinuria + tubular **AKI** (grade-3 anchor) | 3 |
| **A4** | **Arch Toxicol 2021**, *s00204-021-03062-8* | **SPC5001 kidney-on-chip** — recapitulating the FIH signal in vitro | 5 |

---

## Papers & sources researched — anchors, reviews & patents

| ID | Source | Role |
|---|---|---|
| **REV** | **Wu et al. 2022**, *PMC10174585* | Marketed-ASO nephrotoxicity review — cross-checked anchor findings (4 rows) |
| **A1** | inotersen — **NEJM 2018 NEURO-TTR** + FDA label 211172 | **Grade-3 glomerulonephritis** — canonical severe anchor |
| **A9** | mipomersen — FDA 203568 + EMA Kynamro EPAR | 2′-MOE gapmer renal monitoring |
| **A8** | volanesorsen — EMA Waylivra + APPROACH (NCT02658175) | APOC3 gapmer renal signal |
| **A10 / A5 / A7** | inclisiran (Leqvio) · givosiran (Givlaari) · nusinersen (Spinraza) | GalNAc-siRNA & intrathecal **negative/low** controls |
| **N3 / N4** | **US 11,105,794 B2** · **US 11,479,818 B2** | In-vitro nephrotox-assay patents (public domain); N4 staged for unique-compound mining |

**`WS` anchor set (36 rows)** — FDA/EMA labels + pivotal trials for: patisiran (Onpattro), vutrisiran (HELIOS-A), lumasiran (ILLUMINATE-B), nedosiran (PHYOX3), eplontersen (Wainua), tofersen (Qalsody), bepirovirsen (B-Clear), olpasiran (OCEAN-DOSE), the DMD PMOs (eteplirsen/golodirsen/casimersen/viltolarsen), pegaptanib (Macugen), fitusiran (Qfitlia), zilebesiran (KARDIA), plus **Crooke 2018 pooled-human** and **Yu 2012 ISIS-113715 monkey** translation references.

---

## Key finding 1 — the functional-not-cytotoxic phenotype is captured, in machine-readable form

- The dataset contains **explicit paired rows** where the *same* oligo is **grade-1 on a functional readout and grade-0 on viability/histopathology.**
- Example (drisapersen, `N2`): A1M proteinuria in **ciPTEC** → grade 1; viability unchanged → grade 0; monkey histopathology clean → grade 0.
- This is the single most important scientific property of the set: a model trained on it can learn the distinction **reversible functional proteinuria vs. structural tubular injury** — which viability-only datasets *cannot* teach.
- **35 functional + 16 injury-biomarker rows** vs. only **7 viability rows** — the readout mix reflects the biology, not assay convenience.

---

## Key finding 2 — the patent panel unlocked sequence-resolved volume

- **US 11,105,794 B2, Table 1** was the breakthrough source: a clean per-oligo panel of LNA/MOE gapmers giving **compound → sequence → SEQ ID → in-vivo nephrotoxicity class**, all **public domain.**
- Mapped the patent's qualitative in-vivo classes to our rubric: *innocuous → 0, low → 1, low/medium & medium → 2, medium/high & high → 3.*
- Impact: **+21 measurement rows and tripled sequence coverage (13 → 33 sequences).** This is the only large block where **sequence and graded outcome sit in the same record** — the most directly model-ready slice of the dataset.

---

## Key finding 3 — animal toxicology over-predicts human renal risk

- A documented, modellable bias: **2′-MOE ASO animal toxicology over-predicts human renal effects.**
- Captured explicitly rather than hidden — e.g. the **Crooke 2018 pooled-human** entry and the **Yu 2012 monkey** ISIS-113715 entry sit in the same table, same readout vocabulary, different species.
- Distribution makes the translation axis learnable: **human 58 · mouse 30 · monkey 7 · rat 8 · multi-species 8**, across **in-vitro 19 / animal 53 / clinical 39** rows.
- A reviewer/modeler can therefore study the **animal→human translation gap directly** instead of treating animal histopathology as ground truth for human risk.

---

## Final dataset — at a glance

| Dimension | Distribution |
|---|---|
| **Records** | **65 oligos · 111 measurements** (≥100 target met; all strict-kidney) |
| **Grade (0/1/2/3)** | 27 · 30 · 39 · 15 |
| **Modality** | ASO gapmer 40 · GalNAc-siRNA 12 · splice-switching/SSO 4 · PMO 4 · siRNA 2 · 1st-gen PS-DNA 2 · aptamer 1 |
| **Backbone** | full-PS 45 · PS/PO-mix 15 · PMO-neutral 4 · mixed 1 |
| **Conjugate** | none 48 · GalNAc 16 · PEG 1 |
| **Stage** | approved 19 · research-panel 30 · phase 3 (incl. disc.) 9 · phase 2 5 · phase 1 1 · class-level 1 |
| **Study type** | animal 53 · clinical 39 · in-vitro 19 |
| **Species** | human 58 · mouse 30 · multi 8 · rat 8 · monkey 7 |
| **Delivery** | systemic 87 · gymnotic/free-uptake 19 · intrathecal 3 · intravitreal 1 · oral 1 |
| **Sequences filled** | **33 / 65** (rest `TBD`, never guessed) · **35 target genes** |

---

## Provenance & redistribution — every row is defensible

- **Each measurement carries `source_id` + `source_ref` + `source_table`** (exact figure / table / label section / patent claim). Any value can be re-verified against its locus.
- **Redistribution tracked per row:** `public_domain` 47 (FDA/EMA labels, USPTO patents — values reproducible) · `summary_stat` 64 (journal-derived figures — derived/summary only).
- **16 distinct source identifiers** in use, all registered in `sources/SOURCES.md` with acquisition state.
- Intended public license for the curated tables: **permissive (e.g. CC-BY)**; third-party full texts are **referenced, not redistributed.**

**QC run after every ingestion round (all currently passing):** schema-enum conformance · column-count integrity (17/23) · referential integrity `measurements.oligo_id → oligos.oligo_id` (**0 orphans**) · no duplicate PKs · `nephrotox_grade ∈ {0,1,2,3}` · sequence policy (only explicitly-sourced sequences filled).

---

## Honest limitations (what a reviewer should know)

- **Grades are provisional** — assigned by rubric, pending the scientific sign-off requested here.
- **Sequence coverage is 33/65.** Remaining gaps are siRNA guide strands and some PMOs whose sequences were not transcribable from available summaries (and never guessed).
- **`WS` rows (36)** rest on search summaries of primary regulatory/trial sources — they need a verification pass against the cited primary document before publication.
- **In-vitro human-system rows (19)** are the scientific core but still a minority; expanding human proximal-tubule panels (ciPTEC / RPTEC-TERT1 / 3D-RPTEC / kidney-on-chip) is the top growth priority.
- **Animal over-prediction** is present by design and must be *modeled*, not ignored.

---

## What we need from German (the ask)

1. **Grade sign-off.** Review the rubric→row mapping in `data/measurements.csv` and the rubric in `schema.md`; confirm or correct grades so we can **remove the `grade_provisional` flag.** Highest-value targets: the grade-2/3 boundary (injury-biomarker vs. AKI) and the patent-class → grade mapping.
2. **Biology sanity check.** Is the **functional-vs-structural** framing (megalin/cubilin → LMW proteinuria → grade 1) faithful, and are the readout→severity assignments physiologically sound?
3. **Source confidence.** Flag any anchor you'd want re-verified against primary text before release (esp. the `WS` set).

**Then (on hold until sign-off):** finalize the ≤12-page narrative; verify `WS` rows; backfill remaining sequences; optionally mine patent **N4 (US 11,479,818)** and **US 11,105,794 Table 2** (per-compound in-vitro EGF values) for the next volume increment.

---

## Repository map (for review)

```
README.md            strategy, scope, domain rationale, live record counter
schema.md            full data dictionary, grade rubric, vocab + QC log
METHODOLOGY.md       Phase-2 methodology deliverable (source→grade→QC)
PRESENTATION.md      this deck
data/oligos.csv      65 oligos  · 17 predictor columns
data/measurements.csv  111 graded rows · 23 columns · full provenance
sources/SOURCES.md   source registry (16 IDs), acquisition state, drop-list
sources/kidney/      drisapersen, Wu, Sandelius, Moisan, SPC5001, patents …
sources/hepatotox/   Dieckmann, Burdick, Hagedorn (chemistry diversity, flagged non-kidney)
```

**Thank you — feedback welcome at the row level.** Every number in this deck regenerates from `data/` (`python` count scripts in the repo history); nothing here is hand-maintained prose detached from the tables.
