# For German's ruling — DEVOTE (NCT04089566), nusinersen

**Prepared by Rocksteady/thrombocytopenia, 2026-10-03. Commit `989a581`.**
**Not classified. No label assigned, no row created, nothing ingested.**

Crank's delegation assigns this endpoint to "prepare DEVOTE (NCT04089566) **for German's ruling —
do not classify it yourselves**." This file is the packet. The decision at the end is German's and
is deliberately left open.

---

## Why this trial is on your desk

`SCIENTIFIC_RULES.md` §E defines a clean clinical negative as requiring **all** of: exact sequence,
human exposure, adequate dose and duration, explicit monitoring, an explicit outcome, and a
traceable denominator. DEVOTE appears to satisfy every one of those six. If that reading holds, it
would be the **first** such record in this endpoint, against a standing count of **zero**.

That is exactly why I am not ruling on it. §H records the sequence-only clinical classifier as
BLOCKED *because* there are zero clean sequence-linked clinical negatives. A record that could
change that premise is not a curation call.

## The trial, from the registry

| | |
|---|---|
| Registry | **NCT04089566**, verified live (HTTP 200, 465,681 bytes) |
| Title | *Escalating Dose and Randomized, Controlled Study of Nusinersen (BIIB058) in Participants With Spinal Muscular Atrophy* |
| Acronym | DEVOTE · **Phase 3** · status **COMPLETED** · `hasResults: **True**` |
| Design | Randomized, double-blind, with an active comparator arm |
| Enrollment | **145 actual** |
| Route | **Intrathecal** — note this, it matters below |

## The pre-specified platelet outcome, verbatim

> **"Percentage of Participants With a Postbaseline Platelet Count Below the Lower Limit of Normal
> on at Least 2 Consecutive Measurements"**
> Timeframe: *Baseline up to Day 302*. Reported as PRIMARY for Parts A and C, SECONDARY for Part B.

This is a **pre-specified outcome with a stated threshold rule** (below LLN on ≥2 consecutive
measurements), not an adverse-event-table mention. Posted results, so **public domain**.

### Posted values, with denominators from the participant-flow module

| Part | Arm | Started (n) | Platelet < LLN ×2 consecutive |
|---|---|---:|---:|
| A | nusinersen 28/28 mg | 6 | **0 %** |
| C | nusinersen 50/28 mg | 40 | **2.5 %** |
| B | infantile-onset, 12/12 mg | 25 | **4 %** |
| B | infantile-onset, 50/28 mg | 50 | **0 %** |
| B | later-onset, 12/12 mg | 8 | **0 %** |
| B | later-onset, 50/28 mg | 16 | **0 %** |

Supporting monitoring in the same trial, also pre-specified and posted: hematology shift tables
(explicitly *"complete blood cell count, with differential and platelet count"*), and coagulation
shift tables for aPTT, PT and INR. **11 of 79 posted outcome measures** carry a
safety/platelet/coagulation term.

## The construct, as this dataset holds it

| | |
|---|---|
| `oligo_id` | TOLG240 |
| `sequence_5to3` | `TCACTTTCATAATGCTGG` (18-mer) |
| `modification_map` | `eT*eC(5m)*eA*eC(5m)*eT*eT*eT*eC(5m)*eA*eT*eA*eA*eT*eG*eC(5m)*eT*eG*eG` |
| notation | `rocksteady_v1` — **composed, not source-verbatim** |
| backbone / ps_count | `full_PS` / 17 |
| `purity_pct` | **TBD** · `purity_method` recovered (IP-HPLC-UV-MS, full-length-product purity) |
| `scientist_disposition` | **NOT_ADJUDICATED** |
| `clinical_model_eligibility` | NO (default for unadjudicated) |

## What argues for, and against, treating this as a qualified negative

Stated as a balance because the balance is the decision, not an answer.

**For**
- Pre-specified outcome with an explicit threshold rule and a defined observation window (Day 302).
- Traceable per-arm denominators from the participant-flow module.
- Randomized, double-blind, phase 3, completed, with an active comparator.
- Public-domain posted results — no rights question at all.
- Exact sequence is known and chemistry is position-resolved.

**Against, or at least unresolved**
1. **Non-monotonic dose response.** 4 % at 12/12 mg against 0 % at 50/28 mg in the same
   infantile-onset population, and 0 % at 28/28 mg against 2.5 % at 50/28 mg in Parts A/C. A
   negative label on the high-dose arms sits beside a non-zero low-dose arm. That pattern needs a
   scientific reading, not an arithmetic one.
2. **Route.** Nusinersen is **intrathecal**. Every other compound in this endpoint's clinical lane
   is subcutaneous or intravenous. Systemic platelet exposure after intrathecal dosing is not
   obviously comparable, and §E's "adequate dose and duration" may not transfer across route
   classes.
3. **Small arms.** Part A n=6 and later-onset 12/12 mg n=8. A 0 % rate on n=6 is weak evidence of
   absence, and §E warns specifically against manufacturing a balanced class.
4. **Paediatric population** — SMA infantile and later-onset. Whether a paediatric platelet
   reference range supports the same LLN rule as the adult trials in this lane is a scientific
   question.
5. **The construct's position chemistry is composed, not source-verbatim** (0 of 34 clinical
   compounds in this endpoint have a verbatim map). §G warns that reference identity is not
   experimental-batch identity.
6. **The compound is `NOT_ADJUDICATED`.** It has no disposition at all in v0.9's 45-record set.

## The decision requested

1. **Does DEVOTE satisfy the six-criterion clean-negative test in §E?** If yes, this endpoint's
   qualified-clinical-negative count moves off zero, which bears directly on §H's rationale for
   blocking the sequence-only classifier.
2. **If yes, at what grain?** Per-arm, or trial-level? Does the 4 % low-dose arm disqualify the
   trial, qualify as a separate positive, or stand as an endpoint-specific finding?
3. **Does intrathecal exposure qualify** for this endpoint's clinical lane, or does it belong in a
   separate route-class lane?
4. **What is nusinersen's disposition** and its model eligibility, if any?

## What happens meanwhile

Nothing. No row is created, no grade is assigned, no eligibility is changed, and the classifier
stays blocked. The registry JSON is retrievable at
`https://clinicaltrials.gov/api/v2/studies/NCT04089566` and the values above can be re-read from
its `resultsSection.outcomeMeasuresModule` without trusting this file.

The one thing I would flag as time-sensitive: these are **public-domain posted registry results**,
so whatever you rule, this material carries no rights encumbrance — unlike roughly 224 rows
currently awaiting a licence decision.
