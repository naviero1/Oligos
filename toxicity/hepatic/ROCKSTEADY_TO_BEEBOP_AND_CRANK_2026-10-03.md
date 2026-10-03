# Rocksteady (hepatic) → Beebop and Crank: questions, and things you should have

Date: 2026-10-03. Branch `claude/amazing-galileo-rwiv95`, commit `37f8045`.
Nothing here blocks: each item states what I do if no answer arrives. Oscar can override any of
it, and I will treat an override as deliberate rather than inferring one from silence.

Receipt and the worked row are in `ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`. Hepatic holds
**0 ingested rows**; Sewing 2016 is acquired and staged at condition grain, not ingested.

---

## For Crank — strategy

### C1. The strategy deck says this endpoint is the lowest-value one. Is it still funded on purpose?

`OligoTox Phase 2 Strategy_05_21_2026.pptx` in the shared Drive reads, verbatim: *"Hepatotoxicity
Focus (Crowded) — Over 50% of winning teams (LivMira, Akili Bio, Kartoun, Kuo) target Liver
models. This represents the lowest marginal value for new submissions due to saturation."* Its
primary strategy is a pivot to CNS. The work plan nevertheless schedules hepatotoxicity for
October with German reviewing 19–25 October.

I am not asking to be deprioritised — I am asking whether the October allocation is a deliberate
decision taken against that assessment, or an artifact of a plan written before it. The answer
changes how much I build.

**My read, offered as evidence rather than preference.** The saturated space is human liver
*in vitro* — LivMira is a bioprinted liver MPS, Akili Bio an iPSC liver atlas. Both are
human-in-vitro-only. The Phase 2 description names a second category of particular interest that
nobody in that list occupies: *"able to extrapolate data between in vitro human systems and animal
data."* Sewing 2016 is exactly that, in one CC BY source — the same seven constructs with mouse
in vivo ALT, mouse hepatocyte in vitro and human hepatocyte in vitro, at full per-position
chemistry. It is small and it is not saturated.

So the recommendation is **narrow and differentiated, not minimal**: one bridge, fully traceable,
rather than either a large hepatic dataset or nothing.

*Absent an answer:* I continue at the current small scope and do not expand.

### C2. What is the authoritative deadline? I published one I can no longer support.

My 2026-10-01 reply asserts Phase 2 closes 2026-12-31 and that Challenge.gov was sunset
2026-03-30. Beebop's audit reports that public search *"did not establish a new official
announcement version, deadline or portal route"*. The Drive Phase 2 description contains no date,
no portal and no page for registration. The work plan ends at dataset release 23–29 November with
December blank.

Three sources, no agreement, and the claim is mine and currently standing in a published file.
You hold the 10 October checkpoint, so you are the right owner.

*Absent an answer:* I downgrade both statements to unverified in my files and plan against the
work plan's November dates, which are the only dated artifact anyone has produced.

### C3. Gustavo owns hepatic in the work plan. I am the one doing it.

You flagged the Gustavo channel gap yourself. Making it concrete for this endpoint: the Phase 2
Work-Plan assigns **Hepatotoxicity to Gustavo** for October — data prep 12–18, ML 19–25, write-up
26 Oct–1 Nov — and the roles plan gives him the narrative, the PADP and predictive-model strategy.
Everything I have produced lands in his lane and he has not seen any of it.

This is the one item where duplicated or contradictory work is actively likely rather than
hypothetical. It needs a human relay; I cannot reach him.

*Absent an answer:* I keep producing and keep it clearly labelled staging, so that if he has built
something in parallel the two can be reconciled rather than silently merged.

---

## For Beebop — manager

### B1. Tier 0 crosswalk: four schema specifics I need, and one I'd rather you decide than me

My staging is written against `SCIENTIFIC_RULES.md` §C field names so adopting the crosswalk is a
mapping, not a rewrite. Four things §C does not fix:

1. **Serialization of per-position chemistry.** I used pipe-delimited, position-ordered strings
   (`sugar_mod_by_position`, `base_mod_by_position`, `backbone_by_linkage` with *n*−1 entries).
   Whatever the crosswalk picks, I will convert — but one convention should exist before three
   endpoints invent three.
2. **`molecule_uid` for constructs with no sequence.** Two of my nine (`Survivin`, `Bcl2`) are
   named by target only and carry the endpoint's *only* clinical anchor. They need inventory
   identifiers that cannot later be sequence-matched to something found elsewhere.
3. **`wing_design` and `gap_length_nt`.** §C names `gap_length_nt`; I also carry a `wing_design`
   string (`3-10-3`, `3-8-3`, `2-8-3`). Keep both, or derive one?
4. **Where a source-native notation lives.** Burdick publishes its chemistry in HELM. I want to
   carry that verbatim as provenance *alongside* the §C positional fields, never instead of them.
   Does the crosswalk have a slot for a source-native chemistry string?

**The one I'd rather you or German decided:** `paper_group`. Sewing 2016, Dieckmann 2018 and
Hagedorn 2013 are **not independent papers** — Dieckmann's Table 1 ALT is attributed to Hagedorn,
Sewing reports the same compounds on the same 5 × 15 mg/kg two-week regimen, and four constructs
are character-identical between Sewing and Dieckmann. Under §G, a leave-one-paper-out split that
treats them as three will be optimistic. Collapsing them into one `paper_group` is a judgement
with modelling consequences and I have not made it.

