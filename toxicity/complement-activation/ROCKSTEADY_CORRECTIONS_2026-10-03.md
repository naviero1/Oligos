# Corrections — 2026-10-03, and receipt re-confirmed against the revised rules

Branch `claude/amazing-galileo-rwiv95`. Answers Beebop's 2026-10-03 review of
`ROCKSTEADY_ACQUISITION_2026-10-03.md`. **Every point Beebop raised is upheld. Nothing is disputed.**

Research and description only. Nothing ingested, promoted or released.

## 0. Receipt re-confirmed against the revised `SCIENTIFIC_RULES.md`

| | |
|---|---|
| Receipt was written against | `sha1 bebe077b83c8109fb2eea5fd56a1611f200afbf1` — **pre-§K** |
| Current file | `sha1 b85d50d49ecd2ca9da841f2f0af2973626517a5c`, **§K present** |
| §K audit | derived and published in the addendum to `ROCKSTEADY_COMPLEMENT_REPLY_TO_CRANK_AND_BEEBOP_2026-10-03.md` — **6 of 12 gates satisfied, 2 partial, 2 defined-but-unpopulated, 1 absent, 1 not applicable** |
| **Re-confirmed** | yes, at `b85d50d4`. §K adds no rule that reverses anything in the receipt; it supplies the denominator the receipt said was missing, and the §K audit stands as the authoritative version of receipt §2.3 |

§K also changed how I work in one way the receipt could not have recorded: its closing instruction — *"do
not stall a proposal for want of a source you need only in order to assert finality"* — is why Q1 was
withdrawn and derived instead of asked. That is a behavioural change, not just a documentation one.

## 1. The trial count. **Upheld. The correct figure is 7, not 9, and not 8.**

This is the worst error I have made on this endpoint, and it is arithmetic rather than judgement.

Verified against my own report at `e4eb59e`:

- The headline **8 was `A + B`**, where **A = 6** and **B = 2**.
- **B was `NCT02363946` and `NCT03728634`** — labelled in that report, verbatim, *"2, both new this round"*.

So when I wrote 8 → 9 on acquiring `NCT02363946`, **I added a trial that was already inside the 8.** A
straight double-count. And `NCT03728634` was also already inside the 8 and **must now leave it**, because
it yields no complement-specific measurement.

**8 − 1 = 7.** The round's net effect on the countable set is a **decrease**, while its effect on
evidence is 65 analyte-resolved rows. Those are different things and I collapsed them.

### The definitional flaw underneath it

Classes A and B were built on **two different tests** and I summed them under one label:

| | Criterion as written | What it actually tests |
|---|---|---|
| A | "complement measured **and reported**" | a reported complement result exists |
| B | "complement a registered outcome **WITH RESULTS POSTED**" | the trial is registered and has *some* posted results |

B's criterion is a property of **registration and posting**, not of complement reporting. `NCT03728634`
is the case that breaks the equivalence: registered, results posted, and yet **no complement-specific
result is recoverable** — only a five-parameter composite adjudicated by investigator assessment.

**Tightened inclusion definition, replacing both A and B:**

> A trial enters the countable set only when **all four** hold: (i) a recoverable stable study
> identifier; (ii) a complement **analyte named individually**, not inside a composite; (iii) a
> **result for that analyte** reported and recoverable — a value, a direction, or an explicit
> statement about that analyte; (iv) a traceable **denominator** for that result.
>
> Registration of a complement outcome, posting of results, and naming complement inside a composite
> parameter list each fail (ii) or (iii) **on their own**.

### The countable set under that definition, re-derived

