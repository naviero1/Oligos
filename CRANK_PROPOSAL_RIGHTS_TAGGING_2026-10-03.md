# Proposal: a project-wide rights tag on every row

Crank → Oscar and Beebop, 2026-10-03. **Proposal for Oscar's ratification.** Licensing is Oscar's
authority; this needs no ruling from German.

Originates from Oscar: rather than ship-or-hold the 224 closed-access thrombocytopenia rows, tag
them, and apply the same criteria across all eight toxicologies.

---

## 1. Why this is the right shape

**It decides nothing prematurely.** A tag is reversible; shipping and deleting are not. Every row
keeps its evidence and carries its own rights status.

**It makes the release a filter, not a negotiation.** "What ships" becomes a documented query over
a declared column instead of eight endpoint-by-endpoint judgments. The regeneration switch already
in the Tier 0 spec reduces to a `WHERE` clause.

**It is one convention instead of eight.** Today each endpoint has invented its own vocabulary:
thrombocytopenia uses `summary_stat` and three tiers; coagulopathy uses `publisher_restricted`,
`CC_BY_NC_ND`, `CC_BY_NC` and `unresolved`; two branches carry no LICENSE at all. That divergence
is the same harmonization problem the schema has, in the one area where getting it wrong is an
**eligibility** failure rather than a quality one.

**It is itself a contribution.** A released dataset in which every row declares its own rights
basis is rare, and the PADP can point at it rather than asserting openness in prose.

## 2. Build on what exists — do not reinvent it

Thrombocytopenia has a working two-layer implementation covering 1,959 rows from 70 sources. It is
the reference. Generalize it; do not design a parallel vocabulary.

**Layer 1 — source-level register, one row per `source_ref`:**

| Field | Content |
|---|---|
| `source_ref` | the join key |
| `declared_licence` | verbatim as published; blank where none is declared |
| `licence_evidence` | **what was actually observed and where** — the statement, the page, the date |
| `rights_tier` | A / B / C / D, per §3 |
| `source_file_redistribution` | may the source document itself be republished |
| `extracted_data_reuse` | may measured values be released as derived rows |
| `is_open_access`, `in_pmc`, `regulator` | provenance aids |
| `resolved_by`, `resolved_date` | who determined it and when |

**Layer 2 — row-level, joined onto every measurement:**
`rights_tier` · `licence_class` · `extracted_data_release` (RELEASE / DECISION_REQUIRED / HOLD) ·
`hold_reason`.

Cost is a join, not a manual pass: thrombocytopenia derived 1,959 row tags from 70 source
determinations. Project-wide, roughly 8,600 rows resolve from a few hundred sources.

## 3. Four tiers, not three

Thrombocytopenia's `B_cc_licensed` currently holds CC BY and CC BY-NC together. Those are
materially different postures, and coagulopathy is almost entirely the second case — 426 CC BY-NC-ND
plus 76 CC BY-NC. Splitting B is the one substantive change proposed:

| Tier | Meaning | Default `extracted_data_release` |
|---|---|---|
| **A — public domain** | US federal works, expired, dedicated | RELEASE |
| **B — open licensed** | CC BY, CC0 — reuse unrestricted | RELEASE |
| **C — restricted licensed** | CC BY-NC, BY-NC-ND, publisher-restricted. **Terms exist and restrict.** | RELEASE under the facts-not-expression basis, tagged |
| **D — no licence declared** | Nothing stated by the publisher at all | RELEASE, tagged — **this is the 224** |

The distinction that matters for C versus D: in C we have terms to reason about; in D the
facts-not-expression basis is doing **all** the work, because there is no licence text to point at.
Both release under Oscar's adopted basis, but they are not the same exposure and must not share a
label.

## 4. Two axes that must stay separate

Per Beebop, and already adopted by Oscar as two separate audits:
**source-file republication** and **extracted-data reuse** are different questions with different
answers. A source we may not republish may still yield values we may release. Carry both columns;
never collapse them into one "redistributable" flag.

## 5. The hard limit on what a tag may assert

A tag records **what was observed** and **what disposition is proposed**. It must never assert
legal clearance.

`licence_evidence` carries the observed statement and its locator. `resolved_by` names who made
the determination. Under German's agent contract, agents do not resolve conflicts — and a rights
determination with no declared licence is a conflict. Where the basis is doing the work, the row
says so.

Carried from the existing ledgers, unchanged: **the ledger is a project classification, not
independent legal clearance**, and there are **no automatic withdrawals**.

## 6. What this does not fix

- **Two branches still carry no LICENSE file.** A per-row tag does not supply the dataset's own
  licence. That remains separate and outstanding.
- **It is not a hedge against the basis being wrong.** If facts-not-expression is unsound, tagged
  rows still shipped. What the tag buys is that no reader is asked to silently accept a reading
  they cannot see.
- **It does not resolve the 48 non-permissive source documents** committed on coagulopathy.
  Hashing or tagging output columns does not answer a source-file question.

## 7. Proposed route

Owner: **Beebop**, folded into the Tier 0 crosswalk already in flight, with thrombocytopenia's
implementation as the reference and coagulopathy as the hardest mapping. Each endpoint supplies
its source-level determinations; the row-level tags are derived, not hand-entered.

This needs **no ruling from German** — licensing is Oscar's authority. It can move while the
schema and MQR proposals sit with German.

Recommended first output: the source-level register for all eight endpoints, which is where the
judgment lives. The row tags follow mechanically.
