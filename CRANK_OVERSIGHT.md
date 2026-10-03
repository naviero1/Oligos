# Crank — Phase 2 oversight tracker

Maintained by Crank, the supervisory layer above Beebop (coordination) and Rocksteady
(per-endpoint execution). Opened 2026-10-03 at Oscar's instruction. Reports to Oscar.

**What this file is:** the standing record of where Phase 2 stands against its end product,
what each toxicology owes, which decisions are open, and what was directed in each round. It
is an oversight and tracking layer. It holds **no measurement, sequence, label or citation of
its own**, and it does not supersede German's scientific authority or Oscar's schema and
release authority.

**Provenance of every number below:** figures are Beebop's recounts and reported values from
`BEEBOP_RESEARCH_ROUND_2026-10-02.md` and the endpoint dossiers under `toxicity/`. Crank has
**not** independently re-extracted primary sources. Where Beebop marked a count
*generated/reported* rather than recounted, that status is carried through here. A number in
this file is a management figure, not a scientifically qualified claim.

---

## 1. The end product Phase 2 is judged on

Source: `Phase 2 description.docx` (Drive) and
`toxicity/_shared/reference/OligoTox_challenge_brief.pdf` (pages 1–3a only; see the scope
caveat in `toxicity/README.md`).

Four parts, one dataset:

| # | Deliverable | Limit | Human lead |
|---|---|---|---|
| 1 | **Narrative** — exec summary, positive/negative controls, findings, how data were produced, predictor-variable measurement and distribution, the public-data gap addressed, how the data support a predictive model | ≤12 pp PDF | Gustavo |
| 2 | **Methodology** — materials and methods, **including methods used to purify and characterize oligo identity** | ≤5 pp PDF | German |
| 3 | **PADP** — open non-exclusive research licensing, dissemination, fallback scenarios incl. US-government utilization | ≤5 pp | Gustavo |
| 4 | **Dataset** — data dictionary + schema + raw data; **per oligo: sequence, location of every chemical modification, purity and characterization data, plus metadata**; openly licensed (e.g. Creative Commons) | no page limit | Oscar |

Optional and scored favourably: code documentation, interactive notebooks, tutorials.

### The three non-negotiables

1. **In vitro human systems are the priority.** The announcement states datasets based on
   in vitro human systems, or able to extrapolate between in vitro human systems and animal
   data, are of particular interest. Animal mass is support, not headline.
2. **Per-oligo sequence, modification location, purity and characterization are mandatory
   dataset contents**, not optional columns.
3. **Open public availability is a condition of eligibility.** Access terms must be defined
   and open.

### Eight toxicities of interest (verbatim scope)

Hepatotoxicity, kidney toxicity, thrombocytopenia, complement activation, coagulopathy,
immunotoxicity, chronic neurotoxicity, hydrocephalus. Acute neurotoxicity is explicitly
**lower priority** and is carried only as a supporting module.

### Calendar reality

`Phase 2 Work-Plan.xlsx` runs endpoint data generation May→October, then:
**November = the four deliverables. December = buffer.** As of 2026-10-03 we are roughly four
weeks from assembly.

---

## 2. Strategic posture — decided 2026-10-03

**Posture: maximize breadth.** Oscar's call. All eight endpoints are driven toward
qualification in parallel; no endpoint is demoted to appendix on scope grounds.

Crank had recommended consolidating to a defensible core. Oscar chose breadth. That decision
is recorded, accepted, and is not reopened here. What follows is the strategy for making
breadth converge rather than fragment.

**Consequence of the posture, stated plainly once.** Breadth across eight endpoints in four
weeks means the qualification bar is a published floor (the Minimum Qualified Record, §4),
not completeness; and the submission's credibility rests on **rigorously documented
missingness** rather than on full characterization coverage. Both are accepted costs of the
chosen posture.

**What breadth changes about the binding constraint.** Under consolidation the constraint
would have been depth. Under breadth it is **convergence**: eight parallel streams produce one
submission only if they share one schema, one counting convention, one missingness
convention, and one release discipline. Absent those, breadth yields eight incompatible
tables and no submission. Convergence work therefore outranks new discovery.

---

## 3. Where each toxicology stands

