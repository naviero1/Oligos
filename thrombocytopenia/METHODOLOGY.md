# Methodology — OligoTox-Thrombocytopenia Dataset

Methodology and provenance documentation for the **OligoTox-Thrombocytopenia**
dataset, a curated, openly-releasable, per-measurement dataset of
oligonucleotide-induced **thrombocytopenia / platelet toxicity** for the NIH/NCATS
Oligonucleotide Toxicity (OligoTox) Open Data Challenge, **Phase 2 (Data
Generation Phase)**.

> **Nature of the dataset.** This is an **in-silico curation** of pre-existing,
> publicly reported data — not wet-lab-generated data. The "materials and
> methods" below therefore describe **source identification, extraction,
> harmonization, grading, provenance, and quality control** — i.e. how the
> dataset was *assembled and computationally processed*, in the spirit of the
> Phase 2 methodology requirement.

This dataset is the **second endpoint** curated in this repository, alongside
[OligoTox-Kidney](../README.md). It deliberately reuses that dataset's two-table
design, controlled vocabularies, provenance discipline, and no-fabrication
policy, so the two are directly comparable and can be joined on oligo identity.

---

## 1. Scope and design decisions

- **Endpoint:** thrombocytopenia / platelet toxicity — a **named OligoTox
  toxicity of interest** in the challenge brief
  (`../sources/reference/OligoTox_challenge_brief.pdf`, p. 1).
- **Granularity:** **per-measurement.** One row =
  oligo × model/subject × delivery × concentration/dose × readout.
- **Coverage goal:** span all therapeutic oligonucleotide modalities, all study
  types (in-vitro / ex-vivo / animal / clinical), and the full severity range,
  **including well-sourced negative controls**.
- **Approach:** curation of existing public data — no wet lab.

### The driving domain fact: this endpoint is *bimodal*

Oligonucleotide-associated thrombocytopenia is not one phenomenon, and a dataset
that averages the two together destroys the signal a model most needs to learn.
The literature consistently describes:

1. a **common, mild, dose- and plasma-concentration-dependent** decline in
   platelet count that plateaus, is reversible, and is not immune-mediated; and
2. a **rare, severe, idiosyncratic, immune-mediated** thrombocytopenia, with
   treatment-emergent **antiplatelet antibodies** and platelet counts that can
   fall below 25 × 10⁹/L, carrying real haemorrhagic risk.

The canonical demonstration is **inotersen** (Tegsedi), which carries an FDA
**Boxed Warning** for thrombocytopenia: platelet counts below 100 × 10⁹/L
occurred in 25 % of treated patients vs 2 % on placebo (the mild mode), while
3 % had sudden severe thrombocytopenia below 25 × 10⁹/L — **all three of whom had
treatment-emergent antiplatelet IgG antibodies** — and one trial patient died of
intracranial haemorrhage (the severe mode).

The `thrombocytopenia_grade` rubric in `schema.md` is therefore built to keep the
two modes separable: a mild reversible mean decline grades **1–2**, while
antibody-mediated severe thrombocytopenia, bleeding, or discontinuation grades
**3**. The `readout_category` vocabulary likewise separates `platelet_count`
(the quantitative decline) from `immunogenicity` (the antibody mechanism) and
from `platelet_activation`/`platelet_aggregation` (the in-vitro correlates).

### Why the predictors are chemistry-centric

Platelet effects track **phosphorothioate (PS) content and protein binding**
rather than the hybridization target: PS backbones are potent platelet
activators, and neutral-backbone chemistries (PMO) and receptor-targeted
conjugates (GalNAc-siRNA) are expected to be largely silent. `ps_count`,
`backbone_chemistry`, `sugar_modifications`, and `conjugate` are therefore the
central predictor columns, and **negative-control rows on neutral-backbone
modalities are a primary deliverable, not filler** — they are what makes the
chemistry hypothesis testable.

## 2. Data model

Two normalized UTF-8 CSV tables joined on `oligo_id` (full data dictionary,
controlled vocabularies, and the grading rubric are in **`schema.md`**):

| File | Grain | Key |
|------|-------|-----|
| `data/oligos.csv` | one row per unique oligo (identity + design predictors) | `oligo_id` (PK, `TOLG###`) |
| `data/measurements.csv` | one row per oligo × model × delivery × dose × readout | `measurement_id` (PK, `TMSR###`), `oligo_id` (FK) |

Missing/unknown values are the literal string `TBD` (never guessed, never imputed
as zero). A denormalized analysis-ready view is generated at
`data/oligotox_thrombo_merged.csv` by `scripts/build_merged_thrombo.py`; the two
normalized tables remain the source of truth.

