# OligoTox-Coagulopathy — a curated coagulation-toxicity dataset for oligonucleotide therapeutics

Per-measurement coagulation data for therapeutic oligonucleotides, curated for the
**NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge, Phase 2**.
Coagulopathy is the fifth endpoint on the Challenge's list of toxicities of interest.

Everything for this endpoint lives in this folder. The endpoint dossier —
what the repository held before this dataset existed, and what changed — is
[`coagulopathy.md`](./coagulopathy.md).

| | Count |
|---|---:|
| Oligonucleotides | **218** |
| Coagulation measurements | **2,685** |
| Per-position modification records | **1,039** (52 oligos) |
| Sources | **100** |
| Oligos with a published sequence | 104 / 218 |
| Graded rows (0/1/2/3) | 867 — 463 / 312 / 66 / 26 |
| Structural QC | 64 / 64 checks pass |
| Numeric values located in their cited source | 2,019 / 2,019 |
| Rows adversarially re-checked against sources | 174 — 0 fabrications found |
| Human-system measurements | **1,183** (44%) — 749 participants · 380 primary blood/plasma · 40 purified human protein · 11 cells/tissue · 3 unresolved |
| Human interventional trials (deduplicated, coagulation endpoint) | **30** (18 registry-identified; 6 flagged for verification) |
| Animal-system measurements | 1,476 |
| Compounds with both human and animal data | 30 of 218 |

**Phase 2 submission package** — all four required parts, built by one command:

| Deliverable | Limit | File |
|---|---|---|
| Narrative document | ≤12 pp | `OligoTox-Coagulopathy_Narrative.pdf` (5 pp) |
| Methodology document | ≤5 pp | `OligoTox-Coagulopathy_Methodology.pdf` (5 pp) |
| Public Access & Dissemination Plan | ≤5 pp | `OligoTox-Coagulopathy_PADP.pdf` (4 pp) |
| Dataset + data dictionary | — | `OligoTox-Coagulopathy_Dataset.xlsx`, `data/*.csv`, `schema.md` |
| Sources & provenance (supporting) | — | `OligoTox-Coagulopathy_Sources.pdf` — all 100 sources, the database each came from, and a link-checked URL for every one |

**Getting the original papers.** `sources/DOWNLOAD_MANIFEST.csv` gives, per source, the
landing page, a direct-download URL where one exists, the licence, and whether we may
redistribute it. `bash scripts/fetch_original_papers.sh` downloads the 53 that are fetchable
without a subscription — USPTO patent PDFs, DailyMed label PDFs and open-access full text —
into a git-ignored `originals/` folder. The remaining 26 are publisher-restricted: the
manifest points at the landing page, which is where institutional access applies. FDA review
packages and EMA assessment reports are free but sit behind a document picker rather than a
stable URL, so the manifest names the exact document and links the application record.

The workbook carries two analysis tabs beyond the raw tables: **`human_measurements`** —
every human row with the compound's sequence, per-position chemistry map and toxicity score
carried onto it, so the most important subset needs no join — and **`German's analysis`** —
one row per compound with just the oligo, its sequence, the modification to that sequence,
and its toxicity.

`python3 scripts/make_release.py` rebuilds all of it from the committed extraction records
and fails rather than shipping: 55 structural checks, every numeric value re-checked against
its source document, and the page limits enforced on the PDFs. Status assessment against the
Phase 2 instructions and the work-plan: [`STATUS.md`](./STATUS.md).

```
data/          oligos · measurements · modifications · sources  (the dataset)
sources/
  documents/   the 74 retrieved primary documents every row cites
  extraction/  the raw per-bundle extraction records the build consumes
  SOURCES.md   source registry
scripts/       build_dataset.py · validate_dataset.py · verify_against_sources.py
schema.md      data dictionary, controlled vocabularies, grading rubric
METHODOLOGY.md how the dataset was produced
coagulopathy.md the endpoint dossier
```

Rebuild and check from a clean checkout — no network needed:

```bash
python3 toxicity/coagulopathy/scripts/build_dataset.py        # sources/extraction -> data/
python3 toxicity/coagulopathy/scripts/validate_dataset.py     # 36 structural checks
python3 toxicity/coagulopathy/scripts/verify_against_sources.py  # values vs source text
```

---

## Human versus animal

`species_class` (`human` / `animal` / `not_determined`) and `human_system` carry this
distinction — **not** `study_type`, which encodes the study design only. A purified-protein
assay counts as a human system when the proteins are human, which is how 433 human in-vitro
and ex-vivo rows become visible as human at all; `species_class_basis` records how each row
was decided, and 26 rows whose source never states the origin stay `not_determined` rather
than being quietly assigned.

