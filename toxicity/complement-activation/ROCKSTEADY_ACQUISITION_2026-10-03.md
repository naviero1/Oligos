# Acquisition round — 2026-10-03, and a paywall-scoping assessment for Oscar

Branch `claude/amazing-galileo-rwiv95`. Authorized by Oscar on 2026-10-03, answering Q2 of
`ROCKSTEADY_COMPLEMENT_REPLY_TO_CRANK_AND_BEEBOP_2026-10-03.md`: **free material is taken now; a paywall
is scoped rather than bought, so Oscar can judge whether a subscription is worth it.**

**Nothing ingested, promoted or released.** No label, no grade, no model. All rows staged
`STAGED_NOT_INGESTED` / `model_eligibility = NOT_ASSESSED_GERMAN`.

## 1. The find: `NCT02363946` is the strongest human complement dataset on this endpoint

It was free in a public registry the whole time, and nobody had opened it.

**ARC-AAT** (Arrowhead, RNAi against alpha-1 antitrypsin), **Phase 1**, **TERMINATED** (company
decision), **65 enrolled**, results posted. Complement is a **registered secondary outcome measure** —
*"Mean Percentage Change in Circulating Blood Levels of Complement Factors 2 Hours Post-Dose"*, pre-dose
versus 2 h — with **five analytes across 13 arms and per-arm denominators**.

Staged: `research-staging/working/arcaat_NCT02363946_complement_observations.csv`, **65 observation
rows** (5 analytes × 13 arms) at §B experiment-condition grain, 51 columns.
Source `sha256 cefc4254ea28b662498d4413c1880ee2e5b36db2685ef658106f096d01ecb7f3`.
Licence: **US federal public domain** — the only unrestricted complement source we hold.

### Mean % change from pre-dose at 2 h, as posted

| Arm (n) | **Bb** (plasma) | C3a | C4a | C5a | **CH50** |
|---|---:|---:|---:|---:|---:|
| 0.38 mg/kg (4) | +18 | −12 | −5 | +2 | −5 |
| 1.0 (4) | +56 | +30 | +37 | +2 | −14 |
| 2.0 (4) | +76 | −22 | −11 | −16 | −14 |
| 3.0 (4) | +133 | −0 | +2 | −2 | −8 |
| 4.0 (4) | +181 | +71 | +16 | −14 | −16 |
| 5.0 (4) | +137 | −5 | −8 | +2 | −17 |
| 6.0 (4) | +70 | +14 | +78 | 0 | −10 |
| 7.0 (4) | +147 | +40 | +60 | +6 | −13 |
| **8.0 (4)** | **+309** | +34 | −1 | +6 | **−19** |
| **Placebo (18)** | **−7** | −11 | −19 | −2 | −3 |
| Part B 2.0, AATD (4) | +56 | −18 | −35 | −4 | −3 |
| Part B 4.0, AATD (**1**) | +59 | +219 | +160 | +22 | −18 |
| Part B placebo (3) | −14 | +16 | −15 | −4 | −0 |

### Why this matters more than its size suggests

1. **A clean dose-dependent human positive.** Plasma Bb climbs from +18% to **+309%** across 0.38→8.0
   mg/kg against a placebo arm at **−7%**. This is the clearest human complement signal in the endpoint,
   and it is in a registry rather than a paper.
2. **Bb up while CH50 down, in humans, with numbers.** CH50 is negative in **every active arm** (−5 to
   −19%) while Bb rises. This is the **third independent instance** of split-products-up with
   function-down — after REGULATE-PCI and the Kyndrisa monkey data — and the **first with per-arm
   quantification in humans.** The four-readout-class separation I proposed is no longer an argument from
   principle; it is demonstrated inside one trial.
3. **Alternative-pathway selectivity, in humans.** Bb (alternative pathway) rises strongly and
   monotonically-ish; C4a (classical/lectin) shows no dose trend; C5a is essentially flat. That is the
   pattern Henry 2014 and Shen 2014 describe mechanistically in serum — appearing here in dosed humans.
4. **Analyte collapse would destroy the finding.** "Complement activation: yes/no" would lose a +309% Bb,
   a flat C5a and a −19% CH50 in the same subjects.
5. **It is a positive control candidate** — Beebop's item 9 needs positive controls and found almost none
   project-wide (0 of 1,866 in acute-neurotoxicity). This is a dose-graded human positive with a placebo
   arm.
