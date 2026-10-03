# Joint review queue — items needing German *and* Gustavo

**Endpoint:** coagulopathy · **Branch:** `claude/coagulopathy-oligos-toxicity-ap70gf` ·
**Dataset commit:** `0680771` · **QC:** 104/104 · **Prepared by:** Rocksteady (coagulopathy), 2026-10-03

**Why this file exists.** Oscar decided on 2026-10-03 that items requiring both the scientific
authority and the model-strategy owner need a home, and that one should exist per endpoint.
`German_requests_100326.md` collects German's decisions; nothing collects the items where a
scientific ruling and a modelling consequence are the *same* decision, and Crank has recorded
that he has no channel to Gustavo at all. This is the first instance of the convention, offered
as a worked example — Crank has been asked to have Beebop create the rest and funnel into them.

**How to read it.** Each item states the question, the measured facts behind it, **why it
matters**, who decides, and what is blocked until they do. Every figure is computed from the
committed tables and is reproducible from the scripts named. Nothing here has been acted on.

**Standing constraint, from `SCIENTIFIC_RULES.md` §A:** no agent assigns toxicity labels,
infers missing values, manufactures negatives, resolves scientific conflicts, or trains a model
German has not permitted. Everything below is therefore a question, not a proposal awaiting
silence.

---

## Item 1 — Does a qualified record require position-resolved chemistry? **This is the one that changes the submission.**

**German decides** (what qualifies as evidence). **Gustavo needs it** (it sets what can be
modelled, and on which lane). Beebop is deriving the Minimum Qualified Record from German's
sign-off gates and has been asked the mechanical half of this separately.

### The facts

Compounds in this dataset carry a printed sequence, position-resolved chemistry, both, or
neither. Counted per evidence lane — rows and compounds, because an MQR counts *records*:

| lane | rows | compounds | rows whose compound has a printed sequence | **rows whose compound has sequence AND position-resolved chemistry** | compounds with both |
|---|---:|---:|---:|---:|---:|
| human participants (clinical) | 749 | 38 | 300 | **292** | 11 |
| human **in vitro** (strict, `study_type = in_vitro`) | 236 | 34 | 17 | **0** | **0** |
| human ex vivo plasma | 198 | 73 | 87 | 10 | 3 |
| animal (supporting) | 1,476 | 109 | 1,340 | **1,048** | 38 |
| **whole dataset** | **2,685** | 218 | — | **1,353 (50%)** | 48 |

### Why it matters, and it is not a bookkeeping question

**Requiring position chemistry inverts the Challenge's own priority.** Phase 2 states that
datasets "based on in vitro human systems or able to extrapolate data between in vitro human
systems and animal data are of particular interest." Under a chemistry-requiring MQR this
endpoint contributes:

- **0 qualified rows** from the strict human in-vitro lane — the lane the Challenge prizes;
- **1,048 qualified rows** from the animal lane — the lane that is explicitly supporting.

So the stricter the qualification rule, the more animal-weighted the submission becomes. That
is a perverse outcome and somebody senior should decide it deliberately rather than discover it.

**It also sets the headline.** The same dataset is honestly describable as "2,685 coagulation
measurements" or as "**11 qualified compounds / 292 qualified rows**". Those are different
submissions. I will not quote a qualified-record count until this is settled, and I would
rather publish 11 and say why than publish 2,685 and have the gate applied by a reviewer.

**And it bounds what Gustavo can build.** §G requires grouped splits by sequence family. A
model restricted to records with position chemistry has 48 compounds across all lanes, 11 of
them clinical — before any grouped split removes a fold. A model allowed to use sequence
without position chemistry has more rows and a coarser chemistry encoding, which §C permits
only as a *secondary derived* variable and never as a causal feature.

### What would help most

A three-tier answer rather than a binary, if the science supports it: records with
sequence + position chemistry; records with sequence only; records with neither. Then the
submission can report all three with their denominators and nobody has to choose between
honesty and volume. **That is a suggestion, not a finding — the tiering is German's.**

**Blocked until answered:** the corrected endpoint scorecard, any qualified-record figure in
the narrative, and Gustavo's choice of modelling lane.

---

## Item 2 — `coag_tox_grade` applies CTCAE cut-offs to 834 non-clinical rows, which §E prohibits

**German decides.** **Gustavo needs it** — this column is the obvious label, and 91% of it may
not be usable as one.

### The facts

`coag_tox_grade` is an ordinal 0–3 assigned mechanically from a control-referenced ratio using
published CTCAE v5.0 cut-offs.

