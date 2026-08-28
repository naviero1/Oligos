# Hepatotoxicity

Liver injury after systemic oligonucleotide dosing, read out in practice as serum ALT/AST elevation with supporting
histopathology. It is the first endpoint named in the Challenge brief's list, quoted verbatim in the repository
register, [`../README.md`](../README.md). **This project extracted no hepatotoxicity data.** Five PDFs are held under
[`sources/`](./sources); none has produced a row. Four sibling endpoints do carry data — kidney-toxicity (769
measurements), thrombocytopenia (1786), chronic-neurotoxicity (2393), hydrocephalus (147); this is not one of them.
This file records what the five PDFs contain, what they would yield, and why none of it was mined.

## 1. Status

| | Value |
|---|---|
| Oligos | 0 — `hepatotoxicity/` holds no `data/` directory |
| Measurement rows | 0 |
| Local source PDFs | 5, all under [`sources/`](./sources) |
| `source_id`s reaching any `measurements.csv` in the repository | none |
| `source_id` registered but unused | `N1` (Dieckmann 2018), defined at `../kidney-toxicity/SOURCES.md:67-79`, re-registered with its DOI at `:138-139` |
| Extraction status | no rows anywhere in the repository; source tables parsed and cross-referenced (§3, §4); no grading rubric written for this endpoint |
| Deck coverage | no source, table or row from this endpoint appears in the kidney deck; grep of `../kidney-toxicity/presentation/PRESENTATION.md` for `hepatotox\|Dieckmann\|Burdick\|Hagedorn` returns zero hits. The deck does argue the liver/kidney framing on two rendered slides — §5 item 8 |

## 2. Work done

Acquisition and registration only: five PDFs acquired, filed and registered under `LOCAL SOURCE FILES` at
`../kidney-toxicity/SOURCES.md` (§ `LOCAL SOURCE FILES`, `hepatotox/` subtree), where Burdick's DOI and Hagedorn's stand against their filenames;
`N1` reclassified from kidney to hepatotoxicity with a stated reason (`:65-79`, "no kidney readout"); citations
confirmed for Hagedorn, Burdick and Kasuya at `:169-175`; `is_kidney_specific = FALSE` reserved for this endpoint's
future rows in [`../kidney-toxicity/schema.md`](../kidney-toxicity/schema.md), `measurements.csv` column table. No table was extracted, no `source_id` assigned to Burdick or
Hagedorn, and no rubric written.

## 3. Sources allocated

Paths verified by directory listing of [`sources/`](./sources); page counts read from the files.

| File | Pages | `source_id` | State | Rows | What it carries |
|---|---:|---|---|---:|---|
| `Dieckmann2018_supp_mmc2_full_with_supptables.pdf` | 14 | `N1` | acquired | 0 | Article + Table 1 (6 tool LNA-ASOs, p.2) + Tables S1, S2 |
| `Dieckmann2018_HDT_236-LNA-ASO_hepatotox_PMC5725219.pdf` | 10 | `N1` | acquired | 0 | The published article; duplicates mmc2's article portion, Table 1 included |
| `Dieckmann2018_supp_mmc1_oligo_sequences_Tm.pdf` | 4 | `N1` | acquired | 0 | Tables S1 (p.2) and S2 (pp.3–4); S1 is name / sequence / target RNA / Tm with no toxicity column. Wholly duplicated inside mmc2 pp.11–14 |
| `Burdick2014_LNA-ASO_hepatotox_seqmotifs_NAR.pdf` | 10 | none assigned | acquired | 0 | Table 1, 11 sequenced 14-mers with ALT/AST (p.6) |
| `Hagedorn2013_hepatotox_from_sequence_NAT.pdf` | 9 | none assigned | acquired | 0 | Main article only; carries no sequence strings at all |

Two hepatocyte panels sit **inside** PDFs filed under `../kidney-toxicity/sources/` and are allocated here, not to
[`../kidney-toxicity/README.md`](../kidney-toxicity/README.md):

| Locus | Content |
|---|---|
| `../kidney-toxicity/sources/US11105794_in_vitro_nephrotox_assay_patent.pdf` p.29, Table 5 | "EGF levels in culture media from primary hepatocytes at day 3 after oligonucleotide treatment", under Example 5. Rows are the patent's own compound numbers (saline, 1-1, 2-1, 3-1, 4-1, 10-1, 11-1, 14-1) with in-vivo grade words. |
| `../kidney-toxicity/sources/Moisan2017_EGF_uptake_nephrotox_ASO_invitro_PMC5363415.pdf` Fig. 3E (legend p.6, methods p.14) | "Measurement of EGF in the supernatant of human hepatocytes treated with 10 and 100 mM of AONs for 3 days"; the methods head the section "Human Hepatocytes and Retinal Pigment Epithelial Cells" and open "Cryopreserved human hepatocytes were suspended in William's Medium E". |

Multi-endpoint material also serving this endpoint (Frazier 2015; MMB 2434 Ch.27, mouse hepatocyte / Kupffer / LSEC
isolation) sits in `../_shared/sources/` and is indexed in [`../_shared/README.md`](../_shared/README.md).

**What extraction would yield.** Burdick Table 1 (PDF p.6, journal p.4887; columns ASO / Target / Sequence (5′–3′)
/ ALT (U/L) / AST (U/L) / Liver lesions) gives 11 rows, all with a sequence and a lesion call, 9 with numeric ALT
and AST (rows `3` and `4a` print `–`); mouse, 3LNA-8DNA-3LNA gapmers, none of the 11 sequences in
`../kidney-toxicity/data/oligos.csv`, so they would be 11 new oligos. Dieckmann mmc2 Table 1 gives 6 rows with sequence, target, ALT
fold-change, hepatotoxic yes/no and Tm. Total: 17 per-oligo records, 15 with a numeric toxicity value.

**Blocker 1 — the 236-oligo per-oligo table is not in the acquired PDFs.** mmc2's article reports that experiment only
in aggregate ("an additional 230 LNA-ASOs were tested … at a fixed concentration of 100 nM", result given as Figure 2);
its supplement (pp.11–14) is Table S1 (the GAPDH design table: 20 printed rows, 19 distinct — `mGAPDH_LNA_236`
appears twice) plus Table S2, genes up-regulated by LNA41 — the same two tables as mmc1. `../kidney-toxicity/SOURCES.md` § "STILL MISSING", bullet "N1 Dieckmann supplement", states the raw per-oligo table is a
separate Excel file; no such file exists under `sources/`.

**Blocker 2 — that dataset is Hagedorn's, so it is one acquisition task, not two.** mmc2's Table 1 legend
attributes its ALT values to reference 6, as does its 236-ASO sentence; reference 6 on mmc2 p.9 is Hagedorn et al.
2013, *Nucleic Acid Ther.* 23, 302–310 — the PDF already in `sources/`, whose own text reads "We
systemically administered 236 different saline-formulated LNA-modified phosphorothioate antisense oligonucleotides
by five intravenous injections of 15 mg/kg". That article carries no sequence strings (an `[ACGTacgt]{12,}` sweep of
all 9 pages returns nothing); its per-oligo data are online-only at `www.liebertpub.com/nat`, of which Supplementary
Table S1 — histopathology scored 0 to 3 across 25 categories — is the acquisition target. Any row taken from Dieckmann
Table 1 must carry Hagedorn's DOI in `source_ref` (`../kidney-toxicity/SOURCES.md` § "Provenance discipline").

## 4. Data

No column in `../kidney-toxicity/data/measurements.csv` records a liver readout, and a scan of all 769 rows for
`hepat`, `liver`, `_alt` and `aspartate` returns exactly two hits, neither a measurement:
`MSR010.source_ref = LiverInt2022_10.1111_liv.15090` (a journal name) and
`MSR044.notes = LNP_delivery_negative_control;grade_provisional`. `is_kidney_specific = TRUE` on 769 of 769 rows
corroborates this but is not evidence — a mislabelled row would be invisible to a constant flag.

### Molecule-level liver/kidney pairings the repo holds and does not record

| Pairing | Liver side | Kidney side |
|---|---|---|
| Dieckmann tool set × patent panel | mmc2 Table 1, 5 of 6 molecules | `OLG050`, `OLG051`, `OLG053`, `OLG054`, `OLG058` (rows `MSR96`, `MSR97`, `MSR99`, `MSR100`, `MSR104`) |
| Within US11105794 | Table 5, hepatocyte EGF (p.29) | Table 1 → the 21 `N3` rows whose `source_table` is `Table1`, of 431 `N3` rows in all |
| Within Moisan 2017 | Fig. 3E, hepatocyte EGF | `MSR080`–`MSR090`, 11 rows over `OLG002`, `OLG041`–`OLG044` |

