#!/usr/bin/env python3
"""
Builds the analysis set for modelling, at the correct grain.

The measurement table is NOT a modelling table, and using it as one would produce
a badly wrong model. Three reasons, each handled here:

1. **Rows are not independent.** One trial arm contributes a row per adverse-event
   term; one patient's episode contributes a row per measurement (that is what
   `event_cluster_id` marks). Treating them as independent observations inflates
   n by an order of magnitude and shrinks every confidence interval.

2. **The unit of exposure is the ARM, not the row.** A trial arm has a denominator
   (`n_at_risk`) and an event count. That is a binomial observation. Rows are the
   terms within it.

3. **`study_type` and `source_id` are shortcut predictors.** A model given them
   learns which register a row came from, not biology. The analysis set therefore
   keeps only `clinical_trial` rows with a real denominator, so that every
   observation is the same kind of thing.

Grain: one row per (trial, arm). Outcome: did that arm report at least one tier-A
event, and how many participants were affected, out of how many at risk.

Output: ml/analysis_set.csv
Usage:  python3 ml/build_analysis_set.py
"""
import csv
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")


def num(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def main():
    rows = list(csv.DictReader(open(os.path.join(DATA, "measurements.csv"))))
    oligos = {o["oligo_name"]: o for o in
              csv.DictReader(open(os.path.join(DATA, "oligos.csv")))}
    registry = {}
    reg_path = os.path.join(DATA, "trial_registry.csv")
    if os.path.exists(reg_path):
        registry = {r["nct_id"]: r for r in csv.DictReader(open(reg_path))}

    arms = defaultdict(lambda: dict(
        tierA_affected=0, tierB_affected=0, n_at_risk=None,
        tierA_terms=set(), grades=set(), rows=0,
        tierB_axes=set(), tierB_affected_nonproc=0))

    for r in rows:
        if r["study_type"] != "clinical_trial":
            continue
        n = num(r["n_at_risk"])
        a = num(r["n_affected"])
        if n is None or a is None or n == 0:
            continue
        key = (r["source_id"], r["arm_label"])
        rec = arms[key]
        rec["rows"] += 1
        rec["n_at_risk"] = max(rec["n_at_risk"] or 0, n)
        rec["oligo_name"] = r["oligo_name"]
        rec["arm_role"] = r["arm_role"]
        rec["delivery_route"] = r["delivery_route"]
        rec["indication"] = r["indication_population"]
        rec["subject_class"] = r["subject_class"]
        rec["nct"] = r["source_id"]
        rec["arm_label"] = r["arm_label"]
        if r["endpoint_tier"] == "A":
            rec["tierA_affected"] = max(rec["tierA_affected"], a)
            if a > 0:
                rec["tierA_terms"].add(r["readout_name"])
        else:
            rec["tierB_affected"] = max(rec["tierB_affected"], a)
            if a > 0:
                rec["tierB_axes"].add(r["tox_axis"])
                # A lumbar-puncture complication is a PROCEDURE outcome. 78.6% of
                # the tier-B positive arms carry it as their ONLY positive axis,
                # so a model scored on undifferentiated tier-B is largely learning
                # "was this arm lumbar-punctured" from its own route feature.
                if r["tox_axis"] != "delivery_procedure_complication":
                    rec["tierB_affected_nonproc"] = max(
                        rec["tierB_affected_nonproc"], a)
        if r["hydroceph_grade"]:
            rec["grades"].add(r["hydroceph_grade"])

    # ---- drop pooled arms that re-count their own siblings ------------------
    # ClinicalTrials.gov results tables often carry a "Total"/"Overall" column
    # ALONGSIDE the arms it sums. Keying on (trial, arm_label) ingested both, so
    # those participants were counted twice inside a single trial. The published
    # "36,324 participants at risk" exceeded the declared enrollment of the very
    # trials it was built from by 28%, which is arithmetically impossible.
    POOLED = re.compile(r"\b(total|overall|pooled|combined|all\s+participants)\b", re.I)
    by_trial = defaultdict(list)
    for key in arms:
        by_trial[key[0]].append(key)
    dropped_pooled = []
    for nct, keys in by_trial.items():
        if len(keys) < 2:
            continue
        for k in keys:
            if not POOLED.search(k[1] or ""):
                continue
            mine = arms[k]["n_at_risk"] or 0
            others = sum(arms[j]["n_at_risk"] or 0 for j in keys if j != k)
            # Only drop when it really is a sum of the siblings, not a cohort that
            # merely has "total" in its name.
            if mine and others and abs(mine - others) <= max(1, 0.02 * mine):
                dropped_pooled.append((k[0], k[1], mine))
                del arms[k]
    if dropped_pooled:
        print("  dropped %d pooled arms double-counting %d participants"
              % (len(dropped_pooled), sum(n for _, _, n in dropped_pooled)))
        for nct, lab, n in sorted(dropped_pooled, key=lambda x: -x[2])[:8]:
            print("     %-14s %-42s n=%d" % (nct, lab[:42], n))

    out = []
    for (nct, arm), rec in sorted(arms.items()):
        o = oligos.get(rec["oligo_name"], {})
        reg = registry.get(nct, {})
        is_control = rec["arm_role"] == "comparator"
        route = rec["delivery_route"]
        out.append(dict(
            nct_id=nct, arm_label=arm, oligo_name=rec["oligo_name"],
            arm_role=rec["arm_role"], is_comparator=int(is_control),
            n_at_risk=rec["n_at_risk"],
            tierA_affected=rec["tierA_affected"],
            tierB_affected=rec["tierB_affected"],
            tierA_event=int(rec["tierA_affected"] > 0),
            tierB_event=int(rec["tierB_affected"] > 0),
            tierB_axes=";".join(sorted(rec["tierB_axes"])) or "none",
            tierB_event_nonprocedure=int(rec["tierB_affected_nonproc"] > 0),
            tierA_terms=";".join(sorted(rec["tierA_terms"])) or "none",
            max_grade=(max(rec["grades"]) if rec["grades"] else ""),
            delivery_route=route,
            route_is_cns=int(route in ("intrathecal_lumbar",
                                       "intracerebroventricular")),
            indication=rec["indication"][:80],
            oligo_class=o.get("oligo_class", "NOT_REPORTED"),
            backbone_chemistry=o.get("backbone_chemistry", "NOT_REPORTED"),
            modification_pattern=o.get("modification_pattern", "NOT_REPORTED"),
            has_sequence=int(o.get("sequence_5to3_asprinted", "NOT_REPORTED")
                             not in ("NOT_REPORTED", "NOT_APPLICABLE")),
            trial_status=reg.get("overall_status", "NOT_REPORTED"),
            n_measurement_rows=rec["rows"],
        ))

    cols = list(out[0].keys())
    path = os.path.join(HERE, "analysis_set.csv")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    n_arms = len(out)
    n_trials = len({r["nct_id"] for r in out})
    n_part = sum(r["n_at_risk"] for r in out)
    print("wrote %s" % path)
    print("  %d arms across %d trials, %d participants at risk (arm-sum)"
          % (n_arms, n_trials, n_part))
    print("  arms with a tier-A event : %d" % sum(r["tierA_event"] for r in out))
    print("  arms with a tier-B event : %d" % sum(r["tierB_event"] for r in out))
    print("  CNS-route arms           : %d" % sum(r["route_is_cns"] for r in out))
    print("  comparator arms          : %d" % sum(r["is_comparator"] for r in out))
    print("  compression from measurements.csv: %d rows -> %d arms"
          % (sum(r["n_measurement_rows"] for r in out), n_arms))


if __name__ == "__main__":
    main()
