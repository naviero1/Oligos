#!/usr/bin/env python3
"""Build the positive/negative control inventory.

    python3 toxicity/coagulopathy/scripts/build_controls_inventory.py
    -> data/controls_inventory.csv

Why this exists. Crank's delegation of 2026-10-03, item 9, records that "kidney,
coagulopathy, hydrocephalus and cns-alternate have no control column at all" and that
Beebop's document skeletons (item 7) cannot be drafted without a control inventory. The
first half of that is no longer true for this endpoint — `control_class` was added to
measurements on 2026-10-03 — so this file publishes the inventory in the shape item 9 asks
for, to unblock item 7 rather than leave Beebop working from a superseded figure.

Phase 2 requires the narrative's executive summary to state "the dataset(s) generated, and
positive/negative controls included", and SCIENTIFIC_RULES.md §E adds two constraints that
shape this file: "Unsourced controls are not training rows" — a control enters training only
when its sequence, chemistry, assay and measured outcome are sourced — and human, human
ex vivo and animal evidence are never pooled, so every count is reported per lane.

One row per (control class × species lane × readout category). The honest headline is in the
`sequence_control` rows: a vehicle or a placebo does not separate a sequence effect from a
chemistry or formulation effect, and the dataset has very few controls that do.
"""
import csv, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"

ROLE = {
    "sequence_control": ("negative", "sequence-matched: scrambled, mismatch, sense-strand or "
                                     "reverse complement. The only control that separates a "
                                     "sequence effect from a chemistry or formulation effect"),
    "pharmacological_positive_control": ("positive", "a drug with a known effect on the assay "
                                                     "(heparin, enoxaparin, bivalirudin, warfarin, protamine)"),
    "placebo": ("negative", "matched placebo in a clinical study"),
    "vehicle_or_buffer": ("negative", "vehicle, buffer, saline or PBS. Controls for the "
                                      "delivery system, NOT for the sequence"),
    "untreated_or_predose": ("reference", "untreated or pre-dose. A reference point, not a "
                                          "treated comparator"),
    "active_comparator": ("comparator", "an active alternative therapy; not a control for the "
                                        "oligonucleotide's own effect"),
    "other_described_control": ("unclassified", "a control is described but does not match a "
                                                "known class; the description is kept verbatim on the row"),
    "no_control_described": ("none", "no control described by the source. These rows cannot "
                                     "support a control-referenced ratio"),
}


def main():
    D = list(csv.DictReader(open(os.path.join(DATA, "measurements.csv"), newline="", encoding="utf-8")))
    O = {o["oligo_id"]: o for o in csv.DictReader(open(os.path.join(DATA, "oligos.csv"), newline="", encoding="utf-8"))}
    M = list(csv.DictReader(open(os.path.join(DATA, "modifications.csv"), newline="", encoding="utf-8")))
    mo = {m["oligo_id"] for m in M}
    S = {s["source_id"]: s for s in csv.DictReader(open(os.path.join(DATA, "sources.csv"), newline="", encoding="utf-8"))}

    def lane(r):
        if r["human_system_subtype"] == "participant":
            return "human_participant"
        if r["human_system_subtype"] in ("primary_blood_or_plasma", "cells_or_tissue",
                                         "purified_or_recombinant_protein"):
            return "human_in_vitro"
        if r["species_class"] == "animal":
            return "animal"
        return "unresolved"

    groups = defaultdict(list)
    for r in D:
        groups[(r["control_class"], lane(r), r["readout_category"])].append(r)

    rows = []
    for (cls, ln, cat), rs in sorted(groups.items(), key=lambda x: (-len(x[1]), x[0])):
        role, desc = ROLE.get(cls, ("unclassified", ""))
        oids = {r["oligo_id"] for r in rs}
        # §E: a control is training-eligible only when sequence, chemistry, assay and outcome
        # are all sourced. Assay and outcome are present by construction on every row here,
        # so the binding constraints are sequence and position-resolved chemistry.
        elig = {o for o in oids
                if str(O.get(o, {}).get("sequence_5to3_asprinted", "")).strip() not in ("", NR, NA)
                and o in mo}
        srcs = {r["source_id"] for r in rs}
        rows.append({
            "control_class": cls,
            "control_role": role,
            "evidence_lane": ln,
            "readout_category": cat,
            "n_rows": len(rs),
            "n_compounds": len(oids),
            "n_compounds_sequence_and_position_chemistry_sourced": len(elig),
            "training_eligible_under_rules_E": "TRUE" if elig else "FALSE",
            "n_sources": len(srcs),
            "example_control_description": next((r["control_description"][:220] for r in rs
                                                 if str(r["control_description"]).strip() not in ("", NR, NA)), NR),
            "what_this_control_does": desc,
        })

    out = os.path.join(DATA, "controls_inventory.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    kc = Counter(r["control_class"] for r in D)
    neg = sum(v for k, v in kc.items() if ROLE.get(k, ("", ""))[0] == "negative")
    print(f"  controls inventory: {len(rows)} control-class x lane x readout groups")
    print(f"    positive controls      {kc.get('pharmacological_positive_control', 0):5d} rows")
    print(f"    SEQUENCE-MATCHED negative {kc.get('sequence_control', 0):5d} rows  <- the one that matters")
    print(f"    all negative-role rows {neg:5d} (vehicle, placebo, sequence)")
    print(f"    no control described   {kc.get('no_control_described', 0):5d} rows")
    elig = sum(1 for r in rows if r["training_eligible_under_rules_E"] == "TRUE")
    print(f"    groups whose compounds have sequence AND position chemistry sourced: {elig} of {len(rows)}")
    print(f"    compounds included as endpoint negative controls: "
          f"{sum(1 for s in S.values() if 'NEGATIVE CONTROL' in str(s['citation']).upper())}")
    print(f"  -> data/controls_inventory.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
