#!/usr/bin/env python3
"""Generate thrombocytopenia/data/oligotox_thrombo_merged.csv — a denormalized,
analysis-ready join of the two canonical thrombocytopenia tables on `oligo_id`.

One row per measurement, enriched with its oligo's design predictors, giving a
single flat "wide" table where each row carries both the predictors (sequence +
chemistry + design) and the graded outcome (thrombocytopenia_grade). Convenient
for EDA and predictive modeling — no join step required.

IMPORTANT: the two normalized tables (thrombocytopenia/data/oligos.csv,
thrombocytopenia/data/measurements.csv) remain the SOURCE OF TRUTH. This merged
file is a *generated, derived view* and should be regenerated with this script
after any change to the canonical tables — never edited by hand (denormalization
duplicates each oligo's design across its measurement rows).

Usage:  python3 scripts/build_merged_thrombo.py
"""
import csv, os

# Paths are anchored to the ENDPOINT folder that owns this script, so all
# thrombocytopenia artefacts stay inside thrombocytopenia/ and nothing is
# written outside it.
ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")
OLIGOS = os.path.join(BASE, "oligos.csv")
MEAS = os.path.join(BASE, "measurements.csv")
OUT = os.path.join(BASE, "oligotox_thrombo_merged.csv")

# oligo design predictors (all oligos.csv columns except the key and its notes)
OLIGO_PRED = ["oligo_name", "aliases", "oligo_class", "target_gene", "indication",
              "developer", "max_phase", "length_nt", "backbone_chemistry",
              "sugar_modifications", "gapmer_design", "conjugate", "ps_count",
              "sequence_5to3", "design_source"]
# measurement outcome/context columns (all measurements.csv columns except keys and notes)
MEAS_COLS = ["study_type", "species", "system_model", "tissue", "delivery_method",
             "dose_or_conc_value", "dose_or_conc_unit", "exposure_duration",
             "readout_category", "readout_name", "readout_value", "readout_unit",
             "effect_direction", "effect_vs_control", "thrombocytopenia_grade",
             "is_platelet_specific", "source_id", "source_ref", "source_table",
             "redistribution"]


def main():
    with open(OLIGOS, newline="", encoding="utf-8") as f:
        oligos = {r["oligo_id"]: r for r in csv.DictReader(f)}
    with open(MEAS, newline="", encoding="utf-8") as f:
        meas = list(csv.DictReader(f))

    # referential-integrity guard: every measurement must reference a known oligo
    orphans = [m["measurement_id"] for m in meas if m["oligo_id"] not in oligos]
    if orphans:
        raise SystemExit(
            f"ERROR: {len(orphans)} measurement(s) reference unknown oligo_id: {orphans[:5]}")

    header = (["measurement_id", "oligo_id"] + OLIGO_PRED + ["notes_oligo"]
              + MEAS_COLS + ["notes_measurement"])

    n = 0
    with open(OUT, "w", newline="", encoding="utf-8") as f:
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
