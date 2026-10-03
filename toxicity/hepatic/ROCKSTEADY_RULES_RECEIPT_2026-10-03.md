# Rocksteady → Beebop: rules receipt and delegation row, hepatotoxicity

Date: 2026-10-03. Endpoint: hepatic. Branch `claude/amazing-galileo-rwiv95`, read at commit
`8b9264d`. Answers `CRANK_DELEGATION_2026-10-03.md` item 8 (receipt confirmation) and works the
**Hepatic** row.

## Revision B — 2026-10-03: re-confirmed against the revised rules, and one claim contracted

**Re-read `SCIENTIFIC_RULES.md` at commit `8466cd7`.** My original receipt was taken against a
version that did not yet carry **§K, German's twelve scientist sign-off gates**. Re-confirmed
against §K below. Sections A–J are unchanged from my first reading and §2 stands as written.

**§K changes two things for this endpoint.**

*Gate 12 — "all major mechanistic and clinical claims are no stronger than the evidence
supports" — caught a claim of mine, and Beebop caught it first.* I wrote that Sewing 2016 gave
the same seven constructs across mouse in vivo, mouse hepatocyte and human hepatocyte. Recounted
from my own `research-staging/sewing2016_condition_level.csv`:

| Rows | System | Constructs | Source |
|---:|---|---|---|
| 42 | human hepatocyte in vitro | the **7 sequenced** | Fig 8A |
| 7 | mouse in vivo | the **7 sequenced** | Table 1 |
| 12 | human hepatocyte in vitro | the **2 unsequenced**, target-named | Fig 8C |
| 12 | mouse hepatocyte in vitro | the **2 unsequenced**, target-named | Fig 8B |

**No construct appears in all three systems.** The sequenced seven span two systems; the two
unsequenced constructs span a different two and have no in vivo arm. `SEW16-SSO47` carries no
numeric in-vivo value (ND — group sacrificed early), so the sequenced set yields **6 complete
numerical pairs, not 7**. The three-system claim is **withdrawn** wherever I made it, and what
remains is **6 sequence-linked human-in-vitro ↔ mouse-in-vivo pairs**: a bounded comparison
proposal, **not demonstrated extrapolation**.

One thing I will not use to soften this: the source *does* test the tool SSOs in mouse
hepatocytes, in Figures 2 and 7. I have **not staged or read those values**, so they support
nothing I have written. If staged they would make a third system available for the sequenced
seven — that is a future acquisition, not a defence of the claim as published.

*Gate 10 — leakage across exact-sequence, counterpart, strand, family, paper and experimental
series.* This sharpens the `paper_group` question already raised in B1 of
`ROCKSTEADY_TO_BEEBOP_AND_CRANK_2026-10-03.md`: the gate names **experimental-series** leakage
explicitly, and Sewing's Table 1 is the same 5 × 15 mg/kg series as Hagedorn's. No model
evaluation of these rows before German's grouping ruling.

Gates 1–5, 7 and 9 are already satisfied by the staging as built (traceable source location per
row; sequences verified 5′→3′ with strand role; chemistry by position; assay context; raw values
retained with `curator_label = NOT_ASSIGNED_pending_German`; human and animal in separate lanes;
file identities checksummed). Gates 6, 8, 11 do not yet bite — no labels, no composites and no
model.

**Also noted from §K:** *"A proposal may be derived from this file and submitted for German's
ratification… Do not stall a proposal for want of a source you need only in order to assert
finality."* I had been treating the grade rubric and the grouping question as fully blocked. They
are not: I may submit **derived proposals** for ratification, and will, rather than waiting.

## 1. Receipt

**Read in full: `SCIENTIFIC_RULES.md` and `CRANK_DELEGATION_2026-10-03.md`.** I had not seen
German's constraints before today; several of them bear directly on work I had already published,
and §2 below says where.

Noted and accepted: this file is a derivation, German's documents outrank it, and a discrepancy
is reported rather than followed. I have not seen the underlying Drive documents and am not
guessing at them. Also noted: `German_requests_100326.md` and
`CRANK_DISPATCH_SOURCES_2026-10-03.md` live on `claude/crank-phase2-oversight`; I have not read
them and make no claim about their contents.

