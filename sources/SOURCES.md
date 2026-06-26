# Sources — prioritized fetch list & drop-instructions

**Network status (2026-06-26):** this session's egress policy **blocks all
outbound web fetch** (CONNECT tunnel denied 403 for PMC, USPTO, publishers,
even Wikipedia; only `WebSearch` summaries work). Therefore primary-source
files must be **downloaded by the user and dropped into this `sources/`
directory** for local extraction. Identifiers below were verified via
`WebSearch` this session.

## How to hand files back for extraction

Drop files here using these names (so I can locate + parse them), then tell me:

```
sources/
  N1_Dieckmann2018_MTNA_PMC5725219.pdf          + supplementary tables (.xlsx/.docx)  ← 236-oligo panel
  N2_drisapersen_ciPTEC_PMC6796739.pdf          + any supplementary files
  N3_US11105794_nephrotox_assay.pdf
  N4_US11479818_nephrotox_assay.pdf
```

For journal papers the **supplementary tables are the high-value payload**
(per-oligo sequence panels with readouts) — please grab those too, not just the
main PDF. CSV/XLSX/DOCX/PDF all fine; I read them locally.

---

## KIDNEY-SPECIFIC (priority — strict-kidney rows)

### N2 — Drisapersen reversible proteinuria / ciPTEC  ✅ strict kidney
- **Title:** *Therapy with 2′-O-Me Phosphorothioate Antisense Oligonucleotides
  Causes Reversible Proteinuria by Inhibiting Renal Protein Reabsorption.*
- **Open access:** PMC**6796739** (`https://pmc.ncbi.nlm.nih.gov/articles/PMC6796739/`)
- **Why:** drisapersen (2′-OMe PS ASO, exon-51 skipping, DMD) in **DMD patients +
  monkey + human ciPTEC**; cell viability + LMW-protein uptake in vitro.
  Maps directly to the functional proximal-tubule phenotype.
- **Redistribution:** journal OA — likely `derived_features_only`; confirm license.

### N3 — US Patent 11,105,794 "In vitro nephrotoxicity screening assay"  ✅ strict kidney
- **PDF (public domain):** `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11105794`
- **Why:** screening assay for nephrotoxicity of nucleic-acid drugs (RNAi
  agents, ASOs, aptamers). Worked examples → per-oligo rows.
- **Redistribution:** `public_domain` (US patent) — values may be reproduced.

### N4 — US Patent 11,479,818 "In vitro nephrotoxicity screening assay"  ✅ strict kidney
- **PDF (public domain):** `https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11479818`
- **Why:** companion patent; identifies **EGFR** as a nephrotox biomarker,
  combinable with **KIM-1**. Examples → per-oligo rows with biomarker readouts.
- **Redistribution:** `public_domain`.

### Additional kidney candidates surfaced this session (to vet)
- **SPC5001 proximal-tubule-on-a-chip** — *"Nephrotoxic antisense oligonucleotide
  SPC5001 induces kidney injury biomarkers in a proximal tubule-on-a-chip,"*
  Arch Toxicol 2021, DOI `10.1007/s00204-021-03062-8`. SPC5001 is a known
  human-nephrotoxic LNA gapmer (apoB) → strong grade-2/3 anchor. _Verify OA._
- **"Nephrotoxicity of marketed antisense oligonucleotide drugs"** — review,
  PMC**10174585**. Good for cross-checking clinical renal grades (anchor rows).
- **"Comparative Renal Toxicopathology of Antisense Oligonucleotides"** — animal
  histopath series (grades 1–3). _Find DOI/OA status._
- **"Preclinical Evaluation of the Renal Toxicity of Oligonucleotide Therapeutics
  in Mice"** — NCBI Bookshelf NBK584232 (methods + readouts).

---

## RECLASSIFIED — N1 is hepatotox, not kidney  ⚠️

