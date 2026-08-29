#!/usr/bin/env python3
"""
Deterministic extraction of hydrocephalus / CSF-dynamics adverse-event rows from
ClinicalTrials.gov v2 study records saved under sources/raw/ctgov_*.json.

Why a script and not hand transcription: every number in the output is copied by
this program from a named JSON path in a committed payload, so any value can be
re-derived and none can be mistyped or recalled from memory. The mapping tables
below (term classification, grading rule, comparator arms, oligo identity) are the
only human judgements, and each is written out once, in the open, and cited by
every row it produces via `grade_basis` / `source_location`.

Output: data/_ctgov_measurements.csv  (a component of data/measurements.csv)
        notes/ctgov_extraction_report.txt (audit trail)

Usage: python3 scripts/extract_ctgov.py
"""
import csv
import glob
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "sources", "raw")
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")

# --------------------------------------------------------------------------
# 1. Endpoint term classification.
#    Keys are matched case-insensitively against the MedDRA preferred term
#    EXACTLY as ClinicalTrials.gov prints it. Terms are never normalised or
#    spelling-corrected: `Meningitis asceptic` below is the source's own
#    misspelling in NCT04617860 and is preserved verbatim.
# --------------------------------------------------------------------------
TERMS = {
    # ---- Tier A: ventricular / CSF-volume outcome -------------------------
    "hydrocephalus": dict(
        tier="A", category="hydrocephalus_event", axis="ventricular_enlargement",
        readout="hydrocephalus_AE"),
    "normal pressure hydrocephalus": dict(
        tier="A", category="hydrocephalus_event", axis="ventricular_enlargement",
        readout="normal_pressure_hydrocephalus_AE"),
    "communicating hydrocephalus": dict(
        tier="A", category="hydrocephalus_event", axis="ventricular_enlargement",
        readout="communicating_hydrocephalus_AE"),
    "cerebral ventricle dilatation": dict(
        tier="A", category="ventricular_morphometry", axis="ventricular_enlargement",
        readout="cerebral_ventricle_dilatation_AE"),
    "ventriculomegaly": dict(
        tier="A", category="ventricular_morphometry", axis="ventricular_enlargement",
        readout="ventriculomegaly_AE"),
    "ventricular dilatation": dict(
        tier="A", category="ventricular_morphometry", axis="ventricular_enlargement",
        readout="ventricular_dilatation_AE"),
    # ---- Tier B: pressure / composition / flow / procedure ----------------
    "intracranial pressure increased": dict(
        tier="B", category="csf_pressure", axis="csf_pressure_disturbance",
        readout="intracranial_pressure_increased_AE"),
    "papilloedema": dict(
        tier="B", category="csf_pressure", axis="csf_pressure_disturbance",
        readout="papilloedema_AE"),
    "papilledema": dict(
        tier="B", category="csf_pressure", axis="csf_pressure_disturbance",
        readout="papilledema_AE"),
    "meningitis aseptic": dict(
        tier="B", category="csf_composition", axis="csf_composition_disturbance",
        readout="meningitis_aseptic_AE"),
    "meningitis asceptic": dict(   # sic — source misspelling, NCT04617860
        tier="B", category="csf_composition", axis="csf_composition_disturbance",
        readout="meningitis_asceptic_AE_sic"),
    "meningitis chemical": dict(
        tier="B", category="csf_composition", axis="csf_composition_disturbance",
        readout="meningitis_chemical_AE"),
    "meningitis": dict(
        tier="B", category="csf_composition", axis="csf_composition_disturbance",
        readout="meningitis_AE"),
    "arachnoiditis": dict(
        tier="B", category="csf_dynamics", axis="csf_composition_disturbance",
        readout="arachnoiditis_AE"),
    "cerebrospinal fluid leakage": dict(
        tier="B", category="csf_dynamics", axis="delivery_procedure_complication",
        readout="csf_leakage_AE"),
    "cerebrospinal fluid protein increased": dict(
        tier="B", category="csf_composition", axis="csf_composition_disturbance",
        readout="csf_protein_increased_AE"),
    "post lumbar puncture syndrome": dict(
        tier="B", category="procedure_complication", axis="delivery_procedure_complication",
        readout="post_lumbar_puncture_syndrome_AE"),
    "traumatic lumbar puncture": dict(
        tier="B", category="procedure_complication", axis="delivery_procedure_complication",
        readout="traumatic_lumbar_puncture_AE"),
}

