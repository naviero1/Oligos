# Working inputs — 2026-10-02/03 research round

**Status: verified working inputs, NOT a dataset and NOT a published report.** Nothing here is a
measurement table, a scientific label, an adjudication or a model-eligible record. These files are
committed only so that verified work survives a container restart — one already destroyed an
in-flight search round on 2026-10-02. They will be folded into
`../../ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md` and may be superseded by it.

| File | What it is | Provenance |
|---|---|---|
| `REGISTER_regulatory_draft.md` | Clinical study register for the four regulatory programmes (drisapersen, inotersen, mipomersen, volanesorsen), with study rosters, verbatim complement passages and denominators | Extracted first-hand from EMA assessment reports parsed locally with `pdftotext -layout` |
| `regulatory_study_identifiers.json` | Machine-readable roster of every study/protocol code and NCT number found in each of the four EMA reports | Same extraction; regex over full text |
| `search_log_pubmed_europepmc.json` | Completed search-coverage logs for PubMed (19 queries) and Europe PMC (32 queries), with per-result classification | Recovered from the journal of the workflow killed by the 2026-10-02 container restart |
| `sewing_extraction_grain_reference.csv` | The 144 candidate rows the Sewing 2017 complement block would yield, as analyte x condition x donor | Parsed from the committed CC-BY file in `../sources/` |

## Two findings these files carry that correct the 2026-10-01 reply

1. **Zero NCT numbers in any of the four EMA reports.** The regulatory record holds the only chronic
   human complement data in the field and identifies every study by sponsor protocol code only.
   Registry cross-linking is a separate, unperformed step.
2. **The GalNAc-conjugated-era negative was overstated.** PubMed/Europe PMC surfaced
   PMID 30570431 / PMC6386089, an integrated clinical assessment of GalNAc3-conjugated 2'-MOE ASOs
   in healthy volunteers recorded as measuring **Bb and C5a**. The reply asserted that generation has
   no human complement measurement, generalising beyond the EMA documents actually checked. Under
   verification; the correction is already conceded.

`sewing_extraction_grain_reference.csv` is a reference parse establishing the grain and denominators.
It is **not** an ingestion: 6 of its 144 rows are PBS normalisers fixed at 1.0, the values are a
derived Stimulation Index rather than absolute concentrations, and no construct identity has been
attached yet because the spreadsheet labels conditions without naming the oligonucleotides.