**Independently measured 2026-10-03** by a nine-endpoint audit commissioned by Crank: one
auditor per endpoint reading its branch directly, each adversarially verified by a second
agent, plus three synthesis agents. 21 agents, no failures. Figures below are measured from
data files unless marked otherwise. Where the audit and Beebop disagreed, the adjudication is
recorded in §9.

| Endpoint | State | Measured mass | Binding blocker |
|---|---|---|---|
| **Kidney** | Only endpoint with a full four-part dossier | 65 oligos / **246 rows** (67 human in-vitro, 81 animal in-vitro, 56 animal in-vivo, 42 clinical); 55/65 sequences | **55.7% animal**; largest single class is animal in-vitro, not human. The 67 human in-vitro rows rest on **11 oligos, 48 of them (72%) from one patent table spanning 3 oligos**. **0/65 purity. No modification-position column exists; PS linkage positions 0/65** |
| **Thrombocytopenia** | Large, scientifically frozen | 229/259 identifiers / 1,959 rows; 451 human-lab, 1,002 clinical, 497 animal; 200/259 sequences | German blocks the clinical sequence classifier (zero clean sequence-linked clinical negatives); **modification maps 44/259 (17%)**; **0/259 purity**; **984/1,959 rows (50.2%) shipped in a submission workbook under terms that forbid redistribution** |
| **Coagulopathy** | Largest dataset; release documents stale | 207/218 identifiers / 2,685 rows; 1,183 human, 1,476 animal, 26 undetermined | **Only 18 of the 30 headline trials carry a registry id**; true human in-vitro set is **34 oligos with 0 position-resolved chemistry**; **0/218 purity**; METHODOLOGY.md and five other files ship stale arithmetic (213/2,388/941/75 vs measured 218/2,685/1,039/100) |
| **Chronic neurotoxicity** | **Two rival datasets, not two views** | original 2,335 rows × 44 cols, 13 oligos; alternate 2,393 rows × 33 cols, 573 oligos | Different rosters, column sets and grade columns (`cns_tox_grade` vs `neurotox_grade`). Choosing one is a **scientific adjudication, not a schema decision**, and it must precede migration |
| **Hydrocephalus** | Exists **three** times | dedicated 1,342 rows × 55 cols (47 compounds); alternate 145; cns-original 12 | **0 human in-vitro and 0 human ex-vivo rows — no human-to-animal bridge at all**; 35/41 human compounds lack sequence and modification map; 41/41 lack purity; generated stats carry release_id `…-dirty` (produced from an uncommitted tree) |
| **Immunotoxicity** | **Evidence is real but lives outside git** | Drive workbook: 15 sheets, 142 catalog records / 141 identifiers, 33 observations, 20 papers. Git: **0 measurement rows** | The governing workbook is **not in version control**, so no immunotoxicity figure is auditable in-repo. Git dossier says "This project extracted no immunotoxicity data" |
| **Hepatotoxicity** | Pre-ingestion | **0 rows.** 9 blobs (4 markdown, 5 PDFs), zero machine-readable data | All 17 extractable per-oligo records are **mouse in vivo**. Sewing 2016 — the only primary human-hepatocyte source — is absent from the repository |
| **Complement activation** | Pre-ingestion | **0 ingested rows.** One 144-row staging CSV its own README calls "not an ingestion" | **6 of 7 MQR fields have no column in existence.** Of the 10 complement rows, **0 human rows carry a numeric value**; one of the 10 is not a complement readout at all |

### Cross-cutting data-model fact that constrains breadth

Kidney's model is kidney-shaped by construction: `is_kidney_specific` is TRUE on 111 of 111
legacy rows and carries no information, and `nephrotox_grade` has a rubric written entirely in
renal terms. **A seven-endpoint register cannot be produced by re-slicing the kidney tables.**
Each endpoint needs its own graded outcome column and its own written rubric, inside a shared
schema. This is the technical reason §4.1 is blocking.

---

## 4. The breadth convergence plan

Six pillars. P1 and P2 are blocking: nothing else converges until they land.

### 4.1 — P1 (blocking): freeze the harmonized schema

