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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "scripts"))
from data_dictionary import DICTIONARY
from assemble import subject_class_for, SUBJECT_CLASSES

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
    mods = load("modifications.csv")

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

    # 11b-2 human / animal division ----------------------------------------
    bad = sorted({r["subject_class"] for r in m if r["subject_class"] not in SUBJECT_CLASSES})
    check("vocabulary: subject_class", not bad, "unexpected: %s" % bad)

    mismatched = [r["measurement_id"] for r in m
                  if r["subject_class"] != subject_class_for(r["species"], r["study_type"])]
    check("subject_class re-derives from (species, study_type)", not mismatched,
          "%d rows disagree e.g. %s" % (len(mismatched), mismatched[:5]))

    bad = [r["measurement_id"] for r in m
           if (r["subject_class"].startswith("human")) != (r["is_human_system"] == "TRUE")
           and r["subject_class"] != "human_population"]
    check("subject_class agrees with is_human_system", not bad,
          "offending: %s" % bad[:5])

    for fname, pred in (("measurements_human.csv",
                         lambda r: r["subject_class"].startswith("human")),
                        ("measurements_animal.csv",
                         lambda r: r["subject_class"].startswith("animal"))):
        view = load(fname)
        expect = [r["measurement_id"] for r in m if pred(r)]
        got = [r["measurement_id"] for r in view]
        check("split view %s matches the canonical table" % fname, expect == got,
              "%d expected vs %d present" % (len(expect), len(got)))

    # 11c per-position modifications table ---------------------------------
    oid = {r["oligo_id"] for r in o}
    bad = sorted({r["oligo_id"] for r in mods if r["oligo_id"] not in oid})
    check("FK modifications.oligo_id -> oligos", not bad, "orphans: %s" % bad[:4])

    by_oligo = collections.defaultdict(list)
    for r in mods:
        by_oligo[r["oligo_id"]].append(int(r["position_5to3"]))
    bad = [k for k, v_ in by_oligo.items() if sorted(v_) != list(range(1, len(v_) + 1))]
    check("modifications positions are contiguous 1..n", not bad,
          "offending oligo_ids: %s" % bad[:4])

    lengths = {r["oligo_id"]: r["length_nt"] for r in o}
    bad = ["%s: %d rows vs length_nt=%s" % (k, len(v_), lengths.get(k))
           for k, v_ in by_oligo.items() if lengths.get(k) != str(len(v_))]
    check("modifications row count equals oligos.length_nt", not bad, "; ".join(bad[:4]))

    allowed_base = {"A", "C", "G", "T", "U", "NOT_REPORTED"}
    bad = sorted({r["nucleobase"] for r in mods if r["nucleobase"] not in allowed_base})
    check("vocabulary: modifications.nucleobase", not bad, "unexpected: %s" % bad[:6])

    allowed_sugar = {"2'-MOE", "DNA_2prime_deoxy", "LNA", "morpholino", "2'-OMe",
                     "2'-F", "RNA_2prime_OH", "NOT_REPORTED"}
    bad = sorted({r["sugar_chemistry"] for r in mods
                  if r["sugar_chemistry"] not in allowed_sugar})
    check("vocabulary: modifications.sugar_chemistry", not bad, "unexpected: %s" % bad[:6])

    bad = [r["oligo_id"] for r in mods if not r["basis"].strip()
           or not r["source_location"].strip()]
    check("every modification position states its basis and locus", not bad,
          "offending: %s" % bad[:4])

    # A sequenced oligo's modification bases must reproduce its stored sequence.
    seqs = {r["oligo_id"]: r["sequence_5to3_asprinted"] for r in o}
    bad = []
    built_by = collections.defaultdict(list)
    for r in sorted((x for x in mods if x["nucleobase"] != "NOT_REPORTED"),
                    key=lambda x: (x["oligo_id"], int(x["position_5to3"]))):
        built_by[r["oligo_id"]].append(r["nucleobase"])
    for k, bases in built_by.items():
        built = "".join(bases)
        if seqs.get(k) not in (None, "NOT_REPORTED", "NOT_APPLICABLE") and built != seqs[k]:
            bad.append("%s: %s vs %s" % (k, built, seqs[k]))
    check("modifications bases reproduce oligos.sequence_5to3_asprinted", not bad,
          "; ".join(bad[:3]))

    # 11d the data dictionary covers every column, and only real columns ----
    #     This is the check whose absence let SCHEMA.md promise purity_pct,
    #     purity_method and identity_confirmation while the builder emitted none.
    tables = {"oligos": o, "measurements": m, "modifications": mods, "sources": s}
    undocumented, phantom = [], []
    for tname, rows_ in tables.items():
        actual = set(rows_[0].keys())
        documented = set(DICTIONARY.get(tname, {}))
        undocumented += ["%s.%s" % (tname, c) for c in sorted(actual - documented)]
        phantom += ["%s.%s" % (tname, c) for c in sorted(documented - actual)]
    check("every column has a data-dictionary entry", not undocumented,
          "undocumented: %s" % undocumented[:8])
    check("data dictionary documents no column that does not exist", not phantom,
          "phantom: %s" % phantom[:8])

    # 11e endpoint isolation — no other toxicity's material may leak in ----
    #     Requested explicitly: the endpoints are separate deliverables and their
    #     files must not mix. This makes that a check rather than a convention.
    # Word-boundary anchored. An earlier version used bare substrings and matched
    # "de-LIVER-y_procedure_complication" and "de-LIVER-y_route" — the check was
    # wrong, not the data.
    FOREIGN = re.compile(r"nephrotox|\bkidney\b|\brenal\b|proximal_tubule|"
                         r"glomerul|hepatotox|\bliver\b|\bALT\b|\bAST\b|"
                         r"thrombocytopen|\bplatelet\b|complement_activation|"
                         r"coagulopath|cns_tox_grade|nephrotox_grade|immunotox|"
                         r"cytokine_release", re.I)
    # Columns that legitimately mention other organs as CONTEXT (a compound's
    # indication, a source's title, free-text notes) are exempt; the graded and
    # categorical columns are not.
    GRADED_COLS = ["readout_category", "readout_name", "tox_axis", "endpoint_tier",
                   "cns_compartment", "hydroceph_grade", "grade_status",
                   "ascertainment", "subject_class"]
    bad = []
    for r in m:
        for c in GRADED_COLS:
            if FOREIGN.search(r.get(c, "")):
                bad.append("%s.%s=%s" % (r["measurement_id"], c, r[c]))
    check("no other endpoint's vocabulary in the graded columns", not bad,
          "%d hits e.g. %s" % (len(bad), bad[:4]))

    foreign_cols = [c for c in m[0] if FOREIGN.search(c)]
    check("no other endpoint's column in measurements", not foreign_cols,
          "columns: %s" % foreign_cols)
    foreign_cols = [c for c in o[0] if FOREIGN.search(c)]
    check("no other endpoint's column in oligos", not foreign_cols,
          "columns: %s" % foreign_cols)

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
        n_modification_positions=len(mods),
        n_oligos_with_position_map=len({r["oligo_id"] for r in mods}),
        n_oligos_with_length=sum(1 for r in o if r["length_nt"] not in
                                 ("NOT_REPORTED", "NOT_APPLICABLE")),
        n_oligos_with_measurements=len({r["oligo_id"] for r in m
                                        if r["oligo_name"] not in
                                        ("NOT_APPLICABLE", "placebo_or_sham_control")}),
        by_subject_class=dist("subject_class"),
        by_subject_class_and_tier=dict(sorted(collections.Counter(
            "%s / tier %s" % (r["subject_class"], r["endpoint_tier"]) for r in m).items())),
        n_human_rows=sum(1 for r in m if r["subject_class"].startswith("human")),
        n_animal_rows=sum(1 for r in m if r["subject_class"].startswith("animal")),
        n_in_vitro_rows=sum(1 for r in m if r["subject_class"].endswith("in_vitro")),
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
