#!/usr/bin/env python3
"""Correct the 21 US 11,105,794 Table 1 rows: rat, not mouse; 15 days, not 7; dose 40 mg/kg.

MSR91-MSR111 (source_id=N3) are 19% of the dataset and were recorded as a 7-day
mouse study with an unknown dose. The patent's own method section for that table
says otherwise, and binds itself to Table 1 explicitly:

  "Purpose bred Wistar Han Crl : WI ( Han ) male rats obtained from Charles River
   Laboratories at 7 to 8 weeks of age were divided into groups of 4 (table 1,
   exp. A) or 8 (table 1, exp. B)"                          -- US 11,105,794 p.25

Three further statements in the same paragraph corroborate the species and the
duration, and publish the dose:

  "dosed at 40 mg / kg on days 1 and 8 ( 2.5 ml / kg ) in the intrascapular region"
  "urinary renal injury biomarkers were measured (Multiplex MAP *Rat* Kidney
   Toxicity Magnetic Bead Panel 2)"
  "On day 15 the rats were sacrificed"

The patent does elsewhere contain the phrase "seven day mouse study", but in a
prophetic passage about stereodefined phosphorothioate linkages that offers rat,
monkey, dog and pig as alternatives -- it is not the Table 1 experiment, and is the
likely origin of the error.

This matters beyond provenance: species is the axis the human/animal division is
built on, and these 21 rows are 40% of the animal side. Uncorrected they move the
animal distribution from mouse 9 / rat 29 to mouse 30 / rat 8.

Verified against sources/US11105794_in_vitro_nephrotox_assay_patent.pdf, in-repo.

Usage:  python scripts/fix_patent_species.py && python scripts/build_merged.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "data", "measurements.csv")

CORRECTION = {
    "species": ("mouse", "rat"),
    "system_model": ("mouse_7day_nephrotox_study", "rat_15day_nephrotox_study"),
    "exposure_duration": ("7_days", "15_days"),
    "dose_or_conc_value": ("TBD", "40"),
}
NOTE = ("species_duration_dose_corrected_2026-09_from_US11105794_p25_method_"
        "WistarHan_rats_dosed_40mgkg_days1and8_sacrificed_day15")


def main():
    with open(MEAS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = reader.fieldnames, list(reader)

    changed = skipped = 0
    for r in rows:
        if r["source_id"] != "N3":
            continue
        if r["species"] == "rat":                 # already corrected; re-runnable
            skipped += 1
            continue
        for col, (old, new) in CORRECTION.items():
            if r[col] != old:
                raise SystemExit(
                    f"{r['measurement_id']}: expected {col}={old!r}, found {r[col]!r} "
                    f"- refusing to overwrite an unexpected value"
                )
            r[col] = new
        assert r["dose_or_conc_unit"] == "mg/kg", r["measurement_id"]
        if NOTE not in r["notes"]:
            r["notes"] = f"{r['notes']};{NOTE}" if r["notes"].strip() else NOTE
        changed += 1

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"corrected {changed} N3 rows (skipped {skipped} already correct)")


if __name__ == "__main__":
    main()
