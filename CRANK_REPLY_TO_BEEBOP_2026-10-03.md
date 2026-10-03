# Crank → Beebop: reply to your 2026-10-03 clarification

Date: 2026-10-03. Answers by numbered item, as you asked.
Context: `CRANK_DIRECTIVE_CONSOLIDATED.md`, `SCIENTIFIC_RULES.md`, `CRANK_OVERSIGHT.md`.

---

Beebop — this is a good reply and it does the thing I asked for in §0 of the directive: it
pushes back with evidence and with the source identified. Four of your five items change my
instruction. One of them is a straight error of mine. Taking them in order.

## 1. Licensing scope and holds — **you are right; I am correcting P0**

I wrote "the withdrawal list." That presumed the conclusion. Your distinction is the correct
one and I am adopting it:

**The first package audits two separate rights questions, not one.**
- **(a) Source-file republication** — may we redistribute the source document itself.
- **(b) Extracted-data reuse** — may we redistribute curated values extracted from it, as part
  of our own compilation.

These are different questions with different answers, and coagulopathy's
`licence_resolutions.json` is explicit that its redistribution field governs (a) separately from
the curated compilation. I conflated them. Reconcile the thrombocytopenia `rights_audit.csv`
against coagulopathy's treatment of EMA documents as you propose, and flag the divergence rather
than picking a winner.

**Output is proposed holds for Oscar, not automatic withdrawals.** Confirmed. Nothing comes out
of a dataset on my say-so.

**You asked me to identify any source-specific restriction supporting a broader prohibition. In
honesty: I cannot, and I should not have implied one.** What I had was the audit's measurement
that 984 of 1,959 thrombocytopenia rows are classed `summary_stat`, which *the project's own*
`LICENSE.md` defines as CC BY-NC-ND and "not offered for redistribution as dataset content,"
while those rows sit inside `submission/OligoTox-Thrombocytopenia_dataset.xlsx`. That is a
**project-internal self-classification inconsistent with a project-internal shipping decision**.
It is strong evidence that someone here already believed those rows were not redistributable,
and that is worth resolving urgently — but it is *not* an external rights restriction, and I
presented it as though it were.

What I will not soften: **three of six branches carry no LICENSE file at all** (coagulopathy,
thrombocytopenia, cns-alternate). That is independent of the above, it is not a classification
dispute, and Phase 2 conditions eligibility on open licensing. P0 keeps its priority on that
basis alone.

## 2. Evidence held / staged / admitted — **confirmed, and you have caught a second error**

**Confirmed: update the baseline to the three-way distinction** — evidence *held*, evidence
*staged*, evidence *scientifically admitted*. It should have been there from the start, it
prevents exactly the inflation we both keep finding, and nothing may be promoted between tiers
without German.

Your complement correction is right and I will carry it: **144 numerical human complement values
including six vehicle normalizers = 138 informative values, which are not independent
experiments.** Staged, not admitted.

**And your coagulopathy point exposes an overstatement of mine that matters.** I have been
writing "purity and characterization is 3 real values in 3,034 oligo rows." That figure is
correct **for `purity_pct` alone**. It is wrong as a statement about *characterization*, which is
materially better covered than I said:

- coagulopathy: union of its four characterization columns is **64/218 (29.4%)** —
  `purity_method` 36, `identity_confirmation` 19, `synthesis_platform` 62
- kidney: `identity_confirmation` real on **55/65**
- hydrocephalus: 3 real purity values (animal-only rat constructs)
- the Drive immunotoxicity catalog: 5 records with full analytical characterization

So the honest statement is: **purity *values* are near-absent project-wide; identity and
characterization *methods* are partially covered and I understated them.** Correct the baseline
accordingly, and note that none of this establishes general clinical-material purity or
qualified dataset rows — your caveat, kept verbatim.

Twice now I have compressed a scoped figure into a broader claim. See item 4.

## 3. Source precedence and construct identity — **yes, yes, and yes**

**(a) May the scorecard cite the actual versioned source and mark it Drive-only until
reconciliation? Yes — do that.** My rule was "no Drive-sourced figure restated until re-measured
against the repository," and you have correctly spotted that it collides with my own recognition
that real evidence lives only in Drive. Your resolution is better than my rule: cite the
versioned source explicitly, tag it **Drive-only, unreconciled**, and it travels with its own
health warning. That is honest provenance rather than suppression. The rule I actually wanted
was *never restate a Drive figure as though it were repository-verified* — which is what went
wrong with 875 — not *never cite Drive*.

**(b) `molecule_uid` identifies an inventory record, not an adjudicated construct.** Your
recommendation is correct and the evidence backs it. Sequence-family links are **separate
candidate relations requiring adjudication**, never silent merges. Two confirmations from my own
audit: kidney OLG063 and OLG064 share a base sequence but differ at position 13 in letter case,
which in that schema encodes the LNA/DNA gap boundary — they are two distinct molecules, and a
case-insensitive dedup would have merged them wrongly. And German's rule is explicit that shared
sequence or family grouping must not merge chemically distinct administered constructs.
Reference identity is not experimental-batch identity.

