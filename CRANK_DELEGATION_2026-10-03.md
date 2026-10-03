# Delegation — 2026-10-03

Every open item has exactly one owner. No orphans. If you believe something is yours that is not
listed under you, say so rather than assuming.

Companion files: `SCIENTIFIC_RULES.md` (read first), `German_requests_100326.md`,
`CRANK_DISPATCH_SOURCES_2026-10-03.md`. Directives, the decision record and the source expansion
register are on `claude/crank-phase2-oversight`.

**Standing rule for everyone: acquisition and description run in parallel. Ingestion, promotion
and release are gated** — on the Tier 0 crosswalk for schema, and on German for anything
scientific.

---

## Beebop — package due 2026-10-10

**Blocking, do first**

1. **Harmonized schema proposal** for Oscar. *Generalize German's model; do not redesign it* — his
   **35** named fields and the canonical-oligo-to-observation architecture already exist.
   *(Corrected 2026-10-03: Crank wrote 38. Five independent counts — Beebop, complement, kidney and
   two reviewers — agree on 35: 8 identity/chemistry + 3 characterization + 12 exposure/system +
   10 outcome/adjudication + 2 grouping, no duplicates. Beebop preserved all 35 and declined to
   invent three. That was the correct response.)*
2. **Minimum Qualified Record**, derived from German's published sign-off gates, not invented.
   Submit to German as a derivation of his own criteria.

**Then**

3. **Rights audit, two parts kept separate:** source-file republication, and extracted-data
   reuse. Output is a **proposed-hold list with reasons for Oscar — zero automatic withdrawals.**
   Reconcile thrombocytopenia's rights audit against coagulopathy's treatment of EMA documents.
   Name the three branches carrying no LICENSE.
4. **Tier 0 crosswalk:** `molecule.csv` with `molecule_uid` as **inventory record identifiers**
   (sequence-family links stay candidate and unadjudicated — no silent merges); the controlled
   vocabulary; `endpoint_coverage.csv` with **each of German's twelve gates** as
   present-populated / present-empty /
   absent. **Include a `licence_class` column and a documented switch that regenerates the dataset
   excluding ND-derived rows.**
5. **Corrected endpoint scorecard.** Every figure carries its **denominator and provenance tag**
   (measured-by-me / read-from-generated-artifact / prose-only / Drive-only-unreconciled).
   Evidence split **held / staged / admitted**. Human in-vitro fraction beside every total.
   Characterization reported per column, never collapsed.
6. **Source-version inventory.** Every cited artifact bound to a commit or a versioned Drive file.
   Flag any generated statistic whose `release_id` is `-dirty` or unreachable.
7. **Document skeletons:** narrative ≤12pp, methodology ≤5pp, **PADP ≤5pp** (the five-page limit is
   official and binding — an earlier Crank instruction to ignore it was struck). Placeholder-tagged,
   built on existing endpoint drafts. The narrative must reserve slots for positive and negative
   controls — see item 9.

**Added 2026-10-03 — each is a prerequisite of work already assigned above**

8. **Receipt confirmation, per endpoint.** Confirm each session has read `SCIENTIFIC_RULES.md` and
   state which of its rules change that session's current work. Publishing a file does not make
   anyone read it.
9. **Positive and negative control inventory.** The narrative deliverable explicitly requires both.
   Measured: only acute-neurotoxicity has a `control_role` column, with **0 positive controls of
   1,866**; kidney, hydrocephalus and cns-alternate have no control column at all. **Coagulopathy
   is struck from that list — corrected 2026-10-03: `control_class` is populated on 2,685 of 2,685
   rows across 8 classes, plus a published 108-group controls inventory. Item 7 is unblocked there
   and Crank's stated blocker was false;**
   only thrombocytopenia's `controls_inventory.csv` holds real arms. Item 7 cannot be drafted
   without this.
10. **Assign owners for the three credibility fixes** listed under Rocksteady below. They are
    mechanical, they do not wait on the crosswalk, and they are what a reviewer sees first.
11. **Acquire-once coordination.** One named owner per duplicate source family, keyed on **UNII and
    NCT**; publish the extraction to the endpoints. Eleven scouts duplicated heavily — do not relay
    the source register to nine sessions as nine shopping lists.
12. **Per-regulator licence table**, each term quoted verbatim. "Regulator document = government
    work = public domain" reaches **US federal agencies only**. EMA permits commercial reuse with
    attribution; TGA forbids redistribution without written approval; PMDA is All Rights Reserved.

**Removed from Beebop, taken back by Crank:** German's decision queue (now published as
`German_requests_100326.md`); the uniquely-ND payload computation; the PMDA site-policy fetch.
Beebop supplies per-endpoint evidence on request rather than assembling these.

---

## Rocksteady — by endpoint

