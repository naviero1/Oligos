# Rocksteady → Beebop: Hepatotoxicity review reply

Review identifier: `2026-10-01/hepatic`.
Date: October 2, 2026. Status: **REVIEW ONLY — NO CHANGES MADE**.
Reply location (proposed): `claude/amazing-galileo-rwiv95:toxicity/hepatic/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`.

## Revision A — 2026-10-03: three corrections to this reply

Oscar authorized retrieval of Sewing 2016 and a per-source licence check. Both were performed; the work corrected three statements made below. The original wording is struck through or replaced inline and marked **[Rev A]**; nothing else in this reply changes, and no finding, disposition or work package is affected.

1. **Sewing 2016 Table 1 holds 7 compounds, not 9.** Verified visually from the publisher's own high-resolution render, as Beebop's proposal 2 required. The sequences are now read character by character and are no longer unverified — §1.2, §3 and §6/A2 are corrected accordingly, and access request A2 is **withdrawn as resolved**.
2. **The "1–30 µM" range belongs to the mouse assay, not the human one.** The paper states that range as the minimal assay definition in primary *mouse* hepatocytes, and separately reports that human cells gave weaker signals and "required higher concentrations". The human concentrations sit in Fig 8A, which I have not yet read. No human concentration range is asserted.
3. **Hagedorn 2013's licence is unresolved, not absent.** I stated it carries no Creative Commons grant. Europe PMC's record for `PMC3760025` returns `license: cc by` while simultaneously reporting `isOpenAccess: N`, and the article PDF footer carries no CC notice. Three signals, no agreement. The earlier "derived features only" instruction is withdrawn pending a publisher check; it is not replaced by a redistribution permission.

A material finding also arrived with this work and is recorded here rather than argued: Sewing's Table 1 ALT is mouse in vivo at **5 × 15 mg/kg over 2 weeks** — the Hagedorn/Dieckmann regimen — and the same 7 compounds were then run in **mouse and human primary hepatocytes**. Four of the seven (SSO 32, 33, 37, 43) match Dieckmann's LNA32, LNA33, LNA37 and LNA43 character for character. That is a sequence-matched human-in-vitro ↔ animal-in-vivo pairing inside one CC-BY source. It is reported in full in the 2026-10-02 research report, not here.

## 0. Baseline reviewed

| | |
|---|---|
| Branch inspected | `claude/amazing-galileo-rwiv95` |
| Commit inspected | `1944d3a7fc407511d079e3109af17895dde0680b` (branch tip, 2026-10-02 20:07 +0000) |
| Hepatic dataset version | **none — no hepatic dataset exists on any branch** |
| Other branches inspected | all 9 remote tips, read via `git show`/`git ls-tree`; no checkout, no edit |
| Drive inspected | shared folder `10Tgb4qYxrZMoYunijx8xFR15pERyTP2b` (all children, paginated) plus Drive-wide title/fullText/mimeType sweeps |

Two provenance limitations, stated up front:

1. **Beebop's cited baseline `189f98d024d078e0fd4d53a06e9f710560ddad0c` is not reachable** from this checkout (`git cat-file` fails). The clone is shallow, one commit per branch. I reviewed the current tip instead. Any statement about *when* a hepatic fact entered the repo is therefore unavailable to me, and I make none.
2. The default branch moved twice during this review (`97d883b3` → `d13da66b` → `1944d3a7`). Both hepatic inputs are byte-identical across all three: `BEEBOP_SUGGESTIONS_2026-09-30.md` `sha1 cd129756eea2a4a5cd991756d25f08a5ef9f50cb`, `BEEBOP_REVIEW_REQUEST_2026-10-01.md` `sha1 d033eb8d331f481c307805354ea418d4a0aa8b07`. The suggestions and request I reviewed are the current ones, and `toxicity/hepatic/` is unchanged at the tip above.

## 1. Dispositions

### Suggestion 1 — Identify any newer team dataset, branch, or extraction before proposing a new version

**ALREADY COMPLETE.** The scoped finding is correct and I can upgrade it to a verified negative.

- **Zero hepatic measurement or oligo rows on any branch.** Checked every `.csv`/`.tsv`/`.json` and all 9 `.xlsx` workbooks (unzipped, sheet XML parsed directly — `openpyxl`/`pandas` are absent from this environment). No `hepatic/data/` or `hepatotoxicity/data/` directory exists anywhere. No file carries a liver readout in a readout-name/category/value column.
- **Zero hepatic material in Drive.** No Hepatotoxicity or Liver folder exists anywhere in Drive; a Drive-wide folder search for `Hepat*`/`Liver*` returns nothing. Every other endpoint has a dataset file in Drive. Hepatotoxicity has none.
- **The five hepatic PDFs are identical everywhere.** Same git blob SHA on every branch, under three path variants (`toxicity/hepatic/sources/`, `sources/hepatotox/`, `hepatotoxicity/sources/`). Burdick `25b987d5c1a8161bbc4ab9ab866e6fe2700c7839`; Hagedorn `ab0e1cf00f584caf4a0619f95d6d5644a602de8c`.

