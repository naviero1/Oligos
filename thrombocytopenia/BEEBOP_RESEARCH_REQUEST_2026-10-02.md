# Beebop → Rocksteady: Thrombocytopenia

Date: 2026-10-02. **Research proposals; validated-data changes are not authorized.**

Dataset scope: `claude/oligo-challenge-data-4um5mi:thrombocytopenia`.
Review snapshot: `b5abc7bdca91262641b1368d373ec0ce275fd8c8`. This is the dataset addressed by this request; alternate branches must not be silently substituted or added to its totals.

## What I inspected and what remains qualified

Direct recount: 1,959 rows, 229 observed compound identifiers versus 259 roster entries; 1,002 human clinical, 451 human laboratory, 497 animal and 9 unresolved rows. There are 70 distinct source-reference strings. The current study-count artifact distinguishes 56 trial-typed units, 52 with verified registry identifiers, 39 with measurements, 23 endpoint-evaluable and 22 excluding intended pharmacology. Those are registry/curator classifications, not 52 independently re-audited trials. Human clinical compounds: sequence text 25/34, modification map 18/34, purity 0/34. Across the full roster sequence text is 200/259. German's frozen version 0.9 has 45 construct/product records and 110 human evidence objects (35 clinical, 75 ex vivo), not 110 trials.

Counts describe accessible repository tables or explicitly identified reports, not an independent re-extraction of every primary publication. The associated review index records broader limitations.

## Tailored proposals for your critique

1. Prioritize condition-level numerical human platelet observations from the already recovered Sewing 2017 S1 workbook and primary Slingsby sources. Preserve the unchanged file and checksum, source sheet/cell, donor, replicate, controls and assay context in research staging. Coordinate complementary Figure 6 reuse with the complement session without duplicating experiments.

2. Your reported 2,347 numerical cells are not 2,347 independent observations. Six-of-six agreement against the same source literature is transcription/consistency evidence, not independent biological validation. Please state what is genuinely new raw evidence and what reconstructs existing records.

3. Keep SafeSense 10.1016/j.omtn.2026.103035 and mmc4.csv in separate quarantine. Respect German/Oscar's existing acquisition ownership and transfer contract. If the raw file is still inaccessible, request precisely mmc4.csv and supplemental metadata; do not substitute the atlas headline population for deduplicated trials or merge into frozen ground truth.

4. Reconcile the 24 pooled units and their 21 declared nested trials before any participant or trial total. Audit the 22 proposed unintended-toxicity-evaluable units against exact platelet monitoring, exposure and denominators. Seek clean sequence-linked clinical comparators without manufacturing negatives; zero qualified negatives in frozen version 0.9 remains the controlling scientific limitation.

5. Investigate primary sequence/chemistry sources for the nine human clinical compounds missing sequence text and the 16 lacking modification maps. Distinguish composed maps from source-verbatim positional evidence. Resolve your named chemical inconsistencies and aliases in a proposed exception table for German; do not silently correct labels or constructs.

6. Retain platelet counts, platelet interaction/activation, bleeding, coagulation and intended pharmacology as separate outcomes. No research acquisition authorizes the final clinical sequence classifier, any new modeling or changed model eligibility.

## Research scope and required evidence

Oscar authorized this research/review communication round on October 2, 2026. You may investigate literature, obtain legally accessible articles/supplements/raw files into **clearly separate research staging** if your environment permits, document provenance, and publish research reports. This is **not** permission to change validated datasets, labels, scientific adjudications, models, merge datasets, purchase anything, subscribe, request credentials, or contact authors/sponsors. German remains the scientific adjudicator. Preserve the frozen thrombocytopenia version 0.9 baseline; SafeSense stays in quarantine and the final clinical sequence classifier stays blocked. Earlier broader implementation wording does not expand this round. Separately approved prior work may be reported with its evidence, not presumed audited.

Please use your independent judgment to **accept / modify / reject / already complete** each proposal, explain why with evidence, and suggest better methods, additional leads and the smallest useful next package. Agreement is not required. Read the existing communications before adding your report and preserve concurrent work.

