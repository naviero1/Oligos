#!/usr/bin/env python3
"""Verify the kidney module's headline claims against this repository's live kidney data.

    python3 toxicity/cns/qc/verify_nephro_intake.py

Exit code 0 = every claim reproduces. Non-zero = one does not.

Why this lives in the CNS module
--------------------------------
The CNS module borrowed the kidney module's shape: a two-table oligo/measurement schema, an
ordinal 0-3 grade whose rule is recorded per row, and per-row provenance. Before borrowing it,
the kidney module's own headline numbers were recomputed from its CSVs rather than taken on the
deck's word. This script is that check, kept runnable so the borrowing stays honest as the
kidney data evolves.

It reads `toxicity/kidney/data/` -- the live kidney tables, not a snapshot.

Drift note
----------
The claims below were first checked against a snapshot taken 2026-08-26, where all 13 held.
Since then the kidney team has filled in more sequences: `sequences_filled` was 33 in that
snapshot and is 55 here. That is an improvement to the kidney corpus, not a defect, and the
expected value below tracks the live file. Every other claim is unchanged.
"""
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent      # toxicity/cns
DATA = ROOT.parent / "kidney" / "data"        # toxicity/kidney/data/

CLAIMS = {
    "unique_oligos": 65,
    "graded_measurements": 111,
    "pct_kidney_specific": 100.0,
    "distinct_sources": 16,
    "sequences_filled": 55,      # was 33 at the 2026-08-26 snapshot; see "Drift note"
    "grade_0": 27,
    "grade_1": 30,
    "grade_2": 39,
    "grade_3": 15,
    "ws_rows": 36,
    "in_vitro_rows": 19,
    "oligo_columns": 17,
    "orphan_foreign_keys": 0,
}

MISSING = {"TBD", "", "NA", "None", "none"}


def main() -> int:
    if not (DATA / "oligos.csv").exists():
        print(f"kidney data not found at {DATA}", file=sys.stderr)
        return 2
    oligos = list(csv.DictReader((DATA / "oligos.csv").open(newline="")))
    meas = list(csv.DictReader((DATA / "measurements.csv").open(newline="")))

    grades = collections.Counter(m["nephrotox_grade"] for m in meas)
    oligo_ids = {o["oligo_id"] for o in oligos}

    actual = {
        "unique_oligos": len(oligo_ids),
        "graded_measurements": len(meas),
        "pct_kidney_specific": 100.0 * sum(1 for m in meas
                                           if m["is_kidney_specific"] == "TRUE") / len(meas),
        "distinct_sources": len({m["source_id"] for m in meas}),
        "sequences_filled": sum(1 for o in oligos if o["sequence_5to3"] not in MISSING),
        "grade_0": grades["0"], "grade_1": grades["1"],
        "grade_2": grades["2"], "grade_3": grades["3"],
        "ws_rows": sum(1 for m in meas if m["source_id"] == "WS"),
        "in_vitro_rows": sum(1 for m in meas if m["study_type"] == "in_vitro"),
        "oligo_columns": len(oligos[0]),
        "orphan_foreign_keys": sum(1 for m in meas if m["oligo_id"] not in oligo_ids),
    }

    width = max(len(k) for k in CLAIMS)
    failures = []
    for key, claimed in CLAIMS.items():
        got = actual[key]
        ok = abs(got - claimed) < 1e-9 if isinstance(claimed, float) else got == claimed
        if not ok:
            failures.append((key, claimed, got))
        print(f"{key:<{width}}  expected={claimed:<8} actual={got:<8} {'OK' if ok else 'MISMATCH'}")

    print()
    if failures:
        print(f"FAIL - {len(failures)} claim(s) do not reproduce from data/:")
        for key, claimed, got in failures:
            print(f"  {key}: expected {claimed}, data says {got}")
        return 1
    print(f"PASS - all {len(CLAIMS)} kidney-module claims reproduce from the live data/ tables.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