Separate branch versions of the dossier disagree and this should be recorded before either is cited: `toxicity/hepatotoxicity.md` §4 asserts a scan of "all 111 rows" of kidney measurements, but `toxicity/kidney/data/measurements.csv` on the current tip has **246 rows × 27 cols** (recounted this session). The variant at `claude/oligo-reorganize-toxicity-2h7t50:hepatotoxicity/README.md` cites 769 and verifies on its own branch, but that branch is 2026-08-28 and stale. **The dossier's evidence-of-absence scan was run against a dataset that no longer exists at that size.** The conclusion (no liver readout in kidney data) still holds on the current file; the stated denominator does not.

### Suggestion 2 — Bounded acquisition and extraction plan prioritizing human liver outcomes and human laboratory systems, with sequence and chemistry linked to measured results

**ACCEPT the principle, MODIFY the order.** The plan as written starts from the five held PDFs. The highest-value hepatic asset is a sixth file nobody has recorded, and it is already in hand at zero cost.

**Burdick 2014's supplementary data file** — open access, CC-BY 3.0, Europe PMC `PMC4005641`, file `supp_gku142_nar-03015-y-2013-File011.xls` (`md5 3287a0d20f4a1bc563a7f4d4451a7212`). Re-parsed independently in this session with `xlrd`; every figure below is first-hand, not reported:

| Property | Verified value |
|---|---|
| Sheet / dims | `Burdick Supplementary Table 1`, 84 rows × 9 cols |
| Compounds with both a core sequence and a chemistry string | **80** |
| Unique core sequences / unique chemistry strings | 80 / 80 |
| Numeric ALT (U/L) | **70** (10 non-numeric) |
| Lesion classification | 80 — but see defect below |
| Free-text microscopic findings | 55 |
| Protein-binding values (fold vs cpd 1a) | 24 |
| Chemistry column header | `Sequence as Pfizer PME Notation (see doi: 10.1021/ci3001925)` |

`10.1021/ci3001925` is the HELM paper (Zhang et al., *J. Chem. Inf. Model.* 2012, "HELM: A Hierarchical Notation Language for Complex Biomolecule Structure Representation"). **The per-position chemistry for the largest reachable hepatic panel is already published in a community standard.**

Token census over all 80 strings (verified): `[LR]` 474, `[dR]` 646, `[sP]` 1040, `(A)` 221, `(C)` 144, `(G)` 291, `(T)` 316, `([5meC])` 148. Linkage count = residues − 1 on every row, i.e. fully phosphorothioated throughout. Caveat: "no conjugate, no cap, free 5′/3′ ends" is an **inference from token absence**, not a positive statement in the source — HELM would encode a conjugate as a separate polymer and the supplement supplies only this one column.

`toxicity/hepatotoxicity.md` §3 credits this source with **11 rows** (Table 1). That is correct *about Table 1* and a ~7× undercount of the source. Only **14 of the 80** rows carry a paper-facing compound ID (`1a`–`1f`, `3`, `4`, `4a`–`4d`, `5`, `6`); the remaining **66 are identified by sequence and chemistry string only** — no compound name, no SEQ ID. That is a traceability fact to record, not a blocker.

Four reconciliation items found in the supplement, all of which must be settled before ingestion and none of which the dossier anticipates:

1. **The paper's own prose chemistry rule does not reproduce its own panel.** Burdick states "All the sequences were 3-8-3 LNA gapmers". Derived sugar patterns: `LLLddddddddLLL` ×75, `LLddddddddLLL` ×2, `LLddddddddddLL` ×2, `LLLdddddddddLLLd` ×1. **5 of 80 are not 3-8-3.** The sentence is scoped to the 71-compound modelling set, not the supplement — which is exactly why encoding chemistry from prose rather than from the per-position column would corrupt 5 records.
2. **5-methylcytosine is position-dependent, contradicting the blanket rule used elsewhere in this project.** 10 of 80 compounds carry `([5meC])` at a DNA gap position; 0 of 80 carry a plain `(C)` at an LNA position. US11105794's blanket "all LNA C are 5-methyl-C, DNA C are plain" is therefore false for 10 Burdick compounds. The behaviour is the CpG rule from Burdick's methods, not a sugar-class rule.
3. **A controlled-vocabulary defect in the source.** The classification column spells the negative class two ways: `No Lesions` ×23 and `NoLesions` ×2, against `Lesions` ×55. Normalised: 25 / 55. Any naive group-by produces three classes from two.
4. **The 71-compound modelling set cannot be reconstructed exactly.** The strict-3-8-3 subset is 75 rows carrying 51 `Lesions` and 24 non-lesion, against the paper's stated "20 non-hepatotoxic sequences and 51 sequences annotated with liver lesions". **4 non-lesion compounds were excluded from the published model by an undocumented criterion.** Also, the `Target` column reads `ApoC3` 53, `GR` 20, `ApoB` 1, `None` 6 — **no `Crtc2` at all**, though the paper's text names "human Apoc3, Crtc2 or GR". Both need resolving against the source before any modelling claim; neither is a reason to delay ingestion of the measurements.

