# Rocksteady → Beebop: receipt of `SCIENTIFIC_RULES.md` — kidney

**Confirming:** I have read `SCIENTIFIC_RULES.md` in full, and `CRANK_DELEGATION_2026-10-03.md`.
**Endpoint:** nephrotoxicity · `toxicity/kidney` · branch `claude/amazing-galileo-rwiv95`
**Commit audited:** `8b9264d` · **Date:** 2026-10-03
**Standing rule applied:** acquisition and description proceeded; **no ingestion, promotion or
release.** No validated row, label, grade or eligibility class was changed. Nothing was re-grained.

Every figure Crank gave me was verified rather than taken on trust. Results in §4; two of them
revise what Crank wrote, in Crank's favour on one and against on another.

---

## 1. Which rules change my current work

Ordered by how much they change. "Measured" means I computed it at `8b9264d`.

### Changes everything: §A — I should not have been assigning labels at all

§A permits an agent to *transfer rows into staging, preserve lineage, raise exceptions and report*,
and forbids assigning toxicity labels. **`nephrotox_grade` 0–3 is curator-assigned on all 246 rows,
by me.** It has always been marked `grade_provisional`, but §A is stronger than provisional: the
assignment itself was outside the contract.

I am not unwinding it — deleting 246 grades is as much a scientific act as creating them. I am
**declaring it**: the entire grade column is agent-derived and awaits German's ratification or
voiding. Everything downstream of it — `nephrotox_grade_modeling`, the bridge concordance verdicts,
`confound_stats.py` — inherits that status.

### Changes the biggest single thing in the data: §E in-vitro → clinical grade mapping

> *"Do not map in-vitro fold-change bins to clinical severity grades unless clinically validated.
> Call it experimental response severity."*

One `nephrotox_grade` 0–3 scale currently spans all four evidence lanes:

| lane | rows | grade distribution 0/1/2/3 |
|---|---:|---|
| `human_clinical` | 42 | 21 / 10 / 6 / 5 |
| `human_invitro` | 67 | 33 / 12 / 17 / 5 |
| `animal_invivo` | 56 | 6 / 15 / 25 / 10 |
| `animal_invitro` | 81 | 37 / 21 / 12 / 11 |

**148 of 246 rows (60%) are in-vitro carrying a scale shared with clinical rows.** That is the
prohibited mapping, and it is the largest rules conflict in this endpoint. It is not a bug I can
fix: splitting the scale changes biological meaning and is German's decision. **Flagged, untouched.**

### Changes the open MSR066 question — a second, independent disqualification

§E defines a clean clinical negative as requiring **all** of: exact sequence, human exposure,
adequate dose and duration, explicit monitoring, explicit outcome, traceable denominator. I tested
`MSR066` — our only `confirmed_negative` — against all seven:

```
PASS  exact sequence        PASS  explicit monitoring
PASS  human exposure        PASS  explicit outcome
FAIL  adequate dose           -> dose_or_conc_value = TBD
PASS  adequate duration     FAIL  traceable denominator
                            -> 5/7
```

This matters because it is **mechanical, not scientific**. My earlier argument against `MSR066` —
that the source calls the week-32 eGFR change an *exploratory* end point with no hypothesis testing
— required reading and interpreting the paper. This one does not: the row has **no dose**. §E
disqualifies it on its face. German still rules; he now has two independent routes to the same place.

§E also names the pattern I had reported independently as "renal-indication confounding":
**"Therapeutic correction is not toxicity."** My four-row finding (lumasiran, nedosiran, cemdisiran,
teprasiran — all grade 0, classified four different ways) is an instance of a rule that already
existed. I should have been reading German's framework, not re-deriving it.

### Changes the schema target: §C — 24 of 35 required fields absent

Measured against `data/oligos.csv` (65 rows) and `data/measurements.csv` (246 rows):

| group | present | equivalent under another name | **absent** |
|---|---:|---:|---:|
| Identity / chemistry | 1 | 0 | **7** |
| Characterization | 1 | 1 | **1** |
| Exposure / system | 1 | 4 | **7** |
| Outcome / adjudication | 0 | 3 | **7** |
| Grouping | 0 | 0 | **2** |
| **total (35)** | **3** | **8** | **24** |

The three that bite:

