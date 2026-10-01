# OligoTox research access register

Updated: 2026-10-01. Prepared by Beebop at Oscar's request.

Purpose: track needed papers, supplements, and structured files; distinguish confirmed paywalls from other acquisition gaps; give Oscar a specific, prioritized document request when necessary.

This reference does not authorize changes to endpoint data, scientific labels, models, or the existing Rocksteady proposals. No author contact, purchase, subscription, or dataset modification was made for this update.

## Status definitions

| Status | Meaning |
|---|---|
| Confirmed paywall | An identified required file is blocked by an observed payment/subscription barrier. Document the barrier and attempted legitimate alternatives. |
| Reported paywall; recheck needed | An earlier session reported a paywall; current access and free alternatives have not been established. |
| Free route identified; technical access blocked | A public full-text route exists, but the current retrieval attempt hit a browser check or another technical obstacle. |
| Free main text read; supplement pending | The article can be read, but required supplementary files have not been obtained or evaluated. |
| Login or application access required | Access needs an account or application action; this is not evidence of a paid subscription. |
| Supplement or structured file missing | The needed file has been identified but is not in the reviewed package; cause of absence remains undetermined. |
| Citation unresolved | Source identity is insufficient or inconsistent; resolve it before requesting payment or treating it as evidence. |
| Acquired | The exact required file is held and its identity/version recorded. Acquisition is distinct from scientific verification. |

## Confirmed paywall requests ready for Oscar

No new request is classified as confirmed in this update. The existing kidney list reports paywalls, but spot checks found free alternatives. The remaining entries below are retained as candidate access gaps rather than falsely certified paywalls.

## Corrections to the existing kidney access list

Baseline: [`toxicity/kidney/SOURCES_TO_ACQUIRE.md`](toxicity/kidney/SOURCES_TO_ACQUIRE.md), read at commit `a7e9d1bb907ac9fd799ab25aedd1183e8ea06d64`. That file was not edited.

| Paper / study | Affected record / area | Current access finding | Still needed | Priority |
|---|---|---|---|---|
| Vupanorsen 2022 randomized study, public archive identifier `PMC9047643` | Kidney `MSR079`; potentially liver evidence after endpoint review | Free route identified at https://pmc.ncbi.nlm.nih.gov/articles/PMC9047643/ ; direct open hit a browser check. The previous journal-homepage link was inadequate. | Acquire article and relevant safety supplements; verify the exact row-to-source mapping. | High |
| Teprasiran 2021 randomized clinical study, identifier 10.1161/CIRCULATIONAHA.120.053029 | Kidney `MSR077` | Free route identified at https://pmc.ncbi.nlm.nih.gov/articles/8487715/ ; direct open hit a browser check. | Acquire article/supplements; distinguish therapeutic renal benefit from evidence of absence of toxicity. | High |
| Tofersen 2022 trial, identifier 10.1056/NEJMoa2204705 | Kidney `MSR042`; chronic neurotoxicity and hydrocephalus | Free published article opened and read at https://eprints.whiterose.ac.uk/id/eprint/193004/1/Miller%20et%20al%202022.pdf . Full text is not blocked by a paywall through this route. | Supplementary appendix and protocol still require separate checking; no endpoint extraction was performed in this update. | High |

The tofersen article identifies the parent trial `NCT02623699` and extension `NCT03070119` together, describes the extension, and reports participant rollover. This is a specific source lead for the neurotoxicity parent/extension gap, not permission to sum their participants or events. See the abstract and trial-design sections. The repository copy's availability does not grant unrestricted redistribution.

## Previously reported paywall candidates: not yet request-ready

These source labels and identifiers are carried from Rocksteady's kidney access list. Their citation identity, present access conditions, and supplement availability need verification before a purchase or upload request. The reported barrier is attributed to Rocksteady; it was not reconfirmed here.

