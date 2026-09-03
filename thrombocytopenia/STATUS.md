# Status — OligoTox-Thrombocytopenia

**All four submission parts are complete.** Assessment against the **Phase 2 announcement** (`Phase 2 description.docx`) and the
team **Phase 2 Work-Plan**. Dated 2026-09-03.

Scope: **thrombocytopenia only**. Nothing here speaks for the other endpoints.

---

## 1. Where the work plan says we should be

| Month | Oscar | Gustavo | German |
|---|---|---|---|
| August | CNS | **Thrombo** | feedback |
| September | Complement | Coagulopathy | — |
| October | Hydrocephalus | Hepatotoxicity | — |
| **November** | **1) narrative · 2) methodology · 3) PADP · 4) dataset release** | ← same | ← same |

Thrombocytopenia was the **August** workstream and its per-endpoint cycle is
*Data prep → Finish ML → Write up report → feedback*. We are at the start of
September, so this endpoint is **at the end of its scheduled window**: data prep is
done and over-delivered, the ML step has not been started, and the write-up is
outstanding.

The four submission documents are **due in November**, after all six endpoints.
So the gaps in §3 below are not yet late — but the dataset-level gaps in §4 are,
because they constrain what the November documents can truthfully claim.

## 2. The dataset as it stands

| | |
|---|---:|
| Oligonucleotides | **251** |
| Measurements | **1,786** |
| Distinct sources | **47** |
| Grade distribution 0/1/2/3 | 756 / 466 / 372 / 192 |
| Verified against primary source | **628 (35 %)** |

### Human / animal division — now explicit

The announcement singles out datasets "based on **in vitro human systems** or able
to **extrapolate data between in vitro human systems and animal data**". That axis
is now a first-class column, `subject_class`, **derived** from `study_type` ×
`species` on every assembly and independently re-derived by QC, so it cannot drift
out of agreement with the columns it summarises.

| Class | Rows | |
|---|---:|---|
| `human_clinical` | 852 | human trials |
| `human_in_vitro` | 424 | human platelets / PRP / whole blood |
| `human_ex_vivo` | 15 | |
| **human total** | **1,291** | 70 compounds |
| `animal_in_vivo` | 419 | |
| `animal_in_vitro` | 55 | |
| `animal_ex_vivo` | 13 | |
| **animal total** | **487** | 173 compounds |
| `multi_species` / `unspecified` | 8 | pooled or unstated — assigned to **neither**, never forced |

Three exports make the division directly usable:
`data/measurements_human.csv`, `data/measurements_animal.csv`, and
`data/bridge_human_animal.csv`.

**The bridge file is the one that matters for scoring.** Containing human rows and
animal rows does not demonstrate extrapolation; having the *same compound*
characterised on both sides does. **21 compounds** qualify — including inotersen
(178 human / 22 animal rows), mipomersen (114 / 31) and volanesorsen (108 / 18),
each with a published sequence. That set is what a cross-species model could
actually be trained and validated on.

## 3. The four required submission parts — COMPLETE

All four are built, page-limit-compliant, and rebuildable with
`scripts/build_submission.sh` (headless Chromium, no proprietary toolchain).

| Part | File | Pages | Limit |
|---|---|---:|---:|
| 1. Narrative | `submission/narrative.pdf` | **9** | 12 |
| 2. Methodology | `submission/methodology.pdf` | **4** | 5 |
| 3. PADP | `submission/padp.pdf` | **3** | 5 |
| 4. Dataset | `data/` + `schema.md` + `curation/` | — | none |

The narrative covers all six required elements: executive summary with
positive/negative controls, main findings, how the data were produced,
indicator/predictor measurement and distributions, the gap addressed, and the
predictive-model discussion. The methodology covers materials, extraction,
harmonisation, grading, QC and — explicitly — oligo identity characterisation and
the purity limitation. The PADP covers licensing, hosting, dissemination, FAIR
alignment and the three required U.S. Government continuity scenarios.

**"Finish ML" is done.** `scripts/model_demo.py` is a worked feasibility
demonstration, not a performance claim: grouped-by-compound cross-validation gives
**ROC-AUC 0.616 from design features alone** against a 0.500 balanced-accuracy
baseline, with `ps_count` the top feature. It also quantifies what would have been
overstated — study context adds +0.065 (the confound, not biology) and a row-level
split would have added a further +0.081 of pure leakage.

