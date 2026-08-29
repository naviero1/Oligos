# What is missing — and what should be generated next

A gap analysis for **OligoTox-CNS**, produced by a 17-agent source sweep across
14 search angles plus three adversarial completeness critics, and cross-checked
against what the extraction lanes actually found.

This document exists because the OligoTox challenge is a **Data Generation**
phase. A curation can only report what the literature already contains; the more
useful thing it can produce alongside the data is a precise, evidence-backed map
of where the literature is *empty*. Every gap below was confirmed by searching
for it and finding nothing — not assumed from absence in our own tables.

---

## The headline finding

**The published literature is richest exactly where the challenge assigns lowest
priority, and close to empty where it assigns highest.**

The brief deprioritises acute neurotoxicity focused on neuronal electrical
activity. That is the best-served area by a wide margin: large scored panels
exist, with published sequences, in the thousands of compounds. The two named
endpoints — chronic neurotoxicity and hydrocephalus — are served by a couple of
dozen documents between them, and the human in vitro systems NCATS explicitly
asks for barely exist at all.

That asymmetry is the single most useful thing this curation has to report. It
says what a Data Generation phase should fund.

---

## Gap 1 — Human in vitro neural systems (the modality NCATS names)

Confirmed empty by direct search, not inferred:

| System | What exists |
|---|---|
| Human iPSC **microglia** + oligonucleotide toxicity | Essentially nothing. One bioRxiv preprint, efficacy-framed. NCATS names microglia explicitly. |
| Human **brain/cortical organoids** + oligonucleotide safety | One paper across a 227-hit query actually doses human organoids and reads out toxicity, and its endpoint is a nuclei count. |
| Human **choroid plexus / ependymal / cilia** models | **Zero.** See Gap 2 — this is the mechanistic human model for the top-priority endpoint. |
| Human iPSC **astrocytes**, **oligodendrocytes** | One paper, efficacy-framed. |
| Human **blood-brain / blood-CSF barrier** models | Absent. |
| In vitro **NfL release** from human neurons | One paper, and it is the most valuable in the whole modality (below). |

A caution for anyone reading a source inventory in this field: **the human in
vitro category is easy to overstate**. Several widely-cited "in vitro" oligo
neurotoxicity assays turn out on inspection to use rat primary cortical neurons,
mouse Neuro-2a, or human *cancer* lines — not human iPSC-derived neural cells.
This dataset's own `system_model` and `species` columns record what each study
actually used, and its 295 in-vitro rows are counted honestly rather than
generously.

**The single most valuable existing bridge** is an iPSC motor-neuron assay
measuring **neurofilament light released into culture supernatant** — the same
biomarker the clinical and non-human-primate rows measure in CSF and plasma. One
assay, one biomarker, three scales. If one human in vitro assay deserves to be
built out and standardised, it is that one.

### What to generate

1. A human iPSC neuron / astrocyte / microglia panel dosed **gymnotically**
   (free uptake, not lipofection — forced delivery exaggerates
   hybridisation-dependent effects and is not what happens in CSF), read out for
   NfL release, glial activation markers, and viability, across a compound set
   with **published sequences**. Sequence plus outcome is the modelling payload;
   an assay on unnamed compounds cannot train anything.
2. **Chronic** exposure designs. One published series showed allele selectivity
   degrading between one and four weeks — a change invisible to any short assay,
   and directly relevant to the chronic endpoint.

---

## Gap 2 — Hydrocephalus has clinical depth and no mechanistic floor

The clinical and regulatory evidence is genuinely good: a European safety
communication with individual case narratives, a PSUR denominator, an
exposure-dependent ventricular-volume ladder with a concurrent placebo arm, and
imaging endpoints. This dataset carries 112 hydrocephalus rows.

Underneath that, there is almost nothing:

- **No published animal study in which an oligonucleotide caused hydrocephalus**,
  with one 19-year-old exception in which an ICV antisense knocked down a
  specific target (Gαi2) and produced ependymal ciliary stasis. Even that is
  plausibly a *pharmacological* effect of losing that target, not a property of
  oligonucleotide chemistry — which decides whether it generalises at all.
- **No non-human-primate ventricular-volume dataset** for any therapeutic
  oligonucleotide.
- **No CSF outflow-resistance measurement**, and **no ependymal cilia
  beat-frequency assay**, for any clinical-stage oligonucleotide.
- **No in vitro model of CSF dynamics** for oligonucleotide toxicity, in any
  system.

There is also a specific confound that must be carried, not hand-waved: **spinal
muscular atrophy itself raises hydrocephalus risk and ventricular volume**
independently of any drug. Any ventriculomegaly row in an SMA patient is
uninterpretable without that baseline, which is why this dataset now carries the
untreated-disease comparison alongside the treated rows.

