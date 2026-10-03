# Rocksteady → Beebop: receipt for `SCIENTIFIC_RULES.md`, and the CNS delegation row

> **Re-confirmed against the revised `SCIENTIFIC_RULES.md` on 2026-10-03 — see
> [`ROCKSTEADY_RULES_RECEIPT_ADDENDUM_K_2026-10-03.md`](./ROCKSTEADY_RULES_RECEIPT_ADDENDUM_K_2026-10-03.md).**
> The revision adds **§K, German's twelve scientist sign-off gates**, and changes
> nothing else — I diffed both versions in full, so §§A–J below stand unamended.
> Against §K my corpus is 3 met, 2 partial, 4 failed, 2 not applicable, 1 absent.
> Also recorded there: five corrections to my own figures, the retirement of the
> 181-compound AUC claim, the controls deliverable gap, and the work freeze.

Receipt identifier: `2026-10-03/cns`. Satisfies delegation item 8 ("confirm each
session has read `SCIENTIFIC_RULES.md` and state which of its rules change that
session's current work").

| | |
|---|---|
| **Branch** | `claude/oligo-cns-toxicity-dataset-tijib6` — the *alternate* CNS lineage |
| **Commit at receipt** | `ce4d677e0b2e4e739092bdc342eab36ce349be56` (2026-10-03T00:02:27Z), clean tree, identical to `origin` |
| **Rules read** | `SCIENTIFIC_RULES.md` (10,603 B, blob `bebe077b83`) · `CRANK_DELEGATION_2026-10-03.md` (9,119 B, blob `3699537407`) · `German_requests_100326.md` |
| **Where I read them** | **Not on my branch.** `git cat-file -e HEAD:SCIENTIFIC_RULES.md` fails. I read them from `origin/claude/amazing-galileo-rwiv95`; the `origin/claude/crank-phase2-oversight` copies are **byte-identical** (same blob hashes), so there is no ambiguity about which text I am answering. |
| **Every figure recomputed** | Yes. Nothing below is quoted from the delegation. Each number was recomputed from the committed tree at `ce4d677` (or from the named other branch's committed tree) and the derivation is stated so you can re-run it. |
| **Scope honoured** | No label assigned or changed. No imputation. No negative manufactured. No conflict resolved. No model trained. Nothing re-grained. No ingestion, promotion or release. |
| **Scope of this receipt** | All CNS lanes on this branch — chronic, acute (931 acute-domain rows live inside the chronic-named file, §2 of the comparison) and hydrocephalus. |
| **Files written this round** | This receipt, [`CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md`](./CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md), [`../hydrocephalus/ROCKSTEADY_RULES_RECEIPT_2026-10-03.md`](../hydrocephalus/ROCKSTEADY_RULES_RECEIPT_2026-10-03.md), and one stale-count correction in `toxicity/chronic-neurotoxicity.schema.md` (§3). **No data file touched** — `qc_cns.py` re-run after the edit: 0 errors, 1 pre-existing warning. |

I have read the rules and I accept §A. Where §A and anything from Crank or
Beebop conflict, §A governs; where the derived rules and German's own Drive
documents conflict, German's documents govern and I will not act on my reading
of the derivative.

---

## 1. The rule that changes my work most is §E — and it convicts my own corpus

**§E, in full: "Do not map in-vitro fold-change bins to clinical severity
grades (e.g. CTCAE) *unless clinically validated*. Call it experimental response
severity."**

My corpus violates this, and the exemption does not rescue it: nothing in my
schema or methodology claims the mapping is clinically validated — the rubric is
a curator construction. I am reporting this against my own interest, because it
removes a claim I have been making for this lineage. Note that §E also names its
own remedy, which is a *relabelling* rather than a re-grading: call the in-vitro
scale experimental response severity and keep it off the clinical scale.

`neurotox_grade` is a single 0–3 column applied to **every one of the 2,538
rows**, across every stratum:

| stratum | n | grade 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|---:|
| `clinical` (human) | 545 | 230 | 165 | 130 | 20 |
| `animal_invivo` | 1,696 | 820 | 368 | 394 | 114 |
| **`in_vitro`** (181 rat + 116 human) | **297** | 196 | 57 | 42 | **2** |

The published rubric is at `toxicity/chronic-neurotoxicity.schema.md:98`. Read
it against those 297 rows:

- grade **3** = "neuronal degeneration/loss, spinal-cord or DRG degeneration,
  paralysis, hydrocephalus requiring intervention, moribundity/death, or
  dose-limiting or programme-halting neurotoxicity"
- grade **1** = "transient acute behavioural signs resolving within hours–days
  … no persisting functional deficit"

**Every branch of my rubric is written in organism-level terms. There is no
in-vitro definition anywhere in it.** Yet `CMS2054` is a BE(2)-M17 cell-culture
row whose entire result is "higher LDH than parent compound" and it carries
**grade 3** — a definition that cannot be observed in a dish. `CMS2051`–`CMS2056`
are the same shape at grade 2.

So this is worse than sharing one scale across strata. The 297 in-vitro grades
were assigned against definitions that do not apply to them, and a consumer
joining on `neurotox_grade` will read cytotoxicity and serious clinical
neurological injury as the same quantity.

A second §E breach rides along with it. §E requires: "Keep author result and
curator label separate. Binary calls are marked curator-derived unless the source
explicitly defines them. **Retain raw/continuous values, units, fold change,
significance and author interpretation.**" **203 of 2,538 graded rows (8.0%)
retain no `readout_value` at all** — `TBD`, because the source published the
number only as a figure — of which 69 are in-vitro and 14 are graded 3. On those
rows the curator's label is the *only* quantitative content, derived from reading
a plot, and there is no raw value beside it to check it against. My corpus also
has no column marking a grade as curator-derived; `neurotox_grade` is
curator-derived on every row but nothing in the schema says so to a consumer.

**What I am doing about it: nothing, and that is deliberate.** §A forbids me to
assign or reassign labels, and re-grading 297 rows is a scientific judgement
reserved to German under §J. I am flagging it and leaving it. It is the first
thing I would want German to rule on, because it changes what this lineage can
claim — see §4 of the [lineage comparison](./CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md).

---

## 2. §B — grain. You asked whether my endpoint is one-row-per-oligo. **It is not.**

| check | result |
|---|---|
| measurement rows | **2,538** |
| distinct `oligo_id` in them | **581** |
| rows per oligo | mean **4.37**, median **2**, max **214** |
| oligos with exactly one row | 149 (25.6% — a consequence of single-condition sources, not of the architecture) |
| two-table normalised design | present: `cns_measurements.csv` + `cns_oligos.csv` |
| **orphan `oligo_id` in measurements** | **0** |
| oligo records never measured | 11 |

So the observation table is at experiment-condition grain and the canonical
oligo table §B asks for exists and resolves completely. Nothing to re-grain, and
I have re-grained nothing.

**But the unit of observation is incomplete, and two of §B's axes are missing
outright.** §B specifies `oligo × chemistry × strand state × dose × time ×
donor/cell system × delivery condition × endpoint`. Measured against the
committed columns:

| §B axis | status in `cns_measurements.csv` |
|---|---|
| oligo | present — `oligo_id` |
| **chemistry** | **ABSENT** |
| **strand state** | **ABSENT** — and absent from the oligo table too, so it is nowhere in the dataset |
| dose | present — `dose_or_conc_value`, `dose_or_conc_unit` |
| time | present — `exposure_duration` |
| donor/cell system | present — `system_model`, `species` |
| delivery condition | present — `delivery_method` |
| endpoint | present — `readout_name` |

**§B's 8-link lineage chain does not close, at two links.** §B requires, for
every model-eligible row: model row → model-eligibility decision → scientific
interpretation → observed measurement → experimental/clinical condition →
biological system/population → exact oligo construct and position chemistry →
exact source location and source URL. Walking it against my columns:
`measurement_id` ✓ → **no explicit model-eligibility column** (`negative_eligible`
and `challenge_priority` are adjacent but neither is that decision) →
`effect_direction`/`effect_vs_control` ✓ → `readout_value`/`readout_unit` ✓ (203
`TBD`) → dose/duration/delivery ✓ → `system_model`/`species` ✓ → **position
chemistry absent** (§3) → `source_ref` + `source_table` ✓ but **no source-URL
column anywhere in any of the three corpus files**, though the 108 `source_ref`
values are all resolvable identifiers (51 DOI, 22 NCT, 1 PMID, 7 patent, 19
regulatory, 8 other). Two hard breaks, both schema matters, both gated.

And the condition key does not yet identify a row. Using
`(oligo_id, system_model, cns_region, delivery_method, dose_or_conc_value,
exposure_duration, readout_name)` there are **162 collisions over 2,376 distinct
keys**. Uniqueness is only reached by appending `readout_value` — i.e. the
measurement is currently identified by its own result. That is a smell, not a
design: either a condition axis is missing (replicate, arm, timepoint) or those
162 are true replicates needing an explicit index. Flagged, not fixed.

---

## 3. §C — the full 35-field audit: 9 met, 10 partial, 16 absent

§C names **35** minimum fields and opens with the requirement that chemistry be
encoded **by position**, with coarse flags such as `is_LNA` "permitted only as
secondary derived variables — never as the primary encoding, and never as a
causal feature". Its closing line governs how I have reported this: "Adding is
fine; **dropping one because your endpoint finds it inconvenient is not** — that
is a question for German." So nothing below is dismissed as inapplicable to CNS;
the absences are reported as absences.

| group | §C field | status | what exists on my branch |
|---|---|---|---|
| Identity and chemistry | `sequence_5to3` | **MET** | `oligos.sequence_5to3`, 466 of 592 real |
| | `strand_role` | **ABSENT** | no strand column in either table |
| | `duplex_partner_id` | **ABSENT** | no duplex partner column; siRNA duplexes unlinked |
| | `backbone_by_linkage` | PARTIAL | `backbone_chemistry`, molecule-level, 6 values |
| | `sugar_mod_by_position` | PARTIAL | `sugar_modifications`, molecule-level, 28 patterns; letter-case gives wing/gap on 268 of 466 |
| | `base_mod_by_position` | PARTIAL | folded into `sugar_modifications` (e.g. `5-methylcytosine`); no positional field |
| | `terminal_modifications` | **ABSENT** | no 5′/3′ terminal-modification column |
| | `gap_length_nt` | PARTIAL | derivable from `gapmer_design` (64 values, 105 `TBD`); not stored numerically |
| Characterization | `purity_pct` | **MET** | `NOT_REPORTED` ×585, `NOT_APPLICABLE` ×7, never blank |
| | `identity_method` | **MET** | `identity_confirmation` + `purity_method`, firewall-checked in `qc_cns.py` |
| | `endotoxin_level` | **ABSENT** | not collected |
| Exposure and system | `formulation` | **ABSENT** | not collected |
| | `delivery_agent` | PARTIAL | `delivery_method` is a route, not an agent |
| | `anticoagulant` | **ABSENT** | not collected |
| | `dose_value` | **MET** | `dose_or_conc_value` |
| | `dose_unit` | **MET** | `dose_or_conc_unit` |
| | `exposure_time_h` | PARTIAL | `exposure_duration` is free text with mixed units (`8wk`, `3h`, `500s_FLIPR_read`), not numeric hours |
| | `cell_system` | **MET** | `system_model` |
| | `cell_subset` | **ABSENT** | not collected |
| | `species` | **MET** | `species`, 5 values |
| | `donor_id` | **ABSENT** | not collected |
| | `donor_class` | **ABSENT** | not collected |
| | `sample_state` | **ABSENT** | not collected |
| Outcome and adjudication | `endpoint_name` | **MET** | `readout_name` + `readout_category` + `endpoint_domain` |
| | `raw_value` | PARTIAL | `readout_value`; 203 of 2,538 are `TBD` (figure-only sources) |
| | `raw_unit` | **MET** | `readout_unit` |
| | `author_interpretation` | PARTIAL | carried by `effect_vs_control` / `effect_direction`, not a dedicated field |
| | `curator_label` | PARTIAL | `neurotox_grade` exists but is **not separated** from the author result, and is misapplied to 297 in-vitro rows — §1 |
| | `immunomodulatory_direction` | **ABSENT** | not collected |
| | `receptor_pathway` | **ABSENT** | not collected |
| | `mechanism_evidence_type` | **ABSENT** | not collected |
| | `clinical_anchor` | PARTIAL | `evidence_class` / `trial_key` / `ascertainment` serve the purpose; no single anchor field |
| | `evidence_confidence` | **ABSENT** | not collected |
| Grouping | `sequence_family_group` | **ABSENT** | §4 |
| | `paper_group` | **ABSENT** | §4 |

**Totals: 9 MET, 10 PARTIAL, 16 ABSENT of 35.**

Dose coverage, since a sibling lane was found to be missing dose from its whole
human lane: that does **not** transfer here. Missing `dose_or_conc_value` is 81
of 545 clinical rows (14.9%), 34 of 1,696 animal in-vivo (2.0%) and 8 of 297
in-vitro (2.7%).

### The positional-chemistry gap, and one defect it exposes

§C's primary requirement is unmet: there is no per-position column at all (no
column matching `*position*` or `*pattern*` exists). What I store is exactly the
molecule-level shape §C permits only as secondary derived —
`backbone_chemistry` (6 values, e.g. `full_PS`), `sugar_modifications` (28, e.g.
`LNA;DNA_gap`), `gapmer_design` (64, e.g. `5-10-5_MOE`).

**Partial positional information does exist and is documented.**
`toxicity/chronic-neurotoxicity.schema.md:124` records the convention that
uppercase marks a modified wing (2′-MOE/cEt/LNA) and lowercase the DNA gap, and
that case is preserved as the source printed it rather than re-cased from the
design motif. Of 466 records with a real sequence, **268 are case-encoded, 197
flat upper, 1 flat lower** — so ~58% carry an implicit wing/gap boundary a
per-position builder could use.

**It disagrees with the authoritative field in 17 records, 16 from one source:**

| records | source | declared `gapmer_design` | case pattern says |
|---|---|---|---|
| CNS290–CNS305 (16) | `doi:10.1093/nar/gkag057` supplement | `5-10-5_MOE`, uniformly | `5-11-4` (12) or `5-12-3` (4) |
| CNS038 (1) | `US12241065B2` | `1-1-1-10-4_LNA_mixed_wing` | cannot be expressed as 3 blocks at all |

225 of the 242 checkable records agree, which is what shows the encoding is
intentional rather than noise. My schema already tells a consumer which wins —
"`gapmer_design` is authoritative for wing/gap structure; case is a
convenience" — and that is sufficient for today. It is **not** sufficient for
§C: when the Tier 0 crosswalk builds a real per-position field those 16 cannot
be transcribed from either source without choosing between them, because a
uniform `5-10-5_MOE` applied across a whole supplement and a per-sequence casing
taken verbatim from that supplement's table cannot both be right. I am not
choosing — that is a source conflict and §A forbids me to resolve it. CNS038 is
the sharper point: a five-block mixed-wing design **cannot be represented** in
`gapmer_design` at all, which is direct evidence for §C's position-level
requirement.

One drift I did fix, because it is description of my own documentation and
nothing else: `schema.md:126` said "268 of the 463 stored sequences are
case-encoded and 176 … flat upper case". 268 is right; the other two were stale
and did not even sum (268 + 176 = 444 ≠ 463). Corrected to the committed truth —
268 case-encoded, 197 flat upper, 1 flat lower, 466 total.

---

## 4. The two grouping columns that "must exist from the start" do not exist

| column | in measurements | in oligos |
|---|---|---|
| `sequence_family_group` | **absent** | **absent** |
| `paper_group` | **absent** | **absent** |
| `split_group` / `cv_fold` | absent | absent |

A correction to my own attribution, because it matters for who decides: the
phrase "these must exist from the start" is **§C's grouping clause (line 89),
cross-referencing §G** — `Grouping (see §G — these must exist from the start):
sequence_family_group, paper_group`. §G itself names no columns; it requires
grouped splits "by sequence family and near-neighbour, by paper and laboratory,
by matched pair, and by experimental series", prohibits random row splitting, and
cites the ~0.94-AUC-random against ~0.65-LOPO gap. So this is a §C schema
obligation enforcing a §G methodological rule, which puts it squarely behind the
Tier 0 crosswalk gate. I have not added the columns.

Worth recording while it is gated: my corpus is unusually exposed to exactly the
leakage §G describes. 2,538 rows carry only **282 distinct normalised sequences**
and 108 distinct `source_ref`, and one oligo reaches **214 rows**. A random
row-level split would place near-duplicate rows of a single sequence on both
sides with near-certainty. I already maintain a leakage key for a different
purpose (`cross_system_pairs_cns.py`, `canon()`, U→T normalised, documented there
as explicitly *not* an identity claim); it is the natural seed for
`sequence_family_group`, and `source_ref` for `paper_group`, whenever the
crosswalk opens.

§G adds a constraint my leakage key already respects and which I flag for
whoever builds the grouping: "Shared-sequence grouping must **not** merge
chemically distinct administered constructs. Reference identity is not
experimental-batch identity." This is why the 150 cross-lineage sequence matches
in the lineage comparison are reported as a leakage/identity key and not as
shared molecules.

---

## 5. §F and §I — already satisfied, one artefact still missing

**§F — `NOT_REPORTED` is the correct value.** **This claim is SUPERSEDED as of
Crank's corrected dispatch of 2026-10-03 and must not be read as compliance.**
The corrected instruction is: *first* harvest nonclinical lot purity from FDA
Pharmacology/Toxicology reviews, which publish per-lot values **unredacted** in
study headers; record withheld-with-evidence only where no lot value exists. Run
as I had it, `NOT_REPORTED` across the board would be a **false missingness
declaration on the one field NIH named mandatory**, for every oligo with an FDA
review — and **10 of mine have one** (`CNS012` nusinersen, `CNS013` tofersen,
`CNS273`–`CNS280`, across 10 FDA source_refs and 229 rows). Two of the documents
are already committed here
(`FDA_NDA209531_nusinersen_PharmacologyReview.pdf`,
`FDA_NDA215887_tofersen_IntegratedReview.pdf`). The sweep is one central job
owned by kidney per answer 8, so I am consuming it rather than duplicating it,
and I have changed no cell. What remains true and narrower: release
specifications and impurity profiles are withheld; measured nonclinical lot
purity is published. Mechanically, what follows is still accurate: The four
characterization columns are never blank: `sequence_provenance` is populated on
466 records (222 publication supplement / 189 patent sequence listing / 43 main
text / 9 WHO INN / 2 regulatory / 1 registry) with 126 `NOT_APPLICABLE`;
`purity_pct`, `purity_method` and `identity_confirmation` are `NOT_REPORTED` on
585 and `NOT_APPLICABLE` on 7. `qc_cns.py` enforces non-blankness and a firewall
preventing `identity_confirmation` from ever carrying a provenance category.

**A stale derived view silently undoes this, and it is the finding I would act
on first if ingestion were open.** My corpus has a third file,
`toxicity/notes/cns/corpus/oligotox_cns_merged.csv` — the denormalised
42-column join, 2,538 rows, built by `build_merged_cns.py`. It carries **none**
of the four characterization columns (`sequence_provenance`, `purity_pct`,
`purity_method`, `identity_confirmation`) and **none** of the seven
evidence-classification columns (`evidence_class`, `trial_key`,
`trial_key_basis`, `ascertainment`, `negative_eligible`, `event_cluster`,
`hydroceph_tier`). It predates both additions and was never regenerated.

So a consumer who reads the merged view — the obvious file to reach for, since
it is the one that needs no join — gets a dataset that fails §F outright and has
no evidence layer at all, while the normalised tables beside it pass. The two
disagree about what the dataset contains. §F's requirement is met in the
normalised tables and silently unmet in the file most likely to be used.

Regenerating it is a build step that writes a data file, which I read as
ingestion rather than description, so I have not run it. The generator exists
and the inputs are committed; it is a one-command fix the moment that gate
opens.

**The Characterization Gap Register §F requires does not exist as an artefact on
my branch.** The underlying facts are all computed and published prose, but
there is no register file. I can produce it from committed data without any
scientific judgement — it is a count of absences. Say the word and it is a
description task, not an ingestion one.

**§I — source corrections.** Structurally inapplicable here, verified rather
than assumed:

- **0** bare author-year source keys. All 108 distinct `source_ref` resolve: 51
  DOI, 22 NCT, 19 regulatory, 7 patent, 1 PMID, 8 other.
- None of the named misattributions (Peacock, Hornung, Herzner, Riera-Tur,
  Fucini, Lenert) appears as a source key, in any lane.
- Two surname matches exist in archived source *documents* and are incidental: a
  reference list inside `toxicity/sources/cns/PMC12925542.jats.xml`, and
  "Goodchild, J., (ed), Methods in Molecular Biology" in the prior-art citation
  list of `toxicity/sources/cns/fpo/US12241065.html:696` — Goodchild as a book
  editor, not the paper at issue.

So §I changes nothing for me. I note it explicitly because "no hits" and "did
not look" are not the same claim.

---

## 6. §D and §H — no change required

**§D — human and animal never pooled.** Already honoured. The lanes are split by
`study_type`/`species` throughout and `evidence_class` (12 values) carries the
distinction on every row. My cross-system work (`cross_system_pairs_cns.py`)
reports pairs; it never merges them into a row. GOLD/SILVER/BRONZE tiers do not
appear in my corpus at all, so there is no risk of my treating them as labels.

**§H — release states.** No release has been published from this branch, there
is no `release_id` anywhere in my tree (`grep -rI release_id` returns nothing),
and release authority is Oscar's under §J. Nothing to correct.

---

## 7. The delegation's figures, recomputed. Three do not hold as stated.

| # | delegation states | I recompute | verdict |
|---|---|---|---|
| 1 | CNS lineages share **144** sequences | **144** | **exact — but mis-scoped.** 144 is my branch ∩ k394sz's **acute partition alone**. The full cross-lineage intersection is **150** (144 acute + 6 added by chronic; 1 sequence is in both k394sz partitions). Derivation in the [comparison](./CNS_LINEAGE_COMPARISON_FOR_GERMAN_2026-10-03.md) §2. |
| 2 | `_shared/cns/README.md` **181**-compound claim needs fixing | **181 exactly** | **the count is right; the claim attached to it is not.** 181 oligos do carry both a rat in-vitro calcium-oscillation score and a mouse in-vivo acute tolerability score. But the README calls this "exactly the in-vitro-to-in-vivo extrapolation the challenge asks for", and it is **rat → mouse**: no human on either side. The same README concedes 26 lines later that "no compound in this release carries both a human and an animal row". Lines 35–37 contradict line 131 of one file. |
| 3 | same README's grade-distribution claim | **unreproducible** | README says "Grades 0/1/2/3 = 56/87/40/57" (sum 240). From k394sz's committed tree: acute measurement-level **74/81/39/51** (245); acute oligo-level by max grade **42/78/26/51** (197); all three endpoints measurement-level **1,614/673/130/175** (2,592). The published figure matches **none** of them. |
| 4 | hydrocephalus has **zero human in-vitro** | **0** | **confirmed, and it is true of all three lineages** — mine (0 of 131 human rows), t172zv (0 of 1,332), k394sz (0 of 12). See the [hydrocephalus receipt](../hydrocephalus/ROCKSTEADY_RULES_RECEIPT_2026-10-03.md). |
| 5 | `PHASE2_COMPLIANCE` says **53** where `n_compounds_real` = **51** | both present, and there is a **third** number | Confirmed at `toxicity/hydrocephalus/PHASE2_COMPLIANCE.md` on t172zv: line 43 renders `n_compounds_real` = 51, line 106 renders `n_oligos` = 53, in one document, unreconciled. The count actually carrying a measurement is **49** (53 stored, 4 never measured) and is published nowhere. |
| 6 | `release_id` is `-dirty` | **`"hydrocephalus-73be6c0-dirty"`** | confirmed verbatim at `toxicity/hydrocephalus/qc/stats.json:356` on t172zv. The identifier does not bind to a reproducible commit, which is release-blocking under §H. |
| 7 | 111-row `measurements.csv` on **five of six** branches in **two divergent versions** | **7 branches, 2 hashes** | version count exact. Branch count higher: `5bea31d258` on `ap70gf`, `0nzivp`, `t172zv`, `4um5mi`, `k394sz` and `2h7t50` (the last deliberately quarantined at `kidney-toxicity/reconcile/data-111row-lineage/`); `1fbe366eaa` **only on my branch, at two paths**. Note `food-tracking-image-app-0nzivp` — an unrelated app branch — carries kidney data. There are **10** remote branches, not six, and 8 physical copies. One reading does rescue the "five": discount `0nzivp` as unrelated and `2h7t50`'s copy as a *deliberately archived* lineage (it sits beside `METHODOLOGY-111row-lineage.md` and `schema-111row-lineage.md` documenting it as a snapshot), and exactly **five** oligo-toxicity branches ship it at a live data path. The denominator of six is not reconstructible under any reading I could test. |
| 8 | canonical 246-row file exists **only** on `claude/amazing-galileo-rwiv95` | on **two** branches | **refuted as stated.** Blob `6f7bb715f9` (246 rows) is at `toxicity/kidney/data/measurements.csv` on both `claude/amazing-galileo-rwiv95` **and** `claude/crank-phase2-oversight`, byte-identical. |

Items 1, 7 and 8 are corrections to the delegation; items 2 and 3 redirect what
needs fixing; 4, 5 and 6 stand as written. I would not have found 1, 2 or 8 by
taking the figures on trust, so the instruction to verify was the right one.

---

## 8. The divergent 111-row file is mine, and one of its three deltas is release-relevant

I own the divergence, so I will state it plainly rather than report it as a
cross-branch mystery. Both blobs are 111 rows and 23 identical columns. Mine
(`1fbe366eaa`) differs from the common copy (`5bea31d258`) in exactly three ways:

1. **`source_ref` — 62 cells canonicalised**, e.g.
   `NEJM2018_NEJMoa1716793` → `doi:10.1056/NEJMoa1716793`.
2. **`notes` — 62 cells extended** with `source_ref_as_cited=…`, preserving the
   original string, so nothing was destroyed.
3. **`redistribution` — 13 cells changed `summary_stat` → `cc_by`.**
4. Saved CRLF (112 CRs against 0).

Deltas 1 and 2 are strictly better and are what §I asks for — this copy is the
only one of the seven with no bare author-year keys. **Delta 3 is the one that
matters and it needs an owner.** `cc_by` is not cosmetic: my own schema records
it as permitting "unrestricted reproduction of the raw values with attribution",
materially stronger than `summary_stat`. If my reclassification is correct the
common copy under-claims rights on 13 rows; if it is wrong, 13 rows are marked
publishable that are not. Either way it must be settled before any kidney
release.

**This is kidney data. Oscar told me the nephrotoxicity work was a mistake and
that this branch is CNS only, so I am not the one to settle it.** I therefore
declare, on the record:

- `data/measurements.csv`, `data/oligos.csv`,
  `toxicity/kidney-nephrotoxicity.{measurements,oligos,shared-molecules}.csv`,
  and the root `PADP.md`, `METHODOLOGY.md`, `schema.md` on this branch are
  **non-authoritative leftovers**. Nothing downstream should read them.
- The 13-row rights delta is handed to whoever owns kidney, with the evidence
  above. It is not withdrawn silently.

**One live hazard, and it is in my CNS pipeline.** Four scripts on this branch
resolve the stale table by constructed path: `corrections_kidney.py:20`,
`fetch_kidney_licences.py:25`, `qc_kidney.py:32-33`, and —
the one that matters — **`split_by_endpoint.py:50-51`**, which is part of the
live CNS pipeline, not the kidney leftovers. Deleting the stale files without
touching that script would break CNS splitting. Removal is therefore a
coordinated change, not a `git rm`, and I have made neither.

---

## 9. §E's clean-negative gate, measured — and a duplicate it exposes

**My `negative_eligible` column is not a test of §E's standard, and the gap is
two orders of magnitude.** §E requires *all* of: exact sequence, human exposure,
adequate dose and duration, explicit monitoring, an explicit outcome, and a
traceable denominator. Narrowing my corpus by the gates I can actually measure:

| filter | rows |
|---|---:|
| `negative_eligible = TRUE` | **1,186** |
| …of which human/clinical (§E requires human exposure) | 171 |
| …of which `ascertainment = explicit_zero_with_denominator` (§E's traceable denominator) | **33** |
| …of which the oligo carries an exact sequence | **27** |

So **at most 27** rows could be §E clean clinical negatives, against 1,186
currently flagged `negative_eligible` — and 27 is an upper bound, because I have
not tested §E's remaining gates (adequate dose and duration, explicit
monitoring). The 1,186 figure includes 819 animal in-vivo and 196 in-vitro rows,
which cannot be clinical negatives by construction. All 1,186 are grade 0.

Nothing downstream should treat `negative_eligible = TRUE` as §E's clean
clinical negative. Re-deriving the predicate is a labelling act and is German's
under §J; I have changed nothing.

**And the gate exposes a double-count.** 7 trials in my corpus are ingested
under *both* ClinicalTrials.gov source conventions (`CNSSRC_CTG_*` and `CT_*`):
`NCT02193074`, `NCT02292537`, `NCT02623699`, `NCT03070119`, `NCT03342053`,
`NCT03761849`, `NCT04089566`. On two of them the same adverse-event table is
represented twice at different fidelity — once as per-arm counts, once as a
percentage:

| trial | compound | `CNSSRC_CTG_*` rows (`n_of_N`) | `CT_*` rows (`pct_incidence`) |
|---|---|---|---|
| `NCT03761849` | CNS014 | `0_of_264` (**CMS1280, TRUE**), `0_of_36` (CMS1281, TRUE), `2_of_263` (CMS1282) | `0.0` (**CMS1443, TRUE**), `0.8` (CMS1442) |
| `NCT03342053` | CNS014 | `0_of_23` (CMS1274, TRUE), `1_of_23` (CMS1275) | `4.3` (CMS1416) |

The arithmetic confirms they are the same facts: 2/263 = 0.76% ≈ 0.8, 1/23 =
4.3%, and the zeros map to 0.0. **CMS1280 and CMS1443 are the same zero from the
same trial flagged `negative_eligible = TRUE` twice**, so the eligible-negative
pool is inflated by at least one double-count, and the percentage-form rows
carry no denominator at all — exactly what §E's traceable-denominator gate is
for.

Which representation should survive is a source-conflict adjudication, which §A
forbids me to resolve. Flagged with the row IDs so it can be settled in one
pass. (This is distinct from the cross-lane duplicate `CMS1450`/`CMS1300` I
resolved in an earlier round; that was within one ingestion convention.)

**German's decision 6 and DEVOTE.** `NCT04089566` is one of the 7
double-ingested trials and carries 20 rows in my corpus. I hold that evidence
with loci and will supply it for the decision-6 assessment on request, **with no
verdict from me** about whether it clears the gate. Noting also that decision 6
names "seven gates" and lists six; settling the count matters, because it
decides what DEVOTE is being measured against.

**German's decision 2 — SUPERSEDED 2026-10-03.** Crank's corrected dispatch
retires the project-wide withheld-with-evidence instruction, so the third
enumerated value I argued for below is **not** the fix: for any oligo with an FDA
Pharm/Tox review the value is published, not withheld, and recording it as
withheld would be a false missingness declaration. The narrower surviving claim
is that release specifications and impurity profiles are withheld while measured
nonclinical lot purity is not. I leave the original paragraph below rather than
delete it, because the reasoning is what was wrong and hiding it would obscure
that. **Original, now superseded:** "Withheld-with-evidence" — a regulator demonstrably holding a purity number
(FDA `(b)(4)`, 56 redactions in inotersen, 84 pages in tofersen; EMA CCI; PMDA
asterisks) — is **not** the same state as `NOT_REPORTED`, which means nobody
measured or published it. My corpus currently flattens both into `NOT_REPORTED`
on 585 records, which loses the very distinction that makes decision 2
answerable. If German rules that blocker (iii) is satisfied by populating
`purity_method` + `identity_confirmation` while recording purity as
withheld-with-evidence, that needs a third enumerated value — a schema change
gated on Tier 0. Flagged, not pre-built.

---

## 10. What I did not do

No label assigned or changed, including the 297 in-vitro grades I just reported
as mis-scaled. No imputation. No negative manufactured. No conflict resolved
between sources — the `CMS1280`/`CMS1443` double-counted negative and the
2-trial cross-ingestion overlap in §9 are flagged with row IDs and left for
adjudication. No model trained. No column added — not
`sequence_family_group`, not `paper_group`, not a per-position chemistry field,
not a third purity state. Nothing re-grained. No ingestion, no promotion, no
release. No file changed on any branch but my own; the `_shared/cns/README.md`,
`PHASE2_COMPLIANCE.md` and `-dirty` `release_id` findings are report-only
because those files live on `k394sz` and `t172zv`, which I do not own.

The one edit I made to data-adjacent content is the stale sequence-case count in
my own `schema.md` (§3 above) — description of my own documentation, correcting
numbers that did not sum.

---
_Generated by [Claude Code](https://claude.ai/code)_
