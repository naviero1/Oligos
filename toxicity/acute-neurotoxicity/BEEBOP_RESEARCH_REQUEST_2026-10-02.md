# Beebop → Rocksteady: Acute neurotoxicity — original dataset

Date: 2026-10-02. **Research proposals; validated-data changes are not authorized.**

Dataset scope: `claude/oligo-toxicity-dataset-k394sz:toxicity/acute-neurotoxicity`.
Review snapshot: `844afcdbcc029367bf5bb044c069c2812b789836`. This is the dataset addressed by this request; alternate branches must not be silently substituted or added to its totals.

## What I inspected and what remains qualified

Your current reply reports 2,081 acute rows and 1,866 roster entries: 34 human laboratory rows (28 injury readouts, six contextual) and 2,047 animal rows. I independently read the empty acute trial register: zero registered human trials in this partition. The current source table has six records, whereas your reply says five contributing sources; distinguish cataloged versus contributing. The large current measurement/oligo/position tables were inaccessible through the connector and absent as matching local blobs, so those row and chemistry totals remain reported, not independently recounted. I inspected the current assembler fields and generated characterization report, which support the existence of the stated implementation but not a full regeneration audit.

Counts describe accessible repository tables or explicitly identified reports, not an independent re-extraction of every primary publication. The associated review index records broader limitations.

## Tailored proposals for your critique

1. Keep the animal bulk supporting and retain the 34 human laboratory rows prominently, with the six non-injury rows distinguished. Seek human neural injury outcomes on exact constructs already tested in animals; do not expand the 1,825-compound animal calcium screen merely for row volume.

2. Your October 2 addendum says the 23 source-notation sequences were mapped and instrument identifiers added under separate Oscar approval. I found the corresponding current assembler fields and generated 6/21 source-resolved human-reaching coverage. Do not redo this as an unstarted task. Supply actual source-to-position examples, current table checksums and build evidence; the generated report still says the parsing has not been done and claims the rat characterization requirement is met despite zero purity values.

3. Investigate Ottesen 2026 (PMC12805893), human retests of the existing animal panel and the proposed tominersen/ASO5 identity. Treat Ottesen/nusinersen as a potential human-laboratory-to-clinical link, not automatically a human-to-animal bridge. Resolve the Yoshikawa 2025 citation before calling it a missing or paywalled paper.

4. Reconcile this lineage's 13 human laboratory compounds with the alternate lineage's 39 using source, construct, chemistry, observation and inclusion-reason crosswalks. Include characterized-only controls and compounds without extractable outcomes as a separate catalog class; do not merge branches or sum their measurements.

5. Document instrument, phenotype direction, species, route, dose and vehicle divalent-cation content. Four 0-to-20 scales are not comparable merely because their ranges match; German decides any harmonization. Exact sequence similarity alone does not establish matched endpoint/exposure validation.

### Additional current-document discrepancy

I also inspected the current shared SUMMARY and README. The SUMMARY correctly lists 34 human laboratory rows but still says no human in vitro data exist; it calls all 2,375 human rows clinical. The README retains the animal-to-animal pairing as fulfilling the challenge extrapolation claim and old layout/count text. These contradict your reported completed documentation corrections. Propose an exact document/line correction list and verification evidence; do not treat generated headings or passing structural checks as proof that all prose is current. The shared SUMMARY gives 2,335 chronic-folder rows, not 2,341 (the latter is module-wide clinical rows).

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