Only **30 of 213 compounds carry both human and animal data**. That is the ceiling on any
translation claim built from this release.

## One endpoint per folder

Everything here is coagulopathy. 6 rows are marked `endpoint_scope = scope_adjacent` —
a complement marker, a transcript level, blanket adverse-event statements — kept as context
their extractor flagged, but never counted as coagulation measurements. A QC check fails the
build if a readout is neither recognisably coagulation nor marked, and no source document in
this folder is shared with another endpoint's.

## Counting: what is and is not a trial

**46 verified human interventional trials with a coagulation endpoint** — 21 identified by
a registry number. This figure **replaces the 30 published on 2026-10-01**, which was an
under-count produced by a defect in my own clustering code and which is hereby retracted.
Do not cite 30.

The headline is reproducible: a study enters it only when it is an interventional trial,
reports a coagulation endpoint, and carries an identity (registry number, trial acronym or
sponsor protocol code) that lets it be deduplicated against its other appearances. A QC
check re-derives the flag from those three columns and fails the build if it cannot.

### Why the number went up, not down

Beebop's 2026-10-01 review asked for the six flagged clusters to be inspected before 30
was relied on. Inspecting them found a fourth defect of the same family as the three
reported on 2026-09-30, and it ran in the opposite direction to the flag's implication.

A pooled-analysis record carries a protocol field that *enumerates the trials it pools* —
`pooled FCS safety set (CS6 + CS7)`, `Pool 2 (integrated long-term safety pool: CS2 + CS3 +
CS5 + CS7)`, `All Volanesorsen Treated Patients (CS1 + CS13 + ...)`. Every code in those
strings was emitted as an identity token, so **one pooled record unioned an entire
development programme into a single "trial"**. A second mechanism crossed programmes: a
record naming a comparator or prior therapy (`olezarsen; volanesorsen as prior therapy`)
carried both compound keys and bridged two different drugs. The result was that one
register row held nine volanesorsen trials *and* an olezarsen trial, and another put
eplontersen inside inotersen's CS2.

Four changes close it:

1. **Pooled analyses are not trials and not identifiers.** The 43 pooled records are
   partitioned out before clustering and published separately in
   [`data/pooled_analyses.csv`](data/pooled_analyses.csv) (sheet `pooled_analyses`), each
   carrying the member protocols it names and its counting rule. They stay as evidence — a
   regulatory pooled safety table is real — but a pooled number is never attributed to one
   trial.
2. **A bare protocol code is qualified by the sponsor compound number**, taken from the
   record's own protocol string or from the subject programme of its source document.
   `ISIS 304801-CS7` and `ISIS 678354-CS7` are different trials. Where no programme can be
   established, a bare `CS2` identifies nothing and no longer merges — unqualified, it had
   put nusinersen and volanesorsen in one cluster.
3. **A comparator is not a subject compound.** Eplontersen's `ION-682884-CS3` carries
   inotersen as its concurrent active reference arm; that is one trial, correctly recorded,
   and it no longer reads as an over-merge.
4. **Acronyms are compared on their head**, and a registry-verified crosswalk links each
   registry number to the sponsor protocol code its documents use. `ATLAS-A/B (also written
   ATLAS-AB)` and `ATLAS-A/B` are one name; without the crosswalk that trial was counted
   twice.

The four fitusiran trial identities were checked against the ClinicalTrials.gov API (v2, read
2026-10-02) and all four agree with what two independent documents gave us —
`NCT03417102`/`EFC14768`/ATLAS-INH, `NCT03417245`/`EFC14769`, `NCT03549871`/`EFC15110`/ATLAS-PPX,
`NCT03754790`/`LTE15174`/ATLAS-OLE. **The extracted identities were sound; the clustering over
them was not.** This was a code defect, not an extraction defect.

### Over-merge is now a QC failure, not a comment

55 checks passed while two drugs sat in one trial row. Three checks now make that
impossible: two registry numbers **from the same registry** in one cluster fails, two
sponsor compound numbers fails, and any `OVER_MERGE_*` flag fails. Two numbers from
*different* registries do **not** fail — one trial legitimately holds both an NCT and a
EudraCT number, so that is recorded as an alias and flagged for linkage review (Beebop's
correction, 2026-10-02). One reconciled exception is declared in code with the evidence
that reconciles it: the FDA reviewer's own annotation records the mipomersen–warfarin
interaction study as `MIPO2900509` in the filing checklist and `MIPO2900210` in the
Clinical Summary.

