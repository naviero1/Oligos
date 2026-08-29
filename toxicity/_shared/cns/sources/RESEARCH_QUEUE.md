# Source register and research queue — OligoTox-CNS

Two kinds of material live under `sources/`:

1. **Ingested** — read by the v1.0 build pipeline. Every row in `data/` traces to one of these.
2. **Gathered, not yet ingested** — retrieved during research and held for v1.1. **No v1.0 row
   depends on any of it**, so nothing in the released dataset changes if these are removed.

## Ingested in v1.0

| ID | Source | Licence | In repo | Contributes |
|---|---|---|---|---|
| **H1** | Hagedorn 2022, *Nucleic Acid Ther* 32(3):151–162 — mouse ICV acute tolerability + rat neuron calcium assay | **CC BY 4.0** | yes | 1,825 oligos / 2,006 measurements — the core |
| **K1** | Miller 2024, *Mol Ther Nucleic Acids* — divalent-cation formulation rescue | CC BY-NC | yes | 7 / 41 |
| **L1** | Kuroda 2025, *Mol Ther Nucleic Acids* — late-onset neurotoxicity, 5′-CP | CC BY-NC | yes | 5 / 6 |
| **C1** | FDA prescribing information (tofersen, nusinersen) via DailyMed | public domain | fetched live | 2 / 12 |
| **O1** | O'Rourke 2026, *Nucleic Acids Res* 54(3):gkaf1333 — acute *inhibition* scales | CC BY-NC | yes | instruments only, 0 rows |

## Gathered for v1.1 — not ingested

| ID | Source | Licence | In repo | What it would add |
|---|---|---|---|---|
| **B1** | Bravo-Hernandez 2026, *Nucleic Acids Res* 54(3):gkag057 — transient acute neuronal *activation* response, rat/mouse/NHP | CC BY-NC | yes | Would upgrade `docs/SCORING_INSTRUMENTS.md` §4 from *[fetch summary]* to *[read directly]*, and add the first **non-human-primate** rows |
| **P1** | US 10,799,523 B2 (Olson et al.) — CNS oligonucleotide patent | **public domain** (US patent) | yes | Patent tables pair sequence with toxicity rating; the format that supplied 21 rows to the sibling kidney module |
| **S1** | Schobel 2021, CHDI — *Preliminary results from GENERATION HD1* | © Roche, conference deck | **no — see below** | Tominersen ventricular-volume and NfL detail behind the clinical failure |
| **B2** | Boak & McColgan 2022, CHDI — *Treatment and post-treatment effects of tominersen in GENERATION HD1* | © Roche, conference deck | **no — see below** | Post-treatment follow-up on the same trial |
| **M1** | McColgan 2023, *N Engl J Med* 389(23) Correspondence — *Tominersen in Adults with Manifest Huntington's Disease* | © NEJM | **no — see below** | The peer-reviewed statement of the GENERATION HD1 outcome |

## Why three sources are on disk but not in git

S1, B2 and M1 are **copyrighted publisher material that is not licensed for redistribution** — a
Roche conference deck twice over, and an NEJM correspondence item. Committing them would
republish them, which is a different act from reading them for research.

They are therefore listed in `.gitignore`. They remain on the working disk, and the table above
records exactly what they are so anyone can retrieve their own copy. This is the same
per-source-terms discipline `LICENSE.md` applies at row level.

**This was a judgement call, not an instruction — say the word and they can be committed.**

Everything else under `sources/` is CC BY, CC BY-NC or US public domain and is committed, so the
v1.0 pipeline rebuilds from the repo alone.
