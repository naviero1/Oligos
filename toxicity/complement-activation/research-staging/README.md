# Research staging — complement activation

Created 2026-10-02 under the research authorization in `../BEEBOP_RESEARCH_REQUEST_2026-10-02.md`.

This folder holds **third-party source material only**. It is not a dataset, it is not validated evidence, and nothing here has been extracted into a measurement table. No scientific label, adjudication or model is established by any file in it.

## Licensing policy for this folder

The Phase 2 description requires that the submitted dataset's access and use terms "allow for open and public access, such as through a creative commons license." A source file whose own licence forbids redistribution or derivatives therefore **cannot be committed here**, even where it is free to read.

Oscar's decision of 2026-10-02: **commit the CC-BY file only; hold everything else as a provenance record plus checksum and re-fetch on demand.**

| Source | Licence | Redistributable here | Action taken |
|---|---|---|---|
| Sewing 2017 `S1 File. Raw data figures` | **CC-BY 4.0** | **yes** | **committed** — `sources/Sewing2017_PLoSONE_S1_raw_data_figures.xlsx` |
| Crooke 2016 supplementary bundle | CC BY-NC-SA 4.0 | no — ShareAlike and NonCommercial | record only |
| Demirjian et al. (QPI-1002 / NCT00554359) | CC BY-NC-**ND** | no — NoDerivatives | record only |
| Mangsbo 2009 | AAI copyright, **no CC licence** | no | record only |
| EMA assessment reports | public documents, no CC grant | not committed (bulk; freely re-fetchable) | record only |
| FDA review documents | US Government work | not committed (bulk; freely re-fetchable) | record only |

Extracted **numerical values** are facts rather than copyrightable expression, so derived observations may enter a dataset from a record-only source with correct attribution. The *file* stays out. Where a licence is ND or SA, the derived-value route is the only one available and must be noted on every row that uses it.

## Committed file

**`sources/Sewing2017_PLoSONE_S1_raw_data_figures.xlsx`**

| | |
|---|---|
| Original filename | `pone.0187574.s001.xlsx` |
| Retrieved from | Europe PMC supplementary-files endpoint for `PMC5673186` (HTTP 200, 580,042-byte bundle) |
| Retrieved on | 2026-10-02 |
| Size | 54,955 bytes |
| `sha256` | `cd4d4b092e112982cb3ab56e6de88101d523933dcf147185c20a829a71f6a3fc` |
| `md5` | `3a87124ce195ca83e915266c1e0d654a` |
| Sheets | 6 — `Figure 1` … `Figure 6` |
| Complement content | sheet **`Figure 6`**, headed "Individual data Whole Blood Assays [Stimulation Index]"; C3a block and C5a block |
| Parent article | Sewing S, Roth AB, Winter M, Dieckmann A, Bertinetti-Lapatki C, Tessier Y, McGinnis C, Huber S, Koller E, Ploix C, Reed JC, Singer T, Rothfuss A (2017) "Assessing single-stranded oligonucleotide drug-induced effects in vitro reveals key risk factors for thrombocytopenia", *PLoS One* 12(11):e0187574 |
| Identifiers | PMID 29107969 · PMC5673186 · doi 10.1371/journal.pone.0187574 |
| Licence | CC-BY 4.0 (Europe PMC `license: cc by`) |

### Shared-source ownership

This same file is the source behind the thrombocytopenia dataset's `EXV-TMB-051` / `EXV-TMB-052` records on `claude/oligo-challenge-data-4um5mi`, where it is cited for platelet activation rather than complement. **It is one acquisition shared between two endpoints, not two.** Any complement rows derived here must be keyed so they cannot be double-counted against the thrombocytopenia records, and the checksum above should be reconciled against whatever that branch holds before either is treated as independent.

## Non-committed sources — provenance records

Held in session scratch during the 2026-10-02 round; re-fetchable at the URLs given. Checksums are recorded so a later session can confirm it has the same bytes.

| File | Bytes | `sha256` (first 16) | Re-fetch route |
|---|---|---|---|
| `mt2016136x1.pdf` (Crooke 2016 Suppl. Tables S1–S10) | 1,934,231 | `449fcc4e86b3e32c` | Europe PMC `supplementaryFiles` for `PMC5112040` |
| `kyndrisa.pdf` (EMA Kyndrisa withdrawal assessment report, 105 pp) | 2,804,042 | `143a347965151cc7` | `ema.europa.eu/en/documents/withdrawal-report/withdrawal-assessment-report-kyndrisa_en.pdf` |
| `tegsedi.pdf` (EMA Tegsedi EPAR, 142 pp) | 2,313,092 | `6ef75b0eda44a7f8` | `ema.europa.eu/en/documents/assessment-report/tegsedi-epar-public-assessment-report_en.pdf` |
| `kynamro.pdf` (EMA Kynamro EPAR, 114 pp) | 3,397,457 | `f56c9137d2376c35` | `ema.europa.eu/en/documents/assessment-report/kynamro-epar-public-assessment-report_en.pdf` |
| `kynamro_refusal.pdf` (EMA grounds for refusal) | 80,931 | `488178ab884d4a21` | `ema.europa.eu/en/documents/other/kynamro-epar-scientific-conclusions-and-grounds-refusal-marketing-authorisation-kynamro_en.pdf` |

Retrieval note worth carrying to the shared access register: the EMA document host rate-limits (HTTP 429) and needs a retry; **FDA `accessdata.fda.gov` returns 404 to a default user agent and 200 to a browser user agent**. Neither is a paywall, and a session that does not know this will wrongly record FDA documents as unavailable.