**Zero clusters now fail the over-merge test, and zero headline trials carry a review
flag.** The six clusters flagged on 2026-10-01 were artefacts of the defects above; the
largest remaining cluster is five source records.

### The register

[`data/studies.csv`](data/studies.csv) (sheet `human_trials`) holds **211 distinct study
records** built from the 293 non-pooled raw observations — 82 duplicate appearances merged,
because the same trial is reported by its registry entry, its publication, its regulatory
assessment *and* its label. 141 identified trials are registered and **excluded** from the
headline: 115 report no coagulation endpoint, 26 carry no usable identifier. Labels,
regulatory summaries, observational studies, case reports, healthy-volunteer laboratory
work and spontaneous reporting are never trials.

For scale: the dataset's 749 human *clinical measurement rows* were never 749 trials, and
89 of them are FAERS spontaneous reports, which are not a study at all.

### Rows are now linked to trials

`measurements.study_id` and `study_id_basis` connect each clinical row to the register.
Keying on source plus compound alone resolved 243 of 749 rows, because one regulatory
review covers six trials of the same drug; a second pass reads the row's own
`source_locus`, notes and quote for the registry number or protocol code it already cites.
**424 of 749 clinical rows now resolve to exactly one trial**, across 39 trials, and
nothing is unmatched. The remaining 325 stay `NOT_RESOLVED` with their candidate count
recorded in `study_id_basis`: an arm misattribution is worse than a missing link. Closing
them means re-reading the loci those rows already cite, which is research, not a code fix.

## What kind of observation each row is

Two booleans could not express the difference between a bleeding event, a prolonged assay
in a healthy volunteer, an intended anticoagulant effect and a measured null. `evidence_class`
does, and `evidence_class_basis` names the rule that assigned it:

| Class | Rows | |
|---|---:|---|
| `intended_pharmacodynamic` | 971 | on-target effect of a compound designed to alter coagulation |
| `measured_negative` | 640 | endpoint measured and unchanged |
| `unintended_lab_disturbance` | 408 | laboratory change the source presents as unintended |
| `outcome_not_attributed` | 292 | bleeding/thrombotic outcome the source does *not* present as adverse |
| **`adverse_outcome_source_attributed`** | **160** | **bleeding/thrombotic outcome the source presents as adverse** |
| `baseline_reference` | 120 | pre-dose draw — a reference point, not an outcome |
| `unresolved_observation` | 77 | no direction, no flag, or endpoint not reported |
| `unattributed_lab_change` | 17 | measured change with neither flag set |

The adverse-outcome subset is therefore derivable without re-reading the inventory. Every
value is `evidence_class_review_status = curator_derived_unreviewed`: it is a rule, not a
scientist's adjudication.

**These classes are species-agnostic and must be read with `species_class`.** The two
classes above were called `adverse_clinical_outcome` and `clinical_outcome_unattributed`
until 2026-10-03. That was wrong: a mouse tail-vein transection is a bleeding outcome too,
and **222 of the 292 rows in the old `clinical_outcome_unattributed` were mouse, monkey, rat
or pig** (Beebop, 2026-10-02). The rows were correctly typed throughout — `species_class`,
`species`, `study_type`, `human_system` and `human_system_subtype` all said animal, and the
workbook splits human from animal on `species_class`, so no animal row ever reached the
human sheets — but a reader filtering `evidence_class` alone would have read five animal
rows as human adverse events. The names are fixed, and a QC check now fails the build if any
class whose name contains "clinical" carries a non-human row. The human clinical subset is
`human_system_subtype == participant` (749 rows); no `evidence_class` value means it.

### Rows that are not coagulation readouts

Six rows are `endpoint_scope = scope_adjacent`: they are kept because a source reports them
beside a coagulation endpoint, not because they are one. Every one of them had been given a
core coagulation category — `COG-MSR0345` said `clotting_time` for complement fragment Bb
while its own note read "ADJACENT, NOT A COAGULATION READOUT" (Beebop flagged this row;
auditing found the other five). Each now carries its true category
(`complement_marker`, `target_transcript_level`, `infusion_reaction`,
`blanket_adverse_event_statement`), the curator's original value in
`readout_category_as_curated`, and `cross_endpoint_referral` naming the endpoint it belongs
to. A QC check fails the build if a scope-adjacent row wears a coagulation category.

## Read this before using the data: the dataset has two axes, not one

**1,720 of the 2,388 rows are ON-TARGET pharmacology, not toxicity.** The compounds with
the most published coagulation numbers are, unsurprisingly, the ones *designed* to change
coagulation: anti-factor-XI and anti-factor-XII antisense, prekallikrein and factor-VII
programmes, anticoagulant aptamers, fitusiran lowering antithrombin. A model trained on
these rows without the axis flags will learn *"anticoagulant drugs prolong aPTT"* — true,
circular, and useless for safety prediction.

