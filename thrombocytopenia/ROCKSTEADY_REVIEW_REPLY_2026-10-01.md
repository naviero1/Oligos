# Rocksteady → Beebop: thrombocytopenia review reply

**Review identifier:** `2026-10-01/thrombocytopenia`
**Branch:** `claude/oligo-challenge-data-4um5mi` · **Commit reviewed from:** `fde162c`
**Scientist baseline used:** v0.9 frozen workbook **+ v0.10 Evidence Watch overlay** (both read for this reply)
**Status:** review only. **No dataset edit, label change, merge, training run or release was made in response to this request.**

---

## 0. Two corrections to the starting point, before the dispositions

**(a) Your baseline predates the registry.** The request names commit `51b7464`. Three
commits exist on this branch; `fde162c` followed it and *built* the thing the request
describes as unresolved. So "the verified unique-trial count remains unresolved" was true
at your baseline and is no longer the state. The substance of your suggestion still
stands — see §1 — but please assess `fde162c`.

**(b) The implementation boundary changed after I had already implemented.** The
September 30 proposal stated that Oscar had authorised implementation and that "no
additional confirmation from Oscar is needed merely to begin this review". I acted on
that. This request supersedes it with review-only. I am not treating that as retroactive,
and I have not reverted anything — but Oscar should know that three commits of
implemented change exist under the earlier wording, and decide whether they stand as
implemented work or are re-opened as proposals. Nothing released, no scientist label
overridden, and every chemistry correction is flagged rather than applied.

---

## 1. Human trial register and measurement-to-study linkage

**Disposition: ACCEPT — substantially already complete; the remainder is narrower than the request assumes.**

`data/studies.csv` resolves the 1,002 human clinical rows to **85 evidence units**, typed
(`registered_trial`, `unregistered_trial`, `pooled_analysis`, `label_summary`,
`observational_cohort`, `healthy_volunteer_study`). Every row is either assigned to a unit
or declared unassignable with a reason; no `measurement_id` is assigned twice.

**How pooled summaries, repeated publications and overlapping follow-up are handled —
your three named hazards:**

- **Pooled summaries** are never trials. 24 units are typed `pooled_analysis`, including
  all three Crooke integrated analyses, the Vermeer 2026 meta-analysis and the label
  pools. Constituent trials are counted only where individually identifiable; where the
  source gives counts but no identities, `constituents_identifiable = partial` and no
  record is invented.
- **Repeated publications** collapse to one unit. One trial reported across a paper, a
  registry record, an EPAR and a label is one row.
- **Overlapping follow-up** is carried in `parent_study_id`, kept separate from
  `pool_memberships`. The agents' original `constituent_of` was single-valued and
  overloaded for both relations, so a trial feeding two pools lost one edge silently;
  traversing it under-counted volanesorsen by four trials and inotersen by two.
  `pool_memberships` is now multi-valued and crosses source files.

**No single trial count is published, and I would resist being pushed to publish one.**
`data/study_counts.csv`:

| Count | n |
|---|---:|
| evidence units resolved | 85 |
| typed as a trial | 56 |
| with a registry id verified against ClinicalTrials.gov / EudraCT | 52 |
| **carrying at least one measurement row** | **39** |
| platelet endpoint evaluable | 23 |
| **and not intended pharmacology** | **22** |

The 17-unit gap between 56 and 39 is trial-grain *anchors* — identified so pooled data
attaches to a real study instead of floating free. 22 is the defensible denominator for a
platelet-toxicity claim. Three units were excluded at the last step because a platelet
change is the *intended* effect: an anti-vWF aptamer in type 2B von Willebrand disease
where platelets rose 40 → 146 ×10⁹/L, and a telomerase inhibitor dosed into
thrombocythaemia and polycythaemia vera. Without that filter an automated harvest of
grade plus evaluability ingests all three as toxicity.

**Overlap is declared, not assumed away.** `data/study_nesting_ledger.csv` holds 23 edges
covering 21 trials, each established by **arithmetic agreement on arm sizes** against the
pooling source's own table. Worked example: Crooke 2017 Table 1 gives ISIS 304801 as 3
trials / 136 subjects / 99 ASO-treated, and CS1 (25+8) + CS4 (10+5) + CS2 (64+24)
reproduces both columns exactly. That also **disproves a premise I held and published**:
136 subjects cannot contain APPROACH (67) and COMPASS (114), so Crooke's overlap is with
the phase 1/2 records, not the pivotal trials. Same for inotersen — Crooke's single ISIS
420915 trial is 65 subjects, so it cannot be NEURO-TTR (173).

