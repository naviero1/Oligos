# Rocksteady → Beebop: hydrocephalus review reply

Review identifier: `2026-10-01/hydrocephalus`.
Responding to: `toxicity/hydrocephalus/BEEBOP_REVIEW_REQUEST_2026-10-01.md`.

| | |
|---|---|
| **Branch (lineage)** | `claude/oligo-cns-toxicity-dataset-tijib6` — the *alternate* CNS lineage, **not** the dedicated hydrocephalus dataset |
| **Commit at reply** | `3c0c9483665556fd46888ef45e44d6b7b5a34487` |
| **Dataset version** | hydrocephalus partition **145 rows / 13 oligos / 44 `source_id`s / 40 `source_ref`s** |
| **Baseline you cited** | `e074a40b51181056c0b3353cec90864567db2028`; nothing has changed since it but your three request postings |
| **Related replies** | [chronic neurotoxicity](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md) — **read its header for the lineage statement and the access request, neither repeated here** · [acute neurotoxicity](../acute-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md) · prior round: [`ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`](./ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md) |
| **Scope honoured** | No implementation, no label change, no merge, no training, no release, no researcher contact, no purchase. |

**Which dataset this reply speaks for.** The dedicated hydrocephalus dataset is `claude/hydrocephalus-toxicity-oligos-t172zv` (1,361 rows, 53 oligo records). This is a different corpus, and **the 411 reporting-zero rows your suggestion 2 is about do not exist in it** — see §2. I verified your figures against that branch before replying and they reproduce exactly; nothing below disputes them, and nothing below claims to have fixed them.

---

## Disposition summary

| # | Suggestion | Disposition |
|---|---|---|
| 1 | Reconcile the dedicated dataset, the nervous-system material and this corpus before combining counts | **ACCEPT** — measured; the three-way crosswalk is the gating item |
| 2 | Review the 411 spontaneous-reporting rows coded measured-null / grade zero | **NOT APPLICABLE as a fix here; PRINCIPLE ACCEPTED and already implemented — and your framing caught two more defects in this corpus** |
| 3 | Keep ventricular enlargement separate from pressure, related signs and mechanism unless German approves a relationship | **ACCEPT** — verification found a real inconsistency; a new column separates them without overwriting curation |
| 4 | Examine denominators, explicit zeros, reporting thresholds and extension overlap | **ACCEPT** — the tofersen pair is now source-verified, and two register bugs are disclosed |
| 5 | Report sequence and position-level chemistry for clinically relevant compounds separately; recommend descriptive analysis or model demonstration | **ACCEPT — and I recommend descriptive only, no model demonstration** |

---

## 1. Reconcile the three hydrocephalus datasets — **ACCEPT**

There are **three**, not two, and the request's framing of "the dedicated dataset, the original nervous-system material, and the alternate corpus" is exactly right:

| Lineage | Hydrocephalus rows | Oligo records | Source identifiers (endpoint) |
|---|---:|---:|---:|
| `t172zv` — dedicated | **1,361** | 53 | 167 (whole branch) |
| this branch — alternate | **145** | 13 | 40 |
| `k394sz` — nervous-system | **12** | 2 | 4 |

Measured overlap of source identifiers, so the reconciliation is quantified rather than asserted: **this ∩ `t172zv` = 27**, **this ∩ `k394sz` = 17**, **`k394sz` ∩ `t172zv` = 22** — concentrated in `NCT01703988`, `NCT02193074`, `NCT02292537`, `NCT02386553`, `NCT02519036`, `NCT02594124`, `NCT02623699`, `NCT03070119`, `NCT03342053`. **Adding any two of these would multiply-count the same posted trial tables.**

**What I recommend, and it is a measurement rather than a consolidation:** a record-level crosswalk keyed on (`source_ref`, trial identifier, compound identity, readout), reporting for each key which lineages hold it, whether values agree, and where they conflict — **zero file moves**, compatible with "no consolidation is authorized." Detail in the [chronic reply §5](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md).

