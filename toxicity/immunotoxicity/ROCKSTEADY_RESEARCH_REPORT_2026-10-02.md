# Rocksteady → Beebop: Immunotoxicity research report

Request: `2026-10-02/immunotoxicity`. Report date: **2026-10-03**.
Status: **RESEARCH ONLY — no validated data, labels, adjudications or models were changed.**

Oscar authorized proposals **3, 4 and 5** of the 2026-10-02 request on 2026-10-03, in that order.
**Proposals 1, 2 and 6 are not started**, and the 20-source coverage log is therefore **not yet
produced**. Nothing here is a dataset change; the workbook was not reopened for writing.

Baseline: branch `claude/amazing-galileo-rwiv95`, repository commit `b51003c` at the time of work.
Dataset version unchanged: workbook v0.2, file id `13gq7Weyd21hR9DoZ68ise_RbbQL7bAST`.

---

## 1. Dispositions on the authorized proposals

| # | Proposal | Disposition |
|---|---|---|
| 3 | Inventory Yoshida 2024 before reacquiring; keep reporter cells distinct from primary human immune cells; resolve Goodchild/Peacock and Hornung/Herzner by actual title and identifier | **ACCEPTED — performed.** §2, §4 |
| 4 | Investigate NCT00734240 and the ISIS 353512 clinical publication; separate intended immunostimulation, secondary immune endpoints and unintended inflammation; no posted results is not a negative | **ACCEPTED — performed, with a negative result on the main target.** §3 |
| 5 | Resolve Alharbi 2026 and its preprint as one study; evaluate cross-paper family overlap | **ACCEPTED — and it overturns part of my 2026-10-01 reply.** §4 |

Also performed under proposal 3's acquisition clause and proposal 2's named targets (Burel S1,
Goodchild 207-panel, Valentin 80-construct matrices): **three of the four target supplements were
acquired through open legal routes.** §2.

---

## 2. Acquisitions — performed, with provenance

All four bundles were retrieved from the **Europe PMC `supplementaryFiles` REST endpoint** for the
article's PMCID. No purchase, no subscription, no credential, no author contact. Originals are held
in local research staging only and are **not committed**; the derived sequence tables below are
committed with attribution.

| Source | PMID / PMCID | OA | Published filename | bytes | sha256 (first 16) |
|---|---|---|---|---:|---|
| Goodchild 2009 | 19630977 / **PMC2724479** | Y | `1471-2172-10-40-S1.xls` | 68,608 | bundle `d822cfbc64fce047` |
| Valentin 2021 | 34057477 / **PMC8216285** | Y | `gkab451_supplemental_file.pdf` | 8,127,839 | bundle `64dfdc8f2b00609f` |
| Yoshida 2024 | 38773176 / **PMC11109122** | Y | `41598_2024_61666_MOESM1_ESM.pdf` | 64,740 | bundle `ddedad6e37eedc65` |
| Alharbi 2026 | 41667621 / **PMC13043311** | Y | 19 files (`41590_2026_2429_MOESM1–19_ESM`) | 9,661,371 | bundle `4c578f7b44c4df96` |
| Jones 2012 full text | 23629027 / PMC3511672 | Y | `fullTextXML` | 107,313 | `65787a55b202b433` |

### 2.1 Goodchild 2009 — acquired; the reported count is a superset, not a match

`1471-2172-10-40-S1.xls` is a genuine legacy BIFF workbook, internal metadata "Last Saved By: Toby
Passioura" — Goodchild 2009's last author, which authenticates the file. Title row: *"siRNA
sequences used for screening"*. Columns: `Guide strand (5'→3')` and `Passenger strand (5'→3')`.

| Measure | Value |
|---|---:|
| Data rows | **267** |
| Distinct oligo identifiers | **259** |
| Rows with a valid guide strand | **246** |
| Rows with a valid passenger strand | **243** |
| Distinct guide sequences | **242** |
| Guide lengths | 21-mer ×234, 19-mer ×6, 25-mer ×6 |

**Important correction to the acquisition expectation.** The request and the memo describe a
"207-small-interfering-RNA panel". The supplement holds **246 guide strands / 259 identifiers — a
superset, not 207.** The mapping from this file to the 207 actually screened is **not established by
the supplement alone** and must come from the paper's figures. I therefore report 246 acquired
sequences and **207 as unverified** until that mapping is done. This is an acquisition count, not a
qualified-observation count.

**What it uniquely adds:** both strands of each duplex. That is the first source in this corpus able
to populate `strand_role` and `duplex_partner_id` from primary data rather than inference. No
chemistry modifications are encoded in this file, and no per-sequence outcome values are in it.

Derived: `research_staging/goodchild2009_S1_sequences.csv`, 267 rows, sha256 `6bb96607aded1dee…`.

### 2.2 Valentin 2021 — acquired; exactly 80, and residue-resolved chemistry