### N1 — Dieckmann et al. 2018, *Mol Ther Nucleic Acids*  ❌ NOT kidney (hepatotox/HDT)
- **Title:** *A Sensitive In Vitro Approach to Assess the
  **Hybridization-Dependent** Toxic Potential of High Affinity Gapmer
  Oligonucleotides.*  MTNA 2018;10:45–54. DOI `10.1016/j.omtn.2017.11.004`.
- **Open access:** PMC**5725219**.
- **Correction:** the priority list filed this as kidney. It is actually a
  **hybridization-dependent (off-target) hepatotoxicity** assay using
  **transfected mouse fibroblasts**, validated on **236 LNA-ASOs** with known
  hepatotoxic potential — **no kidney readout**.
- **Still valuable:** that **236-oligo panel** (sequences + design + HDT score)
  is the single biggest *volume* source available → use for the **hepatotox
  fallback** category, every row flagged `is_kidney_specific=FALSE`.
- **Redistribution:** journal OA — `derived_features_only`; confirm.

---

## HEPATOTOX FALLBACK (use only if kidney stalls below 100; flag every row `is_kidney_specific=FALSE`)

- **N1 Dieckmann 236-oligo panel** (above) — largest single panel.
- **Hagedorn et al.** — hepatotox ASO panels. _Confirm DOI._
- **Burdick et al.** — ASO hepatotox sequence series. _Confirm DOI._
- **Kasuya et al.** — siRNA/ASO tox panel. _Confirm DOI._
- **Creyon 2025** — ML/large-panel oligo tox dataset. _Confirm citation/DOI._

_(DOIs intentionally left unconfirmed rather than guessed; fill on retrieval.)_

---

## ANCHOR SOURCES USED (clinical / regulatory — marketed oligos, seed rows MSR001–016)

These were extracted via `WebSearch` (no full-text fetch) into the 16 provisional
anchor rows. Labels/EMA = `public_domain`; journal stats = `summary_stat`.

| ID | Source | Used for | Redistribution |
|----|--------|----------|----------------|
| A1 | Inotersen — NEJM 2018 `NEJMoa1716793` (NEURO-TTR) + FDA label 211172 | crescentic GN 3%, UPCR>5×ULN 15%, SCr rise 11% | public_domain |
| A2 | Inotersen FSGS case — AJKD 2022 `S0272-6386(22)00929-5` | biopsy FSGS | summary_stat |
| A3 | SPC5001 — van Poelgeest 2013 `10.1111/bcp.12738` | ATN/AKI, urinary KIM-1, β2-microglobulin | summary_stat |
| A4 | SPC5001 PT-on-chip — Arch Toxicol 2021 `10.1007/s00204-021-03062-8` (PMID 33961089) | **in-vitro** KIM-1 induction | summary_stat |
| A5 | Givosiran — NEJM 2019 `NEJMoa1913147` (ENVISION) + FDA label | eGFR decline / SCr rise 15% vs 7% | public_domain |
| A6 | Givosiran — Liver Int 2022 `10.1111/liv.15090` (ENVISION 24-mo) | CKD onset/worsening (5 pts) | summary_stat |
| A7 | Nusinersen — FDA label (Spinraza PI) | urine protein 58% vs 34% | public_domain |
| A8 | Volanesorsen — EMA SmPC (Waylivra) + APPROACH `NCT02658175` | proteinuria 7.84%, FSGS 1/14 | public_domain |
| A9 | Mipomersen — FDA label 203568 + EMA EPAR (Kynamro) | proteinuria 9% vs 3%, GN case | public_domain |
| A10 | Inclisiran — FDA label (Leqvio) + Novartis SmPC | no renal signal (**negative control**) | public_domain |
| REV | "Nephrotoxicity of marketed ASO drugs" — PMC10174585 | cross-check of clinical renal grades | summary_stat |

_Sequences for all anchor oligos are published (labels/INN/patents) but were left
`TBD` rather than recalled from memory — retrieve to satisfy the Phase 2
"sequences of all oligos tested" requirement._

## NEWLY SURFACED SOURCES & SEARCH ALIASES (added 2026-06-26)

