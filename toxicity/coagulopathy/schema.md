# Schema — OligoTox-Coagulopathy

Four normalised UTF-8 CSV tables with a header row.

```
sources.csv  ──<  oligos.csv  ──<  measurements.csv
                       └────────<  modifications.csv   (one row per nucleotide position)
```

**Missing values.** `NOT_REPORTED` = the source does not report this. It has not been
estimated, imputed, or filled from background knowledge. `NOT_APPLICABLE` = the field has
no meaning for this row (a dose for an in-vitro spike-in; a 5′→3′ base string for a
polydisperse mixture or a duplex). Cells are never blank, never zero-as-missing, and the
`TBD` sentinel used by the sibling kidney dataset does not appear here — a QC check
enforces that.

**Booleans** are `TRUE`/`FALSE`.

---

## `data/sources.csv` — the provenance registry

One row per source document. 75 rows.

| Column | Description |
|---|---|
| `source_id` | Primary key, `COG-Snnn`. |
| `citation` | Full citation as the document states it. |
| `identifier` | PMCID / PMID / DOI / US patent number / DailyMed set id. |
| `document_file` | File in `sources/documents/`. The row's evidence is re-readable from the repository. |
| `retrieval_route` | How it was obtained (Europe PMC REST, DailyMed API, USPTO PDF endpoint, …). |
| `licence` | Licence as stated by the source. |
| `redistribution` | `public_domain` \| `CC_BY` \| `CC_BY_NC` \| `CC_BY_NC_ND` \| `publisher_restricted` \| `unresolved`. |
| `extraction_bundle` | Which extraction bundle read this source — audit trail, not data. |
| `n_oligos`, `n_measurements` | Roll-ups, recomputed by the build and checked by QC. |

## `data/oligos.csv` — one row per compound

213 rows. Identity and the design predictors a model would use as input features.

| Column | Description |
|---|---|
| `oligo_id` | Primary key, `COG-OLGnnn`. |
| `oligo_name`, `aliases` | Name and `;`-separated alternates, accumulated when one compound appears in several sources. |
| `oligo_class` | `ASO_gapmer` \| `ASO_mixmer` \| `splice_switching_ASO` \| `siRNA` \| `GalNAc_siRNA` \| `aptamer` \| `PMO` \| `tcDNA_ASO` \| `CpG_ODN` \| `polydisperse_ssDNA` \| `other`. |
| `modality` | `single_stranded_ASO` \| `double_stranded_siRNA` \| `aptamer` \| `mixture` \| `other`. |
| `target_gene`, `indication`, `developer`, `max_phase` | Development context. |
| `length_nt` | Length **as the source declares it**, or `NOT_REPORTED`. Always a plain integer — qualifying prose is moved to `sequence_note`. |
| `length_nt_from_sequence` | Length **computed** from `sequence_base`. Held separately so a declared length can be checked against the string rather than trusted. |
| `sequence_5to3_asprinted` | The sequence exactly as the source prints it, preserving any case convention that encodes chemistry. |
| `sequence_base` | Nucleobases only, upper case, chemistry stripped — `[ACGTU]+`, enforced by QC. `NOT_APPLICABLE` for duplexes and polydisperse mixtures, which have no single 5′→3′ string. |
| `sequence_note` | Anything the source said about the sequence or length that is not itself sequence (a 3′ cap, strand layout, a qualification). Kept verbatim so nothing is discarded. |
| `terminal_modification` | A terminal residue with no position in a 5′→3′ base string — e.g. a 3′-inverted dT cap. Held at oligo level precisely because it cannot own a position row. |
| `sequence_locus` | Where in the document the sequence is printed. |
| `backbone_chemistry` | `full_PS` \| `mixed_PO_PS` \| `full_PO` \| `PMO_neutral` \| `other` \| `NOT_REPORTED`. |
| `sugar_modifications`, `gapmer_design`, `conjugate`, `ps_count` | Design predictors. |
| `purity_pct`, `purity_method`, `identity_confirmation`, `synthesis_platform` | The Challenge's oligo-characterisation requirement, recorded as each source states it. `purity_pct` is `NOT_REPORTED` for every compound — see METHODOLOGY §3. |
| `source_ids` | `;`-separated sources that describe this compound. |
| `n_measurements`, `notes` | Roll-up and free text. |

## `data/modifications.csv` — per-position chemistry

