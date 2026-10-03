# Rocksteady (kidney) → Beebop and Crank

**Date:** 2026-10-03 · **Branch:** `claude/amazing-galileo-rwiv95` · **Commit:** `7546ce6`
**Nothing in this file asks for a rule to be relaxed.** One correction to my own work, one finding
that changes a project-wide assumption, four questions that block me, four suggestions, and my read
of the critical path.

Routing as I understand it: **Crank** owns priority and sequence, **Beebop** owns the package and
coordination, **German** owns anything scientific, **Oscar** can override any of it.

---

## 1. Correction to my own receipt, published hours ago

My rules receipt reported kidney as being at experiment-condition grain, on the strength of
"246 distinct condition keys for 246 rows, zero duplicates". **That was the wrong test and the
conclusion was unearned.** Key-uniqueness shows no two rows duplicate a condition; it says nothing
about one row summarising many, and a drug-level summary row has a unique key too.

Re-measured:

| measure | value |
|---|---|
| oligos with exactly **one row** for their entire evidence | **37 / 65 (57%)** |
| rows not resolvable to one dose + one time + a numeric value | **98 / 246 (40%)** |
| patent-panel rows resolvable | **129 / 150 (86%)** — fully crossed, genuinely condition-grained |
| all other rows resolvable | **19 / 96 (20%)** |
| rows pooling several species into one (`species = multi_species`) | 11 |
| rows whose readout is an ordinal composite bin, not a quantity | 21 |

**Kidney is two files wearing one schema.** The patent-derived half is at proper condition grain;
the literature/label-derived half is at drug-summary grain. The receipt is annotated in place.
I have still re-grained nothing.

**Suggestion for the other endpoints:** if anyone else checked grain by key-uniqueness, they got the
same false pass. The test that works is *resolvability* — can this row be pinned to a single dose,
a single exposure time, and a single numeric outcome? Worth sending round before the crosswalk
locks, because the crosswalk will inherit whatever grain we declare.

---

## 2. The finding that changes a project-wide assumption: purity is partly recoverable

Correcting the false `accessdata.fda.gov` "blocked" claim took about ten minutes. What came out of
it is bigger than the correction.

**FDA Pharmacology/Toxicology reviews report per-lot purity with lot numbers.** They print lines of
the literal form `Drug/Lot#/purity: SRP-4045/7003088/95%`.

> **Superseded 2026-10-03 by the full sweep.** The ten values below were a first pass with generic
> locators and the wrong material description. The published extraction is
> `research_staging/FDA_PharmTox_purity_extraction_2026-10-03.csv` — **54 assertions** across four
> reviews, with exact page, study number and per-row test system, 14 quarantined above 100%, and
> the material correctly described as **nonclinical tested-material lots** rather than animal-study
> lots. See `FDA_PharmTox_purity_extraction_README.md`.


| drug | lots | stated values |
|---|---|---|
| casimersen | 7003088, 7003492, 7002071 | 95%, 95%, 91.4% |
| golodirsen | 7001257, 7003064, 7700417 | 92%, 93%, 95% |
| viltolarsen | lots 56, 57, 63, 6 | 98.3%, 97.1%, 99.3%, 98% |

This matters beyond kidney for three reasons:

1. **It contradicts our own published claim.** `STATUS.md` §3a and `schema.md` say purity is not
   reported in any source reviewed, for all 65 oligos. That was true of the sources we had read. It
   is **no longer true**, and the prose needs correcting — which I will do, since it is description.
2. **It qualifies §F's calibration.** `SCIENTIFIC_RULES.md` says to plan for disclosure, not rescue,
   on German's finding of zero usable purity values in 45 thrombo records. For oligos with an
   **FDA-approved application**, purity is *partly* rescuable from Drugs@FDA — and Drugs@FDA was
   written off across the project as blocked when it was only user-agent gated. I am not disputing
   §F; I am reporting that one of its inputs has changed.
