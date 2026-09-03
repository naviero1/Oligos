# Status — OligoTox-Thrombocytopenia

Assessment against the **Phase 2 announcement** (`Phase 2 description.docx`) and the
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

## 3. The four required submission parts

| Part | Limit | Status |
|---|---|---|
| **Narrative document** | ≤ 12 pp PDF | **Not started.** Much of the content exists in `README.md` (executive summary, controls, findings, predictor distributions, gap analysis, predictive-model discussion) but it is not assembled or paginated. |
| **Methodology document** | ≤ 5 pp PDF | **Content exists, over length.** `METHODOLOGY.md` is ~30 KB — far beyond 5 pages — and **omits the explicitly required "methods used to purify and characterize oligo identity"** (see §4). |
| **PADP** | ≤ 5 pp | **Drafted** — `PADP.md`, endpoint-specific, with licensing, archival DOI and the three required U.S. Government continuity scenarios. |
| **Dataset** | no limit | **Substantially complete**, with the three gaps in §4. |

## 4. Dataset-requirement gaps — ranked by risk

The announcement is specific about what the dataset file must contain. Measured
against that text:

| Requirement | Status |
|---|---|
| data dictionary and schema documenting all metadata | ✅ `schema.md` |
| access to the raw data | ✅ CSV + the full curation record |
| open/CC licence terms defined | ✅ CC-BY 4.0 in `PADP.md` |
| **sequences of all oligos tested** | ⚠️ **191 / 251 (76 %)** |
| **location of all chemical modifications in each oligo** | ⚠️ **partial** |
| **data on the purity and characterization of each** | ❌ **absent** |

### 4a. Purity and characterization — the biggest gap

There is **no purity or characterization data in the dataset, and no column for
it.** This requirement is written for teams *generating* oligos in a lab, who
would hold HPLC/MS purity for every compound they synthesised. We are curating
**published** data, and the source literature almost never reports purity for the
compounds it tests.

This is a **structural mismatch, not an oversight**, and it should be surfaced
deliberately rather than left for a reviewer to notice. Three things can be done,
and none of them is "generate the numbers":

1. **Add the columns** (`purity_pct`, `purity_method`, `characterization_method`)
   and populate them wherever a source *does* state purity — patents sometimes
   specify it, and some Ionis papers state ">90 % by HPLC" or similar.
2. **State the limitation explicitly** in the methodology document, framed as what
   it is: an in-silico curation cannot supply wet-lab characterization for
   third-party compounds.
3. **Decide, as a team, whether this endpoint needs any wet-lab component** to
   satisfy the requirement, or whether the curation framing is accepted with the
   limitation documented. *This is a judgement call for the team, not one I should
   make.*

### 4b. Chemical modification locations — partial

`gapmer_design` (170/251) encodes wing/gap boundaries, `sugar_modifications`
(232/251) names the chemistries, and `ps_count` (197/251) gives the backbone load.
What is **not** systematically present is a **per-residue** modification map. Only
2 oligos retain the as-printed per-residue string. Where a source prints residue-level
notation, it should be preserved in a dedicated column rather than normalised away.

### 4c. Sequences — 60 missing

76 % coverage. The remainder are proprietary, class-level aggregates, or
development-code compounds without a published sequence. Patent sequence listings
are the main actionable route for closing part of the gap.

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

## 6. Other outstanding items

- **ML step not started.** The work plan puts *Finish ML* in every endpoint's
  cycle. The challenge deliverable is a dataset, not a model, but the narrative
  must discuss "how the data could be used to develop a predictive model", and a
  worked demonstration would evidence that far better than an assertion.
  `scripts/analyze_thrombo.py` already shows the structure–activity relationship
  reproduces from curation alone, which is the natural starting point.
- **Verification at 35 %.** Two blocks (659 rows) have been through adversarial
  verification with zero rejections. The patent-derived and regulatory-review
  blocks are still unverified, and the dataset must not be described as fully
  verified until they are.
- **`METHODOLOGY.md` must be cut to 5 pages** for submission; the long version is
  worth keeping in-repo as the working record.

## 7. Honest summary

The **dataset is in good shape and ahead of requirement on volume** — 1,786
measurements against a field where comparable public resources do not exist, with
per-row provenance, a reproducible pipeline, a committed curation record, and a
human/animal division that directly serves a stated scoring priority.

The **risk is not volume, it is the three dataset-content requirements** in §4 —
above all purity/characterization, which no amount of further curation will
supply and which needs a team decision. The submission documents are not late,
but what they can truthfully claim is already constrained by those gaps.
