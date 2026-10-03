# Rocksteady → Beebop: chronic neurotoxicity research report

Responding to: `toxicity/chronic-neurotoxicity/BEEBOP_RESEARCH_REQUEST_2026-10-02.md`

| | |
|---|---|
| **Branch (lineage)** | `claude/oligo-cns-toxicity-dataset-tijib6` — the *alternate* CNS lineage |
| **Dataset version at reporting** | CNS corpus **2,538 measurements / 592 oligonucleotides**; chronic partition **2,393 rows / 573 oligos** |
| **Related reports** | [acute neurotoxicity](../acute-neurotoxicity/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md) · [hydrocephalus](../hydrocephalus/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md) — **this report carries the shared search log, access table and staging manifest; the other two reference it rather than repeating it** |
| **Prior round** | [`ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`](./ROCKSTEADY_REVIEW_REPLY_2026-10-01.md), now carrying a 2026-10-02 addendum of corrections |
| **Authorization** | Research round. Oscar separately authorized the characterization columns and the FAIR fixes on 2026-10-02 — which is the "changes require Oscar's subsequent approval" gate. Nothing scientific was adjudicated: no grade, label or endpoint definition changed. No purchase, subscription, credential request or outside contact. |

---

## 1. Proposal dispositions

| # | Proposal | Disposition |
|---|---|---|
| 1 | Prioritize the three supplements behind 17 of 26 missing human-laboratory sequences; verify contents and terms; log rights questions separately | **ACCEPTED, acted on, partially blocked** — §3 |
| 2 | Modify the identity-field fill: do not confuse reference identity with tested-batch confirmation | **ACCEPTED IN FULL — you were right, and it is implemented** — §2 |
| 3 | Resolve the `NCT02623699` false positive and the partition-dependent `NCT03070119` flag in a crosswalk; the 21–29 range is not a verified interval | **ACCEPTED; range withdrawn** — §5 |
| 4 | Source-level timing and phenotype review of the 522 candidates; keep 21 sponsor and 48 ineligible grade-zero rows out of quantitative claims | **ACCEPTED — the queue is built and contains zero verdicts** — §4 |
| 5 | One cross-lineage human-compound crosswalk, 13 versus 39; compare source-resolved positional chemistry, not generic sugar descriptions | **ACCEPTED, not started; it is the gating item** — §5 |
| 6 | Recover valeriasen conditions; do not promote it; your original-branch claim is stale | **ACCEPTED; claim retracted** — §6 |

### Where I disagree

Nothing in this request. One correction to your round's inventory: it records *"Alternate hydrocephalus … reply's narrower verified-trial subset is 4 compounds, 2 sequences."* The sequence figure is **3**, not 2 — nusinersen (18 nt), tofersen (20) and tominersen (20) all carry sequences; only inclisiran does not. The error originated in my 10-01 reply and your round repeated it; both are now corrected.

---

## 2. Proposal 2 — the identity field. Implemented exactly as you specified.

Your objection was that copying `design_source` into analytical identity confuses **reference identity** (the designed molecule as a document printed it) with **tested-batch confirmation** (analysis of the vial that was dosed). Correct, and my 10-01 proposal would have manufactured the appearance of characterization. Four columns now, with the two kept apart:

| Column | State across 592 molecules |
|---|---|
| `sequence_provenance` | `publication_supplement` 222 · `patent_sequence_listing` 189 · `publication_main_text` 43 · `who_inn_nomenclature` 9 · `regulatory_document` 2 · `registry_metadata` 1 · `NOT_APPLICABLE` 126 |
| `purity_pct` | `NOT_REPORTED` **585** · `NOT_APPLICABLE` 7 |
| `purity_method` | `NOT_REPORTED` **585** · `NOT_APPLICABLE` 7 |
| `identity_confirmation` | `NOT_REPORTED` **585** · `NOT_APPLICABLE` 7 |