One data model all eight endpoints write into. Shared core entities (oligo / construct and
chemistry / source / study-experiment / observation / provenance), one shared evidence-class
vocabulary, and a **per-endpoint graded outcome column each carrying its own written rubric**.
Owner: Oscar — this is his assigned role (dataset schema and data dictionary). Beebop's job is
to assemble the cross-branch column inventory and propose the harmonization. Until this is
frozen, every parallel endpoint stream is accruing rework.

### 4.2 — P2 (blocking): publish the Minimum Qualified Record

Breadth cannot mean perfection everywhere, so the floor must be explicit and public. A row
ships only if it carries:

1. a resolvable oligo identifier;
2. sequence present, **or** explicitly flagged absent with a reason;
3. modification positions mapped, **or** explicitly flagged absent with a reason;
4. purity/characterization value, **or** a documented recovery attempt plus an explicit
   missingness reason;
5. an evidence class from the shared vocabulary (human in vitro / human ex vivo / human
   clinical / animal / unresolved);
6. provenance to a registered `source_id` with a locator;
7. an endpoint outcome plus the rubric it was graded under.

Rows below the floor go to a labelled staging tier. They never enter headline counts and never
enter the released dataset unlabelled. Reference identity is not experimental-batch identity;
shared-sequence grouping must not merge chemically distinct administered constructs.

### 4.3 — P3: the critical path is the three thin endpoints

Hepatic (0 rows), complement (0 rows) and immunotoxicity (catalog that does not join) are the
only endpoints that can make breadth fail outright. They get first call on effort, bounded
named targets rather than open research, and a shorter reporting cadence:

- **Hepatic** — the nine human-hepatocyte constructs to qualified rows. Burdick's 80-construct
  panel is staged as clearly-labelled animal support, never presented as human progress.
- **Complement** — human whole-blood / serum complement assay files; the Sewing raw-file
  acquisition is shared with thrombocytopenia so the effort is paid once.
- **Immunotoxicity** — fix compound→observation linkage *first*. A 142-record catalog that
  joins one identifier yields approximately zero trainable rows; linkage, then raw
  cytokine/receptor outcomes with donor and assay context for constructs already held.

### 4.4 — P4: cut the duplicate CNS lineage

Two parallel nervous-system lineages are duplication, not breadth, and they are the one place
breadth still requires a cut. Run the source/construct/observation crosswalk, pick the
authoritative lineage, archive the other as a frozen lineage. Human-lab compound coverage
already differs across them (13 original vs 39 alternate identifiers) and **no branch totals
may be added**. Acute neurotoxicity remains a supporting module per the brief's explicit
deprioritization; it does not receive breadth budget.

### 4.5 — P5: start the three documents now, not in November

The highest-leverage deadline move. Narrative, methodology and PADP are drafted **now**,
against the frozen schema, with named numeric placeholders, so that November is number-landing
and editing rather than writing. Beebop produces a placeholder-tagged skeleton for each so
every figure has a slot waiting for it. Leads per the roles plan: Gustavo narrative + PADP,
German methodology, Oscar schema/dictionary and the optional notebook.

### 4.6 — P6: make documented missingness the differentiator

Purity coverage is at or near zero across every endpoint, against a brief that names purity and
characterization as mandatory. The answer is not to hide it and not to invent it. Build a
**Characterization Gap Register**: per oligo, what is missing, why, what was attempted, and
what would close it. This satisfies the narrative's required "gap in publicly available data"
discussion, protects against overclaiming, and is a genuine contribution in its own right.
Standing rule for Rocksteady: **documented absence beats silent `NOT_REPORTED`, and both beat
fabrication, always.**

### 4.7 — Governance carried forward unchanged

- **Release identifiers.** One canonical branch per endpoint; every accepted dataset, source
  inventory, figure and document bound to a frozen release tag. Cross-branch version drift is
  a live defect, not a cosmetic one.
- **Counting discipline stays exactly as Beebop has it** — human trials vs human laboratory vs
  animal kept separate, trials counted once across registry/papers/labels/outcomes, no summing
  of overlapping participant denominators, animal evidence in separate supporting tables. It is
  correct and it matches the challenge's own priority. Extend it into the shared schema.
