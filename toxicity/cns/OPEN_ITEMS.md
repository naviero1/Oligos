# OPEN ITEMS — OligoTox-CNS

Every item has an **owner** and a **status**. Items that affect a conclusion are restated at the point
of that conclusion in the narrative and methodology documents.

Status vocabulary: `OPEN` · `IN PROGRESS` · `RESOLVED` · `ACCEPTED-LIMITATION` (will not be resolved
within this submission; disclosed instead).

---

## OI-01 — No CNS source material was supplied at intake

**Owner:** Claude (this session) · **Status:** RESOLVED (2026-08-26) · **Raised:** 2026-08-26

*Resolution:* five sources located and retrieved over the network; four contribute data
(1,839 oligonucleotides / 2,065 measurements) and one contributes measurement instruments. All
retrieved files are committed to `sources/` so the dataset stays rebuildable. The schema
assumption below was carried through and is now visible in `docs/SCHEMA.md` for review.

The upload contained a completed Nephrotoxicity module and an Immunotoxicity module with 24 primary
PDFs. It contained **no CNS/neurotoxicity papers, no CNS CSVs, and no prior CNS work**. The
instruction was only "The toxicity will be CNS."

*Consequence:* unlike the immunotoxicity module — which extracted from PDFs held locally on disk —
every CNS row must be located and read over the network. Sources behind publisher paywalls may be
unreachable, which will bias the corpus toward open-access (PMC), preprint, patent, and regulatory
material. The provenance tier of every row records which applies.

*Assumption being made:* that the CNS module should follow the **same two-table schema and the same
0–3 severity grading philosophy** as the nephrotoxicity module, so the three modules compose into one
programme. This is an inference from the sibling artefacts, not an instruction. **If the intent was a
different schema, this is the moment to say so.**

---

## OI-02 — "Purity and characterization of each oligo" is largely not published

**Owner:** Claude · **Status:** OPEN · **Raised:** 2026-08-26

The challenge requires the dataset to contain *"data on the purity and characterization of each"*
oligo. This is straightforward for a submitter who **synthesised** the oligos. It is only partially
satisfiable by **literature curation**, because:

- Journals almost never print per-compound purity (%) or observed mass alongside toxicity results.
- Methods sections typically state the *method* ("purified by AEX-HPLC, identity confirmed by
  ES-MS") without per-compound values.
- Patents and regulatory documents sometimes do better; commercial vendors' certificates of analysis
  are not public.

*Approach — no number will be invented.* Three fields are carried per oligo:
`purity_pct` (value only where printed), `purity_method` (verbatim from the source's Methods),
`identity_confirmation` (verbatim). Absent values are `NOT_REPORTED`, and the completeness report
counts them explicitly rather than hiding them.

*This is disclosed as a limitation in both PDFs.* It is the single largest gap between what this
dataset is and what the challenge text describes.

---

## OI-03 — Modification *position* vs modification *motif*

**Owner:** Claude · **Status:** RESOLVED (2026-08-26) · **Raised:** 2026-08-26

*Resolution:* in the released data **no row needed the motif-expansion path**. 1,830 of 1,839
oligonucleotides are `position_resolved_from_source` (1,825, case convention) or
`position_resolved_from_source_typeface` (5, PDF span styling); the remaining 9 are
`NOT_REPORTED`. `derived_from_motif` exists in the vocabulary but has a count of zero, so no
user has to filter it out.

The challenge requires *"the location of all chemical modifications in each oligo"*. Sources report
this at two very different resolutions:

1. **Position-resolved** — e.g. a patent table using case to mark LNA vs DNA (`CGTcagtatgcgAATC`), or
   an explicit per-position list. Fully satisfies the requirement.
2. **Motif-level** — e.g. "5-10-5 MOE gapmer, full PS". The positions are *derivable* from the motif
   plus the length, but that derivation is an inference, not source content.

*Approach:* store both. `modification_pattern` holds the source's own words; `modification_positions`
holds a per-position expansion **only** where the source is position-resolved. Where a per-position
string is generated from a stated motif, `modification_position_basis` records `derived_from_motif`
so a downstream user can exclude those rows. Nothing is expanded from a motif the source did not
state.

---

## OI-04 — Severity grading rubric for CNS toxicity is not yet fixed

**Owner:** Claude · **Status:** RESOLVED as to construction (2026-08-26); grades remain
`provisional` pending expert sign-off · **Raised:** 2026-08-26

*Resolution:* the rubric was not invented. Rows on the 0–20 acute tolerability scale use the
cut-offs published by Hagedorn et al. (4, 7, 18), which reproduces those authors' own
"roughly 60% suitable for further development" at 112/181 = 61.9%. Clinical rows use a separate
stated rubric and a separate `tox_axis`. Every graded row carries its rule in `grade_basis`. The
four-axis taxonomy is documented in `docs/SCHEMA.md` and `docs/SCORING_INSTRUMENTS.md`.
**The remaining open part is expert confirmation of the grades themselves.**

The nephrotoxicity module uses a 0–3 ordinal grade with named anchors. CNS toxicity does not have an
equally settled ladder, and it spans at least four phenomenologically distinct axes (acute
behavioural, subacute/delayed neurodegeneration, neuroinflammatory, and on-target/hybridisation-
dependent). A rubric collapsing these into one 0–3 scale must be justified, not asserted.

*How it was closed:* the rubric was written from published scales rather than invented, and every
grade carries `grade_basis` naming the rule applied. Like the kidney module, all grades ship as
`provisional` pending subject-matter-expert sign-off.

---

## OI-05 — This is a curated dataset, not a wet-lab-generated one

**Owner:** user (scope decision) · **Status:** OPEN — needs a decision

Phase 2 is the "Data Generation Phase" and asks for data created "through the collection, generation,
and contribution of data". **Collection is explicitly in scope**, and both sibling modules are
collection-based, so this module proceeds the same way.

But the reviewer-facing consequence should be a deliberate choice, not a default: a curated dataset
cannot claim novel experimental controls, replicates, or synthesis QC of its own. Its contribution is
*harmonisation across sources that have never been placed in one schema*, which is exactly what the
immunotoxicity module argues in its conclusions.

*Decision needed from the user:* confirm that a curation-based CNS module is what is wanted, or say
that wet-lab or in-silico *generation* (e.g. computed sequence/chemistry descriptors as a genuinely
new contributed layer) should be added on top. **Proceeding on the curation assumption meanwhile.**

---

## OI-07 — No public human *in vitro* CNS oligonucleotide toxicity data was found

**Owner:** Claude · **Status:** OPEN — ACCEPTED-LIMITATION for v1.0 · **Raised:** 2026-08-26

The challenge prioritises datasets *"based on in vitro human systems or able to extrapolate data
between in vitro human systems and animal data."* This release satisfies the **second** clause —
181 compounds carry paired in vitro and in vivo readouts — but not the first: only 12 of 2,065
measurements are human-derived, and all twelve are clinical adverse-event incidences. The field's
standard predictive screen is a **rat** primary-neuron calcium assay.

A targeted search for published, sequence-resolved human iPSC-neuron or organoid data on
oligonucleotide CNS toxicity found a 2023 review describing such models as *"promising"* for
seizure-liability assessment — i.e. a future direction — and no public dataset.

*This is reported as a finding (F-10), not hidden.* If the intent is to compete specifically on
the human in vitro criterion, closing this would require generating data rather than curating it,
which is a scope decision for the user.

---

## OI-08 — Two sources contradict each other on divalent-cation rescue

**Owner:** subject-matter expert · **Status:** OPEN — documented, not resolved

Source K1 shows Ca²⁺/Mg²⁺ abolishing acute CNS toxicity; source O1 reports no such effect at
1–100 mM. The reconciliation offered — that they measure *activation* and *inhibition* phenotypes
respectively — is our reading, and is stated as such in `docs/SCORING_INSTRUMENTS.md` § 3. It
should be confirmed by someone with domain expertise before it is relied on.

---

## OI-06 — Deliverable naming was not specified

**Owner:** user · **Status:** OPEN — proceeding on a default

The mission's `<outputs>` block says only "Check steps" where exact deliverable filenames were
expected. Defaults being used, mirroring the challenge's own wording:

| Deliverable | Path |
|---|---|
| Narrative document (≤12 pp) | `deliverables/OligoTox-CNS_Narrative.pdf` |
| Methodology document (≤5 pp) | `deliverables/OligoTox-CNS_Methodology.pdf` |
| Dataset workbook | `deliverables/OligoTox-CNS_Dataset.xlsx` |
| Data dictionary + schema | `docs/SCHEMA.md`, `docs/DATA_DICTIONARY.md` |
| Licence | `LICENSE` (CC BY 4.0 intended) |

Say the word if different names are required by the submission portal.