- **Never blank.** `qc_cns.py` fails on a blank, because a blank cannot be told from a question nobody asked.
- **`NOT_APPLICABLE` ≠ `NOT_REPORTED`.** Seven records are class-level or cohort-level aggregates — an NHP safety database, an adverse-event atlas, an unexposed disease-background comparator. The purity of "the ASO class" is a category error, not a gap.
- **The firewall is enforced, not promised.** QC fails if `identity_confirmation` ever equals a `sequence_provenance` category.
- **A value can only enter through a table that requires the document and the exact locus.** It is empty and must stay empty until someone reads a document that states a value.

**Zero reported values is verified, not assumed.** A full-text search of every measurement row's `notes` and `source_table`, and every oligo record's `notes`, for purity values, purification methods (HPLC, UPLC, AEX, mass spectrometry, desalting, salt exchange, phosphoramidite synthesis) and identity-confirmation statements returns **no hits across 2,538 rows and 592 records**.

**One lead recorded and deliberately not transcribed.** Your round reports that `doi:10.1089/nat.2021.0071` — which supplies 181 molecules here — states a purification method and an RP-UPLC-MS identity confirmation in a sibling lineage's extraction. I have not written it. A second-hand report of another session's extraction is not a document read during this curation, and the no-fabrication rule does not have an exception for a trustworthy colleague. It is in the acquisition plan at §3.

**Recording the columns' existence is not closure**, as both you and the hepatic request insist. The requirement is open; it is now *measurable*.

---

## 3. Proposal 1 and the acquisition attempt — what was obtained, and the exact barrier

### 3a. The sequence gap, with its denominator

**26 of 39 human-laboratory molecules carry no sequence** (13 do). Triaged by the licence of the source that would carry it:

| | Molecules | Sources |
|---|---:|---|
| **CC-BY — readable *and* republishable** | **17** | `10.1016/j.omtn.2025.102692` (11), `10.1016/j.xhgg.2025.100450` (4), `10.1186/s13024-024-00725-9` (2) |
| `summary_stat` — our licence policy bars bulk reproduction | 9 | five further DOIs |

**Your caveat is accepted and the triage is corrected accordingly.** A `summary_stat` tag records a *licence* limit, not evidence that a sequence is unpublished, and not that every form of factual reuse is barred. The two are now logged separately: the 9 are "rights question open", not "sequence unavailable". Within them, three are likely unpublished *by design* — two scramble controls and `BLOCK-iT Fluorescent Oligo`, a proprietary reagent.

### 3b. Europe PMC first, as the kidney lane found. It worked for full text.

All three CC-BY targets resolve to open-access PMC records **with supplements**:

| DOI | PMCID | OA | hasSuppl | full text |
|---|---|---|---|---|
| `10.1016/j.omtn.2025.102692` | PMC12744863 | Y | Y | **retrieved, 169,393 B** |
| `10.1016/j.xhgg.2025.100450` | PMC12148737 | Y | Y | **retrieved, 119,204 B** |
| `10.1186/s13024-024-00725-9` | PMC11040766 | Y | Y | **retrieved, 268,529 B** |
| `10.1056/NEJMoa2204705` | — | **N** | **N** | not in Europe PMC |

Staged under `toxicity/sources/cns/_staging_2026-10-02/` with `MANIFEST.csv` carrying SHA-256, byte count, retrieval URL, retrieval date, DOI/PMID/PMCID, the gap each addresses and the licence as recorded in this corpus.

### 3c. One partial recovery, not ingested

**`PMC12148737`'s main text carries three inline 20-mers** — `AGATTCGCCAACCCAGGAGC`, `CCCCACAGATTCGCCAACCC`, `GTCTGCCTCTCCCCACCAGG`. They are recorded in the manifest as **recovered candidates requiring verification**, and they are **not written into the dataset**: mapping a sequence to the right `oligo_id`, strand and per-position chemistry is extraction, which this round does not authorize. The other two papers carry **zero** inline 15–25mers; their sequences are in supplements.

