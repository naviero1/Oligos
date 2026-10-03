# Receipt, revision 2 — re-confirmed against the revised `SCIENTIFIC_RULES.md`, with §K audited

**Endpoint:** thrombocytopenia · **Branch:** `claude/oligo-challenge-data-4um5mi`
**For:** Beebop · **Date:** 2026-10-03 · **Supersedes:** nothing in `ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`

Revision 1 was written against a version of the rules file that did not yet contain **§K, German's
twelve scientist sign-off gates**. That section was added after several receipts went in, mine
included, so revision 1 confirmed a file that has since grown. This revision re-confirms the read
and audits the endpoint gate by gate. The §A–§J analysis in revision 1 stands unchanged and is not
repeated here.

**Read in full, this revision:** `SCIENTIFIC_RULES.md` at `origin/claude/crank-phase2-oversight`,
including §K. The file still does not exist on this branch — flagged in revision 1, still worth
fixing, since a rule invisible to the session bound by it is the failure the file exists to close.

I also note §K's closing paragraph, which changes how I work rather than what I measure: *a proposal
may be derived from this file and submitted for ratification; only an authority claim requires
German's primary documents; do not stall a proposal for want of a source needed only to assert
finality.* Revision 1 held several findings back as unproposable. They are proposals, and they are
below.

---

## 1. The headline figure

**Zero of 1,959 rows clear all twelve gates.**

Not because the rows are bad. Because gates 2, 5 and 6 require fields that **do not exist in this
schema at all**, so they fail identically on every row and no amount of per-row curation moves the
number. Three absent columns, not 1,959 deficient rows.

This is the figure to quote if anyone asks whether this endpoint is sign-off ready. It is a measure
of distance remaining, and the distance is three schema fields and one re-scaling wide — not a
rebuild. Reproduce it with `scripts/audit_signoff_gates.py`; the per-gate figures land in
`data/signoff_gate_audit.csv`.

**Tally: 4 PASS · 4 PARTIAL · 3 FAIL · 1 not applicable.**

---

## 2. Gate by gate, each verdict carrying its measurement

### Gate 1 — traceable primary source and exact source location · **PASS**

`source_ref` on 1,959/1,959; an in-document locus on 1,959/1,959, of which **1,719 name a
table, figure or supplement cell** and **240 name a document section** for facts stated in prose
rather than tabulated. A section is the exact location of a prose fact, so those are not missing
loci.

This gate passing does not make a single row qualified. It is the one gate this endpoint was built
to satisfy from the start.

### Gate 2 — sequence verified 5′→3′, strand identity and duplex partner · **FAIL**

Sequences on 200/259 constructs, directional and verified where present. But **`strand_role` and
`duplex_partner_id` do not exist as columns.** For the **6 double-stranded constructs** the gate
cannot be evaluated even in principle: nothing in the data records which strand a sequence is, or
what it pairs with.

This is the cleanest failure of the twelve and the one I would fix first.

### Gate 3 — modification encoded by position, not only as a molecule-level flag · **PARTIAL**

Position-resolved `modification_map` on **44/259**. Molecule-level chemistry only on **194/259** —
which is precisely the state this gate excludes. And of the 44 maps, **0 are source-verbatim**:
every one is a reconstruction from a described chemistry.

Two maps were **reverted** this round because they had been composed from a related molecule's
backbone rather than read from a source — one of them my own error, where eplontersen inherited
inotersen's all-phosphorothioate backbone and was wrong on 6 of 19 linkages while contradicting its
own `backbone_chemistry` field. A new QC gate (backbone consistency) caught a second instance.
The relevant point for §K: a position map that is *inferred* should not be counted toward gate 3 as
if it were *read*, and the `characterization_source` column now lets a reviewer tell the difference.

### Gate 4 — assay context: cell system, donor, delivery/formulation, dose, exposure time · **PARTIAL**

`system_model` 1,959/1,959 · `delivery_method` 1,950/1,959 · dose 1,748/1,959 ·
`exposure_duration` 1,839/1,959 · **`donor_id` column ABSENT.**

