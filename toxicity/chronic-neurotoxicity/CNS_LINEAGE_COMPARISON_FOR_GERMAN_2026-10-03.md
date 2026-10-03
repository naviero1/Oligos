# CNS lineage comparison, prepared for German

Prepared for German's decision 1 ("which CNS lineage is authoritative"), per the
2026-10-03 delegation row "CNS both lineages — stop feeding both".

**This document does not contain a recommendation.** Under §J the choice of
authoritative lineage is a scientific decision reserved to German, and under §A
I may not resolve a conflict between sources. What follows is the evidence
needed to decide, with every figure recomputed from committed trees and the
derivation stated. Where the comparison favours my own lineage I say so; where
it convicts it, §4 says that too.

| | |
|---|---|
| **Lineage A ("mine")** | `claude/oligo-cns-toxicity-dataset-tijib6` @ `ce4d677` — the *alternate* lineage |
| **Lineage B** | `claude/oligo-toxicity-dataset-k394sz` — the *original* lineage |
| **Shared ancestry** | none meaningful. `git merge-base --is-ancestor` shows neither descends from the other; common ancestor `e8e25c0` (2026-08-28). These are independent curations, not a fork and its parent. |
| **Normalisation used for sequence comparison** | upper-cased, `U`→`T`, non-`ACGT` stripped, ≥12 nt retained. Column `sequence_5to3` (A) and `sequence_base` (B — `sequence_5to3_asprinted` gives the same result). This is a **leakage/identity key, not a claim that two matched sequences are the same construct**: chemistry is not compared. |

---

## 1. Rosters

| | A — tijib6 | B — k394sz |
|---|---:|---:|
| measurement rows | **2,538** | **4,428** |
| oligo records | 592 | 1,881 |
| distinct normalised sequences (≥12 nt) | **282** (see basis note) | **1,685** |
| partition **files** | 2: `chronic-neurotoxicity` 2,393 + `hydrocephalus` 145 | 3: acute 2,081 + chronic 2,335 + hydrocephalus 12 |
| **acute evidence** | **931 rows** — carried *inside* the chronic-named file, not partitioned out | 2,081 rows / 1,866 oligos, as its own partition |
| grade column | `neurotox_grade` | `cns_tox_grade` |
| rows carrying a grade | 2,538 (**100%**) | 2,592 (**58.5%**; 1,836 `not_graded`) |

**Basis note, because two defensible counts exist for A.** The figures above
come from A's canonical corpus `toxicity/notes/cns/corpus/cns_oligos.csv` (592
records → **282** sequences). A's two *partition* files hold 586 records / 581
distinct ids → **279** sequences. The gap is the **11 oligo records that carry no
measurement** (`CNS001, 006, 007, 010, 011, 015, 545, 576, 578, 582, 585` — the
same 11 `qc_cns.py` warns about), of which 3 carry sequences found nowhere else.
An independent recomputation on the partition-file basis returns 279/276 and
**the same shared total of 150**, so the headline overlap is basis-independent;
only A's unique count moves (132 on the corpus basis, 129 on the partition
basis). I report the corpus basis and name the discrepancy rather than pick the
flattering number.

The roster gap is almost entirely one study. In B, **1,825 of 4,428 rows (41%)**
are a single rat primary-neuron calcium-oscillation screen, and B's own README
records that 1,825 of its 1,879 oligos are LNA/DNA full-PS gapmers from that one
study. So B's 6× sequence advantage is one large SAR screen with chemistry held
nearly constant — a genuine strength for isolating sequence effects, and a
genuine narrowness across chemistries.

---

## 2. Shared sequences — the delegation's 144 is exact, and scoped to one partition

| intersection | count |
|---|---:|
| A ∩ B, **full cross-lineage** | **150** |
| A ∩ B's **acute** partition | **144** ← the delegation's figure |
| A ∩ B's **chronic** partition | 7 |
| A ∩ B's **hydrocephalus** partition | 1 |
| sequences in both of B's partitions (so counted twice above) | 1 |

144 + 7 − 1 = **150**. The stated 144 reproduces exactly but describes the
overlap with B's *acute partition alone*; the cross-lineage total is 150. Six
sequences are shared only via B's chronic partition and are invisible to the
144 figure. **150 is stable across both of A's bases** (canonical corpus and
partition files), so it is not an artefact of which of A's files is read.

One narrower reading of the stated figure fails outright. German's decision-1
note describes the overlap as between "the 13-oligo original and the 573-oligo
alternate" and attaches 144 to it. Between B's *chronic* table (13 records, 7
with a sequence) and A's chronic table the intersection is **7**, not 144. So
144 cannot be the figure for the pairing that sentence describes.

| | count |
|---|---:|
| unique to A | **132** |
| unique to B | **1,535** |
| shared | 150 |

