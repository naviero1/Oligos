# Curation record — OligoTox-Thrombocytopenia

The **raw provenance chain** behind `../data/oligos.csv` and
`../data/measurements.csv`: what each curation agent actually returned, what the
adversarial verifiers ruled on it, and which sources were discovered and
triaged.

## Why this is committed

The published CSVs are a *derived artefact*. Without these inputs the assembly
is not reproducible — you could re-read the cited sources, but you could not
re-run the pipeline, diff a re-extraction against the original, or audit how a
particular value entered the dataset.

They were also, until now, held only in an **ephemeral scratchpad**. This
repository has already lost an entire session's uncurated work to a reclaimed
container once (see the reconstruction note in the root `README.md`), and the
same failure would have taken this record with it.

Files are pretty-printed with sorted keys so they diff cleanly in review rather
than appearing as one-line blobs.

## Layout

```
lanes/       one file per extraction producer — the rows as the agent returned them
verdicts/    adversarial-verification rulings, keyed for re-application
discovery/   the source sweep and triage that decided what to extract
```

### `lanes/` — extraction output

| File | Producer | Content |
|---|---|---|
| `labels_lane.json` | curator, direct | FDA/EMA label rows for inotersen, olezarsen, nusinersen, imetelstat, volanesorsen — all `public_domain` |
| `lane_preclinical_negatives.json` | lane agent | animal in-vivo + the negative-control set, sourced from FDA reviews and EMA EPARs |
| `lane_patents_panels.json` | lane agent | Ionis patent panels — the largest `public_domain` block |
| `lane_crooke2017.json` | dedicated agent | the pooled Ionis safety database (59 trials, 16 ASOs, 3,476 subjects) |
| `lane_patents2_reviews.json` | lane agent | follow-up patents, the AE meta-analysis, and the aptamer rows |
| `workflow_harvest.json` | `harvest_workflow.py` | everything extracted by the multi-source workflow |

`workflow_harvest.json` deserves particular note: it is harvested from a
workflow journal that lives outside the repository and is itself ephemeral, so
this is the **only durable copy** of those extractions.

### `verdicts/` — adversarial verification

Each verdict carries a `natural_key` — `(oligo_name, source_ref, source_table,
readout_name, dose)` — drawn from the row's own content, so it survives the
`measurement_id` renumbering that any re-assembly causes. `freeze_verdicts.py`
stamps that key on; `apply_verdicts.py` prefers it over the volatile id.

| File | Block | Result |
|---|---|---|
| `verdicts_crooke.json` | Crooke 2017, 387 rows | 382 confirmed · 5 corrected · 0 rejected |
| `verdicts_invitro.json` | in-vitro human platelet, 272 rows | 246 confirmed · 26 corrected · 0 rejected |

### `discovery/` — what was found and why it was chosen

| File | Content |
|---|---|
| `sources_dedup.json` | the 33 unique sources from the ten-lane sweep, deduplicated from 47 hits, each with its verified access route and the extraction roadmap the discovery agent wrote |
| `extract_targets.json` | the 14 highest-yield sources selected for extraction, and the reasoning |
| `label_scan.json` | the systematic FDA-label platelet sweep across every approved oligonucleotide, including the **negative** results that establish which modalities have no label platelet content |

`label_scan.json` records absences deliberately. A drug whose label never
mentions platelets is evidence of a kind, but it is **not** a measured zero, and
no grade-0 row was ever created from it — see `../METHODOLOGY.md`.

## Re-running from this record

```
# run from the thrombocytopenia/ endpoint folder
scripts/merge_lane_files.py   out.json  curation/lanes/*.json
scripts/assemble_thrombo.py   out.json            # verdicts, dedupe, stable keys
scripts/apply_verdicts.py     curation/verdicts/*.json
scripts/qc_thrombo.py                             # gates the round
scripts/build_merged_thrombo.py                   # derived analysis view
scripts/refresh_docs.py                           # regenerate the generated docs
```

`scripts/ingest_thrombo.sh` runs the whole sequence, and can be invoked from anywhere — it anchors every path to this endpoint folder.

## What is *not* here

Third-party full texts are **referenced, never redistributed** — every row
carries a `source_ref` and an exact `source_table` locus instead. Downloaded
PDFs used during extraction were working files and are deliberately not
committed.
