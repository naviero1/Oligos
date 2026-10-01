# OligoTox research-source compendium

Updated: 2026-10-01. Prepared by Beebop at Oscar's request.

This is a shared reference directory, not a new instruction to implement toxicology changes. Endpoint proposals remain subject to Oscar's approval. The 20 resources below preserve Oscar's supplied list; the proposed uses distinguish discovery services, original data archives, and contextual evidence.

Related reference: [research access register](RESEARCH_ACCESS_REGISTER.md), including papers reported as paywalled, alternative access routes, and missing supplements. Finding a resource does not mean that its data have been acquired or scientifically qualified.

## Papers and discovery

| Resource | Link | Proposed use in this challenge | Interpretation / access note |
|---|---|---|---|
| PubMed | https://pubmed.ncbi.nlm.nih.gov/ | Identify biomedical primary studies and resolve citations. | Citation records can link to freely accessible or publisher-hosted articles. An abstract is not the underlying experiment table. |
| Europe PMC (PubMed Central) | https://europepmc.org/ | Find full text, supplementary material, citation links, and deposited-data leads. | Availability varies by article and file. Record the original publication and supplement, not just the discovery page. |
| OpenAlex | https://openalex.org/ | Discover related works, citation networks, and alternative locations for a paper. | A catalog record is not evidence that the full text or supplements are available. |
| Semantic Scholar | https://www.semanticscholar.org/ | Find related papers, citations, and full-text routes. | Verify generated summaries against the primary article. |
| ResearchRabbit | https://www.researchrabbit.ai/ | Expand from a verified seed paper through connected literature. | Citation-network discovery can overrepresent well-connected research; retain a separate endpoint and compound search. |
| Undermind | https://www.undermind.ai/ | Explore narrow scientific questions and follow literature trails. | Assisted discovery; returned conclusions require primary-source verification. Access to a search product does not purchase publisher rights. |
| Elicit | https://elicit.com/ | Screen literature and organize candidate extraction questions. | Suggested extractions remain provisional until checked against exact source locations. |
| Consensus | https://consensus.app/ | Discover candidate papers and orient an evidence question. | Use the underlying study for dataset entries. A synthesized answer is not a toxicity label. |

## Research data and supporting resources

| Resource | Link | Proposed use in this challenge | Qualification needed |
|---|---|---|---|
| GEO (Gene Expression Omnibus) | https://www.ncbi.nlm.nih.gov/geo/ | Locate expression experiments, sample metadata, processed measurements, and deposited study files. | Confirm the actual tested oligonucleotide, species, exposure, and endpoint. |
| SRA (Sequence Read Archive) | https://www.ncbi.nlm.nih.gov/sra | Recover raw high-throughput sequencing data associated with relevant experiments. | Sequenced biological samples are not automatically the sequence of the administered oligonucleotide. Intervention identity usually needs the methods, supplements, or another source. |
| PRIDE (Proteomics Identifications Database) | https://www.ebi.ac.uk/pride/ | Locate proteomics experiments relevant to mechanism or response. | Require explicit linkage to the tested construct and experimental conditions. Protein measurements do not automatically establish toxicity. |
| ProteomeXchange | https://www.proteomexchange.org/ | Find proteomics deposits across member repositories. | Deduplicate the discovery record and the underlying deposit; they are not two experiments. |
| BioStudies | https://www.ebi.ac.uk/biostudies/ | Find supporting files and links that connect a publication to its study data. | Check individual files, versions, sample annotations, and reuse conditions. |
| ArrayExpress, within BioStudies | https://www.ebi.ac.uk/biostudies/arrayexpress | Locate functional-genomics experiments, protocols, sample annotations, and raw/processed data links. | Avoid counting the same deposit again through another archive or publication. |
| ClinicalTrials.gov | https://clinicaltrials.gov/ | Establish study identity, interventions, arms, results, and parent/extension relationships where documented. | Registration alone does not establish an observed toxicity outcome. Keep registry protocols, distinct participant cohorts, and publications separate. |
| Comparative Toxicogenomics Database | https://ctdbase.org/ | Identify chemical–gene–disease relationships and source-publication leads. | Contextual or inferred relationships cannot replace observed, sequence-linked experimental outcomes. |
| ICE (Integrated Chemical Environment) | https://ice.ntp.niehs.nih.gov/ | Explore assay information, chemical-safety data, and methods. | Establish relevance to the particular oligonucleotide before treating any result as direct evidence. |
| ToxCast (Toxicity Forecaster) data | https://www.epa.gov/comptox-tools/exploring-toxcast-data | Explore assay definitions and chemical bioactivity data. | Broad chemical assays are not automatically a therapeutic-oligonucleotide toxicity dataset; verify tested substance identity. |
| Zenodo | https://zenodo.org/ | Find deposited datasets, code, and supplementary research outputs. | Record the precise version, source linkage, and license. Repository presence does not validate scientific quality. |
| Dryad | https://datadryad.org/ | Find study-associated datasets and supporting files. | Check the linked publication, data dictionary, experimental units, and reuse terms. |

