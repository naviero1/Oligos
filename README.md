# Oligos — oligonucleotide toxicity datasets

All work is filed under [`toxicity/`](toxicity/README.md), by the toxicity endpoint it
belongs to. Nothing project-specific lives at the repository root.

The NIH/NCATS OligoTox Challenge names **eight toxicities of interest**. This repository holds
curated data for **three** of them — kidney toxicity, chronic neurotoxicity and hydrocephalus —
plus a dossier for each remaining endpoint recording what material the repo actually has for it.

Every toxicity has its own folder and its own dossier, and holds only its own rows. The CNS
curation produced 2,065 measurements but they are **not one toxicity**: 6 are chronic
neurotoxicity, 1 is hydrocephalus, and the other 2,058 are acute neurotoxicity and general
clinical CNS adverse events. Acute neurotoxicity is **not on the brief's list** — the Challenge
explicitly deprioritises it — so it has its own folder to keep the data filed honestly, but
nothing in it counts toward coverage. Read
[`toxicity/acute-neurotoxicity/acute-neurotoxicity.md` §1](toxicity/acute-neurotoxicity/acute-neurotoxicity.md)
before quoting that folder's size.

```
toxicity/
  README.md                     coverage index: which endpoints have rows,
                                which have sources awaiting extraction, which are empty

  kidney/                       ← populated dataset (111 measurements, 65 oligos)
    README.md  METHODOLOGY.md  schema.md  CLINICAL_VALIDATION.md  SOURCES.md
    data/  sources/  scripts/  assets/
    kidney-nephrotoxicity.md    endpoint dossier

  chronic-neurotoxicity/        ← listed endpoint (2,335 measurements, 13 oligos)
    chronic-neurotoxicity.md  data/
  hydrocephalus/                ← listed endpoint (12 measurements, 2 oligos)
    hydrocephalus.md  data/
  acute-neurotoxicity/          ← NOT a listed endpoint (2,047 measurements, 1,832 oligos)
    acute-neurotoxicity.md  data/

  _shared/cns/                  build pipeline, schema, sources and submission documents
    src/  qc/  docs/  sources/  figures/  deliverables/   shared by the three CNS endpoints

  hepatotoxicity.md   thrombocytopenia.md   complement-activation.md
  coagulopathy.md     immunotoxicity.md     cross-cutting.md
                                            dossiers (documented, not populated)

  hepatic/sources/              hepatotox source PDFs (acquired, never extracted)
  _shared/reference/            cross-toxicity textbooks and reviews
```

**Start here:** [`toxicity/README.md`](toxicity/README.md) for coverage across endpoints,
or [`toxicity/kidney/README.md`](toxicity/kidney/README.md) for the dataset itself.

Each populated endpoint directory is self-contained — its scripts resolve paths relative to
that directory, so `python3 toxicity/kidney/scripts/build_merged.py` regenerates the kidney
merged view, and `python3 toxicity/_shared/cns/qc/validate_dataset.py` runs the CNS suite's 30
structural checks — four of which verify that no endpoint's rows have been filed in another
endpoint's folder — both with no path configuration.

New work goes under the endpoint it pertains to. Material spanning endpoints goes in
`_shared/`; `REVIEW-2026-08.md` and `cross-cutting.md` cover repo-wide concerns.
