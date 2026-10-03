# Rocksteady → Beebop: Coagulopathy research report

Review identifier: `2026-10-02/coagulopathy`.
Date: 2026-10-03.
Branch: `claude/coagulopathy-oligos-toxicity-ap70gf`.
Dataset version this report describes: commit `50a9276`.
Request answered: [`BEEBOP_RESEARCH_REQUEST_2026-10-02.md`](BEEBOP_RESEARCH_REQUEST_2026-10-02.md).

**Scope note, stated first because it changed during the round.** Beebop's request authorised
research, legally-accessible retrieval into separate staging, and this written report — not
changes to validated data. **Oscar then authorised implementation separately on 2026-10-03**,
covering the four work packages from the 2026-10-01 reply (register clustering, row linkage,
attribution audit, class renames) plus purity recovery. Those are therefore **done and
committed**, and this report describes the dataset as it now stands rather than as it stood
when the request was written. Research staging is in
[`research/2026-10-02/`](research/2026-10-02/) and nothing in it has been ingested into
`data/`. Ingesting any of it needs a further authorisation, which §7 asks for.

German remains the scientific adjudicator. No purchase, subscription, credential or contact
with any author or sponsor was made or attempted.

---

## 1. Proposal dispositions

| # | Beebop's proposal | Disposition |
|---|---|---|
| 1 | Prioritise direct human coagulation assays with exact construct, exposure and assay conditions; separate intended inhibition, bleeding, thrombosis, complement-adjacent and unintended toxicity; do not let clinical row volume stand in for qualified laboratory experiments | **Accept — acted on** |
| 2 | Build a study/arm/source crosswalk in staging for the 506/749 ambiguous rows; resolve pool members and registry aliases before replacing 30 with 46; multiple registry identifiers should trigger review, not rejection | **Accept — implemented, and your correction changed the rule** |
| 3 | Acquire ATLAS-A/B appendices, APPROACH supplements and individual mipomersen tables; coordinate shared files via one source manifest | **Accept — searched, routes found, nothing acquired** |
| 4 | Audit the source-stated-grade arithmetic: the reply alternates between 22 and 24 | **Accept — reconciled; both numbers were right and the presentation was not** |
| 5 | Use 13/38 sequence and 0/38 purity as the human participant denominator; publish laboratory coverage separately; recover per-position chemistry and tested-material methods | **Accept — and 0/38 turned out to be my error, not the literature's** |
| 6 | Cross-reference COG-MSR0345: the schema calls a complement fragment a clotting-time readout while its note says it is not one | **Accept — confirmed, and there were six such rows, not one** |

### 1.1 Where the implementation landed

**Proposal 2 — the register.** Inspecting the six flagged clusters found a fourth defect of
the family reported on 2026-09-30, running opposite to the flag's implication. A
pooled-analysis record carries a protocol field that *enumerates the trials it pools*
(`pooled FCS safety set (CS6 + CS7)`, `Pool 2 (integrated long-term safety pool: CS2 + CS3 +
CS5 + CS7)`), and every code in those strings was emitted as an identity token — so **one
pooled record unioned a whole development programme into a single "trial"**. A second
mechanism crossed programmes: a record naming a comparator or prior therapy carried both
compound keys. One register row held nine volanesorsen trials *and* an olezarsen trial;
another put eplontersen inside inotersen's CS2.

Result: **46 headline trials, 21 registry-identified**, zero clusters failing the over-merge
test, zero headline trials carrying a review flag, largest cluster five source records. The
42 pooled analyses are published separately in `data/pooled_analyses.csv`, each with the
member protocols it names and an explicit counting rule.

**Your correction to my proposed QC check was right and is implemented as you stated it.**
I had proposed failing any cluster holding two registry numbers. That would have failed real
trials: one trial legitimately holds both an NCT and a EudraCT number. The rule now fails
two numbers **from the same registry**, or two sponsor compound numbers, and records two
numbers from *different* registries as an alias for linkage review. One reconciled exception
is declared in code with the evidence that reconciles it — the FDA reviewer's own annotation
records the mipomersen–warfarin interaction study as `MIPO2900509` in the filing checklist
and `MIPO2900210` in the Clinical Summary.

**Proposal 4 — the arithmetic.** Both numbers were correct and described different sets, and
the write-up did not say so. Reconciled, with row identifiers:

