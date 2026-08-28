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

This dataset is one of **four** curated in this repository — see
[`../README.md`](../README.md) for the register. It deliberately reuses the kidney
dataset's two-table design, controlled vocabularies, provenance discipline, and
no-fabrication policy, so the datasets can be **joined on oligo identity**. Their graded
columns are *not* comparable: each endpoint carries its own independently written 0–3
rubric.

---

## 1. Scope and design decisions

- **Endpoint:** thrombocytopenia / platelet toxicity — a **named OligoTox
  toxicity of interest** in the challenge brief
  (`../_shared/sources/OligoTox_challenge_brief.pdf`, p. 1).
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
`../_shared/scripts/paper_search.py` (shared with the kidney dataset) wraps the scholarly
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

### Adversarial verification — RUN ON THE TWO LARGEST BLOCKS

Every extracted row is passed to an **independent agent instructed to refute it**:
to fetch the cited source and confirm it actually contains the claimed value at
the claimed locus, that the grade follows the rubric, and that the row is
genuinely about platelets. Verdicts are `CONFIRMED`, `CORRECTED` (real finding,
wrong field — corrections applied) or `REJECTED` (unsupported — row dropped), and
`scripts/apply_verdicts.py` applies them mechanically so a rejected row cannot
survive by oversight.

**Status: 659 of 1,336 rows (49 %) verified against their primary sources.**

| Block | Rows | Result | Method |
|---|---:|---|---|
| Crooke 2017 pooled clinical | 387 | **382 CONFIRMED · 5 CORRECTED · 0 REJECTED** | every source cell transcribed into an independent machine-readable reference, then a checker parsed each row's locus and compared value, n/N, dose band and grade (377 rows); 10 by hand against the figure image |
| In-vitro human platelet (Sewing 2017 + Haematologica) | 272 | **246 CONFIRMED · 26 CORRECTED · 0 REJECTED** | all 115 Sewing values **recomputed from the S1 raw per-replicate workbook** — every mean, SD and n reproduces exactly; Haematologica values matched to Results prose, inset tables and a 600 dpi figure render |

**Zero rows were rejected**, and no value error survived in either block —
including through Crooke's multiple-denominator structure (2,363 vs 2,368;
1,877/1,878/1,788) and the Table 3 vs Supp S6 population split.

The remaining **677 rows are still `unverified`** — chiefly the patent-derived
and regulatory-review blocks. The dataset should be described as *partially*
verified until those complete.

Two corrections the verifiers made to *this document's own assumptions*, recorded
because being wrong in the methodology is worse than being wrong in a row:

- The Haematologica Table 1 "bitmap" caveat was **overstated**. The table is a
  bitmap in the JATS XML but is **fully text-extractable from the publisher PDF**,
  and the extractor had already used it. Sequences there were not lost.
- Two verifier corrections were vocabulary collisions, not data errors: 18 rows
  used `IL8_release`/`MCP1_release` where the identical Sewing readout is
  hyphenated, and 8 LDH rows needed `is_platelet_specific = FALSE`.

### Data-integrity defects found and corrected

Three defects were found *after* rows had passed schema QC — a reminder that
structural validity and correctness are different properties.

1. **A cross-source name collision on the central predictor.** The join key is
   the compound name, which assumes a name denotes one molecule everywhere.
   `ODN 2395` is a standard CpG reagent that is **fully phosphorothioate**, but
   Sewing 2017 uniquely synthesised a phosphodiester variant and named it
   `ODN2395`, reserving `ODN2395_Thio` for the PS form. Merging on the bare name
   therefore attached **39 rows describing an active PS compound** to an oligo
   record asserting `ps_count = 0` / `full_PO`. This inflated the zero-PS
   bucket's mean grade and *directly undercut the phosphorothioate hypothesis the
   dataset exists to test.* Fixed by a documented, source-aware disambiguation
   rule in the assembler; every remap is reported.

2. **A mechanism confound inverting the headline result.** `imetelstat` carries
   `ps_count = 0` — literally correct, since its N3′→P5′ **thiophosphoramidate**
   backbone contains no phosphorothioate linkages, but misleading, because that
   backbone *is* fully thio-substituted. Its 93 high-grade rows made up **74 % of
   the zero-PS bucket** and pushed that bucket's mean grade **above every
   phosphorothioate bucket**. Its thrombocytopenia is on-target
   telomerase-inhibitor myelosuppression, so it is evidence neither for nor
   against the backbone hypothesis. It is now excluded from the
   structure-activity tests only — the rows remain in the dataset, and the
   exclusion is stated in the analysis output and in `README.md`.