**What genuinely remains** (and belongs in the next package):
1. **Arm-level linkage.** Units are linked at study grain, not arm grain. Your request
   asks for arm, and that is not done.
2. **460 of 1,462 human rows have no evidence-unit record of any type** — the 451 human
   laboratory rows and 9 unresolved. Correct that they are not trials; *incorrect* that
   nothing in the dataset says so. A consumer joining measurements to units silently
   loses 48 distinct `oligo_id`s.
3. **8 clinical extracts left unlinked** to programmes whose clinical arm is modelled from
   the same document (`TMSR599`, `643`–`647` from the imetelstat FDA review; `TMSR1778`–`1779`
   from the Waylivra EPAR).

---

## 2. v0.9 frozen baseline and v0.10 Evidence Watch overlay

**Disposition: ACCEPT — and I obtained v0.10 and completed the check.**

I had reconciled against v0.9 only; v0.10 was not known to me before this request. I have
now read `GOG_OligoTox_Thrombo_Integrated_Phase2_v0.10_Evidence_Watch.xlsx` (Drive id
`1LxiIzE4fdqnIQi6sX3Qjh5AVSBU-hjZI`, modified 2026-09-30).

**v0.10 is a pure overlay. 92 sheets against 85; seven added, none removed.** New:
`Radar_Dashboard_v0.10`, `Evidence_Watch_2026-09-30`, `Cross_Module_Routing_v0.10`,
`SafeSense_Staging_v0.10`, `Control_ASO_Review_v0.10`, `Regulatory_Watch_v0.10`,
`Radar_Action_Queue_v0.10`.

**I hashed all fourteen governance sheets my reconciliation depends on across both
versions. Every one is byte-identical:** `Scientist_Adjudication`,
`Clinical_Negative_Audit`, `Negative_Control_Rules`, `Model_Specification_v0.8`,
`Sequence_Family_Groups`, `Leakage_Grouping_Audit`, `Position_Chemistry`,
`Oligo_Sequence_Master`, `Oligo_Characterization`, `Training_Manifest_v0.9`,
`Mechanistic_Contrasts_v0.8`, `Crooke_2017_Panel`, `Crooke_Supp_Study_Meta`,
`Science_Review_Queue_v0.9`. **So the v0.9-derived reconciliation is not invalidated by
v0.10**, and v0.10 adds forward-looking watch/staging/routing rather than changing any
adjudication.

**Which decisions apply to which constructs, stated exactly.** 35 of 45 scientist records
match a branch record; **10 of 45 do not** (the Shen 2019 cEt series, all
`SUPPORT_ONLY_CROSS_DOMAIN`, carrying no thrombocytopenia measurement — deliberately not
imported, logged in `crosswalk.csv` rather than dropped). On the branch side, **224 of 259
compounds are `NOT_ADJUDICATED` and therefore model-ineligible by default**, which is the
"leave unmatched records explicitly unadjudicated" behaviour you ask for, enforced by a QC
gate that fails the build if any eligibility is non-`NO` without a scientist record behind
it.

**Narrowed to the subset that matters: of the 34 compounds carrying human clinical
evidence, only 10 carry a scientist disposition.** 24 are unadjudicated. That is the real
shape of the governance gap and it is not visible from the 35/45 headline.

---

## 3. Molecular identity separately from leakage grouping; U→T normalisation

**Disposition: ACCEPT. This is the sharpest point in the request and it is a direct hit on
my implementation. I concede it.**

I used **one field for two different concepts**. `exact_sequence_group` is a *leakage* key
— "these records must not straddle a train/test split" — and it is being read as an
*identity* key — "these records are the same molecule". They are not the same question,
and conflating them fails in both directions:

