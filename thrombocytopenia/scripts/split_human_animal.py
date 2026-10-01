#!/usr/bin/env python3
"""Build the human-first evidence views over the thrombocytopenia dataset.

WHY THIS IS ORDERED THE WAY IT IS
  Human clinical evidence is the headline, human laboratory evidence is the part
  the challenge singles out ("datasets based on in vitro human systems"), and
  animal evidence is supporting material. Earlier versions of this script mixed
  them: `germans_analysis.csv` was sorted on a POOLED human+animal grade, which
  put "Dmpk Chol-ASO" -- a compound with zero human rows -- second in the file,
  ranked above every human clinical finding, on the strength of one mouse
  bleeding observation. No animal record may influence a human count, a human
  label, or a human ranking. Animal data is kept in full, in its own appendix.

  Grade means are gone from the ranking. Averaging an ordinal severity grade
  across heterogeneous endpoints, doses, durations and biological systems does
  not produce a meaningful number. Each compound now carries a grade HISTOGRAM
  (`0:12;1:3;2:1`), which says everything the mean said and nothing it did not.

OUTPUTS (reading order)
  data/coverage_and_limitations.csv   what this dataset does and does not support
  data/measurements_human_clinical.csv  human clinical outcome records
  data/measurements_human_lab.csv       human in vitro / ex vivo records
  data/measurements_human.csv           all human rows (compatibility view)
  data/measurements_unresolved.csv      species/subject unresolved -- assigned to neither side
  data/measurements_animal.csv          animal appendix
  data/bridge_human_animal.csv          compounds with both, exposures shown side by side
  data/germans_analysis.csv             compound · sequence · modification · toxicity

Usage:  python3 scripts/split_human_animal.py
"""
import csv, os, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")

# Identity plus the two things a reader always needs -- SEQUENCE and TOXICITY
# GRADE -- lead every enriched export, so they are visible without scrolling.
LEAD = ["measurement_id", "oligo_id", "oligo_name", "sequence_5to3",
        "thrombocytopenia_grade", "subject_class", "modification_map",
        "gapmer_design", "sugar_modifications", "backbone_chemistry", "ps_count",
        "conjugate", "length_nt", "oligo_class", "target_gene",
        "scientist_disposition", "clinical_model_eligibility",
        "mechanistic_model_eligibility", "exact_sequence_group"]

HUMAN_CLINICAL = {"human_clinical"}
HUMAN_LAB = {"human_in_vitro", "human_ex_vivo"}