# --------------------------------------------------------------------------
# 2. Grading rules. Each rule states the sentence written into `grade_basis`,
#    so no grade in the dataset exists without its rule attached.
# --------------------------------------------------------------------------
def grade_for(term_key, serious, n_affected):
    """Return (grade, grade_basis). Applies SCHEMA.md 'hydroceph_grade rubric'."""
    if n_affected == 0:
        return 0, ("0 = endpoint term is listed in this trial's posted adverse-event "
                   "table with an explicitly reported count of 0 in this arm "
                   "(SCHEMA.md rubric grade 0; ascertainment = measured_null)")
    meta = TERMS[term_key]
    if meta["category"] == "hydrocephalus_event":
        if serious:
            return 3, ("3 = serious adverse event coded to a MedDRA hydrocephalus term "
                       "(SCHEMA.md rubric grade 3, clause 'a serious adverse event coded "
                       "as hydrocephalus'). Seriousness is the registry's own "
                       "classification, not a clinical judgement made here.")
        return 2, ("2 = non-serious adverse event coded to a MedDRA hydrocephalus term; "
                   "graded moderate because the registry records no permanent CSF "
                   "diversion (SCHEMA.md rubric grade 2).")
    if meta["category"] == "ventricular_morphometry":
        return 1, ("1 = imaging/morphometric ventricular finding reported as an adverse "
                   "event without a stated symptom or intervention "
                   "(SCHEMA.md rubric grade 1).")
    if meta["category"] in ("csf_pressure", "csf_composition", "csf_dynamics"):
        return 2, ("2 = symptomatic raised intracranial pressure, papilloedema, "
                   "aseptic/chemical meningitis or arachnoiditis, named explicitly at "
                   "SCHEMA.md rubric grade 2. Registry seriousness is recorded in notes "
                   "and does not change the grade, because grade 3 requires a permanent "
                   "CSF diversion or a fatal/disabling outcome, neither of which the "
                   "registry states.")
    if meta["category"] == "procedure_complication":
        return 1, ("1 = self-limited complication of the lumbar-puncture delivery "
                   "procedure (SCHEMA.md rubric grade 1). tox_axis is "
                   "delivery_procedure_complication so these rows can be excluded from "
                   "any compound-attributable analysis.")
    raise AssertionError("ungraded category: " + meta["category"])


# --------------------------------------------------------------------------
# 3. Oligonucleotide identity per trial. Written out explicitly rather than
#    parsed from free-text intervention names.
# --------------------------------------------------------------------------
TRIAL_OLIGO = {
    # --- CNS-delivered (intrathecal) oligonucleotides: the exposed class -----
    "NCT01703988": "nusinersen", "NCT01839656": "nusinersen",
    "NCT02193074": "nusinersen", "NCT02292537": "nusinersen",
    "NCT02386553": "nusinersen", "NCT02462759": "nusinersen",
    "NCT02594124": "nusinersen", "NCT04089566": "nusinersen",
    "NCT02623699": "tofersen", "NCT03070119": "tofersen", "NCT04856982": "tofersen",
    "NCT02519036": "tominersen", "NCT03342053": "tominersen",
    "NCT03761849": "tominersen", "NCT03842969": "tominersen",
    "NCT04000594": "tominersen", "NCT05686551": "tominersen",
    "NCT03186989": "BIIB080", "NCT04494256": "BIIB105",
    "NCT03225833": "WVE-120101", "NCT04617847": "WVE-120101",
    "NCT03225846": "WVE-120102", "NCT04617860": "WVE-120102",
    "NCT05032196": "WVE-003",
    # --- Systemically delivered oligonucleotides: the ROUTE-CONTRAST control -
    # These reach the CSF only across an intact blood-brain barrier. If the
    # hydrocephalus signal is a property of intrathecal delivery rather than of
    # oligonucleotide chemistry, these arms must be null. They are included so
    # that prediction is testable, not assumed.
    "NCT00628498": "defibrotide", "NCT01836549": "imetelstat",
    "NCT03399370": "inclisiran", "NCT03532542": "casimersen_or_golodirsen",
}

