# OligoTox-Kidney — Source Register

**Complete provenance for every value in the dataset**
**NIH/NCATS OligoTox Open Data Challenge, Phase 2 · Endpoint: nephrotoxicity**

*Generated from the dataset itself, not from recollection: every source below is cited by at
least one row of `data/measurements.csv` or `data/oligos.csv`. Row and compound counts are
recomputed from those files.*

---

## 1. How provenance works in this dataset

Every one of the **246 measurements** carries three provenance fields, and no row exists
without all three:

| Field | Meaning |
|---|---|
| `source_id` | Short key into this register (e.g. `N3`, `K1`, `A11`) |
| `source_ref` | The document — DOI, patent number, PMC ID, or DailyMed SPL identifier |
| `source_table` | The **exact locus** inside it: table number, figure panel, or label section |

A fourth field, `redistribution`, governs whether a raw value may be republished:
**`public_domain` 182 rows** (US patent material and US federal labels), **`summary_stat`
64 rows** (derived figures from copyrighted publications).

Sequence provenance is tracked separately in `oligos.csv` via `design_source` and
`identity_confirmation`, because a sequence and a toxicity value often come from different
documents.

**The single most important distinction in this register** is §6: sources we *retrieved and
read* versus sources we *cite but did not retrieve*. 36 rows rest on the latter, and they
are marked in the data as well as here.

---

## 2. Databases and repositories used

| Database | Base URL | Used for | Reachable from our environment |
|---|---|---|---|
| Google Patents | `https://patents.google.com` | Patent full text (N3, N4) | Intermittent (503s); PDFs held locally |
| USPTO Patent Public Search | `https://ppubs.uspto.gov` | Patent verification | Yes |
| PubMed Central (PMC) | `https://pmc.ncbi.nlm.nih.gov/articles/` | Open-access full text | **Yes** |
| PubMed | `https://pubmed.ncbi.nlm.nih.gov/` | Abstracts, PMIDs | Yes |
| DailyMed (NLM) | `https://dailymed.nlm.nih.gov/dailymed/` | US prescribing information (SPL) | **Yes — our route to FDA labels** |
| Drugs@FDA | `https://www.accessdata.fda.gov/scripts/cder/daf/` | FDA review documents | **NO — blocked** |
| WHO INN | `https://cdn.who.int/media/docs/default-source/international-nonproprietary-names-(inn)/` | Chemical nomenclature → sequences | **Yes** |
| NCBI Bookshelf | `https://www.ncbi.nlm.nih.gov/books/` | Monographs (NBK…) | Yes |
| ClinicalTrials.gov | `https://clinicaltrials.gov/study/` | Trial registrations (NCT…) | Yes |
| EMA | `https://www.ema.europa.eu/en/medicines/human/EPAR/` | EPARs and SmPCs | Yes |
| J-STAGE | `https://www.jstage.jst.go.jp/` | J. Toxicol. Sci. | Yes |
| DOI resolver | `https://doi.org/` | Journal articles generally | Publisher-dependent |
| NEJM · Circulation/AHA · ScienceDirect · Oxford Academic | — | Trial publications | **NO — paywalled (403)** |

---

## 3. Primary sources retrieved in full — the backbone (185 rows, 75%)

### N4 — US Patent 11,479,818 B2 · **81 rows · 9 compounds** · public domain
*"In vitro nephrotoxicity screening assay"* (EGFR/KIM-1 readout).
`https://patents.google.com/patent/US11479818B2/en` · local copy:
`sources/US11479818_in_vitro_nephrotox_assay_patent_EGFR.pdf`
**Locus:** Table 5, p.30 — EGFR mRNA, KIM-1 mRNA and KIM-1 protein on **rat primary PTEC**,
9 compounds × 3 concentrations × 3 biomarkers, day 3, gymnotic exposure.
Values normalised to compound 1-1, **not** saline.
Extracted by `scripts/extract_n4_table5.py`, with 4 parsed cells checked against the printed
table before writing.