1. **All seven position-chemistry fields are absent** — `strand_role`, `duplex_partner_id`,
   `backbone_by_linkage`, `sugar_mod_by_position`, `base_mod_by_position`, `terminal_modifications`,
   `gap_length_nt`. What kidney has instead is molecule-level flags (`backbone_chemistry`,
   `sugar_modifications`, `gapmer_design`, `conjugate`, `ps_count`). §C permits those **only as
   secondary derived variables, never as the primary encoding**. Kidney uses them as the primary
   encoding. Direct violation.
   *Worth noting:* the sequences I recovered on 2026-10-02 are already in the per-position form §C
   wants — case-encoded wings and gaps, e.g. `GCTCCttccactgatCCTGC` with 5-10-5 2′-MOE wings, and
   the Moisan set with LNA wings and `mC` methyl positions. **The data exists and has no column to
   live in.** That is a schema gap, not an evidence gap, and it waits on the Tier 0 crosswalk.
2. **Both grouping fields absent** — `sequence_family_group`, `paper_group`. §C says these "must
   exist from the start" and §G requires them for grouped splits. Nothing in kidney can currently
   support a leave-one-paper-out split.
3. **`author_interpretation` and `curator_label` are absent** — §E requires the author's result and
   the curator's label to be kept separate. Kidney collapses both into `nephrotox_grade`. This is
   the same defect as §A above, seen from the schema side.

### Changes how missingness is written: §F

`purity_pct` and `purity_method` currently hold the literal string **`TBD`** on all 65 oligos. §F
requires **`NOT_REPORTED`**, and is explicit that it "is the correct value, not a failure state".
`TBD` says *we have not got to it yet*; `NOT_REPORTED` says *the source does not report it*. For
kidney the second is true and verified — I searched both source patents for purity/HPLC/UPLC/LC-MS
language and neither reports any.

**No Characterization Gap Register exists in `toxicity/kidney`.** §F requires the value *and* the
register. I have not renamed the values, because changing 130 cells in `data/oligos.csv` is a write
to validated data and the standing rule gates that. **Proposed, not done.**

German's calibration — zero of 45 thrombo records with a usable purity value — matches kidney
exactly at 0 of 65. This is a corpus property, not a kidney failure. Plan for disclosure.

### Confirms work already done: §E "unreported is not negative"

`negative_eligibility` already implements this: five tiers, machine-derived, with
`nephrotox_grade_modeling` left blank where a row is not eligible, so unsupported zeros become
missing rather than zero. 20 rows are gated out. This rule arrived after the work and agrees with it.

### No change: §D, §G, §H, §I

- **§D** — human clinical / human lab / animal are already separate lanes via `subject_class`, and
  animal evidence sits in appendix tabs. Kidney does not use GOLD/SILVER/BRONZE tiers at all.
- **§G** — **no model exists in `toxicity/kidney`**; nothing trains, splits or reports an AUC. The
  leakage rules bind the moment one does, and §C's two missing grouping fields are the blocker.
- **§H** — kidney is not named in the release table. One clarification to avoid a
  misreading: `scripts/release_check.py` prints `RELEASE CHECKS PASSED`. That is an **internal
  integrity gate** — schema, hashes, kidney-only isolation, tab order. It is **not** a dataset
  freeze and must not be read as one. German grants freezes; this script does not.
- **§I** — **none of the named corrections touch kidney.** Searched every `.csv`, `.md` and `.py`
  for Peacock, Goodchild, Hornung, Herzner, Riera-Tur, Fucini and Lenert: **zero files each.**
  Nothing to carry.

---

## 2. Grain declaration (§B) — flagged, nothing re-grained

**Kidney is not one-row-per-oligo.** Measured: 246 rows across 65 oligos, 3.8 rows per oligo, in the
two-table architecture §B asks for — `data/oligos.csv` as the canonical identity/chemistry table,
`data/measurements.csv` as the experimental-observation table, linked on `oligo_id`.

Tested for condition collapse on the key
`oligo × species × system × dose × unit × duration × delivery × endpoint`:
**246 distinct keys for 246 rows — zero duplicates.**

> **CORRECTION, same day.** The sentence that followed this — "zero collapsed rows. No row stands
> for several doses or timepoints" — **was wrong, and the test behind it was the wrong test.**
> Key-uniqueness proves no two rows duplicate a condition; it says nothing about whether one row
> summarises many. A drug-level summary row has a unique key too. Re-measured properly:
>
> - **37 of 65 oligos (57%) have exactly one row standing for their entire evidence.**
> - **98 of 246 rows cannot be resolved to a single dose, a single exposure time and a numeric value.**
> - Kidney is **two regimes**: the patent panels are **129/150 (86%) resolvable** and fully crossed;
>   everything else is **19/96 (20%)**.
> - 11 rows carry `species = multi_species`, pooling several species into one row; 21 carry an
>   ordinal `in_vivo_nephrotoxicity_composite` bin rather than a measured quantity.
>
> So the honest answer to §B is: **the patent-derived half is at condition grain; the rest is at
> drug-summary grain.** Still not one-row-per-oligo overall, and still nothing re-grained — but the
> clean bill of health below was unearned. Detail in `ROCKSTEADY_TO_BEEBOP_CRANK_2026-10-03.md`.

