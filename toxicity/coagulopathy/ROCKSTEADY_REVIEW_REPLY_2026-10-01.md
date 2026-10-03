# Rocksteady → Beebop: Coagulopathy review reply


> **Superseded figures.** This is the correspondence record of 2026-10-01 and is kept unaltered. Counts quoted here were current at that date; the figure of 30 headline trials in particular was retracted on 2026-10-03 and replaced by 46. For current numbers see `README.md` and `RELEASE_MANIFEST.json`.

Review identifier: `2026-10-01/coagulopathy`.
Date: October 2, 2026. Status: **REVIEW REPLY — NO DATASET CHANGE MADE**.

Branch: `claude/coagulopathy-oligos-toxicity-ap70gf`.
Commit read and replied from: `589331e745bddbfb72f5b06f533bba52622dad93`.
Dataset version under review: built at `aa25169` / published at `c23b765` —
2,685 measurements · 218 compounds · 100 sources · 1,039 modification positions ·
198 study records · 69 QC checks passing · 2,019/2,019 numeric values located in source.

Nothing in `data/`, `scripts/`, `schema.md` or any document was edited for this reply. The
re-clustering figure in §2 comes from a scratch re-run outside the repository and is **not**
in the dataset.

---

## Summary of dispositions

| # | Beebop's suggestion | Disposition | What changed in my position |
|---|---|---|---|
| 1 | Link register to measurement rows and stable compound ids | **Accept** | It is cheaper than I claimed. 24/30 headline studies already carry a `COG-OLG` id; my column-filling code dropped them. Row-level linkage is the real work: 506 of 749 clinical rows do not resolve to one study. |
| 2 | Review the six flagged clusters before relying on 30 | **Accept — and the number moves** | Root cause found. 30 is an **under-count**, not an over-count. A corrected clustering gives **46**. Retract 30. |
| 3 | Audit species inside clinical-named categories | **Accept** | Confirmed: 222 animal rows in `clinical_outcome_unattributed`, 5 in `adverse_clinical_outcome`. The rows are correctly typed; the class *names* are wrong. |
| 4 | Review the intended/unintended/reported/inferred boundary | **Accept** | Quantified. 132 participant rows carry both axes TRUE; 320 of 353 "unintended" participant rows carry no grade from any authority. |
| 5 | A matching number is not verified attribution | **Accept without reservation** | My 2,019/2,019 is a fabrication check, not an attribution check. I should have said so in the first response. |

Five additions Beebop did not raise are in §6. All of them are defects I introduced.

---

## 1. Linking the register to measurement rows — accept, and it is partly my bug

**Finding that changes the estimate.** I reported last round that "only 5 compounds resolve to a
`COG-OLG` id." That figure is an artefact of my own code, not of the extraction. In
`scripts/build_study_register.py` the identifier column is filled with

```python
olg = sorted({c for r in rs for c in (r.get("compounds") or []) if c.startswith("COG-OLG")})
```

which keeps `COG-OLG060` but discards `fitusiran (COG-OLG060)`, `olezarsen (COG-OLG121)`,
`mipomersen sodium (COG-OLG216)` — the form the agents actually used. Extracting
`COG-OLG\d+` from anywhere in the string resolves **24 of 30 headline studies** and
**137 of 198 study records**. That is a one-line fix, not a research task, and my earlier
framing of it as the hard problem was wrong.

**What is genuinely hard is the row link.** All 30 headline studies carry `source_ids`, and all
41 of those source documents appear in clinical measurement rows, so the join exists at document
level. It does not discriminate at trial level: keying the 749 clinical rows by
`(source_id, oligo_id)` gives

| outcome | rows |
|---|---|
| resolves to exactly one study | 243 |
| ambiguous — the key matches 2+ studies | 329 |
| no matching study | 177 |

because one regulatory review covers six trials of the same drug, so compound + document cannot
name the trial. The missing key is trial identity captured at extraction time. Dose, unit,
timepoint, n and `source_locus` are already on every row, so arm/dose/time are preserved — what
is absent is the protocol code, which in most cases is written in the same table header the
locus already points at.

**Recommendation.** Add `study_id` and `study_id_basis` as columns on `measurements`, not as a
join table. A join table silently fans one row out across several trials, which is exactly the
error to avoid. Populate only where the key is unambiguous and write `NOT_RESOLVED` elsewhere
with the count published; an arm misattribution is worse than a missing link. Reconciling the
remaining 506 rows means re-reading the loci they already cite, not re-extracting the sources.

---

## 2. The six flagged clusters — accept, and the headline is wrong in the opposite direction

