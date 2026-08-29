# Public Access & Dissemination Plan (PADP) — OligoTox-Thrombocytopenia

**NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge, Phase 2
(Data Generation).**

This plan covers the **thrombocytopenia / platelet-toxicity** endpoint only. The
sister nephrotoxicity dataset has its own plan at `../PADP.md`; the two are
independent submissions and neither depends on the other.

It describes how this dataset is licensed, made publicly accessible, and
disseminated, and — as the Challenge requires — **how the U.S. Government can
allow interested parties to use the dataset even if the submitting team does not
itself continue to use or distribute it.**

---

## 1. Scope — the "solution" covered by this plan

| Artifact | Description |
|---|---|
| `data/oligos.csv` | unique oligonucleotides — identity + design predictors (17 columns) |
| `data/measurements.csv` | graded per-measurement platelet-toxicity records (23 columns) |
| `data/oligotox_thrombo_merged.csv` | generated denormalized analysis view (regenerated, never hand-edited) |
| `schema.md` | Data dictionary, controlled vocabularies, and the 0–3 grade rubric |
| `METHODOLOGY.md` | Assembly, grading conventions, QC, verification status, known limitations |
| `SOURCES.md` | Source registry with per-source redistribution class |
| `README.md` | Overview, the controlled comparisons, and the fitness-for-purpose analysis |
| `scripts/` | The full pipeline — assembly, verdict application, QC, reporting |
| `curation/` | The curation record — raw extractions, verification verdicts, source sweep |

Live counts are in `README.md`, generated from the CSVs so they cannot drift.

The dataset is a **curation of already-published data**. It contains **no
human-subjects data, no personally identifiable information, and no protected
health information** — only aggregate/experimental toxicology values and design
descriptors drawn from public literature, regulatory documents, and patents.
There are therefore **no privacy, consent, or data-use-agreement constraints** on
redistribution.

### Why the curation record is included

`curation/` holds the raw agent extractions, the adversarial-verification
verdicts, and the source sweep. It is committed so the published tables are
**reproducible from their inputs**, not merely re-checkable against their
citations — a consumer can rebuild both CSVs byte-for-byte and audit how any
value entered the dataset. It contains **no third-party full texts**: sources are
referenced by identifier and exact locus, never redistributed, so it carries the
same licensing position as the tables.

## 2. Licensing scheme

- **Curated data tables, documentation, scripts and curation record** produced by
  the team are released under **Creative Commons Attribution 4.0 International
  (CC-BY 4.0)** — a **permissive, irrevocable** licence letting **anyone**
  (including the U.S. Government and any third party) access, reuse,
  redistribute, modify and build upon the dataset in perpetuity, subject only to
  attribution. *(A more permissive dedication such as CC0 1.0 can be substituted
  at NCATS's preference.)*
- **Underlying third-party full texts are never redistributed.** Every row records
  its rights status in the `redistribution` column, so a consumer can filter to
  exactly the rows they are entitled to reuse:

| Class | Meaning |
|---|---|
| `public_domain` | USPTO patents, FDA/EMA documents — reproduce without restriction |
| `cc_by` | source is CC-BY licensed; raw values reproducible **with attribution** |
| `derived_features_only` / `summary_stat` | copyrighted content; derived features or summary statistics under fair use |
| `verify` | rights unresolved — must be settled before release |

  A `cc_by` classification is taken from the article's **own licence field**,
  never from the fact that it is free to read. This per-row tracking is what makes
  the dataset lawfully redistributable as a whole.
- **No patents, trade secrets, or restrictive IP** are or will be claimed. There
  is no proprietary component whose withdrawal could remove public access.

Because the licence is **irrevocable once granted**, third-party use does **not**
depend on the team's continued participation.

## 3. Public access — hosting and persistence

- **Primary distribution:** the public repository `naviero1/Oligos`, openly
  accessible without registration.
- **Independent archival persistence + citable identifier:** a versioned snapshot
  of each release will be deposited in a public long-term archive (e.g. **Zenodo**
  or an **NIH-designated repository**) and assigned a **DOI**, guaranteeing the
  dataset remains findable and retrievable **independently of the team or any
  single hosting account**.
- **Non-proprietary formats:** UTF-8 **CSV** for data, **Markdown** for
  documentation, **JSON** for the curation record — all openable with free,
  ubiquitous tooling.

## 4. Dissemination

- **Documentation for reuse:** `README.md`, `schema.md`, `METHODOLOGY.md`,
  `SOURCES.md`, and `curation/README.md`.
- **Reproducibility:** `scripts/ingest_thrombo.sh` runs the whole pipeline from
  the committed curation record; QC gates the round.
- **FAIR alignment:**

| Principle | How the dataset meets it |
|---|---|
| **Findable** | Stable primary keys (`TOLG###`, `TMSR###`); archival DOI; descriptive metadata |
| **Accessible** | Open repository + archive; open CSV/Markdown/JSON; no gatekeeping |
| **Interoperable** | Controlled vocabularies, normalized two-table schema shared with the sister kidney dataset, standard formats |
| **Reusable** | CC-BY 4.0 + per-row provenance (`source_id`, `source_ref`, `source_table`) so any value is re-verifiable, plus the inputs needed to rebuild it |

## 5. Continuity and U.S. Government use contingency *(required)*

- **Scenario A — Normal operation.** The team maintains the repository and
  archival deposit. Third parties use the dataset under CC-BY 4.0.
- **Scenario B — Team ceases activity or fails to disseminate.** No action by the
  team is needed for continued public use: the dataset has **already been released
  under an irrevocable CC-BY 4.0 licence** and a **copy is deposited in an
  independent public archive with a DOI**. The U.S. Government and any interested
  party may continue to access, copy, host and build upon it **without further
  permission**. The permissive licence and the independent archival copy are the
  mechanisms that accomplish this plan.
- **Scenario C — Explicit government grant.** The team additionally grants the
  U.S. Government a **non-exclusive, irrevocable, royalty-free right** to use,
  reproduce, distribute, publicly display, host copies of, and **authorize others
  to use** the dataset and its documentation. This right survives any cessation of
  the team's activity.

In no scenario does third-party or Government use depend on the team's ongoing
involvement, on a proprietary service, or on any revocable permission.

## 6. Maintenance and versioning

- **Versioned releases** with a changelog; each release archived under its own DOI
  so prior versions remain citable.
- **Verification status is tracked in-repo.** Rows verified against their primary
  source carry a `verified_against_source` marker; `METHODOLOGY.md` states which
  blocks have been verified and which remain outstanding. A release must not be
  described as fully verified while any block is outstanding.
- **Provisional grades** are flagged in-row pending subject-matter review.
- Corrections and additions are tracked through the repository's public history.

## 7. Stewardship

- **Maintainer:** the submitting team, via the public repository.
- **Fallback steward:** the independent public archive (Zenodo / NIH-designated
  repository) preserves the deposited snapshot and DOI irrespective of team status.
- **Challenge contact:** as listed in the Phase 2 submission record.

## 8. Compliance summary

- Consistent with **NIH Scientific Data Sharing / Public Access policy** and **FAIR**.
- **Open, irrevocable licence** (CC-BY 4.0) ensures perpetual public usability.
- **No PII/PHI / no human-subjects data** → no privacy or consent barriers.
- **Provenance and redistribution tracked per row** → lawful reuse is verifiable
  at the record level, and the dataset is rebuildable from its committed inputs.