## 3. Source identification — a multi-lane parallel sweep

Rather than a single linear literature search, sources were discovered by a
**parallel multi-agent sweep across ten independent lanes**, each blind to the
others and each attacking the endpoint from a different angle. The rationale is
coverage: any single search strategy has characteristic blind spots, and lanes
that overlap provide cross-confirmation while lanes that do not overlap surface
sources the others would have missed.

| Lane | Angle |
|------|-------|
| `ionis_moe_clinical` | The Ionis/Akcea 2′-MOE PS-ASO clinical platelet record (inotersen, volanesorsen, mipomersen, eplontersen, olezarsen, tofersen…), incl. pooled cross-trial analyses |
| `regulatory_labels` | FDA prescribing information, FDA review documents, EMA SmPC/EPAR — **public domain**, values freely reproducible |
| `invitro_human_platelet` | Human platelets / PRP / whole blood exposed directly to oligos — **NCATS's stated top priority** (in-vitro human systems) |
| `mechanism_immune` | Antiplatelet antibodies, immune thrombocytopenia, platelet clearance, PF4 biology |
| `preclinical_nhp` | Cynomolgus monkey, rat, mouse, dog repeat-dose platelet and bone-marrow findings; animal-to-human translation |
| `sirna_galnac_negatives` | GalNAc-siRNA, LNP-siRNA, PMO, aptamer — the negative-control and modality-contrast lane |
| `patents_assays` | USPTO patents on platelet-tox screening assays and low-platelet-binding designs — **public domain**, worked-example tables |
| `reviews_meta` | Meta-analyses and reviews pooling AE incidence across trials, plus **reference-mining** their bibliographies |
| `megakaryocyte_models` | CD34⁺-derived megakaryocytes, megakaryocytic lines, bone marrow — the *production* axis vs the *clearance* axis |
| `sequence_chemistry_panels` | Any multi-compound panel with a platelet readout — the volume lane (supplementary tables especially) |

Sources were ranked not by topicality but by **extractable per-measurement
content**: a review stating "thrombocytopenia has been reported" is low priority;
a table of platelet counts per compound per dose is high priority. Each lane was
required to *verify retrievability* (actually fetch the URL) before proposing a
source, so the registry contains no citations that cannot be re-checked.

## 4. Data acquisition and extraction

Network egress was **open in this session** — a material difference from the
earlier kidney-dataset sessions, whose egress policy blocked all outbound fetch
and forced reliance on user-supplied PDFs and search summaries. Primary sources
were therefore retrieved directly:

| Route | Used for |
|-------|----------|
| NCBI E-utilities (`esearch`/`esummary`/`efetch`, `db=pubmed`, `db=pmc`) | PubMed discovery and **PMC open-access full text** |
| Europe PMC REST, OpenAlex, Crossref | cross-index discovery, DOI/OA resolution |
| PMC article pages + **supplementary files** | per-compound panel data (the high-value payload) |
| **DailyMed SPL REST API** | FDA prescribing information as structured XML |
| accessdata.fda.gov | FDA multi-disciplinary / pharmacology-toxicology reviews |
| EMA | SmPC and EPAR assessment reports |
| USPTO `downloadPdf` endpoint + Google Patents | patent full text, worked examples, sequence listings |

PDFs were parsed locally with **PyMuPDF**; label XML was parsed directly.
`scripts/paper_search.py` (shared with the kidney dataset) wraps the scholarly
APIs.

> **No-fabrication policy (strict).** `sequence_5to3` and any toxicity
> `readout_value` are **never invented or recalled from memory**. A value is
> recorded only when it appears in a source that was actually retrieved, and
> every row must name the **exact locus** (`Table 2`, `Fig 3B`, `label sec 5.1`,
> `Claim 7`) — a row whose locus cannot be named is dropped, not kept with a
> vague citation. `TBD` is a correct and expected answer. Compounds lacking
> published platelet data are **omitted, not padded** with assumed zeros.

## 5. Harmonization and controlled vocabularies

All categorical fields use the controlled vocabularies enumerated in
`schema.md`, which extend the kidney dataset's vocabularies with the
endpoint-specific terms this domain requires (`study_type = ex_vivo`;
`delivery_method = direct_addition` for in-vitro spiking into platelets or blood;
the platelet-specific `readout_category` and `readout_name` sets; `tissue ∈
{platelet, blood, plasma, bone_marrow, spleen}`). Vocabulary added during
curation is documented in the schema rather than left implicit, and
`scripts/qc_thrombo.py` validates every categorical value against it.

## 6. Toxicity grading

