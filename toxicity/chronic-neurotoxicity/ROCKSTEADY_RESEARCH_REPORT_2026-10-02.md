# Rocksteady → Beebop: research report, 2026-10-02 round

**Branch:** `claude/oligo-toxicity-dataset-k394sz` · **Dataset:** 4,428 measurements / 1,879
oligonucleotides / 9 sources · **47/47 QC checks pass** · **44 artefacts byte-identical across two
full runs**

Scope respected: this round authorised research, literature assessment and reports — not dataset
merges, label changes, model changes or lineage consolidation. None of those was done. The
documentation repairs below were separately authorised by Oscar on 2026-10-02.

---

## 1. Yoshikawa 2025 — resolved, and I was wrong

You asked me to resolve this before calling it missing or paywalled. You were right to.

**It exists.** My four Europe PMC queries returned nothing because **Europe PMC does not index it**.
Crossref does:

> Yoshikawa K, Kato Y, Takizawa M, Aruga C, Kagawa T, Uchibayashi N, Nagafuku N, Ishibashi Y,
> Matsuda N. *Development of an in vitro screening assay to predict acute CNS toxicity induced by
> antisense oligonucleotides and mechanistic exploration of its toxicity.*
> **J Pharmacol Toxicol Methods** 2025;135:107844. **doi:10.1016/j.vascn.2025.107844**

The DOI prefix is `j.vascn`, not a title I could guess from. **My earlier statement that the record
could not be confirmed to exist was wrong**, and the correction matters: it is a real, citable
paper, and it is the closest published work to this module's subject that I have found.

**It is genuinely paywalled** — Elsevier, TDM user licence, no open-access deposit. So "paywalled"
was right for the wrong reason.

**Access request.** Title, journal, volume and DOI above. Needed because it is an *in vitro
screening assay for ASO CNS toxicity with mechanistic work* — if its assay is human-derived it is
directly the Challenge's priority data class. I cannot determine human versus rodent from metadata
alone. Barrier: confirmed publisher paywall, not a login wall or a browser check.

## 2. Ottesen 2026 — investigated, and I am retracting my own recommendation

I told you and Oscar this was the highest-value lead, on the grounds that its F18MOE is sequence-
and chemistry-identical to nusinersen and so would bridge human laboratory to human clinical on one
molecule. **I retrieved the full text (PMC12805893, CC BY, 194 kB JATS) and that recommendation was
wrong.**

| readout searched for | occurrences in full text |
|---|---:|
| splicing | 146 |
| RNA-seq / transcriptome | 29 / 20 |
| cytotoxicity, viability, apoptosis, caspase, MTT, CellTiter, LDH, cell death | **0 each** |
| "toxicity" | 3 — all in discussion or reference titles, none a measurement |

**It contains no toxicity readout at all.** It is a transcriptome and splicing perturbation study.
Under this module's own rule that is `off_target_expression` — context, not injury — the exact
class I separated off the toxicity axes this week.

It remains worth ingesting as **context** on a marketed CNS compound in a human cell line, and the
compound identity claim holds. It does **not** close the human in vitro toxicity gap, and I should
not have said it would before reading it.

## 3. The 13-versus-39 crosswalk

Not performed: it needs the alternate branch's tables and this round does not authorise reading
across lineages for consolidation. What your audit already resolves is the headline — your figures
give the alternate corpus **13/39 with sequence text**, against **8/13** here. So the gap is
substantially a *counting-convention* difference, not a 26-compound evidence advantage.

**My concrete question stands:** does the alternate corpus admit compounds with no extractable
per-compound outcome? This branch retains 21 such compounds as `CHARACTERISED_ONLY` with a stated
reason. If the alternate includes its equivalents in the 39 and this branch counts them separately,
that single convention may account for most of the difference, and the reconciliation is cheap.

## 4. Search-coverage log

Run 2026-10-02. Primary query unless stated: *antisense oligonucleotide neurotoxicity human iPSC
neuron organoid*. **Blocked services are recorded as blocked, not as searched.**

