# Submission status — nephrotoxicity, 3 September 2026

Assessed against the Phase 2 brief (`Phase 2 description.docx`) and the team work plan
(`Phase 2 Work-Plan.xlsx`), both in the shared Drive. **Scope: kidney only** — verified,
see §4.

**All four Phase 2 artefacts now exist and `scripts/release_check.py` passes.** Two
requirements remain open on their merits, not through inaction; both are in §3 and both
need a team decision rather than more curation.

---

## 1. The four required deliverables

| # | Deliverable | Artefact | State |
|---|---|---|---|
| 1 | Narrative document (≤12 pp) | `NARRATIVE.md` | **Drafted** — exec summary, controls, findings, production, variables, gap, modelling |
| 2 | Methodology document (≤5 pp) | `METHODOLOGY_PHASE2.md` | **Drafted** — including the required "methods used to purify and characterize oligo identity" (§5) |
| 3 | Public Access & Dissemination Plan (≤5 pp) | `PADP.md` | **Complete** — CC BY 4.0, three continuity scenarios incl. U.S. Government grant |
| 4 | Dataset (dictionary + schema + data) | `schema.md`, `data/*.csv` | **Complete** — 65 oligos × 20, 246 measurements × 25, merged 246 × 44, bridge view |

Rendering to PDF is the only remaining mechanical step; all four are written to the
brief's required section structure.

## 2. Dataset at submission

| `subject_class` | rows | share |
|---|---:|---:|
| `animal_invitro` (rat primary PTEC) | 81 | 32.9% |
| `human_invitro` (human PTEC, PTEC-TERT1, ciPTEC, 3D-RPTEC, tubule-on-chip) | 67 | 27.2% |
| `animal_invivo` (rat, mouse, monkey) | 56 | 22.8% |
| `human_clinical` | 42 | 17.1% |

**246 measurements · 65 oligos · 35 target genes · 15 bridging oligos.**
109 rows (44.3%) human. Grades 0/1/2/3 = 97/58/60/31. Sequences 55/65. Doses 207/246.

Growth this cycle: **111 → 246 measurements**, human in-vitro **19 → 67** (smallest class
to second-largest), bridge set **9 → 15**.

## 3. Open on merit — needs a team decision

**a. Purity data is absent for all 65 oligos, and cannot be curated.** The brief requires
it twice. We verified rather than assumed: both source patents were searched for purity /
HPLC / UPLC / LC-MS / mass-spec language and neither reports any; labels and trial papers
do not publish per-batch purity. No wet lab was run. `purity_pct` and `purity_method` are
explicit `TBD` with the reason recorded, and the *identity* half of the requirement is
answered in full via `identity_confirmation` (55/65 established, method recorded per
oligo). **The decision required is how to present this in the submission** — as a stated
limitation of the curation approach, which is our recommendation, rather than as a silent
blank.

**b. The negative class is improved but not clean.** The provenance/outcome confound was
weakened 3.7× (Fisher p = 4.5 × 10⁻⁵ → 1.65 × 10⁻⁴) by adding measured negatives, and
`renal_endpoints_measured` now flags **13 grade-0 clinical rows as not supported as
measured negatives**. The hazard is now machine-readable rather than hidden, which is the
important change. But 36 `WS` rows remain search-derived, and closing them needs NEJM /
Circulation trial papers and FDA Pharmacology-Toxicology reviews that this environment
cannot fetch (`accessdata.fda.gov` blocked). **The decision required is whether to ship
with the rows flagged, or to obtain those documents first.**

## 4. Scope isolation — verified

`scripts/release_check.py` asserts it on every run: 246/246 `is_kidney_specific=TRUE`;
`tissue` only `kidney`/`proximal_tubule`; zero hepatic readouts, models or hepatotoxicity
source panels; viability rows renal-tissue only. Hepatotoxicity material held elsewhere in
the repository contributes **no rows**.

Two false positives were found and fixed in the checker itself, not the data:
case-insensitive `ALT` matches "he**alt**hy_volunteer", and *Liver International* is the
journal that published the **givosiran CKD** finding — a kidney result. The gate now
matches biomarker abbreviations case-sensitively with word boundaries and checks source
provenance against actual hepatotoxicity source identifiers.

## 5. Closed this cycle

- **21 rows (19% of the then-dataset) recorded a rat study as mouse**, with a published
  dose left `TBD`. Verified against the patent's own method section and corrected; species
  moved from mouse 30 / rat 8 to rat 29 / mouse 9.
- **`subject_class`** added — the explicit human/animal divider, derived not hand-entered —
  plus `animal_invitro`, a class the earlier version silently collapsed into `animal_invivo`.
- **US 11,105,794 Table 2** extracted (+48 human in-vitro rows) and **US 11,479,818
  Table 5** extracted (+81 rat in-vitro rows incl. KIM-1). Both parsed reproducibly with
  anchor checks against the printed tables; both grading rubrics anchored on the source's
  own innocuous control.
- **Three approved DMD PMOs** added (golodirsen, casimersen, viltolarsen), previously
  carrying no rows at all, contributing measured human negatives.
- **`renal_endpoints_measured`**, **`identity_confirmation`**, **`purity_pct`/`purity_method`**
  added. **`LICENSE`** (CC BY 4.0) added at repository root.
- **`NARRATIVE.md`** and **`METHODOLOGY_PHASE2.md`** written; `PADP.md` reconciled.
- Documentation reconciled to data throughout (row counts, species table, sequence counts,
  the unqualified "animal over-predicts" claim).

## 6. Honest summary

The dataset is **real, growing and defensible**: 246 measurements, per-row provenance,
strict-kidney isolation machine-verified, and the class the brief values most now well
represented. The scientific findings — bidirectional animal↔human translation, a human
cell system out-detecting the animal in-vivo grade on a known human nephrotoxin, and the
provenance confound itself — are genuine contributions rather than filler.

It is **submission-ready in structure**, with two substantive caveats (§3) that are
disclosed in the narrative rather than hidden, and grades that remain **provisional
pending scientific sign-off**. That sign-off is the single most valuable thing a reviewer
can add now.
