# OligoTox-Thrombocytopenia — A Curated Platelet-Toxicity Dataset for Oligonucleotide Therapeutics

A curated, openly-releasable, **per-measurement** dataset of
**thrombocytopenia / platelet toxicity** signals for therapeutic
oligonucleotides, built for the **NIH/NCATS Oligonucleotide Toxicity (OligoTox)
Open Data Challenge, Phase 2** (Data Generation Phase).

Thrombocytopenia is one of the toxicities of interest named in the challenge
brief (`../sources/reference/OligoTox_challenge_brief.pdf`, p. 1), alongside
hepatotoxicity, kidney toxicity, complement activation, coagulopathy,
immunotoxicity, chronic neurotoxicity and hydrocephalus.

The deliverable is a **dataset**, not a model: openly-releasable,
well-documented, and reproducible — which is what NCATS scores.

This is the **second endpoint** in this repository, alongside
**[OligoTox-Kidney](../README.md)**. It reuses that dataset's two-table design,
controlled vocabularies, provenance discipline and no-fabrication policy, so the
two are directly comparable and join on oligo identity.

---

## Why this endpoint is worth curating carefully

**Oligonucleotide thrombocytopenia is bimodal**, and a dataset that averages the
two modes together destroys the signal a predictive model most needs:

1. a **common, mild, dose- and plasma-concentration-dependent** platelet decline
   that plateaus and is reversible; and
2. a **rare, severe, idiosyncratic, immune-mediated** thrombocytopenia with
   treatment-emergent **antiplatelet antibodies**, counts below 25 × 10⁹/L, and
   real haemorrhagic risk.

**Inotersen** (Tegsedi) shows both in one FDA label — the basis of its **Boxed
Warning**. Platelet counts fell below 100 × 10⁹/L in **25 %** of treated patients
vs **2 %** on placebo (mild mode), while **3 %** had sudden severe
thrombocytopenia below 25 × 10⁹/L — **all three with treatment-emergent
antiplatelet IgG** — and one trial patient died of intracranial haemorrhage
(severe mode).

The `thrombocytopenia_grade` rubric (`schema.md`) is built to keep these
separable, and `readout_category` separates `platelet_count` from
`immunogenicity` and from the in-vitro `platelet_activation` /
`platelet_aggregation` correlates.

## Why the predictors are chemistry-centric

Platelet effects track **phosphorothioate (PS) content and protein binding**
rather than the hybridization target. PS backbones are potent platelet
activators via **glycoprotein VI**; neutral-backbone chemistries and
receptor-targeted conjugates should be largely silent.

A systematic sweep of every approved oligonucleotide's FDA label
(`../scripts/scan_labels_platelet.py`) supports this cleanly: **every PMO**
(neutral morpholino backbone) and **every siRNA / GalNAc-siRNA** returns *zero*
platelet mentions, while inotersen (70 mentions), imetelstat (30), nusinersen
(11) and olezarsen (6) do not.

`ps_count`, `backbone_chemistry`, `sugar_modifications` and `conjugate` are
therefore the central predictor columns — and **well-sourced negative controls
are a primary deliverable, not filler**, because they are what makes the
chemistry hypothesis testable.

> **An honest caveat, enforced in code.** Label *silence* is not a measured zero.
> A compound whose label never mentions platelets is evidence of absence only in
> the weak sense; a grade-0 row still requires a source that reports platelet
> monitoring having been done. The scan script says so in its own output, and no
> grade-0 row is created from silence.

## Four controlled comparisons the dataset is built around

Curation deliberately sought **matched pairs and titration series** — cases where
one design variable moves while the others are held fixed. These are what let a
model learn a mechanism rather than a correlation, and they are the dataset's
most distinctive content.

**1. Backbone chemistry, sequence held fixed — `ODN2395` PS vs non-PS.**
The same 22-mer with and without a phosphorothioate backbone, on human platelets
(Sewing 2017; CC-BY, so the raw values are redistributable):

| | ODN2395 non-PS | ODN2395 PS |
|---|---|---|
| PS linkages | 0 | 21 |
| PAC-1 binding (MFI, 10 µM) | 1.65 | **18.94** |
| grade | 0 | 2 |

