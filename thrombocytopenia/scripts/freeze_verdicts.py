#!/usr/bin/env python3
"""Re-key verdict files from volatile measurement_ids to a stable NATURAL KEY.

Verifiers address rows by `measurement_id`, but those ids are assigned by sort
order at assembly time. Re-assembling after ingesting a new lane renumbers them,
which would make every stored verdict point at the wrong row — silently
discarding hard-won verification work, or worse, applying a correction to an
unrelated measurement.

This resolves each verdict's id against the CURRENT tables and stamps the row's
natural key onto it:

    (oligo_name, source_ref, source_table, readout_name, dose_or_conc_value)

That tuple is stable across renumbering because it is drawn from the row's own
content. Run this BEFORE re-assembling; `apply_verdicts.py` then matches on the
natural key and ignores the stale id.

Usage:  python3 scripts/freeze_verdicts.py verdicts1.json [verdicts2.json ...]
        (rewrites each file in place, adding a "natural_key" to every verdict)
"""
import csv, json, os, re, sys

# Paths are anchored to the ENDPOINT folder that owns this script, so all
# thrombocytopenia artefacts stay inside thrombocytopenia/ and nothing is
# written outside it.
ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def natural_key(row, names):
    return "|".join([
        norm(names.get(row["oligo_id"], "")),
        norm(row.get("source_ref")),
        norm(row.get("source_table")),
        norm(row.get("readout_name")),
        norm(row.get("dose_or_conc_value")),
    ])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(os.path.join(BASE, "oligos.csv"), newline="", encoding="utf-8") as f:
        names = {r["oligo_id"]: r["oligo_name"] for r in csv.DictReader(f)}
    with open(os.path.join(BASE, "measurements.csv"), newline="", encoding="utf-8") as f:
        rows = {r["measurement_id"]: r for r in csv.DictReader(f)}

    for p in sys.argv[1:]:
        d = json.load(open(p, encoding="utf-8"))
        n_ok = n_miss = 0
        for v in d.get("verdicts") or []:
            r = rows.get(v.get("measurement_id"))
            if not r:
                n_miss += 1
                continue
            v["natural_key"] = natural_key(r, names)
            n_ok += 1
        json.dump(d, open(p, "w", encoding="utf-8"))
        print(f"  {os.path.basename(p):<28} keyed {n_ok}, unresolved {n_miss}")
    print("\nVerdicts are now re-appliable after a re-assembly.")


if __name__ == "__main__":
    main()
