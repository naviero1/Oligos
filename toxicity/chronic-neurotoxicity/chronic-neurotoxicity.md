# Chronic neurotoxicity — endpoint dossier

**Status:** `delivered (thin)` · **Register:** [`../README.md`](../README.md) · **Data:** [`./data/`](./data/) · **Shared CNS pipeline:** [`../_shared/cns/`](../_shared/cns/)

Chronic neurotoxicity is the seventh endpoint on the Challenge's list, quoted verbatim at
[`../README.md`](../README.md#scope-authority). A previous revision recorded it as
`not-addressed` and declared it **out of scope for Phase 2**. **That decision is superseded:**
this folder holds curated, graded rows.

The superseding is narrow, and §2 is the part to read first. The CNS curation produced 2,065
measurements in total; **6 of them are chronic**, and they are the only ones in this folder.
The rest belong to other endpoints and live in those folders, not here.

## 1. Status

| Item | Count | Basis |
|---|---:|---|
| Measurement rows | **6** | [`./data/measurements.csv`](./data/measurements.csv) — all `tox_axis = late_onset_neurodegeneration` |
| Oligos | **5** | [`./data/oligos.csv`](./data/oligos.csv) — ASO1–ASO5 of source `L1` |
| Per-position modification records | 91 | [`./data/modifications.csv`](./data/modifications.csv) |
| `source_id`s | **1** | `L1` — Kuroda 2025 |
| Grades | 0 → 1, 2 → 2, 3 → 3 | `cns_tox_grade`; the CNS module's own column, not `nephrotox_grade` |
| Sequences published | 5 / 5 | every compound is position-resolved |
| Ungraded rows | 0 | |
| Human rows | 0 | mouse ×5, rat ×1 |

The three prerequisites the previous revision set for advancing this endpoint have been met: a
chronic/acute boundary is defined (§2), a neurotoxicity-specific graded column exists with a
written rubric ([`../_shared/cns/docs/SCHEMA.md`](../_shared/cns/docs/SCHEMA.md) § Grading), and
a primary source was acquired from outside the kidney library.

## 2. Why only 6 rows, when the CNS curation produced 2,065

The brief states that submissions focused on acute neurotoxicity, "specifically alterations of
neuronal electrical activity", are **lower priority**. The CNS sources were curated as one
corpus but do not describe one toxicity, so the corpus was split by endpoint and each endpoint
keeps only its own rows:

| Endpoint folder | Rows | Share | Listed in the brief? |
|---|---:|---:|---|
| [`../acute-neurotoxicity/`](../acute-neurotoxicity/) | 2,058 | 99.7% | **no** — the deprioritised axis, plus general clinical CNS AEs |
| **this folder** | **6** | 0.3% | yes |
| [`../hydrocephalus/`](../hydrocephalus/) | 1 | <0.1% | yes |

Quoting "2,065 CNS measurements" as chronic-neurotoxicity coverage would overstate it by a
factor of ~340. The allocation rule is code, not prose:
[`../_shared/cns/src/endpoints.py`](../_shared/cns/src/endpoints.py), enforced by four checks in
the QC suite that fail if any row sits in the wrong folder.

**Where the boundary is drawn.** The split is by *time to onset*, taken from the source rather
than invented. `L1` states its compounds are non-toxic acutely — three produce no acute signs,
one resolves within a day — yet cause hypoactivity and motor loss from day 3, two requiring
humane sacrifice at day 7. The brief defines neither "acute" nor "chronic", so this line is the
module's, and is recorded as such.

## 3. Sources allocated

| `source_id` | Source | Licence | Rows | Local file |
|---|---|---|---:|---|
| `L1` | Kuroda T. et al. 2025, *Mol Ther Nucleic Acids* 36 — late-onset neurotoxicity and its mitigation by 5′-cyclopropylene | CC BY-NC | 6 | [`../_shared/cns/sources/L1_Kuroda2025/`](../_shared/cns/sources/L1_Kuroda2025/) |

`L1` reaches this endpoint and no other. The full source register, including five further
sources gathered but not extracted, is
[`../_shared/cns/sources/RESEARCH_QUEUE.md`](../_shared/cns/sources/RESEARCH_QUEUE.md).

## 4. Data

| Locus | Oligo | Target | Species / route | Grade |
|---|---|---|---|---:|
| `L1-MSR-00001` | `Kuroda2025_ASO1` | MAPT | mouse, intracerebroventricular | 2 |
| `L1-MSR-00002` | `Kuroda2025_ASO2` | HDAC2 | mouse, intracerebroventricular | 3 |
| `L1-MSR-00003` | `Kuroda2025_ASO3` | SNCA | mouse, intracerebroventricular | 3 |
| `L1-MSR-00004` | `Kuroda2025_ASO4` | SNCA | mouse, intracerebroventricular | 2 |
| `L1-MSR-00005` | `Kuroda2025_ASO5` | HTT | mouse, intracerebroventricular | **0 — designated non-toxic control** |
| `L1-MSR-00006` | `Kuroda2025_ASO2` | HDAC2 | rat, intrathecal | 3 |

Two properties make these six worth more than their count suggests. All five oligos carry
**position-resolved chemistry**, recovered from the source's typeface (bold = LNA, bold-italic =
2′-MOE), so each is a per-nucleotide map rather than a motif string. And `ASO5` is an explicit
negative control on the same axis, which is what lets the other five read as a contrast rather
than a list.

`readout_value` is `NOT_REPORTED` on all six: the source publishes its tolerability scores only
as figures. Grades come from the severity the authors state in words, recorded per row in
`grade_basis`, with `readout_is_qualitative = TRUE`. No number was read off a figure.

## 5. Known issues

- **Delivered but thin.** Six rows, one source, one laboratory, two rodent species. Supports no
  distributional claim and should not be modelled alone.
- **Grades are provisional** (`grade_status = provisional` on every row), pending
  subject-matter-expert review — the same posture as the kidney module.
- **These rows carry no rubric of their own.** They use `cns_tox_grade`, whose 0–3 cut-offs come
  from the *acute* source `H1` (4, 7, 18). For these six the grade is assigned from stated
  severity instead — a different procedure under the same column name. `grade_basis`
  distinguishes them row by row; aggregating on `cns_tox_grade` alone would blur the two.
- **One row is one group, not one animal** (n = 4 per group).
- Scope-authority caveat unchanged: cite the brief's pp.1–3a only
  ([`../cross-cutting.md` §1.1](../cross-cutting.md#11-challenge-brief--provenance-defect-pp3b6)).

## 6. Not done, and next step

| Not done | Cause |
|---|---|
| No second chronic source | Only `L1` reports a late-onset per-compound readout. The five queued sources are not chronic. |
| No human chronic data | No human *in vitro* CNS source was found at all — [`../_shared/cns/OPEN_ITEMS.md`](../_shared/cns/OPEN_ITEMS.md) OI-07. |
| Numeric chronic scores | Published as figures only; extracting them would mean reading values off plots. |

1. **Rebalance toward this axis.** The curation's weight is on the deprioritised endpoint.
   Adding chronic sources moves the submission from 6 rows to a defensible dataset; adding acute
   ones does not.
2. **Work the patent.** `P1` (US 10,799,523 B2) is public domain and queued but not extracted; a
   sequence-plus-toxicity-rating patent table is the format that supplied 21 rows to
   [kidney](../kidney/kidney-nephrotoxicity.md).
3. **Split the grade column, or document the split harder** — either a separate
   `chronic_tox_grade`, or a rubric section stating plainly that two assignment procedures share
   one column.