- **Authority is unchanged.** German holds endpoint definitions, phenotype and control
  decisions, scientific labels, qualification and freeze authority. Oscar holds schema,
  engineering and release authority. Implementation remains gated on Oscar's authorization;
  research rounds do not settle scientific questions.

---

## 5. Deliverable readiness

| Deliverable | Status | Gap to close |
|---|---|---|
| Dataset | Kidney only is assembled; seven endpoints range from large-but-unqualified to empty | harmonized schema (§4.1), MQR applied across all eight (§4.2), release tags |
| Narrative ≤12 pp | kidney-scope `PRESENTATION.md` exists; no cross-endpoint narrative | skeleton with placeholders now (§4.5); cross-endpoint findings and controls |
| Methodology ≤5 pp | kidney `METHODOLOGY_PHASE2.md` exists | must cover purification and characterization across every endpoint that ships |
| PADP ≤5 pp | kidney `PADP.md` exists | licensing settlement: NC clause on 758 rows, 224 rows awaiting Oscar's call |
| Optional notebook | not started | depends on frozen schema |

---

## 6. Open decisions

| # | Decision | Owner | Status |
|---|---|---|---|
| D1 | Harmonized cross-endpoint schema and data dictionary | Oscar | **open — blocking** |
| D2 | Minimum Qualified Record floor ratified | Oscar + German | **open — blocking** |
| D3 | Authoritative CNS lineage after crosswalk | Oscar | open |
| D4 | Open-licence terms; NC clause on 758 rows; 224 rows | Oscar | **partly resolved 2026-10-03** — see `CRANK_DECISIONS_2026-10-03.md`. Facts-not-expression basis adopted project-wide; PMDA facts-only; TGA retry then stop; Elsevier grant recorded verbatim as `conditional_publisher_grant`. Per-row holds still pending the two-part rights audit |
| D8 | **Phosphorothioate stereochemistry — are stereoisomers distinct constructs, and may they be pooled?** | **German** | **open — blocks GSRS ingestion and the schema's chemistry representation** |
| D9 | **Does DEVOTE (NCT04089566) pass all seven clean-negative gates?** | **German** | **open — blocks the clinical classifier German has frozen** |
| D5 | Kidney MSR066 — favourable renal result as confirmed negative | German | open |
| D6 | Thrombocytopenia clinical sequence classifier (blocked: no clean sequence-linked clinical negatives) | German | open |
| D7 | Shared trial/extension counting convention across endpoints | Oscar + German | open |

---

## 7. Round log

| Date | Round | Artifact |
|---|---|---|
| 2026-09-30 | Beebop suggestions to Rocksteady, nine endpoints | `BEEBOP_HANDOFF_INDEX_2026-09-30.md` |
| 2026-10-01 | Beebop review requests; implementation held pending Oscar | `BEEBOP_REVIEW_ROUND_2026-10-01.md` |
| 2026-10-02 | Beebop research requests, twelve published; inventory audit | `BEEBOP_RESEARCH_ROUND_2026-10-02.md` |
| 2026-10-03 | **Crank directive 001** — breadth convergence plan | `CRANK_DIRECTIVE_001_2026-10-03.md` |

---

## 8. Standing caveats

- Publishing a file does not launch, control or oblige any Claude Code session. Work requested
  is not work completed.
- A source file, a populated field or a finished narrative does not establish scientifically
  qualified data or challenge compliance.
- Measurement rows are not independent experiments, patients or donors. Compound counts are
  recorded identifiers unless molecular deduplication is established.
- No branch totals are added across lineages.

---

## 9. Independent audit, 2026-10-03

Crank commissioned a nine-endpoint audit reading the six branches directly: one auditor per
endpoint, each adversarially verified by a second agent instructed to refute rather than agree,
plus a schema architect, a reasoning auditor and a completeness critic. 21 agents, no failures.

### 9.1 Verdict on Beebop's reasoning: **sound, with reservations. Do not bypass.**

Beebop's arithmetic reproduces **wherever a file was reachable** — nine adversarially verified
audits found zero numerical discrepancies in its reachable figures. Its provenance labelling
("recounted" / "reported" / "generated" / "directly read", and saying outright which tables it
could not recount) is the most valuable thing in the baseline and is what made this
adjudication possible at all. It refused to sum overlapping inventories and was right every
time tested; it rejected a subordinate's prose figure in favour of a measured one; it declined
to state a coagulopathy trial total it could not defend **and was vindicated** (30 headline
flags, only 18 with a real registry id); and it caught a live front-door misstatement of the
challenge's central priority that no auditor tested.

