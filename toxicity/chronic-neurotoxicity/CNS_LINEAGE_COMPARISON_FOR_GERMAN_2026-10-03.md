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

> **The normalization that produced these figures, written down beside them as
> Crank's 2026-10-03 answer 5 requires.**
>
> `canon(s)` = `strip()` → `upper()` → `replace("U","T")` → strip every character
> outside `[ACGT]` → keep only if length ≥ 12. Columns: `sequence_5to3` on this
> branch; `sequence_base` on `k394sz`, cross-checked against
> `sequence_5to3_asprinted` with an identical result.
>
> **This normalization is case-INSENSITIVE, and that makes it unusable as a merge
> basis.** Answer 5 sets case-sensitive joining as the project default precisely
> because, in this corpus, letter case encodes modification position — uppercase
> wing, lowercase DNA gap — so upper-casing discards chemistry and can collapse
> two distinct molecules into one. Case-insensitive merging is **forbidden
> without adjudication**.
>
> So every figure in this section — 144, 150, 132, 1,535 — is a **candidate-link
> count for leakage control and for sizing the overlap**, and is *not* a count of
> shared molecules or a licence to join. §3 below measures what the case
> information would have preserved: 11 of the 150 map to more than one as-printed
> construct, 9 disagree on chemistry across the lineages, and 5 carry more than
> one chemistry within this branch alone. Nothing has been merged.

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

### On chronic neurotoxicity specifically, A strictly dominates

B's chronic table holds 13 records carrying **7** distinct canonical sequences
(the other 6 are `NOT_REPORTED`). A's chronic table holds 573 records carrying
**276**. **All 7 of B's chronic sequences are present in A's chronic set — B is a
strict sequence-subset of A on this endpoint.**

So for the endpoint that actually carries priority, choosing A loses **zero**
sequences, and choosing B loses 269. The 144/150 overlap figure obscures this
because it is dominated by the acute partition. This is the single cleanest fact
I can offer G-1, and it is one-directional.

### The 150 is a candidate-link count, not a merge basis — measured

§G requires that "shared-sequence grouping must **not** merge chemically
distinct administered constructs. Reference identity is not experimental-batch
identity." That is not hypothetical here:

| of the 150 shared canonical sequences | count |
|---|---:|
| mapping to **more than one** distinct as-printed construct on B's side | **11** |
| whose `sugar_modifications` sets **disagree between the lineages** | **9** |
| carrying **more than one chemistry inside A alone** | **5** |

Worked example — `ATTTCCAAATTCACTT` is one base sequence and three constructs in
A (`LNA;DNA_gap`, `LNA;DNA_gap;2'-OMe_single_gap_substitution`,
`LNA;DNA_gap;5'-cyclopropylene_DNA_single_gap_substitution`) against one in B.
`ATCACTGATTTTGAAGTCCC` is `2'-MOE;DNA_gap;5-methylcytosine` **and** `LNA;DNA_gap`
in A, `LNA;DNA_gap` only in B — two different backbone chemistries behind one
sequence string.

**Also: the two lineages share zero `oligo_id` strings.** The identifier
namespaces are completely disjoint, so canonical sequence is the *only* available
join key — which is precisely why the 144/150 figure keeps being read as stronger
than it is. Any crosswalk must carry these links as **candidate and
unadjudicated**, which is also what the Tier 0 instruction requires. I have not
merged anything.

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
lineage and would be lost outright by a straight choice. (That sum adds across
lineages, which the standing rule otherwise forbids. It is set arithmetic over
two **disjoint** sequence sets, used only to size what a straight choice
destroys — it is **not** a combined dataset size, and no row or compound total
from the two branches may be added.)

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

### Row counts flatter both lineages. The molecule counts are the real sample size.

Added after reading Crank's 2026-10-03 oversight audit, which reports the
project-wide figure "the real sample size is ~25 molecules, not thousands of
rows". Its CNS numbers reproduce exactly on my recomputation, and they correct
the row-count framing above — including in my own favour, so I state them
plainly:

| | A — tijib6 | B — k394sz (acute) |
|---|---:|---:|
| human in-vitro **rows** | 116 | 34 |
| distinct oligos behind those rows | 39 | 13 |
| …of which graded | 39 | 9 |
| **…of which graded AND sequence-bearing** | **13** | **7** |

So the honest statement of A's human-laboratory advantage is **13 molecules
against 7**, not 116 rows against 34. A 3.4× row advantage is a 1.9× molecule
advantage, and 13 is a very small training set by any standard. A's human
*clinical* mass is similarly concentrated: 545 rows rest on 30 oligos, only 10
of them sequence-bearing.