def load():
    with open(os.path.join(BASE, "oligos.csv"), newline="", encoding="utf-8") as f:
        orows = list(csv.DictReader(f))
    with open(os.path.join(BASE, "measurements.csv"), newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        return {r["oligo_id"]: r for r in orows}, list(orows[0].keys()), rdr.fieldnames, list(rdr)


def enriched_columns(ocols, mcols):
    cols = list(LEAD)
    for c in [c for c in ocols if c not in LEAD]:
        cols.append("oligo_notes" if c == "notes" else c)
    for c in [c for c in mcols if c not in LEAD]:
        cols.append("measurement_notes" if c == "notes" else c)
    return cols


def enrich(rows, oligos, cols):
    out = []
    for m in rows:
        o = oligos.get(m["oligo_id"], {})
        r = {}
        for c in cols:
            if c == "oligo_notes":        r[c] = o.get("notes", "")
            elif c == "measurement_notes": r[c] = m.get("notes", "")
            elif c in m:                   r[c] = m[c]
            else:                          r[c] = o.get(c, "")
        out.append(r)
    return out


def write(name, cols, rows):
    with open(os.path.join(BASE, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    print(f"  {len(rows):>5} rows  ->  data/{name}")


def grade(r):
    try: return int(r["thrombocytopenia_grade"])
    except (ValueError, TypeError, KeyError): return 0


def hist(rows):
    c = collections.Counter(grade(r) for r in rows)
    return ";".join(f"{k}:{c[k]}" for k in sorted(c))


def worst(rows):
    if not rows: return "", ""
    w = max(rows, key=grade)
    return (f"{w.get('readout_name','')} = {w.get('readout_value','')} "
            f"{w.get('readout_unit','')}".strip(),
            f"{w.get('source_ref','')[:70]} :: {w.get('source_table','')[:90]}")


def exposure(rows):
    if not rows: return "", "", ""
    w = max(rows, key=grade)
    d = f"{w.get('dose_or_conc_value','')} {w.get('dose_or_conc_unit','')}".strip()
    return d, w.get("exposure_duration", ""), w.get("system_model", "")


def main():
    oligos, ocols, mcols, meas = load()
    cols = enriched_columns(ocols, mcols)

    buckets = collections.defaultdict(list)
    for m in meas:
        sc = m.get("subject_class") or ""
        if sc in HUMAN_CLINICAL:   buckets["human_clinical"].append(m)
        elif sc in HUMAN_LAB:      buckets["human_lab"].append(m)
        elif sc.startswith("animal"): buckets["animal"].append(m)
        else:                      buckets["unresolved"].append(m)

    hc, hl = buckets["human_clinical"], buckets["human_lab"]
    an, un = buckets["animal"], buckets["unresolved"]
    human = hc + hl

    print("\nEVIDENCE VIEWS (human first)")
    write("measurements_human_clinical.csv", cols, enrich(hc, oligos, cols))
    write("measurements_human_lab.csv", cols, enrich(hl, oligos, cols))
    write("measurements_human.csv", cols, enrich(human, oligos, cols))
    write("measurements_unresolved.csv", cols, enrich(un, oligos, cols))
    write("measurements_animal.csv", cols, enrich(an, oligos, cols))

    # ---- cross-species bridge ------------------------------------------------
    # Kept because the challenge explicitly prioritises extrapolation between
    # human in vitro systems and animal data. The single-number
    # `grade_gap_animal_minus_human` it used to publish is GONE: it differenced
    # mean ordinal grades measured at unrelated doses, durations and endpoints,
    # and read as a translational statistic while establishing nothing. Each
    # side now shows its own worst finding WITH its exposure, and every row
    # carries an explicit statement of whether the comparison is qualified.
    bh, ba = collections.defaultdict(list), collections.defaultdict(list)
    for m in human: bh[m["oligo_id"]].append(m)
    for m in an:    ba[m["oligo_id"]].append(m)
    bridge = sorted(set(bh) & set(ba), key=lambda k: -(len(bh[k]) + len(ba[k])))

    bcols = ["oligo_id", "oligo_name", "oligo_class", "backbone_chemistry", "ps_count",
             "conjugate", "sequence_5to3", "n_human_clinical_rows", "n_human_lab_rows",
             "human_max_grade", "human_grade_histogram", "human_worst_finding",
             "human_worst_dose", "human_worst_duration", "human_system",
             "n_animal_rows", "animal_max_grade", "animal_grade_histogram",
             "animal_worst_finding", "animal_worst_dose", "animal_worst_duration",
             "animal_species", "exposure_comparable", "interpretation_limit"]
    brows = []
    for oid in bridge:
        o = oligos.get(oid, {})
        H, A = bh[oid], ba[oid]
        hd, hdur, hsys = exposure(H)
        ad, adur, _ = exposure(A)
        comparable = "no" if not (hd and ad) else "unknown"
        why = ("dose or duration missing on at least one side"
               if comparable == "no" else
               "endpoint, dose and duration not verified as matched across species")
        brows.append({
            "oligo_id": oid, "oligo_name": o.get("oligo_name", "?"),
            "oligo_class": o.get("oligo_class", ""),
            "backbone_chemistry": o.get("backbone_chemistry", ""),
            "ps_count": o.get("ps_count", ""), "conjugate": o.get("conjugate", ""),
            "sequence_5to3": o.get("sequence_5to3", "TBD"),
            "n_human_clinical_rows": sum(1 for r in H if r["subject_class"] in HUMAN_CLINICAL),
            "n_human_lab_rows": sum(1 for r in H if r["subject_class"] in HUMAN_LAB),
            "human_max_grade": max(grade(r) for r in H), "human_grade_histogram": hist(H),
            "human_worst_finding": worst(H)[0], "human_worst_dose": hd,
            "human_worst_duration": hdur, "human_system": hsys,
            "n_animal_rows": len(A), "animal_max_grade": max(grade(r) for r in A),
            "animal_grade_histogram": hist(A), "animal_worst_finding": worst(A)[0],
            "animal_worst_dose": ad, "animal_worst_duration": adur,
            "animal_species": ";".join(sorted({r.get("species", "") for r in A})),
            "exposure_comparable": comparable, "interpretation_limit": why})
    write("bridge_human_animal.csv", bcols, brows)

    # ---- German's analysis ---------------------------------------------------
    # One row per compound: the oligo, its sequence, the modification to that
    # sequence, and the toxicity. RANKED ON HUMAN EVIDENCE ONLY. Animal columns
    # are present and clearly suffixed, but never enter the sort key, and any
    # compound with no human evidence sorts below every compound that has some.
    by_o = collections.defaultdict(list)
    for m in meas: by_o[m["oligo_id"]].append(m)

    gcols = ["rank", "oligo_name", "sequence_5to3", "modification_summary", "modification_map",
             "modification_map_notation", "gapmer_design", "sugar_modifications",
             "backbone_chemistry", "ps_count", "conjugate", "length_nt", "oligo_class",
             "target_gene", "has_human_evidence", "human_clinical_max_grade",
             "human_clinical_grade_histogram", "n_human_clinical",
             "human_lab_max_grade", "human_lab_grade_histogram", "n_human_lab",
             "worst_human_finding", "worst_human_locus", "evidence_class",
             "scientist_disposition", "clinical_model_eligibility",
             "mechanistic_model_eligibility", "exact_sequence_group",
             "APPENDIX_animal_max_grade", "APPENDIX_animal_grade_histogram",
             "APPENDIX_n_animal", "APPENDIX_worst_animal_finding"]
    grows = []
    for oid, rows in by_o.items():
        o = oligos.get(oid, {})
        C = [r for r in rows if r.get("subject_class") in HUMAN_CLINICAL]
        L = [r for r in rows if r.get("subject_class") in HUMAN_LAB]
        A = [r for r in rows if (r.get("subject_class") or "").startswith("animal")]
        parts = []
        for k, fmt in (("gapmer_design", "{}"), ("sugar_modifications", "{}"),
                       ("backbone_chemistry", "{}"), ("ps_count", "{} PS"),
                       ("conjugate", "{}-conjugated")):
            v = o.get(k, "")
            if v not in ("", "TBD", "NA") and not (k == "conjugate" and v == "none"):
                parts.append(fmt.format(v.replace(";", "+")))
        ev = "+".join(x for x, ok in (("clinical", C), ("human_lab", L), ("animal", A)) if ok) or "none"
        wf, wl = worst(C or L)
        grows.append({
            "oligo_name": o.get("oligo_name", "?"),
            "sequence_5to3": o.get("sequence_5to3", "TBD"),
            "modification_summary": " · ".join(parts) if parts else "TBD",
            "modification_map": o.get("modification_map", "TBD"),
            "modification_map_notation": o.get("modification_map_notation", ""),
            "gapmer_design": o.get("gapmer_design", ""),
            "sugar_modifications": o.get("sugar_modifications", ""),
            "backbone_chemistry": o.get("backbone_chemistry", ""),
            "ps_count": o.get("ps_count", ""), "conjugate": o.get("conjugate", ""),
            "length_nt": o.get("length_nt", ""), "oligo_class": o.get("oligo_class", ""),
            "target_gene": o.get("target_gene", ""),
            "has_human_evidence": "yes" if (C or L) else "no",
            "human_clinical_max_grade": (max(grade(r) for r in C) if C else ""),
            "human_clinical_grade_histogram": hist(C) if C else "",
            "n_human_clinical": len(C),
            "human_lab_max_grade": (max(grade(r) for r in L) if L else ""),
            "human_lab_grade_histogram": hist(L) if L else "",
            "n_human_lab": len(L),
            "worst_human_finding": wf, "worst_human_locus": wl,
            "evidence_class": ev,
            "scientist_disposition": o.get("scientist_disposition", ""),
            "clinical_model_eligibility": o.get("clinical_model_eligibility", ""),
            "mechanistic_model_eligibility": o.get("mechanistic_model_eligibility", ""),
            "exact_sequence_group": o.get("exact_sequence_group", ""),
            "APPENDIX_animal_max_grade": (max(grade(r) for r in A) if A else ""),
            "APPENDIX_animal_grade_histogram": hist(A) if A else "",
            "APPENDIX_n_animal": len(A),
            "APPENDIX_worst_animal_finding": worst(A)[0] if A else ""})

    # HUMAN-ONLY sort key. Compounds with no human evidence go last, and nothing
    # about their animal data can lift them.
    def key(r):
        has = r["has_human_evidence"] == "yes"
        return (0 if has else 1,
                -(int(r["human_clinical_max_grade"]) if r["human_clinical_max_grade"] != "" else -1),
                -r["n_human_clinical"],
                -(int(r["human_lab_max_grade"]) if r["human_lab_max_grade"] != "" else -1),
                -r["n_human_lab"], r["oligo_name"].lower())
    grows.sort(key=key)
    for i, r in enumerate(grows, 1): r["rank"] = i
    write("germans_analysis.csv", gcols, grows)

    # ---- coverage and limitations -------------------------------------------
    nseq = sum(1 for o in oligos.values() if o.get("sequence_5to3") not in ("", "TBD", "NA"))
    nmap = sum(1 for o in oligos.values() if o.get("modification_map") not in ("", "TBD"))
    npur = sum(1 for o in oligos.values() if o.get("purity_pct") not in ("", "TBD"))
    elig = sum(1 for o in oligos.values() if o.get("clinical_model_eligibility") not in ("NO", ""))
    mech = sum(1 for o in oligos.values() if o.get("mechanistic_model_eligibility") == "YES")
    lim = [
        ("human clinical outcome records", len(hc),
         "OUTCOME RECORDS, NOT TRIALS. Many are dose-band cells of one pooled table. "
         "See data/studies.csv for the trial-grain count."),
        ("human laboratory / ex vivo records", len(hl),
         "Human in vitro and ex vivo platelet systems. Not clinical trials; directly "
         "relevant to the challenge's stated in-vitro-human priority."),
        ("animal records (appendix)", len(an),
         "Supporting evidence only. Excluded from every human count, label and ranking."),
        ("unresolved records", len(un),
         "Species or subject class not established. Assigned to neither side."),
        ("compounds", len(oligos), "Compound records, not trials."),
        ("compounds with a sequence", nseq, f"{len(oligos)-nseq} carry TBD."),
        ("compounds with a per-residue modification map", nmap,
         f"{len(oligos)-nmap} carry TBD. Location of chemical modifications is a Phase 2 requirement."),
        ("compounds with a purity value", npur,
         "Purity is NOT REPORTED in the sources curated so far, including the "
         "scientist-governed package. Recorded as TBD, never inferred."),
        ("compounds scientist-eligible for clinical modelling", elig,
         "PROVISIONAL in every case. All other compounds are model-ineligible by default."),
        ("compounds scientist-eligible for mechanistic modelling", mech,
         "Per the scientist-governed package v0.9 training manifest."),
        ("qualified clinical negatives", 0,
         "The scientist package rules CLEAN_CLINICAL_NEGATIVE 'NOT YET AVAILABLE'. "
         "Absence of a reported platelet event is NOT a measured negative."),
    ]
    write("coverage_and_limitations.csv", ["item", "count", "limitation"],
          [{"item": a, "count": b, "limitation": c} for a, b, c in lim])

    print(f"\n  human clinical {len(hc):>5} rows · {len({m['oligo_id'] for m in hc})} compounds")
    print(f"  human lab      {len(hl):>5} rows · {len({m['oligo_id'] for m in hl})} compounds")
    print(f"  animal         {len(an):>5} rows · {len({m['oligo_id'] for m in an})} compounds (appendix)")
    print(f"  unresolved     {len(un):>5} rows")
    print(f"  bridge         {len(brows):>5} compounds with both sides")
    nh = sum(1 for r in grows if r["has_human_evidence"] == "yes")
    print(f"  German's analysis: {len(grows)} compounds, {nh} with human evidence (ranked first), "
          f"{len(grows)-nh} animal-only (ranked last)")
    print(f"  top 3 by human evidence: " +
          ", ".join(f"{r['oligo_name']}(g{r['human_clinical_max_grade'] or r['human_lab_max_grade']})"
                    for r in grows[:3]))


if __name__ == "__main__":
    main()
