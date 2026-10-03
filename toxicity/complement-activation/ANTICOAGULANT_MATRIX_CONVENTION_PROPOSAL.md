# Proposal: a matrix and anticoagulant convention for human blood endpoints

**Status: PROPOSAL. Nothing is implemented. No other endpoint's files have been touched.**

Raised by Rocksteady, 2026-10-03, from the complement-activation research round
(`ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md`, §6). Oscar authorized drafting it. It is published on
`claude/amazing-galileo-rwiv95` only, because thrombocytopenia and coagulopathy live on other branches
and Beebop's instruction is to propose corrections rather than overwrite another endpoint's work.

**Scope: the three endpoints whose evidence is read out of human blood** — complement activation,
thrombocytopenia, coagulopathy. All three draw on overlapping human whole-blood, plasma and serum
experiments, and in several cases *literally the same papers*. None of the three currently records the
anticoagulant.

## The finding

Across the six human complement sources whose Methods were read first-hand this round:

| Source | Matrix | Anticoagulant as actually reported |
|---|---|---|
| Sewing 2017 (`PMC5673186`) | whole blood → plasma for ELISA | **"anticoagulant-sprayed vacutainer tubes" — chemical identity never given, no concentration, no catalogue number** |
| Mangsbo 2009 (`PMC2857538`) | whole-blood loop; hirudin plasma for pathway work | Corline heparinised surface **plus soluble heparin 0.5 U/mL**; EDTA 10 mM as stop. **The abstract calls the blood "fresh non-anticoagulated" — the paper contradicts its own Methods** |
| de Boer 2022 (`PMID 36104112`) | whole blood **and** plasma | **lepirudin 50 µg/mL**; EDTA 10 mM stop. Chosen deliberately: lepirudin "does not interfere with the complement cascade" |
| ARC-520 (`PMC5516171`) | **serum** for CH50, **plasma** for Bb | **not reported** for the complement plasma |
| Demirjian / QPI-1002 (`PMC5733816`) | plasma | K₂-EDTA Vacutainer |
| GalNAc3 integrated (`PMC6386089`) | not stated | **not reported** |

**Three of six do not report it. One contradicts itself. The three that do report use heparin, lepirudin
and EDTA — which are not interchangeable for complement.** Heparin modulates complement; EDTA abolishes
it, which is exactly why two of these studies use it as a *stop* reagent; lepirudin is selected
precisely for being inert. A dataset that pools a heparin-loop C3a with an EDTA-plasma C3a is pooling
two different assays under one column name.

A seventh source makes the point about matrix rather than anticoagulant. ARC-520 states, in one
sentence: *"Venous blood samples were collected and processed to produce **serum** (for complement CH50
analysis) **or plasma** (for split products-Bb analysis)."* Matrix was chosen **per analyte, inside a
single trial**. "Serum and whole blood are not interchangeable" understates the problem: serum and
plasma are not interchangeable *within one study*.

## Why a shared convention rather than three local fixes

1. **The same papers feed several endpoints.** Sewing 2017 is already cited by thrombocytopenia
   (`EXV-TMB-051`/`EXV-TMB-052`) for platelet activation and is being read here for complement — one
   acquisition, two endpoints, one anticoagulant question. Mangsbo and de Boer both report complement
   *and* cytokines. Paul 2010 reports coagulation, platelets and complement from one Chandler loop.
2. **The anticoagulant is a shared confounder, not an endpoint-specific one.** Citrate depletes the
   calcium that the classical and lectin complement pathways and much of the coagulation cascade both
   need. Heparin modulates complement and is a direct anticoagulant. EDTA abolishes complement. Any of
   them changes what a platelet, a clotting time and a split product mean, simultaneously.
3. **Three separate conventions would diverge**, and a later cross-endpoint merge would silently pool
   incompatible assays — the exact failure mode Beebop's deduplication rules exist to prevent.

## Proposed fields

Mandatory and non-null on **every** row whose observation derives from a blood, plasma or serum sample,
human or animal:

| Field | Values | Notes |
|---|---|---|
| `matrix` | `whole_blood` · `plasma` · `serum` · `csf` · `urine` · `tissue` · `cell_culture` · `cell_free` · `not_reported` | per analyte, not per study |
| `anticoagulant` | `none` · `citrate` · `k2_edta` · `k3_edta` · `lithium_heparin` · `sodium_heparin` · `heparin_unspecified` · `lepirudin` · `hirudin` · `ctad` · `other` · **`not_reported`** | the agent in the collection tube |
| `anticoagulant_concentration` | free text as printed, or `not_reported` | e.g. `0.5 U/mL`, `50 µg/mL` |
| `surface_treatment` | e.g. `corline_heparin_surface` · `none` · `not_reported` | a heparinised *surface* is not a soluble anticoagulant; Mangsbo has both |
| `stop_reagent` | e.g. `edta_10mM` · `none` · `not_reported` | the reagent used to halt activation before storage |
| `sample_handling` | free text — centrifugation, temperature, storage, time-to-processing | Mangsbo samples into EDTA at 1 h or 6 h; de Boer stores at −70 °C |
| `anticoagulant_provenance` | `stated_for_this_assay` · `stated_elsewhere_in_source_for_a_different_assay` · `inferred` · `not_reported` | **the trap field — see below** |

### The provenance field is the one that matters

Two sources in this round would have produced a fabricated anticoagulant without it, because each names
an anticoagulant for a *different* assay in the same paper:

- **Sewing 2017** names sodium citrate and ACD — for its **washed-platelet** workstream (PAC-1,
  P-selectin, Figures 1 and 5) only. Its complement data are Figure 6, from "anticoagulant-sprayed"
  tubes. Carrying citrate across would invent a detail the paper never claims.
- **ARC-520** names EDTA — in its **siRNA pharmacokinetic** methods. The paper never links it to the
  Bb plasma. Carrying it across would be the same error.

Both are cases where the honest value is `not_reported` while a careless extraction yields a confident
wrong answer. `anticoagulant_provenance` is what makes the difference auditable instead of invisible.

### Rules

1. **`not_reported` is mandatory where the source is silent, and is never replaced by a plausible
   default.** Three of six complement sources are silent. That is a finding about the literature, not a
   gap to be filled.
2. **Never carry an anticoagulant across assays within a source.** Record it only against the assay the
   source attaches it to.
3. **Where a source contradicts itself, record both and flag it.** Mangsbo's abstract says
   "non-anticoagulated"; its Methods say heparin 0.5 U/mL on a heparinised surface. The Methods are the
   specific statement and should govern, with the contradiction preserved.
4. **Matrix is per analyte.** One study may use serum for a functional assay and plasma for a split
   product, as ARC-520 does.
5. **A surface treatment is not a soluble anticoagulant.** Separate fields.
6. **Two rows may not share a numeric column across incompatible matrix/anticoagulant combinations**
   without an explicit, adjudicated comparability statement. German's call per endpoint.

## Cost, and what it is not

Seven fields, six of them free text or a short enum, populated at extraction time from text the curator
is already reading. No re-acquisition of any source is required. For complement it would be populated
from material already in hand for all seven sources.

It is **not** a comparability claim. Recording that one study used lepirudin and another heparin does
not make them poolable — it makes the question visible. Whether they may share a column stays with
German.

## What I am asking for

- **Oscar**: whether to propagate this to thrombocytopenia and coagulopathy, and if so by what route,
  given they sit on separate branches. I have deliberately not edited their folders.
- **German**: the comparability rule in item 6 — specifically whether any complement analyte measured in
  heparinised whole blood may ever share a numeric column with the same analyte measured in
  EDTA or citrate plasma.

## Evidence trail

Every anticoagulant statement above was read first-hand this round from the source's Methods, not from a
secondary summary. Per-source detail, with verbatim quotations, is in
`research-staging/working/access_verification_sewing_mangsbo_deboer.json` and
`research-staging/working/new_human_leads_verified.json`.
