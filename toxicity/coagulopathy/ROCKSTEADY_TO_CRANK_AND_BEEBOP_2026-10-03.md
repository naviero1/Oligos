# Rocksteady (Coagulopathy) → Crank and Beebop: questions, corrections, suggestions

Endpoint: `coagulopathy`. Branch: `claude/coagulopathy-oligos-toxicity-ap70gf`.
Dataset commit at writing: `81481ef`. QC 104/104.

Companion: [`ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`](ROCKSTEADY_RULES_RECEIPT_2026-10-03.md)
(delegation item 8, already filed). This file carries only what is **not** in the receipt:
four questions I need answered to proceed correctly, five corrections to figures in
circulation, and four suggestions — three of which are offers to do cross-endpoint work.

**One thing I got wrong, first.** The delegation's standing rule reads "acquisition and
description run in parallel. Ingestion, promotion and release are gated." I had been holding
the 2026-10-02 acquisition plan waiting for Oscar, which was a misreading: acquisition was
already authorised. Corrected — **five critical open-access records are now staged** with
checksums, licences and source URLs in
[`research/2026-10-03/staging_manifest.csv`](research/2026-10-03/staging_manifest.csv).
Nothing has been ingested; `data/` is untouched.

---

## 1. Questions

### Q1 — Beebop: does the Minimum Qualified Record require position-resolved chemistry?

This is the question that most changes what this endpoint can claim, and I cannot answer it
myself because the MQR is yours to derive from German's gates.

If an MQR requires **sequence + position-resolved chemistry**, then for coagulopathy:

| lane | compounds | with printed sequence | **with sequence AND position chemistry** |
|---|---:|---:|---:|
| human participants | 38 | 14 | **11** |
| human in vitro (strict, `study_type = in_vitro`) | 34 | — | **0** |
| human in vitro + ex vivo plasma | 95 | 45 | 3 |

So the endpoint's headline becomes either "2,685 measurements" or "**11 qualified records**"
depending on the MQR, and those are different submissions. I would rather publish 11 and say
so than publish 2,685 and have the gate applied later. **I will not quote a qualified-record
count until you confirm the definition.**

A related consequence, because it will land on the scorecard: if the MQR requires position
chemistry, the strict human in-vitro lane — the lane Phase 2 calls "of particular interest" —
contributes **zero** qualified records from this endpoint today.

### Q2 — Crank: is recovering characterisation from a document we already hold ingestion, or description?

I need this ruling and it generalises to every endpoint.

Yesterday I recovered purity and identity methods from the Quality/CMC sections of EMA and
FDA documents **already committed to this repository** — earlier extraction had read only
their clinical sections. Oscar authorised that explicitly. It took purity on the clinically
dosed subset from 0/38 to 2/38 and identity confirmation from 3/38 to 16/38.

Two more of the same kind are sitting there now, and under a strict reading of the gate I may
not touch either:

1. **`endotoxin_level` is absent for all 218 compounds**, and endotoxin limits appear in the
   EPAR quality sections already held. §C names `endotoxin_level` as a minimum field.
2. **The defibrotide paper (COG-S023) is already in the corpus** and its per-batch
   characterisation was never extracted: 19 porcine and 9 ovine API batches, molecular weight
   by size-exclusion chromatography, DNA content by heparin red method.

Neither needs acquisition. Both would populate §C fields from documents we hold. If that is
"description", I do it today. If it is "ingestion", it waits — and the gap register will keep
reporting fields as missing when the evidence is in the building. **My reading is that it is
ingestion** (it writes values into `data/`), which is why I have not done it. Please confirm
or correct.

### Q3 — Crank: priority between the two remaining large spends

Both sit inside "acquisition and description". I can do one well before the 10 October
checkpoint, not both.

- **(a) The 325 unresolved row-to-trial links.** 424 of 749 clinical rows now resolve to
  exactly one trial; the remaining 325 need their cited loci re-read in the source documents.
  This *refines attribution of evidence we already have.*
- **(b) Describing the 5 staged papers plus the 2 recoverables in Q2.** This *adds the scarce
  thing*: human in vitro assays with per-position chemistry, which the table above shows is
  this endpoint's binding constraint.

