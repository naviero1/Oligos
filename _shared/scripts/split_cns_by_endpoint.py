#!/usr/bin/env python3
"""Partition the CNS corpus into its two NCATS endpoint folders.

The CNS curation was carried out as ONE corpus covering two of the Challenge's
named toxicities. Every row declares which one it serves through
`challenge_priority`, so the partition is read off the data rather than inferred:

    challenge_priority == 'high_hydrocephalus'  ->  hydrocephalus/
    everything else                             ->  chronic-neurotoxicity/

The split is exhaustive and disjoint: no measurement appears in both folders, and
the two row counts sum to the corpus total. `cns_oligos.csv` is filtered per side
to the oligos its own measurements reference, so each folder is a self-contained
two-table dataset. A molecule may legitimately appear in both oligo tables — an
oligo is a compound identity, not a toxicity observation.

Inputs are the corpus files as curated on branch
`claude/oligo-cns-toxicity-dataset-tijib6` (data/cns_oligos.csv,
data/cns_measurements.csv). Re-run after any change to them.

Usage:  python _shared/scripts/split_cns_by_endpoint.py <cns_oligos.csv> <cns_measurements.csv>
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HYDRO_KEY = "high_hydrocephalus"
TARGETS = {
    "hydrocephalus":         lambda r: r["challenge_priority"] == HYDRO_KEY,
    "chronic-neurotoxicity": lambda r: r["challenge_priority"] != HYDRO_KEY,
}

def write(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)

def main(oligos_path, meas_path):
    oligos = list(csv.DictReader(open(oligos_path, newline="")))
    meas = list(csv.DictReader(open(meas_path, newline="")))
    by_id = {o["oligo_id"]: o for o in oligos}

    orphans = sorted({m["oligo_id"] for m in meas} - set(by_id))
    if orphans:
        raise SystemExit(f"ERROR: {len(orphans)} measurement(s) reference unknown oligo_id: {orphans[:5]}")

    total = 0
    for folder, keep in TARGETS.items():
        sub = [m for m in meas if keep(m)]
        used = [by_id[i] for i in dict.fromkeys(m["oligo_id"] for m in sub)]
        n = write(os.path.join(ROOT, folder, "data", "measurements.csv"), meas[0].keys(), sub)
        k = write(os.path.join(ROOT, folder, "data", "oligos.csv"), oligos[0].keys(), used)
        print(f"{folder:24s} {n:5d} measurements  {k:4d} oligos")
        total += n

    if total != len(meas):
        raise SystemExit(f"ERROR: partition is not exhaustive: {total} != {len(meas)}")
    print(f"{'partition total':24s} {total:5d} == corpus {len(meas)}  (disjoint, exhaustive)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
