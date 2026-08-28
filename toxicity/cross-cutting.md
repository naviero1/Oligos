# Cross-cutting artifacts

Artifacts that serve **no single endpoint**: either source material spanning several of
the eight Challenge endpoints, or endpoint-neutral infrastructure — schema, methodology,
dissemination, tooling — reusable unchanged if a second endpoint were populated. Filing
any of it under one endpoint would either duplicate it seven times or hide it from the
endpoints it also serves. One artifact listed here belongs to no endpoint at all (§3).

Endpoint dossiers: [kidney-nephrotoxicity](./kidney-nephrotoxicity.md) ·
[hepatotoxicity](./hepatotoxicity.md) · [complement-activation](./complement-activation.md) ·
[coagulopathy](./coagulopathy.md) · [thrombocytopenia](./thrombocytopenia.md) ·
[immunotoxicity](./immunotoxicity.md) · [chronic-neurotoxicity](./chronic-neurotoxicity.md) ·
[hydrocephalus](./hydrocephalus.md)

## 1. Cross-cutting source material

| File | Size | Endpoints served | Role |
|---|---|---|---|
| [`sources/reference/OligoTox_challenge_brief.pdf`](../sources/reference/OligoTox_challenge_brief.pdf) | 6 pages | all eight (scope authority) | Defines the endpoint list this register is keyed to. **Cite pp.1–3a only.** |
| [`sources/reference/CasarettDoull_Toxicology_textbook.pdf`](../sources/reference/CasarettDoull_Toxicology_textbook.pdf) | 1,473 pages | all (background only) | General toxicology definitions. No per-oligo data. |
| [`sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf`](../sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf) | 12 pages | kidney, hepatotox, thrombocytopenia, complement | Multi-endpoint ASO safety review; dedicated thrombocytopenia section. |
| [`sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf`](../sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf) | 416 pages | kidney, complement, coagulopathy, hepatotox | Multi-chapter volume. **Misfiled under `sources/kidney/`** — see §1.4. |

Registered in [`sources/SOURCES.md`](../sources/SOURCES.md) at lines 200 (MMB 2434), 208
(Frazier2015), 210 (Casarett & Doull), 211 (challenge brief).

### 1.1 Challenge brief — provenance defect (pp.3b–6)

Page 1 carries the sentence the whole register depends on, verbatim:

> Toxicities of interest include:
> Hepatotoxicity, kidney toxicity, thrombocytopenia, complement activation,
> coagulopathy, immunotoxicity, chronic neurotoxicity, and hydrocephalus.

Pages 1 to mid-3 read as an authentic NCATS executive summary. From mid-page 3 the
document changes character and **is not usable as evidence**:

- Raw markdown headings survive in the rendered PDF: `### Types of Toxicity` and
  `### Safety Assessment` (p.3), `### Mitigating Toxicity` and `### Key Literature on
  Oligonucleotide Therapeutics and Toxicity` (p.4), `### Accessing the Literature` and
  `### Conclusion:` (p.6).
- The six-item bibliography on pp.4–6 has author fields that are not names — entry 3 is
  attributed to "K. M. S. M. F. B. R. R. R. D. R. K. M. R. R. M. J. M. M. A. A. H.",
  entry 4 to "A. M. A. M. N. H. J. A. G.", entry 6 to "J. M. H. R. L. V. M. P. G. I. A."
- It closes: "If you need further details on a specific study or topic, let me know!"

Cite pp.1–3a as scope authority; cite nothing from pp.3b–6; enter none of its six
bibliography entries into the source registry. `SOURCES.md:211` registers the file as
"challenge executive summary" with no caveat — annotate that entry.

### 1.2 Casarett & Doull

1,473 pages of general toxicology. Whole-volume keyword profile: immunotox 494,
kidney 650, hepatotox 318, nephrotox 230, complement 143, coagul 143, platelet 176,
thrombocytopeni 52, hydrocephal 6 — but **oligonucleotide 13** and **antisense 7**. It
supplies background organ-toxicity definitions and nothing oligonucleotide-specific; no
row in `data/measurements.csv` derives from it.

### 1.3 Frazier 2015

Genuinely multi-endpoint over 12 pages: hepatotox 25, kidney 22, platelet 19,
complement 18, thrombocytopeni 16, nephrotox 7, coagul 0. It is structured around three
numbered challenges — #1 (p.4), #2, toxicity unrelated to accumulation (p.5), and a
dedicated section headed **"THROMBOCYTOPENIA (CHALLENGE #3)"** (p.7). Cross-reference it
from kidney, hepatotoxicity, thrombocytopenia and complement-activation; it belongs to
none of them alone.

### 1.4 Methods in Molecular Biology 2434 — misfiling finding

**Finding.** The file sits in `sources/kidney/` and its filename advertises a renal
chapter, but it is the whole 416-page volume *Antisense RNA Design, Delivery, and
Analysis* (28 chapters, six parts). The renal chapter is real, but is one of four in
Part V "Safety and Toxicology":