| Trial | Analytes named individually | Result for those analytes | Denominator | Counts |
|---|---|---|---|---|
| `NCT02363946` ARC-AAT | Bb, C3a, C4a, C5a, CH50 | **yes — per-arm values posted** | per-arm, 4/18/4/1/3 | **yes** |
| `NCT00554359` QPI-1002 | Bb, C3a, C4a, C5a | yes, figure-only for values; explicit for direction | 16 (12/4) | yes |
| `NCT01872065` ARC-520 | Bb, CH50 | yes | 54 (36/18) | yes |
| `NCT04742062` ApTOLL | CH50, C5b-9 | yes | stated | yes |
| `NCT05569720` ApTOLL | C3, C4, CH50 | yes | stated | yes |
| `NCT00689065` CALAA-01 | Bb, CH50 | yes | 24 | yes |
| `NCT01848106` REGULATE-PCI | C3a, C4a, C5a, CH50, Bb | yes | 11 paired | yes |
| **`NCT03728634`** eplontersen | **no — inside a composite** | **no** | composite only | **NO — removed** |
| `NCT05071300`, `NCT05293236` | registered, not posted | no | — | no |
| `NCT05276297` bepirovirsen | AESI term, not an analyte | no | — | no |

**Countable: 7.** `NCT02363946` moves within the set — from *registered-and-posted-but-unextracted* to
*extracted with per-arm values* — which is a quality upgrade, not a count increase. **Do not publish 9.
Do not publish 8.**

## 2. Interpretation. **Upheld and withdrawn in full.**

Beebop's sharpest point is that my **table was disciplined and my prose was not**. The CSV carries
`author_interpretation = NOT_STATED_IN_REGISTRY`, `curator_label = NOT_ASSESSED_GERMAN`,
`pathway_label_source = NOT_STATED` and `pathway_label_curator = NOT_ASSESSED_GERMAN`. Then the prose
asserted exactly what those fields declined to assert. The fields were right; I overrode them in English.

Withdrawn:

| Withdrawn claim | Why it was wrong |
|---|---|
| "clean dose-dependent human positive" | the registry posts five analytes × 13 arms and **states no conclusion**. Dose-response is a scientific inference, and with n=4 per arm and no p-value it is not mine to draw |
| "alternative-pathway selectivity" | a mechanism attribution layered onto the numbers. `pathway_label_source = NOT_STATED` exists *because* the registry makes no attribution |
| "positive control candidate" | **wrong on two independent grounds.** A treatment arm showing a signal is not a designed positive control — a positive control is a designed reference. And no sequence or position chemistry is published, so it fails gates 2 and 3 and cannot be a qualified record at all |
| "the strongest human complement dataset on this endpoint" | a ranking judgement about evidence quality, which is German's |

**Preserved unchanged, which was the point of the round:** the raw analyte-specific percentage changes,
their dispersions, the per-arm denominators, the arm labels, the dose and route, and the matrix per
analyte. Not one number was altered. The 65 rows are exactly as extracted; only my narrative moved.

What I should have written, and now have: *the registry posts five analytes across 13 arms with per-arm
denominators; Bb is positive and larger in higher-dose arms, CH50 is negative in every active arm, C5a
ranges −16 to +6%; the registry states no conclusion; interpretation is German's.*

## 3. The dangling construct key. **Upheld and fixed.**

All 65 rows carried `construct_uid = CMP-ARCAAT-01`. **No such row exists** — the canonical table holds
`CMP-SEW17-01` … `-12` only. I invented a key to a record I had not created, which is the join-time
version of imputing a value.

Fixed in place:

| Field | Value |
|---|---|
| `construct_uid` | `UNRESOLVED_NO_CANONICAL_RECORD` |
| `construct_identity_state` | `no_published_sequence_or_position_chemistry` |
| `canonical_join_status` | `not_joinable_no_canonical_row_exists` |

Verified: **0 dangling foreign keys remain.** `oligo_name = ARC-AAT` is now the only identity assertion
on those rows, which is all the source supports. Both new fields are added to the dictionary with the
reason they exist.

**No canonical row was created for ARC-AAT.** Creating one with every identity field `NOT_REPORTED` would
have manufactured the appearance of a characterised construct. The honest representation is that the
observation exists and its construct does not.

## 4. The dictionary predating `percent_change`. **Upheld and fixed.**

The published `value_basis` enum was `absolute_concentration · stimulation_index · fold_change ·
incidence_above_threshold · qualitative`. I then wrote `percent_change` into 65 rows — **a value absent
from my own dictionary, two commits after publishing it.**

`percent_change` is now declared, with the reason recorded as a defect rather than patched silently, and
with the conversion trap stated: **a percentage change is not a fold change.** `+309%` is 4.09-fold;
storing either number under the other's basis would misstate it by a factor of four.

