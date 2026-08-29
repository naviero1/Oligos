# Scoring instruments for CNS oligonucleotide toxicity

Harmonising measurements across sources is only defensible if the instruments themselves are
written down. This file records each scale exactly as its source defines it, so that a reader
can judge whether two rows in `measurements.csv` are really comparable.

**Provenance of this file.** Instruments marked **[read directly]** were transcribed from the
source PDF held in `sources/`. Instruments marked **[fetch summary]** were obtained through a
summarising web fetch of the publisher's page and have *not* been checked against the PDF;
they are documented here for context and **no dataset row depends on them**.

---

## 1. Acute tolerability score, 0–20 — mouse ICV

**[read directly]** Hagedorn et al. 2022, *Nucleic Acid Ther* 32(3):151–162 (source **H1**),
Materials and Methods.

> "For 1 h following the single bolus injection of ASO, animals were observed for behavioral
> side effects using a modified functional observational battery, as recommended by the
> Oligonucleotide Safety Working Group. The severity of side effects was scored using a
> tolerability scale divided into five neurobehavioral categories: (1) hyperactivity,
> (2) decreased activity and arousal, (3) motor dysfunction/ataxia, (4) abnormal posture and
> breathing, and (5) tremor/convulsions. Each category was scored on a scale of 0 to 4. Scores
> for each category were summed to a final acute tolerability score going from 0 (no side
> effects) to 20 (severe signs in all categories, including convulsions resulting in
> euthanasia). The acute tolerability scores for each mouse were averaged to produce a
> representative score for each treatment group."

| property | value |
|---|---|
| range | 0–20 (5 categories × 0–4) |
| observation window | 0–1 h after a single ICV bolus |
| dose used in H1 | 100 µg in 5 µL 0.9% saline |
| animals | adult female C57BL/6J, **4–6 per treatment group**, scores averaged |
| aggregation | group mean — so one dataset row is a group, not an animal |

### Severity bands — the source's own cut-offs

> "Based on inspection of the cumulative distribution of tolerability scores (Fig. 1B), we
> divided ASO into those with mild, moderate, marked, and severe tolerability signs using score
> cutoffs at 4, 7, and 18. We judged that only ASOs with no or mild tolerability signs,
> corresponding to roughly 60% of all ASOs assessed, were suitable for further development."

These are the cut-offs `cns_tox_grade` uses. See `docs/SCHEMA.md` § Grading.

### The same 0–20 scale in other sources

- **Miller et al. 2024** (source **K1**) reports an "average acute tolerability score" on the
  same 0–20 range after ICV dosing in mice. Rows from K1 are graded with the H1 cut-offs, and
  `grade_basis` says so explicitly.
- **Kuroda et al. 2025** (source **L1**) **[read directly]**, Supplementary Table S2, defines a
  five-category × 0–4 scale with a separate rat variant. Its categories are
  (1) consciousness — decreased exploration, decreased responsiveness;
  (2) motor function — ataxia, strength;
  (3) appearance — abnormal posture, abnormal breathing;
  (4) hyperactivity — increased home-cage exploration, stereotypy;
  (5) involuntary movement — tremors, seizure.
  The category set is close to but **not identical** with H1's, and L1 applies it in the
  **late-onset** window (days), not the acute window (1 h). L1 rows therefore carry
  `tox_axis = late_onset_neurodegeneration` and must not be pooled with acute rows without
  accounting for that.

---

## 2. Spontaneous calcium-oscillation score — rat primary cortical neuron

**[read directly]** Hagedorn et al. 2022 (source **H1**), Materials and Methods.

> "A scoring system was developed where a score of 1 was given for each 1 s read where signal
> increase was >50% of the average control amplitude value. A score of 0 was given for each 1 s
> read, which increased <50% of average control amplitude value. For each ASO, the total summed
> score was calculated and converted to percent of control."