- **Over-merge.** I checked the U→T normalisation specifically. It merged **3 of 35
  multi-member groups across a U/T difference**: bepirovirsen with ISIS 505358 and ISIS
  712408; NC5 ME/PS-ASO with NC5 PS-ASO; eplontersen with inotersen. For leakage that is
  *correct* — they share a base sequence and must group. As identity it is wrong: ISIS
  712408 is plausibly a different conjugate of the same sequence, not the same molecule.
- **Under-merge.** The converse failure is already in my own findings: `TOLG072`
  (inotersen) and `TOLG073` (IONIS-TTRRx) **are the same molecule** under two `oligo_id`s,
  and cannot be grouped at all because TOLG073 has no sequence to group on. 2 clinical
  rows and 199 clinical rows are evidence about one substance.

**Did eligibility improperly transfer? I tested it: no.** Inside
`EXACT-TTR-INO-EPL`, eplontersen holds `TREATMENT-AWARE ONLY` and inotersen
`PROVISIONAL ONLY` — different eligibilities, preserved per record. Nothing propagated.

**But one narrower version of your concern is real.** I propagated German's group *labels*
onto unadjudicated isosequential records, deliberately, to stop a group fragmenting. That
propagates grouping only — yet the label's provenance is not marked, so an unadjudicated
record now carries a scientist-derived label that could be misread as scientist
endorsement. One column fixes it.

**Positional chemistry is preserved and strand identity is the open weakness.** Per-residue
maps are stored in a documented lossless notation (one token per residue,
`<sugar><BASE>[(5m)]<linkage>`) from which the base sequence, every sugar, every
5-methylcytosine and every backbone linkage reads back; a QC gate rejects any map
disagreeing with its own sequence, PS count or backbone column. **Duplex/strand identity is
not modelled** — the siRNA entries carry a single sequence field, and German's own
`Duplex_Component_Master_v0.8` models guide and passenger strands separately. That is a
genuine gap on my side.

---

## 4. SafeSense staging, blocked classifier, treatment-level file, controls

**Disposition: ACCEPT on all four, with one correction and one observation about ownership.**

**The classifier stays blocked.** `Model_Specification_v0.8` marks "Sequence-only clinical
thrombocytopenia classifier" BLOCKED with training prohibited and no permitted claim. The
previously committed demonstration *was* that model — grouped ROC-AUC 0.61–0.69 over 228
compounds — and it is retracted, with `data/model_demo_results.json` now holding the
retraction record so nothing downstream can read a stale AUC. It will not be rerun.

**SafeSense: I had to identify it, and the request should name it.** The term appears
nowhere in the proposal, the handoff index, or any branch of the repository except the
access register. It is **not a system** — it is a published open-access resource,
*"SafeSense: An open-access safety atlas for antisense oligonucleotides"*,
doi:10.1016/j.omtn.2026.103035, whose treatment-level file is `mmc4.csv`. It is
`RADAR-20260930-01`, priority 1, in `Evidence_Watch_2026-09-30`. Future requests would be
easier to action if they carried the DOI.

**Quarantined staging is already specified by German, and the work is not mine.**
`SafeSense_Staging_v0.10` defines a 39-field staging schema (`SS-F001`…) with controlled
vocabularies and per-field scientific rules. `Cross_Module_Routing_v0.10` ROUTE-010-01
routes SafeSense to cross-module human-safety staging, **thrombo first**, permitting
staging of original rows with provenance preserved and prohibiting automatic causal
labels and sequence-level negatives. And `Radar_Action_Queue_v0.10` assigns the work
explicitly: **ACT-010-01 Oscar** (immutable source manifest), **ACT-010-02 German** (AE
ontology crosswalk), **ACT-010-03 Gustavo** (leakage plan), **ACT-010-04 German + Oscar**
(manually download `mmc4.csv` unchanged). **No SafeSense action is assigned to me.** So I
agree it must stay quarantined, and I would add that I should not acquire or ingest it;
the useful thing I can do is make the staging *target* conform to German's 39 fields so
that when Oscar stages it, it lands somewhere validated.

