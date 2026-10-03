#!/usr/bin/env python3
"""Build the Characterization Gap Register required by SCIENTIFIC_RULES.md §F.

    python3 toxicity/coagulopathy/scripts/build_characterization_gap_register.py
    -> data/characterization_gap_register.csv

§F: "Where sources do not supply analytical identity or purity, those fields must remain
NOT_REPORTED unless primary CMC, synthesis, HPLC, MS, CGE or lot-level records are recovered.
NOT_REPORTED is the correct value, not a failure state. [...] Alongside it, record in the
Characterization Gap Register what is missing, why, what was attempted, and what would close
it. The field value and the register are both required: the value states the truth, the
register discharges the requirement."

This endpoint had the values and not the register. The register is derived, not asserted:
every row's `why` and `what_would_close_it` follows from the compound's own characterisation
state and from what the 2026-10-03 regulatory quality-section sweep actually found, so it
cannot drift from the data it describes.

One row per compound × missing field. A compound with nothing missing produces no rows.
"""
import csv, json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"

# field -> (what it is, what document class would close it)
FIELDS = {
    "purity_pct": ("tested-batch purity value",
                   "a certificate of analysis, a lot-release record, or the CMC module of a "
                   "marketing application (Module 3.2.S.4)"),
    "identity_confirmation": ("analytical identity confirmation",
                              "the drug-substance specification or characterisation section "
                              "of a regulatory quality assessment, or a publication's methods"),
    "purity_method": ("the analytical method used to determine purity",
                      "the drug-substance specification, or a publication's synthesis and "
                      "purification methods"),
    "endotoxin_level": ("endotoxin level",
                        "the drug-substance or finished-product specification; endotoxin "
                        "limits appear in the EPAR quality sections already held and were "
                        "not extracted — this is recoverable without new acquisition"),
    "sequence_5to3_asprinted": ("the printed sequence",
                                "a publication, patent example, sponsor protocol chemistry "
                                "section, or label DESCRIPTION section that prints it"),
    "position_chemistry": ("position-resolved chemistry (one row per nucleotide)",
                           "a source that prints the sequence with a chemistry legend, or a "
                           "sponsor protocol chemistry section giving the gapmer architecture"),
}


def nf(v):
    return bool(v) and str(v).strip() not in ("", NR, NA)


def main():
    O = list(csv.DictReader(open(os.path.join(DATA, "oligos.csv"), newline="", encoding="utf-8")))
    D = list(csv.DictReader(open(os.path.join(DATA, "measurements.csv"), newline="", encoding="utf-8")))
    M = list(csv.DictReader(open(os.path.join(DATA, "modifications.csv"), newline="", encoding="utf-8")))
    mo = {m["oligo_id"] for m in M}
    part = {r["oligo_id"] for r in D if r["human_system_subtype"] == "participant"}
    vitro = {r["oligo_id"] for r in D if r["human_system_subtype"] in
             ("primary_blood_or_plasma", "cells_or_tissue", "purified_or_recombinant_protein")}
    swept = set()
    cp = os.path.join(ROOT, "sources", "characterisation.json")
    if os.path.exists(cp):
        swept = {r.get("oligo_id") for r in json.load(open(cp, encoding="utf-8"))["records"]}

    rows = []
    for o in O:
        oid = o["oligo_id"]
        lane = ("human_participant" if oid in part else
                "human_in_vitro" if oid in vitro else "animal_or_other")
        for field, (what, closes) in FIELDS.items():
            have = (oid in mo) if field == "position_chemistry" else nf(o.get(field))
            if have:
                continue

            # WHY, derived from this compound's own state rather than asserted
            if field == "purity_pct" and o.get("purity_limits_redacted") == "TRUE":
                why = ("the regulatory document NAMES the purity test and WITHHOLDS the numeric "
                       "acceptance limit, which public assessment reports routinely do. The value "
                       "exists; it is not published")
                attempted = ("2026-10-03 regulatory quality-section sweep of the held EMA assessment "
                             "reports and FDA integrated reviews: the test is named, the limit is not printed")
                closes_this = ("the unredacted CMC module (3.2.S.4.1 specification), which is not "
                               "public. A certificate of analysis for a specific lot would also close it")
            elif oid in swept:
                why = ("the compound's regulatory quality section was read on 2026-10-03 and does "
                       "not state this field")
                attempted = ("2026-10-03 regulatory quality-section sweep (11 extraction passes, "
                             "11 independent verification passes) over the documents held for this compound")
                closes_this = closes
            elif field in ("sequence_5to3_asprinted", "position_chemistry"):
                why = "no held source prints it for this compound"
                attempted = ("2026-10-02 twenty-resource search round (16 of 20 resources searched; "
                             "see research/2026-10-02/search_coverage_log.csv). Sponsor protocol "
                             "chemistry sections were identified as an unexploited route but have "
                             "not been ingested")
                closes_this = closes
            else:
                why = ("no held source states it, and this compound has no regulatory quality "
                       "document in the corpus — it is characterised only by the publication that "
                       "reports its coagulation result")
                attempted = ("2026-10-03 regulatory quality-section sweep found no quality document "
                             "for this compound; 2026-10-02 search round found no characterisation source")
                closes_this = closes

            rows.append({
                "oligo_id": oid,
                "oligo_name": o["oligo_name"],
                "evidence_lane": lane,
                "missing_field": field,
                "what_is_missing": what,
                "why_it_is_missing": why,
                "what_was_attempted": attempted,
                "what_would_close_it": closes_this,
                "field_value_in_dataset": NR,
                "max_phase": o.get("max_phase", NR),
                "n_measurements": o.get("n_measurements", "0"),
            })

    out = os.path.join(DATA, "characterization_gap_register.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    c = Counter(r["missing_field"] for r in rows)
    lanes = Counter(r["evidence_lane"] for r in rows)
    print(f"  {len(rows)} gap records over {len({r['oligo_id'] for r in rows})} compounds")
    for k, v in c.most_common():
        print(f"    {v:4d}  {k}")
    print("  by lane:", dict(lanes))
    red = sum(1 for r in rows if "WITHHOLDS" in r["why_it_is_missing"])
    print(f"  of the purity gaps, {red} are a WITHHELD LIMIT rather than an absent value")
    print(f"  -> data/characterization_gap_register.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