**2. A phosphorothioate/length titration — the `(AC)n` series.**
Repeats of the same dinucleotide varying only in length, and therefore in PS
count, give a monotonic activation curve with a threshold between 9 and 11
linkages: (AC)5 → 2.12 MFI (grade 0), (AC)6 → 4.58, (AC)7 → 8.58,
(AC)8 → 16.79 (grade 2). This is the "key risk factor" of that paper's title,
captured as per-compound rows.

**3. PS count and conjugation, sequence and design held fixed —
`ISIS 416858` vs `fesomersen`.** From an Ionis FXI patent (public domain, so
values are freely reproducible): identical nucleobase sequence
`ACGGCATTGGTGCACAGTTT` and identical 5-10-5 MOE design, differing only in 19 vs
13 PS linkages plus a GalNAc conjugate — dose-dependent monkey platelet decline
vs none.

**4. Exposure, sequence and chemistry held fixed — volanesorsen vs olezarsen.**
Olezarsen's sequence is not published as a plain string, but the FDA label's
IUPAC chemical name spells out every residue; parsing it deterministically gives
`AGCTTCTTGTCCAGCTTTAT` — **identical to volanesorsen's independently published
sequence**, exactly as expected for the GalNAc-conjugated APOC3 analogue, and the
stated molecular formula `P20S19` independently fixes full-PS chemistry at 20
residues. The two therefore share sequence *and* chemistry, differing only in the
GalNAc conjugate and the ~20× lower dose that hepatocyte targeting permits:

| | volanesorsen | olezarsen |
|---|---|---|
| sequence / chemistry | `AGCTTCTTGTCCAGCTTTAT`, 5-10-5 2′-MOE, full PS | **identical** |
| conjugate | none | GalNAc |
| platelets < 100 × 10⁹/L | **47 %** (APPROACH) | not reported at this severity |
| mean platelet change | nadir −48 000/mm³ | **−6 % to −10 %** |
| outcome | **dose-limiting**; ITP a Common AR | no major bleeding events |

This isolates **exposure and conjugation — not sequence** — as the driver, which
is precisely the inference the dataset exists to support.

## Mechanism must be labelled, not assumed

`imetelstat` (Rytelo) causes
severe thrombocytopenia, but as **on-target telomerase-inhibitor myelosuppression
in MDS**, not PS-backbone platelet binding. It is retained for modality breadth
and explicitly mechanism-flagged so a model cannot attribute it to chemistry.
Likewise, volanesorsen's **anti-drug** antibodies carried no altered safety
profile, and must not be conflated with inotersen's **anti-platelet** IgG, which
tracked with severe events.

## Data model

Two normalized tables joined on `oligo_id` (full dictionary in **`schema.md`**):

| File | Grain | Key |
|------|-------|-----|
| `data/oligos.csv` | one row per unique oligo (identity + design predictors) | `oligo_id` (`TOLG###`) |
| `data/measurements.csv` | one row per oligo × model × delivery × dose × readout | `measurement_id` (`TMSR###`), `oligo_id` (FK) |

Missing/unknown values are the literal string `TBD` — never guessed, never
imputed as zero. A denormalized analysis-ready view is generated at
`data/oligotox_thrombo_merged.csv`; the two normalized tables remain canonical.

## How it was built

A **ten-lane parallel multi-agent sweep** (clinical, regulatory, in-vitro human
platelet, mechanism/immune, preclinical NHP, non-ASO negative controls, patents,
reviews/meta-analyses, megakaryocyte models, sequence-chemistry panels), each
lane blind to the others, then **per-source extraction** against verified full
text, then **adversarial verification** in which an independent agent is
instructed to *refute* every extracted row against its cited source.

Network egress was open in this session, so primary sources were retrieved
directly (PMC/E-utilities, Europe PMC, DailyMed SPL, EMA, USPTO, FDA
accessdata) rather than relying on user-supplied PDFs as the kidney dataset had
to. Full detail, including the two grading conventions and the QC suite, is in
**`METHODOLOGY.md`**; the verified source registry is in **`SOURCES.md`**.

