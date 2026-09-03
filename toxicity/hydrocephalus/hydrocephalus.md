# Hydrocephalus — endpoint dossier

**Status:** `delivered (single row)` · **Register:** [`../README.md`](../README.md) · **Data:** [`./data/`](./data/) · **Shared CNS pipeline:** [`../_shared/cns/`](../_shared/cns/)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list, quoted verbatim at
[`../README.md`](../README.md#scope-authority). A previous revision recorded it as
`not-addressed` with zero artifacts. **That is superseded by exactly one row.**

One row is a small thing to revise a dossier for. It is recorded because the previous revision's
claim was that *no oligonucleotide-specific material of any kind* bears on the endpoint, and that
is no longer true. The endpoint moves from "nothing" to "one regulatory datum" — a different
statement from "delivered".

## 1. Status

| Item | Count | Basis |
|---|---:|---|
| Measurement rows | **1** | `C1-MSR-00011` in [`./data/measurements.csv`](./data/measurements.csv) |
| Oligos | **1** | nusinersen (`C1-OLG-0002`) |
| Per-position modification records | 0 | the prescribing information prints no sequence |
| `source_id`s | **1** | `C1` — FDA prescribing information via DailyMed |
| Grade | 3 | a serious neurological event named in Warnings and Precautions |
| Human rows | 1 of 1 | the only endpoint here that is entirely human |

## 2. The row

| Field | Value |
|---|---|
| Locus | `C1-MSR-00011` |
| Oligo | nusinersen (Spinraza), 12 mg intrathecal, splice-switching 2′-MOE ASO |
| Readout | `hydrocephalus_postmarketing` |
| Value | `NOT_REPORTED` — **frequency not estimable** |
| Source | SPINRAZA prescribing information, DailyMed setid `dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94`, label published 2026-04-06, § 6.2 Postmarketing Experience |
| Redistribution | public domain (US Government work) |

The value is `NOT_REPORTED` by construction, not omission. Post-marketing reports are
spontaneous, from a population of uncertain size, so no denominator exists and the label states
no frequency. The module's rule is that a missing number stays missing. **No incidence has been
estimated for this endpoint, and none can be from this source.**

## Human versus animal

The Challenge brief prioritises datasets *"based on in vitro human systems or able to extrapolate
data between in vitro human systems and animal data"*, so this folder splits its measurements on
that axis. Both files are written even when one is empty, so an absence is a file you can open
rather than something you have to notice.

| file | rows | subject classes present |
|---|---:|---|
| [`data/measurements_human.csv`](./data/measurements_human.csv) | 1 | human_clinical |
| [`data/measurements_animal.csv`](./data/measurements_animal.csv) | 0 | — none — |

Every row also carries `subject_class` (`human_clinical`, `human_invitro`, `animal_invivo`,
`animal_invitro`) and `subject_group`, both derived by
[`../_shared/cns/src/endpoints.py`](../_shared/cns/src/endpoints.py) and checked by four QC rules.
**`human_invitro` is zero across the whole CNS module** — that class is named precisely so its
emptiness is visible in the data rather than only in a caveat.

## 3. What is adjacent but is not this endpoint

Nusinersen appears in two endpoint folders — its one hydrocephalus row here, its three other
clinical rows in [`../acute-neurotoxicity/`](../acute-neurotoxicity/). An oligonucleotide is an
entity, not an endpoint; measurement rows are never duplicated, but a compound measured on two
axes is listed in both folders' `oligos.csv`. It is the only compound in this release that does
so.

Two nearby rows are deliberately **not** allocated here, since raised pressure and ventricular
enlargement relate to hydrocephalus without being it:

| Locus | What it is | Why not here |
|---|---|---|
| `C1-MSR-00002` | tofersen — papilledema and/or elevated intracranial pressure, 4 patients | A sign that *may* accompany hydrocephalus; the label reports it as its own finding and diagnoses no hydrocephalus. Allocating it here would be this dossier's inference, not the source's statement. |
| `C1-MSR-00012` | nusinersen — aseptic meningitis and arachnoiditis, post-marketing | A distinct post-marketing entry. Arachnoiditis can cause communicating hydrocephalus, but the label draws no such link. |

Both sit in [`../acute-neurotoxicity/`](../acute-neurotoxicity/).

The tominersen material queued in
[`../_shared/cns/sources/RESEARCH_QUEUE.md`](../_shared/cns/sources/RESEARCH_QUEUE.md) is the
obvious route to a real hydrocephalus dataset — the GENERATION HD1 programme reported
**dose-dependent ventricular volume increase**, the quantitative readout this endpoint lacks.
None is extracted, and three of those sources are copyrighted and held out of the repository (§5).

## 4. Data-model support

Unlike the kidney tables, the CNS schema holds this endpoint without new columns: `tox_axis`
already enumerates `clinical_serious_neurological`, and `cns_tox_grade` has a clinical rubric arm
(3 = a serious neurological event named in Warnings and Precautions). The previous revision's
finding — that extraction "would require new columns, not just new rows" — was true of the
kidney tables at [`../kidney/data/`](../kidney/data/) and remains true of them. It does not apply
to the CNS schema.

What is still missing is a **quantitative** hydrocephalus readout: there is no
ventricular-volume, imaging or CSF-dynamics field. One `NOT_REPORTED` row needs none; a real
dataset would.

## 5. Known issues

- **One row is not coverage.** A single label entry with no denominator supports no rate, no
  comparison and no model. The status says so.
- **Grade 3 is assigned from the label's own seriousness, not a measured severity.** The rule is
  in `grade_basis`; it is a regulatory classification, not a graded observation.
- **No imaging or ventricular-volume field exists** — §4.
- **The sources that would populate this endpoint are held out of the repository.** Two Roche
  CHDI conference decks and an NEJM correspondence item are copyrighted and not licensed for
  redistribution, so they are gitignored; see the research queue.
- Scope-authority caveat unchanged: cite the brief's pp.1–3a only
  ([`../cross-cutting.md` §1.1](../cross-cutting.md#11-challenge-brief--provenance-defect-pp3b6)).

## 6. Not done, and next step

| Not done | Cause |
|---|---|
| Any second row | No other source in the corpus reports hydrocephalus for an oligonucleotide. |
| A quantitative readout | Requires a ventricular-volume or imaging field the schema lacks. |
| The tominersen evidence base | Retrieved but not extracted, and partly held out on redistribution grounds. |

1. **Decide the tominersen sources.** The only realistic route to a hydrocephalus dataset — both
   an extraction decision and a redistribution one.
2. **If extracted, add a ventricular-volume field** rather than forcing a continuous imaging
   readout into `readout_value` as free text.
3. **Do not re-run the kidney sweeps.** The previous revision's `hydrocephal` sweep over the 18
   kidney PDFs stands (7 hits in 2 files, none oligonucleotide-specific). This row came from a
   source outside that library.
