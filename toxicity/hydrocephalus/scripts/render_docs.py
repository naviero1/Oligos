#!/usr/bin/env python3
"""
Renders the generated statistics block in README.md from qc/stats.json.

The sibling kidney dataset's deck claimed "every number regenerates from data/"
while every count in it was typed inline, and a review found four mutually
incompatible figures for one statistic across four documents. This script is the
mechanism that makes the equivalent claim true here: the block between the
GENERATED markers is machine-written from the QC suite's own output, so a count
in the documentation cannot drift from the data.

Usage: python3 scripts/render_docs.py    (run after qc/validate.py)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BEGIN = ("<!-- BEGIN GENERATED: qc/validate.py writes qc/stats.json; "
         "scripts/render_docs.py renders this block. Do not hand-edit. -->")
END = "<!-- END GENERATED -->"

TIER_A = ("hydrocephalus (communicating, obstructive or normal-pressure), "
          "ventriculomegaly / ventricular dilatation, shunt or drain placement")
TIER_B = ("raised intracranial pressure, papilloedema, aseptic or chemical "
          "meningitis, arachnoiditis, CSF leak or protein rise, post-lumbar-"
          "puncture syndrome")


def table(title, mapping, key_header="Value", note=""):
    lines = ["| %s | Rows |" % key_header, "|---|---:|"]
    for k, v in mapping.items():
        lines.append("| %s | %s |" % (k if k else "*(not graded)*", v))
    body = "\n".join(lines)
    return "**%s**%s\n\n%s\n" % (title, (" — " + note) if note else "", body)


def main():
    stats_path = os.path.join(ROOT, "qc", "stats.json")
    if not os.path.exists(stats_path):
        sys.exit("qc/stats.json not found — run python3 qc/validate.py first")
    s = json.load(open(stats_path))

    parts = []
    parts.append(
        "| | Count |\n|---|---:|\n"
        "| Measurement rows | **%(n_measurements)d** |\n"
        "| Oligonucleotides described | **%(n_oligos)d** |\n"
        "| — of which carry at least one measurement | %(n_oligos_with_measurements)d |\n"
        "| Distinct sources | %(n_sources)d |\n"
        "| Tier-A rows with a positive finding | %(tier_A_positive)d |\n"
        "| Tier-A rows that are explicit measured negatives | %(tier_A_null)d |\n"
        "| Grade-3 (severe) rows | %(grade3_rows)d |\n"
        "| Oligonucleotides with a published sequence | %(oligos_with_sequence)d |\n"
        "| QC checks run / failed | %(checks_run)d / %(checks_failed)d |\n" % s)

    parts.append(table(
        "Endpoint tier", s["by_endpoint_tier"], "Tier",
        "**A** = " + TIER_A + ". **B** = " + TIER_B + "."))
    parts.append(table("Study type", s["by_study_type"], "Study type"))
    parts.append(table(
        "Ascertainment", s["by_ascertainment"], "Ascertainment",
        "how the endpoint's presence or absence was established. A grade of 0 is "
        "only permitted where this is `measured_null`"))
    parts.append(table(
        "Attribution, as stated by the source", s["by_attribution"], "Attribution",
        "what the SOURCE concluded about causation. `not_discussed` dominates "
        "because registry and pharmacovigilance records carry no causality "
        "assessment at all — that is a property of those sources, not an omission "
        "here"))
    parts.append(table(
        "Toxicity axis", s["by_tox_axis"], "Axis",
        "`disease_background_rate` rows carry no compound; "
        "`delivery_procedure_complication` rows are attributable to the lumbar "
        "puncture rather than to any molecule"))
    parts.append(table(
        "Severity grade", s["by_grade"], "`hydroceph_grade`",
        "rubric in [`SCHEMA.md`](SCHEMA.md#hydroceph_grade-rubric-03); all grades "
        "are provisional"))
    parts.append(table(
        "Delivery route", s["by_delivery_route"], "Route",
        "systemically dosed oligonucleotides are included as a deliberate route "
        "contrast"))
    parts.append(table("Readout category", s["by_readout_category"], "Category"))
    parts.append(table(
        "Redistribution rights", s["by_redistribution"], "Rights",
        "tracked per row"))

    clusters = s.get("multi_row_event_clusters", {})
    if clusters:
        rows = "\n".join("| `%s` | %d |" % (k, v) for k, v in sorted(clusters.items()))
        parts.append(
            "**Event clusters** — rows sharing an `event_cluster_id` describe **one** "
            "clinical episode and must not be counted as independent events.\n\n"
            "| `event_cluster_id` | Rows |\n|---|---:|\n%s\n" % rows)

    top = list(s["rows_per_source"].items())[:10]
    rows = "\n".join("| `%s` | %d |" % (k, v) for k, v in top)
    parts.append("**Largest sources** (top 10 of %d)\n\n| `source_id` | Rows |\n|---|---:|\n%s\n"
                 % (s["n_sources"], rows))

    block = BEGIN + "\n\n" + "\n".join(parts) + "\n" + END

    path = os.path.join(ROOT, "README.md")
    text = open(path).read()
    if BEGIN not in text or END not in text:
        sys.exit("generated markers not found in README.md")
    pre = text[:text.index(BEGIN)]
    post = text[text.index(END) + len(END):]
    open(path, "w").write(pre + block + post)
    print("rendered %d statistics tables into README.md" % len(parts))


if __name__ == "__main__":
    main()
