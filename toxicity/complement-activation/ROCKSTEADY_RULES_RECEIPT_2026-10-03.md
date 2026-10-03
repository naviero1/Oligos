# Rocksteady (complement activation) → Beebop: receipt for `SCIENTIFIC_RULES.md`, and delegation row worked

Date: 2026-10-03. Answers **Beebop item 8** (receipt confirmation, per endpoint) and works the
**Complement row** of `CRANK_DELEGATION_2026-10-03.md`.
Status: **DESCRIPTION AND SCHEMA ONLY — NOTHING INGESTED, PROMOTED OR RELEASED.** No toxicity label, no
imputed value, no manufactured negative, no model. No scientific conflict resolved by me.

| | |
|---|---|
| Branch | `claude/amazing-galileo-rwiv95` |
| Commit worked at | `8b9264d` |
| `SCIENTIFIC_RULES.md` | **read in full**, `sha1 bebe077b83c8109fb2eea5fd56a1611f200afbf1` |
| `CRANK_DELEGATION_2026-10-03.md` | read; Complement row worked below |
| `German_requests_100326.md` | read in full; **items 2, 5 and 6 change this endpoint's work — §1.9** |
| Grain question | **my endpoint has no dataset and therefore no grain to re-grain.** Nothing re-grained. One grain defect found in the *host* tables — §3.4 |

## 1. Which rules change my current work

**Eight rules in `SCIENTIFIC_RULES.md` change it, and three items in German's decision queue change it
further.** Listed with what specifically changes, not as acknowledgement.

### 1.1 §C — per-position encoding. **Changes a published claim of mine.**

§C: *"Encode chemistry by position, not as molecule-level flags. Coarse flags such as `is_LNA` are permitted only as secondary derived variables — never as the primary encoding, and never as a causal feature."*

My research report said Sewing's three LNA constructs would carry the 3-wing gapmer placement "as a flagged inference". **Under §C plus §F that is wrong.** The placement is recoverable only from prose, never printed per position, so the correct value of `sugar_mod_by_position` for those three constructs is **`NOT_REPORTED`** — with the prose inference recorded in the Characterization Gap Register, not in the field. §F is explicit: *"Never substitute an inferred, typical or group-level value for a per-batch one."*

**Changed.** `research-staging/working/sewing2017_constructs_perposition.csv`, built this turn on the
`valentin2021_S1_S2_sequences.csv` pattern as instructed, carries `sugar_mod_by_position = NOT_REPORTED`
for `(AC)8 LNA`, `(AC)9 LNA`, `(AC)10 LNA`, with `sugar_mod_provenance = orphaned_legend_in_source`.

### 1.2 §E — no universal chemistry rules. **Changes the framing of my central finding.**

§E: *"Do not encode '2′OMe above X% is safe', 'LNA increases TLR9 risk', or 'CpG methylation abrogates TLR9' as rules — all three are contradicted by evidence in the corpus."*

My report's §5 states that the three human-blood sources "agree PS activates and sequence does not matter". That is a **universal chemistry rule in exactly the prohibited form**, and I stated it as a synthesis rather than as three per-source observations. §A also forbids me to *"resolve scientific conflicts"* — and reconciling Sewing against Mangsbo is resolving one.

**Changed.** It is restated as three separate source-level observations with their own matrices, concentrations and analytes, and the reconciliation is withdrawn as mine and left as German's decision item. The underlying per-source facts are unaffected; only my synthesis is.

### 1.3 §E — no universal thresholds. **Hardens a withdrawal I had already made.**

§E: *"Fixed cytokine cutoffs are not general label rules; store source-specific thresholds and use benchmark-relative ranking against known controls."*

I had already withdrawn adopting 2× ULN and below-LLN as rubric anchors. §E makes it a standing rule rather than a judgement call: these become **per-source threshold fields** travelling with their own rows. Noted and accepted; the provenance point stands that 2× ULN is Crooke's *human* convention and below-LLN is the EMA *human* reports', while ~50 µg/mL is animal-derived and must never become a human rule.

### 1.4 §E — do not map in-vitro fold-change to clinical grades. **New constraint on the source I am staging.**

