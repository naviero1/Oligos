# Thrombocytopenia

Reduced circulating platelet count following oligonucleotide treatment — observed with "approximately 10%" of 2′-MOE PS
ASOs and dose-limiting in two phase I oncology trials (Frazier 2015, PDF p.7), and severe in the highest dose group of
three phase 3 programmes (MMB Ch.25, PDF pp.355–356). It is the third endpoint in the Challenge brief's list, quoted
verbatim in [`README.md`](./README.md) under "Scope authority". **This project holds no thrombocytopenia data and
acquired no source for it.** Its only material sits inside four cross-cutting files held for other endpoints (§3).

## 1. Status

| | Value |
|---|---|
| Oligos in [`data/oligos.csv`](../data/oligos.csv) | 0 |
| Measurement rows in [`data/measurements.csv`](../data/measurements.csv) | 0 |
| Local source PDFs | 0 dedicated; of the 4 cross-cutting PDFs in §3, only Frazier 2015 has a section on the endpoint |
| `source_id`s reaching `measurements.csv` | none; none was ever assigned |
| Mentions in the curated corpus | 0 — `grep -rniE -e thrombocytopeni -e platelet` over `data/`, `sources/*.md`, `scripts/`, `METHODOLOGY.md`, `schema.md`, `PADP.md` and `PRESENTATION.md` exits 1. The endpoint is named in `README.md` and `REVIEW-2026-08.md`, both part of the index layer this reorganization added. |

## 2. Work done

No extraction work: no PDF acquired, no `source_id` assigned, no row extracted, no rubric written. The assessment below
— keyword sweeps over all 18 PDFs in `sources/` and every cell of both CSVs, plus the reference-list scan in §5 — was
performed for this dossier.

**Decision, recorded here 2026-08-28: thrombocytopenia is out of scope for Phase 2.** The material in §3 was assessed
and carries no per-compound platelet value, so no row can be built from it. Nothing in `data/`, `sources/` or `scripts/`
mentions the endpoint (§1, §4), so no other position on it is recorded; §7 item 1 carries this one into `README.md`.

## 3. Sources allocated

No file in `sources/` is a thrombocytopenia source. The four below belong to [`cross-cutting.md`](./cross-cutting.md),
section 1 "Cross-cutting source material", and are only cross-referenced here; none has a `source_id`. Paths verified by
directory listing; hit counts are case-insensitive regex counts over each file's full text extract, recomputed here.

| File | Pages | `thrombocytopeni` / `platelet` | State | Rows | What it carries |
|---|---:|---|---|---:|---|
| `sources/reference/Frazier2015_ASO_therapies_review_ToxPathol.pdf` | 12 | 16 / 19 | acquired; `sources/SOURCES.md:208` | 0 | The only substantive treatment held: dedicated section "THROMBOCYTOPENIA (CHALLENGE #3)", PDF p.7, carrying 13 of the 16 hits. The abstract names thrombocytopenia as the third of three "lingering challenges"; the section reports reduced platelet counts with "approximately 10%" of 2′-MOE PS ASOs and calls the effect "compound-specific rather than a common oligonucleotide class effect" (PDF p.7), yet names no compound and gives every quantity for a chemistry class or a dose level only |
| `sources/kidney/MethodsMolBiol2022_book_incl_renal-tox-mice_chapter.pdf` | 416 | 5 / 4 | acquired; `sources/SOURCES.md:200` | 0 | No section on the endpoint: Ch.25 §3.1.3 is "Sequence Dependent, But Hybridization Independent: Inflammation, Liver, and Kidney Toxicities" (opens PDF p.354) and thrombocytopenia is a passage inside it, PDF pp.355–356. The 9 hits fall on PDF pp.23 and 27 (Ch.1), 355, 356, and 363 and 364 (reference entries, §7) |
| `sources/reference/CasarettDoull_Toxicology_textbook.pdf` | 1,473 | 52 / 176 | acquired; `sources/SOURCES.md:210` | 0 | General toxicology background only; 13 `oligonucleotide` and 7 `antisense` hits in 1,473 pages |
| `sources/reference/OligoTox_challenge_brief.pdf` | 6 | 1 / 0 | acquired; `sources/SOURCES.md:211` | 0 | The single hit is the eight-endpoint scope sentence on p.1 |

