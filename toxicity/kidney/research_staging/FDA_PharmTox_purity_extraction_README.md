# FDA Pharmacology/Toxicology purity extraction — for all endpoints

**Owner:** Rocksteady / kidney, assigned by Crank 2026-10-03.
**File:** `FDA_PharmTox_purity_extraction_2026-10-03.csv` — **54 lot-value assertions** drawn from
four FDA Pharmacology/Toxicology reviews.
**Status: staged research output. Nothing here is ingested, promoted or adjudicated.**

This exists because `accessdata.fda.gov` was recorded project-wide as blocked. It is not. It is
**user-agent gated**: the default `curl` agent receives HTTP 404 and a 420-byte apology page, a
browser agent receives the document. Any endpoint whose register says "Drugs@FDA — blocked" can
retrieve these.

## What this is, and the words to use for it

Each row is **one assertion, from one printed line, on one page, in one review.** The material is a
**nonclinical tested-material lot** — the lot of test article used in a specific nonclinical study.

**It is not "animal-study lot".** I used that phrase first and it is wrong: the studies include
human-derived systems (human hepatic microsomes pooled from 50 donors; primary human hepatocytes
from 3 donors) and bacterial systems (Ames reverse-mutation assays). The `test_system` column
records what the source text supports, and `not_determined_from_source_text` on 38 of 54 rows means
exactly that — not "animal".

**It is not clinical-lot purity.** No row here describes material given to a human subject.

## Rules this extraction follows, and asks you to keep

- **No averaging.** Where one lot carries different values in different places, each is a separate
  row. Golodirsen lot `7001257` appears as 92% and 91% on different pages of its own review and as
  91% in the casimersen review. Three assertions, not one lot with a note.
- **No capping and no global propagation.** A value is recorded as printed, attached to the study it
  was printed in. Do not lift it to the oligo, to a sibling study, or to a clinical lot.
- **Attribution follows the test article, not the review.** `SRP-4053` (golodirsen) appears inside
  the casimersen review; it is attributed to golodirsen with `review_subject_drug = casimersen`.
- **One row is not a kidney oligo at all.** `ISIS 401724` appears as a comparator; it is labelled
  `ISIS_401724_NOT_on_kidney_roster` and carries no `kidney_oligo_id`.

## The quarantine — 14 rows, and what is *not* claimed about them

14 assertions report a value **above 100 per cent**. They carry
`value_status = QUARANTINED_exceeds_100_percent` and must not be ingested as purity.

**The cause is not determined by this extraction, and no explanation is offered.** A value above
100% cannot be a proportion of material, but naming what it *is* — assay, content, potency against
a reference standard, or something else — would be an inference from the number alone. That is
German's to rule on.

One observation is recorded because it is measured rather than inferred, and whoever rules on this
will want it:

> For inotersen, the separation is complete across all 17 of its assertions. **All 12 values above
> 100% are attached to a formulated preparation at a stated concentration** (`RP420915-009,
> 0.3 mg/mL, 102.7%`). **All 5 values at or below 100% are attached to a lot identifier with no
> concentration** (`Lot CA420915-001, 91.9%`). The same page can carry both forms.

That is a correlation in the printed text. It is not an explanation, and it is not generalised to
the casimersen (101%) or viltolarsen (100.9%) entries, which are lot-identifier-only and therefore
do not fit the pattern.

## Columns

| column | meaning |
|---|---|
| `assertion_id` | `FDAPURnnn`, unique within this file |
| `attributed_drug` / `kidney_oligo_id` | which molecule the **test article** is; the oligo id is kidney's local identifier and will not match yours |
| `test_article_as_printed` / `lot_as_printed` | exactly as the source prints them |
| `entry_form` | `lot_identifier_only` or `formulated_preparation_at_stated_concentration` |
| `reported_value_as_printed` | the number as printed, not normalised |
| `value_status` | `as_printed` or `QUARANTINED_exceeds_100_percent` |
| `material_class` | always `nonclinical tested-material lot` |
| `test_system` | derived from the study title/section text; `not_determined_from_source_text` where the text does not say |
| `source_document`, `review_subject_drug`, `pdf_page_index`, `study_number`, `study_title` | the locator |
| `lot_value_pairing` | how a lot was matched to a value — `positional_1to1`, `one_value_many_lots`, `regex_pair`, `lot_keyword` |
| `source_line_as_printed` | the printed line, so you can check the parse |

`pdf_page_index` is the **page index within the PDF**, 1-based, not the printed page number — the
reviews carry their own internal numbering and the two differ.

## Coverage and what is not here

| review | NDA | assertions |
|---|---|---|
| casimersen | 213026 | 16 |
| golodirsen | 211970 | 13 |
| inotersen | 211172 | 17 |
| viltolarsen | 212154 | 8 |

Only these four reviews were swept, and only for purity. `217388` (eplontersen) and `219019`
(nedosiran) were not located under the probed URL patterns. The inotersen review additionally
contains HPLC ×21, LC-MS ×3, mass spectrometry ×4, capillary gel electrophoresis and a dedicated
impurity-qualification study — **analytical identity material that this sweep did not extract.**

If your endpoint holds an oligo with an approved US application, the same route will probably reach
its review. Tell me the application number and I will add it rather than have you re-derive the
method.

## Reproducing it

Source PDFs are not committed — they are US federal work products and therefore public domain, but
they are large. `logs/acquisition_manifest.json` carries each URL, retrieval date, byte size and
SHA-256. Re-fetch with a browser user agent and check the hash; all four were re-fetched during this
work and matched byte for byte.