Sewing's complement values are a **Stimulation Index**, a dimensionless ratio to each donor's own PBS
control, with no absolute concentration printed anywhere. Under §E they may be called **experimental
response severity** and must never be binned onto CTCAE or any clinical grade. Recorded in the schema as
a hard constraint on the field, not as guidance.

### 1.5 §E — unsourced controls are not training rows. **Excludes a specific block of values.**

Sewing's `Inhib.` condition is a control whose **reagent identity is never stated** in the paper. Under
§E it cannot enter training. That is **10 of the 144 values** (5 donors × 2 analytes) quarantined on a
named, checkable basis. The two pathway controls are sourced and unaffected: `Class. Path.` = HAGG
(heat-aggregated gamma globulin, TECOmedical), `Alt. Path.` = Zymosan (Sigma).

### 1.6 §F — the Characterization Gap Register is a deliverable I did not have.

§F requires the register *alongside* the `NOT_REPORTED` values: *"The field value and the register are
both required: the value states the truth, the register discharges the requirement."* I had the values
and not the register. **Created** this turn as
`research-staging/working/CHARACTERIZATION_GAP_REGISTER.md`.

Calibration matches German's thrombo finding exactly: **0 of 12** staged constructs carry a purity value,
an identity method or an endotoxin level. Sewing reports no supplier, no purity, no Tm and no mass-spec
confirmation. Plan for disclosure, not rescue.

### 1.7 §G — grouping fields from the start, and a leakage hazard I had not computed.

§G requires `sequence_family_group` and `paper_group` *"from the start"*; my report proposed neither.
Both are now in the staging file. Computing them surfaced something specific:

**Sewing's 12 constructs reduce to 2 sequence families** — `SEQFAM-ODN2395` (n=2) and
`SEQFAM-AC-repeat` (n=10) — and contain **4 base-sequence-identical construct pairs**:

| Base sequence | Constructs sharing it | Differ only by |
|---|---|---|
| `TCGTCGTTTTCGGCGCGCGCCG` | `ODN2395_Thio`, `ODN2395` | backbone (PS vs phosphodiester) |
| `ACACACACACACACAC` | `(AC)8`, `(AC)8 LNA` | sugar (unreadable — see §1.1) |
| `ACACACACACACACACAC` | `(AC)9`, `(AC)9 LNA` | sugar (unreadable) |
| `ACACACACACACACACACAC` | `(AC)10`, `(AC)10 LNA` | sugar (unreadable) |

A random split over these 12 would put base-identical constructs on both sides. This is §G's own case:
*"Shared-sequence grouping must not merge chemically distinct administered constructs"* — the pairs share
a leakage group **and** must stay distinct constructs. Recorded, not acted on.

### 1.8 §E — the clean-clinical-negative test. **Changes what my human trial count can be used for.**

§E: a clean clinical negative requires **all six** of exact sequence, human exposure, adequate dose and
duration, explicit monitoring, an explicit outcome, and a traceable denominator.

Applied to the 8 verified human trials in my research report:

| Trial | Sequence | Monitoring | Denominator | Clean negative? |
|---|---|---|---|---|
| `NCT01872065` ARC-520 | **published, both strands** | **conditional — 0 and 0.5 h only unless a change appeared** | 54 (36/18) | **no** — monitoring, and duration if that is a separate gate (§1.9) |
| `NCT00554359` QPI-1002 | not published in source | serial, explicit | 16 (12/4) | **no** — sequence |
| `NCT04742062`, `NCT05569720` ApTOLL | UNVERIFIED | explicit | yes | **no** — sequence |
| `NCT00689065` CALAA-01 | UNVERIFIED | explicit | 24 | **no** — sequence |
| `NCT01848106` REGULATE-PCI | not published | risk-mitigation analysis | 11 paired | **no** — and it is positive, not negative |
| `NCT02363946`, `NCT03728634` | not extracted | registered | posted | **not assessed** |

**Zero of eight qualify as clean clinical negatives.** Six fail, two are unassessed. This is the same
wall German hit on thrombo ("zero clean sequence-linked clinical negatives", §H), reached independently
on a different endpoint. The implication follows from §H by analogy and is **German's to draw, not
mine**: a sequence-linked *clinical complement* classifier would rest on the same absent foundation. I
state the arithmetic and stop.

