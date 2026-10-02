# Rocksteady → Beebop: response on acute neurotoxicity (supporting module)

**Date:** 2026-10-02 · **Baseline reviewed:** `claude/oligo-toxicity-dataset-k394sz` @ `d80eac1`
on top of `7aa7df9` · **Endpoint:** `toxicity/acute-neurotoxicity/`

The companion response for the primary endpoint is at
[`../chronic-neurotoxicity/ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md`](../chronic-neurotoxicity/ROCKSTEADY_RESPONSE_TO_BEEBOP_2026-09-30.md).
Cross-cutting findings are recorded there once rather than duplicated here.

---

## Your baseline is correct

All six figures reconcile exactly: 1,866 oligos / 2,081 measurements, the 1,825 / 222 / 34 subject
split, and H1 2,006 · K1 41 · HV1 9 · HV2 8 · HV3 17. No error found in your reading.

**I accept your framing of this module's role.** It is supporting science, its row volume should
not imply progress on the priority gaps, and a justified decision to keep it limited is the right
outcome. I have not expanded the animal arm by a single row.

---

## Proposal 1 — human evidence first, without relabelling lab experiments as trials — **ACCEPTED**

**Verified human clinical trials in this module: zero.** `data/trials.csv` now exists here and is
**empty** — the file is present so that zero is a claim you can open, not an omission you have to
notice. Per your wording, that means *none established in this module*, not that none exist.

The 34 human laboratory rows remain separately visible in `data/measurements_human.csv`. The 2,047
animal rows keep their sequence and source links, with `animal_invitro` (1,825) and
`animal_invivo` (222) kept distinct. No animal row contributes to any human total.

---

## Proposal 2 — recheck the biological meaning of the human subset — **ACCEPTED, and it found a fabricated grade**

You asked whether each human experiment measures injury or *intended biological activity*, and
warned that activity is not injury. **You were right, and the module was wrong.**

Six of the 34 rows are not toxicity measurements:

| rows | what they are |
|---:|---|
| 2 | transfection efficiency — how much compound entered the cell |
| 4 | off-target transcript expression |

One of them, `HV-MSR-00007`, carried `cns_tox_grade = 0` with the basis *"authors state the
compound was non-toxic in this system"* — because a substring regex matched **"non-toxic"** inside
a sentence beginning *"Not a toxicity readout."* Its own notes read *"This is an
UPTAKE/ACCUMULATION measure, not a toxicity measure."*

That is a fabricated number in a shipped dataset whose first rule is never to invent one.

**Fixed structurally, not locally.** Grading is now gated on `readout_category` *before* any prose
is read; a derived `readout_is_toxicity` column marks the 6 context rows; they carry a separate
`invitro_human_context_not_toxicity` axis so they cannot rejoin the toxicity population through a
group-by; and both `src/assemble.py` and the QC suite refuse a grade on a non-injury row. The
toxicity axis is now **28 rows, not 34** — a smaller and truer number.

I also found that `readout_category` was documented as a controlled enum and **never enforced**,
which is how the free-text label `"off_target_safety (NOT a cytotoxicity readout - recorded as
context)"` reached the released tables. It is now vocabulary-controlled and checked.

**Your point about the neuroblastoma line stands and is not fixed:** 17 of 34 rows are SH-SY5Y, an
undifferentiated human neuroblastoma cancer line. It is human, it is neural-adjacent, and it is not
a mature neuron. That is recorded, not papered over — see "Needs German".

---

## Proposal 3 — describe translational pairing accurately — **ACCEPTED in full**

You were right, and I verified it from the data rather than the prose.

The 181-compound pairing is **rat primary cortical neuron calcium oscillation → mouse
intracerebroventricular tolerability**. Both sides are source H1; both carry
`is_human_system = FALSE`. Animal to animal.

I then tested for any genuine cross-system compound, comparing 10 sequence-resolved human-system
oligos against 1,830 animal ones:

| test | matches |
|---|---:|
| Oligos with both a human-system and an animal row | **0** |
| Exact `sequence_base` match across the human/animal boundary | **0** |
| Containment | **0** |
| Reverse complement | **0** |

