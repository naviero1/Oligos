#!/usr/bin/env python3
"""Extract US 11,479,818 Table 5 -- rat primary PTEC, EGFR and KIM-1 -- into measurements.

`SOURCES.md` had N4 acquired but unmined ("mine for any unique compounds"). Table 5
is its most valuable table: 9 of the panel's compounds at 3 concentrations, read on
three biomarkers including **KIM-1**, the canonical kidney injury marker, which the
dataset otherwise carries only from Sandelius.

The cells are RAT primary PTEC, not human -- the patent is explicit: "the EGFR
biomarker in rat primary PTEC cells can be used to predict the in vivo toxicity of
oligonucleotides. The cells are however more sensitive to oligonucleotide treatment,
and it is therefore recommended to perform the evaluation ... at lower oligonucleotide
concentrations than for human PTEC and PTEC-TERT1 cells."

That makes these rows `animal_invitro`, a class the dataset did not previously have,
and it is why they are worth the effort: the same compounds now carry human in-vitro
(US 11,105,794 Table 2), rat in-vitro (here) and rat in-vivo (US 11,105,794 Table 1)
evidence. For compounds 1-1 / 3-1 / 4-1 that is a three-way human-cell / animal-cell /
animal-animal comparison from one laboratory, which is the strongest extrapolation
material in the dataset.

NORMALISATION DIFFERS FROM TABLE 2. These values are "% 1-1" -- normalised to the
innocuous reference compound, not to saline. Recorded in `readout_unit` as
`pct_compound_1-1_reference` so the two patents' numbers are never silently pooled.

GRADING (a curation decision, stated so it can be re-derived):
  KIM-1 mRNA and protein rise with injury:   <200 / 200-499 / 500-1499 / >=1500 -> 0/1/2/3
  EGFR mRNA falls with injury:               >70 / 40-70 / 20-39 / <20        -> 0/1/2/3
Both are anchored on compound 1-1, which is 100 by construction here and therefore
grades 0 on every readout -- the same anchoring principle used for Table 2.
All rows are `grade_provisional`.

Usage:  python scripts/extract_n4_table5.py && python scripts/split_human_animal.py \
        && python scripts/build_merged.py
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "sources", "US11479818_in_vitro_nephrotox_assay_patent_EGFR.pdf")
MEAS = os.path.join(ROOT, "data", "measurements.csv")

COMPOUND = {
    "1-1": ("OLG045", "innocuous"), "3-1": ("OLG047", "medium"), "4-1": ("OLG048", "high"),
    "15-1": ("OLG059", "medium_high"), "16-1": ("OLG060", "medium_high"),
    "17-1": ("OLG061", "high"), "18-1": ("OLG062", "low"),
    "19-1": ("OLG063", "low_medium"), "19-2": ("OLG064", "high"),
}
READOUTS = [("EGFR_mRNA", "decrease"), ("KIM-1_mRNA", "increase"), ("KIM-1_protein", "increase")]
ANCHORS = {  # (compound, conc, readout) -> printed value
    ("1-1", 1, "EGFR_mRNA"): 100.0,
    ("3-1", 10, "KIM-1_mRNA"): 3622.0,
    ("19-2", 10, "KIM-1_protein"): 712.0,
    ("4-1", 100, "EGFR_mRNA"): 11.0,
}


def grade(readout, val):
    if readout == "EGFR_mRNA":                       # falls with injury
        return 0 if val > 70 else 1 if val >= 40 else 2 if val >= 20 else 3
    return 0 if val < 200 else 1 if val < 500 else 2 if val < 1500 else 3


def parse():
    import pdfplumber
    with pdfplumber.open(PDF) as pdf:
        t = pdf.pages[29].extract_text(layout=True) or ""
    i = t.find("TABLE 5")
    if i < 0:
        raise SystemExit("TABLE 5 not found on page 30 - patent layout changed?")
    out, current = [], None
    for line in t[i:i + 2600].splitlines():
        s = line.strip()
        if not s or s.startswith(("TABLE", "US 11,4", "EGFR and KIM", "In vivo", "toxicity")):
            continue
        cm = re.search(r"\b(\d{1,2}-\d)\b(?!\d)", s)
        # a compound token is one of the known labels; anything else is a data-only line
        if cm and cm.group(1) in COMPOUND:
            current = cm.group(1)
            s = s[cm.end():]
        if current is None:
            continue
        nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s)]
        if len(nums) not in (6, 7):     # conc + 3x(value[,SD]); one cell lacks its SD
            continue
        conc, rest = int(nums[0]), nums[1:]
        vals, sds, k = [], [], 0
        for r in range(3):
            vals.append(rest[k]); k += 1
            # the final readout may be missing its SD on one row
            if k < len(rest) and not (r == 2 and len(rest) == 5):
                sds.append(rest[k]); k += 1
            else:
                sds.append(None)
        for (name, direction), v, sd in zip(READOUTS, vals, sds):
            out.append({"compound": current, "conc": conc, "readout": name,
                        "direction": direction, "val": v, "sd": sd})
    return out


def main():
    parsed = parse()
    got = {(r["compound"], r["conc"], r["readout"]): r["val"] for r in parsed}
    for k, want in ANCHORS.items():
        if got.get(k) != want:
            raise SystemExit(f"anchor FAILED {k}: parsed {got.get(k)!r}, patent prints {want}")
    expected = len(COMPOUND) * 3 * 3
    if len(parsed) != expected:
        raise SystemExit(f"parsed {len(parsed)}, expected {expected} - refusing to write a partial table")
    print(f"parsed {len(parsed)} cells; {len(ANCHORS)} anchors match the printed table")

    with open(MEAS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = reader.fieldnames, list(reader)
    if any(r["source_id"] == "N4" for r in rows):
        print("N4 rows already present - nothing to do")
        return

    n = max(int(re.sub(r"\D", "", r["measurement_id"])) for r in rows)
    new = []
    for i, r in enumerate(sorted(parsed, key=lambda x: (x["compound"], x["readout"], x["conc"])), 1):
        oid, invivo = COMPOUND[r["compound"]]
        g = grade(r["readout"], r["val"])
        if r["readout"] == "EGFR_mRNA":
            direction = "decrease" if r["val"] < 85 else "no_change" if r["val"] <= 115 else "increase"
        else:
            direction = "increase" if r["val"] > 115 else "no_change" if r["val"] >= 85 else "decrease"
        row = {c: "" for c in fields}
        row.update({
            "measurement_id": f"MSR{n + i}", "oligo_id": oid,
            "study_type": "in_vitro", "species": "rat", "subject_class": "animal_invitro",
            "system_model": "rat_primary_PTEC", "tissue": "proximal_tubule",
            "delivery_method": "gymnotic_free_uptake",
            "dose_or_conc_value": str(r["conc"]), "dose_or_conc_unit": "uM",
            "exposure_duration": "3_days",
            "readout_category": "injury_biomarker",
            "readout_name": r["readout"], "readout_value": f"{r['val']:g}",
            "readout_unit": "pct_compound_1-1_reference",
            "effect_direction": direction,
            "effect_vs_control": f"{r['val'] / 100:.2f}x",
            "nephrotox_grade": str(g), "is_kidney_specific": "TRUE",
            "source_id": "N4", "source_ref": "US11479818", "source_table": "Table 5",
            "redistribution": "public_domain",
            "notes": (f"patent_compound_{r['compound']};invivo_class_{invivo};"
                      f"SD_{'NA' if r['sd'] is None else format(r['sd'], 'g')};"
                      "normalised_to_compound_1-1_NOT_saline_do_not_pool_with_N3_Table2;"
                      "rat_cells_more_sensitive_than_human_per_patent;"
                      "grade_from_rubric_see_scripts_extract_n4_table5;grade_provisional"),
        })
        new.append(row)

    with open(MEAS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows + new)
    print(f"appended {len(new)} rat in-vitro rows ({new[0]['measurement_id']}..{new[-1]['measurement_id']})")
    dist = {}
    for r in new:
        dist[r["nephrotox_grade"]] = dist.get(r["nephrotox_grade"], 0) + 1
    print("  grade distribution:", dict(sorted(dist.items())))


if __name__ == "__main__":
    main()