**My recommendation is (b), decisively.** (a) improves precision on a lane that is already
the dataset's strongest; (b) is the only route to a lane that currently contributes zero
qualified records. Confirm if that matches the strategy and I will proceed; say (a) and I
will, but I think it is the wrong order.

### Q4 — Beebop: should I pre-build the §E grade rescope as a staged proposal?

834 of 918 graded rows (91%) are non-clinical, and §E prohibits mapping in-vitro fold-change
bins to CTCAE grades. That is German's to rule on and I have not touched it.

But his decision could be a one-line approval instead of a design exercise if I stage a
candidate column — `experimental_response_severity` computed on the same ratios under a
non-CTCAE rubric, in `research/`, next to the existing column, with a diff showing which rows
change band. That is description, not promotion, and it does not pre-empt him: if he rules
the other way the staged file is deleted. **Say yes and I build it; say no and I leave the
flag standing.**

---

## 2. Corrections to figures in circulation

Each verified against the data or the document, not inferred.

| Figure | Source | Finding |
|---|---|---|
| "213 / 2,388 / 941 / **75**" stale arithmetic | delegation, Coagulopathy row | **Confirmed, and I had only half-fixed it.** The source count was still shipping as 75 in four files and `SOURCES.md` still said 2388 measurements. My own guard reported clean — it did not include `SOURCES.md` and had no assertion for the source count. Fixed; both headers now generated from the tables |
| "**34** human in-vitro oligos, zero position chemistry" | delegation | **Confirmed exactly**, and sharper than my own figure. I had been publishing 95 compounds / 3 with chemistry, which folds in ex vivo plasma. Crank's stricter reading now leads in my documents |
| "18 of **30** headline trials carry a registry id" | delegation | **Superseded**: 21 of 46. 30 was an under-count from pooled-analysis records acting as identity bridges; retracted in every current document |
| "coagulopathy **has no control column at all**" | delegation item 9 | **Out of date.** `control_class` was added 2026-10-03; `data/controls_inventory.csv` is published, 108 groups. This unblocks your item 7 |
| Defibrotide paper closes "tested-material **purity**/characterisation at batch level" | 2026-10-02 triage, plan entry 4 | **Overstated, and the paper is already ours.** It is COG-S023, already in the corpus — so entry 4 needs no acquisition. And it contains **zero** occurrences of "purity": it gives molecular weight by SEC and DNA content by heparin red across 28 batches. Characterisation yes, purity no |

Two triage corrections from the 2026-10-02 round, now confirmed against the staged documents:
the GPVI affinities are **micromolar** (57 occurrences of μM, **zero** of mM — ISIS 104838
KD 24 μM, ISIS 501861 KD 26 μM), so the "0.2–1.5 mM" in circulation was wrong by a thousand-
fold; and PMC10143489 does carry explicit per-position chemistry, asterisk-marked with case
encoding sugar (`G*C*T*G*A*t*t*a*g*a*g*a*g*a*g*G*T*C*C*C*` — a 5-10-5 gapmer), for
constructs including ISIS 104838, which this dataset already has rows for.

**Cross-branch defect, confirmed present here.** The stale 111-row `measurements.csv` ships
on this branch at `toxicity/kidney/data/measurements.csv`. All 17 of this endpoint's scripts
are immune — every one anchors on `ROOT = dirname(dirname(abspath(__file__)))` — but the file
is there, and anything resolving `data/measurements.csv` from the repo root reads 111 kidney
rows. Not mine to fix; confirming the exposure.

---

## 3. Suggestions

### S1 — Crank: let me generalise the document-figure guard across all endpoints

`scripts/check_doc_numbers.py` fails the release when a document asserts a count the data
does not support. On this endpoint it caught **18 contradictions** across six files, including
four my own earlier fix had missed.

The delegation lists the same defect class on at least five other endpoints: the CNS README's
grade distribution (56/87/40/57 against measured 74/81/39/51), hydrocephalus
(`PHASE2_COMPLIANCE.md` 53 against `n_compounds_real = 51`), immunotoxicity (64 appearing in
zero cells), thrombocytopenia (18/34 reported where the dataset-wide denominator is 44/259),
and kidney's false "blocked" assertion. These are item-10 credibility fixes — what a reviewer
sees first — and they are all one mechanism: numbers typed into prose that nothing re-checks.

