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

## Five controlled comparisons the dataset is built around

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

**5. A single nucleoside, everything else held fixed — `ISIS 972163` vs
`ISIS 972116`.** The finest-grained contrast in the dataset, from the Ionis APOL1
patent (public domain). Identical bases (`CGTCAATATATTCTTT`), identical 9-base
DNA gap, identical 3-9-4 design; the wings differ by **one nucleoside**
(`kkk-d9-kkke` vs `kkk-d9-keke` — cEt → 2′-MOE at a single position). In the same
rat table: **556 vs 325 K/µL**, a 41 % platelet difference.

That patent also holds a **species-discordant** case worth modelling rather than
averaging away: SEQ ID 413 appears as three different wing chemistries, and all
three are the worst compounds in rat (144 / 294 / 112 vs 725 control) while
sitting at 80–92 % of control in mouse.

## Does the assembled data actually support these inferences?

A curated dataset that cannot reproduce its field's best-established
structure-activity relationship is not ready to train anything. `scripts/analyze_thrombo.py`
checks this directly — descriptive and non-parametric, with `TBD` excluded rather
than coerced to zero. Run it after any ingestion round.

<!-- BEGIN FITNESS ANALYSIS -->

**Backbone chemistry orders as the phosphorothioate hypothesis predicts**,
with no modelling:

| backbone | n rows | n oligos | mean grade |
|---|---:|---:|---:|
| `PMO_neutral` | 10 | 6 | 0.10 |
| `PS_PO_mix` | 26 | 6 | 0.27 |
| `full_PO` | 57 | 6 | 0.44 |
| `full_PS` | 1483 | 167 | 0.99 |

Mean grade also rises with phosphorothioate count (0 → 0.39; 13–16 → 0.60; 17–19 → 1.09; 20+ → 1.47 linkages).

Modality orders PMO 0.10 < GalNAc_siRNA 0.27 < siRNA 0.50 < ASO_gapmer 0.89 < splice_switching_ASO 0.90 < other 1.17 < aptamer 1.60.

**The caveat that must travel with this.** Grade is partly confounded with
study type — severe thrombocytopenia is observed in trials, not in dishes:

| study type | n rows | mean grade | % grade 3 |
|---|---:|---:|---:|
| ex_vivo | 26 | 1.38 | 15.4% |
| in_vitro | 478 | 1.07 | 7.3% |
| clinical | 773 | 1.00 | 11.1% |
| animal_invivo | 416 | 0.70 | 6.5% |

Any model trained here must account for study type rather than learn it
as biology.

<!-- END FITNESS ANALYSIS -->

## Two things a modeller must do before using this

Both are correct properties of the data, not defects — but both will mislead a
naive join, and `qc_thrombo.py` reports each on every run.

1. **Exclude `dose_or_conc_value == "0"` before joining grade to design
   features.** 31 control-arm rows carry grade 1–2. That is right — the rubric
   grades the *observed* band regardless of arm, and a placebo subject whose
   platelets fell below 75 × 10⁹/L did have that event — but joined naively it
   teaches a model that a compound caused an effect at zero dose. The rows are
   kept because they carry the comparator denominators.

2. **Account for study type; do not learn it as biology.** Severe
   thrombocytopenia is observed in trials, not in dishes, so grade is partly
   confounded with study design. The generated table above quantifies it.

A third, narrower caveat: the `< 0.5 × BSLN` relative-decline band is graded 2
under the rubric's "requiring monitoring" clause. That is a documented judgement
call, applied uniformly across all 23 such rows; a reviewer could reasonably set
it to 1, and doing so is a one-line filter.

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
text, then an **adversarial verification** stage in which an independent agent is
instructed to *refute* every extracted row against its cited source.

> **Verification status: 659 of 1,336 rows (49 %) verified.** The two largest
> blocks have been through adversarial verification — an independent agent
> instructed to *refute* each row against its cited source:
> **Crooke 2017 pooled clinical, 387 rows → 382 confirmed / 5 corrected / 0
> rejected**, and the **in-vitro human platelet block, 272 rows → 246 confirmed /
> 26 corrected / 0 rejected**, where all 115 Sewing values were recomputed from
> the paper's raw per-replicate workbook and every mean, SD and n reproduced
> exactly. No value error survived in either block. The remaining **677 rows are
> still `unverified`** — chiefly patent-derived and regulatory-review blocks — so
> the dataset is *partially* verified, not fully. Verified rows carry a
> `verified_against_source` marker in `notes`. See `METHODOLOGY.md` for the
> per-block detail and the four data-integrity defects found and fixed.

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
python3 scripts/refresh_docs.py                             # regenerate the tables below
```

<!-- BEGIN RECORD COUNTER -->

*Generated by `scripts/report_thrombo.py` and regenerated after every ingestion round, so the documented numbers cannot drift from the data.*

## Record counter

| | Count |
|---|------|
| Unique oligos (`oligos.csv`) | **251** |
| Measurement rows (`measurements.csv`) | **1786** |
| — of which strict-platelet | **1595** |
| — of which adjacent-haematology (flagged) | **191** |
| Grade distribution (0/1/2/3) | 756 / 466 / 372 / 192 |
| Distinct target genes | **60** |
| Distinct sources (`source_ref`) | **47** |
| Oligos with sequence (not TBD) | **192 / 251** |

## Independent (predictor) variables — `oligos.csv`

| Variable | Distribution |
|----------|--------------|
| **Modality (`oligo_class`)** | ASO_gapmer 186 · other 43 · PMO 6 · aptamer 5 · splice_switching_ASO 5 · GalNAc_siRNA 4 · siRNA 2 |
| **Backbone (`backbone_chemistry`)** | full_PS 191 · TBD 34 · PS_PO_mix 10 · full_PO 6 · PMO_neutral 6 · mixed 3 · NA 1 |
| **Conjugate** | none 225 · GalNAc 14 · lipid 5 · TBD 5 · other 1 · PEG 1 |
| **Development stage (`max_phase`)** | research_panel 135 · preclinical 52 · phase_1 24 · approved 16 · phase_2 10 · class_review 8 · phase_3 4 · TBD 1 · approved_EMA 1 |
| **Sugar modifications** | DNA_gap 174 · 2'-MOE 155 · cEt 37 · 5-methylcytosine 19 · TBD 19 · DNA 15 · 2'-OMe 11 · LNA 9 · DNA_deoxyribose 8 · morpholino 7 |
| **Sequence available** | 192 / 251 (rest `TBD`, never guessed) |

## Dependent (indicator) variables — `measurements.csv`

| Variable | Distribution |
|----------|--------------|
| **`thrombocytopenia_grade`** | 0: 756 · 1: 466 · 2: 372 · 3: 192 |
| **Study type** | clinical 852 · in_vitro 482 · animal_invivo 424 · ex_vivo 28 |
| **Species** | human 1291 · mouse 175 · monkey 174 · rat 85 · minipig 52 · multi_species 4 · NA 4 · dog 1 |
| **Delivery route** | systemic_dose 1264 · direct_addition 496 · TBD 9 · gymnotic_free_uptake 9 · intrathecal 6 · intravitreal 2 |
| **Readout category** | platelet_count 977 · platelet_activation 195 · clinical_outcome 191 · platelet_binding 117 · platelet_aggregation 114 · immunogenicity 94 · coagulation 49 · megakaryocyte 24 · histopathology 14 · viability 11 |
| **Redistribution** | summary_stat 841 · public_domain 742 · cc_by 203 |
| **Platelet-specific** | TRUE 1595 / 1786 |

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
