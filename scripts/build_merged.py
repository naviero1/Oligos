#!/usr/bin/env python3
"""Generate data/oligotox_kidney_merged.csv — a denormalized, analysis-ready join
of the two canonical tables on `oligo_id`.

One row per measurement (111), enriched with its oligo's design predictors, giving
a single flat "wide" table where each row carries both the predictors (sequence +
chemistry + design) and the graded outcome (nephrotox_grade). Convenient for EDA
and predictive modeling — no join step required.

IMPORTANT: the two normalized tables (data/oligos.csv, data/measurements.csv) remain
the SOURCE OF TRUTH. This merged file is a *generated, derived view* and should be
regenerated with this script after any change to the canonical tables — never edited
by hand (denormalization duplicates each oligo's design across its measurement rows).

Usage:  python scripts/build_merged.py
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")
MEAS   = os.path.join(ROOT, "data", "measurements.csv")
OUT    = os.path.join(ROOT, "data", "oligotox_kidney_merged.csv")

# Column lists are DERIVED from the actual CSV headers, never hardcoded: a hardcoded
# list silently drops any column added to a canonical table (which is how the
# sequence-provenance columns went missing from this view once already).
# Convention: the key columns and `notes` are placed explicitly; everything else
# carries through in file order.
def _passthrough(fieldnames, exclude):
    return [c for c in fieldnames if c not in exclude]

def main():
    orx = csv.DictReader(open(OLIGOS, newline=""))
    oligos = {r["oligo_id"]: r for r in orx}
    mrx = csv.DictReader(open(MEAS, newline=""))
    meas = list(mrx)

    # oligo design predictors = every oligos.csv column except the key and its notes
    OLIGO_PRED = _passthrough(orx.fieldnames, {"oligo_id", "notes"})
    # measurement outcome/context = every measurements.csv column except the keys and its notes
    MEAS_COLS = _passthrough(mrx.fieldnames, {"measurement_id", "oligo_id", "notes"})

    # referential-integrity guard: every measurement must reference a known oligo
    orphans = [m["measurement_id"] for m in meas if m["oligo_id"] not in oligos]
    if orphans:
        raise SystemExit(f"ERROR: {len(orphans)} measurement(s) reference unknown oligo_id: {orphans[:5]}")

    header = (["measurement_id", "oligo_id"] + OLIGO_PRED + ["notes_oligo"]
              + MEAS_COLS + ["notes_measurement"])

    n = 0
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for m in meas:
            o = oligos[m["oligo_id"]]
            row = [m["measurement_id"], m["oligo_id"]]
            row += [o[c] for c in OLIGO_PRED]
            row += [o["notes"]]
            row += [m[c] for c in MEAS_COLS]
            row += [m["notes"]]
            w.writerow(row)
            n += 1

    print(f"wrote {OUT}: {n} rows x {len(header)} columns")

if __name__ == "__main__":
    main()
