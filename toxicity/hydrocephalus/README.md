# OligoTox-Hydrocephalus

A curated, openly-releasable dataset pairing **oligonucleotide design** with
**measured hydrocephalus and CSF-dynamics outcomes**, built for the NIH/NCATS
Oligonucleotide Toxicity (OligoTox) Open Data Challenge, **Phase 2 (Data
Generation)**.

Hydrocephalus is the eighth and last endpoint on the Challenge's list of
toxicities of interest. Until this release it was the endpoint this repository
recorded as **`not-addressed`**: zero rows, zero sources, no scope decision
([`../hydrocephalus.md`](../hydrocephalus.md)). That dossier
set three conditions for advancing it — acquire a primary source, add CNS terms
to the vocabularies, and write a separate graded column with its own rubric —
and concluded that doing so would be *"a second dataset, not an extension of this
one."* This directory is that second dataset.

---

## Dataset at a glance

<!-- BEGIN GENERATED: qc/validate.py writes qc/stats.json; scripts/render_docs.py renders this block. Do not hand-edit. -->

| | Count |
|---|---:|
| Measurement rows | **680** |
| Oligonucleotides described | **28** |
| — of which carry at least one measurement | 26 |
| Distinct sources | 46 |
| Tier-A rows with a positive finding | 25 |
| Tier-A rows that are explicit measured negatives | 253 |
| Grade-3 (severe) rows | 15 |
| Oligonucleotides with a published sequence | 0 |
| QC checks run / failed | 29 / 0 |

**Endpoint tier** — **A** = hydrocephalus (communicating, obstructive or normal-pressure), ventriculomegaly / ventricular dilatation, shunt or drain placement. **B** = raised intracranial pressure, papilloedema, aseptic or chemical meningitis, arachnoiditis, CSF leak or protein rise, post-lumbar-puncture syndrome.

| Tier | Rows |
|---|---:|
| A | 278 |
| B | 402 |

**Study type**

| Study type | Rows |
|---|---:|
| background_epidemiology | 3 |
| clinical_case | 5 |
| clinical_trial | 326 |
| pharmacovigilance | 266 |
| regulatory_label | 80 |

**Ascertainment** — how the endpoint's presence or absence was established. A grade of 0 is only permitted where this is `measured_null`

| Ascertainment | Rows |
|---|---:|
| measured_null | 520 |
| measured_positive | 160 |

**Attribution, as stated by the source** — what the SOURCE concluded about causation. `not_discussed` dominates because registry and pharmacovigilance records carry no causality assessment at all — that is a property of those sources, not an omission here

| Attribution | Rows |
|---|---:|
| disease_attributed | 3 |
| drug_attributed | 13 |
| not_discussed | 664 |

**Toxicity axis** — `disease_background_rate` rows carry no compound; `delivery_procedure_complication` rows are attributable to the lumbar puncture rather than to any molecule

| Axis | Rows |
|---|---:|
| csf_composition_disturbance | 138 |
| csf_dynamics | 1 |
| csf_pressure_disturbance | 84 |
| delivery_procedure_complication | 179 |
| disease_background_rate | 3 |
| ventricular_enlargement | 275 |

