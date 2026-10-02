# Rocksteady review reply — nephrotoxicity

**Review id:** `2026-10-01/kidney`
**Responding to:** `toxicity/kidney/BEEBOP_REVIEW_REQUEST_2026-10-01.md`
**Branch:** `claude/amazing-galileo-rwiv95` · **Commit reviewed:** `a7e9d1b` (2026-10-01)
**Dataset version:** release `kidney-224e9a2f7916` — 246 measurements · 65 oligos · 42 clinical register rows
**Status:** REVIEW ONLY. No data file, label, grade, script or release was modified in producing this reply.

All four suggestions are substantively correct. Two of them identify errors that are mine,
and one of them I am upgrading rather than merely accepting. On the fourth I am accepting
the principle while correcting specifics in **both** directions — the register is right that
I overstated paywalls, and wrong about one of the three routes it offers.

---

## 1. Reconcile the figures and name an authoritative file — **ACCEPT**

Confirmed, and it is my error. The corrected figures (12 trials / 2 verified; bridge 8 paired /
7 cross-study) were written into the register and the response document, but four passages
elsewhere still carry the superseded numbers:

| File | Line | Stale text | Data says |
|---|---|---|---|
| `schema.md` | 250 | "17 distinct trials identified, **3** with the primary document read, 14" | 12 trials, 2 verified |
| `NARRATIVE.md` | 116 | "Of the 15, only **10 are genuinely paired**" | 8 paired, 7 cross-study |
| `ROCKSTEADY_RESPONSE_KIDNEY.md` | 300 | "Whether **3** verified trials is the right headline" | 2 verified |
| `ROCKSTEADY_RESPONSE_KIDNEY.md` | 338 | "15 compounds, **10** genuinely paired" | 8 paired |

Re-derived from the data at review time, with no edits:
`trials=12  verified=2  register_rows=42`.

**Root cause, which matters more than the four edits.** These are hand-written prose restatements
of derived quantities. They went stale because nothing forces them to track the data — the same
failure mode that produced the earlier `source_ref` split (`US11105794` / `US11105794B2`) and the
field-rename cascade. Correcting the four passages fixes the symptom and leaves the mechanism.

**Recommended disposition:** `data/*.csv` is authoritative; every headline figure in prose becomes a
generated value. Concretely — a `scripts/figures.py` emitting a single `FIGURES.md` of named
quantities, with the prose documents referencing those names, and `release_check.py` failing if any
numeral in a tracked sentence disagrees with the generated value. That turns this class of error
from "caught on review" into "cannot be committed". Pending authorization.

**One point I do not accept.** I would not nominate `ROCKSTEADY_RESPONSE_KIDNEY.md` as authoritative
for anything. It is a dated reply to a specific round, and two of the four stale figures are in it.
Reply documents should be immutable records of what was said when, explicitly not sources of truth.
I propose marking it and this file as such in-place rather than maintaining them.

---

## 2. Are same-source comparisons genuinely matched? — **ACCEPT, AND GO FURTHER**

The suggestion asks whether `paired_same_source` comparisons are matched on construct, chemistry,
endpoint, exposure and timing. I audited all 8 read-only. The answer is worse than the suggestion
implies, and the label should be **withdrawn as a quality claim**, not caveated.

```
oligo    endpoint match  route match  unit match  human readout_name          animal readout_name
OLG008   SHARED          same         SHARED      A1M_albumin_RAP_uptake      urinary_A1M, tubular_damage
OLG012   none            same         SHARED      kidney_toxicity_monitored   renal_toxicity, renal_tubular…
OLG013   none            same         SHARED      kidney_toxicity_monitored   proximal_tubule_vacuolation
OLG041   none            DIFFERS      none        intracellular_ATP           renal_histopathology
OLG042   none            DIFFERS      none        extracellular_EGF, intra…   renal_histopathology
OLG043   none            DIFFERS      none        intracellular_ATP           renal_histopathology
OLG045   none            same         none        extracellular_EGF           EGFR_mRNA, KIM-1_mRNA, KIM-1…
OLG048   none            same         none        extracellular_EGF           EGFR_mRNA, KIM-1_mRNA, KIM-1…

endpoint shared 1/8 · unit shared 3/8 · delivery route same 5/8
```

Four distinct defects, in descending severity:

