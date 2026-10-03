# Receipt — `SCIENTIFIC_RULES.md` read, and what it changes here

**Endpoint:** thrombocytopenia · **Branch:** `claude/oligo-challenge-data-4um5mi` · **Commit:** `989a581`
**For:** Beebop, delegation item 8 · **Date:** 2026-10-03

**Confirmed read in full:** `SCIENTIFIC_RULES.md` and `CRANK_DELEGATION_2026-10-03.md`, both from
`origin/claude/crank-phase2-oversight`. **Neither file exists on this branch** — the instruction said
"at the repository root on your current branch", and it is not there; I read them from that branch
and from `claude/amazing-galileo-rwiv95`, which also carries both. Worth fixing, because a rule
invisible to the session following it is the exact failure the rules file was written to close.

I have not treated this file as authority. Where it and German's Drive documents differ, German wins.

---

## 1. Rules that change my work — in order of how much they change

### 1.1 §E: in-vitro bins must not be mapped to CTCAE. **This is the big one.**

> "Do not map in-vitro fold-change bins to clinical severity grades (e.g. CTCAE) unless clinically
> validated. Call it experimental response severity."

My `thrombocytopenia_grade` is a 0–3 scale documented as **CTCAE-aligned with explicit in-vitro
analogues**. Measured: **523 of 523 in-vitro and ex-vivo rows carry that grade, 307 of them above
zero** (grade 1: 99, grade 2: 169, grade 3: 39). So this rule is violated on every laboratory row
in the endpoint, and the violation is structural rather than incidental — the rubric was designed
to do it, so that a bench readout and a trial outcome would "land on a comparable scale". That was
the wrong design goal.

**I have changed nothing.** Renaming or re-scaling the indicator changes biological meaning on
1,959 rows and is German's call. What I propose, for German: keep the clinical rows on the
CTCAE-aligned scale, split the laboratory rows onto a separately named
`experimental_response_severity`, and retire the single pooled column. I am not implementing that.

### 1.2 §A: the agent contract forbids assigning toxicity labels

> "no agent may ... assign toxicity labels ... Permitted: transfer rows into a locked staging
> schema, preserve source row lineage, generate an exception queue, and report."

`thrombocytopenia_grade` is a curator-assigned toxicity label on **1,959 rows**. On the plainest
reading of the contract, producing it exceeded what any agent is permitted to do, and that is true
of the whole dataset rather than of some recent change. I am flagging it rather than deleting
anything: the labels are documented, rubric-driven and reversible, and destroying them
unilaterally would be its own violation. **German should rule on whether the existing grades stand
as curator-derived provisional values or must be withdrawn.**

Related, and cheaper to fix once ruled on: §E requires author result and curator label kept
separate. I have **no `author_interpretation` field** — the grade sits alone with no record of what
the source itself concluded.

### 1.3 §G: shared-sequence grouping must not merge chemically distinct constructs

> "Shared-sequence grouping must **not** merge chemically distinct administered constructs."

My `exact_sequence_group` does exactly that, and I had already conceded it as a design error in the
2026-10-01 review reply. It now has a rule behind it rather than only my opinion. Measured: it
merges 3 of 35 multi-member groups across a U/T difference, and it places `ODN2395_Thio` (PS 21)
in the same group as `ODN2395` (PS 0) — same base sequence, chemically distinct administered
material. The fix I proposed — split identity from the leakage key — is now rule-mandated.
**Still not implemented; it is schema, so it is gated on the Tier 0 crosswalk.**

### 1.4 §C: coarse chemistry flags may never be a primary encoding or a causal feature

The retracted classifier used `bb_full_PS`, `sug_LNA`, `sug_MOE`, `cls_gapmer` as primary features.
This rule independently confirms that retraction was correct, and for a reason I had not given:
not merely that the model was blocked, but that **molecule-level flags are the wrong encoding**.
Position-resolved chemistry exists for only 44 of 259 compounds, so a position-encoded model is not
currently buildable either — which is a better argument against the model than the AUC was.

### 1.5 §F: `NOT_REPORTED` is the correct value, and my sentinel is wrong

> "those fields **must remain `NOT_REPORTED`** ... `NOT_REPORTED` is the **correct value**, not a
> failure state."

I use **`TBD`** throughout for missing purity and characterization. `TBD` implies pending work;
`NOT_REPORTED` asserts a fact about the source. The rules file is right that these are different
claims, and mine is the weaker one. A sentinel rename is mechanical but it touches every row, so it
is schema and gated.

German's calibration — "**zero** of 45 thrombo records with a usable purity value ... plan for
disclosure, not rescue" — matches my independent finding exactly (0/259 values; method recovered
for 11; FDA withholds the criteria under FOIA Exemption 4 with citable page-count stamps). **I
withdraw any framing of purity as recoverable.** It is a disclosure item.

### 1.6 §F: the Characterization Gap Register

My `data/recovery_ledger.csv` (18 entries, 10 critical) already carries missing item, why it
matters, sources searched, next action, stopping criterion and owner — the four things §F requires
plus two. I am treating it as this endpoint's register; if German wants a different shape, say so.

## 2. Rules I was already following

- **§B two-table architecture** — canonical `oligos.csv` linked to `measurements.csv`. Separate, as required.
- **§D lane separation** — human clinical / human laboratory / animal appendix / unresolved are
  separate views; intended pharmacology is a distinct flag with a per-unit reason.
- **§E unreported is not negative** — enforced by a QC gate that errors if any row's text asserts a
  clinical negative. Qualified clinical negatives: **0**.
- **§E intended pharmacology and therapeutic correction are not toxicity** — 3 units excluded on
  exactly these grounds (anti-vWF aptamer raising platelets; telomerase inhibitor in thrombocythaemia).
