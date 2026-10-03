# CNS lineage comparison — prepared for German

**Date:** 2026-10-03 · **Prepared by:** Rocksteady (CNS, original lineage) · **Status:**
**decision input only — no merge, no selection, no re-grain performed**

Crank's delegation asks this lineage to stop feeding both CNS corpora and to prepare the
comparison for German. This is that comparison. It takes no decision, and nothing in either
corpus was changed to produce it.

**Declared bias:** I built the original lineage. Where a judgement could favour it, I have given
the measurement instead and said what the alternate does better.

Measured 2026-10-03 from the committed trees. Alternate lineage read at
`claude/oligo-cns-toxicity-dataset-tijib6`, file `toxicity/chronic-neurotoxicity.{oligos,measurements}.csv`.

---

## 1. Rosters

| | original (`…-k394sz`) | alternate (`…-tijib6`) |
|---|---:|---:|
| Oligonucleotide records | **1,879** | 573 |
| Distinct nucleobase sequences | **1,686** | 277 |
| Records carrying a sequence | 1,858 / 1,879 (98.9 %) | **573 / 573 (100 %)** |
| Measurement rows | 4,428 across three endpoint folders | 2,393 in one file |
| Per-position modification records | **32,898** | not present as a separate table |

The alternate's 573 records resolve to 277 distinct sequences, so roughly half its roster is
repeated sequence under different record identifiers. The original's 1,879 resolve to 1,686.

## 2. Shared sequences — I measure 149, not 144

Crank states 144. Comparing nucleobase sequences after stripping chemistry notation and
upper-casing, **I measure 149**. The difference is small and almost certainly a normalisation
choice (U/T unification, or whether repeated records are collapsed before intersecting).

**I have not adopted either figure.** The method behind mine: strip all characters outside
`ACGTU`, upper-case, compare as sets. 1,686 against 277, intersection 149.

Those 149 shared sequences map to **287 oligo records** on this side: 277 from source H1
(Hagedorn), 5 from L1, 3 from HV1, 2 from C1. **The overlap is almost entirely the H1 animal
screen** — both lineages ingested the same Hagedorn supplementary table. The lineages differ in
what they admitted *around* that common core, not in the core itself.

## 3. Evidence composition — the alternate holds two things this lineage does not

| | original | alternate |
|---|---:|---:|
| Non-human primate rows | **0** | **238** |
| Human laboratory rows | 34 | **116** |
| Human clinical rows | 2,341 | 414 (133 registry, 100 publication, 101 label, 80 other) |
| Animal rows | 2,053 | 1,863 |
| Species represented | rat, mouse, human | rat, mouse, human, **monkey**, sheep |

**This is the finding that matters for the decision.** The alternate carries 238 monkey rows and
roughly three times the human laboratory evidence. Both are classes this lineage lacks entirely or
nearly so, and the human laboratory class is the one the Challenge prioritises.

Against that, Beebop's audit reports the alternate's 116 human laboratory rows span **39
identifiers with sequence text for 13**, so they are not 116 fully characterised constructs; and
its `chronic-neurotoxicity`-named file contains **931 acute-domain rows**, so its endpoint labelling
and this lineage's are not directly comparable without reconciliation.

## 4. Rubric and architecture differences

| | original | alternate |
|---|---|---|
| Endpoint separation | three physical folders, each self-contained | one table, endpoint carried in a column |
| Evidence taxonomy | `subject_class` (4 values) + `subject_group` | `evidence_class` (6 values), finer on clinical provenance |
| Chemistry encoding | per-position table, 32,898 records | molecule-level fields |
| Trial accounting | `trials.csv`, 22 verified / 16 index cohorts | no register located |
| Chronicity | explicit `chronic_qualification` column | not located |
| Controls | `control_role`: 15 negative, 1 vehicle, **0 positive** | no control column located |
| Structural QC | 47 checks, all passing | not located |
| Reproducibility | 44 artefacts byte-identical across two full runs | not assessed |

The alternate's `evidence_class` is **better than this lineage's `subject_class`** on one axis: it
distinguishes registry, publication and label provenance within human clinical evidence, which this
lineage collapses into a single `human_clinical` value and recovers only from `source_id`.

## 5. What is lost either way

**If the alternate is retired:** 238 non-human-primate rows and the larger human laboratory layer,
both classes this lineage cannot reconstruct from its own sources; and the finer clinical-provenance
taxonomy.

**If this lineage is retired:** the per-position chemistry table (32,898 records), the trial
register and its 22/16 cohort distinction, the chronicity qualification, the control inventory, the
47-check QC suite, byte-level reproducibility, and roughly 1,400 distinct sequences the alternate
does not hold.

**Neither is a superset of the other.** The honest read is that the original is stronger on
structure, chemistry and provenance machinery, and the alternate is stronger on exactly the
evidence class the Challenge prioritises.

## 6. What this document deliberately does not do

- **No merge, and no proposal to merge.** Record-level reconciliation across 149 shared sequences
  needs a construct-level crosswalk that distinguishes reference identity from tested-material
  identity. That is Tier 0 work and it is gated.
- **No recommendation of a winner.** I built one of the two.
- **No re-grain.** See the companion receipt on observation grain.

## 7. For German

1. **Are the 238 non-human-primate rows worth preserving at the cost of carrying two lineages**,
   or should they be a targeted re-extraction into one?
2. **Is the alternate's `evidence_class` taxonomy the one to standardise on?** It is finer than
   this lineage's on clinical provenance, and adopting it is a schema change, not a merge.
3. **The 149 shared sequences are not 149 shared experiments.** Same base sequence can differ by
   sugar, base, linkage, strand, conjugate and formulation. Before anything is deduplicated, the
   rule for when two records are the same *construct* is yours.