One structural observation worth preserving: **raised intracranial pressure and
hydrocephalus dissociate.** One drug shows papilloedema and raised pressure with
zero hydrocephalus; another shows ventriculomegaly. They are separate
`readout_name`s here for that reason, and a model that collapses them will learn
a relationship that does not exist.

### What to generate

1. **Ventricular volume as a routine endpoint in non-human-primate intrathecal
   studies.** It is imaging on animals already being dosed and imaged. Its
   absence is why the clinical signal surfaced only after marketing: a
   nonclinical package for one of these drugs contains zero occurrences of
   "ventricle", "hydrocephalus" or "ependyma".
2. **A human choroid-plexus / ependymal organoid assay** — cilia beat frequency,
   barrier function, CSF secretion — dosed with clinical-stage oligonucleotides.
   This is the missing mechanistic human model for the top-priority endpoint, and
   choroid plexus organoids now exist as a platform.

---

## Gap 3 — Chronic neurotoxicity is thin, and partly mislabelled

Most of what sits under "oligonucleotide neurotoxicity" is 1–24 hour acute
scoring. Genuine chronic per-measurement data comes from a small number of
sources. The distinction matters enough that this dataset makes it a column
(`endpoint_domain`) rather than leaving it to a reader's judgement.

The related and more damaging problem is **recovery**. `reversibility` is
`not_assessed` on 1,927 of 2,329 rows, because most studies never looked. A
finding cannot be classified as chronic or transient without a follow-up
timepoint, so this single omission limits what the whole dataset can say about
its own priority endpoint.

### What to generate

**Add a recovery arm.** This is the cheapest high-value change available in the
entire field: the animals are already dosed, the histopathology is already run,
and one extra timepoint converts an ambiguous finding into a classified one. A
regulatory nonclinical review that *does* include recovery groups is
correspondingly the most informative document in this dataset.

---

## Gap 4 — Sequences and outcomes live in different documents

Nearly every clinical and regulatory source carries rich CNS outcomes and **no
sequence**. Nearly every panel with sequences carries acute rodent scores and no
clinical outcome. The join between them is what a predictive model needs.

Three routes close it, all used here: WHO INN nomenclature (which spells out
every residue longhand and is therefore a deterministic parse rather than a
transcription), patent sequence listings paired with tolerability tables, and
European assessment reports, which occasionally print a sequence where the US
label does not.

**What to generate:** sponsors publishing sequence alongside CNS outcome for
clinical-stage compounds. 122 of this dataset's 585 oligonucleotides still have
no published sequence, and a substantial share of those are proprietary rather
than merely unretrieved.

---

## A methodological warning for anyone repeating this work

Independent search agents converge on the same key papers and then **cite them
under drifting author lists**. In one sweep a single paper appeared five times
under four mutually inconsistent author strings — at most one correct, the rest
plausible-looking fabrications produced by paraphrase.

This is why every row in this dataset keys on a **canonical identifier** — DOI,
PMID, NCT number or patent number — with the citation as written preserved
separately, and why the source registry is generated from the data rather than
maintained by hand. An author string is not an identifier, and a source inventory
that keys on prose will silently double-count its own evidence and overstate its
coverage.

The same discipline caught the most serious error in this dataset: an exposure
figure attributed to a real regulatory document that appeared nowhere in it. It
was found by re-reading the 181-page source, not by checking the row for
plausibility. Nothing internal to a dataset can catch that class of error.

---

## Tooling notes, so the next round does not lose the time

- `accessdata.fda.gov` returns **HTTP 404 for valid, existing review documents**
  unless a browser User-Agent is sent. Concluding "the document does not exist"
  from a bare 404 there is wrong — and cost this project an entire round, because
  the FDA nonclinical reviews are among the best chronic-neurotoxicity sources in
  existence and were initially recorded as unobtainable.
- The drugs@FDA overview endpoint 404s. Probe the fixed filename suffixes
  directly instead: `IntegratedR`, `MultidisciplineR`, `PharmR`, `MedR`,
  `ClinPharmR`, `StatR`, `SumR`, `OtherR`, `RiskR`, `Approv`.
- `WebFetch` cannot read PDFs — it returns decoded binary. Download with `curl`
  and a browser User-Agent, then extract with PyMuPDF (`import pymupdf`, not the
  deprecated `fitz`).
- ClinicalTrials.gov's JSON API (`/api/v2/studies/<NCT>`) returns per-arm adverse
  event counts with denominators, which is already this dataset's grain and is
  public domain.
- Patent full text read through an HTML mirror **wraps long table cells across
  rows**, silently truncating a 20-mer sequence to 10 nt. Always reconcile a
  parsed sequence against a length declared in the same row.
