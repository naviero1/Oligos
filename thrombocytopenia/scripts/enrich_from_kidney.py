#!/usr/bin/env python3
"""Emit an oligo-only lane carrying design metadata from the sister
OligoTox-Kidney dataset, for compounds that also appear in the thrombocytopenia
measurements.

Why this exists. The two datasets in this repository cover different endpoints
but overlap heavily in *compounds* — the same marketed oligonucleotides appear in
both. The kidney dataset's `data/oligos.csv` records were validated against WHO
INN chemical nomenclature and patent sequence listings (see ../schema.md
"Data-dictionary QC log"), including a duplex reverse-complement self-check. Re-
deriving them here would risk reintroducing an error that dataset has already
ruled out, and would waste the validation work.

Two concrete gaps this closes:
  - `max_phase` drifts stale in older sources. Crooke 2017 lists inotersen as
    phase 1 because it predates the 2018 approval, and mipomersen as phase 3
    though Kynamro was approved in 2013. The kidney records carry the current
    stage with its label provenance, and assemble_thrombo's max_phase merge takes
    the most advanced value, so the stale figure loses.
  - Sequences left `TBD` here are often already published and validated there.

This emits oligos ONLY — never measurements. Kidney-endpoint outcomes are not
platelet outcomes and must not leak across endpoints. Each enriched row records
in `notes` that its design metadata was reused, so the provenance is not lost.

Usage:
  python3 scripts/assemble_thrombo.py <merged.json>          # first pass
  python3 scripts/enrich_from_kidney.py > kidney_lane.json   # then
  python3 scripts/merge_lane_files.py merged2.json <merged.json> kidney_lane.json
  python3 scripts/assemble_thrombo.py merged2.json           # re-assemble
"""
import csv, json, os, re, sys

# Paths are anchored to the ENDPOINT folder that owns this script, so all
# thrombocytopenia artefacts stay inside thrombocytopenia/ and nothing is
# written outside it.
ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ENDPOINT)   # repository root — READ-ONLY from here
KIDNEY = os.path.join(REPO, "data", "oligos.csv")
THROMBO_MEAS = os.path.join(ENDPOINT, "data", "measurements.csv")
THROMBO_OLIGOS = os.path.join(ENDPOINT, "data", "oligos.csv")


def norm(n):
    return re.sub(r"[^a-z0-9]", "", (n or "").lower())


def main():
    with open(KIDNEY, newline="", encoding="utf-8") as f:
        kidney = {norm(r["oligo_name"]): r for r in csv.DictReader(f)}

    # names already present in the thrombocytopenia dataset
    present = {}
    with open(THROMBO_OLIGOS, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            present[norm(r["oligo_name"])] = r["oligo_name"]

    out = []
    for k, name in sorted(present.items(), key=lambda kv: kv[1].lower()):
        kr = kidney.get(k)
        if not kr:
            continue
        row = {c: kr[c] for c in kr if c != "oligo_id"}
        # keep the thrombocytopenia dataset's own spelling of the join key
        row["oligo_name"] = name
        row["notes"] = (kr.get("notes", "")
                        + ";design_metadata_reused_from_OligoTox-Kidney_oligos.csv"
                        ";validated_there_against_WHO_INN_nomenclature_and_patent_sequence_listings")
        out.append(row)

    json.dump({"lane": "kidney_design_enrichment", "oligos": out, "measurements": []},
              sys.stdout, indent=1)
    print(f"\n# enriched {len(out)} compound(s) shared with the kidney dataset",
          file=sys.stderr)


if __name__ == "__main__":
    main()