A structural point worth German's attention, and a defect in A it exposes.
**A's partition file names do not correspond to endpoint domains.** Only 290 of
the 2,393 rows in A's `chronic-neurotoxicity.measurements.csv` carry
`endpoint_domain = chronic_neurotoxicity`; **931 carry
`acute_neurotoxicity`**, alongside neuroinflammation 733, clinical_neuro_ae 232,
csf_biomarker 76, neurobehavioral 55, cytotoxicity 46 and neurodegeneration 30.
So A does hold substantial acute evidence — it is simply not partitioned out,
and the file name misdescribes 88% of its contents. That is what makes the
144-sequence overlap with B's *acute* partition unsurprising rather than
puzzling. It is a naming and structure problem in A, flagged here and not fixed:
re-partitioning is a re-graining act and the delegation forbids me to re-grain.

Whichever
lineage is chosen, those 150 sequences are the only place a record-level
crosswalk can be built, and 132 + 1,535 = 1,667 sequences exist in exactly one
lineage and would be lost outright by a straight choice.

---

## 3. Evidence composition — the decisive difference, and it favours A

| | A — tijib6 | B — k394sz |
|---|---:|---:|
| **human in-vitro rows** | **116** | **34** |
| human clinical rows | 545 | 2,341 |
| human rows, total | 661 (**26.0%**) | 2,375 (**53.6%**) |
| animal in-vivo rows | 1,696 | 228 |
| animal in-vitro rows | 181 (rat) | 1,825 (rat) |
| species represented | **5** — mouse 1,014, rat 622, monkey 239, human 661, sheep 2 | **3** — human 2,375, rat 1,826, mouse 227 |
| **non-human primate rows** | **239** | **0** |

Two things follow, and they point in opposite directions.

**In A's favour.** The Challenge prioritises human laboratory evidence, and B's
own README concedes "34 rows is not a strong showing in it". A carries **116
human in-vitro rows — 3.4× B's** — and is the only lineage with non-human
primate data (239 monkey in-vivo rows), which for intrathecally delivered ASOs
is the most translationally relevant animal evidence available. A also grades
every row and spans 5 species against B's 3.

**In B's favour.** B carries **4.3× A's human clinical evidence** (2,341 against
545 rows) and 1,535 sequences A does not have. If the intended use is training a
sequence-to-toxicity model, B is the only lineage with enough distinct sequences
to attempt it; A's 282 sequences across 2,538 rows will not support it. B also
leaves its in-vitro continuous readouts explicitly `not_graded` rather than
grading them — see §4, where that turns out to be the §E-compliant choice.

A's evidence breakdown, for completeness (`evidence_class`, 12 values):
animal_invivo 1,696 · human_trial_registry 196 · animal_laboratory 181 ·
**human_laboratory 116** · human_label_pooled 113 · human_trial_publication 113 ·
human_trial_sponsor 70 · human_case_report 18 · human_class_review 14 ·
human_observational 12 · human_background_epi 7 · human_postmarketing 2.

---

## 4. The rubric difference — and why it removes one of A's apparent advantages

The two lineages grade on differently-named columns with materially different
scopes.

| | A — `neurotox_grade` | B — `cns_tox_grade` |
|---|---|---|
| coverage | all 2,538 rows | 2,592 of 4,428; 1,836 `not_graded` |
| grade distribution | 0:1,246 1:590 2:566 3:136 | 0:1,614 1:673 2:130 3:175 |
| in-vitro rows graded | **297 — yes** | **0 — deliberately not** (`grade_basis = in_vitro_continuous_readout_not_graded`, 1,825 rows) |
| basis recorded per row | no `grade_basis` column; rubric in `schema.md:98`, rationale in `notes` when non-obvious | **`grade_basis` + `grade_status` on every row**, quoting the cutoff applied (e.g. "ANS>7 marked/severe (Hagedorn2022 Fig.1B cutoffs 7,18)") |
| status flag | none | `provisional` / `not_graded` |

**A's 100% grading coverage looked like an advantage and it is partly an
artefact of a §E violation.** §E: "Do not map in-vitro fold-change bins to
clinical severity grades (e.g. CTCAE) *unless clinically validated*. Call it
experimental response severity." A's mapping is not clinically validated —
nothing in its schema claims it is. A's rubric (`schema.md:98`) is written wholly in
organism-level terms — grade 3 is "neuronal degeneration/loss … paralysis …
moribundity/death, or dose-limiting or programme-halting neurotoxicity"; grade 1
is "transient acute behavioural signs resolving within hours–days". It contains
**no in-vitro branch**. Yet 297 in-vitro rows carry grades on it, including
`CMS2054`, a BE(2)-M17 cell-culture row whose whole result is "higher LDH than
parent compound", graded **3**.

B does not do this. By leaving 1,825 in-vitro continuous readouts ungraded, **B
is §E-compliant on exactly the point where A is not**, and B's per-row
`grade_basis` satisfies §E's requirement that the author's result and the
curator's label stay separable, which A's schema currently does not.