Of the 14 remaining PDFs in `sources/`, one carries hits — `sources/kidney/Wu_Nephrotoxicity_marketed_ASO_drugs_review_PMC10174585.pdf` (1 / 1),
both in its reference list (PDF pp.13 and 17, the subject of §5) and neither in its body text; the other 13 return 0 for both terms.

## 4. Data

**Zero rows.** A case-insensitive sweep of every cell of `data/measurements.csv` (111 × 23) and `data/oligos.csv` (65 ×
17) for `platelet|thrombocyt|h[ae]matolog|PLT|bleed|coagul` returns 0 hits, and the `readout_category` enum at
[`schema.md`](../schema.md)`:54` has no value that could hold a haematology readout. The one link to the dataset runs
through oligo identity: MMB 2434 Ch.25 §3.1.3 (PDF p.355; running head book p.360) states "Severe TCP was observed in the
phase 3 studies for volanesorsen and inotersen as well as for drisapersen [86, 100, 101]." All three are in the dataset:

| `oligo_id` | `oligo_name` | Kidney rows |
|---|---|---|
| `OLG001` | inotersen | 5 — MSR001–MSR004, MSR076 |
| `OLG005` | volanesorsen | 2 — MSR012, MSR013 |
| `OLG008` | drisapersen | 8 — MSR017–MSR024 |

15 of the 111 rows are therefore on molecules an acquired source names for severe phase-3 thrombocytopenia; all 15 are
renal measurements and carry no platelet information. The overlap names compounds for an acquisition plan, nothing more.

## 5. Known issues

The two most directly relevant primary sources are transcribed below from the reference list of an acquired PDF — they
are that source's citations, not this dossier's, and neither appears in `sources/SOURCES.md`: Narayanan et al. 2020,
*Nucleic Acid Ther* 30:94–103 (PMID 32043907), on inotersen-mediated thrombocytopenia, reference [10] of the Wu review at
PDF p.13; and Crooke et al. 2017, *Nucleic Acid Ther* 27:121–129 (PMID 28145801), on 2′-MOE ASO effects on platelets in
human trials, reference [74] at PDF p.17. `SOURCES.md:178-180` recommends mining that reference list, and neither paper
reached the registry. (The "Crooke pooled 2′-MOE" at `METHODOLOGY.md:197` for `OLG031` is a renal paper, not this one.)

## 6. Not done, and why

| Not done | Cause |
|---|---|
| No rows extracted | No in-repo source attaches a platelet value to a named compound. Frazier 2015 §THROMBOCYTOPENIA (PDF p.7) gives quantities — "below 40,000/mL", "more than 20 mg/kg/wk in monkeys", "3.0 mg/kg/day" — but attaches none to a compound, and the review has no numbered tables (`TABLE`/`Table` regex count over its text extract = 0); MMB Ch.25 §3.1.3 names three compounds (§4) without per-study values. |
| No grading rubric | The 0–3 ladder in [`schema.md`](../schema.md) is written entirely in renal terms and is not transferable — see [`cross-cutting.md`](./cross-cutting.md), section 4 "What must change if a second endpoint is populated". |
| Scope decision not landed | The decision in §2 is not reflected outside `toxicity/`: `README.md` § "Scope (decided — not under review)" still records kidney with no exclusions, and neither `METHODOLOGY.md` §1 nor `sources/SOURCES.md` records an exclusion for this endpoint. |

## 7. Next step

1. Carry the out-of-scope statement into `README.md` § "Scope (decided — not under review)" and `METHODOLOGY.md`
   section 1 (`## 1. Scope and design decisions`, line 20).
2. Register Frazier 2015 under the four endpoints [`cross-cutting.md`](./cross-cutting.md) allocates it to in section
   1.3 "Frazier 2015" — kidney, hepatotoxicity, thrombocytopenia, complement activation; the single `reference/` filing
   at `SOURCES.md:208` under-describes it. That file's MMB 2434 allocation (section 1 table; section 1.4 "Methods in
   Molecular Biology 2434 — misfiling finding") omits thrombocytopenia, which §3 and §4 show Ch.25 carries — reconcile.
3. If the endpoint is advanced, acquire Narayanan 2020 or Crooke 2017 (§5), or the two candidates transcribed from MMB's
   reference list — Sewing et al. 2017, *PLoS One* 12(11):e0187574 (ref. 82, PDF p.363) and Henry et al. 2017, *Nucl
   Acid Ther* 27(4):197–208 (ref. 99, PDF p.364). Schema first: a separate graded column, not a reuse of
   `nephrotox_grade`.
