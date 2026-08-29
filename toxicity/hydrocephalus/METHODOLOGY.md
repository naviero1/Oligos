# Methodology — OligoTox-Hydrocephalus

Materials and methods for the hydrocephalus dataset, NIH/NCATS Oligonucleotide
Toxicity (OligoTox) Open Data Challenge, Phase 2 (Data Generation).

---

## 1. Design

OligoTox-Hydrocephalus is a **curated** dataset. No wet-lab experiment was
performed. The methods below are therefore of two kinds, and are kept strictly
separate:

- **(a) the experimental and reporting methods of the source studies**, recorded
  so that a user knows how each measurement was generated; and
- **(b) the curation methods used here** to retrieve, extract, harmonise and
  grade them.

Conflating the two would let curation choices masquerade as experimental fact.
This separation follows the sibling **OligoTox-CNS** release, whose conventions —
the `NOT_REPORTED` / `NOT_APPLICABLE` / empty distinction, `grade_basis`,
`grade_status`, `readout_is_qualitative`, and a QC suite that exits non-zero —
this dataset adopts so the two can be pooled.

### No-fabrication policy (strict)

No sequence, count, denominator, quotation, DOI, PMID or NCT identifier in this
dataset was recalled from memory or inferred. Every value was copied by a script
from a payload committed under `sources/raw/`, or transcribed from a full text
that is also committed, and carries the exact locus it came from. Where a source
is silent the field is `NOT_REPORTED`. **No number was read off a figure**: where
a value is published only graphically, `readout_value` is `NOT_REPORTED` and
`readout_is_qualitative` is `TRUE`.

---

## 2. Endpoint definition

