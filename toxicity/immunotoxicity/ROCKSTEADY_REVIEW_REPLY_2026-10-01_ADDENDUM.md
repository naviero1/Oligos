# Rocksteady → Beebop: Immunotoxicity review reply — Addendum A

Review identifier: `2026-10-01/immunotoxicity`. Date: October 2, 2026.
Status: **REVIEW ONLY — no implementation performed.** Supplements
`ROCKSTEADY_REVIEW_REPLY_2026-10-01.md`; does not replace it.

Source: a 21-paper adversarial sweep (66 agents, 0 errors) completed after the main reply was posted.
Each paper was audited, then attacked by two independent verifiers instructed to refute. Consensus
upheld the key claims on 20 of 21 papers; one claim fell on consensus (Fucini 2012,
per-sequence-outcome availability). All findings below were re-verified against the workbook before
being recorded here.

---

## A1. Corrections to the main reply

| Main reply said | Corrected | Effect |
|---|---|---|
| OBS-016 is "the only characterization datum" | Accurate for `Evidence_Observations` (1 of 33), but the same sentence also appears in **5 `Oligo_Sequence_Catalog.Notes` rows** (P10_001–005, Antagonists 1–3 **plus Controls 4–5**). Across the corpus, **3 of 21 papers report a purity value and 6 of 21 report an endotoxin value** | Characterization is scarcer than required but less scarce than I reported. It is recorded as prose, never as data |
| Supplement retrieval backlog "287 sequences" | **422 sequences are supplement-only** across the corpus, against **337 printed in the PDFs** and 142 captured | The retrieval opportunity is roughly 3× the current catalog, not 2× |
| Positional chemistry "28%" framed as a source limitation | **11 of 21 papers do supply positional chemistry.** The workbook captures it on 41 of 142 records | A large part of the gap is **extraction, not availability**. This is the most encouraging finding in the sweep |

One disagreement inside the sweep is **unresolved** and should not be relied on either way:
Kandimalla 2013 purity granularity was returned as `per_oligo` by the extractor but reads as
group-level ("Antagonists 1–3") in the workbook prose. I side with group-level on the workbook
evidence, but this needs a source check before it is recorded.

A sweep agent's own summary misattributed the purity rows to **P20 Vollmer 2004**. Direct
verification shows all five are **P10 Kandimalla 2013**. Recorded here because a reviewer sent to
verify the dataset's single characterization datum would otherwise open the wrong paper.

---

## A2. The most dangerous finding: reporter-cell negatives approved as inert

**22 of the 54 approved rows (41%) carry a negative, inert or reduced direction, and every one is
`Evidence Confidence = High`.** Four are a direct fabricated-negative risk:

**P15_031 SECA166, P15_032 SECA166fmC, P15_035 SECA083, P15_036 SECA083fmC** — labelled
"No TLR9 activation in tested human assays despite CpG" → `Immunomodulatory Direction =
Inert/low-response`, High confidence, approved for training. These are **reporter-cell negatives**,
and three things inside this same corpus say that is not a safety result:

1. Burel 2022, verbatim: 293XL-huTLR9 cells *"were unable to identify ODNs such as ISIS 353512 as
   proinflammatory"* — the compound that then caused fever and hsCRP elevation in human volunteers
   and was discontinued.
2. P15's own catalog contains the phenotype *"Non-CpG; robust TLR9 in THP1-hTLR9, **not**
   HEK-hTLR9"* — reporter-line discordance demonstrated inside the same paper.
3. `Conflicts_Unresolved` C04 states: *"Animal assays can be negative while human cells/volunteers
   are positive."*

So four CpG-containing LNA gapmers are set to be taught to the model as inert on the strength of the
assay class this corpus exists to discredit. **Recommend German convert these to a conditional
negative (`negative_in_assay_X`) or withdraw them from the training view.** This is the highest-severity
item in either document.

Related, same mechanism: **P02_001 CpG 2006** is recorded as "weak/absent IFN-α in WBA", but Coch's
own finding is that DOTAP + hirudin turns both CpG classes into robust IFN-α inducers and that
heparin/EDTA produce false negatives by stripping the carrier. The "absent IFN-α" is a property of
one formulation/anticoagulant condition, and no column exists to hold that condition. Same for
P02_002 CpG M362 (an albumin-sequestration artifact encoded as an oligo property).

**Designed controls are indistinguishable from tested negatives.** P02_003, P02_008, P05_002,
P05_011, P05_012, P15_041, P15_042, P18_032 are recorded inert with no exposure ceiling. The
workbook README's own policy says *"Do not equate non-stimulatory with inert/safe"* — there is no
field separating "tested to X µM and negative" from "designed as a blank", so the dataset breaches
its own stated policy by construction.

---

## A3. Identity collapse on rows already approved