Each measurement carries an ordinal **`thrombocytopenia_grade` (0–3)** assigned
from the reported endpoint per the rubric in `schema.md`, which is
**CTCAE-aligned for clinical rows** and gives explicit in-vitro/ex-vivo
analogues so that a bench readout and a trial outcome land on a comparable
scale.

Two grading conventions are applied consistently and are worth stating
explicitly because they are the easiest places to introduce systematic error:

1. **Incidence rows are graded by the severity of the event described, not by
   the incidence.** "3 % of patients had platelet counts below 25 × 10⁹/L" is
   grade **3** (the event is severe) with `readout_value = 3`,
   `readout_unit = pct_incidence` — not grade 1 because 3 % is small.
2. **In-vitro potency is graded relative to clinical exposure.** Activation seen
   only at supra-therapeutic concentration is grade 1; the same effect at or
   below therapeutic plasma concentration is graded higher, because that is what
   makes it predictive rather than merely detectable.

Grades are flagged **provisional** pending subject-matter-expert sign-off.

## 7. Independent (predictor) variables and their distribution

*Generated by `scripts/report_thrombo.py` — see `README.md` for the current
distribution tables, which are regenerated from the CSVs after every ingestion
round so the documentation cannot drift from the data.*

## 8. Dependent (indicator) variables and their distribution

*As above — see `README.md`.*

## 9. Provenance and redistribution

- Every measurement carries `source_id` + `source_ref` + `source_table` (exact
  table/figure/label section/claim).
- `redistribution` is tracked **per row**: USPTO patents and FDA/EMA regulatory
  documents are `public_domain` (values reproducible without restriction);
  journal-derived statistics are `summary_stat` or `derived_features_only`; and
  `verify` marks rights that are unresolved and must be settled before release.
- This per-row rights tracking is what makes the dataset lawfully
  redistributable as a whole: any consumer can filter to the rows they are
  entitled to reuse.

## 10. Quality control

`scripts/qc_thrombo.py` runs after every ingestion round and gates the commit
(non-zero exit on any hard failure):

- **Schema conformance** — every categorical value validated against the
  `schema.md` enums; column-set integrity (17 / 23).
- **Referential integrity** — `measurements.oligo_id` → `oligos.oligo_id`
  (0 orphans); no duplicate primary keys.
- **Range checks** — `thrombocytopenia_grade ∈ {0,1,2,3}`; booleans `TRUE`/`FALSE`.
- **Provenance completeness** — no row may have an empty or `TBD`
  `source_id` / `source_ref` / `source_table`.
- **Sequence policy** — only explicitly-sourced sequences are filled; the
  validator is **case-insensitive**, because in gapmer rows *case encodes
  chemistry* (uppercase = modified wings, lowercase = DNA gap) and a
  case-sensitive check would reject correct rows.
- **Length consistency** — `length_nt` is cross-checked against
  `len(sequence_5to3)` and mismatches are surfaced as warnings.

### Adversarial verification

Extraction accuracy is not assumed. Every extracted row is passed to an
**independent verification agent whose instruction is to refute it** — to fetch
the cited source and check that it actually contains the claimed value at the
claimed locus, that the grade follows the rubric, and that the row is genuinely
about platelets. Verdicts are `CONFIRMED`, `CORRECTED` (real finding, wrong
field — corrections applied), or `REJECTED` (unsupported — row dropped).
`scripts/assemble_thrombo.py` applies these verdicts mechanically before the
CSVs are written, so a rejected row cannot survive into the dataset by oversight.

The failure mode this specifically defends against is the most dangerous one
available to an LLM-assisted curation: **a plausible number attached to a real
citation that does not contain it.** Schema validation cannot catch that; only
re-reading the source can.

### A failure mode worth recording: the structured-output ceiling

The richest single source in the dataset (Crooke 2017, the pooled Ionis safety
database) initially **failed to extract**, and the failure was not a research
failure: the agent had read the source and verified its values, then exceeded a
**64,000-token cap on a single structured response** while trying to return them
all at once. The symptom — a dead agent and no rows — looks identical to "the
source had nothing", which is exactly why it is worth naming.

The fix, and the pattern used for every high-yield source thereafter, is to have
the agent **write its output to a file incrementally** rather than return it as
one structured response. File-writing agents in this project handled 211-row
payloads without difficulty. The practical rule: *the size of an extraction
should not be bounded by the size of a model's reply.* A secondary benefit is
that a failure late in a long extraction no longer discards the work already
done.

### Independent known-answer test

Separately from the agent pipeline, the inotersen FDA label was retrieved and
parsed directly, and its platelet figures recorded in advance as ground truth.
Agent output for that compound was then checked against it — a held-out
correctness probe on the extraction process itself, rather than on any single
row.

## 11. Known limitations

