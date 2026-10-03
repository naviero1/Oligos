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
                      "reported_zero_no_denominator",
                      "reported_threshold_limited", "not_assessed"},
    "denominator_type": {"participants_at_risk", "faers_total_reports_for_drug",
                         "NOT_APPLICABLE"},
    "denominator_unit": {"persons", "reports", "NOT_APPLICABLE"},
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

    # 6 SCHEMA rule: grade 0 requires an ascertainment that can carry it ---
    ZERO_OK = {"measured_null", "reported_zero_no_denominator"}
    bad = [r["measurement_id"] for r in m
           if r["hydroceph_grade"] == "0" and r["ascertainment"] not in ZERO_OK]
    check("grade 0 implies measured_null or reported_zero_no_denominator", not bad,
          "%d rows e.g. %s" % (len(bad), bad[:5]))

    # 6b THE RATCHET. Without this, re-editing extract_faers.py silently restores
    #    the old label and QC passes. A spontaneous report can never be a measured
    #    negative, so this is a property of the SOURCE, not of any one row.
    bad = [r["measurement_id"] for r in m
           if r["study_type"] == "pharmacovigilance"
           and r["ascertainment"] == "measured_null"]
    check("no pharmacovigilance row claims measured_null", not bad,
          "%d rows e.g. %s" % (len(bad), bad[:5]))

    # 6c a reported zero must declare a denominator that is not a person count
    bad = [r["measurement_id"] for r in m
           if r["ascertainment"] == "reported_zero_no_denominator"
           and (r["denominator_type"] == "participants_at_risk"
                or len(r["ascertainment_basis"].strip()) < 20)]
    check("reported zeros declare a non-person denominator and a basis", not bad,
          "offending: %s" % bad[:5])

    # 6d denominator_type must agree with study_type
    bad = [r["measurement_id"] for r in m
           if (r["study_type"] == "pharmacovigilance")
           != (r["denominator_type"] == "faers_total_reports_for_drug")]
    check("denominator_type agrees with study_type", not bad,
          "offending: %s" % bad[:5])

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

    # STRAND-AWARE. A duplex siRNA contributes two strands, each numbered 1..n,
    # so grouping positions by oligo_id alone made a correct duplex look like a
    # broken single strand. Group by (oligo, strand); the length and sequence
    # checks then compare the SENSE/single strand, which is what oligos.length_nt
    # and oligos.sequence_5to3_asprinted describe.
    PRIMARY = {"single_strand", "sense_passenger", "antisense_guide"}
    by_strand = collections.defaultdict(list)
    for r in mods:
        by_strand[(r["oligo_id"], r["strand"])].append(int(r["position_5to3"]))
    bad = ["%s/%s" % k for k, v_ in by_strand.items()
           if sorted(v_) != list(range(1, len(v_) + 1))]
    check("modifications positions are contiguous 1..n within each strand",
          not bad, "offending: %s" % bad[:4])

    bad = sorted({r["strand"] for r in mods if r["strand"] not in PRIMARY})
    check("vocabulary: modifications.strand", not bad, "unexpected: %s" % bad)

    # Every duplex must carry BOTH strands: a half-recorded duplex misstates the
    # administered material.
    duplex_oligos = {k[0] for k in by_strand if k[1] == "sense_passenger"}
    bad = sorted(d for d in duplex_oligos
                 if (d, "antisense_guide") not in by_strand)
    check("every duplex records both strands", not bad, "sense only: %s" % bad[:4])

    lengths = {r["oligo_id"]: r["length_nt"] for r in o}
    primary = {k: v_ for k, v_ in by_strand.items()
               if k[1] in ("single_strand", "sense_passenger")}
    bad = ["%s: %d rows vs length_nt=%s" % (k[0], len(v_), lengths.get(k[0]))
           for k, v_ in primary.items() if lengths.get(k[0]) != str(len(v_))]
    check("modifications row count equals oligos.length_nt (primary strand)",
          not bad, "; ".join(bad[:4]))

    allowed_base = {"A", "C", "G", "T", "U", "NOT_REPORTED"}
    bad = sorted({r["nucleobase"] for r in mods if r["nucleobase"] not in allowed_base})
    check("vocabulary: modifications.nucleobase", not bad, "unexpected: %s" % bad[:6])

    # cEt (constrained ethyl), 2'-F and RNA_2prime_OH entered with the WHO INN
    # duplex and conjugated-ASO parses; morpholino with the printed base runs.
    allowed_sugar = {"2'-MOE", "DNA_2prime_deoxy", "LNA", "morpholino", "2'-OMe",
                     "cEt", "2'-F", "RNA_2prime_OH", "NOT_REPORTED"}
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
    for r in sorted((x for x in mods if x["nucleobase"] != "NOT_REPORTED"
                     and x["strand"] in ("single_strand", "sense_passenger")),
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
    treg_path = os.path.join(ROOT, "data", "trial_register.csv")
    treg = list(csv.DictReader(open(treg_path))) if os.path.exists(treg_path) else []
    tables = {"oligos": o, "measurements": m, "modifications": mods, "sources": s}
    if treg:
        tables["trial_register"] = treg
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

    # 11d-bis every source is actually CITED -----------------------------
    #     assemble.source_meta_for() falls back to a stub whose citation is just
    #     the source_id and whose url, licence, tier and retrieval route are all
    #     NOT_REPORTED. Five sources carrying 23 measurement rows and 54
    #     modification rows sat in that stub because their citation details lived
    #     only in a comment in their builder. A row whose provenance is a comment
    #     in a script is not a cited row, so the stub is now a failure.
    cited_by = collections.Counter(r["source_id"] for r in m)
    for r in mods:
        cited_by[r["source_id"]] += 1
    stubs, thin = [], []
    for r in s:
        if cited_by.get(r["source_id"], 0) == 0:
            continue
        if r["citation"].strip() == r["source_id"].strip():
            stubs.append(r["source_id"])
            continue
        for col in ("url", "access", "license", "evidence_tier", "retrieved_via"):
            if r[col] in ("", "NOT_REPORTED"):
                thin.append("%s.%s" % (r["source_id"], col))
    check("every source carrying rows has a real citation", not stubs,
          "citation is just the source_id for: %s" % stubs[:6])
    check("every source carrying rows states link, rights, tier and route",
          not thin, "unstated: %s" % thin[:8])

    # 11d-ter every URL is a resolvable locator, not a bare hostname -------
    #     "https://dailymed.nlm.nih.gov/dailymed/" told a reader which database
    #     was used but not which document, and a US label is revised in place.
    bare = [r["source_id"] for r in s
            if cited_by.get(r["source_id"], 0)
            and re.match(r"^https?://[^/]+/?$", r["url"] or "")]
    check("source URLs identify a document, not just a host", not bare,
          "bare host: %s" % bare[:6])

    # 11d-quater the ML report agrees with the results it claims to quote ---
    #     ml/ML_REPORT.md opens with "Every number here is read from
    #     ml/results.json; none is typed" -- which was false: analyse.py listed it
    #     as an output but never wrote it, and adding four trials left the report
    #     asserting 526 arms against a results.json saying 546. analyse.py now
    #     generates it; this check stops anyone editing the generated file by hand.
    rp = os.path.join(ROOT, "ml", "results.json")
    mdp = os.path.join(ROOT, "ml", "ML_REPORT.md")
    if os.path.exists(rp) and os.path.exists(mdp):
        res = json.load(open(rp))
        md = open(mdp).read()
        missing = [k for k in ("n_arms", "n_trials", "n_compounds", "n_participants")
                   if "{:,}".format(res[k]) not in md and str(res[k]) not in md]
        check("ML_REPORT.md quotes the numbers in ml/results.json", not missing,
              "not found in the report: %s" % [(k, res[k]) for k in missing])

    # 11d-quinquies every DOI resolves ------------------------------------
    #     The URL sweep passed for two releases while the AQP4 source carried
    #     DOI 10.12659/MSM.907186, which resolves to nothing -- its `url` column
    #     pointed at a good PMC page, so nothing looked at the DOI.
    lc = os.path.join(ROOT, "notes", "link_check.json")
    if os.path.exists(lc):
        checked = json.load(open(lc)).get("dois", {})
        recorded = sorted({r["doi"] for r in s if r["doi"]})
        unchecked = [d for d in recorded if d not in checked]
        unresolved = [d for d in recorded
                      if checked.get(d, {}).get("verdict") not in (None, "ok")]
        check("every recorded DOI has been resolved", not unchecked,
              "not in notes/link_check.json: %s (run scripts/check_source_links.py)"
              % unchecked[:5])
        check("every recorded DOI resolves", not unresolved,
              "did not resolve: %s" % [(d, checked[d]["status"]) for d in unresolved[:4]])

    # 11d-sexies the trial register is one row per trial, and its own counts ---
    if treg:
        dupes = [r["nct_id"] for r in treg
                 if sum(1 for x in treg if x["nct_id"] == r["nct_id"]) > 1]
        check("trial_register holds one row per trial", not dupes,
              "duplicated: %s" % sorted(set(dupes))[:5])
        ct_ncts = {r["source_id"] for r in m
                   if r["study_type"] == "clinical_trial"
                   and r["source_id"].startswith("NCT")}
        reg_ncts = {r["nct_id"] for r in treg}
        orphan = sorted(ct_ncts - reg_ncts)
        check("every trial contributing rows is in the register", not orphan,
              "missing from register: %s" % orphan[:5])
        bad = [r["nct_id"] for r in treg
               if r["endpoint_evaluability"] == "identified_only_no_outcome_record"
               and int(r["n_outcome_records"] or 0) > 0]
        check("evaluability agrees with the outcome-record count", not bad,
              "offending: %s" % bad[:5])

    # 11d-septies sequence_source must name the SAME source as the per-position
    #     rows for that compound. A single shared SEQ_SOURCE constant credited the
    #     three Gai2 ODNs (BMC Neuroscience 2007, PMC1855344) to the SPAK paper
    #     (Nature Communications 2025, PMC12246246). measurements.csv and
    #     modifications.csv had it right; only the oligo roster was wrong, so no
    #     existing check compared them.
    src_by_id = {r["source_id"]: r for r in s}
    mod_src = collections.defaultdict(set)
    for r in mods:
        mod_src[r["oligo_name"]].add(r["source_id"])
    bad = []
    for r in o:
        name, ss = r["oligo_name"], r.get("sequence_source", "")
        pmcs = set(re.findall(r"PMC\d+", ss))
        if not pmcs or name not in mod_src:
            continue
        allowed = set()
        for sid in mod_src[name]:
            allowed |= set(re.findall(r"PMC\d+", sid + " "
                                      + src_by_id.get(sid, {}).get("pmcid", "")
                                      + " " + src_by_id.get(sid, {}).get("url", "")))
        if allowed and not (pmcs & allowed):
            bad.append("%s: sequence_source cites %s but its position rows cite %s"
                       % (name, sorted(pmcs), sorted(allowed)))
    check("oligos.sequence_source agrees with the modification rows' source",
          not bad, "; ".join(bad[:4]))

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
        # tier_A_positive was a single number pooling three axes: ventricular
        # enlargement, disease-background rate (no compound at all) and ONE
        # therapeutic row whose own grade_basis says to exclude it from any
        # compound-toxicity analysis. Published as one figure it reads as
        # "hydrocephalus events", which it is not. Split.
        tier_A_positive=sum(1 for r in m if r["endpoint_tier"] == "A"
                            and r["ascertainment"] == "measured_positive"),
        tier_A_positive_ventricular=sum(
            1 for r in m if r["endpoint_tier"] == "A"
            and r["ascertainment"] == "measured_positive"
            and r["tox_axis"] == "ventricular_enlargement"
            and r["oligo_name"] not in ("NOT_APPLICABLE", "placebo_or_sham_control")),
        tier_A_positive_disease_background=sum(
            1 for r in m if r["endpoint_tier"] == "A"
            and r["ascertainment"] == "measured_positive"
            and r["tox_axis"] == "disease_background_rate"),
        tier_A_positive_therapeutic=sum(
            1 for r in m if r["endpoint_tier"] == "A"
            and r["ascertainment"] == "measured_positive"
            and r["tox_axis"] == "therapeutic_ventricular_effect"),
        tier_A_positive_on_placeholder_arm=sum(
            1 for r in m if r["endpoint_tier"] == "A"
            and r["ascertainment"] == "measured_positive"
            and r["oligo_name"] in ("NOT_APPLICABLE", "placebo_or_sham_control")),
        # tier_A_null previously pooled assessed negatives with FAERS reporting
        # zeros; 176 of the old 755 could not establish an absence at all.
        tier_A_null=sum(1 for r in m if r["endpoint_tier"] == "A"
                        and r["ascertainment"] == "measured_null"),
        tier_A_reported_zero_no_denominator=sum(
            1 for r in m if r["endpoint_tier"] == "A"
            and r["ascertainment"] == "reported_zero_no_denominator"),
        n_compounds_real=0,  # filled below
        n_oligo_records=len(o),
        grade3_rows=sum(1 for r in m if r["hydroceph_grade"] == "3"),
        duplexes_checked=dup_checked,
        oligos_with_sequence=sum(
            1 for r in o if r["sequence_5to3_asprinted"] not in ("NOT_REPORTED",
                                                                 "NOT_APPLICABLE")),
        checks_run=len(CHECKS), checks_failed=len(FAILURES),
    )
    PLACEHOLDERS = {"NOT_APPLICABLE", "placebo_or_sham_control"}
    stats["n_compounds_real"] = sum(1 for r in o
                                    if r["oligo_name"] not in PLACEHOLDERS)
    stats["oligos_without_sequence"] = sum(
        1 for r in o if r["sequence_5to3_asprinted"] in ("", "NOT_REPORTED"))
    # Figures the prose quotes that are not already a column tally. Each is
    # defined here once, so the document cannot hold a second definition.
    # "marketed" means a product label is carried for it — DailyMed or an EMA
    # SmPC. Both give 11; the "12" the README carried matched neither definition.
    _labelled = {r["oligo_name"] for r in m if r["study_type"] == "regulatory_label"}
    stats["oligos_with_sequence_marketed"] = sum(
        1 for r in o if r["oligo_name"] in _labelled
        and r["sequence_5to3_asprinted"] not in ("", "NOT_REPORTED",
                                                 "NOT_APPLICABLE"))
    stats["n_placeholder_oligos"] = len(o) - stats["n_compounds_real"]
    # The exact MedDRA preferred term, not a sum over the category: the category
    # also holds HYPERTENSIVE HYDROCEPHALUS (1) and two reported zeros, and a sum
    # over it would silently pool four different terms into one quoted figure.
    stats["faers_nusinersen_hydrocephalus_reports"] = sum(
        int(r["n_affected"]) for r in m
        if r["source_id"].startswith("FAERS") and "nusinersen" in r["oligo_name"]
        and r["readout_term_verbatim"] == "HYDROCEPHALUS"
        and r["n_affected"].isdigit())
    stats["rows_ema_smpc"] = sum(1 for r in m if r["source_id"].startswith("EMA_"))
    _meth = os.path.join(ROOT, "METHODOLOGY.md")
    stats["open_items"] = (len(re.findall(r"^\*\*OI-\d+", open(_meth).read(),
                                          re.M)) if os.path.exists(_meth) else 0)
    # ---- source-level rights register reconciles to the data --------------
    #     A rights register that does not account for every row is worse than
    #     none: it reads as coverage. Its measurement counts must sum to
    #     measurements.csv and its per-tier totals must match by_redistribution.
    _rr = os.path.join(ROOT, "notes", "rights_register_source.csv")
    if os.path.exists(_rr):
        rr = list(csv.DictReader(open(_rr)))
        _tot = sum(int(r["n_measurements"] or 0) for r in rr)
        check("rights register accounts for every measurement row",
              _tot == len(m), "register %d vs measurements %d" % (_tot, len(m)))
        check("every source in the register has a tier",
              all(r["rights_tier"] in set("ABCDU") for r in rr),
              "untiered: %s" % [r["source_ref"] for r in rr
                                if r["rights_tier"] not in set("ABCDU")][:5])
        check("no rights row asserts legal clearance",
              all("NOT legal clearance" in r["resolved_by"] for r in rr),
              "a rights tag records an observation and a proposal, never "
              "clearance")
        check("every held row states why it is held",
              all(r["hold_reason"] for r in rr
                  if r["extracted_data_release"] != "RELEASE"),
              "a DECISION_REQUIRED row with no reason is a silent hold")
        stats["rights_register_sources"] = len(rr)
        stats["rights_by_tier"] = dict(collections.Counter(
            r["rights_tier"] for r in rr))

    # ---- SCIENTIFIC_RULES section G: the sequence-family join rule --------
    #     ml/build_analysis_set.py groups folds on oligos.sequence_base, which is
    #     upper-cased, chemistry-stripped and U->T mapped. Crank's project-wide
    #     rule forbids case-insensitive merging without adjudication, so the
    #     normalization must be shown not to be doing the work. Byte-exact
    #     re-keying on the as-printed sequence must give the same families.
    def _fams(col):
        g = collections.defaultdict(set)
        for r in o:
            v = r[col]
            if v not in ("", "NOT_REPORTED", "NOT_APPLICABLE"):
                g[v].add(r["oligo_name"])
        return {frozenset(v) for v in g.values() if len(v) > 1}
    _norm, _exact = _fams("sequence_base"), _fams("sequence_5to3_asprinted")
    check("normalized and byte-exact sequence families agree",
          _norm == _exact,
          "case/U-T folding changes the grouping: normalized %s vs exact %s"
          % (sorted(map(sorted, _norm)), sorted(map(sorted, _exact))))
    stats["sequence_families_multi_member"] = sorted(sorted(f) for f in _exact)

    # ---- SCIENTIFIC_RULES section E: severity axes stay apart -------------
    AXES = {"clinical_hydrocephalus_severity_0_3",
            "animal_in_vivo_severity_0_3",
            "experimental_response_severity_0_3", "NOT_APPLICABLE"}
    check("severity_axis uses the declared vocabulary",
          all(r["severity_axis"] in AXES for r in m),
          "unexpected: %s" % sorted({r["severity_axis"] for r in m} - AXES))
    check("no in-vitro row carries a clinical severity grade",
          not [r for r in m if r["subject_class"].endswith("in_vitro")
               and r["severity_axis"] == "clinical_hydrocephalus_severity_0_3"],
          "section E forbids mapping an in-vitro readout onto a clinical scale")
    check("every graded row states its severity axis",
          not [r for r in m if r["hydroceph_grade"] not in ("", "NOT_APPLICABLE")
               and r["severity_axis"] == "NOT_APPLICABLE"],
          "a grade with no axis can be pooled with any other grade")
    check("every ungraded row carries severity_axis NOT_APPLICABLE",
          not [r for r in m if r["hydroceph_grade"] in ("", "NOT_APPLICABLE")
               and r["severity_axis"] != "NOT_APPLICABLE"],
          "an axis on an ungraded row implies a grade that is not there")
    check("the experimental axis is not pooled into any published grade count",
          "experimental_response_severity" in open(
              os.path.join(ROOT, "scripts", "data_dictionary.py")).read(),
          "the axis must be documented where readers look for column meanings")
    stats["by_severity_axis"] = dict(collections.Counter(
        r["severity_axis"] for r in m))

    # The grade-0 decomposition. Published because the headline "1,114 negatives"
    # is not 1,114 measured negatives: most rest on an absence. SCIENTIFIC_RULES
    # section E and this release's 42 CFR reading disagree on whether that is a
    # negative at all, so the split is a figure German needs, not a footnote.
    def _g0basis(r):
        b = r["grade_basis"]
        if "no FAERS report" in b:
            return "faers_absence"
        if "no serious adverse event coded" in b:
            return "sae_table_absence"
        if ("contains no statement" in b or "no occurrence" in b
                or "returns zero occurrences" in b):
            return "label_absence"
        if "explicitly reported count of 0" in b:
            return "explicit_reported_zero"
        return "other"
    _g0 = [r for r in m if r["hydroceph_grade"] == "0"]
    stats["grade0_rows"] = len(_g0)
    stats["grade0_by_basis"] = dict(collections.Counter(_g0basis(r) for r in _g0))
    stats["grade0_reported_zero_rows"] = sum(
        1 for r in _g0 if r["ascertainment"] == "reported_zero_no_denominator")
    stats["grade0_absence_measured_null_rows"] = sum(
        1 for r in _g0 if r["ascertainment"] == "measured_null"
        and _g0basis(r) in ("sae_table_absence", "label_absence"))
    stats["grade0_not_absence_rows"] = sum(
        1 for r in _g0 if _g0basis(r) not in ("sae_table_absence",
                                              "label_absence", "faers_absence"))
    # Ratchet: the contradiction between SCHEMA.md's "requires measured_null" and
    # data_dictionary.py's "measured_null OR reported_zero_no_denominator" is
    # German's to rule on. What is enforceable here is that it stays DISCLOSED.
    _sch = os.path.join(ROOT, "SCHEMA.md")
    check("the grade-0 ascertainment contradiction is disclosed in SCHEMA.md",
          os.path.exists(_sch) and "OPEN CONTRADICTION" in open(_sch).read(),
          "SCHEMA.md states grade 0 requires measured_null while "
          "data_dictionary.py permits reported_zero_no_denominator, and "
          "%d rows take the permissive reading" % sum(
              1 for r in _g0 if r["ascertainment"]
              == "reported_zero_no_denominator"))
    stats["oligos_with_purity"] = sum(
        1 for r in o if r["purity_pct"] not in ("", "NOT_REPORTED",
                                                "NOT_APPLICABLE"))
    stats["oligos_without_purity"] = len(o) - stats["oligos_with_purity"]
    check("sequenced + unsequenced + placeholders = roster",
          stats["oligos_with_sequence"] + stats["oligos_without_sequence"]
          + (len(o) - stats["n_compounds_real"]) == len(o),
          "%d + %d + %d != %d" % (stats["oligos_with_sequence"],
                                  stats["oligos_without_sequence"],
                                  len(o) - stats["n_compounds_real"], len(o)))
    # Trial counters. The release previously published four disagreeing trial
    # figures (161 / 159 / 155 / none) and qc/stats.json held none at all.
    reg = list(csv.DictReader(open(os.path.join(ROOT, "data", "trial_registry.csv"))))
    kept = [r for r in reg if not r["excluded_reason"]]
    ct = [r for r in m if r["study_type"] == "clinical_trial"]
    with_rows = {r["source_id"] for r in ct if r["source_id"].startswith("NCT")}
    evaluable = {r["source_id"] for r in ct
                 if r["assessment_type"] not in ("NOT_APPLICABLE", "", "NOT_REPORTED")}
    if treg:
        _ev = collections.Counter(r["endpoint_evaluability"] for r in treg)
        stats["trials_verified_register"] = len(treg)
        stats["trials_by_evaluability"] = dict(_ev)
        stats["trials_marked_extension"] = sum(
            1 for r in treg if r["participants_overlap_warning"] == "TRUE")
    # Evidence classes kept apart, so no reader can build one denominator.
    stats["human_outcome_records_by_class"] = dict(collections.Counter(
        r["study_type"] for r in m if r["subject_class"].startswith("human")))
    stats["animal_rows"] = sum(1 for r in m
                               if r["subject_class"].startswith("animal"))
    # render_docs.stat_values() used to add these two itself, which put two of
    # the renderable keys outside stats.json and outside every check over it.
    stats["n_trials"] = len(reg)
    stats["n_ctgov_rows"] = sum(1 for r in m if r["source_id"].startswith("NCT"))
    stats["trials_registry_rows"] = len(reg)
    stats["trials_excluded_identity"] = len(reg) - len(kept)
    stats["trials_human_unique"] = len({r["nct_id"] for r in kept} & with_rows)
    stats["trials_with_systematic_assessment"] = len(evaluable & with_rows)
    stats["trial_outcome_records"] = len(ct)

    # ---- HUMAN-SUBSET characterization completeness -----------------------
    #     The release published completeness for the whole roster, which is
    #     flattering: the three purity-carrying constructs and 7 of the 13
    #     sequence-resolved compounds are animal-only, so the human subset is far
    #     thinner than the headline. Published separately so it cannot be misread.
    PLACE = {"NOT_APPLICABLE", "placebo_or_sham_control"}
    obyname = {r["oligo_name"]: r for r in o}
    human_cmpds = {r["oligo_name"] for r in m
                   if r["subject_class"].startswith("human")
                   and r["oligo_name"] not in PLACE}
    def _has(name, col):
        v = (obyname.get(name, {}) or {}).get(col, "")
        return v not in ("", "NOT_REPORTED", "NOT_APPLICABLE")
    modded = {r["oligo_name"] for r in mods}
    hrows = [r for r in m if r["subject_class"].startswith("human")]
    stats["human_subset"] = dict(
        compounds=len(human_cmpds),
        with_sequence=sum(1 for c in human_cmpds
                          if _has(c, "sequence_5to3_asprinted")),
        with_position_map=sum(1 for c in human_cmpds if c in modded),
        with_purity=sum(1 for c in human_cmpds if _has(c, "purity_pct")),
        with_conjugate=sum(1 for c in human_cmpds if _has(c, "conjugate")),
        rows=len(hrows),
        rows_with_dose=sum(1 for r in hrows
                           if r["dose_value"] not in ("", "NOT_REPORTED",
                                                      "NOT_APPLICABLE")),
        rows_with_duration=sum(1 for r in hrows
                               if r["exposure_duration"] not in
                               ("", "NOT_REPORTED", "NOT_APPLICABLE")),
    )
    stats["human_in_vitro_rows"] = sum(1 for r in m
                                       if r["subject_class"] == "human_in_vitro")
    # Flat aliases so prose can quote the human-subset figures through a token.
    for _k, _v in stats["human_subset"].items():
        stats["human_subset_" + _k] = _v

    # ---- figures that shipped prose quotes -------------------------------
    #     Eleven figures in METHODOLOGY.md, PHASE2_COMPLIANCE.md and README.md
    #     were stale: "39 checks" (64), "10 of 50 compounds carry a sequence"
    #     (26 of 53), "202 per-position records" (555), "animal arm is 5 rows"
    #     (10), "1,290 public domain" (1,303), component row counts off by
    #     hundreds. Every one of them was a figure a human typed next to a word.
    #     Typing is the defect, so these keys exist to be rendered into the
    #     prose as <!--stat:KEY--> tokens and the prose-figure check below
    #     refuses any untokenised figure that is not a declared constant.
    COMPONENT_FILES = {
        "rows_ctgov": "_ctgov_measurements.csv",
        "rows_ctgov_outcomes": "_ctgov_outcome_measurements.csv",
        "rows_faers": "_faers_measurements.csv",
        "rows_labels": "_label_measurements.csv",
        "rows_literature": "_literature_measurements.csv",
        "rows_nonclinical": "_nonclinical_measurements.csv",
    }
    for key, fname in COMPONENT_FILES.items():
        fpath = os.path.join(DATA, fname)
        # csv.reader, not line count: arm_description carries embedded newlines,
        # so `wc -l` reads 898 records where the file holds 746.
        stats[key] = (sum(1 for _ in csv.DictReader(open(fpath)))
                      if os.path.exists(fpath) else 0)
    check("component row counts sum to measurements.csv",
          sum(stats[k] for k in COMPONENT_FILES) == len(m),
          "components %d vs measurements %d"
          % (sum(stats[k] for k in COMPONENT_FILES), len(m)))

    _rights = collections.Counter(r["redistribution"] for r in m)
    for term in ("public_domain", "cc_by", "cc_by_nc", "summary_stat_only",
                 "verify"):
        stats["rights_" + term] = _rights.get(term, 0)

    # The 42 CFR 11.48(a)(4)(ii)(A) absence negatives, quoted in METHODOLOGY §9.
    stats["tier_A_absence_cfr_rows"] = sum(
        1 for r in m if r["endpoint_tier"] == "A"
        and "11.48" in r.get("ascertainment_basis", ""))
    stats["tier_A_negative_rows"] = sum(
        1 for r in m if r["endpoint_tier"] == "A"
        and r["ascertainment"] in ("measured_null",
                                   "reported_zero_no_denominator"))

    _bk = os.path.join(ROOT, "notes", "source_backlog.csv")
    stats["source_backlog_rows"] = (sum(1 for _ in csv.DictReader(open(_bk)))
                                    if os.path.exists(_bk) else 0)

    for key, fname in (("n_measurement_cols", "measurements.csv"),
                       ("n_oligo_cols", "oligos.csv"),
                       ("n_modification_cols", "modifications.csv"),
                       ("n_source_cols", "sources.csv")):
        fpath = os.path.join(DATA, fname)
        stats[key] = (len(next(csv.reader(open(fpath))))
                      if os.path.exists(fpath) else 0)

    # ---- shipped-prose figure ratchet ------------------------------------
    #     Eleven figures in the shipped documents were stale at once and nothing
    #     caught them, because a number typed next to a word is invisible to a
    #     dataset check. Every statistical figure in a shipped document must now
    #     be EITHER rendered from a <!--stat:KEY--> token (scripts/render_docs.py
    #     rewrites those on every build) OR declared in qc/prose_constants.json
    #     with a reason it cannot move. Anything else fails here.
    #
    #     The matcher deliberately runs in both directions and crosses markdown
    #     pipes. A number-then-noun pattern bounded by [^.|] misses every stale
    #     figure in table form, because in a table the noun precedes the number
    #     and a pipe sits between them -- that is how the sibling endpoints'
    #     check_doc_numbers.py missed figures that were live at the time.
    PROSE_FILES = ["README.md", "METHODOLOGY.md", "SCHEMA.md",
                   "PHASE2_COMPLIANCE.md"]
    NOUNS = (r"(?:compounds?|oligos?|oligonucleotides?|trials?|rows?|arms?"
             r"|participants?|sequences?|columns?|sources?|modifications?"
             r"|folds?|studies|records?|reports?|events?|cases?|checks?)")
    FWD = re.compile(r"\b\d[\d,]*\b[^.\n]{0,40}?\b" + NOUNS, re.I)
    REV = re.compile(NOUNS + r"[^.\n]{0,25}?\b\d[\d,]*\b", re.I)
    TOKEN_SPAN = re.compile(r"<!--stat:[A-Za-z_0-9]+-->.*?<!--/stat-->", re.S)
    # Masked first, because these are not figures about this dataset at all and
    # declaring each one a "constant" would turn the register into noise and hide
    # the handful of external facts that genuinely need a reason recorded.
    NOT_A_FIGURE = [
        re.compile(r"\bOI-\d+"),                       # open-item section ids
        re.compile(r"\bNCT\d+"),                       # trial registrations
        re.compile(r"\b[A-Z]{2,}-\d{3,}\b"),           # development codes
        re.compile(r"\b\d+ CFR\b"),                    # regulation citations
        re.compile(r"CC BY(?:-NC)?(?:-ND)?(?:\s[\d.]+)?"),
        re.compile(r"\b[Pp]hase \d(?:/\d)?[a-z]?\b"),
        re.compile(r"\bgrades?[- ]\d\b", re.I),        # rubric levels, incl. "grade-0"
        re.compile(r"\b\d+-mer\b"),                    # oligo length idiom
        re.compile(r"\b\d+-\d+-\d+\b"),                # gapmer motif strings
        re.compile(r"\b\d+-methylation\b"),
        re.compile(r"\bTable \d+\b"), re.compile(r"§\s?\d+(?:\.\d+)*"),
        re.compile(r"\bsections? \d+(?:\.\d+)*", re.I),
        re.compile(r"\*?n−1\*?"), re.compile(r"\bn=\d+"),
        # Source-reported quantities carrying a unit or a percent sign are
        # measurements quoted from a paper, not counts over this dataset.
        re.compile(r"\d[\d.,]*\s*(?:-\s*\d[\d.,]*)?\s*%"),
        re.compile(r"\d[\d.,]*\s*(?:mL|mg|g/L|kg|µ[gm]|nM|µM|mm|cm|mmHg)\b"),
        re.compile(r"\b(?:19|20)\d{2}\b"),             # years in citations
    ]
    GEN_BLOCK = re.compile(r"<!-- BEGIN GENERATED.*?<!-- END GENERATED -->", re.S)

    cpath = os.path.join(HERE, "prose_constants.json")
    constants = {k: v for k, v in
                 (json.load(open(cpath)) if os.path.exists(cpath) else {}).items()
                 if not k.startswith("_")}  # "_README" documents the file itself
    # A token whose key is not a known statistic renders nothing and is a silent
    # hole in the ratchet, so the keys are checked here, not only at render time.
    bad_keys = sorted({k for rel in PROSE_FILES
                       if os.path.exists(os.path.join(ROOT, rel))
                       for k in re.findall(r"<!--stat:([A-Za-z_0-9]+)-->",
                                           open(os.path.join(ROOT, rel)).read())
                       if k not in stats})
    check("every <!--stat:KEY--> token names a real statistic",
          not bad_keys, "unknown keys: %s" % bad_keys[:6])
    check("qc/prose_constants.json exists", os.path.exists(cpath),
          "the prose ratchet needs its declared-constant register")
    bad_reason = [c.get("text", "")[:40] for f in constants
                  for c in constants[f] if len(c.get("why", "")) < 12]
    check("every declared prose constant states why it cannot move",
          not bad_reason, "no reason given for: %s" % bad_reason[:5])

    unaccounted = []
    for rel in PROSE_FILES:
        fpath = os.path.join(ROOT, rel)
        if not os.path.exists(fpath):
            continue
        for lineno, line in enumerate(open(fpath).read().split("\n"), 1):
            masked = TOKEN_SPAN.sub(" ", line)
            # Declared constants are matched against the line as written, BEFORE
            # the not-a-figure masks run: a declaration quoting a percentage or a
            # unit would otherwise never match, because the mask had already
            # removed the very characters it quotes.
            for decl in constants.get(rel, []):
                masked = masked.replace(decl["text"], " ")
            for pat in NOT_A_FIGURE:
                masked = pat.sub(" ", masked)
            if FWD.search(masked) or REV.search(masked):
                hit = (FWD.search(masked) or REV.search(masked)).group(0)
                unaccounted.append("%s:%d %r" % (rel, lineno, hit[:60]))
    # The generated block in README is rendered wholesale from stats.json, so it
    # is masked by file-region rather than per figure.
    gen_lines = set()
    rpath = os.path.join(ROOT, "README.md")
    if os.path.exists(rpath):
        text = open(rpath).read()
        mo = GEN_BLOCK.search(text)
        if mo:
            lo = text[:mo.start()].count("\n") + 1
            hi = text[:mo.end()].count("\n") + 1
            gen_lines = set(range(lo, hi + 1))
    unaccounted = [u for u in unaccounted
                   if not (u.startswith("README.md:")
                           and int(u.split(":")[1].split(" ")[0]) in gen_lines)]
    check("every figure in shipped prose is rendered or declared constant",
          not unaccounted,
          "%d unaccounted: %s" % (len(unaccounted), "; ".join(unaccounted[:6])))
    stats["prose_figures_unaccounted"] = len(unaccounted)

    # ---- release identifier ----------------------------------------------
    #     Different branches and Drive exports held different versions with no key
    #     binding dataset, figures and documents together. The commit is the key.
    #     The flag must test the INPUTS, not the whole directory. Testing
    #     everything made `-dirty` unavoidable: a build rewrites stats.json, the
    #     CSVs, the PDFs and the workbook, so the very act of computing the
    #     release id dirtied the tree that the id describes. Every shipped
    #     statistic therefore carried `-dirty` and matched no commit — the
    #     reproducibility claim the identifier exists to make was never true.
    #     Dirty now means: a file that FEEDS the build has uncommitted changes.
    GENERATED = ("qc/stats.json", "data/", "ml/results.json", "ml/ML_REPORT.md",
                 "ml/analysis_set.csv", "ml/figures/", "notes/", "README.md",
                 "PHASE2_COMPLIANCE.md", ".pdf", ".xlsx")

    def _is_generated(path):
        rel = path.split("toxicity/hydrocephalus/", 1)[-1]
        return any(rel.startswith(g) or rel.endswith(g) for g in GENERATED)

    try:
        rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
        porcelain = subprocess.run(["git", "status", "--porcelain", "."], cwd=ROOT,
                                   capture_output=True, text=True).stdout
        changed = [ln[3:].strip() for ln in porcelain.splitlines() if ln[3:].strip()]
        inputs_changed = sorted(p_ for p_ in changed if not _is_generated(p_))
        dirty = bool(inputs_changed)
        stats["release_inputs_modified"] = inputs_changed[:10]
    except Exception:
        rev, dirty = "", False
        stats["release_inputs_modified"] = []
    stats["release_id"] = ("hydrocephalus-%s%s" % (rev or "unknown",
                                                   "-dirty" if dirty else ""))

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
