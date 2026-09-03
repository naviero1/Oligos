# Coagulopathy

**Endpoint key:** `coagulopathy` · **Status:** delivered — 213 oligonucleotides, 2,388 measurements; **9 open defects in §7, none a release blocker** · **Register:** [`../README.md`](../README.md)

Coagulopathy is the fifth endpoint in the Challenge brief's list of toxicities of interest,
quoted verbatim in [the register index](../README.md#scope-authority). In oligonucleotide
safety it is, per the characterisation this project started from, prolongation of
coagulation time at high plasma Cmax of phosphorothioate-backbone ASOs.

**This dossier previously recorded the endpoint as `background-only`: zero rows, zero
sources, its entire footprint three class-level passages inside a book held for a different
endpoint.** That is no longer the state. The dataset, its methodology, its data dictionary
and its sources are in this folder; grading rules and the data dictionary are not restated
here — see [`METHODOLOGY.md`](METHODOLOGY.md) and [`schema.md`](schema.md).

---

## 1. Status summary

| | Value | Source of the figure |
|---|---|---|
| Unique oligos | 213 | `data/oligos.csv` (213 × 28) |
| Measurement rows | 2,388 | `data/measurements.csv` (2,388 × 38) |
| Per-position modification records | 941 over 47 oligos | `data/modifications.csv` |
| Sources | 75, all with the cited document committed | `data/sources.csv`, `sources/documents/` |
| Sequences published | 97 of 213 | `sequence_base` not `NOT_REPORTED`/`NOT_APPLICABLE` |
| Graded rows | 867 (0/1/2/3 = 463/312/66/26) | `coag_tox_grade`; 1,521 ungraded, each with a stated reason |
| Structural QC | 45 / 45 pass | `scripts/validate_dataset.py`, exits non-zero on failure |
| Numeric values found in their cited source | 1,876 / 1,876 | `scripts/verify_against_sources.py` |
| Rows adversarially re-checked | 174 | §6 — 0 fabrications |

## 2. What the repository held before, and what it was worth

The prior dossier's finding stands and is preserved here, because it is the baseline the
dataset is measured against. Before this round the endpoint's whole footprint was three
passages in *Methods in Molecular Biology* 2434 — a 416-page volume filed under
`kidney/sources/` behind a renal filename:

- **Ch. 25 §3.1.2**, headed "Sequence and Hybridization Independent Effects: Coagulation
  Time and Complement Activation", opens on "prolongation of coagulation time and
  activation of the alternative complement system" and then develops **the complement half
  only**. Re-extracted this round and confirmed: that clause is the entire coagulation
  content — class-level, directional, naming no compound, dose or value.
- **Ch. 1, book p.9** carries the only compound-named coagulation observation the
  repository held: GEM91 causing "prolongation of activated partial thromboplastin time
  (aPTT)" in humans, with no value and no dose.
- **Ch. 1, book p.12** attributes the effect to "the poly-anionic nature of the PS linkage".

**The endpoint's only recorded lead is now closed.** The prior dossier's §"Next step" named
Crooke ST, Baker BF, Kwoh TJ, et al. (2016), *Mol Ther* 24(10):1771–1782 — MMB Ch. 25
reference [61] — as the single retrieval lead, noting honestly that "whether it reports
per-compound coagulation times is **unverified**; the expectation rests on its title
alone." It was retrieved and read this round. It does not report those values. The
expectation was wrong, and the lead is recorded in [`SOURCES.md`](SOURCES.md) under
"Not used as a source of rows" rather than left open.

## 3. Scope decision

Recorded here, because the prior dossier noted that no scope decision for this endpoint
existed anywhere in the repository.

**In scope:** clotting times (aPTT, PT/INR, TT, ACT), fibrinogen, D-dimer, thrombin
generation, coagulation-factor and antithrombin activity, anti-Xa/anti-IIa, and bleeding or
thrombotic outcomes a source attributes to a coagulation defect.

**Out of scope: platelet count alone.** Thrombocytopenia is a separate Challenge endpoint
with its own dossier at [`../thrombocytopenia.md`](../thrombocytopenia.md). This boundary
was set before extraction and it matters: the largest concentration of
"coagulation-adjacent" text the repository already held — 16 hits on p.7 of
`_shared/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf` — is entirely
thrombocytopenia and belongs there, not here.

**Both toxicity and on-target pharmacology are in scope, on separate flags.** 1,720 of the
2,388 rows are on-target: the compounds with published clotting numbers are mostly the ones
designed to change clotting. Excluding them would have discarded most of the endpoint's
quantitative literature; pooling them would teach a model that anticoagulants prolong aPTT.
They are therefore kept and flagged, and `on_target_effect` and `unintended_toxicity` may
both be true on one row (144 rows — fitusiran above all, where the mechanism of action is
also the mechanism of harm).

## 4. Data

Records live in [`data/`](data/); the documents every row cites are in
[`sources/documents/`](sources/documents/); the raw extraction records the build consumes
are in [`sources/extraction/`](sources/extraction/), so the pipeline is reproducible from a
clean checkout with no network access.

| Axis | Distribution |
|---|---|
| Study type | animal in vivo 1,430 · clinical 453 · in vitro 297 · ex vivo human plasma 205 |
| Species | human 850 · monkey 818 · mouse 569 · rat 33 · pig 21 · minipig 17 · other 11 |
| Readout category | clotting time 1,160 · factor activity 387 · bleeding 240 · thrombotic 220 · fibrinogen 144 · platelet–coagulation crosstalk 83 · anticoagulant activity 76 · thrombin generation 47 · fibrinolysis 31 |
| Effect direction | increase 702 · no change 573 · decrease 544 · not reported 449 · not applicable (pre-dose baseline) 120 |
| Axis flags | on-target only 1,576 · unintended only 289 · both 144 · neither 379 |
| Redistribution | public domain 1,382 · CC BY-NC-ND 426 · CC BY 307 · publisher-restricted 192 · CC BY-NC 76 · unresolved 5 |

## 5. What the data shows

Detail in [`README.md`](README.md). In brief: the class effect the MMB chapter states at
class level is now quantified per compound — full-PS compounds show a median aPTT of
1.42× control among non-on-target rows — **but 42 of those 48 rows come from a single
source**, so it is one well-controlled experiment, not a meta-analysis. One source
(US 9,061,044) contradicts its own tables, and the prose is the wrong half; the
contradicting sentence is carried verbatim on all 126 of its rows. And one source
demonstrates that in-vitro aPTT saturates on PS content and cannot discriminate toxic from
non-toxic compounds, so its nulls are encoded as a method limitation rather than a safety
finding.

## 6. Verification

Three passes, in increasing strength:

1. **Structural** — 45 checks, all passing, re-runnable from the CSVs alone.
2. **Source presence** — every numeric readout searched for in the document its row cites:
   **1,876 / 1,876 located.**
3. **Adversarial semantic** — 174 rows (every grade-3 row, plus stratified samples of
   grade-2, measured-null, unintended-toxicity, clinical and qualitative rows) re-checked by
   independent reviewers instructed to *refute* them. **117 confirmed, 50 corrected,
   2 refuted, 5 unverifiable. No fabricated value or quote was found in any stratum.**

**The kidney dataset's defining defect does not repeat here.** `../kidney/CLINICAL_VALIDATION.md`
concluded that that dataset's negative class was substantially "nobody looked" rather than
"looked and found nothing", and that it should not be used to train a model until fixed.
Four reviewers tested this dataset's nulls specifically and could not break them: the null
rows are measured nulls with the assay and control arm traceable in the source, and
endpoints that were merely never mentioned are typed `NOT_REPORTED` with notes saying so —
several stating "Do not score this as evidence of no effect."

Ten defect classes were found and **corrected in the build**, so a rebuild reproduces the
fixes and QC guards them; the per-fix row counts print on every run. The corrections are
summarised in [`README.md`](README.md#what-verification-found) and the three row-level ones
are in [`sources/verification_corrections.json`](sources/verification_corrections.json),
matched on a natural key so a correction that no longer applies fails closed rather than
retargeting silently.

The single largest was a provenance failure, not a data one: 80 rows cited a supplementary
PDF that was never staged, because the document parser took the *last* filename in a cell
naming several files. Every quote was faithful to the real article throughout. A QC check
now fails the build if any source's document is missing from `sources/documents/`.

## 7. Known issues

Open, and not fixed. Each is a verification finding that could not be corrected
mechanically without re-reading sources row by row.

1. **`unintended_toxicity` is partly curator inference, not source framing.** In one
   sampled stratum 8 of 24 rows had it set where the source's own conclusion is that the
   compound is safe. A mechanical rule was applied to the clearest class (a stated null is
   no longer flagged as a toxicity, 11 rows), but the flag needs a source-conditioned
   definition: TRUE only where the source uses adverse framing.
2. **`effect_direction` drifts in sign on process-named readouts.** Where a readout names a
   *process* ("in_vitro_coagulation", "blood_flow_velocity_AUC") rather than a measured
   time or level, the direction sometimes encodes the biological outcome instead of the
   number's movement — "coagulation inhibited" recorded as `increase`. Two instances
   confirmed; 437 process-named rows are exposed to it. `effect_vs_control` carries the
   prose, so the information is recoverable, but a filter on
   `(readout_name, effect_direction)` gets the sign backwards.
3. **Values cited *by* a source rather than measured *in* it are not systematically
   distinguished.** A `value_origin` column now exists and is set on the two refuted rows,
   but it has not been swept across the dataset.
4. **Adjacent-row pickup in reflowed patent tables**, confirmed once (a Table 148 row whose
   value belongs to a neighbouring compound with a near-identical ISIS number). Tables 116,
   117 and 148 of US 10,772,906 need a row-label-by-row-label re-check.
5. **A bleeding-event row attributed to the wrong column** of a four-column table
   (PMC8820988 Table 2) — flagged, not yet re-keyed.
6. **`severity_stated_by_source` is `NOT_REPORTED` on rows whose source does state
   severity**, typically in the prose paragraph immediately preceding the cited table.
   Patent examples almost always narrate their tables; that narration was not swept.
7. **`control_value` does three different jobs** — a matched control arm, a within-subject
   baseline, and (in single-arm cohorts) a different analyte. Only the first two are
   controls.
8. **Derived ratios are not distinguishable from printed ones.** Some `ratio_to_control`
   values are computed here, some are printed by the source; `ratio_basis` records the
   method but not the provenance.
9. **The grade rule cannot see a reference range.** Mitigated by two guards and the
   `grade_caveat` flag (§ schema), but 155 grades still rest on a ratio inside the range
   where normal variation lives. Filter on `grade_caveat` before treating grade 1 as a
   finding.

## 8. Not done, and why

| Not done | Cause |
|---|---|
| Figure-only values digitised | Reading a number off a plotted panel is not transcription. Those rows carry `NOT_REPORTED` with `readout_is_qualitative = TRUE`. The largest single loss is one source's entire PT/aPTT time course. |
| Volanesorsen covered properly | Its EU SmPC and the APPROACH/COMPASS reports were not retrieved; a compound with well-documented severe thrombocytopenia is represented by an n=4 negative. |
| PMO chemistry given a measured null | None exists. Not one measured PT or aPTT value was found for eteplirsen, golodirsen, viltolarsen or casimersen. Their rows record regulatory *silence*, explicitly flagged as not a measured null. |
| Clinical compounds given sequences | No clinical compound in this dataset has a published sequence in the sources used. Sequence-to-phenotype modelling is restricted to patent and preclinical compounds. |
| Grades signed off | No subject-matter expert has reviewed them. Every grade carries `grade_status = provisional`. |

## 9. Next step

1. Resolve §7.1 and §7.2 — both are single-column sweeps with a written rule, and both
   change how the table reads under the obvious query.
2. Re-check Tables 116/117/148 of US 10,772,906 by row label (§7.4). Those three tables are
   a large share of the dataset and share a whitespace-only layout with near-identical
   compound numbers.
3. Retrieve the volanesorsen EU SmPC and the Nagano supplement (`mmc1`), the two named
   retrieval gaps.
4. Subject-matter review of the grading, after which `grade_status` can move off
   `provisional`.
5. **Two human systems sit unextracted inside patents already in the dataset**, found while
   resolving system origin and recorded here so they are not lost:
   - `COG-S034` (US 9,376,680, SERPINC1) **Example 8**: "thrombin generation studies were
     performed on Factor IX (FIX) and Antithrombin- (AT-) depleted human plasma" — the one
     genuinely human functional coagulation assay in that patent, and currently uncaptured.
   - `COG-S035` (US 10,772,906, Factor XI) **Example 7** uses human HepB3 cells, and
     Examples 1–5 and 30–32 measure human Factor XI mRNA in HepG2.
   Both would add human rows to a dataset whose human/animal balance is its main weakness.
   Note also that this patent defines "animal" as including humans (`:472`), so the phrase
   cannot be read as non-human anywhere in it — a trap for any future sweep.
