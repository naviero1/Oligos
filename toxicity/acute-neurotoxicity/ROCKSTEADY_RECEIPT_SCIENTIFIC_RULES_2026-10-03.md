# Rocksteady (CNS acute) → Beebop: receipt for `SCIENTIFIC_RULES.md`

**Date:** 2026-10-03 · **Branch:** `claude/oligo-toxicity-dataset-k394sz`

`SCIENTIFIC_RULES.md` read in full. The CNS endpoints are covered by one receipt, since the rules
that bite are shared and the delegation row is "CNS — both lineages":

**[`../chronic-neurotoxicity/ROCKSTEADY_RECEIPT_SCIENTIFIC_RULES_2026-10-03.md`](../chronic-neurotoxicity/ROCKSTEADY_RECEIPT_SCIENTIFIC_RULES_2026-10-03.md)**

What falls specifically on this folder:

## §B grain — this is where the one-row-per-oligo problem lives

Source H1 contributes **2,006 of this folder's 2,081 rows** and is strictly one row per
(oligo, readout): one calcium-oscillation score and one tolerability score per compound, with no
dose, time or replicate axis inside a readout. `dose_value` and `exposure_duration` are populated
on all 2,006 rows but are constant per readout.

**That is the source's grain, not the schema's** — Hagedorn publishes one summary score per
compound. The other sources in this folder (K1 at 5.86 rows per key, HV3 at 1.89, HV1 at 1.50) are
observation-grained in the same schema.

**Nothing re-grained. German's call.**

## §G leakage — the model lives here too

All 181 paired compounds are H1: **one source, one paper, one laboratory**. Leave-one-paper-out is
not computable (n_papers = 1), and `sequence_family_group` / `paper_group` do not exist. The 0.929
AUC is a within-source number and will be labelled as one.

## Beebop item 9 — control inventory

Confirmed from this folder: `control_role` holds **13 negative controls (H1, all G-free and
sequence-matched) and 0 positive controls**. Module-wide the figures are 15 negative, 1 vehicle,
**0 positive**. Crank's "0 positive controls of 1,866" is correct for this folder's roster.

The narrative deliverable requires both classes. **There is no positive control anywhere in this
module**, and no source in it designates one — that is a disclosure, not something I can close by
selection.

## Crank's figure for this folder

The acute dossier's "Graded rows | 245 — 74/81/39/51" reproduces exactly on measurement. Crank
cited it as the correction for a README sentence that is module-level; the two populations differ,
and the README now carries the module-wide figure with the animal panel broken out separately.