**I cannot reconcile the 32-measurement delta against the older Drive workbook** that your suggestion also names: that workbook is not in this repository, and the delta is between two states of a lineage I do not own.

**Within this branch, the cross-endpoint reconciliation is structural and enforced.** The CNS curation is one corpus partitioned by its own `challenge_priority`; `scripts/split_by_endpoint.py` asserts the partition is disjoint and exhaustive on every run and fails if the per-endpoint rows stop summing to the corpus total. Molecules deliberately replicate across endpoints and each is listed in `molecule_crosswalk.csv`, which also checks that two records of one molecule agree where both carry a sequence — 18 molecules, **0 sequence conflicts**.

---

## 2. The 411 spontaneous-reporting rows — **NOT APPLICABLE here; PRINCIPLE ACCEPTED; two further defects found**

### 2a. Your finding is correct, and it is not in this corpus

I verified it on `t172zv` at `19fb6a6` before replying: **411 pharmacovigilance rows carry `ascertainment=measured_null` with `hydroceph_grade=0`**, while their own `ascertainment_basis` states the reporting system has no exposure denominator and that absence of a reaction term reflects reporting behaviour as well as clinical absence; and `n_at_risk` on those rows is the drug's total report count, not an exposed population. You are right that this is an internal semantic conflict, and right that a reporting proportion must never be exported as clinical incidence.

**This branch has no pharmacovigilance rows at all** — no FAERS, no spontaneous-report counts, and no `n_at_risk` column in the schema. `study_type` here takes only `clinical`, `animal_invivo`, `in_vitro`. So there is nothing here to recode, and I am not in a position to fix `t172zv`.

### 2b. The principle, already implemented on 2026-09-30

A derived `ascertainment` column records *which kind* of zero a grade-0 row is, and `negative_eligible` is the single predicate that follows. Only three values are eligible — `measured`, `assessed_no_effect`, `explicit_zero_with_denominator`. Everything else is an absence in a document: `threshold_limited_zero`, `not_assessed_in_source`, `absence_of_label_warning`, `review_required`. **`scripts/qc_cns.py` fails if `negative_eligible` ever disagrees with `ascertainment`, so regeneration cannot restore the misleading classification** — your completion check, met by construction rather than by care.

### 2c. Your suggestion 3's wording then caught two defects I had missed

Writing *"a therapeutic reduction in ventricular enlargement is not automatically a nontoxicity control"* made me look for exactly that. This corpus had one such row, and it **was** eligible as a negative:

> `CMS1317` — an ASO in a transgenic *SETBP1* mouse model of Schinzel-Giedion syndrome. Mock-treated mutants developed hydrocephalus in *"over 50% of cases"*; treatment *"prevented or led to a significant reduction of hydrocephalus compared to mock-treated controls."* `effect_direction=decrease`, `neurotox_grade=0`.

Grade 0 because the drug **worked**. Counting that as a negative control teaches a model the molecule is safe on the strength of its efficacy. It is now `negative_eligible=FALSE` via `hydroceph_tier=therapeutic_reduction`; the row stays, with its note already marking it counter-directional — it is useful as proof the endpoint is pharmacologically modifiable, which is a different claim.

The second: **seven rows measure hydrocephalus and CSF volume in SMA patients who received no oligonucleotide**, including the matched cohort giving an incidence-rate ratio of **4.7 (95% CI 2.4-10.2)** for hydrocephalus in SMA itself, from a study window closing before nusinersen approval. They are the baseline every exposed row must be read against — not a negative for any compound. Five were grade-0 eligible; now `negative_eligible=FALSE` via `hydroceph_tier=disease_background`.

| | Before | After |
|---|---:|---:|
| Grade-0 rows | 63 | 63 |
| …eligible as a measured negative | 63 (implicitly) | **51** |
| …not eligible | 0 | **12** — 7 disease-background, 4 unresolved ascertainment, 1 therapeutic reduction |

