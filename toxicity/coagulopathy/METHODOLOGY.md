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

The Challenge requires the methods used to purify and characterise oligo identity. Until
2026-10-03 this section reported `purity_pct` as `NOT_REPORTED` for every compound and
attributed that to the literature: "per-compound purity is almost never published alongside
toxicity results." **That explanation was wrong, and the error was ours.** Earlier
extraction read the *clinical* sections of the EMA assessment reports and FDA integrated
reviews already held in `sources/documents/` and never opened their Quality / CMC sections,
where the purity and identity methods for every approved compound are set out. Nothing had
to be acquired to close this; the evidence was in the repository.

### Method

Eleven parallel extraction passes, one per compound programme, each reading only that
programme's documents, followed by eleven independent verification passes that
string-matched every quote against the cited file and checked every numeric purity against
a printed purity context. Eight programmes verified clean. Three reported defects, all
metadata rather than values — one spliced quote, two page misattributions, one unsupported
claim about redaction markers — and each is corrected in
`sources/characterisation.json` with the correction recorded in the record itself. The
same checks now run inside `verify_against_sources.py`, so the evidence is re-checked on
every build rather than resting on a one-off review.

### What these documents do and do not give

A public EPAR **names every purity and impurity test and withholds the numeric acceptance
limit**. For volanesorsen, for example, the active-substance specification lists purity,
specified impurities, unspecified impurities, total degradation products and total
impurities, all by ion-pair HPLC with UV and mass-spectrometric detection
(IP-HPLC-UV-MS) — and prints no limit for any of them. That is recorded as
`purity_limits_redacted = TRUE` with `purity_pct` left `NOT_REPORTED`: **a withheld limit
is a finding, never a value.** 12 compounds are in that state.

FDA integrated reviews occasionally print a value, and when they do it belongs to a **lot**:

| Compound | Lot | Purity | Basis |
|---|---|---|---|
| fitusiran | P07916 | 98.5% | tested batch |
| olezarsen | lot not named in the quoted passage | 91.3% | tested batch (drug substance CA678354-002) |
| tofersen | TA666853-008 | 90% | tested batch |
| tofersen | TA666853-001 | 94% | tested batch |

Tofersen therefore carries **no single `purity_pct`**. Both lot values are kept in
`purity_batches` and `purity_pct` is `NOT_REPORTED` with the basis
`multiple_lots_reported_with_different_values_see_purity_batches`. Choosing one lot as "the"
compound's purity would transfer one batch's result to every use of that compound, and a
drug-substance *specification* is likewise never spread across batches — `purity_pct_basis`
always says which kind of number it is. A QC check fails the build if a compound with
several lot purities reports a single one.

### Coverage, with the denominators that matter

Phase 2 asks for the purity and characterisation of **each oligo tested**, so the honest
denominator is the subset actually dosed in people, not the whole roster.

| | all 218 | 38 dosed in human participants | 95 in human in vitro systems |
|---|---:|---:|---:|
| sequence as printed | 121 | 14 | 45 |
| nucleobase sequence | 104 | 13 | 43 |
| position-resolved chemistry | 52 | 11 | 3 |
| purity value (single) | 2 | 2 | 1 |
| purity test named but limit withheld | 12 | 12 | 2 |
| purity method named | 46 | 11 | 36 |
| identity confirmation | 32 | 16 | 18 |
| other characterisation tests | 16 | 16 | 3 |
| purification / manufacture | 14 | 14 | 3 |
| counterion | 17 | 17 | 3 |
| impurity classes | 12 | 12 | 2 |

Read against the previous release this is 0/38 → 2/38 for a purity value, 1/38 → 11/38 for
a named method, 3/38 → 16/38 for identity confirmation, and 0/38 → 14/38 for purification.
It remains **thin**, and the two gaps that matter most are unchanged by this work: only 14
of the 38 clinically dosed compounds have a printed sequence, and only 11 have
position-resolved chemistry. No model can learn sequence-dependent toxicity from a compound
whose sequence we do not hold.