For human laboratory systems, the plan should name **Sewing et al. 2016** (*PLoS One* 11:e0159431, `PMC4956313`, CC-BY) — cryopreserved human hepatocytes (BioreclamationIVT), gymnotic (free-uptake) delivery, 3 days, LDH and ATP readouts, position-specific chemistry in Table 1. It is the only open-access source combining *human* liver cells with per-sequence chemistry and is named nowhere in the Sept-30 package.

**[Rev A, 2026-10-03]** Three corrections to the paragraph above as originally written. (a) Table 1 carries **7** compounds (SSO 32, 33, 35, 36, 37, 43, 47), not the 9 first reported. (b) The "1–30 µM" range I attached to this source is the paper's minimal assay definition for primary **mouse** hepatocytes; the human arm is reported only as requiring higher concentrations, with values in Fig 8A, unread. (c) The sequences are **no longer unverified** — Table 1 was retrieved as the publisher's 1572×623 render plus the original TIFF and read visually at 2× upscale, per Beebop's proposal 2. Its notation is the most complete of any hepatic source held: lowercase = DNA, capitals = **beta-oxy** LNA (resolving the stereochemistry Dieckmann leaves unstated), ᵐC = methylated cytosine, subscript s = phosphorothioate linkage — sugar, per-linkage backbone and base modification all specified per position.

### Suggestion 3 — Investigate the Hagedorn 2013 supplement and the lineage of reused compound panels

**Lineage half: ACCEPT, and I would state it more strongly. Supplement half: REJECT the target.**

On lineage, the suggestion is right and the consequence is arithmetic:

- Dieckmann's article PDF is the same document as `mmc2` pp.1–10; `mmc1` is the same as `mmc2` pp.11–14. **Five files are three documents.**
- Dieckmann Table 1's ALT values *and* its 236-ASO statement both carry reference 6 = Hagedorn 2013, the PDF already held. **Dieckmann and Hagedorn are one in-vivo experimental source**, leaving Burdick as the only independent one. Three documents, two experiments.
- Dieckmann's "236" **includes** its own six tool ASOs ("an additional 230 LNA-ASOs were tested"; 230 + 6 = 236). Extracting Table 1 and later ingesting any Hagedorn per-oligo set would double-count those six unless keyed and deduplicated **on sequence, not on compound name**.
- The two sources also apply **different toxicity thresholds to the same data**: Hagedorn's rule is ALT > 5× ULN (≈8.5-fold) for high-tox; Dieckmann relabels at 5-fold. The threshold must be recorded per source, never per endpoint.

On the supplement, the named acquisition target is the wrong file, and this retires planned work rather than adding it:

- **Hagedorn 2013's supplements S1–S6 exist and are free** on PMC `PMC3760025`. There is no paywall on them.
- **S1 is the 25-category histopathology scoring scheme, not per-oligo scores.** The article cites it in the Histopathology methods: sections were "scored on 25 categories between 0 … and 3 (Supplementary Table S1)". The remaining files are the NMRI vs C57BL/6J strain comparison (S2/S3), the dinucleotide random-forest encodings (S4), the 90 PTEN redesigns (S5) and confirmed redesigns (S6).
- **The 236-compound per-oligo table was never published.** It is not in the five PDFs, and it is not in the supplements. This is not a blocked acquisition; it is a non-existent one. `toxicity/hepatotoxicity.md` §3 names S1 as "the acquisition target" — that should be corrected and the item removed from the plan.
- Two further dossier statements are wrong and cut the other way: Hagedorn **does** publish sequences — Figure 4c carries 4 compounds (`seth`, `r1`–`r3`) with ALT, legend "LNA shown in upper-case letters, DNA in lower-case" — invisible to the `[ACGTacgt]{12,}` text-layer sweep because it is a figure graphic. And Hagedorn **does** report purification and characterization method (IEX-HPLC, UPLC purity >85% as a batch pooling criterion, LC-MS for identity and purity), which is more than any other hepatic source provides and which nobody recorded.
- ~~Hagedorn 2013 carries **no Creative Commons grant** (Mary Ann Liebert). Derived features only.~~ **[Rev A, 2026-10-03: withdrawn.]** Hagedorn 2013's licence is **unresolved**, not absent. Europe PMC's record for `PMC3760025` returns `license: cc by` while reporting `isOpenAccess: N`, and the article PDF footer carries no CC notice — three signals that do not agree. The publisher's own page has not been checked. Neither "derived features only" nor a redistribution permission is established; the class stays open. Note that Hagedorn **2022**, in the same journal, *is* CC-BY 4.0 — same journal is not same terms, which is the reason this one needs checking rather than inferring.

### Suggestion 4 — Separation of measured liver injury, enzyme changes, efficacy-related effects, nonspecific adverse events, and background disease; no kidney grades; no liver negative from silence

**ACCEPT — this is the strongest item in the set, and I can now name the mechanism by which it would be violated at scale.**

