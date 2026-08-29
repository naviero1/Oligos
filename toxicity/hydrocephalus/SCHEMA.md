# Schema — OligoTox-Hydrocephalus

Data dictionary, controlled vocabularies and the grading rubric for the
**hydrocephalus** endpoint of the NIH/NCATS Oligonucleotide Toxicity (OligoTox)
Open Data Challenge, Phase 2.

Three normalized UTF-8 CSV tables. `oligos` and `measurements` join on `oligo_id`;
both carry `source_id` into `sources`.

| File | Grain | Key |
|---|---|---|
| `data/oligos.csv` | one row per oligonucleotide — identity and design predictors | `oligo_id` (PK) |
| `data/measurements.csv` | one row per oligo × population/model × route × dose × readout × arm | `measurement_id` (PK), `oligo_id` (FK) |
| `data/sources.csv` | provenance registry | `source_id` (PK) |

`data/hydrocephalus_merged.csv` is a **generated** denormalized join of the first
two, produced by `scripts/build_merged.py`. It is never hand-edited.

---

## Missing-value convention

Inherited from the sibling **OligoTox-CNS** release so the two datasets can be
pooled. Three distinct states, never collapsed:

| Literal | Meaning |
|---|---|
| `NOT_REPORTED` | The source does not report this value. It has **not** been estimated, imputed, or filled from background knowledge. |
| `NOT_APPLICABLE` | The field has no meaning for this row (e.g. a comparator arm for a single-arm case report). |
| *(empty cell)* | The field does not apply to this table's row type. |

Booleans are `TRUE`/`FALSE`. No value is ever guessed. See `METHODOLOGY.md`
§"No-fabrication policy".

---

## Endpoint definition and tiers

This dataset's endpoint is **hydrocephalus and the CSF-dynamics disturbances that
produce or accompany it**. Because "hydrocephalus" alone is a rare, hard endpoint
that would yield too few rows to model, the dataset records a second, wider tier —
explicitly labelled, never silently pooled.

| `endpoint_tier` | Definition | Examples |
|---|---|---|
| **A** | The core endpoint: a ventricular or CSF-volume outcome. | hydrocephalus (communicating or obstructive), ventriculomegaly, ventricular volume change, CSF hypersecretion, shunt or external ventricular drain placement |
| **B** | CSF-dynamics adjacent: a pressure, composition or flow disturbance on the causal path to, or clinically bundled with, tier A. | raised intracranial pressure, papilloedema, aseptic/chemical meningitis, CSF protein or white-cell rise, post-lumbar-puncture syndrome, choroid-plexus or ependymal injury |

Tier C — general CNS or neurological adverse events with no ventricular, pressure,
or CSF readout — is **out of scope and contributes no rows**. Route of
administration is not evidence of this endpoint: an intrathecally dosed compound
with only a renal or hepatic readout does not belong here.

**Any analysis that pools tier A with tier B must say so.** `endpoint_tier` exists
precisely so the pooling is a stated choice rather than an accident.

---

## Column definitions — where they live, and why not here

**The authoritative column list is [`scripts/data_dictionary.py`](scripts/data_dictionary.py).**
It is rendered as the `data_dictionary` sheet of
`OligoTox-Hydrocephalus_Dataset.xlsx`, and `qc/validate.py` asserts both
directions: every column present in every CSV has an entry, and every entry
corresponds to a real column.

The definitions are deliberately **not** duplicated in this file. An earlier
version of this schema listed `purity_pct`, `purity_method` and
`identity_confirmation` as columns of `oligos.csv` while the builder emitted none
of them, and nothing caught it — the same documentation-versus-data drift the
sibling kidney dataset was reviewed for, reproduced here. Prose cannot be
enforced; a module that the QC suite imports can be. What follows is the part of
the schema that is conceptual rather than enumerative.

---

## The four tables

| File | Grain | Key |
|---|---|---|
| `data/oligos.csv` | one row per oligonucleotide — identity and design predictors | `oligo_id` (PK) |
| `data/measurements.csv` | one row per oligo × population/model × route × readout × arm | `measurement_id` (PK), `oligo_id` (FK) |
| `data/modifications.csv` | **one row per nucleotide position** — the per-position chemistry | (`oligo_id`, `strand`, `position_5to3`) |
| `data/sources.csv` | provenance registry | `source_id` (PK) |

`data/hydrocephalus_merged.csv` is a **generated** denormalized join of the first
two, produced by `scripts/assemble.py`. It is never hand-edited.

### Why `modifications.csv` exists

The Challenge brief requires the dataset to contain *"the sequences of all oligos
tested, as well as the location of all chemical modifications in each oligo"*. A
per-oligo motif string such as `5-10-5` states the design; it does not state the
location. This table states the location, one row per position.

