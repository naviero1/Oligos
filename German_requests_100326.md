# German — decisions required

**2026-10-03 (10/03/26).** Seven open items. Each blocks work that is otherwise ready.
Nothing here asks you to produce data; each asks for a ruling only you hold.

Prepared by Crank (Phase 2 oversight). Evidence is measured from the repository unless marked
otherwise. Where a figure is generated or reported rather than recounted, it says so.

---

## 1. CNS lineage — which dataset is authoritative

**Why.** Chronic neurotoxicity exists as two parallel datasets. They cannot both ship, and no
schema migration can begin until one is authoritative.

**Context.** They are not two views of one dataset. Original: 2,335 rows × 44 columns, 13 oligos,
grade column `cns_tox_grade`. Alternate: 2,393 rows × 33 columns, 573 oligos, grade column
`neurotox_grade`. Different rosters, different column sets, different grade distributions; 144
exact sequences shared. Hydrocephalus exists three times over (dedicated 1,342 rows; alternate
145; cns-original 12).

**Needed.** Which lineage is authoritative; whether the other is archived or merged; and if
merged, on what basis the two grade columns reconcile.

**Blocks.** Schema migration for CNS and hydrocephalus. Any cross-endpoint row count.

---

## 2. Thrombocytopenia freeze — which of the six blockers still bind

**Why.** Your v0.9 records the final public dataset freeze as **NOT GRANTED** with six mandatory
blockers. Nothing releases until each is closed or explicitly waived.

**Context.** The six: (i) no clean sequence-linked clinical comparator strategy; (ii) SafeSense
and Sewing structured files not locally available; (iii) analytical identity and purity absent
from all 45 oligo records; (iv) relational implementation and deterministic export tests
incomplete; (v) grouped POC outputs, sensitivity analyses and model card not returned; (vi)
repository, persistent identifier, executed licence, preservation plan and release audit open.
New since v0.9: we have now established that numeric release purity is **systematically withheld
by every regulator** — FDA redacts as `(b)(4)` (56 redactions in the inotersen review, 84 pages
withheld in tofersen), EMA deletes commercially confidential information, PMDA masks with
asterisks. Blocker (iii) may be unclosable from public sources.

**Needed.** Which blockers remain binding today, and which may be discharged by **documented
missingness** rather than closure — specifically whether (iii) is satisfied by populating
`purity_method` and `identity_confirmation` while recording `purity_pct` as withheld-with-evidence.

**Blocks.** Thrombocytopenia release, and the precedent for the bar applied to the other seven
endpoints.

---

## 3. Immunotoxicity — which CRITICAL corrections remain open

**Why.** Your v0.1 memo records **MAJOR SCIENTIFIC REVISION REQUIRED** with ten CRITICAL items.
Without disposition the endpoint cannot be signed off or ingested.

**Context.** Two of the memo's named retrieval gaps are now closed: Goodchild 2009 S1 and
Valentin 2021 Supplementary Tables S1/S2 were acquired 2026-10-03 and are committed as derived
CSVs. The genuine Hornung 2005 paper has also been located (the file previously circulating under
that name is Herzner 2015). The remaining CRITICAL items are unaddressed: target label design,
ground-truth provenance, universal thresholds, unit of observation, the 2'OMe / LNA / CpG rules,
the gap-length claim, and antagonist labelling.

**Needed.** Which CRITICAL items remain open now the supplements are in hand, and whether any
part of the endpoint may move from *staged* to *scientifically admitted*.

**Blocks.** Immunotoxicity ingestion and sign-off.

---

## 4. Drive versus repository — which store is authoritative

**Why.** The two stores have diverged and have produced errors in **both** directions.

**Context.** Every immunotoxicity count in circulation (141 identifiers, 142 catalog records, 33
observations) traces to a Drive workbook that is not under version control, while the repository
dossier for that endpoint states "This project extracted no immunotoxicity data." Nine
independent audit agents consequently declared the endpoint empty. Conversely, a Drive-sourced
figure of 875 position records was carried into a summary against a measured 831.

