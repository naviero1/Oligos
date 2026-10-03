# Characterization Gap Register — complement activation

Required by `SCIENTIFIC_RULES.md` §F: *"Alongside it, record in the Characterization Gap Register what is
missing, why, what was attempted, and what would close it. The field value and the register are both
required: the value states the truth, the register discharges the requirement."*

Opened 2026-10-03. Covers every construct and source currently staged for this endpoint.
**`NOT_REPORTED` is the correct value in every row below, not a failure state.**

## Cause taxonomy

German's decision queue item 2 establishes that numeric release purity is **systematically withheld by
every regulator** — FDA redacts as `(b)(4)`, EMA deletes commercially confidential information, PMDA
masks with asterisks — and asks whether that blocker may be discharged by documented missingness rather
than closure. §F alone does not distinguish *why* a field is empty, and the distinction decides whether a
gap is closable at all. This register therefore records cause:

| `*_gap_cause` | Meaning | Closable? |
|---|---|---|
| `not_reported_by_source` | the publication simply omits it | **possibly** — a synthesis or CMC paper may carry it |
| `withheld_as_confidential` | a regulator holds it and redacts it | **no**, from public sources |
| `deferred_to_citation` | the source points at another paper for it | possibly — acquire that paper |
| `unobtainable_paywalled` | named, located, behind a confirmed paywall | on access only |

**Complement's gaps are currently all `not_reported_by_source`.** No complement construct's purity has
been sought from a regulator and redacted; the gap is a publication-level omission. That is a materially
better position than thrombocytopenia's and should not be reported as though it were the same wall.

## Register — Sewing 2017 constructs (12 of 12)

Source: Sewing S, Roth AB, Winter M, Dieckmann A, Bertinetti-Lapatki C, Tessier Y, McGinnis C, Huber S,
Koller E, Ploix C, Reed JC, Singer T, Rothfuss A (2017), *PLoS One* 12(11):e0187574, PMID 29107969,
PMC5673186, CC-BY. Staged file `sewing2017_constructs_perposition.csv`,
`sha256 cd4d4b092e112982cb3ab56e6de88101d523933dcf147185c20a829a71f6a3fc` on the raw supplement.

| Field | Constructs affected | Value | Cause | Attempted | What would close it |
|---|---:|---|---|---|---|
| `purity_pct` | **12 of 12** | `NOT_REPORTED` | `not_reported_by_source` | full text and supplement read first-hand; no purity figure, no HPLC/CGE trace, no Tm, no mass-spec confirmation anywhere | a synthesis or CMC description for the Roche tool-ON panel, or the supplier's certificate of analysis. **No supplier is named**, which is itself a blocker |
| `identity_method` | **12 of 12** | `NOT_REPORTED` | `not_reported_by_source` | as above | same |
| `endotoxin_level` | **12 of 12** | `NOT_REPORTED` | `not_reported_by_source` | as above | same. Relevant here: endotoxin is itself a complement activator, so its absence is a live confounder, not a clerical gap |
| `supplier` | **12 of 12** | `NOT_REPORTED` | `not_reported_by_source` | Methods name vendors for the ELISA kits, the plate reader and the pathway-control reagents, but **not for the oligonucleotides** | author correspondence — not authorized, and not proposed |
| `sugar_mod_by_position` | **3 of 12** — `(AC)8 LNA`, `(AC)9 LNA`, `(AC)10 LNA` | `NOT_REPORTED` | `orphaned_legend_in_source` | Table 2's own legend promises *"bold letters: locked nucleic acid"*; **there is no bold in the table.** Verified three independent ways — the publisher JATS XML holds zero `<bold>` elements in Table 2, the PDF embeds no bold monospace font (page 7 is `CourierNewPSMT` regular throughout), and the publisher's table image shows no bold glyph | the authors' original sequence file, or any later paper reusing the same panel with positions printed |
| `gap_length_nt` | **3 of 12** (same) | `NOT_REPORTED` | `orphaned_legend_in_source` | as above | as above |
| `stereochemistry_by_linkage` | **12 of 12** | `NOT_REPORTED` | `not_reported_by_source` | no stereochemistry is reported and the constructs are not described as stereopure | a GSRS record, pending German's item 5 ruling. Field exists now so a later pull cannot be lost |

### The inference that is deliberately NOT in the field

Prose in the same paper does constrain the LNA placement — Methods: *"had three flanking LNA
modifications on each side"*; Results: *"flanking three nucleotides of (AC)8, (AC)9 and (AC)10"*; Fig 5
legend: *"without and with 3 LNA modifications in the flanks."* That implies 3-10-3, 3-12-3 and 3-14-3
gapmers.

**It is recorded here and nowhere else.** §C makes per-position encoding the primary representation and
§F forbids substituting an inferred value for a per-batch one, so `sugar_mod_by_position` reads
`NOT_REPORTED` with `sugar_mod_provenance = orphaned_legend_in_source`. Promoting the inference into the
field is German's call, not a curator's convenience.

The consequence is worth stating plainly: **the Phase 2 requirement for "the location of all chemical
modifications in each oligo" cannot be satisfied for 3 of these 12 constructs from this source.** That is
a disclosure, not a rescue.

## Register — human clinical sources

| Source | Construct identity available? | Characterization | Cause |
|---|---|---|---|
| **ARC-520** `NCT01872065` | **yes** — both RNAi trigger sequences printed in full (Table 1), with 2′-modified sugars, deoxy residues, an inverted-dT 3′ cap and a `dTsdT` phosphorothioate overhang | purity, identity method, endotoxin: `NOT_REPORTED` | `not_reported_by_source`. ⚠ reading `f` as 2′-fluoro is an **inference from table notation**, not stated in prose — so per-position sugar assignment is itself partly provenance-flagged |
| **QPI-1002** `NCT00554359` | **no** — sequence not published in the source | all `NOT_REPORTED` | `not_reported_by_source` |
| **GalNAc3 integrated** `PMC6386089` | compounds named with Ionis IDs and 20-mer sequences in Table 1 | not assessed this round | `not_reported_by_source` |
| **ApTOLL** ×2, **CALAA-01**, **REGULATE-PCI** | sequences `UNVERIFIED` | all `NOT_REPORTED` | `not_reported_by_source` |
| **The 11 regulatory studies** | n/a — sponsor protocol codes only, **zero NCT numbers across all four EMA reports** | purity expected `withheld_as_confidential` per German item 2 | **not yet attempted.** Must not be recorded as `not_reported_by_source` without checking |

## Calibration against German's figure

German reports **zero of 45** thrombocytopenia oligo/product records with a usable purity value or
complete identity method. Complement's equivalent, at this commit, is **zero of 12** staged constructs —
the same result on a much smaller denominator, and from publication omission rather than regulator
redaction.

**Plan for disclosure, not rescue.** The honest Phase 2 statement for this endpoint is that no staged
construct carries tested-material characterization, that the cause is publication-level omission, and
that for three constructs even the modification locations are unreadable from the source that supplies
them.

## Open items this register hands on

- **Oscar / Beebop**: whether `purity_gap_cause` and `identity_gap_cause` should be adopted
  project-wide. They are not in §C; German's item 2 is the reason they exist, and the thrombocytopenia
  regulator-redaction finding is the case that motivates them.
- **German**: whether the prose-derived LNA placement may ever be promoted into
  `sugar_mod_by_position`, and under what provenance value.
- **Not proposed**: author or supplier contact. Not authorized, and no round has authorized it.
