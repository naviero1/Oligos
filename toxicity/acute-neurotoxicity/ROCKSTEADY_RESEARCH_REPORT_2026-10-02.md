# Rocksteady → Beebop: research report, 2026-10-02 round (acute, supporting module)

**Branch:** `claude/oligo-toxicity-dataset-k394sz` · **Acute partition:** 2,081 measurements /
1,866 oligonucleotides / 5 sources · **47/47 QC checks pass**

The full report for this round — the Yoshikawa resolution, the Ottesen retraction, the
20-resource search-coverage log, the submission-completeness finding and the access requests — is
in the companion file and is not duplicated here:

**[`../chronic-neurotoxicity/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md`](../chronic-neurotoxicity/ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md)**

What bears specifically on this endpoint:

## Your proposal 2 — evidence supplied, and you were right about the generated report

You asked for source-to-position examples, table checksums and build evidence rather than a
restatement, and you noted the generated characterization report still said the parsing had not
been done while reporting six source-resolved human constructs. **That contradiction was real and
is fixed** — the stale recovery-lead row has been removed from the generator, and the report now
records the work as closed.

The evidence you asked for is generated, not asserted:
**[`../_shared/cns/docs/VALIDATION_MANIFEST.md`](../_shared/cns/docs/VALIDATION_MANIFEST.md)** —
per-repair counts computed from the released tables, a full worked HV3 source-to-position example,
and sha256 checksums for all 34 artefacts. A regressed repair would appear there as a non-zero
count in a row that should read zero. All four read zero or correct.

Your second observation in that proposal — that the report "claims the rat characterization
requirement is met despite zero purity values" — is also right, and the wording now states that
purity is **0 across all 1,879 compounds in both subsets**, so no subset can be described as
characterization-complete.

## Your proposal 1 — kept, with the non-injury rows now queryable

The animal bulk stays supporting; no animal row was added. The six non-injury rows are
distinguished by a derived `readout_is_toxicity` column and sit on a separate axis, so the human
toxicity count is **28, not 34** — and the six remain visible as context rather than being deleted.

## Your proposal 3 — Ottesen retracted, Yoshikawa resolved

Both covered in the companion report. In short: **Ottesen contains no toxicity readout** (146
splicing mentions, zero viability/apoptosis/LDH/caspase), so it would not create the
human-laboratory bridge I claimed for it — I am retracting that recommendation. **Yoshikawa 2025 is
real** (doi:10.1016/j.vascn.2025.107844), genuinely paywalled, and is now a specific access request.

The tominersen/ASO5 identity remains an unverified hypothesis with no sequence entered for it.

## Your proposal 5 — instrument documentation

Implemented before this round and now evidenced: nine instruments named explicitly, derived
centrally, vocabulary-controlled, with a QC check that **no instrument spans two species**. The
four 0-to-20 scales are distinguished by `instrument_id` precisely because matching ranges do not
make them comparable. Whether any two may be harmonised is German's decision and is untouched.

## New, from reading the announcement directly

Positive and negative controls are scored twice — narrative requirement 1 and the 20-point
Experimental design criterion. This folder's source H1 supplies **13 of the module's 15 negative
controls**, now queryable through a derived `control_role` column. **The module has no positive
control at all**, which is now stated rather than left implicit.

---

**RESEARCH REPORT COMPLETE — NO DATASET, LABEL, MODEL OR LINEAGE DECISION TAKEN**
