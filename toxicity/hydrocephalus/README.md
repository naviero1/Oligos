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
| Measurement rows | **904** |
| Oligonucleotides described | **34** |
| — of which carry at least one measurement | 29 |
| Distinct sources | 52 |
| Tier-A rows with a positive finding | 55 |
| Tier-A rows that are explicit measured negatives | 326 |
| Grade-3 (severe) rows | 18 |
| Oligonucleotides with a published sequence | 4 |
| QC checks run / failed | 30 / 0 |

**Endpoint tier** — **A** = hydrocephalus (communicating, obstructive or normal-pressure), ventriculomegaly / ventricular dilatation, shunt or drain placement. **B** = raised intracranial pressure, papilloedema, aseptic or chemical meningitis, arachnoiditis, CSF leak or protein rise, post-lumbar-puncture syndrome.

| Tier | Rows |
|---|---:|
| A | 382 |
| B | 522 |

**Study type**

| Study type | Rows |
|---|---:|
| animal_invivo | 5 |
| background_epidemiology | 3 |
| clinical_case | 5 |
| clinical_trial | 347 |
| pharmacovigilance | 456 |
| regulatory_label | 88 |

**Ascertainment** — how the endpoint's presence or absence was established. A grade of 0 is only permitted where this is `measured_null`

| Ascertainment | Rows |
|---|---:|
| measured_null | 694 |
| measured_positive | 209 |
| not_assessed | 1 |

**Attribution, as stated by the source** — what the SOURCE concluded about causation. `not_discussed` dominates because registry and pharmacovigilance records carry no causality assessment at all — that is a property of those sources, not an omission here

| Attribution | Rows |
|---|---:|
| disease_attributed | 3 |
| drug_attributed | 23 |
| not_discussed | 878 |

**Toxicity axis** — `disease_background_rate` rows carry no compound; `delivery_procedure_complication` rows are attributable to the lumbar puncture rather than to any molecule

| Axis | Rows |
|---|---:|
| csf_composition_disturbance | 198 |
| csf_dynamics | 1 |
| csf_pressure_disturbance | 123 |
| delivery_procedure_complication | 198 |
| disease_background_rate | 3 |
| therapeutic_ventricular_effect | 2 |
| ventricular_enlargement | 379 |

