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
| Measurement rows | **1329** |
| Oligonucleotides described | **53** |
| — of which carry at least one measurement | 47 |
| Distinct sources | 190 |
| Tier-A rows with a positive finding | 62 |
| Tier-A rows that are explicit measured negatives | 735 |
| Grade-3 (severe) rows | 22 |
| Oligonucleotides with a published sequence | 13 |
| QC checks run / failed | 47 / 0 |

**Endpoint tier** — **A** = hydrocephalus (communicating, obstructive or normal-pressure), ventriculomegaly / ventricular dilatation, shunt or drain placement. **B** = raised intracranial pressure, papilloedema, aseptic or chemical meningitis, arachnoiditis, CSF leak or protein rise, post-lumbar-puncture syndrome.

| Tier | Rows |
|---|---:|
| A | 798 |
| B | 531 |

**Study type**

| Study type | Rows |
|---|---:|
| animal_invivo | 8 |
| background_epidemiology | 3 |
| clinical_case | 15 |
| clinical_trial | 757 |
| in_vitro | 2 |
| pharmacovigilance | 456 |
| regulatory_label | 88 |

**Ascertainment** — how the endpoint's presence or absence was established. A grade of 0 is only permitted where this is `measured_null`

| Ascertainment | Rows |
|---|---:|
| measured_null | 1108 |
| measured_positive | 220 |
| not_assessed | 1 |

**Attribution, as stated by the source** — what the SOURCE concluded about causation. `not_discussed` dominates because registry and pharmacovigilance records carry no causality assessment at all — that is a property of those sources, not an omission here

| Attribution | Rows |
|---|---:|
| disease_attributed | 3 |
| drug_attributed | 33 |
| not_discussed | 1293 |

**Toxicity axis** — `disease_background_rate` rows carry no compound; `delivery_procedure_complication` rows are attributable to the lumbar puncture rather than to any molecule

| Axis | Rows |
|---|---:|
| csf_composition_disturbance | 210 |
| csf_dynamics | 3 |
| csf_pressure_disturbance | 126 |
| delivery_procedure_complication | 188 |
| disease_background_rate | 3 |
| therapeutic_ventricular_effect | 2 |
| ventricular_enlargement | 797 |

