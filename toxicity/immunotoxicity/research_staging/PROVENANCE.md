# Research staging — provenance

Acquired 2026-10-03 under the 2026-10-02 research round (proposals 3, 4, 5).
Retrieval route for every item: Europe PMC REST `supplementaryFiles` endpoint for the article's
PMCID. No purchase, subscription, credential or author contact was used.

## What is committed here, and what is not

Committed: **derived sequence tables only** — factual sequence/chemistry data extracted from
open-access supplements, with attribution below. Publisher-formatted originals (PDF/XLS/XLSX
bundles) are held in local session staging and are **not committed**, to avoid redistributing
publisher files.

| Derived file | Rows | sha256 | Derived from | Licence / access |
|---|---:|---|---|---|
| `goodchild2009_S1_sequences.csv` | 267 | `6bb96607aded1dee66e0b299f9ad697fe8cc72bf65ae71a344eaf09e6825bfad` | `1471-2172-10-40-S1.xls` (68,608 bytes) from PMC2724479 | BMC Immunology, open access |
| `valentin2021_S1_S2_sequences.csv` | 127 | `f52e73a4330c567a6524ab4d558f8a52d61e4a49f755d9690a5d770e0d51065b` | `gkab451_supplemental_file.pdf` (8,127,839 bytes) from PMC8216285 | Nucleic Acids Research, open access |

## Source attribution

- **Goodchild A, Nopper N, King A, Doan T, Tanudji M, Arndt GM, Poidinger M, Rivory LP, Passioura T.**
  Sequence determinants of innate immune activation by short interfering RNAs.
  *BMC Immunology* 2009. DOI 10.1186/1471-2172-10-40, PMID 19630977, PMCID PMC2724479.
- **Valentin R, Wong C, Alharbi AS, Pradeloux S, Morros MP, Lennox KA, Ellyard JI, Garcin AJ, et al.**
  Sequence-dependent inhibition of cGAS and TLR9 DNA sensing by 2'-O-methyl gapmer oligonucleotides.
  *Nucleic Acids Research* 2021. DOI 10.1093/nar/gkab451, PMID 34057477, PMCID PMC8216285.

## Column semantics

`goodchild2009_S1_sequences.csv` — `oligo_id`, `guide_5to3`, `passenger_5to3`. Transcribed verbatim
from the supplement; no chemistry is encoded in the source and none was inferred. 246 rows carry a
valid guide strand and 243 a valid passenger. The source holds 259 distinct identifiers, a
**superset** of the 207-siRNA screen reported in the article; the mapping to the screened 207 is
**not established** by this file.

`valentin2021_S1_S2_sequences.csv` — `name`, `notation` (verbatim), `bases_5to3`, `length_nt`,
`twoOMe_positions`, `PS_linkage_after_positions`. Decomposed mechanically from the published
notation documented in the source caption: uppercase alone = DNA, `m` prefix = 2'-O-methyl base,
`*` = phosphorothioate linkage. 115 of 127 rows yield per-position 2'OMe maps; 123 yield PS maps.
Table S2 contributes exactly 80 screen ASOs.

## Not acquired

Burel 2022 Supplementary Table S1 — no open route found (no PMCID, not open access, no supplement
listed in Europe PMC). See the access request in `ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md` §5.

## Status

Acquisition is not qualification. Nothing here has been ingested, labelled or adjudicated, and no
validated dataset was changed. German's scientific adjudication is required before any of this
becomes evidence.
