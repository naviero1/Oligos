# Where we stand — nephrotoxicity, 3 September 2026

Assessed against the Phase 2 brief (`Phase 2 description.docx`) and the team work plan
(`Phase 2 Work-Plan.xlsx`), both in the shared Drive. Scope: **kidney only**.

## Schedule position

The work plan puts **nephro data prep in July**, with Aug = CNS/thrombocytopenia,
Sept = complement/coagulopathy, Oct = hydrocephalus/hepatotoxicity, and **Nov = the four
submission deliverables**. Nephro is therefore past its slot and should be closing out.
It is *substantively* built — **165 measurements, 65 oligos** (111 at the start of this
pass) — but not closed: the items
in §3 below are open, and two of them cannot be closed by more curation.

## 1. The dataset against the four explicit Phase 2 requirements

The brief states the dataset "**must contain** the sequences of all oligos tested, as well
as the location of all chemical modifications in each oligo, data on the purity and
characterization of each, and any additional metadata."

| Requirement | Status | Detail |
|---|---|---|
| Data dictionary + schema | **Met** | `schema.md`, per-column, with controlled vocabularies and a QC log |
| Sequences of **all** oligos tested | **Partial — 55/65** | 6 proprietary (Moisan, Sandelius), 2 class-level aggregates, 2 Ionis code compounds with no INN. See `METHODOLOGY.md` §11 |
| **Location** of all chemical modifications | **Partial** | `sugar_modifications` 65/65, but position-resolved only where case encodes it (21/55 sequences) or `gapmer_design` is populated (40/65); `ps_count` 38/65 |
| **Purity and characterization** of each | **Absent — 0 coverage** | No column exists, and no value. Discussed in §3 |
| Open licence (e.g. Creative Commons) | **Described, not applied** | CC-BY 4.0 specified in `PADP.md`, but **no `LICENSE` file exists** in the repository |

## 2. The human/animal division (added this pass)

The brief singles out datasets "based on in vitro human systems **or able to extrapolate
data between in vitro human systems and animal data**" as of particular interest, so this
division is a scoring criterion, not housekeeping.

| `subject_class` | rows | share | change this pass |
|---|---:|---:|---|
| `human_invitro` | 67 | 40.6% | **19 → 67** (Table 2 extraction) |
| `animal_invivo` | 56 | 33.9% | 53 → 56 |
| `human_clinical` | 42 | 25.5% | 39 → 42 (DMD PMO labels) |

Total measurements **111 → 165** this pass.

The split was already clean — no human `animal_invivo` rows, no animal `clinical` rows —
but implicit in a two-column join. It is now the derived field `subject_class`, plus the
`data/human_animal_bridge.csv` view.

**Two observations worth acting on.**

*The category the brief values most was our smallest — this is now fixed.* Human in-vitro
was 17.1%; extracting US 11,105,794 Table 2 (48 quantitative rows on primary human PTEC
and PTEC-TERT1 under gymnotic exposure) makes it **the largest class at 40.6%**. The
remaining candidate is the companion patent US 11,479,818 (`N4`), still unextracted.

*The extrapolation evidence is now 15 oligos* (was 9): 6 concordant, 6 animal-over-predicts,
3 animal-**under**-predicts. The under-prediction
cases — inotersen (human grade 3 crescentic glomerulonephritis vs animal 1) and givosiran
(human 2 vs animal 1) — are the safety-relevant direction, and they contradict the
received wisdom that animal tox over-predicts human renal effects. That is a genuine
finding and is the most defensible thing the dataset currently says about extrapolation.
It is also bounded: 15 oligos is still not a rule, and 3 of the 6 over-prediction verdicts
(lumasiran, vutrisiran, AON-C) rest on human grade-0 values that source retrieval could not
support. The other 3 — golodirsen, casimersen, viltolarsen — rest on *measured* human
negatives, so the over-prediction side is now half well-founded rather than mostly not.

## 3. Open items, hardest first

