#!/usr/bin/env python3
"""
Deterministic extraction of PRE-SPECIFIED VENTRICULAR OUTCOME MEASURES from
ClinicalTrials.gov results, as distinct from adverse-event tables.

Why this is a separate component from extract_ctgov.py. An adverse-event count
is a clinician noticing something and coding it; a pre-specified outcome measure
is a quantity the protocol required to be measured in every participant, on a
schedule, by an instrument. For hydrocephalus the difference is decisive: these
are the only rows in the dataset where the ventricles were actually measured
rather than incidentally observed, and they are the only continuous ones.

Selection is an EXPLICIT ALLOW-LIST, not a pattern match, because a pattern for
"CSF" over this field sweeps in cerebrospinal-fluid pharmacokinetics and
neurofilament biomarkers, which are drug exposure and neuronal injury — neither
is a CSF-dynamics endpoint. Every entry below was read before being listed.

Output: data/_ctgov_outcome_measurements.csv

Usage: python3 scripts/extract_ctgov_outcomes.py
"""
import csv
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "sources", "raw")
DATA = os.path.join(ROOT, "data")
TODAY = date.today().isoformat()

# (nct, exact outcome title, oligo, tier, readout_category, tox_axis, readout_name,
#  comparator group id or None)
ALLOW = [
    ("NCT02519036",
     "Ventricular Volume as Assessed by Structural Magnetic Resonance Imaging (MRI)",
     "tominersen", "A", "ventricular_morphometry", "ventricular_enlargement",
     "ventricular_volume_MRI", "OG000"),
    ("NCT03342053",
     "Mean Percentage Change in Ventricular Volume Boundary Shift Integral From "
     "Baseline to 15 Months",
     "tominersen", "A", "ventricular_morphometry", "ventricular_enlargement",
     "ventricular_volume_boundary_shift_integral_pct_change", None),
]

# A trial where ventricular imaging for hydrocephalus is a PRE-SPECIFIED PRIMARY
# outcome but results are not yet posted. Recorded as not_assessed with no grade:
# it is evidence about ascertainment, not about the endpoint.
PLANNED = [
    ("NCT05686551", "tominersen",
     "DB Period: Change From Baseline in Structural Magnetic Resonance Imaging (MRI) "
     "Assessing Any New Abnormalities Including Radiographic Features Consistent With "
     "Hydrocephalus and Other Relevant MRI Safety Findings"),
]


def load(nct):
    with open(os.path.join(RAW, "ctgov_%s.json" % nct)) as fh:
        return json.load(fh)