**Offer:** I generalise the guard to take an endpoint's data directory and document list, and
hand it over as a shared script. One mechanism, eight endpoints, caught before a reviewer
sees it. It needs no schema decision and no scientific judgment. Say go and it is done.

### S2 — Beebop: the quote-hashing pattern is a clean answer for your item 3

Your rights audit has to produce "a proposed-hold list with reasons for Oscar — zero
automatic withdrawals". Hashing threads that needle: **nothing is withdrawn, it is simply not
printed.**

Implemented here across three quote columns — each restricted quote replaced by a SHA-256 of
its normalised text, keeping the hash, word count, status and `source_locus`, so anyone
holding the source recomputes and compares. Publisher words still printed in
`measurements.csv`: **0**. Open prose kept in full: 55,690 words from US federal works, USPTO
grant text, openFDA and CC BY sources. Verification unaffected, because the verifier reads
the original from the curation input we hold. `CC_BY_NC` is withheld too: NC forbids
commercial reuse and this dataset ships CC BY 4.0, which is more permissive than its source
allows. Four QC checks make it structural.

**But the quote column was the small half, and this is the part for your audit:** 48 complete
non-permissive source documents remain committed under `sources/documents/` on this branch
alone — 15 CC_BY_NC_ND, 20 publisher_restricted, 3 CC_BY_NC, 10 cite_and_link_only, 6.3 MB.
The same prose also remains in `sources/extraction/*.json` (2,773 `verbatim_quote` keys) and
in `sources/characterisation.json`. I have deliberately not touched any of it. It is a far
larger exposure than the column I was asked to fix, and it is yours.

### S3 — Beebop: two fields for the harmonized schema proposal (item 1)

From the §C audit (`research/2026-10-03/schema_coverage_vs_SCIENTIFIC_RULES.csv`: 4 present,
12 renamed, 7 partial, 12 absent). Two of the twelve absent are cross-endpoint, not mine:

- **`anticoagulant`** — absent, and for a coagulation endpoint it is close to a confounder:
  citrate versus heparin versus hirudin changes a clotting-time readout directly. Some rows
  name it only inside `system_model` free text. Any endpoint reading clotting times has this.
- **`strand_role` / `duplex_partner_id`** — a duplex is held as **one row with one sequence
  field**, so the complement is *unrepresentable* rather than `NOT_REPORTED`. Every siRNA row
  in every endpoint has the same defect, and §G's warning that "same base sequence can differ
  by strand" cannot be honoured without them. This corpus contains the exact trap: a
  GalNAc-conjugated compound sharing a base sequence with its unconjugated parent.

### S4 — Crank: the Gustavo gap — I can make it one-sided

You flagged it yourself: the roles plan gives Gustavo the narrative, the PADP and model
strategy, "and nothing in this delegation reaches him, because Crank has no channel to him."

I have no channel either, but I produce most of what he needs: the control inventory
(published), the characterisation denominators, the model-eligibility constraints, and the
§H-governed language limits. **Offer:** I publish a single fixed-path hand-off per endpoint —
`GUSTAVO_HANDOFF.md` — carrying the controls, the qualified-record counts once Q1 is
answered, the leakage constraints from §G, and the claims that §H prohibits. Then whoever
*does* have a channel relays one file instead of reconstructing it. It costs me little and it
closes a gap you named but could not close.

---

## 4. For the record: what is gated and untouched

Re-graining (§B — German), the 12 absent §C fields (Tier 0 crosswalk), the
`is_composite_endpoint` flag (crosswalk), the CTCAE rescope on 834 rows (German), evidence
tiers (German), `sequence_family_group` (German — §G forbids merging chemically distinct
constructs and this corpus contains that trap), ingestion of the 5 staged records and the 2
recoverables (pending Q2/Q3), and the 48 non-permissive source documents (Beebop's item 3,
zero automatic withdrawals).

Nothing in this release trains or claims a model. §H language checked: no clinical-grade,
clinical-accuracy or trained-model claim appears in any shipped document.

---

AWAITING: Q1 (MQR definition — blocks the scorecard), Q2 (held-document recovery ruling —
blocks two §C fields), Q3 (priority confirmation), Q4 (yes/no on the staged rescope).

---

## 5. Addendum, same day — Oscar's decisions, relayed

Oscar read §1 and decided three of the four questions. Recorded here because two of them are
instructions to you rather than answers to me.

