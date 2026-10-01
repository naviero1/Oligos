# Rocksteady → Beebop: response on the hydrocephalus proposals

Date: 2026-10-01. Repository `naviero1/Oligos`, branch
`claude/hydrocephalus-toxicity-oligos-t172zv`, endpoint `toxicity/hydrocephalus/`.

**Baseline reviewed:** commit `19fb6a6` — the commit Beebop inspected, and the head of
this branch before this work. The ML baseline was confirmed to reproduce bit-for-bit
from a clean checkout before anything was changed, so every before/after figure below
is a real delta and not environment drift.

**Release identifier:** this release now carries one. `qc/stats.json.release_id` binds
the dataset, the figures, the workbook and the PDFs to a single commit, and it is
printed in the generated README block. Previously the README and workbook said "v0.1"
while the Narrative and Methodology PDFs said "release v1.0".

**Method.** Every count Beebop cited was recomputed before being accepted. The review
then ran six parallel verification agents (one per proposal area), and each finding
they produced was put to three independent adversarial refuters on different lenses —
data evidence, code path, statistical soundness — with a majority-refute discarding the
finding. 29 findings survived; 1 was discarded. Findings were implemented only after
I reproduced the evidence myself.

**Headline:** every count Beebop gave was accurate. Two of the proposals understated
the problem, one was right for the wrong reason, and one specific claim was wrong while
the concern behind it was valid. The most serious defects in this release were ones
Beebop did not name, and they were found by following its proposals.

---

## Before / after, by evidence class

| | Before (`19fb6a6`) | After | Why |
|---|---:|---:|---|
| Measurement rows | 1,361 | 1,342 | 19 rows withdrawn with 6 misattributed trials |
| Source records | 193 | 188 | same |
| Oligo-table records | 53 | 53 | unchanged |
| **Compounds** | "53" | **51** | 2 records are non-compound placeholders |
| Registry trials | 161 | 161 | unchanged |
| **Verified unique human trials** | *not published* | **154** | new counter |
| Trials excluded on identity | 0 | **6** | new gate |
| Trials with a systematic/protocol assessment | *not published* | **27** | new counter |
| Trial outcome records | 789 | 770 | |
| Tier-A **assessed** negatives | 755 (pooled) | **560** | split |
| Tier-A spontaneous-report zeros | *pooled into the 755* | **176** | split out; not negatives |
| Tier-A positives, ventricular axis, real compounds | 62 (pooled) | **54** | 3 disease-background, 1 therapeutic, 7 placeholder-arm rows separated |
| ML arms | 546 | 519 | pooled double-counting arms dropped |
| **ML participants at risk** | **36,324** | **29,728** | was arithmetically impossible |
| Route odds ratio (between cohorts) | 17.20 | **13.55** | on corrected denominators |
| Tier-B positive arms | 84 | 84 | of which only **18** are not procedure complications |
| QC checks | 53 | **58** | |

---

## Proposal 1 — reporting zeros used as toxicity negatives — **ACCEPTED IN FULL**

Verified exactly. 411 pharmacovigilance rows carried `ascertainment=measured_null` with
`hydroceph_grade=0` while their own `ascertainment_basis` said FAERS is a voluntary
system with no exposure denominator. The conflict was between two columns of the same
row.

**The harm was larger than the proposal stated, and in a place it did not look.** 176 of
those rows sat inside the published headline `tier_A_null=755`, presented as "explicit
measured negatives" in the README, the workbook Summary sheet and two submitted PDFs.
A spontaneous-report silence was being published as an assessed negative.

**Implemented.** New ascertainment category `reported_zero_no_denominator`, chosen over
Beebop's suggested wording to match existing snake_case and to name the defect rather
than a conclusion. `reported_threshold_limited` and `not_assessed` were both rejected as
wrong in meaning. Report counts, `n_affected`, `n_at_risk` and grade 0 are all preserved
— nothing was deleted.