It is filled **per dimension, not per oligo**: a row may carry a known sugar and
an unknown base, or the reverse.

- Where a label states the motif in words — tofersen's *"five MOE nucleosides at
  the 5′ and 3′-ends of the molecule flanking a gap of ten 2′-deoxynucleosides"*
  for a 20-mer — the **sugar** at every position is fixed without naming a single
  base.
- Where a sequence is published, the **nucleobase** at every position is known
  even if the source states no modification at all.

Both cases are marked in `basis`, and `qc/validate.py` checks that positions run
contiguously 1..n, that n equals `oligos.length_nt`, and that the bases in this
table reproduce `oligos.sequence_5to3_asprinted` exactly where one is stored.

The four morpholinos contribute **no** rows. Their labels give a molecular formula
but the phosphorus count is P = n for eteplirsen, golodirsen and casimersen and
P = n−1 for viltolarsen, because some carry a 5′-piperazine bearing an extra
phosphorus and some do not. Length is therefore ambiguous for that class, and a
per-position table cannot be built on an ambiguous length.

### On `length_nt`

Length is recorded with a `length_nt_basis` saying how it was established:
stated in the label, counted from a published sequence, or derived from the
label's molecular formula. The derivation is legitimate only because the tofersen
label states **both** a 20-mer and P19, pinning P = n−1 for that chemistry class;
it is applied to nusinersen (P17, S17 → 18 residues) and to nothing else.

### On purity and identity characterisation

The Challenge asks specifically for *"the methods used to purify and characterize
oligo identity"*. A full-text sweep of all sixteen committed US labels for
purity, purification, chromatography, mass-spectrometry, identity and
characterisation language returns **no statement about the drug substance in any
of them** — every hit is a patient baseline characteristic or an efficacy assay.
`purity_pct` is therefore `NOT_REPORTED` for every compound in this release, and
`purity_method` / `identity_confirmation` are `NOT_REPORTED` except where a
research source names a supplier. This is a property of the published record, and
the sibling OligoTox-CNS release reports the same for all 1,839 of its compounds.

---

## `hydroceph_grade` rubric (0–3)

Severity is graded on **clinical/structural consequence**, not on the size of a
number. The rubric is written for this endpoint and is **not** transferable to or
from the sibling `nephrotox_grade` or `cns_tox_grade` columns.

| Grade | Definition |
|---|---|
| **0** | The endpoint was assessed and no ventricular, pressure or CSF-composition abnormality was found. Requires `ascertainment = measured_null`. |
| **1** | **Mild / biochemical or asymptomatic.** A CSF composition change (protein or cell-count rise), or an imaging finding without symptoms, requiring no intervention and resolving spontaneously. |
| **2** | **Moderate / symptomatic, reversible.** Symptomatic raised intracranial pressure, papilloedema, or aseptic/chemical meningitis; ventriculomegaly with symptoms; managed medically or by dose interruption, without a permanent CSF diversion. |
| **3** | **Severe.** Hydrocephalus requiring permanent CSF diversion (shunt or external ventricular drain), a serious adverse event coded as hydrocephalus, or a CSF-dynamics event that is fatal, life-threatening, or causes persistent disability. |

Rules that constrain the rubric, and which the QC suite enforces:

1. **Every graded row must state its `grade_basis`.** Where a grade derives from a
   regulatory seriousness classification rather than from a clinical description,
   `grade_basis` says exactly that.
2. **Grade 0 requires `ascertainment = measured_null`.** A row that was never
   assessed is `not_assessed` with an **empty** grade, not a zero. This is the
   rule the sibling kidney dataset lacked.
3. **The scale is censored by study type.** An `in_vitro` or `csf_composition`
   row cannot reach grade 3, because grade 3 is defined by whole-organism
   intervention. Grades are therefore **not comparable across `study_type`**, and
   any model trained on this column must carry `study_type` as a covariate or
   stratify on it. This is stated here rather than discovered later.
4. **Grade is a property of the measurement, not of the compound.** The same
   oligonucleotide may carry grade 3 in one arm and grade 0 in another.
5. All grades ship `grade_status = provisional` pending subject-matter-expert
   review.

---

## Deliberate limits of this schema

- **It records no disproportionality statistic.** Pharmacovigilance rows carry
  report counts and the drug's total report base; PRR/ROR and their intervals are
  left to the user, because a spontaneous-reporting ratio is an analysis, not a
  measurement, and its denominator assumptions belong to whoever makes them.
- **It records no attribution of its own.** `attribution_as_stated` reproduces
  the source's conclusion. Where a source draws none, the value is `not_discussed`
  and stays that way.
- **It records no number read off a figure.** Where a source publishes a value
  only graphically, `readout_value` is `NOT_REPORTED` and
  `readout_is_qualitative` is `TRUE`.
