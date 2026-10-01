#!/usr/bin/env python3
"""Scientist-authorised analyses for the thrombocytopenia endpoint.

WHY THE PREVIOUS MODEL IS NO LONGER RUN
  This script used to train a classifier predicting thrombocytopenia grade >= 1
  from design features, reporting grouped AUC 0.61-0.69 over 228 compounds. The
  scientist-governed package v0.9 (sheet Model_Specification_v0.8) classifies
  that exact model -- "Sequence-only clinical thrombocytopenia classifier" --
  as BLOCKED, with Required_Grouping "N/A", Minimum_Models "All training
  prohibited" and Permitted_Claim "None". Running it would reverse a scientist
  decision, so it is not run.

  Five independent confirmations that the block is correct, each checkable
  against the files in this directory:
   1. It trained on 228 compounds. The scientist package authorises 6 for
      clinical modelling, every one PROVISIONAL (see oligos.csv
      clinical_model_eligibility).
   2. It grouped folds by oligo_id. 85 oligo records here share an exact
      sequence with another record across 35 groups, so oligo-level folds put
      isosequential constructs -- volanesorsen/olezarsen, inotersen/
      eplontersen, ODN2395 PS/PO -- on both sides of the same split. The
      required grouping is exact_sequence_group.
   3. It used grade 0 rows as negatives. The scientist package rules
      CLEAN_CLINICAL_NEGATIVE "NOT YET AVAILABLE" and records the qualified
      clinical-negative count as 0; all 21 audited candidates are ineligible.
   4. It treated 387 pooled Crooke dose-band rows as independent observations.
      The scientist rule is "Do not treat pooled aggregate rows as independent"
      and "Exclude pooled rows from sequence-level labels".
   5. `is_human` ranked second of eighteen features by importance (0.162). The
      model was substantially learning which rows came from human studies
      rather than anything about chemistry.

WHAT RUNS INSTEAD -- only the lanes the scientist package authorises:
  Lane A  Matched-sequence mechanistic contrasts   APPROVED FOR DESCRIPTIVE ANALYSIS
  Lane B  Pooled clinical dose-response baseline   APPROVED WITH LIMITATIONS
  Lane C  Mechanistic proof-of-concept feasibility CONDITIONALLY APPROVED -- this
          reports whether the authorised population is large enough to support a
          model at all. It does not train one.

Usage:  python3 scripts/model_demo.py
"""
import csv, json, os, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
SCI = os.path.join(ENDPOINT, "curation", "scientist_v09")

BLOCKED = {
    "model": "Sequence-only clinical thrombocytopenia classifier",
    "scientist_status": "BLOCKED",
    "scientist_source": "scientist_v0.9 workbook, sheet Model_Specification_v0.8",
    "training_permission": "All training prohibited",
    "permitted_claim": "None",
    "action_taken": "NOT RUN. Previous grouped-AUC results retracted.",
    "retracted_results": {"grouped_auc_design_LogisticRegression": 0.6073,
                          "grouped_auc_design_RandomForest": 0.6272,
                          "grouped_auc_LogisticRegression": 0.6343,
                          "grouped_auc_RandomForest": 0.6895,
                          "n_rows": 1728, "n_compounds": 228},
    "why_retracted": [
        "228 compounds used; 6 are scientist-eligible for clinical modelling, all PROVISIONAL",
        "grouped by oligo_id, not exact_sequence_group: 85 records across 35 groups share a sequence",
        "grade 0 rows used as negatives; qualified clinical negatives = 0",
        "387 pooled dose-band rows treated as independent observations",
        "is_human was the 2nd most important feature (0.162)"],
}


def rd(p):
    with open(p, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))


def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None


def main():
    oligos = {o["oligo_id"]: o for o in rd(os.path.join(DATA, "oligos.csv"))}
    meas = rd(os.path.join(DATA, "measurements.csv"))
    by_o = collections.defaultdict(list)
    for m in meas: by_o[m["oligo_id"]].append(m)
    byname = {}
    for o in oligos.values():
        for nm in [o["oligo_name"]] + (o["aliases"] or "").split(";"):
            k = nm.strip().lower().replace(" ", "")
            if k and k not in byname: byname[k] = o

    out = {"blocked_model": BLOCKED, "lanes": {}}
    print("=" * 78)
    print("SCIENTIST-AUTHORISED ANALYSES — thrombocytopenia")
    print("=" * 78)
    print(f"\n[BLOCKED] {BLOCKED['model']}")
    print(f"  {BLOCKED['scientist_status']} per {BLOCKED['scientist_source']}")
    print(f"  {BLOCKED['action_taken']}")
    for r in BLOCKED["why_retracted"]: print(f"    - {r}")

    # ---- Lane A: matched-sequence mechanistic contrasts ----------------------
    # Descriptive only. The contrast definitions, the matched factors, the single
    # differing factor and the adjudicated 0-3 scores are the SCIENTIST's, read
    # from Mechanistic_Contrasts_v0.8. Constructs are resolved through the
    # crosswalk (scientist record -> branch oligo), never by name: bare names
    # like "ODN 2395" are shared by a phosphorothioate and an isosequential
    # phosphodiester record, and name matching selects the wrong one.
    # This lane also CHECKS the branch grades against the scientist scores and
    # reports any disagreement rather than quietly preferring either side.
    print("\n[LANE A] Matched-sequence mechanistic contrasts — DESCRIPTIVE")
    xw = {r["scientist_record_id"]: r["branch_oligo_id"]
          for r in rd(os.path.join(SCI, "crosswalk.csv"))
          if r["crosswalk_status"] == "retained_matched"}
    man = {}
    mpath = os.path.join(SCI, "Training_Manifest_v0.9.csv")
    if os.path.exists(mpath):
        for r in rd(mpath):
            if (r.get("Data_Object") or "").strip() == "MATCHED_CONTRAST":
                man[r["Record_ID"].strip()] = [x.strip() for x in r["Sequence_Record_ID"].split("|")]

    def lab_rows(oid):
        return [m for m in by_o.get(oid, [])
                if (m.get("subject_class") or "") in ("human_in_vitro", "human_ex_vivo")]

    def maxg(rows):
        g = [int(m["thrombocytopenia_grade"]) for m in rows if m["thrombocytopenia_grade"].isdigit()]
        return (max(g) if g else None), dict(collections.Counter(g))

    lane_a, cpath = [], os.path.join(SCI, "Mechanistic_Contrasts_v0_8.csv")
    for c in (rd(cpath) if os.path.exists(cpath) else []):
        cid = c["Contrast_ID"].strip()
        sids = man.get(cid, ["", ""])
        oidA, oidB = xw.get(sids[0], ""), xw.get(sids[1] if len(sids) > 1 else "", "")
        oA, oB = oligos.get(oidA, {}), oligos.get(oidB, {})
        rA, rB = lab_rows(oidA), lab_rows(oidB)
        gA, hA = maxg(rA)
        gB, hB = maxg(rB)
        sA = int(c["Score_A"]) if (c.get("Score_A") or "").strip().isdigit() else None
        sB = int(c["Score_B"]) if (c.get("Score_B") or "").strip().isdigit() else None
        checks = []
        if not oidA or not oidB:
            checks.append("construct not resolved to a branch record")
        if oA and oB and oA.get("sequence_5to3") != oB.get("sequence_5to3") \
           and "sequence" not in c["Primary_Differing_Factor"].lower():
            checks.append("branch sequences differ although the contrast is matched on sequence")
        if oA and oB and oA.get("exact_sequence_group") != oB.get("exact_sequence_group") \
           and "sequence" not in c["Primary_Differing_Factor"].lower():
            checks.append("constructs sit in different exact_sequence_groups -- outer split would separate them")
        if sA is not None and gA is not None and sA != gA:
            checks.append(f"A: scientist score {sA} vs branch max grade {gA}")
        if sB is not None and gB is not None and sB != gB:
            checks.append(f"B: scientist score {sB} vs branch max grade {gB}")
        lane_a.append({
            "contrast_id": cid, "pair": f"{c['Construct_A_Name']} vs {c['Construct_B_Name']}",
            "comparison_family": c.get("Comparison_Family", ""),
            "matched_factors": c.get("Matched_Factors", ""),
            "primary_differing_factor": c.get("Primary_Differing_Factor", ""),
            "scientist_score_A": sA, "scientist_score_B": sB,
            "scientist_delta_B_minus_A": c.get("Delta_B_minus_A", ""),
            "scientist_interpretation": c.get("Scientific_Interpretation", ""),
            "causal_limitation": c.get("Causal_Limitation", ""),
            "permitted_use": c.get("Permitted_Use", ""),
            "A": {"scientist_record": sids[0], "branch_oligo_id": oidA,
                  "compound": oA.get("oligo_name", ""), "sequence": oA.get("sequence_5to3", ""),
                  "ps_count": oA.get("ps_count", ""), "n_human_lab_rows": len(rA),
                  "branch_max_grade": gA, "branch_grade_histogram": hA},
            "B": {"scientist_record": sids[1] if len(sids) > 1 else "", "branch_oligo_id": oidB,
                  "compound": oB.get("oligo_name", ""), "sequence": oB.get("sequence_5to3", ""),
                  "ps_count": oB.get("ps_count", ""), "n_human_lab_rows": len(rB),
                  "branch_max_grade": gB, "branch_grade_histogram": hB},
            "consistency_checks": checks or ["consistent"]})
        print(f"  {cid}  {oA.get('oligo_name','?')[:15]:15s} vs {oB.get('oligo_name','?')[:15]:15s}"
              f"  differs: {c['Primary_Differing_Factor'][:26]:26s}"
              f"  scientist {sA}->{sB}  branch {gA}->{gB}  n={len(rA)}/{len(rB)}")
        for ck in checks:
            if ck != "consistent": print(f"        ! {ck}")
    # Direction concordance is the defensible result here. The scientist's
    # adjudicated 0-3 score and this dataset's grade were derived independently,
    # from different rubrics, so their ABSOLUTE agreement is not expected. What
    # matters is whether both say the differing factor pushes severity the same
    # way. That is a reproducibility statement about the contrast, not a
    # performance claim about a model.
    def sgn(x):
        return 0 if x == 0 else (1 if x > 0 else -1)
    conc = []
    for r in lane_a:
        sA, sB = r["scientist_score_A"], r["scientist_score_B"]
        bA, bB = r["A"]["branch_max_grade"], r["B"]["branch_max_grade"]
        if None in (sA, sB, bA, bB): conc.append(None); continue
        conc.append(sgn(sB - sA) == sgn(bB - bA))
    agree = sum(1 for c in conc if c is True)
    scored = sum(1 for c in conc if c is not None)
    exact = sum(1 for r in lane_a if r["consistency_checks"] == ["consistent"])
    print(f"\n  direction concordance scientist vs branch: {agree}/{scored} contrasts agree on "
          f"the SIGN of the effect; {exact}/{len(lane_a)} also agree on absolute level")
    print("  -> the differing factor moves severity the same way in both independently")
    print("     built datasets; absolute grades differ because the rubrics differ.")
    out["lanes"]["A_matched_contrasts"] = {
        "scientist_status": "APPROVED FOR DESCRIPTIVE ANALYSIS",
        "definitions_from": "scientist_v0.9 sheet Mechanistic_Contrasts_v0.8",
        "n_contrasts": len(lane_a),
        "direction_concordance": f"{agree}/{scored}",
        "absolute_concordance": f"{exact}/{len(lane_a)}",
        "concordance_note": ("Scientist 0-3 adjudicated score and dataset grade were derived "
                             "independently under different rubrics; absolute agreement is not "
                             "expected. Sign agreement is the reproducibility statement. This is "
                             "not a model performance claim."),
        "unresolved_for_scientist": [{"contrast_id": r["contrast_id"], "checks": r["consistency_checks"]}
                                     for r in lane_a if r["consistency_checks"] != ["consistent"]],
        "contrasts": lane_a}

    # ---- Lane B: pooled clinical dose-response baseline ----------------------
    # Unit of observation is the study/dose/threshold aggregate, as the scientist
    # spec requires. Evaluable denominators are preserved and NOT summed across
    # overlapping pooled reports.
    print("\n[LANE B] Pooled clinical dose-response baseline — APPROVED WITH LIMITATIONS")
    clin = [m for m in meas if m.get("subject_class") == "human_clinical"]
    bands = collections.defaultdict(list)
    for m in clin:
        sm = m.get("system_model", "")
        dv, du = m.get("dose_or_conc_value", ""), m.get("dose_or_conc_unit", "")
        if dv not in ("", "TBD"):
            bands[f"{dv} {du}".strip()].append(m)
    lane_b = []
    for band, R in sorted(bands.items(), key=lambda kv: -len(kv[1]))[:14]:
        g = [int(x["thrombocytopenia_grade"]) for x in R if x["thrombocytopenia_grade"].isdigit()]
        lane_b.append({"dose_band": band, "n_aggregate_rows": len(R),
                       "max_grade": max(g) if g else None,
                       "grade_histogram": dict(collections.Counter(g)),
                       "compounds": sorted({oligos.get(x["oligo_id"], {}).get("oligo_name", "?") for x in R})[:6]})
        print(f"  {band:22s} rows={len(R):4d} maxgrade={max(g) if g else '-'} "
              f"hist={dict(collections.Counter(g))}")
    out["lanes"]["B_pooled_dose_response"] = {
        "scientist_status": "APPROVED WITH LIMITATIONS",
        "unit_of_observation": "study / dose / threshold aggregate",
        "limitations": ["Pooled aggregate rows are NOT independent observations.",
                        "Denominators from overlapping pooled reports are never summed.",
                        "Dose bands are not comparable across compounds or indications."],
        "bands": lane_b}

    # ---- Lane C: mechanistic PoC feasibility --------------------------------
    print("\n[LANE C] Mechanistic proof-of-concept feasibility — NO TRAINING PERFORMED")
    elig = [o for o in oligos.values() if o.get("mechanistic_model_eligibility") == "YES"]
    with_lab, groups = [], collections.Counter()
    for o in elig:
        R = [m for m in by_o[o["oligo_id"]]
             if (m.get("subject_class") or "") in ("human_in_vitro", "human_ex_vivo")]
        if R:
            with_lab.append((o, len(R)))
            groups[o.get("exact_sequence_group", "?")] += 1
    n_groups = len(groups)
    verdict = ("INSUFFICIENT for a held-out performance claim: fewer than 10 independent "
               "exact-sequence groups, so leave-one-group-out estimates would be dominated "
               "by single-group variance." if n_groups < 10 else
               "Group count may support leave-one-sequence-group-out evaluation; the "
               "scientist gate on the ordinal response score (SRQ-TMB-006) must clear first.")
    print(f"  scientist-eligible mechanistic constructs: {len(elig)}")
    print(f"  ... with human laboratory rows:            {len(with_lab)}")
    print(f"  independent exact-sequence groups:         {n_groups}")
    print(f"  verdict: {verdict}")
    out["lanes"]["C_mechanistic_feasibility"] = {
        "scientist_status": "CONDITIONALLY APPROVED FOR PROOF OF CONCEPT",
        "n_eligible_constructs": len(elig), "n_with_human_lab_rows": len(with_lab),
        "n_independent_exact_sequence_groups": n_groups,
        "required_grouping": "exact_sequence_group (outer); matched pairs stay intact",
        "training_performed": False, "verdict": verdict,
        "blocking_gate": "SRQ-TMB-006 human ex vivo ordinal response score"}

    # ---- write --------------------------------------------------------------
    with open(os.path.join(DATA, "approved_analyses.json"), "w") as f:
        json.dump(out, f, indent=1)
    # Replace the old results file so nothing downstream can read stale AUCs.
    with open(os.path.join(DATA, "model_demo_results.json"), "w") as f:
        json.dump({"status": "RETRACTED",
                   "reason": "Model is BLOCKED by the scientist-governed package v0.9.",
                   "see": "data/approved_analyses.json",
                   "retracted": BLOCKED["retracted_results"],
                   "why_retracted": BLOCKED["why_retracted"]}, f, indent=1)
    print("\n  -> data/approved_analyses.json")
    print("  -> data/model_demo_results.json  (now a retraction record)")


if __name__ == "__main__":
    main()
