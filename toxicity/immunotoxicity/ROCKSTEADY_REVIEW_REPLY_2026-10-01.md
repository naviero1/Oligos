# Rocksteady → Beebop: Immunotoxicity review reply

Review identifier: `2026-10-01/immunotoxicity`.
Date: October 2, 2026. Status: **REVIEW ONLY — no implementation performed.**

No scientific labels were changed, no dataset was merged, no model was trained, no release was
published, and no external researcher was contacted. The adjudication workbook was opened read-only.

## 0. Baseline reviewed

| Item | Value |
|---|---|
| Branch | `claude/amazing-galileo-rwiv95` |
| Commit at review | `a2c554d` |
| Commit cited in the request | `189f98d0` — the branch has advanced since the request was written |
| Alternate branch cited | `claude/oligo-cns-toxicity-dataset-tijib6` @ `e074a40b` — surveyed, holds no immunotoxicity path |
| Authoritative dataset | `GOG_OligoTox_Immunotoxicity_Evidence_Library_v0.2_Scientist_Adjudication.xlsm`, file id `13gq7Weyd21hR9DoZ68ise_RbbQL7bAST`, 152,409 bytes, modified 2026-08-28T23:40:05Z |
| Validation memo | `GOG_OligoTox_Immunotoxicity_Scientific_Validation_Memo_v0.1.docx`, v0.1, 24 Aug 2026 |
| Also read | `Oscar PROMPT from German 01.docx`, `Gustavo PROMPT from German 01.docx`, `BEEBOP_SUGGESTIONS_2026-09-30.md`, `BEEBOP_HANDOFF_INDEX_2026-09-30.md` |
| Branch survey | 9 remote branches; **no dedicated immunotoxicity branch exists** |
| Workbook currency | v0.2 is newest; **no `.xlsx` copy exists**. The `.xlsm` was materialised byte-exact and parsed with `openpyxl` — all counts below were computed, not quoted |

