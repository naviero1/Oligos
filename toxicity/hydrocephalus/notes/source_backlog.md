# Source backlog — retrieved and verified, NOT yet extracted

A multi-modal source-discovery pass (8 blind sweeps, 4 completeness critics and 12 gap-fills, 24 agents) returned 188 unique sources. The release extracts 53 of them. The 100 listed here were **retrieved and inspected by the discovery pass and are not carried in `data/` under their own `source_id`**, and are recorded so that the gap is visible rather than silent.

Read "not extracted" carefully: some entries are *partially* covered already. The SMA incidence cohort contributes 3 rows here but its by-sex and by-age strata were not taken; the FAERS entries overlap the 456 aggregate rows in `data/` but add case-level detail (report ids, ages, outcomes) that is not carried. Others — EudraVigilance, WHO VigiBase, the EMA CHMP assessment reports, the FDA pharmacology/toxicology reviews, the PMDA documents, the two patent families — are genuinely absent in every form. `notes/source_backlog.csv` carries the same list with retrieval routes, exact loci and per-source caveats.

Estimated yield if all were extracted: roughly **1,076 further measurement rows**, more than the current release — though that figure double-counts wherever a backlog entry overlaps rows already present. Their absence is a completeness limit, not a quality one: nothing in `data/` depends on them.

These estimates are the discovery agents' own, not verified here. Nothing in this file is evidence for any claim; it is a work list.

## Highest priority

| Tier | Type | Source | Est. rows | Rights |
|---|---|---|---:|---|
| A | pharmacovigilance | EudraVigilance DAP — per-PT outcome, reporter-qualification and age/sex breakd (`EMA DAP analyses /shared/PHV DAP/DAP/DAP_Ind`) | 140 | cc_by |
| A | pharmacovigilance | WHO VigiBase via VigiAccess — reported ADR counts by MedDRA SOC and PT for 14  (`VigiAccess (Uppsala Monitoring Centre) Fable`) | 110 | verify |
| A | pharmacovigilance | EudraVigilance Data Analysis System (DAP) — substance-level reaction PT case c (`EMA DAP Substance High Level Code 12676156 (`) | 77 | cc_by |
| A | pharmacovigilance | openFDA FAERS — nusinersen (SPINRAZA) Tier A hydrocephalus / ventricular case  (`FAERS safetyreportid: 13565474, 13711639, 13`) | 37 | public_domain |
| A | pharmacovigilance | openFDA FAERS route-controlled comparison of hydrocephalus and CSF-dynamics pr (`openFDA drug/event endpoint, no publication `) | 32 | public_domain |
| A | background_incidence | The incidence of hydrocephalus among patients with and without spinal muscular (`PMID 33962637 / PMCID PMC8105953 / DOI 10.11`) | 24 | cc_by |
| A | regulatory_label | Qalsody (tofersen) — CHMP Assessment report, EPAR public assessment report (`EMA/276404/2024 · Procedure No. EMEA/H/C/005`) | 24 | cc_by |
| A | pharmacovigilance | FDA SrLC dated negative audit across 22 oligonucleotide therapeutics — nusiner (`FDA SrLC DrugNameIDs: nusinersen 1373, etepl`) | 22 | public_domain |
| A | pharmacovigilance | openFDA FAERS — tofersen (QALSODY) Tier A + Tier B CSF case series (`FAERS safetyreportid: 23343319, 23608436, 23`) | 21 | public_domain |
| A | pharmacovigilance | openFDA FAERS — 20-oligo drug-level hydrocephalus-family count matrix with den (`openFDA FAERS aggregate, 20 oligonucleotide `) | 20 | public_domain |
| A | background_incidence | Macrostructural Brain Abnormalities in Spinal Muscular Atrophy: A Case-Control (`PMID 39308455 / PMCID PMC11415185 / DOI 10.1`) | 20 | cc_by_nc |
| A | nonclinical_invivo | NDA 206488 EXONDYS 51 (eteplirsen) Pharmacology/Toxicology NDA Review and Eval (`NDA 206488 Orig1 s000 PharmR; SHA256 b73fc7e`) | 18 | public_domain |
| A | regulatory_label | Spinraza (nusinersen) — CHMP Assessment report for the 28 mg / 50 mg line exte (`EMA/CHMP/379593/2025 · Procedure No. EMEA/H/`) | 15 | cc_by |
| A | nonclinical_invivo | Preclinical evaluation of antisense oligonucleotide therapy in a mouse model o (`PPR1113960 / PMC12637667 / DOI 10.1101/2025.`) | 14 | derived_features_only |
| A | clinical_trial_AE | Tau-targeting antisense oligonucleotide MAPTRx in mild Alzheimer's disease: a  (`PMID 37095250; PMCID PMC10287562; DOI 10.103`) | 12 | cc_by |
| A | clinical_trial_AE | Efficacy and Safety of AP 12009 in Adult Patients With Recurrent or Refractory (`NCT00761280`) | 12 | public_domain |
| A | clinical_case_report | Antisense oligonucleotide-mediated knockdown therapy in two infants with sever (`PMID 41981306 / PMC13099374 / DOI 10.1038/s4`) | 10 | derived_features_only |
| A | pharmacovigilance | openFDA FAERS — measured-zero negative control set (10 oligonucleotides) (`openFDA FAERS negative results across eplont`) | 10 | public_domain |

