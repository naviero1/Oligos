#!/usr/bin/env python3
"""
Quality-control suite for OligoTox-Hydrocephalus.

Exits non-zero on any failure, so a broken dataset cannot be released quietly.
Also writes qc/stats.json — every count quoted in README.md and METHODOLOGY.md is
read from that file rather than typed, so no document can state a number the data
does not contain.

Usage: python3 qc/validate.py
"""
import collections
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

FAILURES = []
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        FAILURES.append("%s — %s" % (name, detail))


def load(fname):
    with open(os.path.join(DATA, fname)) as fh:
        return list(csv.DictReader(fh))


VOCAB = {
    "study_type": {"clinical_trial", "clinical_case", "pharmacovigilance",
                   "animal_invivo", "in_vitro", "background_epidemiology",
                   "regulatory_label"},
    "endpoint_tier": {"A", "B"},
    "readout_category": {"hydrocephalus_event", "ventricular_morphometry",
                         "shunt_or_drain_intervention", "csf_pressure",
                         "csf_composition", "csf_dynamics", "procedure_complication",
                         "histopathology_choroid_ependyma"},
    "ascertainment": {"measured_positive", "measured_null",
                      "reported_threshold_limited", "not_assessed"},
    "attribution_as_stated": {"drug_attributed", "procedure_attributed",
                              "disease_attributed", "multifactorial", "undetermined",
                              "not_discussed"},
    "tox_axis": {"ventricular_enlargement", "csf_pressure_disturbance",
                 "csf_composition_disturbance", "csf_dynamics",
                 "delivery_procedure_complication", "disease_background_rate",
                 "therapeutic_ventricular_effect"},
    "grade_status": {"provisional", "expert_confirmed", "not_graded"},
    "redistribution": {"public_domain", "cc_by", "cc_by_nc", "summary_stat_only",
                       "derived_features_only", "verify"},
    "effect_direction": {"increase", "decrease", "no_change", "NOT_APPLICABLE"},
    "species": {"human", "mouse", "rat", "monkey", "pig", "multi_species"},
}