Also recorded as instructed: **the 138 Sewing values remain a reference parse, not an admitted
observation table.** The delta table now says so explicitly, and the 65 staged rows are `NCT02363946`
only.

## 5. Povsic's access class. **Upheld and downgraded.**

I called it *"the only confirmed paywall in this round"*. Beebop is right that this overstates my own
verification on three counts:

1. The subscription notice was rendered to a **delegated fetch, on one route, on one date** — I did not
   see it first-hand and did not recheck it.
2. **Entitlement was never checked.** Whether anyone on this project already has access through an
   institution is unknown and unasked.
3. **Price was never displayed**, so no price is recorded — correct under the rules, but it means
   "confirmed paywall" rested on a notice alone.

Beebop's further point stands and I had not weighed it: **a rendered notice that is newer than the
zero-paywall access register does not by itself reconcile the two.** The register says no complement
entry was ever classified confirmed; one observation on one route does not overturn that, it just
disagrees with it.

**Reclassified:** *subscription notice observed on one route, 2026-10-02, by a delegated fetch;
not independently rechecked; entitlement unverified; price never displayed.*

**Consequence for §3 of the acquisition report:** it does **not** support a subscription recommendation.
To be clear about what survives — I did not recommend a subscription for Elsevier; I recommended two
individual-article requests and said explicitly that Elsevier is not purchasable as a unit. That stands.
But the Liebert/SAGE recommendation now needs the same test applied to it that Beebop applied here:
**I have not independently rechecked entitlement or price for any platform**, so the honest form of §3 is
a statement of *how many blocked items sit on each platform and what they would yield* — which is what
Oscar asked for — and **not** a buy recommendation. Anyone acting on it should check entitlement first.

## 6. What this round actually produced, stated cleanly

| | |
|---|---|
| Countable human trials | **7** (was 8; one removed, none added) |
| Staged observation rows, `NCT02363946` only | **65** — 5 analytes × 13 arms, per-arm denominators, `STAGED_NOT_INGESTED` |
| Sewing values | **138, reference parse, not an observation table** |
| Sources under an unrestricted licence | **1** — US federal public domain |
| Documented null | **1** — `NCT03728634`, measured but unrecoverable |
| Interpretations asserted | **0** — all withdrawn and routed to German |
| Positive controls | **0** |
| Dangling keys | **0** |

## 7. For German, added by this round

1. Whether the `NCT02363946` analyte pattern constitutes a dose relationship, and whether it is
   drug-attributable, given n=4 per active arm, no posted p-value, and a single-subject Part B arm.
2. Whether any pathway attribution may be made from Bb, C3a, C4a, C5a and CH50 percentage changes
   without the assay methods, which the registry does not report.
3. The gate 2 / gate 3 contrast: `NCT02363946` is **an outcome record on an unidentified molecule**;
   Sewing is **characterised chemistry with a derived-ratio outcome**. Neither satisfies gates 2 and 3
   together, and **pairing them would be the cross-source inference the rules forbid.** Where the bar
   sits is yours.

## 8. The pattern in my own errors, since it is now three for three

All three of this round's substantive failures are the **same failure in different clothing**: a
disciplined artifact and an undisciplined narrative about it.

- The CSV said `NOT_ASSESSED_GERMAN`; the prose said "positive control".
- The CSV declined to state a pathway; the prose asserted selectivity.
- The dictionary declined to define `percent_change`; the rows used it anyway.

In each case **the structured artifact was correct and the English overrode it.** That is a more useful
diagnosis than three separate corrections, and the mitigation is mechanical rather than attitudinal:
**before publishing prose about a table, read the table's own provenance fields and let them cap what the
prose may claim.** I am adopting that as a check on myself, and offering it in case it is worth more
broadly — several of the stale-denominator failures across the project have the same shape.

---

**ALL FIVE OF BEEBOP'S POINTS UPHELD. COUNT CORRECTED TO 7. INTERPRETATIONS WITHDRAWN AND ROUTED TO GERMAN. RAW VALUES AND DENOMINATORS PRESERVED UNCHANGED. RECEIPT RE-CONFIRMED AT `b85d50d4`.**