Both tables are present and machine-readable. **Supplementary Table S2 contains exactly 80 ASOs**,
matching the reported figure — this one is confirmed, not an expectation. Table S1 adds 47 further
oligonucleotides. 127 unique (name, notation) rows in total.

The notation is **per-residue chemistry**, stated in the caption: *"UPPERCASE alone for DNA, 'm'
indicates 2'OMe base, and * denotes the phosphorothioate backbone."* Example:

```
[cGAS]ASO1-146   mA*mU*mG*mG*mC*C*T*T*T*C*C*G*T*G*C*mC*mA*mA*mG*mG
                 → bases AUGGCCTTTCCGTGCCAAGG, 2'OMe at 1-5 and 16-20, PS throughout
```

| Measure | Value |
|---|---:|
| Unique rows (S1 + S2) | **127** |
| Table S2 screen ASOs | **80** |
| Rows with resolvable per-position 2'OMe | **115 / 127** |
| Rows with resolvable PS linkages | **123 / 127** |
| Lengths | 20-mer ×86, 21-mer ×33, 24-mer ×4, 45-mer ×2, 70-mer ×2 |

Table S2 also carries **four receptor-resolved quantitative readouts per ASO** (cGAS, TLR9, TLR7,
TLR8), with concentrations stated and values normalised to ISD70, ODN2006 and R848 controls, plus
author-defined subsets (10 strongest cGAS inhibitors; 17 with <10% inhibition; 10 / 16 most and 16
weakest TLR9 inhibitors; 4 inhibiting TLR7/9 and cGAS by <30%). This is multi-label,
receptor-specific, per-construct data with positional chemistry — the shape the validation memo's
"Layer 1" models require.

Derived: `research_staging/valentin2021_S1_S2_sequences.csv`, 127 rows, sha256 `f52e73a4330c567a…`,
with `bases_5to3`, `length_nt`, `twoOMe_positions`, `PS_linkage_after_positions`.

### 2.3 Yoshida 2024 — inventoried first, as instructed, then its supplement acquired

Inventory before reacquisition: the **main article was already held in Drive** (`Yoshida_2024.pdf`,
file id `1zaDuzPUbh1jmEBRS_cyRe-r82flbuZIi`, with `Yoshida_2024_suplementary_data.pdf`,
`1CBe0-hrhhnqT061wq-DyCeKi5vQalQLu`). I read the held main text rather than refetching it. I then
acquired the publisher supplement from PMC to confirm the Drive copy's contents.

**Supplementary Table S1 is "TLR9 activity values in Figures 1, 2, 4, and 5" — numeric mean and SD
for every construct, from triplicate experiments.** Approximately **43 distinct measurement rows**
(13 + 5 + 6 + 12 + 10, less 3 values explicitly duplicated between Figures 2a and 2b), of which 4
are solvent controls, leaving **~39 oligo-linked numeric outcomes**.

This is the most significant acquisition of the three, because it is the first source in the corpus
that supplies, per construct and in one place: sequence, positional chemistry (bold/underline in the
main figures), a numeric outcome, a dispersion estimate, a replicate count (n = 3), assay system,
concentration (5 µM) and exposure (18 h). Sign-off Gate 5, "Raw/continuous outcomes retained when
available", currently reads **FAIL**; this source can begin to close it.

**Two caveats that must travel with every row.** The values are **normalised percentages** relative
to SY-ODN18 or ODN2006 = 100, not absolute cytokine concentrations. The system is **HEK-Blue hTLR9
reporter cells**, not primary human immune cells — the authors state that limitation themselves.
Per proposal 3, these classify as `human_cell_line_reporter`, and must not be pooled with PBMC data.

### 2.4 Burel 2022 Table S1 — NOT acquired

Europe PMC returns **no PMCID, `isOpenAccess = N`, `hasSuppl = N`** for PMID 35976085. There is no
open route to the journal supplement through this endpoint. See §5 for the access request. The two
preprints (§4.3) are the remaining open avenue and were not retrieved in this round.

### 2.5 Alharbi 2026 — acquired, and it is not a sequence table

19 files. Contents are **per-figure source data**: one `.xlsx` per main and extended-data figure
(e.g. `Fig 1a(64×10)`, `Ext Dat Fig 6f(100014×6)`, `Ext Dat Fig 7d(4810×12)`), plus three PDFs.
`MOESM4` holds screen data split by chemistry class (`Screens 2'OME` 68×9, `Screens Hybrids` 35×7,
`Screens RNA` 19×3, `Screens DNA` 67×3). A scan of the smaller workbooks found **no sequence-like
cells**, so construct sequences are in the PDF supplements and were not extracted in this round.

Worth recording: this is raw figure-level source data with replicate structure, which is rare in this
corpus and directly relevant to Gate 5.

---

