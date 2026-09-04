# Where the coagulopathy endpoint stands

**Date:** 2026-09-03 · **Endpoint:** coagulopathy only · **Branch:** `claude/coagulopathy-oligos-toxicity-ap70gf`

Assessed against the three things that actually define "done": the Phase 2 instructions in
the Drive folder, the Challenge's stated evaluation preferences, and the team work-plan.

---

## 1. The four Phase 2 deliverables

The instructions require four parts. All four exist for this endpoint, built by one
command (`scripts/make_release.py`) and re-checked on every build.

| # | Required | Limit | Status | Artifact |
|---|---|---|---|---|
| 1 | Narrative document | ≤ 12 pp | **built — 5 pp** | `OligoTox-Coagulopathy_Narrative.pdf` |
| 2 | Methodology document, incl. oligo purification/characterisation | ≤ 5 pp | **built — 5 pp** | `OligoTox-Coagulopathy_Methodology.pdf` |
| 3 | Public Access & Dissemination Plan | ≤ 5 pp | **drafted — 4 pp** | `OligoTox-Coagulopathy_PADP.pdf` |
| 4 | Dataset: data dictionary + schema + raw data | no limit | **built** | `OligoTox-Coagulopathy_Dataset.xlsx` + `data/*.csv` + `schema.md` |

Every element the narrative is required to contain is present and is generated from the
data rather than written beside it: executive summary with positive and negative controls;
findings and conclusions; how the data were produced including computational processing;
how indicators and predictors were measured and their distributions; the gap addressed;
and how the data support a predictive model.

The dataset requirement is met item by item — sequences of all oligos tested (97 of 213
have one published; the rest are recorded `NOT_REPORTED`, never guessed), **the location of
every chemical modification** (941 per-position records over 47 compounds), purity and
characterisation data (method where stated; `purity_pct` is `NOT_REPORTED` throughout,
which is a property of the literature, not of the curation), additional metadata, and an
open licence.

**Optional documentation** the instructions invite — code used to collect and process the
dataset — is present and is the strongest part of the submission: a deterministic build, 55
structural checks, and a verification pass that re-reads every source document.

## 2. Against what the Challenge says it values

| Challenge preference | Where we stand |
|---|---|
| "Datasets based on **in vitro human systems**" | 1,183 of 2,685 rows (44%) are human or human-derived, up from 886 after a targeted human sweep added the EMA assessment reports, the FDA reviews with named coagulation sections, and the pharmacovigilance tier. Explicit in `species_class` / `human_system`, including for purified-protein assays where a species field cannot express it. |
| "…or able to **extrapolate between in vitro human systems and animal data**" | Supported but **bounded**: only 30 of 218 compounds carry both human and animal measurements. This is the honest ceiling on any translation claim from this release. |
| Reduce reliance on animal studies | 1,476 animal against 1,183 human. Materially improved and still the main open weakness; five extraction bundles were cut short by a session limit and are resumable. |
| High-quality, AI-ready, open | Four normalised tables, controlled vocabularies, a data dictionary covering all 90 columns, CC BY 4.0, and a build that fails rather than ships a broken table. |
| Positive/negative controls | 572 measured nulls, distinguished throughout from "never measured" — the failure mode a prior review found in the sibling kidney dataset, tested here by four independent reviewers and not reproduced. |

## 3. Against the work-plan

The plan schedules coagulopathy data-prep for 7–13 Sept, ML for 14–20 Sept, write-up for
21–27 Sept, and the four submission documents across November. **The dataset and all four
documents are complete now**, which puts this endpoint roughly two months ahead of the
plan. The time that buys is better spent on §5 than on new endpoints.

## 4. Ownership — read this before treating the documents as finished

The roles document assigns the **narrative and the PADP to Gustavo**, the **methodology to
German**, and data engineering, schema, ETL, QC and tooling to Oscar. What is delivered
here is complete on the data-engineering side and **drafted** on the other three, so that
the numbers, distributions and licence facts inside them are accurate rather than
reconstructed later. They need their owners' review, and at submission the PADP will
most likely consolidate into a single plan covering all endpoints rather than one per
endpoint.

## 5. What is genuinely outstanding

Ranked by how much it would change the submission:

1. **Grades are unreviewed.** Every grade carries `grade_status = provisional`. This is the
   one item that needs a subject-matter expert and cannot be closed by more curation.
2. **Sequences for the human subset.** 787 human rows belong to compounds with no published
   sequence. `sequence_status` separates the gaps that cannot be closed (polydisperse
   mixtures, duplexes) from ~12 approved compounds marked
   `recoverable_from_WHO_INN_nomenclature`. Recovering those is the highest-value remaining
   task, and the kidney dataset's `fill_inn_sequences.py` is the validated precedent.
3. **Five extraction bundles were cut short by a session limit** and are resumable from
   their run IDs: the 120 ClinicalTrials.gov records, the human ex-vivo aptamer panels, the
   PMO/siRNA FDA reviews, and the phase 1 clinical set including brogidirsen.
4. **The human/animal imbalance.** The sweep that ran added: FDA reviews with
   named coagulation sections (Kynamro §7.3.5.7, Spinraza §8.4.6.3), the Waylivra EPAR
   which closes the volanesorsen gap, 120 ClinicalTrials.gov records with structured
   results, and human ex-vivo aptamer panels. When those rows land the release rebuilds
   with one command and every document and figure updates itself.
3. **Nine open defects** in `coagulopathy.md` §7 — chiefly that `unintended_toxicity` is
   partly curator inference rather than source framing, and that `effect_direction` drifts
   in sign on process-named readouts. Both are single-column sweeps with a written rule.
4. **The class-effect finding rests on one source** (42 of 48 rows). More independent
   full-PS coagulation data would move it from an experiment to a result.
5. **No clinical compound has a published sequence**, which caps sequence-to-phenotype
   modelling at the patent and preclinical compounds.

## 6. Risks worth naming

- **The on-target/toxicity split is the submission's central claim and its central
  fragility.** 1,720 rows are on-target pharmacology. If a reviewer reads the row count
  without the flags, the dataset looks like a large toxicity set that is mostly not
  toxicity. The narrative leads with this rather than burying it.
- **Grade 1 is soft by construction.** CTCAE grades against a limit of normal that these
  sources do not publish; 155 grades rest on a ratio within normal variation and are
  flagged. If a reviewer treats grade 1 as signal without filtering, they will overstate
  the dataset.
- **Scope discipline.** One endpoint per folder, enforced: 6 rows are marked
  `scope_adjacent` (a complement marker, a transcript, blanket adverse-event statements)
  rather than counted as coagulation, and a QC check fails the build if any readout is
  neither recognisably coagulation nor marked. No source document is shared with another
  endpoint's folder.