## Proposed search order

1. Start with the specific gap: a missing sequence, position-level chemical map, raw endpoint, human trial identity, or characterization of the tested material.
2. Resolve the source publication and follow its own supplement and data-availability links.
3. Search publication identifiers, compound aliases, study identifiers, and dataset accessions in the relevant discovery services and archives.
4. Expand through citations when direct searches fail. Record unsuccessful routes so another session does not repeat the same access failure.
5. Rank acquisition by the number and importance of eligible human observations it could unlock. Preserve animal evidence as supporting material, excluded from human trial totals.

This ordering is a proposal for review, not evidence that a new literature search or dataset extraction has been completed.

## Evidence and sequence requirements to preserve

- Count verified, deduplicated human trials separately from human clinical measurements, human laboratory experiments, animal experiments, and papers.
- Record exact sequence, orientation, strand/duplex identity, position-specific chemistry, conjugates, and provenance. Keep published molecular identity distinct from analytical identity and purity of the tested batch.
- A base sequence shared by two chemically different constructs may justify a leakage group, but does not make the constructs experimentally interchangeable.
- Preserve raw outcomes and assay context. Missing reports are not negative outcomes. Intended therapeutic activity is not automatically adverse toxicity.
- Keep discovery summaries, reviewed source documents, extracted observations, scientific adjudication, and model eligibility as separate stages.
- Recover required characterization where possible and record missingness explicitly. Missingness tracking documents a gap; it does not close it.

## Access policy requested by Oscar

An identified, needed paper or supplement that cannot be accessed because of a paywall belongs in the access register. Beebop or Rocksteady may ask Oscar for that specific document, including why it matters. No purchase, subscription, or author/sponsor contact is implied by the request.

A useful request names the paper and identifier, the exact article/supplement/data file needed, the toxicology and affected records, the gap it could close, attempted legitimate access routes, the observed barrier, and priority. A price is recorded only if actually displayed, with the date.

Paywalls, account requirements, browser checks, broken links, unresolved citations, and missing supplements are separate conditions. An open article can still have an unavailable supplement. Finding a free reading copy does not establish redistribution permission.

## Verification notes

Resource landing pages were checked on 2026-10-01. Some pages required scripts or returned technical access errors; these were not classified as paywalls. Detailed search-product pricing and authenticated features were not evaluated.

Supporting official descriptions:

- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [Europe PMC (PubMed Central): supplementary-file discovery update](https://blog.europepmc.org/2026/01/europe-pmc-2025-a-year-in-review.html)
- [OpenAlex](https://openalex.org/) and [Semantic Scholar documentation](https://www.semanticscholar.org/product/api)
- [GEO (Gene Expression Omnibus) overview](https://www.ncbi.nlm.nih.gov/geo/info/overview.html)
- [SRA (Sequence Read Archive)](https://www.ncbi.nlm.nih.gov/sra)
- [ProteomeXchange mission and members](https://www.proteomexchange.org/)
- [BioStudies](https://www.ebi.ac.uk/biostudies/) and [ArrayExpress](https://www.ebi.ac.uk/biostudies/arrayexpress)
- [Comparative Toxicogenomics Database: resource-authored 2025 update](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701581/)
- [ICE (Integrated Chemical Environment) official description](https://ntp.niehs.nih.gov/whatwestudy/niceatm/comptox/ct-ice/ice)
- [ToxCast (Toxicity Forecaster) data documentation](https://www.epa.gov/comptox-tools/exploring-toxcast-data)