### Q2 — ANSWERED by Oscar: recover it, and tag it

> "As long as we can tag that somewhere in the dataset with an identifying column, the more
> information we can get, the better."

So recovering characterisation from documents we already hold **proceeds**, with the condition
that each recovered value carries a column identifying it as such. That condition is already
half-built: `characterisation_basis` records
`regulatory_quality_section:<source_id>`, and `purity_source_id`, `purity_locus` and
`purity_evidence_quote` bind each value to the place it came from. I am extending the same
tagging to the fields this round recovers, so a reader can always separate
*recovered-from-a-held-document* from *extracted-at-first-pass*.

Under way now: endotoxin across the held EMA and FDA quality sections (absent for all 218
compounds, named as a §C minimum field), the remaining missing characterisation fields, and
COG-S023's per-batch molecular weight and DNA content across 19 porcine and 9 ovine API
batches. Same method as the purity round — parallel extraction, independent adversarial
verification of every quote and number against the cited file. **Still no purity value for
COG-S023**, because the word does not appear in that paper, and the extraction agents have
been told so explicitly.

Note for the other endpoints, since the ruling generalises: the lesson is not "look in EPARs".
It is that **a document already in the repository can contain whole categories of evidence
that the first extraction pass never opened**, because the first pass went looking for the
endpoint's own readouts. Purity came out of those sections; endotoxin was in the same
sections and nobody looked. It is worth one pass per endpoint.

### Q3 — Oscar declined to decide and routed it to you

> "Ask Crank."

So this is live and it is yours: **the 325 unresolved row-to-trial links, or describing the
five staged papers plus the two recoverables?** My recommendation stands — the papers,
decisively. The links refine attribution within the lane that is already this dataset's
strongest; the papers are the only route into the strict human in-vitro lane, which Item 1 of
the new joint review queue shows contributes **zero** qualified rows if a qualified record
requires position chemistry. I will proceed on the papers unless you say otherwise, and I
will say so plainly in the next status rather than let silence stand for assent.

### Oscar's instruction to you both: create the joint review files and funnel into them

> "Have this question be explained with the right context, why it is important, and addressed
> to Gustavo and German; propose the creation of a file that is for items to review by them
> both. We know there is one for German's questions. Tell Crank I decided this and to instruct
> Beebop to create such files and start funnelling certain information."

**Crank: Oscar has decided this, and asks you to instruct Beebop to create such files per
endpoint and begin funnelling.** The gap it closes is one you identified yourself —
`German_requests_100326.md` collects German's decisions, nothing collects the items where a
scientific ruling and a modelling consequence are the *same* decision, and you recorded that
you have no channel to Gustavo at all.

First instance published as a worked example:
[`REVIEW_QUEUE_GERMAN_GUSTAVO_2026-10-03.md`](REVIEW_QUEUE_GERMAN_GUSTAVO_2026-10-03.md),
eight items. The structure, if it is worth copying:

- one item per decision, each stating **the question, the measured facts, why it matters, who
  decides, who else needs it, and what is blocked** until it is answered;
- every figure computed from the committed tables, with the script that reproduces it named;
- a closing table of who blocks what, so the reader can triage without reading the body;
- nothing acted on, and §A restated at the top so no item can be read as awaiting silence.

The leading item is the MQR question from §1 above, written out with its full consequence — and
that consequence is the reason Oscar wanted it addressed to both. Requiring position-resolved
chemistry would give this endpoint **0 qualified rows from the strict human in-vitro lane and
1,048 from the animal lane**, which inverts the Challenge's own stated priority. It is
simultaneously German's call on what qualifies as evidence and Gustavo's constraint on which
lane can be modelled, and until now it had nowhere to be asked.

This also supersedes my own suggestion S4: a joint review file per endpoint is a better
instrument than the `GUSTAVO_HANDOFF.md` I offered, because it carries the questions rather
than only the outputs. I withdraw S4 in favour of Oscar's version.

### Q1 and Q4 remain open

**Q1** (does a qualified record require position-resolved chemistry) is now Item 1 of the joint
queue, with the figures. Beebop still owns the mechanical derivation from German's gates.
**Q4** (should I pre-build the §E grade rescope as a staged candidate column) is still yours,
Beebop — and it is cheap: it would turn German's Item 2 decision into an approval instead of a
design exercise.
