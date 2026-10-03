# Characterization Gap Register — hepatotoxicity

Required by `SCIENTIFIC_RULES.md` §F: *"Alongside it, record in the Characterization Gap Register
what is missing, why, what was attempted, and what would close it. The field value and the
register are both required: the value states the truth, the register discharges the requirement."*

Opened 2026-10-03 at commit `8466cd7`. Covers every construct currently staged for this endpoint.
**`NOT_REPORTED` is the correct value in every row below, not a failure state.**

Cause taxonomy adopted from the complement endpoint's register rather than reinvented, so the two
remain comparable. Complement's register records German's finding that numeric release purity is
**systematically withheld by every regulator** (FDA redacts `(b)(4)`, EMA deletes commercially
confidential information, PMDA masks) — which is why `withheld_as_confidential` is a distinct and
non-closable cause rather than a variant of "not reported".

| Cause | Meaning | Closable? |
|---|---|---|
| `not_reported_by_source` | the publication omits it | possibly — a synthesis or CMC paper may carry it |
| `deferred_to_citation` | the source points at another paper for it | possibly — acquire that paper |
| `withheld_as_confidential` | a regulator holds it and redacts it | **no**, from public sources |
| `unobtainable_paywalled` | named, located, behind a verified paywall | on access only |
| `access_unverified` | believed inaccessible, but the barrier has not been verified | unknown until checked |

## Coverage

| Field | Populated | `NOT_REPORTED` | Denominator |
|---|---:|---:|---|
| `purity_pct` | 0 | 9 | 9 staged constructs |
| `identity_method` | 0 | 9 | 9 staged constructs |
| `endotoxin_level` | 0 | 9 | 9 staged constructs |

Burdick 2014's 80 constructs are **not yet staged** and are therefore not in these denominators.
When staged they will add 80 constructs at the same three fields, on the `deferred_to_citation`
cause below. Stating that now so the denominator does not appear to improve by omission.

## Register

### R1 — Sewing 2016, 7 sequenced constructs (`SEW16-SSO32/33/35/36/37/43/47`)

| | |
|---|---|
| Missing | `purity_pct`, `identity_method`, `endotoxin_level` |
| Cause | `not_reported_by_source` |
| Why | The paper is an assay-establishment study. Its Materials and Methods describe cell isolation, culture and readouts; it does not describe oligonucleotide synthesis, purification or analytical identity, and names no supplier for the tool SSOs. |
| Attempted | Full-text sweep of the Europe PMC XML (`sha256 6a5f45eb…`) for purity, HPLC, UPLC, mass spectrometry, ESI, endotoxin, counterion, desalt, lot and batch: **zero hits** in the oligonucleotide context. Supplementary bundle (`sha256 eda70881…`) inspected: figures and one supporting table, no CMC content. |
| Would close it | The Roche synthesis record for the myd88 tool set, or a sibling publication from the same group that states it. Sewing 2016 cites no synthesis reference of its own — unlike Burdick, there is no citation to follow. |
| Status | **Open, no identified route.** Not a paywall; the information appears not to be published. |

### R2 — Sewing 2016, 2 unsequenced constructs (`SEW16-Survivin`, `SEW16-Bcl2`)

| | |
|---|---|
| Missing | `sequence_5to3`, all per-position chemistry, plus the three characterization fields |
| Cause | `not_reported_by_source` |
| Why | Described only as "two historical development SSOs targeting Survivin and Bcl2". No sequence, no chemistry, no identifier is given. |
| Attempted | Full-text and figure-legend read. The paper cites references 19–21 for their clinical liver effects but does not identify the molecules by name, code or sequence. |
| Would close it | References 19–21, then an identity route from the named clinical molecule to a published sequence. **This is a two-step inference and the second step is the dangerous one** — matching a target name to a sequence found elsewhere would assert an identity this source does not support. Not to be done without German. |
| Status | **Open.** These two carry the endpoint's only clinical anchor (grade 3 liver enzyme increases in phase 1, per the authors) and cannot enter a sequence-linked dataset from this source. |

### R3 — Burdick 2014, 80 constructs (staged next)

| | |
|---|---|
| Missing | `purity_pct`, `identity_method`, `endotoxin_level` |
| Cause | `deferred_to_citation` |
| Why | Methods state "All oligonucleotides were synthesized as previously reported (10)." Reference 10 is Stanton et al. 2012, *Nucleic Acid Ther.* 22:344–359, doi `10.1089/nat.2012.0366`, PMID 22852836. |
| Attempted | Europe PMC core record: `pmcid` null, `isOpenAccess N`, `hasSuppl N`, `inPMC N`. **The publisher's own access condition has not been checked.** |
| Would close it | Stanton 2012 full text and any synthesis supplement. Note that Robert Stanton is a co-author of Burdick 2014 itself, so this is the same group's method rather than an unrelated reference. |
| Status | **Open.** My earlier classification of this as a *confirmed paywall* was wrong and stays retracted — absence from PMC is not a paywall. Correct current class: `access_unverified`. Verifying the publisher condition is the next targeted provenance action, not a broad search. |

### R4 — Dieckmann 2018, 6 constructs (not staged; read for lineage only)

| | |
|---|---|
| Missing | `purity_pct`, `identity_method`, `endotoxin_level` |
| Cause | `not_reported_by_source` |
| Why | Zero hits across article and supplement for the full CMC token set. The paper names a supplier only: *"All LNA-ASOs and derivatives… were derived from Exiqon (Denmark)."* |
| Would close it | An Exiqon/Qiagen certificate of analysis for the specific lots, which is not a public artifact. |
| Status | **Open, no public route.** Compounded by a second problem recorded here because it bears on identity: Dieckmann Table 1 joins **Exiqon-supplied material** to **ALT values generated on Hagedorn's in-house material**. Characterization of one does not characterize the other. |

### R5 — Hagedorn 2013, 236-construct panel (not staged)

| | |
|---|---|
| Missing | per-construct `purity_pct` and `identity_method` |
| Cause | `not_reported_by_source` — at the per-batch grain |
| Why | **This is the one source that does publish characterization method**: IEX-HPLC purification, UPLC purity with fractions above **85%** pooled, and LC-MS to verify compound identity and purity. But it is a **process-level criterion applied to a batch**, never a per-compound value. |
| Would close it | Per-compound release data, which the paper does not contain. |
| Status | **Open at the per-construct grain; partially discharged at the method grain.** §F forbids spreading a group-level range across batches, so the 85% threshold must **not** populate `purity_pct` for any construct. It does, however, satisfy the Phase 2 methodology document's separate requirement for *"the methods used to purify and characterize oligo identity"* — the two requirements are distinct and this source meets one of them. |

## What this register says about the endpoint

Hepatic has **0 of 9** staged constructs with a purity value and no identified public route to one
for 9 of 9. German's calibration for thrombocytopenia — **0 of 45** records with a usable purity
value or complete identity method — is the same picture, and his instruction is to plan for
disclosure rather than rescue. Hepatic will disclose.

Exactly one targeted action could change any row here: **verifying Stanton 2012's actual publisher
access condition** (R3), which governs 80 constructs. That is a single check, not a search
programme, and it is the next provenance action for this endpoint.