- **§E do not collapse distinct outcomes** — `readout_category` keeps platelet count, activation,
  binding/aggregation, coagulation, immunogenicity and megakaryocyte separate.
- **§G grouped splits, LOPO** — `publication_group` exists; random splitting is not used anywhere.
- **§H** — classifier BLOCKED and retracted; freeze NOT GRANTED; release eligibility stated as NOT
  ELIGIBLE in `STATUS.md`.
- **§I known source corrections** — I checked all nine named identifiers against this endpoint's 70
  sources and every one is **absent**: Peacock_2009, Goodchild, Hornung, Herzner, Riera-Tur,
  Fucini, Lenert, PMID 19630977, PMID 20490286. Nothing to carry.

## 3. The grain question, flagged and not acted on

**This endpoint is *not* one-row-per-oligo.** `measurements.csv` is already at experiment-condition
grain and is linked to a canonical oligo table, which is the §B architecture.

But the grain is **partial**, and the gap is specific: of §C's named fields, **19 are absent
entirely** —

`strand_role`, `duplex_partner_id`, `terminal_modifications`, `gap_length_nt`, `endotoxin_level`,
`formulation`, `delivery_agent`, `anticoagulant`, `cell_subset`, `donor_id`, `donor_class`,
`sample_state`, `author_interpretation`, `curator_label`, `immunomodulatory_direction`,
`receptor_pathway`, `mechanism_evidence_type`, `clinical_anchor`, `evidence_confidence`

The two that bite hardest:

- **`donor_id` is absent**, so the unit of observation cannot currently reach "× donor". The staged
  Sewing 2017 data *has* per-replicate structure, which is why promoting it would be the single
  largest step toward true condition grain — and why it is gated.
- **`strand_role` / `duplex_partner_id` are absent**, so the siRNA entries carry one sequence field
  for a duplex. German's own `Duplex_Component_Master_v0.8` models guide and passenger separately;
  I never extracted those sheets. That also explains a discrepancy worth recording: Beebop cites
  v0.9 as holding **875** position records where I measured **831** — the 44-row difference is
  `Duplex_Position_Chem_v0.8`, the strand-level sheet I did not pull. Both figures are right; mine
  was single-strand only.

**I have re-grained nothing and added no field.** Per the standing rule, this is schema, so it is
gated on the Tier 0 crosswalk, and the biological-meaning question is German's.

## 4. Crank's four items for this endpoint — status

| Item | Status |
|---|---|
| SafeSense `mmc4.csv` | Route established and **open**: PMID 42633286 / PMC13499347, `isOpenAccess=Y`, `supplementaryFiles` → HTTP 200. **Not acquired** — ownership is German + Oscar per ACT-010-04. Licence is **CC BY-NC-ND**; the ND clause is the one that bites a restructured dataset |
| Sewing 2017 S1 | **Retrieved and staged** at condition level: 2,347 cells with exact cell loci, `sha256 cd4d4b09…a3fc`. Of those, 163 resolve to a named construct and 190 are controls — a cell is not an observation. Not ingested |
| DEVOTE NCT04089566 | **Packet prepared, not classified** — `curation/german_queue/DEVOTE_NCT04089566_FOR_GERMAN.md`. Pre-specified platelet outcome with a threshold rule, posted results, per-arm denominators. It may satisfy all six §E criteria, which is precisely why I did not rule |
| Report maps at 44/259 | **Done.** 44/259 (16%) dataset-wide now leads, with the 18/34 and 20/48 subsets beside it and every denominator stated |

### The 984 rows: figure confirmed, conclusion superseded

Crank's **984 of 1,959** is confirmed exactly — it is the legacy `redistribution` column's
`summary_stat` count. But that column was a **blanket tag** meaning "a number extracted from a
paper", not a per-licence determination. Resolving all 70 source documents against
publisher-declared licences gives:

| licence_class | rows |
|---|---:|
| `public_domain_us_federal` | 748 |
| `cc_nc_noncommercial` | 747 |
| `cc_permissive` | 229 |
| `closed_no_open_licence` | **224** |
| `cc_nd_derivatives_restricted` | **11** |

**1,735 of 1,959 (88%) are releasable on publisher-declared terms; 224 need a decision**, and the
top five sources are 181 of those 224. Output is a **proposed-hold list with reasons — zero
automatic withdrawals**, per Beebop's item 3. `curation/rights/` now carries
`shipped_row_rights.csv`, `proposed_hold_rows.csv` and `exclude_nd_derived_rows.csv`, the last
being the ND exclusion list Beebop's crosswalk switch needs.

Per §E's two-part split: this answers **extracted-data reuse** only. **Source-file republication**
is a separate question and I have not answered it — no retrieved PDF or archive is committed; only
checksums, URLs and inventories are.

## 5. Where I have reached the edge of this file

Per §J, these are the points where following the rules would require a scientific judgment, so I stopped:

1. **Does the CTCAE-aligned grade stand on 523 laboratory rows, or must those rows move to a
   separately named experimental-severity scale?** (§1.1)
2. **Do the existing 1,959 curator-assigned grades stand as provisional, or must they be
   withdrawn under §A?** (§1.2)
3. **DEVOTE** — the four questions in its packet.
4. **Whether `TBD` → `NOT_REPORTED`** is a rename or a re-assertion that needs per-row evidence.
5. **Whether intrathecal exposure** belongs in this endpoint's clinical lane at all.

And one for Oscar, not German: **the 224-row licence decision and the NC/ND position**.

---

**Acquisition and description continue. Nothing has been ingested, promoted, re-grained or released.**