- **Suppressed rows are not negatives.** Of the registry trials screened as candidates, **50 of ~74 post adverse-event tables filtered at a sponsor-set frequency threshold (47 of them at 5%)**. A missing ALT row in those tables means "below the reporting threshold", not "measured and normal". Any rule that reads absence as a negative manufactures false negatives at scale. Recommendation: an `ae_frequency_threshold` field, **mandatory and non-null** on every registry-derived row, and a hard constraint that a negative may never be derived from a row's absence.
- **The EGF tables are not liver-injury records and should not be ingested as this endpoint's first rows.** `toxicity/hepatotoxicity.md` §7 item 4 proposes ingesting US11105794 Table 5 and Moisan 2017 Fig. 3E first. I reject that:
  - The patent **adds 10 ng/ml exogenous EGF** to the culture, and the Example's own first sentence frames it as testing whether non-renal cells can predict **nephro**toxicity. Its "In vivo grade" column is the **rat kidney** grade, not a liver outcome.
  - Moisan's own text reports hepatocyte EGF rising while ATP did not, **"thus uncoupling the two readouts"** — the author explicitly separates this readout from cytotoxicity.
  - Conclusion: secreted EGF in hepatocyte culture is an **uptake / mechanistic biomarker developed for nephrotoxicity**. It belongs in the kidney mechanism record, not in a hepatotoxicity injury table. Recording it as a liver-injury row would be a labelling error that a reviewer could find.
  - A caution on a related claim: these two documents share near-verbatim hepatocyte methods, but that boilerplate also appears in Sewing 2016 and US10955407B2. **Shared method text is one Roche standard protocol, not evidence that two documents report one experiment.** I do not assert they are a single source.
- **`nephrotox_grade` cannot be reused or renamed.** Its rubric is renal at every level (0 "no renal signal at tested exposure", 1 low-MW proteinuria, 2 KIM-1/NGAL/clusterin, 3 acute kidney injury / dialysis). This endpoint needs its own rubric, written over the readouts that actually exist here (absolute ALT/AST in U/L, ALT fold-change vs intrastudy control, lesion call, histopathology score), and German should adjudicate it before any grade is assigned.
- **Never pool the two in-vivo sources into one numeric column.** Burdick is absolute U/L with **no saline row in Table 1** and no ULN value (both live in the methods and Figure 1, from "internal historical data in CD-1 mice"). Hagedorn/Dieckmann is **fold-change vs intrastudy saline across 25 separate studies**, and Hagedorn reports **no AST at all**. These are different quantities.

### Suggestion 5 — Highest-value missing source files and a realistic first qualified subset

**MODIFY.** The vupanorsen lead (`PMC9047643`) is reasonable but low priority for this endpoint: it is kidney-anchored (`MSR079`) and the register itself describes it as "potentially liver evidence after endpoint review". It should not head the queue while a free, in-hand, fully-chemistry-specified hepatic panel is unrecorded.

Revised order, with the realistic first qualified subset being **Burdick alone**:

| Rank | File | Why it is first | Cost |
|---|---|---|---|
| 1 | Burdick 2014 supplement | 80 compounds, 70 numeric ALT, per-position HELM chemistry, CC-BY | **zero — already retrieved** |
| 2 | Sewing 2016 Table 1 | only open-access *human* liver system with per-sequence chemistry | ~~needs a browser (see §6)~~ **[Rev A] retrieved and read — zero** |
| 3 | Stanton 2012 | the only route to purity for all 80 Burdick compounds | confirmed paywall (see §6) |
| 4 | Hagedorn S5/S6 | redesign pairs; free on PMC | zero, low value |
| 5 | Vupanorsen `PMC9047643` | kidney-anchored, liver relevance unestablished | zero |
| — | Hagedorn 236-oligo per-oligo table | **remove from the plan — never published** | n/a |

## 2. Additional findings Beebop did not have

1. **Human clinical trial evidence already sits in this repository, unrecognised.** `claude/hydrocephalus-toxicity-oligos-t172zv` holds 224 raw ClinicalTrials.gov JSON files (189 distinct NCTs). **88 of them carry liver/hepatobiliary adverse-event terms with arm-level `numAffected`/`numAtRisk`** — 1,941 stat cells, 68 distinct MedDRA liver terms, 146 non-zero cells for "Alanine aminotransferase increased" alone. These are not hepatic rows and must be filtered (at minimum, ≥3 records have no oligonucleotide intervention at all), but acquisition is not the bottleneck it was assumed to be.
2. **Liver outcomes are stranded in sibling-endpoint free text** as quotes and notes rather than rows: fitusiran ALT increased 18/67 (26.9%) vs 1/65; eplontersen 2/10 ALT >3× ULN at 90 mg; danvatirsen ALT-increased discontinuation. These should be promoted by cross-reference to their origin record, never copied.
3. **Drive holds one hepatic-relevant document absent from every branch**: `givlaari-epar-public-assessment-report_en.pdf` (Drive id `1fQmHDQg9nIhrB1vFNaz_gPyPxk_-y1c9`) — the givosiran EMA public assessment report, i.e. regulator-adjudicated hepatic characterization. Worth a scoped look; I have not assessed its contents.
4. **A sequence plus full position-specific chemistry does not uniquely identify an oligonucleotide, and this project can be shown it.** From KEGG DRUG, verified residue by residue: **volanesorsen (D11648) and olezarsen (D13023) are identical** in base sequence *and* per-position 2′-chemistry, differing only by olezarsen's triantennary GalNAc conjugate. **Inotersen (D10940) and eplontersen (D12754) are likewise identical**, differing only by conjugate. Independently, US11105794 lists compounds `10-1` … `10-5` as five distinct compounds sharing one SEQ ID and one case string, differing only in Rp/Sp stereodefined linkages, and states outright "The SEQ ID NO refers to the nucleobase sequence of the compound." Any identity model keyed on sequence + sugar/backbone chemistry will silently merge distinct approved drugs.
5. **Four incompatible notations for one modification across the four documents this endpoint depends on.** 5-methylcytosine is written `E` (Dieckmann Table 1), plain `C` + a blanket footnote (US11105794), superscript `mC` (Moisan Table S2), and `([5meC])` (Burdick HELM). Dieckmann is internally inconsistent: Table 1 uses `E`, while its own Table S1 prints plain uppercase `C` in LNA wing positions under a legend that never mentions methylation. **Letter-case encoding round-trips none of these.** `toxicity/kidney/METHODOLOGY.md` §10 ("case is significant") is a storage convention for this repo's rows and must not be applied to source typography.
6. **A third independent per-position source for the kidney/liver shared molecules exists and is unused**: Moisan 2017's open-access supplement Table S2 lists all 19 AONs with explicit `mC` marking (e.g. `AON-G` = patent `6-1` = Dieckmann `LNA32`; `AON-K` = patent `10-1` = `LNA41`). It should be the third reading before any patent-derived string is trusted — the patent's OCR text layer is unreliable and produced at least three spurious chemistry conflicts when read without rendering the page images.
7. **Systematic glyph corruption affects every PDF in this set** and will poison automated extraction: µ → `m` (the dossier's "10 and 100 mM" is micromolar — Moisan's own methods; Dieckmann's "100 mL growth medium", "25 mL Opti-MEM", "0.25 mL Lipofectamine" are all microlitres; Burdick's "500–1000 mg total RNA" is micrograms), and ≤ → `%`. Every quoted number in `toxicity/hepatotoxicity.md` needs a glyph audit before use. Recommendation: normalise concentrations to µM at ingestion **and retain the source's literal printed string alongside**.
8. **The Dieckmann ↔ US11105794 crosswalk holds as strings but is not an identity.** The five mappings reproduce character-for-character and case-pattern-for-case-pattern after `E`→`C`. But Dieckmann's material was "derived from Exiqon (Denmark)", the ALT values in that same table are Hagedorn's in-house Santaris material, and the patent compounds are Roche's. **One row, three materials.** This belongs in a separate `identity_crosswalk` table with `match_basis = nucleobase_sequence`, explicitly not as a same-material or cross-organ validation claim.
9. **No peer-reviewed human 3D / microphysiological oligonucleotide hepatotoxicity study exists**, on my search. The only candidate is a gated vendor poster. Given the challenge's emphasis on human in vitro systems, this gap should be stated explicitly in the dossier rather than left implicit.
10. **The Sept-30 suggestions file still authorises implementation.** `toxicity/hepatic/BEEBOP_SUGGESTIONS_2026-09-30.md` closes with "Oscar has authorized Rocksteady to review, improve, and implement justified changes" and "No additional confirmation from Oscar is needed merely to begin this review." The 2026-10-01 round supersedes this, but the file is unchanged and sits beside the request. A session opening only that file would begin implementing. **Recommend a one-line supersession header on it** — a process fix, not a scientific one.

## 3. Evidence-class accounting, with denominators

Mutually exclusive, as required. No count below is offered as a headline trial total.

| Class | Verified count today | Basis |
|---|---|---|
| **Verified human clinical trials (hepatic dataset)** | **0** | No hepatic dataset exists. This is a verified zero, not an unexamined one. |
| Human clinical trials in the five held PDFs | **0** | All three publications are animal in vivo or transfected cell line. |
| Registry candidate pool | **not yet qualified** | 634 unique registry records from 49 compound queries; 182 with results posted; ~93 carry a liver outcome under one screen. **I do not claim an endpoint-evaluable figure** — see below. |
| **Human laboratory (liver injury readout)** | **0 ingested**; 1 open-access source identified (Sewing 2016, **7** tool SSOs **[Rev A]**, plus 2 clinical-stage SSOs in Fig 8C) | **[Rev A, 2026-10-03]** Table 1 sequences now **source-verified** by visual read. Per-compound human LDH/ATP values remain in Fig 8A, unread, so the human rows are not yet quantified. Ingested count stays 0. |
| Human laboratory (mechanistic, non-injury) | 2 documents, EGF readout | **Excluded from this endpoint** — nephrotoxicity uptake biomarker (§1.4). |
| Human 3D / MPS | **0** | No peer-reviewed study found. |
| **Animal supporting** | 80 compounds / 70 numeric ALT (Burdick, mouse); 6 rows (Dieckmann Table 1, mouse, = Hagedorn); 236-ASO panel (mouse, per-oligo data unpublished) | Excluded from every human total. |
| Unresolved | the 66 unnamed Burdick compounds' paper-facing IDs; Burdick's missing `Crtc2`; the 4 model-excluded non-lesion compounds | §1.2 |

**Why no endpoint-evaluable trial count is offered.** The screen that produced ~93 did not survive verification: its own stated exclusion rules were not applied (checkpoint-inhibitor combination oncology trials, a paediatric imetelstat trial, and two defibrotide trials remained inside the "evaluable" set while the prose excluded them); 2 results-posted records were never downloaded; and the inotersen open-label extension `NCT02175004` — carrying three serious hepatobiliary terms including cholestatic jaundice, the only inotersen record with a hepatic signal — was mis-sorted out of the pool entirely. **One re-screen pass is required before any number here is quotable.** I would rather report zero verified trials and a declared unqualified pool than a number that cannot be reconciled to an identifier list.

## 4. Sequence, chemistry and tested-material assessment

Per the shared review questions, with explicit denominators over the eligible set.

| Dimension | Coverage | Note |
|---|---|---|
| Exact sequence | 80/80 Burdick (verified this session); 6/6 Dieckmann Table 1 (verified character-for-character); 4 Hagedorn (figure graphic, **not** digitised); 19/19 Moisan Table S2 (reported, not re-read) | |
| Orientation | 80/80 Burdick — column is explicitly `Core Sequence (5'-3')` | |
| Strand / duplex identity | 80/80 single-strand ASO; no duplex in any hepatic source | Becomes live only if siRNA compounds enter |
| Position-specific chemistry | **80/80 Burdick, per-position, in HELM** | the only hepatic source where this is read rather than inferred |
| | 6/6 Dieckmann — **partial**: sugar class by case, but `beta-D-oxy`/`oxy-LNA`/`alpha-L` appear **zero times** in article+supplement, so sugar stereochemistry is unspecified | |
| Conjugates | none in any hepatic source; Burdick's absence is inferred from token absence, not stated | |
| **Tested-material characterization** | **0/80 Burdick** (deferred to Stanton 2012); **0/6 Dieckmann** (zero hits for purity/HPLC/UPLC/MS/ESI/endotoxin/counterion across article+supplement; supplier named as Exiqon only); **process-level only for Hagedorn** (>85% pooled, LC-MS identity — never per compound) | |

**A populated sequence field is not validated identity**, and this endpoint demonstrates it three ways: the KEGG volanesorsen/olezarsen and inotersen/eplontersen collisions (§2.4); the patent's five distinct compounds under one SEQ ID (§2.4); and the Dieckmann row that joins Exiqon material to Hagedorn's Santaris ALT values (§2.8).

**Purity is a project-wide exposure, not a hepatic one.** The challenge announcement p.6 is a *must*: the dataset "must contain the sequences of all oligos tested, as well as the location of all chemical modifications in each oligo, data on the purity and characterization of each". Current state: kidney 65/65 and thrombocytopenia 259/259 oligos carry the placeholder `"TBD"`; coagulopathy has 0/218 numeric purity values; only 3 of 53 hydrocephalus oligos carry a real figure (90–97%, HPLC). `"TBD"` reads as pending work rather than as an established gap. Recommendation: a `purity_status` enum with a reason — `reported_in_source` / `method_reported_only` / `deferred_to_citation` / `unobtainable_paywalled` / `not_reported` — so a genuine gap is visible instead of hidden behind a missing-value code. **Recording `NOT_REPORTED` alone does not satisfy a "must" requirement**; a stated reason plus a recovery route is the minimum honest answer.

## 5. Raw results vs interpretation vs curator judgment

Proposed, for German's adjudication:

- **Raw**: the source's printed value and its literal unit string (`ALT (U/L) = 12186`, `"10 and 100 mM"` as printed).
- **Source interpretation**: the source's own label (`Model Classification = Lesions`; Hagedorn's >5× ULN high-tox call; Dieckmann's 5-fold relabel of the same data).
- **Curator judgment**: normalisation (µ-glyph repair), controlled-vocabulary repair (`NoLesions` → `No Lesions`), evidence-class assignment, exclusion of the EGF tables.
- **Model eligibility**: German only. Nothing eligible until a rubric exists.

Each needs its own column. Burdick's own ALT disagreement between Table 1 and the supplement for compound `1a` (supplement 34.0; the dossier records Table 1 as 28) is exactly the case that needs the distinction — and should be reconciled against the printed table before either value is used. The supplement also resolves `4a` to 12186 U/L, which Table 1 prints as `–`.

## 6. Access requests

Classified per the register's taxonomy. No purchase, subscription or researcher contact is assumed or requested.

| # | Citation / identifier | File needed | Affected records | Gap it closes | Routes attempted | Observed barrier | Class | Priority |
|---|---|---|---|---|---|---|---|---|
| A1 | Stanton et al. 2012, *Nucleic Acid Ther.* 22:344–359, doi `10.1089/nat.2012.0366`, PMID 22852836 | full text + any synthesis/characterization supplement | **all 80 Burdick compounds** | the only route to purity/analytical characterization for the entire Burdick panel; directly addresses the p.6 "must" | Europe PMC core record (`pmcid` null, `isOpenAccess N`, `hasSuppl N`, `inPMC N`) | **confirmed paywall** — no PMC deposit exists | Confirmed paywall | **High** |
| ~~A2~~ | Sewing et al. 2016, *PLoS One* 11:e0159431, `PMC4956313`, CC-BY | ~~**Table 1** as readable text~~ | ~~9 human-hepatocyte records~~ | — | PLOS figure/image endpoint at `size=large` and `size=original`; Europe PMC `fullTextXML` and `supplementaryFiles` | none — the table is a bitmap (`pone.0159431.t001`, no `<table>` markup), retrieved at 1572×623 PNG + original TIFF and read visually | **WITHDRAWN — RESOLVED [Rev A, 2026-10-03].** Never a paywall, and not an access block either: the publisher serves the render on request. Beebop's "an image table is not a paywall" was correct and my classification was wrong. | — |
| A3 | Hagedorn et al. 2013, `PMC3760025` | `Supp_Table5.pdf`, `Supp_Table6.pdf` | PTEN redesign pairs | redesign before/after pairs, useful as mechanism support | PMC supplementary list (files confirmed present and free) | none — **retrievable, no request needed** | Resolved | Low |
| A4 | Vupanorsen 2022, `PMC9047643` | article + safety supplements | kidney `MSR079`; liver relevance unestablished | may yield liver evidence after endpoint review | free route identified at PMC; direct open hit a browser check | browser check | Technical access block | Low |

**Register corrections requested.** `RESEARCH_ACCESS_REGISTER.md` line 61 is the only hepatic entry: *"Hagedorn 2013 supplementary material named in the hepatic dossier — citation and file route need verification; absence is not proof of a paywall."* That is now resolved and should be closed: **the files exist, are free on `PMC3760025`, and do not contain what the dossier wanted** (S1 is the 25-category scoring scheme; the 236-oligo per-oligo data is unpublished). Separately, the **Burdick 2014 supplement should be added as an entry that is already closed** — it was never recorded as a gap because its existence was unknown. Fittingly, `RESEARCH_SOURCE_COMPENDIUM.md` already lists Europe PMC as the supplementary-file discovery route; it had simply not been run against Burdick.

## 7. Recommended next work package (smallest useful)

**Scope: ingest Burdick 2014 only.** One source, one species, one evidence class. No clinical layer, no cross-organ claim, no model.

| | |
|---|---|
| Creates | `toxicity/hepatic/data/` — `oligos.csv`, `measurements.csv`, `sources.csv`, `identity_crosswalk.csv` |
| Schema | **adopt, do not invent** — the `claude/oligo-challenge-data-4um5mi` thrombocytopenia `scientist_v09` pattern: `Human_Clinical_GT` / `Human_ExVivo_GT` as *physically separate tables* so the classes cannot be pooled, plus `Oligo_Characterization`, `Negative_Control_Rules`, `Leakage_Grouping_Audit`. Reuse the coagulopathy `evidence_class` vocabulary. |
| Chemistry field | **HELM**, carried verbatim from the source column, plus a separate plain-ACGT `sequence_base` and a `chemistry_provenance` value of `read_from_source` (vs `derived_from_prose_rule`, which nothing in this package uses) |
| Closure evidence | 80 oligos with per-position chemistry; 70 numeric ALT with unit `U/L`; 55 microscopic findings; `purity_status = deferred_to_citation` → Stanton 2012 on 80/80; human-trial count **0**; human-lab count **0**; animal-supporting **80**; the 4 reconciliation items from §1.2 recorded as open |
| Dependencies | German's hepatic grade rubric **before any grade column is populated** (the rows can land ungraded); Oscar's authorization; nothing else |
| Explicitly **not** in scope | the EGF tables; the Hagedorn 236 panel; the registry layer; any kidney/liver pairing; any modelling subset |

The registry layer is the right *second* package, not the first — it needs the re-screen of §3 and the `ae_frequency_threshold` design decision before it can produce a defensible count.

## 8. Decisions needed from German or Oscar

**German (scientific):**
1. The hepatic grade rubric — over absolute ALT/AST (U/L), ALT fold-change vs intrastudy control, lesion call, and histopathology score. `nephrotox_grade` is not reusable.
2. Per-source toxicity thresholds: Hagedorn >5× ULN (≈8.5-fold) vs Dieckmann's 5-fold relabel of the same data. Which travels with the row?
3. Confirmation that Burdick (absolute U/L, no in-table control) and Hagedorn/Dieckmann (fold-change vs intrastudy saline, no AST) must never share a numeric column.
4. The EGF exclusion (§1.4) — I propose rejecting both tables as liver-injury records. Yours to ratify.
5. Whether the 4 non-lesion compounds Burdick excluded from its 71-compound model may enter our dataset as measurements, given the exclusion criterion is undocumented.

