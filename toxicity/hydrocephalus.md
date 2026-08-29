# Hydrocephalus — endpoint dossier

**Status:** `delivered (single row)` · **Register:** [`./README.md`](./README.md) · **Module:** [`./cns/`](./cns/) · **Cross-cutting sources:** [`./cross-cutting.md`](./cross-cutting.md)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list, quoted verbatim at
[`README.md`](./README.md#scope-authority). A previous revision recorded it as `not-addressed`
with zero artifacts of any kind. **That is superseded by exactly one row.**

One row is a small thing to revise a dossier for. It is recorded because the previous revision's
claim was that *no oligonucleotide-specific material of any kind* bears on the endpoint, and that
is no longer true: the CNS module at [`./cns/`](./cns/) carries a graded, sourced,
oligonucleotide-specific hydrocephalus observation. The endpoint moves from "nothing" to "one
regulatory datum", which is a different statement from "delivered".

## 1. Status

| Item | Count | Basis |
|---|---:|---|
| Measurement rows, this endpoint | **1** | `C1-MSR-00011` in [`cns/data/measurements.csv`](./cns/data/measurements.csv) |
| Oligos carrying them | **1** | nusinersen (`C1-OLG-0002`) |
| `source_id`s | **1** | `C1` — FDA prescribing information via DailyMed |
| Grade | 3 | `cns_tox_grade`; a serious neurological event named in Warnings and Precautions |
| Dedicated source PDFs | 0 | The label is read live from DailyMed, not held as a PDF |
| Extraction status | extracted and curated | Covered by the module's 26/26 structural checks |

## 2. The row

| Field | Value |
|---|---|
| Locus | `C1-MSR-00011` |
| Oligo | nusinersen (Spinraza), 12 mg intrathecal, splice-switching 2′-MOE ASO |
| Readout | `hydrocephalus_postmarketing` |
| Value | `NOT_REPORTED` — **frequency not estimable** |
| Axis | `clinical_serious_neurological` |
| Source | SPINRAZA prescribing information, DailyMed setid `dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94`, label published 2026-04-06, § 6.2 Postmarketing Experience |
| Redistribution | public domain (US Government work) |

The value is `NOT_REPORTED` by construction, not by omission. Post-marketing reports are
spontaneous, from a population of uncertain size, so no denominator exists and the label states
no frequency. The module's rule is that a missing number stays missing: `readout_value` is
`NOT_REPORTED` and `readout_is_qualitative` is `TRUE`. **No incidence has been estimated for this
endpoint, and none can be from this source.**

## 3. What is adjacent but is not this endpoint

Two nearby rows are deliberately *not* allocated here, since raised pressure and ventricular
enlargement are related to hydrocephalus without being it:

| Locus | What it is | Why not allocated here |
|---|---|---|
| `C1-MSR-00002` | tofersen — papilledema and/or elevated intracranial pressure, 4 patients | Raised intracranial pressure is a sign that *may* accompany hydrocephalus; the label reports it as its own finding and does not diagnose hydrocephalus. Allocating it here would be this dossier's inference, not the source's statement. |
| `C1-MSR-00012` | nusinersen — aseptic meningitis and arachnoiditis, post-marketing | A distinct post-marketing entry. Arachnoiditis can cause communicating hydrocephalus, but the label draws no such link. |

Both sit on `clinical_*` axes and are indexed by [`chronic-neurotoxicity.md`](./chronic-neurotoxicity.md) §2.

The tominersen material queued in [`cns/sources/RESEARCH_QUEUE.md`](./cns/sources/RESEARCH_QUEUE.md)
is the obvious place a real hydrocephalus dataset would come from — the GENERATION HD1 programme
reported **dose-dependent ventricular volume increase**, and ventricular volume is the
quantitative readout this endpoint lacks. None of it is extracted, and three of those sources are
copyrighted and held out of the repository (§5).

## 4. Data-model support

Unlike the kidney tables, the CNS module can hold this endpoint without new columns: `tox_axis`
already enumerates `clinical_serious_neurological`, and `cns_tox_grade` has a clinical rubric arm
(3 = a serious neurological event named in Warnings and Precautions). The previous revision's
finding — that extraction "would require new columns, not just new rows" — was true of
[`kidney/data/`](./kidney/data/), the kidney tables, and remains true of them. It does not apply to
[`cns/data/`](./cns/data/).

What the module still lacks is a **quantitative** hydrocephalus readout: there is no
ventricular-volume, imaging or CSF-dynamics field. One row of `NOT_REPORTED` needs no such field;
a real dataset would.

## 5. Known issues

- **One row is not coverage.** A single label entry with no denominator supports no rate, no
  comparison and no model. The status reads `delivered (single row)` for that reason.
- **Grade 3 is assigned from the label's own seriousness, not from a measured severity.** The
  rule is recorded in `grade_basis`; it is a regulatory classification, not a graded observation.
- **No imaging or ventricular-volume field exists** in the module — see §4.
- **The sources that would populate this endpoint are held out of the repository.** Two Roche
  CHDI conference decks and an NEJM correspondence item are copyrighted and not licensed for
  redistribution, so they are gitignored; see
  [`cns/sources/RESEARCH_QUEUE.md`](./cns/sources/RESEARCH_QUEUE.md).
- The scope-authority caveat applies unchanged: cite the brief's pp.1–3a only
  ([`cross-cutting.md` §1.1](./cross-cutting.md#11-challenge-brief--provenance-defect-pp3b6)).

## 6. Not done, and next step

| Not done | Cause |
|---|---|
| Any second row | No other source in the module reports hydrocephalus for an oligonucleotide. |
| A quantitative readout | Requires a ventricular-volume or imaging field, which the schema does not have. |
| The tominersen evidence base | Retrieved but not extracted, and partly held out of the repo on redistribution grounds. |

1. **Decide the tominersen sources.** They are the only realistic route to a hydrocephalus
   dataset. That is both an extraction decision and a redistribution one.
2. **If extracted, add a ventricular-volume field** to the CNS schema rather than forcing a
   continuous imaging readout into `readout_value` as free text.
3. **Do not re-run the kidney sweeps.** The previous revision's `hydrocephal` sweep over the 18
   kidney PDFs stands and returned 7 hits in 2 files, none oligonucleotide-specific. Nothing in
   this revision changes that; the new row came from a source outside that library.
