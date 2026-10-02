# OligoTox-CNS

**An open, sequence-resolved dataset of central-nervous-system toxicity for oligonucleotide
therapeutics.**

Built for the NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, **Phase 2 (Data
Generation)**. Sibling modules in the same programme cover nephrotoxicity and immunotoxicity;
this is the CNS module.

<!-- GENERATED:headline -->
| | |
|---|---|
| Oligonucleotides | **1,879** |
| CNS toxicity measurements | **4,428** |
| Per-position chemical-modification records | **32,898** |
| Sources | **9** (8 contributing data, 1 contributing instruments) |
| Sequences published | 1,858 / 1,879 (98.9 %) |
| Position-resolved modification maps | 1,853 / 1,879 (98.6 %) |
| Verified unique human trials | **22** (16 independent cohorts) &mdash; see `docs/TRIAL_REGISTER.md` |
| Human laboratory measurements | **34** &mdash; the class the Challenge prioritises |
| Licence | CC BY 4.0 for our work; per-row source terms in `LICENSE.md` |
| Structural QC | **47 / 47 checks pass** (`qc/validate_dataset.py`) |
<!-- /GENERATED:headline -->

---

## What makes this dataset useful

Every row pairs an oligonucleotide's **design** with a **measured CNS outcome**, which is what a
predictive model needs and what the public literature has not previously offered in one place.

1. **Sequence *and* modification position, for nearly every compound.** Not "5-10-5 MOE gapmer",
   but a per-nucleotide table: position 1 is an LNA adenine, position 4 is a 2′-deoxy thymine,
   and so on, for all 32,898 positions.
2. **Paired in vitro and in vivo readouts on the same molecules.** 181 oligonucleotides carry
   both a rat primary-neuron calcium-oscillation score and a mouse acute tolerability score,
   which is exactly the in-vitro-to-in-vivo extrapolation the challenge asks for.
3. **The full severity range, including deliberate negative controls.** Grades 0/1/2/3 =
   56/87/40/57. Thirteen sequence-matched G-free negative-control ASOs are included by design.
4. **Four mechanistically distinct toxicity axes kept separate** rather than collapsed into one
   "toxic/not" label — acute behavioural, acute neuronal excitability, late-onset
   neurodegeneration, and three clinical axes.
5. **Nothing invented.** No sequence and no number was ever filled from background knowledge.
   Where the literature is silent the field says `NOT_REPORTED`, and the completeness report
   counts those explicitly.

---

## Layout

```
SUMMARY.md              one-page consolidated summary — START HERE
data/                   the dataset
  oligos.csv              1,879 × 45   one row per oligonucleotide — the predictors
  measurements.csv        4,428 × 36   one row per outcome — the response
  modifications.csv      32,898 ×  8   one row per nucleotide position
  sources.csv                 5 × 18   provenance registry
deliverables/
  OligoTox-CNS_Dataset.xlsx            the same data as a workbook, with README,
                                       data dictionary and a live-formula summary
  OligoTox-CNS_Narrative.pdf           narrative document (≤12 pages)
  OligoTox-CNS_Methodology.pdf         methodology document (≤5 pages)
docs/
  SCHEMA.md                            why the schema is shaped this way; the grading rubric
  DATA_DICTIONARY.md                   every column defined (generated — do not hand-edit)
  SCORING_INSTRUMENTS.md               each measurement scale, verbatim from its source
  PADP.md                              public access and dissemination plan
figures/                               eight figures, all rendered from data/
qc/
  validate_dataset.py                  46 structural and provenance checks
  verify_nephro_intake.py              verifies the sibling module used as pattern reference
src/                                   the build pipeline (see below)
sources/                               the retrieved source files the build reads
  RESEARCH_QUEUE.md                    every source, its licence, and what is queued for v1.1
LICENSE.md                             licence terms, including the per-row breakdown
OPEN_ITEMS.md                          every open question, with an owner and a status
PROJECT_STATE.md                       assignment, intake, and phase log
```

## Rebuilding from scratch

```bash
python3 src/build_hagedorn.py      # source H1  → data/staged/
python3 src/build_curated.py       # sources K1, L1, C1 → data/staged/
python3 src/build_ctgov.py         # source CT1 → data/staged/
python3 src/build_human_invitro.py # sources HV1-HV3 → data/staged/
python3 src/assemble.py            # staged → toxicity/<endpoint>/data/*.csv
python3 qc/validate_dataset.py     # 46 checks; exit 0 = all pass
python3 src/make_figures.py        # data/ → figures/
python3 src/baseline_model.py      # data/ → figures/baseline_model.json
python3 src/make_release.py        # data/ → deliverables/*.xlsx + docs/DATA_DICTIONARY.md
python3 src/make_pdfs.py           # → narrative + methodology PDFs
python3 src/make_padp.py           # → PADP PDF
python3 src/make_sources.py        # → source register PDF
python3 src/make_evidence_reports.py    # → docs/TRIAL_REGISTER, CHRONIC_QUALIFICATION,
                                   #   TRANSLATIONAL_PAIRING, CHARACTERIZATION_COVERAGE
python3 src/make_validation_manifest.py # → docs/VALIDATION_MANIFEST.md (+ artefact checksums)
python3 src/make_summary.py        # → SUMMARY.md + LICENSE.md + README generated regions
```

The full-text articles are not needed to rebuild, and are gitignored because they are large
binaries the pipeline never reads. To reconstitute them:

```bash
python3 src/fetch_papers.py        # → sources/papers/, 11 papers, each verified against
                                   #   its expected title, not just its HTTP status
```

No network access is needed: every source the build reads is committed under `sources/`.

Dependencies: `openpyxl`, `pymupdf`, `matplotlib`, `reportlab`.

---

## Known limitations — read these before using the data

Stated plainly here and in full in [`OPEN_ITEMS.md`](OPEN_ITEMS.md):

- **Per-compound purity is not in the literature.** `purity_pct` is `NOT_REPORTED` for all
  1,879 oligonucleotides. The purification and identity-confirmation *method* is captured where
  the source states it (1,825 / 1,879). This is the largest gap between what this dataset is and
  what the challenge text describes, and it is a property of the published record, not of the
  curation.
<!-- GENERATED:human -->
- **The human arm is clinical, and the human laboratory arm is thin.** 2,375 of
  4,428 measurements are human-derived: 2,341 are
  adverse-event counts from clinical trials and **34 are human *in
  vitro***. The Challenge prioritises the latter class, and 34 rows is
  not a strong showing in it. The predictive in vitro screen in this field remains **rat** primary
  neurons. No compound in this release carries both a human and an animal row, so the dataset
  cannot yet extrapolate between human in vitro and animal systems &mdash; see
  `docs/TRANSLATIONAL_PAIRING.md`.
<!-- /GENERATED:human -->
- **Chemistry is narrow.** 1,825 of 1,879 oligonucleotides are LNA/DNA full-phosphorothioate
  gapmers from one study. That is a strength for isolating sequence effects (chemistry is held
  constant) and a weakness for generalising across chemistries.
- **Grades are provisional** pending subject-matter-expert review.
- **Two sources disagree** about whether divalent cations mitigate acute CNS toxicity. They are
  measuring different phenotypes; see `docs/SCORING_INSTRUMENTS.md` § 3.

---

## Licence

CC BY 4.0 for everything we created. Row-level content carries its source's terms in the
`redistribution` column: 2,018 of 4,428 measurements (97.7 %) are CC BY 4.0 or US public domain;
47 are CC BY-NC and are individually marked. See [`LICENSE.md`](LICENSE.md).