### 3d. The barrier, typed precisely

Both supplement routes fail, and **neither failure is a paywall**:

| Route | Outcome | Barrier type |
|---|---|---|
| `europepmc.org/articles/<PMCID>/bin/mmc1.pdf` (and `mmc2`, `.xlsx`) | **HTTP 403**, `text/html` error page, all three papers, all four filenames | **technical blocking** (bot wall) |
| `europepmc.org/…/<PMCID>/supplementaryFiles` | HTTP 200 but **the whole package, no `Range` support** — it is generated on the fly, and exceeded **286 MB** for PMC12744863 before I stopped it | **impractical bulk route**, not an access denial |

The reason the package is enormous is visible in the full text's own file list: `mmc1.pdf, mmc2.mp4, mmc10.mp4, mmc11.mp4, mmc12.mp4, mmc13.mp4, mmc14.mp4, mmc15.pdf`. **The sequence table is in `mmc1.pdf`; the bulk is movie files.** I aborted the download and deleted the 286 MB partial rather than exhaust the session's disk allowance, and I did not retry the other two.

**These are open-access CC-BY papers.** Nothing is being paid for or circumvented — a free file is sitting behind a bot wall, and a browser would fetch each `mmc1.pdf` in seconds. That is the request at §7.

---

## 4. Proposal 4 — the 522-row queue, built, with zero verdicts

`chronic-neurotoxicity.chronic-eligibility-queue.csv`. My 10-01 reply deferred this to German, which was right about the verdict and wrong about the preparation: "German's call" had become a reason not to assemble the material.

**522 candidate rows** (`endpoint_domain` ∈ {`chronic_neurotoxicity` 290, `clinical_neuro_ae` 232}), sorted human-first by strength of timing evidence. `chronic_eligibility` and `chronic_eligibility_basis` are emitted **empty**.

| Evidence present | Rows |
|---|---:|
| `exposure_duration` as reported | 511 / 522 |
| verbatim **onset** snippet | 65 |
| verbatim **observation-window** snippet | 54 |
| verbatim **competing-explanation** snippet — the *source* raises it | 35 |
| a reversibility determination | 127 |

`timing_evidence`: `onset_and_window` 6 · `onset_only` 59 · `window_only` 48 · `duration_only` 404 · `none` 5.
By class: animal in-vivo 210 · trial registry 90 · label 59 · trial publication 55 · human laboratory 50 · sponsor 46 · class review 12.

Snippets are **extracted, never summarised** — the adjudicator reads the source's own words bounded to the matched region, with the exact locus alongside. **Exposure duration alone does not establish chronic injury**, as you say, which is why `duration_only` is the largest and weakest stratum.

**A trap worth naming.** "Onset" is ambiguous here: `infantile-onset SMA` and `later-onset SMA` name a disease phenotype, not when an event began. A naive match tagged rows on the population descriptor alone. Handing an adjudicator noise labelled as evidence is worse than handing them nothing, so the population forms are masked; `CMS1175`, `CMS1341` and `CMS1342` now correctly read `duration_only`, while `CMS1163` ("onset after 5-58 doses") and `CMS1201` ("developed a change in gait that progressed over 6 months to paraparesis") are kept.

**The 21 unquantified sponsor rows and the 48 ineligible grade-zero rows are excluded from every quantitative and negative claim**, by predicate (`ascertainment=review_required`, `negative_eligible=FALSE`), not by convention.

---

## 5. Proposals 3 and 5 — the crosswalk is the gating item, and the range is withdrawn

**Withdrawn:** the 21–29 verified-trial interval. Your objection is correct — I built it from the same extension flags I had just shown to carry a false positive on the parent (`NCT02623699`, triggered by a note that merely *mentions* the extension) and a partition-dependent false negative on the real extension (`NCT03070119`, flagged in one register and not the other). A range derived from unreliable flags is not a cohort interval. Nothing replaces it until the crosswalk is built from primary sources.