def main():
    rows = []
    for nct, title, oligo, tier, cat, axis, readout, comp_gid in ALLOW:
        doc = load(nct)
        ps = doc["protocolSection"]
        conditions = "; ".join(ps.get("conditionsModule", {}).get("conditions", []))
        oms = doc["resultsSection"]["outcomeMeasuresModule"]["outcomeMeasures"]
        om = next((o for o in oms if o.get("title") == title), None)
        if om is None:
            raise SystemExit("outcome not found in %s: %r" % (nct, title))
        groups = {g["id"]: g["title"] for g in om.get("groups", [])}
        denoms = {}
        for dn in om.get("denoms", []):
            for c in dn.get("counts", []):
                denoms[c["groupId"]] = c.get("value")
        unit = om.get("unitOfMeasure", "NOT_REPORTED")
        param = om.get("paramType", "NOT_REPORTED")
        disp = om.get("dispersionType", "NOT_REPORTED")

        for cl in om.get("classes", []):
            timepoint = cl.get("title") or om.get("timeFrame") or "NOT_REPORTED"
            for cat_ in cl.get("categories", []):
                for meas in cat_.get("measurements", []):
                    gid = meas.get("groupId")
                    val = meas.get("value")
                    if val is None:
                        continue
                    is_ctrl = "placebo" in groups.get(gid, "").lower()
                    comp_val = None
                    if comp_gid and gid != comp_gid:
                        comp_val = next((m for m in cat_["measurements"]
                                         if m.get("groupId") == comp_gid), None)
                    pct = readout.endswith("pct_change")
                    rows.append(dict(
                        oligo_name=("placebo_or_sham_control" if is_ctrl else oligo),
                        source_key=nct, study_type="clinical_trial", species="human",
                        strain="NOT_APPLICABLE",
                        system_model=("%s — pre-specified MRI outcome measure, arm '%s'"
                                      % (nct, groups.get(gid, ""))),
                        is_human_system="TRUE", indication_population=conditions[:120],
                        arm_label=groups.get(gid, ""), arm_description="NOT_APPLICABLE",
                        arm_role="comparator" if is_ctrl else "exposed",
                        cns_compartment="whole_ventricular_system",
                        delivery_route="intrathecal_lumbar",
                        dose_value="NOT_REPORTED", dose_unit="NOT_APPLICABLE",
                        dose_regimen=groups.get(gid, ""),
                        exposure_duration=om.get("timeFrame", "NOT_REPORTED")[:150],
                        timepoint=timepoint,
                        endpoint_tier=tier, readout_category=cat,
                        readout_name=readout, readout_term_verbatim=title[:200],
                        readout_value=val, readout_unit=unit,
                        readout_is_qualitative="FALSE",
                        n_affected="NOT_APPLICABLE",
                        n_at_risk=denoms.get(gid, "NOT_REPORTED"),
                        comparator_arm=(groups.get(comp_gid, "NOT_APPLICABLE")
                                        if comp_gid and not is_ctrl
                                        else "NOT_APPLICABLE"),
                        n_affected_comparator="NOT_APPLICABLE",
                        n_at_risk_comparator=(denoms.get(comp_gid, "NOT_REPORTED")
                                              if comp_gid and not is_ctrl
                                              else "NOT_APPLICABLE"),
                        statistic="%s; dispersion %s = %s" % (
                            param, disp, meas.get("spread", "NOT_REPORTED")),
                        effect_direction=("increase" if pct and float(val) > 0
                                          else "decrease" if pct and float(val) < 0
                                          else "NOT_APPLICABLE"),
                        effect_vs_control=(
                            "comparator arm '%s' at the same timepoint: %s %s"
                            % (groups.get(comp_gid, ""), comp_val.get("value"), unit)
                            if comp_val else "NOT_APPLICABLE"),
                        seriousness="NOT_APPLICABLE",
                        assessment_type="protocol_specified_MRI_outcome_measure",
                        organ_system="Nervous system disorders",
                        source_vocabulary="NOT_APPLICABLE",
                        hydroceph_grade="",
                        grade_basis=(
                            "NOT GRADED. This is a continuous, protocol-specified "
                            "measurement of ventricular volume, not a per-subject "
                            "severity classification; the 0-3 rubric does not apply. "
                            "It is reported exactly as published, and no change score "
                            "or test statistic is computed here."),
                        grade_status="not_graded",
                        ascertainment="measured_positive",
                        ascertainment_basis=(
                            "The strongest ascertainment in this dataset: the protocol "
                            "required ventricular volume to be measured by structural "
                            "MRI in every participant on a fixed schedule, so this "
                            "value exists whether or not anything abnormal was seen. "
                            "For a continuous readout, measured_positive means the "
                            "quantity was measured and reported; magnitude and "
                            "direction are carried by readout_value and "
                            "effect_direction, not by this column."),
                        attribution_as_stated="not_discussed",
                        attribution_evidence=(
                            "An outcome-measure table reports values by arm and states "
                            "no causal interpretation. Attribution must be read from "
                            "the concurrent comparator arm."),
                        tox_axis=axis, event_cluster_id="NOT_APPLICABLE",
                        source_ref=nct,
                        source_location=(
                            "resultsSection.outcomeMeasuresModule.outcomeMeasures"
                            "[title='%s'].classes[title='%s'].categories[0]."
                            "measurements[groupId='%s']" % (title[:60], timepoint, gid)),
                        redistribution="public_domain",
                        notes=("Pre-specified MRI outcome measure. ClinicalTrials.gov "
                               "v2 API record, retrieved %s." % TODAY),
                    ))

    for nct, oligo, measure in PLANNED:
        doc = load(nct)
        ps = doc["protocolSection"]
        conditions = "; ".join(ps.get("conditionsModule", {}).get("conditions", []))
        status = ps.get("statusModule", {}).get("overallStatus", "NOT_REPORTED")
        rows.append(dict(
            oligo_name=oligo, source_key=nct, study_type="clinical_trial",
            species="human", strain="NOT_APPLICABLE",
            system_model="%s — pre-specified PRIMARY outcome; results not posted" % nct,
            is_human_system="TRUE", indication_population=conditions[:120],
            arm_label="all arms", arm_description="trial status: %s" % status,
            arm_role="exposed", cns_compartment="whole_ventricular_system",
            delivery_route="intrathecal_lumbar", dose_value="NOT_REPORTED",
            dose_unit="NOT_APPLICABLE", dose_regimen="NOT_REPORTED",
            exposure_duration="NOT_REPORTED", timepoint="NOT_REPORTED",
            endpoint_tier="A", readout_category="ventricular_morphometry",
            readout_name="structural_MRI_hydrocephalus_features_PLANNED",
            readout_term_verbatim=measure[:300], readout_value="NOT_REPORTED",
            readout_unit="NOT_APPLICABLE", readout_is_qualitative="TRUE",
            n_affected="NOT_APPLICABLE", n_at_risk="NOT_APPLICABLE",
            comparator_arm="NOT_APPLICABLE", n_affected_comparator="NOT_APPLICABLE",
            n_at_risk_comparator="NOT_APPLICABLE", statistic="NOT_REPORTED",
            effect_direction="NOT_APPLICABLE", effect_vs_control="NOT_APPLICABLE",
            seriousness="NOT_APPLICABLE",
            assessment_type="protocol_specified_MRI_outcome_measure",
            organ_system="Nervous system disorders", source_vocabulary="NOT_APPLICABLE",
            hydroceph_grade="", grade_basis=("NOT GRADED. No result exists to grade."),
            grade_status="not_graded", ascertainment="not_assessed",
            ascertainment_basis=(
                "The successor trial to GENERATION HD1 makes radiographic features "
                "consistent with hydrocephalus a PRIMARY outcome measured by structural "
                "MRI. Results are not posted. This row records that the endpoint is now "
                "protocol-specified for this compound — evidence about ascertainment "
                "practice, not about the endpoint — and carries no grade."),
            attribution_as_stated="not_discussed",
            attribution_evidence="No result; no attribution to record.",
            tox_axis="ventricular_enlargement", event_cluster_id="NOT_APPLICABLE",
            source_ref=nct,
            source_location=("protocolSection.outcomesModule.primaryOutcomes"
                             "[measure='%s...']" % measure[:50]),
            redistribution="public_domain",
            notes=("Included because the absence of protocol-specified ventricular "
                   "imaging is this endpoint's central ascertainment limitation, and "
                   "this trial is the first to remove it. Retrieved %s." % TODAY),
        ))

    out = os.path.join(DATA, "_ctgov_outcome_measurements.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote %s: %d rows" % (out, len(rows)))
    for r in rows:
        print("  %-24s %-13s %-10s %8s %-6s n=%s" % (
            r["arm_label"][:24], r["timepoint"][:13], r["oligo_name"][:10],
            r["readout_value"], r["readout_unit"][:6], r["n_at_risk"]))


if __name__ == "__main__":
    main()