**Needed.** A standing rule: which store governs when they differ; and whether the immunotoxicity
workbook, or a faithful CSV reduction of it, should be committed to the repository.

**Blocks.** Baseline reconciliation across every endpoint.

---

## 5. Phosphorothioate stereochemistry — are stereoisomers distinct constructs

**Why.** The NCATS/FDA GSRS registry supplies per-linkage modification positions for roughly
24–30 molecules we already hold — our worst-covered mandatory field. It also carries
stereochemistry our schema cannot represent.

**Context.** Rovanersen registers as `Phosphorothioate R-isomer → 1_13` and
`S-isomer → 1_1;1_5-1_12;1_14-1_15`. These are stereopure molecules. Recording them as plain
`full_PS` would be irreversible loss. This is the same question as your standing rule that shared
sequence or family grouping must not merge chemically distinct administered constructs.

**Needed.** Are stereoisomers distinct constructs? May they be pooled for modelling? If distinct,
confirm a stereochemistry field is added before ingestion.

**Blocks.** GSRS ingestion. Acquisition is proceeding; the pull is staged raw and unparsed pending
your ruling.

---

## 6. DEVOTE — does it pass the clean-negative gates

**Why.** Zero clean sequence-linked clinical negatives exist project-wide. That absence is the
stated reason the clinical sequence classifier is blocked. DEVOTE is the strongest candidate
found.

**Context.** NCT04089566. Adverse-event reporting uses `frequencyThreshold: '0'`, so absences are
**measured zeros** rather than unreported. Platelet and coagulation endpoints are **prespecified
primary**, not an incidental safety table. Per-arm denominators are traceable (6/40; 25/50/8/16).
Nusinersen's sequence and per-position chemistry are already held, so no new chemistry work is
required.

**Needed.** Does it pass all seven gates — exact sequence, human exposure, adequate dose and
duration, explicit monitoring, explicit outcome, traceable denominator? If not, which gate fails.

**Blocks.** The clinical sequence classifier.

**Warning, not a request.** NCT03358030 was proposed as a clean negative and **is not one**:
thrombocytopenia at 4/53, 6/54 and 7/50 against 0/53 placebo, plus a serious immune
thrombocytopenic purpura and a cerebral haemorrhage. It is a dose-graded **positive**, and is
proposed instead as the positive control opposite DEVOTE.

---

## 7. Kidney MSR066 — is a favourable renal result a negative

**Why.** A favourable therapeutic renal-function result is currently carried as a confirmed
negative for nephrotoxicity.

**Context.** Flagged 2026-10-02. **No label was changed**, pending your endpoint and control
review. Note your own rule that a same-analyte or same-source bridge is not proof of comparable
human and animal experiments.

**Needed.** Is a favourable renal-function outcome in a treated population a negative for
nephrotoxicity, or a different outcome class?

**Blocks.** Kidney negative-eligibility labelling, and the precedent for therapeutic-correction
cases in other endpoints — the same trap your v0.9 names for platelet counts.

---

## Summary

| # | Decision | Blocks |
|---|---|---|
| 1 | CNS authoritative lineage | Schema migration, CNS + hydrocephalus |
| 2 | Which of six thrombo blockers still bind | Release; the bar for all endpoints |
| 3 | Open CRITICAL items, immunotoxicity | Ingestion and sign-off |
| 4 | Drive vs repository authority | Baseline reconciliation, all endpoints |
| 5 | Stereoisomers distinct? | GSRS ingestion; chemistry representation |
| 6 | Does DEVOTE pass the gates | The blocked clinical classifier |
| 7 | Favourable renal result = negative? | Kidney labelling; precedent elsewhere |

Items 5 and 6 are new today and each has a concrete artifact waiting. Items 1–4 and 7 have been
open since 2026-10-02 or earlier.

No dataset edit, label change, merge, training run or release is proposed by this document.
