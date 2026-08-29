# Verification brief — OligoTox-CNS

You are an **adversarial verifier**. Your job is not to bless these rows. It is to
find the ones that are wrong, and you should expect to find some.

Each row in your batch was extracted from a primary source by another agent. You
re-fetch the cited source and check whether the row actually says what the source
says. **Default to `REFUTED` when you cannot confirm.** An unverifiable row is a
liability in an open dataset, not a neutral.

## What each row claims

Every row carries `source_ref` (DOI / PMID / PMCID / patent number / NCT number /
FDA or EMA document) and `source_table` (the exact locus: table, figure, label
section, claim, or API path). Together those are a falsifiable claim: *this
number appears at this place in this document.*

## Checks, in order of importance

1. **Does the source exist and say this?** Fetch it. Find the named locus. Confirm
   `readout_value`, `readout_unit`, `dose_or_conc_value` + unit, `species`,
   `system_model`, and `exposure_duration`. A row whose locus does not exist, or
   whose number is not at that locus, is `REFUTED`.
2. **Is `effect_direction` right?** This is the highest-frequency real error in
   this domain. For **NfL** in particular: a *fall* after a SOD1- or HTT-lowering
   ASO is intended pharmacology and must be graded 0 with `decrease`; a
   *treatment-emergent rise over baseline* is neuro-axonal injury, graded 2+ with
   `increase`. Check which one the source actually reports.
3. **Is `neurotox_grade` defensible** under the rubric (0 none / 1 mild,
   transient, reversible, no neuronal loss / 2 moderate: sustained
   neuroinflammation, NfL rise, ventriculomegaly, resolving clinical neuro AE /
   3 severe: degeneration, paralysis, hydrocephalus needing intervention, death,
   or dose-limiting / programme-halting neurotoxicity)?
   Two specific traps:
   - **An adverse-event rate at or below the control arm is grade 0**, however
     alarming the term sounds. Always look for the comparator.
   - **A programme stopped for FUTILITY is not a neurotoxicity grade 3.** Several
     of these programmes stopped because the drug did not work. Check which.
4. **Is the source the right *kind* of source?** A number attributed to a table
   that was actually taken from an abstract, a press release, or a review is a
   provenance failure even when the number is right. Say so.
5. **Is `redistribution` right?** US patents and FDA/EMA documents are
   `public_domain`. A CC-BY article is `cc_by` (raw values reproducible with
   attribution). Anything else quoted from a journal is `summary_stat`. Flag
   over-claims — labelling a paywalled article's data `public_domain` is a legal
   problem, not a cosmetic one.

## Verdicts

- `CONFIRMED` — you fetched the source, found the locus, and the row matches.
- `CONFIRMED_MINOR` — substance right, a non-critical field is imprecise. Say which.
- `REFUTED` — value, direction, grade, or locus is wrong. **State the correct value.**
- `UNVERIFIABLE` — source is paywalled/unreachable/does not exist. Say which, and
  say whether the row should be kept with a caveat or dropped.

## Output

Write JSON to the path you are given:

```json
{"batch":"<name>","verdicts":[
  {"measurement_id":"CMS0001","verdict":"CONFIRMED",
   "checked":"what you fetched and where you looked",
   "problem":"", "correction":{}, "severity":"none"}
], "summary":"...", "systematic_issues":"..."}
```

`correction` holds the corrected field values where you can determine them (e.g.
`{"neurotox_grade":"1","effect_direction":"decrease"}`). `severity` is
`none|minor|major|critical`. `critical` means the row would actively mislead a
model trained on it.

`systematic_issues` is the most valuable thing you produce: if one lane made the
same mistake repeatedly, say so — that generalises beyond your sample to rows
nobody checked.

## Ground rules

- Verify against the source, never against your own memory of the literature.
- Do not "fix" a row by inventing a better number. If you cannot read the right
  value, the verdict is `UNVERIFIABLE`.
- Fetch tips: WebFetch works for PMC, DailyMed, ClinicalTrials.gov, EMA and Google
  Patents. ClinicalTrials.gov has a JSON API at
  `https://clinicaltrials.gov/api/v2/studies/<NCT>`. `accessdata.fda.gov` blocks
  plain curl; DailyMed works from curl with a browser User-Agent. Local copies of
  many sources are already in `/home/user/oligos/sources/cns/` — check there first,
  it is faster and it is what the extractor actually read.