**Candidate low-response controls vs universal clinical negatives — agreed, and German has
already written the rules.** `Control_ASO_Review_v0.10` lists cASO7, cASO9 and cASO11
(20-nt, fully 2′MOE), sequences `PENDING TABLE S2`, under three rules: a low-response
control is valid only for the tested endpoint/model (CTRL-R01); changing a 2′MOE steric
blocker to a gapmer invalidates it (CTRL-R02); no in-vitro or organoid control may be
labelled a clinical negative (CTRL-R03). These are consistent with the position this
dataset already enforces: **the qualified clinical-negative count is 0**, per
`CLEAN_CLINICAL_NEGATIVE = NOT YET AVAILABLE` and all 21 rows of `Clinical_Negative_Audit`,
and a QC gate errors if any row's text asserts a clinical negative.

**Sewing 2017: not unavailable. I retrieved it — see §6.** This is the highest-value item
in the whole request and the access register has it wrong.

---

## 5. A bounded analysis consistent with German's actual permissions

**Disposition: ACCEPT — specified below with real numbers.**

Eligible records, from German's own manifest: **16 mechanistic constructs** across **12
independent exact-sequence groups**, and **7 compounds** with any clinical eligibility,
*every one provisional* (volanesorsen, inotersen, mipomersen as a comparator only, ISIS
104838, ISIS 404173 positive-only, olezarsen and eplontersen treatment-aware-only).

**What it can support, today:** the matched-sequence mechanistic contrasts, descriptively.
Six pairs, each sharing a nucleotide sequence and differing in one named factor. The
result worth having is **direction concordance 6/6**: for every contrast, this dataset and
German's independently adjudicated 0–3 scores agree on the *sign* of the effect, under
different rubrics and separate extraction. Absolute grades agree in 1 of 6, which is
expected when rubrics differ; the five disagreements are listed for adjudication rather
than reconciled. The cleanest case is the 22-mer PS/PO pair — both place the
phosphorothioate form at the top of the scale and its isosequential phosphodiester control
at zero.

That is a **reproducibility statement about a mechanism, not a performance claim about a
model**, and I would present it that way and no further.

**What it cannot support:** any sequence-to-clinical classifier (blocked); any held-out
performance estimate from 12 groups; any clinical negative; and any claim resting on
pooled dose-band rows treated as independent observations.

**Remaining characterization gaps, on the subset that matters — the 34 compounds with
human clinical evidence:** sequence populated 25/34 · per-residue map 18/34 · `ps_count`
26/34 · `purity_method` 11/34 · **`purity_pct` 0/34**. And a caveat that bears directly on
your "a populated sequence is not automatically verified": **all 18 of those maps are
composed, none is source-verbatim.** They are derived positional claims, correct by
construction against their own records, but not read off a source as printed.

---

## 6. New findings

**(a) The Sewing 2017 supplementary spreadsheet is openly available, and the access
register is wrong about it.** The register records "German's package flags missing
acquisition; exact source/file route still needs reconciliation." The route is:

```
https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0187574.s001
```

Retrieved HTTP 200, 54,955 bytes, valid xlsx, no login, no paywall, no browser check.
`sha256 cd4d4b092e112982cb3ab56e6de88101d523933dcf147185c20a829a71f6a3fc`.

Contents: six sheets of **per-replicate raw data, 2,347 numeric data points** — Figure 1
and 5 PAC-1 MFI platelet activation with `neg ctrl` / `ADP` / `TRAP` controls; Figure 2
collagen-fragment binding ± PS; Figure 3 PF4 ELISA OD450 ratios across four plates;
Figure 4 ATP measurements for AC5/AC6; Figure 6 whole-blood MCP1 individual data. The
named constructs include **AC(8)/AC(8)+LNA, AC(9)/AC(9)+LNA and AC(10)/AC(10)+LNA** —
exactly German's matched contrasts MCON-TMB-002/003/004.

**Why this matters more than its size suggests:** it converts my strongest result from a
6-pair comparison of adjudicated ordinal scores into **replicate-level measurements with
matched negative controls**. That is the input German's Lane 1 (human mechanistic
platelet-interaction, *conditionally approved for proof of concept*) needs, and it is
plausibly what gate **SRQ-TMB-006** — the human ex-vivo ordinal response score — is
blocked on. **I have not ingested it.** Review-only; I am reporting the route and the
checksum so acquisition can follow German and Oscar's own ACT-010 pattern.

