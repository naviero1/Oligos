# OligoTox-Coagulopathy — a curated coagulation-toxicity dataset for oligonucleotide therapeutics

Per-measurement coagulation data for therapeutic oligonucleotides, curated for the
**NIH/NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge, Phase 2**.
Coagulopathy is the fifth endpoint on the Challenge's list of toxicities of interest.

Everything for this endpoint lives in this folder. The endpoint dossier —
what the repository held before this dataset existed, and what changed — is
[`coagulopathy.md`](./coagulopathy.md).

| | Count |
|---|---:|
| Oligonucleotides | **213** |
| Coagulation measurements | **2,388** |
| Per-position modification records | **941** (47 oligos) |
| Sources | **75** |
| Oligos with a published sequence | 97 / 213 |
| Graded rows (0/1/2/3) | 867 — 463 / 312 / 66 / 26 |
| Structural QC | 45 / 45 checks pass |
| Numeric values located in their cited source | 1,876 / 1,876 |
| Rows adversarially re-checked against sources | 174 — 0 fabrications found |

```
data/          oligos · measurements · modifications · sources  (the dataset)
sources/
  documents/   the 74 retrieved primary documents every row cites
  extraction/  the raw per-bundle extraction records the build consumes
  SOURCES.md   source registry
scripts/       build_dataset.py · validate_dataset.py · verify_against_sources.py
schema.md      data dictionary, controlled vocabularies, grading rubric
METHODOLOGY.md how the dataset was produced
coagulopathy.md the endpoint dossier
```

Rebuild and check from a clean checkout — no network needed:

```bash
python3 toxicity/coagulopathy/scripts/build_dataset.py        # sources/extraction -> data/
python3 toxicity/coagulopathy/scripts/validate_dataset.py     # 36 structural checks
python3 toxicity/coagulopathy/scripts/verify_against_sources.py  # values vs source text
```

---

## Read this before using the data: the dataset has two axes, not one

**1,720 of the 2,388 rows are ON-TARGET pharmacology, not toxicity.** The compounds with
the most published coagulation numbers are, unsurprisingly, the ones *designed* to change
coagulation: anti-factor-XI and anti-factor-XII antisense, prekallikrein and factor-VII
programmes, anticoagulant aptamers, fitusiran lowering antithrombin. A model trained on
these rows without the axis flags will learn *"anticoagulant drugs prolong aPTT"* — true,
circular, and useless for safety prediction.

Two boolean columns keep the axes apart, and **both may be true on one row**:

| | rows |
|---|---:|
| `on_target_effect` only — designed anticoagulant/procoagulant pharmacology | 1,576 |
| `unintended_toxicity` only — coagulation disturbance presented as an adverse effect | 289 |
| **both** — an on-target compound whose effect the source reports as harm | 144 |
| neither — context rows (assay controls, comparators, background) | 379 |

The 144 both-true rows are the scientifically interesting class: fitusiran is the clearest
case, where antithrombin lowering is the mechanism of action *and* the mechanism of the
thrombotic events. The dataset does not resolve that tension; it records it.

## What the data shows