**Severity grade** — rubric in [`SCHEMA.md`](SCHEMA.md#hydroceph_grade-rubric-03); all grades are provisional

| `hydroceph_grade` | Rows |
|---|---:|
| *(not graded)* | 26 |
| 0 | 694 |
| 1 | 100 |
| 2 | 66 |
| 3 | 18 |

**Delivery route** — systemically dosed oligonucleotides are included as a deliberate route contrast

| Route | Rows |
|---|---:|
| NOT_APPLICABLE | 3 |
| intracerebroventricular | 3 |
| intrathecal_lumbar | 404 |
| intravenous | 216 |
| intravitreal | 24 |
| subcutaneous | 254 |

**Readout category**

| Category | Rows |
|---|---:|
| csf_composition | 176 |
| csf_dynamics | 64 |
| csf_pressure | 123 |
| histopathology_choroid_ependyma | 1 |
| hydrocephalus_event | 220 |
| procedure_complication | 177 |
| shunt_or_drain_intervention | 40 |
| ventricular_morphometry | 103 |

**Redistribution rights** — tracked per row

| Rights | Rows |
|---|---:|
| cc_by | 8 |
| cc_by_nc | 3 |
| public_domain | 880 |
| summary_stat_only | 5 |
| verify | 8 |

**Event clusters** — rows sharing an `event_cluster_id` describe **one** clinical episode and must not be counted as independent events.

| `event_cluster_id` | Rows |
|---|---:|
| `L1-EVT-01` | 5 |
| `L2-BASELINE` | 3 |
| `L3-TOFERSEN-SAE` | 3 |
| `N1-SPAK` | 2 |
| `N2-AQP4` | 3 |

**Largest sources** (top 10 of 52)

| `source_id` | Rows |
|---|---:|
| `FAERS_openFDA` | 456 |
| `NCT02519036` | 36 |
| `NCT02594124` | 36 |
| `NCT02623699` | 36 |
| `NCT03070119` | 24 |
| `NCT03761849` | 24 |
| `NCT03186989` | 22 |
| `NCT03225846` | 21 |
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

- **Ventricular volume rose with tominersen dose, measured by protocol-specified
  MRI against a concurrent placebo arm.** The phase 1/2a trial (NCT02519036) made
  ventricular volume a pre-specified MRI outcome. From screening to day 197 the
  placebo arm moved 35.58 → 36.46 mL (+2.5%, n=12), while the two highest dose
  arms moved 39.33 → 44.43 mL (+13.0%, n=9) and 27.53 → 33.02 mL (+19.9%, n=10).
  In the open-label extension (NCT03342053) the ventricular-volume boundary shift
  integral rose **46.1% on monthly dosing against 18.8% on bimonthly** at 15
  months. These are the only rows in the dataset where the ventricles were
  *measured* rather than incidentally observed, and they are the reason the
  adverse-event counts below should not be read as the whole signal. Group sizes
  are small and the dataset computes no test statistic — the values are recorded
  exactly as published.
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
  and aseptic meningitis (sections 5.1–5.2); the EU SmPC quantifies them —
  serious increased intracranial pressure and/or papilloedema in 2.7% and aseptic
  meningitis in 1.4% of tofersen-treated participants, with CSF white blood cells
  increased in 27.9% and CSF protein increased in 26.5% (n=147) — and names no
  hydrocephalus at all.
- **The two regulators read the same nusinersen evidence differently, and the
  dataset records both.** The FDA label mentions hydrocephalus only in **section
  6.2 Postmarketing Experience**. The EMA gives it **its own subheading under
  section 4.4 Special warnings and precautions for use**: *"communicating
  hydrocephalus not related to meningitis or bleeding … Some patients were
  implanted with a ventriculo-peritoneal shunt."* A jurisdiction contrast on an
  identical molecule is a datum about how strong the signal is judged to be, not
  a discrepancy to be resolved away. Meanwhile nusinersen's own posted trial
  results contain no hydrocephalus term — the signal is entirely post-marketing,
  which is exactly what the FAERS rows (22 hydrocephalus reports) show.
- **The successor trial made the endpoint a primary outcome.** GENERATION HD2
  (NCT05686551) specifies, as a *primary* outcome, change from baseline in
  structural MRI "assessing any new abnormalities including radiographic features
  consistent with hydrocephalus". Results are not posted. That row carries no
  grade and `ascertainment = not_assessed`: it is evidence about how this endpoint
  is now ascertained, not about the endpoint.
- **Two rodent studies put an oligonucleotide on both sides of the endpoint.** A
  SPAK-targeting siRNA delivered in a lipid nanoparticle *prevents*
  ventriculomegaly in a kaolin-induced model; an AQP4-targeting siRNA *aggravates*
  it in an intraventricular-haemorrhage model, against the dataset's only
  **designed** negative control — a scrambled non-targeting siRNA. The protective
  rows sit on `tox_axis = therapeutic_ventricular_effect` and are ungraded, so a
  beneficial effect can never be read as an absent one. The SPAK duplexes are also
  the only compounds here with a published sequence, and each passes the
  sense/antisense reverse-complement check the QC suite runs.
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
python3 scripts/extract_ctgov.py          # ClinicalTrials.gov posted adverse-event tables
python3 scripts/extract_ctgov_outcomes.py # pre-specified ventricular MRI outcome measures
python3 scripts/extract_faers.py          # openFDA FAERS  (cached; re-runs cost no quota)
python3 scripts/extract_labels.py         # DailyMed Structured Product Labels
python3 scripts/build_literature.py       # curated full-text and EMA SmPC rows
python3 scripts/build_nonclinical.py      # curated rodent rows (both effect directions)
python3 scripts/build_oligos.py           # design predictors parsed from labels
python3 scripts/assemble.py               # canonical tables + provenance registry + merged view
python3 qc/validate.py                    # 30 checks; writes qc/stats.json
python3 scripts/render_docs.py            # regenerates the counts in this file
```

Every network call is cached under `sources/raw/`, so a re-run is offline and
deterministic. No dependency beyond the Python standard library.

## Provenance and licensing

Every measurement carries `source_id`, `source_ref` and an **exact**
`source_location` — a JSON path, a label section with its LOINC code, or a
figure/table locus. Category words such as "results" are rejected by the QC
suite.

The overwhelming majority of the dataset is **public domain**: US Government
works (ClinicalTrials.gov, FAERS, DailyMed labels). The remainder is CC BY;
`summary_stat_only` where a licence carries a no-derivatives term; and `verify`
for the EMA rows, whose reuse terms were not established in this session — the
verbatim text is quoted as evidence and a redistributor should resolve the
licence before republishing those values. `redistribution` records this per row,
and every value it takes is actually used by rows in the table.

## Status

**v0.1.** All grades ship `grade_status = provisional` pending subject-matter
expert review. Known gaps, including the absence of published sequences and of
nonclinical animal rows, are stated as numbered open items in
[`METHODOLOGY.md`](METHODOLOGY.md#open-items) rather than left for a reader to
discover.