## 3. Proposal 4 — NCT00734240 and the ISIS 353512 clinical publication

**Result on the main target is negative, and that is the finding.** A Europe PMC search for
`"ISIS 353512"` returns 9 records. **None is a standalone trial report for the Phase 1 study.** The
compound appears in Burel 2022, in its two preprints, in reviews, and seven times inside Jones 2012
as a comparator.

So the position is unchanged and now source-backed:

| Element | Status |
|---|---|
| NCT00734240 exists, Phase 1, n = 103, healthy volunteers 18–55, completed 2008-07 → 2010-03, Ionis, org study ID `ISIS 353512 CS1` | registry record read at source |
| Results posted on the registry | **No** |
| Primary publication of the trial | **None found** |
| Adverse inflammatory outcome (IL-6 / hs-CRP elevation, fever, chills, discontinuation) | documented **only secondhand**, via Burel 2022 and reviews |
| Endpoint-evaluable for immunotoxicity | **No** |

Per the request: **no posted results is not a negative outcome.** This record stays
`trial_identified = true`, `primary_source_read = registry only`, `endpoint_evaluable = no`, and the
adverse outcome remains an unsourced narrative claim until a primary document is obtained.

### 3.1 Two human publications for the successor compound were found, both open access

| Publication | Trial | Detail |
|---|---|---|
| **Warren MS, Hughes SG, Singleton W, Yamashita M, Genovese MC.** *Results of a proof of concept, double-blind, randomized trial of a second generation antisense oligonucleotide targeting high-sensitivity C-reactive protein (hs-CRP) in rheumatoid arthritis.* Arthritis Res Ther 2015. DOI 10.1186/s13075-015-0578-5, PMID 25885521, **PMC4415222, OA** | **Matches NCT01414101 (n = 51)** | Phase II, double-blind, placebo-controlled, ISIS 329993 (ISIS-CRPRx) 100/200/400 mg SC, 3 active : 1 placebo. Dose-dependent hs-CRP reduction (−19.5 / −56.6 / −76.7% vs −14.4% placebo at Day 36). *"no serious infections and no elevations in liver function tests, lipids, creatinine or other lab abnormalities related to ISIS-CRPRx"* |
| **Jones NR, Pegues MA, McCrory MA, … Baker BF, Norris DA, Crooke RM, Graham MJ, Szalai AJ.** *A Selective Inhibitor of Human C-reactive Protein Translation Is Efficacious In Vitro and in C-reactive Protein Transgenic Mice and Humans.* Mol Ther Nucleic Acids 2012;1:e52. DOI 10.1038/mtna.2012.44, PMID 23629027, **PMC3511672, OA, hasSuppl = Y** | **`ISIS 329993-CS1`**, a Phase 1 first-in-human study | Verbatim: *"A phase I double-blind, placebo-controlled, dose escalation, first in human clinical study (ISIS 329993-CS1) … administered to healthy volunteers has been completed"*; *"The treatment with ISIS 329993 was well tolerated across the full dose range and with multiple doses; no serious adverse events occurred"* |

**A conflict I checked and can rule out.** Jones 2012's abstract states an anti-CRP ASO was "well
tolerated" in healthy volunteers, which on its face contradicts the ISIS 353512 account. Reading the
full text resolves it: that statement is about **ISIS 329993**, the successor (45 mentions), not
ISIS 353512 (7 mentions, as comparator). **There is no contradiction with Burel.** Recording the
check because the apparent conflict would otherwise sit unexamined.

### 3.2 Leads opened

- **`ISIS 329993-CS1` is a Phase 1 first-in-human study distinct from the two Phase 2 records
  I previously registered** (NCT01414101, NCT01710852). Its registry identifier has not been
  resolved. The org-study-ID convention mirrors `ISIS 353512 CS1` = NCT00734240.
- Jones 2012 has **supplementary materials** (`hasSuppl = Y`) which the text says contain the
  tolerability detail (*"see Supplementary Materials and Methods"*). Not retrieved this round.
- Further Ionis identifiers surfaced in Jones 2012 and are catalog-relevant: **ISIS 353491,
  ISIS 141923** (control ASO), **ISIS 329992, ISIS 301012** (mipomersen).
- A sourced human clinical **negative** now exists: Warren 2015's safety statement, with a stated
  denominator (n = 51, 3:1) and defined monitoring. Sourced negatives of this kind are scarce
  across the project and this one should not be discarded — but it is a negative for
  **ISIS 329993**, never transferable to ISIS 353512.

### 3.3 Intent separation, as requested

The three classes stay separate and must not be summed into a toxicity headline:

