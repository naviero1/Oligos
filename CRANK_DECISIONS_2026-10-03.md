# Oscar's decisions — 2026-10-03

Four redistribution and schema decisions arising from `SOURCE_EXPANSION_REGISTER_2026-10-03.md`,
put to Oscar and answered the same day. Recorded here so the basis for every downstream row is
traceable to a dated decision rather than to an agent's inference.

**Context that matters for all four: no purchase decision was pending.** Across eleven scouts,
zero leads were `PAYWALLED_VERIFIED` — not one price, purchase page or payment requirement was
observed anywhere. Every decision below is about **redistribution terms**, not money.

---

## D-1 — PMDA review reports: **facts only; documents not redistributed**

**Observed, verbatim:** the PMDA English site states "Copyright (c) Pharmaceuticals and Medical
Devices Agency, All Rights Reserved." The documents retrieve freely (viltolarsen 1,634,124 bytes;
tofersen 1,567,366 bytes; both HTTP 200, no login). Each carries: "This English translation … is
intended to serve as reference material … In the event of any inconsistency between the Japanese
original and this English translation, the Japanese original shall take precedence."

**Oscar's decision:** extracted **facts** may be ingested and cited. The **documents are not
redistributed**. The **Japanese original is cited as the authority**, with the English translation
identified as reference material.

**Why it matters:** this is the only route to a per-position regulator convention for a PMO, and
it supplies a second independent specification for nusinersen.

**Carried instruction:** nobody fetched the PMDA Site Policy page (`/english/0013.html`). Fetch it
once and record what it says — a more permissive clause may exist that no one has read. That
fetch does not reopen the decision; it refines the basis string.

## D-2 — TGA AusPARs: **retry from different egress**

**Observed, verbatim:** TGA copyright policy states "You are not permitted to re-transmit,
distribute or commercialise the material without prior written approval," with requests directed
to `tga.copyright@tga.gov.au`; reproduction is otherwise permitted only as fair dealing under the
Copyright Act 1968. **No price was observed.** Six oligonucleotide AusPARs were located by exact
filename (nusinersen, patisiran, vutrisiran, givosiran, inclisiran, donidalorsen), but **no scout
retrieved a document body** — HTTP 503, then transport errors.

**Oscar's decision:** retry retrieval from a different egress path. Output is **not
redistributable**; treat anything recovered on the same facts-only basis as D-1.

**Scope discipline:** worth is MEDIUM at best and strictly as a cross-check against the EMA and
PMDA nusinersen specifications. **Time-box it.** If a second egress attempt fails, stop and record
the failure rather than spending further sessions — the value does not justify an open-ended hunt,
and the register already carries the specification from two other regulators.

## D-3 — ND-licensed and conditional-grant material: **adopt the facts-not-expression basis**

**Observed, verbatim:** PMC11255113 and PMC13571576 both carry `cc by-nc-nd`. Soule 2022 carries a
time-limited Elsevier grant: "These permissions are granted for free by Elsevier for as long as
the COVID-19 resource centre remains active." The Soule 2016 Duke thesis has `dc.rights` **empty**
— freely downloadable (9,470,413 bytes, HTTP 200) with no stated reuse licence at all.

**Oscar's decision:** adopt the **"extracted values are facts, not expression"** basis
project-wide — the reasoning the thrombocytopenia branch already applies. Specifically:

1. Extracted measurements from ND-licensed sources **may ship as derived rows**.
2. The Elsevier grant is recorded **verbatim** in `sources.csv` under a new value
   `conditional_publisher_grant`. It is **not** relabelled `CC_BY`, and its time limitation
   travels with it.
3. Where a CC BY sibling exists, **prefer it** (PMC7870851 for Wave chemistry; Kim 2023 for
   per-position notation).
4. **Immediate free fix, do now:** coagulopathy ships **30,885 words of verbatim publisher prose
   across 687 rows** in the `verbatim_quote` column, inside a file intended to ship openly. Drop
   or hash that column on those rows. The numbers beside it are measurements; the quote is the
   authors' expression. This removes the exposure and loses no measurement.

**Recorded caveat, raised before the decision and accepted with it.** Crank advised that this is a
**legal judgment, not a technical one**, and that Crank is not qualified to vouch for it. The
verbatim licence terms were supplied and verified; the soundness of relying on them was not
assessed. Oscar adopted the basis with that caveat on the table. **The PADP must state this basis
explicitly** — licensing is the section a reviewer will scrutinise, and an unstated basis reads
worse than a declared one. If counsel becomes available, this is the item to spend it on.

## D-4 — Phosphorothioate stereochemistry: **German decides, before any schema change**

**Observed:** GSRS carries per-linkage stereochemistry. Rovanersen returns
`'Phosphorothioate R-isomer' → 1_13` and `'Phosphorothioate S-isomer' → 1_1;1_5-1_12;1_14-1_15`.
These are **stereopure molecules**. Our schema has **no stereochemistry column**, and recording
them as plain `full_PS` would be silently and unrecoverably wrong.

**Oscar's decision:** this goes to **German first**, as a scientific decision, **before** any
schema change and **before** GSRS ingestion.

**Crank's note, recorded because it corrects Crank:** I had recommended simply adding the column
in Tier 0. Oscar is right and I was wrong about the category. Whether two stereoisomers are
distinct constructs — and whether they may be pooled for modelling — is the same question as
German's standing rule that shared sequence or family grouping **must not merge chemically
distinct administered constructs**. It is his ruling, not an engineering convenience.

**Consequence:** GSRS **acquisition proceeds** (it is the highest-value find on the register and
closes modification positions for ~24–30 held molecules). **GSRS ingestion is blocked** pending
German. Stage the pull with raw stereochemistry strings preserved verbatim and unparsed; do not
normalise them into any existing chemistry field.

---

## Entering German's decision queue

D-4 joins the queue, and it should be put to him with the evidence rather than as an open
question. The queue now reads:

| # | Decision | Blocks |
|---|---|---|
| G-1 | Authoritative CNS lineage, after crosswalk | Tier 1 migration for that endpoint |
| G-2 | Thrombocytopenia freeze (currently **not granted**) and its six mandatory blockers | Release |
| G-3 | Immunotoxicity CRITICAL correction list | Sign-off on that endpoint |
| G-4 | Whether Drive or repository is authoritative where they diverge | Baseline reconciliation |
| G-5 | **Phosphorothioate stereochemistry: are stereoisomers distinct constructs, and may they be pooled for modelling?** | **GSRS ingestion; the schema's chemistry representation** |
| G-6 | Whether DEVOTE (NCT04089566) passes all seven clean-negative gates | The blocked clinical classifier |

G-5 and G-6 are both newly raised by this round and both have a concrete artifact waiting on
them. Put them to German together.

## Per-regulator licence table — a correction, not a decision

Independent of all four decisions: we have been generalising **"regulator document = government
work = public domain."** That reaches **US federal agencies only**. EMA permits commercial reuse
with attribution; TGA forbids redistribution without written approval; PMDA is All Rights
Reserved. Build a per-regulator licence table with **each term quoted verbatim**, and stop using
one basis string across them. This repairs the legal basis currently claimed under 216
thrombocytopenia rows for documents the EMA published.

---

*Crank. Decisions put to Oscar and answered 2026-10-03.*
