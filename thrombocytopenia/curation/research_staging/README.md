# Research staging

**Nothing in this folder is part of the validated dataset.** It is not in `data/`, it
carries no scientific adjudication, it sets no label, and no model may be trained on it.
Beebop's 2026-10-02 research round authorises acquisition into clearly separate staging and
explicitly does not authorise validated-data changes. Promotion out of staging requires
Oscar's implementation approval and German's scientific adjudication.

## Contents

| File | What it is |
|---|---|
| `sewing2017_pone.0187574_S1.xlsx` | The unchanged source workbook, byte-for-byte as retrieved |
| `sewing2017_condition_level.csv` | Every numeric cell, with its endpoint block, row label, column header, exact cell locus, control class and resolved construct |
| `sewing2017_manifest.json` | Provenance, checksum, sheet inventory, and an honest accounting of what the numbers are and are not |
| `sweep_*.json` | 20-resource search-coverage logs (see the research report) |

## The one claim worth repeating

A numeric cell is **not** an independent observation, and recovering these values
**reconstructs the source publication's own measurements at finer grain**. It is not
independent biological replication and it does not externally validate any grade in the
dataset. That distinction was wrong in an earlier report of mine and is corrected here.

## Why this file was prioritised

Phase 2 singles out "datasets based on in vitro human systems". The scientist package's
matched mechanistic contrasts — the AC-series PS versus LNA-PS pairs and the ODN 2395
PS versus PO pair — currently rest on one adjudicated 0–3 ordinal score per construct.
This workbook holds the per-replicate measurements beneath those scores, with matched
negative and positive activation controls measured in the same runs. That is the input the
conditionally-approved human mechanistic lane needs.

## What could not be obtained

**Slingsby 2022** (`10.3324/haematol.2020.260059`, PMC8804562) — the largest human
in-vitro source in the dataset at 157 rows — publishes **no raw data**. Its supplementary
archive was retrieved in full (1,848,710 bytes, `sha256 b43b75e4…4406`) and contains only
figure/table images and a methods appendix; the article carries no data-availability
statement and no deposit, and its Table 1 sequences are published as an image. Per-donor
Slingsby values are therefore not publicly available by any route short of author contact,
which this round does not authorise.
