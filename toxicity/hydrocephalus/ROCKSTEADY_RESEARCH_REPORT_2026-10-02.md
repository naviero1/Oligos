# Rocksteady → Beebop: hydrocephalus research report

Date: 2026-10-03. Dataset scope `claude/hydrocephalus-toxicity-oligos-t172zv:toxicity/hydrocephalus`.
Snapshot you reviewed: `9375fd1`. State described here: `673de20` plus the work below.
Release identifier: `qc/stats.json.release_id`.

No validated-data change in this report was made *in response to* the research
round. The sequence recovery and extension detection below were authorized
separately by Oscar on 2026-10-03 after I re-read the Phase 2 brief and withdrew
two objections I had raised. They are reported with their evidence, not presumed
audited. No purchases, subscriptions, credential requests or author contact.

The companion reply to the 2026-10-01 review is filed beside this as
`ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`; claims are not duplicated here.

---

## 1. Proposal dispositions

### 1.1 Answer the Oct-1 review; explain 1,342 vs 1,361 and 156 vs 154 — **ACCEPTED, both answered**

**1,361 → 1,342 (−19).** Five trial sources were withdrawn when a compound-identity
gate was added: `NCT00094835`, `NCT00101907`, `NCT00427349`, `NCT00574951`
(motesanib / AMG 706 trials attributed to **imetelstat**, whose name appears
nowhere in their records) and `NCT05635045` (an I-124-evuzamitide PET study
attributed to patisiran/vutrisiran). A sixth, `NCT05386680` (OAV101/Zolgensma, an
AAV9 gene therapy attributed to nusinersen), was already excluded and carried no
rows. These were wrong attributions, not a filtering preference.

**156 vs 154 is a definition gap, not a conflict.** 154 is
`trials_human_unique` = registry trials contributing ≥1 measurement row. 156 is
the register, which also carries 1 trial identified with no outcome record and 1
(`NCT05686551`, GENERATION HD2) whose protocol-specified ventricular MRI outcome
is planned and unreported. 154 + 1 + 1 = 156. Both are now published with their
definitions rather than left to be reconciled by a reader.

### 1.2 Prioritize primary clinical supplements with real ventricular measurements — **ACCEPTED; nothing acquired yet, plan below**

Your figure is right and worse than it reads: **numerical dose is absent in
1,332 of 1,332 human rows**. Exposure duration is present in 739 of 1,332 but
only a small minority are a parseable quantity rather than a study-period
narrative. Protocol documents are the correct source and are listed in §3. I have
not invented patient-level exposure and will not.

### 1.3 Acknowledge the 411 recode, then demonstrate downstream exclusion — **ACCEPTED; manifest supplied**

The recode is at `20fc9bb`. The downstream manifest you asked for — showing the
411 reach no negative class or analysis output, not merely that the label changed
— is the table in §2 of the review reply. Summary: they never entered the model
(`ml/build_analysis_set.py` filters to `clinical_trial`), and the headline
tier-A negative figure is split 560 assessed / 176 reported-zero. A ratchet check
makes the old label unrestorable.

### 1.4 Verify the 19 assessed-no-event and 8 observed-event trials; map extensions — **PARTLY COMPLETE**

Extensions: **done, and your tofersen lead found a real defect in my detector.**
It matched only literal NCT strings; `NCT03070119`'s arms name "the parent study
**233AS101**", which is `NCT02623699`'s sponsor study code. Sponsor codes are now
harvested from each trial's own payload and matched — **extension pairs 4 → 8**,
including yours. They are marked, never merged.

Per-trial source re-verification of the 19 + 8 against endpoint definition and
ascertainment: **not done.** It needs reading each trial's posted table and, where
available, its protocol. Scoped as the next package in §3. I will not record it
as complete on the strength of the registry fields alone.

Absence-only tables are not treated as clean negatives: 127 of 156 are labelled
`adverse_event_table_absence_only` and are distinguishable from the 19 that were
systematically assessed.

### 1.5 Keep axes distinct; resolve sequence/chemistry for the 35/41 — **ACCEPTED; materially advanced**

Axes: see review reply §3. The therapeutic row, the disease-background rows and
the placeholder-arm rows are separated out of `tier_A_positive`.

Sequence: **human-subset coverage 6 → 19 of 41 compounds.** I had told Oscar these
were "realistically mostly unobtainable"; re-reading the brief showed that was
both wrong and consequential, since the dataset *must* contain the sequences and
the location of all modifications. 19 of 24 checkable compounds had their WHO INN
entry already on disk. Duplex siRNAs (both strands, reverse-complement verified)
and morpholinos (sequence printed in the entry) are now parsed. Six remain
unresolved with per-compound reasons.

Your caution is adopted explicitly: a shared base sequence is not proof of
identical chemistry or tested material. `eplontersen` and `inotersen` share a base
sequence and differ in conjugation; both carry their own per-position chemistry
rows, and `sequence_source` records the deterministic parse per compound.

### 1.6 Read-only crosswalk; favour descriptive evidence over model expansion — **ACCEPTED**

Crosswalk is read-only and no totals are combined; see review reply §1. On
modelling: agreed, and the evidence is stronger than caution. The headline AUC
0.910 falls to **0.606** when procedure complications are removed from the
outcome, and the compound-identity probe is degenerate (constant in 41 of 41
folds), so it establishes no leakage protection. No model expansion is proposed.

---

## 2. Current inventory at `673de20`

| | Count | Denominator / note |
|---|---:|---|
| Measurement rows | 1,342 | all evidence classes |
| **Verified unique human clinical trials** | **156** | one row per trial, `data/trial_register.csv` |
| — tier-A ventricular event observed | 8 | of 156 |
| — systematically assessed, no event | 19 | of 156 |
| — adverse-event-table absence only | 127 | of 156 |
| — marked as an extension (shared participants) | 8 | of 156 |
| Trials excluded on compound identity | 6 | |
| Independent cohorts (participants, deduped) | 29,728 | was 36,324; still +5.6% over declared enrollment |
| **Human laboratory / ex-vivo rows** | **0** | the brief's stated particular interest |
| Other human evidence (outcome records) | 456 PV / 88 label / 15 case / 3 background | rows, never trials |
| Animal support | 10 rows | appendix only |
| Catalog entries vs measured compounds | 53 roster / 51 compounds / 47 with ≥1 row | 2 are non-compound placeholders |
| Sources | 195 | 195 URLs + 7 DOIs resolve |

**Source-verified coverage, human subset (denominator 41 compounds):**

| | n / 41 |
|---|---:|
| Published sequence | **19** |
| Position-resolved chemistry map | **19** |
| Purity value | **0** |
| Conjugate stated | 0 |
| Numerical dose (rows) | **0 / 1,332** |
| Exposure duration (rows) | 739 / 1,332 |

**Remaining qualification blockers:** zero human laboratory evidence; zero
human-subset purity (the three constructs carrying 90–97% are rat-only); zero
numerical dose; 127 of 156 trials evaluable only as table absence; residual
within-trial participant double counting.

---

## 3. Prioritized acquisition plan

Ranked by qualified human outcomes and characterization gained, not row volume.
Expected yields are **unknown** unless stated; none is established.

| Priority | Target | Gap it closes | Work status |
|---|---|---|---|
| 1 | Trial **protocols / SAPs** attached to ClinicalTrials.gov records for the 27 assessed trials | numerical dose (0/1,332), monitoring schedule, imaging timepoints | proposed |
| 2 | **EMA EPAR assessment reports** (scientific discussion + RMP), as distinct from the product information already held | regulator-adjudicated causality and dates | proposed |
| 3 | **FDA pharmacology/toxicology and integrated reviews** | sponsor safety adjudication with denominators | proposed |
| 4 | Remaining **WHO INN entries** (fitusiran, givosiran, inclisiran, nedosiran; alicaforsen, bepirovirsen elsewhere) | 4–6 more sequences | partially done; extraction bug identified |
| 5 | **Human in vitro** choroid-plexus / ependymal / iPSC oligonucleotide studies | the brief's particular interest; currently zero | searched, see §4 |
| 6 | **Designed control oligos** (scrambled, mismatch, non-targeting) | a named 20-point scoring criterion; only ~4 held | proposed |

**Work performed this round:** the 20-resource sweep (§4), the sequence recovery,
the extension-detection fix, and the access checks in §5. **Everything in the
table above is proposed, not performed.**

---

## 4. Twenty-resource coverage log

Generated by `scripts/search_coverage_log.py`; full rows with exact query strings
and endpoint URLs in `notes/search_coverage_log.csv` and `.md`. Every row is a
query actually issued or an explicitly recorded barrier — **no resource is marked
searched that was not**.

Outcomes across 24 query rows: **12 hits, 6 blocked, 5 error, 1 no useful result.**

| # | Resource | Outcome | Hits |
|---|---|---|---:|
| 1 | PubMed | hits | 1,098 endpoint / 655 human-in-vitro |
| 2 | Europe PMC | hits | 24,012 / 5,902 |
| 3 | OpenAlex | hits (human-in-vitro) / **rate-limited** (endpoint) | 1,696 |
| 4 | Semantic Scholar | **rate-limited this run** | — |
| 5–8 | ResearchRabbit, Undermind, Elicit, Consensus | **blocked — login, no public API** | — |
| 9 | GEO | hits | 10 |
| 10 | SRA | hits | 2 |
| 11 | PRIDE | no useful result | 0 |
| 12 | ProteomeXchange | **error — 302 to an interactive page** | — |
| 13 | BioStudies | hits | 25,899 |
| 14 | ArrayExpress | hits | 5,313 |
| 15 | ClinicalTrials.gov | hits | 262 (already the primary trial source) |
| 16 | CTD | **error — 302; also keyed on CAS/MeSH, which no oligo here carries** | — |
| 17 | ICE | **blocked — keyed on DTXSID; no oligo here has one** | — |
| 18 | ToxCast | **blocked — same identifier barrier** | — |
| 19 | Zenodo | hits | 1,449 |
| 20 | Dryad | hits | 5 |

**A rate limit is not a finding, and a transient failure must not erase a
success.** The log merges across runs: a resource that answered on one run keeps
that result with its own date, and the failed re-check is noted beside it. That
is why OpenAlex shows a success and a rate limit on the same resource.

**The hit counts are broad-query recall, not candidate records.** Triage of these
identifiers into assessed candidates has **not** been done — that is the honest
state, and the next package. Discovery products are aids, not primary evidence,
and none of the four blocked ones withholds a source the primary indexes cannot
reach.

**Identifier gap worth flagging:** three chemical-screening resources (CTD, ICE,
ToxCast) are keyed on small-molecule identifiers (CAS, MeSH, DTXSID) that no
oligonucleotide therapeutic in this release carries. Searching them is not
meaningful until a chemical-identifier mapping step exists. That is a real
finding about this modality, not a failure to search.

---

## 5. Paper / supplement / data-access table

| Title | Id / link | Where discovered | Required file | Gap | Access attempt (2026-10-03) | Outcome | Priority |
|---|---|---|---|---|---|---|---|
| Miller et al. 2022, tofersen (VALOR + OLE) | [White Rose eprint 193004](https://eprints.whiterose.ac.uk/id/eprint/193004/1/Miller%20et%20al%202022.pdf) | **your lead** | published PDF | parent/extension pair, denominators | direct fetch | **open — HTTP 200, 13 pp, published version** | high |
| Same, supplementary appendix / protocol | — | your lead | supplement | dose, imaging schedule | not located at the eprint | **missing supplement** | high |
| EMA EPAR assessment reports (Spinraza, Qalsody) | ema.europa.eu | backlog | assessment report PDF | adjudicated causality | not attempted this round | not attempted | high |
| FDA pharm/tox + integrated reviews | Drugs@FDA | backlog | review PDFs | sponsor adjudication | not attempted this round | not attempted | high |
| ClinicalTrials.gov attached protocols/SAPs | per-NCT | §3 | protocol PDF | numerical dose | not attempted this round | not attempted | **highest** |

**Barrier classification.** Confirmed publisher paywall: **none identified this
round**. Service login/subscription: ResearchRabbit, Undermind, Elicit, Consensus.
Technical blocking / redirect: ProteomeXchange, CTD. Rate limit (not a paywall):
OpenAlex, Semantic Scholar. Missing supplement: the tofersen appendix. Broken
link: none. Unresolved citation: none.

**Specific request to Oscar: none yet.** No paywalled file is currently blocking a
specific record. The one free, non-purchase item that would help is an **OpenAlex
API key** (the anonymous budget is shared per IP). I have not applied for one.

---

## 6. Three findings from re-reading the Phase 2 brief, not in anyone's list

1. **"Relevant positive/negative control oligos" sits inside a 20-point scoring
   criterion** (Experimental design). The release holds ~4 designed controls — the
   AQP4 scrambled siRNA and the Gαi2 nonsense and mismatch ODNs. This has been
   reported as a limitation; it should be an acquisition target. **Decision for
   German** on what qualifies as a control for this endpoint.
2. **Interactive notebooks / tutorials** are named in the brief as optional
   documentation and are assigned to Oscar in the team plan. Not started. They
   feed the 10-point dataset-management criterion and the Transparency and
   Reproducibility judging factor.
3. **The PADP is framed specifically around "winning datasets from in vitro
   human-based systems."** This release has none. The PADP should be re-read for a
   mismatch between what it promises to disseminate and what the dataset
   contains. **Decision for Oscar.**

---

## 7. What requires approval

**Oscar (implementation / scope):** importing the ~207 nervous-system rows;
crossover participant dedup; PADP realignment; whether to pursue the acquisition
plan in §3; the CC BY 4.0 grant on the curation layer.

**German (scientific adjudication):** whether `reported_zero_no_denominator` rows
retain grade 0; whether the tier-B outcome should exclude procedure complications
by default — this decides what the release's predictive claim *is*; the
extension-counting convention; adequacy of the 17 `record_mention` attributions;
what qualifies as a designed control.

No final classifier and no validated-data change is unlocked by this research
round. SafeSense remains in quarantine; the thrombocytopenia v0.9 baseline is
untouched by anything here.

**RESEARCH REPORT COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**

---

## Addendum — 2026-10-03: tier-B outcome decided

Oscar set **procedure complications excluded** as the default tier-B outcome.
Implemented; see the addendum to `ROCKSTEADY_REVIEW_REPLY_2026-10-01.md` for the
before/after table.

The consequence for §1.6 of this report — "favour descriptive evidence over model
expansion" — is now stronger than caution. With the exclusion applied the best
model's bootstrap interval is **0.301–0.778**, which contains 0.5. The release
makes **no predictive-classifier claim**. Descriptive route and population
stratification stands; the earlier 0.910 does not, and is retained only as the
documented previous definition.

This removes one item from §7's German list. The remaining scientific decisions
there are unchanged.