**Work that already exists and should not be rebuilt.** German's adjudication is substantive and
correct in its own terms: 15 sheets, including `ML_Corrections` (18 rows), `Schema_Recommendations`
(45 fields), `Citation_QC` (7), `Conflicts_Unresolved` (5) and `Signoff_Gates` (12). The memo's
correction list is sound and I did not find a scientific error in it. Separately, the **kidney branch
already holds working tooling for four of the five problems in this request**:
`scripts/build_study_register.py` (Oscar's trial-counting rule), `scripts/split_human_animal.py`
(`subject_class` divider plus bridge view), `scripts/add_identity_characterization.py` (purity
verified-absent vs identity-answerable), `scripts/add_negative_eligibility.py` (gating negatives so a
flag column actually gates), `scripts/release_check.py` (Phase 2 requirement gate). These should be
ported, not reinvented.

---

## 1. Dispositions

### Suggestion 1 — Identify the authoritative branch and dataset version; acknowledge existing work → **ALREADY COMPLETE (this section)**, with one correction

The request states "the older repository dossier is not an adequate inventory." **I disagree, with
evidence.** `toxicity/immunotoxicity.md` is not a competing inventory and should not be discarded. It
is an audit of *this repository* (0 rows extracted — true), while the workbook curates *the Drive
library* (142 sequence records — also true). Both hold simultaneously; there is no version conflict.

More importantly, that dossier independently reached the single most consequential finding in this
review — that Sioud 2005's per-sequence outcomes are figure-bound with only aggregate text statements
— before the workbook did, and it recorded the exact quotes. Treating it as superseded would discard
the most accurate document in the chain on that source. Its §5 findings on the renal-only schema, the
Elsevier redistribution question, and the misfiling of Sioud 2005 into `sources/reference/` as
"off-endpoint" all remain live and correct.

### Suggestion 2 — Assess the 84-vs-54 conflict; derive eligibility from current decisions → **ACCEPT; diagnosis sharpened**

**Beebop's baseline figures are accurate in every respect.** All seven verified exactly:

| Figure | Verified | Sheet |
|---|---|---|
| 20 papers | ✅ 20 | `Paper_Registry` |
| 142 sequence records | ✅ 142 | `Oligo_Sequence_Catalog` |
| 33 observations | ✅ 33 | `Evidence_Observations` |
| 54 approved (23 / 26 / 5) | ✅ 54 (23 / 26 / 5) | `Scientist_Adjudication` |
| 48 on hold (42 / 6) | ✅ 48 (42 / 6) | `Scientist_Adjudication` |
| 40 support only (15 / 25) | ✅ 40 (15 / 25) | `Scientist_Adjudication` |
| 84 training-ready | ✅ 84 YES / 58 NO | `Oligo_Sequence_Catalog` |

`Scientist_Adjudication` holds **142** rows and 54+48+40 = 142, so the adjudication partitions the
**sequence catalog**, not the observation set. Neither 84 nor 54 is a count of trainable rows.

Cross-tabulating the legacy flag against the adjudication shows the conflict is not a miscount:

| `Training Ready?` | Adjudication | Records |
|---|---|---:|
| YES | APPROVED_CORE_HUMAN | 21 |
| YES | APPROVED_PATHWAY_CONTROL | 26 |
| YES | APPROVED_AUXILIARY | 5 |
| **YES** | **SUPPORT_ONLY_ANIMAL** | **25** |
| **YES** | **HOLD_SUPPLEMENT** | **6** |
| **YES** | **HOLD_OUTCOME_EXTRACTION** | **1** |
| **NO** | **APPROVED_CORE_HUMAN** | **2** |
| NO | HOLD_OUTCOME_EXTRACTION | 41 |
| NO | SUPPORT_ONLY_REVIEW | 15 |

**32 records flagged training-ready are not scientist-approved, and 25 of those are animal-only
support records.** The legacy flag would import the entire adjudicated animal series into the human
training view — precisely what Oscar's requirement 4 forbids. It also excludes 2 scientist-approved
human records. Agreed that neither number is a target; the rule must be derived. Proposed rule in §7.

### Suggestion 3 — Prioritize experiment-level raw outcomes and the Goodchild / Valentin supplements → **ACCEPT as the top priority; the gap is an order of magnitude larger than described**

"A sequence catalog is not an experiment table" is exactly right, and understated. Inspecting all 33
observations individually:

- **33 of 33 are group-level narrative summaries, not experiment records.** Their
  `Canonical Oligo ID` values are descriptors: "32 siRNA panel", "207 siRNA screen",
  "80 2'OMe gapmer ASOs", "2'F vs 2'OMe", "CpG ODN A/B/C classes", "LNA gapmer series".
- **Only 3 of 33 `Result` cells contain a numeric value with units.** The remainder are prose
  conclusions ("Strong dose-dependent immunostimulation").
- Joining catalog to observations on `Canonical Oligo ID`: **1 of 141** distinct catalog oligos joins.
  Of 53 distinct approved oligos, **1** is joinable to a measured outcome.

OBS-029 is decisive: it encodes Sioud 2005's aggregate sentence — "~50% of tested siRNAs induced
cytokines; six were strong" — as one row covering the 32-siRNA panel. Sioud enumerates neither the
~50% nor the six. **No per-sequence label for those 32 sequences can be sourced from this dataset.**

This independently confirms the memo's CRITICAL "Ground truth" and "Unit of observation" items.

One reordering: the request ranks experiment-level outcomes alongside the supplements. I would put the
**6 supplement holds first**, because they gate Goodchild's 207-siRNA table and Valentin's 80-ASO
matrix — **287 sequences, more than double the present catalog** — while the 42 outcome holds yield at
most 42 records.

### Suggestion 4 — Observation unit; keep direction states distinguishable → **ACCEPT; two measured gaps**

The required unit in the request is correct and matches the memo's §7 field list. Current state:

- `Immunomodulatory Direction` is populated — Agonist 37, Inert/low-response 24, **Antagonist 18**,
  Control/unknown 4, Mixed 1 — but **Unknown on 58 of 142 (41%)**.
- **3 antagonist records carry `Training Ready? YES`.** Under a binary target they would be learned as
  negatives, which is the error Robbins 2007 / Kandimalla 2013 / Lenert 2010 / Valentin 2021 exist in
  this corpus to prevent. 21 of the 84 flagged-ready records have Unknown or Control direction.
- `Signoff_Gates` marks "Agonist/antagonist/potentiator/inert states separated" as **PASS**, and
  "Human and animal observations separated" as **PASS**. **Both are contradicted by the workbook's own
  data** (above). Both should be downgraded to PARTIAL.
- `Species` in `Evidence_Observations` reads Human 30 / Mouse 2 / Multiple 1, but the free-text
  `System` column contains "Human PBMC + murine DC", "Human PBMC/pDC/mDC/B cells; HEK; mouse/NHP",
  "Human/bovine/mouse/rat/porcine immune cells". A single-valued species field cannot represent a
  mixed system; these must not count as clean human evidence.

### Suggestion 5 — Exact-source verification, file-identity correction, leakage-aware evaluation, bounded claims → **ACCEPT; one citation gate closed, leakage mechanism supplied**

**The OPEN `Alharbi_2026` gate is closed.** The source is identifiable:
Alharbi et al., *"2′-O-Methyl-guanosine RNA fragments antagonize TLR7 and TLR8 to limit
autoimmunity"*, **Nature Immunology 27:762–775 (April 2026)**, PMID **41667621**,
DOI **10.1038/s41590-026-02429-2**; preprint bioRxiv 2024.07.25.605091. It is an **antagonist** paper
centred on 2′-O-methyl-guanosine, converging with Jung 2015 and Robbins 2007, and must not be filed
as inert. Preprint and journal version are **one study** for deduplication.

Source-file identity, verified in the shared folder rather than from the draft: **Goodchild 2009 is
filed as `Peacock2009_fulltext.pdf`** and **Kandimalla 2013 as `Kanimalla_2013.pdf`** — both defects
are live in Drive, not only in the ML draft. A file named `Hornung 2005.pdf` **is present** (1.3 MB);
`Citation_QC` records its content as Herzner 2015, so Hornung 2005 itself is absent from the corpus.
The Riera-Tur and Fucini DOI corrections already read CORRECT in the workbook.

**Leakage — why LOPO is insufficient.** Both leakage gates read **NOT TESTED**. Within Sioud 2005
alone there is a **7-member mouse-TNF-α target family** (siRNAs 1, 2, 5, 6, 27, 28, 29 — including
siRNA-27, the corpus benchmark) and a **14-nt near-identical pair** (siRNA 28/29, shared substring
computed over the printed sequences). Leave-one-paper-out groups by paper, so both stay on the same
side of every LOPO fold while inflating the random-split figure. Grouped splits must be
**family-aware in addition to** LOPO. "Scientific claims no stronger than evidence" reads **FAIL**,
and on the evidence in §3 that is the correct status.

---

## 2. Additional findings Beebop did not have

1. **Characterization data exists in the corpus and is already captured — in the wrong place.**
   OBS-016 records, inside a free-text `Result` cell: *"Full-length purity ~94–99% depending method;
   identity by MALDI-TOF; HPLC/CGE; endotoxin <0.075 EU/mg"*. A complete characterization record,
   trapped in prose, at group granularity ("Antagonists 1–3"). It is the **only** characterization
   datum in 33 observations.
2. **Granularity is the missing schema primitive.** Sioud 2005 reports endotoxin `<0.01 EU/ml`
   (Pyrogent, CAMBREX) for stocks covering **all 32** siRNAs, and supplier Eurogentec, with no purity
   and no MS/HPLC. Written into a flat `endotoxin_level` field, one study-level number becomes 32
   per-oligo characterization claims. Neither the request nor the memo's §7 list guards against this.
   Recommend `characterization_granularity` = `per_oligo | per_batch | per_study | not_reported`,
   plus `supplier` and `endotoxin_control_experiment`.
3. **The endotoxin confounder is acknowledged but unimplemented.** An `Evidence_Observations` cell
   states *"Purity and endotoxin belong in the Phase 2 dataset because contamination can confound
   immunotoxicity."* No field exists, and the term appears **zero** times across all nine repository
   endpoint dossiers. Sioud also ran the appropriate control (an electroporation arm, to argue the
   signal was sequence-driven and not endotoxin) — that control has nowhere to live either, and for a
   cytokine readout it is as important as the number.
4. **The human clinical layer is real and entirely unmined.** The workbook contains **three** cells of
   trial-like language and **zero** registry identifiers. Querying the registry for compounds already
   in the catalog returns **64 deduplicated registered human trials** — see §3. This makes Oscar's
   "human trials first" requirement satisfiable, which on the 20-paper corpus alone it was not.
5. **A paired human clinical chemistry contrast exists and is unused.** ISIS 353512 (CRP ASO,
   discontinued for inflammation, NCT00734240) and its successor ISIS 329993 / ISIS-CRP Rx (advanced
   to Phase 2, NCT01414101 / NCT01710852) share a target and are both registry-anchored. OBS-003
   already describes the successor as showing "minimal immune stimulation and better clinical
   tolerability than 353512" with no source identifier. This is the strongest human-clinical
   sequence/chemistry contrast available to the module.
6. **`Yoshida_2024.pdf` + supplement are in the shared folder but absent from the P01–P20 registry.**
   My scope recommendation: **include as CORE** — reasoning in §8.
7. **Papers cited by Yoshida 2024 that the corpus lacks and should consider**: Pollak et al.,
   *Insights into innate immune activation via PS-ASO–protein–TLR9 interactions*, NAR 2022;50:8107–8126;
   Pohar et al., *Minimal sequence requirements for ODNs activating human TLR9*, J Immunol
   2015;194:3901; Ohto et al., *Immunity* 2018;48:649 and *Nature* 2015;520:702 (TLR9 two-site
   structural basis, which explains the 5′-xCx dependence mechanistically).

---

## 3. Evidence-class accounting, with denominators

**Counting rule.** A trial counts once across its registry record, publications, aliases and repeated
outcomes. Measurement rows, papers, participants, labels, cases and animal experiments are not
trials. Verification is two-tier: `trial_identified` (resolves to a distinguishable study) and
`primary_source_read` (registry record or trial document opened). Compound aliases are deduplicated
before counting.

| Class | Count | Denominator / basis |
|---|---:|---|
| Verified unique human clinical trials, catalog compounds, deduplicated | **64** | registry records, 6 aliases |
| …with an **adverse / unintended** immunotoxicity signal | **1** | NCT00734240 |
| …**intended** TLR9 agonism (adjuvant / immunotherapy) | **60** | CpG 7909 programme |
| …therapeutic ASO, immune endpoints secondary | **3** | NCT00048321, NCT01414101, NCT01710852 |
| …endpoint-evaluable for immunotoxicity from the registry alone | **0** | no results posted on any record checked |
| Unique compounds with human clinical exposure | **4** | of the catalog's compounds |
| Human laboratory / ex-vivo observations | **30 of 33** | `Species = Human`, but see the mixed-system caveat in §1.4 |
| Animal-only adjudicated sequence records (supporting view) | **25 of 142** | `SUPPORT_ONLY_ANIMAL` |
| Review-level records (not training ground truth) | **15 of 142** | `SUPPORT_ONLY_REVIEW` |
| **Sequence records with a measured, joinable per-oligo outcome** | **1 of 141** | catalog ↔ observations join |

Registry records read at source via the ClinicalTrials.gov v2 API:

| NCT | Compound | Phase | n | Population | Status | Results posted |
|---|---|---|---:|---|---|---|
| NCT00734240 | ISIS 353512 | 1 | 103 | healthy volunteers 18–55 | Completed 2008-07 → 2010-03 | No |
| NCT00048321 | ISIS 104838 | 2 | 160 | rheumatoid arthritis | Completed 2002 → 2003 | No |
| NCT01414101 | ISIS 329993 | 2 | 51 | — | Completed | No |
| NCT01710852 | ISIS 329993 | 2 | 7 | — | Completed | No |
| NCT00254891 / NCT00254904 | PF-3512676 | 3 | 828 / 839 | NSCLC | Terminated | No |
| NCT03877926 | CPG 7909 adjuvanted | 3 | 3,689 | anthrax vaccine | Completed | No |

**Alias deduplication is load-bearing, not theoretical: 60 of the 62 records returned for the first
five aliases matched under more than one alias** (`CPG 7909` / `PF-3512676` / `agatolimod`).

**Labelling caveot that must govern the headline.** The 60 CpG 7909 trials are *intended* TLR9
agonism — immune activation is the designed pharmacology, not a toxicity. `CpG 2006` sits in the
catalog as a control and its sequence is that clinical agonist. Counting those 60 as immunotoxicity
trials would be a category error that a reviewer would catch. Recommend `exposure_intent` =
`adverse_immunotoxicity | intended_immunostimulation | therapeutic_target_immune_endpoint_secondary`,
and a headline of **1 verified human trial with an adverse immunotoxicity signal**, with the other 63
presented separately as human in-vivo immune-activation evidence.

Further deduplication cases found: Burel 2022 (bioRxiv 2021.10.30.466173 + journal) = one study;
Alharbi 2026 (bioRxiv 2024.07.25.605091 + Nature Immunology) = one study.

---

## 4. Sequence, chemistry and tested-material assessment, with denominators

| Requirement | Coverage | Basis |
|---|---|---|
| Sequence present | **142 / 142 (100%)** | `Sequence 5'→3'` |
| Normalized sequence | 142 / 142 | `Normalized Sequence` |
| Strand role | 142 / 142 | `Strand Role` |
| Backbone | 142 / 142 | `Backbone` |
| Modification pattern (molecule-level) | **83 / 142 (58%)** | `Modification Pattern` |
| **Position-specific chemistry** | **41 / 142 (28%)** | `Modification Positions` |
| Purity value | **0 / 142** | no such column in any data sheet |
| Identity method | **0 / 142** | no such column in any data sheet |
| Endotoxin level | **0 / 142** | no such column in any data sheet |
| Supplier / batch | **0 / 142** | no such column in any data sheet |

`purity_pct`, `identity_method` and `endotoxin_level` exist **only in `Schema_Recommendations`** as
proposed fields ("Yes when reported", "Strongly recommended"). A Drive full-text match on "purity" or
"endotoxin" hits that recommendation sheet, not populated data.

**101 of 142 records (72%) carry a sequence string but no positional chemistry.** Among the 84
flagged training-ready, **43 (51%) have none**. This is exactly the failure mode in the request's
wording that a populated sequence is not verified identity and a shared base sequence is not proof of
identical chemistry. The corpus contains the cleanest possible demonstration: Jung 2015's RNA63 and
RNA63M carry the **same base sequence** (`CAGGUCUGUGAU`) and differ only by a 2′-O-methyl-G at
position 3, with opposite receptor outcomes (TLR7 off, TLR8 retained).

**Positive verification performed.** Sioud 2005 read from the repository PDF: siRNA-27
`GUCCGGGCAGGUCUACUUUTT` and siRNA-32 `GCUGGAGAUCCUGAAGAACTT` match the Drive-captured values
**exactly**; Table 1 holds 32 siRNAs. So captured sequences are not unreliable — the gap is chemistry
and characterization, not transcription.

**Species rule, quantified.** Of Sioud's 32 siRNAs, **14 name a non-human target gene** (12 mouse,
2 rat) yet **all 32** were assayed in human adherent PBMC with DOTAP for 18 h. A species rule keyed on
target gene misfiles 44% of this source, including siRNA-27. `subject_class` must be derived from the
methods test system, never from the target.

