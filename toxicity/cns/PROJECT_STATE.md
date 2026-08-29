# OligoTox-CNS — Project State

**Module:** CNS / neurotoxicity of oligonucleotide therapeutics
**Challenge:** NIH/NCATS Oligonucleotide Toxicity Open Data Challenge — **Phase 2 (Data Generation)**
**Branch:** `claude/oligo-toxicity-dataset-k394sz`
**Started:** 2026-08-26

---

## Assignment

Sibling modules already exist in this programme:

| Module | Owner | State at intake |
|---|---|---|
| Nephrotoxicity | (prior session) | `oligos.csv` 65 rows × 17 cols; `measurements.csv` 111 rows × 23 cols; 29-slide review deck |
| Immunotoxicity | Team GOG (Gustavo Canteros) | PBMC immunostimulation dataset, ~27 papers, LR/RF/LightGBM models, AUC 0.94 held-out |
| **CNS** | **this session** | **new — to be built** |

User instruction (2026-08-26): *"The toxicity will be CNS."*

---

## Intake — what was supplied

Uploaded 2026-08-26, unpacked to `notes/intake/`:

1. `Nephrotoxicity/oligos.csv`, `measurements.csv`, `OligoToxKidney (3).pptx` (29 slides, image-only + speaker notes)
2. `Immunotoxicity/` — `Oligotoxicity_Immuno_using Machine Learning techniques.docx` + 24 primary PDFs

**No CNS source material was supplied.** All CNS data must be located and extracted from the public
literature by this session. This is recorded as OI-01 in `OPEN_ITEMS.md`.

### Verification of the nephrotoxicity intake (recomputed from the CSVs, not taken from the deck)

| Claim on deck | Recomputed | Match |
|---|---|---|
| 65 unique oligos | 65 rows, 17 cols | yes |
| 111 graded measurements | 111 rows, 23 cols | yes |
| 100% kidney-specific | `is_kidney_specific` TRUE × 111 | yes |
| 16 distinct sources | 16 distinct `source_id` | yes |
| 33/65 sequences filled | 33 non-`TBD` `sequence_5to3` | yes |
| grade split 27/30/39/15 | `{0:27, 1:30, 2:39, 3:15}` | yes |
| 36 "WS" rows | `source_id == WS` × 36 | yes |
| no orphan FKs | `measurements.oligo_id ⊄ oligos.oligo_id` = ∅ | yes |

Command: `python3 qc/verify_nephro_intake.py` → `PASS — all 13 deck claims reproduce exactly from the
intake CSVs.` (exit 0). Every deck number regenerates from the CSVs.
The nephrotoxicity module is therefore treated as an **authoritative pattern reference** for schema,
grading philosophy, and provenance discipline.

---

## What the CNS module must deliver (from the challenge text)

1. **Narrative document** — single PDF, ≤12 pages
   - executive summary of dataset(s) + positive/negative controls
   - main findings and conclusions
   - how data were produced (experimental design, acquisition, computational processing)
   - how indicators and predictor variables were measured; their distributions; distribution of
     predictors amongst tested oligos
   - how the results address a gap in publicly available oligo-toxicity data
   - how the data could be used to develop a predictive model
2. **Methodology document** — single PDF, ≤5 pages, incl. **methods used to purify and characterize
   oligo identity**
3. **Dataset files** — no page limit
   - data dictionary + schema documenting all metadata
   - raw data as Excel (or similar) or documented access instructions
   - must contain: **sequences of all oligos tested**, **location of all chemical modifications in
     each oligo**, **purity and characterization data for each**, plus additional metadata
   - open licence (e.g. Creative Commons)

### Known structural tension — raised now, not at the end

The challenge asks for data produced by "collection, generation, **and** contribution". This module is a
**literature-curation** dataset, like its two siblings. Two requirements are only partially satisfiable
by curation and are tracked as open items:

- **Purity / characterization per oligo** (OI-02) — synthesis QC (HPLC/AEX purity %, MS-confirmed mass,
  endotoxin) is *rarely* published alongside toxicity results. Where a source reports it, it is
  captured; where it does not, the field is `NOT_REPORTED` and the *source's own* stated QC method is
  captured instead. Nothing is estimated.
- **Modification position per oligo** (OI-03) — recorded as an explicit per-position modification
  string only where the source states it. Motif-level ("5-10-5 MOE gapmer") is recorded as such and
  flagged as pattern-derived rather than position-verified.

---

## Phases

| # | Phase | State |
|---|---|---|
| 0 | Intake, verification, charter | done |
| 1 | Extraction from papers (fan-out research) | in progress |
| 2 | Consolidation of data into schema | pending |
| 3 | Completeness / QC check | pending |
| 4 | Documentation assembly (2 PDFs + dataset pack) | pending |

## Non-negotiable rules for this module

1. **No invented sequences. No invented numbers.** Missing is `NOT_REPORTED` / `UNKNOWN` and is
   counted in the completeness report.
2. Every presented number traces to a **named source + exact table/figure**.
3. Assumptions live in `OPEN_ITEMS.md` and are restated wherever they affect a conclusion.
4. Every deliverable is re-opened and inspected after creation — rendered to image where it is a
   document.
