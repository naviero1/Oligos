#!/usr/bin/env python3
"""Bind data, schema, documents, figures and verification results to one commit.

    python3 toxicity/coagulopathy/scripts/build_release_manifest.py

    -> RELEASE_MANIFEST.json

Added after Beebop's 2026-09-30 review, which observed that different branches and Drive
exports hold different versions of this endpoint with no way to tell which counts belong to
which artefacts. The manifest records the commit, a SHA-256 for every released file, and
the counts and check results that were true for THAT commit -- so a workbook or a PDF can
always be traced back to the data it was built from.
"""
import csv, hashlib, json, os, subprocess, datetime
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "RELEASE_MANIFEST.json")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"


def sh(*a):
    try:
        return subprocess.run(a, capture_output=True, text=True, cwd=ROOT, timeout=60).stdout.strip()
    except Exception:
        return ""


def digest(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(n):
    with open(os.path.join(ROOT, "data", n), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    D, O, M, S = load("measurements.csv"), load("oligos.csv"), load("modifications.csv"), load("sources.csv")
    studies = load("studies.csv") if os.path.exists(os.path.join(ROOT, "data", "studies.csv")) else []

    files = {}
    for rel in ("data/measurements.csv", "data/oligos.csv", "data/modifications.csv",
                "data/sources.csv", "data/studies.csv", "schema.md", "METHODOLOGY.md",
                "README.md", "PADP.md", "STATUS.md", "coagulopathy.md", "SOURCES.md",
                "OligoTox-Coagulopathy_Dataset.xlsx", "OligoTox-Coagulopathy_Narrative.pdf",
                "OligoTox-Coagulopathy_Methodology.pdf", "OligoTox-Coagulopathy_PADP.pdf",
                "OligoTox-Coagulopathy_Sources.pdf", "sources/DOWNLOAD_MANIFEST.csv"):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            files[rel] = {"sha256": digest(p), "bytes": os.path.getsize(p)}

    hum = [r for r in D if r["species_class"] == "human"]
    # Use the register's own decision column. Recomputing the rule here produced a second,
    # higher number (57 vs 30) because it omitted the identity requirement -- exactly the
    # kind of drift this manifest exists to prevent.
    trials = [r for r in studies if r.get("headline_trial") == "TRUE"]
    flagged = [r for r in trials if r.get("review_flag")]

    man = {
        "endpoint": "coagulopathy",
        "generated": datetime.date.today().isoformat(),
        "commit": sh("git", "rev-parse", "HEAD"),
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD"),
        "tree_dirty": bool(sh("git", "status", "--porcelain", "--", ".")),
        "counts": {
            "sources": len(S), "compounds": len(O), "measurements": len(D),
            "modification_positions": len(M),
            "human_measurements": len(hum),
            "animal_measurements": sum(1 for r in D if r["species_class"] == "animal"),
            "undetermined_origin": sum(1 for r in D if r["species_class"] == "not_determined"),
            "compounds_with_sequence": sum(1 for r in O if r["sequence_base"] not in (NR, NA, "")),
            "compounds_with_purity_value": sum(1 for r in O if r["purity_pct"] not in (NR, NA, "")),
        },
        "human_study_register": {
            "present": bool(studies),
            "study_records": len(studies),
            "headline_human_interventional_trials": len(trials) if studies else None,
            "of_which_registry_identified": sum(1 for r in trials if r.get("identity_basis") == "registry_number"),
            "flagged_for_manual_verification": [r["study_id"] for r in flagged],
            "headline_rule": ("design=interventional_trial AND a coagulation endpoint AND a "
                              "verifiable identity (registry number, trial acronym or sponsor "
                              "protocol token). Pooled analyses, labels, regulatory summaries, "
                              "observational studies, case reports, healthy-volunteer laboratory "
                              "work and spontaneous reporting are excluded."),
            "by_design": dict(Counter(r.get("design", "") for r in studies)) if studies else {},
            "note": ("Headline human-trial total. Counts each study once across its registry "
                     "record, publications, regulatory reports and label."
                     if studies else
                     "UNESTABLISHED - no register built yet; do not quote a trial total."),
        },
        "evidence_class": dict(Counter(r["evidence_class"] for r in D)),
        "human_system_subtype": dict(Counter(r["human_system_subtype"] for r in hum)),
        "grade_authority": dict(Counter(r["grade_authority"] for r in D)),
        "grading": {
            "scored_rows": sum(1 for r in D if r["coag_tox_grade"] != NR),
            "source_reported_grades": sum(1 for r in D if r["source_stated_grade"] != NA),
            "rows_flagged_near_unity": sum(1 for r in D if r["grade_caveat"] == "within_reference_range_resolution"),
            "validated_clinical_grades": sum(1 for r in D if r["is_validated_clinical_grade"] == "TRUE"),
            "all_provisional": all(r["grade_status"] == "provisional" for r in D),
        },
        "files": files,
        "checks": {"note": "Run scripts/validate_dataset.py and scripts/verify_against_sources.py; "
                           "both exit non-zero on failure. Results are not asserted here."},
        "scientific_status": {
            "grades_reviewed_by_subject_matter_expert": False,
            "evidence_class_reviewed": False,
            "challenge_eligibility_assessed": False,
            "note": "Structural checks passing is not scientific approval. Labels, controls, "
                    "model eligibility and final claims remain with the team's scientist.",
        },
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2)
        fh.write("\n")
    print(f"  wrote RELEASE_MANIFEST.json  commit {man['commit'][:10]}  {len(files)} files hashed")
    print(f"    trials: {man['human_study_register']['headline_human_interventional_trials']}"
          f"  human rows: {man['counts']['human_measurements']}  animal rows: {man['counts']['animal_measurements']}")


if __name__ == "__main__":
    main()
