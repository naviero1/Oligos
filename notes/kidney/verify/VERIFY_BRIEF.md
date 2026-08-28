# Verification brief — OligoTox-Kidney

You are an **adversarial verifier**. Your job is not to bless these rows. It is to
find the ones that are wrong, and you should expect to find some. In the
companion CNS dataset, an identical exercise refuted 149 of 412 sampled rows.

## Why these rows specifically

Every row in your batch carries `source_id = WS`. That flag means the value was
taken from a **search-engine summary**, not from the full text — the session that
created them had no outbound web access. `METHODOLOGY.md` §4 path 3 commits to
verifying them against the cited primary source **before publication**, and that
promise has not yet been kept. Network access now works, so it can be.

Treat them as unproven claims, not as data needing a rubber stamp.

## What each row claims

`source_ref` names the document and `source_table` the exact locus. Together they
are a falsifiable claim: *this finding appears at this place in this document.*
Note that many of these `source_ref` values are **slugs rather than identifiers**
(`Yu2012_Toxicology_ISIS113715_monkey`, `Alicaforsen_review_ScienceDirect`). Part
of your job is to resolve each to a real DOI, PMID, PMCID, patent number, NCT
number or FDA application number — or to report that it does not resolve, which
is itself a finding.

## Checks, in order of importance

1. **Does the source exist and say this?** Find the named locus. Confirm the
   finding, the species, the model, the dose and the readout. A row whose source
   cannot be found, or whose claim is not at that locus, is `REFUTED`.
2. **Is the finding real, or is it absence of evidence?** Many of these rows
   assert a negative — `no_signal`, `none`, `no_change`, graded 0. A negative is
   only legitimate if the source **measured** renal function and found nothing.
   "The label does not mention kidney toxicity" is silence, not a measured
   negative, and a grade-0 row resting on silence teaches a model a false
   negative. This is the single most likely error class in your batch: check
   every grade-0 row for whether anything was actually measured.
3. **Is `nephrotox_grade` defensible** under the rubric (0 none / 1 mild,
   functional, reversible, no viability loss / 2 moderate: injury-biomarker
   elevation or histopathology / 3 severe: AKI, glomerulonephritis, renal
   failure, dose-limiting)? Two traps:
   - **An adverse-event rate at or below the control arm is grade 0**, however
     alarming the term. Always look for the comparator.
   - **Grade 3 requires the source's own words** to denote AKI, renal failure,
     dialysis, glomerulonephritis or a dose-limiting/programme-halting renal
     effect. A serious-adverse-event code is not severity.
4. **Is the finding attributable to the oligonucleotide?** Check for a control
   group, and for confounding by the underlying disease or by the delivery route.
5. **Is `redistribution` right?** FDA/EMA documents and US patents are
   `public_domain`. A CC-BY article is `cc_by` (raw values reproducible with
   attribution). CC-BY-NC and CC-BY-ND are **not** — those stay `summary_stat`,
   because republishing their tables inside a CC-BY dataset would conflict with
   the non-commercial and no-derivatives terms. Read the licence statement in the
   document; do not infer it from the publisher.

## Verdicts

- `CONFIRMED` — you fetched the source, found the locus, and the row matches.
- `CONFIRMED_MINOR` — substance right, a non-critical field imprecise. Say which.
- `REFUTED` — value, direction, grade or locus is wrong. **State the correct value.**
- `UNVERIFIABLE` — source paywalled, unreachable, or does not exist. Say which,
  and say whether the row should be kept with a caveat or dropped.

## Output

Write JSON to the path you are given:

```json
{"batch":"<name>","verdicts":[
  {"measurement_id":"MSR040","verdict":"CONFIRMED",
   "checked":"what you fetched and where you looked",
   "problem":"", "correction":{}, "severity":"none",
   "resolved_source_ref":"doi:10.xxxx/yyyy or PMID:12345678 or NCT01234567"}
], "summary":"...", "systematic_issues":"..."}
```

`correction` holds corrected field values **as bare values only** —
`{"nephrotox_grade":"1","effect_direction":"no_change"}`. Never write a sentence
into a value field: `"nephrotox_grade": "1 unless ..."` is a useful argument and
a corrupted cell. Reasoning goes in `problem` / `checked`.

`resolved_source_ref` is the canonical identifier you established for the source.

`systematic_issues` is the most valuable thing you produce: if the same mistake
recurs, say so — that generalises to rows nobody checked.

## Ground rules

- Verify against the source, never against your own memory of the literature.
- Do not "fix" a row by inventing a better number. If you cannot read the right
  value, the verdict is `UNVERIFIABLE`.
- Fetch tips: `WebFetch` works for PMC, DailyMed, ClinicalTrials.gov, EMA and
  Google Patents, but **cannot read PDFs** — download those with
  `curl -sSL -A "Mozilla/5.0 ... Chrome/124.0 Safari/537.36"` and parse with
  `python3 -c "import pymupdf; ..."`. `accessdata.fda.gov` returns 404 to
  non-browser clients, so a bare 404 there does not mean the document is absent —
  pass the User-Agent and try again. ClinicalTrials.gov has a JSON API at
  `https://clinicaltrials.gov/api/v2/studies/<NCT>`. Local source PDFs already
  live in `/home/user/oligos/sources/kidney/` — check there first.
