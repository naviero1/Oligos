#!/usr/bin/env python3
"""Bind the dataset, documents and figures to one release identifier with checksums.

Beebop's "Common gaps" notes that different branches and Drive exports hold different
versions, so each accepted dataset, source inventory and document should be bound to a
release identifier. Without that, a reviewer holding an older Drive export cannot tell
whether a count they are reading belongs to the dataset they have.

The release id is derived from the content, not the clock: it is the first 12 hex
characters of a SHA-256 over the canonical tables. The same data always yields the same
id, and any change to a table changes it.

Usage:  python scripts/make_release_manifest.py
"""
import csv, hashlib, json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)

CANONICAL = ["data/oligos.csv", "data/measurements.csv"]
DERIVED = ["data/oligotox_kidney_merged.csv", "data/human_animal_bridge.csv",
           "data/clinical_study_register.csv", "data/OligoTox-Kidney.xlsx"]
DOCS = ["NARRATIVE.md", "METHODOLOGY_PHASE2.md", "PADP.md", "schema.md",
        "SOURCE_REGISTER.md", "CLINICAL_VALIDATION.md", "STATUS.md",
        "NARRATIVE.pdf", "METHODOLOGY_PHASE2.pdf", "PADP.pdf", "SOURCE_REGISTER.pdf"]

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    canon = {f: sha(D(f)) for f in CANONICAL if os.path.exists(D(f))}
    rel = hashlib.sha256("".join(canon[k] for k in sorted(canon)).encode()).hexdigest()[:12]

    o = list(csv.DictReader(open(D("data/oligos.csv"), newline="")))
    m = list(csv.DictReader(open(D("data/measurements.csv"), newline="")))
    reg = (list(csv.DictReader(open(D("data/clinical_study_register.csv"), newline="")))
           if os.path.exists(D("data/clinical_study_register.csv")) else [])
    trials = {r["study_key"] for r in reg if r["evidence_class"] == "trial"}
    readt = {r["study_key"] for r in reg if r.get("counts_as_verified") == "TRUE"}
    cls = {}
    for r in m:
        cls[r["subject_class"]] = cls.get(r["subject_class"], 0) + 1

    try:
        commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()[:12]
    except Exception:
        commit = "unknown"

    man = {
        "release_id": f"kidney-{rel}",
        "endpoint": "kidney / nephrotoxicity",
        "git_commit": commit,
        "counts": {
            "oligos": len(o),
            "measurements": len(m),
            "human_clinical_trials_identified": len(trials),
            "human_clinical_trials_report_read": len(readt),
            "clinical_measurement_rows": cls.get("human_clinical", 0),
            "human_laboratory_rows": cls.get("human_invitro", 0),
            "animal_appendix_rows": cls.get("animal_invitro", 0) + cls.get("animal_invivo", 0),
            "unique_compounds_with_clinical_evidence":
                len({r["oligo_id"] for r in reg}) if reg else None,
            "sequences_present": sum(
                1 for r in o if r["sequence_5to3"].strip() not in ("TBD", "", "NA")),
            "rows_gated_from_negative_training": sum(
                1 for r in m if not r.get("nephrotox_grade_modeling", "").strip()),
        },
        "canonical_sha256": canon,
        "derived_sha256": {f: sha(D(f)) for f in DERIVED if os.path.exists(D(f))},
        "document_sha256": {f: sha(D(f)) for f in DOCS if os.path.exists(D(f))},
        "notes": [
            "release_id is content-derived from the canonical tables; identical data yields "
            "an identical id, and any table change changes it.",
            "Derived files are regenerable: build_merged.py, split_human_animal.py, "
            "build_study_register.py, build_workbook.py.",
            "All grades remain provisional pending scientific sign-off.",
        ],
    }
    with open(D("RELEASE_MANIFEST.json"), "w") as fh:
        json.dump(man, fh, indent=2, sort_keys=False)
        fh.write("\n")
    print(f"release_id: {man['release_id']}  (git {commit})")
    for k, v in man["counts"].items():
        print(f"  {k:<48}{v}")

if __name__ == "__main__":
    main()
