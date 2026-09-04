# OligoTox-CNS

**An open, sequence-resolved dataset of central-nervous-system toxicity for oligonucleotide
therapeutics.**

Built for the NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, **Phase 2 (Data
Generation)**. Sibling modules in the same programme cover nephrotoxicity and immunotoxicity;
this is the CNS module.

| | |
|---|---|
| Oligonucleotides | **1,839** |
| CNS toxicity measurements | **2,065** |
| Per-position chemical-modification records | **32,569** |
| Sources | **5** (4 contributing data, 1 contributing instruments) |
| Sequences published | 1,830 / 1,839 (99.5 %) |
| Position-resolved modification maps | 1,830 / 1,839 (99.5 %) |
| Licence | CC BY 4.0; 97.7 % of rows freely reusable including commercially |
| Structural QC | **26 / 26 checks pass** (`qc/validate_dataset.py`) |

---

## What makes this dataset useful

Every row pairs an oligonucleotide's **design** with a **measured CNS outcome**, which is what a
predictive model needs and what the public literature has not previously offered in one place.

1. **Sequence *and* modification position, for nearly every compound.** Not "5-10-5 MOE gapmer",
   but a per-nucleotide table: position 1 is an LNA adenine, position 4 is a 2′-deoxy thymine,
   and so on, for all 32,569 positions.
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
  oligos.csv              1,839 × 45   one row per oligonucleotide — the predictors
  measurements.csv        2,065 × 36   one row per outcome — the response
  modifications.csv      32,569 ×  8   one row per nucleotide position
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
  validate_dataset.py                  26 structural and provenance checks
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
python3 qc/validate_dataset.py     # 34 checks; exit 0 = all pass
python3 src/make_figures.py        # data/ → figures/
python3 src/baseline_model.py      # data/ → figures/baseline_model.json
python3 src/make_release.py        # data/ → deliverables/*.xlsx + docs/DATA_DICTIONARY.md
python3 src/make_pdfs.py           # → narrative + methodology PDFs
python3 src/make_padp.py           # → PADP PDF
python3 src/make_sources.py        # → source register PDF
python3 src/make_summary.py        # → SUMMARY.md + LICENSE.md
```

No network access is needed: every source the build reads is committed under `sources/`.

Dependencies: `openpyxl`, `pymupdf`, `matplotlib`, `reportlab`.

---

## Known limitations — read these before using the data

Stated plainly here and in full in [`OPEN_ITEMS.md`](OPEN_ITEMS.md):

- **Per-compound purity is not in the literature.** `purity_pct` is `NOT_REPORTED` for all
  1,839 oligonucleotides. The purification and identity-confirmation *method* is captured where
  the source states it (1,825 / 1,839). This is the largest gap between what this dataset is and
  what the challenge text describes, and it is a property of the published record, not of the
  curation.
- **The in vitro arm is rat, not human.** Only 12 of 2,065 measurements are human-derived, and
  all of them are clinical. There is no human in vitro CNS oligonucleotide toxicity data in this
  release because we did not find a published, sequence-resolved source of it.
- **Chemistry is narrow.** 1,825 of 1,839 oligonucleotides are LNA/DNA full-phosphorothioate
  gapmers from one study. That is a strength for isolating sequence effects (chemistry is held
  constant) and a weakness for generalising across chemistries.
- **Grades are provisional** pending subject-matter-expert review.
- **Two sources disagree** about whether divalent cations mitigate acute CNS toxicity. They are
  measuring different phenotypes; see `docs/SCORING_INSTRUMENTS.md` § 3.

---

## Licence

CC BY 4.0 for everything we created. Row-level content carries its source's terms in the
`redistribution` column: 2,018 of 2,065 measurements (97.7 %) are CC BY 4.0 or US public domain;
47 are CC BY-NC and are individually marked. See [`LICENSE.md`](LICENSE.md).