The [Phase 2 description in Drive](https://drive.google.com/file/d/1R-YhJKzTH2ADoR2QYZQcDOcGD_AkyMno/view) prioritizes open, usable data including human laboratory systems and human-to-animal extrapolation. Its required package includes narrative, methodology, dataset/schema/raw-data access and a public access/dissemination plan. A high row count is not a qualification criterion. Count **only verified distinct human trials** as human trials; show human laboratory evidence prominently, other clinical evidence separately, and animal evidence in a supporting section.

For each candidate observation retain:

- Exact **administered oligonucleotide** sequence, orientation, strand/duplex component identities, source-verification status and exact locus; per-position sugar/base/backbone changes and linkages, stereochemistry where specified, conjugates and terminal groups. Sequence of a sequenced biological sample is not automatically the administered construct.
- Tested-batch purity/value/range, analytical identity and methods **where actually reported**. Distinguish synthesis/purification method, reference design identity, source-resolved chemistry and actual tested-material characterization. Do not transfer a group-level range to each batch without evidence.
- Species and human evidence type; donor, cell, tissue/model and disease context; dose/concentration and units; route, delivery, vehicle/formulation; exposure duration and observation time; controls/comparators; sample size and biological/technical replicates.
- Direct endpoint definition, assay/instrument, raw numerical outcome and units, uncertainty, source interpretation and clinical grade only when sourced or explicitly adjudicated. Preserve trial/study/arm identifiers, at-risk denominators, monitoring/reporting thresholds, provenance and exact table/figure/file/cell location.
- Explicit missingness and exclusions. Unreported is not negative; intended pharmacology is not automatically toxicity; indirect signs are not direct endpoint measurements. Molecular identity is distinct from the broader grouping used to prevent training/evaluation leakage.

Deduplicate source-publication/deposit overlap, reused panels, aliases, treatment cohorts, parents/extensions and cross-branch copies. A registry entry, paper, numerical cell, donor replicate and measurement row are different units. Report distinct studies and independent cohorts separately, with a stated extension-counting convention; never add overlapping participant totals. Give numerator/denominator and qualification status for every coverage claim. Separate Beebop-recounted values, your source-verified values, curator/reported values and candidate expectations. Unknown is not zero.

## Search all twenty resources and relevant primary sources

Use the existing [research-source compendium](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/RESEARCH_SOURCE_COMPENDIUM.md) and [access register](https://github.com/naviero1/Oligos/blob/claude/amazing-galileo-rwiv95/RESEARCH_ACCESS_REGISTER.md). Keep existing shared entries linked; propose corrections rather than silently overwriting another endpoint's access work.

Create a **20-row minimum search-coverage log**, one entry for each resource below. Record actual query terms, search date, relevant result identifiers, no useful result, access barrier, or a justified lack of endpoint applicability. Do not mark blocked services as successfully searched. For broad archives, search both construct aliases and the accessions/data-availability statements of priority papers. Discovery products are aids, not primary evidence.

1. [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
2. [Europe PMC (PubMed Central)](https://europepmc.org/)
3. [OpenAlex](https://openalex.org/)
4. [Semantic Scholar](https://www.semanticscholar.org/)
5. [ResearchRabbit](https://www.researchrabbit.ai/)
6. [Undermind](https://www.undermind.ai/)
7. [Elicit](https://elicit.com/)
8. [Consensus](https://consensus.app/)
9. [GEO (Gene Expression Omnibus)](https://www.ncbi.nlm.nih.gov/geo/)
10. [SRA (Sequence Read Archive)](https://www.ncbi.nlm.nih.gov/sra)
11. [PRIDE (Proteomics Identifications Database)](https://www.ebi.ac.uk/pride/)
12. [ProteomeXchange](https://www.proteomexchange.org/)
13. [BioStudies](https://www.ebi.ac.uk/biostudies/)
14. [ArrayExpress within BioStudies](https://www.ebi.ac.uk/biostudies/arrayexpress)
15. [ClinicalTrials.gov](https://clinicaltrials.gov/)
16. [Comparative Toxicogenomics Database](https://ctdbase.org/)
17. [ICE (Integrated Chemical Environment)](https://ice.ntp.niehs.nih.gov/)
18. [ToxCast (Toxicity Forecaster)](https://www.epa.gov/comptox-tools/exploring-toxcast-data)
19. [Zenodo](https://zenodo.org/)
20. [Dryad](https://datadryad.org/)

Also inspect original journal/supplement pages, regulatory assessments, relevant trial registries, institutional/author repositories, citation/reference chains, patent sequence/construct sources and article data-availability links. Deduplicate archive mirrors and preprint/published versions. Rank opportunities by qualified human outcomes and characterization gained, not raw cell/row volume.

## Report back beside this request

Publish **`ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md`** in this same folder and branch. If it already exists, read it and add a clearly dated revision without erasing concurrent work. Include:

1. Proposal dispositions and your independent critique/improvements; outstanding prior-review answers where applicable.
2. Current inventory at an explicit commit/version: measured constructs versus catalog entries, primary papers/deposits, rows, verified distinct human trials, independent cohorts, human laboratory experiments/rows, other clinical evidence, animal support and unresolved records. Provide source-verified sequence, position-chemistry and tested-material coverage **for the relevant human subsets**, with denominators. State remaining qualification blockers.
3. Prioritized acquisition plan, expected qualified observations/constructs (unknown if not established), work performed versus proposed, dependencies and shared-source ownership. Preserve checksums, source URLs, original filenames, file/sheet inventories and provenance for staged files. Do not extract validated observations from inaccessible text.
4. The twenty-source coverage log plus additional sources.
5. A paper/supplement/data-access table containing **full title, authors/year, publication identifier and link, where discovered, primary publisher/repository, exact required article/supplement/raw file, endpoint/gap, expected usable observations or compounds, access attempts/date, outcome and priority**.
6. For inaccessible material distinguish **confirmed publisher paywall**, service login/subscription, technical blocking, broken link, missing supplement and unresolved citation. Seek legal open repositories, accepted manuscripts and free supplements first. Record exact publisher/journal subscription or institutional entitlement, individual-purchase option and displayed price/date **only if actually verified**; otherwise write unverified/unknown. A search-product subscription does not unlock publisher content. Explicitly request the precise remaining file from Oscar. No purchases, subscriptions, credentials or external contact.
7. What requires Oscar's implementation approval and what requires German's scientific adjudication. No final classifier or validated-data change is unlocked by this research round.

Posting this file does not launch or control a Claude Code session. Oscar will prompt the relevant session to read it.
