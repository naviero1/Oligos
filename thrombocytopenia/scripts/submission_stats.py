#!/usr/bin/env python3
"""Compute every number quoted in the submission documents, from the data.

The narrative, methodology and PADP quote dozens of counts. Hand-maintaining them
guarantees drift: a stale table looks exactly like a fresh one, and the documents
had already gone out of date once within a single working session. So the HTML
sources carry {{placeholders}} and this module supplies the values, making it
impossible to ship a document whose numbers disagree with the dataset it describes.

Usage:  python3 scripts/submission_stats.py        # print the resolved values
        (imported by render_submission.py)
"""
import csv, json, os, collections, statistics

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")


def _read(name):
    with open(os.path.join(BASE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt(n):
    return f"{n:,}"


def stats():
    o, m = _read("oligos.csv"), _read("measurements.csv")
    bridge = _read("bridge_human_animal.csv")
    C = lambda k, rows=m: collections.Counter(r[k] for r in rows)
    sc = C("subject_class")
    st = C("study_type")
    rc = C("readout_category")
    rd = C("redistribution")
    oc = collections.Counter(r["oligo_class"] for r in o)
    bb = collections.Counter(r["backbone_chemistry"] for r in o)
    cj = collections.Counter(r["conjugate"] for r in o)

    human = sum(v for k, v in sc.items() if k.startswith("human"))
    animal = sum(v for k, v in sc.items() if k.startswith("animal"))
    hcomp = len({r["oligo_id"] for r in m if r["subject_class"].startswith("human")})
    acomp = len({r["oligo_id"] for r in m if r["subject_class"].startswith("animal")})

    # mean grade by backbone and by PS-count band, excluding the mechanism-confounded
    # compound — the same exclusion analyze_thrombo.py applies and for the same reason
    excl = {"imetelstat"}
    oid_name = {r["oligo_id"]: r["oligo_name"].lower() for r in o}
    odesign = {r["oligo_id"]: r for r in o}
    keep = [r for r in m if oid_name.get(r["oligo_id"], "") not in excl]

    def mg(rows):
        g = [int(r["thrombocytopenia_grade"]) for r in rows]
        return statistics.mean(g) if g else float("nan")

    bb_rows = collections.defaultdict(list)
    for r in keep:
        bb_rows[odesign.get(r["oligo_id"], {}).get("backbone_chemistry", "TBD")].append(r)

    def psband(lo, hi):
        out = []
        for r in keep:
            v = odesign.get(r["oligo_id"], {}).get("ps_count", "")
            try:
                p = float(v)
            except (TypeError, ValueError):
                continue
            if lo <= p <= hi:
                out.append(r)
        return out

    d = {
        "n_meas": fmt(len(m)), "n_oligos": fmt(len(o)),
        "n_sources": fmt(len({r["source_ref"] for r in m})),
        "n_targets": fmt(len({r["target_gene"] for r in o
                              if r["target_gene"] not in ("", "TBD", "NA")})),
        "n_seq": fmt(sum(1 for r in o if r["sequence_5to3"] not in ("", "TBD", "NA"))),
        "pct_seq": f"{100*sum(1 for r in o if r['sequence_5to3'] not in ('','TBD','NA'))//len(o)}",
        "n_verified": fmt(sum(1 for r in m if "verified_against_source" in r["notes"])),
        "pct_verified": f"{100*sum(1 for r in m if 'verified_against_source' in r['notes'])//len(m)}",
        "n_human": fmt(human), "n_animal": fmt(animal),
        "n_neither": fmt(len(m) - human - animal),
        "n_human_comp": fmt(hcomp), "n_animal_comp": fmt(acomp),
        "n_bridge": fmt(len(bridge)),
        "g0": fmt(C("thrombocytopenia_grade")["0"]), "g1": fmt(C("thrombocytopenia_grade")["1"]),
        "g2": fmt(C("thrombocytopenia_grade")["2"]), "g3": fmt(C("thrombocytopenia_grade")["3"]),
        "st_clinical": fmt(st["clinical"]), "st_invitro": fmt(st["in_vitro"]),
        "st_animal": fmt(st["animal_invivo"]), "st_exvivo": fmt(st["ex_vivo"]),
        "hc_clinical": fmt(sc["human_clinical"]), "hc_invitro": fmt(sc["human_in_vitro"]),
        "hc_exvivo": fmt(sc["human_ex_vivo"]),
        "ac_invivo": fmt(sc["animal_in_vivo"]), "ac_invitro": fmt(sc["animal_in_vitro"]),
        "ac_exvivo": fmt(sc["animal_ex_vivo"]),
        "rc_count": fmt(rc["platelet_count"]), "rc_clinical": fmt(rc["clinical_outcome"]),
        "rc_activation": fmt(rc["platelet_activation"]),
        "rc_bindagg": fmt(rc["platelet_binding"] + rc["platelet_aggregation"]),
        "rc_immuno": fmt(rc["immunogenicity"]),
        "rc_other": fmt(rc["megakaryocyte"] + rc["histopathology"] + rc["viability"] + rc["coagulation"]),
        "rd_public": fmt(rd["public_domain"]), "rd_ccby": fmt(rd["cc_by"]),
        "rd_summary": fmt(rd["summary_stat"] + rd["derived_features_only"]),
        "oc_gapmer": fmt(oc["ASO_gapmer"]), "oc_other": fmt(oc["other"]),
        "oc_pmo": fmt(oc["PMO"]), "oc_aptamer": fmt(oc["aptamer"]),
        "oc_sso": fmt(oc["splice_switching_ASO"]),
        "oc_sirna": fmt(oc["siRNA"] + oc["GalNAc_siRNA"]),
        "bb_fullps": fmt(bb["full_PS"]), "bb_mix": fmt(bb["PS_PO_mix"]),
        "bb_fullpo": fmt(bb["full_PO"]), "bb_pmo": fmt(bb["PMO_neutral"]),
        "bb_tbd": fmt(bb["TBD"]), "bb_other": fmt(bb["mixed"] + bb["NA"]),
        "cj_none": fmt(cj["none"]), "cj_galnac": fmt(cj["GalNAc"]),
        "cj_lipid": fmt(cj["lipid"]), "cj_peg": fmt(cj["PEG"] + cj["other"]),
        "cj_tbd": fmt(cj["TBD"]),
        "n_gapmer_design": fmt(sum(1 for r in o if r["gapmer_design"] not in ("", "TBD", "NA"))),
        "n_sugar": fmt(sum(1 for r in o if r["sugar_modifications"] not in ("", "TBD", "NA"))),
        "n_pscount": fmt(sum(1 for r in o if r["ps_count"] not in ("", "TBD", "NA"))),
    }
    for key, rows in (("mg_pmo", bb_rows.get("PMO_neutral", [])),
                      ("mg_mix", bb_rows.get("PS_PO_mix", [])),
                      ("mg_po", bb_rows.get("full_PO", [])),
                      ("mg_ps", bb_rows.get("full_PS", []))):
        d[key] = f"{mg(rows):.2f}"
        d["n" + key[2:]] = fmt(len(rows))
        d["c" + key[2:]] = fmt(len({r["oligo_id"] for r in rows}))
    for key, band in (("ps0", (0, 0)), ("ps13", (13, 16)), ("ps17", (17, 19)), ("ps20", (20, 99))):
        d["mg_" + key] = f"{mg(psband(*band)):.2f}"

    ml_path = os.path.join(BASE, "model_demo_results.json")
    if os.path.exists(ml_path):
        ml = json.load(open(ml_path, encoding="utf-8"))
        d["ml_rows"] = fmt(ml["n_rows"])
        d["ml_comp"] = fmt(ml["n_compounds"])
        ga = ml.get("grouped_auc", {})
        d["ml_design"] = f"{ga.get('design:RandomForest', 0):.3f}"
        d["ml_context"] = f"{ga.get('RandomForest', 0):.3f}"
        d["ml_gap"] = f"{ga.get('RandomForest', 0) - ga.get('design:RandomForest', 0):+.3f}"
        d["ml_top"] = ml["top_features"][0]["feature"] if ml.get("top_features") else "ps_count"
    for b in bridge[:3]:
        i = bridge.index(b) + 1
        d[f"bridge{i}_name"] = b["oligo_name"]
        d[f"bridge{i}_h"] = b["n_human_rows"]
        d[f"bridge{i}_a"] = b["n_animal_rows"]
    return d


if __name__ == "__main__":
    for k, v in sorted(stats().items()):
        print(f"  {k:<18} {v}")