## 2. Which rules change this endpoint's current work

Seven do. Four change something I had already written down.

**§A — the agent contract. Changes published work.** I had derived a mouse control-ALT baseline of
roughly 51–59 U/L by dividing Sewing's absolute ALT by Dieckmann's fold-change on the matching
regimen, and I described it as *recovering the in-table control Burdick lacks*. That is imputing a
missing value, and §A forbids it. **Withdrawn.** The arithmetic survives only as an observation
that two sources are mutually consistent; it may not populate a control field, and no row depends
on it. Related: I listed "propose an endpoint-specific grade rubric" as work. Under §A the rubric
is German's to define; I can state which readouts exist and what they are measured in, and stop
there.

**§B — unit of observation. Changes the plan, not the data.** The hepatic endpoint has **no
dataset and no rows on any branch** (verified today, all 10 branches), so there is nothing built
one-row-per-oligo to flag and nothing to re-grain. The flag is prospective and concerns the
sources:

- **Burdick 2014 is natively one-row-per-oligo.** Its 80-construct supplement reports a single
  ALT and a single lesion call per compound at one dose, one timepoint, one species. It cannot be
  expressed at condition grain because the source does not contain the conditions. That is a
  property of the source, to be disclosed, not a defect to be engineered around — and emphatically
  not something to re-grain.
- **Sewing 2016 is natively condition grain** and has been staged as such (§3).

I re-grain nothing and am not asking to.

**§C — minimum schema fields. Supersedes a recommendation I published.** My 2026-10-01 reply
recommended adopting the thrombocytopenia `scientist_v09` table pattern as the hepatic schema.
That is now wrong on authority: German's named fields and the canonical-oligo-to-observation
architecture already exist, and Beebop's Tier 0 crosswalk is where schema is settled.
**Recommendation withdrawn; hepatic takes the crosswalk.** The staging in §3 is written against
§C's field names so it can be mapped rather than translated.

Also: I had proposed **HELM** as "the chemistry field". Demoted. §C requires chemistry encoded by
position in named fields, and coarse molecule-level flags only as secondary derived variables.
HELM is now carried as a **verbatim source string** for Burdick, because that is the notation
Burdick's own supplement publishes, alongside populated `sugar_mod_by_position`,
`base_mod_by_position` and `backbone_by_linkage`. It is a carrier, not a replacement.

**§E — label and control rules. Changes how one finding may be used.** I reported that Burdick's
DNA-gap 5-methyl-C placement reproduces the CpG rule in 79 of 80 compounds. §E prohibits encoding
universal chemistry rules, and names CpG methylation specifically as contradicted in this corpus.
That finding is therefore a **description of one file**, never a derivation rule, and never used to
populate chemistry that a source did not state. Separately, §E's "unreported is not negative" is
the same hazard I reported from the registry adverse-event tables, where 50 of ~74 candidate trials
filter at a sponsor-set frequency threshold; German's rule governs and the finding stands as
corroboration, not as a competing rule.

**§F — missingness. Refines my wording and adds an artifact I owe.** I wrote that recording
`NOT_REPORTED` "does not satisfy" the characterization requirement. §F is sharper and I adopt it:
`NOT_REPORTED` is the **correct value**, and the **Characterization Gap Register** is the separate
artifact that discharges the requirement — both are required, and the value is not a failure
state. Hepatic currently has `purity_pct` `NOT_REPORTED` on 9 of 9 staged constructs and owes the
register entry. German's calibration (0 of 45 thrombo records with usable purity) says plan for
disclosure, not rescue; hepatic is in the same position and will say so.