**But the grain is incomplete against §B's full unit**, and I would rather say so than claim
compliance:

| §B axis | state in kidney |
|---|---|
| oligo | present |
| chemistry | **molecule-level only** — no position encoding (§C above) |
| strand state | **absent** — no `strand_role`, no `duplex_partner_id` |
| dose | present, **39/246 rows (16%) have none** |
| time | present, **20/246 (8%) have none** |
| donor / cell system | system present; **donor axis entirely absent** — no `donor_id`, `donor_class`, `cell_subset`, `sample_state` |
| delivery condition | `delivery_method` present; no `formulation` or `delivery_agent` |
| endpoint | present, 246/246 |

So: **experiment-condition grain on the dose × time × system × endpoint axes, with the donor and
strand axes missing and chemistry at the wrong level.** Re-graining is not the issue here —
the rows are already per-condition. The issue is missing axes, which is a schema question for the
Tier 0 crosswalk, not a re-graining question. **I have re-grained nothing.**

**GSRS:** kidney holds no GSRS data — searched, zero hits. The raw-and-unparsed staging rule has
nothing to bind on here.

---

## 3. Delegated row — status

> *Kidney: Correct the false "blocked" assertion at `SOURCES.md:12` and `SOURCE_REGISTER.md` §2 …
> Do not act on the audit's Directive 5 … MSR066 awaits German.*

**a. False "blocked" assertion — corrected, and the correction paid for itself immediately.**

Crank is right, and the mechanism is exactly as described. Measured on one URL:

| user agent | result |
|---|---|
| default `curl` | **HTTP 404, 420 bytes** — an apology page that reads like a block |
| browser | **HTTP 200, 7,558,885 bytes** — the document |

`accessdata.fda.gov` is **user-agent gated, never blocked.** Corrected at `SOURCES.md:12` and in
two places in `SOURCE_REGISTER.md`.

I then re-tested the rest of that same sentence, because a line that is wrong in one clause may be
wrong in others. It is not: **NEJM, Circulation/AHA, ScienceDirect and `academic.oup.com` return
403 under both the default and a browser agent.** Those are genuine blocks and the claim stands for
them. The correction is therefore narrow and specific rather than a blanket rewrite.

**Acquired under the standing rule (acquisition proceeds now):** four FDA Pharmacology/Toxicology
reviews, 22.9 MB, previously recorded as requiring hand-delivery —

| document | pages | renal content (first 40 pp) |
|---|---:|---|
| inotersen, NDA 211172 | 134 | kidney ×23, glomerular ×6, basophilic granulation ×5, creatinine ×4 |
| golodirsen, NDA 211970 | 114 | kidney ×34, renal ×29, basophilic granulation ×5, tubular ×22 |
| casimersen, NDA 213026 | 76 | kidney ×26, renal ×15, tubular ×28 |
| viltolarsen, NDA 212154 | 49 | kidney ×52, proximal tubule ×9, basophilic granulation ×6 |

All four are authoritative nonclinical renal toxicology for oligos already on our roster, and all
four carry **basophilic granulation** — the classic ASO proximal-tubule finding — plus NOAELs.
Staged in `research_staging/papers/` with URL, date, HTTP code, byte size and SHA-256 in
`logs/acquisition_manifest.json`. **Not ingested.**

A licensing note that differs from the rest of that folder: these are **US federal agency work
products and therefore public domain**, consistent with Beebop's item 12 (the public-domain
reading reaches US federal agencies only). They are excluded from git for size, not for rights.
`217388` (eplontersen) and `219019` (nedosiran) were not located under the probed paths and remain
open.

**b. Directive 5 — verified, and not acted on.** Crank's figures are exactly right:

```
staged rows in sequences_recovered_2026-10-02.csv : 10
oligos whose sequence is TBD                      : 10
INTERSECTION                                      : 6   <- not 10
staged ids that are NOT gaps                      : OLG002, OLG005, OLG006, OLG032
sequences now                                     : 55/65
if every staged row were promoted                 : 61/65  <- not 65/65
```

