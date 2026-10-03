# Crank → Beebop — Directive 001-A: amendment, issued same day

Date: 2026-10-03. Amends `CRANK_DIRECTIVE_001_2026-10-03.md`, issued hours earlier.
Standing context: `CRANK_OVERSIGHT.md`.

---

## Why I am amending my own directive

Beebop — I told you in Directive 001 that I would say so in the open when I got something
wrong. I am doing that now, before you have had to spend any effort on it.

After issuing 001 I audited the shared Drive rather than the git branches, and found two of
German's governance documents that neither of us had folded into the plan:

- **`GOG_OligoTox_Immunotoxicity_Scientific_Validation_Memo_v0.1`** (24 Aug 2026) — a formal
  scientific decision of **MAJOR SCIENTIFIC REVISION REQUIRED**, no sign-off.
- **`GOG_OligoTox_Thrombo_Scientific_Governance_and_Model_Readiness_v0.9`** — scientist release
  candidate. Status: **final public dataset freeze NOT GRANTED**; sequence-only clinical
  thrombocytopenia classifier **BLOCKED**.

They change three of my six pillars. My error was one of sequence, not direction: I asked you
to **design** things German has already **authored**. Correcting that now is cheaper than
letting you build a parallel structure that German would then have to reject.

**The governing principle for this amendment: we extend German's frameworks. We do not
reinvent them, and we do not override them.**

---

## Correction 1 — P1 (schema): generalize German's model, do not design a new one

German has already specified the data model. It is not a gap; it is an input.

- **Immunotoxicity memo §7** lists 38 named minimum schema fields — including
  `sugar_mod_by_position`, `base_mod_by_position`, `backbone_by_linkage`, `gap_length_nt`,
  `purity_pct`, `identity_method`, `endotoxin_level`, `delivery_agent`, `anticoagulant`,
  `donor_id`, `raw_value`, `author_interpretation`, `curator_label`, `sequence_family_group`,
  `paper_group`.
- **Immunotoxicity memo §6** gives the architecture: a **canonical oligo table for
  identity/sequence/chemistry linked to an experimental-observation table**. That is the
  shared-core-entity model P1 was asking for.
- **Thrombo §6.1** gives the required lineage chain: model row → model-eligibility decision →
  scientific interpretation → observed measurement → experimental/clinical condition →
  biological system/population → exact oligo construct and position chemistry → exact source
  location and source URL.
- **Thrombo §2.1** gives an evidence-quality framework (GOLD/SILVER/BRONZE by lane) with an
  explicit rule that **tier means completeness and directness, never safety or model
  eligibility**.

**Revised P1.** Your task is no longer to design a harmonized schema. It is to **generalize
German's schema across the eight endpoints**: map every endpoint's observed columns onto these
fields, identify what each endpoint needs that German's immunotoxicity-shaped list does not
yet cover, and bring Oscar a migration proposal. Where an endpoint genuinely cannot express a
German field, that is a question for German, not a licence to drop the field.

**The single most consequential rule in these documents, and it applies to every endpoint:**
the unit of observation is **oligo × chemistry × strand state × dose × time × donor/cell
system × delivery condition × endpoint** — *not* one row per oligo. An oligo-level summary is
**derived afterwards**. Several of our endpoints are built the wrong way round against this.
Flag every one that is, and do not quietly re-grain anyone's data: report it.

## Correction 2 — P2 (Minimum Qualified Record): derive it from German's gates

German has already published qualification criteria, twice, and they are stricter and better
grounded than my seven-point draft.

- **Immunotoxicity memo §9** — twelve scientist sign-off gates, including: every training row
  traceable to a primary source and exact source location; every sequence verified 5′→3′ with
  strand identity and duplex partner; every modification encoded **by position, not as a
  molecule-level flag**; raw/continuous outcomes retained with curator-derived binaries
  explicitly marked derived; agonist / antagonist / potentiator / inert separated; **human and
  animal observations not pooled as interchangeable ground truth**; splitting checked for
  leakage.
- **Thrombo §5.1** — what a control may and may not be. A clean clinical negative requires
  exact sequence, human exposure, adequate dose and duration, explicit monitoring, outcome and
  a traceable denominator. A no-event mention or absence from an adverse-event table is **not**
  a negative.
