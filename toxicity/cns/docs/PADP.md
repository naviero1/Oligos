# Public Access and Dissemination Plan — OligoTox-CNS

Written to satisfy the challenge requirement that *"any terms for data access and data use
should be defined in allowing for open and public access, such as through a creative commons
licence"*, and to align with the NIH Data Management and Sharing Policy.

---

## 1. What is being shared

The complete dataset, the complete build pipeline, and every source file the pipeline reads.

| artefact | format | shared |
|---|---|---|
| `data/oligos.csv` | CSV, UTF-8 | yes |
| `data/measurements.csv` | CSV, UTF-8 | yes |
| `data/modifications.csv` | CSV, UTF-8 | yes |
| `data/sources.csv` | CSV, UTF-8 | yes |
| `deliverables/OligoTox-CNS_Dataset.xlsx` | XLSX | yes — the same data, plus README, data dictionary and a live-formula summary sheet |
| `docs/` | Markdown | yes — schema, data dictionary, scoring instruments, this plan |
| `src/`, `qc/` | Python | yes — the whole pipeline, so any number can be regenerated |
| `figures/` | PNG | yes |
| `sources/` | XLSX, PDF, DOCX | yes, where the source licence permits redistribution |

There is **no restricted tier**. There are no human subjects, no personally identifiable
information and no consent constraints: every measurement is either a preclinical result or an
aggregate incidence figure already published in an FDA label.

## 2. Access terms

No registration, no data-use agreement, no access committee, no embargo. Files are plain CSV
and XLSX openable without proprietary software.

Licence, in full, in `LICENSE.md`:

- Everything created by this project — schema, code, documentation, figures, derived fields —
  is **CC BY 4.0**.
- Row-level content carries the terms of its source, recorded per row in `redistribution`:
  **2,018 of 2,065 measurements (97.7 %)** are CC BY 4.0 or US public domain and are reusable
  for any purpose including commercially; **47 (2.3 %)** derive from CC BY-NC sources, are
  individually marked, and are removable with a one-line filter.

## 3. Where it will live

| channel | purpose | state |
|---|---|---|
| Public git repository | canonical source of truth; full history, so any figure or table can be traced to the commit that produced it | **live** |
| Zenodo deposit | archival copy with a citable DOI, so the dataset can be referenced in publications | **planned at submission** — the repository is structured for direct deposit |
| Challenge submission portal | the narrative PDF, methodology PDF and dataset workbook | at submission |

Zenodo is chosen over a domain repository because there is no established public repository for
oligonucleotide toxicity data — which is part of the gap this dataset addresses. Deposit will
carry the same CC BY 4.0 terms and the same per-row `redistribution` column.

## 4. FAIR

**Findable.** Stable primary keys (`oligo_id`, `measurement_id`) with source-prefixed
identifiers. A planned Zenodo DOI. Every source carries DOI, PMID and PMCID in `sources.csv`.

**Accessible.** Non-proprietary formats over plain HTTP, no authentication. The build pipeline
is included, so the dataset can be rebuilt from the sources rather than taken on trust.

**Interoperable.** Controlled vocabularies on every categorical column, enforced by
`qc/validate_dataset.py` rather than by convention. Sequences use standard 5′→3′ notation.
Chemistry uses one vocabulary across all sources (`LNA`, `2'-MOE`, `DNA_2prime_deoxy`).
Foreign keys are checked, not assumed.

**Reusable.** A per-row provenance trail — source, exact table or figure, and redistribution
terms. A data dictionary generated from the schema definitions so it cannot drift. An explicit
missing-value vocabulary that distinguishes "not reported" from "not applicable" from zero.

## 5. Quality control

`qc/validate_dataset.py` runs 26 checks covering key uniqueness, referential integrity,
controlled-vocabulary conformance, grade range, sequence self-consistency (declared length and
base counts against the actual sequence), modification-table completeness and contiguity, and
the provenance rule that **no numeric readout may exist without a named source table or
figure**. All 26 pass. The script exits non-zero on any failure, so it can gate a release.

`qc/verify_nephro_intake.py` independently reproduces all 13 headline claims of the sibling
nephrotoxicity module from its raw CSVs, since that module was used as the pattern reference.

## 6. Maintenance

Version 1.0 is a complete, self-consistent release. Anticipated future work, in priority order:

1. Subject-matter-expert review of the provisional severity grades, converting
   `grade_status` from `provisional` to `expert_confirmed`.
2. Extraction of the two acute-inhibition and acute-activation scoring datasets currently
   documented as instruments only (`docs/SCORING_INSTRUMENTS.md` §§ 3–4), which would add
   non-human-primate rows and a second chemistry class (2′-MOE).
3. Any human in vitro CNS data that becomes available — the largest scientific gap in v1.0.

Corrections will be made by pull request against the public repository, with the QC suite as
the merge gate; each release will be re-deposited to Zenodo with a new version DOI, and the
concept DOI will always resolve to the latest.

## 7. Preservation

The repository is self-contained: the source files the pipeline reads are committed alongside
the code, so the dataset remains rebuildable even if a publisher URL rots. The Zenodo deposit
provides independent long-term archival.