| Class | Count | Note |
|---|---:|---|
| **Unintended inflammation** in humans | **1 trial** (NCT00734240) | no primary publication; not endpoint-evaluable |
| **Secondary immune endpoints**, therapeutic ASO | 3 trials (NCT00048321, NCT01414101, NCT01710852) + the unresolved `ISIS 329993-CS1` | Warren 2015 publishes one of them |
| **Intended immunostimulation** (TLR9 agonist) | 60 trials, CpG 7909 / PF-3512676 / agatolimod | designed pharmacology, **not** toxicity |

I accept Beebop's correction without reservation: these are **trials of catalog-associated
compounds**, not 64 validated toxicity trials. The endpoint-qualified verified distinct human trial
total for immunotoxicity remains **unknown**, and on present evidence the count of trials with a
*sourced* immunotoxicity outcome is **0**.

---

## 4. Proposal 5 — source identity, resolved by identifier

### 4.1 Goodchild / Peacock — the phantom is confirmed phantom

| | |
|---|---|
| True source | **Goodchild A, Nopper N, King A, Doan T, Tanudji M, Arndt GM, Poidinger M, Rivory LP, Passioura T.** *Sequence determinants of innate immune activation by short interfering RNAs.* BMC Immunology 2009. DOI 10.1186/1471-2172-10-40, PMID **19630977**, PMCID **PMC2724479** |
| Drive filename | `Peacock2009_fulltext.pdf` — **wrong** |
| Does a Peacock 2009 BMC Immunology paper exist? | **No.** A targeted Europe PMC query (`AUTH:"Peacock" AND JOURNAL:"BMC Immunology" AND PUB_YEAR:2009`) returns **hitCount = 0** |

So `Peacock_2009_BMC` is not a mis-citation of a real paper — there is no such paper. The key and the
Drive filename should both resolve to Goodchild 2009. No "Peacock" appears in the author list.
*(Correction to my own earlier note: the PMCID is PMC2724479, not PMC2731760 as I first supposed.)*

### 4.2 Hornung / Herzner — both confirmed, and the gap is real

| | |
|---|---|
| The file named `Hornung 2005.pdf` actually contains | **Herzner AM, Hagmann CA, Goldeck M, Wolter S, Kübler K, Wittmann S, Gramberg T, Andreeva L, …** *Sequence-specific activation of the DNA sensor cGAS by Y-form DNA structures as found in primary HIV-1 cDNA.* Nature Immunology 2015. DOI 10.1038/ni.3267, PMID **26343537**, PMCID PMC4669199, **OA = N** |
| The intended source, confirmed to exist | **Hornung V, Guenthner-Biller M, Bourquin C, Ablasser A, Schlee M, Uematsu S, Noronha A, Manoharan M, …** *Sequence-specific potent induction of IFN-alpha by short interfering RNA in plasmacytoid dendritic cells through TLR7.* Nature Medicine 2005. DOI **10.1038/nm1191**, PMID **15723075**, **no PMCID, OA = N** |

`Citation_QC` is correct that the file is Herzner. Hornung 2005 is genuinely **absent** from the
corpus and is **paywalled with no open route found** — see §5.

### 4.3 Alharbi — one study, but I resolved the wrong paper on 2026-10-01

Taking the request's instruction literally first: **Alharbi 2026 and its preprint are one study.**
Nature Immunology 27:762–775 (2026), DOI 10.1038/s41590-026-02429-2, PMID 41667621, PMCID
**PMC13043311, OA = Y** ≡ bioRxiv `2024.07.25.605091`. One study, counted once.

**But my 2026-10-01 reply claimed this closed the OPEN `Alharbi_2026` citation gate, and that claim
is now doubtful.** There are **two** relevant Alharbi papers:

| | |
|---|---|
| **Alharbi AS et al.** *Rational design of antisense oligonucleotides modulating the activity of TLR7/8 agonists.* **Nucleic Acids Research 2020**, DOI 10.1093/nar/gkaa523, PMID **32544249**, PMCID **PMC7367172, OA = Y** | ASOs designed to modulate TLR7/8 agonist activity |
| **Alharbi AS et al.** *2'-O-Methyl-guanosine RNA fragments antagonize TLR7 and TLR8 to limit autoimmunity.* **Nature Immunology 2026**, PMID 41667621 | host rRNA fragments as natural TLR7/8 antagonists |

Three facts favour **NAR 2020** as the intended source for the affected rows:

1. **Alharbi AS is a co-author of Valentin 2021** (`Valentin R, Wong C, Alharbi AS, …`), the paper
   whose 2'OMe-gapmer rows carry the unresolved citation.
2. **Valentin 2021's own Supplementary Table S2 caption cites it**: *"R848 (TLR7/8 – Alharbi et al.,
   Nucleic Acids Res. 2020)"*.
3. NAR 2020 is about **designed ASOs modulating TLR7/8** — far closer to a 2'OMe-gapmer
   immunomodulation row than the 2026 paper's host-rRNA autoimmunity mechanism.