### The methods, as the sources state them

For the approved antisense and siRNA compounds the recovered methods are consistent across
sponsors and worth stating plainly, because they are the answer to "how was identity
characterised":

- **Identity** — accurate mass by MS, usually within an IP-HPLC-UV-MS run; sequence
  confirmation by thermal melting temperature (Tm); failure-sequence analysis of crude
  material by IP-HPLC-TOF-MS to confirm the claimed nucleotide sequence; structure
  elucidation by ¹H, ¹³C and ³¹P NMR with high-resolution ESI-TOF.
- **Purity and impurities** — a single IP-HPLC-UV-MS method determines assay, purity and
  impurities together; impurities are specified as *groups* (specified, unspecified, total
  degradation products, total impurities) rather than as individual components.
- **Other attributes** — counterion identity and content by ICP-OES, elemental impurities
  by ICP-MS, water by Karl Fischer, residual solvents by GC, endotoxin and microbial
  limits by Ph. Eur. methods.
- **Diastereomeric composition** — a 20-mer full-phosphorothioate is a mixture of 2¹⁹
  (524,288) diastereoisomers, with no individual diastereoisomer contributing more than
  about 0.0018% of the total. This is stated in the volanesorsen assessment and is a
  property of the chemistry class, not of one compound: **"the sequence" and "the molecule"
  are not the same thing for a phosphorothioate**, and any model treating a PS sequence as
  a single species is modelling a mixture.

Identity here means the printed sequence together with its per-position chemistry. QC checks
that every declared length equals the actual string (plus any documented terminal residue)
and that every modification row's nucleobase matches the sequence at that position.

No purity value was estimated, inferred from a synthesis platform, or carried across from
another compound. Values recovered from a regulatory quality section are marked
`characterisation_basis = regulatory_quality_section:<source_id>`; values already extracted
from publications were not overwritten, and the two provenances are held in separate columns.

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
| Effect direction | increase 702 · no change 573 · decrease 544 · not reported 449 · not applicable (pre-dose baseline) 120 |
| Grade | ungraded 1,521 · 0 → 463 · 1 → 312 · 2 → 66 · 3 → 26 (155 grades flagged `within_reference_range_resolution`) |
| Axis | on-target only 1,576 · unintended only 289 · both 144 · neither 379 |

**On negative controls.** 573 rows carry a measured null (`effect_direction = no_change`),
and they are the class most at risk of meaning "nobody looked". The extraction contract
required that a null be written only where the source reports a measured null, with
reporting silence recorded separately in `notes`; the verification pass tested this
stratum specifically, because a prior review of the sibling kidney dataset found its
negative class was substantially "nobody looked" rather than "looked and found nothing".
**That defect does not repeat here**: four independent reviewers tried to break the null
class and could not — the nulls are measured nulls, and unmeasured endpoints are typed
`NOT_REPORTED` with notes saying so explicitly.

## 10. Quality control

Two committed scripts, both exiting non-zero on failure:

- `validate_dataset.py` — 45 structural checks (keys, referential integrity, vocabularies,
  grade reproducibility, sequence/modification consistency, roll-ups, and nine invariants
  added after verification). All pass. Defects caught during the build, and their fixes,
  are logged in `schema.md`.
- `verify_against_sources.py` — re-reads the committed documents and confirms every numeric
  readout appears in the source its row cites. **1,876 / 1,876 located.**

Structural QC proves internal consistency; source verification proves the numbers were not
invented. Neither proves a number was read from the *right* cell, so a third pass did that
by hand: 174 rows re-checked by reviewers instructed to refute them (117 confirmed, 50
corrected, 2 refuted, 5 unverifiable, no fabrication). Ten defect classes were found and
corrected in the build; the residue is carried as open issues. Both the corrections and the
residue are documented in [`coagulopathy.md`](./coagulopathy.md).

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