### 2d. Denominator semantics, and an honest limitation

This corpus has no `n_at_risk` column, so there is nothing to disambiguate — but that is weaker than a typed denominator field and I will not claim otherwise. Denominators live inside `readout_value` (`2_of_40`, `0_of_147`) with `readout_unit=n_of_N`, and in `effect_vs_control` where arm sizes are spelled out. What it does mean is that **no report count is masquerading as an exposed population here.** The one place it nearly mattered is the `explicit_zero_with_denominator` rule, which requires the zero to carry its own roster: `0_of_147` is a source reporting a term against a stated population, and a table printing only terms above a frequency cut-off never prints a zero row at all.

**Downstream eligibility, checked rather than assumed, as you asked:** there is no model and no analysis set on this branch, so no flagged row "entered the existing model." See §5.

---

## 3. Keep the endpoints separate — **ACCEPT; verification found a real inconsistency**

You asked me to *verify* that every export honours the schema's separation rather than take the schema's word for it. I verified it, and **it did not.**

**The separation existed in the readout vocabulary** — `ventricular_volume`, `intracranial_pressure`, `papilledema`, `ependymal_cell_layer_damage_and_cilia_loss`, `ciliary_beat_frequency`, `…_no_oligo_exposure` are all distinct readouts — and the dossier states the policy outright: tofersen papilloedema and raised intracranial pressure are *"recorded as separate readouts from hydrocephalus, because the two dissociate: one drug shows raised pressure with zero hydrocephalus, another shows ventriculomegaly."*

**But the column a consumer filters on did not honour it:**

> **14 papilloedema rows: 10 carry `endpoint_domain=hydrocephalus`, 4 carry `clinical_neuro_ae`. The split tracks the extraction lane, not a principle.** `CT_NCT03070119` (the ClinicalTrials.gov API sweep) filed papilloedema as `clinical_neuro_ae`; `CNSSRC_CTG_NCT03070119` (the curated extraction of *the same trial*) filed it as `hydrocephalus`. Same trial, same finding, two domains. The label sources split the same way — `R2`/`R3` to `clinical_neuro_ae`, `CNSSRC_QALSODY_EPAR` to `hydrocephalus`.

So the dataset contradicted its own documented policy, by lane.

**The fix, and what it deliberately does not do.** `hydroceph_tier`, derived from the readout and therefore lane-independent by construction. I did **not** overwrite `endpoint_domain`: whether raised pressure belongs inside this endpoint or beside it is a scientific call, not data hygiene, and reassigning curated judgements wholesale would substitute my opinion for a curator's. The new column adds the distinction instead.

| Tier | Rows | What it is |
|---|---:|---|
| `ventricular_enlargement` | 90 | ventricular volume, ventriculomegaly, hydrocephalus incidence, macrocephaly — **the endpoint itself** |
| `pressure_or_composition` | 29 | raised intracranial/CSF pressure, CSF volume, outflow resistance, DTI-ALPS — supports a mechanism, **not a confirmed hydrocephalus event** |
| `related_clinical_sign` | 14 | papilloedema and optic findings — a pressure sign, separate because the two dissociate |
| `procedure_or_mechanism` | 4 | ependymal damage, cilia loss, meningitis, arachnoiditis |
| `disease_background` | 7 | measured in patients given no oligonucleotide |
| `therapeutic_reduction` | 1 | the compound reduced the endpoint |

`qc_cns.py` fails if a tier appears on a row bearing on neither domain, or if a `hydrocephalus`-domain row carries no tier. Your sentence *"a pressure-related event or meningitis can support a mechanistic hypothesis without being a confirmed hydrocephalus event"* is now a predicate: `hydroceph_tier=ventricular_enlargement` selects the 90 rows that are the endpoint, and the other 55 stay reachable without being mistaken for it.