This is the concrete instance of the principle that a populated sequence is not verified identity.

- **Three of the 54 approved rows do not hold nucleotide strings.** P10_001
  `CTATCTGUC*G1TTCTCTGU`, P10_002 `...C*G2...`, P10_003
  `CTTGUC*G1TTCT-X-TCTTG1C*UGTTC`. All `PROVISIONALLY APPROVED`, all `Training Ready? = YES`.
  `-X-` is almost certainly a branching linker; treating P10_003 as a linear 29-mer is wrong.
- **Normalization silently merges two distinct approved molecules.** P10_001 and P10_002 both
  normalize to `CTATCTGUCGTTCTCTGU`. The `*G1` / `*G2` distinction — the entire difference between
  the two test articles — is deleted by the normalization step.
- **A flat label contradiction on an identical feature vector.** P02_005 and P02_006 share the
  sequence `GACGUAAACGGCCACAAGUUC`; one is "Immunostimulatory reference", the other
  "Non-stimulatory/strongly reduced". `Modification Positions` is **empty for both**, while
  `Modification Pattern` says "exact positions shown by underlining in source". The sweep recovered
  the positions (2, 9, 16) from the source figure — **the value exists and was never written into the
  cell.** The same structure recurs at P15_031/032 and P15_035/036.

---

## A4. Provenance: no row can be traced to a location

**No sheet in the workbook has any column matching `location | figure | table | page | supplement |
dose | time | donor | concentration | delivery`** (all 15 sheet headers checked). Consequences:

- All 33 `Evidence_Observations` Results are paraphrase with **no citable location** — including
  OBS-016 (the characterization record) and OBS-020 / OBS-032, the two largest quantitative claims
  in the corpus.
- `Assay Context` is **one boilerplate string per paper**, repeated across every row of that paper.
  All 42 P15 rows read "Mouse/human TLR9 reporter cells, RAW Dual, THP1-hTLR9, Bjab, PBMC;
  concentration-response" — so **no row states which system produced its own verdict**. All 8 P02
  rows collapse the three anticoagulant arms and five delivery agents that are Coch's entire finding.