Dose and exposure are well covered. Donor information has no column, so per-donor variation cannot
be modelled, reported, or even counted — and §B names donor/cell system as part of the unit of
observation, so this is the same omission showing up twice.

### Gate 5 — raw outcomes retained; curator-derived labels explicitly marked derived · **FAIL**

Continuous `readout_value` retained on **1,589/1,959**, alongside the label rather than replaced by
it — that half passes. The other half fails outright: **1,959 curator-assigned grades and no column
stating that they are curator-derived.** A downstream reader cannot distinguish a grade this
curation effort assigned from a grade a source reported, because the data does not say.

All 1,959 go to German as provisional (§4 below). I have not renamed or re-scaled the column.

### Gate 6 — agonist, antagonist, potentiator and inert/low-response separated · **FAIL**

**No response-state column exists.** `effect_direction` records which way a readout moved —
increase 706, no_change 647, decrease 603, TBD 3 — which is not what the gate asks for.

Generalising the gate off receptor pharmacology onto this endpoint: it asks that a construct
*measured and found inert* be separable from one *actively harmful* and from one that *potentiates*
another agent's effect. The 647 `no_change` rows are the interesting case — some are genuine
measured inertness, which is a positive control for the absence of the effect, and some are
underpowered nulls. The data does not currently tell them apart.

### Gate 7 — human and animal not pooled as interchangeable ground truth · **PASS**

**1,453 human** and **497 animal** rows in separate views, with **9 assigned to neither** because
they are unresolved or pooled multi-species findings — forcing those onto one side is the pooling
this gate forbids, so they are left out of both. The scientist-facing ranking is computed
on human evidence only. The pooled `grade_gap_animal_minus_human` column — which asserted exactly
the interchangeability this gate forbids, by subtracting one species' grade from another's — was
**deleted** and replaced by per-side exposure plus `exposure_comparable` and an explicit
`interpretation_limit`.

### Gate 8 — endpoint-specific outcomes not collapsed into a composite · **PASS**

**439 distinct `readout_name` values** survive on the rows: platelet_count 1,083 ·
clinical_outcome 226 · platelet_activation 196 · platelet_aggregation 119 · platelet_binding 117 ·
immunogenicity 105 · coagulation 62 · megakaryocyte 26. The grade is layered **over** the named
readout, not in place of it, and `is_platelet_specific` (1,734/1,959) keeps a true platelet readout
separable from a general haematology or safety signal.

### Gate 9 — citation metadata and file identities pass QC · **PASS**

**70 sources** on stable `source_uid`s, after resolving 55 colliding `source_id`s. **27 citation
defects** found by auditing my own search fleet's output and corrected: a fabricated title, three
sources falsely logged as searched, a yield figure inferred by word-counting rather than read, and
twenty cross-family duplicates.

Stated plainly: gate 9 passes *now*. It did not pass before that audit, and the defects were in work
my own fleet produced and logged as clean.

### Gate 10 — split leakage checked across six axes · **PARTIAL**

`exact_sequence_group` 259/259 · `scaffold_family` 35/259 · `publication_group` 35/259 ·
`matched_pair_id` 4/259. **Strand leakage cannot be checked** — it needs gate 2's absent fields.
**Experimental-series leakage has no key**; the study registry's 23 arithmetically-proved nesting
edges are the nearest thing and do not cover it.

The cost of ignoring this is measured rather than asserted: **~0.94 under random row splitting
versus ~0.65 under leave-one-paper-out.** Random row splitting is prohibited here (§G) and that
gap is why.

### Gate 11 — LOPO and sequence-family grouped performance with uncertainty · **NOT APPLICABLE**

No model is trained. The classifier's release state is **BLOCKED** (§H) and the prior one was
**retracted** rather than re-reported, with a retraction record written. There is no performance to
report, so the gate is not applicable — not passed.

It becomes live the moment a model is trained, and reporting any single accuracy figure without
LOPO and sequence-family grouping would fail it immediately. Given gate 10's measured 0.94/0.65
gap, that is not a hypothetical risk.

### Gate 12 — claims no stronger than the evidence supports · **PARTIAL**

Your recurring cross-endpoint finding is conclusions broader than the measured evidence supports.
It applied here. **Three overstatements, all three in the artifacts a reviewer would actually
read**, all three corrected this round:

| What it said | Why it was too strong | What it says now |
|---|---|---|
| "The dataset reproduces the field's structure–activity relationship from curation alone" | It describes the ordering of **curator-assigned, provisional** labels, 523 of which derive from a mapping §E prohibits; and the load-bearing neutral-backbone comparator rests on **1 human row** | "The ordering the phosphorothioate hypothesis predicts is present in the curated data", with all three dependencies stated in the same block |
| "This per-row tracking is what makes the dataset lawfully redistributable as a whole" | A project classification asserted as a legal conclusion | "A project classification, not legal clearance", with source-file republication split from extracted-fact reuse |
| A trial count quotable as 56 qualified trials | 56 is what **typed** as a trial; 39 carry measurements; **19** survive this endpoint's four-test audit | The full ladder with every rung's loss reason, and an explicit note that none of the three is a count of qualified trials |

PARTIAL, not PASS, and deliberately so: the corrections were needed at all. One document set
produced three instances of the same failure mode. Passing this gate is a property of the next
document I write, not of the three I just fixed.

---

## 3. What I propose, under §K's proposal clause

Four schema proposals. Each is derived from §K and submitted for German's ratification; none is
implemented, and none needs his primary documents to be *proposed*.

1. **Add `strand_role` and `duplex_partner_id`** (gate 2). Unblocks gate 2, and unblocks the strand
   axis of gate 10. Six constructs need it today; any siRNA acquisition needs it from the start.
2. **Add `grade_provenance`** (gate 5) — `source_reported` | `curator_derived` — defaulting to
   `curator_derived` on all 1,959 rows, since that is the truth. One column, no re-labelling, and
   it makes the provisional status machine-readable instead of prose in a referral document.
3. **Add `donor_id`** (gate 4, §B). Absent in most sources; `NOT_REPORTED` is then the correct
   value (§F) and the Characterization Gap Register counts it. The column's absence currently hides
   the gap rather than recording it.
4. **Add `response_state`** (gate 6) separating measured-inert from unmeasured and from harmful.
   The 647 `no_change` rows are where the negative controls live, and Phase 2 asks for positive and
   negative controls by name.

Proposals 1–3 are mechanical. Proposal 4 requires a scientific judgement per row and should not be
bulk-populated by an agent.

---

## 4. Referrals to German — provisional, with history preserved

Written up in full at **`curation/german_queue/GRADE_REFERRAL_2026-10-03.md`**:

- **523 in-vitro and ex-vivo rows** whose grade was derived from a clinical severity scale, which
  §E prohibits absent clinical validation.
- **All 1,959 curator-assigned grades**, as provisional pending gate 5.
- **DEVOTE (NCT04089566)** stays **unclassified**; the packet is prepared, the ruling is his.

The historical columns are **preserved, not rewritten**. Nothing is renamed, re-scaled or dropped.

---

## 5. Two cautions I am recording against myself

- **No substance-identifier join exists.** **Neither table has a structured identifier column** —
  no UNII, CAS, InChIKey, SMILES, ChEMBL or DrugBank field in the 259 constructs or the 1,959
  measurements. What does exist is prose: **8 of 259** constructs carry a CAS-shaped registry number
  inside a free-text note, and **exactly one** (danvatirsen, UNII `31N550RD05`) carries a UNII value,
  in a provenance sentence rather than a field. Eight prose mentions are not a join key, so any
  crosswalk to an external substance registry today would in practice be matched on **names and
  chemistry** — which is how the ODN 2395 collision happened, where a bare name was shared by a
  phosphorothioate and its isosequential phosphodiester control and the name match picked the wrong
  record. I will not describe the identifier join as available. (My earlier draft of this caution
  said "no UNII anywhere"; one exists, in prose. The conclusion is unchanged, the figure was wrong.)
- **Sewing 2016 ≠ Sewing 2017.** Same author, same journal, different documents. Verified: no
  reference to Sewing 2016 appears anywhere in my files, so there is no conflation to undo — the
  caution is recorded so that no later deduplication pass invents one. **Author + journal is not a
  duplication key.**

---

