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

Status as of the 2026-10-02 Beebop round. "Qualified" means meeting the Minimum Qualified
Record in §4 — which is new, so no endpoint is yet assessed against it.

| Endpoint | State | Reported mass | Binding blocker |
|---|---|---|---|
| **Kidney** | Only endpoint with a full four-part dossier | 65 oligos / 246 rows recounted; 67 human-lab, 137 animal | 0/65 purity values; MSR066 favourable renal result currently treated as a confirmed negative, pending German |
| **Thrombocytopenia** | Large, scientifically frozen | 229 of 259 identifiers / 1,959 rows; 451 human-lab, 1,002 clinical, 497 animal | German reports zero clean sequence-linked clinical negatives and blocks the clinical sequence classifier; 0/34 purity; SafeSense quarantined; 224 rows need a licensing decision |
| **Coagulopathy** | Large, counts defective | 207 of 218 identifiers / 2,685 rows; 431 human-lab, 749 participant rows, 1,476 animal | study/arm attribution and intended-pharmacology exclusion unresolved; headline trial total not defensible; 0/38 purity |
| **Chronic neurotoxicity** | **Two competing lineages** | original 2,335 generated; alternate 2,393 recounted (incl. 931 acute) | duplicate lineages not reconciled; chronicity not established by registry outcomes; 0/21 purity and identity |
| **Hydrocephalus** | Dedicated set exists, counts conflict | 47 reported / 53 roster; 1,342 generated (older reply said 1,361); 0 human-lab | count reconciliation; 127 absence-only register rows must not inflate the 27 assessed/observed; 0/41 purity |
| **Immunotoxicity** | Rich catalog, **not yet trainable** | 141 identifiers / 142 catalog records; 33 narrative observations | compound→observation linkage broken: **1 identifier literally joins**, and that result is qualitative. Drive folder empty |
| **Hepatotoxicity** | Sources held, nothing ingested | **0 dedicated rows** | Burdick panel is animal-only (80 constructs); nine human-hepatocyte constructs await source-table verification. Drive folder empty |
| **Complement activation** | Background only | **0 dedicated rows** | no dedicated source table; proposed 19-study pool unreconciled. Drive folder empty |

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
| D4 | Open-licence terms; NC clause on 758 rows; 224 rows | Oscar | open |
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