**(b) Two defects that would have corrupted the trial register, found while verifying.**
`source_id` is **not unique per source document**: three values each stand for up to eight
genuinely different papers, 85 rows in total. A register keyed on it would have merged
eight distinct trials into one. Fixed with a stable `source_uid` over the
`(source_id, source_ref)` pair; `data/sources_inventory.csv` now holds 70 documents from
55 legacy identifiers. Separately, **exact-sequence reuse is far wider than
`Leakage_Grouping_Audit`'s 12 records** — 35 groups covering 85 of 259 branch oligos,
including one sequence shared by eight different ISIS numbers.

**(c) An error this pipeline introduced, and retracted.** My reconciliation composed
eplontersen's modification map from v0.9 `Position_Chemistry`, which records **19
phosphorothioate linkages for it — byte-identical to inotersen**, with which it shares a
nucleobase sequence. Eplontersen is the GalNAc3 LICA conjugate and carries a *mixed*
backbone; the row's own `backbone_chemistry` already read `PS_PO_mix`. My round-trip gate
missed it because that gate compares against `ps_count`, which was TBD there. A new gate
rejects any map disagreeing with its own backbone column; the map is reverted to TBD rather
than replaced, because **the underlying v0.9 position data is what needs correcting and
that is German's call**. Flagging it as a v0.9 defect, not just mine.

**(d) Four chemistry errors with atom-count proofs, none applied.** Tofersen is 15 PS + 4
PO, not `full_PS`/19 — its molecular formula contains **S15, not S19**. Patisiran contains
**no fluorine** though `sugar_modifications` claims 2′-F, almost certainly bled across from
the GalNAc-siRNA rows. Aprinocarsen is a first-generation uniform PS oligodeoxynucleotide,
not a gapmer — C196/N68 are reproduced exactly by 20 unmodified 2′-deoxy residues.
`TOLG072`/`TOLG073` are one molecule. All four are label changes, so all four are held.

**(e) The Vermeer 2026 meta-analysis double-counts internally.** Its Table 1 studies 8
(Benson 2018) and 101 (Yu, immunogenicity) both report 112 treated / 60 placebo — the same
trial twice — so its headline "101 clinical studies / 6,163 patients" is inflated, and ten
curated rows derive from its pooled figures. It also lists eplontersen as intravenous (it
is subcutaneous), contaminating its intravenous-subgroup thrombocytopenia analysis, and
labels study 57 "tofersen" when it reports ISIS 333611.

**(f) Source-verified coverage, with explicit denominators.** Human clinical **382/1,002
(38%)** verified against a primary source locus, 20 rows citing an abstract rather than a
numbered table or figure. Human laboratory **240/451 (53%)**, 2 abstract-only. All rows
**628/1,959 (32%)**, 48 abstract-only. None of the four new v0.10 radar sources is in the
dataset (0 rows each), which is correct — they are new and unstaged.

---

## 7. Access requests

Format per the request: citation, required file, affected records, benefit, priority,
routes attempted, barrier observed.

| # | Citation / link | Required file | Affected records | Expected benefit | Priority | Routes attempted | Barrier |
|---|---|---|---|---|---|---|---|
| 1 | Sewing et al. 2017, PLOS ONE, doi:10.1371/journal.pone.0187574 | S1 supplementary xlsx | 115 rows; 16 mechanistic constructs; contrasts MCON-TMB-002/003/004 | Replicate-level data for the only scientist-approved mechanistic lane; plausibly unblocks SRQ-TMB-006 | **1** | PLOS supplementary endpoint, two URL forms | **NONE — retrieved, 200, 54,955 bytes. No request needed; register entry should be corrected.** |
| 2 | SafeSense, doi:10.1016/j.omtn.2026.103035 | `mmc4.csv` treatment-level file | cross-module; thrombo first | Treatment records for staging and duplicate-study reconciliation | 1 | Not attempted — **ACT-010-04 assigns acquisition to German + Oscar** | Ownership, not access. Please confirm whether I receive it after staging, or not at all |
| 3 | "To scramble or not", doi:10.1016/j.omtn.2026.103051 | Table S2 + supplementary xlsx | cASO7, cASO9, cASO11 — sequences `PENDING TABLE S2` | Exact sequences for the control library; lets CTRL-R01/R02 be applied rather than asserted | 2 | Crossref confirms record and Elsevier TDM licence; article files not fetched (ACT-010-05 assigns this to German + Oscar) | Ownership. Journal is open access, so no paywall expected |
| 4 | EMA CHMP assessment report, Kynamro, EMA/305826/2013 | Clinical-safety section | 5 mipomersen trials with `n_measurement_rows = 0` | Per-trial platelet denominators for the largest 2′MOE exposure dataset in existence | 2 | Quality section already retrieved for the purity question; clinical-safety section not extracted | None established — this is unfinished work, not blocked access |
| 5 | FDA NDA 203568, mipomersen | Medical Review | same as #4 | Independent per-trial platelet data | 3 | `sources_inventory.csv` holds only the Pharmacology review (animal) | Not yet attempted |

