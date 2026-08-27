# Extraction contract — OligoTox-CNS

Every extraction agent MUST follow this document exactly. Output is merged
mechanically, so deviations cost a re-run.

## 0. The one rule that overrides all others

**Never fabricate.** Not a sequence, not a dose, not an incidence, not a DOI, not
a PMID, not an NCT number, not a patent number, not a table number.

You may only write a value that you **read out of a document you actually
fetched in this session**. Values recalled from memory are forbidden, including
ones you are confident about. If you cannot fetch the document, write `TBD` and
say so in `extraction_notes`. A dataset with 40 verified rows beats one with 120
rows of which 30 are invented, because the invented ones destroy the credibility
of the other 90.

Corollary: `source_table` must name the **exact locus you read** — "Table 2",
"Section 5.1", "Figure 3B", "Claim 7", "adverse reactions table, row 4". Writing
"Table 2" when you actually read the abstract is a fabrication.

## 1. What we are building

A per-measurement dataset of **CNS toxicity of therapeutic oligonucleotides**
for the NIH/NCATS OligoTox Open Data Challenge, Phase 2.

The challenge brief names **chronic neurotoxicity** and **hydrocephalus** as
toxicities of interest, and explicitly *deprioritizes* acute neurotoxicity work
focused on **alterations of neuronal electrical activity** (MEA and similar).
So: chronic neurotoxicity and hydrocephalus rows are the most valuable;
acute-neurotoxicity rows are welcome but must be flagged; MEA/electrophysiology
rows are lowest value and must be flagged `low_acute_electrophysiology`.

NCATS particularly wants **in vitro human-based systems** (iPSC-derived neurons,
microglia, astrocytes, organoids), supplemented by animal in vivo/in vitro data.

## 2. Grain

**One row per `oligo × model/subject × CNS region × delivery × dose × readout`.**

One oligo at one dose measured for NfL *and* for ventricular volume is **two
rows**. One oligo measured at three doses is **three rows** per readout. Split
aggressively — that is where the record volume legitimately comes from. Do not
manufacture volume by splitting a single reported number into fake sub-rows.

## 3. Output format

Return JSON with exactly two arrays, `oligos` and `measurements`, plus
`extraction_notes`.

Use **placeholder oligo ids** of the form `TMP_<yourlane>_<n>` (e.g.
`TMP_reg_1`). The assembler renumbers to `CNS###`. Every measurement's
`oligo_id` must match one of the `oligos` you return in the same response.

### `oligos[]` — 17 fields, all required (use `TBD` / `NA`, never blank)

`oligo_id`, `oligo_name`, `aliases`, `oligo_class`, `target_gene`, `indication`,
`developer`, `max_phase`, `length_nt`, `backbone_chemistry`,
`sugar_modifications`, `gapmer_design`, `conjugate`, `ps_count`,
`sequence_5to3`, `design_source`, `notes`

- `oligo_class` ∈ `ASO_gapmer` | `siRNA` | `GalNAc_siRNA` | `splice_switching_ASO` | `PMO` | `aptamer` | `other`
- `max_phase` ∈ `approved` | `approved_EMA` | `phase_3` | `phase_3_discontinued` | `phase_2` | `phase_2_discontinued` | `phase_1` | `phase_1_discontinued` | `preclinical` | `research_panel` | `named_patient` | `class_review`
- `backbone_chemistry` ∈ `full_PS` | `PS_PO_mix` | `full_PO` | `PMO_neutral` | `mixed` | `TBD`
- `conjugate` ∈ `none` | `GalNAc` | `lipid` | `peptide` | `PEG` | `divalent` | `other` | `TBD`
- `gapmer_design`: e.g. `5-10-5_MOE`, `3-10-3_cEt`; `NA` for uniformly modified SSOs, siRNA, PMO
- `sequence_5to3`: **`TBD` unless you read the actual string in a fetched
  document.** Case is meaningful (uppercase = modified wing, lowercase = DNA
  gap) — preserve the case the source printed. For duplexes store the
  guide/antisense strand and put the sense strand in `notes`.

### `measurements[]` — 26 fields, all required

`measurement_id` (use `TMP_<lane>_m<n>`), `oligo_id`, `study_type`, `species`,
`system_model`, `cns_region`, `delivery_method`, `dose_or_conc_value`,
`dose_or_conc_unit`, `exposure_duration`, `endpoint_domain`,
`challenge_priority`, `readout_category`, `readout_name`, `readout_value`,
`readout_unit`, `effect_direction`, `effect_vs_control`, `neurotox_grade`,
`reversibility`, `is_cns_specific`, `source_id`, `source_ref`, `source_table`,
`redistribution`, `notes`

Controlled vocabularies:

- `study_type` ∈ `in_vitro` | `animal_invivo` | `clinical`
- `species` ∈ `human` | `monkey` | `rat` | `mouse` | `multi_species` | `NA`
- `cns_region` ∈ `whole_brain` | `cortex` | `hippocampus` | `cerebellum` | `brainstem` | `striatum` | `spinal_cord` | `DRG` | `ventricle` | `CSF` | `meninges` | `optic_nerve` | `peripheral_nerve` | `systemic` | `NA`
- `delivery_method` ∈ `intrathecal` | `intracerebroventricular` | `intracisternal` | `intraparenchymal` | `intravitreal` | `systemic_dose` | `gymnotic_free_uptake` | `transfection` | `lipofection` | `TBD`
- `dose_or_conc_unit` ∈ `uM` | `nM` | `ug/mL` | `mg/kg` | `mg` | `ug` | `fold_Cmax` | `NA` | `TBD`
- `endpoint_domain` ∈ `chronic_neurotoxicity` | `hydrocephalus` | `acute_neurotoxicity` | `neuroinflammation` | `neurodegeneration` | `neurobehavioral` | `cytotoxicity` | `csf_biomarker` | `clinical_neuro_ae`
- `challenge_priority` ∈ `high_chronic_neurotox` | `high_hydrocephalus` | `medium` | `low_acute_electrophysiology`
  - use `high_hydrocephalus` for every hydrocephalus/ventriculomegaly/ICP row
  - use `low_acute_electrophysiology` **if and only if** `readout_category = electrophysiology`
- `readout_category` ∈ `functional` | `injury_biomarker` | `viability` | `accumulation` | `histopathology` | `imaging` | `behavioral` | `clinical_neuro_outcome` | `electrophysiology` | `transcriptomic`
- `effect_direction` ∈ `increase` | `decrease` | `no_change` | `TBD`
- `reversibility` ∈ `reversible` | `partially_reversible` | `irreversible` | `not_assessed` | `TBD`
- `is_cns_specific` ∈ `TRUE` | `FALSE` (`FALSE` = a non-CNS comparator row, e.g. a systemically dosed oligo with no CNS exposure kept as a negative control)
- `redistribution` ∈ `public_domain` (US patents, FDA/EMA documents) | `summary_stat` (numbers quoted from a journal article) | `derived_features_only` | `verify`

## 4. Grading — `neurotox_grade` 0–3

| Grade | Definition |
|---|---|
| 0 | No CNS signal at the tested exposure — no behavioural, biomarker, imaging or histopathologic change; incidence at or below concurrent control. **Record these. Negative controls are as valuable as positives.** |
| 1 | Mild / transient, reversible — transient acute behavioural signs resolving in hours–days, isolated mild glial-marker or CSF-protein rise, mild pleocytosis; no neuronal loss, no persisting deficit. |
| 2 | Moderate — sustained neuroinflammation (astrogliosis/microgliosis), treatment-emergent NfL rise, ventriculomegaly without decompensation, or a clinically significant but resolving neurologic AE (aseptic meningitis, radiculitis, myelitis, papilledema). |
| 3 | Severe — neuronal degeneration/loss, spinal-cord or DRG degeneration, paralysis, hydrocephalus requiring intervention, moribundity/death, or dose-limiting / programme-halting neurotoxicity. |

Put `grade_provisional` in `notes` on every row (grades await scientific
sign-off), plus a short rationale when the grade is not obvious.

### Direction is a grading input, not decoration

**NfL is both an efficacy and a toxicity biomarker.** A *fall* in CSF or plasma
NfL after a SOD1- or HTT-lowering ASO is the intended pharmacology — grade **0**,
`effect_direction = decrease`. A *treatment-emergent rise over baseline* is
neuro-axonal injury — grade **2** or worse, `effect_direction = increase`.
Never file an NfL row with `effect_direction = TBD`. The same logic applies to
target-protein reduction: efficacy is not toxicity.

Likewise, an adverse event whose rate is **the same as or below placebo** is a
grade-0 row, not a grade-2 row. Always look for the control arm.

## 5. Sourcing rules

Prefer, in order:
1. **US regulatory documents** (FDA labels via DailyMed, drugs@FDA review PDFs) and
   **US patents** — public domain, values reproducible.
2. **EMA** EPARs, SmPCs, PRAC documents — public domain.
3. **Open-access primary articles** (PMC) — quote numbers as `summary_stat`.
4. **ClinicalTrials.gov posted results** — public domain.

Reviews are for *finding* primary sources and for cross-checking; prefer to cite
the primary source. If you must cite a review for a number, say so in `notes`.

### Fetching tips that work in this environment

- `WebFetch` works for PMC, DailyMed, ClinicalTrials.gov, EMA, Google Patents.
- `www.accessdata.fda.gov` blocks plain `curl` with a bot-detection page. DailyMed
  works from `curl` **if you pass a browser User-Agent**:
  `curl -sSL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" <url>`
- ClinicalTrials.gov has a JSON API:
  `https://clinicaltrials.gov/api/v2/studies/NCT01234567` — the
  `resultsSection.adverseEventsModule` gives per-arm AE counts with denominators,
  which is exactly our grain.
- For PDFs, download then parse with `python3 -c "import pymupdf; ..."` (installed).

## 6. `extraction_notes`

State plainly: which documents you actually fetched; which you tried and failed
to fetch; which numbers you had to leave `TBD` and why; anything you suspect but
could not confirm; and any conflict between two sources. This is how the
assembler knows what to re-check — under-reporting a doubt is worse than
reporting one.