| Chapter | Title (book p.) | Endpoint served |
|---|---|---|
| 24 | Intrathecal Delivery of Therapeutic Oligonucleotides … CNS (p.345) | delivery route; chronic neurotoxicity context |
| 25 | Preclinical Safety Assessment of Therapeutic Oligonucleotides (p.355) | complement activation **and** coagulopathy — §3.1.2 "Effects: Coagulation Time and Complement Activation", PDF p.354 |
| 26 | Preclinical Evaluation of the Renal Toxicity of Oligonucleotide Therapeutics in Mice (p.371) | kidney |
| 27 | Protocol for Isolation and Culture of Mouse Hepatocytes (HCs), Kupffer Cells (KCs), and Liver Sinusoidal Endothelial Cells (LSECs) … (p.385) | hepatotoxicity |

Whole-volume keyword counts confirm the imbalance: antisense 517, oligonucleotide 443,
complement 43, kidney 34, renal 19, hepatotox 5, coagulation 4. Recommendation (not yet
done): move it into `sources/reference/` and index it **per chapter**, so Ch.25 is
citable from complement-activation and coagulopathy, Ch.26 from kidney, Ch.27 from
hepatotoxicity.

## 2. Endpoint-neutral infrastructure

| Artifact | What it does | Verified defect |
|---|---|---|
| [`schema.md`](../schema.md) | Data dictionary, controlled vocabularies, 0–3 rubric, QC log | Rubric at lines 74–77 is written in renal terms only; `is_kidney_specific` (line 61) presumes a kidney/not-kidney split |
| [`METHODOLOGY.md`](../METHODOLOGY.md) | 13-section Phase 2 methodology deliverable | — |
| [`PADP.md`](../PADP.md) | Public Access & Dissemination Plan; licensing, hosting, continuity | Lines 103–104 state the dataset "has **already been released** under an irrevocable CC-BY 4.0 license"; the repository contains **no LICENSE file** |
| [`sources/SOURCES.md`](../sources/SOURCES.md) | Source registry across all buckets | Carries the un-caveated brief entry (§1.1) and the MMB misfiling (§1.4) |
| [`scripts/fill_inn_sequences.py`](../scripts/fill_inn_sequences.py) | Parses WHO INN chemical nomenclature into sequences; documented at `METHODOLOGY.md:84` | Endpoint-neutral — would run unchanged on a hepatotox or immunotox oligo table |
| [`scripts/paper_search.py`](../scripts/paper_search.py) | OpenAlex / Europe PMC / PMC / Crossref search and OA full-text helper | **Documented nowhere in the curated corpus** — absent from README, METHODOLOGY, schema, PADP, SOURCES and PRESENTATION |

`scripts/build_merged.py` is *not* cross-cutting: it writes
`data/oligotox_kidney_merged.csv` and is allocated to [kidney-nephrotoxicity](./kidney-nephrotoxicity.md).

## 3. Unallocated

[`sources/_unrelated/Tipthara2016_urinary_lipidomics_OFFTOPIC.pdf`](../sources/_unrelated/Tipthara2016_urinary_lipidomics_OFFTOPIC.pdf)
— 901,081 bytes, urinary lipidomics, not oligonucleotide-related. It serves no endpoint
on the Challenge list and supplies no row. `SOURCES.md:212-213` already files it under
"off-topic upload, flagged for REMOVAL", yet it remains **tracked** (`git ls-files` lists
it) — contradicting `PADP.md:46`, "Underlying third-party full texts are never
redistributed."

**Recommendation: `git rm` it. This has not been done.**

## 4. What must change if a second endpoint is populated

Four cross-cutting artifacts are kidney-shaped today and would need rework before any
non-kidney row could be ingested:

| Artifact | Why it blocks a second endpoint |
|---|---|
| `nephrotox_grade` rubric, `schema.md:74-77` | Grades 1–3 are defined in renal terms (proteinuria, KIM-1/NGAL/clusterin, dialysis). A hepatotox or thrombocytopenia row cannot be graded against it. |
| `is_kidney_specific` flag | TRUE for all 111 rows; zero FALSE rows exist. As a boolean it can only express kidney vs not-kidney and would need to become an endpoint key. |
| [`assets/datamodel.svg`](../assets/datamodel.svg) | Renders the literal field name `nephrotox_grade (0–3)`; embedded at `PRESENTATION.md:318`. |
| [`assets/extraction.svg`](../assets/extraction.svg) | Renders "111 graded rows" and the kidney-only source_ids N2, K1, M1, N3, REV, WS; embedded at `PRESENTATION.md:464`. |

Both SVGs are allocated to the kidney dossier because they appear only in the kidney
deck, but their subject matter — the data model and the extraction ladder — is
infrastructure; they would stop being kidney-specific on re-cut. The three built deck
binaries at the repository root embed the current renderings, and no rebuild command
exists in the repo (a grep for `marp|npx|pandoc|libreoffice|soffice` outside `toxicity/`
returns only `marp: true` at `PRESENTATION.md:2`).
