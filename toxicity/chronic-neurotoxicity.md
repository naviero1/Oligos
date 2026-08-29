# Chronic neurotoxicity — endpoint dossier

**Status:** `delivered (thin)` · **Register:** [`./README.md`](./README.md) · **Module:** [`./cns/`](./cns/) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Chronic neurotoxicity is the seventh endpoint on the Challenge's list, quoted verbatim at
[`README.md`](./README.md#scope-authority). A previous revision of this dossier recorded the
endpoint as `not-addressed` and declared it **out of scope for Phase 2**. **That decision is
superseded.** A CNS module now exists at [`./cns/`](./cns/) and carries curated, graded rows.

The superseding is narrower than it looks, and §2 is the part to read first: the module holds
**2,065 CNS measurements, of which 6 are chronic**. The remaining 99.1% sit on the acute axis
the brief deprioritises. This dossier records both the delivery and that imbalance.

## 1. Status

| Item | Count | Basis |
|---|---:|---|
| Measurement rows, this endpoint | **6** | `tox_axis = late_onset_neurodegeneration` in [`cns/data/measurements.csv`](./cns/data/measurements.csv) |
| Oligos carrying them | **5** | ASO1–ASO5 of source `L1` |
| `source_id`s reaching them | **1** | `L1` — Kuroda 2025 |
| Grades present | 0 → 1, 2 → 2, 3 → 3 | `cns_tox_grade`; the module's own column, not `nephrotox_grade` |
| Source PDFs held | 1 | [`cns/sources/L1_Kuroda2025/`](./cns/sources/L1_Kuroda2025/) |
| Extraction status | extracted and curated | 26/26 structural checks pass — `python3 toxicity/cns/qc/validate_dataset.py` |

The three prerequisites the previous revision set for advancing this endpoint have all been met:
a chronic/acute boundary is defined (§2), a neurotoxicity-specific graded column exists with a
written rubric ([`cns/docs/SCHEMA.md`](./cns/docs/SCHEMA.md) § Grading), and primary sources were
acquired from outside the kidney library ([`cns/sources/RESEARCH_QUEUE.md`](./cns/sources/RESEARCH_QUEUE.md)).

## 2. The allocation problem — read before quoting the module's size

The brief states that submissions focused on acute neurotoxicity, "specifically alterations of
neuronal electrical activity", are **lower priority**. The CNS module's headline count is 2,065
measurements. Allocated against that sentence:

| Axis | Rows | Share | Endpoint |
|---|---:|---:|---|
| `acute_neuronal_excitability` — spontaneous calcium oscillations in rat cortical neurons | 1,825 | 88.4% | acute — *literally* alterations of neuronal electrical activity |
| `acute_behavioural` — 0–20 tolerability score, ≤1 h after dosing | 222 | 10.7% | acute |
| `late_onset_neurodegeneration` — onset ≥3 days | **6** | **0.3%** | **chronic — this dossier** |
| `clinical_*` — human adverse events | 12 | 0.6% | clinical; 1 of them is [hydrocephalus](./hydrocephalus.md) |

**99.1% of the module is the deprioritised axis.** The module is a strong dataset for a question
the brief ranks low, and a six-row dataset for the question it ranks high. Anyone citing "2,065
CNS measurements" as chronic-neurotoxicity coverage would be misreading it by a factor of ~340.

Where the boundary is drawn: the module separates axes by **time to onset**, taking it from the
sources rather than inventing it. Source `L1` states its compounds are non-toxic acutely — three
produce no acute signs, one resolves within a day — yet cause hypoactivity and motor loss from
day 3, two requiring humane sacrifice at day 7. That separation is the module's operational
chronic/acute line. The brief defines neither term, so the line is the module's, and is recorded
as such in [`cns/docs/SCHEMA.md`](./cns/docs/SCHEMA.md).

## 3. Sources allocated

| `source_id` | Source | Licence | Rows here | Local file |
|---|---|---|---:|---|
| `L1` | Kuroda T. et al. 2025, *Mol Ther Nucleic Acids* 36 — late-onset neurotoxicity and its mitigation by 5′-cyclopropylene | CC BY-NC | 6 | [`cns/sources/L1_Kuroda2025/`](./cns/sources/L1_Kuroda2025/) |

The module's other four `source_id`s (`H1`, `K1`, `C1`, `O1`) reach the acute and clinical axes,
not this one; they are itemised in [`cns/sources/RESEARCH_QUEUE.md`](./cns/sources/RESEARCH_QUEUE.md).

The two CNS reference PDFs previously filed to this endpoint in the shared Drive — an ML strategy
analysis and a mechanisms white paper — are held at [`cns/notes/intake/user_briefs/`](./cns/notes/intake/user_briefs/).
They are orientation material: no row traces to either.

## 4. Data

The six rows, by locus. Values are not reproduced here beyond what allocation requires; the CSV
is the source of truth.

| Locus | Oligo | Target | Species / route | Grade |
|---|---|---|---|---:|
| `L1-MSR-00001` | `Kuroda2025_ASO1` | MAPT | mouse, intracerebroventricular | 2 |
| `L1-MSR-00002` | `Kuroda2025_ASO2` | HDAC2 | mouse, intracerebroventricular | 3 |
| `L1-MSR-00003` | `Kuroda2025_ASO3` | SNCA | mouse, intracerebroventricular | 3 |
| `L1-MSR-00004` | `Kuroda2025_ASO4` | SNCA | mouse, intracerebroventricular | 2 |
| `L1-MSR-00005` | `Kuroda2025_ASO5` | HTT | mouse, intracerebroventricular | **0 — designated non-toxic control** |
| `L1-MSR-00006` | `Kuroda2025_ASO2` | HDAC2 | rat, intrathecal | 3 |

Two properties make these six worth more than their count suggests. All five oligos carry
**position-resolved chemistry** — recovered from the source's typeface, where bold marks LNA and
bold-italic marks 2′-MOE — so each is a per-nucleotide map, not a motif string. And `ASO5` is an
explicit negative control on the same axis, which is what lets the other five be read as a
contrast rather than a list.

`readout_value` is `NOT_REPORTED` on all six: the source publishes its tolerability scores only
as figures. The grades come from the severity the authors state in words, recorded per row in
`grade_basis`, with `readout_is_qualitative = TRUE`. No number was read off a figure.

## 5. Known issues

- **The endpoint is delivered but thin.** Six rows, one source, one laboratory, two rodent
  species. It supports no distributional claim and should not be modelled on its own.
- **Grades are provisional.** `grade_status = provisional` on every row in the module, pending
  subject-matter-expert review — the same posture as the kidney module.
- **Chronic rows carry no separate rubric of their own.** They use the module's `cns_tox_grade`
  0–3 scale, whose cut-offs are taken from the *acute* source `H1` (4, 7, 18). For the six
  chronic rows the grade is assigned from stated severity instead, which is a different
  procedure under the same column name. `grade_basis` distinguishes them row by row; a reader
  aggregating on `cns_tox_grade` alone would blur the two.
- **One row is one group, not one animal** (n = 4 per group).
- The scope-authority caveat applies unchanged: cite the brief's pp.1–3a only
  ([`cross-cutting.md` §1.1](./cross-cutting.md#11-challenge-brief--provenance-defect-pp3b6)).

## 6. Not done, and next step

| Not done | Cause |
|---|---|
| No second chronic source | Only `L1` reports a late-onset per-compound readout. The queue in [`cns/sources/RESEARCH_QUEUE.md`](./cns/sources/RESEARCH_QUEUE.md) holds five further sources, none of which is chronic. |
| No human chronic data | The module's only human rows are clinical adverse events (§2). No human *in vitro* CNS source was found at all — [`cns/OPEN_ITEMS.md`](./cns/OPEN_ITEMS.md) OI-07. |
| Numeric chronic scores | Published as figures only; extracting them would mean reading values off plots. |

Ordered next steps, highest value first:

1. **Rebalance toward the chronic axis.** The module's weight is on the deprioritised endpoint.
   Adding chronic sources moves the submission from 6 rows to a defensible dataset; adding acute
   ones does not.
2. **Work the patent.** `P1` (US 10,799,523 B2) is public domain and queued but not extracted.
   A sequence-plus-toxicity-rating patent table is the format that supplied 21 rows to the
   [kidney](./kidney/kidney-nephrotoxicity.md) endpoint.
3. **Split the grade column, or document the split harder.** Either a separate
   `chronic_tox_grade`, or a rubric section stating plainly that two assignment procedures share
   one column.