**One genuine arithmetic error reached Crank:** 875 position records against a measured 831 —
a Drive-sourced figure Beebop itself had flagged as unreconciled, restated with the caveat
stripped. Beebop applied its own Drive-reconciliation rule to everyone except itself.

**The structural reservation** is compression loss between Beebop's per-endpoint requests
(rigorous, correctly denominated) and its round-doc summary to Crank (denominators dropped,
dataset-wide coverage replaced by the flattering priority subset, caveats stripped). Every
confirmed Beebop error is a summary-layer artifact, not an analysis-layer one.

**Direction of bias:** Beebop under-reports weakness rather than over-reporting strength, and
never inflated a reachable count. Evidence classes are never mixed. The bias is in *salience
and denominator choice* — and because every figure carries an honest provenance tag, it is
visible and correctable rather than concealed.

**Remedy, cheap:** every summary figure carries its denominator and provenance tag (Beebop
already produces both one layer down), and no Drive-sourced figure is restated until
re-measured against the repository.

### 9.2 The audit layer itself needs a correction pass

Crank cannot treat these audits as a clean check on Beebop. Several erred **in Beebop's
direction**: the coagulopathy audit "confirmed" the 30 headline trials with a whole-table
registry count; the thrombocytopenia verifier cleared Beebop of the 875 error by grepping the
wrong file; the cns-original audit asserted a PADP page limit that exists nowhere; the
cns-alternate audit charged Beebop with leaving rows unaccounted that Beebop's own text
accounts for. **Beebop's numbers survived this scrutiny better than the scrutiny did.**

**Do not act on the kidney audit's Directive 5.** It claims a staging file holds 10 candidate
sequences against the 10 TBD gaps; the id sets intersect at **6**, four staged rows target
oligos that already carry sequences, and two are flagged for German's adjudication. Acting on
it would push chemistry changes through as gap-filling. It is an audit claim, not a Beebop
claim.

### 9.3 P1 reassessed: a single harmonized schema across eight endpoints is **not achievable** by November

The schema architect's verdict is no, for three independent reasons, each sufficient on its own:

1. **Three endpoints have nothing to migrate.** Hepatic, immunotoxicity and complement hold
   zero ingested measurement rows between them. For these the work is greenfield population
   plus evidence acquisition plus writing a rubric from nothing — months, and gated by source
   availability outside anyone's control.
2. **Two endpoints have rival implementations with no canonical version.** Chronic neurotoxicity
   exists twice and hydrocephalus three times, with different rosters, columns and grade
   columns. Choosing is a scientific adjudication that must precede migration.
3. **The mandatory characterization field is 99.9% absent.** `purity_pct` holds a real value on
   **3 of 3,034** oligo rows project-wide, all three animal-only rat constructs. A harmonized
   schema makes that legible; it cannot make it go away.

**What is achievable, and it is substantial:** a **five-endpoint harmonized register** over the
endpoints that hold adjudicated rows — kidney, thrombocytopenia, coagulopathy, hydrocephalus,
and one chosen chronic-neurotoxicity lineage. Roughly **8,567–8,625 measurement rows and
1,118–1,168 oligo records**, all measured.

**Adopted fallback — three tiers, each independently shippable:**

- **Tier 0 — crosswalk only (week 1, ~5 days, zero risk, changes no existing file).** Ship
  `molecule.csv` with a `molecule_uid` over all 3,034 roster rows; the controlled-vocabulary
  document; and `endpoint_coverage.csv` stating, per endpoint, measured rows, measured oligos,
  subject-class distribution, rubric name or none, and each MQR field as
  present-populated / present-empty / absent. **This is what actually unblocks November**,
  because assembly needs a defensible cross-endpoint statement, not one physical table — and it
  makes the three empty endpoints and the two rival datasets *declared facts* rather than gaps a
  reviewer discovers.