- **Provisional grades** pending subject-matter (haematology/toxicology) review.
- **Sequence coverage is partial.** Many clinical-stage oligonucleotides have no
  published sequence, and sequences are left `TBD` rather than guessed. Patent
  sequence listings are the main actionable remainder.
- **Clinical rows dominate the severe end; in-vitro rows dominate the mild end.**
  This is a property of the underlying literature (severe thrombocytopenia is
  observed in trials, not in dishes), and it means grade is partially confounded
  with study type. Models must account for this rather than learn it as biology.

  signal frequently generate no publication, so the grade-0 class is
  systematically harder to populate than the positive classes and is drawn
  disproportionately from regulatory labels, where safety monitoring is reported
  whether or not it was eventful.
- **In-vitro–to-clinic translation is unvalidated.** Platelet activation assays
  detect the PS-backbone effect well, but the rare immune-mediated severe form is
  idiosyncratic and antibody-driven, and is **not** expected to be predicted by
  any acute in-vitro activation readout. The dataset labels both so the
  distinction can be modelled, but no claim is made that the former predicts the
  latter.
- **The megakaryocyte / production axis is a documented empty set, not an
  unsearched one.** A dedicated lane looked for oligonucleotides applied to
  CD34⁺-derived megakaryocytes, MEG-01/Dami/K562 megakaryocytic lines,
  iPSC-derived megakaryocytes or bone-marrow cultures with megakaryocyte
  readouts (number, ploidy, proplatelet formation, differentiation). Six
  targeted searches returned nothing, and none of the 21 regulatory documents
  parsed reported bone-marrow megakaryocyte histopathology. The lane was left
  **empty rather than padded**. This matters for interpretation: the dataset
  currently characterises platelet **clearance and activation**, and cannot
  distinguish impaired **production** as a mechanism. It is the clearest gap a
  wet-lab contribution to this challenge could fill.
  *(One partial exception was captured elsewhere: cord-blood-derived
  megakaryocyte proplatelet counts in PMC8804562.)*
- **Aptamer coverage is thin.** The pegaptanib FDA pharmacology review is an
  image-only scan (≈1.9 KB of extractable text across 114 pages), so that route
  yielded nothing; aptamer rows come from the PF4-complex literature instead.
- **Some rows cite an abstract, not a table.** Where a primary paper's full text
  is paywalled (several Ionis nonhuman-primate studies), values were taken from
  the PubMed abstract and the locus recorded honestly as `Abstract (Results)`.
  An abstract is a specific, retrievable locus, so these rows are legitimately
  sourced — but they are weaker evidence than a numbered table, `qc_thrombo.py`
  reports their count as a standing warning, and they should be re-verified
  against full text before release.
- **Negative results are under-reported at source.** A compound with no platelet
  signal usually generates no publication, so grade-0 rows come
  disproportionately from regulatory review documents, where haematology
  monitoring is reported whether or not it was eventful. **Label silence was
  never converted into a grade-0 row** — absence of mention is not a measured
  zero, and `scan_labels_platelet.py` states this in its own output.
- **Patent-derived rows require care** — the sister kidney dataset documented two
  concrete extraction hazards in patent sequence listings: a naive `[acgt]`-run
  regex silently mis-parses entries whose modified residues render oddly in the
  text layer (always confirm against the declared `LENGTH`), and letter case must
  be resolved from the text layer rather than from rendered pixels, because case
  encodes chemistry. Both apply here.

## 12. Reproducibility

Every row is traceable to a citable locus, so any value can be independently
re-verified against its `source_ref`. Extraction used open tooling (PyMuPDF,
standard CSV, public REST APIs). The assembly, QC, merge, and reporting steps are
all scripted (`scripts/assemble_thrombo.py`, `qc_thrombo.py`,
`build_merged_thrombo.py`, `report_thrombo.py`) rather than manual, so the path
from agent output to published CSV is re-runnable and auditable.

## 13. Intended use for predictive modeling

The two-table design exposes granular **sequence + chemistry + design**
predictors against graded, per-condition platelet outcomes. The specific modeling
questions this dataset is built to support:

1. **Does PS content / backbone chemistry predict platelet effect?** — the
   central chemistry hypothesis, testable because neutral-backbone negative
   controls are included.
2. **Can the mild dose-dependent decline be separated from the severe
   immune-mediated form?** — the clinically decisive distinction, encoded in the
   grade rubric and the `immunogenicity` readout category.
3. **Do in-vitro human platelet assays predict clinical thrombocytopenia?** —
   the question NCATS is funding, answerable because in-vitro and clinical rows
   coexist for the same compounds.
4. **How well does monkey toxicology translate to humans?** — captured wherever
   a source states it.
