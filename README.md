# Oligos — oligonucleotide toxicity datasets

All work is filed under [`toxicity/`](toxicity/README.md), by the toxicity endpoint it
belongs to. Nothing project-specific lives at the repository root.

The NIH/NCATS OligoTox Challenge names **eight toxicities of interest**. This repository
holds curated data for **one** of them — kidney toxicity — and a dossier for each of the
others recording what material the repo actually has for it.

```
toxicity/
  README.md                     coverage index: which endpoints have rows,
                                which have sources awaiting extraction, which are empty

  kidney/                       ← the populated dataset (111 measurements, 65 oligos)
    README.md  METHODOLOGY.md  schema.md  CLINICAL_VALIDATION.md  SOURCES.md
    data/  sources/  scripts/  assets/
    kidney-nephrotoxicity.md    endpoint dossier

  hepatotoxicity.md   thrombocytopenia.md   complement-activation.md
  coagulopathy.md     immunotoxicity.md     chronic-neurotoxicity.md
  hydrocephalus.md    cross-cutting.md      endpoint dossiers (documented, not populated)

  hepatic/sources/              hepatotox source PDFs (acquired, never extracted)
  _shared/reference/            cross-toxicity textbooks and reviews
```

**Start here:** [`toxicity/README.md`](toxicity/README.md) for coverage across endpoints,
or [`toxicity/kidney/README.md`](toxicity/kidney/README.md) for the dataset itself.

Each populated endpoint directory is self-contained — its `scripts/` resolve paths
relative to that directory, so `python3 toxicity/kidney/scripts/build_merged.py`
regenerates the kidney merged view with no path configuration.

New work goes under the endpoint it pertains to. Material spanning endpoints goes in
`_shared/`; `REVIEW-2026-08.md` and `cross-cutting.md` cover repo-wide concerns.