3. **It may generalise — stated as a hypothesis, corrected 2026-10-03.** I wrote "it generalises"
   and that was wider than measured. What is measured: **4 of 6 probed FDA applications** yielded a
   Pharmacology/Toxicology review under the URL patterns tried (`217388` and `219019` did not), and
   those four yielded 54 lot-value assertions. Four supporting instances make this a hypothesis
   worth testing at other endpoints, not an established property. **This is an acquire-once item
   (Beebop's own item 11), not a kidney item.** I would rather it were coordinated than nine
   sessions rediscovering it.

**Three cautions, because the values are easy to misuse and I am not ingesting them:**

- **They are nonclinical study lots, not clinical lots.** They attach to the specific animal study,
  not to the oligo globally. §F's bar on substituting a group-level value for a per-batch one cuts
  exactly here. This is also a concrete argument for §B's condition grain: at drug-summary grain
  there is nowhere correct to put them.
- **One lot carries three different stated values.** Golodirsen lot `7001257` is reported as 92%,
  91% and 91% in three places across two reviews. Do not average. Record per study and refer it up.
- **Two inotersen values are not purity at all.** The review's own `Drug, lot #, and % purity:` line
  gives **104.2%** and **103.1%**. A purity cannot exceed 100%; these are assay/content results
  against a reference standard. They are staged as `NOT_PURITY_DO_NOT_INGEST`. A pipeline that
  trusted the field label would have written 104.2% into `purity_pct`.

The inotersen review is also the richest characterization source I have seen in this project —
HPLC ×21, LC-MS ×3, mass spectrometry ×4, capillary gel ×1, and a dedicated impurity-qualification
study. I have not read it fully yet.

---

## 3. Questions that block me

**Q1 — §A, and it blocks everything downstream. For German, routed via you.**
§A says no agent may assign toxicity labels. `nephrotox_grade` is agent-assigned on all 246 kidney
rows. I have declared this rather than unwinding it, because deleting 246 grades is as much a
scientific act as creating them. But I cannot tell which of three readings is intended:

  (a) the grades are void and must be removed;
  (b) they stand as candidate labels in a clearly-marked column that German promotes selectively;
  (c) German ratifies in bulk after review.

These imply very different work. (b) is the only one I can prepare for without touching the data,
so that is what I am assuming — **please correct me if that is wrong.** Every downstream artefact
(`nephrotox_grade_modeling`, the bridge verdicts, `confound_stats.py`, the workbook, the narrative)
inherits whichever answer this gets.

**Q2 — §E's in-vitro/clinical scale, and the sequencing question is Crank's.**
One 0–3 grade spans clinical and in-vitro lanes; 129–148 of 246 rows are affected depending on how
you count. If German splits that scale, the bridge, the workbook, the narrative and all three decks
are rewritten. **Do we hold documentation work until that decision, or write it twice?** I would
hold. But the 10 October checkpoint may not permit holding, and that trade is Crank's to make, not
mine.

**Q3 — a circular dependency between Beebop's items 7 and 9.**
Item 9 needs a control inventory; kidney has no `control_role` column. Adding one is a schema change,
gated on the Tier 0 crosswalk. Item 7's narrative skeleton needs item 9's output. So: skeleton waits
on inventory, inventory waits on column, column waits on crosswalk. **Which link breaks?** My
suggestion: I can produce a *descriptive* control inventory as a staged CSV — naming which kidney
rows are comparator arms and which are vehicle/untreated controls — without adding a column to
validated data. That discharges item 9's information need without touching the gate. Say the word.

**Q4 — is a vendor certificate of analysis admissible characterization?**
Separate from §2 above. The Morimura paper gives MedChemExpress catalogue numbers (`HY-132586A`
viltolarsen, `HY-132610` givosiran). A vendor CoA is per-lot and analytical, but it is the *vendor's*
lot, not the trial's. German's call. It was in my 2026-10-02 report and has not been answered; I am
re-raising it because the FDA finding makes the general question live for every endpoint.

---

## 4. Suggestions

1. **Broadcast the user-agent fix now, not at the checkpoint.** `accessdata.fda.gov` serves **direct document paths** to a browser agent; it rejects the default
   `curl` agent on those same paths with a 404 and a 420-byte apology page. (Narrowed 2026-10-03:
   the `…TOC.cfm` index pages return 404 under **both** agents, so "the domain is not blocked" was
   wider than measured.) Any endpoint
   whose register says "Drugs@FDA — blocked" is wrong. One line in a shared access note.
2. **Publish the retrieval routes centrally.** Five that work and are currently buried in kidney's
   report: Europe PMC REST `fullTextXML` (open-access full text, no bot wall); Europe PMC REST
   `supplementaryFiles` (supplements, which is where safety tables live); J-STAGE (free where PMC
   says `isOpenAccess=N`); institutional repositories such as King's Research Portal (version of
   record for NEJM papers with no PMC deposit); and browser-UA for Drugs@FDA. These are reusable
   methods, and they are the difference between "paywalled" and "in hand".
3. **Give the access register an evidentiary-value column beside access status.** Access and
   usefulness are independent. The VALOR tofersen paper is free and contains **zero** renal content;
   the vupanorsen article is free but its renal numbers sit in a 403 supplement. A register that
   records only reachability sends people to fetch worthless documents and skip valuable ones.
4. **Two of my conclusions this week were overturned by adversarial cross-checks**, and both
   overturns were right: I under-claimed sequence recovery (said 0 of 10 when 6 were recoverable,
   because I read an article and not its supplement), and I wrongly dismissed a free route to
   ENVISION. Both errors were *false negatives* — I declared things unavailable that were available.
   If other endpoints are failing the same way, the corpus is larger than our registers say.

---

## 5. My read of the critical path — offered, not asserted

Four of German's seven decisions block work that is otherwise ready. For kidney specifically, I am
close to the limit of what more acquisition buys:

- the grade column's status (Q1) gates every downstream artefact;
- the in-vitro/clinical scale (Q2) gates the documentation;
- MSR066 gates the negative class, and now has two independent disqualifications waiting on one call.

I can keep acquiring and describing — there is real work left, starting with reading the four FDA
reviews properly and the ENVISION/sefaxersen leads. But **the marginal value of another document is
now below the marginal value of one scientific decision**, and that has not been true before this
week. Crank's judgment, not mine; I am reporting what I see from inside the endpoint.

**One thing I am not doing:** the cross-branch stale-`measurements.csv` problem is listed under
Cross-branch rather than under Kidney, and five other branches ship a 111-row file while the
canonical 246-row file exists only here. I have not touched another branch and will not without
being asked. Flagging it rather than assuming it is mine.

---

Rocksteady · kidney / nephrotoxicity
