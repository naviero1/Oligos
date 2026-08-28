# Sources — OligoTox-Thrombocytopenia

Source registry for the thrombocytopenia dataset. Every `source_id` used in
`data/measurements.csv` must appear here with its identifier, retrieval route,
and **redistribution status**.

**Network status (this session): OPEN.** Unlike the earlier kidney-dataset
sessions — whose egress policy blocked all outbound fetch and forced reliance on
user-supplied PDFs — this session reached PMC, NCBI E-utilities, Europe PMC,
DailyMed, and USPTO directly. Sources below were retrieved live and their
identifiers verified, not recalled.

## Redistribution classes

| Class | Meaning | Typical source |
|---|---|---|
| `public_domain` | reproduce freely, no restriction | USPTO patents, FDA/EMA documents |
| `cc_by` | reproduce **raw values** with attribution | PLOS and other CC-BY open-access articles |
| `derived_features_only` | derived features only | copyrighted journal content |
| `summary_stat` | summary statistics under fair use | copyrighted journal content |
| `verify` | rights unresolved — settle before release | — |

A `cc_by` classification must come from the article's **own licence field**
(Europe PMC `license`, or the article's rights statement), never from the fact
that it happens to be free to read.

---

## Independently verified anchors (retrieved and parsed in-session)

### `T-FDA-INO` — Inotersen (TEGSEDI) FDA prescribing information ✅ retrieved
- **Route:** DailyMed SPL REST API, setid `8513207e-b55f-417b-9473-af785146a543`,
  SPL version 10, published 2024-01-26. Parsed from structured XML.
- **Why it is the canonical anchor:** carries an FDA **Boxed Warning** —
  "WARNING: THROMBOCYTOPENIA AND GLOMERULONEPHRITIS" — and section 5.1 reports
  the full severity range for a single compound, which is exactly what the 0–3
  rubric needs to be calibrated against:
  platelet count < 100 × 10⁹/L in **25 %** of treated patients vs **2 %** placebo;
  < 75 × 10⁹/L in **14 %** vs **0 %**; nadir < 75 × 10⁹/L in **39 %** of patients
  whose baseline platelets were < 200 × 10⁹/L vs **6 %** at baseline ≥ 200;
  **3 %** with sudden severe thrombocytopenia < 25 × 10⁹/L; **one fatal
  intracranial haemorrhage**; and **all 3** severe cases had treatment-emergent
  **antiplatelet IgG antibodies**.
- **Why it matters mechanistically:** this single label documents *both* modes of
  the endpoint — the common dose-dependent decline and the rare
  antibody-mediated severe form — and is the evidence base for the bimodal
  rubric in `schema.md`.
- **Assay caveat worth recording:** antiplatelet antibody/EDTA interaction caused
  **platelet clumping** that made 2 measurements uninterpretable and delayed
  diagnosis. Platelet counts from EDTA tubes in antibody-positive patients are
  not always trustworthy.
- **Redistribution:** `public_domain`.

### `T-SEWING` — Sewing et al. 2017, *PLoS One* ✅ verified retrievable
- **Title:** *Assessing single-stranded oligonucleotide drug-induced effects in
  vitro reveals key risk factors for thrombocytopenia.*
- **IDs:** PMID **29107969** · PMCID **PMC5673186** · DOI **10.1371/journal.pone.0187574**
- **Why:** the highest-value **in-vitro human platelet** source — which is
  NCATS's explicitly stated priority for this challenge (in-vitro human systems).
  Panel of single-stranded oligonucleotides assessed for platelet effects with
  per-compound readouts.
- **Redistribution:** **`cc_by`** — licence confirmed as `cc by` via the Europe
  PMC record. Raw per-compound values may be reproduced with attribution.

---

## Lane-discovered sources

*Populated from the ten-lane discovery sweep described in `METHODOLOGY.md` §3.
Each entry carries the identifier, verified access route, what per-measurement
data it contains, and its redistribution class.*

<!-- BEGIN LANE SOURCES -->
<!-- END LANE SOURCES -->

---

## Provenance discipline

- Each extracted row → `source_id` (registered here), `source_ref` (DOI / PMID /
  PMCID / patent number / label ID), `source_table` (exact table, figure, claim,
  or label section), and `redistribution`.
- A row whose exact locus cannot be named is **dropped**, not kept with a vague
  citation.
- Patents and regulatory documents: reproduce freely. CC-BY articles: reproduce
  with attribution. Other journal content: prefer derived features or summary
  statistics.
