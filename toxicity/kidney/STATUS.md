# Where we stand — nephrotoxicity, 3 September 2026

Assessed against the Phase 2 brief (`Phase 2 description.docx`) and the team work plan
(`Phase 2 Work-Plan.xlsx`), both in the shared Drive. Scope: **kidney only**.

## Schedule position

The work plan puts **nephro data prep in July**, with Aug = CNS/thrombocytopenia,
Sept = complement/coagulopathy, Oct = hydrocephalus/hepatotoxicity, and **Nov = the four
submission deliverables**. Nephro is therefore past its slot and should be closing out.
It is *substantively* built — 111 measurements, 65 oligos — but not closed: the items
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

| `subject_class` | rows | share |
|---|---:|---:|
| `animal_invivo` | 53 | 47.7% |
| `human_clinical` | 39 | 35.1% |
| `human_invitro` | 19 | 17.1% |

The split was already clean — no human `animal_invivo` rows, no animal `clinical` rows —
but implicit in a two-column join. It is now the derived field `subject_class`, plus the
`data/human_animal_bridge.csv` view.

**Two observations worth acting on.**

*The category the brief values most is our smallest.* Human in-vitro is 17.1% of rows.
Expanding it is the highest-scoring marginal work available, and `METHODOLOGY.md` §11
already names the candidates (ciPTEC / RPTEC-TERT1 panels, the pending in-vitro
nephrotoxicity-assay patents).

*The extrapolation evidence is 9 oligos.* Those 9 carry both human and animal data:
4 concordant, 3 animal-over-predicts, 2 animal-**under**-predicts. The under-prediction
cases — inotersen (human grade 3 crescentic glomerulonephritis vs animal 1) and givosiran
(human 2 vs animal 1) — are the safety-relevant direction, and they contradict the
received wisdom that animal tox over-predicts human renal effects. That is a genuine
finding and is the most defensible thing the dataset currently says about extrapolation.
It is also fragile: 9 oligos is not a rule, and 2 of the 3 over-prediction verdicts rest
on human grade-0 values that source retrieval could not support.

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

**b. The negative class is not yet trustworthy.** Provenance and outcome are near-perfectly
confounded: 0 of 20 search-derived clinical rows reach grade ≥2, against 11 of 19
anchor-sourced rows (one-sided Fisher p = 4.5 × 10⁻⁵). Direct retrieval of 7 unverified
absence claims left 1 standing. Full analysis in `CLINICAL_VALIDATION.md`; the recommended
`renal_endpoints_measured` field is **not yet implemented**. Until it is, grade 0 conflates
"looked and found nothing" with "nobody looked".

**c. No `LICENSE` file.** PADP describes CC-BY 4.0; the repository does not carry it. A
one-file fix, but the brief asks for access terms to be *defined*, and a described licence
is not an applied one.

**d. 33 rows still lack a dose.** Down from 54 after the patent correction. Most of the
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
- Documentation reconciled to data: stale 46/65 sequence count, stale species table, and
  the unqualified "animal over-predicts" claim all corrected.

## Honest summary

The dataset is **real and defensible on volume** — the ≥100-row target is met, provenance
is per-row, and the corrections in §4 removed a 19% species error. It is **not yet
submission-ready**, and the two reasons are (a) a requirement we structurally cannot meet
by curation alone (purity/characterization) and (b) a negative class that has not
survived verification. Both need a decision from the team rather than more extraction.
