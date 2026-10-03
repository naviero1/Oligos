# German — interpretation needed: what an absence from a required table is

**From:** Rocksteady (hydrocephalus) · **cc:** Crank, Beebop, Oscar
**Date:** 2026-10-03 · **Release:** `hydrocephalus-<commit>` (figures below from `qc/stats.json`)
**Status:** nothing re-graded, re-labelled or deleted. This is a request for a reading.

---

## 1. The figure, and why it is the largest single number at this endpoint

`data/measurements.csv` holds 1,114 rows graded 0. That is 83% of the dataset and it is
what makes this endpoint look like it has a large negative class. It decomposes:

| Basis for the grade 0 | Rows | `ascertainment` as recorded |
|---|---:|---|
| No tier-A term in a trial's **posted serious-adverse-event table** | 507 | `measured_null` |
| No matching statement in a **prescribing information** | 76 | `measured_null` |
| No **FAERS** report for this drug carries the reaction term | 411 | `reported_zero_no_denominator` |
| An **explicitly reported count of 0** in a results table | 113 | `measured_null` |
| Other (protective direction, within-patient negative, designed control) | 7 | mixed |

So **583 rows are stamped `measured_null` on the strength of an absence**, and only
**120 rows** rest on something other than an absence of any kind.

## 2. The two readings, stated fairly

**§E of `SCIENTIFIC_RULES.md`** says, in terms, that a no-event mention or an absence
from an adverse-event table is not a negative. Read strictly, the 583 rows are not
measured negatives and `ascertainment = measured_null` overstates them.

**§9 of this release's `METHODOLOGY.md`** argues the opposite for the 507: 42 CFR
11.48(a)(4)(ii)(A) requires a posted serious-adverse-event table to list *all* serious
adverse events **with no frequency threshold**, unlike subparagraph (B) which sets 5% for
non-serious ones. If the table is complete by law, then the absence of a tier-A term from
it is a reported zero *for serious events*, not silence. The regulation text is committed
at `sources/raw/ecfr_42CFR11.48_results_reporting.xml` and cited in every affected row.

**I am not neutral about which is more defensible, and I should be clear that I was the
one who decided it.** `METHODOLOGY.md` records OI-01 as "RESOLVED in this release" on that
reading. That was an evidentiary ruling made by an agent, which §A reserves to you. The
reading may well be right. It is not mine to close.

## 3. What the reading changes, precisely

**It does not change any model.** No grade and no `ascertainment` value is a feature or an
outcome in `ml/analyse.py`. The outcome is `tierB_event_nonprocedure`, built from
`n_affected` counts; the features are route, indication, oligo class and backbone
chemistry plus two identity probes. A ruling moves no AUC.

**It changes what the dataset claims to contain**, which is the part that bears on
"Experimental design including positive/negative control oligos" and on any downstream
negative-class work:

- Under the §E reading, this endpoint has roughly **120 negatives**, not 1,114, and the
  release must say so wherever it describes its negative class.
- Under the CFR reading, it has 583 + 113 = **696 serious-event negatives** plus 411
  weaker pharmacovigilance absences, with the limits already stated per row: the absence
  is evidence about *serious* events only, and is never evidence that imaging was done.

**It also settles a live internal contradiction.** `SCHEMA.md` says grade 0 *requires*
`ascertainment = measured_null`; `scripts/data_dictionary.py` says grade 0 is *permitted*
on `measured_null` **or** `reported_zero_no_denominator`, and `qc/validate.py` enforces the
permissive version — so the 411 FAERS rows satisfy the code and violate the schema
document. Both cannot stand. The contradiction is now disclosed in `SCHEMA.md` rather than
silently carried, and whichever way you rule, one of those two files changes.

## 4. The question, in three parts

1. **Does the 42 CFR 11.48(a)(4)(ii)(A) completeness argument survive §E, for the 507
   rows?** If it does, is `measured_null` the right value, or should those rows take a
   distinct value — `reported_zero_serious_events_only`, say — that records *what kind* of
   zero it is rather than borrowing a word that means "assessed and found absent"?
2. **Do the 76 prescribing-information rows ride with them or not?** A label is not bound
   by 11.48, so the completeness argument does not reach them. They may be a weaker class.
3. **Which document is wrong on grade 0** — `SCHEMA.md`'s "requires `measured_null`" or
   `data_dictionary.py`'s permissive rule? This is the same question in schema clothing,
   so answering (1) probably answers it.

## 5. What I am explicitly not asking for

- **Not** permission to delete rows. Every one of them is a sourced observation with a
  locator, and the absence itself is a fact about the record.
- **Not** permission to relabel them negative-to-positive or to strip the grade. They stay
  `grade_status = provisional`.
- **Not** a binary. If the right answer is a third value, or a split, or "keep it and
  change the wording", that is a better answer than either side of a yes/no.

## 6. Where the numbers come from

Every figure above is in `qc/stats.json` under `grade0_rows`, `grade0_by_basis`,
`grade0_reported_zero_rows`, `grade0_absence_measured_null_rows` and
`grade0_not_absence_rows`, computed by `qc/validate.py` from `grade_basis` and
`ascertainment`, and rendered into the documents rather than typed. The decomposition
rule is in that script so you can check the classification, not just the totals.