**My extension-counting rule, declared** because kidney's suggestions require it and I never had: **one `trial_key` per registry posting, overlap disclosed.** A choice, not a law, and the convention must be identical across all nine endpoints or no total is comparable.

**Not started, and it is the gate.** A record-level crosswalk keyed on (`source_ref`, trial identifier, compound identity, readout) across the three CNS lineages — **zero file moves**, a measurement rather than a consolidation. Measured overlap of source identifiers: this branch 91, `k394sz` 26, `t172zv` 167, sharing **17 / 27 / 22 pairwise**, concentrated in `NCT02519036`, `NCT02623699`, `NCT03070119`, `NCT03342053`, `NCT03761849`, `NCT01703988`, `NCT02193074`, `NCT02292537`, `NCT02386553`. Adding rows across lineages would multiply-count the same posted tables.

**On comparing source-resolved positional chemistry rather than generic sugar descriptions** — accepted, and now quantified. `cross_system_pairs_cns.py` computes **exact-construct identity** (base sequence *and* every recorded chemistry field) separately from **leakage grouping** (base sequence with U collapsed to T). Consequences:

- **168 of 581 records cannot be keyed exactly**, because a sequence or a chemistry field is missing. That is the characterization gap expressed as a matching limit.
- **8 exact-construct cross-band groups exist, every one animal-to-animal.** Not one spans a human band.
- The *"animal in vivo and human clinical = 12 molecule-records"* figure in my 10-01 replies is **withdrawn**: by identity it is 5, and by exact construct it is zero across a human band. It rested on the U→T key — the very normalisation I had flagged as unsafe in one section while relying on it in another.

**13 versus 39 human-laboratory compounds** is the crosswalk's first question and I have not answered it; it needs the original branch's records, not an inference from its counts.

---

## 6. Proposal 6 — valeriasen, and a retraction

**Retracted:** my statement that the original branch lacks trial and eligibility support. Your round reports its current register holds **22 trials with six extension flags**. Stale when I wrote it.

**valeriasen stays descriptive.** It is the only human-laboratory-to-human-clinical pair in this corpus: an n-of-1 ASO assayed in the patient's own *KCNT1* p.R474H iPSC-derived neurons, then given to that patient. The in-vitro assay found no injury — grade 0 on transcriptome-wide off-target DEGs and on neurite morphology — and the patient developed grade-3 raised intracranial pressure and status dystonicus. **A transcriptomic and morphological finding is not a general safety claim, and one discordant case is not predictive validation in either direction.** Its exact conditions and the source's own interpretation are an acquisition item (§7): the corpus holds the readouts but not the full exposure context, and its sources are `summary_stat`.

---

## 7. The twenty-source coverage log, and what it honestly says

Full log: **[`../chronic-neurotoxicity.search-log-2026-10-02.csv`](../chronic-neurotoxicity.search-log-2026-10-02.csv)** — 20 rows, one per resource, with query terms, date, HTTP outcome, result identifiers, finding, barrier and a `searched` flag. Generated by `scripts/search_log_cns.py --date 2026-10-02`, re-runnable.

**9 of 20 actually searched. 11 recorded as NOT searched, each with its barrier named.** Your instruction that blocked services must not be marked searched is the reason this is 9 and not 20 — the first run of my own script logged two HTTP 429s as successful, which I fixed before reporting.

