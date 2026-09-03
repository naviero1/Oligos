# Source register and research queue — OligoTox-CNS

Two kinds of material live under `sources/`:

1. **Ingested** — read by the v1.0 build pipeline. Every row in `data/` traces to one of these.
2. **Gathered, not yet ingested** — retrieved during research and held for v1.1. **No v1.0 row
   depends on any of it**, so nothing in the released dataset changes if these are removed.

## Ingested in v1.0

| ID | Source | Licence | In repo | Contributes |
|---|---|---|---|---|
| **H1** | Hagedorn 2022, *Nucleic Acid Ther* 32(3):151–162 — mouse ICV acute tolerability + rat neuron calcium assay | **CC BY 4.0** | yes | 1,825 oligos / 2,006 measurements — the core |
| **K1** | Miller 2024, *Mol Ther Nucleic Acids* — divalent-cation formulation rescue | CC BY-NC | yes | 7 / 41 |
| **L1** | Kuroda 2025, *Mol Ther Nucleic Acids* — late-onset neurotoxicity, 5′-CP | CC BY-NC | yes | 5 / 6 |
| **C1** | FDA prescribing information (tofersen, nusinersen) via DailyMed | public domain | fetched live | 2 / 12 |
| **CT1** | ClinicalTrials.gov posted results — MedDRA adverse-event tables for 22 trials of CNS-delivered oligonucleotides | **public domain** (US Government work) | yes, 29 JSON files | 2,329 / 6 — the module's principal human source and its only quantitative hydrocephalus rows |
| **O1** | O'Rourke 2026, *Nucleic Acids Res* 54(3):gkaf1333 — acute *inhibition* scales | CC BY-NC | yes | instruments only, 0 rows |

## Gathered for v1.1 — not ingested

| ID | Source | Licence | In repo | What it would add |
|---|---|---|---|---|
| **B1** | Bravo-Hernandez 2026, *Nucleic Acids Res* 54(3):gkag057 — transient acute neuronal *activation* response, rat/mouse/NHP | CC BY-NC | yes | Would upgrade `docs/SCORING_INSTRUMENTS.md` §4 from *[fetch summary]* to *[read directly]*, and add the first **non-human-primate** rows |
| **P1** | US 10,799,523 B2 (Olson et al.) — CNS oligonucleotide patent | **public domain** (US patent) | yes | Patent tables pair sequence with toxicity rating; the format that supplied 21 rows to the sibling kidney module |
| **S1** | Schobel 2021, CHDI — *Preliminary results from GENERATION HD1* | © Roche, conference deck | **no — see below** | Tominersen ventricular-volume and NfL detail behind the clinical failure |
| **B2** | Boak & McColgan 2022, CHDI — *Treatment and post-treatment effects of tominersen in GENERATION HD1* | © Roche, conference deck | **no — see below** | Post-treatment follow-up on the same trial |
| **M1** | McColgan 2023, *N Engl J Med* 389(23) Correspondence — *Tominersen in Adults with Manifest Huntington's Disease* | © NEJM | **no — see below** | The peer-reviewed statement of the GENERATION HD1 outcome |

## Why three sources are on disk but not in git

S1, B2 and M1 are **copyrighted publisher material that is not licensed for redistribution** — a
Roche conference deck twice over, and an NEJM correspondence item. Committing them would
republish them, which is a different act from reading them for research.

They are therefore listed in `.gitignore`. They remain on the working disk, and the table above
records exactly what they are so anyone can retrieve their own copy. This is the same
per-source-terms discipline `LICENSE.md` applies at row level.

**This was a judgement call, not an instruction — say the word and they can be committed.**

Everything else under `sources/` is CC BY, CC BY-NC or US public domain and is committed, so the
v1.0 pipeline rebuilds from the repo alone.

---

## Human *in vitro* backlog — identified 18 2026-09, not yet extracted

The Challenge brief's stated particular interest is *"datasets based on in vitro human systems or
able to extrapolate data between in vitro human systems and animal data"*. The released dataset has
**zero** `human_invitro` rows. An earlier revision of this file, and of the narrative, said no such
published source had been found. **That was wrong, and it was wrong because the first sweep was too
narrow** — it searched for oligonucleotide *neurotoxicity* screening platforms rather than for
oligonucleotide studies that happen to report a toxicity readout in a human neural system.