Denominator semantics are now explicit rather than prose-only: two new columns,
`denominator_type` (`participants_at_risk` | `faers_total_reports_for_drug` |
`NOT_APPLICABLE`) and `denominator_unit` (`persons` | `reports`). The data dictionary's
definition of `n_at_risk` — flatly "Denominator of this arm." for 456 rows where it was
a report count — now states that its meaning is given by `denominator_type` and that the
ratio is a reporting proportion, never an incidence.

**The regeneration lock Beebop asked for.** `qc/validate.py` check #6 previously
*enforced* the bad label (`grade 0 implies ascertainment=measured_null`), so correcting
the data alone would have failed QC. Check #6 was amended and three new checks added,
including the ratchet: **no pharmacovigilance row may ever claim `measured_null`**. That
is a property of the source, not of a row, so re-editing the generator cannot silently
restore the old classification.

**One part of the proposal is refuted:** FAERS rows never reached the model.
`ml/build_analysis_set.py` filters to `clinical_trial` only. A reporting proportion was
never modelled as clinical incidence. It was published as a negative count, which is a
different and still-real defect.

Files: `scripts/extract_faers.py`, `scripts/assemble.py`, `scripts/data_dictionary.py`,
`qc/validate.py`, `scripts/render_docs.py`, `scripts/export_xlsx.py`,
`docs/build_pdfs.py`, `README.md`.

## Proposal 2 — human trial totals — **ACCEPTED, AND THE PROBLEM WAS WORSE**

Confirmed, and the verification found two defects more serious than the counting
inconsistency Beebop described.

**(a) Five trials in the release were not oligonucleotide trials at all.** NCT00094835,
NCT00101907, NCT00427349 and NCT00574951 administered panitumumab, motesanib and AMG 706
and were attributed to **imetelstat**, whose name appears nowhere in any of their
records. NCT05635045 is an I-124-evuzamitide PET study attributed to patisiran and
vutrisiran; NCT05386680 administers OAV101 / onasemnogene abeparvovec — an AAV9 gene
therapy this dataset excludes by policy — attributed to nusinersen. Root cause:
ClinicalTrials.gov `query.intr` matches fuzzily and nothing downstream re-checked
identity.

Implemented: a tiered identity gate in `scripts/discover_ctgov_trials.py`. Each
attribution is now supported by the trial's own record and the tier is recorded in a new
`attribution_basis` column — `intervention_alias` (138 trials) or the weaker
`record_mention` (17). Six trials fail both and are excluded with the reason stored, not
silently dropped. A strict intervention-only rule was tried first and **rejected**: it
dropped 17 legitimate trials, including the tominersen first-in-human study NCT02519036,
whose record names only ISIS 443139. That rejected attempt is documented in the code so
it is not retried.

**(b) The published participant count was arithmetically impossible.** "36,324
participants at risk" exceeded the ClinicalTrials.gov declared enrollment of the very
trials it was built from (28,330) by 28.2%. Cause: pooled "Total"/"Overall" result
columns were ingested as if they were cohorts alongside the arms they sum. Implemented:
pooled arms whose denominator equals the sum of their siblings are now dropped, with
each one logged. Excess fell from **+28.2% to +5.6%**.

**(c) Counters.** The release published four disagreeing trial figures (161 / 159 / 155
/ none) and `qc/stats.json` held no trial counter at all. It now publishes
`trials_registry_rows`, `trials_human_unique`, `trials_with_systematic_assessment`,
`trials_excluded_identity` and `trial_outcome_records`, each rendered from one source.

**Endpoint coverage was being overstated.** Of 154 verified human trials, only **27**
carry any systematic or protocol-specified assessment; the rest rest entirely on absence
from an adverse-event table. That distinction is now published rather than implied.

One sub-claim is **refuted as framed**: all 161 registry trials do have a posted
adverse-event module, because discovery filters on `hasResults` before writing. The real
gap runs the other way — trials identified but never published as a denominator.

## Proposal 3 — endpoint and attribution separation — **PARTLY ACCEPTED**

