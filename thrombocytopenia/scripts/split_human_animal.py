#!/usr/bin/env python3
"""Split the thrombocytopenia measurements into human and animal evidence, ENRICH
both with their oligo's design metadata, identify the compounds that bridge the
two, and emit a compact compound-level structure-activity view.

WHY THE SPLITS ARE ENRICHED, NOT RAW
  `measurements.csv` is normalised: it carries `oligo_id`, not the sequence. That
  is correct for a canonical table but wrong for the file people actually read.
  The human subset is the one scientists work from, and it is useless without the
  sequence and the toxicity score in the same row — nobody should have to perform
  a join to answer "what does this compound look like and what did it do?".
  So the human and animal exports are DENORMALISED: every oligo design field is
  carried alongside every measurement field.

OUTPUTS
  data/measurements_human.csv    human rows, design fields joined in (sequence first)
  data/measurements_animal.csv   animal rows, same shape
  data/bridge_human_animal.csv   compounds measured in BOTH, human vs animal side by side
  data/germans_analysis.csv      one row per compound: oligo · sequence · modification · toxicity

Rows that are neither human nor animal (pooled `multi_species`, or species NA) are
excluded from both splits and counted, never silently assigned to a side.

Usage:  python3 scripts/split_human_animal.py
"""
import csv, os, collections, statistics

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")

# Column order for the enriched splits. Identity and the two things the reader
# always needs — SEQUENCE and TOXICITY GRADE — come first, before the long tail of
# context, so they are visible without scrolling.
LEAD = ["measurement_id", "oligo_id", "oligo_name", "sequence_5to3",
        "thrombocytopenia_grade", "modification_map", "gapmer_design",
        "sugar_modifications", "backbone_chemistry", "ps_count", "conjugate",
        "length_nt", "oligo_class", "target_gene"]


def load():
    with open(os.path.join(BASE, "oligos.csv"), newline="", encoding="utf-8") as f:
        orows = list(csv.DictReader(f))
    oligos = {r["oligo_id"]: r for r in orows}
    ocols = list(orows[0].keys())
    with open(os.path.join(BASE, "measurements.csv"), newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        return oligos, ocols, rdr.fieldnames, list(rdr)


def enriched_columns(ocols, mcols):
    """LEAD columns first, then every remaining oligo and measurement column."""
    rest_o = [c for c in ocols if c not in LEAD]
    rest_m = [c for c in mcols if c not in LEAD]
    # disambiguate the two `notes` columns rather than letting one silently win
    cols = list(LEAD)
    for c in rest_o:
        cols.append("oligo_notes" if c == "notes" else c)
    for c in rest_m:
        cols.append("measurement_notes" if c == "notes" else c)
    return cols


def enrich(m, oligos, ocols, mcols, cols):
    o = oligos.get(m["oligo_id"], {})
    row = {}
    for c in cols:
        if c == "oligo_notes":
            row[c] = o.get("notes", "")
        elif c == "measurement_notes":
            row[c] = m.get("notes", "")
        elif c in mcols and c not in ("notes",):
            row[c] = m.get(c, "")
        elif c in ocols and c not in ("notes",):
            row[c] = o.get(c, "")
        else:
            row[c] = m.get(c, o.get(c, ""))
    return row


def write(path, cols, rows):
    with open(os.path.join(BASE, path), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote data/{path:<30} {len(rows):>5} rows × {len(cols)} cols")


def main():
    oligos, ocols, mcols, meas = load()
    cols = enriched_columns(ocols, mcols)

    human = [m for m in meas if (m.get("subject_class") or "").startswith("human")]
    animal = [m for m in meas if (m.get("subject_class") or "").startswith("animal")]
    other = len(meas) - len(human) - len(animal)

    write("measurements_human.csv", cols,
          [enrich(m, oligos, ocols, mcols, cols) for m in human])
    write("measurements_animal.csv", cols,
          [enrich(m, oligos, ocols, mcols, cols) for m in animal])

    # ---- cross-species bridge -------------------------------------------------
    def stats(rows):
        g = [int(r["thrombocytopenia_grade"]) for r in rows]
        return len(g), (statistics.mean(g) if g else float("nan")), (max(g) if g else "")

    by_h, by_a = collections.defaultdict(list), collections.defaultdict(list)
    for m in human:
        by_h[m["oligo_id"]].append(m)
    for m in animal:
        by_a[m["oligo_id"]].append(m)
    bridge = sorted(set(by_h) & set(by_a), key=lambda k: -(len(by_h[k]) + len(by_a[k])))

    bcols = ["oligo_id", "oligo_name", "oligo_class", "backbone_chemistry", "ps_count",
             "conjugate", "sequence_5to3", "n_human_rows", "human_mean_grade",
             "human_max_grade", "n_animal_rows", "animal_mean_grade", "animal_max_grade",
             "animal_species", "grade_gap_animal_minus_human"]
    brows = []
    for oid in bridge:
        o = oligos.get(oid, {})
        hn, hm, hx = stats(by_h[oid])
        an, am, ax = stats(by_a[oid])
        brows.append({"oligo_id": oid, "oligo_name": o.get("oligo_name", "?"),
                      "oligo_class": o.get("oligo_class", ""),
                      "backbone_chemistry": o.get("backbone_chemistry", ""),
                      "ps_count": o.get("ps_count", ""), "conjugate": o.get("conjugate", ""),
                      "sequence_5to3": o.get("sequence_5to3", ""),
                      "n_human_rows": hn, "human_mean_grade": f"{hm:.2f}", "human_max_grade": hx,
                      "n_animal_rows": an, "animal_mean_grade": f"{am:.2f}", "animal_max_grade": ax,
                      "animal_species": ";".join(sorted({r.get("species", "") for r in by_a[oid]})),
                      "grade_gap_animal_minus_human": f"{am - hm:+.2f}"})
    write("bridge_human_animal.csv", bcols, brows)

    # ---- German's analysis: compound · sequence · modification · toxicity ------
    # A compact structure-activity view for scientific review: one row per compound,
    # the chemistry that defines it, and what it actually did — with the HUMAN
    # evidence broken out separately, because that is the subset that matters most
    # and averaging it into the animal data would hide it.
    by_o = collections.defaultdict(list)
    for m in meas:
        by_o[m["oligo_id"]].append(m)

    gcols = ["oligo_name", "sequence_5to3", "modification_summary", "modification_map",
             "gapmer_design", "sugar_modifications", "backbone_chemistry", "ps_count",
             "conjugate", "length_nt", "oligo_class", "target_gene",
             "max_toxicity_grade", "mean_toxicity_grade", "n_measurements",
             "human_max_grade", "human_mean_grade", "n_human", "n_animal",
             "worst_finding", "evidence_span"]
    grows = []
    for oid, rows in by_o.items():
        o = oligos.get(oid, {})
        g = [int(r["thrombocytopenia_grade"]) for r in rows]
        h = [r for r in rows if (r.get("subject_class") or "").startswith("human")]
        a = [r for r in rows if (r.get("subject_class") or "").startswith("animal")]
        hg = [int(r["thrombocytopenia_grade"]) for r in h]
        worst = max(rows, key=lambda r: int(r["thrombocytopenia_grade"]))

        # one human-readable string describing the chemistry, since "the modification
        # to that sequence" lives across four columns in the canonical schema
        parts = []
        if o.get("gapmer_design") not in ("", "TBD", "NA"):
            parts.append(o["gapmer_design"])
        if o.get("sugar_modifications") not in ("", "TBD", "NA"):
            parts.append(o["sugar_modifications"].replace(";", "+"))
        if o.get("backbone_chemistry") not in ("", "TBD", "NA"):
            parts.append(o["backbone_chemistry"])
        if o.get("ps_count") not in ("", "TBD", "NA"):
            parts.append(f"{o['ps_count']} PS")
        if o.get("conjugate") not in ("", "TBD", "NA", "none"):
            parts.append(f"{o['conjugate']}-conjugated")
        grows.append({
            "oligo_name": o.get("oligo_name", "?"),
            "sequence_5to3": o.get("sequence_5to3", "TBD"),
            "modification_summary": " · ".join(parts) if parts else "TBD",
            "modification_map": o.get("modification_map", "TBD"),
            "gapmer_design": o.get("gapmer_design", ""),
            "sugar_modifications": o.get("sugar_modifications", ""),
            "backbone_chemistry": o.get("backbone_chemistry", ""),
            "ps_count": o.get("ps_count", ""), "conjugate": o.get("conjugate", ""),
            "length_nt": o.get("length_nt", ""), "oligo_class": o.get("oligo_class", ""),
            "target_gene": o.get("target_gene", ""),
            "max_toxicity_grade": max(g), "mean_toxicity_grade": f"{statistics.mean(g):.2f}",
            "n_measurements": len(g),
            "human_max_grade": (max(hg) if hg else ""),
            "human_mean_grade": (f"{statistics.mean(hg):.2f}" if hg else ""),
            "n_human": len(h), "n_animal": len(a),
            "worst_finding": f"{worst.get('readout_name','')} = {worst.get('readout_value','')}"
                             f" {worst.get('readout_unit','')}".strip(),
            "evidence_span": "human+animal" if h and a else ("human" if h else
                             ("animal" if a else "other")),
        })
    # worst compounds first, then most-evidenced — the reading order a reviewer wants
    grows.sort(key=lambda r: (-r["max_toxicity_grade"],
                              -float(r["mean_toxicity_grade"]), -r["n_measurements"]))
    write("germans_analysis.csv", gcols, grows)

    print()
    print(f"  human   {len(human):>5} rows · {len({m['oligo_id'] for m in human})} compounds")
    print(f"  animal  {len(animal):>5} rows · {len({m['oligo_id'] for m in animal})} compounds")
    print(f"  neither {other:>5} rows  (pooled multi-species / species NA)")
    print(f"  bridge  {len(brows):>5} compounds measured in BOTH")
    print(f"  German's analysis: {len(grows)} compounds; "
          f"{sum(1 for r in grows if r['sequence_5to3'] not in ('TBD','NA',''))} with a sequence, "
          f"{sum(1 for r in grows if r['max_toxicity_grade'] == 3)} reaching grade 3")


if __name__ == "__main__":
    main()
