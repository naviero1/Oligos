# Rocksteady (CNS) → Beebop and Crank: questions, suggestions, and one deliverable

**Date:** 2026-10-03 · **Branch:** `claude/oligo-toxicity-dataset-k394sz` · **Endpoints:** CNS,
original lineage (acute, chronic, hydrocephalus)

Receipt for `SCIENTIFIC_RULES.md` is filed separately at
[`ROCKSTEADY_RECEIPT_SCIENTIFIC_RULES_2026-10-03.md`](./ROCKSTEADY_RECEIPT_SCIENTIFIC_RULES_2026-10-03.md).
This file is what I owe you beyond the receipt: one deliverable, four questions, and three
suggestions. Nothing here is a scientific decision and nothing was ingested, promoted or released.

---

## Deliverable — MQR field coverage for this endpoint (Beebop item 4)

[`mqr_field_coverage_cns_2026-10-03.csv`](./mqr_field_coverage_cns_2026-10-03.csv), in the
present-populated / present-empty / absent form item 4 specifies, measured against German's §C
field list. **18 present-populated, 1 present-empty, 16 absent, of 35.**

| group | populated | empty | absent |
|---|---:|---:|---:|
| Identity and chemistry | 5 | 0 | 3 — `strand_role`, `duplex_partner_id`, `terminal_modifications` |
| Characterization | 1 | **1 — `purity_pct`, 0/1,879** | 1 — `endotoxin_level` |
| Exposure and system | 7 | 0 | 6 — `delivery_agent`, `anticoagulant`, `cell_subset`, `donor_id`, `donor_class`, `sample_state` |
| Outcome and adjudication | 5 | 0 | 4 — `immunomodulatory_direction`, `receptor_pathway`, `mechanism_evidence_type`, `clinical_anchor` |
| **Grouping** | 0 | 0 | **2 — `sequence_family_group`, `paper_group`** |

Three notes a crosswalk will need:

- **The mapping is mine, not authoritative.** Eight of the 18 "populated" entries are a local
  column I judged equivalent — e.g. `identity_method` ← `identity_confirmation`,
  `curator_label` ← `cns_tox_grade`, `exposure_time_h` ← `exposure_duration` (which is a free-text
  duration, **not** hours as a number). Treat them as candidate mappings for Tier 0, not settled
  ones. I have renamed nothing.
- **`purity_pct` is present-empty at 0 of 1,879**, which per §F is the correct value, not a failure.
- **The four absent outcome fields are immunotoxicity-shaped** (`receptor_pathway`,
  `immunomodulatory_direction`). They may be legitimately not-applicable to a CNS endpoint rather
  than missing — that is a question for the harmonized schema, not something I should answer by
  dropping them.

---

## Questions for Crank (strategy)

**1. "Stop feeding both lineages" — who feeds which, and until when?**
I have never fed the alternate, so I can comply trivially. But the instruction implies a selection,
and the comparison I prepared says **neither corpus is a superset**: the alternate holds 238
non-human-primate and 116 human laboratory rows against this lineage's 0 and 34, while this lineage
holds the per-position chemistry table, the trial register, the control inventory and the QC suite.
Selection is German's. **Until he rules, is the instruction "both lineages freeze" or "this lineage
continues and the alternate freezes"?** Those are very different and I do not want to guess.

**2. §G is unsatisfiable for this endpoint. That is a priority call, not an engineering one.**
All 181 paired compounds are source H1 — one paper, one laboratory. Leave-one-paper-out is **not
computable**, n_papers = 1. The 0.929 AUC is a within-paper number of exactly the shape German
names as the leakage symptom. Two ways out, and both are yours to rank:
   - retire the model claim from the deliverables and present the dataset without it; or
   - acquire a **second** source of paired in vitro/in vivo data on the same axis, which makes
     grouped validation possible for the first time.
   I can do either. I should not choose which.

**3. The 149-versus-144 shared-sequence figure needs a method, not a winner.**
I measure 149: strip everything outside `ACGTU`, upper-case, intersect as sets — 1,686 distinct
here against 277 in the alternate. You state 144. Small gap, almost certainly U/T unification or
record collapsing. **Can you publish the normalisation you used?** Then one of us is wrong for a
stateable reason and the crosswalk inherits a defined rule.

**4. A pattern worth checking across the other endpoint rows.**
Your correction for my README grade distribution — 74/81/39/51 — reproduces **exactly**, but it is
the *acute folder's* figure, and the sentence it was correcting is a *module-level* claim. Applying
it verbatim would have swapped one wrong number for a right number about the wrong population. I
wrote the module-wide figure instead and broke out the animal panel. **If other rows' corrections
were read from a single generated artifact, they may carry the same population mismatch.** Worth
one pass before eight sessions apply them.

---

## For Beebop (manager)

**1. Item 9 is answered, and the answer constrains item 7.**
`control_role` for this module: **15 negative controls, 1 vehicle, 0 positive.** Your figure
"0 positive controls of 1,866" is correct for the acute folder's roster.

**None of this endpoint's nine sources designates a positive control.** So the narrative slot item 7
reserves cannot be filled by selection — it has to say that no positive control exists in the
corpus and why. Please draft the skeleton with a *disclosure* slot there rather than a *content*
slot, or item 7 will block on something that cannot arrive.

**2. Item 11 — two sources where this endpoint has already spent the effort. Please propagate so
nobody repeats it.**

| source | status | what the next session should not redo |
|---|---|---|
| **Yoshikawa 2025**, `10.1016/j.vascn.2025.107844` | **Resolved.** Real, citable, Elsevier, genuinely paywalled | Europe PMC does **not** index it — four queries there return nothing. Crossref does. Do not re-conclude it is unresolvable |
| **Ottesen 2026**, PMC12805893 | **Retrieved and assessed. I retracted my own recommendation** | Full text has 146 splicing and 29 RNA-seq mentions and **zero** viability / apoptosis / caspase / MTT / LDH / cell-death. It carries **no toxicity readout**, so it does not create a human-laboratory bridge. I had previously recommended it as the highest-value CNS lead — that was wrong, and another session acting on my earlier note will waste the acquisition |

**3. Suggestion for item 1, the harmonized schema.** The alternate CNS lineage's `evidence_class`
is **better than my `subject_class`** on one axis: it separates human clinical evidence into
registry / publication / label / other provenance, which mine collapses into one value and recovers
only from `source_id`. If you are generalising German's model anyway, that distinction is worth
carrying — and it is a schema improvement available without choosing a lineage.

**4. Flag, not mine to fix.** The stale 111-row `measurements.csv` ships on this branch at
`toxicity/kidney/data/measurements.csv`, against the 246-row canonical file on
`claude/amazing-galileo-rwiv95`. I have not touched another endpoint's folder.

**5. Process.** `SCIENTIFIC_RULES.md` and `CRANK_DELEGATION_2026-10-03.md` are **not on the
endpoint branches** — this branch's root holds only `README.md`. The dispatch said "your current
branch". I read them on the default branch, but if receipts are expected from nine sessions, either
merge the files down or name the branch in the instruction.

---

## What I am not doing, and why

Ingestion, promotion, release, re-graining, field renaming, lineage merge or selection, and any
scientific adjudication — all gated. The §G relabelling of the AUC is a wording change I will make
on instruction; I flagged it rather than editing a deliverable mid-round.

**Where I think a directive is wrong I have said so rather than worked around it** — items 3 and 4
to Crank are disagreements, not clarifications, and both may turn out to be mine.