**Recommendation: German decides which paper the affected rows cite; NAR 2020 is the likelier
intended source, and a year transposition (2020 → "2026") is a plausible origin of the wrong PMID.**
I withdraw the claim that the gate is closed. It is now *resolvable* — both candidates are identified
and both are open access — but choosing between them is a scientific adjudication, not a lookup.

### 4.4 Burel is a three-way deduplication case, not two-way

| Version | Identifier |
|---|---|
| Journal | DOI 10.1089/nat.2022.0033, PMID 35976085 |
| Preprint 1 | bioRxiv **10.1101/2021.10.30.466173** — same title |
| Preprint 2 | bioRxiv **10.1101/2021.12.12.472280** — *"Mechanism Driven Early Stage Identification and Avoidance of Antisense Oligonucleotides Causing TLR9 Mediated Inflammation"* |

My 2026-10-01 reply recorded Burel as a two-way preprint/journal pair. There are **two** preprints.
Whether preprint 2 is the same study or a companion needs inspection before the extension-counting
convention is applied; it must not be assumed to collapse.

---

## 5. Access requests — the precise remaining files

Classified per `RESEARCH_ACCESS_REGISTER.md`. **No price, subscription or entitlement was verified,
so all cost fields read unverified.** No purchases, credentials or author contact.

| Required file | Source | Affected records | Access finding | Status | Priority |
|---|---|---|---|---|---|
| **Burel 2022 Supplementary Table S1** (ODN sequences) | Nucleic Acid Ther, DOI 10.1089/nat.2022.0033, PMID 35976085 | The corpus's clinical anchor, which has **0 sequence rows**; ISIS 353512 / 104838 / 330012 identity | Europe PMC: no PMCID, `isOpenAccess = N`, `hasSuppl = N`. No open route found via that endpoint. Publisher page not opened; **paywall not confirmed by observation** | **Login or technical route unestablished — not a confirmed paywall** | **High** |
| **Hornung et al. 2005 full text** | Nat Med, DOI 10.1038/nm1191, PMID 15723075 | Fills the P08 slot, which currently holds Herzner 2015 | No PMCID, `OA = N`. No open repository route found in this round | **Confirmed no open route via Europe PMC; publisher paywall unverified** | Medium |
| **Primary publication of NCT00734240** | — | The single unintended-inflammation anchor | **Does not appear to exist.** 9 `"ISIS 353512"` records, none a trial report | **Unresolved citation — publication may not exist** | **High** |
| **Registry identifier for `ISIS 329993-CS1`** | Named in Jones 2012 | Would add a verified Phase 1 to the register | Not resolved; not among NCT01414101 / NCT01710852 | **Unresolved citation** | Medium |
| **Jones 2012 Supplementary Materials and Methods** | PMC3511672 | Tolerability detail for ISIS 329993-CS1 | `hasSuppl = Y`, open access — **retrievable, simply not fetched this round** | **Supplement pending; free route confirmed** | Medium |
| **Alharbi 2026 sequence tables** | PMC13043311 | Antagonist construct identity | 19 files acquired; sequences are in the PDF supplements, not extracted | **Acquired; extraction pending** | Low |
| Goodchild 207-of-246 screened-subset mapping | PMC2724479 main text figures | Which of the 246 acquired sequences were screened | Article is open access; mapping requires reading the figures | **Free route confirmed; work pending** | **High** |

**Nothing in this table requires a purchase.** The one item I would ask Oscar for directly is
**Burel 2022 Supplementary Table S1**, because the corpus's clinical anchor has no sequence rows and
no open route to its sequences was found.

---

## 6. What this changes, and what it does not

**Acquired this round:** 246 guide strands with 243 duplex partners (Goodchild); 127 constructs with
per-position 2'OMe and PS maps, including the confirmed 80-ASO screen with four receptor readouts
(Valentin); ~39 oligo-linked numeric outcomes with SD and n = 3 (Yoshida); 19 files of per-figure
source data (Alharbi). Against a catalog of 142 records in which **1 identifier joins an outcome and
that outcome is qualitative**, this is a material change in what the module could qualify.

**It does not change any count in the dataset.** Nothing was ingested, no label was assigned, no
adjudication was touched. Acquisition is not qualification: the Goodchild rows have no chemistry and
no outcomes, the Valentin outcomes are normalised to controls, and the Yoshida outcomes are reporter
percentages from a cell line. Every one needs German's adjudication before it is evidence.

**Requires Oscar's implementation approval:** ingesting any of the above; adding the schema fields
needed to hold per-position chemistry, duplex partners, replicate counts and normalisation basis.

**Requires German's scientific adjudication:** which Alharbi paper the affected rows cite (§4.3);
whether Burel preprint 2 is the same study (§4.4); whether reporter-cell percentages may sit
alongside PBMC data; and the four reporter-cell negatives flagged in Addendum A §A2, which remain
the highest-severity open item in this endpoint.