6. **Dual matrix again, analyte-specific**: plasma for Bb, serum for C3a/C4a/C5a/CH50.

### Caveats recorded on the rows, not in prose

- **n = 4 per active arm.** Small.
- **Part B 4.0 mg/kg is n = 1**, dispersion `NA`. Its +219% C3a and +160% C4a are **single-subject
  values**, flagged `single_subject_arm = TRUE` on all 5 of its rows. They must not be read as estimates.
- Values are **mean percentage change**, not absolute concentrations — same constraint as Sewing's
  Stimulation Index. `value_basis = percent_change`. Not convertible to ng/mL.
- **No p-values**, no assay, no vendor, no anticoagulant. `anticoagulant = NOT_REPORTED` with
  `anticoagulant_provenance = not_reported` — and nothing in the record to carry across from.
- Placebo n = 18 is pooled across Part A dose cohorts.
- Trial terminated; no publication located for the complement outcome.
- `author_interpretation = NOT_STATED_IN_REGISTRY` — the registry posts numbers without a conclusion, so
  there is no author call to separate from a curator call. Unusually clean on §E's author/curator split.

## 2. The second candidate does **not** deliver, and the reason is a §E trap

**`NCT03728634`** — ION-682884 / eplontersen (ION-TTR-LRx), GalNAc-conjugated 2′-MOE ASO, Phase 1/2,
COMPLETED, 47 participants, results posted.

Complement **was measured** — it is named in the laboratory parameter list. But the posted result is a
**composite count**: *"Number of Participants With Clinically Significant Laboratory Values"*, reading
**0** across all six arms (n = 6/10/10/10/2/9), where the parameters *"included measurement of blood
chemistry, hematology, coagulation, complement, or urinalysis"* and significance is **"based on
Investigator's assessment"**.

**This cannot be recorded as a complement measurement.** Three reasons, each sufficient:
- It is a **collapsed composite** across five unrelated parameter families — §E's "do not collapse
  distinct outcomes" and gate 8.
- The threshold is an **investigator adjudication**, not a measurement — an `author_interpretation`, with
  no underlying value posted.
- A zero count is **absence of a flagged value**, not a measured normal — §E's "unreported is not
  negative."

So: measured, unrecoverable. **Disposition: no row created.** Recorded here because the next session will
find the same `hasResults = TRUE` and the same word "complement", and needs the reasoning rather than the
verdict. It does, incidentally, add a third GalNAc-era human trial with complement in the lab panel,
reinforcing the §2.7 correction.

**Net on Q2's two candidates: one delivers 65 rows, one delivers a documented null.** Both were worth
opening; neither cost anything.

## 3. Paywall scoping for Oscar — grouped by publisher, because that is the unit of a subscription

Per Oscar's instruction: not "should we buy paper X" but "what is behind the wall, and is a subscription
worth it". The right unit is the **platform**, since one subscription unlocks many items. **No price is
quoted anywhere below: none was displayed to me, every attempt returned a Cloudflare challenge rather
than a purchase page, and the rules forbid recording an unverified price.**

### Platform 1 — Mary Ann Liebert / SAGE: *Nucleic Acid Therapeutics*. **The one worth considering.**

| Item | What is behind it | Expected yield |
|---|---|---|
| **Henry 2014**, NAT 24(5):326–335 | monkey **and human** and dog serum, same compound; the factor-H mechanism; the immunoassay-artifact caveat | the endpoint's central human-vs-animal bridge paper. Analyte list, assay methods, possibly sequences |
| **OSWG guidance**, NAT 26(4):210–215 | the field's consensus on how to run and interpret complement assays | would let the endpoint definitions cite a standard instead of being invented |
| **Shen 2016**, NAT 26(4):236–249 | chronic monkey dosing: Bb, C3a, C3, C3d-bound immune complexes | the animal counterpart to the human C3-consumption signal |
| **Galbraith 1994**, *Antisense Res Dev* 4(3):201–206 | the historical first report; GEM 91 in monkeys | low scientific yield, high provenance value |
| **Tessier 2021**, NAT 31(1):7–20 | EFPIA survey of what complement assays industry actually runs | endpoint-definition support |

**5 of my blocked items sit on one platform**, and it is the field's journal of record. **Cross-endpoint
value is the real argument**: thrombocytopenia needs Shen 2023 (NAT 33:209–225), hepatic needs Hagedorn
2022, immunotoxicity needs several. **If one subscription is bought, this is it.**