3. **A half-finished fix — the same collision, one level up.** Correcting the
   `ODN 2395` collision in `measurements.csv` was **not sufficient**. The
   oligo-level merge unions `aliases` and `design_source` by design, so the PS
   form's identity (`ISIS 818290`, `PS-ODN 2395`, the Haematologica source) had
   already leaked onto the **phosphodiester** record asserting `ps_count = 0`.
   Anyone resolving by alias would map the PS reagent onto the PO record and get
   the central predictor backwards — precisely the error the first fix was meant
   to prevent. Found by the in-vitro verifier, which checked the mapping
   *functionally* (re-deriving each record's values from the raw workbook) rather
   than by name. Fixed in the data and in the assembler, which now applies
   disambiguation to oligo entries as well as measurements.

4. **A controlled-vocabulary typo** (`public_documain`) that left one row's
   rights status unparseable. Now corrected from an explicit table of unambiguous
   near-misses, with every correction reported; anything not in that table still
   fails QC, which is the right outcome for a value whose meaning is unclear.

Defects 1–3 share a lesson worth generalising: **both produced structurally
valid data that pointed the wrong way scientifically.** Neither would have been
caught by schema validation, referential integrity, or range checks. They were
caught by asking whether the assembled data still reproduced a relationship the
field already knows — which is the reason `analyze_thrombo.py` exists and is run
after every ingestion round.

### Three table-extraction hazards, all of which occurred

Patent and review tables are the highest-volume sources here and also the most
dangerous, because every failure mode below produces **plausible, well-formed,
wrong data** rather than an error. Two were inherited as warnings from the sister
kidney dataset; the third was discovered here. All three were caught, and they
are recorded because anyone re-running this pipeline will meet them again.

1. **Line-wrapped sequence cells truncate silently.** A naive `[ACGT]`-run regex
   over a patent table returns a plausible short sequence when a cell wraps — one
   run produced **94 corrupted sequences** this way, and Table 50 of the PKK
   patent wraps *every* cell, yielding 8–10-mers from 16–20-mers. *Guard:* accept
   a sequence only after it matches an **independently declared length** — the
   `LENGTH` field, the target start/stop span, or the gapmer-motif sum. Across
   the APOL1 patent, 2,631 sequences passed dual validation (span *and* motif
   sum) with zero conflicts.

2. **Chemistry encoding is invisible to a renderer.** Letter case encodes
   modified wings vs DNA gap; in one paper chemistry is encoded by **font
   colour**, and phosphorothioate vs phosphodiester by **underline**. *Guard:*
   resolve encoding from the PDF **text layer** (PyMuPDF span attributes), never
   from rendered pixels — and where the text layer cannot carry it, as with the
   underline, leave `backbone_chemistry`/`ps_count` as `TBD` rather than guess.

3. **Header/row misalignment silently returns the wrong analyte** *(discovered
   here, and the most dangerous of the three)*. In three of five tables in the
   APOL1 patent, the header row **omits the leading row-label cell**, so
   addressing a column by header name is off by one — which returned **RBC counts
   where platelet counts were intended in 35 of 55 rows**. Nothing about the
   result looks wrong: the values are real haematology numbers of plausible
   magnitude from the correct study. *Guard:* three independent checks —
   right-alignment of the numeric block, an assertion against the units row, and
   a magnitude sanity check — after which all 55 values were re-verified against
   an independent manual transcription (55/55), and the 9 PKK values matched
   Google Patents cell-for-cell.

The general lesson: for tabular extraction, **validate every value against
something outside the parse** — a declared length, a units row, a second host, or
a hand transcription. A parser that is merely self-consistent will fail silently.

### Cross-dataset sequence agreement

Because the datasets in this repository share many compounds, sequences
curated here can be checked against the sister kidney dataset's records — which
were independently validated there against **WHO INN chemical nomenclature** and
**patent sequence listings**, including a duplex reverse-complement self-check.

`scripts/enrich_from_kidney.py` merges those design records in (oligos only —
kidney *outcomes* are never carried across, since a renal finding is not a
platelet finding), and `assemble_thrombo.py` reports any field where two sources
disagree.

**Result: zero sequence conflicts.** Every sequence independently extracted here
— from FDA label chemical names, patent sequence listings, and journal methods
sections — agrees base-for-base with the independently validated record. Two
different derivation paths reaching the same string is meaningful evidence that
neither is a transcription artefact, which matters for this project because
mis-parsed sequences are its most likely silent failure. Sequence coverage rose
from 112 to **120 of 132** oligos through this merge, without a single value
being guessed.

The merge also corrects **stale development stages**. `max_phase` means the
*maximum* phase a compound reached, so two sources disagreeing usually means one
is simply older: Crooke 2017 lists inotersen as phase 1 (it predates the 2018
approval) and mipomersen as phase 3 (Kynamro was approved in 2013). The
assembler therefore merges `max_phase` by taking the most advanced value rather
than the first-seen one, and unions `;`-separated list fields such as
`sugar_modifications` instead of discarding the fuller value.

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

Separately from the agent pipeline, and **before any extraction agent ran**, the
inotersen FDA label was retrieved and parsed directly by the curator and its
platelet figures written down as ground truth. The assembled dataset was then
checked against that held-out record — a correctness probe on the extraction
*process*, not on any single row.

**Result: 6 / 6 match.** Every figure independently read off the label appears in
the assembled data with the same value, at the correct grade, against the
correct locus:

| Ground-truth figure (TEGSEDI label) | Value | In dataset | Grade |
|---|---|---|---|
| platelet count < 100 × 10⁹/L | 25 % (vs 2 % placebo) | ✓ | 2 |
| platelet count < 75 × 10⁹/L | 14 % (vs 0 %) | ✓ | 2 |
| nadir < 75 × 10⁹/L, baseline < 200 × 10⁹/L | 39 % (vs 6 %) | ✓ | 2 |
| sudden severe thrombocytopenia < 25 × 10⁹/L | 3 % | ✓ | 3 |
| treatment-emergent antiplatelet IgG in severe cases | 3 / 3 | ✓ | 3 |
| fatal intracranial haemorrhage | 1 patient | ✓ | 3 |

The grading also separates correctly along the bimodal split the rubric was
designed for: the mild-mode incidence rows land at grade 2 and the
severe/antibody/fatal rows at grade 3, with no inflation of the former or
softening of the latter.

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