1. **7 of 8 pairs share no biological endpoint.** Only `OLG008` is a genuine match — a human A1M/RAP
   uptake assay against animal urinary A1M, the same analyte either side. The other seven compare
   different measurements and call it a pair.
2. **2 of 8 compare an assertion to an observation.** `OLG012` and `OLG013` have human
   `kidney_toxicity_monitored` — a statement that monitoring occurred — set against observed animal
   lesions (`proximal_tubule_vacuolation`). That is not a comparison of results at all.
3. **3 of 8 differ in delivery route.** `OLG041/042/043` (Moisan) put human gymnotic in-vitro uptake
   against animal systemic in-vivo dosing. Different exposure, so discordance is uninterpretable.
4. **The Roche pairs differ in analyte *and* normalisation.** `OLG045/048`: human `extracellular_EGF`
   normalised to saline control against animal `EGFR_mRNA` normalised to compound 1-1 reference —
   already flagged do-not-pool at extraction, then pooled by the bridge anyway.

**Separately, and not in the suggestion: the pairing test is partly vacuous.** Pairing is decided by
intersecting `source_ref` across argmax-grade rows. Where human and animal grades tie at 0, the
argmax set is the entire row set, so almost any shared source yields `paired`. For compounds
concordant at grade 0 the flag therefore carries close to no information, which inflates the paired
count independently of the endpoint problem above.

**Recommended disposition.** Retire `comparison_type ∈ {paired_same_source, cross_study}` and replace
it with explicit per-dimension flags — `endpoint_match`, `analyte_match`, `normalisation_match`,
`route_match`, `timing_match` — each derived, each independently auditable, plus a
`comparison_strength` that is the conjunction. On current data exactly one of fifteen bridge rows
(`OLG008`) would qualify as a matched comparison. The bridge should be labelled
**hypothesis-generating** wherever it appears, including in `NARRATIVE.md` and the decks, and should
not be described as translation evidence. The audit script is written and ready
(`audit_pairing.py`, held in scratch, not committed under the hold).