941 rows over 47 oligos: **one row per nucleotide position, 5′→3′**, for every compound
whose source publishes position-resolved chemistry. This is the table that answers the
Challenge's requirement for "the location of all chemical modifications in each oligo".

| Column | Description |
|---|---|
| `oligo_id` + `position` | Composite primary key. Positions are contiguous from 1 (QC-enforced). |
| `nucleobase` | `A` \| `C` \| `G` \| `T` \| `U`. Must equal `sequence_base` at that position (QC-enforced). |
| `sugar_mod` | `DNA` \| `RNA` \| `LNA` \| `2'-MOE` \| `2'-OMe` \| `2'-F` \| `cEt` \| `morpholino` \| `tcDNA` \| `NOT_REPORTED`. |
| `backbone_linkage_3p` | The linkage 3′ of this position: `PS` \| `PO` \| `PN` \| `NOT_APPLICABLE` (3′ terminus) \| `NOT_REPORTED`. |
| `is_5_methyl_C` | `TRUE` only where the source states it. `FALSE` means *not stated*, not an affirmative denial. |
| `basis` | **How the chemistry at this position was determined** — e.g. the source's own case legend, quoted. Every row carries one; per-position chemistry is never modelled or inferred. |

## `data/measurements.csv` — one row per measured outcome

2,388 rows. Grain: oligo × system × delivery × dose × timepoint × readout.

| Column | Description |
|---|---|
| `measurement_id` | Primary key, `COG-MSRnnnn`. |
| `oligo_id`, `source_id` | Foreign keys. |
| `study_type` | `in_vitro` \| `ex_vivo_human_plasma` \| `animal_invivo` \| `clinical`. |
| `species` | `human` \| `monkey` \| `minipig` \| `pig` \| `rat` \| `mouse` \| `dog` \| `rabbit` \| `sheep` \| `cow` \| `guinea_pig` \| `NOT_APPLICABLE` (purified system). |
| `system_model`, `matrix` | Model/subject, and `plasma` \| `whole_blood` \| `serum` \| `in_vivo` \| `purified_system`. |
| `delivery_method`, `dose_value`, `dose_unit`, `timepoint`, `exposure_duration`, `n_subjects` | Exposure. `n_subjects` matters: several clinical rows are badly underpowered and that must be visible. |
| `readout_category` | `clotting_time` \| `factor_activity` \| `fibrinogen` \| `thrombin_generation` \| `fibrinolysis_marker` \| `anticoagulant_activity` \| `bleeding_outcome` \| `thrombotic_outcome` \| `platelet_coag_crosstalk`. |
| `readout_name` | e.g. `aPTT`, `PT`, `INR`, `TT`, `ACT`, `fibrinogen`, `D_dimer`, `anti_Xa`, `anti_IIa`, `FXI_activity`, `antithrombin_activity`, `peak_thrombin`, `bleeding_event`, `thrombotic_event`. |
| `readout_value` | The value **exactly as printed**, including any `±` or range. Not reformatted; downstream parsing takes the leading number. |
| `readout_unit`, `readout_is_qualitative` | Unit, and whether the row carries no number at all. |
| `control_value`, `control_description` | The matched control and what it was. |
| `effect_direction` | `increase` \| `decrease` \| `no_change` \| `NOT_REPORTED`. **`no_change` means a measured null** — the endpoint was assessed and was unremarkable. It is never used for an endpoint that was simply not mentioned; that case is `NOT_REPORTED` with the reason in `notes`. |
| `effect_vs_control` | The effect size as the source expresses it. |
| `ratio_to_control` | Control-referenced ratio, computed by the build. `NOT_REPORTED` when none is derivable. |
| `ratio_basis` | **How** the ratio was obtained, or why it could not be: `value_over_matched_control`, `value_is_already_control_referenced`, `no_matched_control_value`, `value_is_censored`, `qualitative_row`, `no_numeric_value`. |
| `coag_tox_grade` | Ordinal `0`–`3`, or `NOT_REPORTED`. Rubric below. |
| `grade_basis` | The exact rule applied — or, for an ungraded row, why no rule applies. Never empty. |
| `grade_status` | `provisional` on every row. No grade has had subject-matter review. |
| `severity_stated_by_source` | Severity **in the source's own words**, verbatim. Where a source contradicts its own tables, this is where the contradiction is preserved. |
| `on_target_effect`, `unintended_toxicity` | The two axes. Both may be `TRUE`. See README. |
| `source_locus` | Exact locus — table number, figure panel, section heading, label section, PDF page. |
| `redistribution` | Inherited from the source. |
| `verbatim_quote` | Text copied from the document that supports this row. Present on all 2,388 rows (QC-enforced). |
| `notes` | Free text, including method limitations and reporting-silence flags. |