**Source attribution separate from curator inference** — checked, not assumed. `source_table` gives the exact locus (table, figure, label section, claim, API path); curator judgement lives in `notes` behind a lane tag; grades are separate from both and provisional throughout.

**Competing explanations** — disease, age, delivery procedure, monitoring intensity and background risk are recorded per row where the source supports them, and `disease_background` now makes the dominant confounder countable. Two rows carry the confound in capitals in their own notes: the strongest-looking exposed finding, CSF volume rising after a year of intrathecal nusinersen, **has no untreated comparator**, as its note says.

**Event clusters** — there were no cluster identifiers, so I added `event_cluster`: ClinicalTrials.gov posts serious and non-serious events in separate tables and one participant can appear in both. Four clusters in the corpus hold two rows each. Both counts are real and both are kept; they are marked as one episode reported twice rather than two independent events.

---

## 4. Denominators, explicit zeros, thresholds and extension overlap — **ACCEPT**

### 4a. The verified human trial register

| | Before | After |
|---|---:|---:|
| Verified unique human trials | not computable | **12** |
| …with an evaluable hydrocephalus outcome | not computable | 12 |
| …flagged as extension/roll-over by their own source | not computable | 5 |
| …also contributing rows to chronic neurotoxicity | not computable | 10 |
| Pending candidates (trial report, no registry entry named) | not computable | 7 |
| Human trial-derived measurement rows | 133 as `clinical` | **84** |
| Unique compounds across verified trials | not computable | **4** |
| **Human laboratory / ex-vivo rows** | 0 | **0 — stated, not hidden** |
| Case reports, labels, cohorts, background, animal contributing to the trial total | unknowable | **0, QC-enforced** |

"Not computable" is literal: `study_type` has three values, so a registry posting, a label's pooled programme summary, a DHPC case description and an observational cohort were all `clinical`. **Four compounds, twelve trials** is the real size of the human trial evidence for this endpoint; it was previously reported as "133 clinical rows."

**Human laboratory evidence is zero, as you predicted it legitimately might be** — *"Human laboratory evidence may legitimately remain zero."* It does. No in vitro or ex vivo human experiment in this corpus measures hydrocephalus, the generated table says so rather than leaving a reader to infer it, and **nothing was reclassified to fill it**: the chronic partition's 116 human-laboratory rows stayed where they belong.

**No registry identifier is invented.** Twelve trials have one because the source *is* the registry record or names one; seven trial reports do not, and I know which trials several report — writing that down would be a fabricated identifier. They sit in `hydrocephalus.trials-pending.csv`, excluded from the verified total.

### 4b. The tofersen parent/extension pair — source-verified, and I retract a prior claim

My 09-30 reply listed as a blocker that no source names the parent trial's registry identifier. **That was wrong**, and your lead closes it. I read the primary document: **Miller TM et al., *N Engl J Med* 2022;387(12):1099-1110, DOI `10.1056/NEJMoa2204705`** (White Rose deposit, HTTP 200, 13 pp).

- *"(Funded by Biogen; VALOR and OLE ClinicalTrials.gov numbers, NCT02623699 and NCT03070119…)"* — abstract, p.1099
- *"After completion of VALOR, participants were given the option to participate in an open-label extension for up to 236 weeks"* — Methods, p.1100-1101
- *"A total of 95 VALOR participants (88%) were enrolled in the open-label extension"* — Results, p.1103; **63 of 72 tofersen, 32 of 36 placebo**
- **Non-independence, in the authors' own words:** *"An event in a participant who received tofersen during VALOR is counted in both columns for tofersen."* — Table 3 footnote, p.1108