**Severity grade** — rubric in [`SCHEMA.md`](SCHEMA.md#hydroceph_grade-rubric-03); all grades are provisional

| `hydroceph_grade` | Rows |
|---|---:|
| *(not graded)* | 26 |
| 0 | 1108 |
| 1 | 94 |
| 2 | 79 |
| 3 | 22 |

**Delivery route** — systemically dosed oligonucleotides are included as a deliberate route contrast

| Route | Rows |
|---|---:|
| NOT_APPLICABLE | 3 |
| NOT_REPORTED | 124 |
| in_culture_medium | 2 |
| intracerebroventricular | 6 |
| intrathecal_lumbar | 321 |
| intravenous | 359 |
| intravitreal | 59 |
| oral | 1 |
| subcutaneous | 452 |
| topical_enema | 2 |

**Readout category**

| Category | Rows |
|---|---:|
| csf_composition | 188 |
| csf_dynamics | 68 |
| csf_pressure | 126 |
| histopathology_choroid_ependyma | 3 |
| hydrocephalus_event | 629 |
| procedure_complication | 165 |
| shunt_or_drain_intervention | 43 |
| ventricular_morphometry | 107 |

**Redistribution rights** — tracked per row

| Rights | Rows |
|---|---:|
| cc_by | 13 |
| cc_by_nc | 3 |
| public_domain | 1290 |
| summary_stat_only | 15 |
| verify | 8 |

**Event clusters** — rows sharing an `event_cluster_id` describe **one** clinical episode and must not be counted as independent events.

| `event_cluster_id` | Rows |
|---|---:|
| `L1-EVT-01` | 5 |
| `L2-BASELINE` | 3 |
| `L3-TOFERSEN-SAE` | 3 |
| `L5-PT1` | 3 |
| `L5-PT2` | 6 |
| `N1-SPAK` | 2 |
| `N2-AQP4` | 3 |
| `N3-GAI2` | 5 |

**Largest sources** (top 10 of 190)

| `source_id` | Rows |
|---|---:|
| `FAERS_openFDA` | 456 |
| `NCT02594124` | 36 |
| `NCT02623699` | 36 |
| `NCT03070119` | 24 |
| `NCT03761849` | 24 |
| `NCT03186989` | 22 |
| `NCT03334617` | 22 |
| `NCT03225846` | 21 |
| `NCT02499328` | 19 |
| `NCT02519036` | 18 |

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
- **Within the registered-trial record the signal is tominersen's alone — but the
  endpoint is not tominersen-specific.** Serious hydrocephalus or normal-pressure
  hydrocephalus adverse events appear in three separate tominersen studies
  (NCT03761849, NCT03342053, NCT03842969), including **2/263 against 0/264 in the
  concurrent placebo arm** of GENERATION HD1, and cerebral ventricle dilatation
  appears across all three dose arms of the open-label extension. No other
  intrathecal programme with posted results — nusinersen, tofersen, BIIB080,
  BIIB105, WVE-120101, WVE-120102, WVE-003 — reports a tier-A serious event. That
  is a statement about registered trials, and it would be the wrong conclusion to
  stop there: the two strongest drug-attributed cases in this dataset come from
  outside that record entirely (next two bullets).
- **A second, independent oligonucleotide produced the same endpoint in both
  patients who received it.** In an n-of-1 protocol, two infants with KCNT1
  epileptic encephalopathy were dosed intrathecally with valeriasen — a different
  ASO, a different target, a different indication and age group — and **both**
  developed ventricular enlargement. Patient 1: severe communicating hydrocephalus
  with transependymal flow eight weeks after her ninth dose, CSF opening pressure
  55 cmH₂O at endoscopic third ventriculostomy, no improvement, care redirected to
  palliation. Patient 2: normal ventricles on day 55, enlargement on days 62 and
  64, external ventricular drain at opening pressure >20 cmH₂O, ventriculoperitoneal
  shunt on day 65. The authors state the events were *"attributable to dosing of
  the study drug"* and call this *"a potential monitorable toxicity of some
  intrathecal antisense oligonucleotides"*.
- **The two drug-attributed cases point to different mechanisms, so the dataset
  keeps them apart.** The tominersen index case was attributed to a **sterile
  meningitis** — CSF protein 2.64 g/L with lymphocytosis. The KCNT1 patients had a
  CSF inflammatory panel that was **negative** (albumin, IgG index, oligoclonal
  bands, neopterin), and their authors' working hypothesis is a **dose-related**
  effect. The evidence for that hypothesis is in the dataset as its only
  reduced-dose rechallenge row: after a two-year pause, patient 2 received two
  intrathecal doses (10 and 15 mg) and five intracerebroventricular doses (3–9 mg)
  under a revised protocol with periodic MRI ventriculograms, **without
  recurrence**. Inflammatory and dose-related routes to the same endpoint should
  not be pooled, which is what `tox_axis` and `event_cluster_id` are for.
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
- **One oligonucleotide is measured both in vitro and in vivo — the only such
  pair here.** An unmodified 18-mer oligodeoxynucleotide against Gαi2 produces
  irreversible ciliary stasis in cultured ependymal cells and, by the
  intracerebroventricular route in vivo, unilateral ventricular dilatation
  restricted to the infused side with a ruptured ependymal layer. It ships with
  two designed control oligonucleotides — a nonsense and an eight-mismatch
  sequence with equal base composition — both null on the same readouts, and it
  is the only source in the release stating a purity value (HPLC-purified,
  90–97%). Its chemistry is a contrast too: unmodified DNA, chosen by the authors
  expressly to avoid the toxicity of stable modified backbones.
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
| [`PHASE2_COMPLIANCE.md`](PHASE2_COMPLIANCE.md) | Every Phase 2 requirement mapped to what exists, what is missing and who owns it |
| `data/trial_registry.csv` | Every oligonucleotide trial with posted results — trial selection as a query, not a judgement |
| `data/measurements_human.csv` / `_animal.csv` | **Generated** views splitting the evidence by `subject_class` |
| `data/oligos.csv` | One row per oligonucleotide — identity and design predictors |
| `data/measurements.csv` | One row per oligo × population/model × route × readout × arm |
| `data/modifications.csv` | **One row per nucleotide position** — the location of each chemical modification |
| `data/sources.csv` | Provenance registry; row counts recomputed, never typed |
| `data/hydrocephalus_merged.csv` | **Generated** denormalized join. Never hand-edit; regenerate with `scripts/assemble.py` |
| `scripts/` | The six extraction and build components, the assembler and the doc renderer |
| `qc/validate.py` | Quality-control suite; exits non-zero on failure and writes `qc/stats.json` |
| `sources/raw/` | Every retrieved payload, committed, so any value can be re-derived offline |
| `notes/` | Per-component audit trails |
| `OligoTox-Hydrocephalus_Dataset.xlsx` | The dataset as a single workbook — README, Summary, data_dictionary, oligos, measurements, modifications, sources — in the same sheet layout as the sibling CNS release |
| [`scripts/data_dictionary.py`](scripts/data_dictionary.py) | The authoritative column definitions, enforced by QC in both directions |

## Reproducing the dataset

From a clean checkout, in order:

```bash
python3 scripts/discover_ctgov_trials.py  # enumerate EVERY oligo trial with posted results
python3 scripts/extract_ctgov.py          # ClinicalTrials.gov posted adverse-event tables
python3 scripts/extract_ctgov_outcomes.py # pre-specified ventricular MRI outcome measures
python3 scripts/extract_faers.py          # openFDA FAERS  (cached; re-runs cost no quota)
python3 scripts/extract_labels.py         # DailyMed Structured Product Labels
python3 scripts/build_literature.py       # curated full-text and EMA SmPC rows
python3 scripts/build_nonclinical.py      # curated rodent rows (both effect directions)
python3 scripts/parse_inn_sequences.py    # sequences + per-position chemistry from WHO INN lists
python3 scripts/build_oligos.py           # design predictors from labels and INN
python3 scripts/assemble.py               # canonical tables + provenance registry + merged view
python3 scripts/build_modifications.py    # per-position chemistry (needs the keys assemble assigns)
python3 qc/validate.py                    # 44 checks; writes qc/stats.json
python3 scripts/render_docs.py            # regenerates the counts in this file
python3 scripts/export_xlsx.py            # the .xlsx workbook (needs openpyxl)
```

Every network call is cached under `sources/raw/`, so a re-run is offline and
deterministic. The only dependency outside the standard library is `openpyxl`,
and only for the final workbook export.

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
expert review. Known gaps are stated as numbered open items in
[`METHODOLOGY.md`](METHODOLOGY.md#open-items) rather than left for a reader to
discover — chiefly that no clinical or marketed compound carries a published
sequence (OI-02), that nonclinical coverage is five qualitative rows (OI-03), and
that only one compound in the release is a designed control (OI-08). A further
100 verified sources were retrieved but not extracted; they are listed in
[`notes/source_backlog.md`](notes/source_backlog.md).
