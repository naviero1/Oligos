# Hydrocephalus — endpoint dossier

**Status:** `delivered` · **Register:** [`../README.md`](../README.md) · **Data:** [`./data/`](./data/) · **Shared CNS pipeline:** [`../_shared/cns/`](../_shared/cns/)

Hydrocephalus is the eighth and last endpoint in the Challenge brief's list. An earlier revision
recorded it as `not-addressed` with zero artifacts; the next recorded a single row whose value was
`NOT_REPORTED`, because the only source was a post-marketing label entry with no denominator.
**It now holds 12 rows, and 11 of them are quantitative.**

## 1. Status

| Item | Count |
|---|---:|
| Measurement rows | **12** |
| — all human | 12 |
| Oligonucleotides | 2 |
| `source_id`s | 2 — C1, CT1 |
| Grades 0/1/2/3 | 8 / 0 / 0 / 4 |

## 2. What changed

The previous revision's closing note said advancing this endpoint would require "a quantitative
readout" and that the module had "no ventricular-volume, imaging or CSF-dynamics field". The
quantitative readout arrived from a direction that needed no new field: **clinical-trial
adverse-event tables report hydrocephalus as a count of affected patients over a count at risk**,
which the existing `readout_value` / `n_per_group` columns already hold.

Rows come from 4 sources across trials of tominersen and nusinersen, and include
**comparator arms with zero events** — that is what makes them usable rather than merely
suggestive. Both grade-0 and grade-3 rows are present.

## Human versus animal

The Challenge brief prioritises datasets *"based on in vitro human systems or able to extrapolate
data between in vitro human systems and animal data"*, so this folder splits on that axis. Both
files are written even when one is empty, so an absence is a file you can open.

| file | rows | subject classes |
|---|---:|---|
| [`data/measurements_human.csv`](./data/measurements_human.csv) | 12 | `human_clinical` 12 |
| [`data/measurements_animal.csv`](./data/measurements_animal.csv) | 0 | — none — |

Every row carries `subject_class` and `subject_group`, derived by
[`../_shared/cns/src/endpoints.py`](../_shared/cns/src/endpoints.py) and checked by four QC rules.
**`human_invitro` is still zero across the whole module** — the class the brief prioritises. An
identified, unextracted backlog of 18 candidate human *in vitro* sources is registered in
[`../_shared/cns/sources/RESEARCH_QUEUE.md`](../_shared/cns/sources/RESEARCH_QUEUE.md).

## 3. Known issues

- **Still small.** 12 rows over 2 compounds. It supports a comparison, not a model.
- **No sequences.** Neither compound's sequence is printed by its source, so this endpoint cannot
  contribute to sequence-to-toxicity modelling.
- **MedDRA terms, not adjudicated diagnoses.** "Hydrocephalus" and "Normal pressure hydrocephalus"
  are coded adverse-event terms as the sponsor reported them.
- **Adjacent findings are deliberately excluded**: raised intracranial pressure and papilloedema
  relate to hydrocephalus without being it, and the sources diagnose no link. They sit in
  [`../chronic-neurotoxicity/`](../chronic-neurotoxicity/).
- Grades are provisional.

## 4. Next step

Ventricular-volume measurements from the tominersen imaging substudies would turn this from an
adverse-event count into a graded continuous readout. That material is identified but not
extracted, and part of it is copyrighted — see
[`../_shared/cns/sources/RESEARCH_QUEUE.md`](../_shared/cns/sources/RESEARCH_QUEUE.md).