Compounding it on A's side: **203 of A's 2,538 graded rows (8.0%) have no
`readout_value`** — figure-only sources — of which 69 are in-vitro and 14 are
graded 3. On those rows A's label is the only quantitative content in the row.

I have not re-graded anything. Under §A I may not assign or reassign labels, and
under §J this is German's call. It is flagged because it changes the comparison:
A's grading completeness should not be read as a quality advantage until the 297
in-vitro grades are ruled on.

---

## 5. What is lost either way

**If B is chosen, A's unique contribution is lost:**

- 116 human in-vitro rows drop to 34 — a 71% loss of the evidence class the
  Challenge scores highest.
- All 239 non-human-primate rows. B has none.
- 2 of 5 species (monkey, sheep).
- 132 sequences.
- A's deduplicated human clinical-trial register, `trial_key` / `trial_key_basis`
  / `ascertainment` / `event_cluster` / `negative_eligible` columns, and the
  verified tofersen parent/extension linkage.
- The four characterization columns in §F's required shape
  (`sequence_provenance` populated on 466 records; purity/method/identity
  explicitly `NOT_REPORTED` rather than blank).

**If A is chosen, B's unique contribution is lost:**

- 1,535 sequences — with them, any realistic prospect of a sequence-level
  predictive model, since A retains only 282.
- 2,341 human clinical rows drop to 545.
- B's acute partition (2,081 rows) as a *partitioned* endpoint. A retains 931
  acute-domain rows of its own, so this is a loss of B's specific acute corpus
  and of clean partitioning, not of acute evidence altogether.
- The 181-oligo rat-in-vitro ↔ mouse-in-vivo paired panel (verified: the
  intersection is exactly 181).
- B's per-row `grade_basis` / `grade_status` audit trail.
- B's per-nucleotide modification table — B's README claims position-level
  chemistry "for all 32,898 positions", which is what §C requires and which A
  does not have in any form beyond sequence letter-case.

**Neither lineage is a superset of the other, and the loss is asymmetric by
scoring criterion.** A is optimised for human relevance and translatability; B
for scale, sequence diversity and position-level chemistry. A straight choice
discards 1,667 of the 1,817 distinct sequences held across both.

For completeness, the option I am not authorised to pursue: the 150 shared
sequences are sufficient to build a record-level crosswalk between the lineages,
which would let a merged corpus be assembled instead of one being discarded.
That is gated on the Tier 0 schema crosswalk and on this decision, and I have
not begun it.

---

## 6. Two claims in B's `_shared/cns/README.md` that should not be carried into a decision

Both are on `k394sz`, which I do not own; report-only, verified against B's
committed tree.

**The 181-compound claim — the count is right, the interpretation is not.**
README lines 35–37 state that 181 oligonucleotides carry both a rat
primary-neuron calcium-oscillation score and a mouse acute tolerability score,
"which is exactly the in-vitro-to-in-vivo extrapolation the challenge asks for".
The intersection is **exactly 181** — the arithmetic is correct. The framing is
not: this is **rat in vitro → mouse in vivo**, with no human on either side, and
the Challenge prioritises human in vitro → clinical. Line 131 of the same file
concedes "no compound in this release carries both a human and an animal row, so
the dataset cannot yet extrapolate between human in vitro and animal systems".
Lines 35–37 and line 131 of one document contradict each other.

**And B's own lineage already reached the right conclusion in a different
file.** `docs/TRANSLATIONAL_PAIRING.md` on the same branch states: "It is a
genuine and useful in-vitro-to-in-vivo bridge, and it is **not** the bridge the
Challenge asks for. Describing it as satisfying the extrapolation clause is an
overclaim, and two documents in this module did so until 2026-10-02." So B
identified and swept this overclaim on 2026-10-02 and fixed two documents;
`_shared/cns/README.md:37` is a **third occurrence the sweep missed**, and it is
now the only place in B where the discredited phrasing survives. This is a
missed-sweep correction, not a disputed scientific judgement — B's own curator
already agrees with the finding.

**The grade distribution does not reproduce.** README line 38 states "Grades
0/1/2/3 = 56/87/40/57" (sum 240). From B's committed tree: acute
measurement-level **74/81/39/51** (245); acute oligo-level by max grade
**42/78/26/51** (197); acute oligo-level by membership **50/79/27/51**; all three
endpoints measurement-level **1,614/673/130/175** (2,592). The published figure
matches none of these constructions and appears to predate the current data.

---

## 7. What is not in this document

No recommendation. No label assigned or changed on either lineage. No sequence
declared identical to another — the 150 matches are a normalised-sequence
intersection with chemistry uncompared, and two matched sequences may be
different constructs. No merge performed, no crosswalk built, no file altered on
`k394sz`. No figure reproduced on trust: every number above was recomputed from
a committed tree.

---
_Generated by [Claude Code](https://claude.ai/code)_
