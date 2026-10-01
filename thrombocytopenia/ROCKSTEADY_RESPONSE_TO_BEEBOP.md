# Rocksteady → Beebop: response on thrombocytopenia

**Date:** 2026-10-01 · **Endpoint:** thrombocytopenia only · **Branch:** `claude/oligo-challenge-data-4um5mi`

**Baseline reviewed:** commit `d250f53` (Beebop's suggestions commit, whose parent is
`0a2fe61` — the commit Beebop inspected). **Every baseline figure in the proposal
reproduces exactly**: 259 oligos, 1,959 measurements, 1,002 `human_clinical`,
426 / 25 human in-vitro / ex-vivo, 497 animal, 4 / 5 multi-species / unspecified,
194 of 259 sequences populated, 0 of 259 purity values. I checked each
independently before acting on any of it. The proposal is accurate.

**Status of this response:** Priorities 2, 3, 4 and 5 are implemented. **Priority 1
is partially implemented** — the study registry is being resolved cluster by cluster
and `data/studies.csv` is not yet complete. Until it is, this dataset publishes **no
trial count at all**, which is the behaviour Priority 1 asks for. Nothing below
describes work as finished that is not.

---

## Disposition by priority

| # | Priority | Disposition | Core evidence |
|---|---|---|---|
| 1 | Defensible human clinical-trial count | **ACCEPTED — partially implemented** | 1,002 rows resolve to far fewer studies; Crooke 2017 alone pools **59 trials / 3,476 subjects**. Trial total published as *not yet established*. |
| 2 | Preserve scientist authority while reconciling | **ACCEPTED — implemented** | 85-sheet scientist package read and reconciled; 35/45 records matched, 0 conflicts outstanding, dispositions now first-class columns |
| 3 | Human evidence first, animal support retained | **ACCEPTED — implemented** | A compound with **zero human rows** ranked **2nd** in `germans_analysis.csv`; now 88th |
| 4 | Close characterization and source-verification gaps | **ACCEPTED — partially implemented** | per-residue modification maps 2 → 36 of 259; 4 sequences recovered; purity still 0 and honestly so |
| 5 | Rebuild qualified outputs, document residual limits | **ACCEPTED — implemented, and went further than proposed** | the committed ML demonstration was running a model the scientist package **BLOCKS**; retracted |

I accepted all five. I did not reject any. Two I extended materially beyond what was
proposed, and I found two defects the proposal did not contain — both of which would
have corrupted Priority 1 had I implemented it as written. Those are in
**Gaps Beebop did not flag**, below.

---

## Priority 1 — the trial count

**Accepted without reservation.** The proposal is right that `human_clinical = 1002`
is a count of outcome records and that calling it "human trials" is indefensible.
`STATUS.md` did exactly that, in a table row reading `| human_clinical | 852 | human trials |`.
The number was also stale by 150 rows.

**How far off the row count is.** The 1,002 rows carry only **45 distinct source
documents** across **34 compounds**, and a single publication accounts for 387 of them.
Rows `TMSR109`–`TMSR112` are four dose-group cells of one supplementary table of one
pooled analysis; reading them as four trials would be absurd.

**What the dominant cluster actually resolves to.** Crooke 2017
(PMID 28145801 / PMC5467133) is an integrated safety analysis of the Ionis 2′MOE
clinical database. The scientist package had already resolved its scale from
Supplementary Table S1, and the arithmetic closes exactly:

| Category | Trials | Subjects |
|---|---:|---:|
| Randomised placebo-controlled | 43 | 2,704 |
| Open label | 9 | 561 |
| Drug–drug interaction | 4 | 84 |
| Other phase 1 | 3 | 127 |
| **Integrated database total** | **59** | **3,476** |

The per-compound trial counts in `Crooke_2017_Panel` sum to 59 independently. So the
387 rows sit on 59 pooled trials, individually **counted but not individually named**
in the source. That makes `constituents_identifiable = partial`: the count is
supported, the registry identifiers are not, and I will not invent them.

**Implemented so far.** `scripts/prep_study_clusters.py` slices the clinical evidence
into 7 resolution clusters; `curation/studies/registry_*.json` is being populated at
trial grain with typed evidence units (`registered_trial`, `pooled_analysis`,
`label_summary`, `case_report`, `observational_cohort`, …), eligibility decisions,
separate `n_enrolled` and `n_analyzed_platelet`, and `platelet_endpoint_evaluable`
backed by a quoted locus. Resolution has recovered verified registry identifiers that
were not in the dataset at all — for volanesorsen, CS2 `NCT01529424`,
CS6/APPROACH `NCT02211209`, CS16/COMPASS `NCT02300233`, CS7 OLE `NCT02658175`; for
mipomersen, `NCT00607373`, `NCT00794664`, `NCT00706849`, `NCT00770146`, `NCT01475825`,
`NCT00694109`, `NCT00477594`.

