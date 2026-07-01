---
marp: true
size: 16:9
paginate: true
footer: 'OligoTox-Kidney  ·  NCATS OligoTox Open Data Challenge — Phase 2'
title: "OligoTox-Kidney — A Curated Nephrotoxicity Dataset for Oligonucleotide Therapeutics"
description: "Findings, methodology, and sources — for scientific review"
---

<style>
:root{
  --ink:#14202B; --primary:#0E4D64; --primary2:#08323F; --teal:#17A2B8;
  --muted:#5A6B78; --bg:#FFFFFF; --panel:#F5F8FA; --line:#E1E8ED;
  --g0:#2E7D32; --g1:#F2B705; --g2:#E8730C; --g3:#C0392B;
}
section{
  font-family:"Liberation Sans","DejaVu Sans",Arial,sans-serif;
  font-size:23px; color:var(--ink); background:var(--bg);
  padding:50px 72px; line-height:1.42;
  display:flex; flex-direction:column; justify-content:flex-start;
}
section h1{ font-size:40px; color:var(--primary); margin:0 0 10px; }
section h2{ font-size:31px; color:var(--primary); margin:0 0 18px; padding-left:16px; border-left:8px solid var(--teal); }
section h3{ color:var(--primary); margin:.2em 0; }
strong{ color:var(--primary); }
a{ color:var(--teal); text-decoration:none; }
section img{ display:block; margin:6px auto; }
ul{ margin:.2em 0; } li{ margin:.28em 0; }
.kicker{ text-transform:uppercase; letter-spacing:2.5px; font-size:14px; font-weight:800; color:var(--teal); margin-bottom:6px; }
section::after{ color:#9AB0BC; font-size:13px; }
footer{ color:#9AB0BC; font-size:13px; }

/* title */
section.title{ background:var(--primary2); color:#EAF3F6; justify-content:center; }
section.title h1{ color:#fff; font-size:50px; border:none; padding:0; }
section.title .kicker{ color:#7FD3E0; }
section.title .sub{ font-size:25px; color:#BFE0E8; margin-top:6px; }
section.title .meta{ margin-top:30px; font-size:18px; color:#8FB6C4; }
section.title .rule{ width:90px; height:6px; background:var(--teal); border-radius:3px; margin:22px 0; }

/* section divider */
section.section{ background:var(--primary); color:#fff; justify-content:center; }
section.section h2{ color:#fff; font-size:44px; border-left:10px solid var(--teal); }
section.section .kicker{ color:#7FD3E0; }
section.section p{ color:#CFE6EC; font-size:23px; }

/* lead / big statement */
section.lead{ justify-content:center; }
section.lead .big{ font-size:38px; line-height:1.32; font-weight:600; color:var(--ink); }
section.lead .big b{ color:var(--primary); }

/* stat tiles */
.tiles{ display:flex; gap:22px; margin-top:28px; }
.tile{ flex:1; background:var(--panel); border:1px solid var(--line); border-top:6px solid var(--teal); border-radius:12px; padding:24px 16px; text-align:center; }
.tile .n{ font-size:58px; font-weight:800; color:var(--primary); line-height:1; }
.tile .l{ font-size:17px; color:var(--muted); margin-top:10px; }

/* bar charts */
.chart{ margin-top:14px; }
.chart .row{ display:flex; align-items:center; gap:16px; margin:9px 0; }
.chart .lab{ width:250px; text-align:right; font-size:20px; color:var(--ink); }
.chart .track{ flex:1; height:30px; background:#EDF1F4; border-radius:6px; }
.chart .fill{ display:block; height:30px; border-radius:6px; background:var(--teal); }
.chart .val{ width:44px; font-weight:800; color:var(--primary); font-size:19px; }
.c0{ background:var(--g0)!important; } .c1{ background:var(--g1)!important; }
.c2{ background:var(--g2)!important; } .c3{ background:var(--g3)!important; }
.dim .fill{ background:#9FB4BE; }

/* callouts */
.note,.warn,.ok{ padding:15px 22px; border-radius:8px; font-size:21px; }
.note{ background:#EAF3F6; border-left:7px solid var(--teal); }
.warn{ background:#FBF3E7; border-left:7px solid var(--g2); }
.ok{ background:#EAF6EC; border-left:7px solid var(--g0); }

/* columns */
.cols{ display:flex; gap:34px; align-items:flex-start; }
.col{ flex:1; }

/* pills */
.pills{ display:flex; flex-wrap:wrap; gap:9px; margin-top:8px; }
.pill{ background:var(--panel); border:1px solid #D8E2E8; border-radius:22px; padding:6px 14px; font-size:15.5px; }
.pill b{ color:var(--primary); }

/* numbered steps */
.step{ display:flex; gap:16px; margin:13px 0; align-items:flex-start; }
.step .k{ background:var(--primary); color:#fff; width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:19px; flex:none; }
.step .t{ font-size:20px; }
.small{ font-size:17px; color:var(--muted); }
.mono{ font-family:"DejaVu Sans Mono",monospace; font-size:16px; }
.crit{ background:var(--panel); border:1px solid var(--line); border-left:6px solid var(--teal); border-radius:10px; padding:14px 18px; }
.crit .h{ font-weight:800; color:var(--primary); font-size:19px; margin-bottom:5px; }
.crit .d{ font-size:16.5px; color:var(--ink); line-height:1.38; }
</style>

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _footer: '' -->

<div class="kicker">NCATS OligoTox Open Data Challenge · Phase 2</div>

# OligoTox-Kidney

<div class="sub">A curated, per-measurement <b style="color:#fff">kidney-toxicity</b> dataset for oligonucleotide therapeutics</div>

<div class="rule"></div>

<div class="meta">
65 oligos · 111 measurements · 35 target genes · 100% kidney-specific<br>
Phase 2 · Data Generation · prepared for biochemistry-expert review · June 2026
</div>

<!--
SPEAKER NOTES — plain English

One-line pitch: we built a clean, well-documented SPREADSHEET of evidence on how
oligonucleotide drugs can harm the kidney — for a public NIH/NCATS data challenge.

Terms:
• "Oligonucleotide" (oligo) = a drug made of a short string of genetic letters
  (DNA/RNA), ~12–25 long, designed to switch a specific gene on/off. ~19 approved.
• "Nephrotoxicity" = kidney toxicity (nephro = kidney).
• "Per-measurement" = each row is one experimental result, the finest detail.
• "NCATS Phase 2" = the data-generation phase of the challenge; it scores DATASETS.
This deck is for a biochemistry expert to review the science and sign off the grades.
-->

---

<!-- _class: lead -->
<!-- _footer: '' -->

<div class="kicker">The idea in one sentence</div>

<div class="big">
Oligonucleotide drugs can injure the kidney in a way the <b>standard safety test misses</b> — so we built a dataset that captures the <b>right</b> signal, one experiment per row, every value traceable to its source.
</div>

<!--
SPEAKER NOTES — plain English

This frames the whole project. The "standard safety test" is the cheap
"are the cells alive?" test. These drugs often DON'T kill cells, so that test
gives a false all-clear. Our dataset is designed to record the subtler "the cell
is alive but not working" damage instead. "Traceable to source" = every number
points back to the exact paper/patent table it came from.
-->

---

## Why this matters

<div class="cols">
<div class="col">

**Oligonucleotides are a booming drug class** — ~19 already approved, dozens in trials, treating diseases nothing else could.

**But the kidney is a common casualty.** The kidney filters and concentrates these drugs, so it is exposed to high levels — and several oligos have caused proteinuria, kidney injury, even kidney failure.

**The catch:** the damage is often *invisible* to routine cell-survival screening (next slides).

</div>
<div class="col">

<div class="note">
<b>The gap Phase 2 targets</b><br>
Most public oligo-tox data is <b>hepatic</b>; kidney-specific data is thin. No open dataset pairs each oligo's <b>design</b> (sequence + chemistry) with a <b>graded kidney outcome</b> — exactly what an <b>in-silico model</b> needs to predict risk early. That is what we assembled.
</div>

</div>
</div>

<!--
SPEAKER NOTES — plain English

Why kidney, why now. Oligo drugs are a fast-growing, important class. The kidney
is especially exposed because it filters the blood and concentrates whatever
passes through, so these drugs pile up there. Several have caused real kidney
problems. "Proteinuria" = protein leaking into urine, a classic kidney-trouble
sign. Most existing open oligo-tox data is about the LIVER; kidney is under-served
— so an open kidney set fills a real public gap (Phase 2's "potential impact").
The missing piece is a tidy table linking each drug's design to a kidney-toxicity
score, ready for an in-silico model — that is our contribution.
-->

---

<!-- _class: section -->
<!-- _footer: '' -->
<!-- _paginate: false -->

<div class="kicker">Part 1</div>

## The science: a quiet kind of kidney injury

<p>Why a cell-survival test gives these drugs a false "all-clear"</p>

---

## How these drugs injure the kidney

![w:1040](assets/mechanism.svg)

<div class="small" style="margin-top:6px">Phosphorothioate ASOs are filtered, then vacuumed into proximal-tubule cells by the megalin/cubilin receptors and stored in lysosomes. Reabsorption of small proteins fails → they leak into urine (proteinuria) — yet the cell stays alive.</div>

<!--
SPEAKER NOTES — plain English (the key science slide)

30-second kidney primer: the kidney filters blood; tiny tubes called TUBULES then
reabsorb the good stuff (small proteins, sugars) back into the blood. The
PROXIMAL TUBULE is the main reabsorbing stretch; its lining cells do this work.

The pathway, left to right in the diagram:
• "PS-ASO" = the most common oligo type; "phosphorothioate (PS)" = a sulfur tweak
  to the drug's backbone that makes it stable and sticky — and easily taken into
  cells.
• "Glomerulus" = the kidney's filter; the drug passes into the filtered fluid.
• "Megalin / cubilin" = receptors (molecular catcher's mitts) on the tubule cells
  whose normal job is to grab small proteins back — they also grab these drugs.
• "Endocytosis" = the cell swallowing them inside; "lysosome" = the cell's
  recycling bin, where the drug piles up.
• Result: the busy, clogged cell stops reabsorbing small proteins, so those
  proteins LEAK into urine = "low-MW proteinuria." But the cell does NOT die.
This is "functional" (not working right) vs "cytotoxic" (killed). It's usually
reversible. We score this mild functional injury as GRADE 1.
-->

---

## The trap: one drug, two tests, opposite answers

![w:980](assets/trap.svg)

<div class="warn" style="margin-top:10px">
A viability/MTT screen asks only <b>"are the cells alive?"</b> — and these drugs don't kill cells. So routine screening calls them <b>clean</b>. Our schema is built to capture the <b>functional</b> signal that test misses.
</div>

<!--
SPEAKER NOTES — plain English

"MTT / viability test" = the standard cheap lab test that just checks if cells are
still alive. Because these drugs leave cells alive, that test says "safe" — a
false all-clear. The functional test (does the cell still reabsorb protein?)
reveals the real problem. The whole dataset exists to record that second kind of
result, not just the misleading first kind.
-->

---

## So we record the *right* readouts

We deliberately weight the data toward **function and injury markers**, not cell survival:

<div class="chart">
<div class="row"><span class="lab">functional</span><span class="track"><span class="fill" style="width:100%"></span></span><span class="val">35</span></div>
<div class="row"><span class="lab">clinical renal outcome</span><span class="track"><span class="fill" style="width:77%"></span></span><span class="val">27</span></div>
<div class="row"><span class="lab">histopathology</span><span class="track"><span class="fill" style="width:69%"></span></span><span class="val">24</span></div>
<div class="row"><span class="lab">injury biomarker</span><span class="track"><span class="fill" style="width:46%"></span></span><span class="val">16</span></div>
<div class="row dim"><span class="lab">viability (kept only to contrast)</span><span class="track"><span class="fill" style="width:20%"></span></span><span class="val">7</span></div>
<div class="row dim"><span class="lab">accumulation</span><span class="track"><span class="fill" style="width:6%"></span></span><span class="val">2</span></div>
</div>

<div class="small" style="margin-top:8px">“Readout” = one measured thing. Biomarkers = chemicals (KIM-1, NGAL, clusterin, cystatin C) that rise when the kidney is stressed. Functional + biomarker rows (51) dwarf viability rows (7) — by design.</div>

<!--
SPEAKER NOTES — plain English

"Readout category" = the KIND of measurement in a row. The bars show how our 111
rows split. We intentionally collected mostly FUNCTIONAL and INJURY-BIOMARKER
results (the meaningful ones) and only a few VIABILITY results (kept just to
contrast against them). Biomarkers named: KIM-1, NGAL, clusterin, cystatin C —
chemicals measurable in urine/blood that signal kidney stress early.
"Histopathology" = what the tissue looks like under a microscope.
-->

---

<!-- _class: section -->
<!-- _footer: '' -->
<!-- _paginate: false -->

<div class="kicker">Part 2</div>

## What we built

<p>The dataset, its structure, and how toxicity is scored</p>

---

## The dataset at a glance

<div class="tiles">
<div class="tile"><div class="n">65</div><div class="l">unique oligos<br>(7 drug families)</div></div>
<div class="tile"><div class="n">111</div><div class="l">graded measurements<br>(target was ≥100)</div></div>
<div class="tile"><div class="n">100%</div><div class="l">kidney-specific<br>(no padding)</div></div>
<div class="tile"><div class="n">16</div><div class="l">distinct sources<br>fully cited</div></div>
</div>

<div class="cols" style="margin-top:26px">
<div class="col note">Spans every oligo modality, all three study types (dish / animal / human), and the full severity range from safe to severe — including deliberate negative controls.</div>
<div class="col ok"><b>35</b> target genes · <b>33/65</b> sequences filled (rest honestly marked “TBD”, never guessed) · every row carries its source.</div>
</div>

<!--
SPEAKER NOTES — plain English

The scoreboard. 65 distinct drugs; 111 measured results (a drug can appear in
several rows). Every row is kidney-specific — we did not pad with other-organ
data. 16 separate sources, all cited. "Modality" = drug family. "Negative
controls" = known-safe examples, needed so a model can tell safe from harmful.
"TBD" = our literal label for missing data we refused to guess.
-->

---

## How the data is organised — two linked tables

![w:1020](assets/datamodel.svg)

<div class="small" style="margin-top:6px">One table describes each <b>drug</b> (the suspected causes); the other lists each <b>result</b> (the effects). They share an ID (<span class="mono">oligo_id</span>) so any result links back to its drug — like two tabs in a spreadsheet joined by a key.</div>

<!--
SPEAKER NOTES — plain English

Two tables avoid repetition. Left = oligos.csv, one row per DRUG with its design
features (the suspected CAUSES of toxicity). Right = measurements.csv, one row per
RESULT with the graded outcome (the EFFECTS). "Primary key (PK)" = a table's
unique ID column. "Foreign key (FK)" = a column pointing to another table's key;
here each result stores the oligo_id of its drug, so the two tables join.
Predictor examples: sequence, chemistry, gapmer design. Outcome example:
nephrotox_grade plus a full source trail.
-->

---

## The scoring system: a 0–3 severity grade

![w:1000](assets/grade-ladder.svg)

<div class="small" style="margin-top:6px">Each result gets one ordinal grade by a written rubric (in <span class="mono">schema.md</span>). <b>All grades are currently flagged “provisional”</b> — confirming them is the sign-off we’re asking a biochemistry expert for.</div>

<!--
SPEAKER NOTES — plain English

Our single "answer" column: a 0-to-3 severity score.
0 = no kidney signal (a genuinely safe example).
1 = mild/functional/reversible — the sneaky protein-leak, cells don't die.
2 = moderate — an injury biomarker rises and/or tissue looks abnormal.
3 = severe — actual acute kidney injury, glomerulonephritis (inflammation of the
    filter units), or kidney failure.
"Ordinal" = ranked (0<1<2<3) but gaps aren't necessarily equal. "Rubric" = the
written rulebook for assigning grades. "Anchor" = a famous example that pins each
level (inotersen for severe, etc.). Every grade is PROVISIONAL until a biochemistry
expert confirms it.
-->

---

## Grades span the full range — including safe controls

<div class="chart">
<div class="row"><span class="lab">0 — no signal (controls)</span><span class="track"><span class="fill c0" style="width:69%"></span></span><span class="val">27</span></div>
<div class="row"><span class="lab">1 — mild / functional</span><span class="track"><span class="fill c1" style="width:77%"></span></span><span class="val">30</span></div>
<div class="row"><span class="lab">2 — moderate injury</span><span class="track"><span class="fill c2" style="width:100%"></span></span><span class="val">39</span></div>
<div class="row"><span class="lab">3 — severe</span><span class="track"><span class="fill c3" style="width:38%"></span></span><span class="val">15</span></div>
</div>

<div class="note" style="margin-top:18px">A healthy spread across all four levels — a usable dataset needs examples of <b>every</b> severity, not just the dramatic ones. The 27 grade-0 rows are real negative controls (GalNAc-siRNA, intrathecal ASO, aptamer).</div>

<!--
SPEAKER NOTES — plain English

How the 111 results split by severity: 27 safe, 30 mild, 39 moderate, 15 severe.
A good dataset needs all levels represented. The grade-0 rows are deliberate SAFE
examples — drug types that spare the kidney: "GalNAc-siRNA" (liver-targeted, so
little reaches the kidney), "intrathecal" ASOs (injected into spinal fluid), and
aptamers. Bars are coloured green→yellow→orange→red to match the grade ladder.
-->

---

## Coverage: every oligonucleotide family

<div class="chart">
<div class="row"><span class="lab">ASO gapmer</span><span class="track"><span class="fill" style="width:100%"></span></span><span class="val">40</span></div>
<div class="row"><span class="lab">GalNAc-siRNA</span><span class="track"><span class="fill" style="width:30%"></span></span><span class="val">12</span></div>
<div class="row"><span class="lab">splice-switching ASO</span><span class="track"><span class="fill" style="width:10%"></span></span><span class="val">4</span></div>
<div class="row"><span class="lab">PMO</span><span class="track"><span class="fill" style="width:10%"></span></span><span class="val">4</span></div>
<div class="row"><span class="lab">siRNA</span><span class="track"><span class="fill" style="width:5%"></span></span><span class="val">2</span></div>
<div class="row"><span class="lab">1st-gen PS-DNA</span><span class="track"><span class="fill" style="width:5%"></span></span><span class="val">2</span></div>
<div class="row"><span class="lab">aptamer</span><span class="track"><span class="fill" style="width:3%"></span></span><span class="val">1</span></div>
</div>

<div class="small" style="margin-top:8px"><b>Gapmer</b> = central DNA “gap” + chemically-modified wings (cuts target RNA). <b>siRNA</b> = double-stranded silencer; <b>GalNAc</b> = sugar tag aiming it at the liver. <b>PMO</b> = neutral-backbone splice fixer (the muscular-dystrophy drugs). <b>Aptamer</b> = an oligo folded to grab a protein, like an antibody.</div>

<!--
SPEAKER NOTES — plain English

Our drugs cover all the oligo families. Gapmers (40) dominate because they're the
most common and most kidney-relevant ASO design. Quick glossary:
• ASO gapmer — antisense strand with a DNA gap flanked by modified wings; the gap
  lets the enzyme RNase H chop the target RNA.
• GalNAc-siRNA — double-stranded silencer carrying a GalNAc sugar that homes it to
  the liver (so the kidney is largely spared).
• splice-switching ASO / PMO — change how a gene is assembled rather than
  destroying it; PMOs are the Duchenne muscular-dystrophy drugs.
• 1st-gen PS-DNA — older phosphorothioate DNA oligos.
• aptamer — an oligo folded into a 3-D shape that binds a target protein.
-->

---

## Coverage: dish → animal → human (the translation axis)

<div class="cols">
<div class="col">
<div class="kicker">Study type</div>
<div class="chart">
<div class="row"><span class="lab">animal</span><span class="track"><span class="fill" style="width:100%"></span></span><span class="val">53</span></div>
<div class="row"><span class="lab">clinical (human)</span><span class="track"><span class="fill" style="width:74%"></span></span><span class="val">39</span></div>
<div class="row"><span class="lab">in-vitro (dish)</span><span class="track"><span class="fill" style="width:36%"></span></span><span class="val">19</span></div>
</div>
</div>
<div class="col">
<div class="kicker">Species</div>
<div class="chart">
<div class="row"><span class="lab">human</span><span class="track"><span class="fill" style="width:100%"></span></span><span class="val">58</span></div>
<div class="row"><span class="lab">mouse</span><span class="track"><span class="fill" style="width:52%"></span></span><span class="val">30</span></div>
<div class="row"><span class="lab">multi-species</span><span class="track"><span class="fill" style="width:14%"></span></span><span class="val">8</span></div>
<div class="row"><span class="lab">rat</span><span class="track"><span class="fill" style="width:14%"></span></span><span class="val">8</span></div>
<div class="row"><span class="lab">monkey</span><span class="track"><span class="fill" style="width:12%"></span></span><span class="val">7</span></div>
</div>
</div>
</div>

<div class="small" style="margin-top:10px">Having dish, animal, and human rows side by side — measured the same way — lets the <b>animal-to-human translation gap</b> be studied directly (Finding 3).</div>

<!--
SPEAKER NOTES — plain English

Where the results come from. "In-vitro" = in a dish; "in-vivo" = in a living
animal; "clinical" = in human patients. We have all three, across several species.
Why it matters: because human and animal results sit in the same table measured
the same way, you can directly compare how well an animal result predicts the
human one — the "translation gap" we return to in Finding 3.
-->

---

<!-- _class: section -->
<!-- _footer: '' -->
<!-- _paginate: false -->

<div class="kicker">Part 3</div>

## How we built it

<p>Methodology, the integrity rule, and the sources researched</p>

---

## Three ways we gathered data — each tagged per row

![w:1000](assets/extraction.svg)

<div class="small" style="margin-top:6px">Every row records <i>how</i> it was obtained, so its reliability is visible. Web-search rows are flagged for re-checking because this secure environment blocks downloading full papers.</div>

<!--
SPEAKER NOTES — plain English

Three data-gathering methods, strongest first:
1. PRIMARY full-text — we read the original papers/patents (PDFs) with a tool
   called PyMuPDF and typed values in by hand. Gold standard.
2. REVIEW / secondary — summary papers that aggregate many studies, cross-checked
   against primary data.
3. WEBSEARCH-derived ("WS") — the weakest tier. Our secure computer BLOCKS direct
   downloading of full papers, so for some drugs we took figures from search-engine
   summaries of their official label/trial, and FLAGGED those rows to be verified
   against the original before any public release. 36 of 111 rows are this type.
"source_id" = a code in each row naming its source, so everything is traceable.
-->

---

## The rule that makes the dataset trustworthy

<div class="warn" style="font-size:24px">
<b>⚠️ Strict no-fabrication policy</b><br><br>
Drug <b>sequences</b> and toxicity <b>values</b> are never invented or recalled from memory. A value goes in <b>only</b> if an explicit, citable, redistribution-permitted source states it. Drugs with no published kidney data were <b>omitted, not padded</b>.
</div>

<div class="cols" style="margin-top:22px">
<div class="col"><div class="kicker">Why sequences are 33/65, not 65/65</div>The 32 blanks are <b>real gaps</b>, honestly marked “TBD”. We could have made the table look complete by guessing — but a falsely-complete table can’t be trusted at all.</div>
<div class="col"><div class="kicker">Why this matters to a reviewer</div>If the easy fields were fudged, none of the hard toxicity values could be believed. Honest blanks are the <b>credibility</b> of the whole dataset.</div>
</div>

<!--
SPEAKER NOTES — plain English

Our integrity rule, stated loudly because it's WHY the data can be trusted.
We never make up two things: the drug's genetic SEQUENCE and any toxicity NUMBER.
Even though an AI assistant helped build this, it was not allowed to fill those
from memory — only from a real, citable, copy-permitted source. If a drug had no
published kidney data, we left it out rather than invent rows to hit the target.
That's why only 33 of 65 drugs have sequences — the rest are honest blanks, which
is more trustworthy than a fake-complete table.
-->

---

## Sources researched

<div class="cols">
<div class="col">
<div class="kicker">Strict-kidney primary (read in full)</div>

- **Janssen 2019** · drisapersen, human kidney-cell injury *(N2 · 10 rows)*
- **US 11,105,794 B2** · patent tox panel *(N3 · 21 rows)*
- **Moisan 2017** · human tubule-cell panel *(M1 · 11 rows)*
- **Sandelius 2020** · urine injury-biomarkers *(K1 · 9 rows)*
- **van Poelgeest 2013** · SPC5001 first-in-human AKI *(A3)*
- **Arch Toxicol 2021** · SPC5001 kidney-on-chip *(A4 · 5 rows)*

</div>
<div class="col">
<div class="kicker">Anchors · review · patents</div>

- **Wu 2022** · marketed-ASO nephrotoxicity review *(REV)*
- **inotersen** · NEJM NEURO-TTR + FDA label — severe anchor *(A1)*
- **mipomersen, volanesorsen** · gapmer renal signals *(A9, A8)*
- **inclisiran, givosiran, nusinersen** · safe controls
- **US 11,479,818 B2** · 2nd patent, queued *(N4)*

</div>
</div>

<div class="small" style="margin-top:10px"><b>+ 36 “WS” rows</b> from FDA/EMA labels & pivotal trials: patisiran, vutrisiran, lumasiran, nedosiran, eplontersen, tofersen, bepirovirsen, olpasiran, the DMD PMOs, pegaptanib, fitusiran, zilebesiran — plus Crooke 2018 (human) & Yu 2012 (monkey) for the translation gap.</div>

<!--
SPEAKER NOTES — plain English

Our bibliography, split into the best kidney-specific papers (read in full) and
the real-world anchors/reviews/patents. The number in italics is each source's
code and how many rows it gave. Highlights:
• N2 Janssen — showed the sneaky dish phenotype + gave 3 real sequences.
• N3 patent — the jackpot: a public-domain table of many oligos with sequence AND
  toxicity together (21 rows, our biggest source).
• M1 Moisan / K1 Sandelius — human kidney-cell panels and urine biomarkers.
• A3/A4 SPC5001 — a drug that caused acute kidney injury first-in-human, also
  reproduced on a "kidney-on-chip" (a chip with living kidney cells).
• A1 inotersen — our severe anchor (caused glomerulonephritis in patients).
• Safe controls: inclisiran, givosiran, nusinersen.
The 36 "WS" rows are mostly approved drugs whose data came from label/trial
summaries (flagged for re-checking). Crooke 2018 (human) and Yu 2012 (monkey) let
us compare species.
-->

---

<!-- _class: section -->
<!-- _footer: '' -->
<!-- _paginate: false -->

<div class="kicker">Part 4</div>

## What the data shows

<p>Three findings worth a biochemistry expert’s attention</p>

---

## Finding 1 — the “invisible” injury, captured

![w:980](assets/paired.svg)

<div class="note" style="margin-top:8px">For the <b>same</b> drug we store <b>paired rows</b>: a mild grade on the functional test, a clean grade on viability/tissue. Side by side they encode “dysfunction without death” — a distinction viability-only datasets simply cannot teach a model.</div>

<!--
SPEAKER NOTES — plain English

Finding 1: we successfully captured the sneaky damage in machine-readable form.
For one drug (drisapersen) we have three rows: protein leak in human kidney cells
→ grade 1; cells alive → grade 0; monkey tissue normal → grade 0. Together they
say "the cell malfunctions without dying." A model trained on this can learn the
difference between reversible functional proteinuria and real structural injury —
something an alive/dead-only dataset can never convey.
-->

---

## Finding 2 — a patent unlocked sequence + toxicity together

![w:980](assets/patent.svg)

<div class="note" style="margin-top:8px">Most sources give a sequence <i>or</i> a toxicity value. This public-domain patent table gave <b>both in the same row</b> for many oligos — the most directly model-ready slice of the dataset, and it tripled our sequence coverage.</div>

<!--
SPEAKER NOTES — plain English

Finding 2: one patent (US 11,105,794) was a goldmine. Its Table 1 lists many
oligos each with BOTH the genetic sequence AND a kidney-toxicity rating in animals
— rare, because usually those live in different places. The patent rated toxicity
in words (innocuous/low/medium/high); we translated those into our 0–3 numbers.
It added 21 rows and tripled our real sequences from 13 to 33. Because cause
(sequence) and effect (grade) sit together, it's the most "model-ready" data.
"Public domain" = freely reproducible (US patents are).
-->

---

## Finding 3 — animal tests over-predict human risk

![w:980](assets/translation.svg)

<div class="note" style="margin-top:8px">A known, consistent bias for this drug class: animal kidneys look worse than patients turn out to be. We captured human and animal rows side by side so the gap can be <b>modelled, not ignored</b> — don't treat animal histopathology as human ground truth.</div>

<!--
SPEAKER NOTES — plain English

Finding 3: for these drugs, animal studies tend to show MORE kidney damage than
humans actually experience. This over-prediction is a known, consistent pattern —
so a model could learn to correct for it. We deliberately placed human data (e.g.
Crooke 2018) and animal data (e.g. Yu 2012 monkey) in the same table, measured the
same way, so the gap is visible and analysable rather than hidden. "Don't treat
animal histopathology as ground truth" = don't assume the animal microscope result
equals the human truth.
-->

---

<!-- _class: section -->
<!-- _footer: '' -->
<!-- _paginate: false -->

<div class="kicker">Part 5</div>

## Why it fits Phase 2 — and what's next

<p>Judging criteria, trust, limitations, and the ask</p>

---

## Built for the four Phase-2 judging criteria

<div class="cols">
<div class="crit col"><div class="h">1 · Ability to solve</div><div class="d">A <b>model-ready</b> design — granular <b>sequence + chemistry</b> predictors against <b>graded</b>, per-condition kidney outcomes; the patent panel even puts sequence <b>and</b> toxicity in one row.</div></div>
<div class="crit col"><div class="h">2 · Potential impact</div><div class="d">Fills a real public-domain gap: most open oligo-tox data is <b>hepatic</b> — kidney is thin. First open set linking oligo <b>design</b> to <b>graded nephrotoxicity</b>, incl. the functional phenotype.</div></div>
</div>
<div class="cols" style="margin-top:14px">
<div class="crit col"><div class="h">3 · Feasibility &amp; rigor</div><div class="d">Strict <b>no-fabrication</b>, per-row provenance, controlled vocabularies and automated <b>QC</b> (0 orphans) — a set researchers can trust and reuse on release.</div></div>
<div class="crit col"><div class="h">4 · Transparency &amp; reproducibility</div><div class="d">Open license (CC-BY) intended; every value <b>traceable</b> to source; all stats regenerate from <span class="mono">data/</span> — <b>FAIR</b>, aligned to NIH data-sharing.</div></div>
</div>

<div class="small" style="margin-top:14px">NCATS's four Phase-2 confidence factors — the dataset was <b>designed against them, not retro-fitted</b>. Submission window 1 May – 31 Dec 2026.</div>

<!--
SPEAKER NOTES — plain English

NCATS scores Phase 2 on four "confidence factors"; this slide maps our work to each:
1. Ability to solve — is the data useful for building computer models that PREDICT
   oligo toxicity? Our design pairs each drug's sequence/chemistry with a graded
   kidney outcome — exactly what such a model needs.
2. Potential impact — does it fill a public gap? Most existing open oligo-tox data
   is about the LIVER; kidney data is scarce. Ours is the first open set linking
   oligo design to graded KIDNEY toxicity, including the easily-missed functional
   injury.
3. Feasibility & rigor — would researchers trust it? Yes: nothing fabricated, every
   row sourced, controlled vocabulary, automated quality checks all passing.
4. Transparency & reproducibility — is it open and re-checkable? Intended CC-BY open
   license; every value traces to its source; all the numbers regenerate from the
   data files. "FAIR" = Findable, Accessible, Interoperable, Reusable — the standard
   for good scientific data that NIH's data-sharing policy expects.
We designed for these four from the start, rather than fitting them afterward.
-->

---

## Every row is defensible

<div class="cols">
<div class="col">
<div class="kicker">Provenance — the paper trail</div>

Each measurement carries its **source**, the **exact** table/figure/claim, and its **redistribution right**, so any value can be re-checked at its origin.

<div class="pills">
<span class="pill"><b>47</b> public-domain rows</span>
<span class="pill"><b>64</b> summary-stat rows</span>
<span class="pill"><b>16</b> sources</span>
</div>

</div>
<div class="col">
<div class="kicker">Quality control — all passing</div>

<div class="ok">
✓ every category value from an allowed list<br>
✓ column counts intact (17 / 23)<br>
✓ every result links to a real drug — <b>0 orphans</b><br>
✓ no duplicate IDs · grades all 0–3<br>
✓ no-guessing sequence rule held
</div>

</div>
</div>

<!--
SPEAKER NOTES — plain English

Two trust pillars. PROVENANCE = the documented origin of each value: which source,
which exact table/figure, and whether we're legally allowed to republish it
("public domain" = yes, e.g. patents and government labels; "summary stat" = we
only reproduce summary figures from copyrighted journals). QUALITY CONTROL =
automated checks that run after each data addition: valid categories, right column
counts, every result points to a real drug (no "orphans"), no duplicate IDs,
grades within 0–3, and the no-guessing rule. All currently pass.
-->

---

## Honest limitations

<div class="cols">
<div class="col">

- **Grades are provisional** — assigned by rubric, awaiting expert sign-off.
- **Sequences 33/65** — remaining gaps (siRNA guide strands, some PMOs) left blank, never guessed.
- **36 “WS” rows** rest on web summaries — need verification against the primary document.

</div>
<div class="col">

- **In-vitro human-cell rows (19)** are the scientific core but still a minority — growing them is the top priority.
- **Animal over-prediction** is present by design — it must be modelled, not ignored.

</div>
</div>

<div class="small" style="margin-top:16px">Stating the soft spots plainly is part of the deliverable — a reviewer should know exactly where to push.</div>

<!--
SPEAKER NOTES — plain English

We state our weaknesses openly — for a scientist that builds trust. The grades
aren't expert-confirmed yet; 32 sequences are still blank; 36 rows came from web
summaries and need re-checking; the human-cell-in-a-dish rows (the most valuable)
are still a minority we want to grow; and the animal-over-prediction bias must be
accounted for in any model.
-->

---

## What we need from the biochemistry expert

<div class="step"><div class="k">1</div><div class="t"><b>Grade sign-off.</b> Check the rubric→row mapping in <span class="mono">measurements.csv</span> so we can remove the “provisional” flag. Hot spots: the <b>grade 2↔3</b> line (biomarker rise vs. true AKI) and the <b>patent words→grade</b> mapping.</div></div>

<div class="step"><div class="k">2</div><div class="t"><b>Biology sanity check.</b> Is the functional-vs-structural story (megalin/cubilin → protein leak → grade 1) faithful, and are the readout→severity calls physiologically sound?</div></div>

<div class="step"><div class="k">3</div><div class="t"><b>Source confidence.</b> Flag any anchor — especially the 36 “WS” rows — you’d want re-verified against the primary text before release.</div></div>

<div class="small" style="margin-top:14px"><b>On hold until sign-off:</b> the ≤12-page narrative · verifying WS rows · backfilling sequences · mining patent N4 for more rows.</div>

<!--
SPEAKER NOTES — plain English

The concrete ask. (1) The big one: review our 0–3 grades against the rulebook and
confirm/correct them — focus on the 2-vs-3 boundary and whether we converted the
patent's word-ratings correctly; their sign-off lets us finalise the grades. (2)
Sanity-check the core biology story. (3) Point out any source they'd want
re-verified, especially the web-summary rows. Everything else (the written
narrative, WS verification, more sequences, a second patent) is paused until they
weigh in, so we don't polish things that might change.
-->

---

## Where everything lives

<div class="mono" style="background:#F5F8FA;border:1px solid var(--line);border-radius:10px;padding:20px 24px;font-size:17px;line-height:1.7">
README.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;strategy, scope, live record counter<br>
schema.md&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;data dictionary + the grade rubric<br>
METHODOLOGY.md&nbsp;&nbsp;&nbsp;how it was built (sources → grading → QC)<br>
PRESENTATION.md&nbsp;&nbsp;this deck (+ plain-English speaker notes)<br>
data/oligos.csv&nbsp;&nbsp;&nbsp;65 drugs · 17 design columns<br>
data/measurements.csv&nbsp;&nbsp;<b style="color:#0E4D64">111 graded rows ← review here</b><br>
sources/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;the source PDFs + the source registry
</div>

<div class="note" style="margin-top:20px"><b>Thank you — feedback welcome at the row level.</b> Every number in this deck regenerates from <span class="mono">data/</span>; nothing here is hand-maintained prose detached from the tables.</div>

<!--
SPEAKER NOTES — plain English

A map of the project folder so the biochemistry expert knows where to look. The key
file for review is data/measurements.csv (the graded results); the rulebook is
schema.md.
Closing point: every count on these slides comes straight out of the data files,
so the deck can't drift from the underlying data. We'd love comments on specific
rows, not just general impressions.
-->