**Not started:** proposals 1, 2 and 6, and the 20-source coverage log.

---

# Revision A — 2026-10-03

Oscar authorized proposals **1, 2 and 6** after the sections above were published. This revision
adds them without altering anything above. Research only; nothing ingested, no label or adjudication
touched. **Three corrections to my own earlier statements are recorded below, two of them to claims I
made twice.**

## A. Proposal 1 — experiment-level reconstruction

### A.1 Correction: the 6 supplement holds are Fucini 2012, not Goodchild and Valentin

My 2026-10-01 reply (§P3) and Addendum A both stated that the 6 `HOLD_SUPPLEMENT` records gate
Goodchild's 207-siRNA table and Valentin's 80-ASO matrix. **That is wrong.** All six are Fucini 2012:

| Record | Paper | Oligo | `Remaining Action` (verbatim, truncated) |
|---|---|---|---|
| P06_001–006 | **P06 Fucini 2012** | β-gal 728 guide / passenger, β-gal control guide / passenger, ApoB guide / passenger | *"Retrieve Supplementary Table S1 and create one experiment-level row pe…"* |

Goodchild (P14) and Valentin (P19) contribute **zero catalog records**, so last round's acquisitions
add new sequences but **release no held record**. The retrieval that actually unblocks held records is
**Fucini 2012 Supplementary Table S1**, and it is blocked — see §B.

### A.2 Composition of the reconstruction targets, measured

| Adjudication | n | Papers | With `Modification Positions` |
|---|---:|---|---|
| APPROVED_CORE_HUMAN | 23 | P15 Riera-Tur 17, P09 Jung 4, P18 Sioud 2 | **21 / 23** (P15 17/17, P09 4/4, P18 0/2) |
| APPROVED_PATHWAY_CONTROL | 26 | P05 Forsbach 12, P02 Coch 7, P20 Vollmer 4, P07 Heil 3 | **0 / 26** |
| APPROVED_AUXILIARY | 5 | P10 Kandimalla 5 | **0 / 5** |
| HOLD_OUTCOME_EXTRACTION | 42 | P18 Sioud 30, P05 Forsbach 11, P02 Coch 1 | **0 / 42** |
| HOLD_SUPPLEMENT | 6 | P06 Fucini 6 | **0 / 6** |

So positional chemistry exists for **21 of the 54 approved records**, all from Riera-Tur and Jung.

### A.3 All 42 outcome-extraction holds are figure-bound

Grouping the holds by their own `Remaining Action` text:

- **30** — *"Extract/digitize Figure 1 TNF-α and IL-6 values or source-defined qualitative result…"* (Sioud 2005)
- **11** — *"Extract Figure 1/2 motif-series outcomes and exact assay condition."* (Forsbach 2008)
- **1** — *"Extract exact strand-specific response from source figures or keep as identity-only sequence."* (Coch 2013)

**42 of 42 require figure digitization. None can be reconstructed from text or tables.**

### A.4 Modified disposition on proposal 1

**MODIFIED, with a recommendation against its stated priority.** The proposal places highest value on
reconstructing the approved human records and the 42 holds. The evidence argues otherwise: all 42
holds need digitization, and 0 of 42 carry positional chemistry, so each reconstructed row would be a
derived figure value attached to a construct of unverified chemistry — carrying two uncertainties
into the primary training view. Per the validation memo, such values must be marked derived with
method and uncertainty, and verified against representative figure points.

By contrast **Yoshida 2024 Supplementary Table S1, already acquired, supplies ~39 oligo-linked
numeric outcomes with mean, SD and n = 3 from a table**, needing no digitization, against constructs
whose modification positions are stated in the paper's own figures. I recommend that as the first
experiment-level package, with the 42 holds second and explicitly flagged as derived.

The reconstruction schema itself (compound–strand–chemistry–dose–donor–assay–timepoint → separate
numerical cytokine and receptor outcomes) is **accepted unchanged**; it is the right unit. German's
existing decisions are preserved — nothing above changes an adjudication.

## B. Proposal 2 — remaining acquisition, and a hard barrier

**Fucini 2012 (10.1089/nat.2011.0334, PMID 22519815, PMCID PMC4047996).** Europe PMC lists
`hasSuppl = Y` but the supplement request returns, verbatim:

> `<errMsg>Article with id PMC4047996 is not open access one</errMsg>`

and `PMC4047996/fullTextXML` returns HTTP 500. Both attempts were made on 2026-10-03.

**Barrier classification: in PMC but outside the open-access subset.** This is *not* a confirmed
publisher paywall and *not* a login gate — it is a reuse-licence restriction on a deposited
manuscript. The PMC article page may still be human-readable; it is not machine-harvestable by the
open route. **This is the single highest-value remaining file, because it is the only one that
releases already-held records (6).** Requested from Oscar in §5 terms.

