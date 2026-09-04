# Original papers — OligoTox-CNS

The article of record for every source the CNS module reads, downloaded from Europe PMC and
DailyMed and verified page-by-page against the expected title. `deliverables/OligoTox-CNS_
SourceRegister.pdf` says what was read out of each one and where inside it.

Every file here is open access or public domain. Each carries its own terms, listed below;
attribution is required for all of the CC-licensed ones.

| ID | Paper | File | Pages | Licence | DOI / identifier | What it gave the dataset |
|---|---|---|---|---|---|---|
| **H1** | Hagedorn 2022, Nucleic Acid Ther 32(3):151-162 | `H1_Hagedorn2022_NucleicAcidTher_PMC9221153.pdf` | 12 | CC BY 4.0 | 10.1089/nat.2021.0071 · PMC9221153 | 1,825 oligos / 2,006 measurements - the module's core. Suppl. Table S1. |
| **K1** | Miller 2024, Mol Ther Nucleic Acids 35(4):102359 (journal version) | `K1_Miller2024_MTNA_journal_PMC11567125.pdf` | 21 | CC BY-NC-ND 4.0 | 10.1016/j.omtn.2024.102359 · PMC11567125 | 7 / 41. The version of record. |
| **K1** | Miller 2024, bioRxiv preprint (the record the supplement was read from) | `K1_Miller2024_bioRxiv_preprint_PMC11185713.pdf` | 50 | CC BY-NC-ND 4.0 | 10.1101/2024.06.06.597639 · PMC11185713 | Same title, authors and Table S2. media-1.pdf came from here. |
| **L1** | Kuroda 2025, Mol Ther Nucleic Acids 36:102692 | `L1_Kuroda2025_MTNA_PMC12744863.pdf` | 17 | CC BY 4.0 | 10.1016/j.omtn.2025.102692 · PMC12744863 | 5 / 6. Suppl. Table S1 encodes chemistry in typeface. |
| **C1** | QALSODY (tofersen) FDA prescribing information | `C1_QALSODY_tofersen_FDA_PI_81356b45.pdf` | 16 | US Government work - public domain | - · DailyMed setid 81356b45-1cb7-4eef-88ea-e44cc18b47c5 | Sections 5.1-5.3, 6.1, 6.2. |
| **C1** | SPINRAZA (nusinersen) FDA prescribing information | `C1_SPINRAZA_nusinersen_FDA_PI_dd70cd5f.pdf` | 30 | US Government work - public domain | - · DailyMed setid dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94 | Sections 5.1-5.3, 6.1, 6.2. |
| **HV1** | Buijsen 2024, Biomedicines 12(9):1933 | `HV1_Buijsen2024_Biomedicines_PMC11428300.pdf` | 13 | CC BY 4.0 | 10.3390/biomedicines12091933 · PMC11428300 | 3 / 9. Table 1 prints all three sequences. |
| **HV2** | Chen 2024, Nature 628:818-825 | `HV2_Chen2024_Nature_PMC11043036.pdf` | 32 | CC BY 4.0 | 10.1038/s41586-024-07310-6 · PMC11043036 | 7 / 8. Values from Source Data 41586_2024_7310_MOESM13_ESM.xlsx. |
| **HV3** | Woffindale 2026, Mol Ther Nucleic Acids 102848 | `HV3_Woffindale2026_MTNA_PMC12925542.pdf` | 12 | CC BY-NC-ND 4.0 | 10.1016/j.omtn.2026.102848 · PMC12925542 | 24 / 17. The 23 sequences are in mmc1.pdf, NOT in this article text. |
| **O1** | O'Rourke 2026, Nucleic Acids Res 54(3):gkaf1333 | `O1_ORourke2026_NAR_PMC12865454.pdf` | 17 | CC BY-NC 4.0 | 10.1093/nar/gkaf1333 · PMC12865454 | Instruments only, 0 rows. Acute-inhibition scales. |
| **B1** | Bravo-Hernandez 2026, Nucleic Acids Res 54(3):gkag057 | `B1_BravoHernandez2026_NAR_PMC12867516.pdf` | 20 | CC BY-NC 4.0 | 10.1093/nar/gkag057 · PMC12867516 | Held, 0 rows. Would add the first non-human-primate rows. |

## Not here, and why

Three items the research read are copyrighted publisher material that is not licensed for
redistribution, so they are named rather than copied. Retrieve your own copy:

| ID | Item | Where |
|---|---|---|
| **M1** | McColgan P, et al. Tominersen in Adults with Manifest Huntington's Disease. *N Engl J Med*. 2023;389(23):2203–2205 (Correspondence). | doi:10.1056/NEJMc2300400 · PMID 38055260 — via an institutional NEJM subscription |
| **S1** | Schobel S. *Preliminary results from GENERATION HD1*. CHDI Therapeutics Conference, 2021. | CHDI Foundation conference materials |
| **B2** | Boak L, McColgan P. *Treatment and post-treatment effects of tominersen in GENERATION HD1*. CHDI Therapeutics Conference, 2022. | CHDI Foundation conference materials |

**P1**, US Patent 10,799,523 B2 (Olson et al.), is a US Government work in the public domain and
is already in the repository at `sources/P1_Olson_US10799523B2/raw/us10799523.pdf`.

**CT1** is not a paper. Its 29 ClinicalTrials.gov records are committed as JSON at
`sources/CT1_ClinicalTrialsGov/`, exactly as the API returned them.

## The supplements are the valuable part

For most of these sources the toxicity data is in the supplementary material, not the article:
H1's Table S1, K1's Table S2, L1's Table S1, HV2's Source Data workbook and HV3's `mmc1.pdf`.
Those files are already in the repository beside each source's folder under `sources/`.

## Reproducing this folder

```bash
python3 src/fetch_papers.py     # re-downloads and re-verifies every file listed above
```