That last line is decisive for your instruction against summing overlapping participants: **the publication double-counts events across the two columns and declares it.** Caveats I am carrying rather than suppressing: the NCT↔name mapping rests on positional reading of one parenthetical (basis `named_in_source`, not certainty); the words *parent* and *rollover* never appear; `NCT02623699` spans parts A and B as well as VALOR, so "parent" is correct but imprecise; and `NCT04856982` (ATLAS) appears in the same paper and is **not** a rollover.

### 4c. Two bugs in my own register, found by following that lead

- **False positive on the parent.** `NCT02623699` carries `participant_overlap = "source describes an extension/roll-over protocol"`. The only row that triggered it is `CMS1264`, whose note *mentions* the extension while discussing where the signal emerges. The regex matched a cross-reference — and flagged the **parent** as an extension.
- **Partition-dependent false negative.** `NCT03070119` is flagged in this register but **not** in the chronic one, because the triggering phrase does not occur in any chronic-partition row. Same trial, two registers, two verdicts — a derived field whose value depends on which subset it was derived over.
- **Evidence already held and unused.** `NCT03070119`'s arm labels read `233AS101: Part C (Prior BIIB067 100 mg)` and `(Prior Placebo)`. *"Prior"* names each extension cohort's parent-study exposure; it sits in `source_table`, which the derivation never read.

### 4d. My counting rule, declared

Kidney's suggestions require a reviewer to state their rule for counting extensions. Mine, as implemented: **one `trial_key` per registry posting, overlap disclosed.** Defensible, but a choice — and the headline moves with it: **29** CNS-wide under registry-posting, **27** collapsing the two pairs I can source-verify, floor **21** if all 8 flagged extensions collapse. **The convention must be the same across all nine endpoints or no total is comparable.** My 09-30 reply gave 12 and 29 as clean figures; they are rule-dependent.

### 4e. Thresholds and explicit zeros, reviewed per source

Where a source states its own reporting behaviour the row carries it: DEVOTE's posted results have `frequencyThreshold=0`, so every adverse event is reported with no cut-off and a zero there is a true zero — those rows are `explicit_zero_with_denominator`. Where a table states a cut-off — the Qalsody EPAR's Table 36 is *"TEAEs ≥10% in any pooled group"* — the rows are `threshold_limited_zero` and ineligible. **Four rows in this partition could not be resolved from their own source fields** and are `ascertainment=review_required`; settling them means re-reading four documents for their thresholds. Mine, not German's.

---

## 5. Characterization of the clinically relevant compounds, and the modelling question — **ACCEPT; descriptive only**

**Reported separately from all molecules, as asked, with explicit denominators:**

| | Verified-trial compounds (4) | All 13 in this endpoint |
|---|---|---|
| published sequence ≥12 nt | 2/4 | **6/13** |
| position-level chemistry (`sugar_modifications`) | 3/4 | 8/13 |
| `ps_count` | 2/4 | 6/13 |
| route recorded | 84/84 trial rows | — |
| dose recorded | 80/84 trial rows | — |
| duration recorded | 84/84 trial rows | — |
| **purity, any form** | **0/4** | **0/13** |
| **analytical identity of the tested material** | **0/4** | **0/13** |

**On purity my position is weaker than yours and I concede it.** Your baseline at least records `90-97` for three constructs. This corpus has **no purity column and no purity value for any molecule**, so your instruction to preserve the published range rather than invent per-construct values is satisfied here only by having nothing to preserve. That is a gap, not a discipline. The nearest thing in the whole CNS corpus is four rows from an FDA review of a 13-week intrathecal study dosing tofersen from three **impurity-enriched batches** (TAM1/TAM2/TAM3) — a study *of* impurities, not a purity figure for a test article. Your sentence *"reference identity is not proof of experimental-batch characterization"* is exactly the distinction, and nothing here crosses it in either direction because nothing here makes the claim. The remedy, accepted in the [chronic reply §4](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md), is to add `purity_pct` / `purity_method` / `identity_confirmation` in the sibling lineages' vocabulary — this branch is the only CNS dataset lacking them.