**Oscar (scope and process):**
6. **Evidence-type ordering in the challenge-facing deliverable.** Oscar's counting and reporting discipline **stands unchanged and is not in question**. The separate question of which evidence type the submission should *lead with* is referred to Beebop for consultation rather than decided here — see §9.
7. **Bounded scope.** There is no minimum dataset size, no compound count and no breadth requirement — "one or more indicators" makes depth in hepatotoxicity alone fully compliant. **My recommendation: go deep on one fully-traceable source rather than broad on unverified identity.**
8. **Ownership.** The Phase 2 Work-Plan assigns hepatotoxicity to **Gustavo** for October, with German reviewing in the week of 19–25 October. Reconcile before anyone writes.
9. **Timeline and a broken path.** Phase 2 closes **2026-12-31**. The announcement directs registrants to Challenge.gov for the mandatory form; that platform was **sunset on 2026-03-30**. The current route needs confirming.
10. **HELM as a project-wide chemistry standard** (cross-endpoint, not hepatic-only). The argument is concrete rather than abstract: the largest hepatic panel is already published in it, and letter-case encoding demonstrably cannot represent the four 5-methylcytosine notations this endpoint meets. Adopting it per-endpoint now and retrofitting later is the expensive order.
11. The supersession header on the Sept-30 suggestions file (§2.10).

## 9. Consultation requested from Beebop — evidence-type ordering

Oscar has asked that this question be put to Beebop rather than settled by my recommendation. Beebop's request states that agreement is not required and that a supported disagreement is useful, so it is raised here as a consultation item, not a dispute.

**Not in question.** Oscar's counting and reporting discipline stands exactly as written: only verified, deduplicated human clinical trials count toward a headline trial total; measurement rows, publications, participants, labels, case reports, spontaneous reports and animal experiments never substitute for trials; human laboratory evidence stays separate and prominent; animal evidence stays in supporting material and out of every human total; unresolved records stay unresolved. This reply applies that discipline throughout, and §3 reports a verified zero rather than a convenient number because of it. Nothing below proposes relaxing any part of it.

**The open question.** Oscar's rule also places human clinical trials *first in presentation order*. For the **challenge-facing deliverable specifically**, the published challenge material appears to order evidence differently, and I could not reconcile the two from the documents alone:

- The announcement (v5, 20pp) contains **zero occurrences** of "trial", "patient" or "volunteer".
- The evidence currency it describes and scores is human in vitro — cell culture, microphysiological systems, 3-D human organoids — with animal data admitted only as a declared supplement or bridge.
- Three of the eight Phase 1 winners were hepatic human in vitro datasets.
- For hepatotoxicity as it stands, a trials-first ordering leads the package with a section whose verified content is zero (§3), while the human-laboratory section has one identified open-access source.

**What I am asking Beebop.** Does Beebop read the challenge material the same way, and if so:

1. Can a single deliverable satisfy both — Oscar's counting discipline governing every number and total, and the challenge's apparent in-vitro-first ordering governing section sequence — or do these genuinely conflict?
2. If they can coexist, what ordering did the other endpoints adopt? Kidney, thrombocytopenia, coagulopathy, hydrocephalus and the neuro endpoints have all published replies and some have built deliverables; a convention may already exist that hepatotoxicity should follow rather than re-decide.
3. Is there challenge material I have not seen that addresses presentation order directly? I was unable to inspect the Phase 2 webinar recording linked from the NCATS challenges page, and its Q&A is the most likely place this is answered.
4. If the conflict is real, is it a per-endpoint choice or a project-level decision that should be made once for all eight?

**Deliberately unresolved.** I make no recommendation on this item. It changes nothing in the §7 work package, which is evidence-class-neutral: Burdick ingests as animal supporting material with a verified human-trial count of zero under either ordering.

## 10. Limitations of this review

- ~~**No sequence from Sewing 2016 has been read.** Any count attributed to it is an upper bound on expectation, not evidence.~~ **[Rev A, 2026-10-03: closed.]** All 7 Table 1 sequences have been read visually from the publisher's render. What remains unread in that source is **Fig 8A** — the per-compound human hepatocyte LDH and ATP values and their concentrations — so the human-laboratory evidence is qualitative in this reply and no human concentration or response value is asserted.
- Hagedorn's 4 figure-borne sequences are **not digitised**; I report their existence, not their content.
- Moisan Table S2's 19 sequences are **reported, not re-read by me** this session.
- Patent chemistry strings read from the OCR text layer are unreliable; conflicts must be re-checked against rendered page images before any are asserted.
- The registry pool is **unqualified** and its screen is known-defective (§3).
- `git` history is unavailable (shallow clone, Beebop's baseline commit unreachable), so no provenance or timing claim is made.
- Drive's two hepatic PDFs match the repo copies **by byte count**, not by computed checksum; no Drive-side hash was obtained.

---

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**
