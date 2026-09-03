#!/usr/bin/env python3
"""Add the explicit `subject_class` divider to measurements.csv, and emit the
human-vs-animal bridge view.

`study_type` and `species` already separate human from animal cleanly, but the
division is implicit -- it takes a two-column join to recover, and the Phase 2
brief makes that division a scoring criterion ("datasets based on in vitro human
systems, or able to extrapolate data between in vitro human systems and animal
data, are of particular interest"). So it is materialised as one field:

    human_clinical  -- study_type=clinical,     species=human    (human trials)
    human_invitro   -- study_type=in_vitro,     species=human    (human cell systems)
    animal_invitro  -- study_type=in_vitro,     species!=human   (animal cell systems)
    animal_invivo   -- study_type=animal_invivo, species!=human  (animal studies)

Note that animal IN VITRO is a distinct class from animal in vivo, and collapsing
the two would be wrong: rat primary PTEC data (US 11,479,818 Table 5) is a cell
system, not a live study, and it pairs with the human cell systems rather than with
the in-vivo work. An earlier version of this script mapped every non-human row to
animal_invivo, which would have silently mislabelled those rows.

The value is DERIVED, never hand-entered, so it cannot drift from the two columns
it summarises; this script is re-runnable and asserts the mapping is total.

It also writes data/human_animal_bridge.csv: one row per oligo carrying BOTH human
and animal evidence. That set is the dataset's actual answer to the extrapolation
criterion, and it is small enough (9 oligos) that it deserves to be addressable
rather than recomputed by every consumer.

Usage:  python scripts/split_human_animal.py && python scripts/build_merged.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "data", "measurements.csv")
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")
BRIDGE = os.path.join(ROOT, "data", "human_animal_bridge.csv")


def classify(row):
    human = row["species"] == "human"
    st = row["study_type"]
    if st == "in_vitro":
        return "human_invitro" if human else "animal_invitro"
    if st == "animal_invivo":
        if human:
            raise ValueError(f"{row['measurement_id']}: species=human with study_type=animal_invivo")
        return "animal_invivo"
    if st == "clinical":
        if not human:
            raise ValueError(f"{row['measurement_id']}: non-human species with study_type=clinical")
        return "human_clinical"
    raise ValueError(
        f"{row['measurement_id']}: unexpected study_type={st!r} - classify explicitly before proceeding"
    )


def main():
    with open(MEAS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = list(reader.fieldnames), list(reader)

    for r in rows:
        r["subject_class"] = classify(r)

    if "subject_class" not in fields:                 # sit it beside `species`
        fields.insert(fields.index("species") + 1, "subject_class")

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    counts = {}
    for r in rows:
        counts[r["subject_class"]] = counts.get(r["subject_class"], 0) + 1
    print("subject_class assigned:")
    for k in ("human_clinical", "human_invitro", "animal_invitro", "animal_invivo"):
        print(f"  {k:<16}{counts.get(k, 0):>4}")
    assert sum(counts.values()) == len(rows), "unclassified rows remain"

    # ---- bridge view: oligos with evidence on BOTH sides of the divide ----
    oligos = {r["oligo_id"]: r for r in csv.DictReader(open(OLIGOS, newline=""))}
    per = {}
    for r in rows:
        per.setdefault(r["oligo_id"], {}).setdefault(r["subject_class"], []).append(r)

    out = []
    for oid, groups in sorted(per.items()):
        human = [x for k in ("human_clinical", "human_invitro") for x in groups.get(k, [])]
        animal = [x for k in ("animal_invivo", "animal_invitro") for x in groups.get(k, [])]
        if not (human and animal):
            continue
        hmax = max(int(x["nephrotox_grade"]) for x in human)
        amax = max(int(x["nephrotox_grade"]) for x in animal)
        ol = oligos[oid]
        out.append({
            "oligo_id": oid,
            "oligo_name": ol["oligo_name"],
            "oligo_class": ol["oligo_class"],
            "sequence_known": "TRUE" if ol["sequence_5to3"].strip() not in ("TBD", "", "NA") else "FALSE",
            "n_human_clinical": len(groups.get("human_clinical", [])),
            "n_human_invitro": len(groups.get("human_invitro", [])),
            "n_animal_invitro": len(groups.get("animal_invitro", [])),
            "n_animal_invivo": len(groups.get("animal_invivo", [])),
            "human_max_grade": hmax,
            "animal_max_grade": amax,
            "concordance": ("concordant" if hmax == amax
                            else "animal_over_predicts" if amax > hmax
                            else "animal_under_predicts"),
            "human_species_models": ";".join(sorted({x["system_model"] for x in human})),
            "animal_species": ";".join(sorted({x["species"] for x in animal})),
        })

    with open(BRIDGE, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"\nwrote {BRIDGE}: {len(out)} oligos with paired human+animal evidence")
    for k in ("concordant", "animal_over_predicts", "animal_under_predicts"):
        print(f"  {k:<24}{sum(1 for r in out if r['concordance'] == k)}")


if __name__ == "__main__":
    main()