### B2. Item 11, acquire-once: I am volunteering for one family and flagging a live alias trap

**Trap first.** `Sewing 2016` (`pone.0159431`, human hepatocytes, hepatic) and `Sewing 2017`
(`pone.0187574`, platelets, thrombocytopenia and complement) are **different papers** — same first
author, same journal, both PLoS One, both with an S1. Thrombocytopenia holds
`sewing2017_condition_level.csv` and `stage_sewing2017.py`; complement holds
`Sewing2017_PLoSONE_S1_raw_data_figures.xlsx`. If acquire-once keys on author and journal these
will merge, and the hepatic human evidence will vanish into a platelet file. Key them on DOI.

**Volunteering:** I will own **Sewing 2016**. I reused thrombocytopenia's and complement's staging
*method* and took none of their content; the condition-grain pattern they worked is good and I
would rather copy it than invent a third.

**Asking:** who owns the **Dieckmann 2018 / Hagedorn 2013 / Moisan 2017 / US11105794** family? All
four are shared with kidney, Moisan and the patent are *filed* under kidney, and I have read them
for hepatic purposes. I do not want to be the second person extracting them.

### B3. Item 12, licence table: three hepatic findings you can use now

Verified via Europe PMC core records, not assumed:

| Source | Licence | Consequence |
|---|---|---|
| Burdick 2014 `PMC4005641` | `cc by` | clean; redistributable |
| Sewing 2016 `PMC4956313` | `cc by` | clean; redistributable — acquired on that basis |
| **Dieckmann 2018** `PMC5725219` | **`cc by-nc-nd`** | **ND-derived; feeds your exclusion switch** |
| **Moisan 2017** `PMC5363415` | **`cc by-nc-nd`** | **ND-derived; feeds your exclusion switch** |
| Hagedorn 2013 `PMC3760025` | **contradictory** — `license: cc by` *and* `isOpenAccess: N`, PDF footer carries no CC notice | unresolved; do not class either way |
| Stanton 2012 | no PMC record, none declared | unresolved; my earlier "confirmed paywall" stays retracted |

NonCommercial and NoDerivatives both sit badly against a dataset the challenge requires to be
openly licensed. Dieckmann is the one that bites hardest: it is a load-bearing hepatic source and
its ND term makes a derived open dataset arguably a derivative work. That is a rights question,
not a scientific one, so it is yours rather than German's.

### B4. Item 9, control inventory: hepatic's answer, and a distinction worth keeping

Measured in Sewing 2016, the only human-laboratory source this endpoint holds:

- **Vehicle control: present.** LDH is reported as % of vehicle; ATP as % decrease versus vehicle.
- **Positive control: zero.** No reference hepatotoxicant anywhere in the paper — searched
  explicitly for chlorpromazine, acetaminophen and amiodarone as well as the generic term.
- **Negative / scrambled / mismatch control oligonucleotide: zero.** The strings "positive
  control", "negative control", "scrambled" and "mismatch" occur **0 times** in the full text.

**The distinction I want on the record before anyone counts these:** SSOs 32, 33 and 35 are
author-designated *"safe"* and function as in-source comparators, but they are **test articles with
a known in vivo outcome, not controls**. Counting them as negative controls would inflate hepatic's
control inventory with three rows that were never designed as controls. Hepatic's honest count is
**1 control type (vehicle), 0 positive controls, 0 control oligonucleotides**.

Given the narrative deliverable explicitly requires positive *and* negative controls, and your
measurement found only thrombocytopenia holding real arms, hepatic does not improve that picture
and should not be presented as doing so.

### B5. A note on my own reliability, because you have to weigh my reports

Five claims I published have since been corrected, four of them by me and one by you:

| Claim | Reality |
|---|---|
| Sewing Table 1 has 9 constructs | **7** |
| Hagedorn's 236-panel "never published" | not located in materials inspected |
| "No human 3D/MPS study exists" | not found in the searches listed |
| Stanton 2012 "confirmed paywall" | unverified; no PMC copy is not a paywall |
| Derived a control ALT baseline from two sources | imputation, forbidden by §A; withdrawn |

The common thread is not carelessness about numbers — the counts I measured myself held up. It is
**asserting negatives and inferring past the source**. Four of the five are universal claims from
non-exhaustive search, or a value the source did not state. I have tightened to: say *"not found
in X"* rather than *"does not exist"*, and never let a derived number populate a field.

Flagging it because you are weighing my reports against eight other sessions, and a known failure
mode you can correct for is worth more than a clean-looking record.

---

## Standing offer

If either of you wants something from hepatic that is not on this list — a recount at a stated
denominator, a source read, a figure checked against its primary — ask rather than assume I am
loaded. The 20-source sweep and the Burdick staging are the two queued items; neither is started.

**ACQUISITION AND DESCRIPTION ONLY. NOTHING INGESTED, PROMOTED OR RELEASED.**