Everything from agent output to published CSV is scripted and re-runnable:

```
python3 scripts/curate_labels_lane.py > labels_lane.json   # curated public-domain label rows
python3 scripts/assemble_thrombo.py  <curation.json>       # apply verdicts, dedupe, assign keys
python3 scripts/qc_thrombo.py                              # gate: enums, FK, ranges, provenance
python3 scripts/build_merged_thrombo.py                    # regenerate the analysis view
python3 scripts/report_thrombo.py                          # regenerate the tables below
```

<!-- BEGIN RECORD COUNTER -->

*Generated by `scripts/report_thrombo.py` and regenerated after every ingestion round, so the documented numbers cannot drift from the data.*

## Record counter

| | Count |
|---|------|
| Unique oligos (`oligos.csv`) | **119** |
| Measurement rows (`measurements.csv`) | **276** |
| — of which strict-platelet | **269** |
| — of which adjacent-haematology (flagged) | **7** |
| Grade distribution (0/1/2/3) | 147 / 67 / 44 / 18 |
| Distinct target genes | **23** |
| Distinct sources (`source_ref`) | **28** |
| Oligos with sequence (not TBD) | **98 / 119** |

## Independent (predictor) variables — `oligos.csv`

| Variable | Distribution |
|----------|--------------|
| **Modality (`oligo_class`)** | ASO_gapmer 100 · PMO 5 · GalNAc_siRNA 4 · splice_switching_ASO 4 · other 4 · siRNA 2 |
| **Backbone (`backbone_chemistry`)** | full_PS 95 · TBD 11 · PS_PO_mix 6 · PMO_neutral 5 · mixed 1 · full_PO 1 |
| **Conjugate** | none 107 · lipid 6 · GalNAc 6 |
| **Development stage (`max_phase`)** | research_panel 89 · approved 14 · preclinical 9 · phase_2 3 · class_review 1 · phase_1 1 · TBD 1 · approved_EMA 1 |
| **Sugar modifications** | 2'-MOE 97 · DNA_gap 97 · cEt 7 · 2'-OMe 6 · morpholino 5 · LNA 4 · 2'-F 4 · tricyclo-DNA 3 · DNA 2 · TBD 1 |
| **Sequence available** | 98 / 119 (rest `TBD`, never guessed) |

## Dependent (indicator) variables — `measurements.csv`

| Variable | Distribution |
|----------|--------------|
| **`thrombocytopenia_grade`** | 0: 147 · 1: 67 · 2: 44 · 3: 18 |
| **Study type** | animal_invivo 219 · clinical 39 · in_vitro 13 · ex_vivo 5 |
| **Species** | mouse 113 · monkey 65 · rat 53 · human 45 |
| **Delivery route** | systemic_dose 257 · direct_addition 13 · intrathecal 6 |
| **Readout category** | platelet_count 242 · clinical_outcome 9 · platelet_activation 9 · platelet_aggregation 8 · immunogenicity 4 · platelet_binding 4 |
| **Redistribution** | public_domain 243 · cc_by 17 · summary_stat 16 |
| **Platelet-specific** | TRUE 269 / 276 |

<!-- END RECORD COUNTER -->

## Provenance & licensing

- Every measurement row is traceable to a **source DOI / PMCID / patent number /
  label section** (`source_id`, `source_ref`, `source_table`).
- **Redistribution is tracked per row** (`redistribution`), so any consumer can
  filter to the rows they are entitled to reuse:
  `public_domain` (USPTO patents, FDA/EMA documents) · `cc_by` (raw values
  reproducible with attribution, confirmed from the article's own licence field)
  · `derived_features_only` / `summary_stat` (fair use) · `verify` (unresolved).
- **Sequences are never guessed.** `sequence_5to3` is `TBD` unless taken from a
  source that was actually retrieved.

See **`../PADP.md`** for the Public Access & Dissemination Plan (CC-BY 4.0,
archival DOI deposit, and the required U.S. Government continuity provisions),
which covers both endpoints in this repository.