| Candidate | Link from the existing list | Affected record | Needed content / purpose | Priority |
|---|---|---|---|---|
| Mongersen clinical paper | https://doi.org/10.1056/NEJMoa1407250 | `MSR056` | Safety tables and supplementary appendix to verify the renal claim. Direct publisher opening in this update returned a technical error, which does not establish a paywall. | High |
| Olpasiran dose-ranging clinical paper | https://doi.org/10.1056/NEJMoa2211023 | `MSR065` | Renal safety tables and appendix. Direct publisher opening returned a technical error, not confirmed payment gating. | High |
| Donidalorsen clinical paper | https://doi.org/10.1056/NEJMoa2402478 | `MSR067` | Verify citation first, then safety tables and appendix. | High |
| Patisiran clinical paper | https://doi.org/10.1056/NEJMoa1716153 | `MSR044` | Verify the drug/record mapping before extracting renal outcomes; source-list association is not accepted automatically. | High |
| Pelacarsen phase-two clinical paper | https://doi.org/10.1056/NEJMoa1905239 | `MSR063` | Primary clinical report and renal safety appendix, distinct from secondary summaries. | High |
| Yu et al. 2012, monkey study of compound ISIS 113715 | https://doi.org/10.1016/j.tox.2012.06.014 | `OLG025` | Sequence and source outcome; animal-support evidence only. | Lower than eligible human evidence |

The prior "alicaforsen review" entry has no exact citation and remains **citation unresolved**, not a confirmed paywall request. The named vutrisiran and fitusiran trials also need exact paper identities and required-file definitions before an access request can be prepared.

## Identified missing data files, with no confirmed paywall cause

| Source / file | Area | Why it matters | Access status |
|---|---|---|---|
| Goodchild 2009 supplementary sequence spreadsheet; https://doi.org/10.1186/1471-2172-10-40 | Immunotoxicity | German's memo identifies the complete 207-sequence screen as supplement-dependent. | Missing in the reviewed evidence package; access cause not determined. |
| Valentin 2021 supplementary tables S1/S2; https://doi.org/10.1093/nar/gkab451 | Immunotoxicity | Complete sequence and modification matrix; link each construct to its experiment. | Missing in the reviewed package; access cause not determined. |
| SafeSense treatment-level file, identified in German's version 0.10 memo as `mmc4.csv`; https://doi.org/10.1016/j.omtn.2026.103035 | Thrombocytopenia and other human safety endpoints | Structured treatment records for staged acquisition, duplicate-study reconciliation, and later scientific review. | Not present in the reviewed package. Application/data-file access must be checked separately; no paywall established. |
| Sewing 2017 supplementary spreadsheet S1 | Thrombocytopenia | Raw source measurements and construct/condition mapping. | German's package flags missing acquisition; exact source/file route still needs reconciliation. |
| Hagedorn 2013 supplementary material named in the hepatic dossier | Hepatotoxicity | Source-level sequences/outcomes and lineage of reused compound panels. | Citation and file route need verification; absence is not proof of a paywall. |
| Actual Hornung 2005 article, replacing the misnamed file identified by German | Immunotoxicity | German's memo says the file named Hornung 2005 contains a different paper. | Source-identity mismatch; verify the intended publication before acquiring it. |

## Entry requirements for future identified-but-unreachable papers

Each entry should retain:

- Exact title, authors, year, persistent identifier, and publisher/repository link.
- Toxicology, affected record identifiers, and the specific gap it would close.
- Required object: main paper, supplement, protocol, raw spreadsheet, or another named file.
- Evidence that the needed data may exist there; distinguish explicit references from speculative leads.
- Species and evidence class, with human trial priority separate from human laboratory value.
- Access attempts, date checked, observed barrier, and legitimate alternative locations checked.
- Priority, expected value, request to Oscar, responsible reviewer, and current status.
- After acquisition: filename, version, file hash, source location, and verification status.

A request to Oscar should be specific: "Please provide [exact paper/file] for [endpoint]. It is needed to verify [specific records or missing data]. We checked [routes] and observed [barrier]. The main article alone is/is not sufficient."

This register does not claim that every known access gap has been rechecked. In particular, the older kidney list also contains open-access papers and regulator-hosted documents blocked by technical access conditions; those must not be relabeled as paywalled. Its cemdisiran paper was subsequently reported as read in Rocksteady's response, so even its acquisition status requires reconciliation before another request.