| # | Resource | Outcome | Searched | What it gave |
|---|---|---|---|---|
| 1 | PubMed | HTTP 200 | **yes** | 19 PMIDs: oligo + analytical-characterization + CNS terms (G2) |
| 2 | Europe PMC | HTTP 200 | **yes** | open-access hits pairing human iPSC neural systems with oligo toxicity; `fullTextXML` retrievable (G1, G3) |
| 3 | OpenAlex | **HTTP 429** | no | rate-limited, with `retryAfter`; two polite retries also 429 |
| 4 | Semantic Scholar | **HTTP 429** | no | unauthenticated Graph API rate-limited; an API key would fix it. Not a paywall |
| 5–8 | ResearchRabbit · Undermind · Elicit · Consensus | HTTP 200 (landing) | no | no public search API; search needs an authenticated interactive session. **No query issued, so not searched.** Discovery aids, not primary evidence |
| 9 | GEO | HTTP 200 | **yes** | 38 series. Caveat carried: a transcriptome of treated cells is not the administered construct |
| 10 | SRA | HTTP 200 | **yes** | 0 runs. Low applicability: a sequenced biological sample is not the dosed oligonucleotide |
| 11 | PRIDE | HTTP 200 | **yes** | proteomics deposits; relevant only to protein-level neuro markers |
| 12 | ProteomeXchange | non-JSON | no | PROXI endpoint did not return parseable JSON; aggregates PRIDE anyway — deduplicate before counting |
| 13 | BioStudies | HTTP 200 | **yes** | 28,486 hits — far too broad to be a finding; needs construct-alias and accession-level queries |
| 14 | ArrayExpress (in BioStudies) | HTTP 200 | **yes** | collection within 13; deduplicate against it |
| 15 | ClinicalTrials.gov | HTTP 200 | **yes** | trial identifiers. Registration alone does not establish an observed outcome — only a posted results module does |
| 16 | Comparative Toxicogenomics DB | HTTP 302 | no | no verified open search API. Also low applicability: contextual/inferred relationships cannot replace observed sequence-linked outcomes |
| 17 | ICE | HTTP 200 | no | interactive portal; bulk download needs a session. Small-molecule dominated |
| 18 | ToxCast | HTTP 200 | no | documentation page only; its chemical library does not carry therapeutic ASOs. Justified low applicability |
| 19 | Zenodo | **HTTP 403** | no | bot-walled HTML error page |
| 20 | Dryad | HTTP 200 | **yes** | 1 dataset |

**The barriers are upstream, not local.** The agent proxy reports `recentRelayFailures: []` and no download gating, so the 429s and 403s are the services' own responses.

**What the log does not claim.** BioStudies' 28,486 hits is a query-design failure, not a finding — the right queries are construct aliases and the accessions named in priority papers' data-availability statements, which is next-round work. Four discovery products remain unsearched and I am not asking for subscriptions to them; a search-product subscription does not unlock publisher content.

---

## 8. Paper, supplement and raw-file access table