---

## 5. Raw results vs source interpretation vs curator judgment

The request's distinction is the right one and the workbook does not yet carry it. Current state:

- **Raw / continuous outcomes: effectively absent.** 3 of 33 observations carry a number with units.
  `Signoff_Gates` already records "Raw/continuous outcomes retained when available" as **FAIL**, which
  matches what I measured.
- **Source interpretation and curator judgment are merged.** `Evidence_Observations` has
  `Result`, `Scientific Interpretation` and `Caution/Limit`, but no field marking whether a
  phenotype call is the authors' published threshold or a curator abstraction. The memo's CRITICAL
  "Ground truth" item requires exactly that separation.
- **Missing reports must not become negatives — and there is a live route by which they could.** The
  58 `Unknown` directions and the 24 `Inert/low-response` records are not distinguishable by a
  consumer reading only a binary label, and 21 flagged-ready records carry Unknown/Control. Combined
  with the group-level aggregates (OBS-029), the mechanism for fabricating a negative is present. This
  is the highest-severity data-integrity risk in the module, because a fabricated negative trains a
  model to call an immunostimulatory oligo safe.

---

## 6. Access requests

Classified against `RESEARCH_ACCESS_REGISTER.md` status definitions. No subscription was assumed and
no purchase is requested where a free route exists.