**a. Purity and characterization data does not exist and cannot be curated.** The brief
requires it twice — in the dataset, and in the methodology document ("the methods used to
purify and characterize oligo identity"). This dataset is an in-silico curation of
published data; per-oligo HPLC/mass-spec purity is essentially never published in labels,
patents or trial papers. No amount of further extraction will produce it. The options are
to state plainly in the methodology *why* it is absent for a curation-type dataset, to
capture the handful of cases where a patent or paper does report purity, or to accept the
gap knowingly. **This should be a deliberate team decision, not a silent omission** — it
is the requirement we are furthest from meeting.

**b. The negative class is improved but still not trustworthy.** Provenance and outcome
remain confounded: 0 of 20 search-derived clinical rows reach grade ≥2, against 11 of 22
anchor-sourced rows. Adding three *measured* human negatives (the DMD PMO labels, which
prescribe cystatin C / UPCR / dipstick monitoring and then report no toxicity) weakened the
association **3.7×**, from one-sided Fisher p = 4.5 × 10⁻⁵ to **p = 1.65 × 10⁻⁴**, and took
anchor-sourced grade-0 clinical rows from 1 to 4. That is progress by the right mechanism —
adding good negatives, not deleting positives — but p = 1.65 × 10⁻⁴ is still strong
evidence of confounding, the 20 WS rows are untouched, and the recommended
`renal_endpoints_measured` field is **still not implemented**. Until it is, grade 0
continues to conflate "looked and found nothing" with "nobody looked".

**c. No `LICENSE` file.** PADP describes CC-BY 4.0; the repository does not carry it. A
one-file fix, but the brief asks for access terms to be *defined*, and a described licence
is not an applied one.

**d. 39 rows still lack a dose.** Down from 54 after the patent correction. Most of the
remainder need FDA Pharmacology/Toxicology reviews, which this environment cannot fetch
(`accessdata.fda.gov` is blocked) — see `SOURCES.md`.

**e. The three narrative deliverables are not drafted.** `METHODOLOGY.md` and `PADP.md`
are substantial but are repository documentation, not the ≤5-page PDFs the brief asks for;
the ≤12-page narrative has no draft (`PRESENTATION.md` is a deck, not the narrative). Due
November per the work plan.

## 4. Closed this pass

- **21 patent rows (19% of the dataset) recorded the wrong species.** `MSR91`–`MSR111`
  said mouse / 7 days / dose unknown; US 11,105,794 p.25 says Wistar Han **rats**, dosed
  40 mg/kg on days 1 and 8, sacrificed day 15, read on a **Rat** Kidney Toxicity panel.
  Corrected and re-verified against the in-repo PDF. Species distribution moves from
  mouse 30 / rat 8 to **rat 29 / mouse 9**; missing doses fall 54 → 33.
- `subject_class` divider and the human/animal bridge view added.
- **US 11,105,794 Table 2 extracted** — acquired in June, never mined. 48 quantitative
  human in-vitro rows (primary human PTEC and PTEC-TERT1, gymnotic exposure, extracellular
  EGF). Human in-vitro **19 → 67**, from the smallest class to the largest. Parsed
  reproducibly from the layout-preserving text with 4 values checked against the printed
  table; grading rubric anchored so the patent's own innocuous control grades 0 throughout.
- **The three approved DMD PMOs added** — golodirsen, casimersen, viltolarsen previously
  had no rows at all. Their human negatives are measured, not absent, and weakened the
  confound as described in §3b.
- Documentation reconciled to data: stale 46/65 sequence count, stale species table, stale
  row counts, and the unqualified "animal over-predicts" claim all corrected.

## Honest summary

The dataset is **real and defensible on volume** — the ≥100-row target is met, provenance
is per-row, and the corrections in §4 removed a 19% species error. This pass grew it
**111 → 165 rows**, turned the class the brief values most from the smallest into the
largest, and removed a 19% species error.

It is **still not submission-ready**, for two reasons that more extraction will not fix:
(a) purity/characterization is required twice by the brief and cannot be curated from
published sources, and (b) the negative class, though measurably better, has not survived
verification. Both need a team decision. The tractable remainder — a `LICENSE` file, the
`renal_endpoints_measured` field, the `N4` companion patent, and the three narrative
PDFs — is ordinary work with a clear path.