| Citation | Where discovered | Publisher / repository | Exact file needed | Gap | Expected gain | Access attempts (2026-10-02) | Outcome | Barrier type | Priority |
|---|---|---|---|---|---|---|---|---|---|
| **Wang et al.**, "Unraveling and controlling late-onset neurotoxicity of antisense oligonucleotides…", *Mol Ther Nucleic Acids* 2025, `10.1016/j.omtn.2025.102692`, PMC12744863 | already cited by 11 corpus molecules; confirmed OA via Europe PMC | Elsevier / Cell Press; mirrored in Europe PMC | **`mmc1.pdf`** (sequence/chemistry table) | G1 | up to **11** human-laboratory molecules gain sequence + per-position chemistry | Europe PMC `fullTextXML` → **200, retrieved**; `/bin/mmc1.pdf` → **403**; `/supplementaryFiles` → 200 but whole package, no Range, aborted at 286 MB (embeds 6 `.mp4`) | main text obtained, **supplement not** | **technical blocking** (bot wall) + impractical bulk route. **Not a paywall** — CC-BY | **High** |
| **Dhamija et al.** (PPP2R5D), *HGG Adv* 2025, `10.1016/j.xhgg.2025.100450`, PMC12148737 | as above | Elsevier / Cell Press; Europe PMC | **`mmc1.pdf`**, `mmc2.pdf` | G1 | up to **4** molecules; **3 inline 20-mers already recovered** from the main text | same routes; full text **200, retrieved** | main text obtained + 3 candidate sequences; supplement not | same | **High** |
| **Ferrari et al.** (human microglia ASOs), *Mol Neurodegener* 2024, `10.1186/s13024-024-00725-9`, PMC11040766 | as above | BMC / Springer Nature; Europe PMC | supplementary table | G1 | **2** molecules — `APOE ASO-1`, `TREM2 ASO-171`, the only two human-lab/animal-lab exact-compound pairs in the corpus | full text **200, retrieved** (0 inline sequences) | main text obtained, supplement not | same | **High** |
| **Miller TM et al.**, "Trial of Antisense Oligonucleotide Tofersen for SOD1 ALS", *NEJM* 2022;387(12):1099-1110, `10.1056/NEJMoa2204705` | Beebop's 2026-10-01 lead; already in the access register | NEJM / Massachusetts Medical Society | **Supplementary Appendix** (Fig. S3 disposition flow; Sections S1–S4) **and the trial protocol** | G4 | pins the `NCT02623699` → `NCT03070119` extension population exactly; settles the counting rule in §5 | White Rose deposit → **200**, main article only, 13 pp; White Rose record page → one document, no appendix; Europe PMC → **no record** (not OA, `inEPMC=N`, `hasSuppl=N`) | main article obtained earlier; **appendix and protocol not** | **missing supplement**. The main article is free by this route; the appendix is off-site at NEJM.org | **High** |
| `doi:10.1089/nat.2021.0071` (Hagedorn; supplies 181 molecules here) | your 2026-10-02 round reports a sibling lineage found purification method + RP-UPLC-MS identity in it | Mary Ann Liebert | the methods/supplement section stating purification and identity confirmation | **G2** | would be the **first** purity-method and analytical-identity evidence in this corpus — currently 0/592 | **not attempted this round** | — | unknown; to be established, not assumed | **High** |
| `doi:10.1038/s41591-026-04314-9` and `doi:10.1093/nar/gkaf346` (valeriasen) | corpus, `summary_stat` | Nature Medicine; NAR | exposure conditions and the authors' own interpretation of the laboratory-to-clinical discordance | G3 | the context for the corpus's only human-lab/human-clinical pair | not attempted this round | — | rights question open (`summary_stat` ≠ unpublished) | Medium |

**Nothing was purchased, no subscription taken, no credential requested, no author or sponsor contacted.** No price is recorded anywhere, because none was displayed to me — per the register's rule, subscription and entitlement status stays **unverified/unknown**.

**Request to Oscar, in the register's wording.** *Please provide `mmc1.pdf` for `10.1016/j.omtn.2025.102692`, `10.1016/j.xhgg.2025.100450` and `10.1186/s13024-024-00725-9` (CNS, chronic neurotoxicity). They are needed to verify sequences and per-position chemistry for up to 17 human-laboratory molecules that currently have none. We checked Europe PMC's per-file route (HTTP 403 bot wall) and its bulk package route (no Range support, 286 MB, embeds video). The main articles alone are **not** sufficient — two of the three carry no inline sequences. These are CC-BY open-access files; a human browser session would download each in seconds, and no payment is involved.* The NEJM supplementary appendix is the one item that may genuinely require your access rather than a browser.

---

## 9. Current inventory at commit

Chronic partition, `claude/oligo-cns-toxicity-dataset-tijib6`:

| | Count |
|---|---:|
| Measurement rows | **2,393** |
| Oligo records | **573** |
| …with a published sequence ≥12 nt | 458 |
| Human rows — all classes | **530** |
| …human laboratory | **116** over 39 molecules |
| …human trial-derived | **295** |
| Animal rows (supporting) | 1,863 |
| Verified unique human trials | **27** |
| Pending trial candidates | 19 |
| `source_id` / `source_ref` | 94 / 89 |
| Grade-0 rows eligible as negatives | 1,135 |
| …**not** eligible | 48 |

**Source-verified coverage for the human subsets, with denominators** — and the headline misleads in the direction you warned about:

| Field | Human laboratory (39) | Human trial-derived (22) | Animal (520) |
|---|---|---|---|
| published sequence ≥12 nt | **13 (33%)** | 10 (45%) | 441 (85%) |
| `ps_count` | 11 (28%) | 10 (45%) | 421 (81%) |
| `gapmer_design` | 7 (18%) | 8 (36%) | 435 (84%) |
| `backbone_chemistry` | 30 (77%) | 12 (55%) | 449 (86%) |
| `sugar_modifications` | 31 (79%) | 13 (59%) | 449 (86%) |
| **purity, any form** | **0** | **0** | **0** |
| **analytical identity of tested material** | **0** | **0** | **0** |

The corpus-level "466 of 592 carry a sequence" figure is carried almost entirely by animal patent panels. **The human subset is the least characterised part of this dataset.**

**Two qualifications I will not paper over.** A populated sequence is **not** a source-verified one: the 458 chronic sequences carry a `design_source` locus, but no independent orientation, strand or duplex-identity verification pass has been run. And **generic sugar descriptions are not per-position chemistry** — `sugar_modifications` holds strings like `2'-MOE;DNA_gap`, which state a design pattern, not a position-resolved map. Your request draws exactly that line and this corpus does not yet meet it.

**Remaining qualification blockers:** chronic eligibility unadjudicated on all 522 candidates; grades provisional throughout; no lineage selected; no tested-material characterization anywhere.

---

## 10. Work performed versus proposed

**Performed this round:** the characterization columns and their QC firewall; the three-instrument separation; the macrocephaly re-tier; exact-construct identity separated from leakage grouping; the 522-row queue; the 20-resource search sweep; three full texts retrieved and staged with checksums; three candidate sequences recovered and *not* ingested; four corrections to my own published claims.

**Proposed, not performed:** the cross-lineage crosswalk (gating, needs nothing but time); the three `mmc1.pdf` files (blocked, §8); the Hagedorn purification method (not attempted); valeriasen conditions (not attempted); BioStudies and ClinicalTrials.gov re-queried at accession and alias level (query design, next round); the narrative's required *"discussion of how the data could be used to develop a predictive model"* — a Phase 2 deliverable I had not previously listed.

**Shared-source ownership.** The tofersen appendix is now a CNS-only request: the kidney lane's 2026-10-01 reply struck that paper from its own list, having read it in full and found *"zero occurrences of creatinine, renal, proteinuria, eGFR, kidney or nephr-"*. The Europe PMC `fullTextXML` route came from that same reply; credit to the kidney lane, and the hydrocephalus and acute reports reference this table rather than filing duplicates.

---

## 11. What needs Oscar, and what needs German

**Oscar — implementation and scope:**
1. **A browser-session download of three CC-BY `mmc1.pdf` files** (§8). Free, open-access, bot-walled.
2. **Which CNS lineage is the submission** — after the crosswalk, not before.
3. **The extension-counting convention**, identical across nine endpoints.
4. **Phase 2 has a deadline of 2026-12-31 and the CNS endpoints have no narrative, no methodology document and no PADP.** The `PADP.md` and `METHODOLOGY.md` at this branch's root are kidney-lineage leftovers, as are `kidney-nephrotoxicity.*.csv`, which should be declared non-authoritative. At 90 days this sequencing is a larger risk than any single data item in this report.

**German — scientific adjudication:**
5. `chronic_eligibility` on 522 rows: adopt it, with what categories, and who adjudicates (§4).
6. Whether the three `score_0_to_7` instruments may ever be pooled — 375 rows. Separation is done and needed no verdict.
7. Whether infant **macrocephaly** is a direct hydrocephalus endpoint — re-tiered to `related_clinical_sign` on the source's own evidence (no imaging), reversibly.
8. Grade calibration across evidence classes; all grades remain provisional.
9. The **valeriasen** discordance: how, and whether, it belongs in the submission.

---

**RESEARCH REPORT COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**

---
_Generated by [Claude Code](https://claude.ai/code)_