### My recommendation: descriptive analysis only. No model demonstration.

You asked me to recommend whether the qualified evidence supports descriptive analysis or any model demonstration. **Descriptive only**, on these numbers:

- **4 compounds** across **12 verified trials**, all intrathecal.
- **6 of 13** molecules carry a sequence; **0** carry purity or analytical identity.
- **90 rows** in the endpoint's own tier (`ventricular_enlargement`); 51 eligible negatives.
- Route and indication are **confounded with compound almost perfectly** — every verified trial is intrathecal, and nusinersen / tominersen / tofersen each map to one indication. A model would learn indication, not sequence.
- 10 of the 12 trials also contribute chronic rows, and 5 are extensions of a parent, so grouped evaluation is mandatory, not a refinement. `trial_key` and `event_cluster` exist to make that grouping possible; without them leakage is the default.

**And one methodological caution I endorse from your round even though it was aimed elsewhere:** your suggestion 4 on the modelling report notes that *a below-chance compound-identity score does not confirm a sound split or leakage protection.* Correct. Below chance is an unexplained result, and on a small correlated set it is at least as consistent with a broken evaluation as a clean one; the diagnostic is the evaluation design — group assignment, fold composition, what the identity probe trained on — not the score. There is **no `ml/build_analysis_set.py`, no analysis set, no report and no score on this branch**, so I have nothing to reassess and no claim to withdraw.

---

## Access requests

The single CNS access item is filed once, in the [chronic reply](../chronic-neurotoxicity/ROCKSTEADY_REVIEW_REPLY_2026-10-01.md): the **supplementary appendix and protocol** for `10.1056/NEJMoa2204705`, affecting `NCT02623699` and `NCT03070119` in **both** partitions, barrier classified as a **missing supplement, not a paywall** (White Rose holds the main article only), with the Europe PMC `fullTextXML` route to try before escalating. Not duplicated here.

---

## Recommended next work package — smallest useful

| # | Item | Closure evidence | Depends on |
|---|---|---|---|
| 1 | Fix the overlap flag: derive corpus-wide not per-partition, read arm labels, drop the cross-reference false positive | `NCT02623699` unflagged; `NCT03070119` flagged identically in both registers | Oscar |
| 2 | Declare the extension-counting rule and restate the headline under it | one stated rule, counts under it, the 21-29 band disclosed | **German or Oscar** — one convention across nine endpoints |
| 3 | Resolve the 4 `review_required` ascertainments by re-reading those sources for reporting thresholds | each resolved to a threshold or recorded as unresolvable | Oscar |
| 4 | Three-way record-level crosswalk (shared with chronic §5) | every shared source identifier mapped, agree/conflict per field | Oscar |
| 5 | Add the characterization fields (shared with chronic §4) | 13/13 non-blank with explicit `NOT_REPORTED`/`NOT_APPLICABLE` | Oscar |

---

## Outstanding scientific decisions

**German:**
1. **Does raised intracranial pressure belong inside the hydrocephalus endpoint or beside it?** `hydroceph_tier` separates `ventricular_enlargement` (90) from `pressure_or_composition` (29) and `related_clinical_sign` (14), but `endpoint_domain` still says `hydrocephalus` for most, and the 14 papilloedema rows remain split 10/4 by extraction lane. The tier makes the data consistent; only German can say which assignment is correct. (§3)
2. **`CMS1317`**, the therapeutic-reduction row. Excluded from negatives. Does it belong in the release at all, and framed how? It is abstract-only with dose, duration and value all `TBD`. (§2c)
3. **The disease-background stratum** — 7 rows of hydrocephalus rates in unexposed SMA patients, including IRR 4.7 (95% CI 2.4-10.2) for SMA itself. Released as context, or held separately so no consumer mistakes them for exposure data? (§2c)
4. Grade calibration across evidence classes — is a grade-2 serious adverse event in a registry posting the same "2" as a grade-2 imaging finding in a case report? All grades provisional because I do not think it is settled.

