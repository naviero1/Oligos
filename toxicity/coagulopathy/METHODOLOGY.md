# Methodology — OligoTox-Coagulopathy

Materials and methods for the coagulation-toxicity dataset, NIH/NCATS Oligonucleotide
Toxicity Open Data Challenge, Phase 2.

## 1. Design

This is a **curated dataset**. No wet-lab experiment was performed. The methods below are
therefore of two kinds, kept strictly apart: **(a)** the experimental methods of the source
studies, recorded as each source states them, and **(b)** the curation methods used to
find, extract, verify and harmonise them. Conflating the two would let curation choices
masquerade as experimental fact.

Snapshot: **<!--N:n_oligos--> oligonucleotides · <!--N:n_meas--> measurements · <!--N:n_mods--> per-position modification
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

Until 2026-10-03 this section reported `purity_pct` as `NOT_REPORTED` for every compound and
blamed the literature. **That was wrong and the error was ours:** earlier extraction read the
*clinical* sections of the EMA assessment reports and FDA integrated reviews already held in
`sources/documents/` and never opened their Quality/CMC sections. Nothing had to be acquired.

Recovery used eleven parallel extraction passes, one per compound programme, each checked by
an independent pass that string-matched every quote against the cited file and every purity
value against a printed purity context. Eight verified clean; three reported metadata defects
(a spliced quote, two page misattributions, one unsupported claim about redaction markers),
each corrected in `sources/characterisation.json` with the correction recorded in the record.
Those checks now run inside `verify_against_sources.py` on every build.

**Two distinctions carry the result.** A public EPAR *names* every purity and impurity test
and *withholds* the numeric limit — volanesorsen's active-substance specification lists
purity, specified and unspecified impurities and total degradation products, all by
IP-HPLC-UV-MS, with no limit printed for any. That is `purity_limits_redacted = TRUE` with
`purity_pct` left `NOT_REPORTED` on 12 compounds: a withheld limit is a finding, never a
value. And a purity value belongs to a **lot** — fitusiran 98.5% (lot P07916), olezarsen
91.3% (drug substance CA678354-002), tofersen 90% (TA666853-008) and 94% (TA666853-001), all
tested batches. Tofersen therefore carries no single `purity_pct`; both values sit in
`purity_batches` and the basis says why. A drug-substance specification is likewise never
spread across batches, and QC fails the build if a compound with several lot purities reports
a single one.

Coverage, against the denominator that matters — the 38 compounds actually dosed in people,
with the whole roster for comparison:

| | all 218 | 38 dosed in participants |
|---|---:|---:|
| sequence as printed | 121 | 14 |
| position-resolved chemistry | 52 | 11 |
| purity value | 2 | 2 |
| purity test named, limit withheld | 12 | 12 |
| purity method named | 46 | 11 |
| identity confirmation | 32 | 16 |

Counterion is recorded for 17 of the 38, purification or manufacture for 14, impurity classes
for 12 and other characterisation tests for 16. Against the previous release that is 0→2
purity values, 1→11 named methods, 3→16 identity confirmations and 0→14 purification records
on the clinically dosed subset. It remains **thin**, and the two worst gaps are untouched:
only 14 of 38 have a printed sequence and only 11 have position-resolved chemistry.

The recovered methods are consistent across sponsors. **Identity** — accurate mass by MS
within an IP-HPLC-UV-MS run; sequence confirmation by thermal melting temperature; failure-
sequence analysis of crude material by IP-HPLC-TOF-MS; structure elucidation by ¹H, ¹³C and
³¹P NMR with high-resolution ESI-TOF. **Purity** — one IP-HPLC-UV-MS method determines assay,
purity and impurities together, with impurities specified as *groups* rather than individual
components. **Other attributes** — counterion by ICP-OES, elemental impurities by ICP-MS,
water by Karl Fischer, residual solvents by GC, endotoxin and microbial limits by Ph. Eur.
One fact deserves emphasis: a 20-mer full-phosphorothioate is a mixture of 2¹⁹ (524,288)
diastereoisomers, no individual isomer above roughly 0.0018% of the total. **"The sequence"
and "the molecule" are not the same thing for a phosphorothioate**, and a model treating a PS
sequence as one species is modelling a mixture.

Identity here means the printed sequence plus its per-position chemistry. QC checks that every
declared length equals the actual string (plus any documented terminal residue) and that every
modification row's nucleobase matches the sequence at that position. No purity value was
estimated, inferred from a synthesis platform, or carried across compounds; regulatory-derived
and publication-derived values are held in separate columns.

## 7. Harmonisation and grading

Categorical fields use the controlled vocabularies in [`schema.md`](./schema.md). Grading
is mechanical, from the control-referenced ratio, by **CTCAE v5.0** cut-offs — a published
standard, not thresholds invented here — and only for the readouts CTCAE defines.
<!--N:n_graded--> of <!--N:n_meas--> rows are graded; the remaining <!--N:n_ungraded--> each
state in `grade_basis` why no published
rule applies. The one deviation, applying CTCAE's limit-of-normal ratios to a
matched-control ratio, is named in every graded row's `grade_basis` so it cannot be
overlooked. All grades are `provisional`.

## 8. Predictor and indicator variables

The variables themselves are defined in `schema.md`, their definitions are in the
`data_dictionary` sheet of the workbook, and their **distributions are reported in the
narrative document** (section 4), which is where the Challenge asks for them. They are
computed from the tables at build time in both documents, never transcribed.

**On negative controls.** <!--N:n_null--> rows carry a measured null
(`effect_direction = no_change`) — the class most at risk of meaning "nobody looked". The
extraction contract required a null only where the source reports a measured null, with
reporting silence recorded separately in `notes`, and verification tested this stratum
specifically because a prior review of the sibling kidney dataset found its negative class
was substantially "nobody looked". **That defect does not repeat here**: four independent
reviewers tried to break the null class and could not.

`control_class` records the reference each row was compared against. Vehicle, buffer and
placebo rows dominate; the sequence-matched negative control — a scrambled or
reverse-complement oligo, the only control that separates a sequence effect from a chemistry
or formulation effect — is present on <!--N:n_seqctrl--> rows. That number is small and is
stated rather than smoothed over.

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