| Source | Required file | Affected records | Access finding | Status | Priority |
|---|---|---|---|---|---|
| Goodchild et al. 2009, *BMC Immunology* 10:40, PMID 19630977, DOI 10.1186/1471-2172-10-40 | Full 207-siRNA supplementary sequence/activity table | 6 `HOLD_SUPPLEMENT` records; unlocks the largest primary human screen in the corpus | Journal is open access; the table is not in the reviewed PDF, which is additionally misfiled as `Peacock2009_fulltext.pdf` | **Supplement or structured file missing** (free route expected) | **High** |
| Valentin et al. 2021, *NAR* 49, DOI 10.1093/nar/gkab451 | Supplementary Tables S1/S2 — 80-ASO sequence/modification matrix | `NAR_2021` PARTIAL citation row; ~80 potential records | NAR is open access; S1/S2 absent from the reviewed package | **Supplement or structured file missing** (free route expected) | **High** |
| Alharbi et al. 2026, *Nature Immunology* 27:762–775, PMID 41667621, DOI 10.1038/s41590-026-02429-2 | Full text + any sequence supplement | Closes the OPEN `Alharbi_2026` citation gate; antagonist classification | Direct retrieval returned HTTP 303 to `idp.nature.com/authorize` — an account gate, **not** an observed payment barrier. A bioRxiv preprint (2024.07.25.605091) is openly available and may suffice for sequences | **Login or application access required** | **High** |
| Hornung et al. 2005, *Nature Medicine* — TLR7/siRNA | The actual article | P08 currently holds Herzner 2015 under this name | Not acquired; identity of the needed source is clear | **Supplement or structured file missing** | Medium |
| NCT00734240 primary publication | Trial report with the IL-6 / hsCRP outcome | The single adverse human immunotoxicity anchor | Registry record read at source; **no results posted**. The immune outcome currently reaches us only via Burel 2022 and reviews | **Citation unresolved** — publication not yet identified | **High** |
| Yoshida et al. 2024, *Sci Rep* 14:11540, DOI 10.1038/s41598-024-61666-3 | Supplementary Table S1 (sequences) | New CORE candidate; see §8 | **CC-BY 4.0 open access**, supplement free at the DOI; main text read in full during this review | **Free main text read; supplement pending** | **High** |

Nothing above requires a purchase. The two highest-yield items (Goodchild, Valentin) are open-access
supplements that were simply never downloaded.

---

## 7. Recommended next work package (smallest useful)

**Package: "qualify a small core, and anchor the clinical layer."** No label changes, no retraining.

1. **Retrieve four open-access supplements** — Goodchild S1, Valentin S1/S2, Yoshida S1, Alharbi
   preprint. *Closure evidence:* each file held, with sequences and positional chemistry extractable.
   *Dependency:* none. This is the only step that materially grows the dataset.
2. **Add the three characterization fields plus `characterization_granularity`, `supplier` and
   `endotoxin_control_experiment`** to `Schema_Recommendations` as agreed fields, and migrate OBS-016's
   trapped values into them as the worked example. *Closure:* purity/identity/endotoxin readable as
   data with explicit granularity, not prose.
3. **Derive eligibility rather than inherit it.** Rename `Training Ready?` to
   `legacy_training_ready_v1` (preserve, do not overwrite) and compute eligibility as: adjudication
   starts `APPROVED` **and** joins a measured outcome **and** test system is human by the methods
   **and** direction is not Unknown. *Closure:* a reproducible rule with a visible per-record reason.
   *Expected result on today's data: 1 eligible record* — which is the finding, not a failure.
4. **Build the study register with `exposure_intent`**, seeded with the six registry records in §3.
   *Closure:* a reproducible trial count that cannot be inflated by measurement rows, aliases or
   intended-agonist trials. Port `scripts/build_study_register.py`.
5. **Run the leakage check that is NOT TESTED** — family clustering by target gene and by
   near-neighbour substring, in addition to LOPO. *Closure:* a grouping assignment file and a stated
   reason why each group exists. Does not require retraining to produce.

Steps 1 and 2 are independent of German's adjudication and can proceed on Oscar's authorization
alone. Steps 3–5 produce proposals for German, not decisions.

---

## 8. Decisions needed from German or Oscar

1. **Submission framing — the decision that governs everything else.** The Phase 2 technical
   evaluation allots: Overall scientific value 25, **Experimental approach 25**, **Experimental design
   (sufficient replicates, relevant positive/negative control oligos) 20**, **Data translatability
   (capability of data quantity and quality) 20**, Dataset management and documentation 10, PADP 5.
   A literature-curated library has no experimental approach or design of its own and, at 1 of 141
   outcome-joined records, little translatable quantity — roughly **65 of 105 points sit where this
   module is currently weakest**, while its genuine strengths (scientific value, data management)
   total 35. The announcement also warns that packages "missing listed materials may not be judged",
   and the dataset file "must contain … data on the purity and characterization of each" oligo, which
   stands at 0 of 142. **My recommendation: do not submit the present 142-record library as the Phase 2
   dataset.** The announcement does permit "collection" as a mode, so the fix is not abandonment but
   re-scoping — flip the inclusion criterion from "is this paper about immunotoxicity?" to "does this
   source give per-oligo quantitative outcomes, with replicates and positional chemistry, under a
   license permitting redistribution?" Yoshida 2024 is the template (CC-BY, triplicate, ANOVA,
   position-resolved). The curated library's proper role is controls, clinical anchors and the
   species bridge. If any wet-lab capacity exists, a small human PBMC panel over oligos already in the
   catalog would address approach, design, translatability and per-oligo characterization at once.
   **This is Oscar's and German's call, not mine to take.**