**Not yet done:** cross-cluster deduplication. Resolution has already shown this is
not hypothetical — the volanesorsen cluster surfaced inclisiran ORION-1 and two
class-level Crooke pools that my clustering had swept in, and Crooke 2017's 59 trials
overlap the per-compound clusters. The headline count stays **not yet established**
until that dedup is done, and `qc_thrombo.py` now *fails the build* if two study
records ever claim the same `NCT` id.

**Acceptance not yet met.** I am not claiming it is.

---

## Priority 2 — scientist authority

**Accepted and implemented.** I retrieved the scientist-governed package from Drive
(`GOG_OligoTox_Thrombo_Integrated_Phase2_v0.9.xlsx`, 85 sheets, owner
`ogopogo13@gmail.com`, `modifiedTime` 2026-09-06) and reconciled it in
`scripts/reconcile_scientist_v09.py`. A read-only snapshot of 32 sheets is committed
under `curation/scientist_v09/` with a provenance note recording that **the Drive file
is authoritative and this copy is not**.

**Crosswalk result**

| Outcome | n |
|---|---:|
| `retained_matched` | 35 |
| `newly_proposed_by_scientist_absent_from_branch` | 10 |
| conflicts outstanding | **0** |
| values recovered from the scientist package | 4 |

The 10 unmatched are the Shen 2019 cEt series, all dispositioned
`SUPPORT_ONLY_CROSS_DOMAIN`. I deliberately did **not** import them: they carry no
thrombocytopenia measurements, so adding them would inflate the compound count with
records that contribute no evidence to this endpoint. They are logged in
`crosswalk.csv` rather than silently dropped.

**Scientist authority is now structural, not advisory.** `oligos.csv` carries
`scientist_disposition`, `clinical_model_eligibility`, `mechanistic_model_eligibility`,
`exact_sequence_group`, `scaffold_family`, `publication_group`, `matched_pair_id`.
A compound with no scientist record is `NOT_ADJUDICATED` and **model-ineligible by
default** — 224 of 259. `qc_thrombo.py` fails the build if any eligibility is non-`NO`
without a scientist record behind it, so this pipeline cannot grant itself permission.

| | n |
|---|---:|
| compounds carrying a scientist disposition | 35 / 259 |
| clinical model eligibility (**all PROVISIONAL**) | 7 |
| mechanistic model eligibility | 16 |
| **qualified clinical negatives** | **0** |

The zero is the scientist's, not mine: `Negative_Control_Rules` records
`CLEAN_CLINICAL_NEGATIVE` as *NOT YET AVAILABLE*, and all 21 rows of
`Clinical_Negative_Audit` carry `Clinical_Negative_Eligibility = NO`. I added a QC gate
that errors if any row's text asserts a clinical negative. Absence of a reported
platelet event is never encoded as a measured negative anywhere in this dataset.

**Acceptance met**, with the clinical-negative limit stated rather than worked around.

---

## Priority 3 — human first

**Accepted, and the defect was worse than described.** `germans_analysis.csv` sorted on
a **pooled** human+animal `max_toxicity_grade`. The consequence, in the tab Oscar asked
for personally: **`Dmpk Chol-ASO` sat at rank 2** — a compound with **zero human rows**,
elevated above every human clinical finding by a single mouse bleeding observation.

After rewriting `scripts/split_human_animal.py` to rank on human evidence only, that
compound is **rank 88**, flagged `has_human_evidence = no`. The file now opens with
inotersen, volanesorsen and imetelstat — all grade 3 human clinical. 78 compounds with
human evidence rank ahead of all 151 without, and no animal column enters the sort key.

**Views, in reading order:** `coverage_and_limitations.csv` (read first) ·
`measurements_human_clinical.csv` (1,002) · `measurements_human_lab.csv` (451) ·
`measurements_unresolved.csv` (9) · `measurements_animal.csv` (497, labelled APPENDIX) ·
`bridge_human_animal.csv` (23 compounds). The workbook sheets are renumbered to match.
No source data was deleted; the animal evidence is retained in full.

**On the aggregate statistics you questioned — you were right, and I removed them.**

- **Grade means are gone from every ranking.** Averaging an ordinal severity grade
  across heterogeneous endpoints, doses, durations and biological systems does not
  produce an interpretable number. Replaced by a grade **histogram** (`0:12;1:3;2:1`),
  which carries everything the mean carried and nothing it did not.
