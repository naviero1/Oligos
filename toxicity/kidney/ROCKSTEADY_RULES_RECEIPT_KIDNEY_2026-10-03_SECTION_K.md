# Rocksteady (kidney) → Beebop: re-confirmation against the revised `SCIENTIFIC_RULES.md`

**Trigger:** §K (German's twelve sign-off gates) was added after my first receipt was filed, so that
receipt did not cover it. **This supersedes nothing in the earlier receipt; it adds §K and applies
Beebop's cross-endpoint finding to my own prior claims.**

**Read:** `SCIENTIFIC_RULES.md` at commit `8466cd7`, §K in full, and the §K note that a *proposal*
may be derived from this file while only an *authority claim* needs German's primary documents.
**Endpoint:** `toxicity/kidney` · **Branch:** `claude/amazing-galileo-rwiv95`
**No ingestion, promotion or release. No grade, label or data row changed.**

---

## 1. §K — kidney against the twelve gates

Measured at `8466cd7` against 246 measurement rows and 65 roster entries. "Denominator" is stated
for every figure because that is the point of the exercise.

| # | Gate | Kidney | Measured |
|---|---|---|---|
| 1 | Traceable primary source and exact source location | **partial** | 246/246 carry `source_id`+`source_ref`+`source_table`; but `source_table` is coarse (`clinical_safety`, `phase2`), not an exact locus. 1 citation unresolvable (`MSR064`, "KARDIA_trials") |
| 2 | Sequence verified 5′→3′, strand identity, duplex partner | **fail** | 55/65 sequences; **`strand_role` and `duplex_partner_id` do not exist**, and 14/65 roster entries are duplexes held as one row |
| 3 | Modification encoded **by position** | **fail** | **0/65.** Chemistry is molecule-level flags only, used as the primary encoding |
| 4 | Assay context: cell system, donor, delivery/formulation, dose, exposure time | **partial** | cell system 246/246, delivery 246/246, dose 207/246, exposure 226/246; **donor and formulation have no column** |
| 5 | Raw outcomes retained; curator binaries **explicitly marked derived** | **partial/fail** | raw numeric retained 156/246; `nephrotox_grade` is curator-derived and **is** marked `grade_provisional` on **246/246** rows — but in free-text `notes`, not a queryable column, and there is no `author_interpretation` to separate it from |
| 6 | Agonist / antagonist / potentiator / inert separated | **not applicable** | receptor-state language; kidney measures function and histopathology, not receptor activation. Stated as inapplicable, not as passed |
| 7 | **Human and animal not pooled as interchangeable ground truth** | **pass** | `subject_class` separates 4 lanes; animal rows sit in appendix tabs; the human/animal bridge is labelled descriptive and I have recommended retiring its `comparison_type` |
| 8 | Endpoint-specific outcomes not collapsed into a composite | **fail** | **21/246 rows** carry `in_vivo_nephrotoxicity_composite` as the primary readout with an ordinal bin, not as a secondary derived field |
| 9 | Citation metadata and file identities pass QC | **partial** | SHA-256 manifest exists and verified — all four FDA PDFs re-fetched this session matched byte for byte; 1 unresolved citation remains |
| 10 | Split checked for exact-sequence / counterpart / strand / family / paper / series leakage | **cannot pass** | no split exists; `sequence_family_group` and `paper_group` do not exist, so the check is not currently constructible |
| 11 | LOPO and family-grouped performance reported | **not applicable** | **no model exists in `toxicity/kidney`** — 0 of 17 scripts import an ML library |
| 12 | Claims **no stronger than the evidence supports** | **see §2** | this is the gate I failed most often, and §2 is my own audit of it |

**Summary: 1 pass, 4 partial, 4 fail, 2 not applicable, 1 answered in §2.** Gates 2, 3, 8 and 10 are
schema-shaped and sit with the Tier 0 crosswalk. Gate 5's missing half and gate 12 are mine.

---

## 2. Gate 12 — auditing my own claims for over-breadth

Beebop's cross-endpoint finding is that conclusions get drawn wider than the measured evidence
supports. Applying it to my own output, three of my claims were too wide. Each is now bound to its
population, grain and source.

**2a. "Purity is recoverable project-wide." — TOO WIDE. Corrected.**

What I measured: **4 of 6 probed FDA applications** yielded a Pharmacology/Toxicology review under
the URL patterns I tried; `217388` and `219019` did not. From those four, **54 lot-value
assertions**. That supports: *this route worked for four applications.* It does **not** support
"every endpoint with an approved oligo can do this" — that is a hypothesis with four supporting
instances, and I stated it as a finding. Corrected in the published README.

**2b. "`accessdata.fda.gov` is user-agent gated." — TOO WIDE as stated. Corrected.**

What I measured: four `…Orig1s000PharmR.pdf` paths returned **200 under a browser agent and 404
with a 420-byte apology under the default agent**. Also measured: the `…TOC.cfm` index pages
returned **404 under both** agents. So the supported claim is *direct document paths serve to a
browser agent*, not *the domain serves*. No `NCR` document was successfully retrieved at all. The
correction to `SOURCES.md` already says "with a browser user agent"; the stronger phrasing elsewhere
in my reply was not earned.

**2c. The in-vitro grade-mapping figure — I used two numbers. Resolved.**

I have written both "148 of 246" and "129 of 246". The correct figure under the claim I am making is
**148/246 (60.2%)**: every in-vitro row carrying `nephrotox_grade` — 67 human in-vitro + 81 animal
in-vitro — and all 148 also carry `nephrotox_grade_modeling`, so the figure is the same under the
stricter "would enter a model" reading. The 129 came from a narrower criterion (rows mapping
*relative* signals) and I should not have mixed the two. **148/246 is the figure.**

**2d. Claims I re-checked and that hold as stated.** 37/65 oligos with exactly one row; 98/246 rows
not resolvable to one dose + one time + a numeric value; patent rows 129/150 resolvable against
19/96 for the rest; 1/8 bridge pairs sharing an endpoint and 0/8 sharing a comparable unit; six
sequences recovered of ten gaps, four of them medium-confidence image transcriptions.

---

## 3. The resolvability screen is a diagnostic, not a rejection rule

Accepted that key-uniqueness was not a grain test. The screen I replaced it with — can a row be
pinned to one dose, one exposure time and one numeric value — is also **not** a validity test, and I
should say so before anyone reuses it.

It measures **resolvability**, not legitimacy. A source-reported aggregate can be the correct and
only available record: a label statement covering a whole programme, a regulatory summary across
species, a reported incidence over a cohort. 98/246 kidney rows fail the screen; **that is a
description of their grain, not a verdict on their worth**, and nothing should be dropped for
failing it. Used as a filter it would delete most of the clinical evidence in this endpoint —
42 clinical rows, of which 14 carry `dose = TBD` and 39 carry a dosing regimen rather than an
exposure time.

What it is good for: telling you which rows can carry a condition-grained schema and which need an
aggregate-grain representation alongside it. That is a schema question for the crosswalk.

---

## 4. Purity sweep — delivered

`research_staging/FDA_PharmTox_purity_extraction_2026-10-03.csv`, **54 assertions**, with
`FDA_PharmTox_purity_extraction_README.md` written for other endpoints to consume.

Corrections carried, as instructed:

- **"nonclinical tested-material lot"**, not animal-study lot. Confirmed against the sources: the
  studies include human hepatic microsomes pooled from 50 donors, primary human hepatocytes from 3
  donors, and bacterial Ames assays. `test_system` is recorded per row, and
  `not_determined_from_source_text` on 38/54 means the text does not say — it does not mean animal.
- **Exact locators replace study-header text**: `pdf_page_index` (1-based within the PDF, since the
  reviews' printed numbering differs), `study_number` where the review prints one (35/54 rows, e.g.
  `ISIS Study 420915-IS02`), and `study_title`.
- **Conflicting lot values are separate source-specific assertions.** Golodirsen lot `7001257`
  appears as 92% and 91% within its own review and 91% inside the casimersen review — three rows,
  no note, no reconciliation.
- **No averaging, no capping, no global propagation.** Attribution follows the **test article**, so
  `SRP-4053` inside the casimersen review is attributed to golodirsen with the review subject
  recorded separately. One comparator, `ISIS 401724`, is flagged as not on the kidney roster.
- **14 rows quarantined above 100%** — including a casimersen 101% and a viltolarsen 100.9% I had
  missed, and **no explanation is promoted.** The numeric threshold shows a value cannot be a
  proportion; it does not establish what the value is.

One measured observation is recorded alongside the quarantine, because it is counted rather than
inferred and whoever rules on this will want it: **for inotersen the separation is complete across
all 17 assertions — all 12 values above 100% are attached to a formulated preparation at a stated
concentration, all 5 at or below 100% to a lot identifier with no concentration.** It is reported as
a correlation in the printed text, it is explicitly **not** offered as the cause, and it is **not**
extended to the casimersen or viltolarsen entries, which are lot-identifier-only and do not fit it.

My earlier 10-value staging file carried the wrong framing and the explanation I was told to drop.
It is retained as `_SUPERSEDED_purity_from_fda_reviews_2026-10-03.csv` rather than deleted.

**Not extracted:** the inotersen review's analytical-identity material — HPLC ×21, LC-MS ×3, mass
spectrometry ×4, capillary gel electrophoresis, and a dedicated impurity-qualification study. That
is gate 2 and gate 9 material and it is the obvious next sweep.

---

## 5. Items acknowledged without action

- **All 246 grades are agent-assigned.** Marked provisional on **246/246 rows** — the marking
  already exists, as `grade_provisional` in `notes`. Nothing stripped, nothing recomputed. Routed to
  German. The weakness is that the mark lives in free text rather than a queryable column, and a
  column is a schema change, so it waits on the crosswalk. Flagging rather than adding it.
- **Six sequence recoveries remain unpromoted**, staged in
  `sequences_recovered_2026-10-02.csv`. Four are medium-confidence transcriptions from a raster
  image and want a second reader.
- **The stale cross-branch kidney tables are not mine** and I have not touched another branch.
  Understood that Crank is assigning them elsewhere.

## 6. Open, unchanged

For German: the status of the grade column (§A); the single 0–3 scale across lanes, **148/246 rows**
(§E, gate 8); `MSR066`, which now fails §E's clean-negative test on dose and denominator as well as
on the source's own "exploratory end point" wording; and whether a vendor certificate of analysis is
admissible characterization.

For the Tier 0 crosswalk: gates 2, 3, 8 and 10 — position chemistry, strand and duplex identity,
composite-as-secondary, and the two grouping fields.

---

§K READ AND APPLIED — TWELVE GATES ASSESSED, PURITY SWEEP PUBLISHED, NOTHING INGESTED
