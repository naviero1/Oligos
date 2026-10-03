# Rubric specification and evidence comparison — for German's ratification

**Endpoint:** coagulopathy · **Branch:** `claude/coagulopathy-oligos-toxicity-ap70gf` ·
**Prepared by:** Rocksteady, 2026-10-03 · **Status: SPECIFICATION ONLY — NO LABEL COMPUTED**

**What this is and is not.** `SCIENTIFIC_RULES.md` §K permits a proposal derived from the rules
to be submitted for German's ratification, and states that only an *authority claim* requires his
primary documents. This is such a proposal. Beebop's instruction of 2026-10-03 permits a rubric
specification and an evidence comparison, and prohibits computing a severity-label column
**including under a staging directory, because that still assigns labels**. Accordingly:

- **No column has been computed.** No candidate severity values exist anywhere in this
  repository, in `data/`, in `research/`, or in a scratch file.
- **No threshold is proposed.** Section 4 lists the decisions and their consequences; it does
  not pick any.
- The evidence in section 3 is the **distribution of values already in the dataset**, reported
  as percentiles. It is not banded, not scored and not labelled.

§A applies: no agent assigns toxicity labels. This document exists so that the decision German
makes is a ratification rather than a design exercise.

---

## 1. What the current column does, and the rule it breaks

`coag_tox_grade` is an ordinal 0–3 assigned mechanically by applying **CTCAE v5.0 cut-offs to a
control-referenced ratio**, for the readouts CTCAE defines. `grade_basis` records the rule
applied per row; the vocabulary in use:

| rule applied | rows |
|---|---:|
| `CTCAE_v5.0_control_referenced:prolongation_>1.0-1.5x` | 247 |
| `CTCAE_v5.0_control_referenced:prolongation_ratio<=1.0` | 239 |
| `source_states_measured_no_change(overrides_control_referenced_ratio)` | 126 |
| `source_states_measured_no_change_on_a_CTCAE_graded_readout` | 99 |
| `CTCAE_v5.0_control_referenced:prolongation_>1.5-2.5x` | 68 |
| `CTCAE_v5.0_control_referenced:fibrinogen_<1.0-0.75x` | 68 |

918 of 2,685 rows are graded. **834 of those 918 (91%) are not clinical** — 679 animal in vivo,
102 in vitro, 50 ex vivo plasma.

§E: *"Do not map in-vitro fold-change bins to clinical severity grades (e.g. CTCAE) unless
clinically validated. Call it experimental response severity."* §K gate 12 adds that claims must
be no stronger than the evidence supports.

**The column is non-compliant as derived, and the non-compliance is not fixed by disclosure.**
The dataset already states `is_validated_clinical_grade = FALSE` on every row, records
`grade_authority` per row, and opens `schema.md` by calling the column a curator-derived research
score. All true, and none of it changes what the derivation does.

---

## 2. Evidence comparison, part A: what CTCAE requires versus what these sources provide

| CTCAE v5.0 assumes | These sources provide | Consequence |
|---|---|---|
| A **clinical** subject with a clinical course | 679 animal in vivo, 152 in vitro / ex vivo rows among the graded | The scale is being applied to systems it was not written for. This is the §E prohibition itself |
| Comparison against the **upper limit of normal** | A **control mean** (vehicle, placebo, pre-dose or buffer) | A ratio marginally above 1.00 is not evidence of prolongation. 157 graded rows already carry `grade_caveat = within_reference_range_resolution` for exactly this reason |
| A defined readout set (aPTT, PT/INR, fibrinogen) | Those, plus readouts CTCAE never defines — `template_bleeding_time`, `thrombus_platelet_accumulation_fluorescence`, `fibrin_formation_fluorescence` | For the undefined readouts the dataset correctly declines to grade. For the defined three it grades across every lane |
| Severity as experienced by a patient | Analytical magnitude of change in an assay | These are different quantities. An eightfold aPTT in purified plasma and a grade 3 bleed in a participant are not the same object |

## 2.1 Evidence comparison, part B: the calibration evidence, which is thin and mostly contrary

24 rows carry a grade a source itself reported. **Five carry both a source grade and the curator
score — the entire calibration set — and four of the five disagree, in both directions:**

| row | source grade | curator score | direction of disagreement |
|---|---:|---:|---|
| `COG-MSR2636` | 1 | **3** | curator more severe by 2 |
| `COG-MSR2637` | 3 | **0** | curator less severe by 3 |
| `COG-MSR2638` | 3 | 2 | curator less severe by 1 |
| `COG-MSR2639` | 3 | 2 | curator less severe by 1 |
| `COG-MSR2640` | 3 | 1 | curator less severe by 2 |