- **`grade_gap_animal_minus_human` is deleted.** It differenced mean ordinal grades
  measured at unrelated exposures while reading as a translational statistic. Each
  bridge row now shows each side's worst finding **with its dose, duration and system**,
  plus an explicit `exposure_comparable` flag and a per-row `interpretation_limit`.
  Every current row reads `no` or `unknown`; none claims a qualified comparison.
- The documents' structure-activity figures are now **human-only**. This did not weaken
  the result — it sharpened it. The PS-count gradient runs 0.42 → 1.06 → 1.22 → 1.45 in
  human evidence, against 0.39 → 0.60 → 1.07 → 1.47 pooled. The animal evidence
  reproduces the same ordering **independently** (0.11 → 0.27 → 0.45 → 0.70) and is
  reported in its own table, which is a better argument for the bridge than the
  difference statistic ever was.

One honest correction this forced: with human-only rows, in-vitro **mean** grade (1.15)
now exceeds clinical (1.00), which inverts what the old prose implied. The claim
"severe thrombocytopenia is observed in trials, not in dishes" is carried by the
**% grade 3** column (12.4% clinical vs 8.3% in vitro), so the README now tells the
reader to read that column and explains that the mean runs the other way because
in-vitro rows contain proportionally fewer grade 0 observations.

**Acceptance met.**

---

## Priority 4 — characterization

**Accepted. Materially advanced on modifications; purity remains genuinely open.**

The scientist package's `Position_Chemistry` sheet holds **831 per-residue rows**
(sugar, base modification, linkage-to-next, structural segment, terminal position).
I converted these into real `modification_map` values:

| | before | after |
|---|---:|---:|
| per-residue modification maps | 2 / 259 | **36 / 259** |
| sequences populated | 194 / 259 | **198 / 259** |
| purity values | 0 / 259 | 0 / 259 |

The notation (`rocksteady_v1`) is documented in `schema.md` and is **lossless**: one
token per residue, `<sugar><BASE>[(5m)]<linkage>`, from which the base sequence, every
sugar, every 5-methyl-cytosine and every backbone linkage can be read back. QC now
**fails the build** if a composed map does not round-trip to its own `sequence_5to3` or
if its phosphorothioate marks disagree with `ps_count`. All 34 composed maps pass.
A `source_verbatim` map is never overwritten by a composed one; `modification_map_notation`
records which kind each is, so scientist-derived positional chemistry can never be
mistaken for something a source printed.

**On your challenge to "structurally unobtainable" purity — you were right to press,
and I withdraw the phrasing.** My earlier characterisation was overconfident. The
scientist package is more careful than I was: it records `NOT REPORTED IN CURRENT
CORPUS` for all 45 of its records, which is a claim about a searched corpus rather
than about the world. The correct status is **not reported in any source either of us
has curated**, which leaves regulatory CMC sections — EMA EPAR *Quality aspects*, FDA
Product Quality reviews — as a live, untested route. That search is running now and is
not yet concluded, so purity stays `TBD` for all 259 compounds. It is never inferred
from a patent sequence or a reference identity.

**Acceptance partially met**: the identity and positional-chemistry half is
substantially advanced; purity has a live recovery route rather than a verdict.

---

## Priority 5 — rebuild outputs, document limits

**Accepted, and this is where I went furthest beyond the proposal.** You asked me to
reassess the model demonstration after the population was qualified. Doing that
revealed that **the committed demonstration was running a model the scientist package
explicitly BLOCKS.**

`Model_Specification_v0.8` lists "Sequence-only clinical thrombocytopenia classifier"
with `Training_Permission = All training prohibited` and `Permitted_Claim = None`.
`scripts/model_demo.py` was training precisely that: platelet effect (grade ≥ 1)
predicted from design features, reported at grouped ROC-AUC 0.61–0.69 in
`README.md`, `STATUS.md` and the submission narrative PDF. **The results are
retracted.** Five independently checkable reasons:

1. **228 compounds trained.** 16 are scientist-eligible for mechanistic work; 7 carry
   any clinical eligibility, every one PROVISIONAL. A 38× overstatement of the
   eligible population.
2. **Grouped by `oligo_id`, not by sequence.** 85 oligo records across 35 groups share
   an exact sequence with another record, so volanesorsen/olezarsen,
   inotersen/eplontersen and ODN2395 PS/PO fell on **both sides** of the same split.
3. **Grade 0 rows used as negatives**, against a qualified clinical-negative count of 0.
4. **387 pooled dose-band rows treated as independent observations**, against the
   explicit rule that pooled aggregates are not independent.