# Route per trial. Never inferred from the compound alone — the same molecule
# can be dosed by more than one route.
TRIAL_ROUTE = {
    "intrathecal_lumbar": {
        "NCT01703988", "NCT01839656", "NCT02193074", "NCT02292537", "NCT02386553",
        "NCT02462759", "NCT02594124", "NCT04089566", "NCT02623699", "NCT03070119",
        "NCT04856982", "NCT02519036", "NCT03342053", "NCT03761849", "NCT03842969",
        "NCT04000594", "NCT05686551", "NCT03186989", "NCT04494256", "NCT03225833",
        "NCT03225846", "NCT04617847", "NCT04617860", "NCT05032196",
    },
    "intravenous": {"NCT00628498", "NCT01836549", "NCT03532542"},
    "subcutaneous": {"NCT03399370"},
}


def route_for(nct):
    for route, ncts in TRIAL_ROUTE.items():
        if nct in ncts:
            return route
    return "NOT_REPORTED"


# Excluded, with the reason recorded rather than silently dropped:
EXCLUDED_TRIALS = {
    "NCT05386680": "OAV101 (onasemnogene abeparvovec) is an AAV9 gene therapy, not "
                   "an oligonucleotide. Out of the Challenge's scope. Retained in "
                   "sources/raw/ as an available same-route, same-disease "
                   "non-oligonucleotide comparator; contributes no row.",
}

# --------------------------------------------------------------------------
# 4. Comparator arms. Explicit per trial, because several trials carry more
#    than one placebo group and an automatic rule would mis-pair them.
#    Value: {treated_event_group_id: comparator_event_group_id}
#    A trial absent from this map has no concurrent control arm.
# --------------------------------------------------------------------------
COMPARATOR = {
    # GENERATION HD1: two cohorts, each with its own placebo group.
    "NCT03761849": {"EG001": "EG000", "EG002": "EG000",      # ODC cohort -> PLB ODC
                    "EG003": "EG005", "EG004": "EG005"},      # NDC cohort -> PLB NDC
    # VALOR: three parts, each with its own placebo group.
    "NCT02623699": {"EG001": "EG000", "EG002": "EG000", "EG003": "EG000", "EG004": "EG000",
                    "EG006": "EG005", "EG007": "EG005", "EG008": "EG005", "EG009": "EG005",
                    "EG011": "EG010"},
}
# Groups that ARE the comparator (so they are labelled, not treated as exposed).
COMPARATOR_GROUPS = {
    "NCT03761849": {"EG000", "EG005"},
    "NCT02623699": {"EG000", "EG005", "EG010"},
}


def is_control_group(nct, group):
    if nct in COMPARATOR_GROUPS and group["id"] in COMPARATOR_GROUPS[nct]:
        return True
    t = (group.get("title", "") + " " + str(group.get("description", ""))).lower()
    return ("placebo" in t or "sham" in t) and "prior" not in t and "previous" not in t