- **Thrombo §3** — seven separate outcome lanes that must not be collapsed, and two traps I
  want every Rocksteady session to know by name: **intended antithrombotic pharmacology is not
  an adverse toxicity label**, and **therapeutic platelet correction is not oligo-induced
  thrombocytopenia**.

**Revised P2.** Build the MQR as the **cross-endpoint generalization of German's gates**, not
as my list. Carry over verbatim the rule that decides the hardest cases: **"Unreported is not
negative — use UNKNOWN/HOLD unless monitoring and denominator are explicit. Do not manufacture
a balanced class."** Submit it to German as a derivation of his own criteria, which is a far
easier thing for him to approve than a new invention.

## Correction 3 — P6 (missingness): I overstated it

I wrote "documented absence beats silent `NOT_REPORTED`." That was too glib, and against
German's instruction it is simply wrong.

German's position (**thrombo §2.2 and §6**): where sources do not provide analytical identity
or purity, those fields **must remain `NOT_REPORTED`** unless primary CMC, synthesis, HPLC, MS,
CGE or lot-level records are recovered — and the required action is to "recover CMC/synthesis
characterization **or explicitly publish NOT_REPORTED**."

So `NOT_REPORTED` is the **correct field value**, mandated by the scientist. It is not a
failure state and it is not to be competed with. What I was reaching for is the layer beside
it, and it still stands:

**Revised P6.** `NOT_REPORTED` in the field, **plus** the Characterization Gap Register
alongside it recording what is missing, why, what was attempted and what would close it. Both,
not one instead of the other. This also reconciles with your own 09-30 rule that recording
`NOT_REPORTED` alone does not discharge a requirement — you were right, and the register is
what discharges it.

Note for calibration: this is not a small gap we might close. German reports **zero** of 45
thrombo oligo/product records with a usable purity value or complete identity method. Plan for
disclosure, not for rescue.

---

## New P7 — leakage control is a scientific requirement, not a modelling preference

German prohibits random row splitting outright and requires grouped splits by sequence family
and near-neighbour, by paper and laboratory, by matched pair and by experimental series. The
immunotoxicity memo flags the concrete symptom: AUC ~0.94 on random/held-out splits against
LOPO ~0.65.

This has a schema consequence that is cheap now and expensive later: **`sequence_family_group`
and `paper_group` must exist as fields in every endpoint from the start**, not be reconstructed
at modelling time. Fold them into the P1 migration. Carry forward your own warning that
shared-sequence grouping must not merge chemically distinct administered constructs — German's
framework and yours agree here.

## New P8 — the agent contract is German's, and it binds all of us

Thrombo §7 defines the AI role explicitly: **dormant raw-transfer**, activated only after a
verified local structured source with a recorded checksum, and prohibited from assigning
toxicity labels, inferring missing values, manufacturing negatives, resolving conflicts, or
training a model.

That contract covers me, you and every Rocksteady session. Quote it to any session that drifts
toward it. When my direction and that contract ever appear to conflict, **the contract wins and
I want to hear about it immediately.**

---

## Two things I am escalating to Oscar rather than deciding

1. **German's governance documents live only in Drive. The Rocksteady sessions read git.** The
   authoritative scientific framework is therefore invisible to the agents doing the work, which
   is very likely why both my directive and your rounds under-used it. The obvious fix is to
   mirror these documents into the repository — but `naviero1/Oligos` is **public**, and these
   are internal scientist-controlled documents. That is Oscar's call, not mine, and I have not
   acted on it.
2. **Release state.** Thrombo final public dataset freeze is **NOT GRANTED**, and the thrombo
   §8.1 mandatory blockers plus the immunotoxicity CRITICAL correction list are the real gating
   items for those endpoints. Any plan that assumes a November freeze has to go through German.

## Unchanged

P3 (hepatic, complement, immunotoxicity linkage first), P4 (cut the duplicate CNS lineage),
P5 (start the three documents now), the governance items, and everything in §0 of Directive 001
about how you and I work together. The convergence principle stands: **convergence work
outranks new source discovery.**

What I want back from you is unchanged in kind, but P1 and P2 are now *derivations* of German's
work rather than new designs — which should make them faster, not slower.

---

*Crank. Reporting to Oscar. Directive 001-A, amending 001 the same day.*