**The class effect is now quantified per compound, from one study.** Among rows that are
*not* on-target pharmacology, full-phosphorothioate compounds show a median aPTT ratio of
**1.42× control** with 17 of 48 rows above 1.5×. This is the effect the safety literature
states at class level ("prolongation of coagulation time … at relatively high doses of PS
backbone ASOs") expressed as per-compound numbers. **The caveat is load-bearing: 42 of
those 48 rows come from a single source** (US 9,061,044, seven ASOs in cynomolgus monkey),
across only 9 distinct oligonucleotides. It is one well-controlled experiment, not a
meta-analysis, and should not be cited as though it were.

**A source that contradicts itself, where the prose is the wrong half.** US 9,061,044
states verbatim that "PT, aPTT and fibrinogen were not significantly altered in monkeys
treated with ISIS oligonucleotides compared to the PBS control." Its own Table 87 shows
every ISIS group above PBS at every timepoint, in a clean compound rank order peaking at
4 h — ISIS 420957 39.13 s against PBS 20.13 s, a 1.94× prolongation. The dataset extracts
the tables and carries the contradicting sentence verbatim in
`severity_stated_by_source` on all 126 rows, so the disagreement travels with the data
instead of being silently resolved. Any pipeline that reads conclusions rather than tables
records a false negative here.

**aPTT saturates on phosphorothioate content in vitro.** One source demonstrates that the
in-vitro aPTT assay cannot discriminate toxic from non-toxic compounds because PS content
alone drives it. Nulls from that assay are encoded as a *method limitation* in `notes`,
never as a safety finding — the opposite reading would teach a model that a saturated
assay means a safe compound.

## Grading

`coag_tox_grade` is an ordinal 0–3 assigned **mechanically** from the control-referenced
ratio using **CTCAE v5.0** laboratory cut-offs — a published, citable rule, not thresholds
invented here. It is applied only to the readouts CTCAE actually defines (aPTT, PT, INR,
TT, ACT prolongation; fibrinogen decrease). The other 1,521 rows are **left ungraded**,
each stating why in `grade_basis`, rather than graded by an invented threshold. Every grade
is `provisional`, and every grade is reproducible from `ratio_to_control` — a QC check
re-derives all 867 and fails the build on any disagreement.

**One limit of that rule is load-bearing and is flagged in the data.** CTCAE grades against
the *upper limit of normal*; these sources publish a control mean, not a reference range.
A ratio a few percent above 1.00 is therefore not evidence of a real prolongation, and
grading it 1 would manufacture coagulopathies out of assay noise. Two guards apply:
a source-stated measured null is regraded to 0 whatever its ratio (122 rows), and every
remaining grade with a ratio in 1.0–1.2× carries
`grade_caveat = within_reference_range_resolution` (155 rows) so it can be filtered out.
**Filter on `grade_caveat` before treating grade 1 as a finding.**

`source_stated_grade` is separate: 15 rows whose source states its own CTCAE grade
(one grade 1, two grade 2, five grade 3, seven grade 4). It is kept in its own column
because a reported clinical grade and a ratio-derived one are different rules and must not
share a field — but a severity query should read both.

## What verification found

174 rows — every grade-3 row plus stratified samples of grade-2, measured-null,
unintended-toxicity, clinical and qualitative rows — were re-checked against their sources
by independent reviewers instructed to *refute* them. Result: **117 confirmed, 50
corrected, 2 refuted, 5 unverifiable, and no fabricated value or quote anywhere.**

**The defect that sank the sibling kidney dataset does not repeat here.** That review found
its negative class was substantially "nobody looked" rather than "looked and found
nothing". Four independent reviewers tested this dataset's nulls specifically and could not
break them: of the null rows sampled, essentially all are measured nulls with the assay and
control arm traceable in the source, and rows where the endpoint was merely *not mentioned*
are consistently typed `NOT_REPORTED` with notes that say so in terms — several warning
"Do not score this as evidence of no effect."

Nine classes of defect were found and **fixed in the build**, not by hand, so a rebuild
reproduces the corrections and QC re-checks them:

| Fix | Rows | What was wrong |
|---|---:|---|
| R1 | 18 | A "relative aPTT" is a *subtracted* delta; dividing it by the control gave fold-change-minus-one and understated grades. |
| R2 | 87 | Percent **inhibition** filed as percent *of control* — inverting every potency ranking (74% inhibition is 0.26 of control, not 0.74). |
| R3 | 113 | A combination arm referenced to the untreated cell, scoring the partner drug's effect as the oligo's. |
| R4 | 120 | Pre-dose baseline draws carried as dosed effect measurements. |
| R5 | 122 | A ratio a hair above 1.00 outranking the source's own statement that nothing changed. |
| R0 | 41 | Grades left stale after R1–R3 changed the ratio under them. |
| R7 | 15 | Source-stated CTCAE grades invisible to a grade query. |
| R8 | 11 | An absence of signal flagged as an adverse finding. |
| R9 | 17 | Combination arms with no column naming the partner agent. |

A tenth was a provenance failure: 80 rows cited a supplementary PDF that was never staged,
because the parser took the *last* filename in a cell naming several files. Their quotes
were faithful to the real article all along; the citation pointed at the wrong document.
`document_file` now resolves to the first path in the cell, and a QC check fails the build
if any source's document is not on disk.

Findings recorded but **not** mechanically fixable, and carried as open issues in
[`coagulopathy.md`](./coagulopathy.md): `unintended_toxicity` is partly curator inference
rather than source framing; `effect_direction` drifts in sign on process-named readouts
(e.g. "coagulation inhibited" recorded as an increase); some values cited *by* a source
rather than measured *in* it are not distinguished; and adjacent-row pickup in reflowed
patent tables was confirmed once and needs a row-label re-check of three large tables.

## Provenance

Every measurement carries `source_id`, `source_locus` (exact table, figure, section or
label section) and a `verbatim_quote` copied from the document. Structural QC enforces
that all three are present on all 2,388 rows. `redistribution` is tracked per row:
1,382 rows are public domain (US patents and FDA labels), 383 are CC BY or CC BY-NC,
426 CC BY-NC-ND, 192 publisher-restricted, 5 unresolved.

Missing values are `NOT_REPORTED` (the source does not report it) or `NOT_APPLICABLE`
(the field has no meaning for this row). Never blank, never zero, never a guess.

## Known limitations

- **Grades are provisional** and mechanical; no subject-matter expert has reviewed them.
  Grade 1 in particular should be filtered on `grade_caveat` (see Grading).
- **97 of 213 oligos have a published sequence**, and no *clinical* compound does —
  inotersen, nusinersen, fitusiran, eplontersen, olezarsen, imetelstat and fesomersen are
  all sequence-less in the public record used here. Sequence-to-phenotype modelling is
  therefore restricted to patent and preclinical compounds; clinical rows can only be
  modelled at the chemistry-class level.
- **PMO chemistry rests on regulatory silence.** Not one measured PT or aPTT value exists
  for eteplirsen, golodirsen, viltolarsen or casimersen. Their rows record that the labels
  name no coagulation finding, explicitly flagged as *silence, not a measured null*.
- **Volanesorsen**, a compound with well-documented severe thrombocytopenia, is represented
  only by an n=4 negative; its EU SmPC and the APPROACH/COMPASS reports were not retrieved.
- **Prothrombotic rows come overwhelmingly from fitusiran**, so "hypercoagulability" risks
  being learned as "fitusiran".
- Figure-only values were never digitised: those rows carry `NOT_REPORTED` with
  `readout_is_qualitative = TRUE` rather than a number read off a plot.
