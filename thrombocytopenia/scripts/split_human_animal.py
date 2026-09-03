#!/usr/bin/env python3
"""Split the thrombocytopenia measurements into human and animal evidence, and
identify the compounds that bridge the two.

The Phase 2 announcement states that datasets "based on in vitro human systems or
able to **extrapolate data between in vitro human systems and animal data** are of
particular interest". This script makes that property explicit and auditable
rather than something a reader has to reconstruct:

  data/measurements_human.csv    every row whose subject is human
  data/measurements_animal.csv   every row whose subject is an animal species
  data/bridge_human_animal.csv   one row per COMPOUND measured in BOTH, with its
                                 human and animal grades side by side

The bridge file is the point. A dataset that merely contains human rows and animal
rows does not support extrapolation; a dataset where the SAME compound is
characterised on both sides does. That set is what a cross-species model can
actually be trained and validated on, so its size is a headline property worth
reporting honestly.

Rows that are neither (pooled `multi_species` findings, or rows whose species is
NA) are excluded from both splits and counted, never silently assigned to a side.

Usage:  python3 scripts/split_human_animal.py
"""
import csv, os, collections, statistics

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")


def main():
    with open(os.path.join(BASE, "oligos.csv"), newline="", encoding="utf-8") as f:
        oligos = {r["oligo_id"]: r for r in csv.DictReader(f)}
    with open(os.path.join(BASE, "measurements.csv"), newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols, meas = rdr.fieldnames, list(rdr)

    human = [m for m in meas if (m.get("subject_class") or "").startswith("human")]
    animal = [m for m in meas if (m.get("subject_class") or "").startswith("animal")]
    other = [m for m in meas if m not in human and m not in animal]

    for name, rows in (("measurements_human.csv", human),
                       ("measurements_animal.csv", animal)):
        with open(os.path.join(BASE, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"wrote data/{name:<28} {len(rows):>5} rows")

    # --- the bridge: compounds characterised on BOTH sides ---------------------
    def grades(rows):
        g = [int(r["thrombocytopenia_grade"]) for r in rows]
        return (len(g), statistics.mean(g) if g else float("nan"), max(g) if g else "")

    by_h = collections.defaultdict(list)
    by_a = collections.defaultdict(list)
    for m in human:
        by_h[m["oligo_id"]].append(m)
    for m in animal:
        by_a[m["oligo_id"]].append(m)
    bridge = sorted(set(by_h) & set(by_a),
                    key=lambda oid: -(len(by_h[oid]) + len(by_a[oid])))

    bcols = ["oligo_id", "oligo_name", "oligo_class", "backbone_chemistry", "ps_count",
             "conjugate", "sequence_5to3", "n_human_rows", "human_mean_grade",
             "human_max_grade", "n_animal_rows", "animal_mean_grade", "animal_max_grade",
             "animal_species", "grade_gap_animal_minus_human"]
    with open(os.path.join(BASE, "bridge_human_animal.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=bcols)
        w.writeheader()
        for oid in bridge:
            o = oligos.get(oid, {})
            hn, hm, hx = grades(by_h[oid])
            an, am, ax = grades(by_a[oid])
            w.writerow({
                "oligo_id": oid, "oligo_name": o.get("oligo_name", "?"),
                "oligo_class": o.get("oligo_class", ""),
                "backbone_chemistry": o.get("backbone_chemistry", ""),
                "ps_count": o.get("ps_count", ""), "conjugate": o.get("conjugate", ""),
                "sequence_5to3": o.get("sequence_5to3", ""),
                "n_human_rows": hn, "human_mean_grade": f"{hm:.2f}", "human_max_grade": hx,
                "n_animal_rows": an, "animal_mean_grade": f"{am:.2f}", "animal_max_grade": ax,
                "animal_species": ";".join(sorted({r.get("species", "") for r in by_a[oid]})),
                "grade_gap_animal_minus_human": f"{am - hm:+.2f}",
            })
    print(f"wrote data/{'bridge_human_animal.csv':<28} {len(bridge):>5} compounds "
          f"measured in BOTH")

    print()
    print(f"  human rows   {len(human):>5}   ({len({m['oligo_id'] for m in human})} compounds)")
    print(f"  animal rows  {len(animal):>5}   ({len({m['oligo_id'] for m in animal})} compounds)")
    print(f"  neither      {len(other):>5}   (pooled multi-species / species NA — "
          f"excluded from both, never assigned)")
    print()
    print("  human subject_class :",
          dict(collections.Counter(m["subject_class"] for m in human)))
    print("  animal subject_class:",
          dict(collections.Counter(m["subject_class"] for m in animal)))
    if bridge:
        gaps = [statistics.mean([int(r["thrombocytopenia_grade"]) for r in by_a[o]])
                - statistics.mean([int(r["thrombocytopenia_grade"]) for r in by_h[o]])
                for o in bridge]
        over = sum(1 for g in gaps if g > 0)
        print()
        print(f"  CROSS-SPECIES BRIDGE: {len(bridge)} compounds have both human and "
              f"animal evidence.")
        mg = statistics.mean(gaps)
        print(f"  Animal grade exceeds human in {over}/{len(bridge)} compounds; "
              f"mean gap {mg:+.2f}.")
        # State the direction the data actually shows. The literature reports that
        # animal toxicology OVER-predicts human platelet effects for 2'-MOE ASOs, so
        # it is tempting to narrate a positive gap — but this bridge set is small and
        # grade is confounded with study type (severe events are seen in trials, not
        # in dishes), so the sign here is not evidence either way and must not be
        # dressed up as confirmation.
        print("  NOTE: this is a descriptive summary, not a translation result. The set")
        print("  is small, and grade is partly confounded with study type, so the sign")
        print("  of this gap should not be read as confirming or refuting the reported")
        print("  animal over-prediction for 2'-MOE ASOs. It marks where the comparison")
        print("  can be made, which is the dataset's contribution.")


if __name__ == "__main__":
    main()