Neither lineage has a human-laboratory sample size that supports a sequence-level
model. That is a finding about the field, not about either curation, and it
belongs in the narrative's required discussion of the public-data gap.

### A's 13 depend entirely on the §E ruling, and could be 0

This must be read before §3 is weighed, and I am stating it because the
comparison is otherwise misleading in my own favour.

**All 13 of A's qualified human-laboratory molecules** — `CNS546`, `CNS549`,
`CNS564`, `CNS565`, `CNS566`, `CNS567`, `CNS570`, `CNS572`, `CNS573`, `CNS574`,
`CNS577`, `CNS581`, `CNS583` — **are graded only on in-vitro rows. Not one of
them carries a single graded non-in-vitro row** (verified per molecule: every one
has `study_type` ∈ {`in_vitro`} exclusively). And all 116 of A's
`human_laboratory` rows are `study_type = in_vitro`.

So the 13 are a subset of the 297 rows I have reported as a §E violation.
**If German withdraws those grades rather than relabelling them, A's
human-laboratory qualified-molecule count goes from 13 to 0**, and §3 — which I
headed "the decisive difference, and it favours A" — is void. If German instead
adopts §E's own remedy and relabels them "experimental response severity", the
13 survive as experimental-response molecules but are no longer graded on the
clinical scale, which changes what they can be used for rather than whether they
exist.

B's equivalent count faces the same question at smaller scale: 7 molecules, of
which B's human in-vitro grades are author-anchored and so may survive §E
untouched (see §4).

**Consequence for sequencing: the §E ruling logically precedes G-1.** A lineage
chosen on §3's evidence composition, before §E is settled, is chosen on a figure
that the §E ruling can set to zero. I am not asking for a particular order — that
is Crank's to sequence and German's to rule — only recording that the dependency
exists and which way it runs.

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

**But B's sequence advantage is entirely in the deprioritised endpoint.** All
**1,535** of B's unique sequences are present in its **acute** partition and
**none** appears in its chronic or hydrocephalus partitions — 100%, not a
majority. And **2,006 of B's 2,081 acute rows (96%) come from a single
`source_id`, `H1`.** The Phase 2 brief states acute neurotoxicity is explicitly
lower priority and carried only as a supporting module, and Crank's convergence
plan P4 states it "does not receive breadth budget".

So for the endpoints that actually carry priority, the roster comparison
inverts: on **chronic neurotoxicity** B holds **13** oligos and A holds **573**.
B's 6× sequence lead is a lead in one large single-source screen of the
lowest-priority endpoint. This does not make that screen worthless — held at
near-constant chemistry it is the best available substrate for isolating
sequence effects — but it is not an argument about chronic neurotoxicity or
hydrocephalus, and it should not be weighed as one.

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
| in-vitro rows graded | **297 — yes** | **23 of its 34 *human* in-vitro rows; 0 of its 1,825 *animal* in-vitro rows** (see the correction below) |
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

**Correction, published 2026-10-03, to a claim I made in B's favour and got
wrong.** I previously wrote that B grades "0 — deliberately not" in-vitro rows
and concluded that "B is §E-compliant on exactly the point where A is not."
**That was false as stated.** Measured: B leaves 0 of its 1,825 *animal*
in-vitro rows graded, but it grades **23 of its 34 *human* in-vitro rows** (19 at
grade 0, 4 at grade 2, 9 of 13 oligos, `grade_status = provisional`). The "0" is
true only of the animal screen.

The conclusion survives, but for a different and more precise reason than I
gave, and the distinction is the one §E actually turns on. B's 23 in-vitro grades
are anchored to explicit author calls — its `grade_basis` on those rows reads
"authors state the compound was non-toxic in this system" (19) and "authors state
a significant toxicity or viability loss in this system" (4). §E permits exactly
this: "Binary calls are marked curator-derived **unless the source explicitly
defines them**." B's are source-defined. **A's 297 are curator-derived against an
organism-level rubric that contains no in-vitro branch**, which is the act §E
prohibits.

So B is better disciplined here, not because it declines to grade in-vitro rows
— it grades them — but because every grade it does assign names the author
statement it rests on, and A's schema has no field in which to say so.

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
  predictive model, since A retains only 282. Note what this loss is and is not:
  all 1,535 sit in the **acute** partition, 96% of whose rows come from one
  source, and acute is the endpoint the brief deprioritises. On chronic
  neurotoxicity itself B holds 13 oligos against A's 573.
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