---

## `coag_tox_grade` rubric (0–3)

Grades use the **CTCAE v5.0** (NCI, 27 November 2017) laboratory criteria. The thresholds
are the published ones; none was devised for this dataset.

| Grade | Prolongation readouts (aPTT, PT, INR, TT, ACT) | Fibrinogen |
|---|---|---|
| **0** | ratio ≤ 1.0 × control | ratio ≥ 1.0 × control |
| **1** | > 1.0 – 1.5 × | < 1.0 – 0.75 × |
| **2** | > 1.5 – 2.5 × | < 0.75 – 0.5 × |
| **3** | > 2.5 × | < 0.5 × |

**A deviation, stated plainly.** CTCAE defines these ratios against the upper (or lower)
limit of normal. This dataset applies them to a ratio against the **matched experimental
control**, because that is what the sources publish — few report a laboratory reference
range. The rule name recorded in every `grade_basis` is therefore
`CTCAE_v5.0_control_referenced`, so the substitution is visible on every graded row rather
than buried in documentation. Where a source reports a measured null on a CTCAE-graded
readout without a derivable ratio, the grade is `0` with basis
`source_states_measured_no_change_on_a_CTCAE_graded_readout`.

**What is deliberately not graded.** CTCAE defines no criterion for factor activity,
antithrombin activity, thrombin generation, bleeding volume, thrombus fluorescence or
clinical event counts. Those 1,446 rows are `NOT_REPORTED` with the reason in
`grade_basis` — grading them would mean inventing thresholds and presenting them with the
authority of a published standard.

**Reproducibility.** Grades are a pure function of `ratio_to_control` and `readout_name`.
`validate_dataset.py` re-derives every one of the 942 graded rows and fails if any
disagrees, so a hand-edited grade cannot survive a build.

---

## QC log

**2026-08-29 — build v1.0.** 36 structural checks pass; `validate_dataset.py` exits
non-zero on any failure. Coverage: primary keys, all three foreign keys, controlled
vocabularies on five columns, boolean domains, grade range, the requirement that every
graded row names its rule *and* every ungraded row names its reason, provenance
(`verbatim_quote` and `source_locus` on every row), the no-blank/no-`TBD` invariants,
sequence purity, declared-versus-computed length, contiguity of modification positions
from 1, agreement between each modification's nucleobase and the sequence at that
position, reproducibility of every grade from its ratio, and agreement of both roll-up
counts with the rows.

Three defects were found by these checks during the build and fixed at source rather than
by relaxing the check:

1. **Prose in sequence cells.** Four `sequence_base` cells carried trailing prose
   (`"GUGGACUAUACCGCGUAAUGCUGCCUCCAC + 3' inverted dT (case-normalised …)"`). The build now
   splits a sequence cell into the leading nucleotide run plus a `sequence_note`.
2. **Spurious compound merges.** Because those contaminated cells were used as the
   deduplication key, 12 distinct compounds had been merged into others. Cleaning the key
   split them back out: 213 compounds, with zero duplicate names and zero duplicate
   sequences remaining.
3. **A terminal cap holding a position row.** A 3′-inverted-dT occupied position 31 of a
   30-base aptamer, breaking the position↔base check. Terminal residues are now lifted to
   `oligos.terminal_modification`, and the length check accounts for them explicitly.

**Source verification.** `verify_against_sources.py` re-reads all 74 committed documents
and confirms every numeric readout appears in the document its row cites:
**1,862 / 1,862 located**. 467 qualitative rows and 45 non-numeric values are out of
scope; 14 rows cite a supplementary PDF not held locally and are reported as skipped
rather than passed. This check itself was wrong on first run — it stripped `<…>` "tags"
from plain-text patent files, deleting whole tables and reporting 120 false fabrications.
Markup is now stripped only from markup files, and the episode is recorded here because
the failure mode (a verifier that silently damages its own evidence) is worth knowing.