def classify(term):
    return TERMS.get(term.strip().lower())


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(NOTES, exist_ok=True)
    rows = []
    report = []
    files = sorted(glob.glob(os.path.join(RAW, "ctgov_*.json")))
    if not files:
        sys.exit("no ctgov_*.json payloads under " + RAW)

    for path in files:
        with open(path) as fh:
            doc = json.load(fh)
        ps = doc.get("protocolSection", {})
        nct = ps.get("identificationModule", {}).get("nctId")
        title = ps.get("identificationModule", {}).get("briefTitle", "")
        if nct in EXCLUDED_TRIALS:
            report.append(f"{nct} EXCLUDED — {EXCLUDED_TRIALS[nct]}")
            continue
        oligo = TRIAL_OLIGO.get(nct)
        if oligo is None:
            report.append(f"{nct} SKIPPED — no oligonucleotide mapping recorded")
            continue
        results = doc.get("resultsSection")
        ae = (results or {}).get("adverseEventsModule")
        if not ae:
            report.append(f"{nct} ({oligo}) — no posted results; contributes no row "
                          f"(recorded in SOURCES.md as results-not-posted)")
            continue

        threshold = ae.get("frequencyThreshold")
        timeframe = ae.get("timeFrame", "")
        conditions = ps.get("conditionsModule", {}).get("conditions", [])
        population = "; ".join(conditions)[:120] or "NOT_REPORTED"
        route = route_for(nct)
        compartment = ("CSF_and_neuraxis" if route in ("intrathecal_lumbar",
                       "intracerebroventricular") else "NOT_APPLICABLE")
        groups = {g["id"]: g for g in ae.get("eventGroups", [])}
        comp_map = COMPARATOR.get(nct, {})

        n_serious_terms = len(ae.get("seriousEvents", []))
        n_other_terms = len(ae.get("otherEvents", []))
        seen_tierA_serious = False

        for kind, serious in (("seriousEvents", True), ("otherEvents", False)):
            for ev in ae.get(kind, []):
                meta = classify(ev.get("term", ""))
                if not meta:
                    continue
                key = ev["term"].strip().lower()
                if serious and meta["tier"] == "A":
                    seen_tierA_serious = True
                for st in ev.get("stats", []):
                    gid = st.get("groupId")
                    g = groups.get(gid, {})
                    n_aff = st.get("numAffected")
                    n_risk = st.get("numAtRisk")
                    if n_aff is None or n_risk is None:
                        continue
                    control = is_control_group(nct, g) if g else False
                    cid = comp_map.get(gid)
                    if cid is None and not control:
                        # single unambiguous control group in this trial?
                        ctrls = [k for k, v in groups.items() if is_control_group(nct, v)]
                        cid = ctrls[0] if len(ctrls) == 1 else None
                    comp_stats = None
                    if cid:
                        comp_stats = next((s for s in ev["stats"] if s.get("groupId") == cid), None)
                    grade, basis = grade_for(key, serious, n_aff)
                    if n_aff == 0:
                        asc = "measured_null"
                        asc_basis = (
                            f"The term is listed in this trial's posted "
                            f"{'serious' if serious else 'other'}-adverse-event table with an "
                            f"explicit count of 0 for this arm. The module declares "
                            f"frequencyThreshold={threshold}, which governs the other-events "
                            f"table only.")
                    else:
                        asc = "measured_positive"
                        asc_basis = (
                            f"Count read from the posted "
                            f"{'serious' if serious else 'other'}-adverse-event table; "
                            f"module frequencyThreshold={threshold}.")
                    rows.append(dict(
                        oligo_name=("placebo_or_sham_control" if control else oligo),
                        source_key=nct,
                        study_type="clinical_trial",
                        species="human",
                        strain="NOT_APPLICABLE",
                        system_model=f"{title[:80]} — arm '{g.get('title','')}'",
                        is_human_system="TRUE",
                        indication_population=population,
                        arm_label=g.get("title", ""),
                        arm_description=str(g.get("description", ""))[:200],
                        arm_role="comparator" if control else "exposed",
                        cns_compartment=compartment,
                        delivery_route=route,
                        exposure_duration=timeframe[:150] or "NOT_REPORTED",
                        timepoint=timeframe[:150] or "NOT_REPORTED",
                        endpoint_tier=meta["tier"],
                        readout_category=meta["category"],
                        readout_name=meta["readout"],
                        readout_term_verbatim=ev["term"],
                        readout_value=n_aff,
                        readout_unit="participants",
                        readout_is_qualitative="FALSE",
                        n_affected=n_aff,
                        n_at_risk=n_risk,
                        comparator_arm=(groups.get(cid, {}).get("title", "") if cid
                                        else "NOT_APPLICABLE"),
                        n_affected_comparator=(comp_stats.get("numAffected")
                                               if comp_stats else "NOT_APPLICABLE"),
                        n_at_risk_comparator=(comp_stats.get("numAtRisk")
                                              if comp_stats else "NOT_APPLICABLE"),
                        statistic="NOT_REPORTED",
                        effect_direction=("no_change" if n_aff == 0 else "increase"),
                        seriousness=("serious" if serious else "non_serious"),
                        assessment_type=ev.get("assessmentType", "NOT_REPORTED"),
                        organ_system=ev.get("organSystem", "NOT_REPORTED"),
                        source_vocabulary=ev.get("sourceVocabulary", "NOT_REPORTED"),
                        hydroceph_grade=grade,
                        grade_basis=basis,
                        grade_status="provisional",
                        ascertainment=asc,
                        ascertainment_basis=asc_basis,
                        attribution_as_stated="not_discussed",
                        attribution_evidence=(
                            "ClinicalTrials.gov results adverse-event modules report "
                            "all-cause adverse events and record no per-event causality "
                            f"assessment; the registry states assessmentType="
                            f"{ev.get('assessmentType','NOT_REPORTED')}. Attribution must "
                            "be read from the concurrent comparator arm, not from this field."),
                        tox_axis=meta["axis"],
                        source_ref=nct,
                        source_location=(
                            f"resultsSection.adverseEventsModule.{kind}"
                            f"[term='{ev['term']}'].stats[groupId='{gid}']"),
                        redistribution="public_domain",
                        notes=(f"ClinicalTrials.gov v2 API record, retrieved "
                               f"{date.today().isoformat()}. Arm at risk n={n_risk}."),
                    ))

        # Trial-level explicit negative for the core endpoint.
        if not seen_tierA_serious:
            for gid, g in groups.items():
                n_risk = g.get("seriousNumAtRisk")
                if not n_risk:
                    continue
                control = is_control_group(nct, g)
                rows.append(dict(
                    oligo_name=("placebo_or_sham_control" if control else oligo),
                    source_key=nct, study_type="clinical_trial", species="human",
                    strain="NOT_APPLICABLE",
                    system_model=f"{title[:80]} — arm '{g.get('title','')}'",
                    is_human_system="TRUE", indication_population=population,
                    arm_label=g.get("title", ""),
                    arm_description=str(g.get("description", ""))[:200],
                    arm_role="comparator" if control else "exposed",
                    cns_compartment=compartment, delivery_route=route,
                    exposure_duration=timeframe[:150] or "NOT_REPORTED",
                    timepoint=timeframe[:150] or "NOT_REPORTED",
                    endpoint_tier="A", readout_category="hydrocephalus_event",
                    readout_name="hydrocephalus_serious_AE",
                    readout_term_verbatim="NOT_APPLICABLE",
                    readout_value=0, readout_unit="participants",
                    readout_is_qualitative="FALSE",
                    n_affected=0, n_at_risk=n_risk,
                    comparator_arm="NOT_APPLICABLE",
                    n_affected_comparator="NOT_APPLICABLE",
                    n_at_risk_comparator="NOT_APPLICABLE",
                    statistic="NOT_REPORTED", effect_direction="no_change",
                    seriousness="serious", assessment_type="NOT_APPLICABLE",
                    organ_system="Nervous system disorders",
                    source_vocabulary="NOT_APPLICABLE",
                    hydroceph_grade=0,
                    grade_basis=("0 = no serious adverse event coded to any tier-A "
                                 "hydrocephalus term appears in this trial's posted "
                                 f"serious-adverse-event table ({n_serious_terms} terms "
                                 "listed). SCHEMA.md rubric grade 0."),
                    grade_status="provisional",
                    ascertainment="measured_null",
                    ascertainment_basis=(
                        f"Derived from absence: this trial posted a serious-adverse-event "
                        f"table listing {n_serious_terms} terms and an other-event table "
                        f"listing {n_other_terms} terms at frequencyThreshold={threshold}; "
                        f"no tier-A hydrocephalus term is among them. This is a statement "
                        f"about the posted document, not a claim that ventricular imaging "
                        f"was performed. See METHODOLOGY.md OI-01."),
                    attribution_as_stated="not_discussed",
                    attribution_evidence=(
                        "No event; no attribution to record."),
                    tox_axis="ventricular_enlargement",
                    source_ref=nct,
                    source_location=("resultsSection.adverseEventsModule.seriousEvents "
                                     "(absence of any tier-A term); eventGroups"
                                     f"[id='{gid}'].seriousNumAtRisk"),
                    redistribution="public_domain",
                    notes=(f"Explicit trial-level negative. ClinicalTrials.gov v2 API "
                           f"record, retrieved {date.today().isoformat()}."),
                ))
        report.append(
            f"{nct} ({oligo}) — {n_serious_terms} serious terms, {n_other_terms} other "
            f"terms, threshold={threshold}, tierA_serious={'YES' if seen_tierA_serious else 'no'}")

    out = os.path.join(DATA, "_ctgov_measurements.csv")
    cols = list(rows[0].keys())
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(NOTES, "ctgov_extraction_report.txt"), "w") as fh:
        fh.write("ClinicalTrials.gov extraction audit trail\n")
        fh.write("=" * 60 + "\n")
        fh.write(f"payloads scanned: {len(files)}\nrows emitted: {len(rows)}\n\n")
        fh.write("\n".join(report) + "\n")

    print(f"wrote {out}: {len(rows)} rows, {len(cols)} columns")
    tiers = {}
    for r in rows:
        tiers[r["endpoint_tier"]] = tiers.get(r["endpoint_tier"], 0) + 1
    print("by tier:", tiers)
    pos = sum(1 for r in rows if r["ascertainment"] == "measured_positive")
    print(f"measured_positive: {pos}   measured_null: {len(rows)-pos}")
    print("\n".join(report))


if __name__ == "__main__":
    main()