- **Tier 1 — view layer (weeks 2–4, reversible).** One adapter per endpoint emitting harmonized
  views; source CSVs untouched; each adapter must reproduce its endpoint's published row count
  exactly before its output is accepted. Coagulopathy is the reference implementation (~2 days,
  closest to the target model).
- **Tier 2 — in-place migration. Post-November.** This is where the released-document blast
  radius lives; not under deadline.

Note this preserves the breadth posture: all eight endpoints appear in Tier 0, five of them with
a harmonized register behind them.

### 9.4 Findings that outrank the schema work

- **Licensing is an eligibility risk, not a quality risk.** **Three of six branches carry no
  LICENSE file at all** (coagulopathy, thrombocytopenia, cns-alternate). Worse, material under
  non-redistributable terms is **already shipped inside submission files**: thrombocytopenia
  ships 984/1,959 rows (50.2%) classed `summary_stat` — which the project's own LICENSE.md
  defines as CC BY-NC-ND and "not offered for redistribution as dataset content" — inside
  `submission/OligoTox-Thrombocytopenia_dataset.xlsx`; coagulopathy ships 254
  publisher-restricted plus 426 CC BY-NC-ND rows. Phase 2 requires an openly licensed dataset.
- **Leakage is already in a shipped split.** `acute-neurotoxicity/data/oligos.csv` ships a
  published train/test split in which **48 of 148 test oligos share an exact sequence with a
  training oligo**, and 115 of 148 are contained in or contain a training sequence.
- **The real sample size is ~25 molecules, not thousands of rows.** Distinct oligos that are
  human-lab **and** graded **and** sequence-bearing: thrombocytopenia 25, coagulopathy 19
  (strictly human in-vitro 7), cns-alternate 13, kidney 7, cns-acute 7, hydrocephalus 0.
- **Purity data exists after all — in Drive, not git.** The immunotoxicity catalog carries real
  analytical characterization on 5 records (~94–99% by IE-HPLC/RP-HPLC/CGE, identity by
  MALDI-TOF, endotoxin <0.075 EU/mg) and **modification positions populated on 41/142**. Harvest
  before describing purity as universally absent.
- **The stale 111-row kidney table is a real file, not stale prose.** Five of six branches
  physically ship an 111-row `measurements.csv`, in **two mutually divergent versions**. Any
  script resolving `data/measurements.csv` by relative path on those branches reads the wrong
  table. The 246-row canonical version exists only on `amazing-galileo`.
- **The CNS front door misstates the challenge's central priority.** `_shared/cns/README.md`
  presents 181 paired compounds as "exactly the in-vitro-to-in-vivo extrapolation the challenge
  asks for"; all 181 measure as animal in-vitro plus animal in-vivo, rat and mouse, **zero human
  rows** — while the same README's line 131 concedes the dataset cannot extrapolate between
  human in-vitro and animal systems. Its grade distribution is also wrong (56/87/40/57 stated
  against 74/81/39/51 measured). A reviewer opens the README first.
- **Positive controls are largely absent**, and the narrative deliverable explicitly requires
  them. Only acute-neurotoxicity has a `control_role` column (0 positive controls of 1,866);
  kidney, coagulopathy, hydrocephalus and cns-alternate oligo tables have no control column at
  all. Only thrombocytopenia's `controls_inventory.csv` holds real positive and negative arms.
- **197 sequences appear in two or more endpoint datasets** with no crosswalk for most pairs
  (coagulopathy↔thrombocytopenia has none).

### 9.5 Beebop was right about immunotoxicity and was disbelieved

Nine audits scoped themselves to git and concluded the endpoint is empty. The completeness
critic opened the Drive workbook directly: it reads cleanly — 15 sheets, 142 catalog records,
141 identifiers, 33 observations at Human 30 / Mouse 2 / Multiple 1, 20 papers. **Beebop's
baseline was accurate.** One figure needs correcting: Beebop's 64 trial candidates appears in
zero cells; the adjudication is 54 approved / 48 hold / 40 support-only.

The lesson is the one already recorded in §9.1 and in Directive 001-A: the Drive/git divergence
is the governing risk on this project, and it has now produced errors in both directions — one
in Beebop's figures, and one in nine auditors concluding an endpoint was empty when its evidence
simply lived elsewhere.