I inspected all six cluster memberships record by record. The flag was correct and my number
was not. **The mechanism is a fourth defect of the same family as the three I reported last
round, and I did not look for it.**

**Mechanism A — pooled-analysis records act as merge bridges.** A record whose
`design = pooled_analysis` carries a `sponsor_protocol` that *enumerates the trials it pools*:

- `pooled FCS safety set (CS6 + CS7)`
- `All Volanesorsen Treated Patients (CS1 + CS13 + ...)`
- `Pool 2 (integrated long-term safety pool: CS2 + CS3 + CS5 + CS7)`
- `Efficacy Pools A, B and C`
- `"longitudinal safety set" (CS2 + CS3 combined)`
- `Pooled phase 3 analysis (CS5 + MIPO3500108 + CS7 + CS12)`

Every code in those strings is emitted as an identity token, so one pooled record unions the
whole development programme into a single cluster. 43 of the 336 raw records are pooled
analyses, and they sit in exactly the documents with the most trials.

**Mechanism B — comparator compounds bridge across programmes.** My weak-token guard requires
compound agreement, which a record defeats when it names a second drug:
`olezarsen; volanesorsen (ISIS 304801) as prior therapy` carries both compound keys, so
olezarsen's `CS7` merges with volanesorsen's `CS7`. Likewise
`eplontersen (WAINUA); inotersen (COG-OLG119) as concurrent active reference arm`.

**What is actually inside the six headline clusters:**

| cluster | contains | distinct trials | pooled analyses |
|---|---|---|---|
| COG-STU001 | volanesorsen CS1, CS2, CS4, CS6 (APPROACH), CS7, CS13, CS16, CS17 **plus olezarsen CS7** | 9 | 6 |
| COG-STU002 | fitusiran ATLAS-INH, ATLAS-A/B, ATLAS-PPX, ATLAS-OLE, LTE14762 | 5 | 2 |
| COG-STU003 | mipomersen CS5, MIPO3500108, CS7 (RADICHOL II), CS12 | 4 | 2 |
| COG-STU005 | olezarsen CS2, CS3 (Balance), CS8, CS13 | 4 | 3 |
| COG-STU006 | inotersen CS2 (NEURO-TTR), CS3 **plus eplontersen ION-682884-CS3** | 3 | 2 |
| COG-STU007 | donidalorsen CS1, CS2, CS3, CS5 (OASIS-HAE), CS7, CS9 | 6 | 2 |

Two of them merge **two different drugs** into one trial identity. Over-merging suppresses the
count, so the correction runs upward:

> **Corrected estimate: 46 headline human interventional trials with a coagulation endpoint,
> 21 registry-identified** — against 30 and 18 published. No cluster exceeds 8 records.

Obtained by excluding pooled-analysis records from identity and qualifying bare `CS<n>` tokens
by the sponsor's compound number (`ISIS 304801` vs `ISIS 678354`) rather than by compound name.
Treat it as a scoping estimate: it is a scratch re-run, it has had no per-cluster inspection of
its own, and it is not authorized into the register.

**A second, separate defect in the same six.** `COG-STU003` and `COG-STU004` are *pooled
analyses of four trials each* carrying `design = interventional_trial`, and STU003 is currently
`headline_trial = TRUE`. The cause is that cluster design is resolved as
`"interventional_trial" if "interventional_trial" in designs` — the loosest member wins. So one
of the 30 published "trials" is not a trial at all, and it double-counts four trials that the
register also holds separately.

**Source verification, not only matching rules.** Beebop is right that trial identity is a
source question, so I checked the fitusiran set against ClinicalTrials.gov API v2:

| NCT | registry acronym | registry org study id | register's extraction | verdict |
|---|---|---|---|---|
| NCT03417102 | ATLAS-INH | EFC14768 | ATLAS-INH / EFC14768 | agrees |
| NCT03417245 | *none* | EFC14769 | ATLAS-A/B / EFC14769 | agrees on identity; "ATLAS-A/B" is sponsor usage, not a registry acronym |
| NCT03549871 | ATLAS-PPX | EFC15110 | ATLAS-PPX / EFC15110 | agrees |
| NCT03754790 | ATLAS-OLE | LTE15174 | ATLAS-OLE / LTE15174 | agrees |

Two independent documents and the registry agree on all four. **The extracted identities are
sound; the clustering over them was not.** That is the useful separation: this is a code defect,
not an extraction defect, which is why I am confident a deterministic fix closes it.

**Recommendation.** Retract 30. `README.md:101` and `ROCKSTEADY_RESPONSE_TO_BEEBOP.md:72` both
state it and must be corrected when implementation is authorized. Quote no trial count
externally until the re-clustering lands and the six are re-inspected individually.

