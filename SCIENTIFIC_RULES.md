# Scientific rules — the operative constraints every session works under

**Status: derived reference. Not the authority itself.**

This file exists because the scientific authority for this project lives in German's governance
documents in the shared Drive, while the Rocksteady endpoint sessions work in this repository
and cannot see them. Rules that are invisible to the people following them are not rules. This
file closes that gap.

It is a **derivation**, prepared by Crank and published at Oscar's direction. It states the
operative constraints in a session-usable form. It does **not** reproduce German's documents,
and it carries no scientific authority of its own. Where this file and German's documents
differ, **German's documents win and this file is wrong.** Report the discrepancy rather than
following this file.

**Scientific authority:** German García-Fresco, PhD — Lead Scientist & Domain Expert.

**Derived from** (internal, Drive, not redistributed here):

| Document | Version / date | Standing |
|---|---|---|
| OligoTox Immunotoxicity Scientific Validation & ML Correction Memo | v0.1, 24 Aug 2026 | Decision: **major scientific revision required**; no sign-off |
| OligoTox Thrombo Scientific Governance and Model Readiness | v0.9 | Scientist release candidate; **final public freeze not granted** |

If you need the underlying documents, ask Oscar. Do not work around their absence by guessing
what they say.

---

## A. The agent contract — binds Crank, Beebop and every Rocksteady session

German defines the AI role on this project as **dormant raw-transfer**, activated only once a
verified local structured source exists with a recorded checksum. Within it, no agent may:

- assign toxicity labels;
- infer or impute missing values;
- manufacture negatives;
- resolve scientific conflicts;
- train or claim a model that German has not permitted.

Permitted: transfer rows into a locked staging schema, preserve source row lineage, generate an
exception queue, and report.

**This contract outranks any instruction from Crank or Beebop.** If a directive appears to
conflict with it, the contract wins — stop and escalate. No deadline justifies crossing it.

## B. Unit of observation — the rule most of our data violates

The primary evidence unit is:

> **oligo × chemistry × strand state × dose × time × donor / cell system × delivery condition ×
> endpoint**

**Not one row per oligo.** An oligo-level summary is *derived afterwards*, never curated as the
primary record.

Architecture: a **canonical oligo table** holding identity, sequence and chemistry, **linked to
an experimental-observation table**. Keep them separate.

Required lineage, end to end, for every model-eligible row:

> model row → model-eligibility decision → scientific interpretation → observed measurement →
> experimental / clinical condition → biological system / population → exact oligo construct and
> position chemistry → exact source location and source URL

If your endpoint is built one-row-per-oligo, **say so — do not silently re-grain it.** Re-graining
changes biological meaning and is German's decision.

## C. Minimum schema fields

Encode chemistry **by position**, not as molecule-level flags. Coarse flags such as `is_LNA` are
permitted only as secondary derived variables — never as the primary encoding, and never as a
causal feature.

Identity and chemistry: `sequence_5to3`, `strand_role`, `duplex_partner_id`,
`backbone_by_linkage`, `sugar_mod_by_position`, `base_mod_by_position`,
`terminal_modifications`, `gap_length_nt`.

Characterization: `purity_pct`, `identity_method`, `endotoxin_level`.

Exposure and system: `formulation`, `delivery_agent`, `anticoagulant`, `dose_value`,
`dose_unit`, `exposure_time_h`, `cell_system`, `cell_subset`, `species`, `donor_id`,
`donor_class`, `sample_state`.

Outcome and adjudication: `endpoint_name`, `raw_value`, `raw_unit`, `author_interpretation`,
`curator_label`, `immunomodulatory_direction`, `receptor_pathway`, `mechanism_evidence_type`,
`clinical_anchor`, `evidence_confidence`.

Grouping (see §G — these must exist from the start): `sequence_family_group`, `paper_group`.

Endpoints will need fields beyond this list. Adding is fine; **dropping one because your
endpoint finds it inconvenient is not** — that is a question for German.

## D. Evidence classification

Human and animal observations are **never pooled as interchangeable ground truth.** Keep human
clinical, human ex vivo / laboratory, and animal in separate lanes, and keep intended
pharmacology separate from adverse toxicity.

Evidence tiers (GOLD / SILVER / BRONZE, scored per lane) describe **completeness and
directness only**. A tier is **not** a toxicity label, **not** a safety statement, and **not**
model eligibility. A GOLD record may be positive, negative, mixed or endpoint-specific. A
scientist override always outranks automated completeness scoring.

Review articles are source-discovery and mechanism references. They are **not** quantitative
training ground truth without their primary sources.

## E. Label and control rules

These are the rules that decide the hard cases. Learn the named traps.

- **Unreported is not negative.** Use `UNKNOWN` / `HOLD` unless monitoring and denominator are
  explicit. **Do not manufacture a balanced class.**
- **A clean clinical negative** requires all of: exact sequence, human exposure, adequate dose
  and duration, explicit monitoring, an explicit outcome, and a traceable denominator. A
  no-event mention, or absence from an adverse-event table, is **not** a negative.
- **Intended pharmacology is not toxicity.** Deliberate inhibition of vWF, thrombin, factor
  IX/XI or platelet function is not an adverse label by default.
- **Therapeutic correction is not toxicity.** A platelet count rising because disease-associated
  thrombocytopenia is being corrected must not be labelled oligo-induced thrombocytopenia.
- **Non-stimulatory is not safe.** Separate `agonist` / `antagonist` / `potentiator` /
  `inert-low-response` / `mixed` / `unknown`. Active antagonists are not ordinary negatives.
- **Keep author result and curator label separate.** Binary calls are marked curator-derived
  unless the source explicitly defines them. Retain raw/continuous values, units, fold change,
  significance and author interpretation.
- **No universal thresholds.** Fixed cytokine cutoffs are not general label rules; store
  source-specific thresholds and use benchmark-relative ranking against known controls.
- **No universal chemistry rules.** Modification effects depend on modified base, exact
  position, strand, sequence, receptor and delivery context. Do not encode "2′OMe above X% is
  safe", "LNA increases TLR9 risk", or "CpG methylation abrogates TLR9" as rules — all three are
  contradicted by evidence in the corpus.
- **Do not collapse distinct outcomes.** Platelet-count decline, platelet activation,
  coagulation, bleeding and thrombosis are separate endpoints with separate biology. Likewise
  keep receptor- and cytokine-specific outcomes separate; a composite is a secondary derived
  field only.
- **Do not map in-vitro fold-change bins to clinical severity grades** (e.g. CTCAE) unless
  clinically validated. Call it experimental response severity.
- **Unsourced controls are not training rows.** A control enters training only when its
  sequence, chemistry, assay and measured outcome are sourced. Proposed or synthetic controls
  belong in a separate design table.

## F. Missingness

Where sources do not supply analytical identity or purity, those fields **must remain
`NOT_REPORTED`** unless primary CMC, synthesis, HPLC, MS, CGE or lot-level records are
recovered. `NOT_REPORTED` is the **correct value**, not a failure state. Never substitute an
inferred, typical or group-level value for a per-batch one.

Alongside it, record in the **Characterization Gap Register** what is missing, why, what was
attempted, and what would close it. The field value and the register are both required: the
value states the truth, the register discharges the requirement.

Calibration: German reports **zero** of 45 thrombo oligo/product records with a usable purity
value or complete identity method. Plan for disclosure, not rescue.

## G. Leakage and validation

**Random row splitting is prohibited.** Grouped splits are required — by sequence family and
near-neighbour, by paper and laboratory, by matched pair, and by experimental series.

Observed symptom in the corpus: ~0.94 AUC on random/held-out splits against ~0.65 leave-one-paper-out.
Report LOPO and grouped performance prominently, with uncertainty. Do not describe internal AUC
as clinical accuracy.

Shared-sequence grouping must **not** merge chemically distinct administered constructs.
Reference identity is not experimental-batch identity: same base sequence can differ by
sugar/base/linkage position, strand, conjugate, stereochemistry and formulation.

Complex models must beat transparent baselines (null/majority, length-only, chemistry-only,
family-only). Report failed or degenerate folds rather than replacing them.

## H. Release state — check before you build

| Item | State |
|---|---|
| Final public dataset freeze (thrombo) | **NOT GRANTED** — German grants it |
| Sequence-only clinical thrombocytopenia classifier | **BLOCKED** — zero clean sequence-linked clinical negatives. No one may train or claim it |
| Human mechanistic platelet-interaction POC | Conditional, under a locked protocol, grouped splits only |
| Immunotoxicity ML dataset / report | Major revision required before sign-off |
| Matched-context analyses | Descriptive only, with causal limitations stated |

Permitted language is governed: exploratory findings are described as exploratory within the
curated panels. Claims of clinical prediction, clinical-grade accuracy, or universal causal
feature rules are prohibited.

## I. Known source corrections

Carry these; do not re-derive them.

- Dataset key `Peacock_2009` is a misattribution — the source is **Goodchild 2009** (PMID
  19630977). Rename or alias.
- A file circulating as "Hornung 2005" is in fact **Herzner et al. 2015** (cGAS / Y-form DNA).
  Do not use it as a Hornung source.
- Riera-Tur 2024 DOI is `10.1089/nat.2024.0013`; Fucini DOI is `10.1089/nat.2011.0334`;
  Lenert PMID is `20490286`.
- Sources whose per-row provenance is unresolved stay excluded from validated training data
  until matched — not auto-resolved.

## J. What this file does not settle

Endpoint definitions, phenotype and control assignments, scientific labels, evidence tiers,
model eligibility, disputed records, and the final dataset/model freeze are German's. Schema
implementation, engineering and release mechanics are Oscar's. Priority and sequence are
Crank's.

If following this file would require you to make a scientific judgment, that is the signal that
you have reached the edge of it. Stop and escalate.
