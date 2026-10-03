# Bounded human-laboratory chemistry recovery — completed

**To:** Beebop, copy Crank · **From:** Rocksteady (coagulopathy) · **2026-10-03**
**Branch:** `claude/coagulopathy-oligos-toxicity-ap70gf`

Done as instructed, in place of the 325 row-to-trial links. Five staged and held sources, four
of which carried recoverable chemistry, constructs already represented, source and batch linkage
preserved in `sources/chemistry_recovery.json`. No unlinked trial row claimed, no chemistry
inferred, no acceptance specification converted into a measured value. No severity label computed.

## 1. What came back — small, and that is the finding

| | |
|---|---:|
| Position-resolved chemistry rows ingested | **106** |
| Constructs they cover | **1** (`COG-OLG183`, Pse08-29) |
| Construct-level facts recorded | 55 |
| Supplier statements recovered | 12 — **0 lot numbers**, none stated anywhere |
| Explicitly not recoverable | 13 |
| `modifications.csv` | 1,039 → **1,145** rows, 52 → **53** oligos |
| Structural QC | 112 → **118** checks, all pass |

**Position-resolved chemistry exists in exactly one of the four sources.** The other three print
no position-keyed legend, and the extraction emitted **zero** position rows for them rather than
expanding a whole-molecule descriptor. That was the correct call and I want it on record as the
load-bearing result: `COG-S057` says *"phosphorothioate oligonucleotide"* at molecule level, and
it was refused as a per-position basis, because a class descriptor does not say which linkages
are PS. Verified independently: the document has no position numbering, no PS count and no
linkage map.

So the strict human-laboratory lane moves from 34 compounds with zero position-resolved
chemistry to 33. The lane's problem is not extraction quality. It is that these papers do not
publish per-position chemistry.

## 2. The defect this turned up, in data already shipped

**Eleven compounds record sequences citing a document this repository does not hold.** All
eleven `COG-S074` compounds cite *Supplementary Table S1*. The held article cannot stand in:
125,483 bytes, **zero** runs of 12+ consecutive A/C/G/T — it prints no nucleotide sequence at
all — and **zero** occurrences of the string `Table S1`. The `sugar_modifications` basis for all
eleven also quotes that absent table's column header, so the chemistry basis is unverifiable from
held sources too.

**§K gate 1 (traceable source and exact location) and gate 2 (sequence verified there) fail for
eleven rows already in the dataset.** It was not caught because `verify_against_sources.py`
checks numeric values and quotes and never checked that a *sequence* resolves at its locus.

Recorded, not repaired: `sequence_locus_held = FALSE`, a `sequence_locus_not_held` gap-register
class, and three validator checks that make the condition impossible to hold silently. Disposition
is German's — review-queue **item 11**, where my recommendation is to acquire the supplementary
file and keep the flag until it lands. The acquisition request is Oscar's to action.

One case went the other way and is fixed: `COG-OLG030` (HD22) cited `COG-S010`, which prints no
sequence either — but `COG-S008` **does** print the 29-mer in Introduction body text, identical to
`sequence_base`. Locus repointed to where it verifies.

## 3. The one judgment call, referred rather than taken

`backbone_linkage_3p = PO` on 105 internal positions rests on an affirmative *"the M08s-1-based
bivalent aptamers were chemically unmodified"*, with the naming bridge to this construct verified.
The source **never prints a linkage term**. Unmodified DNA is phosphodiester to any chemist, and
it is still a step the document does not take in words, so it is declared in every row's `basis`
as `CURATOR EXPANSION`, enforced by a validator check, reversible in one query, and put to German
as review-queue **item 10** — including the precedent it sets against the `COG-S057` refusal.
Sugar (`DNA`) is separately stated and survives either ruling.

## 4. Verification, and the defects I honoured rather than shipped

Adversarial pass, one verifier per source, 141 claims: `COG-S074` **CLEAN** (116 checked),
`COG-S010` DEFECTS_FOUND (10), `COG-S008` DEFECTS_FOUND (12), `COG-S057` **CLEAN** (3).
Injection scan: 8 of 8 agent transcripts, suspicious **NONE**, outbound requests **0**.

Three defects found and acted on, not argued with:

1. **`COG-S010` quote not verbatim** — the document reads *"We therefore conjugated…"*, the
   recovery wrote *"we conjugated…"*. Quote **withdrawn**, status recorded.
2. **`COG-S008` locus claim wrong** — the HD22 text opens its own paragraph; the preceding
   sentence is NU172 entering phase II, not HD1. Locus **corrected**.
3. **`COG-S057` "single-stranded" is not stated** — the words *single*, *strand*, *duplex* and
   *complementary* appear nowhere in that document. **Demoted** to curator characterisation.

Also honoured: `[M08s G2]c` is a separate added antidote and is **not** recorded as a
constitutive duplex partner; the 5' poly-dA linker and amino modifier belong to HD22-7A-DAB and
are not carried onto HD22; the 11F7t 2'-O-methyl linker is not carried onto HD22 either.

## 5. Two bugs in my own guards, found while wiring this up

- **The position-integrity check I first wrote was wrong**, and it failed loudly on 391
  pre-existing rows. It indexed `sequence_5to3_asprinted`, which is the *source's rendering*: it
  carries conjugate prefixes (`40 kDa mPEG-GUGGAcuAuAcc…`, so position 1 lands on the "4" of the
  PEG mass) and in several sources **letter case is the modification legend**
  (*uppercase-2'F, lowercase-2'O-Methyl*), so a case-sensitive compare reads a chemistry
  annotation as a different base. Corrected to index `sequence_base` case-blind: **1,145 of
  1,145 position rows match, zero mismatches.** The data was right; my check was not.
- **Two stale QC counts** in `README.md` and `schema.md`, caught by the matcher Crank made me
  fix. Both were live figures hard-coded in prose, so they drift by construction; both now point
  at the script instead of restating a number.

## 6. Still blocked, unchanged

The 325 row-to-trial links remain untouched per your reversal.
`CRANK_ANSWERS_AND_ROUTING_2026-10-03.md` answer 6 still instructs "do the 325 first" and is
superseded by it — flagging so the branch is not read as contradicting itself.

---

CHEMISTRY RECOVERY COMPLETE — 106 POSITIONS, 1 CONSTRUCT · 11 SEQUENCES FLAGGED UNVERIFIABLE ·
NO CHEMISTRY INFERRED · NO SEVERITY LABEL COMPUTED · ITEMS 10 AND 11 AWAITING GERMAN
