# CHANGES — OligoTox-CNS

## v1.0 — 2026-08-26 — initial release

The CNS module of the NCATS oligonucleotide toxicity Phase 2 submission, built from nothing: no
CNS source material was supplied at intake (see `PROJECT_STATE.md`).

### Dataset

| file | rows × cols | what it is |
|---|---|---|
| `data/oligos.csv` | 1,839 × 45 | one row per oligonucleotide — the predictors |
| `data/measurements.csv` | 2,065 × 36 | one row per CNS toxicity outcome — the response |
| `data/modifications.csv` | 32,569 × 8 | one row per nucleotide position — the per-position chemistry |
| `data/sources.csv` | 5 × 18 | provenance registry |

Sources: **H1** Hagedorn 2022 (CC BY, 1,825 oligos / 2,006 measurements), **K1** Miller 2024
(CC BY-NC, 7 / 41), **L1** Kuroda 2025 (CC BY-NC, 5 / 6), **C1** FDA prescribing information
(public domain, 2 / 12), **O1** O'Rourke 2026 (instruments only, 0 rows).

### Pipeline

`src/build_hagedorn.py` → `src/build_curated.py` → `src/assemble.py` →
`qc/validate_dataset.py` → `src/make_figures.py` → `src/make_release.py` → `src/make_pdfs.py`,
plus `src/baseline_model.py` and `qc/verify_nephro_intake.py`.

### Deliverables

- `deliverables/OligoTox-CNS_Narrative.pdf` — 8 pages (limit 12)
- `deliverables/OligoTox-CNS_Methodology.pdf` — 3 pages (limit 5)
- `deliverables/OligoTox-CNS_Dataset.xlsx` — 7 sheets incl. a live-formula summary
- `docs/{SCHEMA,DATA_DICTIONARY,SCORING_INSTRUMENTS,PADP}.md`, `LICENSE.md`, `README.md`
- `figures/` — 8 figures, all regenerated from `data/`

---

## Errors caught and fixed during the build

Recorded because each was caught by **looking at the rendered output**, not by reading the code
that produced it. Every one would have shipped as a plausible-looking wrong number.

| # | What was wrong | How it was caught | Fix |
|---|---|---|---|
| 1 | The assay-reproducibility figure grouped "replicates" on `sequence_base`, merging oligonucleotides that share a nucleobase sequence but carry LNA at *different positions* — different molecules. Gave a spurious n = 25, CV 30.5 %. | Rendering the figure and noticing the replicate count disagreed with the earlier hand check | Group on `sequence_5to3_asprinted`, whose case encodes LNA position → true set: n = 14, CV 17.3 % |
| 2 | The dose-response and cation-rescue curves selected rows by dose and cation alone, pulling control groups from unrelated source figure panels onto the same curve — four different scores at x = 0 | Rendering the figure and seeing four points stacked at 0 mM | Select rows by the source figure panel each group belongs to |
| 3 | The "across all" AUCs were computed over the 157 feature-complete rows, but the narrative attributed them to 181 | Re-reading the PDF against the model script's own output | Sequence-only comparisons now use all 181; only the fitted regression is restricted, and the caption says so |
| 4 | The methodology claimed length and base composition were checked for "1,839 of 1,839" — but 9 oligonucleotides have no published sequence to check against | Reading the rendered methodology page | Now states 1,830 of 1,830, and names the 9 |
| 5 | "1,825 … LNA/DNA full-phosphorothioate **gapmers**" — the 1,825-compound core is 1,726 gapmers plus 99 mixmers | Cross-checking the narrative against the `gapmer_shape` counts | Reworded to "oligonucleotides — 1,726 conventional gapmers and 99 mixmers" |
| 6 | The predictor sentence quoted 1,732 gapmers while Figure 5 plots 1,731 gap lengths (tofersen is class-assigned as a gapmer but its gap length is unreported) | Comparing the sentence to the figure beside it | Quote the count the figure actually plots |
| 7 | `Mg²⁺` / `Ca²⁺` rendered as missing-glyph boxes; a stray page break left a methodology page almost empty; a figure annotation overlapped the n/median block; a completeness bar rounded 99.5 % up to 100 % | Reading the rendered pages | Superscript tags, page break removed, annotation moved with a leader line, one decimal place |
| 8 | The workbook's Summary sheet used whole-column `COUNTIF`, which LibreOffice could not recalculate within nine minutes across a 32,569-row sheet | Two recalculation timeouts | Bounded ranges sized to the data. Headless LibreOffice on this 4-CPU machine still could not finish, so instead **every one of the 15 formulas was independently evaluated against the CSVs and matches `qc/validate_dataset.py` exactly**; the workbook's README sheet says the Summary computes on open and points programmatic users at the CSVs |

## Deliberate decisions worth recording

- **Supplementary files are fetched through Europe PMC, not PubMed Central.** PMC gates binary
  downloads behind a JavaScript proof-of-work challenge that returns an HTML stub *with HTTP 200*
  in place of the requested file. A stub like that would have been parsed as data. Detected by
  checking the file type of the download rather than trusting the status code.
- **No value passed through a summarising fetch layer.** During source discovery, one such
  summary returned a nucleotide sequence containing a Cyrillic character. All sequences are read
  cell-by-cell or by parsing PDF span styling.
- **The 1,825 in vitro readings are deliberately left ungraded.** Grading a continuous readout
  for which the source defines no severity bands would mean inventing thresholds.
- **The 0–3 grade uses the source authors' own cut-offs (4, 7, 18)**, which reproduces their
  stated "roughly 60 % suitable for further development" at 61.9 %. The mapping was not tuned to
  hit that number.
- **A richer model that lost to the published one is reported anyway** — it is a useful negative
  result about where the constraint actually lies.