**There is no evidence base for asserting that the curator scale tracks source severity.** Five
paired observations, four disagreements, no consistent direction. Any rubric that replaces this
one should be ratified on its construction, not on agreement with a calibration set this small.

---

## 3. Evidence comparison, part C: the ratio distribution already in the dataset

Descriptive only. **Not banded, not scored.** 1,668 of 2,685 rows carry a derivable
control-referenced ratio; the lanes are kept separate because §D and gate 7 forbid pooling them.

| lane | n | min | p25 | median | p75 | p95 | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| human participant | 264 | −3.78 | 0.29 | 0.99 | 1.78 | 6.86 | 144.50 |
| human laboratory | 192 | 0.00 | 0.96 | 1.00 | 1.11 | 3.78 | 6.40 |
| animal | 1,208 | 0.00 | 0.83 | 1.00 | 1.15 | 1.74 | 12.00 |
| unresolved origin | 4 | 0.00 | 2.40 | 2.70 | 10.00 | 10.00 | 10.00 |

Readouts carrying a ratio, largest first: aPTT 430, PT 313, fibrinogen 123, FXI activity 92,
thrombus platelet accumulation 65, antithrombin activity 63, template bleeding time 57, fibrin
formation 52.

**Three things this distribution shows that bear on any rubric:**

1. **The median is 1.00 in all three substantive lanes.** The mass of this dataset is *no
   change*, which is a property worth preserving and easy to destroy with a threshold placed
   near unity.
2. **The lanes have different dispersion.** p95 is 6.86 in participants, 3.78 in human
   laboratory, 1.74 in animal. One set of cut-offs applied across all three does not mean the
   same thing in each — which is the mechanism by which a single scale becomes misleading.
3. **Negative and zero ratios exist** (participant min −3.78; zeros in all lanes). Any rubric
   must say what a negative or zero control-referenced ratio means before it can band one; the
   current CTCAE mapping has no answer and those rows are among the ungraded.

---

## 4. The specification: the decisions to be made, with consequences — none taken

### D1. Does a non-clinical ordinal exist at all?

| option | consequence |
|---|---|
| **(a) No ordinal for non-clinical rows.** Retain `ratio_to_control`, `effect_direction` and the source's own words; drop the ordinal for 834 rows | Fully §E-compliant. Loses an ordering a modeller would have to reconstruct, and it would be reconstructed *without* the caveats the dataset carries |
| **(b) A separate `experimental_response_severity`**, explicitly not a clinical grade, defined per lane | §E's own suggested remedy. Requires German to set the construction. Risk: a reader treats it as a clinical grade anyway, which is what happened to the current column |
| **(c) Keep an ordinal only where a source graded it** (24 rows) | Unimpeachable and almost empty. Would reduce graded rows from 918 to 24 |

### D2. If an ordinal exists, on what is it constructed?

Not thresholds — the *basis*. Options German may wish to rule between: analytical magnitude
relative to the control with lane-specific dispersion; magnitude relative to the assay's own
reference interval where the source states one; rank within the readout's own distribution
inside its lane; or a purely qualitative three-state (unchanged / changed / changed beyond the
source's stated reference). **No numbers are proposed here, by instruction.**

### D3. May the 84 graded clinical rows keep a CTCAE-derived grade?

The denominator is still a control mean rather than the upper limit of normal. Either the
deviation is acceptable and documented, or those 84 move to the same basis as the rest.

### D4. What happens to the 157 `within_reference_range_resolution` rows?

They are flagged because the ratio sits close enough to 1.00 that the control's own resolution
cannot distinguish a real change. Under any new rubric they are either excluded, or carried with
the flag, or collapsed into "unchanged".

### D5. Does the rescoped field apply across lanes at all?

Gate 7 and §D forbid pooling human and animal as interchangeable ground truth. A single ordinal
spanning both may be legitimate as a *within-lane* ordering and illegitimate as a cross-lane one.
If so, that should be stated in the field's own definition rather than left to the reader.

---

## 5. What happens after ratification, and what will not happen before it

On German's ruling, the implementation is mechanical: `grade_basis` already records the rule
applied per row, so a rescope rewrites a derivation that is already explicit and auditable, and
`grade_authority`, `is_validated_clinical_grade` and `evidence_class_review_status` already exist
to mark what is derived and unreviewed.

**Until then: no severity-label column is computed, anywhere.** Not in `data/`, not in
`research/`, not in a scratch directory. The existing `coag_tox_grade` is left exactly as it is
and carries its non-compliance in the open — changing it silently would be the same category of
error as having derived it this way in the first place.

---

RUBRIC SPECIFICATION — NO LABEL COMPUTED, NO THRESHOLD PROPOSED, AWAITING GERMAN'S RATIFICATION