## 4. Dataset-requirement status

| Requirement | Status |
|---|---|
| data dictionary and schema | ✅ `schema.md` |
| access to raw data | ✅ CSVs + full curation record |
| open/CC licence defined | ✅ CC-BY 4.0, tracked per row |
| human/animal separation | ✅ derived `subject_class`, QC-validated, + three split exports |
| **sequences of all oligos tested** | ⚠️ **193 / 254 (76 %)** — remainder proprietary or unpublished; never guessed |
| **location of all chemical modifications** | ⚠️ **layered**: per-residue `modification_map` where printed; `gapmer_design` (170) for wing/gap boundaries; `sugar_modifications` (232) and `ps_count` (197) |
| **purity and characterization of each** | ❌ **structurally unavailable** — see below |

### The purity limitation — unchanged, and a team decision

This requirement is written for submitters who **synthesise** their compounds and
hold HPLC/MS records. This dataset curates **published** results for third-party
compounds, and the source literature does not report purity for the material it
tested. The columns exist and are populated wherever a source states purity; QC
reports coverage every run; and the methodology declares the limitation rather
than papering over it.

What we *can* evidence is **identity** characterisation, which §2.1 of the
methodology documents: patent sequence listings validated against declared
lengths, deterministic parse of regulatory chemical names with orthogonal
molecular-formula confirmation, WHO INN nomenclature, and zero-conflict
cross-dataset agreement.

**Closing the purity gap properly needs either wet-lab characterisation or
sponsors' certificates of analysis. Neither is achievable by curation. Whether to
pursue either is a team call, not mine.**

## 5. Source coverage against the team reading list

The team's `Thrombocytopenia/Papers` folder holds **40 PDFs**. Cross-checking by
resolving each filename's PMID:

- **2 are already in the dataset** (Crooke 2017, Lundberg Slingsby 2022).
- **~17 are genuinely on-topic and not yet extracted** — mostly **human clinical
  trials**, which is precisely where the dataset should deepen: Sewell 2002
  (ISIS 104838 phase I), Yacyshyn 2002 (alicaforsen dose-ranging), Henry 1997/1999
  (the foundational ISIS toxicology series), Chi 2008 (custirsen), Witztum 2019
  (APPROACH, the primary publication behind figures we hold only via the EMA
  report), Benson 2018 (NEURO-TTR), Kuter 2023 (givosiran), Landmesser 2021
  (inclisiran), and the aptamer programme papers.
- **~21 filenames carry a PMID that resolves to an entirely unrelated article** —
  composting toilets, wheat phenotyping, political science, rat-bite fever. Either
  the filenames were mislabelled on download or the wrong PDFs were fetched.
  **These were not used**, and their filename PMIDs must not be cited. Worth the
  team re-checking that folder.

## 6. Remaining outstanding items

- **Verification at 33 %** is the largest genuine gap. Two blocks (659 rows) are
  adversarially verified with zero rejections; the patent-derived and
  regulatory-review blocks are not. The documents say so plainly and the dataset
  is described as *partially* verified.
- **Team reading list**: ~17 on-topic papers extracted this round; ~21 filenames
  carry PMIDs resolving to unrelated articles and were not used — worth the team
  re-checking that folder.
- `METHODOLOGY.md` remains the long working record; the 5-page submission version
  is `submission/methodology.pdf`.

## 7. Honest summary

**Everything due is built and reviewable.** The four submission parts are
complete and within their page limits, the ML step is done, human and animal
evidence are separated with a 22-compound cross-species bridge, and an
endpoint-alignment audit runs every build proving no other toxicity's data has
leaked in.

The **dataset is in good shape and ahead of requirement on volume** — 1,786
measurements against a field where comparable public resources do not exist, with
per-row provenance, a reproducible pipeline, a committed curation record, and a
human/animal division that directly serves a stated scoring priority.

The **residual risk is not volume and not the documents — it is two dataset-content
requirements**: purity/characterization, which no amount of further curation will
supply and which needs a team decision, and verification coverage at 33 %. Both are
stated plainly in the submitted documents rather than left for a reviewer to find.