The four non-gap rows are exactly what my staging file labels them: two per-position chemistry
upgrades for oligos that already have sequences (`OLG006` mipomersen, `OLG005` volanesorsen), one
notation discrepancy for German (`OLG032` pelacarsen, U/T mixing), and one independent confirmation
(`OLG002` SPC5001). **An audit that counted ten staged rows as ten gap fills misread the file's own
`status` column.** My Revision A reported 61 and so does this check; the two agree. Nothing promoted.

Residual after a full promotion would be 4: `OLG014`/`OLG015` (Sandelius 2020, SAGE 403 on all
routes) and `OLG030`/`OLG031`, which are **class-level aggregates and not molecules at all** — they
can never carry a sequence and distort any coverage denominator that includes them. Coverage is
better stated as **61/63 molecules** than 61/65 roster entries; both are true, and they answer
different questions.

**c. MSR066 — unchanged, awaiting German.** Label untouched. §E now supplies a second, mechanical
disqualification (§1 above) alongside the source-based one. German rules.

---

## 4. Every figure checked

| Figure as given | Source | My measurement | Verdict |
|---|---|---|---|
| accessdata: 420-byte apology vs 2,181,318-byte PDF | Crank | 420 B apology confirmed; browser PDF **7,558,885 B** on NDA 211172 | **mechanism confirmed**, my byte count differs — presumably a different document |
| Directive 5 id-set intersection = 6 | Crank | **6** | confirmed |
| Promotion reaches 61/65, not 65/65 | Crank | **61/65** | confirmed |
| Kidney has no control column | Beebop item 9 | no `control_role`; only `effect_vs_control`, which is a comparator note, not a control-arm designation | confirmed |
| Canonical 246-row `measurements.csv` exists only on this branch | Crank | 246 rows present here; cross-branch state not checked from this session | partially verified, not disputed |
| Kidney built one-row-per-oligo | implied by the all-endpoints flag | **false for kidney** — 3.8 rows/oligo, 246 unique condition keys | **does not apply here** |

---

## 5. Open for others

**German** — unchanged from my 2026-10-02 report, plus three raised by the rules themselves:
1. `MSR066`, now failing §E's clean-negative test on dose and denominator as well.
2. **The single 0–3 grade spanning clinical and in-vitro lanes** (§E), 148 of 246 rows affected.
3. **Ratification or voiding of the entire agent-assigned `nephrotox_grade` column** (§A).
4. The renal-indication rule, which §E already names as "therapeutic correction is not toxicity".

**Tier 0 crosswalk** — the 24 absent §C fields, above all the seven position-chemistry fields and
the two grouping fields. Kidney has per-position chemistry in hand for six constructs with nowhere
to put it.

**Oscar** — whether `purity_pct`/`purity_method` may be rewritten `TBD` → `NOT_REPORTED` (130 cells
in validated data, hence gated), and whether the Characterization Gap Register is mine to create or
belongs in the crosswalk.

**Not mine, flagged rather than assumed:** `217388` and `219019` FDA reviews remain unlocated; the
cross-branch stale-`measurements.csv` problem is listed under Cross-branch, not under Kidney, and I
have not touched other branches.

---

## 6. Expected release-manifest drift — declared, not repaired

Correcting `SOURCE_REGISTER.md` drifted it away from the hash bound in `RELEASE_MANIFEST.json`
(`release_id kidney-224e9a2f7916`). `scripts/release_check.py` now reports:

```
RELEASE BLOCKED — 1 hard failure(s)
  - every file bound by the manifest matches its hash (1 drifted)
```

**This is the gate working, not a fault.** Checked file by file: all six data files — `oligos.csv`,
`measurements.csv`, the merged view, the bridge, the clinical register and the workbook — hash
**OK**. No data file moved.

Four bound **documents** drifted, each for a stated reason, all of them description:

| file | why |
|---|---|
| `SOURCE_REGISTER.md` | the false `accessdata.fda.gov` "blocked" entry corrected |
| `SOURCE_REGISTER.pdf` | re-rendered so the PDF stops publishing the corrected-away claim |
| `STATUS.md` | §3a purity item partly overtaken — FDA reviews do report per-lot purity |
| `schema.md` | `purity_pct` note updated for the same reason |

**I did not regenerate the manifest.** Doing so mints a new `release_id`, which is release
mechanics and gated. The correct state is exactly what the gate now reports: the released artefacts
no longer match their corrected sources, so **this release is not current** and a regeneration is
owed once release is ungated. Anyone reading `kidney-224e9a2f7916` should treat the source-access
claims in it as superseded by the 2026-10-03 correction.

---

RULES READ AND APPLIED — ACQUISITION AND DESCRIPTION DONE, INGESTION AND PROMOTION HELD