| graded rows | 918 of 2,685 |
|---|---:|
| **not clinical — the case §E names** | **834 (91% of graded)** |
| — animal in vivo | 679 |
| — in vitro | 102 |
| — ex vivo plasma | 50 |
| clinical, where CTCAE is defined | 84 |

§E: *"Do not map in-vitro fold-change bins to clinical severity grades (e.g. CTCAE) unless
clinically validated. Call it experimental response severity."*

### Why it matters

The dataset already discloses a lot: `is_validated_clinical_grade` is FALSE on every row,
`grade_authority` names who assigned each grade, and `schema.md` opens by calling the column
"a curator-derived research score, not a clinical grade". **But hedged wording does not satisfy
a prohibition on the mapping itself** — the derivation is still CTCAE and the column is still
named for toxicity grade. A modeller who takes `coag_tox_grade` as a label is training on a
clinical severity scale applied to mouse tail-bleed ratios for 679 of its rows.

There is a second, narrower question inside it: even the 84 clinical rows use a **control mean**
as the denominator where CTCAE uses the upper limit of normal. That deviation has always been
disclosed, and 157 graded rows carry `grade_caveat = within_reference_range_resolution`
precisely because a ratio a few percent above 1.00 is not evidence of prolongation.

### The decisions

1. Do non-clinical rows keep an ordinal at all, or are they rescoped to
   `experimental_response_severity` under a non-CTCAE rubric?
2. May the 84 clinical rows keep a CTCAE-derived grade given the denominator deviation?
3. Gustavo: if (1) rescopes, is the rescoped ordinal usable as a training label, or does
   modelling fall back to the raw ratio plus `effect_direction`?

I have offered Beebop to stage a candidate rescoped column in `research/` — computed, diffed
against the current bands, not promoted — so that German's decision is an approval rather than
a design exercise. **Awaiting his yes/no before building it.**

**Blocked until answered:** any label-bearing release, and Gustavo's label choice.

---

## Item 3 — Zero training-eligible sequence-matched negative controls

**German decides** whether sequence-dependent analysis proceeds without them. **Gustavo needs
it** — it is a hard bound on what the model can claim to have learned.

### The facts

`data/controls_inventory.csv`, 108 groups. By control class:

| control | rows |
|---|---:|
| vehicle or buffer | 1,277 |
| untreated or pre-dose | 314 |
| placebo | 223 |
| pharmacological positive control (heparin, enoxaparin, bivalirudin, warfarin, protamine) | 81 |
| active comparator | 28 |
| **sequence-matched negative control** (scrambled, mismatch, sense-strand, reverse complement) | **8** |

Those 8 rows cover **3 compounds**, and **none of the 3 has both a printed sequence and
position-resolved chemistry**. §E: *"Unsourced controls are not training rows"* — a control
enters training only when its sequence, chemistry, assay and measured outcome are all sourced.
So under §E as written, this endpoint has **zero training-eligible sequence-matched negative
controls.**

### Why it matters

A vehicle controls for the delivery system. A placebo controls for being in a trial. **Neither
separates a sequence effect from a chemistry or a formulation effect** — only a scrambled or
reverse-complement oligo does. Without them, a model that appears to learn
"sequence → coagulopathy risk" cannot be shown not to have learned
"phosphorothioate content → coagulopathy risk", which is a chemistry-class effect the
literature already attributes to the backbone rather than the sequence.

This is structurally the same finding German reports for thrombo — *zero clean sequence-linked
clinical negatives* — arrived at independently at a different endpoint and by a different
route. That convergence is itself worth his attention: it suggests the gap is a property of the
published literature, not of one curation effort.

**Blocked until answered:** whether any sequence-dependent claim is permissible for this
endpoint, and whether acquisition should be re-prioritised toward sequence-control experiments
specifically.

---

## Item 4 — `sequence_family_group` cannot be computed without an adjudication

**German decides.** **Gustavo needs it** — §G *requires* grouped splits by sequence family, so
without this there is no compliant validation design.

§G requires the column "from the start" and simultaneously forbids what the obvious
implementation would do: *"Shared-sequence grouping must not merge chemically distinct
administered constructs. Reference identity is not experimental-batch identity."*

This corpus contains the exact trap, twice:

- a GalNAc-conjugated compound and its unconjugated parent targeting the same site — same base
  sequence, different administered molecule;
- `COG-OLG142`, recorded verbatim as *"same base sequence as BAY 2306001 / ISIS 416858"*.

Grouping on base sequence merges those and leaks across the split. Not grouping them leaves
near-neighbours in different folds, which §G also prohibits. **The rule that decides is
scientific**, and §A forbids me from resolving it.