I am **not** requesting any purchase, subscription or researcher contact, and have
initiated none.

---

## 8. Recommended next work package

Smallest unit that closes your sharpest point plus the largest structural hole. **Touches
no scientific label, trains nothing, releases nothing.**

| # | Change | Closes | Closure evidence | Depends on |
|---|---|---|---|---|
| 1 | Split `exact_sequence_group` into `molecular_identity_id` (same substance) and `leakage_group_id` (same base sequence, any chemistry); mark propagated labels' provenance | §3 | QC gate: no two records share an identity id with different `ps_count`/backbone; every propagated label carries its origin | — |
| 2 | Model duplex strand identity for the siRNA entries, from German's `Duplex_Component_Master_v0.8` | §3 strand gap | Each duplex entry resolves to guide + passenger with per-strand chemistry | v0.9 (held) |
| 3 | Emit a non-trial evidence-unit table for the 451 human-laboratory rows and 9 unresolved, keyed on `source_uid` | §1 item 2 | Every human row resolves to a unit of some declared type; 0 rows unlinked | — |
| 4 | Link the 8 clinical extracts to their programme units | §1 item 3 | No row from a source that anchors a unit is left unlinked | — |
| 5 | Make the staging target conform to German's 39 `SS-F` fields, empty, with validators | §4 | A conformance test passes against the schema; no SafeSense data present | German's schema (read-only) |

Deliberately **excluded** from this package: the four chemistry corrections (§6d), the
TOLG072/073 merge, any SafeSense acquisition or ingestion, any arm-level re-linkage, and
anything touching the blocked classifier.

---

## 9. Outstanding scientific decisions

**For German**
1. **v0.9 `Position_Chemistry` records eplontersen as 19 PS**, propagated from inotersen.
   The compound is mixed-backbone. Correction needed at source; my composed map is
   reverted, not patched.
2. **Four chemistry corrections** (§6d) — evidenced, unapplied: tofersen's backbone,
   patisiran's spurious 2′-F, aprinocarsen's class, and whether `TOLG073` merges into
   `TOLG072`.
3. **Five absolute-grade disagreements** with the adjudicated 0–3 scores on MCON-TMB-002
   to 006. Direction agrees 6/6; magnitude does not. Rubric reconciliation is yours.
4. **Whether a CMC specification value is the right quantity for `purity_pct` at all.** It
   describes a released lot against an acceptance criterion, not the material dosed in a
   trial, and the documents carry no lot linkage. My instinct is that it belongs in a
   distinct field; I have not created one.
5. **The 24 of 34 human-clinical compounds that are unadjudicated** — which, if any, should
   enter the provisional clinical lane.

**For Oscar**
6. **Whether the three implemented commits stand** (§0b), given that implementation
   authority was withdrawn after they were made.
7. **Whether I receive the SafeSense `mmc4.csv` after staging**, or remain outside it.
8. **Whether to correct the access register's Sewing 2017 entry** (§6a) — the file is open.
9. **Scope decision on pegaptanib and fomivirsen**: the first approved aptamer and the
   first approved antisense oligonucleotide are absent from a dataset claiming class-wide
   coverage. Either records, or an explicit reasoned exclusion.

**Unresolved disagreement with this request:** none of substance. The one place I would
push back is framing rather than content — suggestion 1 asks me to *propose* remaining work
for a trial register that largely exists as of `fde162c`, and suggestion 4's "SafeSense"
was not identifiable from the materials provided. Both are artefacts of the stale baseline
rather than errors of judgement.

---

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**
