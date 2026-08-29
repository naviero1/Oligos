# Schema — OligoTox-CNS

The column-by-column definitions live in [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md), which is
generated from `src/assemble.py` so that it cannot drift from the released files. This document
explains **why the schema is shaped the way it is**, which the dictionary cannot.

---

## Four tables

```
      sources.csv                        one row per source document
          ▲   source_id
          │
      oligos.csv                         one row per oligonucleotide  — THE PREDICTORS
          ▲   oligo_id
          ├──────────────────────────┐
          │                          │
  measurements.csv            modifications.csv
  one row per measured        one row per NUCLEOTIDE POSITION
  CNS outcome                 within an oligonucleotide
  — THE RESPONSE              — the per-position chemistry
```

The split is the standard one: the **causes** (sequence, chemistry, design) are stored once per
molecule; the **effects** are stored once per measurement, because one molecule is usually
measured several times — in this release most oligonucleotides carry an in vitro readout and 181
of them additionally carry an in vivo readout.

`modifications.csv` is the unusual table, and it exists for a specific reason: the challenge
requires *"the location of all chemical modifications in each oligo"*. A summary string
("5-10-5 MOE gapmer") does not satisfy that; a table with one row per position does. It is the
largest table in the release (32,569 rows) and is directly joinable to `oligos.csv`.

The same information is also carried in `oligos.modification_positions` as a compact token
string, for users who would rather not join:

```
1:A:LNA;2:T:LNA;3:T:LNA;4:T:DNA_2prime_deoxy;5:C:DNA_2prime_deoxy; …
```

---

## Position-resolved versus motif-level chemistry

Sources describe modification placement at two very different resolutions, and conflating them
would silently manufacture precision. Every oligonucleotide therefore carries
`modification_position_basis`:

| value | meaning | count in v1.0 |
|---|---|---|
| `position_resolved_from_source` | the source prints the position of each modification — in source H1 the sequence's own upper/lower case does this | 1,825 |
| `position_resolved_from_source_typeface` | the source encodes chemistry in **typeface** (bold = LNA, bold-italic = 2′-MOE); recovered by parsing the PDF's span styling, not by hand | 5 |
| `derived_from_motif` | expanded from a stated design motif plus the length. **Not used in this release** — no row needed it | 0 |
| `NOT_REPORTED` | the source does not give positions | 9 |

The two `position_resolved_*` values are both source content, not inference. The distinction is
kept because the second involved a parsing step that a user may wish to audit
(`src/build_curated.py::parse_kuroda_sequences`).

**Verification, not assertion.** For source H1 the case convention was checked against the
paper's own `Number_LNA` column: the count of upper-case characters equals the published LNA
count for **all 1,825 rows**, with zero mismatches. That is what licenses reading position out
of case. `qc/validate_dataset.py` re-checks, for every oligonucleotide, that the modification
table has exactly one contiguous row per position and that each row's nucleobase matches the
sequence at that position.

---

## Grading — `cns_tox_grade` 0–3

CNS toxicity has no single settled severity ladder, so an invented one would be the weakest
part of the dataset. Instead each grade is produced by a **named published rule**, recorded in
that row's `grade_basis`, and every grade ships as `grade_status = provisional`.

### Rows measured on the 0–20 acute tolerability score (sources H1, K1)

The cut-offs are Hagedorn et al.'s own (Fig. 1B): *"we divided ASO into those with mild,
moderate, marked, and severe tolerability signs using score cutoffs at 4, 7, and 18."*

| grade | rule | meaning |
|---|---|---|
| 0 | ANS = 0 | no observable signs |
| 1 | 0 < ANS ≤ 4 | mild |
| 2 | 4 < ANS ≤ 7 | moderate |
| 3 | ANS > 7 | marked or severe |

The boundary that matters is between grade 1 and grade 2, because that is exactly the authors'
developability line: *"only ASOs with no or mild tolerability signs, corresponding to roughly
60% of all ASOs assessed, were suitable for further development."*

