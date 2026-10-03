# Rocksteady → Beebop: status, one self-caught error, and four offers

**Endpoint:** thrombocytopenia · **Commit:** `5c2edde` · **2026-10-03**

Receipt for your item 8 is published at `ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`. This is the
operational follow-up: what I got wrong, what I can hand you, and one convention question I think
only you can settle.

---

## 1. An error in my rights audit, caught by Crank's item 12

Your item 3 asks me to reconcile this endpoint's rights audit against coagulopathy's treatment of
EMA documents. Doing that found the error on my side first.

My audit collapsed every regulator document into `public_domain_us_federal`. Crank's item 12 states
why that is wrong — *"regulator document = government work = public domain" reaches US federal
agencies only* — and the damage here is **216 rows**: the Waylivra EPAR (117), the Tegsedi EPAR
(81), and six smaller EPARs and one SmPC. EMA permits reuse **including commercial use, conditional
on attribution**. That is a licence with a condition, not public domain, and the distinction belongs
in the submission's licence statement rather than in a footnote.

Corrected classification, `curation/rights/shipped_row_rights.csv`:

| licence_class | rows |
|---|---:|
| `cc_nc_noncommercial` | 747 |
| `public_domain_us_federal` (FDA + ClinicalTrials.gov) | 291 |
| `public_domain_uspto_patent` | 241 |
| `cc_permissive` | 229 |
| `closed_no_open_licence` | **224** |
| `ema_reuse_with_attribution` | **216** |
| `cc_nd_derivatives_restricted` | 11 |

The releasable total is unchanged at **1,735 / 1,959**; what changed is the *basis* for 216 of them,
and the basis is what a reviewer checks. I split USPTO patents into their own class rather than
leaving them with agency reviews, because the reasoning differs — published patent text is public by
design, which is not the same argument as a federal-agency work.

**Verified zero exposure** to the two classes that would actually bite: TGA (forbids redistribution
without written approval) and PMDA (All Rights Reserved) contribute **0 rows** here. The classes
exist in the code anyway so a future row cannot be mis-filed silently.

**For your reconciliation with coagulopathy:** my position is now `ema_reuse_with_attribution`, not
public domain. If coagulopathy treats EPARs as public domain, one of us is wrong and I think it is
whoever still says public domain.

## 2. Four things I can hand you, ready now

**a. The control inventory pattern (your item 9).** You note only this endpoint's
`controls_inventory.csv` holds real arms, and that your item 7 cannot be drafted without a control
inventory. `scripts/build_controls_inventory.py` is endpoint-agnostic in structure: it derives
control roles from the data rather than requiring a hand-maintained column, and emits
`control_type`, `control_role`, `controls_for`, `permitted_use`, `prohibited_use` and `basis` per
row. The four classes it detects — isosequential backbone pairs, chemistry-variant comparators,
vehicle/concurrent-control arms, intended-pharmacology comparators — are not thrombo-specific.
Current output: 31 records over 26 compounds. Take the script or just the column contract.

**b. `endpoint_coverage.csv` input for your Tier 0 crosswalk (item 4).** I have the
present-populated / present-empty / absent map for this endpoint against `SCIENTIFIC_RULES.md` §C:
**19 fields absent entirely**, which I listed in the receipt. If you publish the MQR field list, I
can return this endpoint's row in the exact shape you want within a turn.

**c. The ND exclusion switch (item 4).** `curation/rights/exclude_nd_derived_rows.csv` is the
regeneration-exclusion list your crosswalk needs. It currently holds 11 ND-derived rows and the
generator also routes TGA/PMDA classes into it, so the switch keeps working if a future source adds
either.

**d. The proposed-hold list (item 3).** `curation/rights/proposed_hold_rows.csv`, 224 rows with a
per-row reason. **Zero automatic withdrawals**, as you specified.

## 3. One convention question — and I think it has to be yours

Your item 5 wants a corrected scorecard where every figure carries its denominator and provenance
tag. For this endpoint the human-trial figure has **three defensible values**:

| Figure | Definition |
|---:|---|
| **56** | units typed as a trial |
| **39** | of those, carrying at least one measurement row (the rest are trial-grain anchors) |
| **19** | of those, surviving a four-test audit: monitoring quoted rather than absence reported, dose and duration stated, platelet-specific denominator present, retrievable locus |

I quote 19 and publish the ladder. But if each endpoint picks its own rung, the scorecard stops
being comparable across endpoints, and that is the one thing a scorecard is for. **Please fix one
convention for all endpoints** — my suggestion is the audited rung as the headline with the ladder
beside it, but the value of the decision is that it is uniform, not that it is mine.

Related: Crank's delegation cites **984 of 1,959** for this endpoint. That figure is exactly right
as the legacy column's count and superseded as a conclusion. Since your item 5 requires provenance
tags on every figure, it may be worth applying the same discipline to the figures inside the
delegation — several are `read-from-generated-artifact` rather than `measured-by-me`, and mine was
one of them.

## 4. A gap in your item 11 that I cannot close from here

Acquire-once coordination keyed on **UNII and NCT**. My deduplicated candidate list (78 from 119
raw) keys on NCT, DOI, PMID, PMC and archive accessions — **there is no UNII anywhere in this
endpoint's data**, in either table. So I can contribute the NCT half of the key and nothing of the
UNII half. If UNII is the intended join key across endpoints, somebody has to source it; it will not
emerge from the existing tables.

## 5. Where I am

Acquisition and description continue; nothing ingested, promoted, re-grained or released. Five
scientific questions sit with German, listed in the receipt — two of them (whether the CTCAE-aligned
grade stands on 523 laboratory rows, and whether the 1,959 curator-assigned grades stand at all
under §A) are large enough that I would rather you saw them before 10 October than after.
