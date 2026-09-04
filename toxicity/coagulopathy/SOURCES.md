# Sources — OligoTox-Coagulopathy

The provenance registry for this endpoint. Every measurement row in
[`data/measurements.csv`](./data/measurements.csv) carries a `source_id` that resolves here,
and every document listed is committed to [`sources/documents/`](./sources/documents/) so a reader can
re-read the evidence without network access.

This file is **generated** from [`data/sources.csv`](./data/sources.csv) — that table is the
source of truth. Regenerate with `scripts/build_sources_md.py` after any rebuild.

**75 sources · 2388 measurements.**

| Redistribution | Sources |
|---|---:|
| `public_domain` | 23 |
| `publisher_restricted` | 18 |
| `CC_BY_NC_ND` | 15 |
| `CC_BY` | 15 |
| `CC_BY_NC` | 3 |
| `unresolved` | 1 |

Rows inherit `redistribution` from their source. Public-domain sources (US patents and
FDA labels) may have their values reproduced freely; `publisher_restricted` and
`CC_BY_NC_ND` sources are cited and their values recorded, but the underlying full texts
are referenced, not redistributed onward.

## Registry

| ID | Rows | Oligos | Source | Identifier | Redistribution |
|---|---:|---:|---|---|---|
| `COG-S035` | 702 | 14 | Modulation of Factor 11 expression. United States Patent US 10,772,906 B2, Ionis Pharmaceuticals, Inc. | US 10,772,906 B2 | `public_domain` |
| `COG-S025` | 156 | 0 | Seth Chhabra E, Liu M. Evaluation of the interference of fitusiran and antithrombin lowering in plasma on rout… | PMC12451317 / PMID 40988732 / doi:10.1016/j.rp… | `CC_BY_NC_ND` |
| `COG-S037` | 156 | 4 | Methods for modulating factor 12 expression. United States Patent US 9,150,864 B2, Isis Pharmaceuticals, Inc. | US 9,150,864 B2 | `public_domain` |
| `COG-S075` | 129 | 8 | Monia BP, Freier SM, Wancewicz EV, et al. (assignee Isis Pharmaceuticals, Inc.). Modulation of transthyretin e… | US 9,061,044 B2 | `public_domain` |
| `COG-S033` | 87 | 10 | Modulation of prekallikrein (PKK) expression. United States Patent US 9,670,492 B2, assignee Ionis Pharmaceuti… | US 9,670,492 B2 | `public_domain` |
| `COG-S074` | 80 | 32 | Nagano M, Kubota K, Sakata A, Nakamura R, Yoshitomi T, Wakui K, Yoshimoto K. A neutralizable dimeric anti-thro… | PMC10445101 / PMID 37621412 / doi 10.1016/j.om… | `CC_BY` |
| `COG-S032` | 69 | 2 | Modulation of factor 7 expression. United States Patent US 9,029,337 B2, assignee Isis Pharmaceuticals, Inc.; … | US 9,029,337 B2 | `public_domain` |
| `COG-S038` | 57 | 1 | Walsh M, Bethune C, Smyth A, Tyrwhitt J, Jung SW, Yu RZ, Wang Y, Geary RS, Weitz J, Bhanot S; CS4 Investigator… | PMC8820988 / PMID 35155859 / doi:10.1016/j.eki… | `CC_BY_NC_ND` |
| `COG-S085` | 57 | 13 | Locally computed FAERS disproportionality table over oligonucleotide therapeutics and coagulation MedDRA prefe… | faers_coag_signal_table.csv — 57 data rows; co… | `public_domain` |
| `COG-S034` | 55 | 21 | Serpinc1 iRNA compositions and methods of use thereof. United States Patent US 9,376,680 B2, assignee Alnylam … | US 9,376,680 B2 | `public_domain` |
| `COG-S093` | 43 | 1 | U.S. Food and Drug Administration, Center for Drug Evaluation and Research. Integrated Review, NDA 219019, QFI… | NDA 219019; FDA Reference ID 5560526 | `public_domain` |
| `COG-S008` | 41 | 10 | Ali AS et al. New High-Affinity Thrombin Aptamers for Advancing Coagulation Therapy. Cells. 2023;12(18):2230. | PMC10526462 / PMID 37759453 / 10.3390/cells121… | `CC_BY` |
| `COG-S073` | 39 | 2 | Zavyalova E, Samoylenkova N, Revishchin A, Turashev A, Gordeychuk I, Golovin A, Kopylov A, Pavlova G. The Eval… | PMC5735248 / PMID 29311929 / doi 10.3389/fphar… | `CC_BY` |
| `COG-S024` | 34 | 1 | DEFITELIO (defibrotide sodium) injection, for intravenous use. US Prescribing Information. Jazz Pharmaceutical… | DailyMed setId 2c3db989-d7ad-41ed-9ebf-698dcf6… | `public_domain` |
| `COG-S039` | 34 | 0 | Buller HR, Bethune C, Bhanot S, Gailani D, Monia BP, Raskob GE, Segers A, Verhamme P, Weitz JI; FXI-ASO TKA In… | PMC4367537 / PMID 25482425 / doi:10.1056/NEJMo… | `publisher_restricted` |
| `COG-S004` | 32 | 1 | Gissel M, Orfeo T, Foley JH, Butenas S. Effect of BAX499 aptamer on tissue factor pathway inhibitor function a… | PMC3508133 / PMID 22951415 / doi 10.1016/j.thr… | `publisher_restricted` |
| `COG-S086` | 32 | 0 | Individual FAERS case records (openFDA drug/event) for ten oligonucleotide-drug x coagulation-PT pairs, up to … | faers_case_records.json — 10 query groups, 32 … | `public_domain` |
| `COG-S036` | 31 | 6 | Compositions and methods for inhibiting gene expression of factor XII. United States Patent US 10,858,658 B2, … | US 10,858,658 B2 | `public_domain` |
| `COG-S041` | 31 | 1 | Lang T, Hodel K, Kubitza E, et al. Pharmacokinetics, pharmacodynamics, and safety of fesomersen in healthy Chi… | PMC10985948 / PMID 38563414 / doi:10.1111/cts.… | `CC_BY_NC` |
| `COG-S027` | 29 | 0 | Young G, Kavakli K, Klamroth R, et al. Safety and efficacy of a fitusiran antithrombin-based dose regimen in p… | PMC12824673 / PMID 40053895 / doi:10.1182/bloo… | `CC_BY_NC_ND` |
| `COG-S028` | 29 | 0 | Pipe SW, Lissitchkov T, et al. Long-term safety and efficacy of fitusiran prophylaxis, and perioperative manag… | PMC11914172 / PMID 39642315 / doi:10.1182/bloo… | `CC_BY_NC_ND` |
| `COG-S042` | 26 | 2 | Ferrone JD, Bhattacharjee G, Revenko AS, Zanardi TA, Warren MS, Derosier FJ, Viney NJ, Pham NC, Kaeser GE, Bak… | PMC6461157 / PMID 30817230 / doi:10.1089/nat.2… | `CC_BY_NC` |
| `COG-S010` | 25 | 11 | Yu H, et al. Aptameric hirudins as selective and reversible EXosite-ACTive site (EXACT) inhibitors. Nat Commun… | PMC11087511 / PMID 38730234 / 10.1038/s41467-0… | `CC_BY` |
| `COG-S031` | 24 | 0 | McCluskey G, Maynadie H, Borgel D, et al. Fitusiran treatment modulates the ratio between alpha- and beta-anti… | PMC13146349 / PMID 42100790 / doi:10.1002/hem3… | `CC_BY_NC_ND` |
| `COG-S026` | 23 | 1 | QFITLIA (fitusiran) injection, for subcutaneous use. US Prescribing Information. Genzyme Corporation. SPL vers… | DailyMed setid 6dd2f8ac-6f90-4cbf-b197-97d7496… | `public_domain` |
| `COG-S072` | 23 | 4 | Braendli-Baiocco A, Festag M, Dumong Erichsen K, Persson R, Mihatsch MJ, Fisker N, Funk J, Mohr S, Constien R,… | PMC5414856 / PMID 28123102 / DOI 10.1093/toxsc… | `CC_BY_NC_ND` |
| `COG-S006` | 22 | 3 | Multi-record PubMed abstract file covering the REG1/REG2 (pegnivacogin RB006 / anivamersen RB007) and BAX499 (… | pubmed_REG1_pegnivacogin_BAX499_abstracts.txt … | `publisher_restricted` |
| `COG-S009` | 22 | 6 | Yu H, Pitoc G, Zhang M, et al. An Aptamer-Based EXACT Anticoagulant as a Sustainable, Animal-Free Alternative … | PMC12822440 / PMID 41053535 / 10.1002/advs.202… | `CC_BY` |
| `COG-S007` | 21 | 6 | Soule EE, Yu H, Olson L, Naqvi I, Kumar S, Krishnaswamy S, Sullenger BA. Generation of an anticoagulant aptame… | PMC8808741 / PMID 35114109 / DOI in retrieved … | `publisher_restricted` |
| `COG-S082` | 21 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use (CHMP). Assessment report: Dawnzera … | EMA/CHMP/303940/2025 | `publisher_restricted` |
| `COG-S088` | 20 | 0 | Craig EM. Clinical Review (Medical Review), NDA 203568, Kynamro (mipomersen sodium) injection. U.S. Food and D… | FDA NDA 203568 Clinical Review; Reference ID 3… | `public_domain` |
| `COG-S023` | 19 | 2 | Abourahma H, Kempaiah P, Farooqui A, Krupa E, et al. A Comparative Study of Porcine and Ovine Derived Defibrot… | PMC13009829 / PMID 41869748 / DOI 10.1177/1076… | `CC_BY_NC` |
| `COG-S014` | 18 | 6 | Crooke S.T. et al. "Antidotes to antisense compounds." United States Patent 8,389,488 B2 (Isis Pharmaceuticals… | US 8,389,488 B2 | `public_domain` |
| `COG-S030` | 18 | 0 | Young G, Sorensen B, Dargaud Y, et al. Targeting of antithrombin in hemophilia A or B with investigational siR… | PMC8251589 / PMID 33587824 / doi:10.1111/jth.1… | `CC_BY_NC_ND` |
| `COG-S020` | 17 | 1 | Stolte B, Nonnemacher M, Kizina K, Bolz S, Totzeck A, Thimm A, Wagner B, Deuschl C, Kleinschnitz C, Hagenacker… | PMC8563549 / PMID 33899154 / doi:10.1007/s0041… | `CC_BY` |
| `COG-S076` | 17 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use (CHMP). Assessment report: Waylivra … | EMA/180717/2019 | `publisher_restricted` |
| `COG-S003` | 16 | 1 | Ay C, Pabinger I, Kovacevic KD, et al. The VWF binding aptamer rondoraptivon pegol increases platelet counts a… | PMC9631691 / PMID 35772170 / doi 10.1182/blood… | `CC_BY_NC_ND` |
| `COG-S018` | 16 | 1 | Maliglowka M, Dec A, Buldak L, Okopien B. The Effects of Inclisiran on the Subclinical Prothrombotic and Plate… | PMC12470796 / PMID 41002634 / doi:10.3390/jcdd… | `CC_BY` |
| `COG-S019` | 16 | 1 | Zhu X, Li H, Hu C, Wu M, Zhou S, Wang Y, Li W. Safety analysis of laboratory parameters in paediatric patients… | PMC11270951 / PMID 39054521 / doi:10.1186/s128… | `CC_BY` |
| `COG-S059` | 15 | 14 | Ohara M, Nagata T, Hara RI, Yoshida-Tanaka K, Toide N, Takagi K, Sato K, Takenaka T, Nakakariya M, Miyata K, M… | PMC11382116 / PMID 39252874 / doi:10.1016/j.om… | `CC_BY_NC_ND` |
| `COG-S095` | 15 | 1 | U.S. Food and Drug Administration, Center for Drug Evaluation and Research. Integrated Review, NDA 218614, TRY… | NDA 218614; FDA Reference ID 5499859 | `public_domain` |
| `COG-S029` | 14 | 0 | Kenet G, Nolan B, Zulfikar B, et al. Fitusiran prophylaxis in people with hemophilia A or B who switched from … | PMC11181353 / PMID 38452197 / doi:10.1182/bloo… | `CC_BY_NC_ND` |
| `COG-S001` | 13 | 2 | Nimjee SM, de Lange F, Pitoc GA, Sullenger BA. Rats subject to extracorporeal membrane oxygenation have improv… | PMC12208382 / PMID 40599554 / doi 10.1097/CP9.… | `CC_BY_NC_ND` |
| `COG-S011` | 13 | 1 | Reed CR, Bonadonna D, Otto JC, McDaniel CG, Chabata CV, Kuchibhatla M, Frederiksen J, Layzer JM, Arepally GM, … | PMC8728519 / PMID 35036063 / 10.1016/j.omtn.20… | `CC_BY_NC_ND` |
| `COG-S040` | 13 | 1 | Crosby JR, Marzec U, Revenko AS, Zhao C, Gao D, Matafonov A, Gailani D, MacLeod AR, Tucker EI, Gruber A, Hanso… | PMC3717325 / PMID 23559626 / doi:10.1161/ATVBA… | `publisher_restricted` |
| `COG-S094` | 12 | 0 | U.S. Food and Drug Administration, Center for Drug Evaluation and Research. Multi-disciplinary Review and Eval… | NDA 217779; FDA Reference ID 5393603 | `public_domain` |
| `COG-S012` | 11 | 1 | Kolyadko VN, Layzer JM, Perry K, Sullenger BA, Krishnaswamy S. An RNA aptamer exploits exosite-dependent allos… | PMC11260126 / PMID 38985762 / DOI in retrieved… | `CC_BY_NC_ND` |
| `COG-S057` | 11 | 1 | Sheehan JP, Lan HC. Phosphorothioate oligonucleotides inhibit the intrinsic tenase complex. Blood. 1998 Sep 1;… | PMID 9716589 | `publisher_restricted` |
| `COG-S079` | 11 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use (CHMP). Assessment report: Tegsedi (… | EMA/411876/2018 | `publisher_restricted` |
| `COG-S096` | 11 | 2 | U.S. Food and Drug Administration, Center for Drug Evaluation and Research. Integrated Review, NDA 217388, WAI… | NDA 217388; FDA Reference ID 5299039 | `public_domain` |
| `COG-S016` | 10 | 1 | Teva Pharmaceutical Industries / OncoGenex Pharmaceuticals. "Custirsen treatment with reduced toxicity." Unite… | US 2014/0275214 A1 | `public_domain` |
| `COG-S017` | 10 | 2 | Jongejan YK, Dirven RJ, Schrader Echeverri E, de Jong AJL, Pronk ACM, Kooijman S, Rensen PCN, Dahlman JE, Eike… | PMC11909755 / PMID 40093962 / doi:10.1016/j.rp… | `CC_BY` |
| `COG-S043` | 10 | 1 | Liang J, Nilsson S, Wikstrom J, Cao H, Zheng S, Xu Q, Yan X, Ueckert S, Sun Q, Guo C, Zhang H, Liang Z, Gao S,… | PMC12230477 / PMID 40562491 / doi:10.1016/j.ja… | `CC_BY` |
| `COG-S061` | 10 | 3 | Aupy P, Echevarria L, Relizani K, Zarrouki F, Haeberli A, Komisarski M, Tensorer T, Jouvion G, Svinartchouk F,… | PMC7063478 / PMID 31881528 / doi:10.1016/j.omt… | `CC_BY` |
| `COG-S062` | 10 | 2 | Henry SP, Novotny W, Leeds J, Auletta C, Kornbrust DJ. Inhibition of coagulation by a phosphorothioate oligonu… | PMID 9361909 / doi:10.1089/oli.1.1997.7.503 | `publisher_restricted` |
| `COG-S015` | 9 | 1 | Archemix Corp. "Aptamer therapeutics useful in the treatment of complement-related disorders." United States P… | US 7,538,211 B2 | `public_domain` |
| `COG-S021` | 9 | 1 | Calcaterra IL, Santoro R, Vitelli N, Cirillo F, D'Errico G, Guerrino C, Cardiero G, Di Taranto MD, Fortunato G… | PMC11428464 / PMID 39335531 / doi:10.3390/biom… | `CC_BY` |
| `COG-S046` | 9 | 1 | RYTELO (imetelstat) for injection, for intravenous use - US Prescribing Information. Geron Corporation. Medica… | DailyMed setid b0fab7ca-e578-43c5-9df6-bdaff41… | `public_domain` |
| `COG-S058` | 9 | 0 | Sheehan JP, Phan TM. Phosphorothioate oligonucleotides inhibit the intrinsic tenase complex by an allosteric m… | PMID 11305914 / doi:10.1021/bi002396x | `publisher_restricted` |
| `COG-S013` | 8 | 1 | Kandimalla E.R., Manning A., Agrawal S. et al. "Mixed backbone antisense oligonucleotides containing 2'-5'-rib… | US 5,886,165 A | `public_domain` |
| `COG-S045` | 8 | 1 | TEGSEDI (inotersen) injection, for subcutaneous use - US Prescribing Information. Akcea Therapeutics, Inc. Ini… | DailyMed setid 8513207e-b55f-417b-9473-af78514… | `public_domain` |
| `COG-S060` | 8 | 4 | Relizani K, Echevarria L, Zarrouki F, Gastaldi C, Dambrune C, Aupy P, Haeberli A, Komisarski M, Tensorer T, La… | PMC8754652 / PMID 34893881 / doi:10.1093/nar/g… | `CC_BY` |
| `COG-S048` | 7 | 1 | DAWNZERA (donidalorsen) injection, for subcutaneous use - US Prescribing Information. Ionis Pharmaceuticals, I… | DailyMed setid 3ff501e0-f75f-07da-e063-6294a90… | `public_domain` |
| `COG-S049` | 7 | 1 | SPINRAZA (nusinersen) injection, for intrathecal use - US Prescribing Information. Biogen. | DailyMed setid dd70cd5f-b0fc-4ba4-a5ea-89a3477… | `public_domain` |
| `COG-S054` | 7 | 6 | NEGATIVE CONTROL (delivery-platform class) - GalNAc-conjugated siRNA US Prescribing Information: GIVLAARI (giv… | DailyMed setids 167e663c-11e1-497b-a3fc-951d65… | `public_domain` |
| `COG-S077` | 7 | 0 | Akcea Therapeutics Ireland Ltd. WAYLIVRA (volanesorsen) EU Risk Management Plan, CTD Module 1.8.2, Version 3.0… | Waylivra EU-RMP v3.0 (24 Feb 2025) | `publisher_restricted` |
| `COG-S080` | 7 | 0 | Mentari E. Clinical Safety Review (Medical Review), NDA 211172, Tegsedi (inotersen). U.S. Food and Drug Admini… | FDA NDA 211172 Medical Review (Reference ID 43… | `public_domain` |
| `COG-S087` | 7 | 0 | Individual FAERS case records (openFDA drug/event) for MACUGEN (pegaptanib sodium) x four coagulation MedDRA p… | faers_pegaptanib_cases.json — 4 query groups, … | `public_domain` |
| `COG-S005` | 6 | 2 | Chan MY, Cohen MG, Dyke CK, et al. Phase 1b randomized study of antidote-controlled modulation of factor IXa a… | PMID 18506005 / doi 10.1161/CIRCULATIONAHA.107… | `publisher_restricted` |
| `COG-S022` | 6 | 1 | Demirjian S, Ailawadi G, Polinsky M, Bitran D, Silberman S, Shernan SK, Burnier M, Hamilton M, Squiers E, Erli… | PMC5733816 / PMID 29270490 / doi:10.1016/j.eki… | `CC_BY_NC_ND` |
| `COG-S055` | 6 | 1 | Younis HS, Crosby J, Huh JI, Lee HS, Rime S, Monia B, Henry SP. Antisense inhibition of coagulation factor XI … | PMID 22246038 / doi:10.1182/blood-2011-10-3871… | `publisher_restricted` |
| `COG-S063` | 6 | 1 | Shaw DR, Rustagi PK, Kandimalla ER, Manning AN, Jiang Z, Agrawal S. Effects of synthetic oligonucleotides on h… | PMID 9175717 / doi:10.1016/s0006-2952(97)00091… | `publisher_restricted` |
| `COG-S090` | 6 | 0 | Medical Review, NDA 209531, Spinraza (nusinersen) injection. U.S. Food and Drug Administration, CDER, 2016. Bo… | FDA NDA 209531 Medical Review; Reference IDs 4… | `public_domain` |
| `COG-S002` | 5 | 1 | Moreno A, Pitoc GA, Ganson NJ, et al. Anti-PEG antibodies inhibit the anticoagulant activity of PEGylated apta… | PMC6707742 / PMID 30827937 / doi 10.1016/j.che… | `publisher_restricted` |
| `COG-S044` | 5 | 1 | Preclinical safety and bleeding evaluation in swine for a small interfering RNA-lipid nanoparticle that preven… | PMC12766900 / PMID 41076269 / doi:10.1016/j.jt… | `unresolved` |
| `COG-S047` | 5 | 1 | TRYNGOLZA (olezarsen) injection, for subcutaneous use - US Prescribing Information. Ionis Pharmaceuticals, Inc… | DailyMed setid 0f51aa8e-8475-8cf9-e063-6394a90… | `public_domain` |
| `COG-S067` | 5 | 0 | Henry SP, Bolte H, Auletta C, Kornbrust DJ. Evaluation of the toxicity of ISIS 2302, a phosphorothioate oligon… | PMID 9184201 / doi:10.1016/s0300-483x(97)03661… | `publisher_restricted` |
| `COG-S084` | 5 | 1 | Astellas Pharma US, Inc. IZERVAY (avacincaptad pegol) intravitreal solution — US Prescribing Information, SPL … | openFDA SPL set_id 1642fe6a-dc26-4d20-ae6e-654… | `public_domain` |
| `COG-S053` | 4 | 4 | NEGATIVE CONTROL (chemistry class) - Phosphorodiamidate morpholino oligomer exon-skipping US Prescribing Infor… | DailyMed setids 33bff678-7829-479e-9110-b8e33a… | `public_domain` |
| `COG-S064` | 4 | 3 | Agrawal S, Rustagi PK, Shaw DR. Novel enzymatic and immunological responses to oligonucleotides. Toxicol Lett.… | PMID 8597089 / doi:10.1016/0378-4274(95)03573-… | `publisher_restricted` |
| `COG-S083` | 4 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use (CHMP). Assessment report: Amvuttra … | EMA/CHMP/689555/2022 | `publisher_restricted` |
| `COG-S097` | 4 | 0 | U.S. Food and Drug Administration, Center for Drug Evaluation and Research. Integrated Review, NDA 215887, QAL… | NDA 215887; FDA Reference ID 5163540 | `public_domain` |
| `COG-S098` | 4 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use. Assessment report: Qalsody (toferse… | EMA/276404/2024 | `public_domain` |
| `COG-S056` | 3 | 0 | Yacyshyn BR, Barish C, Goff J, Dalke D, Gaspari M, Yu R, Tami J, Dorr FA, Sewell KL. Dose ranging pharmacokine… | PMID 12269969 / doi:10.1046/j.1365-2036.2002.0… | `publisher_restricted` |
| `COG-S068` | 3 | 1 | Burel SA, Han SR, Lee HS, Norris DA, Lee BS, Machemer T, Park SY, Zhou T, He G, Kim Y, MacLeod AR, Monia BP, L… | PMID 23692080 / doi:10.1089/nat.2013.0422 | `publisher_restricted` |
| `COG-S092` | 3 | 1 | Committee for Medicinal Products for Human Use (CHMP). Assessment report: Spinraza (nusinersen). Procedure No.… | EMA/289068/2017; EMEA/H/C/004312/0000 | `CC_BY` |
| `COG-S099` | 3 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use. Assessment report: Rytelo (imetelst… | EMA/13310/2025 | `public_domain` |
| `COG-S052` | 2 | 1 | NEGATIVE CONTROL - ONPATTRO (patisiran) injection, lipid complex, for intravenous use - US Prescribing Informa… | DailyMed setid e87ec36f-b4b4-49d4-aea4-d4ffb09… | `public_domain` |
| `COG-S065` | 2 | 2 | Schmidt M, Hagner N, Marco A, Koenig-Merediz SA, Schroff M, Wittig B. Design and Structural Requirements of th… | PMC4440985 / PMID 25826686 / doi:10.1089/nat.2… | `CC_BY` |
| `COG-S066` | 2 | 1 | Peters S, Wirkert E, Kuespert S, Heydn R, Johannesen S, Friedrich A, Mailaender S, Korte S, Mecklenburg L, Aig… | PMC8780845 / PMID 35057094 / doi:10.3390/pharm… | `CC_BY` |
| `COG-S071` | 2 | 1 | [Author byline not present in the retrieved file and therefore not asserted.] siRNA-mediated reduction of a ci… | PMC11109470 / PMID 38779336 / doi:10.1016/j.om… | `CC_BY_NC_ND` |
| `COG-S078` | 2 | 0 | European Medicines Agency. Waylivra (volanesorsen) Product Information: Annex I Summary of Product Characteris… | Waylivra EPAR Product Information (SmPC + Pack… | `publisher_restricted` |
| `COG-S089` | 2 | 0 | Clinical Pharmacology and Biopharmaceutics Review(s), NDA 203568, Kynamro (mipomersen sodium). U.S. Food and D… | FDA NDA 203568 Clinical Pharmacology Review; R… | `public_domain` |
| `COG-S091` | 2 | 1 | Committee for Medicinal Products for Human Use (CHMP). Assessment report: Kynamro (mipomersen), solution for i… | EMA/305826/2013; EMEA/H/C/002429/0000 | `unresolved` |
| `COG-S050` | 1 | 1 | NEGATIVE CONTROL - WAINUA (eplontersen) injection, for subcutaneous use - US Prescribing Information. AstraZen… | DailyMed setid d7dcb847-71dd-4fff-82d0-d43a465… | `public_domain` |
| `COG-S051` | 1 | 1 | NEGATIVE CONTROL - QALSODY (tofersen) injection, for intrathecal use - US Prescribing Information. Biogen. | DailyMed setid 81356b45-1cb7-4eef-88ea-e44cc18… | `public_domain` |
| `COG-S069` | 1 | 0 | Glover JM, Leeds JM, Mant TG, Amin D, Kisner DL, Zuckerman JE, Geary RS, Levin AA, Shanahan WR Jr. Phase I saf… | PMID 9316823 | `publisher_restricted` |
| `COG-S070` | 1 | 1 | Sereni D, Tubiana R, Lascoux C, Katlama C, Taulera O, Bourque A, Cohen A, Dvorchik B, Martin RR, Tournerie C, … | PMID 9987700 / doi:10.1177/00912709922007552 | `publisher_restricted` |
| `COG-S081` | 1 | 0 | Clinical Pharmacology Review, NDA 211172, Tegsedi (inotersen). U.S. Food and Drug Administration, Center for D… | FDA NDA 211172 Clinical Pharmacology Review (R… | `public_domain` |
| `COG-S100` | 1 | 1 | European Medicines Agency, Committee for Medicinal Products for Human Use. Assessment report: Tryngolza (oleza… | EMA/277774/2025 | `public_domain` |

## Not used as a source of rows

**Crooke ST, Baker BF, Kwoh TJ, et al. (2016)**, "Integrated safety assessment of
2′-O-methoxyethyl chimeric antisense oligonucleotides in non-human primates and healthy
human volunteers", *Mol Ther* 24(10):1771–1782, doi 10.1038/mt.2016.136 — the single lead
[`coagulopathy.md`](./coagulopathy.md) recorded for this endpoint before this dataset
existed. Retrieved and read this round: it does not report the per-compound coagulation
values its title implies. Closed as context, not a row source.

**Methods in Molecular Biology 2434, Ch. 25 §3.1.2** (the volume is held at
[`../kidney/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](../kidney/sources/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf),
where `coagulopathy.md` records it as misfiled under a renal filename) — the passage that defined this endpoint
for the project ("prolongation of coagulation time … at relatively high doses of PS
backbone ASOs"). Class-level prose naming no compound, dose or value; it frames the
dataset but supplies no rows.