def main():
    m = load("measurements.csv")
    o = load("oligos.csv")
    s = load("sources.csv")

    # 1 primary keys ------------------------------------------------------
    for tbl, rows, key in (("measurements", m, "measurement_id"),
                           ("oligos", o, "oligo_id"), ("sources", s, "source_id")):
        ids = [r[key] for r in rows]
        dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
        check("PK unique: %s.%s" % (tbl, key), not dupes, "duplicates: %s" % dupes[:5])
        check("PK non-empty: %s.%s" % (tbl, key), all(ids), "empty key present")

    # 2 referential integrity ---------------------------------------------
    oids, sids = {r["oligo_id"] for r in o}, {r["source_id"] for r in s}
    orphan_o = {r["measurement_id"] for r in m if r["oligo_id"] not in oids}
    orphan_s = {r["measurement_id"] for r in m if r["source_id"] not in sids}
    check("FK measurements.oligo_id -> oligos", not orphan_o,
          "%d orphans e.g. %s" % (len(orphan_o), sorted(orphan_o)[:3]))
    check("FK measurements.source_id -> sources", not orphan_s,
          "%d orphans e.g. %s" % (len(orphan_s), sorted(orphan_s)[:3]))

    # 3 controlled vocabularies -------------------------------------------
    for col, allowed in VOCAB.items():
        bad = sorted({r[col] for r in m if r.get(col) and r[col] not in allowed
                      and r[col] not in ("NOT_REPORTED", "NOT_APPLICABLE")})
        check("vocabulary: %s" % col, not bad, "unexpected values: %s" % bad[:6])

    # 4 grade range --------------------------------------------------------
    bad = [r["measurement_id"] for r in m
           if r["hydroceph_grade"] not in ("", "0", "1", "2", "3")]
    check("hydroceph_grade in {0,1,2,3} or blank", not bad, "offending: %s" % bad[:5])

    # 5 every graded row states its rule -----------------------------------
    bad = [r["measurement_id"] for r in m if r["hydroceph_grade"] != ""
           and len(r["grade_basis"].strip()) < 20]
    check("every graded row has a grade_basis", not bad, "offending: %s" % bad[:5])

    # 6 SCHEMA rule: grade 0 requires ascertainment = measured_null --------
    bad = [r["measurement_id"] for r in m
           if r["hydroceph_grade"] == "0" and r["ascertainment"] != "measured_null"]
    check("grade 0 implies ascertainment=measured_null", not bad,
          "%d rows e.g. %s" % (len(bad), bad[:5]))

    # 7 not_assessed rows must not carry a grade ---------------------------
    bad = [r["measurement_id"] for r in m
           if r["ascertainment"] == "not_assessed" and r["hydroceph_grade"] != ""]
    check("not_assessed rows carry no grade", not bad, "offending: %s" % bad[:5])

    # 8 provenance ---------------------------------------------------------
    bad = [r["measurement_id"] for r in m
           if not r["source_ref"].strip() or not r["source_location"].strip()]
    check("every row has source_ref and source_location", not bad,
          "offending: %s" % bad[:5])
    CATEGORY_WORDS = {"results", "methods", "discussion", "safety", "clinical",
                      "nonclinical", "abstract", "table", "figure"}
    bad = [r["measurement_id"] for r in m
           if r["source_location"].strip().lower() in CATEGORY_WORDS]
    check("source_location is a locus, not a category word", not bad,
          "offending: %s" % bad[:5])

    # 9 numerator <= denominator -------------------------------------------
    bad = []
    for r in m:
        try:
            a, n = int(r["n_affected"]), int(r["n_at_risk"])
        except (ValueError, TypeError):
            continue
        if a > n:
            bad.append(r["measurement_id"])
    check("n_affected <= n_at_risk", not bad, "offending: %s" % bad[:5])

    # 10 no fabricated sequences -------------------------------------------
    filled = [r["oligo_name"] for r in o
              if r["sequence_5to3_asprinted"] not in ("NOT_REPORTED", "NOT_APPLICABLE")
              and r["sequence_source"].startswith("NOT_REPORTED")]
    check("no sequence is filled without a stated source", not filled,
          "offending: %s" % filled[:5])

    # 11 label self-consistency: phosphorus count fixes residue count ------
    #    A 20-mer single strand has 19 internucleoside linkages; the label's
    #    molecular formula P count therefore equals length_nt - 1 for a fully
    #    phosphorylated linear oligo, or length_nt where a terminal phosphate is
    #    present. Checked only where BOTH values are published.
    checked = 0
    bad = []
    for r in o:
        f, L = r["molecular_formula"], r["length_nt"]
        if f in ("NOT_REPORTED", "NOT_APPLICABLE") or L in ("NOT_REPORTED",
                                                            "NOT_APPLICABLE"):
            continue
        mp = re.search(r"P(\d+)", f.replace(" ", ""))
        if not mp:
            continue
        checked += 1
        p, n = int(mp.group(1)), int(L)
        if p not in (n - 1, n):
            bad.append("%s: P%d vs length %d" % (r["oligo_name"], p, n))
    check("label formula P-count agrees with stated length", not bad,
          "checked %d; mismatches %s" % (checked, bad))

    # 11b duplex self-consistency for every published siRNA ----------------
    #     The antisense (guide) strand must be the exact reverse complement of
    #     the sense strand recorded in notes, once TT/dTdT overhangs are trimmed.
    #     This depends on no external source being correct, so it catches a
    #     plausible-but-wrong transcription that two agreeing documents would not.
    comp = {"A": "U", "U": "A", "G": "C", "C": "G", "T": "A"}
    dup_checked, dup_bad = 0, []
    for r in o:
        guide = r["sequence_5to3_asprinted"]
        m2 = re.search(r"sense strand ([ACGUT]+)", r.get("notes", ""))
        if not m2 or guide in ("NOT_REPORTED", "NOT_APPLICABLE"):
            continue
        sense = m2.group(1)
        gcore = guide[:-2] if guide.endswith(("TT", "UU")) else guide
        score = sense[:-2] if sense.endswith(("TT", "UU")) else sense
        rc = "".join(comp.get(b, "?") for b in reversed(score))
        dup_checked += 1
        if rc != gcore:
            dup_bad.append("%s: expected %s got %s" % (r["oligo_name"], rc, gcore))
    check("siRNA duplex guide == reverse complement of sense", not dup_bad,
          "checked %d; mismatches %s" % (dup_checked, dup_bad))

    # 12 background rows carry no compound ---------------------------------
    bad = [r["measurement_id"] for r in m
           if r["tox_axis"] == "disease_background_rate"
           and r["oligo_name"] != "NOT_APPLICABLE"]
    check("disease_background_rate rows carry no compound", not bad,
          "offending: %s" % bad[:5])

    # 13 merged view regenerates -------------------------------------------
    merged = os.path.join(DATA, "hydrocephalus_merged.csv")
    before = open(merged, "rb").read() if os.path.exists(merged) else b""
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "assemble.py")],
                   capture_output=True, check=True)
    after = open(merged, "rb").read()
    check("hydrocephalus_merged.csv regenerates byte-identically", before == after,
          "regeneration changed the file")

    # ---- statistics ------------------------------------------------------
    def dist(col, rows=m):
        return dict(sorted(collections.Counter(r[col] for r in rows).items()))

    clusters = collections.Counter(r["event_cluster_id"] for r in m
                                   if r["event_cluster_id"] != "NOT_APPLICABLE")
    stats = dict(
        n_measurements=len(m), n_oligos=len(o), n_sources=len(s),
        n_oligos_with_measurements=len({r["oligo_id"] for r in m
                                        if r["oligo_name"] not in
                                        ("NOT_APPLICABLE", "placebo_or_sham_control")}),
        by_endpoint_tier=dist("endpoint_tier"),
        by_study_type=dist("study_type"),
        by_ascertainment=dist("ascertainment"),
        by_attribution=dist("attribution_as_stated"),
        by_tox_axis=dist("tox_axis"),
        by_grade=dist("hydroceph_grade"),
        by_delivery_route=dist("delivery_route"),
        by_readout_category=dist("readout_category"),
        by_redistribution=dist("redistribution"),
        by_source_tier=dict(sorted(collections.Counter(
            r["evidence_tier"] for r in s).items())),
        rows_per_source=dict(sorted(
            ((r["source_id"], int(r["n_measurements"])) for r in s),
            key=lambda kv: -kv[1])),
        multi_row_event_clusters={k: v for k, v in clusters.items() if v > 1},
        tier_A_positive=sum(1 for r in m if r["endpoint_tier"] == "A"
                            and r["ascertainment"] == "measured_positive"),
        tier_A_null=sum(1 for r in m if r["endpoint_tier"] == "A"
                        and r["ascertainment"] == "measured_null"),
        grade3_rows=sum(1 for r in m if r["hydroceph_grade"] == "3"),
        duplexes_checked=dup_checked,
        oligos_with_sequence=sum(
            1 for r in o if r["sequence_5to3_asprinted"] not in ("NOT_REPORTED",
                                                                 "NOT_APPLICABLE")),
        checks_run=len(CHECKS), checks_failed=len(FAILURES),
    )
    with open(os.path.join(HERE, "stats.json"), "w") as fh:
        json.dump(stats, fh, indent=2)

    width = max(len(n) for n, _, _ in CHECKS)
    for name, ok, detail in CHECKS:
        print("%s  %-*s %s" % ("PASS" if ok else "FAIL", width, name,
                               "" if ok else detail))
    print("\n%d checks, %d failed" % (len(CHECKS), len(FAILURES)))
    print(json.dumps({k: v for k, v in stats.items()
                      if k.startswith(("n_", "tier_", "grade3", "oligos_"))}, indent=2))
    if FAILURES:
        print("\nFAILURES:\n  " + "\n  ".join(FAILURES))
        sys.exit(1)


if __name__ == "__main__":
    main()