**Severity grade** — rubric in [`SCHEMA.md`](SCHEMA.md#hydroceph_grade-rubric-03); all grades are provisional

| `hydroceph_grade` | Rows |
|---|---:|
| *(not graded)* | 3 |
| 0 | 520 |
| 1 | 94 |
| 2 | 48 |
| 3 | 15 |

**Delivery route** — systemically dosed oligonucleotides are included as a deliberate route contrast

| Route | Rows |
|---|---:|
| NOT_APPLICABLE | 3 |
| intrathecal_lumbar | 356 |
| intravenous | 144 |
| intravitreal | 14 |
| subcutaneous | 163 |

**Readout category**

| Category | Rows |
|---|---:|
| csf_composition | 116 |
| csf_dynamics | 44 |
| csf_pressure | 84 |
| hydrocephalus_event | 217 |
| procedure_complication | 158 |
| shunt_or_drain_intervention | 1 |
| ventricular_morphometry | 60 |

**Redistribution rights** — tracked per row

| Rights | Rows |
|---|---:|
| cc_by | 8 |
| public_domain | 669 |
| summary_stat_only | 3 |

**Event clusters** — rows sharing an `event_cluster_id` describe **one** clinical episode and must not be counted as independent events.

| `event_cluster_id` | Rows |
|---|---:|
| `L1-EVT-01` | 5 |
| `L2-BASELINE` | 3 |
| `L3-TOFERSEN-SAE` | 3 |

**Largest sources** (top 10 of 46)

| `source_id` | Rows |
|---|---:|
| `FAERS_openFDA` | 266 |
| `NCT02594124` | 36 |
| `NCT02623699` | 36 |
| `NCT03070119` | 24 |
| `NCT03761849` | 24 |
| `NCT03186989` | 22 |
| `NCT03225846` | 21 |
| `NCT02519036` | 18 |
| `NCT05032196` | 18 |
| `NCT03842969` | 15 |

<!-- END GENERATED -->

---

## What makes this endpoint hard, and what the dataset does about it

Hydrocephalus is not like hepatotoxicity or nephrotoxicity. Three problems make a
naive dataset actively misleading, and each one is answered by a column rather
than by a caveat in a document nobody reads.

**1. The disease causes the endpoint.** The populations dosed with CNS
oligonucleotides — spinal muscular atrophy, Huntington's disease, ALS — have
elevated baseline rates of exactly this outcome. A matched-cohort study of 5,354
SMA patients in the **era before nusinersen was approved** found hydrocephalus at
15.5 per 100,000 person-months against 3.3 in matched non-SMA controls, an
incidence rate ratio of **4.7 (95% CI 2.4–10.2)**. A model trained on
drug-exposed rows alone would attribute a fourfold disease effect to the drug.
Those baseline rows are **in the dataset**, carrying no compound, on
`tox_axis = disease_background_rate`.

**2. The delivery procedure causes the endpoint.** Repeated lumbar puncture
produces post-LP syndrome, CSF leak and low-pressure states across every
intrathecal programme, in **placebo arms as much as treated arms**. Those rows
are kept and labelled `tox_axis = delivery_procedure_complication` so they can be
excluded from compound-attributable analysis in one filter.

**3. Almost nobody images the ventricles.** For most compounds, the absence of a
hydrocephalus finding means nobody looked. The `ascertainment` column separates
`measured_positive`, `measured_null` (actively assessed and not found),
`reported_threshold_limited` and `not_assessed`, and the QC suite **enforces**
that a grade of 0 can only be assigned where ascertainment is `measured_null`.

The result is a dataset whose negatives are as trustworthy as its positives —
which is what makes it trainable.

---

## What the data shows

These are observations recorded in the tables, not conclusions this project is
asserting; every one traces to a row and a locus.

- **Hydrocephalus among CNS-delivered oligonucleotides is tominersen-specific in
  the trial record.** Serious hydrocephalus or normal-pressure hydrocephalus
  adverse events appear in three separate tominersen studies (NCT03761849,
  NCT03342053, NCT03842969), including **2/263 against 0/264 in the concurrent
  placebo arm** of GENERATION HD1. Cerebral ventricle dilatation appears across
  all three tominersen dose arms of the open-label extension. No other
  intrathecal oligonucleotide programme — nusinersen, tofersen, BIIB080, BIIB105,
  WVE-120101, WVE-120102, WVE-003 — reports a tier-A serious event in its posted
  results.
- **The mechanism is documented end to end in one patient.** The index case
  (Stoker 2021, CC BY) records rising CSF protein to 2.64 g/L with lymphocytosis
  to 46 cells/mm³, then ventricular dilation on serial MRI, then **increased
  resistance to CSF outflow measured directly by lumbar infusion study**, then a
  ventriculoperitoneal shunt. That is a complete causal chain from tier B to tier
  A, and it is why the two tiers are recorded together but never pooled silently.
- **The other intrathecal ASOs show the pressure axis without the ventricular
  one.** The QALSODY label carries papilloedema, elevated intracranial pressure
  and aseptic meningitis (sections 5.1–5.2); the SPINRAZA label names
  hydrocephalus, aseptic meningitis and arachnoiditis in **section 6.2
  Postmarketing Experience** — that is, from spontaneous reports, not from the
  trials, whose posted results contain no hydrocephalus term.
- **Route contrasts.** Systemically dosed oligonucleotides are included
  deliberately so the intrathecal signal is testable rather than assumed. Their
  FAERS hydrocephalus counts are ~1 report against thousands, and the two
  hydrocephalus events in their trial records occur in populations where the
  disease itself causes hydrocephalus — paediatric brain tumours (imetelstat) and
  post-transplant hepatic veno-occlusive disease (defibrotide). One
  normal-pressure hydrocephalus signal sits in the **placebo arm** of an
  inclisiran trial (2/778).

---

## Layout

| Path | What it is |
|---|---|
| [`SCHEMA.md`](SCHEMA.md) | Data dictionary, controlled vocabularies, tier definitions, `hydroceph_grade` rubric |
| [`METHODOLOGY.md`](METHODOLOGY.md) | How the dataset was assembled; source-study methods kept separate from curation methods; open items |
| `data/oligos.csv` | One row per oligonucleotide — identity and design predictors |
| `data/measurements.csv` | One row per oligo × population/model × route × readout × arm |
| `data/sources.csv` | Provenance registry; row counts recomputed, never typed |
| `data/hydrocephalus_merged.csv` | **Generated** denormalized join. Never hand-edit; regenerate with `scripts/assemble.py` |
| `scripts/` | The four extraction components, the assembler and the doc renderer |
| `qc/validate.py` | Quality-control suite; exits non-zero on failure and writes `qc/stats.json` |
| `sources/raw/` | Every retrieved payload, committed, so any value can be re-derived offline |
| `notes/` | Per-component audit trails |

## Reproducing the dataset

From a clean checkout, in order:

```bash
python3 scripts/extract_ctgov.py      # ClinicalTrials.gov posted adverse-event tables
python3 scripts/extract_faers.py      # openFDA FAERS  (cached; re-runs cost no quota)
python3 scripts/extract_labels.py     # DailyMed Structured Product Labels
python3 scripts/build_literature.py   # curated full-text rows
python3 scripts/build_oligos.py       # design predictors parsed from labels
python3 scripts/assemble.py           # canonical tables + provenance registry + merged view
python3 qc/validate.py                # 29 checks; writes qc/stats.json
python3 scripts/render_docs.py        # regenerates the counts in this file
```

Every network call is cached under `sources/raw/`, so a re-run is offline and
deterministic. No dependency beyond the Python standard library.

## Provenance and licensing

Every measurement carries `source_id`, `source_ref` and an **exact**
`source_location` — a JSON path, a label section with its LOINC code, or a
figure/table locus. Category words such as "results" are rejected by the QC
suite.

The overwhelming majority of the dataset is **public domain**: US Government
works (ClinicalTrials.gov, FAERS, DailyMed labels). The remainder is CC BY, or
carried as summary statistics only where a licence carries a no-derivatives
term. `redistribution` records this per row, and every value it takes is actually
used.

## Status

**v0.1.** All grades ship `grade_status = provisional` pending subject-matter
expert review. Known gaps, including the absence of published sequences and of
nonclinical animal rows, are stated as numbered open items in
[`METHODOLOGY.md`](METHODOLOGY.md#open-items) rather than left for a reader to
discover.