The first has numbers on both sides. Dieckmann encodes 5-methylcytosine as `E`; US11105794 states the same chemistry
as plain `C` (PDF p.25, "All LNA C units are 5 ′ methyl C and all internucleoside linkages are phosphorothioate
linkage"; p.22 states the same chemistry in the claims in slightly different words), so substituting `E`→`C` in the
upper-case positions reproduces five patent compounds character-for-character. Both are Roche — US11105794 PDF p.1,
field (73) "Assignee : Hoffmann - La Roche Inc."; `../kidney-toxicity/SOURCES.md:177` ("Roche (Dieckmann, Hagedorn, Berrera)") for Dieckmann.

| Dieckmann | Sequence | ALT fold | Hepatotoxic | → | `oligos.csv` sequence | Patent class | `nephrotox_grade` |
|---|---|---:|---|---|---|---|---:|
| LNA32 | EAAaggaaacacaEAT | 1.09 | no | `OLG050` | CAAaggaaacacaCAT | innocuous | 0 |
| LNA33 | EAAatgctgaaacTAT | 1.02 | no | `OLG051` | CAAatgctgaaacTAT | innocuous | 0 |
| LNA37 | GEEtcccagttccTTT | 41.54 | yes | `OLG053` | GCCtcccagttccTTT | low_medium | 2 |
| LNA41 | EAEattccttgctETG | 44.57 | yes | `OLG054` | CACattccttgctCTG | medium | 2 |
| LNA39 | GTEagaaacaaccAEE | 1.06 | no | `OLG058` | GTCagaaacaaccACC | high | 3 |
| LNA43 | GATgcctcccaGTT | 36.48 | yes | — | no match (14-mer) | — | — |

Two of the three liver-negative ASOs are kidney grade 0 and both liver-positive ASOs are kidney grade 2; `OLG058` dissociates, liver-negative against the patent's "high" class and grade 3.

Pairings 1 and 2 intersect at `OLG054` (patent compound 10-1) and `OLG058` (14-1): each carries a liver value in two
independent documents plus a graded kidney row, the dissociating molecule among them. The table above is transcribed
source data held outside any `data/` — no script validates it, `../kidney-toxicity/scripts/build_merged.py` does not see it, the `../kidney-toxicity/schema.md` QC log
does not cover it, and ingestion rather than this dossier is where it would become a record. That is a departure from
the traceability rule stated in the register, [`../README.md`](../README.md), recorded here rather than left implicit.

> **Caveats travelling with this table.** The two endpoints were measured in different species on different schedules:
> liver = mouse, 5 × 15 mg/kg i.v., ALT at 2 weeks (mmc2 p.2 legend); kidney = Wistar Han male rats, 40 mg/kg on days 1
> and 8 intrascapular, day 15 (US11105794 p.25). The pairing is hypothesis-generating, not a comparison. These five
> rows inherit the `N3` defects in [`../kidney-toxicity/README.md`](../kidney-toxicity/README.md), section 6 "Known issues" —
> items 1 (species and design), 4 (the grades are a within-panel relative rank) and, for `MSR96`/`MSR97`/`MSR99`, 10 (ID padding).

## 5. Known issues

1. `../kidney-toxicity/SOURCES.md:76-78` frames the Dieckmann panel as "the single biggest *volume* source available → use for the
   **hepatotox fallback** category". The volume is not there (blocker 1); the value is the cross-reference above. This
   does not contradict `:75`, which correctly says Dieckmann reports no kidney readout.
2. `../kidney-toxicity/METHODOLOGY.md:60-62` ("None ingested as rows yet") and `../kidney-toxicity/SOURCES.md` § "Extraction status"
   ("pending") together read as an absence of available data, when 17 per-oligo records are in hand. Exclusion is
   legitimate; it is simply not recorded as a decision at either locus. The "Record counter" table that carried a
   hepatotox-fallback row did not survive the rewrite of `../kidney-toxicity/README.md`, so that third locus is gone.
3. Of the five fallback candidates at `../kidney-toxicity/SOURCES.md:83-91`, Kasuya 2016 has a confirmed DOI (`10.1038/srep30377`) and is flagged open access at `:174-175` but was never acquired; only Creyon 2025 (`:89`) remains uncited.
4. The `is_kidney_specific = FALSE` branch is used by zero of the 769 kidney rows, so deliberate exclusion is indistinguishable from non-attainment.
5. `../kidney-toxicity/SOURCES.md:79` leaves N1's redistribution as "journal OA — `derived_features_only`; confirm". It was never confirmed, and `derived_features_only` and `verify` are used by zero of the 769 kidney rows, so neither has a worked precedent.
6. `nephrotox_grade` cannot be reused: the rubric in `../kidney-toxicity/schema.md` is renal at every level — 0 "No renal signal at tested
   exposure", 1 low-MW proteinuria, 2 KIM-1/NGAL/clusterin or histopathology, 3 "acute kidney injury … renal failure / dialysis".
7. The "case encodes chemistry" rule at `../kidney-toxicity/reconcile/METHODOLOGY-111row-lineage.md:184-187` describes how sequences are stored in this repo's rows and
   does not transfer to source typography — Burdick prints all upper case, Dieckmann adds an `E` token. Restate it per source at ingestion and carry the 3-8-3 design in `gapmer_design`, not in the string.
8. `../kidney-toxicity/presentation/PRESENTATION.md:167` and `:647` argue on rendered slides that open oligo-tox data is liver-focused and kidney under-served, without mentioning that five liver PDFs are held.

## 6. Not done / blocked

| Not done | Cause |
|---|---|
| Any row ingested | Scope decision, kidney-only; 17 records extractable today with no new acquisition |
| The 236-oligo in-vivo dataset | Not in the repo — it is Hagedorn's, published as online-only supplementary tables (blocker 2) |
| Kasuya 2016, Creyon 2025 | Never acquired (issue 3) |
| A hepatotoxicity grading rubric | Never written |
| A `source_id` for Burdick and Hagedorn | Never assigned |
| Redistribution determination for N1 | Never confirmed (issue 5) |
| The two in-repo hepatocyte panels | Never noticed; both PDFs are filed under `../kidney-toxicity/sources/` and were mined for kidney readouts only |

## 7. Next step

1. Record the scope decision in the register [`../README.md`](../README.md) and at `../kidney-toxicity/SOURCES.md` § "Extraction status" (out of scope for Phase 2, five PDFs held, two carrying 17 extractable per-oligo records); retract `:76-78`'s volume framing and correct `:83-91` to mark Kasuya and Creyon as never acquired.
2. Assign `source_id`s to Burdick and Hagedorn; resolve N1's redistribution class; mark `../kidney-toxicity/SOURCES.md:143`'s "Assignee to confirm on the patent face" as confirmed (Hoffmann-La Roche).
3. Before any ingestion, this endpoint needs its own two-table dataset under `hepatotoxicity/data/` with a `hepatotox_grade` column and its own rubric, on the pattern of the four populated endpoints. Do not reuse or rename `nephrotox_grade`.
4. If the scope is widened, ingest in this order: US11105794 Table 5 and Moisan Fig. 3E (already held and parsed for
   kidney; the first `is_kidney_specific = FALSE` rows), then Burdick Table 1, then Dieckmann Table 1 carrying Hagedorn's DOI. Acquire Hagedorn's Supplementary Table S1 before attempting the 236-oligo set.

---

Index: register [`../README.md`](../README.md) · [`../kidney-toxicity/README.md`](../kidney-toxicity/README.md) · [`../thrombocytopenia/README.md`](../thrombocytopenia/README.md) · [`../chronic-neurotoxicity/README.md`](../chronic-neurotoxicity/README.md) · [`../hydrocephalus/README.md`](../hydrocephalus/README.md) · [`../_shared/README.md`](../_shared/README.md) · [`../kidney-toxicity/METHODOLOGY.md`](../kidney-toxicity/METHODOLOGY.md) · [`../kidney-toxicity/schema.md`](../kidney-toxicity/schema.md) · [`../kidney-toxicity/SOURCES.md`](../kidney-toxicity/SOURCES.md)
