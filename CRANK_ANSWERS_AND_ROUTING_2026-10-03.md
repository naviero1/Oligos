# Crank — answers to open questions, and who owns what

2026-10-03, evening. Answers to questions sessions are currently blocked on or guessing at, then
the routing table. Checkpoint remains **2026-10-10**.

Six Crank figures were wrong today and have been corrected at source in
`CRANK_DELEGATION_2026-10-03.md` and `CRANK_DISPATCH_SOURCES_2026-10-03.md`. The verticals were
right in every case. If you were working from 38 schema fields, "18 of 30" coagulopathy trials,
"984 of 1,959" thrombocytopenia rows, "six of seven MQR fields", or a project-wide instruction to
record purity as withheld-with-evidence — stop, and re-read those two files.

---

## Answers

**1. Do the rules void existing curator-assigned toxicity grades?**
**No. Existing grades stand as PROVISIONAL, pending German.** Do not strip, recompute or
re-derive them. Mark them provisional and move on. This is deliberately the cheap answer: the
exposure is kidney 246/246 rows, thrombocytopenia 1,959/1,959, hydrocephalus 1,316/1,342, CNS
2,538/2,538 and coagulopathy 918 graded — nine endpoints answering this nine different ways is a
far worse outcome than one conservative convention.

**2. Does §E forbid mapping in-vitro readouts onto clinical severity scales?**
**Yes.** German's rule is explicit: do not label in-vitro fold-change bins with CTCAE or any
clinical grade unless clinically validated. Rename the axis **experimental response severity**.
Affected and already measured: coagulopathy 834 of 918 graded rows are non-clinical;
thrombocytopenia 523 of 523 laboratory rows, 307 of them above zero; CNS 297 in-vitro rows,
including two cell-culture rows graded against a definition reading "paralysis / moribundity /
death". Renaming is not a relabelling of the science — the values do not change.

**3. Generalize `check_doc_numbers.py` to eight endpoints?**
**Not yet — fix the matcher first.** Its pattern matches number-then-noun within 60 characters
using `[^.|]`, so it cannot cross a markdown pipe, and in a table the noun precedes the number.
It therefore misses stale figures in table form, including ones live in `coagulopathy.md` right
now. Fix, re-run against known-stale files to prove it catches them, then generalize.

**4. CNS — do both lineages freeze, or does one continue?**
**Both freeze net-new divergent work. Neither is authoritative until German rules (G-1).** Two
agents are currently guessing differently and a wrong guess costs days in the wrong column.
Continue only: the lineage comparison prepared for German, and fixes to already-published
material. Crank will not pick the lineage — it is a scientific adjudication about evidence
quality and scope.

**5. The Tier 0 sequence-join rule — publish it as a rule, not a preference.**
**Case-sensitive is the default.** In this corpus letter case encodes modification positions
(uppercase wing, lowercase gap), so case-insensitive joining silently discards chemistry and can
merge two distinct molecules — kidney OLG063/OLG064 differ only at position 13 in case.
Case-insensitive merging is **forbidden without adjudication**. Whatever normalization produced
the "144 shared sequences" figure must be written down beside the figure.

**6. Coagulopathy Q3 — the default was wrong.**
That question defaulted to action: silence meant proceeding with five staged papers. **Do the 325
unresolved row-to-trial links first.** Those are integrity on data we already hold and already
report; five more papers add mass to a dataset whose problem is not mass.

**7. §G failure on the original CNS lineage (AUC 0.929, `n_papers = 1`).**
**Retire the claim.** Leave-one-paper-out is not computable at n=1, so the figure cannot be
defended. Do not acquire more data to rescue the metric — that would almost certainly mean more
acute-axis material, which the brief deprioritises and Crank's P4 excludes from breadth budget.

**8. The FDA Pharmacology/Toxicology purity sweep is ONE central job.**
**Owner: kidney**, which found the seam. Four reviews already yield roughly 30 values. Nine
sessions each opening the same PDFs is the duplication the audit found in the data and the
sourcing, arriving a third time. Kidney publishes the extraction; other endpoints consume it.

---

## Routing — who owns what now

| Owner | Item |
|---|---|
| **Beebop** | Items 1 and 2 repair, then re-submit for German: add the four missing columns (`licence_class`, `measurement_intent`, `curator_label`, `staging_state` — all four already shipped and populated in complement's 65×51 file, so paste rather than design); **mark the generalization clause inside gate 8 as Crank's, not German's**; and add a verbatim carry-forward field for German's own prior gate verdicts (he has already graded all twelve: 6 PARTIAL, 2 FAIL, 2 PASS, 2 NOT TESTED, with an owner each). Then items 3–12 of the delegation. |
| **Beebop** | Propose the branch-ancestry fix with Oscar. The eight branches share **no common git ancestor**, so there is no safe merge path to assemble one submission. Crank will put a proposal to Oscar; Beebop owns the mechanics. |
| **Rocksteady — thrombocytopenia** | Regenerate `submission/` so the shipped artifact carries the corrected rights text (currently still wrong in `PADP.md`, `submission/padp.html` and the rendered PDF). **Authorised by Oscar.** The 224 licence-restricted rows await Oscar's separate ruling — do not include or exclude them on your own initiative. |
| **Rocksteady — kidney** | Own the central FDA Pharm/Tox purity sweep (answer 8) and publish the extraction for other endpoints. Separately: 311 cells across `oligos.csv` and `oligotox_kidney_merged.csv` assert `purity_not_published_by_any_source_verified_not_assumed`. That is a positive claim of exhaustive search and it is now false for four oligos. **Propose** the corrected note string; do not alter validated data until German or Oscar authorises. |
| **Rocksteady — all** | Apply answers 1, 2 and 5. Mark grades provisional, rename in-vitro severity axes, adopt the case-sensitive join rule. |
| **Rocksteady — both CNS** | Freeze net-new divergent work (answer 4). Finish the comparison for German. |
| **Rocksteady — coagulopathy** | 325 row-to-trial links before the five staged papers (answer 6). |
| **Oscar** | Relay to German (7 decisions, live) and to Gustavo (handover verified). Rule on the 224 rows. |
| **German** | The seven decisions in `German_requests_100326.md`. Four block work that is otherwise ready. |
| **Crank** | Branch-ancestry proposal to Oscar; German item 8 (off-target scope) held until the seven are answered; monitoring to 10 October. **Adding nothing else.** |
