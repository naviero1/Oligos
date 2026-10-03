# Hepatic research staging

**Nothing in this directory is ingested, promoted, validated or model-eligible.** It is raw
transfer under `SCIENTIFIC_RULES.md` §A, held separately from any dataset. Schema is gated on
Beebop's Tier 0 crosswalk; anything scientific is gated on German.

There is still **no hepatic dataset** anywhere in this repository — 0 rows on all 10 branches,
verified 2026-10-03. This staging does not change that and must not be read as changing it.

## Held

| File | What it is | Licence |
|---|---|---|
| `sources/Sewing2016_PLoSONE_pone.0159431.pdf` | the article, 15pp | CC BY |
| `sources/Sewing2016_Table1_sequences.{tif,png}` | publisher renders of Table 1, the construct table | CC BY |
| `sources/Sewing2016_Fig8_mouse_human_hepatocytes.jpg` | Figure 8, the mouse/human comparison | CC BY |
| `sources/Sewing2016_supplementary_files.zip` | Europe PMC supplementary bundle | CC BY |
| `stage_sewing2016.py` | the transfer script; regenerates both tables | — |
| `sewing2016_constructs.csv` | canonical oligo table, 9 constructs | — |
| `sewing2016_condition_level.csv` | observation table, 73 rows | — |

Sewing 2016 is CC BY, so the source files are redistributable here with attribution. That was
established by licence check before acquisition, not assumed.

## Why two tables

`SCIENTIFIC_RULES.md` §B requires a canonical oligo table holding identity and chemistry, linked
to a separate experimental-observation table, at the grain
`oligo × chemistry × strand state × dose × time × donor / cell system × delivery condition × endpoint`.
This source supports that grain natively: Figure 8 reports each construct at three
concentrations in two readouts and two species. The structure follows the precedent already
worked by thrombocytopenia (`sewing2017_condition_level.csv`) and complement
(`sewing_extraction_grain_reference.csv`) — a different Sewing paper, reused method.

## Extraction method and source locator — per transferred value

Stated here because a reader must be able to tell a transcribed cell from an estimated one.

| Block | Source locator | Method | Digitised? |
|---|---|---|---|
| Construct sequences and per-position chemistry | **Table 1** | publisher renders `Sewing2016_Table1_sequences.tif` (1572×623, original) and `.png`, read visually at 2× upscale, grayscale, unsharp | **No** — printed glyphs |
| Mouse in vivo ALT, 7 values | **Table 1**, column "ALT [U/L]" | same render | **No** — printed numerals |
| Human hepatocyte LDH and ATP, 7 constructs × 3 concentrations | **Figure 8A** | `Sewing2016_Fig8_mouse_human_hepatocytes.jpg`, read visually at 1.7× upscale | **No** — see below |
| Mouse hepatocyte LDH and ATP, 2 constructs × 3 concentrations | **Figure 8B** | same render | **No** |
| Human hepatocyte LDH and ATP, 2 constructs × 3 concentrations | **Figure 8C** | same render | **No** |

**Figure 8 is a printed numeric heat-map table, not a plot.** Every value is printed as a numeral
in its own cell; the colour fill is decoration over the number. No value here was read off an
axis, interpolated from a bar height, or otherwise estimated, and no pixel-measurement tool was
used. That is why these rows carry numerals rather than ranges, and it is the answer to the
standing question about whether hepatic digitised anything: **it did not.**

The authors' own colour-scale bins are recorded below as source-specific and are not labels.

Where a value is absent it is `NOT_REPORTED` with the source's stated reason — `SEW16-SSO47`
carries no in vivo ALT because, in the table's own footnote, that group "had to be sacrificed
early due to severe toxicity."

## What these rows do and do not pair — contracted 2026-10-03

An earlier version of this README and of three sibling files described this source as giving the
same seven constructs across mouse in vivo, mouse hepatocyte and human hepatocyte. **That is
wrong and is withdrawn.** Measured from `sewing2016_condition_level.csv`:

| Rows | System | Constructs | Source |
|---:|---|---|---|
| 42 | human hepatocyte in vitro | the **7 sequenced** | Fig 8A |
| 7 | mouse in vivo | the **7 sequenced** | Table 1 |
| 12 | human hepatocyte in vitro | the **2 unsequenced** | Fig 8C |
| 12 | mouse hepatocyte in vitro | the **2 unsequenced** | Fig 8B |

**No construct appears in all three systems.** The sequenced seven span human-in-vitro and
mouse-in-vivo. The two unsequenced constructs span human- and mouse-in-vitro and have no in vivo
arm. Because `SSO47` has no numeric in vivo value, the sequenced set yields **6 complete
numerical pairs, not 7**.

What this supports is a **bounded two-system comparison proposal over 6 sequence-linked
constructs**. It does **not** demonstrate validated extrapolation, and it is not available for
model evaluation until German rules on grouping — Sewing's Table 1 is the same 5 × 15 mg/kg
experimental series as Hagedorn 2013, which §K gate 10 names as leakage to be checked.

The source does test the tool SSOs in mouse hepatocytes in Figures 2 and 7. **Those values are
not staged and have not been read.** They are a future acquisition, not support for anything
written here.

## Two things that must travel with these rows

**Fig 8 values are means.** The legend reads "Data are means from 2 experiments in triplicates".
Replicate-level values are not published, `donor_id` and `donor_class` are `NOT_REPORTED`, and
the replicate structure is recorded per row rather than inferred.

**Author binning is source-specific.** Figure 8's colour scale (ALT <150 / 150–300 / 300–800 /
>800; LDH <120 / 120–150 / 150–200 / >200; ATP 0–20 / 20–40 / 40–60 / >60) is the authors' own.
It is not carried as a label and is not a general threshold rule — §E.

## Counts, with denominators

| Quantity | Value |
|---|---|
| Constructs | 9 |
| Constructs with a published sequence | **7 / 9** (Survivin and Bcl2 are named by target only) |
| Constructs with per-position chemistry | **7 / 9** |
| Constructs with a purity value | **0 / 9** |
| Constructs with an analytical identity method | **0 / 9** |
| Observation rows | 73 |
| — human cell system | **54** |
| — animal (mouse in vivo serum ALT 7, mouse hepatocyte 12) | **19** |
| Verified human clinical trials contributed | **0** |

The 7 sequenced constructs target **mouse** Myd88 and were applied to human hepatocytes, where
they have no cognate target. The observed cytotoxicity is therefore not target-mediated. That is
the authors' point, and it is a fact a reader of these rows needs.

`SEW16-Survivin` and `SEW16-Bcl2` carry the only clinical anchor in this source — the authors
report grade 3 liver enzyme increases in phase 1 for both — and publish **no sequence** for
either. They cannot enter a sequence-linked dataset from this source. That is a gap to record,
not to close by matching a name to a sequence found elsewhere.

## Characterization gap (§F)

`purity_pct`, `identity_method` and `endotoxin_level` are `NOT_REPORTED` on 9 of 9 constructs.
`NOT_REPORTED` is the correct value. The register entry that discharges the requirement is owed
and not yet written: what is missing, why, what was attempted, what would close it.
