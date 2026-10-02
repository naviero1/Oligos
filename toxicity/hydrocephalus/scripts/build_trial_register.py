#!/usr/bin/env python3
"""
Builds data/trial_register.csv — the deduplicated, verified HUMAN CLINICAL TRIAL
register, and the first evidence table this release presents.

Why this table exists. The release could previously answer "how many measurement
rows" instantly and "how many actual trials" not at all: four different trial
figures appeared across its documents (161 / 159 / 155 / none) and qc/stats.json
held no trial counter. Oscar's standing rule is that a headline trial total counts
VERIFIED, DEDUPLICATED, ACTUAL HUMAN CLINICAL TRIALS — never measurement rows,
papers, participants, labels, cases, spontaneous reports or animal experiments.
This is the register that total is computed from, one row per trial.

It also separates two things that were conflated. A trial being IDENTIFIED is not
the same as a trial having an EVALUABLE hydrocephalus outcome: most trials here
contribute only the absence of a term from an adverse-event table, which is a
reported zero under 42 CFR 11.48(a)(4)(ii)(A) but is not a ventricular
assessment. `endpoint_evaluability` states which.

Overlapping cohorts are marked, not merged. Where a trial's own arm text names a
parent NCT that is also in this release, `extension_of` records it — those
participants are the same people, so the two trials' denominators must never be
added. Detection is textual and therefore a floor, not a complete list.

Output: data/trial_register.csv
Usage:  python3 scripts/build_trial_register.py   (after scripts/assemble.py)
"""
import csv
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

NCT_RE = re.compile(r"\bNCT\d{8}\b")


def main():
    reg = list(csv.DictReader(open(os.path.join(DATA, "trial_registry.csv"))))
    meas = list(csv.DictReader(open(os.path.join(DATA, "measurements.csv"))))

    trials = [r for r in reg if not r["excluded_reason"]]

    # A trial can contribute an outcome record WITHOUT posting results:
    # NCT05686551 (GENERATION HD2) carries a protocol-specified ventricular MRI
    # outcome that is planned and not yet reported, recorded deliberately because
    # the absence of protocol-specified imaging is this endpoint's central
    # ascertainment limitation. discover_ctgov_trials.py filters on hasResults, so
    # such a trial never reaches trial_registry.csv. The register must still cover
    # it, or the register is not a register of this release's trials.
    in_reg = {r["nct_id"] for r in trials}
    contributing = {r["source_id"] for r in meas
                    if r["study_type"] == "clinical_trial"
                    and r["source_id"].startswith("NCT")}
    for nct in sorted(contributing - in_reg):
        src = next(r for r in meas if r["source_id"] == nct)
        trials.append(dict(nct_id=nct, drug=src["oligo_name"],
                           route=src["delivery_route"], overall_status="NOT_REPORTED",
                           brief_title="(no results posted; see notes on its rows)",
                           conditions=src["indication_population"],
                           attribution_basis="measurement_row_only",
                           discovery="carried as a planned/unreported outcome",
                           excluded_reason=""))
    known = {r["nct_id"] for r in trials}

    rows_by_nct = defaultdict(list)
    for r in meas:
        if r["study_type"] == "clinical_trial" and r["source_id"].startswith("NCT"):
            rows_by_nct[r["source_id"]].append(r)

    out = []
    for t in trials:
        nct = t["nct_id"]
        rows = rows_by_nct.get(nct, [])
        arms = {r["arm_label"] for r in rows if r["arm_label"]}

        systematic = {r["assessment_type"] for r in rows
                      if r["assessment_type"] not in ("", "NOT_REPORTED",
                                                      "NOT_APPLICABLE")}
        tierA_pos = [r for r in rows if r["endpoint_tier"] == "A"
                     and r["ascertainment"] == "measured_positive"
                     and r["tox_axis"] == "ventricular_enlargement"]
        grades = [r["hydroceph_grade"] for r in rows if r["hydroceph_grade"]]

        planned = [r for r in rows if r["ascertainment"] == "not_assessed"]
        if not rows:
            evaluability = "identified_only_no_outcome_record"
        elif len(planned) == len(rows):
            evaluability = "planned_outcome_no_results_posted"
        elif tierA_pos:
            evaluability = "tier_A_event_observed"
        elif systematic:
            evaluability = "systematically_assessed_no_event"
        else:
            evaluability = "adverse_event_table_absence_only"

        # Overlapping cohorts: a parent NCT named in this trial's own arm text.
        parents = set()
        for r in rows:
            for blob in (r["arm_description"], r["arm_label"], r["notes"]):
                for hit in NCT_RE.findall(blob or ""):
                    if hit != nct and hit in known:
                        parents.add(hit)

        out.append(dict(
            nct_id=nct,
            compound=t["drug"],
            route=t["route"],
            overall_status=t["overall_status"],
            brief_title=t["brief_title"],
            conditions=t["conditions"],
            attribution_basis=t.get("attribution_basis", "NOT_REPORTED"),
            discovery=t.get("discovery", "NOT_REPORTED"),
            endpoint_evaluability=evaluability,
            assessment_types=";".join(sorted(systematic)) or "NOT_APPLICABLE",
            n_outcome_records=len(rows),
            n_arms=len(arms),
            tier_A_positive_rows=len(tierA_pos),
            max_hydroceph_grade=(max(grades) if grades else ""),
            extension_of=";".join(sorted(parents)) or "NOT_APPLICABLE",
            participants_overlap_warning=("TRUE" if parents else "FALSE"),
        ))

    out.sort(key=lambda r: (r["compound"].lower(), r["nct_id"]))
    cols = list(out[0])
    with open(os.path.join(DATA, "trial_register.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    ev = defaultdict(int)
    for r in out:
        ev[r["endpoint_evaluability"]] += 1
    overlap = sum(1 for r in out if r["participants_overlap_warning"] == "TRUE")
    print("wrote data/trial_register.csv: %d verified human clinical trials" % len(out))
    for k in sorted(ev, key=lambda k: -ev[k]):
        print("   %-38s %4d" % (k, ev[k]))
    print("   %-38s %4d" % ("marked as extensions of a listed trial", overlap))


if __name__ == "__main__":
    main()