### N3 — US Patent 11,105,794 B2 · **69 rows · 21 compounds** · public domain
*"In vitro nephrotoxicity screening assay"*.
`https://patents.google.com/patent/US11105794B2/en` · local copy:
`sources/US11105794_in_vitro_nephrotox_assay_patent.pdf`
**Two distinct loci:**
- **Table 1** (21 rows) — in-vivo nephrotoxicity grades. Method section p.25 establishes the
  design: *"Wistar Han Crl : WI (Han) male rats"*, dosed *"at 40 mg/kg on days 1 and 8"*,
  read on a *"Multiplex MAP **Rat** Kidney Toxicity Magnetic Bead Panel 2"*, sacrificed
  *"on day 15"*. This paragraph is why the species/duration/dose correction was made.
- **Table 2** (48 rows) — extracellular EGF on **primary human PTEC and PTEC-TERT1**,
  3 compounds × 4 concentrations × 2 systems × 2 timepoints, % of saline.
- **SEQUENCE LISTING** — the formal listing, source of 21 sequences (validated base-for-base
  against the listing rather than the examples table).

### M1 — Moisan et al. 2017 · **11 rows · 5 compounds** · summary_stat
*EGF uptake / nephrotoxicity of ASOs in vitro.* PMC**5363415**
`https://pmc.ncbi.nlm.nih.gov/articles/PMC5363415/` · local copy in `sources/`
**Locus:** Table 1, Fig 1C–2, Fig 2, Fig 2C, Fig 2D — human PTEC-TERT1 intracellular ATP and
extracellular EGF. **Prints no sequences** (verified) — hence AON-A/C/D/E remain sequence-`TBD`.

### N2 — Janssen et al. 2019 · **10 rows · 3 compounds** · summary_stat
*Therapy with 2′-O-Me phosphorothioate ASOs causes reversible proteinuria by inhibiting renal
protein reabsorption.* PMC**6796739**
`https://pmc.ncbi.nlm.nih.gov/articles/PMC6796739/` · local copy in `sources/`
**Locus:** Fig 1A (study DMD114673), Fig 1D, Fig 1E, Fig 5E–G, results, 39-week necropsy.
Drisapersen in DMD patients + monkey + human ciPTEC — the row set that captures the
functional-not-cytotoxic phenotype.

### K1 — Sandelius et al. 2020 · **9 rows · 2 compounds** · summary_stat
*Urinary kidney biomarker panel for ASO tubular toxicity.* PMID **33084520**
`https://pubmed.ncbi.nlm.nih.gov/33084520/` · local copy in `sources/`
**Locus:** results, results_histopath. cEt ASO in mouse; KIM-1 / clusterin / NGAL / cystatin C.
Tool and control ASO sequences are **proprietary and unpublished**.

### A4 — Arch. Toxicol. 2021 · **5 rows · 1 compound** · summary_stat
*Nephrotoxic ASO SPC5001 induces kidney injury biomarkers in a proximal tubule-on-a-chip.*
DOI `10.1007/s00204-021-03062-8` · `https://doi.org/10.1007/s00204-021-03062-8`
**Locus:** results — quantitative in-vitro fold-changes.

### REV — Wu et al. 2022 · **4 rows · 4 compounds** · summary_stat
*Nephrotoxicity of marketed antisense oligonucleotide drugs.* PMC**10174585**
`https://pmc.ncbi.nlm.nih.gov/articles/PMC10174585/` · local copy in `sources/`
**Locus:** golodirsen / casimersen / viltolarsen / nusinersen sections. Used for
cross-checking clinical grades rather than as sole primary evidence.

---

## 4. Regulatory labels and clinical anchors (A1–A13, 21 rows)

