# Chronic neurotoxicity — endpoint dossier

**Status:** `delivered` · **Register:** [`../README.md`](../README.md) · **Data:** [`./data/`](./data/) · **Shared CNS pipeline:** [`../_shared/cns/`](../_shared/cns/)

Chronic neurotoxicity is the seventh endpoint on the Challenge's list, quoted verbatim at
[`../README.md`](../README.md#scope-authority). Two earlier revisions of this dossier recorded it
as `not-addressed` and then as `delivered (thin)` with six rows. **It is now the module's largest
endpoint and its human arm.**

## 1. Status

| Item | Count |
|---|---:|
| Measurement rows | **2,335** |
| — of which human | **2,329** |
| — of which animal | 6 |
| Oligonucleotides | 13 |
| Per-position modification records | 91 |
| `source_id`s | 3 — C1, CT1, L1 |
| Grades 0/1/2/3 | 1532 / 592 / 91 / 120 |

## 2. What counts as chronic here, and the caveat

Two kinds of row:

**Animal late-onset (6 rows, source `L1`).** Gapmers that
are *not* acutely toxic — three produce no acute signs, one resolves within a day — yet cause
hypoactivity and motor loss from day 3, two requiring humane sacrifice at day 7, and one of four
rats dying at day 14 after intrathecal dosing. All five compounds carry position-resolved
chemistry recovered from the source's typeface.

**Human clinical (2,329 rows, sources `CT1` and `C1`).** Adverse-event counts from
24 distinct sources covering
trials of intrathecally delivered oligonucleotides. These are filed here because trial adverse
events are collected across **chronic exposure** — months to years of repeat dosing — making them
the human evidence for this endpoint.

**The caveat, recorded rather than glossed:** it is the *exposure* that is chronic, not necessarily
each event. A term such as "Headache" may describe an acute reaction to a single dose. The registry
publishes no time-to-onset per event, so a finer split would be our inference rather than the
source's statement. Filter on `source_id` or `study_type` to isolate the clinical rows.

## Human versus animal

The Challenge brief prioritises datasets *"based on in vitro human systems or able to extrapolate
data between in vitro human systems and animal data"*, so this folder splits on that axis. Both
files are written even when one is empty, so an absence is a file you can open.

| file | rows | subject classes |
|---|---:|---|
| [`data/measurements_human.csv`](./data/measurements_human.csv) | 2329 | `human_clinical` 2329 |
| [`data/measurements_animal.csv`](./data/measurements_animal.csv) | 6 | `animal_invivo` 6 |

Every row carries `subject_class` and `subject_group`, derived by
[`../_shared/cns/src/endpoints.py`](../_shared/cns/src/endpoints.py) and checked by four QC rules.
**`human_invitro` is still zero across the whole module** — the class the brief prioritises. An
identified, unextracted backlog of 18 candidate human *in vitro* sources is registered in
[`../_shared/cns/sources/RESEARCH_QUEUE.md`](../_shared/cns/sources/RESEARCH_QUEUE.md).

## 3. Sources

| `source_id` | Source | Licence | Rows |
|---|---|---|---:|
| `CT1` | ClinicalTrials.gov posted results — MedDRA adverse-event tables, per-arm numerators **and denominators**, including comparator arms | public domain | 2,318 |
| `C1` | FDA prescribing information (tofersen, nusinersen) via DailyMed | public domain | 11 |
| `L1` | Kuroda T. et al. 2025, *Mol Ther Nucleic Acids* 36 — late-onset neurotoxicity and its mitigation by 5′-cyclopropylene | CC BY-NC | 6 |

`CT1` is retrieved through the ClinicalTrials.gov **API**, not the results web page: that page is a
client-side application whose HTML contains none of the adverse-event text, so scraping it returns
nothing while appearing to succeed. The retrieved JSON is committed so the build does not depend on
the service.

## 4. Known issues

- **The human rows carry no sequence.** Trial registries print drug names, not oligonucleotides.
  8 of 13 compounds
  here have `sequence_5to3_asprinted = NOT_REPORTED`. They are still useful as outcome anchors, but
  they cannot train a sequence-to-toxicity model.
- **Grades on clinical rows come from trial seriousness, not measured severity** — grade 3 means the
  event appeared in the trial's serious-adverse-event table. The rule is in `grade_basis` per row.
- **A grade-0 row means no event in that arm**, which is what makes the comparator arms usable as
  negative controls.
- **All grades are provisional**, pending subject-matter-expert review.
- **The animal arm is still six rows from one laboratory.**

## 5. Next step

The human arm is now substantial; the animal late-onset arm is not. A second late-onset animal
source would let the two be compared, which is the point of holding them in one endpoint. The
patent `P1` (US 10,799,523 B2, public domain) remains queued and unextracted.