This also settles the open question at `ROCKSTEADY_RESPONSE_KIDNEY.md:289` ("does
same-patent-different-table count as genuinely paired?"). On this evidence: no.

---

## 3. Reassess the provisional clinical negative and the surviving animal over-prediction — **ALREADY COMPLETE, NO ACTION TAKEN**

Both items were already routed to German before this round, and I have not touched either:

- the single remaining provisional clinical negative — `ROCKSTEADY_RESPONSE_KIDNEY.md` §6 item 2;
- the surviving animal over-prediction — §6 item 4b.

`nephrotox_grade` is unchanged across all 246 rows this round; no regrading occurred, consistent with
the hold and with German's authority over labels. I confirm the suggestion's constraint was observed.

One note for German's benefit when this is taken up: per §2 above, the surviving over-prediction sits
on a comparison that fails the endpoint-match test, so the question "is the animal over-predicting?"
may not be well posed for that pair. I would put the comparison validity question to German *before*
the grading question, rather than alongside it.

---

## 4. Prioritize missing sequences, primary reports and characterization; separate article from supplement access — **ACCEPT, WITH CORRECTIONS BOTH WAYS**

The article-vs-supplement distinction is a real improvement I had not made, and it is now demonstrated
rather than assumed. I tested every route before replying.

### 4a. The register is right: I overstated paywalls

`SOURCES_TO_ACQUIRE.md` reports confirmed paywalls that I had not actually confirmed — I inferred them
from publisher error responses, which can be bot checks rather than entitlement walls. Verified this
round:

| Source | My file said | Verified now |
|---|---|---|
| Vupanorsen TRANSLATE-TIMI 70 (`MSR079`) | Circulation paywall; link was the journal homepage | **Free full text retrieved**, PMC9047643, 171,996 B, real article |
| VALOR tofersen (`MSR042`) | NEJM paywall | **Free full text retrieved**, White Rose eprints, 13 pp |

The register's three-way status taxonomy is better than my binary and I adopt it.

### 4b. But "free" is not "data-bearing" — the suggestion's own point, confirmed hard

Retrieving the free article does **not** in general retrieve the renal evidence:

- **Vupanorsen, `MSR079`.** The free article contains **zero** occurrences of creatinine, eGFR,
  proteinuria or urine. Renal content is four qualitative sentences — "no confirmed instances of
  significant decline in renal function" — plus confirmation that renal function was a prespecified
  safety endpoint with prespecified repeat-testing criteria. The quantitative values are in
  Supplemental Material, hosted at `ahajournals.org/doi/suppl/10.1161/CIRCULATIONAHA.122.059266`,
  which returns **403**; the PMC supplementary directory returns **404**.
  *Effect if authorized:* `source_access` not_read → fetched_and_read, and
  `renal_endpoints_measured` cannot_determine → measured, since the article establishes the endpoint
  existed. It must **not** reach `confirmed_negative`: my own eligibility gate requires a quantitative
  value, and the article has none. This is exactly the distinction the suggestion asks for, and the
  gate already enforces it correctly without modification.
- **VALOR tofersen, `MSR042`.** Now read in full: 13 pp, VALOR confirmed (82 mentions), and
  **zero** occurrences of creatinine, renal, proteinuria, eGFR, kidney or nephr- (the eight `urin`
  matches are "d*urin*g"). The paper carries no renal content whatsoever.
  *Disposition:* **strike it from the acquisition list.** It cannot inform this endpoint. My row does
  not depend on it — `MSR042` correctly cites `Qalsody_FDA_label;EMA_EPAR` with
  `renal_endpoints_measured=not_measured`, so there is no attribution error to fix; the item was
  simply never worth acquiring. One of my four priority requests was waste, and reading it is what
  proved that.

### 4c. The register is wrong on one route

It offers `PMC8487715` as a free route to the teprasiran trial. Direct retrieval returns a
**reCAPTCHA interstitial** (21,208 B, 360 words, zero mentions of teprasiran). `europepmc.org` HTML
returns a Cloudflare challenge. The route as written does not work from this environment. I flag it
because an access register whose entries have not been executed will mislead whoever works the list.

### 4d. New finding: a route that does work, and unlocks three unread trials

The **Europe PMC REST `fullTextXML` endpoint** (`ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`)
is a machine API with no bot wall, and serves full text for open-access records. Swept across all ten
unread trials:

| Trial | Oligo | PMCID | OA | Result |
|---|---|---|---|---|
| Teprasiran ph2 Circ 2021 | teprasiran | PMC8487715 | Y | **7,330 w** — creatinine 15, eGFR 19, cystatin 11, kidney 54 |
| PHYOX3 | nedosiran | PMC11068990 | Y | **6,919 w** — eGFR 22, kidney 57, creatinine 3 |
| PROMOVI | eteplirsen | PMC8673535 | Y | **7,661 w** — proteinuria 6 |
| NEURO-TTR | inotersen | PMC12611561 | N | in EPMC but not OA — XML refused, HTML bot-walled |
| TRANSLATE-TIMI 70 | vupanorsen | PMC9047643 | N | article obtained as HTML; numbers in 403 supplement |
| van Poelgeest SPC5001 | SPC5001 | PMC4693495 | N | in EPMC but not OA — XML refused, HTML bot-walled |
| Donidalorsen ph3 | donidalorsen | — | — | no PMC record |
| ENVISION | givosiran | — | — | no PMC record |
| Mongersen ph2 | mongersen | — | — | no PMC record |
| OCEANa-DOSE | olpasiran | — | — | no PMC record |

**Three of ten unread trials are retrievable now, free, with no human in the loop** — and teprasiran
in particular is an AKI-prevention trial whose renal endpoints are primary, with cystatin C and eGFR
throughout. The access problem is materially smaller than either my file or the register states, and
it is concentrated: **four NEJM papers with no PMC record are the genuine hard wall.**

*Effect if authorized:* verified trials plausibly 2 → 5, which is the headline figure disputed in
suggestion 1. I have not performed the reads-for-extraction or changed any row.

### 4e. Access requests, request-ready

Highest value first. Nothing here needs a purchase decision before the free routes above are worked.

| Priority | Source | Need | Affected | Routes attempted / barrier |
|---|---|---|---|---|
| 1 | Circulation 2022, `10.1161/CIRCULATIONAHA.122.059266` | **Supplement only** — renal safety tables | `MSR079` | publisher suppl 403; PMC bin 404. Article already in hand |
| 2 | NEJM 2019 `10.1056/NEJMoa1913147` (ENVISION, givosiran) | Article + safety supplement | ENVISION rows | no PMC record; needs library/institutional |
| 3 | NEJM 2018 `10.1056/NEJMoa1716793` (NEURO-TTR, inotersen) | Article + renal AE tables | NEURO-TTR rows | PMC12611561 not OA; XML refused, HTML bot-walled |
| 4 | NEJM 2024 `10.1056/NEJMoa2402478` (donidalorsen) | Article + supplement | donidalorsen rows | no PMC record |
| 5 | NEJM 2023 `10.1056/NEJMoa2211023` (OCEANa-DOSE, olpasiran) | Article + supplement | olpasiran rows | no PMC record |
| 6 | NEJM 2015 `10.1056/NEJMoa1407250` (mongersen) | Article | mongersen rows | no PMC record |
| 7 | Br J Clin Pharmacol `10.1111/bcp.12738` (van Poelgeest, SPC5001) | Article — nephrotoxicity is the finding | SPC5001 rows | PMC4693495 not OA; bot-walled |
| — | VALOR tofersen, NEJM 2022 | **Withdrawn** | `MSR042` | read in full; contains no renal content (§4b) |

A human-browser PDF download would clear items 1, 3 and 7 without any subscription, since all three
are either free-but-bot-walled or a free supplement behind a 403.

### 4f. Sequences and characterization — unchanged, and correctly open

10 of 65 oligos lack sequences and all 65 lack purity. Both remain verified-unreported rather than
unobtained, and neither is closed by any document above. I am not proposing to change their status;
`purity_pct`/`purity_method` should stay explicit `TBD` with the reason recorded, per `STATUS.md` §3a.

---

## 5. New findings this round, not prompted by the suggestions

1. **The pairing test is partly vacuous at tied grades** (§2), independent of the endpoint mismatch.
2. **One of my own priority acquisitions was worthless** and reading it proved so (§4b, VALOR).
3. **A general-purpose free full-text route exists** that I had not used (§4d), and it changes the
   access picture from "mostly paywalled" to "four hard NEJM walls".
4. **My own recollection of the §2 figures was wrong** in the strict direction: I had it as zero of
   eight pairs sharing an endpoint; re-running against the actual column names gives **1 of 8**, with
   `OLG008` a genuine match. Corrected above. Stated because a review that overstates a flaw is as
   unreliable as one that hides it.

## 6. Recommended smallest-useful next work package

In dependency order, three steps, none requiring a purchase:

1. **Figure generation** (§1) — `scripts/figures.py` + `release_check.py` numeral assertion, then
   correct the four stale passages. Smallest, removes a recurring error class, and must precede any
   change to the trial count so the count cannot go stale again.
2. **Per-dimension match flags** (§2) — land the audit as a build step, retire `comparison_type`,
   relabel the bridge hypothesis-generating in `NARRATIVE.md`, `PRESENTATION.md` and the three decks.
   `PRESENTATION.md` and the decks still carry the suppressed "animal over-predicts" headline and are
   the most externally visible stale artefacts in the repository.
3. **Work the three free trial reports** (§4d) — teprasiran, PHYOX3, PROMOVI. Extract renal endpoints
   with the existing anchor-check discipline; expect verified trials 2 → 5.

Step 3 changes scientific content and so should additionally await German, not only Oscar.

## 7. Outstanding decisions

**For German (scientific):**
1. The single remaining provisional clinical negative (`RESPONSE` §6 item 2) — unchanged, awaiting you.
2. The surviving animal over-prediction (§6 item 4b) — and first, per §3, whether that comparison is
   valid at all given it fails the endpoint-match test.
3. Whether `OLG008` alone constitutes a defensible matched human↔animal comparison, or whether the
   bridge should be presented purely as hypothesis generation with no comparison claim.
4. Whether `kidney_toxicity_monitored` (`OLG012`, `OLG013`) should remain a measurement row at all, or
   move to a monitoring-provenance annotation.

**For Oscar (scope and implementation):**
5. Authorize the §6 package, or any subset. Nothing in it is started.
6. Whether to request a human-browser download for access items 1, 3 and 7 — free, no subscription,
   needs a person with a browser rather than a purchase.
7. Whether the four NEJM papers justify library or institutional access, now that the free routes have
   reduced the hard wall to exactly those four.

---

REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION
