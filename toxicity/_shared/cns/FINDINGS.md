# FINDINGS — OligoTox-CNS

Every number below names the command that regenerates it. Nothing here is quoted from memory or
from a secondary source; where a claim comes from a source's own text it is quoted and attributed.

---

## F-01 — The field's largest public CNS dataset is roughly 12× bigger than it is usually cited as

Hagedorn et al. 2022 is consistently cited for **148** mouse-dosed compounds — including by the
team's own ML strategy brief and by an independent literature sweep run for this project.
Its Supplementary Table S1 in fact contains **1,825** oligonucleotides, each with a printed
sequence and a measured in vitro calcium-oscillation score; **181** of them additionally carry a
mouse acute tolerability score.

> ```
> python3 -c "import openpyxl; ws=openpyxl.load_workbook('sources/H1_Hagedorn2022/Suppl_TableS1.xlsx')['S1']; \
> rows=[r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]; \
> print(len(rows), sum(1 for r in rows if isinstance(r[13], (int, float))))"
> # -> 1825 181
> ```
> `python3 qc/validate_dataset.py` → `n_oligos: 1839`, of which 1,825 come from source H1

The 1,644 calcium-only compounds have been effectively invisible because they sit in a
spreadsheet behind a download challenge, with chemistry encoded in text case. **Making the full
table usable is this project's single largest contribution.**

---

## F-02 — The sequence-derived score tracks in vivo toxicity better than the in vitro assay does

| predictor | AUC vs "tolerability score > 4", n = 181 |
|---|---|
| published sequence-only linear model | **0.888** |
| measured in vitro calcium-oscillation score | 0.735 |

> `python3 src/baseline_model.py` → `auc_all_published_linear`, `auc_all_measured_invitro`

On the held-out set (19 compounds against a different target gene, held out by the original
authors) both reach AUC 0.929, and the published model classifies at **89.5 %** accuracy at its
published cut-off of 70.

**This is not a criticism of the assay; it is a statement about noise** — see F-03. The source
authors reach the same conclusion in their own words: *"the model being able to capture the
underlying effect on calcium oscillations without the biological noise of the measurement
procedure… the calculated score represents a model-guided average estimate of this observable
compared to the measured score."*

**Consequence for modelling:** do not treat the in vitro score as ground truth to be predicted,
and do not discard a candidate on a single plate run.

---

## F-03 — The in vitro assay's reproducibility is measurable from the dataset: CV 17.3 %

One control oligonucleotide, `TAGccctaaagtcCCA`, appears **14 times** in Supplementary Table S1 —
it was run on 14 independent plates.

| n | mean | SD | CV | range |
|---|---|---|---|---|
| 14 | 92.4 | 16.0 | **17.3 %** | 68.15 – 128.50 |

> `python3 src/make_figures.py` → figure F6 and the `F6` line of `figures/figure_numbers.txt`

**This nearly went in wrong.** The first version of the figure grouped replicates on
`sequence_base` — the chemistry-stripped nucleobase string — which merges oligonucleotides that
share a base sequence but carry LNA at different positions. Those are *different molecules*, and
the spurious group gave n = 25 and CV 30.5 %. Grouping on the as-printed sequence, whose case
encodes LNA position, gives the true replicate set. Caught by rendering the figure and reading
it.

---

## F-04 — Guanine is a graded risk factor, and its position matters more than its count

Median mouse acute tolerability score (0–20) by guanine count:

| G count | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| median score | 0.3 | 3.2 | 7.3 | 7.7 | 15.0 | 20.0 | 20.0 |
| n | 81 | 37 | 16 | 30 | 11 | 3 | 3 |

By length of the guanine-free stretch measured from the 3′ end:

| G-free 3′ stretch (nt) | 0–4 | 5–9 | 10–14 | 15–20 |
|---|---|---|---|---|
| median score | 12.3 | 6.8 | 2.5 | 0.3 |
| n | 45 | 28 | 21 | 87 |

> `python3 src/make_figures.py` → figure F5 and the `F5` lines of `figures/figure_numbers.txt`

The 3′-position relationship has 21–87 compounds per bin and is the more reliable of the two; the
extreme guanine-count bins are n = 3 and should be read as a trend only. **Both group sizes are
printed on the figure** so a reader cannot mistake the n = 3 bins for solid ground.

---

## F-05 — Formulation can override sequence entirely

At a fixed 10 nmol ICV dose of the same molecule, adding calcium to the injectate:

| added Ca²⁺ (mM) | 0 | 4 | 8 | 12 | 16 | 32 |
|---|---|---|---|---|---|---|
| acute tolerability score | 19.5 | 11.75 | 6.75 | 3.25 | 1.5 | 1.0 |

> `python3 src/make_figures.py` → figure F7 and the `F7 Ca rescue` line

Magnesium produces a similar but shallower effect (19.5 → 2.75 at 16 mM, 4.0 at 32 mM).

**Consequence:** a model trained on sequence and chemistry alone, over data pooled across studies
using different vehicles, will attribute a formulation effect to the molecule.
`formulation_ca_mM` and `formulation_mg_mM` are therefore first-class columns.

**This also nearly went in wrong.** The first version of the figure selected rows by dose and
cation concentration alone, which pulled control groups from unrelated figure panels onto the
same curve at x = 0 (four different scores at 0 mM). Rows are now selected by the source figure
panel they belong to. Caught by rendering the figure and reading it.

---

## F-06 — Two 2024–2026 sources contradict each other on cation rescue, and both are right

- Source **K1** (Miller 2024): adding Ca²⁺ or Mg²⁺ abolishes the acute phenotype (F-05).
- Source **O1** (O'Rourke 2026): divalent cation supplementation at 1–100 mM did **not** alter
  the acute response measured there.

They measure different phenotypes: K1 scores an **activation** syndrome (hyperactivity, tremor,
convulsions, 0–20 scale, ~1 h); O1 scores an **inhibition** syndrome (progressive loss of motor
function, 0–7 scale, scored at 3 h). A model trained on a pooled "CNS toxicity" label would learn
across a real mechanistic boundary.

> `docs/SCORING_INSTRUMENTS.md` § 3 records both instruments and this contradiction.

This is only visible when sources are placed side by side — neither paper states it.

---

## F-07 — Acute and late-onset toxicity are separable, and acute screening misses late-onset

Source L1 reports gapmers that produce **no acute toxicity** (or acute signs resolving within a
day) yet cause hypoactivity and motor loss beginning three or more days after dosing — severe
enough that two of five compounds required humane sacrifice at day 7, and one of four rats dosed
intrathecally died at day 14.

> `data/measurements.csv`, rows with `tox_axis = late_onset_neurodegeneration`

The dataset keeps the windows on separate axes so a model is not trained to call a late-onset
toxin safe.

---

## F-08 — More features did not help: the constraint is labelled examples, not features

| model | inputs | held-out AUC | held-out accuracy |
|---|---|---|---|
| published linear model | base composition + 3′ G-free length | 0.929 | 89.5 % |
| logistic regression fitted here | 12 sequence and geometry features | 0.857 | 78.9 % |

> `python3 src/baseline_model.py`

With 138 labelled training compounds, the extra features cost more in variance than they buy in
signal. Reported because it is a **useful negative result**: anyone planning to model this data
should invest in labelled in vivo examples, not in feature engineering.

---

## F-09 — Per-compound purity is not in the published record

`purity_pct` is `NOT_REPORTED` for **all 1,839** oligonucleotides. The purification and
identity-confirmation *method* is captured where stated, for **1,825 of 1,839**.

> `python3 qc/validate_dataset.py` → `missingness: {'purity_pct': 1839, 'purity_method': 14, …}`

This is the largest gap between this dataset and the challenge's description of one. It is a
property of the literature, not of the curation, and no value has been estimated to close it.
Tracked as **OI-02**.

---

## F-10 — The predictive in vitro screen for CNS oligonucleotide toxicity is rodent, not human

Only **12 of 2,065** measurements are human-derived, and all twelve are clinical adverse-event
incidences. The in vitro arm is rat primary cortical neuron.

> `python3 qc/validate_dataset.py` → `human_system_measurements: 12`

The challenge specifically prioritises *"datasets based on in vitro human systems or able to
extrapolate data between in vitro human systems and animal data."* This dataset satisfies the
second clause — 181 compounds carry paired in vitro and in vivo readouts — but **not the first**.

We searched for published, sequence-resolved human iPSC-neuron or organoid data on
oligonucleotide CNS toxicity. A 2023 review states that *"using human induced pluripotent stem
cell-derived neuronal models for the in vitro assessment of seizure liability is promising for
ONDs"*, describing it as a future direction rather than established practice, and we found no
public dataset. **Stated as a finding, not glossed over: the human in vitro layer this challenge
asks for does not appear to exist publicly yet.**

---

## Verification summary

| claim type | how verified |
|---|---|
| Dataset integrity | 26 structural and provenance checks, all passing (`qc/validate_dataset.py`) |
| Transcription fidelity | The source's published linear model, re-implemented from its supplementary methods, reproduces the source's own score column for all 1,825 rows (0 mismatches) |
| Chemistry encoding | Upper-case count equals the source's declared LNA count for all 1,825 rows (0 mismatches) |
| Grading rubric | Reproduces the source authors' stated "roughly 60 % suitable for further development" at 112/181 = 61.9 % |
| End-to-end usability | A baseline classifier trained only on the released CSVs reaches the accuracy the original authors report on their own held-out set |
| Every figure and PDF page | Rendered to an image and read; five substantive errors found and fixed this way (F-03, F-05, and three in the PDFs — see `CHANGES.md`) |
