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
| Regulatory labelling | DailyMed v2 API, `spls/<setid>.xml` | Verbatim, regulator-adjudicated risk statements with LOINC-coded sections |
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

**4.2 openFDA FAERS (`scripts/extract_faers.py`, 266 rows).** One exact query per
(drug, MedDRA term) pair. An aggregation counting drugs within a term was tried
first and rejected: openFDA caps a `count` aggregation at 100 buckets without an
API key, which silently drops precisely the rare drug/term pairs this endpoint is
about. The direct pair query returns `meta.results.total` with no cap, so a zero
is a real zero. Transport failures are retried and **never cached as zeros**.

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

**4.5 Design predictors (`scripts/build_oligos.py`).** Chemistry is parsed from
section 11 DESCRIPTION of the committed labels by high-precision patterns, and
every filled value stores the sentence it matched in `design_source_text`.
Identity for unapproved compounds comes from the ClinicalTrials.gov records.

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

`qc/validate.py` runs **29 checks** and exits non-zero on any failure. They cover
primary-key uniqueness and non-emptiness on all three tables; referential
integrity on both foreign keys; controlled-vocabulary conformance on ten columns;
grade range; the requirement that every graded row state its rule; the
grade-0/`measured_null` rule; the requirement that `not_assessed` rows carry no
grade; presence of `source_ref` and a `source_location` that is a locus rather
than a category word; `n_affected ≤ n_at_risk`; the no-fabricated-sequence rule;
the requirement that background-rate rows carry no compound; and byte-identical
regeneration of the derived merged view.

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

**OI-02 — no sequences.** `sequence_5to3_asprinted` is `NOT_REPORTED` for every
compound. No US label prints the base sequence; both intrathecal ASO labels render
the structure as a figure with no text layer. The WHO INN Recommended lists spell
out every residue longhand and are this project's established route for sequence
recovery (the sibling kidney dataset filled 9 compounds that way and validated the
parser by reproducing two known duplexes character-for-character). That retrieval
is not attempted here rather than approximated. Until it is done, the Challenge's
"sequences of all oligos tested" requirement is unmet for this endpoint.

**OI-03 — no nonclinical rows.** The dataset is entirely human. Animal studies
dosing oligonucleotides by the intracerebroventricular or intrathecal route and
reporting ventricular or CSF-dynamics outcomes were not extracted in this pass.
These would add the dose–response and mechanism resolution the clinical record
cannot provide.

**OI-04 — no protective/therapeutic rows.** Oligonucleotides developed *to treat*
hydrocephalus (for example agents targeting choroid-plexus CSF hypersecretion)
would populate `tox_axis = therapeutic_ventricular_effect`, which is declared in
the schema and currently used by no row. They are the natural negative-direction
control class.

**OI-05 — EMA and other regulators not covered.** Labelling evidence is US FDA
only. EMA SmPCs and EPAR nonclinical sections would add both statements and, for
compounds withdrawn from the US market such as inotersen — for which DailyMed
returned no current label — the only available regulatory text.

**OI-06 — grades are provisional.** Every row ships `grade_status = provisional`.
No subject-matter expert has reviewed the rubric or its application.

**OI-07 — one compound row is a composite.** `casimersen_or_golodirsen` covers
NCT03532542, an extension study of both compounds whose posted adverse-event
table does not separate them. Its rows must not be treated as belonging to either
compound individually.
