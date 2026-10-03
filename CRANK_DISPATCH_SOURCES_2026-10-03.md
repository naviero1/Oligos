# Crank → Beebop: source dispatch, 2026-10-03

Companion to `SOURCE_EXPANSION_REGISTER_2026-10-03.md` on this branch. Operational instructions
for relaying source work to Rocksteady. Checkpoint remains **2026-10-10**.

**Authorization unchanged.** Acquisition and description proceed in parallel. **Ingestion,
promotion and release remain gated** — on Tier 0 for the schema, and on German for anything
scientific. Nothing in this dispatch authorizes a dataset edit, a label, a merge or a release.

---

## 1. The headline you should relay first: there is almost nothing behind a paywall

Across eleven scouts, **zero leads were `PAYWALLED_VERIFIED`**. Not one price, purchase page or
payment requirement was observed anywhere. Every access failure was a bot wall, a rate limit, an
egress block, a 403 or a transport error.

Two consequences, both of which correct standing claims in our own registers:

- **`accessdata.fda.gov` is not blocked.** `toxicity/kidney/SOURCES.md:12` and
  `SOURCE_REGISTER.md` §2 both assert it is. Verified by byte count: default user agent returns
  HTTP 302, a 420-byte "FDA Apology" page; a browser user agent returns HTTP 200 and a
  2,181,318-byte, 711-page PDF. **Correct both files.** This converts kidney's largest stated
  dead end into ordinary retrieval work.
- **Fucini 2012 supplementary data is retrievable.** We class it "no open route found" and call
  it our highest-value outstanding file. The per-file REST endpoint 403s; the article page serves
  it. One GET from `pmc.ncbi.nlm.nih.gov/articles/instance/4047996/bin/Supp_Data.pdf`, 251.7 KB.

Standing rule from this round: **a technical failure is not a paywall, and a register entry
asserting a block must name what was actually observed.** Five scouts rediscovered the user-agent
fix independently while a sixth concluded the opposite and left the false assertion standing.

## 2. Acquire once, centrally — this is the main operational instruction

Eleven scouts duplicated heavily: seven chased the same EMA EPAR family, eight mined
ClinicalTrials.gov with six trial-level collisions, four chased GSRS, three PMDA files drew five
proposals, and seven independently rediscovered the purity ceiling. **This is the same failure
mode the data audit found — 197 sequences in two or more endpoint datasets, 10 rows inflating to
28 across files — now reappearing one level upstream in sourcing.**

**Do not relay the register to nine sessions as nine shopping lists.** Appoint a single owner per
duplicate family, acquire once, key on **UNII and NCT**, and publish the extraction to the
endpoints. The twelve families are enumerated in register §5. A session that notices another has
already fetched a document stands down — exactly one scout did this spontaneously; make it the
default.

## 3. Free wins — start now, no decision from anyone

Register §4 lists ten. Sequence them this way:

1. **EMA legal notice** first. It is a file edit, not an acquisition, and it is what makes
   several other items redistributable rather than merely readable: it converts 64 coagulopathy
   rows out of `publisher_restricted`/`unresolved` and repairs the legal basis under 216
   thrombocytopenia rows currently justified as "US Government work" for documents the EMA
   published.
2. **The two false-block corrections** in §1 above.
3. **GSRS acquisition** — see §4 before any of it is ingested.
4. **WHO INN re-extraction.** The PDFs are already on disk and already validated base-for-base.
   **State in writing that this is a re-extraction of a held source, not a new acquisition.**
   Presenting it as new acquisition is exactly the overstatement that has damaged this project.
5. The remaining items: Kim 2023 Table 13 (CC BY, use the Springer host — the PMC mirror serves a
   21 KB wall page), the imetelstat and Idera and Roche patents, the EudraCT posted results, and
   the Fucini supplement.

## 4. GSRS is the highest-value find — and it carries a schema blocker

The NCATS/FDA substance registry closes **modification positions** for ~24–30 held molecules in
one scripted pass. Public domain, no key, machine-readable, from the agency running the
Challenge. It is the single best answer to our joint-worst mandatory field: currently 0 of 27
coagulopathy clinical compounds, 0 of 12 complement, 0 of 65 position-resolved in kidney.

**Acquire it now. Do not ingest it yet.** GSRS carries **per-linkage phosphorothioate
stereochemistry** — rovanersen returns `Phosphorothioate R-isomer → 1_13` against
`S-isomer → 1_1;1_5-1_12;1_14-1_15`. These are **stereopure molecules and our schema has no
stereochemistry column.** Recording them as plain `full_PS` would be silently and unrecoverably
wrong, and it is exactly the class of error that survives review and poisons a model. The
stereochemistry column is a schema decision for Oscar; raise it in the Tier 0 proposal. Stage the
GSRS pull until it is resolved.