### Confirmed identifiers for the priority sources (search under any of these)
- **N2** drisapersen proteinuria — *Mol Ther Nucleic Acids* 2019; **PMC6796739**;
  Cell Press pii **S2162-2531(19)30244-6** (ScienceDirect **S2162253119302446**);
  Utrecht (Masereeuw lab, ciPTEC). Drug dosed 6 mg/kg; readout urinary A1M.
  Aliases: "2OMePS reversible proteinuria", "drisapersen A1M proximal tubule".
- **N1** Dieckmann — pii **S2162-2531(17)30288-3**; **PMC5725219**;
  DOI 10.1016/j.omtn.2017.11.004. (hepatotox, 236 LNA-ASOs, mouse fibroblasts.)
- **N3/N4** patents, both *"In vitro nephrotoxicity screening assay"*:
  **US 11,479,818** = EGFR-mRNA-decrease readout; **US 11,105,794** =
  EGF-in-supernatant-increase readout. Tool reference oligo SEQ ID NO:1 =
  `CGTcagtatgcgAATc` (β-D-oxy-LNA + PS). Assignee to confirm on the patent face.
  Sibling application: **US 2015/0219625** *"In vitro assay for predicting renal
  proximal tubular cell toxicity."* Find WO/EP family via Google Patents
  "Also Published As" / Espacenet.

### NEW kidney-specific sources to fetch (strict-kidney)
- **Sandelius et al. 2020** *"Urinary Kidney Biomarker Panel Detects Preclinical
  Antisense Oligonucleotide-Induced Tubular Toxicity,"* *Toxicol Pathol*;
  DOI 10.1177/0192623320964391; **PMID 33084520**. cEt ASO 50 mg/kg in mice →
  proximal tubular pathology + KIM-1, clusterin, NGAL, cystatin C. (AstraZeneca)
- **Engelhardt 2016** *"Comparative Renal Toxicopathology of Antisense
  Oligonucleotides"* (review), *Nucleic Acid Ther* 26:199–209;
  DOI 10.1089/nat.2015.0598; **PMID 26983026**. **Reference-list goldmine.**
- **3D-RPTEC platform** (tests SPC5001 + nucleic-acid drugs; ATP depletion +
  high-content biomarkers). Find via "3D-RPTEC oligonucleotide nephrotoxicity
  SPC5001 high-content".
- **"Preclinical Evaluation of the Renal Toxicity of Oligonucleotide Therapeutics
  in Mice"** — *Methods Mol Biol* 2022; **PMID 35213032**; Bookshelf **NBK584232**.
- **Frazier 2015** "Antisense Oligonucleotide Therapies" (Toxicol Pathol,
  10.1177/0192623314551840); **Frazier 2022** kidney-effects review
  (10.1177/01926233221100414).

### Hepatotox fallback — now with confirmed citations
- **Hagedorn 2013** *"Hepatotoxic potential of therapeutic oligonucleotides can be
  predicted from their sequence and modification pattern,"* *Nucleic Acid Ther*.
- **Burdick 2014** *"Sequence motifs associated with hepatotoxicity of LNA-modified
  ASOs,"* *Nucleic Acids Res* 42:4882–4891; DOI 10.1093/nar/gku142.
- **Kasuya 2016** *"RNase H1-dependent hepatotoxicity caused by LNA gapmer ASOs,"*
  *Sci Rep* 6:30377; DOI 10.1038/srep30377 (**open access**).

### Source-hunting strategy
- Mine the reference lists of the two reviews — **Engelhardt 2016** and
  **"Nephrotoxicity of marketed ASO drugs" (PMC10174585)** — they aggregate most
  primary renal-tox papers.
- Key labs / authors: **Roche** (Dieckmann, Hagedorn, Berrera); **AstraZeneca**
  (Sandelius, Söderberg, Andersson); **Ionis** (Henry, Frazier, Engelhardt);
  **Utrecht/ciPTEC** (Masereeuw).
- Key journals: *Nucleic Acid Therapeutics*, *Mol Ther Nucleic Acids*,
  *Toxicologic Pathology*, *Nucleic Acids Research*.
