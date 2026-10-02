# Rocksteady research report — nephrotoxicity

**Responding to:** `toxicity/kidney/BEEBOP_RESEARCH_REQUEST_2026-10-02.md` (review snapshot `6c5797a2590e`)
**Branch:** `claude/amazing-galileo-rwiv95` · **Inventory commit:** `b51003c02ef66b5f226dff02300e3970367a855b`
**Dataset version:** release `kidney-224e9a2f7916` — 246 measurements · 65 roster entries · 42 clinical register rows
**Research date:** 2026-10-02 · **Authorization:** Oscar, 2026-10-02, research/review round
**Status:** RESEARCH ROUND. No validated data, label, grade, eligibility class, adjudication or model was changed.
Acquired material is held in `research_staging/`, outside `data/`.

Work actually performed this round: **4 primary sources retrieved and read in full** (3 trial reports
+ German's routed human 3D-PTEC paper), **20/20 resources logged**, **36 trial registry records
surfaced**, **1 sequence-recovery attempt completed with a null result**. Work proposed but not
performed is marked as such throughout.

---

## 1. Proposal dispositions

| # | Proposal | Disposition |
|---|---|---|
| 1 | Prioritize the 67 human laboratory rows; investigate `10.2131/jts.51.75` | **ACCEPT — substantially executed** |
| 2 | Verify the remaining 10 clinical studies, starting with teprasiran / PHYOX3 / PROMOVI | **ACCEPT — 3 of 10 executed** |
| 3 | Reconsider MSR066 | **ACCEPT — and the defect is four times larger than stated** |
| 4 | Per-dimension bridge audit; recover the 10 missing sequences | **MODIFY — audit already complete; recovery target is not 10** |
| 5 | Correct access classifications | **ACCEPT — executed, and it immediately paid off** |

### P1 — Human laboratory rows and the routed 3D-PTEC source — ACCEPT, substantially executed

German's routed source is **Morimura et al., *Predicting nucleic acid drug-induced nephrotoxicity
using a 3D human renal proximal tubule spheroid model*, J Toxicol Sci 51(1):75–87, 2026**
(`10.2131/jts.51.75`, PMID 41500580). Europe PMC reports `isOpenAccess=N, inEPMC=N`. **It is
nevertheless free**: J-STAGE serves the full PDF at
`jstage.jst.go.jp/article/jts/51/1/51_75/_pdf/-char/en`. Retrieved, 13 pp, 6,530 words,
SHA-256 `2882260fdfa7dcc9…`. This single case vindicates P5 before P5 is even argued: a PMC
"not open access" flag said nothing about the publisher's own free route.

**Overlap check, as requested before staging — the answer is complete overlap, and that is the
good outcome.** The paper tests exactly three compounds, all already on our roster:

| Test compound | Our id | Chemistry (per Table 1) | MW (g/mol) | Vendor / catalog | Cmax (Table 2) |
|---|---|---|---|---|---|
| SPC5001 | `OLG002` | PS, LNA, 5mC | 4689.85 (5726.02 Alexa-647 labelled) | Ajinomoto Bio-Pharma Services, custom synthesis | unknown |
| Viltolarsen | `OLG013` | PMO | 7386.42 | MedChemExpress `HY-132586A` | 0.043 µmol/L |
| Givosiran | `OLG003` | PS, 2′-OMe, 2′-F | 16300.6 | MedChemExpress `HY-132610` | 0.021 µmol/L |

Why this matters more than a new-compound find:

1. **It is a human-laboratory ↔ human-clinical bridge for three compounds.** All three already carry
   human *clinical* renal outcomes in our dataset. That is a human-to-human comparison, which is
   strictly better evidence than the animal bridge whose eight "pairs" collapsed to one matched
   comparison in the October 1 review.
2. **It independently corroborates our strongest translational finding.** The paper's own Table 2
   records SPC5001 as "withdrawn due to nephrotoxicity… multiple foci of tubular necrosis and
   oligonucleotide deposition… in the renal biopsy" while its nonclinical column reads "no clear
   nephrotoxicity was observed". That is the animal-under-predicts case, stated by an independent
   group, and the 3D-RPTEC model detects SPC5001 ("significant ATP depletion… only after prolonged
   exposure to SPC5001").
3. **It is the first concrete lead on the 0/65 purity gap.** Two of three test articles are
   catalogue items with vendor part numbers. A vendor certificate of analysis is a *tested-material*
   purity document, which is precisely the artefact the Challenge asks for and that no trial paper or
   label publishes. This does not close the gap — the vendor's lot is not the trial's lot, and that
   distinction must be preserved — but it converts "unobtainable" into "obtainable for a defined
   subset", which is a different problem.
4. Readouts are ATP, LDH, KIM-1, NGAL and high-content analysis, directly commensurate with our
   existing `intracellular_ATP` and `KIM-1` human in-vitro readouts.
5. **It repairs one of the two weakest bridge pairs identified on October 1.** `OLG013` is
   viltolarsen, and its human side is currently `kidney_toxicity_monitored` — a monitoring
   assertion, not a measurement, which is exactly why I flagged that pair as uninterpretable.
   Morimura supplies real human in-vitro readouts for viltolarsen, and its Table 2 records clinical
   **increased β2-microglobulin and NAG** plus nonclinical increased BUN/creatinine. That converts
   `OLG013` from an assertion-versus-lesion comparison into a measurement-versus-measurement one.

**Current state of the 67 human laboratory rows** (computed at `b51003c`, not asserted): 55/67 carry
a numeric `readout_value`, 61/67 carry a dose or concentration. The gap P1 targets is therefore not
primarily numerical-readout recovery — it is **per-position chemistry, donor/model context and
tested-material method**, which is where the Morimura table contributes and where our patent-derived
rows remain thin.

*Not performed:* extraction of the paper's per-compound dose–response values into staged rows. The
figures are the quantitative locus (Figs 3–6) and figure-level extraction from a PDF needs the
anchor-check discipline we use for patent tables; I did not attempt it in the time available and
would rather do it correctly than quickly.

### P2 — Clinical study verification — ACCEPT, 3 of 10 executed

All three leads named in my October 1 reply were retrieved via the Europe PMC REST `fullTextXML`
endpoint and read in full. Checksums and HTTP evidence in `research_staging/logs/acquisition_manifest.json`;
extracted facts in `research_staging/trial_verification_2026-10-02.csv`.

**PROMOVI / eteplirsen (`MSR040`) — CONFIRMED AND ENRICHED.** NCT02255552, N=79, open-label, 96 weeks.
Source: *"Overall, 8 eteplirsen-treated patients (10.1%) experienced renal TEAEs; each as proteinuria,
which resolved by end of study in all but one individual."* Our row already said `proteinuria 10.1
pct_incidence`, grade 1 — **correct, and now source-verified rather than search-derived.** The paper
adds what the row lacked: the denominator (8/79), and that **3/79 (3.8%) of the proteinuria was
investigator-assessed as drug-related** (Table 5). This is our single best clinical row — human,
quantified, denominator-bearing, and in a **non-renal indication**, so it is not subject to the
confound in P3. It would be the **third verified trial**.

**Teprasiran (`MSR077`) — quantitative value recovered, confound identified.** NCT02610283, 360
randomised, 341 dosed, mITT-bsCr 165 placebo / 157 teprasiran. Monitoring: daily to day 7, then
~day 30/90/365, serum creatinine and cystatin C, independent DMC. Thresholds: AKIN on sCr through
day 5; MAKE90 = death, RRT, or ≥25% eGFR reduction at day 90. Results: AKI 58/157 (36.9%) vs 82/165
(49.7%), ARR −12.8%, OR 0.58, p=0.02 — **this is the efficacy endpoint**. The separable *safety*
comparisons are AKI-as-SAE 5.5% vs 6.8%, and MAKE90 20.9% teprasiran vs 19.3% placebo, OR 1.1
(95% CI 0.6–1.9), p=0.71. Investigator-attributed related AEs were hypotension, ALT and AST — none
renal. Our row's `AKI_incidence = reduced` has no number; the number now exists, but see P3: the
primary endpoint is therapeutic, so the defensible locus is the safety comparison, not the headline.

**Extension-counting, which P2 explicitly asked for.** The teprasiran paper names **four** NCTs:
`NCT02610283` (this phase 2), `NCT03510897` (the larger phase 3 built on it), and `NCT00802347` /
`NCT02610296` (delayed graft function in kidney transplant). Registry search separately surfaced
`NCT00554359`, a phase 1 of **I5NP** — an earlier name for the same molecule. Five trial identifiers,
one molecule. Our register currently holds one teprasiran study key, which is correct, but the
convention needs stating explicitly before any of the other four is added, or the trial total will
inflate on a single drug.

**PHYOX3 / nedosiran (`MSR046`) — PARTIALLY CONFIRMED, and a provenance split is required.**
NCT04042402 (rollover from NCT03847909), N=13, interim analysis at 2.5 years. The paper's primary
objective — annual rate of eGFR decline — was *too preliminary to analyse*; only descriptive eGFR is
reported, as "mean eGFR remained stable (62–84.2 mL/min per 1.73 m²) to month 30". **Our row's value
`eGFR = 2.5 pct_change` does not appear in this paper** and appears to derive from the Rivfloza
label, which the `source_ref` lists alongside it. One row currently cites two documents for one
number without saying which supplied it. Also material and absent from our row: **3/13 (23.1%) had
serious adverse events including acute kidney injury, kidney failure and pyelonephritis** — all
investigator-assessed as unrelated to nedosiran, because kidney stones and nephrocalcinosis are PH1
disease manifestations.

*Not performed:* the remaining 7 of 10. Four have no PMC deposit at all (donidalorsen, ENVISION
givosiran, mongersen, OCEANa-DOSE olpasiran — all NEJM); two are in Europe PMC but not open access
and are bot-walled (NEURO-TTR inotersen `PMC12611561`, van Poelgeest SPC5001 `PMC4693495`); one
(vupanorsen) has its article free but its renal numbers in a 403 supplement. See §5.

### P3 — MSR066 — ACCEPT, and the defect is four times larger than Beebop found

Beebop is factually right. `MSR066` records cemdisiran in IgA nephropathy with
`effect_vs_control = "placebo −6.3; cemdisiran −2.9 (favourable)"`, `readout_value = −2.9`
mL/min/1.73 m² change from baseline at week 32, and `negative_eligibility = confirmed_negative`.
Both arms are losing filtration; the drug arm loses less. That is a **therapeutic effect on
kidney-disease progression**, and it cannot establish absence of nephrotoxicity, because a
therapeutic benefit and a toxic injury act on the same measurement in opposite directions and are
not separable from a single between-arm difference. Our own `CLINICAL_VALIDATION.md:51` contains the
tell in writing: *"A genuine measured negative, **in fact favourable vs placebo**."*

**The independent finding: this is not one mislabelled row, it is an unruled class.** Four of our 42
clinical rows are drugs whose *indication is itself a kidney disease*. All four are grade 0. All four
are classified differently:

| Row | Drug | Indication | `negative_eligibility` |
|---|---|---|---|
| `MSR045` | lumasiran | primary hyperoxaluria type 1 | `efficacy_derived_negative` |
| `MSR046` | nedosiran | primary hyperoxaluria | `asserted_negative_regulatory` |
| `MSR066` | cemdisiran | IgA nephropathy / PNH | `confirmed_negative` |
| `MSR077` | teprasiran | acute kidney injury prevention | `not_eligible_negative` |

Same structure — renal-indication drug, renal functional endpoint, renal-disease population — four
different answers. `MSR045` already carries the right one, so the dataset contains its own precedent.

**Source-grounded disposition for German, no label changed:** introduce a *derived* rule — if the
oligo's indication is a renal disease **and** the readout is a renal functional endpoint, then
`negative_eligibility = efficacy_derived_negative` and `nephrotox_grade_modeling` is left blank.
Derived, not hand-entered, consistent with how `subject_class` and `renal_endpoints_measured` are
already produced. Applied, it reclassifies `MSR046`, `MSR066` and `MSR077` and leaves `MSR045` as-is.

**Consequence German must weigh, stated plainly:** `MSR066` is the **only** `confirmed_negative`
among 42 clinical rows. Reclassifying it leaves the kidney dataset with **zero confirmed clinical
negatives**. I think that is the correct and more honest state — and it converges with German's
independent finding of zero clean sequence-linked clinical negatives in thrombocytopenia, which
suggests a property of the evidence base rather than a curation failure in either endpoint. It also
means no clinical row is currently usable as a modeling negative, which is a material fact for the
narrative and for any future classifier.

Note that `MSR040` (eteplirsen, DMD) is untouched by this rule and remains a measured human clinical
**positive** — the non-renal indications are where clean nephrotoxicity signal lives.

### P4 — Bridge audit and sequence recovery — MODIFY

**The per-dimension bridge audit was completed and published on October 1**, before this request. Its
verified figures: of 8 `paired_same_source` comparisons, **1/8 share a biological endpoint** (`OLG008`,
human A1M/RAP uptake vs animal urinary A1M), 3/8 share a unit, 5/8 share a delivery route, 2/8
compare a monitoring assertion (`kidney_toxicity_monitored`) against an observed animal lesion, and
the pairing test is **vacuous where grades tie at 0** because the argmax set becomes the whole row
set. Recommendation stands: retire `comparison_type` in favour of per-dimension match flags and
label the bridge hypothesis-generating. Beebop's framing — "eight same-source links and one shared
analyte do not establish eight comparable translational pairs" — matches that result exactly.

**Sequence recovery: the target is not ten. Recovered this round: zero. Honest breakdown:**

| Count | Entries | Status |
|---|---|---|
| 2 | `OLG030` `GalNAc_siRNA_class_Janas`, `OLG031` `ASO_2MOE_class_human_pooled` | **Not molecules.** Class-level aggregates pooling observations across a chemistry class. They can never carry a sequence and should not sit in a sequence-coverage denominator. |
| 4 | `OLG041` AON-A, `OLG042` AON-C, `OLG043` AON-D, `OLG044` MYD88-E | **Verified unpublished.** Moisan 2017 (`PMC5363415`) retrieved and read in full: it contains **zero** nucleotide strings of 12–25 nt. Proprietary Roche research AONs. Not an access barrier — the primary source does not publish them. |
| 2 | `OLG025` ISIS113715, `OLG026` ISIS104838 | **Not recoverable from open literature.** Searched Europe PMC (44 and 41 hits); open-access hits are reviews naming the compounds without sequences. Remaining route: Ionis patent sequence listings. Not attempted this round. |
| 2 | `OLG014`, `OLG015` cEt tool/control ASOs | Source is Sandelius 2020 (PMID 33084520), not retrieved this round. Tool compounds; disclosure uncertain. |

**Denominator correction:** sequence coverage should be reported as **55/63 molecules (87.3%)**, not
55/65. Reporting 55/65 understates coverage by counting two aggregates as missing molecules.

**Dedup check, unprompted and clean:** Moisan 2017 states *"a PCSK9-targeting LNA-AON drug (SPC5001,
herein AON-B)"*. AON-B is SPC5001. Our roster handles this correctly — `OLG002` is SPC5001 with
alias `Moisan2017_AON` and a populated case-encoded sequence (`TGCtacaaaacCCA`), and `MSR089`/`MSR090`
are its Moisan rows. There is no duplicate molecule. One cosmetic improvement: the alias could read
`Moisan2017_AON-B` for exactness.

### P5 — Access classification — ACCEPT, executed, and it paid off immediately

I accept the correction without reservation; my `SOURCES_TO_ACQUIRE.md` inferred paywalls from
publisher error responses, which do not establish entitlement walls. Two independent vindications of
Beebop's rule appeared within this round:

- **German's routed paper** reads `isOpenAccess=N, inEPMC=N` in Europe PMC and is **free on J-STAGE**
  (§P1). Had I trusted the PMC flag, I would have filed it as an access request.
- **Conversely, "free" repeatedly turned out not to mean "data-bearing"**: the vupanorsen article is
  free and contains no renal numbers; the VALOR tofersen paper is free and contains no renal content
  at all. Open access and evidentiary value are independent properties, and the register should carry
  both.

Corrected taxonomy for every source previously called blocked is in §5.

---

## 2. Current inventory at commit `b51003c`

Separating **Beebop-recounted**, **my source-verified**, and **curator/reported** values as required.

| Quantity | Value | Qualification |
|---|---:|---|
| Measurement rows | 246 | recounted by both parties, agree |
| Roster entries | 65 | 63 distinct molecules + 2 class aggregates (§P4) |
| `human_clinical` rows | 42 | recounted, agree |
| `human_invitro` rows | 67 | recounted, agree; 55/67 numeric readout, 61/67 dosed |
| `animal_invivo` / `animal_invitro` | 56 / 81 | recounted, agree (137 animal total) |
| Distinct identified trial keys | 12 | register status |
| **Verified distinct human trials** | **2** | register status at this commit; **3rd (PROMOVI) now evidenced but not yet promoted** |
| Independent human cohorts | unknown | no experiment-level register exists; not established |
| Human laboratory experiments | unknown | row count is not experiment count; not established |
| Sequence coverage | 55/63 molecules (87.3%) | field coverage; per-position source verification not established |
| Tested-material purity | **0/65** | verified unreported across all sources reviewed, including the 4 read this round |
| Confirmed clinical negatives | 1 | **recommended to become 0** pending German (§P3) |

**Remaining qualification blockers:** (a) all grades provisional pending German; (b) no clinical row
survives as a modeling negative if §P3 is accepted; (c) per-position chemistry is source-resolved for
only part of the roster; (d) tested-batch identity is nowhere established — reference identity is not
batch identity; (e) 7 of 10 identified trials unread.

## 3. Prioritized acquisition plan

Expected yields are stated as **unknown** where not established, per the request.

| Rank | Target | Expected gain | Dependency |
|---|---|---|---|
| 1 | **Sefaxersen GOLDEN trial**, `PMC13553563`, free | Renal safety of an IgAN ASO in a **non-renal** (geographic atrophy) population — breaks the §P3 confound for a kidney-targeted molecule. Expected usable observations: unknown, likely ≥1 clinical row | none; retrievable now |
| 2 | **Morimura 2026 figure-level extraction** (file in hand) | Up to 3 human-lab constructs × 4 readouts × dose–time; expected qualified rows: unknown pending figure digitization | none; needs anchor-checked extraction |
| 3 | **Vendor CoA for `HY-132586A`, `HY-132610`** | First tested-material purity values in the dataset, for 2 constructs. **Not the trial lot** — must be recorded as vendor-lot characterization, not batch identity | Oscar: is vendor-lot purity in scope? |
| 4 | **Sefaxersen phase 2 IgAN**, Kidney Int, PMID 41443406, `OA=N` | Renal endpoints in IgAN; expected: unknown | access needed (§5) |
| 5 | **IONIS-FB-LRx phase 2 IgAN**, NCT04014335, completed | Completed trial, renal endpoints; publication not yet located | search + access |
| 6 | Circulation 2022 **supplement only** (vupanorsen) | Quantitative renal safety tables; would move `MSR079` from asserted to measured | 403 — human browser |
| 7 | 4 NEJM articles + supplements | Closes 4 of 7 unread trials | institutional access |
| 8 | Ionis patent sequence listings | `ISIS113715`, `ISIS104838` sequences | none; not attempted |
| — | VALOR tofersen | **withdrawn** — read in full, zero renal content | n/a |

**Staged files, with provenance preserved** (`research_staging/`): 4 primary sources, original
filenames, source URLs, retrieval date 2026-10-02, HTTP codes and SHA-256 recorded in
`logs/acquisition_manifest.json`. No validated observation was extracted from any inaccessible text.

**Shared-source ownership:** none of the four files retrieved this round overlaps another endpoint's
access work. I have proposed corrections to `RESEARCH_ACCESS_REGISTER.md` in §5 rather than editing
another endpoint's entries.

## 4. Twenty-resource coverage log

Search date **2026-10-02**. Machine-readable copy: `research_staging/logs/search20_log.json`.
Blocked services are **not** marked searched. Counts from loose relevance matching are flagged,
because a large hit count against an unfiltered query is not coverage.

| # | Resource | Query | HTTP | Result | Status |
|---|---|---|---:|---|---|
| 1 | PubMed (E-utilities) | `oligonucleotide nephrotoxicity` | 200 | 148 | searched |
| 2 | Europe PMC (REST) | same; plus 5 targeted compound queries | 200 | 2,319 | searched — **primary productive route**; serves `fullTextXML` for the OA subset |
| 3 | OpenAlex | same | **429** | — | **not searched** — rate-limited on 5 attempts across both search and single-DOI endpoints. Not a paywall |
| 4 | Semantic Scholar | same | 200 | 183,651 | searched; count is **loose relevance matching**, not 183k relevant papers |
| 5 | ResearchRabbit | — | 200 | — | **not searched** — account sign-in, no public API. Not a content paywall |
| 6 | Undermind | — | 200 | — | **not searched** — paid service, no public API |
| 7 | Elicit | — | 200 | — | **not searched** — account/subscription, no public API |
| 8 | Consensus | — | 200 | — | **not searched** — account required, no public API |
| 9 | GEO | `antisense oligonucleotide kidney`; + 23 compound names | 200 | 100 / per-compound | searched — **spot-checked and negative**, see below |
| 10 | SRA | same | 200 | 40 | searched; no renal oligo-toxicity deposit identified |
| 11 | PRIDE | `oligonucleotide kidney` | 200 | **0** | searched |
| 12 | ProteomeXchange (PROXI) | `oligonucleotide` | 200 | no relevant | searched |
| 13 | BioStudies | `oligonucleotide kidney`; + 23 compounds | 200 | 100,732 | searched; headline count is **loose matching**; per-compound quoted queries used instead |
| 14 | ArrayExpress (in BioStudies) | same | 200 | 6,284 | searched; same caveat |
| 15 | ClinicalTrials.gov (API v2) | 4 queries incl. `siRNA nephropathy`, `antisense glomerulonephritis` | 200 | 13 / 21 / 3 / 2 → **36 distinct NCTs** | searched — **highest-yield resource this round** |
| 16 | CTD | `mipomersen` batch query | **302** | — | **not searched** — endpoint redirects to HTML; oligos are poorly represented as CTD chemicals |
| 17 | ICE (NIEHS) | portal | 200 | — | reachable; **no endpoint applicability** — curated assays are small-molecule oriented |
| 18 | ToxCast / CompTox | portal | 200 | — | reachable; **no endpoint applicability** — library excludes therapeutic oligonucleotides |
| 19 | Zenodo | `oligonucleotide nephrotoxicity`; + 23 compounds | 200 | 1,155 | searched; no renal oligo-toxicity dataset identified |
| 20 | Dryad | `oligonucleotide kidney` | 200 | 2 | searched; not relevant |

**Totals: 12 searched, 4 not searched (login/subscription), 2 technically blocked, 2 reachable but
not applicable.**

**Material negative result, verified not assumed.** The repository route is empty for this endpoint.
Per-compound searches across GEO/SRA/BioStudies/Zenodo returned hits for 22 of 23 compounds, but
spot-checking the most promising — inotersen, 13 GEO records, the drug with our strongest clinical
nephrotoxicity signal — showed **all 13 are neural-progenitor expression samples with zero renal
relevance**. Keyword presence in repository metadata is not endpoint relevance. Consequence: for
oligonucleotide nephrotoxicity, **primary literature and journal supplements are the only productive
acquisition route**, which is why §3 and §5 are weighted entirely toward papers and supplements.

**Additional sources inspected beyond the twenty:** J-STAGE (productive — §P1), DOI content
negotiation, journal supplement endpoints at `ahajournals.org`, White Rose institutional eprints,
and the ClinicalTrials.gov registry records listed below.

**New leads from resource 15, absent from our dataset.** These are **registry records, not verified
trials**, and are not counted anywhere:

| NCT | Drug | Phase / status | Why it matters |
|---|---|---|---|
| `NCT05797610` | **Sefaxersen** (RO7434656) | 3, active | ASO for IgA nephropathy; molecule absent from dataset |
| `NCT04014335` | **IONIS-FB-LRx** | 2, completed | Complement factor B ASO in IgAN; completed, so data should exist |
| `NCT07271186` | ALN-ANG3 | 2, recruiting | Diabetic kidney disease |
| `NCT06989359` | ADX-038 | 2, recruiting | Complement-mediated kidney disease |
| `NCT00554359` | I5NP | 1, completed | **Same molecule as teprasiran** — extension-counting item, not a new drug |
| `NCT03159416` | inclisiran | 1, completed | Dedicated renal-impairment PK study |

## 5. Paper / supplement / data access table

Classified per the request's taxonomy. Prices and entitlements are **unverified** throughout — none
was checked, and no purchase, subscription or credential was used.

| Source | Identifier / link | Discovered via | Needed file | Gap addressed | Attempt (2026-10-02) | Outcome | Class | Priority |
|---|---|---|---|---|---|---|---|---|
| Morimura K, Takahashi E, Maeda H, Nishioka Y, Araki A, Mizumoto H, Jimbo Y (2026). *Predicting nucleic acid drug-induced nephrotoxicity using a 3D human renal proximal tubule spheroid model.* J Toxicol Sci 51(1):75–87 | `10.2131/jts.51.75`; PMID 41500580 | German evidence-watch memo via Beebop | full article | human lab chemistry + characterization | J-STAGE `_pdf/-char/en` | **200, 13 pp retrieved** | free publisher route (PMC flag said `OA=N`) | done |
| Thielmann M, Corteville D, Szabo G, Swaminathan M, Lamy A, Lehner LJ, et al. (2021). *Teprasiran, a Small Interfering RNA, for the Prevention of Acute Kidney Injury in High-Risk Patients Undergoing Cardiac Surgery.* Circulation | `PMC8487715`; `10.1161/CIRCULATIONAHA.120.053029`; NCT02610283 | my Oct-1 reply | full text | trial verification | EPMC REST `fullTextXML` | **200, 7,330 w** | open access | done |
| Groothoff J, Sellier-Leclerc AL, Deesker L, Bacchetta J, Schalk G, Tönshoff B, et al. (2024). *Nedosiran Safety and Efficacy in PH1: Interim Analysis of PHYOX3.* Kidney Int Rep | `PMC11068990`; NCT04042402 | my Oct-1 reply | full text | trial verification | EPMC REST `fullTextXML` | **200, 6,919 w** | open access | done |
| McDonald CM, Shieh PB, Abdel-Hamid HZ, Connolly AM, Ciafaloni E, Wagner KR, et al. (2021). *Open-Label Evaluation of Eteplirsen in Patients with Duchenne Muscular Dystrophy Amenable to Exon 51 Skipping: PROMOVI.* J Neuromuscul Dis | `PMC8673535`; NCT02255552 | my Oct-1 reply | full text | trial verification | EPMC REST `fullTextXML` | **200, 7,661 w** | open access | done |
| Moisan A et al. (2017). *Inhibition of EGF Uptake by Nephrotoxic Antisense Drugs In Vitro…* | `PMC5363415` | existing `design_source` | full text | sequence recovery | EPMC REST `fullTextXML` | **200, read** — no sequences present | open access; **data absent from source** | done |
| Jaffe GJ, Wykoff CC, McCaleb ML, Barrett TD, Frazer-Abel A, Norris D, et al. (2026). *GOLDEN: Efficacy and Safety of Complement Factor B Antisense, Sefaxersen, in Geographic Atrophy.* Ophthalmol Sci | `PMC13553563` | resource 2 this round | full text + safety tables | non-renal-indication renal safety | not yet attempted | — | open access | **1** |
| Sato T, Fukase H, Ishida T, Karasawa A (2026). *A First-in-Japanese Phase 1, Double-Blind, Placebo-Controlled, Parallel-Cohort Study of Sefaxersen.* Clin Pharmacol Drug Dev | `PMC13555670` (Europe PMC marks this record a duplicate pending deletion; the sibling record is PMID 42713733, `OA=N`) | resource 2 | full text | renal safety, phase 1 | not yet attempted | — | open access | 2 |
| Sefaxersen phase 2 IgAN | PMID 41443406, Kidney International | resource 2 | article + supplement | IgAN renal endpoints | not yet attempted | — | `OA=N, inEPMC=N` — entitlement **unverified** | 3 |
| Vupanorsen TRANSLATE-TIMI 70 **supplement** | `10.1161/CIRCULATIONAHA.122.059266` | Oct-1 reply | **supplement only** | quantitative renal safety for `MSR079` | publisher suppl; PMC bin | **403 / 404** | **technical block** on a free supplement | 4 |
| NEURO-TTR inotersen | `PMC12611561`; `10.1056/NEJMoa1716793` | register | article + renal AE tables | our top signal | EPMC XML; PMC HTML; europepmc HTML | XML refused; **reCAPTCHA**; Cloudflare | in EPMC, `OA=N`; **technical block** | 5 |
| van Poelgeest SPC5001 | `PMC4693495`; `10.1111/bcp.12738` | register | article | SPC5001 human data | same three routes | same | in EPMC, `OA=N`; **technical block** | 6 |
| ENVISION givosiran | `10.1056/NEJMoa1913147` | register | article + supplement | trial verification | EPMC search | **no PMC deposit** | missing deposit; paywall **unverified** | 7 |
| Donidalorsen phase 3 | `10.1056/NEJMoa2402478` | register | article + supplement | trial verification | EPMC search | no PMC deposit | missing deposit; paywall unverified | 8 |
| OCEANa-DOSE olpasiran | `10.1056/NEJMoa2211023` | register | article + supplement | trial verification | EPMC search | no PMC deposit | missing deposit; paywall unverified | 9 |
| Mongersen phase 2 | `10.1056/NEJMoa1407250` | register | article | trial verification | EPMC search | no PMC deposit | missing deposit; paywall unverified | 10 |
| Sandelius 2020 | PMID 33084520 | existing `design_source` | sequence listing | `OLG014`/`OLG015` | not attempted | — | unknown | 11 |
| Ionis patent sequence listings | — | — | sequence listings | `ISIS113715`, `ISIS104838` | not attempted | — | unresolved citation | 12 |
| VALOR tofersen | White Rose eprints | Beebop register | — | — | retrieved and read previously | **zero renal content** | free; **struck as valueless** | — |

**Precise request to Oscar.** Three items need only a person with a browser, not a purchase:
the **vupanorsen Circulation supplement** (403), **NEURO-TTR inotersen** `PMC12611561`, and
**van Poelgeest** `PMC4693495` — all free-or-deposited and defeated by bot protection, not by
entitlement. The four NEJM articles are the only items that may genuinely require institutional
access, and whether they do is **unverified**.

**Proposed corrections to `RESEARCH_ACCESS_REGISTER.md`** (not applied — it is shared):
`PMC8487715` is listed as a free teprasiran route, but direct retrieval returns a reCAPTCHA
interstitial; the working route is the Europe PMC REST `fullTextXML` endpoint, which should be
recorded as the general method for the OA subset. Second, the register should carry an
"evidentiary value" column beside access status — VALOR tofersen is free and worthless here, and
that combination needs to be representable.

## 6. Access-barrier classification summary

- **Confirmed publisher paywall:** none. No entitlement wall was directly verified this round.
- **Service login / subscription (search tools, not content):** ResearchRabbit, Undermind, Elicit, Consensus.
- **Technical blocking:** OpenAlex (429, 5 attempts); CTD batch endpoint (302); PMC HTML and
  europepmc.org HTML (reCAPTCHA / Cloudflare) for `PMC12611561` and `PMC4693495`; `ahajournals.org`
  supplement (403).
- **Missing repository deposit:** 4 NEJM articles — **does not prove a paywall**.
- **Missing supplement:** PMC supplementary directory 404 for `PMC9047643`.
- **Unresolved citation:** `MSR064` "KARDIA_trials"; Ionis sequence listings.
- **Free and retrieved:** 5 sources (4 this round + VALOR previously).
- **Free but evidentially empty:** VALOR tofersen.

## 7. What needs whose approval

**German — scientific adjudication:**
1. `MSR066`, and the derived renal-indication rule in §P3; accepting it takes confirmed clinical negatives to **zero**.
2. Whether `MSR046`'s value may be split between the PHYOX3 paper and the Rivfloza label, and which supplies the number.
3. Whether the PHYOX3 renal SAEs (AKI, kidney failure, pyelonephritis; investigator-assessed unrelated, PH1 disease manifestations) should be recorded at all, and if so how.
4. Whether `OLG008` alone constitutes a defensible matched human↔animal comparison (carried over from Oct-1; unanswered).
5. Whether `kidney_toxicity_monitored` rows should remain measurements (carried over; unanswered).
6. Whether a vendor-lot certificate of analysis is admissible as characterization, given it is not the trial lot.

**Oscar — implementation and scope:**
7. Promotion of `MSR040`/PROMOVI to verified, taking verified trials 2 → 3.
8. The extension-counting convention, before any of teprasiran's other four NCTs is added.
9. A human-browser download for the three bot-walled free items in §5.
10. Whether the four NEJM papers justify institutional access.
11. Whether to add sefaxersen and IONIS-FB-LRx as new constructs, and whether the sequence-coverage denominator becomes 63 rather than 65.

No final classifier, label change, merge or release is unlocked by this round, and none was performed.

---

RESEARCH ROUND COMPLETE — AWAITING GERMAN'S ADJUDICATION AND OSCAR'S IMPLEMENTATION APPROVAL
