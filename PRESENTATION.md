---
marp: true
title: "OligoTox-Kidney — A Curated Nephrotoxicity Dataset for Oligonucleotide Therapeutics"
description: "Findings, methodology, and sources — for scientific review"
paginate: true
---

# OligoTox-Kidney

### A curated, per-measurement **nephrotoxicity** dataset for therapeutic oligonucleotides

Built for the **NIH / NCATS Oligonucleotide Toxicity (OligoTox) Open Data Challenge — Phase 2** (Data Generation Phase; submission window 1 May – 31 Dec 2026)

**For scientific review — German (biochemist)**
Snapshot: 65 oligos · 111 measurements · 35 target genes · all strict-kidney

> This deck is a Markdown/Marp presentation. It can be read as a document on GitHub or exported to slides (`marp PRESENTATION.md --pdf`). Every claim traces to a row in `data/` and a source in `sources/SOURCES.md`.

<!--
SPEAKER NOTES — plain English (read this to understand the slide)

What this project is, in one breath: we are building a clean, well-documented
SPREADSHEET of evidence about how a certain class of modern drugs can harm the
kidney. We are NOT building an AI or a lab experiment — we are collecting and
organising facts that already exist in the scientific literature.

Key terms on this slide:
• "Oligonucleotide" (say: ah-LIG-oh-NEW-clee-oh-tide), or "oligo" for short =
  a drug made from a short string of genetic letters (the same A/C/G/T/U
  letters as DNA and RNA), usually 12–25 letters long. Instead of a normal
  small-molecule pill, the drug IS a tiny piece of designed genetic code that
  switches a specific gene on or off. ~19 are approved; this is one of the
  hottest areas of new medicine.
• "Nephrotoxicity" (NEFF-roh-tox-issity) = kidney toxicity, i.e. damage or
  dysfunction of the kidney caused by a drug. "Nephro" = kidney.
• "NIH / NCATS" = the US National Institutes of Health and one of its centres.
  They are running a public "challenge" (a competition) asking teams to build
  open datasets about oligo toxicity. We are entering the data-generation phase.
• "Per-measurement" = the finest level of detail: each line in our spreadsheet
  is ONE measured result from ONE experiment, not a vague summary of a drug.
• "Strict-kidney" = every single row is about the kidney specifically (we did
  not pad the set with liver or other-organ data).
• "Marp" = the simple tool that turns this text file into slides. Not science —
  just the format.
-->

---

## What we are building (and what we are *not*)

- **A dataset, not a model.** NCATS Phase 2 scores an **openly-releasable, well-documented, reproducible dataset**. We are not training a predictor — we are assembling the labelled substrate one could be trained on.
- **Endpoint: kidney toxicity / nephrotoxicity** — one of the named OligoTox endpoints of interest.
- **Method: in-silico curation** of already-published data — no wet lab. The "methods" are *source identification, extraction, harmonization, grading, provenance, and QC*.
- **Granularity: strict-kidney, per-measurement.** One row = **oligo × cell-model/subject × delivery × concentration/dose × readout.**
- **Coverage goal:** span every therapeutic oligo modality and the full severity range (including negative controls). Target **≥ 100 measurement rows — met (111).**

<!--
SPEAKER NOTES — plain English

This slide draws the boundary around the job so expectations are clear.

• "Dataset, not a model" = we deliver the ORGANISED EVIDENCE (the spreadsheet),
  not an artificial-intelligence program. Someone could later train an AI on our
  spreadsheet, but that is a separate job. The competition rewards the quality of
  the data itself.
• "Openly-releasable / reproducible" = anyone can download it, and anyone can
  re-check every number against its original source. That trustworthiness is
  exactly what is being graded.
• "Labelled substrate" = the raw material (the data) with answers attached
  (each row says how toxic it was). "Substrate" here just means "the stuff you
  build on top of."
• "Endpoint" = the specific type of harm we are tracking. Ours is kidney damage.
  (In tox studies an "endpoint" is the outcome you measure.)
• "In-silico" (in-SILL-ih-koh) = "done on a computer," as opposed to "in-vitro"
  (in a dish) or "in-vivo" (in a living animal/person). We did no lab work; we
  curated existing results on a computer.
• "Curation" = carefully selecting, cleaning, and organising existing data —
  like a museum curator choosing and labelling exhibits.
• "Harmonization" = forcing everyone's differently-worded results into ONE
  consistent format so they can be compared.
• "QC" = quality control: automated checks that catch mistakes.
• "Granularity" = how zoomed-in the data is. Our row = one oligo, tested in one
  model (a dish of cells or an animal or a patient), given one way ("delivery"),
  at one dose, measured by one readout. The "×" just means "combined with."
• "Modality" = the TYPE of oligo drug (there are several families — explained on
  the next slides). "Span every modality" = include all the families.
• "Negative controls" = examples that are known to be SAFE for the kidney. You
  need safe examples as well as harmful ones, otherwise you cannot tell them
  apart. We deliberately included safe ones.
• Bottom line: target was at least 100 rows; we have 111.
-->

---

## Why kidney, and why this is scientifically non-trivial

The central biology that shaped every design decision:

1. **Oligo nephrotoxicity is frequently *functional*, not *cytotoxic*.**
   Phosphorothioate ASOs are filtered and reabsorbed by **proximal tubule epithelial cells via megalin/cubilin-mediated endocytosis**, accumulating in the lysosomal compartment. This produces **reversible low-molecular-weight proteinuria** (impaired reabsorption of albumin, α1-microglobulin, RAP) **with no loss of cell viability.**
   → **A viability/MTT readout will score these compounds as clean.** That is the trap this dataset is designed to avoid.
2. **Toxicity = sequence + chemistry + design *together*** — not chemistry class alone. Two MOE gapmers of identical chemistry can differ by orders of magnitude in renal signal based on sequence. So we record **granular per-oligo design predictors.**
3. **Marketed-drug data alone is too small** (~19 approved oligos, a minority with renal signal). Volume and mechanistic resolution come from **in-vitro human proximal-tubule panels** and **patent toxicity panels.**

<!--
SPEAKER NOTES — plain English (this is the most important science slide; take it slow)

THE BIG IDEA: these drugs can hurt the kidney in a SNEAKY way that the usual
safety test misses. Understanding that one fact justifies the whole project.

First, a 30-second kidney primer:
• The kidney filters your blood. The filtered fluid passes through tiny tubes
  called TUBULES, which reabsorb the good things (small proteins, sugars) back
  into the blood and let waste continue out as urine.
• The "PROXIMAL TUBULE" is the first and main reabsorbing stretch of that tube.
  Its lining cells are the "proximal tubule epithelial cells." ("Epithelial" =
  the cells that line a surface.)

Now the mechanism, term by term:
• "Phosphorothioate (PS) ASO" = the most common oligo design. "ASO" = antisense
  oligonucleotide, a single strand that sticks to a target gene's RNA to silence
  it. "Phosphorothioate" is a chemical tweak to the drug's backbone (one oxygen
  swapped for sulfur) that stops the body destroying it too fast — but it also
  makes the drug stick to proteins and get taken into cells. Useful, but it is
  part of why the kidney soaks them up.