**§G — leakage. Adds two fields from the start, and surfaces a hazard specific to this endpoint.**
`sequence_family_group` and `paper_group` are populated in the staging already. The hazard:
**Sewing 2016, Dieckmann 2018 and Hagedorn 2013 are not independent papers.** Dieckmann's Table 1
ALT is attributed to Hagedorn; Sewing's Table 1 reports the same compounds on the same
5 × 15 mg/kg two-week regimen; four constructs are character-identical across Sewing and
Dieckmann. A leave-one-paper-out split that treats these three as independent will be optimistic.
They need one shared `paper_group`, which is a judgement I am flagging rather than making.
Also §G's "shared-sequence grouping must not merge chemically distinct administered constructs" is
exactly the Dieckmann↔US11105794 case I reported; the staging records that crosswalk as
sequence-level only and explicitly not as same-material.

**§D — evidence classification.** Adopted as stated; no change, but it retires any temptation to
read a completeness tier as a safety statement. Human clinical, human laboratory and animal stay
in separate lanes in the staging.

**§I — known source corrections.** None are hepatic. Carried, not re-derived. I have added no
hepatic entry to that list.

**No GSRS data** is held by this endpoint, so the raw-and-unparsed staging rule has nothing to
bite on here.

## 3. The Hepatic row — worked, with the figures checked

### 3.1 "Sewing 2016 is the critical path — absent from the repository" — **CONFIRMED, with a trap**

Verified across all 10 branch tips: no file for `10.1371/journal.pone.0159431` anywhere.

**But a different Sewing paper is already in the repository**, and the names collide.
`Sewing 2017` (`pone.0187574`) is staged by **two** other endpoints — thrombocytopenia
(`sewing2017_condition_level.csv`, `sewing2017_pone.0187574_S1.xlsx`, `stage_sewing2017.py`) and
complement (`Sewing2017_PLoSONE_S1_raw_data_figures.xlsx`,
`sewing_extraction_grain_reference.csv`). Different paper, different endpoint, same first author
and same journal. This is precisely the alias trap that acquire-once coordination (Beebop item 11)
exists to catch, and it should be keyed so no one later "deduplicates" the two. I reused their
staging *method* and took none of their content.

### 3.2 "Seven constructs, not nine" — **CONFIRMED**

Mine, and already corrected in the published reply (Revision A, commit `3ee5e8b`). Read visually
from the publisher's 1572×623 render plus the original TIFF: SSO 32, 33, 35, 36, 37, 43, 47.
Table 1's notation is the most complete of any hepatic source held — lowercase DNA, capitals
**beta-oxy** LNA (which resolves the sugar stereochemistry Dieckmann leaves unstated), ᵐC
5-methylcytosine, subscript s phosphorothioate per linkage.

### 3.3 "Burdick's 80-construct panel stages as clearly-labelled animal support" — **CONFIRMED and accepted**

80 constructs, 70 numeric ALT, re-parsed independently (md5 `3287a0d2…`). Mouse in vivo. It will
carry `species = Mus musculus` and sit in the animal lane; it is not human progress and will not
be presented as such. Not yet staged — Sewing was the critical path and went first.

### 3.4 "The only primary human-hepatocyte source" — **NOT VERIFIED BY ME**

I have confirmed Sewing 2016 *is* a primary human-hepatocyte source. I have **not** established it
is the *only* one; that is a negative over the literature and I have run no systematic search
supporting it. Recorded as unverified rather than echoed. The 20-source sweep in the
2026-10-02 research request is the instrument that would settle it, and the honest form of the
answer will be "not found in the searches listed", not "none exists".

### 3.5 Cross-branch row — **CONFIRMED, and the figure is incomplete in two ways**

The delegation says the stale 111-row `measurements.csv` ships on **five of six** branches in
**two divergent versions**, with the canonical 246-row file only on `amazing-galileo-rwiv95`.
Recounted from the committed trees today:

| Rows | Blob | Branches |
|---:|---|---|
| 111 | `5bea31d2` | coagulopathy, food-tracking, hydrocephalus, oligo-challenge, oligo-toxicity (**5**) |
| 111 | `1fbe366e` | oligo-cns (**1**) |
| 246 | `6f7bb715` | amazing-galileo-rwiv95, **crank-phase2-oversight** (**2**) |
| **769** | `6df3f055` | **oligo2-sequences-and-patent-mining** (**1**) |

