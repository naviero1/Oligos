# Public Access & Dissemination Plan (PADP)

**OligoTox-Coagulopathy dataset — NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data
Challenge, Phase 2 (Data Generation).**

> **Draft for team review.** Per [`Phase Roles Assignment Plan`], the PADP is Gustavo's
> deliverable. This is a drafted, endpoint-scoped version prepared alongside the
> coagulopathy dataset so the data-side facts in it (licence mix, per-row redistribution
> terms, hosting shape) are accurate and do not have to be reconstructed later. It needs
> the team's sign-off before submission, and at submission time it will most likely be
> **consolidated with the other endpoints into a single PADP** covering the whole release —
> the Challenge asks for one plan per submission, not one per endpoint.

This plan describes how the OligoTox-Coagulopathy dataset is licensed, made publicly
accessible and disseminated, and — as the Challenge requires — how others and ultimately
the U.S. Government can allow interested parties to use it if the submitting team does not.

---

## 1. Scope — the "solution" covered by this plan

The solution is the **curated dataset and its documentation**, specifically:

| Component | Path |
|---|---|
| Four normalised data tables | `data/{sources,oligos,measurements,modifications}.csv` |
| Single-file release workbook | `OligoTox-Coagulopathy_Dataset.xlsx` |
| Data dictionary, controlled vocabularies, grading rubric | `schema.md` (and the workbook's `data_dictionary` sheet) |
| Methodology | `METHODOLOGY.md` |
| Provenance registry | `SOURCES.md`, `data/sources.csv` |
| Build, QC and verification code | `scripts/` |
| Raw extraction records | `sources/extraction/` |

**Not part of the solution:** the third-party source documents in `sources/documents/`.
They are retrieved copies of other people's copyrighted works, held so that every row's
evidence is auditable. They are **referenced, not relicensed**, and §2.3 governs them.

## 2. Licensing scheme

### 2.1 The curated tables and documentation

Released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Anyone may
use, adapt and redistribute them, including commercially, with attribution. This is a
**non-exclusive** licence granted to the world; the team retains no power to withdraw it
from anyone who has already received the data.

### 2.2 The code

Released under the **MIT licence**. The build, QC and verification scripts are what make
the dataset reproducible and checkable, so they are licensed at least as permissively as
the data.

### 2.3 Underlying sources — per-row terms, tracked

The dataset is a curation of published data, so redistribution rights vary by source and
are recorded **per row** in the `redistribution` column rather than asserted globally:

| Term | Rows | What a user may do |
|---|---:|---|
| `public_domain` | 1,382 | US patents and FDA labels. Values may be reproduced freely. |
| `CC_BY_NC_ND` | 426 | Cited; values recorded as data. Redistribute the source text only under its own terms. |
| `CC_BY` | 307 | Fully redistributable with attribution. |
| `publisher_restricted` | 192 | Cited; the extracted value is a fact, the source text is not redistributed. |
| `CC_BY_NC` | 76 | Non-commercial reuse of the source text; the extracted values are cited facts. |
| `unresolved` | 5 | Flagged for resolution before final release. |

The team's position, stated plainly: **individual measured values are facts and are not
themselves copyrightable**; what is licensed under CC BY 4.0 is the curated compilation,
its structure, its documentation and its code. Where a source's licence restricts
redistribution of the *document*, that document is cited, and the release does not
distribute it onward outside the audit copy. Users who wish to redistribute a source
document itself must obtain it from its publisher under its own terms.

### 2.4 Attribution

Users must cite **both** this dataset and the underlying primary sources for the rows they
use. `data/sources.csv` supplies the citation and identifier for every row, so the
requirement is mechanically satisfiable.

## 3. Public access — hosting and persistence

1. **Primary:** a public GitHub repository, which is where the dataset is developed and
   where its full revision history, including every correction, is visible.
2. **Archival:** deposit of each tagged release in a **Zenodo** record, which mints a DOI,
   is independent of the team's accounts, and persists if the repository is removed. The
   DOI is the citable identifier.
3. **Format:** UTF-8 CSV plus a single XLSX workbook. No proprietary format, no database
   server, no API key. The CSVs are canonical; the workbook is generated from them.
4. **No registration, no request process, no embargo.** Access is anonymous download.

Persistence is not contingent on the team: the Zenodo record and the CC BY licence together
mean the data survives the team's dissolution, loss of funding or loss of interest.

## 4. Dissemination

- **Announcement** to the oligonucleotide safety community — the Oligonucleotide Safety
  Working Group, the TIDES/TIDE meetings and the DIA oligonucleotide conference are where
  this audience is.
- **A methods paper** describing the curation and the dataset, submitted to an open-access
  venue, with the DOI as the persistent pointer.
- **Registration in data indices** so the dataset is discoverable by search rather than only
  by referral: re3data / FAIRsharing and Google Dataset Search via schema.org metadata.
- **A worked example**, as an executable notebook, showing how to load the tables, apply the
  two axis flags, filter on `grade_caveat`, and train a baseline model — because the single
  most likely misuse of this dataset is to train across the on-target rows without the
  flags, and documentation alone has not proved sufficient to prevent that.

## 5. Continuity and U.S. Government use contingency *(required)*

The Challenge requires a plan for the case where the winner does not maximise public access
and does not permit others to do so on reasonable terms. **This dataset is structurally
immune to that failure**, and the mechanism matters more than the promise:

1. **The licence is irrevocable.** CC BY 4.0 cannot be withdrawn from anyone who has
   received the work. If the team stops maintaining the dataset, every copy already
   distributed remains fully usable, adaptable and redistributable.
2. **The archival copy is outside the team's control.** A Zenodo deposit cannot be deleted
   by the depositor at will; its DOI continues to resolve.
3. **Reproducibility does not depend on the team.** The build, QC and verification scripts
   are MIT-licensed and run from a clean checkout with no network access, so any third
   party can rebuild the dataset from the committed extraction records and verify it
   against the committed sources. Nothing about the pipeline requires a person.
4. **Explicit grant to the U.S. Government.** The team grants the U.S. Government a
   non-exclusive, irrevocable, royalty-free, worldwide right to use, reproduce, distribute
   and prepare derivative works of the solution, and **to authorise others to do so on its
   behalf**, for any purpose. This grant is not contingent on the team's continued
   participation, and applies immediately, not only on the team's failure.

**Scenarios.**

| Scenario | What happens |
|---|---|
| Team continues normally | Team maintains the repository and issues versioned releases; DOI per release. |
| Team stops maintaining | Zenodo record and CC BY licence keep the data available and reusable indefinitely. Any third party may fork and continue under §2. |
| Team refuses a reasonable request | The requester does not need permission: CC BY 4.0 already grants it. There is no gate to refuse at. |
| Team dissolves or is unreachable | §5.4 lets the U.S. Government authorise others directly; §5.3 means they can rebuild and verify without the team. |

## 6. Maintenance and versioning

Semantic versioning on releases. Every release states its counts and its QC result. A
correction is a new version, never a silent edit — the row-level corrections applied so far
are committed as `sources/verification_corrections.json` and applied by the build, so the
change is legible in the history rather than buried in a CSV diff.

**Known state at this version, disclosed rather than smoothed over:** all grades are
`provisional` and have had no subject-matter review; the open defects are enumerated in
[`coagulopathy.md`](coagulopathy.md) §7. A user is entitled to know what is unfinished
before they build on it.

## 7. Stewardship

Contact and issue tracking through the public repository, so requests and defects are
visible to everyone rather than resolved privately. Defect reports against specific rows
are welcome and are the reason `verbatim_quote` and `source_locus` exist on all 2,388 rows:
any user can check any row against its source without asking the team for anything.

## 8. Compliance summary

| Challenge requirement | Where met |
|---|---|
| Dissemination of the solution and the knowledge to use it | §3, §4 |
| Non-exclusive licences for research purposes | §2.1, §2.2 |
| Provision for others to use it if the winner cannot | §5.1–§5.3, with scenarios |
| Specific licensing schemes and scenarios | §2, §5 table |
| U.S. Government authorisation of third parties | §5.4 |
| Public posting of this PADP | Agreed; this document is written for publication. |
