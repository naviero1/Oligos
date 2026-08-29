# Methodology — OligoTox-Coagulopathy

Materials and methods for the coagulation-toxicity dataset, NIH/NCATS Oligonucleotide
Toxicity Open Data Challenge, Phase 2.

## 1. Design

This is a **curated dataset**. No wet-lab experiment was performed. The methods below are
therefore of two kinds, kept strictly apart: **(a)** the experimental methods of the source
studies, recorded as each source states them, and **(b)** the curation methods used to
find, extract, verify and harmonise them. Conflating the two would let curation choices
masquerade as experimental fact.

Snapshot: **213 oligonucleotides · 2,388 measurements · 941 per-position modification
records · 75 sources.**

## 2. Scope — what counts as this endpoint

Included: clotting times (aPTT, PT/INR, TT, ACT), fibrinogen, D-dimer, thrombin generation,
coagulation-factor and antithrombin activity, anti-Xa/anti-IIa activity, and bleeding or
thrombotic outcomes a source attributes to a coagulation defect.

Excluded, deliberately: **platelet count alone**. Thrombocytopenia is a separate Challenge
endpoint with its own dossier at [`../thrombocytopenia.md`](../thrombocytopenia.md). A
platelet-related row appears here only where the source ties it to a cascade readout, and
says so in `notes`. This boundary was set before extraction, after finding that the
repository's largest existing store of "coagulation-adjacent" text — 16 hits on one page of
a review already held — is entirely thrombocytopenia and belongs to that endpoint.

Both **unintended coagulopathy** and **on-target anticoagulant/procoagulant pharmacology**
are in scope, on separate flags, because the second is where nearly all published
per-compound clotting numbers live and because bleeding risk from an on-target
anticoagulant is a genuine safety signal. They are never pooled: see README.

## 3. Source identification

Eight independent search axes were run in parallel — mechanism/in-vitro assays; clinical
trials; nonclinical toxicology; siRNA and LNP; aptamers; regulatory labels; patents;
reviews used as a citation map. Each axis was required to **retrieve and open** a candidate
and quote the coagulation passage before reporting it; nothing entered the work-list on the
strength of a title or a search summary. 96 raw candidates were merged to 73 distinct
sources, then triaged into an extraction work-list ranked by whether the source gives
per-compound numbers, per-compound qualitative statements, or class-level prose only.

Two results of that pass are worth recording because they are negative:

- **The project's only previously recorded lead was closed.** `coagulopathy.md` named
  Crooke et al. (2016), *Mol Ther* 24(10):1771–1782, as the single lead for this endpoint,
  on the strength of its title. It was retrieved and read: it does not report the
  per-compound coagulation values the title implies. It is recorded as context, not as a
  source of rows.
- Three sources whose granularity two axes disagreed about were resolved **downward**, to
  qualitative, because their values live only in figure panels.

## 4. Retrieval

All documents were retrieved directly; no value in this dataset comes from a search-engine
summary. This is a deliberate break from the sibling kidney dataset, which was built under
a network policy that blocked outbound fetch and whose own validation file concluded that
its search-derived clinical rows had produced a provenance/outcome confound. Routes used:

| Route | Sources |
|---|---|
| PMC / Europe PMC open-access JATS full text | 27 |
| NLM DailyMed SPL XML (US prescribing information) | 8 |
| NCBI eutils PubMed abstract (where no open full text exists) | 8 |
| USPTO grant text | 7 |
| Other staged full text and supplementary files | 25 |

Every retrieved document is committed to [`sources/documents/`](./sources/documents/), so
each row's evidence can be re-read from the repository without network access. One
supplementary PDF could not be retrieved; the 14 rows citing it are flagged and excluded
from source verification rather than quietly passed.

## 5. Extraction

Sources were divided into 14 bundles by compound family and document type, and read
individually. Extraction rules, enforced by the output contract:

- Every measurement carries a **verbatim quote** and an **exact locus** (table number,
  figure panel, section heading, label section, page). A row that could not be quoted was
  not written.
- **No value was read off a figure.** Where a number exists only in a plotted panel, the
  row carries `NOT_REPORTED` with `readout_is_qualitative = TRUE`. This cost real yield —
  one source's entire PT/aPTT time course is a figure — and the loss is recorded rather
  than recovered by pixel-reading.
- **Per-position chemistry is transcribed, never modelled.** A `modifications` row exists
  only where the source publishes position-resolved chemistry, and each row records in
  `basis` how the position was determined, normally the source's own case legend quoted
  verbatim.
- Severity is recorded **in the source's own words**; no grade was assigned during
  extraction.

## 6. Oligonucleotide identity, purity and characterisation

The Challenge requires the methods used to purify and characterise oligo identity. The
compounds were synthesised by the source laboratories, so what can be reported is what each
source states, and `purity_pct` is **`NOT_REPORTED` for all 213 compounds**. No purity
value was estimated, inferred from a synthesis platform, or carried across from another
compound. Where a source states a synthesis platform, purification method or identity
confirmation, it populates `synthesis_platform`, `purity_method` and
`identity_confirmation`. This absence is a property of the published literature, not of the
curation: per-compound purity is almost never published alongside toxicity results.