## What the completeness critics said was still missing

- **EMA EPAR **Assessment Reports** (scientific discussion + RMP) were never retrieved — the sweeps stopped at EPAR *Product Information* (the SmPC/Annex ** — This is the single highest-value missing modality. It supplies (a) a regulator-adjudicated Tier A statement that hydrocephalus is a recognised *class* risk of intrathecal ASOs — something no source in the inventory provi
- **FDA Drugs@FDA **review packages** (Integrated Review, Multi-discipline Review, Pharmacology/Toxicology Review, Summary Review) were never retrieved. A** — FDA reviewer documents are the only public place where the sponsor's *primary* safety adjudication is re-derived independently, with denominators, per-arm counts and the reviewer's causality reasoning — richer and differ
- **ClinicalTrials.gov **attached large documents** (Study Protocol, SAP, and where posted the redacted CSR) were never downloaded — all 29 ctgov_*.json f** — The protocol is the only document that states what was *scheduled to be measured* — MRI ventricular-volume acquisition timepoints, the hydrocephalus safety-monitoring and dose-interruption/stopping rules, and the amendme
- **No **time-resolved label history**: the inventory has only the current DailyMed SPL (Spinraza SPL v21, Apr 2026) and the current EU SmPC, so the date ** — It converts a single static 'label mentions hydrocephalus' row into a dated causal-adjudication timeline (first FAERS reports -> US 6.3 Postmarketing addition May 2018 -> MHRA DSU Sept 2018 -> EU SmPC 4.4/4.8 wording), a
- **Every FAERS query in the inventory is **drug-list-driven** (20 named oligos, each probed for hydrocephalus PTs). The inverse query — reaction-first, e** — A list-driven sweep can only confirm the hypotheses that built the list; it cannot discover a new drug. Since 5,367 FAERS reports carry the HYDROCEPHALUS PT (already in the inventory as a denominator), one aggregation ov
- **openFDA FAERS is the **only** spontaneous-report database used. Three other national/global systems, each with different reporter populations and none** — The hydrocephalus signal for nusinersen was first acted on in Europe (MHRA DSU Sept 2018, EU DHPC), not the US, which means the EU spontaneous-report corpus is the one most likely to hold cases the US database never rece
- **The **EU Clinical Trials Register (EudraCT)** was never queried, so EU-registered oligonucleotide trials and EU-posted result sets are entirely absent** — EudraCT AE tables are populated from a separate sponsor submission with different MedDRA coding decisions and different arm pooling than ClinicalTrials.gov, so per-arm counts can and do diverge — and where they diverge, 
- ****Patent literature was never searched** — no espacenet/Google Patents/PatentsView call appears anywhere in the 93-source inventory or the raw directo** — This dataset is explicitly 'sequence-and-design-resolved', and a large fraction of the oligos already in the inventory have an outcome but NO disclosed sequence or chemistry — valeriasen/KT777 and its nine congeners, jac
- **Regulatory **safety communications and adjudication meetings** are represented by exactly one item in the whole inventory (the MHRA Drug Safety Update** — These are the documents in which a regulator or an independent monitoring committee states a causal judgement and a date — the tominersen iDMC halt is the direct cause of the 'regression of ventricular increases after do
- **Preprint servers were never queried at their own APIs — the one preprint in the inventory (Research Square PPR1031561) arrived incidentally via Europe** — The tominersen ventricular-volume dataset and the GENERATION HD1 post-hoc imaging analyses were presented at CHDI/AAN well before and in more granularity than the journal record the inventory relies on (a 2023 'Clinical 