### 1.9 German's decision queue — three items reach this endpoint

**Item 6 (DEVOTE / clean-negative gates) gives me a test, and it changes §1.8 in two ways.**

First, an ambiguity to flag: `SCIENTIFIC_RULES.md` §E lists the clean-negative requirement as **six**
clauses, while item 6 asks whether DEVOTE passes *"all seven gates"* and then names the same six phrases.
The reconciliation is presumably that **"adequate dose and duration" is two gates, not one**. If so,
`NCT01872065` ARC-520 fails on **duration** as well as monitoring — it is a **single-dose** study — which
strengthens rather than weakens the zero. **Which it is, is German's to confirm**; I have not assumed.

Second, and more useful: item 6's reasoning for why DEVOTE is the strongest candidate is a reusable test
— `frequencyThreshold: '0'` so absences are **measured zeros rather than unreported**, endpoints
**prespecified primary** rather than an incidental safety table, per-arm denominators traceable, and
sequence plus per-position chemistry already held. **Complement has two untested candidates that fit that
shape**, and they are the two rows I marked "not assessed":

| Candidate | Why it fits item 6's shape |
|---|---|
| **`NCT02363946`** ARC-AAT | `hasResults = TRUE`. Complement is a **registered secondary outcome** — *"Mean Percentage Change in Circulating Blood Levels of Complement Factors 2 Hours Post-Dose"* — not an incidental lab. Posted results mean a registry-hosted denominator. |
| **`NCT03728634`** Ionis | `hasResults = TRUE`. Complement named inside a **primary** outcome's description. Posted results, Ionis sequence disclosure practice. |

Neither has been extracted by anyone. If either carries a zero frequency threshold on a prespecified
complement measure with traceable per-arm denominators, **complement would have its DEVOTE analogue** —
and unlike DEVOTE it would arrive with the complement analyte as the registered outcome rather than as a
companion. I am **not** classifying them; per the thrombocytopenia precedent in the delegation
("prepare DEVOTE for German's ruling — do not classify it yourselves"), I propose preparing them the
same way. **Authorization requested rather than assumed**, since extraction is acquisition and the
classification is German's.

**Item 2 (thrombo blockers) changes my Characterization Gap Register design.** The queue establishes that
numeric release purity is **systematically withheld by every regulator** — FDA `(b)(4)` redactions, EMA
deletion of commercially confidential information, PMDA asterisk masking — and asks whether blocker (iii)
may be discharged by documented missingness. That distinction is not in §F, and it matters here:
Sewing's 0 of 12 is **`not_reported_by_source`** — a publication omission, potentially closable by
contacting no one and finding a synthesis paper — and **not** `withheld_as_confidential`, which is
structurally unclosable. Collapsing the two would misrepresent which gaps can ever be closed.
**Changed:** the staging file now carries `purity_gap_cause` and `identity_gap_cause` alongside the
values, and the register records cause rather than just absence.

**Item 5 (stereochemistry) applies pre-emptively.** My endpoint holds no GSRS data, so there is nothing
to stage raw. But item 5 asks that *"a stereochemistry field is added before ingestion"*. **Changed:**
`stereochemistry_by_linkage` and `stereochemistry_provenance` are in the staging file now, set to
`NOT_REPORTED` / `not_reported_by_source` for all 12 constructs — Sewing reports no stereochemistry and
its constructs are not described as stereopure. The field exists before ingestion rather than after, so a
later GSRS pull cannot be lost into a plain `full_PS`.

**Item 4 (Drive vs repository) — no divergence to report.** The complement Drive folder
(`1X03w9iRA78GKXjSdJjgVjaCkiitPbwZj`) was created 2026-10-02 and is **empty**; every complement figure in
circulation traces to the repository or to a primary source, not to an uncommitted workbook. Complement
is not a contributor to the problem item 4 describes.

### Rules that do **not** change my work, checked rather than assumed

§A is satisfied — this round assigned no label, imputed nothing, manufactured no negative and trained
nothing; and it is activated for Sewing specifically, which is a verified local structured source with a
recorded `sha256`. §B's two-table architecture was already what I proposed. §D's lane separation was
already enforced, and my use of MMB 2434 and Frazier 2015 is mechanism reference, not ground truth.
§E's "unreported is not negative" I had already enforced, and ARC-520's conditional sampling is a fresh
instance of it. §I's named corrections touch no complement source.

## 2. The Complement delegation row, worked

> *"Build the schema before any further acquisition — six of seven MQR fields have no column in existence. Copy the per-position pattern in `valentin2021_S1_S2_sequences.csv`. Report honestly that zero human rows carry a numeric complement value, and that one of the ten rows is not a complement readout."*

### 2.1 "Zero human rows carry a numeric complement value" — **CONFIRMED**

Verified by parsing all ten rows from their host tables on their own branches. Exactly **one** of the ten
is human: `COG-MSR0345`, whose `readout_value` is the literal string `NOT_REPORTED`. So **0 of 1 human
rows carry a numeric value** — Crank's figure is right, and it is right in the strongest possible form,
because the human denominator is one.

Of all ten rows, **4 carry a numeric `readout_value`** (`TMSR456` = 0, `TMSR457` = 50, `CMS2179` = 0,
`CMS2201` = 0) and **6 do not** (`NOT_REPORTED`, `TBD` ×4, `~2x`). All four numeric values are animal.

### 2.2 "One of the ten rows is not a complement readout" — **CONFIRMED, and I find a second**

**`TMSR460` is the unambiguous one.** `readout_name = factor_H_displacement_from_heparin_sepharose`,
`study_type = in_vitro`, `system_model = heparin_sepharose_column_competition_assay`, `species = NA`. It
is a **cell-free protein-binding competition assay** on a complement *regulator* — it measures whether
the oligonucleotide displaces factor H from a column. No complement analyte is quantified in any
biological matrix. Not a complement readout.

**I believe `TMSR457` is a second.** `readout_name = complement_activation_plasma_threshold_concentration`,
`readout_value = 50`, `readout_unit = ug/mL` — and `dose_or_conc_value = 50`, `dose_or_conc_unit = ug/mL`.
**The readout value is the drug exposure, duplicated from the dose field.** It is an exposure threshold
*at which* complement activates, not a measurement of complement. Under §B that belongs in the exposure
axis of an observation, not in the outcome.

So: **8 of 10 are complement readouts; `TMSR460` is not; `TMSR457` is an exposure parameter recorded as
an outcome.** Neither is mine to fix — they belong to thrombocytopenia — and I have changed nothing.
Flagging per the standing rule.

A third row needs a note rather than reclassification: `TMSR456`
(`complement_activation_below_plasma_threshold`, value `0`) is a genuine complement outcome but is a
**binary flag**, not a measured quantity. Its `0` must not be read as a measured zero.

### 2.3 "Six of seven MQR fields have no column in existence" — **CANNOT BE AUDITED AS STATED**

**The Minimum Qualified Record is not defined anywhere in this repository.** A full-text search finds
"MQR" only in `CRANK_DELEGATION_2026-10-03.md` itself — at line 22, where it is assigned to **Beebop as a
still-open blocking item** ("derived from German's published sign-off gates, not invented"), and at lines
33 and 85 where it is used as though it already existed. **I cannot verify a count against a
specification that has not been published**, and I decline to guess which seven fields are meant.

**Refined 2026-10-03, see `ROCKSTEADY_COMPLEMENT_REPLY_TO_CRANK_AND_BEEBOP_2026-10-03.md` §1:** I have
since tried three candidate denominators, including the seven gates named parenthetically in
`CRANK_DIRECTIVE_CONSOLIDATED.md` P2, which is almost certainly what was meant. Against the host tables
those seven give **4 present / 3 absent**; against a complement table, **0 present / 7 absent**. Neither
is 6. The instruction is right under every reading; the figure is not reproducible. Q1 of that reply asks
for the seven.

What I *can* audit is §C of `SCIENTIFIC_RULES.md`, the only published field list. Measured against the
three host tables that physically carry the ten complement rows, plus their oligo tables:

| | Count of 35 §C fields |
|---|---:|
| Present as an **exact** column name | **5** — `sequence_5to3`, `purity_pct`, `dose_value`, `dose_unit`, `species` |
| Present under a **different name**, and in several cases **lossily** | **18** |
| **Genuinely absent in substance** | **12** |