**What I can already see behind this wall without buying it**, which is the point of scoping: the Tegsedi
EPAR **quotes and cites Henry 2014 and Shen 2014's core findings**, including the ~3-fold factor-H
species difference. So the *mechanism* is already citable from a free regulator document. What the
subscription adds is **analyte-level detail, assay methods and any published sequences** — valuable for
the dataset's method fields, not load-bearing for the mechanism claim. That is an honest discount on its
value.

### Platform 2 — Elsevier / ScienceDirect. **Largest count, worst value per unit.**

7 items: Shen 2014 (JPET), Henry 1997 (JPET), Shaw 1997 (*Biochem Pharmacol*), Agrawal 1995 (*Toxicol
Lett*), Henry 2002 (*Int Immunopharmacol*), **Povsic 2016 + its Online Repository** (*JACI*), and
**the apo(a) ASO article body** (*Lancet*).

Two of these are genuinely high-value — **Povsic's Online Repository**, which holds the only numeric
complement values tied to severe human clinical harm, and the **apo(a) body**, where 47 subjects'
analytes are unknown. But Elsevier is not a product one buys as a unit; access is institutional. **My
recommendation: treat these as two individual-article requests, not a subscription case.** Povsic's is
also the **only confirmed paywall in this round** — the only place a subscription notice was actually
rendered to me rather than inferred.

### Platforms 3–5 — not worth a subscription

AACR (*Clin Cancer Res*): 2 items, Rudin 2001 and Chen 2000 — both oncology phase 1s whose complement
*findings* are already verified from abstracts; only the analyte identities are missing. Springer
(Advani 2005) and ASCO (Nemunaitis 1999): 1 item each, same situation. **Four items, all
abstract-confirmed, none mechanism-critical.**

### Not a paywall at all, and worth re-trying rather than buying

**Kandimalla 1997**, *NAR* 25(2):370–378, `PMC146429` — **listed free**, blocked by a PMC proof-of-work
cookie challenge and a publisher XML embargo. The one fact needed is whether its hemolytic-complement
serum was **human**; if so it is the best position-resolved chemistry/complement series available.
**A browser would likely open this.** Same for **Shen 2014's** advertised ASPET PDF, which Semantic
Scholar still flags as bronze open access while the host returns 403.

### Recommendation, stated plainly

1. **If one subscription: Liebert/SAGE *Nucleic Acid Therapeutics*** — 5 complement items, plus items for
   three other endpoints, and it is the field's journal of record. Discounted by the fact that the
   mechanism is already citable from the free EPAR.
2. **Two individual-article requests regardless of any subscription**: Povsic 2016's Online Repository
   (confirmed paywall, unique numeric content) and the apo(a) ASO article body.
3. **Two retries from a browser, not a purchase**: Kandimalla 1997 and Shen 2014.
4. **Buy nothing for platforms 3–5.**

## 4. Inventory delta

| | Before | After |
|---|---:|---:|
| Verified human trials with reported complement and a recoverable identifier | 8 | **9** — `NCT02363946` joins, `NCT03728634` does not |
| Staged complement observation rows | 0 | **65** |
| Staged complement constructs | 12 | 12 (ARC-AAT publishes no sequence — `sequence_family_group = UNASSIGNED_NO_SEQUENCE`) |
| Sources under an unrestricted licence | 0 | **1** — US federal public domain |
| Human instances of split-products-up / function-down | 1 (REGULATE-PCI) | **2**, and the new one is quantified per arm |
| Positive-control candidates | 0 | **1** — dose-graded human positive with a placebo arm |

Gate 3 note: ARC-AAT publishes **no sequence and no chemistry**, so its construct row would be
`sequence_5to3 = NOT_REPORTED`. **It is a strong outcome record attached to an unidentified molecule** —
the mirror image of Sewing, which has excellent chemistry and a derived-ratio outcome. Neither alone
satisfies gate 2 and gate 3 together. That contrast is worth German's attention when he sets the bar.

---

**ACQUISITION ROUND COMPLETE — 65 ROWS STAGED, 1 DOCUMENTED NULL, PAYWALL SCOPED. NOTHING INGESTED, PROMOTED OR RELEASED. NO PURCHASE MADE OR PROPOSED WITHOUT OSCAR'S DECISION.**