• "Megalin / cubilin" = two receptors (molecular catcher's mitts) on the surface
  of those proximal-tubule cells whose normal job is to grab small proteins out
  of the filtered fluid and pull them back in. Unfortunately they ALSO grab these
  PS-ASO drugs.
• "Endocytosis" = the process of a cell swallowing something by wrapping it in a
  bubble and pulling it inside.
• "Lysosomal compartment / lysosome" = the cell's stomach / recycling bin. The
  drug piles up there.
• So: the drug gets filtered, the tubule cells vacuum it up via megalin/cubilin,
  and it accumulates inside them.

What goes wrong — and why it's sneaky:
• "Functional, not cytotoxic." CYTOTOXIC means "kills cells" (cyto = cell).
  FUNCTIONAL means "the cells are still alive but not doing their job properly."
  These drugs mostly cause the second kind: the tubule cells survive but get so
  busy hoarding the drug that they stop reabsorbing small proteins well.
• "Low-molecular-weight proteinuria" = small proteins leaking into the urine.
  PROTEINURIA = protein in urine (a classic sign of kidney trouble).
  "Low-molecular-weight" = the SMALL proteins specifically — their appearance
  points to a TUBULE reabsorption problem (as opposed to a damaged filter).
  Examples named: albumin, α1-microglobulin ("A1M"), and RAP — these are normal
  small blood/filtrate proteins that should be reabsorbed; finding them in urine
  means reabsorption failed.
• "Reversible" = it goes away when you stop the drug — so it is real toxicity but
  usually not permanent damage. That nuance matters for grading severity later.
• "No loss of cell viability" = the cells don't die. "Viability" = the fraction
  of cells still alive.

THE TRAP (the punchline):
• "MTT / viability readout" = the standard cheap lab test that just asks "are the
  cells still alive?" Because these drugs DON'T kill cells, that test says
  "harmless" — a FALSE all-clear. Our dataset is built to capture the functional
  signal that the cheap test misses. This is the project's reason to exist.

Points 2 and 3, quickly:
• Point 2: toxicity depends on the exact genetic SEQUENCE plus the CHEMISTRY plus
  the DESIGN, all together — not just the drug family. "MOE gapmer" = a popular
  ASO design (explained on the data-model slide). "Orders of magnitude" = 10×,
  100× differences. Two drugs that look chemically identical can differ hugely in
  kidney risk because of their letter sequence. So we record lots of fine design
  details ("granular predictors") for each drug, hoping the pattern is learnable.
• Point 3: there are only ~19 approved oligo drugs, and few have kidney signals,
  so approved drugs alone can't give us 100+ rows. The bulk of the data comes
  from (a) lab experiments on human kidney cells and (b) toxicity tables inside
  patents. Those are explained later.
-->

---

## The schema captures the *right* phenotype

Because the injury is functional, the readout vocabulary is deliberately weighted toward **function and injury biomarkers**, not viability:

| Readout category | Rows | Examples |
|---|---:|---|
| **functional** | 35 | LMW proteinuria, A1M/albumin reabsorption, eGFR/creatinine shift, RAP |
| **clinical_renal_outcome** | 27 | proteinuria, AKI, glomerulonephritis on label/trial |
| **histopathology** | 24 | tubular degeneration, basophilic granules, glomerular change |
| **injury_biomarker** | 16 | **KIM-1, NGAL, clusterin, cystatin C**, osteopontin |
| **viability** | 7 | included only to *pair against* functional positives |
| **accumulation** | 2 | tubular drug accumulation |

The dataset deliberately encodes **paired functional-positive / structural-negative rows on the same agent** (e.g. drisapersen: grade-1 A1M proteinuria *alongside* grade-0 viability and grade-0 monkey histopathology) — that pairing *is* the functional-not-cytotoxic signal in machine-readable form.

<!--
SPEAKER NOTES — plain English

This slide proves we followed through on the previous slide's insight: we
collected the RIGHT kinds of measurements, not just the easy "are cells alive?"
one.

• "Schema" = the structure/blueprint of our spreadsheet (what columns exist and
  what's allowed in them).
• "Phenotype" = the observable result/outcome — what the toxicity actually looks
  like. "The right phenotype" = we measured the functional damage, not just death.
• "Readout" = a single measured thing in an experiment. "Readout category" = the
  KIND of measurement. The table shows how our 111 rows split across kinds.

The six categories explained:
• FUNCTIONAL (35 rows) = the cells/organ are alive but not working right. Items:
  - "LMW proteinuria" = small proteins leaking into urine (from previous slide).
  - "A1M / albumin reabsorption" = whether those small proteins are being
    reabsorbed properly.
  - "eGFR" = estimated Glomerular Filtration Rate = a score of how well the
    kidney filters blood; lower = worse.
  - "Creatinine" = a waste chemical the kidney clears; if it rises in the blood,
    the kidney is filtering worse. A "shift" = a change from normal.
  - "RAP" = one of those small marker proteins again.
• CLINICAL_RENAL_OUTCOME (27) = what was actually seen in PATIENTS (in trials or
  on the drug's official label). "Renal" = kidney.
  - "AKI" = Acute Kidney Injury = a sudden drop in kidney function.
  - "Glomerulonephritis" = inflammation of the glomeruli, the kidney's tiny
    filter units (more serious — a structural disease, not just dysfunction).
• HISTOPATHOLOGY (24) = what the tissue looks like under a MICROSCOPE.
  ("Histo" = tissue, "pathology" = disease.) 
  - "Tubular degeneration" = the tubule cells looking damaged.
  - "Basophilic granules" = blue-staining specks inside cells under the
    microscope — here, clumps of accumulated drug; a classic ASO footprint.
  - "Glomerular change" = visible change in the filter units.
• INJURY_BIOMARKER (16) = chemicals you can measure in urine or blood that rise
  when the kidney is stressed — an early-warning panel. ("Biomarker" = a
  measurable biological signal.) The named ones:
  - "KIM-1" (Kidney Injury Molecule-1) = goes up with proximal-tubule injury.
  - "NGAL" = goes up early in acute kidney injury.
  - "Clusterin" = tubule-injury marker.
  - "Cystatin C" = a marker of overall filtering function.
  - "Osteopontin" = another kidney-stress marker.
• VIABILITY (7) = the simple "are the cells alive?" test. We kept only a few, on
  purpose, to CONTRAST against the functional findings (see below).
• ACCUMULATION (2) = simply measuring how much drug piled up in the tubule.

THE CLEVER PART ("paired rows"):
• For the SAME drug we sometimes have two rows that, side by side, tell the whole
  story. Example — drisapersen (an experimental muscular-dystrophy oligo):
  - one row: small-protein (A1M) leakage = a real but mild functional problem →
    we graded it 1.
  - another row: cells still alive (viability fine) → graded 0.
  - another row: monkey kidney tissue under microscope looked normal → graded 0.
  Put together, those rows literally spell out "dysfunction without cell death."
• "Grade 0/1/..." = our 0–3 severity score, defined on the next-but-one slide.
• "Machine-readable form" = arranged as tidy numbers/labels a computer can learn
  from, rather than buried in paragraphs of a paper.
-->

---

## Data model — two normalized tables

Joined on `oligo_id`; full dictionary + controlled vocabularies + grading rubric in `schema.md`.

| File | Grain | Key | Cols |
|---|---|---|---:|
| `data/oligos.csv` | one row per unique oligo (identity + **design predictors**) | `oligo_id` (PK) | 17 |
| `data/measurements.csv` | one row per oligo × model × delivery × dose × readout (**graded outcomes**) | `measurement_id` (PK), `oligo_id` (FK) | 23 |

**Predictor columns (oligos):** class, target gene, backbone chemistry, sugar modifications, gapmer design, conjugate (GalNAc/PEG), PS count, length, sequence (5′→3′), development stage.

**Outcome columns (measurements):** study type, species, system/model, tissue, delivery, dose/conc, exposure, readout name/value/unit, effect direction vs control, **`nephrotox_grade`**, `is_kidney_specific`, and full provenance (`source_id`, `source_ref`, `source_table`, `redistribution`).

Missing/unknown is the literal `TBD` — **never guessed, never imputed as zero.**

<!--
SPEAKER NOTES — plain English

This slide shows how the spreadsheet is physically organised: TWO linked tables.

Why two tables? To avoid repeating yourself. One table describes each DRUG once;
the other lists each EXPERIMENTAL RESULT. They are linked by a shared ID.

• "Normalized tables" = a database tidiness principle: store each fact in exactly
  one place. Drug facts live in one file; result facts in the other.
• "CSV" = a plain spreadsheet file (comma-separated values); opens in Excel.
• "Grain" = what one row represents.
• "oligos.csv" = one row per DRUG (65 rows). "measurements.csv" = one row per
  RESULT (111 rows). One drug can have many results, so 65 drugs → 111 rows.
• "Joined on oligo_id" = each result carries the ID of the drug it used, so you
  can match a result back to its drug — like a foreign key in a database.
• "PK (primary key)" = the unique ID column for a table (no duplicates allowed).
• "FK (foreign key)" = a column that points to another table's primary key. In
  measurements, oligo_id is an FK pointing to the oligos table.
• "Cols" = number of columns (17 in the drug table, 23 in the results table).

PREDICTOR columns = the drug's design features (the suspected CAUSES of toxicity).
Plain-English glossary:
• "Class / modality" = which oligo family (gapmer, siRNA, PMO, aptamer…).
• "Target gene" = the gene the drug is designed to silence/affect.
• "Backbone chemistry" = the chemistry of the drug's spine. "Full-PS" =
  every link is the sulfur-modified phosphorothioate type; "PS/PO mix" = some
  sulfur (PS), some normal (PO = phosphodiester) links. PS = sticky/stable but
  more kidney uptake.
• "Sugar modifications" = chemical tweaks to the sugar part of each letter (e.g.
  "2′-MOE" or "LNA") that boost stability and target-binding.
• "Gapmer design" = a specific ASO layout: a central DNA "gap" flanked by two
  chemically-modified "wings." The gap lets an enzyme (RNase H) chop the target
  RNA; the wings protect the drug. Very common design.
• "Conjugate" = an extra molecule bolted on to steer delivery. "GalNAc" (gal-NACK)
  = a sugar tag that homes the drug to LIVER cells; "PEG" = a polymer that makes
  the drug last longer in blood. "none" = no conjugate.
• "PS count" = how many of those sulfur-modified links the drug has.
• "Length" = how many letters long the oligo is.
• "Sequence (5′→3′)" = the actual genetic letters of the drug, written in the
  standard direction (5-prime to 3-prime are just the two ends of the strand).
• "Development stage" = how far the drug got: approved, or still in phase 1/2/3
  trials, or just a research compound.

OUTCOME columns = what happened in each experiment (the EFFECTS). Highlights:
• "Study type" = in-vitro (dish) / animal / clinical (humans).
• "Species" = human, mouse, rat, monkey…
• "System/model" = the exact test system (a named human cell line, an animal
  study, etc.). "Tissue" = kidney part involved.
• "Delivery" = how the drug was given (injection, free uptake into cells, etc.).
• "Dose/conc, exposure" = how much, and for how long.
• "Readout name/value/unit" = what was measured, the number, and its unit.
• "Effect direction vs control" = did it go UP or DOWN compared with an untreated
  comparison sample ("control").
• "nephrotox_grade" = our 0–3 kidney-toxicity severity score (next slide).
• "is_kidney_specific" = TRUE/FALSE flag; here always TRUE.
• "Provenance" columns = the paper trail (which source, which table/figure, and
  whether we're legally allowed to republish it). Detailed two slides on.

• "TBD" = "to be determined" — our literal text for "we don't have this yet." We
  NEVER guess and NEVER silently fill a blank with zero (a zero would be a lie —
  it would say "we measured this and it was none," which isn't true).
-->

---

## The graded label: `nephrotox_grade` (0–3)

An ordinal severity scale assigned from the reported endpoint (rubric in `schema.md`):

| Grade | Meaning | Canonical anchor |
|:---:|---|---|
| **0** | No renal signal (true negative control) | GalNAc-siRNA, intrathecal ASO, aptamer negatives |
| **1** | Mild / **functional** / reversible — **no viability loss** | drisapersen A1M proteinuria (ciPTEC) |
| **2** | Moderate — injury biomarker ↑ and/or histopathology | tubular basophilic granules; KIM-1/NGAL rise |
| **3** | Severe — AKI / glomerulonephritis / renal failure | **inotersen** (grade-3 GN); **SPC5001** (tubular AKI, FIH) |

> **All grades currently carry a `grade_provisional` flag in `notes`.** Removing that flag is the **scientific sign-off we are asking German to perform** (see final slide). Grades were assigned by rubric, but the rubric→row mapping is exactly where domain judgment is most valuable.

<!--
SPEAKER NOTES — plain English

This is our scoring system — the single "answer" column that turns messy
findings into one comparable number from 0 (safe) to 3 (severe).

• "Graded label" = the answer/score attached to each row. In machine-learning
  terms the "label" is the thing you'd train a model to predict.
• "Ordinal scale" = a ranked scale where order matters but the gaps aren't
  necessarily equal (0 < 1 < 2 < 3 in severity). Like a hotel star rating.
• "Rubric" = the written rule book that says which findings earn which grade. It
  lives in the file schema.md so anyone can audit our judgement calls.
• "Canonical anchor" = a textbook reference example for that grade — a
  well-known drug everyone agrees belongs there, so the scale is calibrated.

The grades:
• 0 = no kidney signal at all — a genuine SAFE example ("negative control").
  Examples are drug types that spare the kidney: "GalNAc-siRNA" (liver-targeted,
  so little reaches kidney), "intrathecal ASO" (injected into spinal fluid, stays
  near the nervous system), and "aptamer" drugs.
• 1 = MILD: the sneaky functional problem from earlier — small-protein leakage,
  reversible, cells don't die. Anchor: drisapersen causing A1M leakage in
  "ciPTEC," which is a lab line of human proximal-tubule kidney cells
  (conditionally immortalised proximal tubule epithelial cells — a standard human
  kidney-cell model in a dish).
• 2 = MODERATE: now there's measurable injury — a biomarker rises (KIM-1/NGAL go
  up) and/or the tissue looks abnormal under the microscope ("basophilic
  granules" = the blue specks of accumulated drug). "↑" just means "increased."
• 3 = SEVERE: real kidney disease/failure. "AKI" = acute kidney injury;
  "glomerulonephritis (GN)" = inflammation of the filter units; "renal failure" =
  kidney stops working. Anchors: INOTERSEN, an approved nerve-disease oligo that
  caused glomerulonephritis in patients; and SPC5001, an experimental oligo that
  caused acute tubular injury the first time it was tried in humans ("FIH" =
  First-In-Human, the very first human trial).

The yellow box — IMPORTANT for German:
• Every grade is currently marked "grade_provisional," meaning PROVISIONAL = not
  yet confirmed by an expert. We assigned grades by following our rubric, but a
  real biochemist (German) should check that each finding was mapped to the right
  number. His sign-off lets us remove the "provisional" flag. This is the main
  thing we want from him.
-->

---

## Methodology — three extraction paths (each tagged per row)

Every row records *how* it was obtained via `source_id`:

1. **Local full-text extraction (primary sources).** PDFs supplied by the team parsed with **PyMuPDF** (text + tables); per-measurement values, doses, sequences, and figure/table loci transcribed by hand.
   → `N2` drisapersen, `K1` Sandelius, `M1` Moisan, `N3` patent panel.
2. **Secondary / review extraction.** Aggregating reviews used for marketed-drug renal findings, cross-checked against primary data. → `REV` = Wu et al. 2022.
3. **`WS` (WebSearch-derived).** This environment's network policy **blocks outbound full-text fetch** (org egress denies the CONNECT tunnel; only search summaries are available). Label/trial figures not supplied as files were taken from **search summaries of the specific FDA/EMA label or trial named in that row's `source_ref`**, flagged `source_id = WS`, and marked **to be verified against the primary source before release.**

<!--
SPEAKER NOTES — plain English

This explains the THREE ways we got our numbers, and how we tag each row so you
always know how trustworthy it is.

• "Extraction" = pulling specific data out of a source document into our table.
• "source_id" = a short code in each row naming where it came from (so the row is
  always traceable).

The three paths, from most to least solid:
1. PRIMARY SOURCES read in full. "Primary source" = the original research paper or
   official document where the data first appeared — the gold standard. The team
   uploaded PDFs and we read them directly.
   - "PyMuPDF" = a software library that reads text and tables out of PDF files.
   - "Transcribed by hand" = we typed the values in carefully, ourselves.
   - "loci" = locations (which figure or table the number came from).
   - The codes (N2, K1, M1, N3) are our nicknames for specific sources, listed on
     the next two slides.
2. SECONDARY / REVIEW sources. A "review" is a paper that SUMMARISES many other
   studies. Convenient, but one step removed from the original, so we cross-check
   it against primary data. Code "REV" = a 2022 review by Wu and colleagues.
3. "WS" = WEBSEARCH-DERIVED — the weakest tier, and we flag it honestly.
   - Why this exists: the secure computer environment we work in BLOCKS direct
     downloading of full papers from the internet (an IT security setting). In
     plain terms: "outbound full-text fetch is blocked," "egress" = outbound
     traffic, "CONNECT tunnel" = the technical way a program opens a web
     connection — it's denied. We could only get short SEARCH-ENGINE SUMMARIES,
     not the full documents.
   - So for some well-known drugs we took the figure from a web summary of the
     drug's official FDA/EMA label or trial, and we MARKED that row "WS" with a
     note that it must be re-checked against the original before any public
     release. 36 of our 111 rows are this type — honest, but provisional.
   - "FDA / EMA" = the US and European medicines regulators; a drug's "label" is
     its official, legally-vetted information sheet.
-->

---

## The rule that governs the whole dataset

> ## ⚠️ No-fabrication policy (strict)
> **`sequence_5to3` and any toxicity `readout_value` are never invented or recalled from memory.**
>
> - A **sequence** is filled only when an explicit string is returned by a credible, redistribution-permitted source — otherwise `TBD`. (e.g. inotersen, corroborated independently against the vutrisiran guide strand.)
> - A **toxicity value** is filled only when reported in the cited source.
> - **Compounds lacking published renal data were omitted, not padded** to hit the count.

This is why sequence coverage is **33/65 and not 65/65** — the remaining 32 are real gaps, honestly marked, not fabricated. For a reviewer, that distinction is the credibility of the whole table.

<!--
SPEAKER NOTES — plain English

This is our integrity rule, and it's worth stating loudly to German because it's
WHY the dataset can be trusted.

• "No-fabrication policy" = we never make anything up. Two things in particular
  are sacred and never invented:
  - "sequence_5to3" = the drug's actual genetic-letter sequence.
  - "readout_value" = any measured toxicity number.
• "Never recalled from memory" = even though an AI assistant helped build this, it
  was not allowed to fill these in from its own memory (which could be wrong).
  A value goes in ONLY if a real, citable source explicitly states it.
• "Redistribution-permitted source" = a source we're legally allowed to copy from
  (e.g. a US patent or government document, which are public domain).
• "Corroborated independently" = double-checked against a second source. Example:
  the sequence for the drug INOTERSEN was confirmed by cross-checking it against
  the published "guide strand" of a related drug, VUTRISIRAN. (A siRNA drug has
  two strands; the "guide strand" is the one that does the targeting.)
• "Compounds lacking published renal data were omitted, not padded" = if a drug
  had no real kidney data, we LEFT IT OUT rather than inventing rows to reach our
  target. "Padded" = bulked up with filler. We refused to pad.

Why the slide brags about "33/65, not 65/65":
• We have real sequences for only 33 of the 65 drugs. We could have made the other
  32 look complete by guessing — but that would be fabrication. Showing honest
  blanks ("TBD") is MORE trustworthy than a falsely-complete table. For a careful
  reviewer, that honesty is the whole point — if we fudged the easy stuff, none of
  the hard stuff could be trusted either.
-->

---

## Papers & sources researched — strict-kidney primary

The scientific backbone — direct nephrotoxicity measurements:

| ID | Source | Contribution | Rows |
|---|---|---|---:|
| **N2** | **Janssen et al. 2019**, *PMC6796739* (drisapersen) | **ciPTEC** human proximal-tubule in-vitro; A1M proteinuria *without* viability loss — the functional phenotype; **3 published sequences** | 10 |
| **N3** | **US 11,105,794 B2** (Roche/patent panel) | Table 1: per-compound LNA/MOE gapmers with **sequence + SEQ ID + in-vivo nephrotox class** — public domain | 21 |
| **M1** | **Moisan et al. 2017**, *PMC5363415* | **RPTEC/TERT1** human tubule panel; ASO uptake / EGF-pathway nephrotox in-vitro | 11 |
| **K1** | **Sandelius et al. 2020**, *PMID 33084520* | Urinary **kidney injury-biomarker** panel (KIM-1/NGAL/clusterin) | 9 |
| **A3** | **van Poelgeest et al. 2013**, *bcp.12738* | **SPC5001** first-in-human — proteinuria + tubular **AKI** (grade-3 anchor) | 3 |
| **A4** | **Arch Toxicol 2021**, *s00204-021-03062-8* | **SPC5001 kidney-on-chip** — recapitulating the FIH signal in vitro | 5 |

<!--
SPEAKER NOTES — plain English

These are our BEST, kidney-specific sources — the "primary" ones we read in full.
"Strict-kidney primary" = original papers (not summaries) that directly measured
kidney effects. The "Rows" column = how many spreadsheet rows each one gave us.
Think of this slide as the bibliography's first division.

• The IDs (N2, N3, M1, K1, A3, A4) are our internal nicknames so each data row
  can point back here. "PMC######" / "PMID########" = public ID numbers for papers
  in the US national library (PubMed). "US 11,105,794 B2" = a US patent number.
  "bcp.12738" / "s00204-..." = journal article DOIs (permanent article IDs).

Source by source:
• N2 — Janssen 2019 (drisapersen): the key paper showing the SNEAKY phenotype in a
  dish. "ciPTEC" = a line of human proximal-tubule kidney cells grown in the lab.
  They saw small-protein (A1M) leakage WITHOUT the cells dying — exactly the
  functional-not-deadly signal. Also gave us 3 real drug sequences. 10 rows.
• N3 — US patent 11,105,794: the volume jackpot. A patent containing a TABLE of
  many oligos, each listed with its sequence, an ID number ("SEQ ID"), and a
  rating of how kidney-toxic it was in animals ("in-vivo nephrotox class").
  Because US patents are "public domain" (free to copy), we could reproduce it.
  "LNA/MOE gapmers" = the gapmer design (central gap + modified wings) using LNA
  or 2′-MOE chemistry in the wings. 21 rows — our single biggest source.
• M1 — Moisan 2017: experiments on "RPTEC/TERT1," another human kidney-tubule cell
  line (immortalised so it keeps growing). Looked at how oligos get taken up and
  disturb the "EGF pathway" (EGF = epidermal growth factor, a cell-signalling
  system). 11 rows.
• K1 — Sandelius 2020: measured the urine INJURY-BIOMARKER panel (KIM-1, NGAL,
  clusterin) — the early-warning chemicals. 9 rows.
• A3 — van Poelgeest 2013: the human story of SPC5001, an oligo that caused
  protein in urine and acute kidney injury the FIRST time it was given to people
  ("first-in-human"). This is a key severe (grade-3) anchor. 3 rows.
• A4 — Arch Toxicol 2021: the SAME drug (SPC5001) reproduced on a "kidney-on-chip"
  — a thumb-sized device with living kidney cells in tiny channels that mimics a
  real kidney. It "recapitulated" (reproduced) the human injury, validating the
  lab model. 5 rows.
-->

---

## Papers & sources researched — anchors, reviews & patents

| ID | Source | Role |
|---|---|---|
| **REV** | **Wu et al. 2022**, *PMC10174585* | Marketed-ASO nephrotoxicity review — cross-checked anchor findings (4 rows) |
| **A1** | inotersen — **NEJM 2018 NEURO-TTR** + FDA label 211172 | **Grade-3 glomerulonephritis** — canonical severe anchor |
| **A9** | mipomersen — FDA 203568 + EMA Kynamro EPAR | 2′-MOE gapmer renal monitoring |
| **A8** | volanesorsen — EMA Waylivra + APPROACH (NCT02658175) | APOC3 gapmer renal signal |
| **A10 / A5 / A7** | inclisiran (Leqvio) · givosiran (Givlaari) · nusinersen (Spinraza) | GalNAc-siRNA & intrathecal **negative/low** controls |
| **N3 / N4** | **US 11,105,794 B2** · **US 11,479,818 B2** | In-vitro nephrotox-assay patents (public domain); N4 staged for unique-compound mining |

**`WS` anchor set (36 rows)** — FDA/EMA labels + pivotal trials for: patisiran (Onpattro), vutrisiran (HELIOS-A), lumasiran (ILLUMINATE-B), nedosiran (PHYOX3), eplontersen (Wainua), tofersen (Qalsody), bepirovirsen (B-Clear), olpasiran (OCEAN-DOSE), the DMD PMOs (eteplirsen/golodirsen/casimersen/viltolarsen), pegaptanib (Macugen), fitusiran (Qfitlia), zilebesiran (KARDIA), plus **Crooke 2018 pooled-human** and **Yu 2012 ISIS-113715 monkey** translation references.

<!--
SPEAKER NOTES — plain English

The second half of the bibliography: real-world drug evidence used as reference
points ("anchors"), one big review, and patents.

• "Anchor" = a well-established example we trust to calibrate the scale.
• "Marketed / approved drug" = a drug already on sale (strongest real-world
  evidence). Most entries below are named by brand (in parentheses).
• "NEJM" = New England Journal of Medicine (top medical journal). "FDA label
  #####" = the US drug's official document and its number. "EMA ... EPAR" =
  the European regulator's public assessment report. Trial names in caps
  (NEURO-TTR, APPROACH, HELIOS-A…) are the specific clinical trials.

Row by row:
• REV — Wu 2022: a REVIEW summarising kidney toxicity of marketed antisense drugs;
  used to cross-check our anchors. 4 rows.
• A1 — INOTERSEN: our headline SEVERE example. In its pivotal trial (NEURO-TTR) and
  on its FDA label it caused glomerulonephritis (filter-unit inflammation) →
  grade 3. "2′-MOE gapmer" chemistry.
• A9 — MIPOMERSEN (Kynamro): another 2′-MOE gapmer; its labels note kidney
  monitoring. "Renal monitoring" = doctors must watch the kidney while dosing.
• A8 — VOLANESORSEN (Waylivra): targets the APOC3 gene; had a kidney signal in the
  APPROACH trial (NCT… is the trial's registry number).
• A10/A5/A7 — INCLISIRAN (Leqvio), GIVOSIRAN (Givlaari), NUSINERSEN (Spinraza):
  used as SAFE/low examples. The first two are "GalNAc-siRNA" (liver-targeted, so
  the kidney is largely spared); nusinersen is given "intrathecally" (into spinal
  fluid) so it stays near the nervous system. Good negative controls.
• N3/N4 — two US PATENTS describing lab tests ("assays") for oligo kidney
  toxicity. N3 we already mined (previous slide). N4 (US 11,479,818) is queued for
  later, to pull out any NEW compounds not already in our set ("unique-compound
  mining"). Patents are public domain, so freely reproducible.

THE "WS" SET (36 rows) — explained on the methodology slide as the web-summary
tier. These are mostly approved oligo drugs whose kidney info we took from
summaries of their official labels/trials and flagged for re-checking. You don't
need every name, but for orientation they include:
• siRNA drugs (mostly liver- or kidney-relevant): patisiran, vutrisiran, lumasiran,
  nedosiran, olpasiran, fitusiran, zilebesiran.
• ASO drugs: eplontersen, tofersen, bepirovirsen.
• "DMD PMOs" = four muscular-dystrophy drugs of the PMO type (eteplirsen,
  golodirsen, casimersen, viltolarsen). "PMO" = a special neutral-backbone oligo
  used to patch faulty gene splicing. ("DMD" = Duchenne muscular dystrophy.)
• pegaptanib (Macugen) = an "aptamer" eye drug (an oligo folded into a shape that
  grabs a target protein, like an antibody made of nucleic acid).
• "Crooke 2018 pooled-human" and "Yu 2012 monkey" = two TRANSLATION references —
  they let us compare what happens in monkeys vs. humans (see the next-but-one
  slide on animals over-predicting human risk). "ISIS-113715" is a research
  compound's code name.
-->

---

## Key finding 1 — the functional-not-cytotoxic phenotype is captured, in machine-readable form

- The dataset contains **explicit paired rows** where the *same* oligo is **grade-1 on a functional readout and grade-0 on viability/histopathology.**
- Example (drisapersen, `N2`): A1M proteinuria in **ciPTEC** → grade 1; viability unchanged → grade 0; monkey histopathology clean → grade 0.
- This is the single most important scientific property of the set: a model trained on it can learn the distinction **reversible functional proteinuria vs. structural tubular injury** — which viability-only datasets *cannot* teach.
- **35 functional + 16 injury-biomarker rows** vs. only **7 viability rows** — the readout mix reflects the biology, not assay convenience.

<!--
SPEAKER NOTES — plain English

The first of three "headline findings." This one says: we successfully captured
the sneaky-damage signal in a form a computer can learn from.

• Recap of the core idea (from slide 3): these drugs often make kidney cells stop
  WORKING properly without KILLING them. A simple "are the cells alive?" test
  misses it.
• "Paired rows" = for the same drug, one row scores the functional problem (a
  grade 1) and another row scores the cell-survival/tissue tests (grade 0). Seen
  together they encode "dysfunction without death."
• The drisapersen example again: protein leakage in human kidney cells = grade 1;
  cells alive = grade 0; monkey tissue normal under microscope = grade 0.
• Why it matters: a computer model trained on this can learn to tell apart:
  - "reversible functional proteinuria" = the mild, goes-away protein leak, vs.
  - "structural tubular injury" = actual physical damage to the tubule.
  A dataset that only recorded "alive/dead" could never teach that difference.
• The numbers (35 functional + 16 biomarker vs only 7 viability) prove we
  prioritised the meaningful measurements over the easy/cheap one. "Assay
  convenience" = picking a test because it's easy rather than because it's
  informative — we deliberately did NOT do that.
-->

---

## Key finding 2 — the patent panel unlocked sequence-resolved volume

- **US 11,105,794 B2, Table 1** was the breakthrough source: a clean per-oligo panel of LNA/MOE gapmers giving **compound → sequence → SEQ ID → in-vivo nephrotoxicity class**, all **public domain.**
- Mapped the patent's qualitative in-vivo classes to our rubric: *innocuous → 0, low → 1, low/medium & medium → 2, medium/high & high → 3.*
- Impact: **+21 measurement rows and tripled sequence coverage (13 → 33 sequences).** This is the only large block where **sequence and graded outcome sit in the same record** — the most directly model-ready slice of the dataset.

<!--
SPEAKER NOTES — plain English

The second headline finding: a single patent gave us a big, unusually complete
block of data — the kind most useful for future modelling.

• "Patent panel" = a table inside a patent document listing many compounds and
  their test results.
• Why it's special: for each oligo it provides BOTH the genetic sequence AND a
  toxicity rating, in the same row. That pairing is rare and valuable — usually
  you find a sequence in one place and toxicity in another.
• "Sequence-resolved volume" = lots of rows that each include the actual sequence.
• "compound → sequence → SEQ ID → in-vivo nephrotox class" = for each drug the
  table lists its name, its letters, an ID number, and a rating of its kidney
  toxicity in live animals ("in-vivo").
• "Public domain" = freely reproducible (US patents are), so we could legally copy
  the values.
• "Mapped the qualitative classes to our rubric" = the patent rated toxicity in
  WORDS (innocuous / low / medium / high). We translated those words into our 0–3
  numbers so they match the rest of the dataset:
  innocuous→0, low→1, low-or-medium & medium→2, medium-high & high→3.
  ("Qualitative" = described in words/categories rather than exact numbers.)
• Impact: +21 rows, and our count of real sequences jumped from 13 to 33 (roughly
  tripled).
• "Model-ready" = in the ideal shape for training a predictive model, because
  cause (sequence) and effect (grade) sit together in one record.
-->

---

## Key finding 3 — animal toxicology over-predicts human renal risk

- A documented, modellable bias: **2′-MOE ASO animal toxicology over-predicts human renal effects.**
- Captured explicitly rather than hidden — e.g. the **Crooke 2018 pooled-human** entry and the **Yu 2012 monkey** ISIS-113715 entry sit in the same table, same readout vocabulary, different species.
- Distribution makes the translation axis learnable: **human 58 · mouse 30 · monkey 7 · rat 8 · multi-species 8**, across **in-vitro 19 / animal 53 / clinical 39** rows.
- A reviewer/modeler can therefore study the **animal→human translation gap directly** instead of treating animal histopathology as ground truth for human risk.

<!--
SPEAKER NOTES — plain English

The third headline finding: animals tend to look MORE kidney-damaged than people
actually turn out to be for this drug type — and we captured that gap on purpose
so it can be studied, not hidden.

• "Animal toxicology over-predicts human renal risk" = when you test these oligos
  (specifically 2′-MOE ASOs) in animals, the kidneys look worse than what
  actually happens in human patients. So animal results can be overly alarming.
  "Renal" = kidney.
• "Documented, modellable bias" = this over-prediction is a known, consistent
  pattern — which means a computer model could actually learn to correct for it.
  A "bias" here = a systematic lean in one direction, not a random error.
• How we captured it: we put HUMAN data and ANIMAL data side by side in the same
  table, measured the same way, so the difference is visible.
  - "Crooke 2018 pooled-human" = combined safety data from many human patients.
  - "Yu 2012 monkey (ISIS-113715)" = a monkey toxicology study of one research
    compound. Same readouts, different species → you can compare directly.
• "Translation axis" / "animal→human translation gap" = the question of how well
  an animal result predicts the human result. "Translation" = carrying a finding
  from one species to another.
• The species/study counts show we have enough of each (58 human, 30 mouse, etc.;
  19 dish + 53 animal + 39 human-clinical rows) to actually study that gap.
• "Treating animal histopathology as ground truth" = blindly assuming the animal
  microscope result equals the human truth. We AVOID that — we let the data show
  where animals and humans disagree. ("Ground truth" = the assumed-correct answer.)
-->

---

## Final dataset — at a glance

| Dimension | Distribution |
|---|---|
| **Records** | **65 oligos · 111 measurements** (≥100 target met; all strict-kidney) |
| **Grade (0/1/2/3)** | 27 · 30 · 39 · 15 |
| **Modality** | ASO gapmer 40 · GalNAc-siRNA 12 · splice-switching/SSO 4 · PMO 4 · siRNA 2 · 1st-gen PS-DNA 2 · aptamer 1 |
| **Backbone** | full-PS 45 · PS/PO-mix 15 · PMO-neutral 4 · mixed 1 |
| **Conjugate** | none 48 · GalNAc 16 · PEG 1 |
| **Stage** | approved 19 · research-panel 30 · phase 3 (incl. disc.) 9 · phase 2 5 · phase 1 1 · class-level 1 |
| **Study type** | animal 53 · clinical 39 · in-vitro 19 |
| **Species** | human 58 · mouse 30 · multi 8 · rat 8 · monkey 7 |
| **Delivery** | systemic 87 · gymnotic/free-uptake 19 · intrathecal 3 · intravitreal 1 · oral 1 |
| **Sequences filled** | **33 / 65** (rest `TBD`, never guessed) · **35 target genes** |

<!--
SPEAKER NOTES — plain English

This is the scoreboard — the whole dataset summarised in counts. "Distribution"
just means "how the rows split across categories." Reading it row by row:

• RECORDS: 65 distinct drugs, 111 measured results. Target was ≥100 → met. Every
  row is kidney-specific.
• GRADE (0/1/2/3): how many results fell at each severity — 27 safe, 30 mild,
  39 moderate, 15 severe. A healthy spread from safe to severe (good for modelling
  — you need examples of every level).
• MODALITY = the drug families and how many of each:
  - "ASO gapmer" (40) = the central-gap antisense design — our biggest group.
  - "GalNAc-siRNA" (12) = liver-targeted double-stranded silencers.
  - "splice-switching / SSO" (4) = oligos that change how a gene is assembled
    ("spliced") rather than destroying it.
  - "PMO" (4) = the neutral-backbone splice-switchers (the muscular-dystrophy
    drug type).
  - "siRNA" (2) = double-stranded silencers without the liver tag.
  - "1st-gen PS-DNA" (2) = older first-generation phosphorothioate DNA oligos.
  - "aptamer" (1) = the antibody-like folded oligo.
• BACKBONE = the spine chemistry: "full-PS" (45, every link sulfur-modified),
  "PS/PO mix" (15, partly normal links), "PMO-neutral" (4, the uncharged PMO
  type), "mixed" (1).
• CONJUGATE = bolt-on targeting tags: most have none (48); 16 carry the liver
  "GalNAc" sugar; 1 carries "PEG" (the long-life polymer).
• STAGE = how far each drug has progressed: 19 approved (on the market), 30 are
  research compounds, the rest are in clinical trials (phase 1→3; "incl. disc." =
  including some discontinued), plus 1 scored at the whole-class level.
• STUDY TYPE = where the result came from: 53 animal studies, 39 human/clinical,
  19 in-vitro (dish).
• SPECIES = which organism: 58 human, 30 mouse, 8 multi-species, 8 rat, 7 monkey.
• DELIVERY = how the drug was given:
  - "systemic" (87) = into the whole body (e.g. injection into blood/under skin).
  - "gymnotic / free-uptake" (19) = in a dish, letting cells absorb the naked oligo
    on their own with no delivery helper ("gymnotic" = "naked" uptake).
  - "intrathecal" (3) = into the spinal fluid. "intravitreal" (1) = into the eye.
    "oral" (1) = by mouth.
• SEQUENCES FILLED: 33 of 65 drugs have their real sequence; the rest are honest
  blanks. 35 different target genes are represented (good diversity).
-->

---

## Provenance & redistribution — every row is defensible

- **Each measurement carries `source_id` + `source_ref` + `source_table`** (exact figure / table / label section / patent claim). Any value can be re-verified against its locus.
- **Redistribution tracked per row:** `public_domain` 47 (FDA/EMA labels, USPTO patents — values reproducible) · `summary_stat` 64 (journal-derived figures — derived/summary only).
- **16 distinct source identifiers** in use, all registered in `sources/SOURCES.md` with acquisition state.
- Intended public license for the curated tables: **permissive (e.g. CC-BY)**; third-party full texts are **referenced, not redistributed.**

**QC run after every ingestion round (all currently passing):** schema-enum conformance · column-count integrity (17/23) · referential integrity `measurements.oligo_id → oligos.oligo_id` (**0 orphans**) · no duplicate PKs · `nephrotox_grade ∈ {0,1,2,3}` · sequence policy (only explicitly-sourced sequences filled).

<!--
SPEAKER NOTES — plain English

Two things here: (1) every number has a paper trail, and (2) we respect copyright.
Both are scored by the competition and both build trust.

• "Provenance" = the documented origin/paper-trail of each value — where exactly it
  came from. Each row stores three breadcrumbs:
  - "source_id" = the short code (N2, A1, WS…) for the source.
  - "source_ref" = the precise reference (paper ID, label number, patent number).
  - "source_table" = the exact figure, table, label section, or patent claim the
    number sits in.
  "Re-verify against its locus" = anyone can open that exact table and confirm the
  number. ("Locus" = the precise spot.)

• "Redistribution" = our legal right to republish a value. Tracked per row:
  - "public_domain" (47 rows) = free to copy outright — US government documents
    (FDA/EMA labels) and US patents ("USPTO" = the US Patent Office).
  - "summary_stat" (64 rows) = from copyrighted journals, so we only reproduce
    SUMMARY statistics / derived figures, not the raw copyrighted tables. This
    keeps us on the right side of copyright.
• "16 source identifiers" = 16 distinct sources in total, all catalogued in
  sources/SOURCES.md with their "acquisition state" (whether we have the file yet).
• "License: CC-BY" = the open licence we intend to release OUR tables under — it
  lets anyone reuse them as long as they credit us. We REFERENCE the third-party
  papers (cite them) but do NOT republish their full text.

• "QC" = quality-control checks that run after every batch of new data
  ("ingestion round" = a round of adding data). In plain terms they confirm:
  - every category value is from the allowed list ("schema-enum conformance";
    an "enum" = a fixed list of allowed values);
  - the tables have the right number of columns (17 and 23);
  - "referential integrity, 0 orphans" = every result points to a real drug; no
    result references a drug ID that doesn't exist (an "orphan" would be a result
    with no matching drug);
  - no duplicate ID numbers;
  - every grade is 0, 1, 2, or 3 (nothing out of range);
  - the no-guessing sequence rule held.
  All of these currently PASS.
-->

---

## Honest limitations (what a reviewer should know)

- **Grades are provisional** — assigned by rubric, pending the scientific sign-off requested here.
- **Sequence coverage is 33/65.** Remaining gaps are siRNA guide strands and some PMOs whose sequences were not transcribable from available summaries (and never guessed).
- **`WS` rows (36)** rest on search summaries of primary regulatory/trial sources — they need a verification pass against the cited primary document before publication.
- **In-vitro human-system rows (19)** are the scientific core but still a minority; expanding human proximal-tubule panels (ciPTEC / RPTEC-TERT1 / 3D-RPTEC / kidney-on-chip) is the top growth priority.
- **Animal over-prediction** is present by design and must be *modeled*, not ignored.

<!--
SPEAKER NOTES — plain English

We state our weaknesses openly. For a scientific reviewer, admitting limits builds
MORE trust, not less — it shows we know exactly where the soft spots are.

• "Grades are provisional" = our 0–3 scores aren't expert-confirmed yet. That's the
  sign-off we're asking German for.
• "Sequence coverage 33/65" = we still lack the genetic sequence for 32 drugs.
  Mostly these are:
  - "siRNA guide strands" = the targeting strand of double-stranded siRNA drugs,
    not always published; and
  - some "PMO" drugs whose sequences weren't available in the summaries we could
    reach. We left these blank rather than guess.
• "WS rows (36)" = the web-summary-sourced rows. They must be double-checked against
  the original FDA/EMA/trial documents before any public release. ("Verification
  pass" = a round of re-checking.)
• "In-vitro human-system rows (19)" = results from human kidney cells in a dish.
  These are the scientific heart of the set (human-relevant, mechanism-revealing)
  but they're still a minority of rows, so GROWING them is our top priority. The
  named models are all human kidney-tubule systems: ciPTEC, RPTEC/TERT1, its 3D
  version, and the kidney-on-chip device.
• "Animal over-prediction... must be modeled, not ignored" = the animal-vs-human
  gap from finding 3 is a feature to account for, not a flaw to hide. Anyone using
  the data should remember animal kidney results run alarmist for these drugs.
-->

---

## What we need from German (the ask)

1. **Grade sign-off.** Review the rubric→row mapping in `data/measurements.csv` and the rubric in `schema.md`; confirm or correct grades so we can **remove the `grade_provisional` flag.** Highest-value targets: the grade-2/3 boundary (injury-biomarker vs. AKI) and the patent-class → grade mapping.
2. **Biology sanity check.** Is the **functional-vs-structural** framing (megalin/cubilin → LMW proteinuria → grade 1) faithful, and are the readout→severity assignments physiologically sound?
3. **Source confidence.** Flag any anchor you'd want re-verified against primary text before release (esp. the `WS` set).

**Then (on hold until sign-off):** finalize the ≤12-page narrative; verify `WS` rows; backfill remaining sequences; optionally mine patent **N4 (US 11,479,818)** and **US 11,105,794 Table 2** (per-compound in-vitro EGF values) for the next volume increment.

<!--
SPEAKER NOTES — plain English

This is the call to action — exactly what we want German (the expert biochemist)
to do. Keep it concrete so he can act without re-reading everything.

1. GRADE SIGN-OFF (the big one): look at our 0–3 scores in the measurements file
   and the rule book (schema.md), and confirm or fix them. Once he approves, we
   delete the "provisional" flag and the grades become final.
   - "rubric→row mapping" = the judgement call of which finding got which grade.
   - Two trickiest spots we'd love him to focus on:
     (a) the line between grade 2 and grade 3 — i.e. is a finding "a worrying
         biomarker rise" (2) or "actual acute kidney injury" (3)?
     (b) whether we translated the PATENT's word-ratings into grades correctly.
2. BIOLOGY SANITY CHECK: does our core scientific story hold up? Specifically the
   chain "drug grabbed by megalin/cubilin → small-protein leakage → we call that a
   mild grade 1." And are our readout-to-severity calls physiologically sensible
   (i.e. do they match how a kidney really behaves)? "Physiologically sound" =
   consistent with real body function.
3. SOURCE CONFIDENCE: point out any reference he'd want re-checked against the
   original before we publish — especially the 36 web-summary ("WS") rows.

• "On hold until sign-off" = the remaining to-do list that we deliberately PAUSED
  until German weighs in, so we don't polish things he might change:
  - finish the short written narrative (≤12 pages) the competition wants;
  - re-verify the WS rows;
  - fill in more sequences where possible;
  - optionally pull more data from a second patent (N4) and from Table 2 of the
    first patent (which has per-drug lab "EGF" values) to add volume.
  "Backfill" = go back and fill gaps. "Volume increment" = another batch of rows.
-->

---

## Repository map (for review)

```
README.md            strategy, scope, domain rationale, live record counter
schema.md            full data dictionary, grade rubric, vocab + QC log
METHODOLOGY.md       Phase-2 methodology deliverable (source→grade→QC)
PRESENTATION.md      this deck
data/oligos.csv      65 oligos  · 17 predictor columns
data/measurements.csv  111 graded rows · 23 columns · full provenance
sources/SOURCES.md   source registry (16 IDs), acquisition state, drop-list
sources/kidney/      drisapersen, Wu, Sandelius, Moisan, SPC5001, patents …
sources/hepatotox/   Dieckmann, Burdick, Hagedorn (chemistry diversity, flagged non-kidney)
```

**Thank you — feedback welcome at the row level.** Every number in this deck regenerates from `data/` (`python` count scripts in the repo history); nothing here is hand-maintained prose detached from the tables.

<!--
SPEAKER NOTES — plain English

A guide to the files in the project folder ("repository" / "repo" = the project's
folder of files, tracked with version control), so German knows where to look.

• README.md = the front-page overview: what we're doing and a live tally of rows.
• schema.md = the data DICTIONARY: defines every column and the grading rule book.
  "Vocab" = the lists of allowed category values. This is where to check our
  grading rules.
• METHODOLOGY.md = the formal write-up of HOW we built it (sources → grading → QC);
  one of the competition's required deliverables.
• PRESENTATION.md = this slide deck.
• data/oligos.csv = the 65 drugs and their 17 design features.
• data/measurements.csv = the 111 results with grades and full source trail (23
  columns). THIS is the file to review for grade sign-off.
• sources/SOURCES.md = the catalogue of all 16 sources and whether we have each
  file ("acquisition state"), plus a "drop-list" of files still wanted.
• sources/kidney/ = the actual kidney source PDFs.
• sources/hepatotox/ = LIVER-toxicity papers kept only for chemistry variety and
  clearly flagged as NOT kidney, so they never pollute the kidney data. ("Hepato"
  = liver.)

• Closing point: "feedback welcome at the row level" = please comment on specific
  rows, not just generalities. "Every number regenerates from data/" = nothing on
  these slides is hand-typed and possibly stale — all the counts come straight out
  of the data files via little Python scripts, so they always match the data.
-->