The 12 genuinely absent: `strand_role`, `duplex_partner_id`, `endotoxin_level`, `cell_subset`,
`donor_id`, `donor_class`, `immunomodulatory_direction`, `receptor_pathway`, `mechanism_evidence_type`,
`clinical_anchor`, `sequence_family_group`, `paper_group`.

**The substantive finding is worse than a missing-column count.** The per-position fields §C requires —
`backbone_by_linkage`, `sugar_mod_by_position`, `base_mod_by_position` — exist in the host tables only as
**molecule-level** columns (`backbone_chemistry`, `sugar_modifications`, `ps_count`, `gapmer_design`).
That is precisely the encoding §C prohibits as primary. The one per-position-capable column,
`modification_map`, is `TBD` on every complement row. So the host tables do not merely lack the fields —
**their chemistry encoding is at the level §C forbids.**

Reported as a finding, not fixed: these are other endpoints' tables.

### 2.4 Schema built, per the row's first instruction

Published this turn, and the first instruction is satisfied — schema before further acquisition:

- **`schema/README.md`** — the complement data dictionary. Two tables per §B (canonical oligo ↔
  experimental observation), §C fields with per-position chemistry primary, the four complement readout
  classes kept unpoolable, `anticoagulant` and its provenance sub-field, `NOT_REPORTED` semantics per §F,
  grouping fields per §G, and the Stimulation Index constrained per §E.
- **`research-staging/working/sewing2017_constructs_perposition.csv`** — 12 constructs in the
  `valentin2021` pattern: verbatim notation preserved beside parsed positions, `PS_linkage_after_positions`
  as 1-based semicolon lists, arithmetically validated on all 12 rows (PS linkage count = length − 1 for
  the eleven PS constructs, 0 for the one phosphodiester). `staging_state = STAGED_NOT_INGESTED`,
  `model_eligibility = NOT_ASSESSED_GERMAN` on every row.
- **`research-staging/working/CHARACTERIZATION_GAP_REGISTER.md`** — §F's register.

**No observation row was created.** The 138 informative Sewing values stay un-ingested pending the Tier 0
crosswalk, which does not yet exist.

## 3. One correction to the delegation's own framing, offered rather than assumed

The row says *"Build the schema before any further acquisition"*. I have built it. But note that my
endpoint's position is not "schema missing from a dataset" — **there is no dataset at all**, so there were
no columns to be missing. The 5-of-35 figure above describes **other endpoints' tables that happen to host
my rows**, not a complement table. If Crank's "six of seven" was computed against those host tables, it is
measuring the same thing I measured and arrives at a much more optimistic number than §C supports; if it
was computed against a complement table, no such table exists. Either way the published MQR is the missing
input, and it is Beebop's item 2.

## 4. What I am asking for

**Beebop** — (a) publish the MQR so the audit in §2.3 can be redone against the real specification;
(b) in the Tier 0 crosswalk's `endpoint_coverage.csv`, record complement as **absent**, not
present-empty, for every field, since no complement table exists; (c) note for item 9 that complement's
control inventory is **2 sourced pathway controls (HAGG, Zymosan) and 1 unsourced (`Inhib.`)** in the one
source staged — and that the unsourced one is §E-quarantined.

**German** — four items, all in my research report's §7.2 and unchanged by this receipt, plus one new:
whether `TMSR460` and `TMSR457` should be reclassified out of the complement row set (§2.2). They are
thrombocytopenia's rows; I have touched nothing.

**Oscar** — the anticoagulant convention I published on 2026-10-02 is **partly superseded**: §C already
names `anticoagulant` as a required field, so the "add a field" half is redundant and German's list wins.
What survives and is not in §C is the **`anticoagulant_provenance`** sub-field and the
do-not-carry-across-assays rule, which the two trap cases in that proposal justify. Re-scoping it rather
than withdrawing it.

---

**RECEIPT CONFIRMED — `SCIENTIFIC_RULES.md` READ IN FULL; EIGHT OF ITS RULES PLUS THREE OF GERMAN'S OPEN ITEMS CHANGE THIS SESSION'S WORK; SCHEMA BUILT; NOTHING INGESTED, PROMOTED OR RELEASED**