Inclusion required a **ventricular, CSF-volume, CSF-pressure or CSF-composition
outcome** reported for an identified oligonucleotide, or a population baseline
for such an outcome. The two-tier definition and the exclusion of tier C
(general neurological adverse events with no CSF or ventricular readout) are in
[`SCHEMA.md`](SCHEMA.md#endpoint-definition-and-tiers).

Two boundary decisions worth stating explicitly:

- **Route of administration is not evidence of the endpoint.** An intrathecally
  dosed compound with only a renal or hepatic readout contributes no row. This is
  the same rule the sibling kidney dossier applied in reverse when it declined to
  treat its three `intrathecal` rows as CNS evidence.
- **Acute neurotoxicity is out of scope.** The Challenge brief deprioritises
  "alterations of neuronal electrical activity", and that axis is already covered
  by the sibling OligoTox-CNS release. Calcium-oscillation and acute
  tolerability endpoints therefore contribute nothing here, even where the same
  source reports both.

---

## 3. Source identification and retrieval

Sources were sought across five deliberately different modalities, because any
single one is biased: a literature search finds published positives, a registry
finds protocol-collected events including zeros, a spontaneous-reporting system
finds post-marketing signals, a label finds regulator-adjudicated risks, and an
epidemiological cohort finds the disease baseline.

| Modality | Route used | What it contributes |
|---|---|---|
| Trial registry | ClinicalTrials.gov v2 API, `/api/v2/studies/<NCT>` | Per-arm adverse-event counts **with denominators and comparator arms**, including explicitly reported zeros |
| Pharmacovigilance | openFDA `drug/event` API | Post-marketing reporting proportions across the whole marketed oligonucleotide class |
| Regulatory labelling (US) | DailyMed v2 API, `spls/<setid>.xml` | Verbatim, regulator-adjudicated risk statements with LOINC-coded sections |
| Regulatory labelling (EU) | EMA Annex I Summaries of Product Characteristics | The EU position on the same molecules, which differs materially from the US one, plus quantified incidences the US label does not give |
| Primary literature | Europe PMC REST `fullTextXML` | The index case and its mechanism; the disease baseline |
| Disease epidemiology | Europe PMC REST `fullTextXML` | Untreated-population incidence — the confounder control |

Every payload retrieved is committed under `sources/raw/`, so the dataset rebuilds
offline and any value can be checked without network access.

---

## 4. Extraction

Three of the four components are **deterministic parsers**, not transcription.
This was a deliberate choice: the single largest defect class found in the review
of the sibling kidney dataset was hand-transcription error — 21 rows recording a
rat study as mouse, a 15-day design as 7 days, and a published dose as absent.
A parser cannot make that error, and its mapping tables are auditable in one
place.

**4.1 ClinicalTrials.gov (`scripts/extract_ctgov.py`, 323 rows).** Walks the
`resultsSection.adverseEventsModule` of each committed study record. Emits one
row per (trial × adverse-event term × arm), copying `numAffected` and
`numAtRisk` from the named JSON path, which is written into `source_location`.
Four human judgements are made, each written out once in the open: the MedDRA
term → tier/category map, the grading rule, the comparator-arm map, and the
trial → compound map. MedDRA terms are matched case-insensitively but never
normalised or spelling-corrected — `Meningitis asceptic` is preserved as the
source prints it in NCT04617860.

**4.1b ClinicalTrials.gov outcome measures (`scripts/extract_ctgov_outcomes.py`,
21 rows).** Kept as a separate component because the epistemics differ. An
adverse-event count is a clinician noticing something and coding it; a
pre-specified outcome measure is a quantity the protocol required to be measured
in every participant, on a schedule, by an instrument. These are the only rows in
the dataset where the ventricles were measured rather than incidentally observed,
and the only continuous ones. Selection is an **explicit allow-list**, not a
pattern match: a pattern over this field for "CSF" sweeps in cerebrospinal-fluid
pharmacokinetics and neurofilament biomarkers, which are drug exposure and
neuronal injury, not CSF dynamics. Values are recorded exactly as published; no
change score or test statistic is computed.

**4.2 openFDA FAERS (`scripts/extract_faers.py`, 456 rows).** One exact query per
(drug, MedDRA term) pair. An aggregation counting drugs within a term was tried
first and rejected: openFDA caps a `count` aggregation at 100 buckets without an
API key, which silently drops precisely the rare drug/term pairs this endpoint is
about. The direct pair query returns `meta.results.total` with no cap, so a zero
is a real zero. Transport failures are retried and **never cached as zeros**.

The term strings themselves are validated before use, and this caught a real
defect. FAERS stores several CSF preferred terms in an abbreviated form — `CSF
PROTEIN INCREASED`, not `CEREBROSPINAL FLUID PROTEIN INCREASED` — and the two are
not interchangeable: the expanded string matches nothing, and an earlier version
of this component queried it and recorded a zero for all nineteen drugs. A
pre-flight check now queries every term database-wide before it is used and drops
any string FAERS does not know, with a line in `notes/faers_extraction_report.txt`
saying so, rather than letting an unknown string manufacture false negatives.
Three of the twenty-seven candidate terms were dropped this way
(`COMMUNICATING HYDROCEPHALUS`, `VENTRICULOMEGALY`,
`CEREBROSPINAL FLUID SHUNT INSERTION`).

For context rather than as rows: database-wide, FAERS holds 5,367 reports
carrying `HYDROCEPHALUS` against 20,692,690 reports in total. Anyone wanting a
disproportionality measure has the numerator, the drug denominator and this
background in the dataset and its audit trail; the dataset computes none itself.

**4.3 DailyMed labels (`scripts/extract_labels.py`, 80 rows).** Parses the SPL
XML and records the matching sentence verbatim with its section title and LOINC
display name. A label that is **silent** on the endpoint produces an explicit
`measured_null` row rather than no row. The word "ventricular" is ambiguous in a
drug label — cardiac ventricular repolarisation and arrhythmia are common — so
matching is CNS-anchored and every sentence rejected by the cardiac filter is
written to the audit report, so the filter itself can be checked.

**4.4 Curated literature (`scripts/build_literature.py`, 11 rows).** These cannot
be parsed; each comes from prose a human read. Each row therefore stores the
**verbatim sentence** it was taken from in `attribution_evidence`, so the value
and its evidence travel together.

**4.4b Per-position chemistry (`scripts/build_modifications.py`, 122 rows).** The
Challenge requires the location of every chemical modification, not a motif
string. Sugar chemistry is resolved at all twenty tofersen positions and all
eighteen nusinersen positions from the labels' own words; nucleobase is resolved
at all twenty-one positions of each sequenced SPAK duplex. The morpholinos are
excluded because their length is ambiguous from the published formula. See
`SCHEMA.md` §"Why `modifications.csv` exists".

**4.5 Design predictors (`scripts/build_oligos.py`).** Chemistry is parsed from
section 11 DESCRIPTION of the committed labels by high-precision patterns, and
every filled value stores the sentence it matched in `design_source_text`.
Identity for unapproved compounds comes from the ClinicalTrials.gov records.

### Purification and identity characterisation

The Challenge asks specifically for the methods used to purify and characterise
oligo identity. Because the compounds were made by their sponsors and not here,
what can be reported is what each source states — and for this release the answer
is almost nothing. A full-text sweep of all sixteen committed US labels for
purity, purification, chromatography, mass-spectrometry, identity and
characterisation language returns **no statement about the drug substance in any
of them**; every hit is a patient baseline characteristic or an efficacy assay.
`purity_pct` is `NOT_REPORTED` for all 35 compounds. The two research-reagent
sources name a supplier (GenePharma, Shanghai) but no purification or
identity-confirmation method. No purity value has been estimated, inferred from a
synthesis platform, or carried across from another compound.

This matches the sibling OligoTox-CNS release, which reports the same for all
1,839 of its oligonucleotides, and is a property of the published literature
rather than of the curation.

### Experimental and reporting methods of the source studies

Recorded here because they determine what the numbers mean.

- **Registry adverse-event tables.** ClinicalTrials.gov results modules declare a
  `frequencyThreshold` governing the *other-events* table; that value is copied
  into every affected row's `ascertainment_basis`. Terms are MedDRA preferred
  terms at the version the sponsor states (`sourceVocabulary`). Assessment is
  recorded as the registry states it (`assessmentType`, commonly
  `NON_SYSTEMATIC_ASSESSMENT` — i.e. adverse events as reported, not
  systematically solicited). **No trial in this release performed protocol-
  specified ventricular imaging**; the tier-A events are clinically diagnosed
  adverse events.
- **FAERS.** Voluntary spontaneous reports, unvalidated, with no exposure
  denominator and no causality assessment.
- **Labels.** Postmarketing-experience sections describe reports from a
  population of uncertain size, for which a causal relationship cannot always be
  established; warnings sections describe risks the regulator has adjudicated.
- **Stoker 2021.** Single patient; serial MRI, serial CSF sampling and a
  **lumbar infusion study** measuring resistance to CSF outflow.
- **Viscidi 2021.** Retrospective matched-cohort study in the US Optum
  de-identified EHR database (~100 million persons), 1 Jan 2007 – 22 Dec 2016;
  hydrocephalus ascertained by ICD-9/ICD-10 code after the index date.

---

## 5. Harmonisation and grading

All categorical fields use the controlled vocabularies in
[`SCHEMA.md`](SCHEMA.md), enforced by the QC suite rather than asserted.

`hydroceph_grade` is a **new ordinal column with its own written rubric**. It is
not a reuse of the sibling `nephrotox_grade` or `cns_tox_grade`, both of which are
written in terms specific to their own organ and are not transferable — a point
the hydrocephalus dossier made before this dataset existed. Every graded row
carries in `grade_basis` the exact rule that produced its grade, so the mapping
from a regulatory seriousness classification, or from a MedDRA term, to a
clinical severity grade is visible on the row rather than implicit.

**The scale is censored by study type**, and this must be carried into any model:
a FAERS row cannot express a clinical course, and a CSF-composition row cannot
reach grade 3, which is defined by whole-organism intervention. `study_type` is a
strong shortcut predictor of the grade and should be a covariate or a
stratification variable, never ignored.

---

## 6. Ascertainment and attribution

These two columns are the methodological core of the release.

**Ascertainment.** A review of the sibling kidney dataset found that grade 0 there
conflated "measured and null" with "nobody looked", and that its negative class
was "substantially *nobody looked* rather than *looked and found nothing*". For
hydrocephalus that conflation would be fatal, because ventricular imaging is
almost never protocol-specified. The `ascertainment` column therefore records how
each presence or absence was established, and the QC suite **enforces** that a
grade of 0 occurs only where ascertainment is `measured_null`.

Three grades of negative are distinguished, weakest last:

1. **An explicitly reported zero in a comparator arm.** The term is listed in the
   trial's table with a count of 0 for that arm — the strongest negative in the
   dataset, because the same protocol found the event elsewhere.
2. **A trial-level absence from a table the law requires to be complete.** No
   tier-A term appears in a trial's posted serious-adverse-event table, which 42
   CFR 11.48(a)(4)(ii)(A) requires to list *all* serious adverse events with no
   frequency threshold. This is a reported zero for serious events. It is not a
   claim that imaging was performed, and a non-serious event below the 5 percent
   threshold of subparagraph (B) would not appear. See **OI-01**.
3. **A silent label, or a FAERS zero.** Weakest: reflects reporting behaviour as
   much as clinical absence.

**Attribution.** `attribution_as_stated` records **what the source concluded**,
never an inference made here. Where a source draws no conclusion the value is
`not_discussed` and stays that way — which is why that value dominates: registry
and pharmacovigilance records carry no causality assessment at all. Attribution
for those rows must be read structurally, from the concurrent comparator arm and
from the disease-baseline rows, which is exactly why both are in the dataset.

---

## 7. Quality control

`qc/validate.py` runs **39 checks** and exits non-zero on any failure. They cover
primary-key uniqueness and non-emptiness on all three tables; referential
integrity on both foreign keys; controlled-vocabulary conformance on ten columns;
grade range; the requirement that every graded row state its rule; the
grade-0/`measured_null` rule; the requirement that `not_assessed` rows carry no
grade; presence of `source_ref` and a `source_location` that is a locus rather
than a category word; `n_affected ≤ n_at_risk`; the no-fabricated-sequence rule;
the requirement that background-rate rows carry no compound; and byte-identical
regeneration of the derived merged view.

Two checks close the defect class this release was itself caught by. The data
dictionary lives in `scripts/data_dictionary.py`, and the suite asserts in **both
directions** that every column in every CSV has an entry and every entry
corresponds to a real column. An earlier version of `SCHEMA.md` declared
`purity_pct`, `purity_method` and `identity_confirmation` while the builder
emitted none of them, and nothing caught it — exactly the documentation-versus-
data drift the sibling kidney dataset was reviewed for. Prose cannot be enforced;
an imported module can.

Three further checks cover the per-position table: positions must run contiguously
1..n, n must equal `oligos.length_nt`, and the bases recorded there must
reproduce `oligos.sequence_5to3_asprinted` exactly wherever a sequence is stored.

One check is a genuine cross-source consistency test rather than a format test:
for every compound whose label publishes **both** a molecular formula and a
residue count, the phosphorus count in the formula must equal the length or the
length minus one, since a linear oligonucleotide of *n* residues has *n−1*
internucleoside linkages. Tofersen passes (`P19`, 20-mer). This check depends on
no external source being correct and would catch a transcription error that two
agreeing documents would not.

`qc/validate.py` writes `qc/stats.json`, and `scripts/render_docs.py` renders the
statistics block of `README.md` from it. **No count in the documentation is
typed.** The sibling kidney deck claimed "every number in this deck regenerates
from `data/`" while every count in it was typed inline, and a review found one
statistic published as four mutually incompatible numbers; this is the mechanism
that makes the claim true rather than aspirational.

---

## 8. Intended use for predictive modelling

The dataset supports the Challenge's aim — predicting toxicity from oligonucleotide
design — but the honest framing is narrower than "train a classifier on it", and
the columns are arranged to make the narrower framing easy and the naive one hard.

What it supports well:

- **Route and compartment as predictors.** Intrathecal versus systemic exposure,
  with systemic oligonucleotides included specifically as the contrast.
- **Separating drug effect from procedure and disease effect.** The three
  `tox_axis` values, the comparator columns and the background-rate rows are what
  make this possible; no other public dataset for this endpoint assembles them
  together.
- **Modelling ascertainment explicitly.** A model that ignores `ascertainment`
  will learn the reporting process, not the biology.

What it does **not** yet support, stated plainly:

- **Sequence-based prediction.** No compound in this release carries a published
  sequence (**OI-02**). Design predictors are currently chemistry- and
  design-level, not sequence-level.
- **Compound-level dose–response.** Doses are recorded where a source states
  them, but the tier-A events are too few for a within-compound dose model.
- **Any causal claim about an individual compound.** With 25 tier-A positive
  rows against a disease baseline whose incidence rate ratio is 4.7, the dataset
  is powered to describe and to control, not to attribute.

---

## Coverage, and what was found but not taken

Source discovery ran as a structured multi-modal pass — eight blind sweeps by
retrieval modality, four completeness critics tasked only with naming what the
sweeps had missed, and twelve gap-fills chasing what the critics named. It
returned 188 unique sources, of which this release carries 53.

The remaining 100 verified sources are listed in
[`notes/source_backlog.md`](notes/source_backlog.md) with their retrieval routes,
exact loci and per-source caveats. That list is the honest statement of this
release's completeness limit: the largest untouched bodies of evidence are
EudraVigilance and WHO VigiBase substance-level reaction counts, the EMA CHMP
assessment reports for tofersen and nusinersen, FDA pharmacology/toxicology
review documents, the Japanese PMDA label and risk-management plan, and two
patent families carrying sequences. None of it is needed for anything asserted
here; all of it would deepen the dataset.

Two corrections the critics produced are already folded into `data/`: the FAERS
term-string defect described in §4.2, and the second drug-attributed clinical
case (§"L5" in `scripts/build_literature.py`) that stopped this release
describing hydrocephalus as a tominersen-specific finding.

## Open items

Numbered so they can be cited from elsewhere in the repository.

**OI-01 — RESOLVED in this release.** Trial-level negatives were originally recorded
as an absence argument about a document. The governing rule has since been retrieved
and verified: **42 CFR 11.48(a)(4)(ii)(A)** requires a results submission to include a
*"Table of all serious adverse events grouped by organ system, with the number and
frequency of each event by arm or comparison group"* — with **no** frequency
threshold, unlike subparagraph (B), which sets 5 percent within any arm for
non-serious events. Absence of a tier-A term from a posted serious-adverse-event
table is therefore a **reported zero for serious events**, not an unreported one, and
that is what the 253 tier-A negative rows now assert. The regulation text is committed
at `sources/raw/ecfr_42CFR11.48_results_reporting.xml` and cited in every affected
row's `ascertainment_basis`.

Two limits remain, and are stated in those rows rather than here: a **non-serious**
ventricular event below the 5 percent threshold would not appear, and none of this is
evidence that ventricular imaging was performed. The residual open question is narrow
— whether every trial in this release is an "applicable clinical trial" bound by the
rule, or posted voluntarily under the same structure.

**OI-02 — PARTIALLY CLOSED; still open for every clinical compound.** Four
compounds now carry a published sequence — the SPAK siRNA duplexes, printed in
full in their source's Materials section, each verified by the sense/antisense
reverse-complement check now run by the QC suite. They are research reagents.
`sequence_5to3_asprinted` remains `NOT_REPORTED` for all 25 clinical and marketed
compounds, which is where the Challenge's requirement actually bites. No US label prints the base sequence; both intrathecal ASO labels render
the structure as a figure with no text layer. The WHO INN Recommended lists spell
out every residue longhand and are this project's established route for sequence
recovery (the sibling kidney dataset filled 9 compounds that way and validated the
parser by reproducing two known duplexes character-for-character). That retrieval
is not attempted here rather than approximated. Until it is done, the Challenge's
"sequences of all oligos tested" requirement is unmet for this endpoint.

**OI-03 — PARTIALLY CLOSED.** Five rodent rows are now carried from two studies
(`scripts/build_nonclinical.py`). Both publish their ventricular measurements
graphically only, so all five are qualitative — the dose–response resolution this
item was opened for is still missing. Systematic extraction of
intracerebroventricular and intrathecal animal tolerability studies has not been
attempted.

**OI-04 — CLOSED.** `tox_axis = therapeutic_ventricular_effect` now carries two
rows: a SPAK-targeting siRNA that prevents ventriculomegaly in a kaolin-induced
model. The axis exists so these rows can be excluded from compound-toxicity
analysis in one filter; they are graded `not_graded`, because grading a prevented
lesion on a harm scale would make a beneficial effect look like an absent one.

**OI-08 — NEW: the dataset now has one designed control, and needs more.** The
AQP4 study's scrambled non-targeting siRNA is the only compound in the release
built to be inactive. Every other negative is a comparator arm, a reported zero
or a silent label. A review of the sibling kidney dataset found its "negative
controls" were negative *observations* rather than designed controls; this
release has the same weakness, now with one exception and with the distinction
recorded in `arm_role` and `ascertainment` rather than glossed.

**OI-05 — PARTIALLY CLOSED.** EMA Summaries of Product Characteristics are now
carried for nusinersen, tofersen and inotersen (8 rows), and they proved to be
more than a duplicate of the US labels: the EMA gives hydrocephalus its own
subheading under section 4.4 for nusinersen where the FDA confines it to section
6.2, and the EU tofersen SmPC quantifies incidences the US label does not.
Inotersen, for which DailyMed returns no current US label, is covered only by its
EU label. Still open: the EPAR nonclinical assessment reports, other EMA products,
and non-EU/US regulators (PMDA, MHRA). One MHRA Drug Safety Update on
nusinersen-associated communicating hydrocephalus was identified during source
discovery and is **not** yet extracted.

**OI-06 — grades are provisional.** Every row ships `grade_status = provisional`.
No subject-matter expert has reviewed the rubric or its application.

**OI-07 — one compound row is a composite.** `casimersen_or_golodirsen` covers
NCT03532542, an extension study of both compounds whose posted adverse-event
table does not separate them. Its rows must not be treated as belonging to either
compound individually.
