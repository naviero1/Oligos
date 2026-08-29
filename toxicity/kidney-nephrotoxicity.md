# Kidney toxicity (nephrotoxicity)

**Endpoint key:** `kidney-nephrotoxicity` · **Status:** delivered (volume target met); **12 open defects in §6, of which 2 are release blockers** · **Register:** [`toxicity/README.md`](./README.md)

Kidney toxicity is one of the eight endpoints named on page 1 of the Challenge brief, quoted verbatim in [the register
index](./README.md#scope-authority). It is the only endpoint here that carries extracted data: `is_kidney_specific` is `TRUE` on 111 of 111 rows
of [`data/measurements.csv`](../data/measurements.csv) and no `FALSE` row exists, so all 65 oligos and all 111 rows belong here and no measurement
row is shared with another endpoint. Two of the 16 `source_id` values are shared at document level rather than row level: `N3` and `M1` also carry
liver-side readouts, cited in [`hepatotoxicity.md` §4 "Data", sub-section "Molecule-level liver/kidney pairings the repo holds and does not record"](./hepatotoxicity.md). Grading rules, extraction
paths and the data dictionary are not restated — see
[`METHODOLOGY.md`](../METHODOLOGY.md) and [`schema.md`](../schema.md).

---

## 1. Status summary

| | Value | Source of the figure |
|---|---|---|
| Unique oligos | 65 | `data/oligos.csv` (65 rows × 17 columns) |
| Measurement rows | 111 | `data/measurements.csv` (111 rows × 23 columns) |
| `source_id` values in use | 16 | `data/measurements.csv`, `source_id` column |
| PDFs in `sources/kidney/` | 8 | 7 endpoint-dedicated + 1 multi-endpoint volume; 5 produced rows (§3a) |
| `source_id`s with a local PDF | 5 of 16 | N2, N3, M1, K1, REV — 55 rows; WS and A1–A10 have none — 56 rows |
| Sequences filled | 55 of 65 | `sequence_5to3 != 'TBD'`; the 10 gaps are itemised at `METHODOLOGY.md:192-201` |
| ≥ 100-record Phase 2 target | met | `README.md` § "Record counter" |
| In-vitro volume | incomplete (19 of 111) | `METHODOLOGY.md:217-219` |
| Grades signed off | 0 of 111 | all rows carry `grade_provisional` in `notes` (`METHODOLOGY.md:122`) |

"Delivered" is this register's own status label, not a claim made anywhere in the repository.

---

## 2. Scope decision, and the work produced under it

The single-endpoint scope is decided and recorded at `README.md` § "Scope (decided — not under review)" and `METHODOLOGY.md:20-35`.
Everything below was produced under it.

| Artifact | Path | Content |
|---|---|---|
| Oligo table | [`data/oligos.csv`](../data/oligos.csv) | 65 × 17 — identity and design predictors |
| Measurement table | [`data/measurements.csv`](../data/measurements.csv) | 111 × 23 — one row per oligo × model × delivery × dose × readout |
| Merged analysis view | [`data/oligotox_kidney_merged.csv`](../data/oligotox_kidney_merged.csv) | 111 × 39; generated, not canonical (`schema.md:131-146`) |
| Clinical-row validation | [`data/clinical_validation_2026-08.md`](../data/clinical_validation_2026-08.md) | 85 lines; August 2026 audit of the 39 `study_type=clinical` rows |
| Merge script | [`scripts/build_merged.py`](../scripts/build_merged.py) | Hard-codes the kidney output filename (line 22) and the measurement column list (`MEAS_COLS`, lines 30-35) |
| Slide deck | [`PRESENTATION.md`](../PRESENTATION.md), built to `OligoTox-Kidney.pptx`, `OligoTox-Kidney-editable.pptx`, `OligoTox-Kidney.pdf` | 832 lines, 29 slides (30 `^---$` lines less the 2 front-matter delimiters = 28 separators); 29 slides/pages in each binary |
| Diagrams | `assets/` (8 SVGs) | `mechanism`, `trap`, `datamodel`, `grade-ladder`, `extraction`, `paired`, `patent`, `translation`; each embedded exactly once, at `PRESENTATION.md:202`, `:232`, `:318`, `:338`, `:464`, `:574`, `:593`, `:613` |

Documentation sections wholly this endpoint's: `README.md` §§ "Scope (decided — not under review)", "Why this design — key domain facts" and "Record counter"; `METHODOLOGY.md:20-35`, `:116-123`, `:124-158`, `:189-219`;
`schema.md:36-80`, whose 0–3 rubric at `:74-77` is written entirely in renal terms. `PRESENTATION.md` is this endpoint end to end.
`scripts/fill_inn_sequences.py` and `scripts/paper_search.py` are endpoint-neutral and are indexed in [`cross-cutting.md` §2](./cross-cutting.md),
which also flags `assets/datamodel.svg` and `assets/extraction.svg` as kidney-shaped infrastructure.

---

## 3. Sources allocated to this endpoint

### 3a. Local PDFs under `sources/kidney/` (all eight paths verified present)

| PDF | `source_id` | Rows | Measurement IDs | Redistribution |
|---|---|---:|---|---|
| `Janssen2019_drisapersen_reversible_proteinuria_ciPTEC_PMC6796739.pdf` | `N2` | 10 | MSR017–MSR026 | `summary_stat` ×10 |
| `US11105794_in_vitro_nephrotox_assay_patent.pdf` | `N3` | 21 | MSR91–MSR99, MSR100–MSR111 | `public_domain` ×21 |
| `Moisan2017_EGF_uptake_nephrotox_ASO_invitro_PMC5363415.pdf` | `M1` | 11 | MSR080–MSR090 | `summary_stat` ×11 |
| `Sandelius2020_urinary_kidney_biomarker_panel_ASO_tubular_tox_PMID33084520.pdf` | `K1` | 9 | MSR031–MSR039 | `summary_stat` ×9 |
| `Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf` | `REV` | 4 | MSR027–MSR030 | `summary_stat` ×4 |
| `US11479818_in_vitro_nephrotox_assay_patent_EGFR.pdf` | `N4` | 0 | — | — |
| `Frazier2022_kidney_effects_review_ToxPathol.pdf` | none | 0 | — | — |
| `MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf` | none | 0 | — | multi-endpoint; indexed per chapter in [`cross-cutting.md` §1.4](./cross-cutting.md) |

Five dedicated PDFs produced 55 of the 111 rows. The eighth file is the 416-page *Methods in Molecular Biology* 2434 volume, misfiled here; only
its Ch.26 belongs to this endpoint.

### 3b. `source_id` values with no local PDF — 56 rows allocated by `source_id`, not by file

| `source_id` | Rows | Oligos | Measurement IDs | Redistribution |
|---|---:|---:|---|---|
| `WS` | 36 | 31 | MSR040–MSR068, MSR073–MSR079 | `public_domain` 16 / `summary_stat` 20 |
| `A4` | 5 | 1 | MSR008, MSR069–MSR072 | `summary_stat` ×5 |
| `A1` | 3 | 1 | MSR001–MSR003 | `public_domain` ×3 |
| `A3` | 3 | 1 | MSR005–MSR007 | `summary_stat` ×3 |
| `A8` | 2 | 1 | MSR012–MSR013 | `public_domain` ×2 |
| `A9` | 2 | 1 | MSR014–MSR015 | `public_domain` ×2 |
| `A2`, `A5`, `A6`, `A7`, `A10` | 1 each | 1 each | MSR004, MSR009, MSR010, MSR011, MSR016 | `summary_stat` ×2 / `public_domain` ×3 |

Anchors A1–A10 and `REV` are defined at `sources/SOURCES.md:100-112`, `WS` at `:123-129`. `WS` is the largest and weakest tier: 36 rows from
search-engine summaries rather than retrieved full text, which `sources/SOURCES.md:126-127` and `METHODOLOGY.md:212-213` both say must be verified
before release. Three registry ranges covering these sources are wrong (§6.12).

---

## 4. Data

### 4a. Where the records live

All of `data/oligos.csv`, `data/measurements.csv` and the generated `data/oligotox_kidney_merged.csv`; no column subsets this endpoint. The
endpoint-bearing columns are `nephrotox_grade` (0–3, rubric at `schema.md:70-80`); `is_kidney_specific`, `TRUE` on 111 of 111 rows and so carrying
zero information, its `FALSE` branch (`schema.md:61`) held for hepatotox rows never ingested; and `tissue`, whose `glomerulus` value is unused (§6.5).

### 4b. Distributions

These tables are a **manual snapshot recomputed from the CSVs at commit `43ed250`**. No mechanism regenerates them, so they are a further node in
the counter-drift problem at §6.7; §8 item 8 is the fix.

**`nephrotox_grade`** — 0: 27 · 1: 30 · 2: 39 · 3: 15 (total 111); by study type:

| `study_type` | grade 0 | 1 | 2 | 3 | total |
|---|---:|---:|---:|---:|---:|
| `in_vitro` | 3 | 5 | 11 | 0 | 19 |
| `animal_invivo` | 6 | 15 | 22 | 10 | 53 |
| `clinical` | 18 | 10 | 6 | 5 | 39 |

No in-vitro row reaches grade 3, and the grade-3 definitions at `schema.md:77` are all whole-organism endpoints, so none is reachable in vitro on
the rubric as written — a consequence no document outside this reorganization states. Referential integrity holds: 0 orphan FKs, 0 duplicate PKs, every oligo has ≥ 1 row.

**Measurement level** (n = 111):

| Variable | Distribution |
|---|---|
| `study_type` | `animal_invivo` 53 · `clinical` 39 · `in_vitro` 19 |
| `species` | `human` 58 · `mouse` 30 · `multi_species` 8 · `rat` 8 · `monkey` 7 |
| `readout_category` | `functional` 35 · `clinical_renal_outcome` 27 · `histopathology` 24 · `injury_biomarker` 16 · `viability` 7 · `accumulation` 2 |
| `delivery_method` | `systemic_dose` 87 · `gymnotic_free_uptake` 19 · `intrathecal` 3 · `intravitreal` 1 · `oral` 1 |
| `tissue` | `kidney` 73 · `proximal_tubule` 38 · `glomerulus` 0 |
| `effect_direction` | `increase` 76 · `no_change` 25 · `decrease` 10 |
| `redistribution` | `summary_stat` 64 · `public_domain` 47 · `verify` 0 · `derived_features_only` 0 |

**Oligo level** (n = 65):

| Variable | Distribution |
|---|---|
| `oligo_class` | `ASO_gapmer` 40 · `GalNAc_siRNA` 12 · `splice_switching_ASO` 4 · `PMO` 4 · `siRNA` 2 · `other` 2 · `aptamer` 1 |
| `backbone_chemistry` | `full_PS` 45 · `PS_PO_mix` 15 · `PMO_neutral` 4 · `mixed` 1 |
| `conjugate` | `none` 48 · `GalNAc` 16 · `PEG_5prime` 1 |
| `max_phase` | `research_panel` 30 · `approved` 18 · `phase_3` 6 · `phase_2` 5 · `phase_3_discontinued` 3 · `approved_EMA` 1 · `phase_1` 1 · `class_review` 1 |
| `sequence_5to3` | 55 filled · 10 `TBD` (OLG014, OLG015, OLG025, OLG026, OLG030, OLG031, OLG041–OLG044) |
| `target_gene` | 35 distinct strings |

---

## 5. What the data shows

Computed from the tables; the rationale behind each point lives in the documents cited and is not repeated. The clinical tier's grade-0 class is
not a finding here but a defect (§6.2).

1. **The functional-not-cytotoxic design is visible in the rows.** `functional` (35) plus `injury_biomarker` (16) is 51 rows against `viability` 7
   (`README.md` § "Why this design — key domain facts", `METHODOLOGY.md:28-34`, but see §6.8).
2. **Severity concentrates in the middle.** Grade 2 is the largest class (39) and grade 3 the smallest (15); of those 15, 8 are `N3` rank-derived
   (§6.4), the other 7 single rows from A1, A2, A3, A8, A9, WS and M1.
3. **A non-phosphorothioate chemistry is pooled into a PS-derived scale.** The four `PMO_neutral` oligos (OLG011 golodirsen, OLG012 casimersen,
   OLG013 viltolarsen, OLG016 eteplirsen) contribute 10 rows, all graded ≥ 1 (grade 1: 2, 2: 7, 3: 1 — MSR051, `renal_failure_premature_death`),
   which the PS-specific mechanism at `METHODOLOGY.md:28-34` does not describe.
4. **One molecule is present twice.** OLG002 (SPC5001) and OLG047 (RocheNTX_Cmpd3-1) share the sequence `TGCtacaaaacCCA` and account for 12 of 111
   rows (11 and 1); not two compounds (`METHODOLOGY.md:202-207`).
5. **Three molecule-level liver/kidney pairings exist.** In the one carrying numbers on both sides, five of the six Dieckmann 2018 tool LNA-ASOs
   are already in `data/oligos.csv` with nephrotoxicity grades, and OLG058 is liver-negative yet carries `nephrotox_grade` 3 at MSR104. Sequences,
   ALT fold-changes, PDF loci and the other two pairings are tabulated in
   [`hepatotoxicity.md` §4 "Data", sub-section "Molecule-level liver/kidney pairings the repo holds and does not record"](./hepatotoxicity.md), not duplicated here.

---

## 6. Known issues

Twelve defects, each verified against the file named; two are release blockers, and the last five are tabulated.

**1. The 21 `N3` rows record the wrong species and study design (blocker).** All 21 carry `species=mouse`,
`system_model=mouse_7day_nephrotox_study`, `exposure_duration=7_days`, `dose_or_conc_value=TBD`. The patent's "Measuring In Vivo Nephrotoxicity"
section binds Table 1 to a rat study — `sources/kidney/US11105794_in_vitro_nephrotox_assay_patent.pdf` PDF p.25 has purpose-bred Wistar Han
Crl:WI(Han) male rats in groups of 4 (exp. A) or 8 (exp. B), dosed at 40 mg/kg on days 1 and 8 in the intrascapular region, urine collected on day
15. (That page's text layer interleaves two columns; this reads the printed page.) Correcting it moves species from mouse 30 / rat 8 to mouse 9 /
rat 29 (`METHODOLOGY.md:146`).

**2. The clinical-validation confound is documented nowhere outside `data/`, and its recommendation is unapplied (blocker).**
`data/clinical_validation_2026-08.md:11-21` cross-tabulates provenance against outcome over the 39 clinical rows: 0 of 20 `WS` rows reach grade ≥
2 against 11 of 19 anchor-sourced rows, one-sided Fisher exact p = 4.5 × 10⁻⁵; `:45` scores "1 of 7 checked absence claims survives as a measured
negative" and `:76` concludes "**Until this field exists, the dataset should not be used to train a nephrotoxicity model.**" No file in the
curated corpus references it: a grep for `clinical_validation` across `*.md` outside `data/`, `toxicity/` and `REVIEW-2026-08.md` returns zero hits. Meanwhile `METHODOLOGY.md:153-154` — the Phase 2
deliverable — says the dataset "deliberately includes **27 grade-0 negative controls** spanning GalNAc-siRNA, siRNA, intrathecal ASO, and aptamer
modalities"; those four categories cover 13 of the 27, and `PRESENTATION.md:368` names three, covering 11. The real composition by `oligo_class`
is `ASO_gapmer` 11 · `GalNAc_siRNA` 9 · `splice_switching_ASO` 3 · `siRNA` 2 · `aptamer` 1 · `other` 1, and 17 of the 27 are `WS` clinical rows —
the population the validation document found unreliable.

**3. `readout_category=clinical_renal_outcome` is applied to 22 rodent rows.** Only 5 of the 27 rows in that category are `study_type=clinical`
(MSR001, MSR005, MSR010, MSR015, MSR077); the other 22 are `animal_invivo` — the 21 `N3` rows plus MSR051. `schema.md:54` gives the value no
definition, so nothing forbids it, but the distribution at `METHODOLOGY.md:148` reads as 27 human clinical renal outcomes.

**4. The patent-word → grade crosswalk is not published.** `N3` rows carry `readout_value` in {`innocuous`, `low`, `low_medium`, `medium`,
`medium_high`, `high`} with `readout_unit=class`. The mapping recovered from the data — `innocuous`→0, `low`→1, `low_medium`→2, `medium`→2,
`medium_high`→3, `high`→3 — places 8 rows at grade 3 beside biopsy-confirmed crescentic glomerulonephritis (MSR001) and acute tubular necrosis
(MSR005), although the patent's classes are a within-panel relative rank. `PRESENTATION.md:603` mentions the translation and `:786` flags it for
sign-off, but no field marks a grade as rank-derived.

**5. `tissue=glomerulus` (`schema.md:49`) is declared and unused.** Five rows carry glomerular lesion names, all tagged `tissue=kidney`: MSR001
`crescentic_glomerulonephritis` (3), MSR004 and MSR013 `focal_segmental_glomerulosclerosis` (3), MSR015 `glomerulonephritis` (3), MSR029
`renal_toxicity_potential_glomerulonephritis` (2). MSR029 is a hazard statement (`readout_value=present`), not a confirmed lesion, which is why §8
item 6 retypes only the other four. `sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf` PDF p.7: "It is important to distinguish
between more medically manageable tubular toxicity and more deleterious glomerular injury, when proteinuria is identified in a patient (or a
preclinical study animal) administered an ASO." `schema.md:76` grades "clinically significant proteinuria" at 2 with no origin qualifier.

**6. Provenance is weaker than the deck claims.** `PRESENTATION.md:715` asserts each measurement carries "the **exact** table/figure/claim".
Classifying all 111 `source_table` values gives 38 true table or figure loci (N3 21, M1 11, N2 6); 16 label, SmPC, EPAR or prose-section
references (REV 4, A1 3, WS 3, A8 2, A5 1, A7 1, A9 1, A10 1); and 57 category words or study-arm names (`results` 18, `clinical_safety` 12,
`nonclinical` 7, `open_label_extension`, `ENVISION_24mo`, `case_biopsy` and similar). K1 is 9 of 9 category words even though the Sandelius PDF
is held locally; A4 is 5 of 5, but has no local full text (§3b). Separately, `redistribution` values `verify` and `derived_features_only`
(`schema.md:65`) are used by zero rows although `schema.md:85-87` and `METHODOLOGY.md:163-165` instruct their use.

**7. Counter drift across this endpoint's own documentation.** The sequence-filled figure is still published three
incompatible ways: `METHODOLOGY.md:135` says 46, `METHODOLOGY.md:192` and `schema.md:126` say 55, and
`PRESENTATION.md:301`, `:493`, `:505`, `:758` say 33; the data says 55. (`README.md` carried a fourth value, 44, and a
reconstruction note asserting "**0 measurement rows**"; both were corrected in the same pass that added this dossier —
see [`REVIEW-2026-08.md`](../REVIEW-2026-08.md), findings B2 and M1.) `PRESENTATION.md:531` lists "inclisiran, givosiran, nusinersen · safe controls", but only inclisiran is all-grade-0 — givosiran (OLG003)
has MSR009 grade 1, MSR010 grade 2, MSR074 grade 1, and nusinersen (OLG004) has MSR011 and MSR030, both grade 1. `PRESENTATION.md:821` claims
"Every number in this deck regenerates from `data/`" while no rebuild mechanism exists in the repo — established in
[`cross-cutting.md` §4, "What must change if a second endpoint is populated"](./cross-cutting.md) and not re-derived here. The consequence for
this endpoint: `33/65` is still present in `OligoTox-Kidney.pdf` and `OligoTox-Kidney-editable.pptx` while `55/65` appears in neither.

| # | Defect | Evidence |
|---|---|---|
| 8 | Albumin is described as a low-molecular-weight protein | `README.md` § "Why this design — key domain facts" and `METHODOLOGY.md:28-34` gloss "low-molecular-weight proteinuria" as "(impaired albumin / α1-microglobulin / RAP reabsorption)", but `sources/kidney/Janssen2019_…PMC6796739.pdf` PDF p.2 reads "RAP (gene name LRPAP1) is a 39 kDa chaperone protein …, whereas albumin is a large ~68 kDa plasma protein…". `PRESENTATION.md` does not repeat it. |
| 9 | The rubric is inconsistently applied at two points | MSR085 (`viability`, `intracellular_ATP` reduced, `effect_vs_control=mild_cytotoxicity`) is graded 1, but `schema.md:75` defines grade 1 as including "no viability loss" and its three identical-readout siblings MSR082, MSR087, MSR089 are graded 2. MSR029 is graded 2 on a preclinical hazard statement (`readout_value=present`), a class the 0–3 rubric does not cover. |
| 10 | Nine primary keys break the `MSR###` padding | MSR91–MSR99 are two-digit against 102 three-digit; `schema.md:44` gives `MSR001` as the form and `sources/SOURCES.md:222` cites "21 compounds (MSR091–111)", but MSR091–MSR099 do not exist. A lexical sort places MSR91–MSR99 after MSR111. |
| 11 | Ten rows pair a percentage unit with a direction word | MSR022, MSR023, MSR080, MSR082, MSR083, MSR085, MSR087, MSR088, MSR089, MSR090 declare `readout_unit=pct_control` while storing `no_change`/`reduced`/`elevated` as `readout_value` — every `pct_control` row. A numeric read would null all ten; nothing in the repo does one (`build_merged.py` uses the stdlib `csv` module). |
| 12 | Registry ranges wrong, three kidney PDFs undeclared | `sources/SOURCES.md:195-200` lists only five of the eight kidney PDFs — M1, N3 and N4 are absent, so the local evidence for 32 of 111 rows is undeclared. `:123` gives `WS` as MSR040–052 (13 rows) when it covers 36. `:95` heads the anchor block "seed rows MSR001–016" while A4 also supplies MSR069–MSR072. |

---

## 7. Not done, and why

Not blocked for volume; blocked for release quality and for the in-vitro expansion the methodology itself calls the priority.

| Not done | Cause |
|---|---|
| In-vitro rows remain a minority (19 of 111) | `METHODOLOGY.md:217-219` calls this the next-round priority but describes the in-vitro patents as "pending". They are acquired (`sources/SOURCES.md:222-223`), so this is unextracted material, not a missing source. |
| US 11,105,794 Tables 2–18 unextracted | Verified by table-header scan: Tables 2–18 span PDF pp.27–33, Table 1 pp.24–25. All 21 `N3` rows carry `source_table=Table1`, so zero in-vitro rows come from this patent. `sources/SOURCES.md:222` names only "Table 2" as outstanding. |
| US 11,479,818 (`N4`) yields 0 rows | Its "Table 1 list of oligonucleotides used in the examples" (PDF p.25) is the same compound panel as `N3`, so it adds no compounds. Its value is a different readout (EGFR-mRNA) on the existing 21 — in-vitro volume, which is what is short. `sources/SOURCES.md:223` still frames it as a hunt for unique compounds. |
| Moisan 2017 Table 1 under-extracted | Verified at PDF p.4: "Table 1. Test AONs and Summary of Kidney Toxicity Assessed in 2-Week Rat Study at 40 mg/kg/week", with kidney weight, urine protein, urinary KIM-1, de/regeneration and two tubulotoxicity grades for all five AONs. The repo holds 3 qualitative rows from it (MSR081, MSR084, MSR086); every quantitative fold-change is discarded. |
| Frazier 2022 yields 0 rows | Acquired review; no extraction attempted. |
| Grades not signed off | All 111 rows carry `grade_provisional`; expert review has not occurred (`METHODOLOGY.md:191`). |
| `WS` tier not verified | 36 rows rest on search summaries. Partly attempted: `data/clinical_validation_2026-08.md` checked 7 of 13 absence claims, and 6 of the 7 did not survive as measured negatives (1 CONFIRMED, 1 PARTIAL kept at 0, 3 REFUTED, 2 UNSUPPORTED). Six remain unchecked (`:72-74`). |
| Distributions in §4b are a manual snapshot | Nothing regenerates them from `data/`, so they drift the moment a row changes (§6.7). |

---

## 8. Next step

1. Resolve the two release blockers in §6 before the dataset is presented as model-ready: the `N3` species/design fields and the unpropagated clinical-validation finding.
2. Correct the 21 `N3` rows (`species=rat`, the real 15-day two-dose design, `dose_or_conc_value=40` with `dose_or_conc_unit=mg/kg`, intrascapular
   route in `notes`), re-run `python scripts/build_merged.py`, correct `METHODOLOGY.md:146`, and log it in the `schema.md` QC log.
3. Zero-pad MSR91–MSR99 to MSR091–MSR099. Outside `data/`, a grep for `MSR9[1-9]` over `*.md` returns this dossier,
   [`hepatotoxicity.md` §4 "Data", sub-section "Molecule-level liver/kidney pairings the repo holds and does not record"](./hepatotoxicity.md),
   whose pairing table names MSR96, MSR97 and MSR99, and [`REVIEW-2026-08.md`](../REVIEW-2026-08.md); all change in the same commit.
   `sources/SOURCES.md:222` needs a separate correction: it prints "MSR091–111", ids that have never existed.
4. Propagate `data/clinical_validation_2026-08.md` into `METHODOLOGY.md` §11, `README.md`, `PADP.md`'s artifact table and the deck's "Honest
   limitations" slide (`PRESENTATION.md:752`), and either add the proposed `renal_endpoints_measured` field to `schema.md` or record why it was
   declined. Until then, correct `METHODOLOGY.md:153-154` and `PRESENTATION.md:368` so the 27 grade-0 rows are not presented as designed negative
   controls.
5. Publish the patent-word → grade crosswalk in `schema.md` beside the rubric, marking `N3` values a within-panel rank.
6. Set `tissue=glomerulus` on MSR001, MSR004, MSR013, MSR015 (not MSR029, §6.5) and qualify `schema.md:76` by origin.
7. Retype or define `clinical_renal_outcome` for the 22 rodent rows and recompute `METHODOLOGY.md:148`. Fix the three `sources/SOURCES.md` ranges
   and add M1, N3 and N4 to its local-file registry.
8. Write a script that emits every published counter from the CSVs, and make §1 and §4b of this file its first output. Then fix the existing
   counters (55/65 everywhere) and delete or date-stamp `README.md` § "Reconstruction note".
9. Extract the in-vitro volume already in hand: US 11,105,794 Tables 2–18 (pp.27–33), US 11,479,818's EGFR-mRNA readout on the same 21 compounds,
   and Moisan 2017 Table 1 re-extracted quantitatively.

Items 2, 3 and 6 are data edits needing a `build_merged.py` re-run; 4, 5, 7, 8 are documentation edits; 9 is the only extraction round. Four
defects carry no step above and are held unassigned: §6.6 (deck provenance sentence; `verify` and `derived_features_only` unused), §6.8 (the
albumin gloss in `README.md` § "Why this design — key domain facts" and `METHODOLOGY.md:28-34`), §6.9 (the MSR085 and MSR029 grades) and §6.11 (the ten `pct_control` units).

---

## Divided by toxicity, and what is duplicated

This dataset is one slice of the kidney corpus, produced by
[`scripts/split_by_endpoint.py`](./scripts/split_by_endpoint.py). Two things happen
in that split and they are **not** the same operation:

**Measurements divide.** A measurement is an observation of one toxicity, so the
rows partition — disjoint and exhaustive. This toxicity holds **111 measurement
rows**, and across all endpoints the per-toxicity counts sum exactly to the corpus
total. The script fails loudly if they ever stop summing, so the partition cannot
silently drift.

**Oligonucleotides duplicate.** A molecule is a compound *identity*, not an
observation. A drug studied for two toxicities belongs in both tables. This
toxicity's oligo table holds **65 molecules**, of which **13 also appear
under another toxicity** — 0 replicated under the same `oligo_id`, and 13
curated independently elsewhere and therefore carrying a *different* id there.

> **Consequence, because it is the easy mistake to make: oligo counts are not
> additive across toxicities. Row counts are.** Summing the oligo tables
> double-counts every molecule studied for more than one toxicity.

| File | What it is |
|---|---|
| [`kidney-nephrotoxicity.measurements.csv`](./kidney-nephrotoxicity.measurements.csv) | this toxicity's 111 graded measurement rows |
| [`kidney-nephrotoxicity.oligos.csv`](./kidney-nephrotoxicity.oligos.csv) | the 65 molecules those rows reference |
| [`kidney-nephrotoxicity.shared-molecules.csv`](./kidney-nephrotoxicity.shared-molecules.csv) | the 13 molecules also present under another toxicity, with the id they carry there |
| [`molecule_crosswalk.csv`](./molecule_crosswalk.csv) | the same ledger across every toxicity at once |

The crosswalk matters most for the 13 molecules curated independently under two
toxicities: nothing links `OLG###` to `CNS###`, so a model keyed on `oligo_id` would
treat one compound as two. Where both records carry a sequence, the split asserts
they agree base-for-base and **fails** if they do not — a disagreement would mean one
of the two is the wrong molecule. Across the whole repository there are currently
**no such conflicts**.

Cross-cutting artifacts are **duplicated into each toxicity that uses them** rather
than shared from a common folder, so every toxicity here is self-contained.
