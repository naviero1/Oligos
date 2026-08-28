# Public Access & Dissemination Plan (PADP)

**OligoTox-Kidney dataset — NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open
Data Challenge, Phase 2 (Data Generation).**

This plan describes how the OligoTox-Kidney dataset is licensed, made publicly
accessible, and disseminated, and — as required by the Challenge — **how the U.S.
Government can allow interested parties to use the dataset even if the submitting
team does not itself continue to use or distribute it.** It is a required component
of the Phase 2 submission and is written to align with NIH Scientific Data Sharing
/ Public Access policy and the FAIR data principles.

---

## 1. Scope — the "solution" covered by this plan

The solution is **two curated, openly-releasable endpoint datasets** and their
documentation. Both are covered by this plan on identical terms.

### 1a. OligoTox-Kidney (nephrotoxicity)

| Artifact | Description |
|---|---|
| `data/oligos.csv` | 65 oligonucleotides — identity + design predictors (17 columns) |
| `data/measurements.csv` | 111 graded per-measurement nephrotoxicity records (23 columns) |
| `schema.md` | Full data dictionary, controlled vocabularies, and the 0–3 grade rubric |
| `METHODOLOGY.md` | How the dataset was assembled (sources → extraction → grading → QC) |
| `sources/SOURCES.md` | Source registry, redistribution status, acquisition state |
| `README.md`, `PRESENTATION.md` | Overview and findings deck |

### 1b. OligoTox-Thrombocytopenia (platelet toxicity)

| Artifact | Description |
|---|---|
| `thrombocytopenia/data/oligos.csv` | 251 oligonucleotides — identity + design predictors (17 columns) |
| `thrombocytopenia/data/measurements.csv` | 1,786 graded per-measurement platelet-toxicity records (23 columns), 628 carrying a `verified_against_source` marker |
| `thrombocytopenia/data/oligotox_thrombo_merged.csv` | generated denormalized analysis view (regenerated, never hand-edited) |
| `thrombocytopenia/schema.md` | Data dictionary, controlled vocabularies, and the 0–3 grade rubric |
| `thrombocytopenia/METHODOLOGY.md` | Assembly, grading conventions, QC, verification status, and known limitations |
| `thrombocytopenia/SOURCES.md` | Source registry with per-source redistribution class |
| `thrombocytopenia/README.md` | Overview, the five controlled comparisons, and the fitness-for-purpose analysis |
| `thrombocytopenia/curation/` | **the full curation record** — raw agent extractions, verification verdicts, and the source sweep |

The thrombocytopenia dataset commits its curation record so the published tables
are **reproducible from their inputs**, not merely re-checkable against their
citations. That record contains no third-party full texts — sources are
referenced by identifier and exact locus, never redistributed — so it inherits
the same licensing position as the tables themselves.

The dataset is a **curation of already-published data**. It contains **no human-
subjects data, no personally identifiable information, and no protected health
information** — only aggregate/experimental toxicology values and design
descriptors drawn from public literature, regulatory labels, and patents. There
are therefore **no privacy, consent, or data-use-agreement constraints** on
redistribution.

---

## 2. Licensing scheme