| property | value |
|---|---|
| cells | primary cortical neurons from Sprague-Dawley rat embryos, embryonic day 19; 25,000 cells/well |
| indicator | fluo-4 AM, read on FLIPR |
| concentration | 25 µM ASO — chosen as "within the range of expected concentrations of ASO in mouse CSF the 1st hour after 100 µg ICV injection" |
| read | 300 s |
| units | percent of untreated control |
| direction | **lower = greater effect.** A score below 100 means oscillations were suppressed. |
| conditions | ± 1 mM added Mg²⁺ |

**Measured reproducibility.** One control ASO (`TAGccctaaagtcCCA`) appears 14 times in
Supplementary Table S1, i.e. it was run on 14 independent plates. Its scores span 68.15–128.50,
mean 92.38, SD 15.99 — a **coefficient of variation of 17.3 %**. Any use of a single
calcium-oscillation value should assume noise of that order. This is computed by
`src/make_figures.py` and shown as figure F6.

---

## 3. Acute neuronal **inhibition** scales, 0–7 — rodent and non-human primate

**[read directly]** O'Rourke et al. 2026, *Nucleic Acids Res* 54(3):gkaf1333 (source **O1**),
Supplementary Figure 1.

Rodent intrathecal scale, scored **3 h after dosing**:

| score | observation |
|---|---|
| 0 | bright, alert, responsive |
| 1 | no tone/movement in tail |
| 2 | weak posterior posture |
| 3 | hind limbs don't support weight, but can still move |
| 4 | hind paws don't move — full hindlimb paralysis |
| 5 | weak anterior posture |
| 6 | fore paws don't move, but animal is still breathing |
| 7 | death |

Separate variants are given for rodent ICV administration and for NHP intrathecal
administration; the NHP scale is reflex-based (knee-jerk reflex, cutaneous reflex, +1 point per
absent side).

**This is a different phenomenon from the 0–20 tolerability score**, and the distinction
matters for anyone pooling data: the tolerability score is dominated by *activation* signs
(hyperactivity, tremor, convulsions), whereas this scale measures progressive *loss* of motor
function. O'Rourke reports that in vitro firing-rate suppression >60 % predicted high in vivo
acute inhibition scores.

### A documented contradiction between two sources

Source **K1** (Miller 2024) shows that adding Ca²⁺ or Mg²⁺ to the injectate abolishes the
acute seizure/activation phenotype — from a score of 19.5 down to 1.0 at 32 mM Ca²⁺
(figure F7). Source **O1** reports the opposite for acute *inhibition*: divalent cation
supplementation at 1–100 mM did **not** alter the acute inhibition response.

Both can be true, because they are measuring different phenotypes; but a model trained on
pooled "CNS toxicity" labels would be learning across a real mechanistic boundary. This is
flagged in `sources.csv` and discussed in the narrative document.

---

## 4. Acute neuronal **activation** (aA) scales, 0–7

**[fetch summary — not verified against the PDF, and no dataset row depends on it]**
Bravo-Hernandez et al. 2026, *Nucleic Acids Res* 54(3):gkag057, Tables 1–3.

Reported as three 0–7 scales — rat after intrathecal dosing, mouse after ICV, and non-human
primate after lumbar puncture — scored at 15, 30, 45, 60, 90 and 120 min post-dose, covering
hunched posture, shivering, twitches, hyperactivity, vocalisation, tremor, seizure and death.
Recorded here because it is the third published instrument in this space and because a future
release should extract it directly; **it is deliberately not used for any current row.**

---

## Summary — what can be pooled with what

| instrument | range | window | sources | pooled in this release? |
|---|---|---|---|---|
| acute tolerability score | 0–20 | ~1 h, acute | H1, K1 | **yes** — same scale, graded with the same cut-offs |
| Kuroda tolerability score | 0–20 | days, late-onset | L1 | **no** — separate `tox_axis`, and scored only qualitatively (values published as figures) |
| calcium-oscillation score | % of control | in vitro | H1 | separate readout, ungraded, continuous |
| acute inhibition score | 0–7 | 3 h | O1 | **no rows** — instrument documented only |
| acute activation (aA) score | 0–7 | 15–120 min | — | **no rows** — instrument documented only |
| clinical adverse-event incidence | % of arm | trial duration | C1 | **no** — graded on a separate clinical rubric |