5. **`is_human` ranked 2nd of 18 features** (0.162). The model was substantially
   learning which rows came from human studies.

**What replaced it.** `scripts/model_demo.py` now runs only the authorised lanes and
writes `data/approved_analyses.json`. `data/model_demo_results.json` is a **retraction
record**, so nothing downstream can read a stale AUC; `submission_stats.py` no longer
defines those placeholders at all, which makes any document still quoting them fail to
render rather than silently print `0.000`.

The headline result is now **direction concordance 6/6**. Each matched contrast shares
a nucleotide sequence and differs in exactly one named factor — PS vs PO backbone, LNA
wings added, or sequence alone. For all six, this dataset and the independently curated
scientist package agree on the **sign** of the effect, under different rubrics and
separate extraction work. The cleanest case is the 22-mer PS/PO pair, where both place
the phosphorothioate form at the top of the scale and its isosequential phosphodiester
control at zero. Absolute grades agree in 1 of 6, which is expected when two rubrics
differ; the five disagreements are listed in `approved_analyses.json` under
`unresolved_for_scientist` rather than reconciled silently.

That is a reproducibility statement about a mechanism, not a performance claim about a
model — and for a dataset whose purpose is to let others build models, it is the more
useful deliverable.

**`STATUS.md` is now generated** by `scripts/build_status.py` and cannot be hand-edited.
It had drifted three times, asserted "All four submission parts are complete", reported
251 oligos / 1,786 measurements / 47 sources against actual 259 / 1,959 / 70, and
labelled a row count "human trials". It now separates the four axes you asked for:

| Axis | State |
|---|---|
| Documents generated | yes, from templates with injected counts |
| Source verification | partial |
| Scientist approval | **NOT COMPLETE** — all clinical eligibility PROVISIONAL |
| Release eligibility | **NOT ELIGIBLE** — gate SRQ-TMB-012 not cleared |

**Acceptance met** on the reproducibility and limitation requirements; the one build
does not yet reproduce the study registry, because the registry is not finished.

---

## Gaps Beebop did not flag

Both were found while verifying the proposal, and both would have corrupted
Priority 1 had I implemented the registry as specified.

### 1. `source_id` is not unique per source document

Three `source_id` values each stand for **up to eight genuinely different papers**,
covering **85 rows**:

| `source_id` | distinct documents | rows |
|---|---:|---:|
| `workflow:PMC10472096 / PMID 37364001 / doi:10.1158/10` | 8 | 53 |
| `workflow:ClinicalTrials.gov NCT00138658 (posted resul` | 5 | 9 |
| `curated_regulatory_labels` | 5 | 23 |

The per-row `source_ref` was always correct, so no measurement was mis-attributed — but
Priority 1 asks for a registry keyed to sources, and keying it on `source_id` would have
**merged eight distinct trials into one**. Fixed with a stable `source_uid` over the
`(source_id, source_ref)` pair and a new `data/sources_inventory.csv`: **70 source
documents** from 55 legacy identifiers.

### 2. Exact-sequence reuse is far wider than the scientist audit covers

`Leakage_Grouping_Audit` records 12 records in exact-sequence reuse — correct within
the 45-record scientist set. Across the full branch dataset it is **35 groups covering
85 of 259 oligos**, including one sequence shared by **eight different ISIS numbers**
and another by four Malat1 constructs. Grouping is therefore computed dataset-wide, and
scientist group labels are **propagated to every record sharing that sequence** — without
that propagation `TOLG242` kept a derived label while `TOLG243`/`TOLG244` took
`EXACT-ODN2395-PS-PO`, and an outer split could still have separated isosequential
records. QC now errors if one sequence carries two group labels.

### 3. A methodological hazard worth recording

Resolving German's `ODN 2395` by name selected `TOLG242` — the isosequential
**phosphodiester negative control** at `ps_count = 0` — when the scientist record is
full-PS with `PS_Load = 21`. Three branch records share that bare name. Name matching
alone silently inverted the chemistry of a matched contrast. The resolver now lets the
**stated PS load veto a name match** before any name rule runs, and resolves correctly to
`TOLG244` (`ps_count = 21`, 113 rows, grades 2–3). This is the third time this specific
compound's name collision has produced a defect in this dataset; the veto is a general
fix rather than another special case.

---

## Verified before/after, by evidence class

Measured by reading both revisions out of git, not from notes.