- **Curated data tables and documentation** produced by the team are released under
  the **Creative Commons Attribution 4.0 International (CC-BY 4.0)** license — a
  **permissive, irrevocable** license that lets **anyone** (including the U.S.
  Government and any third party) access, reuse, redistribute, modify, and build
  upon the dataset in perpetuity, subject only to attribution.
  *(License choice is the team's proposal; a more permissive dedication such as
  CC0 1.0 can be substituted at NCATS's preference.)*
- **Underlying third-party full texts are never redistributed.** Journal articles
  are **referenced by DOI/PMID**, not copied. Values reproduced in the tables are
  limited to (a) **public-domain** sources — USPTO patents and U.S./EU regulatory
  labels — and (b) **summary statistics** used under fair use. Every row records
  its rights status in the `redistribution` column (`public_domain` or
  `summary_stat`).
- **No patents, trade secrets, or restrictive IP** are or will be claimed over the
  dataset. There is no proprietary component whose withdrawal could remove public
  access.

Because the license is **irrevocable once granted**, the ability of third parties
to use the dataset does **not** depend on the team's continued participation.

---

## 3. Public access — hosting and persistence

- **Primary distribution:** a public code-hosting repository (GitHub —
  `naviero1/Oligos`), openly accessible without registration.
- **Independent archival persistence + citable identifier:** a versioned snapshot
  of each release will be **deposited in a public, long-term archive** (e.g.,
  **Zenodo** or an **NIH-designated repository**) and assigned a **DOI**. This
  guarantees the dataset remains findable and retrievable **independently of the
  team or any single hosting account.**
- **Non-proprietary formats:** UTF-8 **CSV** for data and **Markdown** for
  documentation — openable with free, ubiquitous tooling, with no software
  dependency or license required to read.

---

## 4. Dissemination

- **Documentation for reuse:** `README.md` (overview), `schema.md` (data dictionary
  + rubric), `METHODOLOGY.md` (assembly + QC), and the findings deck.
- **Discoverability:** descriptive metadata and keywords, a citable DOI, and links
  from the Challenge submission record.
- **FAIR alignment:**

| Principle | How the dataset meets it |
|---|---|
| **Findable** | Stable primary keys (`oligo_id`, `measurement_id`); archival DOI; descriptive metadata |
| **Accessible** | Open repository + archive; open CSV/Markdown; no gatekeeping |
| **Interoperable** | Controlled vocabularies (common data elements), normalized two-table schema, standard formats |
| **Reusable** | CC-BY 4.0 license + per-row provenance (`source_id`, `source_ref`, `source_table`) so any value is re-verifiable |

---

## 5. Continuity and U.S. Government use contingency *(required)*

The Challenge requires a plan for how the U.S. Government can allow interested
parties to utilize the solution **if the team fails to utilize it and does not
permit others to use it under reasonable terms.** The following scenarios cover
this:

- **Scenario A — Normal operation.** The team maintains the repository and archival
  deposit and disseminates updates. Third parties use the dataset under CC-BY 4.0.
- **Scenario B — Team ceases activity or fails to disseminate.** No action by the
  team is needed for continued public use: the dataset has **already been released
  under an irrevocable CC-BY 4.0 license** and a **copy is deposited in an
  independent public archive with a DOI.** The U.S. Government and any interested
  party may continue to access, copy, host, and build upon the dataset **without
  further permission.** The permissive license and independent archival copy are
  the mechanisms that accomplish this plan.
- **Scenario C — Explicit government grant.** The team additionally grants the U.S.
  Government a **non-exclusive, irrevocable, royalty-free right** to use, reproduce,
  distribute, publicly display, host copies of, and **authorize others to use** the
  dataset and its documentation. This right survives any cessation of the team's
  activity and enables the Government to allow interested parties to utilize the
  dataset under reasonable terms.

In no scenario does third-party or Government use depend on the team's ongoing
involvement, on a proprietary service, or on any revocable permission.

---

## 6. Maintenance and versioning

- **Versioned releases** with a changelog; each release archived under its own DOI
  so prior versions remain citable and retrievable.
- **Provisional grades** are flagged in-row; a post-expert-review release will
  clear the `grade_provisional` flag and note the reviewer's disposition.
- Corrections and additions are tracked through the repository's public history.

---

## 7. Stewardship

- **Maintainer:** the submitting team, via the public repository, until (and beyond)
  archival deposit.
- **Fallback steward:** the independent public archive (Zenodo / NIH-designated
  repository) preserves the deposited snapshot and DOI irrespective of team status.
- **Challenge contact:** as listed in the Phase 2 submission record.

---

## 8. Compliance summary

- Consistent with **NIH Scientific Data Sharing / Public Access policy** and **FAIR**.
- **Open, irrevocable license** (CC-BY 4.0) ensures perpetual public usability.
- **No PII/PHI / no human-subjects data** → no privacy or consent barriers to
  sharing.
- **Provenance and redistribution tracked per row** → lawful reuse is verifiable
  at the record level.