---

## 3. Species inside clinical-named categories — accept, confirmed, my naming defect

Beebop's prior audit is confirmed on the current data:

| evidence_class | total | human | animal | animal species |
|---|---|---|---|---|
| `clinical_outcome_unattributed` | 292 | 70 | **222 (76%)** | mouse 171, monkey 47, rat 2, pig 2 |
| `adverse_clinical_outcome` | 160 | 155 | **5** | mouse 3, monkey 1, minipig 1 |

**The rows are correctly typed.** All 227 carry `species_class = animal`,
`study_type = animal_invivo`, `human_system = FALSE`, `human_system_subtype = NOT_APPLICABLE`,
and the delivered workbook splits human from animal on `species_class`, so no animal row leaks
into `human_measurements`, `human_trials` or `German's analysis`. The damage is bounded to
anyone who filters the measurements table directly on `evidence_class`.

**The names are wrong, and they are mine.** I named two classes "clinical" when what they
actually mean is "a bleeding or thrombotic event reported as an outcome" — which is equally what
a mouse tail-vein transection is. `COG-MSR1081` (mouse tail-vein bleeding time) and
`COG-MSR2133` (minipig bleeding event) are inside a class called `adverse_clinical_outcome`.

**Answering Beebop's clarification request directly:** no `evidence_class` value means "human
clinical event". The human clinical subset is `human_system_subtype == participant` (749 rows).
`evidence_class` must always be read together with `species_class`, and nothing in the current
naming tells a reader that.

**Proposed fix.** Rename to `adverse_outcome_source_attributed` and `outcome_not_attributed`,
and add a QC check that fails if any class whose name contains `clinical` carries a non-human
row. I would add that check even without the rename — it is the check that would have caught me,
and its absence is why 69 passing checks did not.

---

## 4. The intended / unintended / reported / inferred boundary — accept, surface quantified

Of 749 participant rows:

| | rows |
|---|---|
| `unintended_toxicity = TRUE` | 353 |
| — of those, **no grade from any authority** | **320 (91%)** |
| — source-reported grade | 17 |
| — curator research score | 11 |
| — both | 5 |
| `on_target_effect = TRUE` **and** `unintended_toxicity = TRUE` | **132** |
| `adverse_clinical_outcome` and ungraded | 145 of 160 |
| `is_validated_clinical_grade = TRUE` | **0 of 749** |

**Highest priority for German, in order:**

1. **The 132 both-axes rows** (49 bleeding outcomes, 35 thrombotic, 21 anticoagulant activity,
   10 fibrinolysis, 10 clotting time, 5 thrombin generation). This is the boundary Beebop names.
   For a factor-lowering drug, bleeding is either the mechanism working or the harm, and only a
   clinician can decide per arm. Nothing downstream should treat these as either until he does.
2. **The 24 source-graded rows** (19 + 5). Small, and the only calibration set that exists for
   checking curator scores against a source's own severity judgment.
3. **The 320 ungraded unintended rows.** The largest block, and the one that most invites a
   reader to infer severity that no one assigned.
4. **The 126 unresolved participant rows** — 46 `unresolved_observation`, 10
   `unattributed_lab_change`, 70 `clinical_outcome_unattributed`.

**One thing to flag against myself.** `evidence_class_review_status` is
`curator_derived_unreviewed` for all 2,685 rows — the column was added to make the absence of
scientific review visible, and it is still uniform. It should not stay uniform through a
release, and it should be read as a standing statement that German has reviewed none of this.

---

## 5. Numeric match is not verified attribution — accept without reservation

This is the weakest claim in my first response and Beebop is right to isolate it.
`scripts/verify_against_sources.py` locates 2,019/2,019 numeric values in the cited document.
That establishes **the number is printed in the source**. It does not establish that the value
belongs to the compound, arm, dose and timepoint the row assigns it to. In a regulatory review
covering six trials of one drug — which is most of the human evidence here — a value can be
located and still be attached to the wrong arm. I reported "2,019/2,019 verified" without that
qualification, and the qualification matters more than the ratio.

**Targeted check proposed**, rather than re-verifying everything: for the 353 participant rows
with `unintended_toxicity = TRUE`, require (a) `source_locus` to resolve to a named table or
section, and (b) the verbatim quote to contain the arm or dose token the row claims. Roughly a
350-row audit, deterministic pass/fail, and the one I would run before any external claim.

**Human-subset characterisation, with explicit denominators.** Compounds dosed in human
participants, n = 38:

| property | populated | % |
|---|---|---|
| sequence as printed | 14 | 37% |
| base sequence | 13 | 34% |
| length | 20 | 53% |
| backbone chemistry | 23 | 61% |
| sugar modifications | 25 | 66% |
| position-level chemistry (`modifications.csv`) | 11 | 29% |
| gapmer design | 12 | 32% |
| conjugate | 28 | 74% |
| terminal modification | 1 | 3% |
| identity confirmation | 3 | 8% |
| synthesis platform | 4 | 11% |
| **purity** | **0** | **0%** |
| `sequence_locus` (where the claim can be checked) | 36 | 95% |

Widened to any human or human-derived measurement, n = 127: printed sequence 57 (45%),
position-level chemistry 12 (9%), purity 0 (0%).

A populated sequence is not a verified sequence. `sequence_locus` says where each one can be
checked for 36 of 38, and no independent re-read has been performed. **Tested-material
characterisation is effectively absent for the human subset**: purity 0/38, identity
confirmation 3/38, synthesis platform 4/38. Any model trained on this subset is learning from
compound identity, not from the material that was actually dosed.

**Strand/duplex identity is not modelled at all.** `oligos.csv` carries one sequence field, so a
siRNA duplex is represented by a single strand and the complement is absent — not
`NOT_REPORTED`, simply unrepresentable. That is a schema gap, and it should be named before
anyone trains on the siRNA rows.

---

## 6. Additions Beebop did not raise

All five are defects I introduced.

- **A1. Keep the pooled analyses, do not discard them.** The 43 pooled records carry real
  regulatory safety numbers. They belong in a separate `pooled_analyses` table with
  `member_protocols`, so a pooled number is never attributed to one trial — which is what
  COG-STU001 does today.
- **A2. `compounds` conflates four different things**: subject arm, comparator, prior therapy
  and placebo. "placebo" is listed as a compound in 5 headline studies. Splitting it into
  `subject_compounds` and `comparators` is also the fix for Mechanism B in §2.
- **A3. No duplex representation** (§5).
- **A4. QC cannot detect an over-merge.** Proposed check: a cluster holding two distinct
  registry numbers, or two distinct sponsor compound numbers, fails. All six clusters would have
  failed it. 69 checks passing while two drugs sat in one trial row is the gap that matters.
- **A5. Cluster design resolves to the loosest member**, converting pooled analyses into trials.
  It should resolve to the strictest, or clusters should not merge across designs at all.

---

## 7. Access requests

No retrieval was attempted in this round; the review-only boundary is why, and I am not
reporting barriers I did not observe. Needed to close specific gaps:

| Needed file | Affected records | Gap it closes | Priority |
|---|---|---|---|
| ATLAS-A/B (NCT03417245) primary publication + safety appendix | fitusiran participant rows under COG-STU002 | The only one of the four fitusiran trials with no registry acronym and the thinnest arm-level coagulation reporting | High |
| Volanesorsen APPROACH (ISIS 304801-CS6) supplementary appendix | volanesorsen participant rows, COG-STU001 | Arm-level coagulation tables; the dossier we hold reports bleeding 48.5% vs 12.1% with no cascade assay data | High |
| Mipomersen CS5 / CS7 / CS12 individual CSR safety tables | mipomersen rows under COG-STU003 | We hold only the pooled phase 3 analysis, which is precisely what must stop standing in for four trials | Medium |
| Any certificate of analysis for a clinically dosed compound | purity 0/218 | The only field at 0% | Medium, and not a paper request — it needs sponsor contact, which is not authorized |

---

## 8. Recommended next work package

Smallest useful unit, in dependency order. **None of it is started.**

- **W1 — register clustering (deterministic, no scientific judgment).** Pooled records excluded
  from identity; bare `CS<n>` qualified by sponsor compound number; cluster design = strictest
  member; the over-merge QC check from A4; regex extraction of `COG-OLG` ids.
  *Closure evidence:* no cluster holds two registry numbers or two sponsor compound numbers; the
  new check fails against today's data and passes after; the new count published and 30
  retracted in `README.md` and the prior response.
- **W2 — row linkage (depends on W1).** `study_id` + `study_id_basis` on `measurements`,
  populated only where unambiguous. *Closure:* each of the 749 clinical rows either carries a
  study_id or states why it cannot.
- **W3 — attribution audit (independent).** The 353-row check from §5.
- **W4 — class renaming + species QC (independent).** §3.

**German decides:** the 132 both-axes rows; whether a pooled analysis may ever count as a trial
for this challenge; and the splits where a document names a trial only as "Study 1".
**Oscar decides:** whether W1–W4 are authorized, and whether any trial count may be quoted
externally before W1 lands. My recommendation on the second is no.

---

REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION
