#!/usr/bin/env python3
"""Extract US 11,105,794 Table 2 -- the human in-vitro EGF panel -- into measurement rows.

Table 2 was acquired with the patent but never extracted (`SOURCES.md`: "Table 2
(per-compound in-vitro EGF) not yet extracted"). It is the highest-value unmined
source in the repository: 48 quantitative data points on **human** proximal tubule
cells, and the Phase 2 brief singles out in-vitro human systems as of particular
interest -- currently the dataset's smallest class at 17.1% of rows.

Design of the assay, from the patent's own text (p.25-27):
  - Two human systems: primary human PTEC, and the immortalised line PTEC-TERT1.
  - Gymnotic (naked, no transfection) exposure: "without assistance of delivery
    technology, herein termed gymnosis or gymnotic delivery".
  - Soluble EGF in the medium, read at day 3 and day 6, as % of the saline control.
    Rising extracellular EGF is the injury signal.
  - Concentrations 3 / 10 / 30 / 100 uM; values are "the average of three identical
    treatments", each reported with its SD.

The page's naive text layer interleaves the columns into an unusable flat number
stream, so this reads the LAYOUT-preserving extraction instead and re-parses it on
every run -- the numbers are never hand-transcribed. Parsed values are checked
against a small set of anchors taken from the patent's own prose before anything
is written.

GRADING. The rubric below is a curation decision, not the patent's. The patent
classifies compounds by *in vivo* toxicity (innocuous / medium / high) and states
its in-vitro significance calls in prose rather than per cell. Grades are
thresholded on fold-elevation over the saline control (=100%):

    < 200%      grade 0     within the range the innocuous compound reaches
    200-499%    grade 1
    500-1499%   grade 2
    >= 1500%    grade 3

The 200% floor is set so that compound 1-1, which the patent calls innocuous,
grades 0 at every concentration in both systems -- i.e. the threshold is anchored
to the patent's own negative control rather than chosen freely. Every row is
flagged `grade_provisional` like the rest of the dataset and needs scientific
sign-off; the raw % and SD are preserved in `readout_value` and `notes` so any
regrade can be done without returning to the PDF.

Usage:  python scripts/extract_patent_table2.py && python scripts/split_human_animal.py \
        && python scripts/build_merged.py
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "sources", "US11105794_in_vitro_nephrotox_assay_patent.pdf")
MEAS = os.path.join(ROOT, "data", "measurements.csv")

# patent compound number -> oligo_id already in oligos.csv, and the patent's in-vivo class
COMPOUND = {
    "1-1": ("OLG045", "innocuous"),
    "3-1": ("OLG047", "medium"),
    "4-1": ("OLG048", "high"),
}
# the four (value, SD) column pairs, in printed order
COLUMNS = [
    ("primary_human_PTEC", "3_days"),
    ("primary_human_PTEC", "6_days"),
    ("PTEC-TERT1", "3_days"),
    ("PTEC-TERT1", "6_days"),
]
# anchors from the patent's own prose / printed table, checked before writing
ANCHORS = {
    ("1-1", 3, "primary_human_PTEC", "3_days"): 95.0,
    ("3-1", 100, "primary_human_PTEC", "6_days"): 915.0,
    ("4-1", 100, "PTEC-TERT1", "6_days"): 8899.0,
    ("4-1", 30, "PTEC-TERT1", "6_days"): 8398.0,
}


def grade(pct):
    if pct < 200:
        return 0
    if pct < 500:
        return 1
    if pct < 1500:
        return 2
    return 3


def parse_table2():
    import pdfplumber
    with pdfplumber.open(PDF) as pdf:
        txt = pdf.pages[26].extract_text(layout=True) or ""
    start = txt.find("TABLE 2")
    if start < 0:
        raise SystemExit("TABLE 2 not found on page 27 - patent layout changed?")
    body = txt[start:start + 2000]

    rows, current = [], None
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("TABLE", "EGF concentration")):
            continue
        cm = re.search(r"\b([134]-1)\b", s)      # a compound label starts a new block
        if cm:
            current = cm.group(1)
            s = s[cm.end():]
        elif "saline" in s:                       # control row, no oligo_id to attach
            continue
        if current is None:
            continue
        nums = re.findall(r"\d+(?:\.\d+)?", s)
        if len(nums) != 9:                        # conc + 4x(value, SD)
            continue
        conc = int(float(nums[0]))
        vals = [float(x) for x in nums[1:]]
        for i, (model, day) in enumerate(COLUMNS):
            rows.append({
                "compound": current, "conc": conc, "model": model,
                "day": day, "pct": vals[i * 2], "sd": vals[i * 2 + 1],
            })
    return rows


def main():
    parsed = parse_table2()
    got = {(r["compound"], r["conc"], r["model"], r["day"]): r["pct"] for r in parsed}
    for k, want in ANCHORS.items():
        if got.get(k) != want:
            raise SystemExit(f"anchor check FAILED for {k}: parsed {got.get(k)!r}, patent prints {want}")
    expected = len(COMPOUND) * 4 * len(COLUMNS)
    if len(parsed) != expected:
        raise SystemExit(f"parsed {len(parsed)} cells, expected {expected} - refusing to write a partial table")
    print(f"parsed {len(parsed)} cells; {len(ANCHORS)} anchors match the printed table")

    with open(MEAS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, existing = reader.fieldnames, list(reader)
    if any(r["source_table"] == "Table 2" and r["source_id"] == "N3" for r in existing):
        print("Table 2 rows already present - nothing to do")
        return

    nmax = max(int(re.sub(r"\D", "", r["measurement_id"])) for r in existing)
    out = []
    for i, r in enumerate(sorted(parsed, key=lambda x: (x["compound"], x["model"], x["day"], x["conc"])), 1):
        oid, invivo = COMPOUND[r["compound"]]
        pct, g = r["pct"], grade(r["pct"])
        direction = "increase" if pct > 115 else "decrease" if pct < 85 else "no_change"
        row = {c: "" for c in fields}
        row.update({
            "measurement_id": f"MSR{nmax + i}",
            "oligo_id": oid,
            "study_type": "in_vitro",
            "species": "human",
            "subject_class": "human_invitro",
            "system_model": r["model"],
            "tissue": "proximal_tubule",
            "delivery_method": "gymnotic_free_uptake",
            "dose_or_conc_value": str(r["conc"]),
            "dose_or_conc_unit": "uM",
            "exposure_duration": r["day"],
            "readout_category": "injury_biomarker",
            "readout_name": "extracellular_EGF",
            "readout_value": f"{pct:g}",
            "readout_unit": "pct_saline_control",
            "effect_direction": direction,
            "effect_vs_control": f"{pct / 100:.2f}x",
            "nephrotox_grade": str(g),
            "is_kidney_specific": "TRUE",
            "source_id": "N3",
            "source_ref": "US11105794",
            "source_table": "Table 2",
            "redistribution": "public_domain",
            "notes": (f"patent_compound_{r['compound']};invivo_class_{invivo};SD_{r['sd']:g};"
                      f"gymnotic_naked_uptake;mean_of_3_identical_treatments;"
                      f"grade_from_fold_over_saline_rubric_see_scripts_extract_patent_table2;"
                      f"grade_provisional"),
        })
        out.append(row)

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(existing + out)
    print(f"appended {len(out)} human in-vitro rows ({out[0]['measurement_id']}..{out[-1]['measurement_id']})")
    dist = {}
    for r in out:
        dist[r["nephrotox_grade"]] = dist.get(r["nephrotox_grade"], 0) + 1
    print("  grade distribution:", dict(sorted(dist.items())))


if __name__ == "__main__":
    main()