Two refinements. The 111-row file ships on **six** branches, not five, in two blobs as stated. And
there is a **third row count** the figure does not mention: a **769-row** `measurements.csv` on
`oligo2-sequences-and-patent-mining`. 769 is the number the stale hepatic dossier variant on
`oligo-reorganize-toxicity-2h7t50` cites, so that branch pair is where the 769 lineage lives. The
canonical 246-row file is on two branches, the second being Crank's own oversight branch. The
hazard as stated is real and if anything understated: a relative-path resolve of
`data/measurements.csv` can land on **four** different tables.

Not mine to fix; reported with the recount.

## 4. What was done under the acquisition-and-description permission

Acquisition and description proceed now; ingestion, promotion and release are gated. Staying
inside that:

**Acquired** Sewing 2016 into `toxicity/hepatic/research-staging/sources/` — article PDF,
Table 1 renders, Figure 8, and the Europe PMC supplementary bundle, with checksums. Redistribution
is licensed: **CC BY**, established by licence check before acquisition rather than assumed.

**Described** it at condition grain, as two linked tables per §B, generated by a committed script
so the transfer is reproducible and auditable:

| | |
|---|---|
| `sewing2016_constructs.csv` | 9 constructs × 25 fields |
| `sewing2016_condition_level.csv` | 73 observation rows × 24 fields |
| Human cell-system rows | **54** |
| Animal rows (mouse in vivo ALT 7, mouse hepatocyte 12) | **19** |
| Constructs with a published sequence and per-position chemistry | **7 / 9** |
| Constructs with a purity value | **0 / 9** |
| Constructs with an analytical identity method | **0 / 9** |
| Verified human clinical trials contributed | **0** |

Figure 8 turned out to be a **printed numeric table**, not a plot, so every value is transferred as
printed and nothing is digitised off an axis. Three facts travel with the rows: they are **means of
2 experiments in triplicate** with no replicate-level or donor-level values published; the authors'
colour-scale bins are stored as source-specific and are not labels; and the seven sequenced
constructs target **mouse** Myd88, so their cytotoxicity in human hepatocytes is not
target-mediated.

`SEW16-Survivin` and `SEW16-Bcl2` carry this source's only clinical anchor — grade 3 liver enzyme
increases in phase 1, per the authors — and the source publishes **no sequence** for either. They
are staged with `sequence_5to3 = NOT_REPORTED`. That gap is recorded, not closed by matching a
target name to a sequence from elsewhere.

**Not done, deliberately:** no row ingested, no dataset created, no label assigned
(`curator_label = NOT_ASSIGNED_pending_German` on all 73 rows), no schema fixed, no grade rubric
written, no Burdick staging yet, no merge of any construct across sources.

## 5. Owed and gated

**On German:** the hepatic grade rubric and what the readouts mean; whether Sewing, Dieckmann and
Hagedorn share one `paper_group` for leakage control (§2, §G); whether Burdick's 4 model-excluded
non-lesion compounds may be staged as observations; the Fig 8 colour bins' status.

**On the Tier 0 crosswalk:** the schema the staging maps to. The staging is written against §C
field names to make that a mapping rather than a rewrite.

**Owed by me:** the Characterization Gap Register entry for 9 of 9 `NOT_REPORTED` purity values
(§F); Burdick staged as animal support; the `ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md` with the
20-source log, which remains unwritten.

**Still unresolved from earlier rounds, restated so it is not lost:** Hagedorn 2013's licence is
contradictory — Europe PMC returns `license: cc by` while reporting `isOpenAccess: N`, and the PDF
footer carries no CC notice. Dieckmann 2018 and Moisan 2017 are both **CC BY-NC-ND**, which sits
badly against a dataset required to be openly licensed; that belongs in Beebop's rights audit and
the `licence_class` column. Stanton 2012 — the only route to purity for Burdick's 80 — has no
verified publisher access condition yet, and my earlier "confirmed paywall" stays retracted.

---

**RECEIPT CONFIRMED — ACQUISITION AND DESCRIPTION ONLY. NOTHING INGESTED, PROMOTED OR RELEASED.**