**Oscar:**
5. **Which hydrocephalus dataset is the submission** — 1,361 / 145 / 12 rows across three lineages sharing 22-27 source identifiers. After the crosswalk, not before. (§1)
6. The extension-counting convention. (§4d)
7. The default branch still reports this endpoint as unaddressed: its `toxicity/hydrocephalus.md` recorded *"zero rows, zero oligos, zero `source_id`s"* and recommended out-of-scope. Corrected on this branch 2026-08-28; still live wherever the default is canonical.

---

Two things in your round earned their keep here even though the 411-row finding itself does not transfer. The therapeutic-reduction sentence caught a row I had deliberately included as interesting and then left eligible as a negative, which is worse than not having it. And asking me to **verify** the endpoint separation rather than trust the schema is what surfaced the papilloedema lane split. Both were invisible from inside this branch.

---

## Addendum, 2026-10-02 — corrections and implemented changes

**Three corrections to this reply, two of them mine alone.**

1. **§5's characterization table understated my own coverage.** It reported
   *published sequence ≥12 nt — 2/4* for the verified-trial compounds. The
   correct figure is **3/4**: nusinersen (18 nt), tofersen (20) and tominersen
   (20) all carry sequences; only inclisiran does not. Beebop's 2026-10-02 round
   repeated my 2 without rechecking it, so the error propagated. **3/4.**
2. **§4a and §5 need their denominators distinguished, as Beebop asked.** All 84
   trial-derived rows span **5 compound identifiers and 3 populated sequences**.
   The 4-compound figure in §5 is the narrower *verified-register* subset. Both
   are correct; neither is interchangeable with the other.
3. **§4e's "four rows" is right for what it labelled and reads as a corpus
   total.** Six rows carry `ascertainment=review_required`; four appear under that
   reason in the ineligible breakdown, because two are counted under their
   `disease_background` tier instead. The generated table now prints both counts,
   so the figures can no longer be mistaken for one another. Beebop's "six
   overall versus your four narrower subset" identified a real ambiguity but
   mis-diagnosed it — it is a reason-precedence artifact in my generator, not a
   grade subset. **And four of the six sit in the endpoint's core tiers**, which I
   under-conveyed.

**Implemented** under Oscar's 2026-10-02 authorization:

- **Macrocephaly re-tiered, and Beebop's audit request settles it.**
  `acquired_macrocephaly` (`CMS1303`, `CMS1304`) is a MedDRA term from DEVOTE's
  serious-adverse-event table — head circumference in an infant, **with no
  imaging reported in the source**. It was in `ventricular_enlargement`; it is now
  `related_clinical_sign`, alongside papilloedema, for the same reason: a
  surrogate sign of raised volume is not a measurement of it. Tiers are now
  **ventricular_enlargement 88** (was 90), **related_clinical_sign 17** (was 15),
  pressure_or_composition 31, procedure_or_mechanism 4, disease_background 7,
  therapeutic_reduction 1. `endpoint_domain` was not touched. **Whether infant
  macrocephaly should count as a direct hydrocephalus endpoint is German's call**,
  and §5's "90 rows in the endpoint's own tier" becomes 88 either way.
- Characterization columns corpus-wide, with analytical identity kept separate
  from sequence provenance per Beebop's modification. For this endpoint:
  **0/13 purity, 0/13 tested-batch identity**, now recorded as `NOT_REPORTED`
  rather than as an absent column.

**§5's descriptive-only recommendation stands and is strengthened.** The
announcement asks the narrative for *"a **discussion** of how the data **could
be** used to develop a predictive model"* — not a model — and scores *"the
demonstrated dataset as it is submitted."* The body above omitted that I still
owe that written discussion; it is now on the deliverable list.

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**

---
_Generated by [Claude Code](https://claude.ai/code)_
