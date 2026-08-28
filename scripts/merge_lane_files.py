#!/usr/bin/env python3
"""Combine curation outputs from several agents/workflows into one payload for
scripts/assemble_thrombo.py.

Curation ran as three kinds of producer, each emitting a slightly different
envelope, and this normalizes them:

  1. the extraction workflow  -> {"lanes":[{lane, oligos, measurements, verified}]}
  2. the standalone lane agents -> {"lane":..., "oligos":[...], "measurements":[...]}
  3. the hand-curated label lane -> same as (1), from scripts/curate_labels_lane.py

Anything matching neither shape is reported and skipped rather than silently
dropped, so a malformed agent output is visible instead of quietly costing rows.

Usage:  python3 scripts/merge_lane_files.py out.json in1.json in2.json ...
"""
import json, sys


# ---------------------------------------------------------------------------
# DETERMINISTIC LANE PRECEDENCE.
#
# assemble_thrombo resolves a scalar conflict between two real values by keeping
# the FIRST one seen, so the merged output depended on the order lanes were passed
# in — globbing `lanes/*.json` gave a different oligos.csv than the ingest
# script's hand-written order. Same inputs, different result: a reproducibility
# defect, and one that quietly picked `TNFA` over the HGNC-canonical `TNF`.
#
# Lanes are therefore sorted by an explicit precedence before merging, so any
# caller gets identical output. Precedence runs from most-curated to bulk
# extraction: design records validated against WHO INN nomenclature and patent
# sequence listings outrank curator-verified regulatory rows, which outrank
# agent-extracted panels, which outrank the bulk workflow harvest.
LANE_PRECEDENCE = [
    "kidney_design_enrichment",      # INN- and patent-validated design metadata
    "curated_regulatory_labels",     # curator-verified, canonical vocabulary
    "preclinical_and_negatives",
    "patents_and_panels",
    "patents2_reviews_aptamers",
    "crooke2017_pooled_clinical",
]


def lane_rank(lane):
    name = lane.get("lane", "")
    for i, key in enumerate(LANE_PRECEDENCE):
        if name.startswith(key):
            return (i, name)
    return (len(LANE_PRECEDENCE), name)   # workflow:* and anything else, then by name

def normalize(path):
    """Return a list of lane dicts from one input file."""
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"  SKIP {path}: unreadable ({e})")
        return []

    if isinstance(d, dict) and isinstance(d.get("lanes"), list):
        lanes = d["lanes"]
    elif isinstance(d, dict) and ("measurements" in d or "oligos" in d):
        lanes = [d]
    elif isinstance(d, list):
        lanes = [x for x in d if isinstance(x, dict) and ("measurements" in x or "oligos" in x)]
    else:
        print(f"  SKIP {path}: unrecognized shape (top-level keys: "
              f"{list(d)[:8] if isinstance(d, dict) else type(d).__name__})")
        return []

    out = []
    for i, ln in enumerate(lanes):
        if not isinstance(ln, dict):
            continue
        out.append({
            "lane": ln.get("lane") or f"{path.split('/')[-1].rsplit('.', 1)[0]}#{i}",
            "oligos": ln.get("oligos") or [],
            "measurements": ln.get("measurements") or [],
            "verified": ln.get("verified"),
        })
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_path, inputs = sys.argv[1], sys.argv[2:]

    collected = []
    for p in inputs:
        collected.extend(normalize(p))

    # sort before reporting, so the printed order is the order actually merged
    lanes = sorted(collected, key=lane_rank)

    tot_o = tot_m = tot_v = 0
    for ln in lanes:
        no, nm = len(ln["oligos"]), len(ln["measurements"])
        nv = len(((ln.get("verified") or {}).get("verdicts")) or [])
        tot_o += no
        tot_m += nm
        tot_v += nv
        print(f"  {ln['lane']:<34} oligos={no:>4}  measurements={nm:>4}  verdicts={nv:>4}")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"lanes": lanes}, f)
    print(f"\nwrote {out_path}: {len(lanes)} lanes, {tot_o} oligo entries, "
          f"{tot_m} measurements, {tot_v} verdicts")
    if tot_m and not tot_v:
        print("NOTE: no verification verdicts present — assemble_thrombo.py will pass "
              "every row through as 'unverified'. Rows from producers that were not "
              "adversarially verified stay flagged in the assembly stats.")


if __name__ == "__main__":
    main()