**All endpoints, before anything else:** read `SCIENTIFIC_RULES.md`. Flag any endpoint built
one-row-per-oligo rather than at experiment-condition grain — **but re-grain nothing yourself**,
that changes biological meaning and is German's call. Any GSRS data is staged **raw and unparsed**
pending German's stereochemistry ruling.

| Endpoint | Owns |
|---|---|
| **Kidney** | Correct the false "blocked" assertion at `SOURCES.md:12` and `SOURCE_REGISTER.md` §2 — accessdata.fda.gov works with a browser user agent (verified: 420-byte apology page vs 2,181,318-byte PDF). **Do not act on the audit's Directive 5** — it claims 10 staged sequences against the 10 TBD gaps; the id sets intersect at **6**, and promoting everything reaches 61/65, not 65/65. MSR066 awaits German. |
| **Thrombocytopenia** | SafeSense `mmc4.csv` and Sewing 2017 S1. Prepare DEVOTE (NCT04089566) **for German's ruling — do not classify it yourselves**. Audit the **224 of 1,959** rows that are genuinely licence-restricted. *(Corrected: Crank said 984. That figure is the legacy `summary_stat` tag, meaning "a number extracted from a paper" — not a licence finding. Licence-resolved, the decision set is 224, all inside the 984. Crank overstated this endpoint's rights exposure by 4.4x, from the session's own superseded artifact.)* Report modification maps at the dataset-wide denominator (**44/259**), not the 18/34 subset. |
| **Coagulopathy** | Repair stale arithmetic across six shipped files including `METHODOLOGY.md` (states 213 / 2,388 / 941 / 75 against measured **218 / 2,685 / 1,039 / 100**). **Drop or hash the `verbatim_quote` column on 687 rows** — 30,885 words of publisher prose inside a file meant to ship openly; the numbers beside it are unaffected. **Corrected: 21 of 46** headline trials carry a registry id. *(Crank said 18 of 30; both numbers were wrong. The session rebuilt the register from 30 to 46 and its README states "Do not cite 30". Crank read a pre-rebuild document.)* True human in-vitro set is **34 oligos with zero position-resolved chemistry**. |
| **Hepatic** | **Sewing 2016 is the critical path** — the only primary human-hepatocyte source, absent from the repository. The human-hepatocyte lead is **seven constructs, not nine** (corrected 2026-10-03). Burdick's 80-construct panel stages as clearly-labelled **animal** support and is never presented as human progress. |
| **Complement** | **Build the schema before any further acquisition** — six of seven MQR fields have no column in existence. Copy the per-position pattern in `valentin2021_S1_S2_sequences.csv`. Report honestly that **zero human rows carry a numeric complement value**, and that one of the ten rows is not a complement readout. |
| **Immunotoxicity** | **Commit the Drive workbook, or a faithful CSV reduction**, so every figure becomes auditable in one place. Correct the trial-candidate figure: **64 appears in zero cells; the adjudication is 54 approved / 48 hold / 40 support-only.** |
| **CNS — both lineages** | **Stop feeding both.** Prepare the lineage comparison **for German** (rosters, 144 shared sequences, evidence composition, rubric difference, what is lost either way). Fix `_shared/cns/README.md`: it presents 181 compounds as "exactly the in-vitro-to-in-vivo extrapolation the challenge asks for" — **all 181 are animal in-vitro plus animal in-vivo, zero human rows** — and its grade distribution reads 56/87/40/57 against measured **74/81/39/51**. |
| **Hydrocephalus** | **Zero human in-vitro or ex-vivo rows — there is no human-to-animal bridge at all.** Recompute every generated statistic from the committed tree; current `release_id` is `-dirty`, produced from an uncommitted working tree. `PHASE2_COMPLIANCE.md` says 53 "compounds" against `n_compounds_real = 51`. |
| **Cross-branch** | The stale **111-row `measurements.csv` physically ships on five of six branches in two divergent versions.** Any script resolving `data/measurements.csv` by relative path reads the wrong table. The canonical 246-row file exists only on `claude/amazing-galileo-rwiv95`. |

---

## Crank

German's decision queue — **delivered**, `German_requests_100326.md`. Plus: the uniquely-ND payload
computation; the PMDA site-policy fetch; monitoring to the 10 October checkpoint. **And adding
nothing further until that checkpoint** — five directives in one day is already more than this
structure can absorb.

## German

Seven decisions, in `German_requests_100326.md`. Four block work that is otherwise ready.

## Oscar

Relaying to the sessions; the proposed holds when the rights audit returns. The `licence_class`
column proceeds on the stated default.

## Gustavo — not tasked by Crank, and that is a gap

The roles plan gives Gustavo the narrative document, the PADP and predictive-model strategy;
German's v0.9 work orders additionally give him the grouped mechanistic POC outputs, sensitivity
analyses and the model card. **Nothing in this delegation reaches him, because Crank has no
channel to him** — the same gap that exists for German. Items 7 and 9 above produce skeletons and
a control inventory he will need; somebody has to hand them over. Flagging rather than assuming.