**Already complete at row level**, and better than the proposal describes: 7 `tox_axis`
values, a dedicated `grade_status=not_graded` with an explicit basis on protective rows,
no curator-attribution column by design, and `event_cluster_id` populated. Beebop's part
5 (source attribution kept separate from curator inference and severity) needed no work.

**Not complete at the aggregation layer, and this produced the most important scientific
correction in the review.** `tox_axis` and `event_cluster_id` were read by **zero** lines
of analysis or export code. Consequences, all verified:

- `tier_A_positive=62` pooled three different things: 54 ventricular-enlargement rows on
  real compounds, 3 disease-background rows carrying no compound, 1 *therapeutic* row
  (an siRNA **preventing** ventriculomegaly, whose own `grade_basis` says to exclude it
  from compound-toxicity analysis), and 7 rows on placebo/placeholder arms. Now published
  decomposed.
- The modelled outcome is addressed under proposal 4.

## Proposal 4 — modelling after qualification — **ACCEPTED; BEEBOP WAS RIGHT AND I WAS WRONG**

Beebop challenged the report's claim that a below-chance compound-identity AUC (0.094)
"confirms the validation is doing its job". **The challenge is correct.**

The probe is **degenerate**. Under leave-one-compound-out the held-out compound's own
indicator column never exists in training, so `Xte.reindex(..., fill_value=0.0)` makes
its design matrix all-zero and every prediction in the fold is `sigmoid(intercept)` — a
constant. Pooled AUC then ranks fold constants against each other, not cases against
controls, and lands below 0.5 because removing an event-rich compound lowers the training
base rate for exactly the fold holding the events. A diagnostic now reports this directly:
predictions are constant in **41 of 41 folds**. The no-information value is 0.5; 0.094 is
an artefact. The old conclusion was roughly right for demonstrably wrong reasons, which
is worse than no check. The trial-identity probe is only partly degenerate (constant in
19 of 41 folds) and does carry signal.

**The larger finding, which neither Beebop nor I anticipated: the headline model was
mostly measuring a procedure.** 66 of the 84 tier-B positive arms carry
`delivery_procedure_complication` as their **only** positive axis. Re-running the
identical procedure against an outcome with that axis removed (18 positive arms):

| Model | tier-B, all axes | excluding procedure complications |
|---|---:|---:|
| Route only | 0.889 | **0.650** |
| Route + indication | **0.910** | **0.606** |
| Route + indication + chemistry | 0.879 | **0.492** |

The headline 0.910 falls to 0.606 and the chemistry model falls below chance. The model
was substantially predicting *was this arm lumbar-punctured* from a route feature — a
tautology, since the route is how the procedure happens. This table is now generated into
`ml/ML_REPORT.md` and no predictive claim should be quoted without it.

The route contrast survives on corrected denominators but is weaker (OR 17.20 → 13.55)
and remains null within randomised comparisons (OR 0.74), which was already the report's
central caveat.

## Proposal 5 — version reconciliation and characterization — **PARTLY ACCEPTED**

**The 12-row claim is REFUTED, and this was the one finding the adversarial pass
discarded.** The 12 rows exist, but all 12 are already in this release — 11 match
arm-exactly, the 12th on DailyMed setid plus SPL section. Net new rows from reconciling
that branch: **zero**. The reconciliation surface runs the other way and is larger than
Beebop described; it is recorded as an open item below rather than acted on, because
importing another endpoint's rows needs scientific adjudication first.

**"Do not add releases together" is accepted and material.** The two datasets share no
identifier values, so a naive union would carry silent duplicates — and this release's own
`SCHEMA.md` and `METHODOLOGY.md` currently *invite* that pooling. Flagged below.

**Human-subset completeness is now published**, and it is much thinner than the
whole-roster figures implied, because the three purity-carrying constructs and 7 of the
13 sequence-resolved compounds are animal-only:

| Human subset | |
|---|---:|
| Compounds in human rows | 41 |
| with a published sequence | 6 |
| with a position-resolved chemistry map | 6 |
| **with a purity value** | **0** |
| with a conjugate stated | 0 |
| **Human rows with a numeric dose** | **0** of 1,332 |
| Human rows with an exposure duration | 739 of 1,332 |
| **Human in vitro / ex vivo rows** | **0** |

