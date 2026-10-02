#!/usr/bin/env python3
"""Build the positive/negative control inventory Phase 2 requires to be reported.

WHY THIS EXISTS
  Phase 2's narrative document must open with "an executive summary of the
  dataset(s) generated, AND POSITIVE/NEGATIVE CONTROLS INCLUDED". Earlier
  reporting led with "zero qualified clinical negatives", which is true of a
  clinical NEGATIVE LABEL and false of CONTROLS -- and it read as though the
  dataset had none. It has several, and they are the strongest evidence in it.

  The two claims are different:
    - "no qualified clinical negative" = no compound may be labelled clinically
      safe. The scientist package rules CLEAN_CLINICAL_NEGATIVE "NOT YET
      AVAILABLE" and all 21 audited candidates ineligible. That stands.
    - "no controls" = false. Isosequential backbone pairs, vehicle/placebo arms,
      LNA-wing comparators and intended-pharmacology comparators are all present.

  This is a DERIVED VIEW. It adds no observation, no label and no adjudication;
  every row is computed from data/oligos.csv and data/measurements.csv.

Usage:  python3 scripts/build_controls_inventory.py
Writes: data/controls_inventory.csv
"""
import csv, os, re, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")


def rd(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def nseq(s):
    return re.sub(r"[^ACGTU]", "", (s or "").upper()).replace("U", "T")


def grade(r):
    try: return int(r["thrombocytopenia_grade"])
    except (ValueError, TypeError, KeyError): return 0


def main():
    O = {o["oligo_id"]: o for o in rd("oligos.csv")}
    M = rd("measurements.csv")
    by_o = collections.defaultdict(list)
    for m in M: by_o[m["oligo_id"]].append(m)

    rows = []

    def add(ctype, role, oid, n, what, permitted, prohibited, basis):
        o = O.get(oid, {})
        rows.append({
            "control_type": ctype, "control_role": role,
            "oligo_id": oid, "compound": o.get("oligo_name", ""),
            "sequence_5to3": o.get("sequence_5to3", ""),
            "backbone_chemistry": o.get("backbone_chemistry", ""),
            "ps_count": o.get("ps_count", ""),
            "n_measurement_rows": n,
            "max_grade_observed": (max(grade(r) for r in by_o[oid]) if by_o.get(oid) else ""),
            "controls_for": what, "permitted_use": permitted,
            "prohibited_use": prohibited, "basis": basis,
            "scientist_disposition": o.get("scientist_disposition", ""),
        })

    # ---- 1. isosequential backbone controls ------------------------------
    # The cleanest control design in the dataset: identical nucleotide sequence,
    # backbone is the only variable. This is a true matched negative control for
    # the phosphorothioate hypothesis.
    seq = collections.defaultdict(list)
    for o in O.values():
        s = nseq(o["sequence_5to3"])
        if len(s) >= 8: seq[s].append(o)
    for s, v in seq.items():
        ps = [x for x in v if (x["ps_count"] or "").isdigit()]
        if len(ps) < 2: continue
        hi, lo = max(ps, key=lambda x: int(x["ps_count"])), min(ps, key=lambda x: int(x["ps_count"]))
        if int(hi["ps_count"]) <= int(lo["ps_count"]): continue
        pair = f"{hi['oligo_name']} (PS {hi['ps_count']}) vs {lo['oligo_name']} (PS {lo['ps_count']})"
        add("isosequential_backbone_pair", "positive_arm", hi["oligo_id"], len(by_o[hi["oligo_id"]]),
            f"backbone effect, matched on sequence: {pair}",
            "Within-pair comparison of the backbone's contribution at a shared sequence.",
            "Do not read the low-PS arm as a clinical negative; it is an assay-level "
            "isosequential comparator, not a monitored clinical outcome.",
            "same normalised nucleotide sequence, differing ps_count")
        add("isosequential_backbone_pair", "negative_arm", lo["oligo_id"], len(by_o[lo["oligo_id"]]),
            f"backbone effect, matched on sequence: {pair}",
            "Within-pair comparator establishing the sequence alone is insufficient.",
            "Do not label clinically safe or universally inert.",
            "same normalised nucleotide sequence, differing ps_count")

    # ---- 2. LNA-wing comparators -----------------------------------------
    for o in O.values():
        nm = (o["oligo_name"] or "")
        if "LNA" not in nm.upper(): continue
        add("chemistry_variant_comparator", "variant_arm", o["oligo_id"], len(by_o[o["oligo_id"]]),
            "effect of adding LNA wings at a shared alternating-AC sequence",
            "Descriptive matched contrast of one named chemical factor.",
            "Not a clinical negative. Per scientist rule CTRL-R02, changing the "
            "sugar/backbone design invalidates transfer of a control's status.",
            "name carries an LNA designation against an unmodified sibling")

    # ---- 3. vehicle / control-arm rows -----------------------------------
    ctrl = [m for m in M if (m.get("dose_or_conc_value") or "") == "0"]
    g0 = sum(1 for m in ctrl if grade(m) == 0)
    byc = collections.Counter(m["oligo_id"] for m in ctrl)
    for oid, n in byc.most_common():
        add("vehicle_or_control_arm", "concurrent_control", oid, n,
            "concurrent unexposed/placebo comparison within the same study",
            "Context for the exposed arm in the same study. Scientist class "
            "PLACEBO_CONTROL is APPROVED_FOR_CONTEXT.",
            "Cannot supply sequence features and cannot serve as a sequence-level "
            "outcome label; a placebo arm has no construct.",
            "dose_or_conc_value == 0")

    # ---- 4. intended-pharmacology comparators ----------------------------
    sp = os.path.join(DATA, "studies.csv")
    if os.path.exists(sp):
        for s in rd("studies.csv"):
            if s.get("intended_pharmacology") == "yes" and s.get("oligo_id"):
                add("intended_pharmacology_comparator", "therapeutic_direction", s["oligo_id"],
                    int(s.get("n_measurement_rows") or 0),
                    "distinguishes a therapeutic platelet change from a toxic one",
                    "Shows the endpoint moving in the intended direction under exposure.",
                    "NEVER harvest as oligonucleotide toxicity. Scientist class "
                    "THERAPEUTIC_CORRECTION_OR_PRESERVATION is SUPPORT_ONLY.",
                    f"study registry: {s.get('intended_pharmacology_reason','')[:110]}")

    cols = list(rows[0].keys())
    with open(os.path.join(DATA, "controls_inventory.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

    agg = collections.Counter(r["control_type"] for r in rows)
    print(f"controls_inventory.csv — {len(rows)} control records")
    for k, v in agg.most_common(): print(f"  {v:4d}  {k}")
    print(f"\n  vehicle/control-arm rows total : {len(ctrl)} ({g0} at grade 0)")
    pairs = agg.get("isosequential_backbone_pair", 0) // 2
    print(f"  isosequential backbone pairs   : {pairs}")
    print(f"  distinct compounds serving as a control: {len({r['oligo_id'] for r in rows})}")
    print("\n  NOTE: a control is not a clinical negative. The scientist package records "
          "0 qualified\n        clinical negatives and that is unchanged by this file.")


if __name__ == "__main__":
    main()