Identity here means the printed sequence together with its per-position chemistry.
97 of 213 compounds have a published sequence; 47 have position-resolved chemistry. QC
checks that every declared length equals the actual string (plus any documented terminal
residue) and that every modification row's nucleobase matches the sequence at that
position.

## 7. Harmonisation and grading

Categorical fields use the controlled vocabularies in [`schema.md`](./schema.md). Grading
is mechanical, from the control-referenced ratio, by **CTCAE v5.0** cut-offs — a published
standard, not thresholds invented here — and only for the readouts CTCAE defines. 942 of
2,388 rows are graded; the remaining 1,446 each state in `grade_basis` why no published
rule applies. The one deviation, applying CTCAE's limit-of-normal ratios to a
matched-control ratio, is named in every graded row's `grade_basis` so it cannot be
overlooked. All grades are `provisional`.

## 8. Predictor variables and their distribution

| Variable | Distribution (n = 213 compounds) |
|---|---|
| Class | aptamer 59 · ASO gapmer 58 · other 36 · GalNAc-siRNA 28 · siRNA 13 · tcDNA-ASO 7 · PMO 4 · polydisperse ssDNA 3 · ASO mixmer 2 · CpG ODN 2 · SSO 1 |
| Backbone | not reported 98 · full-PS 57 · mixed PO/PS 34 · full-PO 14 · PMO-neutral 4 · other/NA 4 |
| Sequence published | 97 / 213 |
| Position-resolved chemistry | 47 / 213 (941 position records) |

## 9. Indicator variables and their distribution

| Variable | Distribution (n = 2,388 measurements) |
|---|---|
| Readout category | clotting time 1,160 · factor activity 387 · bleeding outcome 240 · thrombotic outcome 220 · fibrinogen 144 · platelet–coagulation crosstalk 83 · anticoagulant activity 76 · thrombin generation 47 · fibrinolysis marker 31 |
| Readout (top) | aPTT 599 · PT 376 · fibrinogen 140 · FXI activity 108 · antithrombin activity 75 · TT 37 · ACT 25 |
| Study type | animal in vivo 1,430 · clinical 453 · in vitro 297 · ex vivo human plasma 205 |
| Species | human 850 · monkey 818 · mouse 569 · rat 33 · pig 21 · minipig 17 · other 11 · not applicable 69 |
| Effect direction | increase 720 · no change 604 · decrease 556 · not reported 508 |
| Grade | ungraded 1,446 · 1 → 462 · 0 → 382 · 2 → 72 · 3 → 26 |
| Axis | on-target only 1,576 · unintended only 300 · both 144 · neither 368 |

**On negative controls.** 604 rows carry a measured null (`effect_direction = no_change`),
and they are the class most at risk of meaning "nobody looked". The extraction contract
required that a null be written only where the source reports a measured null, with
reporting silence recorded separately in `notes`; the verification pass in
[`coagulopathy.md`](./coagulopathy.md) tested this stratum specifically, because a prior
review of the sibling kidney dataset found its negative class was substantially
"nobody looked" rather than "looked and found nothing".

## 10. Quality control

Two committed scripts, both exiting non-zero on failure:

- `validate_dataset.py` — 36 structural checks (keys, referential integrity, vocabularies,
  grade reproducibility, sequence/modification consistency, roll-ups). All pass. Three
  defects it caught during the build, and their fixes, are logged in `schema.md`.
- `verify_against_sources.py` — re-reads the committed documents and confirms every numeric
  readout appears in the source its row cites. **1,862 / 1,862 located.**

Structural QC proves internal consistency; source verification proves the numbers were not
invented. Neither proves a number was read from the *right* cell — that is the semantic
verification pass, recorded in the dossier.

## 11. Limitations

Stated in full in [`README.md`](./README.md#known-limitations). In brief: grades are
provisional and mechanical; no clinical compound has a published sequence; PMO chemistry
rests on regulatory silence rather than a measured null; prothrombotic rows come
overwhelmingly from one compound family; the quantified PS class effect rests
overwhelmingly on one study; figure-only values were not digitised.

## 12. Reproducibility

Deterministic and fully committed. From a clean checkout, with no network access:
`build_dataset.py` → `validate_dataset.py` → `verify_against_sources.py`. The build reads
the committed extraction records in `sources/extraction/` and writes `data/`; it uses only
the Python standard library. Every number in this document and in `README.md` is
recomputable from `data/`.

## 13. Intended use for predictive modelling

The four-table design exposes sequence, per-position chemistry and design predictors
against graded, per-condition coagulation outcomes. The two axis flags are not optional
metadata: any model trained across `on_target_effect = TRUE` rows without them will learn
that anticoagulant drugs prolong clotting times, which is true, circular and useless for
safety prediction. The intended target is the **unintended** class — the
hybridization-independent, Cmax-driven prolongation associated with phosphorothioate
content — with the on-target rows serving as a mechanistically-explained positive class and
the 604 measured nulls as negatives.