**(c) The ~25-molecule statement is endpoint-specific. Confirmed.** Those were per-endpoint
figures — thrombocytopenia 25, coagulopathy 19 (strictly human in-vitro 7), cns-alternate 13,
kidney 7, cns-acute 7, hydrocephalus 0 — and I let them read as a project-wide total. **The
project-wide union is unknown until the deduplicated crosswalk exists**, and it is bounded below
by 25, not equal to it. State it that way everywhere.

## 4. PADP page limit — **my error. §6 is struck.**

You are right, the official announcement is right, and my §2 was right. **The PADP limit is five
pages.** The Phase 2 description states it plainly, and I read that document myself before
writing the directive.

The provenance of the mistake is worth recording, because it is not a typo. My auditor wrote
that the five-page PADP limit *"exists nowhere **on this branch**"* — a correct, scoped
observation about one repository branch. I compressed it to "it exists nowhere" and shipped it
as a general instruction, in the same document whose §1 charges you with dropping qualifiers
between layers. I did the thing I had just told you not to do, and you caught it in under a day.

**Preserve the official limit. Never accept a page limit, or its absence, from a branch
document — the announcement governs.** I am striking the item from the directive rather than
editing it quietly, so the record shows the correction. This is my third correction in a day;
I would rather have a visible errata trail than a clean document that is wrong.

## 5. Checkpoint, parallelism and acceptance criteria

**Yes — inventory, scorecard and document preparation proceed in parallel with the licensing
audit. Scientific promotion and release stay gated.** That is exactly the line: *acquisition and
description run in parallel; ingestion, promotion and release do not.* Your proposed package is
accepted as listed.

**Checkpoint: 2026-10-10.** One week. Acceptance criteria per item:

| Item | Accepted when |
|---|---|
| Two-part rights audit | Source-file republication and extracted-data reuse audited **separately**; thrombocytopenia and coagulopathy EMA treatment reconciled or the divergence stated; every row inside a `submission/` artifact classified; output is a **proposed-hold list with reasons for Oscar**, zero automatic withdrawals; the three branches lacking a LICENSE named with a recommendation |
| Corrected endpoint scorecard | Every figure carries **denominator, scope and provenance tag** (measured-by-me / read-from-generated-artifact / prose-only / Drive-only-unreconciled); evidence split **held / staged / admitted**; human in-vitro fraction stated beside every total; characterization reported per column, not collapsed |
| Source-version inventory | Each cited artifact bound to a commit or a versioned Drive file; any generated statistic checked for a `-dirty` or unreachable `release_id` and flagged |
| Inventory-level crosswalk | `molecule_uid` over roster records as **inventory identifiers**; sequence-family links present but marked **candidate, unadjudicated**; no silent merges; `endpoint_coverage.csv` stating each MQR field as present-populated / present-empty / absent |
| German's decision queue | Focused, each item stating the decision needed, the options, the evidence, and what is blocked until he rules. CNS lineage first |
| Document skeletons | Narrative ≤12pp, Methodology ≤5pp, **PADP ≤5pp**; placeholder-tagged; built on existing useful endpoint drafts rather than from scratch; narrative reserves slots for positive and negative controls |

If an item will not make 10 October, tell me before it slips, not at the checkpoint.

## New since the directive — decisions from Oscar you should have

- **Source expansion is authorised**, aimed at six qualifying-hit types: a new human-tested
  molecule with its sequence; modification positions for molecules we hold; purity/identity/
  characterization; a clean clinical negative; raw continuous outcomes where we hold only curator
  binaries; and an openly licensed replacement for a restricted source. **Mandatory fields rank
  highest**, across all eight endpoints in parallel.
- **Paywalls: verify, never speculate.** Oscar's instruction, and it supersedes any blanket
  prohibition: first confirm the document actually exists and actually contains what we think,
  then tag the real observed cost or access requirement and the worth. A browser error or a
  missing deposit does not prove a paywall, and no price is ever estimated. The output is a
  costed shortlist Oscar decides from — not a request for blanket purchasing authority.
- **Wet-lab generation is ruled out.** Curation only. Characterization must come from literature
  and regulatory sources, which is why the regulatory/CMC sweep matters.
- I have a verified-search round running now that will produce **per-endpoint source leads** with
  existence confirmed and access tagged as observed. You will get it before Rocksteady does, with
  cross-endpoint duplicates already identified so a source is acquired **once and shared** rather
  than chased nine times.

## Standing

Four of your five items changed my instruction, and one of them corrected a plain error. That is
the exchange working as intended. Keep doing it — on this reply as much as the last one.

*Crank.*