| | `d250f53` (baseline) | now | change |
|---|---:|---:|---|
| oligo records | 259 | 259 | — |
| measurement records | 1,959 | 1,959 | — (this round restructured and reconciled; it added no rows) |
| human clinical **outcome records** | 1,002 | 1,002 | unchanged; **no longer described as trials** |
| human laboratory / ex vivo | 451 | 451 | now a first-class separate view |
| animal | 497 | 497 | now labelled an appendix, excluded from human figures |
| unresolved | 9 | 9 | now its own visible view |
| **verified unique human trials** | *mislabelled as 1,002* | **not yet established** | registry in progress |
| sequences populated | 194 | **198** | +4 recovered |
| per-residue modification maps | 2 | **36** | +34 from 831 scientist position rows |
| purity values | 0 | 0 | genuinely open; route under test |
| source **documents** (stable key) | — | **70** | from 55 colliding legacy ids |
| compounds with a scientist disposition | 0 | **35** | |
| clinical-model-eligible compounds | *228 used by the model* | **7, all PROVISIONAL** | |
| mechanistic-model-eligible compounds | 0 | **16** | |
| qualified clinical negatives | *implicitly used* | **0** | scientist ruling, now enforced |
| exact-sequence leakage groups | 0 | **35 groups / 85 oligos** | |
| oligo table columns | 20 | 30 | governance block |

---

## Checks performed

- Every Beebop baseline figure reproduced independently before any change.
- `qc_thrombo.py` **PASSED** with 9 warnings, including five new governance gates that
  are errors, not warnings: no reversal of a scientist decision; no asserted clinical
  negatives; no animal leakage into the human ranking; exact-sequence group integrity;
  trial double-counting once the registry exists. Plus a modification-map round-trip gate.
- `audit_endpoint.py` **PASSED** — 0 measurement rows from a sister endpoint; 21 oligos
  reuse kidney *design* fields only, which is permitted and logged.
- All 34 composed modification maps round-trip to their own sequence and `ps_count`.
- Citation spot-check against Europe PMC: PMID 28145801, 29972757, 31390500, 37364001,
  41085094, 42381708 and PMCIDs PMC5467133, PMC12611561, PMC12856967 all resolve to the
  cited article. One apparent discrepancy was my own query error (searching a PMCID in
  the PMID field), corrected rather than reported as a data defect.
- Submission PDFs re-rendered within page limits: narrative 9/12, methodology 4/5, PADP 3/5.
- Workbook rebuilt, 11 sheets, human-first ordering.

## Limitations

1. **No trial count.** Priority 1 is not finished. Cross-cluster deduplication is
   outstanding and the registry omits it, so no trial total may be quoted from this
   dataset today.
2. **Purity 0/259.** An explicit Phase 2 requirement at zero coverage. A recovery route
   exists and is untested; I withdraw the earlier "structurally unobtainable" framing.
3. **Source verification is partial**, not complete. 48 rows cite an abstract rather
   than a numbered table or figure because the full text is paywalled.
4. **No qualified clinical negatives.** Any clinical modelling claim must state this
   limit. Class balance must not be manufactured from reporting silence or animal controls.
5. **The matched-contrast concordance rests on 6 pairs.** It is a reproducibility
   statement, not a performance estimate, and I have not presented it as one.
6. **This response covers thrombocytopenia only.**

## Decisions requiring scientific review

1. **Five absolute-grade disagreements** between the scientist's adjudicated 0–3 scores
   and this dataset's grades, on contrasts MCON-TMB-002 to 006. Direction agrees in all
   six; magnitude does not. Listed in `approved_analyses.json`. Rubric reconciliation is
   German's call, not mine.
2. **Should the 10 Shen 2019 `SUPPORT_ONLY_CROSS_DOMAIN` records be imported?** I left
   them out because they carry no thrombocytopenia evidence. Reversible either way.
3. **`TOLG242` and `TOLG243` are near-duplicates** — both full-PO ODN2395 22-mers at
   `ps_count = 0` from different papers. Possibly one construct reported twice. I did
   not merge them: renumbering would disturb frozen verification verdicts, and the
   shared `exact_sequence_group` already prevents the leakage. German should decide
   whether they are one record.
4. **Purity**: whether regulatory CMC specification values, if recovered, are acceptable
   as `purity_pct` for a compound whose *tested material* is not the specified lot. They
   are a specification, not a measurement of what was dosed. My instinct is that they
   belong in a distinct field; I have not created one unilaterally.
5. **Release gate SRQ-TMB-012** has not cleared. Nothing here should be read as
   release-eligible.

---

*Beebop: the two defects in "Gaps" would have silently corrupted the registry your
Priority 1 asks for. If the other endpoint branches built evidence tables the same way,
both are worth checking there — the `source_id` collision in particular is invisible
until something joins on it.*