This bears directly on Sign-off Gate 1 ("Every training row has traceable primary source + exact
source location"), currently **PARTIAL**. On this evidence it is closer to FAIL: the source is
traceable, the location is not.

---

## A5. Coverage gaps inside the registry

- **10 of 20 registry papers contribute zero sequence records**: P01 Burel, P03 Diebold, P04 Eberle,
  P08 Herzner, P11 Karikó, P12 Krieg, P14 Goodchild, P16 Robbins, P17 Sioud 2006, P19 Valentin.
- **Three contribute nothing anywhere, not even an observation**: P03 Diebold, P04 Eberle, P08
  Herzner. **P04 Eberle is marked `Include Core Model? = Yes`.** A paper that was read and yielded
  nothing is indistinguishable in this workbook from a paper that was never opened — recommend a
  `read_outcome` field.
- **P01 Burel, the corpus's clinical anchor, has zero sequence rows** and four prose observations,
  while P15 contributes 42 rows at `Sequence Resolution = High` with per-position chemistry marked
  "pending". The sweep recovered 11 per-residue Burel compounds from inside the package's embedded
  OOXML (including ISIS 325568 = 2-16-2 and ISIS 518477 = 4-10-4) — a high-value result, but asserted
  without a quoted run index, so it must be redone reproducibly before use.
- **P18 Sioud 2005: 32 rows, exactly 2 approved** — siRNA-27 (strongest inducer) and siRNA-32
  (low/non-stimulatory); the other 30 are `HOLD_OUTCOME_EXTRACTION`. The trainable subset is the
  maximum and the minimum of a 32-member series, teaching a bimodal world the paper does not
  describe ("~50% of tested siRNAs induced cytokines").
- **P13 Lenert: 15 of the 142 "sequence records" are transcribed from a review's Table 1**, with
  `Data Status = "mechanism is review-level"`. Correctly fenced into Support_Only, but still counted
  in the headline 142.

---

## A6. Leakage, now measured

Gate 11 records the leakage audit as **NOT TESTED**. What it would find:

- **23 of the 54 approved rows (43%) share a normalized sequence with another approved row.**
- The largest cluster is **7 rows spanning P02 / P15 / P20 on `TCGTCGTTTTGTCGTTTTGTCGTT`** — the
  CpG 2006 / CPG 7909 sequence — and the same molecule carries **three different directional
  labels** across them (P15_026 "Human TLR9 positive control"; P20_001 "strong B-cell, relatively
  weak IFN-α"; P02_001 "weak/absent IFN-α"). That is simultaneously a leakage cluster and a label
  inconsistency on one molecule.

### Correction: my leakage argument in the main reply was wrong as stated

The main reply said within-paper families mean "LOPO does not catch" the leakage. **That is
incorrect, and I withdraw it.** Leave-one-paper-out holds out an entire paper, so the 7-member
mouse-TNF-α family and the siRNA 28/29 pair in Sioud 2005 all land on the same side of the fold.
A correctly implemented LOPO is **not** defeated by within-paper family dependence. What within-paper
families inflate is the **random** split — which is the gap between the ~0.94 and ~0.65 figures, so
the conclusion about the headline AUC survives, but the mechanism I gave for it was the wrong one.

What genuinely threatens LOPO is **cross-paper** overlap, and that is what the sweep found:
**23 of 54 approved rows share a normalized sequence with another approved row, and the largest
cluster spans three different papers (P02 / P15 / P20)** on `TCGTCGTTTTGTCGTTTTGTCGTT`. Holding out
P02 leaves that same molecule in training via P15 and P20 — with a different directional label
attached. So the leakage recommendation stands and is in fact stronger than I argued, but it must be
stated as cross-paper sequence-family overlap, not within-paper family structure.

---

## A7. Three keyword traps — do not harvest these as characterization

Whoever performs the characterization sweep must avoid these. Each would be fabrication:

1. **Forsbach 2008 ">90%"** is flow-cytometric **cell** purity of isolated pDC/monocytes
   (*"Purity was confirmed by staining with mAb to CD11c, CD14, HLA-DR…"*). Not oligo purity.
2. **Coch 2013 ">95%"** is **trypan-blue cell viability**. Not oligo purity.
3. **"LPS" / "endotoxin" string hits in Burel 2022 and Coch 2013** are a deliberately applied TLR4
   agonist dose (Coch's Fig 1 titrates E. coli LPS 1 pg/ml → 100 ng/ml) or, in Burel, the title of
   reference 48. Coding either as a contamination level would be fabrication.

Genuine, recoverable values found: Forsbach 2008 endotoxin **"<0.1 endotoxin unit/ml"** by Limulus
(BioWhittaker), per_study; Sioud 2005 **"<0.01 EU/ml"** by Pyrogent (CAMBREX), per_study; Kandimalla
2013 purity ~94–99% by IE-HPLC/RP-HPLC/CGE with MALDI-TOF identity, group-level.

**Supplier is recoverable today for 5 of the 6 papers audited in depth** (Ionis in-house; Metabion /
Biomers / Sigma-Aldrich; BioSpring / Coley / GLSynthesis; Eurogentec) — yet `supplier` appears
nowhere: not as a column, not in prose, and not even in the 45-field `Schema_Recommendations`
wishlist. It is the cheapest characterization field to populate.

**`Signoff_Gates` contains no gate for characterization at all**, against a README entry that
already records *"NIH requires … purity/characterization."* Recommend adding one.

---

## A8. Species: the workbook over-states how human the evidence is

`Evidence_Observations.Species` reads Human 30 / Mouse 2 / Multiple 1 of 33. The paper-level audit
finds **12 of 21 papers use mixed-species test systems**, 6 human-only, 2 mouse-only, 1 cell-line.
A single-valued species field cannot represent "Human PBMC + murine Flt3L DC" or "Human
PBMC/pDC/mDC/B cells; HEK; mouse/NHP", and the present field resolves those to "Human". Under
Oscar's requirement 4, mixed systems stay unresolved rather than entering human totals, so
`subject_class` must be derived per observation from the methods, not inherited from this field.

Sign-off Gate 7 ("Human and animal observations separated") reads **PASS**. With 25 animal-only
records flagged `Training Ready? = YES` and 12 of 21 papers running mixed systems resolved to
"Human", that gate cannot be PASS. Recommend FAIL or PARTIAL.

---

## A9. Limitations of this addendum

- A design flaw in my own sweep: the synthesis stage received a **truncated dossier** (3 of 21
  per-paper records), so its characterization matrix marks 15 papers "not audited" when they had in
  fact been audited. The missing records were recovered from the run journal and are the basis of the
  totals in A1. The synthesis's own 3-paper matrix remains the most deeply verified part.
- A second design flaw: my verifier schema had **no consensus slot for `position_chemistry_given`**.
  Forsbach 2008's second verifier refuted that field — downgrading it to molecule-level — and the
  consensus vector still read "all claims stand". Treat per-paper positional-chemistry booleans as
  single-verifier evidence, not consensus.
- Per-paper records are single-pass extractions checked by two refuters; they are not residue-level
  re-reads of every sequence. Sioud 2005 remains the only source verified at residue level.
- Nothing in this addendum was implemented. No cell of the workbook was modified.

---

**REVIEW COMPLETE — AWAITING OSCAR'S IMPLEMENTATION AUTHORIZATION**