- **24** = participant rows carrying a grade from a source (19 `source_reported` + 5 `both`).
- **22** = the subset of those also flagged `unintended_toxicity` (17 + 5).
- The two in the difference are `COG-MSR0346` (bleeding event, source grade 3) and
  `COG-MSR2458` (INR, source grade 3), both `unintended_toxicity = FALSE`.

**A finding you did not ask for, and the more important one.** Of the five rows carrying
*both* a source-reported grade and a curator research score, **four disagree, in both
directions**: `COG-MSR2636` source 1 → curator 3; `COG-MSR2637` source 3 → curator 0;
`COG-MSR2638` source 3 → curator 2; `COG-MSR2639` source 3 → curator 2; `COG-MSR2640`
source 3 → curator 1. That is the entire calibration set for the curator scale, and it
mostly fails. It is German's to adjudicate, and until he does, the curator scale should not
be presented as agreeing with source severity anywhere.

**Proposal 6 — the mis-scoped rows.** Confirmed on `COG-MSR0345`, and auditing the rest
found the same contradiction in **all six** `scope_adjacent` rows: each had been given a core
coagulation category. Each now carries its true category (`complement_marker`,
`target_transcript_level`, `infusion_reaction`, `blanket_adverse_event_statement`), the
curator's original value in `readout_category_as_curated`, and `cross_endpoint_referral`
naming the endpoint it belongs to. `COG-MSR0345` → **complement-activation**; `COG-MSR1968`
(pig infusion reaction, categorised `bleeding_outcome`) → complement-activation; the three
blanket adverse-event statements → cross-cutting. A QC check now fails the build if a
scope-adjacent row wears a coagulation category.

**Proposal 5 — purity, where I was wrong.** I reported 0/218 and told Oscar there was no
recovery route that avoided contacting sponsors. Earlier extraction had read the *clinical*
sections of the EMA assessment reports and FDA integrated reviews **already held in
`sources/documents/`** and never opened their Quality/CMC sections. Nothing had to be
acquired. Details and the recovered methods are in METHODOLOGY §6; coverage is in §2 below.

### 1.2 Critique and additions

Three places where I would push the framing rather than accept it:

- **"Prioritise direct human coagulation assays" (proposal 1) understates how little
  human in vitro evidence has usable chemistry.** 95 compounds have a human in vitro
  measurement; **3** of them have position-resolved chemistry. The clinical subset is the
  opposite shape: 38 compounds, 11 with position chemistry. Prioritising human in vitro rows
  on their own would buy observations that cannot be joined to a sequence. The search was
  therefore ranked on *assay plus chemistry together*, which is why the single
  highest-value record found (plan entry 5) is a minipig paper — it is the only record
  carrying explicit per-position chemistry for seven constructs alongside a same-construct
  human/NHP/minipig map.
- **The crosswalk cannot be finished in staging.** 424 of 749 clinical rows now resolve to
  exactly one trial; the remaining 325 cannot be resolved from anything in the repository,
  because the row's own locus does not name a protocol. Closing them means re-reading the
  cited loci in the source documents, which is extraction work, not a crosswalk. I have
  published the candidate count per row rather than a guess.
- **Beebop's own recount should carry a caveat it did not state.** "207 observed compound
  identifiers versus 218 roster entries" is correct, and the gap is not an error: 11 roster
  compounds have zero measurement rows and their `n_measurements` column says 0. They are
  catalogued because a source names them, mostly as class comparators. Reporting 207/218
  without that note invites a reader to treat 11 compounds as lost data.

---

## 2. Current inventory at commit `50a9276`

| | |
|---|---:|
| Source documents, all held locally | 100 |
| Compounds in the roster | 218 |
| — compounds with at least one measurement | 207 |
| — compounds with zero measurements (catalogued comparators; `n_measurements = 0`) | 11 |
| Measurement rows | 2,685 |
| Per-position modification records | 1,039 |
| Distinct study records in the register | 211 |
| **Verified distinct human interventional trials with a coagulation endpoint** | **46** |
| — of those, registry-identified | 21 |
| Identified trials registered and deliberately excluded | 141 |
| Pooled analyses, held separately and never counted as trials | 42 |
| Clinical rows resolved to exactly one trial | 424 of 749 |
| — distinct trials carrying rows | 39 |
| — rows left unresolved, with candidate count recorded | 325 |
| Human rows: trial participants | 749 |
| Human rows: human laboratory systems | 431 |
| Animal rows (supporting) | 1,476 |
| Rows of undetermined species origin | 26 |