- Patents: Google Patents → "Also Published As" + "Cited By"; Espacenet patent
  family; USPTO Patent Public Search (ppubs.uspto.gov).

## LOCAL SOURCE FILES (committed to repo, organized 2026-06-26)

Uploaded via GitHub and sorted under `sources/`:

```
sources/
  kidney/      — strict-kidney primary sources & reviews
    Janssen2019_drisapersen_reversible_proteinuria_ciPTEC_PMC6796739.pdf  (= N2; drisapersen patients+monkey+ciPTEC)
    Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf   (= source "REV"; marketed-ASO renal review)
    Frazier2022_kidney_effects_review_ToxPathol.pdf               (DOI 10.1177/01926233221100414)
    Sandelius2020_urinary_kidney_biomarker_panel_ASO_tubular_tox_PMID33084520.pdf  (= K1; cEt ASO mouse; KIM-1/clusterin/NGAL/cystatin-C)
    MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf       (book; contains the renal-tox-in-mice chapter, NBK584232)
  hepatotox/   — hepatotox fallback panels (every extracted row → is_kidney_specific=FALSE)
    Dieckmann2018_HDT_236-LNA-ASO_hepatotox_PMC5725219.pdf        (N1 main PDF)
    Dieckmann2018_supp_mmc1_oligo_sequences_Tm.pdf                (Table S1: GAPDH LNA-ASO sequences + Tm; NO per-oligo tox)
    Dieckmann2018_supp_mmc2_full_with_supptables.pdf              (article + supp; Myd88 set 3 toxic/3 tolerated; aggregate 236 analysis)
    Burdick2014_LNA-ASO_hepatotox_seqmotifs_NAR.pdf               (DOI 10.1093/nar/gku142)
    Hagedorn2013_hepatotox_from_sequence_NAT.pdf                  (DOI 10.1089/nat.2013.0436)
  reference/   — background reviews / textbooks / project docs (NOT per-row data)
    Frazier2015_ASO_therapies_review_ToxPathol.pdf                (DOI 10.1177/0192623314551840)
    Sioud_oligo_immunostimulation_cytokines_book.pdf             (immunostimulation; off-endpoint)
    CasarettDoull_Toxicology_textbook.pdf                         (general toxicology textbook, ~22 MB)
    OligoTox_challenge_brief.pdf                                  (challenge executive summary)
  _unrelated/  — off-topic upload, flagged for REMOVAL
    Tipthara2016_urinary_lipidomics_OFFTOPIC.pdf                  (urinary lipidomics — NOT oligonucleotide-related)
```

**Extraction status:** pending (next step). Hepatotox panels (Burdick, Hagedorn)
= volume for the fallback bucket; kidney reviews (Wu, Frazier) + the MMB renal
chapter = strict-kidney cross-reference and any extractable per-oligo findings.

**STILL MISSING — highest-priority strict-kidney VOLUME (please add to `sources/kidney/`):**
- ~~**N2** drisapersen ciPTEC — PMC6796739~~ ✅ **acquired** (Janssen 2019)
- **N3/N4** USPTO patents 11,105,794 & 11,479,818 (public domain; contain oligo sequences + readouts) — **strict kidney** — ⛔ couldn't be located by user; **#1 remaining gap**
- **N1 Dieckmann supplement** — ✅ acquired (mmc1 = Table S1 GAPDH sequences+Tm; mmc2 = article + Myd88 labeled set). BUT these PDFs only give the 6-oligo Myd88 labeled set + sequence/Tm design data; the **full 236 per-oligo tox values are NOT in them** (aggregate analyses only — raw per-oligo table is a separate Excel). Hepatotox volume from here is limited.
- ~~**Sandelius 2020** urinary biomarker panel — PMID 33084520~~ ✅ **acquired** (K1; extracted → MSR031–039)

## Provenance discipline
- Each extracted row → `source_id` (N1…), `source_ref` (DOI/patent),
  `source_table` (exact table/figure/claim), `redistribution`.
- Patents = reproduce freely. Journal supplementary = prefer derived features /
  summary stats unless the license permits raw redistribution.