## 6. The submission was regenerated, and the rights error was in four more places than you named

You said the rights fix had landed in `curation/rights/` only, and that `PADP.md`, `submission/padp.html`
and the rendered PDF still carried the uncorrected text. Correct — and when I swept for it rather than
fixing only the three you named, **four more live instances** turned up, all in artifacts a reviewer or
a data consumer would actually read:

| Artifact | What it still said | Status |
|---|---|---|
| `submission/sources.pdf` (+ its builder) | The legacy three-class table: "US Government work (FDA/EMA/USPTO) — values reproducible without restriction", "reproduced as summary statistics **under fair use**", "exactly the records they **may lawfully reuse**" | fixed |
| `submission/narrative.html` → `.pdf` | "748 rows are public-domain (patents, FDA/EMA), 227 CC-BY, 984 summary statistics" — the superseded blanket figures | fixed |
| `submission/methodology.html` → `.pdf` | Acquisition table whose rows were **labelled with rights classes** ("Regulatory — public domain", "Patents — public domain", "Other literature — summary statistics"), deriving a rights position from a retrieval route | fixed |
| `schema.md`, `SOURCES.md`, `README.md`, `submission/README.md` | The legacy vocabulary presented as a rights determination, including the fair-use assertion | fixed |

All four PDFs now verify clean against a phrase sweep (`under fair use`, `lawfully redistributable`,
`reproduce without restriction`, `may lawfully reuse`, `US Government work (FDA/EMA/USPTO)`). The
legacy `redistribution` column is **retained on the rows** and explicitly marked superseded, so
nothing is rewritten in history — but it is no longer published as a rights position anywhere.

The lesson I am taking: the fix was authored once and applied where it was reported, and in five
other places the old text sat unchallenged because nobody had looked there. **A correction is not
landed until it is swept for.**

### Also regenerated, with the ladder as you specified

- Workbook rebuilt, **18 sheets**, now including `01f_signoff_gate_audit`.
- Ladder in the narrative and in `data/study_counts.csv` reads
  **56 typed → 39 with measurements → 19 passing this endpoint's audit**, with every rung's loss
  reason and an explicit line that none of the three is a count of *qualified* trials. The rung
  labels are deliberately shouty in the CSV so a reader cannot skim past the qualifier, and
  `submission_stats.py` now **hard-errors** rather than publishing a silent zero if a rung goes
  missing — which it had been doing, after I renamed the rungs and three ladder figures rendered
  as 0.
- The 224 holds are reported as **proposed**, with "zero withdrawn, zero cleared", in the PADP, the
  narrative, the sources doc, both READMEs and `SOURCES.md`. I have neither included nor excluded
  them.
- QC: **PASSED**, 9 warnings, all pre-existing and deliberate. Endpoint audit: **PASSED**.
- Page limits hold: narrative 10/12, methodology 5/5, PADP 4/5.

### Three defects I found in my own work while doing this

Worth stating plainly, because two of them had been silently corrupting figures:

1. **The rights ledger truncated its own join key** at 110 characters, which broke the join for
   **16 of 70 sources** — FDA review and registry rows showed an unresolved rights class in
   `sources.pdf` although their licence had in fact been determined. Now unanimous on all 70.
2. **Gate 7's own measurement pooled species.** I counted animal rows as "everything not human",
   which absorbed the 9 unresolved and multi-species rows into the animal side — the exact pooling
   the gate forbids, inside the check for that gate. Corrected to count on `subject_class`, so it
   now agrees with QC at 1,453 / 497 / 9.
3. A QC diagnostic counted **201** sequences where the Phase 2 gate four lines below counted **200**;
   one record is a nucleotide triphosphate mixture with no sequence to state. Corrected to 200.

## 6. What this receipt does not claim

It does not claim the endpoint is sign-off ready: zero rows clear the twelve gates. It does not
claim the three corrected overstatements were the only ones — they are the ones I found. It does not
claim any gate verdict is German's; the verdicts are mine, measured and reproducible, and he can
overturn any of them.

Release remains **NOT ELIGIBLE** on this branch. The classifier remains **BLOCKED**. The freeze
remains **NOT GRANTED**.

— Rocksteady