| ID | Source | Locus | Rows | Link |
|---|---|---|---|---|
| A1 | Inotersen — NEJM 2018 NEURO-TTR + FDA label 211172 | label §5.2 | 3 | `https://doi.org/10.1056/NEJMoa1716793` |
| A2 | Inotersen FSGS case report — AJKD 2022 | case_report | 1 | `S0272-6386(22)00929-5` |
| A3 | SPC5001 — van Poelgeest et al. 2013 | results, case_biopsy | 3 | `https://doi.org/10.1111/bcp.12738` |
| A5 | Givosiran — NEJM 2019 ENVISION + Givlaari label | ENVISION; label | 1 | `https://doi.org/10.1056/NEJMoa1913147` |
| A6 | Givosiran — Liver Int. 2022, ENVISION 24-month | ENVISION_24mo | 1 | `https://doi.org/10.1111/liv.15090` |
| A7 | Nusinersen — Spinraza FDA label | label §5.3; Studies 1–2 | 1 | DailyMed |
| A8 | Volanesorsen — EMA SmPC Waylivra + APPROACH | SmPC §4.4/4.8 | 2 | `NCT02658175` |
| A9 | Mipomersen — FDA label 203568 + EMA EPAR Kynamro | label §5; EPAR | 2 | DailyMed / EMA |
| A10 | Inclisiran — Leqvio FDA label + Novartis SmPC | label §6 | 1 | DailyMed |
| A11 | **Golodirsen — Vyondys 53** | §5.2 Kidney Toxicity | 2 | `dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=35c227d1-5b24-44b0-b5d3-f0f6b1c46bd5` |
| A12 | **Casimersen — Amondys 45** | §5.2 Kidney Toxicity | 2 | `…setid=e9e5fd44-eeda-4580-bba1-a734828bbcc3` |
| A13 | **Viltolarsen — Viltepso** | §5.1 Kidney Toxicity | 2 | `…setid=1ffff9a8-6d6a-4dcb-8493-1b6cc3a5d123` |

A11–A13 were read directly on DailyMed in this work. All three carry the same structure —
kidney toxicity observed in animals, **not** observed in the human studies, renal monitoring
nonetheless mandated (serum cystatin C, urine dipstick, UPCR). They are the dataset's
best-supported human negatives.

All three also warn that **"creatinine may not be a reliable measure of kidney function in DMD
patients"** because of reduced skeletal muscle mass — a caveat that applies to every DMD row.

---

## 5. Sequence provenance — WHO INN chemical nomenclature (20 sequences)

WHO publishes complete residue-by-residue nomenclature for INN-named oligonucleotides, from
which sequence is recoverable by deterministic parse. Every list below was fetched as a PDF
and parsed by `scripts/fill_inn_sequences.py`.

**URL pattern:** `https://cdn.who.int/media/docs/default-source/international-nonproprietary-names-(inn)/rl<NN>.pdf`

| Recommended INN List | Compounds recovered |
|---|---|
| 71 | patisiran |
| 73 | mongersen, revusiran |
| 75 | fitusiran |
| 76 | cemdisiran, givosiran, inclisiran |
| 78 | teprasiran |
| 79 | alicaforsen *(correction entry)*, lumasiran |
| 80 | viltolarsen |
| 81 | tofersen |
| 83 | olpasiran, vupanorsen |
| 84 | pelacarsen |
| 85 | bepirovirsen, nedosiran |
| 86 | donidalorsen, zilebesiran |
| 88 | fazirsiran |

**Identity confirmation across all 65 oligos:** patent sequence listing 25 · WHO INN
nomenclature 20 · regulatory label 7 · peer-reviewed publication 3 · not established 10.

Other sequence sources: `WO2016033424A1` (patent), `PMC8673535` (PROMOVI), NCBI Bookshelf
`NBK549761` and `NBK588653`, and the Onpattro/Oxlumo/Amvuttra/Wainua/Qalsody labels.

---

## 6. Cited but **not retrieved** — 36 rows, flagged in the data

These rows were derived from **search-engine summaries** of the named documents during an
earlier session whose network policy blocked full-text fetch. **The document was not opened.**
They carry `source_id = WS` and must be verified against the primary source before release.

This is disclosed rather than buried because it has a measurable consequence: among these
rows, **zero reach nephrotoxicity grade ≥2**, against 11 of 22 anchor-sourced clinical rows
(one-sided Fisher p = 4.5 × 10⁻⁵). Direct retrieval of 7 of them left only **one** standing as
a measured negative. Full analysis in `CLINICAL_VALIDATION.md`.

**Blocked for us — require manual acquisition:**