A targeted sweep across ten angles found the sources below. Each reports a per-compound outcome in
a human-derived neural system. None is extracted yet, so **no released row depends on any of them**;
they are listed so the gap is a costed backlog rather than an unknown.

| Source | Human system | What it carries | Sequences printed? |
|---|---|---|---|
| Woffindale C, Galindo Riera N, Wood MJA, Varela MA. Design, validation, and functional impact of oligonucleoti | SH-SY5Y human neuroblastoma (neuronal); plus HEK293-APPswe human non-neuronal comparator; mouse | 11 bispecific gapmer ASOs designed against 20 candidate AD genes. Viability tested across 0.1-100 nM (specific doses nam | yes |
| Flynn LL, et al. Single stranded fully modified-phosphorothioate oligonucleotides can induce structured nuclea | SH-SY5Y human neuroblastoma (the study's only neuronal line); primary human dermal fibroblasts  | 90+ oligonucleotide sequences (18-30 nt) across four chemistries - 2'-O-methyl phosphorothioate (main focus), PMO, DNA p | yes |
| Ottesen EW, Murzyn WA, Kaas RL, Bertrand KJ, Payne JL, Singh RN. A therapeutic antisense oligonucleotide encom | SH-SY5Y human neuroblastoma ('neuron-like', Supplementary Figure S7); GM03813 SMA patient fibro | F18MOE is an 18-mer with sequence and chemistry identical to nusinersen (a marketed CNS ASO), compared head-to-head with | yes |
| Buijsen RAM, et al. Calcium-Enhanced Medium-Based Delivery of Splice Modulating Antisense Oligonucleotides in  | 2D hiPSC-derived neuronal cultures at day 11-14 maturation, ~40% MAP2+ neurons / ~60% GFAP+ ast | Three 2'-O-methoxyethyl phosphorothioate ASOs with FULL SEQUENCES PRINTED IN TABLE 1: control H40 (FAM-labelled) 5'-UCC  | yes |
| Thirumalai S, Livesey FJ, Patani R, Hung C. APP antisense oligonucleotides are effective in rescuing mitochond | hiPSC-derived astrocytes from a healthy control individual and from an individual with Down syn | A single 20-mer APP-targeting gapmer, PS backbone with five 2'-MOE nucleotides each side and 5-methyl-deoxycytidine in t | yes |
| Drygin D, Barone S, Bennett CF. Sequence-dependent cytotoxicity of second-generation oligonucleotides. Nucleic | A549 human lung carcinoma, HepG2 human hepatocellular carcinoma, Hep3B (p53-null). ALL HUMAN, b | 43 second-generation (2'-MOE) oligonucleotides screened for cytotoxicity at 100-1000 nM, with per-oligonucleotide result | yes |
| Antisense oligonucleotide therapeutic approach for Timothy syndrome. Nature. 2024;628:818-825 (Pasca lab). | Timothy syndrome patient hiPSC-derived human cortical organoids (hCO), dissociated hCO neurons  | SOURCE: 'to identify adverse effects of ASOs in human neural cells we measured their toxicity, immunogenicity and off-ta | not stated |
| Oligonucleotides Targeting DNA Repeats Downregulate Huntingtin Gene Expression in Huntington's Patient-Derived | HD patient-derived iPSC lines (from NINDS repository) neuralised to neural stem cells (NSC), ne | SOURCE. Compound: CAG19, a 19-nt DNA/LNA mixmer anti-gene oligonucleotide with full phosphorothioate backbone. Sequence  | yes |
| Calcium-Enhanced Medium-Based Delivery of Splice Modulating Antisense Oligonucleotides in 2D and 3D hiPSC-Deri | Human iPSC-derived neural progenitor cells differentiated with STEMdiff Forebrain Neuron kit an | SOURCE. Table 1 prints three ASO sequences, all 2'-O-methoxyethyl-modified phosphorothioate: (1) H40 FAM-labelled 5'-UCC | yes |
| Targeted antisense oligonucleotide treatment rescues developmental alterations in spinal muscular atrophy orga | SMA patient and control hiPSC-derived spinal cord organoids (SCOs, lines C1-C3 and S1-S5) and b | SOURCE. Oligonucleotides: MO-10-34, a splice-modulating morpholino (PMO) targeting SMN2, tested both unconjugated ('bare | not stated |
| Bowles KR, Silva MC, Whitney K, Bertucci T, Berlind JE, Lai JD, Garza JC, Boles NC, Mahali S, Strang KH, Marsh | Human iPSC-derived telencephalic/cerebral organoids from frontotemporal dementia patients carry | The single ASO-in-cerebral-organoid study identified by the Lange 2022 review. Two oligonucleotides: a PIKFYVE-targeting | yes |
| Chen X, Birey F, Li MY, Revah O, Levy R, Thete MV, Reis N, Kaganovsky K, Onesto M, Sakai N, Hudacova Z, Hao J, | Human cortical organoids (hCO), human subpallial organoids (hSO) and human forebrain assembloid | ASO.14, ASO.17, ASO.18, ASO.20 and ASO.Scr; 20-nt, phosphorothioate backbone, 2'-MOE, 5-methylcytosine, made by IDT. Con | not stated |
| Faravelli I, Rinchetti P, Tambalo M, Simutin I, Mapelli L, Mancinelli S, Miotto M, Rizzuti M, D'Angelo A, Cord | Human iPSC-derived SPINAL CORD organoids and cerebral organoids from 5 SMA type 1 male donor li | Morpholino MO-10-34 targeting the SMN2 ISS-N1 region downstream of exon 7, and an r6 (arginine-rich cell-penetrating pep | yes |
| Buijsen RAM, van der Graaf LM, Kuijper EC, et al. Calcium-Enhanced Medium-Based Delivery of Splice Modulating  | hiPSC-derived 2D neurons and astrocytes (control NPCs from a prior study), and 3D cerebral orga | Three 2'-O-methoxyethyl phosphorothioate ASOs, ALL SEQUENCES PRINTED IN TABLE 1: H40 5'-UCC UUU CAU CUC UGG GCU C-3'; HT | yes |
| Konig S, Shen X, Mantovani G, Winkler GS, Zhu Z, Moeendarbary E. Transferrin-Functionalized Liposomes Enhance  | Microfluidic 3D BBB chip: human brain microvascular endothelial cells, astrocytes and pericytes | MAPT-targeting phosphorothioate ASO, Cy3-labelled. SOURCE PRINTS THE SEQUENCE: 5'-GCTTTTACTGACCATGCGAG-3'; scrambled con | yes |
| Selvakumaran J, Ursu S, Bowerman M, Lu-Nguyen N, Wood MJ, Malerba A, Yanez-Munoz RJ. An Induced Pluripotent St | iPSC-derived brain microvascular endothelial cells (BMECs) in monoculture from three fibroblast | Pip6a-conjugated phosphorodiamidate morpholino oligomer (Pip6a-PMO) targeting SMN2 pre-mRNA exon 7 inclusion, with Pip6a | not stated |
| Yuan NY, Richards WD, Parham KT, Clark SG, Greuel K, Polzin B, Smith SW, Lebakken CS. Neural organoids incorpo | Human iPSC-derived neural organoids incorporating iPSC-derived MICROGLIA - a neuroimmune organo | NO OLIGONUCLEOTIDE IS TESTED. The compounds are developmental neurotoxins and industrial chemicals (lead acetate is the  | not stated |
| Means JC, Martinez-Bengochea AL, Louiselle DA, Nemechek JM, Perry JM, Farrow EG, Pastinen T, Younger ST. Rapid | Patient-derived CARDIAC organoids from Duchenne muscular dystrophy patients (one with a structu | Included ONLY as a documented exclusion so the parent does not re-surface it: this is the highest-profile 'personalised  | not stated |

**Priority order for extraction.** The three worth doing first all print full sequences: the
calcium-enhanced-delivery study (three 2'-MOE PS ASOs, Table 1, tested in both hiPSC-derived 2D
neurons and 3D cerebral organoids), the Timothy-syndrome cortical-organoid study (five 20-mer
2'-MOE ASOs with explicit toxicity, immunogenicity and viability readouts), and the 43-compound
2'-MOE cytotoxicity screen, which is the only one large enough to model on its own.

Extracting even the first of these moves `human_invitro` off zero and changes how this module reads
against the brief's priority clause.