| # | Resource | Result | Status |
|---|---|---|---|
| 1 | PubMed (eutils esearch) | 1 hit | searched |
| 2 | Europe PMC REST | 89 hits — the pool HV1–HV3 and the queued backlog came from | searched |
| 3 | OpenAlex | HTTP error / rate limited (429 on a prior call) | **not searched — service error** |
| 4 | Semantic Scholar | HTTP error | **not searched — service error** |
| 5 | ResearchRabbit | account required | **blocked — login wall** |
| 6 | Undermind | subscription required | **blocked — subscription wall** |
| 7 | Elicit | account required | **blocked — login wall** |
| 8 | Consensus | account required | **blocked — login wall** |
| 9 | GEO (eutils, *antisense oligonucleotide neurotoxicity*) | 0 hits | searched, no useful result |
| 10 | SRA (eutils, *antisense oligonucleotide neuron toxicity*) | 0 hits | searched, no useful result |
| 11 | PRIDE | timeout | **not searched — service timeout** |
| 12 | ProteomeXchange (PROXI API) | reachable, returned dataset records | searched; no CNS-oligo toxicity dataset identified |
| 13 | BioStudies | 28,474 — query not applied as a phrase | reachable; **count not a result**, needs refinement |
| 14 | ArrayExpress (via BioStudies) | 6,007 — same caveat | reachable; **count not a result** |
| 15 | ClinicalTrials.gov API v2 (*antisense oligonucleotide intrathecal*) | 22 studies | searched — matches the 22 already in `data/trials.csv` |
| 16 | Comparative Toxicogenomics Database | HTTP error on batch query endpoint | **not searched — service error** |
| 17 | ICE (NIEHS) | API responds, keyed on CASRN; oligonucleotides have no CASRN here | searched; **not applicable to this endpoint** |
| 18 | ToxCast | portal, no open query API identified | **not searched — no programmatic route** |
| 19 | Zenodo | 1,898 records, none identified as CNS-oligo toxicity | searched, no useful result |
| 20 | Dryad | 0 records | searched, no useful result |

**Honest reading of this log: it did not find new qualifying human in vitro sources.** The
Europe PMC pool is the one that previously yielded HV1–HV3 and the eight queued candidates. Four
services are behind login or subscription walls I will not attempt to circumvent, and four more
failed on service errors that a later retry may clear. Nothing here changes the dataset.

## 5. Submission-completeness finding, outside both requests

Reading the official announcement directly (20 pp, retrieved 2026-10-02) surfaced two items neither
of us had raised:

- **The registration form is mandatory and is not in this repository.** p14 requires a completed
  form from the Challenge.gov Resources tab, submitted to the challenge mailbox; p13 states that
  *"submission packages that are missing listed materials may not be judged."* This is the highest
  binary risk in the project and it is administrative, not scientific. **It needs Oscar — it carries
  participant identity details I must not invent.**
- **Positive and negative controls are scored twice** — narrative requirement 1, and named in the
  20-point Experimental design criterion. The module had 16 control compounds that were not
  queryable; a derived `control_role` column now marks **15 negative controls and 1 vehicle**.
  **There are zero positive controls**, which is now stated rather than left implicit.

Also worth recording against your proposal framing: the announcement's priority class is **in vitro
human-based systems**, with animal data admitted as a *supplement* to it. It never mentions clinical
trials. That does not override Oscar's presentation order, which is his to set — but it does mean
the 2,341 clinical rows are neither the priority class nor the sanctioned supplement, and the
narrative should say so plainly rather than lead with them.

## 6. What changed in the data this round

Nothing scientific. One schema addition, from the Challenge's own scoring criterion:

| | |
|---|---|
| `control_role` | derived in `src/endpoints.py` from an **explicit** source designation only; a compound is a test compound unless its source says otherwise |

Plus documentation repairs under Oscar's separate authorisation, evidenced in
[`VALIDATION_MANIFEST.md`](../_shared/cns/docs/VALIDATION_MANIFEST.md), and a new QC check that
fails the build if any document quotes a retired release figure — the defect class that produced
this entire round.

---

**RESEARCH REPORT COMPLETE — NO DATASET, LABEL, MODEL OR LINEAGE DECISION TAKEN**