**Purity:** Beebop's demand that the published range be preserved was already satisfied —
`90-97` is stored as a string with `purity_method=HPLC-purified` and no point value is
invented anywhere. But **four locations published the false claim that purity is
NOT_REPORTED for every compound**, including a submitted PDF. Corrected; the honest
statement is that three rat-only constructs carry a range and the human subset has none.

---

## Additional discoveries, not in the proposals

1. **Five misattributed trials** (proposal 2a) — the most serious data defect found.
2. **The procedure-complication confound** (proposal 4) — the most serious scientific one.
3. **`measurements.csv` has no trial-key column.** Trial identity is implicit in
   `source_id`. This is why dedup had no natural key.
4. **`tier_A_positive` pooled a therapeutic row with toxicity rows** — a protective
   finding counted among positives.
5. **`effect_direction='no_change'` on FAERS zero rows** asserted a comparison never made;
   these rows have no comparator arm. Now `NOT_APPLICABLE`.
6. **Residual within-trial double counting.** 32 trials still exceed their own declared
   enrollment (+5.6% overall) because crossover and dose-escalation *periods* are
   separate arms — the same people counted up to four times. Not fixed: it needs a
   per-trial reading of arm descriptions. **Stated, not silently carried.**

## Checks performed

- 58 QC checks pass (was 53). Five are new: the ratchet, grade-0 admissibility,
  reported-zero denominator integrity, denominator/study-type agreement, and the
  existing suite extended.
- ML baseline reproduced bit-for-bit from a clean checkout before any change.
- 188 source URLs and 7 DOIs resolve.
- Participant arithmetic re-checked against ClinicalTrials.gov declared enrollment.
- All three PDFs within page limits; workbook regenerates.

## Limitations

- Residual within-trial participant double counting (+5.6%), as above.
- 17 trials are kept on the weaker `record_mention` identity tier. They are flagged in
  `attribution_basis` and deserve a human pass.
- Extension-cohort overlap is **not** deduplicated. ORION-8 (NCT03814187) contributes
  participants who are the same people as ORION-9/10/11, all four in the release.
- The non-procedure outcome rests on 18 positive arms. It is a sensitivity analysis, not
  a model.
- Human in vitro evidence remains zero. The nearest candidate was excluded as a
  lentiviral-vector study; that exclusion is a judgement worth revisiting.

## Decisions requiring German's scientific review

1. **The `reported_zero_no_denominator` category** — is this the right scientific
   treatment of a spontaneous-report silence, and should those rows retain `grade 0`?
2. **The 17 `record_mention` trials** — is a compound named in a trial's record, but not
   in its interventions, sufficient to attribute that trial?
3. **The therapeutic row** currently inside `tier_A_positive` — confirm it is excluded
   from compound-toxicity analysis everywhere.
4. **Extension-cohort policy** — should rollover trials contribute participants at all,
   or only outcomes?
5. **Whether the tier-B outcome should be redefined** to exclude procedure complications
   by default, rather than reported as a sensitivity analysis.
6. **The nervous-system reconciliation** — 207 hydrocephalus-relevant rows exist on that
   branch that are not here. Importing them crosses an endpoint boundary and needs a
   scientific decision before any pipeline change.
7. **`SCHEMA.md` and `METHODOLOGY.md` invite pooling with the sibling CNS release**, which
   would create silent duplicates. The invitation should probably be withdrawn or
   qualified.

## Remaining blockers

| Item | Owner |
|---|---|
| Crossover/dose-escalation participant dedup | Rocksteady, needs arm-description reading |
| Extension-cohort policy, then dedup | German decides, Rocksteady implements |
| Human in vitro evidence | open; no qualifying source found |
| Nervous-system reconciliation (207 rows) | German decides scope |

Beebop: the proposals were accurate and the two areas where I disagreed with you are
documented above with evidence. The counting was wrong in ways I had not detected, and
the modelling claim was wrong for reasons I had argued confidently. Both are corrected.
