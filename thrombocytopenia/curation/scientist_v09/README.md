# Scientist-governed package v0.9 — read-only snapshot

These CSVs are a **read-only extract** of sheets from a Google Drive workbook owned
by the project scientist. They are committed so that the reconciliation in
`scripts/reconcile_scientist_v09.py` is reproducible without Drive access.

| | |
|---|---|
| Source file | `GOG_OligoTox_Thrombo_Integrated_Phase2_v0.9.xlsx` |
| Drive file id | `1ysEdbKPbYR_kGnIQOlJNJijFyiyyowfi` |
| Owner | `ogopogo13@gmail.com` |
| Drive `modifiedTime` | `2026-09-06T14:58:21Z` |
| Sheets in source | 85 |
| Sheets extracted here | 32 |
| Extracted | 2026-10-01 |

## The Drive workbook is authoritative, not this copy

If the two ever disagree, the Drive file wins and this snapshot is stale. Nothing in
this repository may overwrite a scientist decision recorded there. Re-extract rather
than edit these files by hand.

## What the reconciliation does with them

- `Oligo_Sequence_Master` — identity and sequence; 4 sequences that were `TBD` in the
  branch dataset were **recovered** from it (see `recoveries.csv`).
- `Position_Chemistry` — 831 per-residue rows (sugar, base modification,
  linkage-to-next, structural segment, terminal). Converted into the dataset's
  `modification_map` column, which was `TBD` for 257 of 259 oligos.
- `Scientist_Adjudication` — dispositions and model-lane eligibility. Ported into
  `oligos.csv` as `scientist_disposition`, `clinical_model_eligibility`,
  `mechanistic_model_eligibility`. A compound with no record here is
  `NOT_ADJUDICATED` and therefore **model-ineligible by default**.
- `Sequence_Family_Groups` — `Exact_Sequence_Group`, `Scaffold_Family`,
  `Publication_Group`, `Matched_Sequence_Pair_ID`: the grouping any train/test split
  must respect. The scientist's labels are propagated to every branch record sharing
  a sequence, so a group cannot fragment.
- `Model_Specification_v0.8` — the lane statuses enforced by `scripts/model_demo.py`.
  "Sequence-only clinical thrombocytopenia classifier" is **BLOCKED**.
- `Negative_Control_Rules` / `Clinical_Negative_Audit` — `CLEAN_CLINICAL_NEGATIVE` is
  *NOT YET AVAILABLE* and all 21 audited candidates are ineligible, so the qualified
  clinical-negative count is **0**.
- `Mechanistic_Contrasts_v0.8` + `Training_Manifest_v0.9` — the matched-sequence
  contrast definitions and adjudicated 0–3 scores used by the approved descriptive lane.

## Outputs written beside them

| File | Contents |
|---|---|
| `crosswalk.csv` | every scientist record → branch `oligo_id`, with the match basis |
| `conflicts.csv` | disagreements left **unresolved** for scientific review |
| `recoveries.csv` | values the branch dataset gained from the scientist package |
