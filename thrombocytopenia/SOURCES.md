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

The ten-lane sweep verified **33 unique sources** (47 hits deduplicated by identifier).
Each was fetched before being listed, so none of these citations is unverified.

| Expected rows | Priority | Access | Identifier | Source |
|---:|---|---|---|---|
| 130 | high | open_access | `PMC5467133 / PMID 28145801 / DOI 10.1089/nat.2016.0650` | The Effects of 2'-O-Methoxyethyl Containing Antisense Oligonucleotides on Plat |
| 60 | high | public_domain | `EMA/180717/2019 (EMEA/H/C/004538)` | Waylivra (volanesorsen) EPAR Public Assessment Report |
| 60 | high | open_access | `PMC5673186 / PMID 29107969 / DOI 10.1371/journal.pone.0187` | Assessing single-stranded oligonucleotide drug-induced effects in vitro reveal |
| 45 | high | public_domain | `FDA NDA 211172 - 211172Orig1s000MedR.pdf (and 211172Orig1s` | FDA Clinical Safety Review, Tegsedi (inotersen) NDA 211172 (Medical Review; co |
| 40 | high | open_access | `PMC8804562 / PMID 33567808 / DOI 10.3324/haematol.2020.260` | Sequence-specific 2'-O-methoxyethyl antisense oligonucleotides activate human  |
| 35 | high | public_domain | `NDA 217779 Orig1s000 MultidisciplineR` | FDA Multi-Discipline Review and Evaluation, NDA 217779 Rytelo (imetelstat) |
| 30 | high | public_domain | `EMA/411876/2018 (EMEA/H/C/004782)` | Tegsedi (inotersen) EPAR Public Assessment Report |
| 30 | high | open_access | `PMC4322051 / PMID 25646267 / DOI 10.1084/jem.20140391` | Phosphorothioate backbone modifications of nucleotide-based drugs are potent p |
| 28 | high | open_access | `PMC10143489 / PMID 37111598 / doi:10.3390/pharmaceutics150` | Platelet Activation by Antisense Oligonucleotides (ASOs) in the Gottingen Mini |
| 25 | high | open_access | `PMC3709655 / PMID 23673861 / DOI 10.1182/blood-2013-01-478` | Complex formation with nucleic acids and aptamers alters the antigenic propert |
| 24 | high | open_access | `EMEA/H/C/004538 product information` | EMA Waylivra (volanesorsen) SmPC / Annex I Product Information |
| 22 | high | open_access | `PMC8264460 / PMID 33540294 / DOI 10.1016/j.thromres.2021.0` | Antisense oligonucleotides and nucleic acids generate hypersensitive platelets |
| 20 | high | open_access | `PMC6386089 / PMID 30570431 / DOI 10.1089/nat.2018.0753` | Integrated Assessment of the Clinical Performance of GalNAc3-Conjugated 2'-O-M |
| 18 | high | public_domain | `NDA 203568 Orig1s000 PharmR` | FDA Pharmacology/Toxicology Review, NDA 203568 Kynamro (mipomersen), R. Wange  |
| 18 | high | open_access | `PMC5112040 / PMID 27357629 / DOI 10.1038/mt.2016.136` | Integrated Safety Assessment of 2'-O-Methoxyethyl Chimeric Antisense Oligonucl |
| 16 | medium | open_access | `PMC6391317 / PMID 30842734 / DOI 10.3389/fphar.2019.00068` | Comparison of Effects of Anti-thrombin Aptamers HD1 and HD22 on Aggregation of |
| 14 | high | open_access | `PMC11447117 / PMID 39138650 / DOI 10.1007/s00415-024-12616` | Switching from inotersen to eplontersen in patients with hereditary transthyre |
| 14 | medium | open_access | `PMC6982813 / PMID 31881749 / DOI 10.3390/s20010152` | Application of Piezo-Based Measuring System for Evaluation of Nucleic Acid-Bas |
| 12 | medium | public_domain | `NDA 209531; DailyMed SPL setid dd70cd5f-b0fc-4ba4-a5ea-89a` | FDA Prescribing Information + Clinical Safety Review, NDA 209531 SPINRAZA (nus |
| 12 | high | open_access | `PMC12611561 / PMID 29972757 / DOI 10.1056/NEJMoa1716793` | Inotersen Treatment for Patients with Hereditary Transthyretin Amyloidosis (NE |
| 12 | high | abstract_only | `PMID 32043907 / doi:10.1089/nat.2019.0829` | Underlying Immune Disorder May Predispose Some Transthyretin Amyloidosis Subje |
| 10 | medium | public_domain | `NDA 218614 label; DailyMed SPL setid 0f51aa8e-8475-8cf9-e0` | FDA Prescribing Information — TRYNGOLZA (olezarsen) injection |
| 10 | medium | open_access | `PMC9618524 / PMID 35908242 / DOI 10.1007/s00415-022-11276-` | Long-term efficacy and safety of inotersen for hereditary transthyretin amyloi |
| 10 | medium | public_domain | `DailyMed SPL setid 0f51aa8e-8475-8cf9-e063-6394a90a6848 (I` | TRYNGOLZA (olezarsen sodium) US Prescribing Information - FDA label |
| 10 | high | abstract_only | `PMID 37093125 / doi:10.1089/nat.2022.0042` | Complement C3d/C4d Deposition on Platelets Correlates with 2'-O-Methoxyethyl A |
| 10 | medium | abstract_only | `PMID 28541820 / doi:10.1089/nat.2017.0666` | Assessment of the Effects of 2'-Methoxyethyl Antisense Oligonucleotides on Pla |
| 9 | high | abstract_only | `PMID 29846725 / doi:10.1093/toxsci/kfy119` | Investigation into the Mechanism(s) That Leads to Platelet Decreases in Cynomo |
| 9 | medium | open_access | `PMC12043408 / PMID 40101742 / doi:10.1093/jimmun/vkae055` | Cellular Immune Changes during Severe Antisense Oligonucleotide-Associated Thr |
| 7 | medium | public_domain | `DailyMed SPL setid 3ff501e0-f75f-07da-e063-6294a90a0cb7 (I` | DAWNZERA (donidalorsen) US Prescribing Information - FDA label |
| 6 | low | abstract_only | `PMID 39155024 / doi:10.1016/j.jtha.2024.08.003` | CpG oligonucleotides induce acute murine thrombocytopenia dependent on toll-li |
| 3 | low | public_domain | `NDA/BLA Qfitlia label; DailyMed SPL setid 6dd2f8ac-6f90-4c` | FDA Prescribing Information — QFITLIA (fitusiran) injection |
| 3 | low | open_access | `PMC9873445 / PMID 36703865 / DOI 10.1155/2023/1884439` | Activation of Most Toll-Like Receptors in Whole Human Blood Attenuates Platele |
| 2 | medium | open_access | `EMEA/H/C/006126 product information` | EMA Wainzua (eplontersen) SmPC / Annex I Product Information |

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