Two verified limits to carry with the pull: imetelstat registers as `substanceClass: chemical`
and pegnivacogin as `polymer`, so neither carries a nucleicAcid record; and the **nusinersen**
record is internally inconsistent with its own systematic name, with the EPAR, and with our
repository — treat that one cell as known-bad and take nusinersen from the EPAR instead.

## 5. Purity: the question is now answered, and the answer changes our treatment

Seven scouts independently reached the same wall. **No public source yields a drug-substance
release purity value for any approved oligonucleotide.** FDA redacts it as `(b)(4)` — 56
redactions in the inotersen review, 84 pages withheld in tofersen. EMA deletes commercially
confidential information. PMDA masks with asterisks. All three numeric findings anyone located
fail on inspection and **must not be ingested as purity**:

- imetelstat 71.2–71.6% (US 11,332,489 B2) is **crude product before preparative RP-HPLC**;
- nusinersen 4.1–6.7% impurities (PMDA) are **deliberately impurity-enriched toxicology batches**;
- Givlaari's NMT 0.5% / NMT 1.0% / NMT 20.0 area % are **acceptance limits, not measurements**.

**The instruction.** Populate `purity_method` and `identity_confirmation` fully and source-cited —
this register can take them from near-zero to roughly 12–15 approved compounds. Record
`purity_pct` as **withheld-with-evidence**, quoting the actual redaction counts, the EMA
confidentiality note and the PMDA asterisk masking. That is a materially stronger disclosure than
a silent `TBD`, it satisfies the Challenge's explicit missingness requirement, and it is not the
same as having the data — say so plainly rather than blurring the two.

**And treat this as narrative material, not only as a gap.** The brief requires a discussion of
the gap in publicly available data. "Numeric purity for oligonucleotide therapeutics is
systematically withheld across three regulators, and here is the documented evidence" is a
finding. Every competing team faces the same wall; we will be able to show it.

This also corrects my own earlier instruction. I told you to harvest purity first and disclose
second. For `purity_pct` that was wrong — it is not withheld from us, it is withheld from
everyone.

## 6. Two specific warnings before anything is promoted

**NCT03358030 is NOT a clean clinical negative. It is a dose-graded positive.** A scout proposed
it as the only candidate satisfying every clause of the clean-negative definition. The
consolidator pulled the same trial's adverse-event module: **Thrombocytopenia at 4/53, 6/54 and
7/50 against 0/53 placebo**, plus a serious immune thrombocytopenic purpura and a cerebral
haemorrhage. Had it shipped as our first clean negative it would have been a third citation-grade
error. It remains valuable — as raw continuous outcomes, and as the **positive control opposite
DEVOTE**. Relay this warning explicitly; it is the kind of item that gets re-proposed.

**DEVOTE (NCT04089566) is the strongest verified clean-negative candidate**, and the clean
negative is the single absence with a named consequence: German is blocking a classifier on it
and we hold zero. Verified: adverse-event `frequencyThreshold: '0'`, so absences are **measured
zeros** rather than unreported; prespecified **primary** platelet and coagulation endpoints rather
than an incidental safety table; traceable per-arm denominators; and nusinersen's sequence and
per-position chemistry already held, so no new chemistry work is required. **Prepare it for
German. Do not classify it yourselves** — whether it passes all seven gates is his ruling, not
ours.

Generalise the method, not just the trial: the `frequencyThreshold: '0'` filter over posted-results
trials of every held compound is our only credible systematic route to clean negatives. Run it
once, centrally.

## 7. A licence correction we must make regardless of Oscar's decisions

We have been generalising **"regulator document = government work = public domain."** That reaches
**US federal agencies only.** EMA permits commercial reuse with attribution; TGA forbids
redistribution without written approval; PMDA is All Rights Reserved. Build a **per-regulator
licence table with each term quoted verbatim**, and stop using one basis string for all of them.
This is a correction, not a decision.

## 8. What is gated on Oscar

Four redistribution questions are with him now: PMDA facts-versus-documents; whether TGA is worth
a retry at all; the basis for ND-licensed and conditional-grant material; and the stereochemistry
schema column in §4. **Acquire nothing under PMDA or TGA terms, and promote nothing from
ND-licensed sources, until he rules.** Everything in §3 is unaffected and proceeds now.

One free item sits inside the third question and is worth flagging early: coagulopathy ships
**30,885 words of verbatim publisher prose** across 687 rows in the `verbatim_quote` column, in a
file intended to ship openly. The numbers beside it are measurements; the quote is the authors'
expression. Dropping or hashing that column on those rows removes the exposure and loses no
measurement.

---

*Crank. Dispatch accompanying the 2026-10-03 source expansion register.*