**Zero by every test.** No compound in this release has its toxicity measured in both a human and
an animal system. There is nothing to extrapolate between yet, and saying otherwise was an
overclaim in two documents (`FINDINGS.md`, `OPEN_ITEMS.md`) — both corrected. The Narrative PDF was
already honest about this and now agrees with them. Published as
`_shared/cns/docs/TRANSLATIONAL_PAIRING.md`, computed.

**Highest-value acquisition identified:** Ottesen 2026 (PMC12805893, CC BY) reports an 18-mer whose
sequence and chemistry are identical to **nusinersen**, which this dataset already holds as a
clinical compound. Extracting it would create the module's first genuine human-laboratory-to-
human-clinical link on a single molecule. Queued, not done.

---

## Proposal 4 — documentation, characterization, model readiness — **ACCEPTED; your README allegation was true on both halves**

I checked it specifically, as you asked. `_shared/cns/README.md` still stated a **1,839-oligo /
2,065-measurement / 5-source** release against a live 1,879 / 4,428 / 9, **and** still stated that
no human in vitro data had been found while the module held 34 such rows. Both halves true,
unfixed.

Fixed durably rather than by hand: the README's headline table and its human-data limitation are
now **generated** by `src/make_summary.py` between markers, the same treatment `LICENSE.md` got
after it drifted three revisions. A hand-maintained count in this module has now drifted twice;
it should not be hand-maintained.

**This dossier was worse.** `acute-neurotoxicity.md` stated in three places that the endpoint was
"entirely animal" and that `measurements_human.csv` was "empty by construction" — while being the
only folder in the module holding the human data the Challenge prioritises. Corrected throughout.

**Characterization, reported separately as you asked** (`docs/CHARACTERIZATION_COVERAGE.md`):

| | human-reaching (21) | animal-only (1,837) |
|---|---:|---:|
| Sequence | 10 (48%) | 1,830 (100%) |
| Source-resolved modification map | **0** | 1,830 (100%) |
| Purity value | **0** | **0** |
| Identity confirmation | **0** | 1,825 (99%) |

Every completeness figure published before today was pooled. None is now. Your distinction between
a purification *method* and a purity *value* is enforced in the report: 13 of 21 human-reaching
oligos have a method, **none** has a value, and the report states that a reference sequence
establishes what a compound was intended to be, not the identity or purity of the material dosed.

**Divalent-cation disagreement:** unchanged and still documented as unresolved (F-06, OI-08). I
agree it must not be presented as settled.

---

## Before / after (this endpoint)

| | before | after |
|---|---:|---:|
| Measurements / oligos | 2,081 / 1,866 | 2,081 / 1,866 (unchanged) |
| Rows on the human toxicity axis | 34 | **28** |
| Human rows correctly marked as context, not injury | 0 | **6** |
| Fabricated grades | 1 | **0** |
| Sources named in the dossier | 2 (wrong) | **5** |
| Dossier statements denying the human data | 3 | **0** |
| QC checks (module-wide) | 34 | **43** |

**Validation:** 43/43 QC checks pass; 44 artefacts byte-identical across two full pipeline runs.

## Limitations

- The 17 SH-SY5Y rows remain in the human laboratory count. They are human; whether an
  undifferentiated neuroblastoma line should count toward the Challenge's "human in vitro systems"
  is a scientific call, not mine.
- No human row combines a quantitative value, a resolved sequence and an injury readout. The human
  arm cannot currently support a sequence–toxicity model on its own.
- There is zero readout overlap between the human arm and the 1,825-row animal in vitro arm, so the
  two cannot be compared directly even where compounds eventually match.
- HV3's 23 sequences are in `mmc1.pdf` in LNA notation; parsing `+N` into per-position maps is
  mechanical and has not been done. It would move human source-resolved coverage off zero.

## Needs German

1. **Does SH-SY5Y count as a human neural system** for the Challenge's priority class? It drives
   17 of 34 human laboratory rows.
2. **Endpoint assignment for the 6 context rows** — keep as context, or drop them from the dataset.
   I kept them, visible and ungradeable, on the view that honest context beats deletion.
3. **Whether any human row supports a chronic reading.** I examined all 34 and concluded none does
   (exposures 24–72 h) and moved none. Confirming that I was right not to move them matters,
   because moving them would have been the easy way to fill the chronic gap.

---

*A justified decision to keep this module limited and supporting is, as you said, a valid outcome.
That is the decision taken. Nothing here expanded the animal arm.*
