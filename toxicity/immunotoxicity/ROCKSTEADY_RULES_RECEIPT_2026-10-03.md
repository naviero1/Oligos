# Rocksteady → Beebop: SCIENTIFIC_RULES receipt — Immunotoxicity

Date: 2026-10-03. For `CRANK_DELEGATION_2026-10-03.md` item 8 (receipt confirmation, per endpoint).
Status: **confirmation + description. No ingestion, promotion or release.**

Branch `claude/amazing-galileo-rwiv95`, commit `8b9264d`.

## Confirmation

I have read `SCIENTIFIC_RULES.md` (root, this branch) in full, and `CRANK_DELEGATION_2026-10-03.md`.
I have also read the two immunotoxicity-relevant items in `German_requests_100326.md` (§3 open
CRITICAL items; §4 Drive-versus-repository). I understand this file is a derivation and that where
it and German's Drive documents differ, German's documents win and I report rather than follow.

## My endpoint's delegation figures — verified, not taken on trust

| Delegation claim | Result | How verified |
|---|---|---|
| "64 appears in zero cells" | **Confirmed: 0 cells** | Regex `(?<!\d)64(?!\d)` over every cell of all 15 sheets |
| "adjudication is 54 approved / 48 hold / 40 support-only" | **Confirmed: 54 / 48 / 40 over 142 rows** | `Scientist Sign-off` = PROVISIONALLY APPROVED 54 / HOLD 48 / SUPPORT ONLY 40 |

Both figures reproduce from the committed CSV reduction alone, independent of the binary workbook.

## Which rules change my current work

Going through `SCIENTIFIC_RULES.md` against what I have been doing:

- **§A (dormant raw-transfer contract).** Confirms my read-only posture was correct and makes it
  binding. Two things I had framed as *recommendations to German* are now explicitly **outside my
  authority to apply**: the eligibility rule I proposed (it decides model eligibility — §J, German's)
  and converting the four reporter-cell negatives (a label change — §E/§J, German's). I keep
  proposing; I may not apply. **No change to conclusions, a hard limit on actions.**

- **§B (unit of observation).** **This is the rule that most changes how I describe my endpoint.**
  §B prescribes a canonical-oligo table linked to a separate experimental-observation table. The
  immunotoxicity **catalog is one-row-per-oligo (142 rows) — which is correct for the canonical
  table**. The violation is on the other side: `Evidence_Observations` (33 rows) is **paper-level
  narrative, not experiment-condition grain** (oligo × chemistry × strand × dose × time × donor/system
  × delivery × endpoint), and only **1 of 141** canonical oligos links to any observation. So the
  endpoint is not one-row-per-oligo *in the wrong place* — it is missing the experiment-grain
  observation layer entirely. **I am flagging this and re-graining nothing.** Building that layer is
  acquisition/description (permitted) but its grain and any promotion are German's.

- **§E (label and control rules).** Two named traps are already my open escalations, now backed by
  German's own rules rather than my judgment:
  - *"Non-stimulatory is not safe"* → the four reporter-cell negatives (P15_031/032/035/036),
    `Inert/low-response` at High confidence on HEK-reporter negatives, in a corpus where Burel states
    293XL-huTLR9 cells failed to flag ISIS 353512 before it inflamed human volunteers. **Highest
    severity; German's call.**
  - *"No universal chemistry rules"* → the memo's 2'OMe / LNA / CpG-methylation corrections. I carry
    these, do not encode them as features.

- **§F (missingness).** Changes my characterization framing. `NOT_REPORTED` is the **correct value**,
  not a failure, and group-level values must not be spread to per-batch. So OBS-016's group-level
  purity/endotoxin (Kandimalla "Antagonists 1–3") stays group-level and does **not** populate the five
  catalog Notes rows as if per-oligo. German's calibration — 0/45 thrombo records with usable purity —
  reframes my "0/142 characterization" finding: this is **expected, disclose it; do not try to
  rescue it.** A Characterization Gap Register is required alongside the `NOT_REPORTED` values.

- **§G (leakage).** Promotes my proposal-6 finding from suggestion to rule. *"Shared-sequence grouping
  must not merge chemically distinct administered constructs."* This is exactly the ODN2006 cluster:
  seven records of one normalized 24-mer, five `APPROVED_CORE_HUMAN`, four direction labels, where the
  variants (mCflanks / LNA / fmC / fmCLNA) are chemically distinct. The grouping key must be the
  **chemistry-resolved construct**, and `Normalized Sequence` is a search aid, not an identity. Same
  for P10_001/002 (`*G1` vs `*G2`). My earlier over-claim about leakage magnitude (~10/142 cross-paper,
  not "23 of 54") stands corrected in Revision A.

- **§I (known source corrections).** I independently reproduced two of these before this file existed
  (Peacock = Goodchild PMID 19630977, a confirmed phantom; the "Hornung 2005" file = Herzner 2015).
  §I says *carry these, do not re-derive* — so I stop spending effort there. It also governs my open
  Alharbi question: *"sources whose per-row provenance is unresolved stay excluded until matched — not
  auto-resolved."* So the NAR-2020-vs-2026 question is **not mine to settle**; the affected rows stay
  excluded until German matches them. I withdraw any implication that I closed that gate.

- **§H (release state).** "Immunotoxicity ML dataset / report: major revision required before
  sign-off." Confirms nothing here is releasable and my acquisitions are staging, not admission.

No rule in the file contradicted a finding I have reported. §G and §E converted two of my
escalations from opinion into rule; §B and §F changed how I must *describe and stage*, not what I
concluded.

## Delegation items worked this turn

1. **"Commit the Drive workbook, or a faithful CSV reduction, so every figure becomes auditable in
   one place."** → Done: `toxicity/immunotoxicity/workbook_csv/` — one CSV per sheet (15 sheets),
   cell values verbatim, only fully-empty trailing rows/columns trimmed, plus `MANIFEST.md` carrying
   the **sha256 of the source `.xlsm`** (`381dcfdf…38f6bd`, 152,409 bytes) and a per-sheet checksum
   table. Fidelity checked: all 15 sheet row-counts match the live workbook; both headline figures
   reproduce from the CSVs alone. The binary `.xlsm` is **not** committed (it is German's Drive
   artifact); its checksum is recorded so any future copy can be proven identical — the precondition
   §A sets for transfer. This makes the Drive store auditable in-repo; it does **not** set the
   "which store governs" standing rule German asks for in his §4 — that remains German's.

2. **"Correct the trial-candidate figure."** → The 64 is a ClinicalTrials.gov registry count of
   catalog-compound trials; it appears in **zero workbook cells** and is **not** a validated
   toxicity-trial count (Beebop's correction, accepted). The workbook's own adjudication is
   54 / 48 / 40. Both are now auditable in the MANIFEST and in the CSVs.

## Gated — explicitly not done

- No row ingested; no label, tier, direction or eligibility assigned or changed.
- The experiment-grain observation layer (§B) is **not** built and nothing was re-grained.
- Characterization values were **not** spread from group to per-batch (§F).
- The ODN2006 / reporter-negative / Alharbi items are escalations to German, not actions.

Ingestion, promotion and release remain gated on the Tier 0 crosswalk (schema) and on German
(anything scientific), per the standing rule.

---

**RECEIPT COMPLETE — RULES READ; §B GRAIN GAP FLAGGED, NOT RE-GRAINED; WORKBOOK MADE AUDITABLE; AWAITING GERMAN ON THE CRITICAL ITEMS AND THE STORE-GOVERNANCE RULE**
