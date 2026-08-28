#!/usr/bin/env python3
"""Emit the OligoTox-Thrombocytopenia distribution tables as Markdown.

The README record-counter and the METHODOLOGY variable-distribution tables are
generated from the canonical CSVs by this script rather than hand-transcribed, so
the documented numbers cannot drift from the data. Re-run after every ingestion
round and paste the output into the docs (or diff it against them).

Usage:  python3 scripts/report_thrombo.py
"""
import csv, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "thrombocytopenia", "data")


def load(name):
    with open(os.path.join(BASE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def dist(rows, col, sep=None):
    c = collections.Counter()
    for r in rows:
        v = (r.get(col) or "TBD").strip()
        if sep and sep in v:
            for p in v.split(sep):
                if p.strip():
                    c[p.strip()] += 1
        else:
            c[v] += 1
    return c


def fmt(c, top=None):
    items = c.most_common(top)
    return " · ".join(f"{k} {v}" for k, v in items)


def main():
    oligos = load("oligos.csv")
    meas = load("measurements.csv")

    print("## Record counter\n")
    print("| | Count |")
    print("|---|------|")
    print(f"| Unique oligos (`oligos.csv`) | **{len(oligos)}** |")
    print(f"| Measurement rows (`measurements.csv`) | **{len(meas)}** |")
    ps = sum(1 for m in meas if m["is_platelet_specific"] == "TRUE")
    print(f"| — of which strict-platelet | **{ps}** |")
    print(f"| — of which adjacent-haematology (flagged) | **{len(meas) - ps}** |")
    g = dist(meas, "thrombocytopenia_grade")
    print(f"| Grade distribution (0/1/2/3) | {' / '.join(str(g.get(str(i), 0)) for i in range(4))} |")
    print(f"| Distinct target genes | **{len([k for k in dist(oligos, 'target_gene') if k not in ('TBD', 'NA')])}** |")
    print(f"| Distinct sources (`source_ref`) | **{len(dist(meas, 'source_ref'))}** |")
    seq = sum(1 for o in oligos if o["sequence_5to3"] not in ("", "TBD"))
    print(f"| Oligos with sequence (not TBD) | **{seq} / {len(oligos)}** |")

    print("\n## Independent (predictor) variables — `oligos.csv`\n")
    print("| Variable | Distribution |")
    print("|----------|--------------|")
    for label, col in [("Modality (`oligo_class`)", "oligo_class"),
                       ("Backbone (`backbone_chemistry`)", "backbone_chemistry"),
                       ("Conjugate", "conjugate"),
                       ("Development stage (`max_phase`)", "max_phase")]:
        print(f"| **{label}** | {fmt(dist(oligos, col))} |")
    print(f"| **Sugar modifications** | {fmt(dist(oligos, 'sugar_modifications', sep=';'), 10)} |")
    print(f"| **Sequence available** | {seq} / {len(oligos)} (rest `TBD`, never guessed) |")

    print("\n## Dependent (indicator) variables — `measurements.csv`\n")
    print("| Variable | Distribution |")
    print("|----------|--------------|")
    print(f"| **`thrombocytopenia_grade`** | {' · '.join(f'{i}: {g.get(str(i), 0)}' for i in range(4))} |")
    for label, col in [("Study type", "study_type"), ("Species", "species"),
                       ("Delivery route", "delivery_method"),
                       ("Readout category", "readout_category"),
                       ("Redistribution", "redistribution")]:
        print(f"| **{label}** | {fmt(dist(meas, col))} |")
    print(f"| **Platelet-specific** | TRUE {ps} / {len(meas)} |")

    print("\n## Top readouts\n")
    for k, v in dist(meas, "readout_name").most_common(20):
        print(f"- {k}: {v}")

    print("\n## Rows per oligo (top 20)\n")
    byo = collections.Counter(m["oligo_id"] for m in meas)
    names = {o["oligo_id"]: o["oligo_name"] for o in oligos}
    for k, v in byo.most_common(20):
        print(f"- {names.get(k, k)} ({k}): {v}")

    print("\n## Sources by row count\n")
    for k, v in dist(meas, "source_ref").most_common(30):
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