| Document | Compound | Publisher |
|---|---|---|
| NEJM 2015 `NEJMoa1407250` | mongersen | NEJM |
| NEJM 2023 OCEAN(a)-DOSE `NEJMoa2211023` | olpasiran | NEJM |
| NEJM 2024 `NEJMoa2402478` | donidalorsen | NEJM |
| Circulation 2021 `CIRCULATIONAHA.120.053029` | teprasiran | AHA |
| TRANSLATE-TIMI 70, Circulation 2022 | vupanorsen | AHA |
| Yu et al. 2012, *Toxicology* | ISIS 113715 | Elsevier |
| Alicaforsen review | alicaforsen | ScienceDirect |
| Engelhardt 2016 `nat.2015.0598` / PMID 29846725 | class | Nature |
| **KARDIA trials** | zilebesiran | *citation unresolvable as recorded — needs a real reference* |
| FDA reviews: `211172` PharmR · `211970` NCR · `213026` NCR · `212154` · `217388` · `219019` | various | Drugs@FDA (blocked) |

**Reachable — we can still retrieve these ourselves:**
`PMC6249674` (Janas 2018) · `PMC6468299` (Janas 2019) · `PMC5790433` (Crooke 2018) ·
`PMC6987735` (revusiran nonclinical) · `PMC8673535` (PROMOVI) · `PMC11068990` (PHYOX3) ·
`PMC11944999` (pegaptanib) · `PMC11020434` (CJASN 2024) · `PMC7577764` (Clin Kidney J) ·
`PMC12369710` (SEQUOIA) · `PMC9804925` (bepirovirsen) · J-STAGE `jts51_75` (3D-RPTEC) ·
Onpattro / Oxlumo / Rivfloza / Amvuttra / Qfitlia / Qalsody / Wainua labels via DailyMed.

---

## 7. Reference material — held but producing no rows

These inform interpretation and are **not** cited by any measurement. Held under
`toxicity/_shared/reference/`.

- Frazier 2015, *ASO therapies review*, Toxicol. Pathol. — DOI `10.1177/0192623314551840`
- Frazier 2022, *Kidney effects review*, Toxicol. Pathol. — DOI `10.1177/01926233221100414` *(in kidney sources)*
- Sioud, *Oligonucleotide immunostimulation / cytokines* (book chapter)
- Casarett & Doull, *Toxicology* (textbook)
- OligoTox Challenge brief (scope authority)
- *Methods Mol. Biol.* 2022, renal-tox-in-mice chapter — NCBI `NBK584232`

**Hepatotoxicity source panels** (Dieckmann 2018 `PMC5725219`, Burdick 2014 NAR
`10.1093/nar/gku142`, Hagedorn 2013 NAT `10.1089/nat.2013.0436`) are held under
`toxicity/hepatic/sources/` and contribute **zero rows** to this kidney dataset. Verified on
every run by `scripts/release_check.py`.

---

## 8. How to verify any single value

1. Open `data/measurements.csv` (or the Excel workbook) and find the row.
2. Read `source_id`, `source_ref` and `source_table`.
3. Find `source_id` in §3–§4 above for the document and its link.
4. `source_table` gives the exact table, figure panel or label section.
5. For values from the two patents, the PDFs are in `sources/` — no re-acquisition needed.
6. For sequences, `design_source` and `identity_confirmation` in `oligos.csv` name the
   document and the method by which identity was established.

Every extraction is re-runnable: `scripts/extract_patent_table2.py`,
`scripts/extract_n4_table5.py` and `scripts/fill_inn_sequences.py` re-parse their sources from
scratch and validate against anchor values before writing.

---

## 9. Summary

| | Rows | Share |
|---|---:|---:|
| Primary sources retrieved and read in full | 185 | 75.2% |
| Regulatory labels read directly (incl. DailyMed) | 21 | 8.5% |
| **Cited but not retrieved (`WS`) — verify before release** | **36** | **14.6%** |
| Review cross-checks | 4 | 1.6% |
| **Total** | **246** | **100%** |

Redistribution: `public_domain` 182 rows · `summary_stat` 64 rows.
Dataset licence: **CC BY 4.0** (repository-root `LICENSE`). Third-party source PDFs retain
their publishers' terms and are included for verification only.