Still outstanding from proposal 2: the **Goodchild 207-of-246 screened-subset mapping**, which needs
the open-access article's figures read, not a new file.

## C. Proposal 6 — cross-paper family overlap

### C.1 Correction: I overstated leakage, twice, and Beebop's challenge is upheld

Measured over all 142 catalog records on normalized sequence (non-alphabetic stripped, U→T):

| Measure | Value |
|---|---:|
| Duplicate-sequence clusters (>1 record) | 12, covering 48 records |
| …of those, spanning **more than one paper** | **1**, covering **7 records** |
| Records in a cross-paper exact cluster | **7 / 142** |
| Cross-paper near-neighbour pairs (≥12 nt shared, not exact) | **2**, involving **3 records** |
| Distinct paper pairs linked by sequence similarity | **1** (P05 Forsbach ↔ P07 Heil, 18 nt and 12 nt) |

**Eleven of the twelve duplicate clusters are within a single paper.** A correctly implemented
leave-one-paper-out split therefore holds them on one side of the fold, exactly as the request
states. My 2026-10-01 reply claimed within-paper families defeat LOPO (withdrawn in Addendum A), and
Addendum A then claimed cross-paper overlap was large, citing 23 of 54 approved rows. **That second
claim is also wrong**: the 23 figure counts approved records sharing a sequence with any other
approved record, which is predominantly within-paper. The honest cross-paper magnitude is **~10 of
142 records**. LOPO is largely intact and I withdraw the stronger framing.

### C.2 The one cross-paper cluster is an identity defect, not a split defect

`TCGTCGTTTTGTCGTTTTGTCGTT` (24 nt) — 7 records across three papers, **5 of them `APPROVED_CORE_HUMAN`**:

| Record | Paper | Oligo name | Adjudication | Direction |
|---|---|---|---|---|
| P02_001 | Coch 2013 | CpG 2006 | APPROVED_PATHWAY_CONTROL | Agonist/response-positive |
| P15_026 | Riera-Tur 2024 | ODN2006 | APPROVED_CORE_HUMAN | Control/unknown |
| P15_027 | Riera-Tur 2024 | **ODN2006mCflanks** | APPROVED_CORE_HUMAN | Agonist/response-positive |
| P15_028 | Riera-Tur 2024 | **ODN2006LNA** | APPROVED_CORE_HUMAN | Unknown |
| P15_029 | Riera-Tur 2024 | **ODN2006fmC** | APPROVED_CORE_HUMAN | Agonist/response-positive |
| P15_030 | Riera-Tur 2024 | **ODN2006fmCLNA** | APPROVED_CORE_HUMAN | Inert/low-response |
| P20_001 | Vollmer 2004 | ODN2006 | APPROVED_PATHWAY_CONTROL | Agonist/response-positive |

Four different direction labels sit on one normalized string. **That divergence is correct biology** —
methylation and LNA context changing TLR9 activation is Riera-Tur's central finding. The defect is
that normalization **erases the chemistry that explains the divergence**: five chemically distinct
variants collapse to the parent's string. A model keyed on normalized sequence cannot learn the
effect; a leakage check keyed on normalized sequence would wrongly merge them and discard real
signal.

This is the same failure the sweep found at P10_001/P10_002 (`*G1` vs `*G2` erased by
normalization). It is an **identity and feature-representation defect**, and it reaches
`APPROVED_CORE_HUMAN` rows. Recommend the leakage grouping key be the **chemistry-resolved**
construct, not the normalized base sequence, and that `Normalized Sequence` be marked explicitly as
a search aid that is not an identity.

### C.3 Alharbi as one study — restated

Nature Immunology 27:762–775 (2026), PMID 41667621, PMCID PMC13043311 ≡ bioRxiv 2024.07.25.605091 —
**one study, counted once**. The unresolved question is which Alharbi paper the affected rows cite
(§4.3 above: NAR 2020, PMID 32544249, remains the likelier intended source). That is German's call.

## D. Twenty-source coverage log

Queried 2026-10-03. **Blocked services are not marked searched.**

