# Research queue — OligoTox-CNS

**The full provenance record is `deliverables/OligoTox-CNS_SourceRegister.pdf`**, which is
generated from the released rows and states, source by source, which database each file came
from, the endpoint that returned it, the table or figure inside it that was read, its licence,
and how many rows it accounts for. It also lists what was retrieved and *not* used, and why.

This file is the working queue that sits behind it: what is ingested, what is next, and what has
been ruled out. It is maintained by hand; where the two disagree, the register is right, because
the register is generated.

## Ingested

| ID | Source | Licence | Contributes |
|---|---|---|---|
| **H1** | Hagedorn 2022, *Nucleic Acid Ther* 32(3):151–162 | CC BY 4.0 | 1,825 oligos / 2,006 measurements — the core |
| **K1** | Miller 2024, *Mol Ther Nucleic Acids* — divalent-cation rescue | **CC BY-NC-ND** | 7 / 41, `summary_stat_only` |
| **L1** | Kuroda 2025, *Mol Ther Nucleic Acids* — late-onset neurotoxicity | **CC BY 4.0** | 5 / 6 |
| **C1** | FDA prescribing information (tofersen, nusinersen) via DailyMed | public domain | 2 / 12 |
| **CT1** | ClinicalTrials.gov posted results, 22 trials | public domain | 6 / 2,329 — the principal human source |
| **HV1** | Buijsen 2024, *Biomedicines* — hiPSC neurons + cerebral organoids | CC BY 4.0 | 3 / 9 |
| **HV2** | Chen 2024, *Nature* — Timothy-syndrome cortical organoids | CC BY 4.0 | 7 / 8 |
| **HV3** | Woffindale 2026, *Mol Ther Nucleic Acids* — SH-SY5Y panel | **CC BY-NC-ND** | 24 / 17, `summary_stat_only` |
| **O1** | O'Rourke 2026, *Nucleic Acids Res* — acute *inhibition* scales | CC BY-NC | instruments only, 0 rows |

K1 and L1 were both recorded under the wrong licence until the source audit; see `FINDINGS.md`
F-13. The `human_invitro` class, which was empty in the first release, now holds 34 measurements.

## Retrieved and held, contributing no row

**B1** Bravo-Hernández 2026 (*NAR* 54(3):gkag057, CC BY-NC) — would add the first non-human-primate
rows. **P1** US 10,799,523 B2 (public domain) — patent tables pair sequence with toxicity rating,
the format that supplied 21 rows to the sibling kidney module.

**S1**, **B2** and **M1** — two Roche CHDI conference decks and an NEJM correspondence item — are
on the working disk but listed in `.gitignore`. They are copyrighted publisher material not
licensed for redistribution; committing them would republish them, which is a different act from
reading them for research. They are named in full in the source register so anyone can retrieve
their own copy. **This was a judgement call, not an instruction — say the word and they can be
committed.**

## Human *in vitro* backlog — next up

Eight sources, all with verified identifiers, listed with their systems and payloads in §7 of the
source register. Highest value first:

1. **Flynn 2022** (PMC9019733, CC BY) — 90+ sequences across four chemistries in SH-SY5Y. The
   largest sequence-resolved human panel found, and big enough to model on its own.
2. **Ottesen 2026** (PMC12805893, CC BY) — an 18-mer with sequence and chemistry identical to
   nusinersen, which is already in this dataset's clinical layer. A direct in-vitro-to-clinical
   bridge on one molecule.
3. **Thirumalai 2025** (PMC11775556, CC BY) — hiPSC astrocytes, control and Down syndrome.
4. **Umek 2021** (PMC8713517, CC BY) — CAG19 in HD patient iPSC-derived neurons.
5. **Faravelli 2025** (PMC12847787, CC BY-NC-ND) — SMA spinal cord and cerebral organoids.
6. **Bowles 2021** (PMC8635409, not open access) — FTD patient cerebral organoids.
7. **König 2025** (PMC12691827, CC BY) — microfluidic 3D BBB chip, sequence printed.
8. **Selvakumaran 2023** (PMC10604610, CC BY) — iPSC brain microvascular endothelial cells.

**One lead with no verified citation.** A study reported as Yoshikawa 2025, *J Pharmacol Toxicol
Methods* 135:107844 — 27 ASOs through a rat calcium-oscillation IC50 assay, then mouse ICV, then a
human iPSC multi-electrode array — would be the closest match in the literature to the brief's
extrapolation clause. Four Europe PMC queries (page number, author and year, title phrase, DOI)
return nothing. **Listed as a lead to chase, not a citation.** No part of the dataset rests on it.

## Ruled out, with the reason

- **Drygin 2004** (PMC545465) — 43 oligos with per-compound cytotoxicity, every sequence printed.
  A549 lung and HepG2/Hep3B liver. Human, but not CNS.
- **Yuan 2025** (PMC12341589) — human iPSC neural organoids with microglia, exactly the right kind
  of system. No oligonucleotide is tested; the compounds are industrial neurotoxicants.
- **Means 2025** (PMC11798851) — the highest-profile personalised-ASO organoid screen, but the
  organoids are cardiac.
- **Seven ClinicalTrials.gov records** (BIIB078, BIIB094, GTX-102, RO7248824, STK-001, WVE-004 and
  a CpG-ODN glioblastoma trial) — all retrieved, all committed, all `hasResults: false`. The
  safety data for these programmes is not public anywhere this pipeline can reach.