**What is already possible, and worth Gustavo knowing:** `paper_group` needs no new column.
Every row carries exactly one `source_id`, so **leave-one-paper-out is computable today**.
§G's LOPO requirement is satisfiable now; only the sequence-family axis is blocked.

---

## Item 5 — Four of the five grade calibration rows disagree with their source

**German decides.** Gustavo: information only, but it bounds trust in the label.

24 participant rows carry a grade a source itself reported. **Five carry both a source grade
and a curator research score — the entire calibration set — and four of the five disagree, in
both directions:**

| row | source grade | curator score |
|---|---:|---:|
| `COG-MSR2636` | 1 | **3** |
| `COG-MSR2637` | 3 | **0** |
| `COG-MSR2638` | 3 | 2 |
| `COG-MSR2639` | 3 | 2 |
| `COG-MSR2640` | 3 | 1 |

Until this is adjudicated, the curator scale must not be presented anywhere as agreeing with
source severity. It currently is not, and should stay that way.

---

## Item 6 — 132 participant rows carry both axes TRUE

**German decides.** Gustavo: these are the rows whose label is genuinely ambiguous.

132 rows have `on_target_effect = TRUE` **and** `unintended_toxicity = TRUE` — 49 bleeding
outcomes, 35 thrombotic, 21 anticoagulant activity, 10 fibrinolysis, 10 clotting time, 5
thrombin generation.

For a factor-lowering drug, bleeding is either the mechanism working or the harm, and §E says
plainly that *"intended pharmacology is not toxicity"* and *"deliberate inhibition of vWF,
thrombin, factor IX/XI or platelet function is not an adverse label by default."* Only a
clinician can decide per arm. A model trained across these without resolution learns that
anticoagulants prolong clotting times — true, circular, useless for safety prediction.

---

## Item 7 — Nineteen composite readouts are filed as single endpoints

**German decides** whether they may be used; Beebop/crosswalk owns the flag.

19 rows carry a source-constructed composite: `coagulopathy_composite`, `aPTT_PT_TT_composite`,
`clinically_relevant_bleeding_composite`, and `platelet_count_fibrinogen_PT_INR_composite` —
the last mixing platelet count with coagulation, which is exactly the conflation §E names
("platelet-count decline, platelet activation, coagulation, bleeding and thrombosis are
separate endpoints with separate biology"). **The sources built these, not us**, which §E
permits as source reporting — but they currently sit under `clotting_time`, `bleeding_outcome`
and `platelet_coag_crosstalk` as though they were single-endpoint observations.

Proposed: an `is_composite_endpoint` flag plus constituent endpoints, so a composite can be
excluded from single-endpoint analysis. Schema, so Tier 0 crosswalk — not added.

---

## Item 8 — Twenty-three of the 46 headline trials rest on one source record

**German decides** whether that is acceptable corroboration for an externally quoted count.

46 verified human interventional trials with a coagulation endpoint, 21 registry-identified,
zero failing the over-merge QC. But **23 of the 46 are built from a single source record**:
`COG-STU053`, `054`, `055`, `056`, `075`, `076`, `083`, `084`, `085`, `100`, `101`, `104`,
`108`, `111`–`115`, `145`, `170`, `205`, `209`, `210`.

Each is identified and endpoint-evaluable, so each is correctly in the total by the stated
rule. None has independent corroboration. **46 is reproducible; it is not independently
corroborated throughout**, and that distinction belongs in whatever document quotes it.

---

## Summary: who is blocking what

| Item | Decides | Also needs | Blocks |
|---|---|---|---|
| 1 — qualified record definition | German | Gustavo, Beebop | the scorecard, every qualified-record figure, Gustavo's lane choice |
| 2 — CTCAE on 834 non-clinical rows | German | Gustavo | any label-bearing release |
| 3 — zero eligible sequence controls | German | Gustavo | any sequence-dependent claim |
| 4 — `sequence_family_group` | German | Gustavo | §G-compliant validation design |
| 5 — grade calibration (4 of 5 disagree) | German | — | trust in the curator scale |
| 6 — 132 both-axes rows | German | Gustavo | label resolution on the ambiguous set |
| 7 — 19 composites | German | crosswalk | single-endpoint analysis |
| 8 — 23 single-record trials | German | — | external quotation of 46 |

**Reproduce any figure here with:** `scripts/validate_dataset.py` (104 checks),
`scripts/audit_scientific_rules.py` (§C/§G field coverage),
`scripts/build_controls_inventory.py`, `scripts/build_characterization_gap_register.py`,
`scripts/audit_attribution.py`. All run from `scripts/make_release.py`.

---

JOINT REVIEW QUEUE — ITEM 1 BLOCKS THE SCORECARD · NOTHING BELOW HAS BEEN ACTED ON
