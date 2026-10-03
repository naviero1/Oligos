# Faithful CSV reduction of the immunotoxicity adjudication workbook

Produced 2026-10-03 for `CRANK_DELEGATION_2026-10-03.md` → Immunotoxicity, item 1:
*"Commit the Drive workbook, or a faithful CSV reduction, so every figure becomes auditable in one place."*

## Source

| | |
|---|---|
| Drive file | `GOG_OligoTox_Immunotoxicity_Evidence_Library_v0.2_Scientist_Adjudication.xlsm` |
| Drive file id | `13gq7Weyd21hR9DoZ68ise_RbbQL7bAST` |
| Drive modified | 2026-08-28T23:40:05Z |
| Bytes | 152409 |
| **sha256 of the .xlsm** | `381dcfdf4a15359392bd04013fb30414e4c5c0e10a962fb5b40b8b699938f6bd` |
| Reduction method | `openpyxl` `data_only=True`; one CSV per sheet; cell values written verbatim; only fully-empty trailing rows and columns trimmed |
| Macros | none present despite the `.xlsm` extension (no `vbaProject.bin`) |

This is a **reduction, not a reinterpretation**: no cell value was altered, merged, normalised, relabelled or dropped. Formulae are captured as their cached computed values, which is what `data_only=True` returns; the workbook's own figures are therefore reproducible from these files by counting rows.

The binary `.xlsm` itself is **not** committed — it is German's Drive artifact. Its checksum is recorded above so any future copy can be proven identical to the one these CSVs came from, which is the precondition `SCIENTIFIC_RULES.md` §A sets for transfer ("a verified local structured source exists with a recorded checksum").

## Sheets

| Sheet | Rows incl. header | Cols | Bytes | sha256 |
|---|---:|---:|---:|---|
| `Dashboard.csv` | 39 | 5 | 1993 | `2417d12b0cb46573960ef7dcc17aab51dcd443ac7202f3f4f2354ec1a0e55965` |
| `README.csv` | 15 | 2 | 1901 | `869885c76b866960b89cee30b10b3808d870fa13013e09bdca07b3d60faca99a` |
| `Paper_Registry.csv` | 21 | 20 | 14160 | `1a9728413d39e1739c00fa94f578f882ed775bc2035f360dd6508013930d8d5f` |
| `Oligo_Sequence_Catalog.csv` | 143 | 25 | 73580 | `7f96d859ba9b2dbb696cfa87d50aef591830d9a506e49a2ac4d6c51d590255e3` |
| `Evidence_Observations.csv` | 34 | 13 | 14561 | `21cb05f699b867cb72d159e28291c85fbb4515ea9122e50392078f476a9e3bb5` |
| `ML_Corrections.csv` | 19 | 7 | 8205 | `41e0ec9f6904cd09b69d9dfc4e7bd54b671773b57c9873cfa8335d09d6e58096` |
| `Schema_Recommendations.csv` | 46 | 5 | 4134 | `81e65d7c7924e22933b71669abb08f6765c15705d7c40e3108f7670363a79fb8` |
| `Citation_QC.csv` | 8 | 5 | 1495 | `0077e56490d4b3d5de21cc5a9f03486f48af1a9f9caff88bdf2c7689741274b1` |
| `Conflicts_Unresolved.csv` | 6 | 6 | 1538 | `528cfd371f0f48c158dd3959315ac635e30a828cf71a1b872c0fd37caf4b2535` |
| `Adjudication_Dashboard.csv` | 28 | 3 | 2046 | `a88a370fe18788427bb21433fb209f907200e29750df676eec99932a6cfab466` |
| `Scientist_Adjudication.csv` | 143 | 20 | 81724 | `47a7a244f97bbca0cfe894e49ea1fb902619fdcb3981ceb2f43fef434e43846a` |
| `Training_Candidates.csv` | 55 | 13 | 21659 | `c31677cc9f18a2cdec5ec81cb165643fc98378474a5b3e28fe147898924353f5` |
| `Hold_Queue.csv` | 49 | 13 | 24326 | `c5cd44e183180c39e966e72428334a46ffc7eb892accc5ce595e4af59c1df910` |
| `Support_Only.csv` | 41 | 13 | 14960 | `17e5b602c6e5610c107d78599572ec3d87e312fa74962b936f5199584f3d44f6` |
| `Signoff_Gates.csv` | 13 | 5 | 2756 | `19ed437882b44708a049d6fde0aab9c0b3b7c9143e530b18ac601eae17470839` |

## The figures these files make auditable

| Figure | Value | Where to count it |
|---|---:|---|
| Registered papers | 20 | `Paper_Registry.csv`, data rows |
| Sequence catalog records | 142 | `Oligo_Sequence_Catalog.csv`, data rows |
| Distinct canonical oligo identifiers | 141 | `Oligo_Sequence_Catalog.csv`, distinct `Canonical Oligo ID` |
| Narrative observations | 33 | `Evidence_Observations.csv`, data rows |
| Provisionally approved | 54 | `Scientist_Adjudication.csv`, `Scientist Sign-off` = `PROVISIONALLY APPROVED` |
| Hold | 48 | same column = `HOLD` |
| Support only | 40 | same column = `SUPPORT ONLY` |
| Legacy training-ready flags | 84 YES / 58 NO | `Oligo_Sequence_Catalog.csv`, `Training Ready?` |
| Position-specific chemistry populated | 41 of 142 | `Oligo_Sequence_Catalog.csv`, `Modification Positions` non-empty |
| Purity / identity-method / endotoxin / supplier columns | **0 columns exist** | absent from every sheet; proposed only in `Schema_Recommendations.csv` |
| Standalone number `64` | **0 cells** | absent from all 15 sheets |