Two boolean columns keep the axes apart, and **both may be true on one row**:

| | rows |
|---|---:|
| `on_target_effect` only — designed anticoagulant/procoagulant pharmacology | 1,576 |
| `unintended_toxicity` only — coagulation disturbance presented as an adverse effect | 289 |
| **both** — an on-target compound whose effect the source reports as harm | 144 |
| neither — context rows (assay controls, comparators, background) | 379 |

The 144 both-true rows are the scientifically interesting class: fitusiran is the clearest
case, where antithrombin lowering is the mechanism of action *and* the mechanism of the
thrombotic events. The dataset does not resolve that tension; it records it.

## What the data shows

**The class effect is now quantified per compound, from one study.** Among rows that are
*not* on-target pharmacology, full-phosphorothioate compounds show a median aPTT ratio of
**1.42× control** with 17 of 48 rows above 1.5×. This is the effect the safety literature
states at class level ("prolongation of coagulation time … at relatively high doses of PS
backbone ASOs") expressed as per-compound numbers. **The caveat is load-bearing: 42 of
those 48 rows come from a single source** (US 9,061,044, seven ASOs in cynomolgus monkey),
across only 9 distinct oligonucleotides. It is one well-controlled experiment, not a
meta-analysis, and should not be cited as though it were.

**A source that contradicts itself, where the prose is the wrong half.** US 9,061,044
states verbatim that "PT, aPTT and fibrinogen were not significantly altered in monkeys
treated with ISIS oligonucleotides compared to the PBS control." Its own Table 87 shows
every ISIS group above PBS at every timepoint, in a clean compound rank order peaking at
4 h — ISIS 420957 39.13 s against PBS 20.13 s, a 1.94× prolongation. The dataset extracts
the tables and carries the contradicting sentence verbatim in
`severity_stated_by_source` on all 126 rows, so the disagreement travels with the data
instead of being silently resolved. Any pipeline that reads conclusions rather than tables
records a false negative here.

**aPTT saturates on phosphorothioate content in vitro.** One source demonstrates that the
in-vitro aPTT assay cannot discriminate toxic from non-toxic compounds because PS content
alone drives it. Nulls from that assay are encoded as a *method limitation* in `notes`,
never as a safety finding — the opposite reading would teach a model that a saturated
assay means a safe compound.

## Grading

`coag_tox_grade` is an ordinal 0–3 assigned **mechanically** from the control-referenced
ratio using **CTCAE v5.0** laboratory cut-offs — a published, citable rule, not thresholds
invented here. It is applied only to the readouts CTCAE actually defines (aPTT, PT, INR,
TT, ACT prolongation; fibrinogen decrease). The other 1,521 rows are **left ungraded**,
each stating why in `grade_basis`, rather than graded by an invented threshold. Every grade
is `provisional`, and every grade is reproducible from `ratio_to_control` — a QC check
re-derives all 867 and fails the build on any disagreement.

**One limit of that rule is load-bearing and is flagged in the data.** CTCAE grades against
the *upper limit of normal*; these sources publish a control mean, not a reference range.
A ratio a few percent above 1.00 is therefore not evidence of a real prolongation, and
grading it 1 would manufacture coagulopathies out of assay noise. Two guards apply:
a source-stated measured null is regraded to 0 whatever its ratio (122 rows), and every
remaining grade with a ratio in 1.0–1.2× carries
`grade_caveat = within_reference_range_resolution` (155 rows) so it can be filtered out.
**Filter on `grade_caveat` before treating grade 1 as a finding.**

`source_stated_grade` is separate: 15 rows whose source states its own CTCAE grade
(one grade 1, two grade 2, five grade 3, seven grade 4). It is kept in its own column
because a reported clinical grade and a ratio-derived one are different rules and must not
share a field — but a severity query should read both.

## What verification found

174 rows — every grade-3 row plus stratified samples of grade-2, measured-null,
unintended-toxicity, clinical and qualitative rows — were re-checked against their sources
by independent reviewers instructed to *refute* them. Result: **117 confirmed, 50
corrected, 2 refuted, 5 unverifiable, and no fabricated value or quote anywhere.**

**The defect that sank the sibling kidney dataset does not repeat here.** That review found
its negative class was substantially "nobody looked" rather than "looked and found
nothing". Four independent reviewers tested this dataset's nulls specifically and could not
break them: of the null rows sampled, essentially all are measured nulls with the assay and
control arm traceable in the source, and rows where the endpoint was merely *not mentioned*
are consistently typed `NOT_REPORTED` with notes that say so in terms — several warning
"Do not score this as evidence of no effect."

Nine classes of defect were found and **fixed in the build**, not by hand, so a rebuild
reproduces the corrections and QC re-checks them:

| Fix | Rows | What was wrong |
|---|---:|---|
| R1 | 18 | A "relative aPTT" is a *subtracted* delta; dividing it by the control gave fold-change-minus-one and understated grades. |
| R2 | 87 | Percent **inhibition** filed as percent *of control* — inverting every potency ranking (74% inhibition is 0.26 of control, not 0.74). |
| R3 | 113 | A combination arm referenced to the untreated cell, scoring the partner drug's effect as the oligo's. |
| R4 | 120 | Pre-dose baseline draws carried as dosed effect measurements. |
| R5 | 122 | A ratio a hair above 1.00 outranking the source's own statement that nothing changed. |
| R0 | 41 | Grades left stale after R1–R3 changed the ratio under them. |
| R7 | 15 | Source-stated CTCAE grades invisible to a grade query. |
| R8 | 11 | An absence of signal flagged as an adverse finding. |
| R9 | 17 | Combination arms with no column naming the partner agent. |

A tenth was a provenance failure: 80 rows cited a supplementary PDF that was never staged,
because the parser took the *last* filename in a cell naming several files. Their quotes
were faithful to the real article all along; the citation pointed at the wrong document.
`document_file` now resolves to the first path in the cell, and a QC check fails the build
if any source's document is not on disk.

Findings recorded but **not** mechanically fixable, and carried as open issues in
[`coagulopathy.md`](./coagulopathy.md): `unintended_toxicity` is partly curator inference
rather than source framing; `effect_direction` drifts in sign on process-named readouts
(e.g. "coagulation inhibited" recorded as an increase); some values cited *by* a source
rather than measured *in* it are not distinguished; and adjacent-row pickup in reflowed
patent tables was confirmed once and needs a row-label re-check of three large tables.

## Provenance

Every measurement carries `source_id`, `source_locus` (exact table, figure, section or
label section) and a `verbatim_quote` copied from the document. Structural QC enforces
that all three are present on all 2,388 rows. `redistribution` is tracked per row:
1,382 rows are public domain (US patents and FDA labels), 383 are CC BY or CC BY-NC,
426 CC BY-NC-ND, 192 publisher-restricted, 5 unresolved.

Missing values are `NOT_REPORTED` (the source does not report it) or `NOT_APPLICABLE`
(the field has no meaning for this row). Never blank, never zero, never a guess.

## Known limitations

- **Grades are provisional** and mechanical; no subject-matter expert has reviewed them.
  Grade 1 in particular should be filtered on `grade_caveat` (see Grading).
- **104 of 218 oligos have a published sequence.** 787 human rows belong to compounds
  without one. A `sequence_status` column says which kind of gap each is: a polydisperse
  mixture and a two-strand duplex *cannot* have one 5′→3′ string, but ~12 approved
  compounds are marked `recoverable_from_WHO_INN_nomenclature` — the WHO INN chemical name
  spells out every residue, and the sibling kidney dataset already proved that parse
  (`toxicity/kidney/scripts/fill_inn_sequences.py`). That is the single highest-value
  remaining task for the human subset.
- Historically no *clinical* compound had a sequence; three now do (nusinersen,
  volanesorsen, tofersen), reconstructed from per-residue chemical nomenclature in the EMA
  and FDA dossiers —
  inotersen, nusinersen, fitusiran, eplontersen, olezarsen, imetelstat and fesomersen are
  all sequence-less in the public record used here. Sequence-to-phenotype modelling is
  therefore restricted to patent and preclinical compounds; clinical rows can only be
  modelled at the chemistry-class level.
- **PMO chemistry rests on regulatory silence.** Not one measured PT or aPTT value exists
  for eteplirsen, golodirsen, viltolarsen or casimersen. Their rows record that the labels
  name no coagulation finding, explicitly flagged as *silence, not a measured null*.
- **Volanesorsen**, a compound with well-documented severe thrombocytopenia, is represented
  only by an n=4 negative; its EU SmPC and the APPROACH/COMPASS reports were not retrieved.
- **Prothrombotic rows come overwhelmingly from fitusiran**, so "hypercoagulability" risks
  being learned as "fitusiran".
- Figure-only values were never digitised: those rows carry `NOT_REPORTED` with
  `readout_is_qualitative = TRUE` rather than a number read off a plot.
