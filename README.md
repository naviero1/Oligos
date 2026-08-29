# Oligos — oligonucleotide toxicity datasets

All work is filed under [`toxicity/`](toxicity/README.md), by the toxicity endpoint it
belongs to. Nothing project-specific lives at the repository root.

The NIH/NCATS OligoTox Challenge names **eight toxicities of interest**. This repository holds
curated data for **three** of them, in **two separate datasets** — kidney toxicity, and (from
the CNS module) chronic neurotoxicity and hydrocephalus — plus a dossier for each remaining
endpoint recording what material the repo actually has for it.

The CNS module is much larger than its endpoint contribution: 1,839 oligonucleotides and 2,065
CNS measurements, of which **6 are chronic neurotoxicity and 1 is hydrocephalus**. The other
99.1% sit on the acute-neurotoxicity axis the Challenge brief explicitly deprioritises. Read
[`toxicity/chronic-neurotoxicity.md` §2](toxicity/chronic-neurotoxicity.md) before quoting the
module's size as coverage.

```
toxicity/
  README.md                     coverage index: which endpoints have rows,
                                which have sources awaiting extraction, which are empty

  kidney/                       ← populated dataset (111 measurements, 65 oligos)
    README.md  METHODOLOGY.md  schema.md  CLINICAL_VALIDATION.md  SOURCES.md
    data/  sources/  scripts/  assets/
    kidney-nephrotoxicity.md    endpoint dossier

  cns/                          ← populated dataset (2,065 measurements, 1,839 oligos;
    SUMMARY.md  README.md         7 of those rows fall on a listed endpoint — see above)
    docs/  data/  sources/  src/  qc/  figures/  deliverables/

  chronic-neurotoxicity.md  hydrocephalus.md    dossiers indexing cns/
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
merged view, and `python3 toxicity/cns/qc/validate_dataset.py` runs the CNS module's 26
structural checks, both with no path configuration.

New work goes under the endpoint it pertains to. Material spanning endpoints goes in
`_shared/`; `REVIEW-2026-08.md` and `cross-cutting.md` cover repo-wide concerns.
