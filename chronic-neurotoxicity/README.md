# Chronic neurotoxicity

Per-measurement CNS-toxicity data for therapeutic oligonucleotides, for the
NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge. **Chronic
neurotoxicity** is one of the eight toxicities the brief names and one of only
two CNS endpoints on it; the other is [hydrocephalus](../hydrocephalus/), curated
in the same pass, in its own folder. The dataset is **chronic-first**: the brief
deprioritises acute neurotoxicity focused on alterations of neuronal electrical
activity, so every row declares its bucket through `endpoint_domain` and
`challenge_priority` — see [*Why acute rows are here*](#why-acute-rows-are-here).

## Status

| | |
|---|---:|
| Measurement rows (`data/measurements.csv`) | **2,393** × 26 columns |
| Unique oligonucleotides (`data/oligos.csv`) | **573** × 17 columns |
| Analysis view (`data/oligotox_cns_merged.csv`, generated) | 2,393 × 42 columns |
| Oligos with a published sequence | 458 / 573 |
| Distinct `source_ref` (canonical identifiers) | 89 |
| Distinct `target_gene` values (raw, case unnormalised) | 43 |
| Rows flagged `is_cns_specific=TRUE` | 2,289 |
| Rows carrying a verifier verdict in `notes` | 228 |
| Orphan measurements / unreferenced oligos | 0 / 0 |
| Grades | provisional on all 2,393 rows |

## What this folder holds, and what it does not

The CNS curation was carried out as **one corpus of 2,540 measurements serving
two named endpoints**, partitioned by its own `challenge_priority` column —
`high_hydrocephalus` (147 rows) to [`../hydrocephalus/`](../hydrocephalus/),
everything else (2,393 rows) here. The partition is disjoint and exhaustive
(147 + 2,393 = 2,540) and is reproduced by
[`../_shared/scripts/split_cns_by_endpoint.py`](../_shared/scripts/split_cns_by_endpoint.py),
which reads the rule off the data rather than inferring it. Each side's
`oligos.csv` is filtered to the oligos its own measurements reference, so both
folders are self-contained two-table datasets; a molecule may appear in both
oligo tables, an oligo being a compound identity, not an observation.
[`README-CNS.md`](README-CNS.md) stays the **corpus-level** document, so its
counts are corpus counts, not the folder counts below.

## Distributions

| `endpoint_domain` | Rows | | `challenge_priority` | Rows |
|---|---:|---|---|---:|
| `acute_neurotoxicity` | 931 | | `medium` | 1,165 |
| `neuroinflammation` | 733 | | `high_chronic_neurotox` | 1,047 |
| `chronic_neurotoxicity` | 290 | | `low_acute_electrophysiology` | 181 |
| `clinical_neuro_ae` | 232 | | **`neurotox_grade`** | **Rows** |
| `csf_biomarker` | 76 | | 0 / 1 | 1,183 / 577 |
| `neurobehavioral` | 55 | | 2 / 3 | 513 / 120 |
| `cytotoxicity` | 46 | | | |
| `neurodegeneration` | 30 | | | |

All counts are computed from this folder's tables; the rubric and controlled
vocabularies are in [`schema-cns.md`](schema-cns.md). The two flags are separate
partitions: `high_chronic_neurotox` is dominated by `neuroinflammation` (665) and
`chronic_neurotoxicity` (268), while of the 931 `acute_neurotoxicity` rows 749
sit at `medium` and 181 at `low_acute_electrophysiology`. **The 1,183 grade-0
rows are deliberate** — a dataset of positives only teaches a model that every
oligonucleotide is neurotoxic, and this endpoint has no shortage of compounds
that were tested and were not.

- `study_type` — `animal_invivo` 1,684, `clinical` 414, `in_vitro` 295; `species`
  — mouse 1,011, rat 612, human 530, monkey 238, sheep 2.
- `delivery_method` — `intrathecal` 1,019, `intracerebroventricular` 1,008,
  `gymnotic_free_uptake` 238, `systemic_dose` 66, `lipofection` 52, and 10 rows
  across `intraparenchymal`, `TBD`, `intracisternal` and `transfection`.
- `oligo_class`, skewed as CNS-delivered chemistry is — `ASO_gapmer` 528, `other`
  24, `splice_switching_ASO` 10, `PMO` 4, `GalNAc_siRNA` 4, `siRNA` 3; 508 of the
  573 oligos are `max_phase = research_panel` compounds and 10 are approved drugs.

**Direction is modelled, not flattened**: 53 rows read neurofilament light, both
an efficacy and a toxicity biomarker here, and none carries `effect_direction =
TBD`, as the schema requires. **`reversibility` is `not_assessed` on 1,972 rows**
(`reversible` 202, `irreversible` 114, `TBD` 58, `partially_reversible` 47) —
largely a correction, since rows had claimed `reversible` from another cohort's
prose. Those with a real assessment come mostly from nonclinical reviews with
designated recovery groups.

## Why acute rows are here

The brief's qualification is narrow: it deprioritises submissions *focused on
alterations of neuronal electrical activity*. Acute neurotoxicity is nonetheless
the most strongly sequence-dependent CNS signal in the literature, and the large
scored panels pairing *published sequences* with *graded outcomes* are all acute
— discarding them would have discarded the only training-shaped data in the
endpoint. So they are included, flagged and separable. Only **181 rows (7.6%)**
are electrophysiology readouts proper, all `in_vitro`, and present only as the
matched in-vitro arm of an in-vivo panel on the same molecules:
`doi:10.1089/nat.2021.0071` contributes 357 rows — 181 mouse
intracerebroventricular acute-tolerability scores and 176 calcium-oscillation
scores in primary cortical neurons, one panel, published sequences, both arms.
Matched pairs are the form the challenge's bridging request takes.

## Verification, provenance and rights

Verification ran over the **whole corpus**, not per folder: 614 verdicts across
11 batches, sampled in strata weighted to risk, verifiers instructed to refute
rather than confirm. Method, batch table and every refuted row are in
[`VERIFICATION-CNS.md`](VERIFICATION-CNS.md); raw verdicts under
[`notes/verify/`](notes/verify/). Of this folder's rows, **228 carry a verdict in
`notes`** — 253 markers (`REFUTED` 132, `CONFIRMED_MINOR` 111, `UNVERIFIABLE` 8,
`CONFIRMED` 2) — and **203 were corrected**. The dominant refutation was grade
inflation: anchoring a grade-3 cutoff to a fraction of a scale's numeric range
rather than to what the scale says the value means.

Every row carries a canonical `source_ref` — patent number, DOI, NCT number or
FDA/EMA document id — plus the exact locus in `source_table`. `redistribution` is
read from the licence statement inside the archived source, not assumed:
`public_domain` 1,526, `cc_by` 533, `summary_stat` 271, `verify` 63; those 63
must be settled before public release. Six documents supply 1,620 of the 2,393
rows and were prioritised for verification — `US9605263B2` 602,
`doi:10.1089/nat.2021.0071` 357, `US10968453B2` 327, `US11851654B2` 133,
`FDA_NDA209531` (nusinersen) 122, `FDA_NDA215887` (tofersen) 79. The registry
[`SOURCES-CNS.md`](SOURCES-CNS.md) is generated from the data and is
corpus-scoped, listing 108 documents across both CNS folders.

## Sources, scripts and notes

**Source documents live in [`../_shared/sources/cns/`](../_shared/sources/cns/)**,
not here: 45 files plus an `fpo/` subdirectory of 16 patent full-text HTML
mirrors served both CNS endpoints in one curation — FDA and EMA reviews, patent
PDFs, PMC JATS XML, WHO INN recommended lists, and the archived spreadsheet the
calcium panel came from. `SOURCES-CNS.md` still cites the old path `sources/cns/`.

[`notes/`](notes/) holds the curation trail:
[`EXTRACTION_CONTRACT.md`](notes/EXTRACTION_CONTRACT.md), which every extraction
agent worked to and whose first rule is that a value may only be written if it
was read out of a document fetched in that session;
[`extractions/`](notes/extractions/), the 12 per-lane JSON outputs;
[`verify/`](notes/verify/), the verifier brief with 11 batch and 11 verdict
files; and [`work/`](notes/work/), the parsing scratch. [`scripts/`](scripts/)
regenerates the folder from those inputs — assembly, corrections, verdicts, QC,
merged view, statistics. The normalised tables are the source of truth; the
merged view is never hand-edited.

## Open work

From [`NEXT-STEPS-CNS.md`](NEXT-STEPS-CNS.md), a gap analysis rather than a
to-do list — every gap confirmed by searching for it and finding nothing:

- **The literature is richest where the challenge assigns lowest priority and
  close to empty where it assigns highest** — the most useful single thing this
  curation reports, and what a Data Generation phase should act on.
- **Human in vitro neural systems barely exist.** Only 295 rows are `in_vitro`,
  and searching found almost no study whose *purpose* is oligonucleotide toxicity
  in human iPSC-derived neural cells. The named priority is a gymnotically dosed
  iPSC neuron / astrocyte / microglia panel read out for NfL release, on compounds
  with published sequences.
- **Recovery arms and chronic designs.** `reversibility` is unassessed on 1,972
  rows because the studies never looked, which limits what this dataset can say
  about its own priority endpoint; one extra timepoint on animals already dosed
  classifies an otherwise ambiguous finding. Most published scoring is 1–24 h
  acute, and one series showed allele selectivity degrading between one and four
  weeks.
- **Sequences and outcomes live in different documents.** 115 of the 573 oligos
  have no published sequence, a substantial share proprietary rather than merely
  unretrieved. **Grades stay provisional** on all 2,393 rows, and `target_gene`
  needs case normalisation.

## Related

[`METHODOLOGY-CNS.md`](METHODOLOGY-CNS.md) (hazards, grading, QC) ·
[`schema-cns.md`](schema-cns.md) (dictionary, rubric) ·
[`README-CNS.md`](README-CNS.md) (corpus level) ·
[`../hydrocephalus/`](../hydrocephalus/) (other half of the partition) ·
[`../kidney-toxicity/`](../kidney-toxicity/) · [`../README.md`](../README.md).