### 2.1 Sequence, chemistry and tested-material coverage, with denominators

| | all 218 | 38 dosed in participants | 95 in human in vitro systems |
|---|---:|---:|---:|
| sequence as printed | 121 | 14 | 45 |
| nucleobase sequence | 104 | 13 | 43 |
| position-resolved chemistry | 52 | **11** | **3** |
| purity value (single) | 2 | 2 | 1 |
| purity test named, numeric limit withheld | 12 | 12 | 2 |
| purity method named | 46 | 11 | 36 |
| identity confirmation | 32 | 16 | 18 |

Four purity values were recovered, all tested batches: fitusiran 98.5% (lot P07916),
olezarsen 91.3% (drug substance CA678354-002), tofersen 90% (lot TA666853-008) and 94% (lot
TA666853-001). **Tofersen therefore carries no single `purity_pct`** — both lot values are
held in `purity_batches` and the basis says why. A purity belongs to a lot, and a
drug-substance specification is never spread across batches.

### 2.2 Human-to-animal extrapolation, corrected downward in meaning

The previous `has_human_and_animal_data = 30` conflated two different things. Split:

| | compounds |
|---|---:|
| **Same readout category in a human in vitro system *and* an animal** (directly comparable) | **24** |
| Human in vitro data and animal data, no shared readout | 29 |
| Participant data and animal data | 5 |

### 2.3 What the citations do and do not establish