**This reproduces:** in the released data, grade ≤ 1 accounts for **112 of 181** in vivo mouse
rows = **61.9 %**, matching the authors' "roughly 60 %". The mapping was not tuned to hit that
number; it falls out of using their cut-offs.

### Rows reported only qualitatively (source L1)

Where a paper publishes its scores only as figures, no numeric value is invented:
`readout_value` is `NOT_REPORTED`, `readout_is_qualitative` is `TRUE`, and the grade comes from
the severity the authors state in words — e.g. early sacrifice at day 7 for humane reasons
→ grade 3; an explicitly designated non-toxic control → grade 0.

### Clinical rows (source C1)

| grade | rule |
|---|---|
| 3 | a serious neurological event named in the label's Warnings and Precautions |
| 2 | an objective CNS inflammatory marker, or meningitis |
| 1 | a symptomatic but non-serious CNS-related adverse reaction |

Clinical grades are **not** interchangeable with preclinical grades; `tox_axis` keeps them
separable.

### Ungraded rows

The 1,825 in vitro calcium-oscillation measurements are deliberately **left ungraded**
(`cns_tox_grade` empty, `grade_status = not_graded`). They are a continuous readout on a
different quantity, and the source defines no severity bands for them. Forcing them onto the
0–3 ladder would invent thresholds.

---

## `tox_axis` — why one severity number is not enough

CNS oligonucleotide toxicity is not one phenomenon. The axis field keeps mechanistically
distinct outcomes from being pooled by accident:

| axis | window | what it is |
|---|---|---|
| `acute_behavioural` | minutes–1 h | the seizure/tremor/hyperactivity phenotype after CSF dosing |
| `acute_neuronal_excitability` | in vitro | suppression of spontaneous calcium oscillations |
| `late_onset_neurodegeneration` | days–weeks | hypoactivity and motor loss appearing ≥3 days after dosing |
| `clinical_serious_neurological` | trial | myelitis, radiculitis, raised intracranial pressure, hydrocephalus |
| `clinical_neuroinflammatory` | trial | CSF white-cell and protein elevation, aseptic meningitis |
| `clinical_cns_tolerability` | trial | headache, back pain, other symptomatic reactions |

`docs/SCORING_INSTRUMENTS.md` states which axes can legitimately be pooled.

---

## `is_human_system`

Broken out as its own boolean because the challenge specifically prioritises *"datasets based on
in vitro human systems or able to extrapolate data between in vitro human systems and animal
data."* Filtering on it is the honest way to see how much of this release is human-derived:
**12 of 2,065 measurements**, all of them clinical. The in vitro arm is rat. That gap is the
subject of the narrative document's discussion.

---

## Missing values

| token | meaning |
|---|---|
| `NOT_REPORTED` | the source does not report this. **Never** estimated, imputed, or filled from background knowledge. |
| `NOT_APPLICABLE` | the field has no meaning for this row. |
| *(empty)* | the field does not apply to this table's row type. |

`purity_pct` is `NOT_REPORTED` for **all 1,839** oligonucleotides. This is not an oversight; it
is what the literature contains. Where a source states its purification and identity-confirmation
*method*, that is captured verbatim in `purity_method` and `identity_confirmation` — present for
1,825 of 1,839. See `OPEN_ITEMS.md` OI-02 and the methodology document.

---

## Regenerating everything

```bash
python3 src/build_hagedorn.py     # source H1  -> data/staged/
python3 src/build_curated.py      # sources K1, L1, C1 -> data/staged/
python3 src/assemble.py           # staged -> data/*.csv
python3 qc/validate_dataset.py    # 26 structural checks, exit 0 = all pass
python3 src/make_figures.py       # data/ -> figures/
python3 src/make_release.py       # data/ -> deliverables/*.xlsx + docs/DATA_DICTIONARY.md
```