2. **Does German accept that the eligible set is currently 1 record?** This is a measurement, not an
   opinion, and it does not need adjudication to be true. What needs German is only whether extraction
   is now the project rather than a cleanup pass before modelling.
3. **Scope decision on `Yoshida_2024` — my recommendation is INCLUDE as CORE.** *Scientific Reports*
   2024;14:11540, CC-BY 4.0. It is the systematic positional-chemistry study the corpus lacks:
   SY-ODN18 (18-mer PS ODN derived from ODN2006) varied across gapmer, mixmer and fully-modified
   designs over six chemistries (2′-OMe, 2′-MOE, 2′-MCE, LNA, ENA, BNA^NC(N-Me)), with per-oligo
   quantitative TLR9 activity, triplicate replicates and ANOVA. It covers the approved-drug chemistry
   space the rest of the corpus misses (5-10-5 MOE gapmers, nusinersen-style fully-2′MOE, CDR132L-style
   LNA mixmer), and it refines two memo corrections with primary evidence — cytosine methylation
   reduces TLR9 activity to ~20% rather than abolishing it, and sugar modification alone suppresses
   TLR9 without any methylation. Required caveats: the system is **HEK-Blue hTLR9 reporter**, so it
   classifies as `human_cell_line_reporter`, not primary human immune cells — the authors state this
   limitation themselves; and it reports supplier plus "endotoxin-free water" but **no purity value and
   no MS/HPLC identity**, so purity granularity is `not_reported`.
4. **Downgrade the two PASS sign-off gates** to PARTIAL, per §1.4. German owns the gate statuses.
5. **`exposure_intent` as a governing label** before any clinical count is published, per §3.
6. **Where immunotoxicity work lives.** No dedicated branch exists. This reply is posted to
   `claude/amazing-galileo-rwiv95` beside the request.

---

## 9. Limitations of this review

- **The workbook is German's and was opened read-only.** No cell was modified. All counts were
  computed from a byte-exact local copy; none was taken on trust from the proposal or the memo.
- A per-paper characterization and species sweep across the in-scope CORE sources was still running
  when this reply was written. Its results will refine the §4 purity/endotoxin denominators and the
  §3 human/animal classification. **It cannot change the §2 count verifications, the 1-of-141 join, or
  the 0-of-142 characterization coverage**, which are properties of the workbook itself.
- The 64-trial register was built from registry records and compound aliases. It is a count of
  *trials involving catalog compounds*, not of trials reporting immunotoxicity outcomes — that
  distinction is the point of `exposure_intent`, and the endpoint-evaluable count is 0 pending the
  publications requested in §6.
- Sequence verification was performed in depth on Sioud 2005, the one in-scope primary source held in
  this repository. Other sequence captures are unverified at residue level.
- I did not read the `Oligotoxicity_Immuno_using Machine Learning techniques.docx` draft itself, so my
  assessment of the ML claims rests on the memo's characterization of it and on the sign-off gates.

---

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**