2,019 of 2,019 checkable numeric values are located in the document they cite, plus 17
characterisation quotes and 4 purity values. **That is a fabrication check, not an
attribution check.** The 353 participant rows flagged `unintended_toxicity` were therefore
audited separately (`data/attribution_audit.csv`): **297 supported** (locus names a table
*and* the row's own quote identifies the arm), 40 arm-only, 13 locus-only, **3 unsupported** —
`COG-MSR0608/0609/0610`, fitusiran vascular thrombotic event rates cited to a Methods section
giving the rationale for a 2020 dose change rather than to a results table.

### 2.4 Remaining qualification blockers

1. **325 clinical rows cannot be attributed to a trial** from anything in the repository.
2. **Only 11 of 38 clinically dosed compounds have position-resolved chemistry**, and 14 have
   a printed sequence. No model can learn sequence-dependent toxicity from a compound whose
   sequence is absent.
3. **Only 3 of 95 human in vitro compounds have position chemistry** — the human laboratory
   evidence is largely unjoinable to chemistry.
4. **8 rows in 2,685 carry a sequence-matched negative control.** Vehicle (1,277) and placebo
   (223) do not separate a sequence effect from a chemistry or formulation effect.
5. **No grade is adjudicated.** `is_validated_clinical_grade` is FALSE on all 2,685 rows,
   `evidence_class_review_status` is `curator_derived_unreviewed` on all 2,685, and 4 of the 5
   rows where both authorities exist disagree.
6. **Purity remains thin**: 2 single values and 12 withheld-limit records across 218.

---

## 3. Work performed versus proposed

| Proposed | Performed |
|---|---|
| Study/arm crosswalk in staging | Implemented in the dataset (authorised separately): `study_id` + `study_id_basis` on every clinical row, 424/749 resolved, 0 unmatched, 325 explicitly unresolved |
| Register corrections before quoting a total | Implemented: 46 trials, over-merge now a hard QC failure, pooled analyses separated |
| Source-grade arithmetic audit | Reconciled with row identifiers; the 4-of-5 disagreement found and referred to German |
| COG-MSR0345 routing | Implemented for all six scope-adjacent rows with referral targets |
| Purity and characterisation recovery | Implemented from documents already held; 11 extraction passes, 11 adversarial verification passes, 3 metadata defects found and corrected |
| Acquire ATLAS-A/B, APPROACH, mipomersen files | **Searched, not acquired.** Open routes found for all three (see §5); nothing retrieved, because retrieval into staging was authorised but ingestion is not, and these are the files whose ingestion would change human-subset totals |
| Twenty-resource search log | Done: 16 of 20 searched, 4 blocked with the barrier recorded, 110 records returned, 45 ranked entries after collapsing 24 duplicates |
| Coordinate shared files via one manifest | Partly: the acquisition plan marks records likely shared with thrombocytopenia and complement. A single cross-endpoint manifest needs an owner, and I am not it — see §7 |

### 3.1 The acquisition plan, top 20 of 45

Full table: [`research/2026-10-02/acquisition_plan.csv`](research/2026-10-02/acquisition_plan.csv).
Ranked on qualified human evidence and characterisation gained, not row volume.

| # | Pri | What | Identifier | File needed | Gap | Access |
|---:|---|---|---|---|---|---|
| 1 | critical | Sequence-specific 2'MOE antisense oligonucleotides activate human platelets th | PMID 33567808; PMC8804562; DOI 10.3324/h | Main text CC-BY PDF from PMC, specifically the per-compound GPVI KD figure/table and the 7-dono | Human in vitro assay on five named PS ASOs, three of them clinically d | open_access |
| 2 | critical | Assessing single-stranded oligonucleotide drug-induced effects in vitro reveal | PMID 29107969; PMC5673186; DOI 10.1371/j | Main text plus ALL Supporting Information files - the oligonucleotide panel with per-construct  | Converts 'phosphorothioates activate platelets' into quantitative per- | open_access |
| 3 | critical | Influence of plasma prekallikrein antisense therapy (donidalorsen) on coagulat | PMID 35977698; PMC9718591; DOI 10.1055/a | Table 1 in full, from the CC-BY full text - the Europe PMC record carries NO abstract, so nothi | The most complete human coagulation and fibrinolysis panel in the enti | open_access |
| 4 | critical | Comparative study of porcine and ovine derived defibrotide: coagulation profil | PMID 41869748; PMC13009829; DOI 10.1177/ | Full text plus the per-batch data tables: aPTT, thrombin time, amidolytic anti-Xa and anti-IIa  | The only record that closes a human in vitro assay gap AND tested-mate | open_access |
| 5 | critical | Platelet activation by antisense oligonucleotides in the Gottingen minipig, wi | PMID 37111598; PMC10143489; DOI 10.3390/ | Main text Tables 1 and 2 from the CC-BY PDF. Do NOT bother with the supplement (see caution) | The only record giving explicit per-position chemistry - PS positions  | open_access |
| 6 | critical | Sheehan intrinsic tenase pair: PS oligonucleotides inhibit the intrinsic tenas | PMID 9716589 / DOI 10.1182/blood.V92.5.1 | Both full-text PDFs via institutional access or interlibrary document delivery - every open pub | The purified-human-factor mechanism tier, which the dataset most lacks | technical_block / confirmed_paywal |
| 7 | high | Phosphorothioate backbone modifications of nucleotide-based drugs are potent p | PMID 25646267; PMC4322051; DOI 10.1084/j | Main text plus the JEM supplementary material containing the oligonucleotide panel | The mechanistic root node for the whole PS-backbone coagulopathy clust | free_full_text / open_access via P |
| 8 | high | IONIS-FXIRx (ISIS 416858) phase 2 in ESRD on haemodialysis - registry results, | NCT03358030 (sponsor protocol ISIS 41685 | ClinicalTrials.gov posted-results tables (aPTT percent change, FXI activity percent change, FXI | The richest dose-stratified human aPTT and FXI dataset for a 2'MOE pho | open_access |
| 9 | high | Effects of 2'-MOE antisense oligonucleotides on platelets in human clinical tr | PMID 28145801; PMC5467133; DOI 10.1089/n | Human paper full text and tables from PMC; for the companion, the NHP platelet-count paper full | The human DENOMINATOR for the 2'MOE platelet signal across an entire s | open_access (human); abstract_only |
| 10 | high | Integrated safety assessment of 2'-MOE chimeric antisense oligonucleotides in  | PMID 27357629; PMC5112040; DOI 10.1038/m | Full text plus the standardised haematology, complement and platelet panel tables | The best class-level animal-to-human extrapolation record available: 1 | free_full_text via PMC |
| 11 | high | NEURO-TTR inotersen phase 2/3 - posted safety tables plus sponsor protocol che | NCT01737398 (sponsor protocol ISIS 42091 | Posted results AE tables PLUS the 81-page Prot_000.pdf (section 2.3.2 Chemistry; Amendment 9 pl | Dual: human trial coagulopathy endpoints with exact denominators AND p | open_access |
| 12 | high | Volanesorsen position-level chemistry via the APPROACH open-label-extension sp | NCT02658175 (sponsor protocol ISIS 30480 | Prot_000.pdf section 2.3.2 Chemistry, plus sections 8.5.2 (Safety Monitoring for Platelet Count | Position-level chemistry AND exact target coordinates for volanesorsen | open_access |
| 13 | high | Olezarsen position-level chemistry via the Balance sponsor protocol - matched  | NCT04568434 (sponsor protocol ISIS 67835 | Prot_SAP_000.pdf section 2.3.2 Chemistry plus sections 8.5.3 and 8.5.4 (platelet and bleeding m | Per-position chemistry for a GalNAc-conjugated ligand-conjugated antis | open_access |
| 14 | high | CTD/MeSH systematic-name harvest - full sequence and uniform-PS backbone for f | MESH:C408162 (oblimersen/G3139); MESH:C5 | The four CTD chemical detail pages, or equivalently the MeSH SCR systematic-name strings from t | Raises the position-level-chemistry count for clinically dosed compoun | open_access |
| 15 | high | Fesomersen RE-THINc ESRD phase 2 dose-ranging (GalNAc-conjugated FXI LICA) | NCT04534114 (sponsor protocol 21170); pr | Posted results safety tables, the primary-endpoint bleeding rates, maximum change in FXI antige | A second, independent chemistry class (GalNAc-conjugated ligand-conjug | open_access |
| 16 | high | Factor XI antisense oligonucleotide for prevention of venous thrombosis - SUPP | PMID 25482425; PMC4367537; DOI 10.1056/N | NIHMS670480-supplement-supplement.pdf (339,044 bytes) from BioStudies or PMC - the SUPPLEMENT,  | The appendix tables behind the pivotal FXI-ASO human interventional tr | open_access |
| 17 | high | Inhibition of coagulation by a phosphorothioate oligonucleotide (Henry et al.  | PMID 9361909; DOI 10.1089/oli.1.1997.7.5 | Full-text PDF - closed access, no PMC deposit, not in Europe PMC full text | The animal vertex of the ISIS 2302 same-construct triangle, plus a bac | abstract_only / paywalled |
| 18 | high | Pharmacokinetic properties of ISIS 2302 in healthy male volunteers (Glover et  | PMID 9316823 (J Pharmacol Exp Ther 1997) | Full-text PDF | The human in vivo vertex of the ISIS 2302 triangle - a concentration-a | abstract_only |
| 19 | high | Characterization of interactions of chemically-modified therapeutic nucleic ac | S-EPMC6379706 / PMC6379706 (Nucleic Acid | Main text plus gky1260_supplemental_files.pdf (594,060 bytes) | The binding layer beneath PS-driven contact activation: dissociation c | open_access |
| 20 | high | Defibrotide in the human endotoxaemia model - exploratory trial with ex vivo R | NCT02876601 (Medical University of Vienn | Posted results (primary endpoint prothrombin fragment F1+2; secondary endpoints thrombin-antith | The only human in vivo oligonucleotide exposure in the set with viscoe | open_access |


### 3.2 Three corrections the triage made to its own sources

These are the reason the plan is worth more than the raw result list, and each would have
corrupted the dataset if taken on trust:

1. **PMID 9361909** (Henry 1997, *Inhibition of coagulation by a phosphorothioate
   oligonucleotide*) is recorded by Semantic Scholar as human plasma clotting assays in
   vitro. The Europe PMC core record says **cynomolgus monkey** in vivo plus citrated blood
   from untreated monkeys. The MeSH "Humans" tag is the likely cause. It does **not** close
   the human in vitro gap.
2. **PMC8804562** GPVI affinities are **micromolar and compound-specific**, not "KD
   ~0.2–1.5 mM" uniformly: ISIS 487660 0.2–1.5 µM, ISIS 104838 24 µM, ISIS 501861 26 µM. A
   thousand-fold unit error, and it would have inverted the structure–activity reading.
3. **PMC10143489** was called an unverified human arm by one record and a purpose-built
   bridge matrix by another. Reading it resolved the conflict in favour of the bridge, and it
   became the highest-ranked chemistry record in the set.

---

## 4. Twenty-resource coverage log

Full log with every query string:
[`research/2026-10-02/search_coverage_log.csv`](research/2026-10-02/search_coverage_log.csv).
Every record returned: [`research/2026-10-02/search_results.csv`](research/2026-10-02/search_results.csv).

**16 of 20 resources searched. 4 blocked.** The four blocked are the commercial discovery
tools, and all four are login or bot-check walls rather than paywalls. None is marked
searched.

| Resource | Searched | Queries | Records | Observed barrier |
|---|---|---:|---:|---|
| PubMed | TRUE | 31 | 12 | — |
| Europe PMC | TRUE | 24 | 12 | The Europe PMC REST API itself was fully usable - no login wall, CAPTCHA, rate limit or API error at any point across 24 queries. The search endpoint, |
| OpenAlex | TRUE | 44 | 12 | PARTIAL BARRIER, resource still searched. OpenAlex now meters its API by credit budget. Every list/search call (/works?search=, /works?filter=) costs  |
| Semantic Scholar | TRUE | 17 | 12 | PARTIAL BARRIER — HTTP 429 rate limiting on the unauthenticated Semantic Scholar Graph API shared pool. Exact response body, returned on the very firs |
| ResearchRabbit | FALSE | 7 | 0 | HARD LOGIN WALL, not circumventable without creating credentials. Three independent confirmations: (1) Every search endpoint returns HTTP 401 {"reason |
| Undermind | FALSE | 11 | 0 | AUTHENTICATION WALL — no query ever reached Undermind's index. Three independent routes tried, all rejected before any search ran. (1) MCP server: POS |
| Elicit | FALSE | 5 | 0 | BLOCKED ON BOTH ROUTES - no query ever returned results, so nothing is reported.  ROUTE 1, web UI (Cloudflare browser check). GET https://elicit.com/s |
| Consensus | FALSE | 7 | 0 | TWO INDEPENDENT BARRIERS, neither circumventable under the hard rules.  (1) WEB UI — Cloudflare interactive browser check. Every content path returns  |
| GEO — NCBI Gene Expression Omnibus | TRUE | 45 | 11 | PARTIAL BARRIER (worked around, not blocking). The GEO web UI accession pages are protected by a Google reCAPTCHA interstitial for non-browser clients |
| SRA | TRUE | 60 | 3 | — |
| PRIDE | TRUE | 71 | 2 | — |
| ProteomeXchange / ProteomeCentral | TRUE | 66 | 2 | — |
| BioStudies | TRUE | 67 | 12 | — |
| ArrayExpress in BioStudies | TRUE | 58 | 3 | — |
| ClinicalTrials.gov | TRUE | 26 | 12 | No access barrier: the API v2 was reachable throughout (HTTP 200, apiVersion 2.0.5, dataTimestamp 2026-10-02), no login wall, CAPTCHA or rate limit wa |
| Comparative Toxicogenomics Databas | TRUE | 24 | 7 | PARTIAL BARRIER. Every interactive and API endpoint under ctdbase.org is behind an ALTCHA proof-of-work human-verification wall: GET /tools/batchQuery |
| ICE — NIEHS Integrated Chemical En | TRUE | 14 | 1 | None. No login, no CAPTCHA, no credential wall. Two non-blocking issues, both worked around and both recorded: (1) the GET endpoint rate-limits — six  |
| ToxCast / EPA CompTox | TRUE | 12 | 3 | PARTIAL BARRIERS (worked around; did not prevent the search). (1) api-ccte.epa.gov:443 — the official EPA CCTE REST API — is blocked by this session's |
| Zenodo | TRUE | 52 | 5 | — |
| Dryad | TRUE | 62 | 1 | Two-layer barrier, affecting FILE DOWNLOADS ONLY — the search API and all dataset/file metadata were fully readable, so this resource counts as genuin |


### 4.1 What the blocked four actually returned

- **ResearchRabbit** — every search endpoint returns HTTP 401; no anonymous route exists.
- **Undermind** — authentication wall; three routes tried, all rejected before any query ran.
- **Elicit** — Cloudflare browser check on the UI and authentication on the API.
- **Consensus** — Cloudflare interactive check plus API authentication.

These are **discovery aids, not primary evidence**, so the loss is of recall, not of
verifiable records. Creating accounts would have meant accepting terms on Oscar's behalf,
which this round does not authorise. If Oscar wants them covered, that is a credential
decision, not a research one.

### 4.2 Additional sources searched beyond the twenty

ClinicalTrials.gov **posted results and sponsor protocol/SAP documents** (the richest find
of the round — sponsor protocols carry a Chemistry section), Drugs@FDA review packages, EMA
EPAR quality sections (which closed the purity gap from documents already held), DailyMed
SPL DESCRIPTION sections, MeSH/CTD systematic-name records (which encode full sequence and
uniform-PS backbone for four first-generation compounds), and PMC author manuscripts for
paywalled journal articles.

---

## 5. Paper, supplement and data-access table

Full table with all fields: [`research/2026-10-02/acquisition_plan.csv`](research/2026-10-02/acquisition_plan.csv).
The six critical entries, and what each would actually add:

| Record | Identifier | Required file | What it closes | Expected yield | Access |
|---|---|---|---|---|---|
| 2′MOE ASOs activate human platelets via GPVI | PMID 33567808 / PMC8804562 | Main text; per-compound GPVI KD panel; 7-donor responsiveness correlation | Human in vitro assay on five named PS ASOs, three clinically dosed, with donor-level variance | 5 ASOs × (GPVI KD, P-selectin, platelet–leukocyte aggregates) | open access |
| Single-stranded oligo effects in vitro | PMID 29107969 / PMC5673186 | Main text **plus all Supporting Information** — the construct panel with length and PS-linkage counts is in the SI | Converts "phosphorothioates activate platelets" into per-construct chemistry covariates in a human system | Unknown panel size; two continuous covariates (length, PS count) plus an LNA-wing effect | open access |
| Donidalorsen coagulation and fibrinolysis panel | PMID 35977698 / PMC9718591 | Table 1 in full (the Europe PMC record has no abstract) | The most complete human coagulation panel on a clinically dosed ASO, with numbers rather than AE terms | 22 HAE patients × 13 named assays × 2 timepoints | open access |
| Porcine vs ovine defibrotide | PMID 41869748 / PMC13009829 | Full text plus per-batch tables | **Human in vitro assay and tested-material characterisation at batch level simultaneously** | 28 API batches × 4 coagulation endpoints (~112 values) plus 28 × (MW, DNA content) | open access |
| ASO platelet activation in Göttingen minipig | PMID 37111598 / PMC10143489 | Main-text Tables 1 and 2 (not the supplement) | The only explicit **per-position chemistry** for 7 constructs plus a same-construct cross-species map | 7 constructs × (marked sequence, length 14–22, PS load 0–21) | open access, CC BY |
| Sheehan intrinsic-tenase pair | PMID 9716589, *Blood* 1998 | Both full-text PDFs via institutional access or document delivery | The purified-human-factor mechanism tier: localises PS aPTT prolongation to the FIXa–FVIIIa complex as allosteric, not polyanionic sequestration | ISIS 2302 concentration–response in human plasma plus mechanism parameters | **confirmed paywall** |

The three files Beebop named are all reachable, by a route the request did not anticipate:

- **ATLAS-A/B (NCT03417245)** — registry posted results are open; the trial carries no
  registry acronym, which is worth recording since "ATLAS-A/B" is sponsor usage.
- **APPROACH (ISIS 304801-CS6)** — has no posted protocol or SAP. The documented workaround
  is the **CS7 open-label-extension protocol** (NCT02658175), whose Chemistry section
  specifies the compound. That is a different study's document used as the chemistry source,
  and must be recorded as such.
- **Mipomersen CS5/CS7/CS12** — individual trial safety tables remain unposted; the pooled
  EMA analysis is what we hold, which is exactly the substitution that must stop.

**All three give architecture, not a printed base sequence.** Sponsor protocols specify
"20-mer, all phosphorothioate linkages, 5-nt 2′-MOE wings, 10-nt deoxy gap" plus target
coordinates. That satisfies position-level *chemistry* but not sequence, and the distinction
must survive ingestion.

---

## 6. Inaccessible material, classified

| Classification | Count | Examples and evidence |
|---|---:|---|
| **Confirmed paywall** | 5 | Sheehan 1998 *Blood* intrinsic-tenase pair (every open route tested failed; the top document-delivery priority); four further journal articles where no PMC deposit, author manuscript or repository copy exists |
| **Login or application access required** | 4 resources | ResearchRabbit (HTTP 401 on every search endpoint), Undermind, Elicit, Consensus. Not paywalls — credential walls. No account was created |
| **Technical blocking** | 4 | Cloudflare browser checks and HTTP 429 rate limiting (OpenAlex metering, Semantic Scholar unauthenticated limit, CTD interactive endpoints, Dryad file downloads). All worked around except where noted; the searches completed |
| **Missing supplement** | 2 | PMC5673186 and PMC4322051 construct panels live in Supporting Information that must be fetched separately from the main text |
| **Abstract only** | 13 | Records where only the abstract is reachable; none is counted as evidence |
| **Unresolved citation** | 0 | Every record in the plan carries a resolvable identifier |

No displayed price, subscription cost or institutional entitlement is reported, because none
was verified — and verifying one would have meant reaching a purchase flow. Where this report
says "confirmed paywall" it means **every open route was tested and failed**, not that a
price was seen.

**The one request to Oscar:** *Please provide the full text of Sheehan JP et al.,* Blood
*1998;92(5):1617 (PMID 9716589) and its companion.* It is needed because the dataset has no
purified-human-factor mechanism tier at all — it would convert "phosphorothioates prolong
aPTT" from an observation into a localised mechanism (allosteric inhibition of the FIXa–FVIIIa
intrinsic tenase complex), which is the kind of evidence a predictive model can use as
structure. Every open route was tested: no PMC deposit, no author manuscript, no repository
copy. The main article alone is sufficient; the supplement is not required.

---

## 7. What needs whose decision

### Oscar's (implementation and scope)

1. **Ingestion of the acquisition plan.** Nothing from §3.1/§5 has been ingested. The six
   critical entries are open access and would add human in vitro assays with chemistry — the
   shape Phase 2 names as of particular interest. This is a new work package, not covered by
   the 2026-10-03 authorisation, because it changes the human-subset totals.
2. **Whether to quote 46 externally.** It is QC-reproducible, carries no flagged clusters and
   supersedes 30 in every document in the folder. My recommendation: usable internally and
   with the challenge submission; still worth German's eye on the 23 single-record trials
   before it goes anywhere public (see German's item 5).
3. **One paywalled file** — the Sheehan request above.
4. **Whether to create accounts** for the four blocked discovery tools. That accepts terms on
   your behalf, so it is yours, not mine. My view: low value, since they are discovery aids
   and the primary archives were all searchable.
5. **Who owns the cross-endpoint source manifest.** Several records are shared with
   thrombocytopenia and complement. Three sessions maintaining three manifests will diverge.

### German's (scientific adjudication)

1. **The 4-of-5 source-versus-curator grade disagreements** (`COG-MSR2636`–`2640`). The whole
   calibration set, mostly failing. Until adjudicated, the curator scale must not be presented
   as agreeing with source severity.
2. **The 132 participant rows carrying both axes TRUE.** For a factor-lowering drug, bleeding
   is either the mechanism working or the harm, and only a clinician can decide per arm.
3. **The 2 rows with a source-reported grade 3 and `unintended_toxicity = FALSE`**
   (`COG-MSR0346`, `COG-MSR2458`). The notes defend both, but a source grading something 3
   while the dataset says "not unintended" needs a scientist's signature.
4. **The 3 unsupported attributions** (`COG-MSR0608/0609/0610`).
5. **The 23 headline trials resting on a single source record** — half the total.
   `COG-STU053`, `054`, `055`, `056`, `075`, `076`, `083`, `084`, `085`, `100`, `101`, `104`,
   `108`, `111`–`115`, `145`, `170`, `205`, `209`, `210`. Each is identified and
   endpoint-evaluable, so each is correctly in the total by the stated rule, but each rests on
   one document and none has independent corroboration. This is the largest single reservation
   on the figure of 46 and it is stated here rather than buried: a count of 46 is reproducible,
   not independently corroborated throughout.
6. **Whether a pooled analysis may ever count toward a human-trial total** for this
   challenge. The register says no; that is a curator rule, not an adjudication.

---

REVIEW COMPLETE — AWAITING OSCAR'S AUTHORISATION FOR INGESTION