| # | Source | Query | Outcome | Hits | Barrier |
|---:|---|---|---|---:|---|
| 1 | PubMed | `antisense oligonucleotide TLR9 inflammatory human` | searched | 12 | — |
| 2 | Europe PMC | `oligonucleotide immunostimulation TLR9 cytokine human PBMC` | searched | 59 | — |
| 3 | OpenAlex | same | **BLOCKED** | — | HTTP 429 after 4 attempts; verbatim *"Insufficient budget. This request has no API key"* — quota/key, not a paywall |
| 4 | Semantic Scholar | same | **BLOCKED** | — | HTTP 429, unauthenticated tier |
| 5 | ResearchRabbit | same | **NOT SEARCHED** | — | site reachable (52 kB); no public search API, interactive account required |
| 6 | Undermind | same | **NOT SEARCHED** | — | reachable (105 kB); no public API |
| 7 | Elicit | same | **NOT SEARCHED** | — | reachable (2.6 MB); no public API |
| 8 | Consensus | same | **NOT SEARCHED** | — | reachable (28 kB); no public API |
| 9 | GEO | `oligonucleotide AND (TLR9 OR immunostimulation)` | searched | 667 | counts unreliable, see D.1 |
| 10 | SRA | same | searched | 2 | — |
| 11 | PRIDE | `oligonucleotide` | searched (page 0) | 5 returned | endpoint does not expose a total |
| 12 | ProteomeXchange | `oligonucleotide` | searched | **0** | no endpoint-relevant datasets |
| 13 | BioStudies | `oligonucleotide TLR9` | searched | 16,306 | keyword match, not leads — see D.1 |
| 14 | ArrayExpress (BioStudies) | `oligonucleotide TLR9` | searched | 1,005 | as above |
| 15 | ClinicalTrials.gov | `antisense oligonucleotide inflammation` | searched | 15 | — |
| 16 | Comparative Toxicogenomics DB | `chem=oligodeoxynucleotide; report=genes_curated` | **BLOCKED** | — | HTTP 302 redirect loop even following redirects |
| 17 | ICE (NICEATM) | `oligonucleotide` | **NOT SEARCHED** | — | reachable; access is interactive UI / bulk download, no documented public query API found |
| 18 | ToxCast / CompTox (CTX API) | chemical search `oligonucleotide` | **BLOCKED** | — | requires an `x-api-key` |
| 19 | Zenodo | `oligonucleotide TLR9` | searched | 604 | keyword match, see D.1 |
| 20 | Dryad | `oligonucleotide TLR9` | searched | **0** | — |

**Tally: 11 of 20 genuinely searched, 4 blocked, 5 have no public query API.** No subscription was
purchased or assumed; no credential was requested. Per the request, a search-product subscription
would not unlock publisher content and none was sought.

### D.1 The archive hit counts are tokenizer artefacts, not leads — verified

A targeted construct-alias pass (ISIS 353512, CPG 7909, PF-3512676, ODN2006, SECA141, SY-ODN18,
ISIS 104838, agatolimod) across GEO, SRA, BioStudies, Zenodo and PubMed appeared to return deposit
hits. **I spot-checked them and they are false positives.** GEO's query translation for
`"SY-ODN18"` is `SY[All Fields]` — 1,250 hits, whose top records are *Drosophila* midgut single-cell
RNA-seq, an E. coli phage sRNA study and HS-SY-II synovial sarcoma cells. `"ISIS 353512"` translates
to `ISIS[All Fields]` — 19 hits, top records on iPSC trophoblast differentiation and
monoacylglycerol acyltransferase 1.

**Phrase search is not honoured by these endpoints, so no deposit was confirmed endpoint-relevant,
and no raw hit count in the table above should be read as an opportunity.** Unknown is not zero: a
relevant deposit may exist and would need either exact-accession search from each priority paper's
data-availability statement, or interactive search. That work is not done.

## E. Open questions

For **German** (scientific adjudication):

1. **The ODN2006 series (§C.2).** Should the five chemistry variants keep one normalized sequence,
   and may `ODN2006fmCLNA` stand as `Inert/low-response` while its parent is `Agonist`? Related:
   P10_001/P10_002 (`*G1` vs `*G2`) collapse the same way.
2. **The four reporter-cell negatives** (Addendum A §A2: P15_031, P15_032, P15_035, P15_036) remain
   the highest-severity open item in this endpoint, unchanged by this round.
3. **Which Alharbi paper** the affected rows cite — NAR 2020 or Nature Immunology 2026 (§4.3).
4. **Digitized figure values**: acceptable for primary training rows at all, given that 0 of the 42
   holds carry positional chemistry?
5. **Reporter-line percentages** (Yoshida, normalized to SY-ODN18 = 100): may they sit in the same
   outcome field as PBMC cytokine measurements, or do they need a separate normalization-basis field?

For **Oscar** (implementation and scope):

6. **Fucini 2012 Supplementary Table S1** — the only file that releases held records; no open route.
7. Whether to attempt the 9 unsearched or blocked sources via routes this environment lacks
   (API keys for OpenAlex / Semantic Scholar / ToxCast; interactive accounts for ResearchRabbit,
   Undermind, Elicit, Consensus, ICE).
8. Whether to spend effort on exact-accession archive searches from each priority paper's
   data-availability statement, given that the keyword pass produced nothing usable.

---

**REVISION A COMPLETE — PROPOSALS 1, 2, 6 AND THE TWENTY-SOURCE LOG REPORTED; THREE SELF-CORRECTIONS RECORDED; AWAITING GERMAN'S ADJUDICATION AND OSCAR'S IMPLEMENTATION AUTHORIZATION**
