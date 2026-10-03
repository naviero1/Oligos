# Pinned baseline — relay of 2026-10-03

Branch tips at the moment Oscar relayed the delegation to all nine Rocksteady sessions and to
Beebop. Progress to the **2026-10-10 checkpoint** is measured against these commits, not against
recollection. Beebop's own practice, applied to Crank.

| Branch | Tip at relay |
|---|---|
| `claude/amazing-galileo-rwiv95` | `37f80458e4dd` |
| `claude/coagulopathy-oligos-toxicity-ap70gf` | `9ee2b59d100f` |
| `claude/crank-phase2-oversight` | `ce733bce87af` |
| `claude/food-tracking-image-app-0nzivp` | `9fd96e4d3f86` |
| `claude/hydrocephalus-toxicity-oligos-t172zv` | `0ba7936a6411` |
| `claude/oligo-challenge-data-4um5mi` | `5c2edde23b12` |
| `claude/oligo-cns-toxicity-dataset-tijib6` | `ce4d677e0b2e` |
| `claude/oligo-reorganize-toxicity-2h7t50` | `ca046e3a78ca` |
| `claude/oligo-toxicity-dataset-k394sz` | `2c429d2b9ce9` |
| `claude/oligo2-sequences-and-patent-mining` | `3c2c0ab6fbaa` |

Captured 2026-10-03 18:21 UTC. Crank issued no data change; every tip above is the
state the endpoint sessions began from after reading `SCIENTIFIC_RULES.md` and
`CRANK_DELEGATION_2026-10-03.md`.

## First response, within minutes of relay — hepatic

`37f8045` — hepatic filed a rules receipt and **acquired Sewing 2016**, the critical-path source
named in the delegation and previously absent from the repository. Verified by Crank against the
committed files, not taken from the commit message:

- **73 observation rows, 54 of them human** (primary human hepatocytes, gymnotic free uptake).
  The endpoint moved from **0 rows to 54 human rows**.
- **Condition grain, correctly applied** — `oligo × dose × time × cell system × endpoint`, in two
  tables (canonical constructs linked to observations) per `SCIENTIFIC_RULES.md` §B.
- **Per-position chemistry present**: `backbone_by_linkage` and `sugar_mod_by_position` pipe-delimited
  per residue, 3-10-3 LNA wings with 5-methyl-C located positionally. German's §7 schema, implemented.
- **`purity_pct`, `identity_method`, `endotoxin_level` = `NOT_REPORTED` on 9/9** — the mandated
  treatment, with the gap register acknowledged as owed and not yet written.
- **`curator_label` = `NOT_ASSIGNED_pending_German`** and every row carries
  `qualification: STAGED RAW VALUE — not validated, not adjudicated, not ingested, not model-eligible`.
  The agent contract honoured exactly; `author_interpretation` kept separate from curator label.
- **`sequence_family_group` and `paper_group` present from the start** — the leakage fields, not retrofitted.
- Licence **CC BY**; counts stated with denominators, including **0 verified human clinical trials
  contributed**.
- Two caveats surfaced unprompted: the 7 sequenced constructs target **mouse** Myd88 and were applied
  to human hepatocytes where they have no cognate target, so the cytotoxicity is **not target-mediated**;
  and the two constructs carrying the clinical anchor publish **no sequence**, recorded as "a gap to
  record, not to close by matching a name to a sequence found elsewhere."

**One open item Crank flags back:** the README discloses that Figure 8 values are means and that the
authors' colour bins are quarantined, but it does not state **how the numeric values were obtained
from Figure 8** — printed cell values, digitised positions, or bin assignment. All 54 human rows
depend on it, so the extraction method belongs in the staging README alongside the rest.

This is the plumbing fix working. The endpoint had been at zero rows since the project began; the
constraint was never the evidence, it was that the rules governing how to stage it were invisible.
