#!/usr/bin/env python3
"""Quality-control validator for the OligoTox-CNS dataset.

Enforces, against `schema-cns.md`:
  1. Column-set conformance for both canonical tables.
  2. Primary-key uniqueness and referential integrity (measurements -> oligos).
  3. Controlled-vocabulary conformance for every enum column.
  4. Range checks (neurotox_grade in 0..3, booleans, numeric dose/value fields).
  5. Provenance completeness (source_id + source_ref + source_table on every row).
  6. Endpoint-policy checks specific to this dataset:
       - NfL rows may not carry effect_direction = TBD (direction is a grading input).
       - challenge_priority must be the acute-electrophysiology bucket if and only if
         the row is an electrophysiology readout.
       - grade 0 rows must not report an increase in an injury readout.
  7. Sequence sanity: only IUPAC bases, case-insensitive (case encodes chemistry),
     and length_nt consistency where both are present.

Exit status is non-zero if any ERROR is raised. WARNINGs are informational.

Usage:  python scripts/qc_cns.py
"""
import csv
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLIGOS = os.path.join(ROOT, "notes", "cns", "corpus", "cns_oligos.csv")
MEAS = os.path.join(ROOT, "notes", "cns", "corpus", "cns_measurements.csv")

TBD = "TBD"

NCT_RE = re.compile(r"^NCT\d{8}$")

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt", "backbone_chemistry",
              "sugar_modifications", "gapmer_design", "conjugate", "ps_count",
              "sequence_5to3", "design_source", "notes"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "cns_region", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "endpoint_domain", "challenge_priority",
             "readout_category", "readout_name", "readout_value", "readout_unit",
             "effect_direction", "effect_vs_control", "neurotox_grade", "reversibility",
             "is_cns_specific", "source_id", "source_ref", "source_table",
             "redistribution", "notes",
             # Derived by scripts/classify_evidence_cns.py. Computed from the
             # columns above, never read from a new document, so they can be
             # deleted and regenerated without losing evidence.
             "evidence_class", "trial_key", "trial_key_basis",
             "ascertainment", "negative_eligible", "event_cluster",
             "hydroceph_tier"]

# The evidence classes, and which of them are claims about humans. A human total
# computed over anything outside HUMAN_CLASSES is wrong by construction, so the
# membership lives here rather than in each consumer.
HUMAN_CLASSES = {"human_trial_registry", "human_trial_publication",
                 "human_trial_sponsor", "human_laboratory", "human_label_pooled",
                 "human_postmarketing", "human_case_report", "human_observational",
                 "human_background_epi", "human_class_review"}
ANIMAL_CLASSES = {"animal_invivo", "animal_laboratory"}
# Which ascertainment categories let a grade-0 row stand as a negative. Kept in
# step with classify_evidence_cns.py, and checked against it below.
NEGATIVE_ELIGIBLE_ASC = {"measured", "assessed_no_effect",
                         "explicit_zero_with_denominator"}

ENUMS = {
    "oligo_class": {"ASO_gapmer", "siRNA", "GalNAc_siRNA", "splice_switching_ASO",
                    "PMO", "aptamer", "other"},
    "max_phase": {"approved", "approved_EMA", "phase_3", "phase_3_discontinued",
                  "phase_2", "phase_2_discontinued", "phase_1", "phase_1_discontinued",
                  "preclinical", "research_panel", "named_patient", "class_review"},
    "backbone_chemistry": {"full_PS", "PS_PO_mix", "full_PO", "PMO_neutral", "mixed", TBD},
    "conjugate": {"none", "GalNAc", "lipid", "peptide", "PEG", "divalent", "other", TBD},
    "study_type": {"in_vitro", "animal_invivo", "clinical"},
    "species": {"human", "monkey", "rat", "mouse", "sheep", "multi_species", "NA"},
    "cns_region": {"whole_brain", "cortex", "hippocampus", "cerebellum", "brainstem",
                   "striatum", "spinal_cord", "DRG", "ventricle", "CSF", "meninges",
                   "optic_nerve", "peripheral_nerve", "systemic", "NA"},
    "delivery_method": {"intrathecal", "intracerebroventricular", "intracisternal",
                        "intraparenchymal", "intravitreal", "systemic_dose",
                        "gymnotic_free_uptake", "transfection", "lipofection", TBD},
    "dose_or_conc_unit": {"uM", "nM", "ug/mL", "mg/kg", "mg", "ug", "fold_Cmax", "NA", TBD},
    "endpoint_domain": {"chronic_neurotoxicity", "hydrocephalus", "acute_neurotoxicity",
                        "neuroinflammation", "neurodegeneration", "neurobehavioral",
                        "cytotoxicity", "csf_biomarker", "clinical_neuro_ae"},
    "challenge_priority": {"high_chronic_neurotox", "high_hydrocephalus", "medium",
                           "low_acute_electrophysiology"},
    "readout_category": {"functional", "injury_biomarker", "viability", "accumulation",
                         "histopathology", "imaging", "behavioral",
                         "clinical_neuro_outcome", "electrophysiology", "transcriptomic"},
    "effect_direction": {"increase", "decrease", "no_change", TBD},
    "reversibility": {"reversible", "partially_reversible", "irreversible",
                      "not_assessed", TBD},
    "is_cns_specific": {"TRUE", "FALSE"},
    "redistribution": {"public_domain", "cc_by", "derived_features_only",
                       "summary_stat", "verify"},
    "evidence_class": HUMAN_CLASSES | ANIMAL_CLASSES,
    "trial_key_basis": {"registry_posting", "named_in_source",
                        "publication_only", "not_a_trial"},
    "ascertainment": {"measured", "reported_event", "assessed_no_effect",
                      "explicit_zero_with_denominator", "threshold_limited_zero",
                      "not_assessed_in_source", "absence_of_label_warning",
                      "review_required"},
    "negative_eligible": {"TRUE", "FALSE", "NA"},
    "hydroceph_tier": {"ventricular_enlargement", "pressure_or_composition",
                       "procedure_or_mechanism", "disease_background",
                       "therapeutic_reduction", "related_clinical_sign", ""},
}

# Readouts where a RISE is recovery, not injury. Without this the grade-0 check
# fires on every rescued phenotype — more neurons, longer neurites, higher
# viability — and trains the curator to ignore its own warnings.
HIGHER_IS_BETTER = ("neurite", "tuj1", "map2", "viability", "neuron_count",
                    "differentiation", "synap", "rotarod", "grip_strength",
                    "latency", "motor_function")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(path, expected_cols, label):
    if not os.path.exists(path):
        err(f"{label}: file missing at {path}")
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        err(f"{label}: no data rows")
        return []
    got = list(rows[0].keys())
    if got != expected_cols:
        missing = [c for c in expected_cols if c not in got]
        extra = [c for c in got if c not in expected_cols]
        err(f"{label}: column mismatch. missing={missing} extra={extra}")
    return rows


def check_enums(rows, label):
    for r in rows:
        rid = r.get("measurement_id") or r.get("oligo_id")
        for col, allowed in ENUMS.items():
            if col not in r:
                continue
            v = (r[col] or "").strip()
            if v and v not in allowed:
                err(f"{label} {rid}: {col}='{v}' not in controlled vocabulary")


def main():
    oligos = load(OLIGOS, OLIGO_COLS, "cns_oligos")
    meas = load(MEAS, MEAS_COLS, "cns_measurements")
    if not oligos or not meas:
        report()
        return

    # --- primary keys -----------------------------------------------------
    for rows, key, label in ((oligos, "oligo_id", "cns_oligos"),
                             (meas, "measurement_id", "cns_measurements")):
        ids = [r[key] for r in rows]
        dupes = [k for k, c in Counter(ids).items() if c > 1]
        if dupes:
            err(f"{label}: duplicate {key}: {dupes[:5]}")

    # --- referential integrity -------------------------------------------
    known = {r["oligo_id"] for r in oligos}
    orphans = [m["measurement_id"] for m in meas if m["oligo_id"] not in known]
    if orphans:
        err(f"cns_measurements: {len(orphans)} orphan oligo_id refs: {orphans[:5]}")
    unused = known - {m["oligo_id"] for m in meas}
    if unused:
        warn(f"cns_oligos: {len(unused)} oligo(s) with no measurement: {sorted(unused)[:5]}")

    # --- controlled vocabularies -----------------------------------------
    check_enums(oligos, "cns_oligos")
    check_enums(meas, "cns_measurements")

    # --- numeric / range checks ------------------------------------------
    for m in meas:
        mid = m["measurement_id"]
        g = m["neurotox_grade"]
        if g not in {"0", "1", "2", "3"}:
            err(f"{mid}: neurotox_grade='{g}' not in 0..3")
        d = m["dose_or_conc_value"]
        # `NA` is a real value here, not a gap: a disease-background row records a
        # rate in an untreated population, so no dose was given. It is distinct
        # from TBD, which means a dose exists and we have not read it. The unit
        # column already admits NA for the same reason.
        if d and d not in (TBD, "NA"):
            try:
                float(d)
            except ValueError:
                err(f"{mid}: dose_or_conc_value='{d}' is neither numeric, NA nor TBD")
        for col in ("source_id", "source_ref", "source_table"):
            if not (m[col] or "").strip() or m[col] == TBD:
                err(f"{mid}: provenance column {col} is empty/TBD")

    for o in oligos:
        oid = o["oligo_id"]
        for col in ("length_nt", "ps_count"):
            v = o[col]
            if v and v not in (TBD, "NA"):
                try:
                    int(v)
                except ValueError:
                    err(f"{oid}: {col}='{v}' is neither an integer nor TBD/NA")

    # --- endpoint-policy checks ------------------------------------------
    for m in meas:
        mid = m["measurement_id"]
        rn = m["readout_name"].lower()
        if "nfl" in rn and m["effect_direction"] == TBD:
            err(f"{mid}: NfL row must declare effect_direction "
                f"(a fall is efficacy, a rise is toxicity)")
        is_ephys = m["readout_category"] == "electrophysiology"
        is_low = m["challenge_priority"] == "low_acute_electrophysiology"
        if is_ephys and not is_low:
            err(f"{mid}: electrophysiology readout must carry "
                f"challenge_priority=low_acute_electrophysiology")
        if is_low and not is_ephys:
            err(f"{mid}: challenge_priority=low_acute_electrophysiology on a "
                f"non-electrophysiology readout ({m['readout_category']})")
        if m["neurotox_grade"] == "0" and m["effect_direction"] == "increase" \
                and m["readout_category"] in {"injury_biomarker", "histopathology"} \
                and not any(k in rn for k in HIGHER_IS_BETTER) \
                and not re.search(r"placebo|control|untreated|sham|vehicle",
                                  m["effect_vs_control"], re.I):
            warn(f"{mid}: grade 0 with an increase in an injury readout and no "
                 f"control comparison in effect_vs_control — verify grading")
        if m["endpoint_domain"] == "hydrocephalus" and \
                m["challenge_priority"] != "high_hydrocephalus":
            warn(f"{mid}: hydrocephalus endpoint not flagged high_hydrocephalus")

    # --- a grade must rest on a measurement -------------------------------
    # "The source did not report toxicity" is not "the source measured toxicity
    # and found none", and only the second is a negative control. A grade-0 row
    # whose value, direction and comparator are all TBD and whose locus is a
    # Methods section is asserting an outcome nothing supports.
    for m in meas:
        if m["neurotox_grade"] == "0" and m["readout_value"] == TBD \
                and m["effect_direction"] == TBD \
                and re.search(r"method", m["source_table"], re.I):
            err(f"{m['measurement_id']}: grade 0 with no value, no direction and a "
                f"Methods-section locus — this is silence, not a measured negative")

    # --- the human/animal firewall ----------------------------------------
    # The point of evidence_class is that "no animal row contributes to a human
    # total" can be checked. It is only checkable if the class never disagrees
    # with the species and study_type it was derived from.
    for m in meas:
        mid, cls = m["measurement_id"], m["evidence_class"]
        human_row = m["species"] == "human"
        if cls in HUMAN_CLASSES and not human_row:
            err(f"{mid}: evidence_class={cls} claims human evidence but "
                f"species={m['species']}")
        if cls in ANIMAL_CLASSES and human_row:
            err(f"{mid}: evidence_class={cls} on a human row")
        if cls == "human_laboratory" and m["study_type"] == "clinical":
            err(f"{mid}: human_laboratory on a clinical row — a trial is not a "
                f"laboratory system")
        if cls == "animal_invivo" and m["study_type"] != "animal_invivo":
            err(f"{mid}: evidence_class=animal_invivo but "
                f"study_type={m['study_type']}")

    # --- a negative must be eligible to be a negative ---------------------
    # This is the rule the FAERS-style failure mode needs. A grade of 0 reached by
    # a document not mentioning something is not a measured negative, and the only
    # thing standing between that row and a model is this predicate.
    for m in meas:
        mid, asc, g = m["measurement_id"], m["ascertainment"], m["neurotox_grade"]
        tier = m["hydroceph_tier"]
        # A grade of 0 reached because the compound IMPROVED the endpoint, or
        # measured in patients given no oligonucleotide at all, is not a negative
        # for that compound however sound its ascertainment.
        want = "NA" if g != "0" else (
            "FALSE" if tier in ("therapeutic_reduction", "disease_background")
            else "TRUE" if asc in NEGATIVE_ELIGIBLE_ASC else "FALSE")
        if m["negative_eligible"] != want:
            err(f"{mid}: negative_eligible={m['negative_eligible']!r} but grade={g} "
                f"with ascertainment={asc} implies {want!r} — re-run "
                f"classify_evidence_cns.py")
        if g == "0" and asc == "reported_event":
            err(f"{mid}: ascertainment=reported_event on a grade-0 row")

    # --- one readout name, how many scales? -------------------------------
    # `acute_neurotoxicity_score` is carried by 642 rows from ten sources, and
    # `readout_unit` is what separates their scales. For most pairs it does the job,
    # but `score_0_to_7` spans five sources whose own notes define DIFFERENT
    # instruments: three patents use a 7-region functional-observational battery
    # summed 0-7, one paper uses a 0-6 ordinal acute-INHIBITION ladder, and one uses
    # an acute neuronal-ACTIVATION score - shaking, tremors, convulsions - read in
    # 15-minute blocks rather than at 3 h. Inhibition and activation are opposite
    # phenotypes. Pooling them on the shared name and unit would average a paralysed
    # animal with a seizing one.
    #
    # A warning, not an error, and deliberately not auto-corrected: rewriting 375
    # rows' units on a reading of their notes is a scale-harmonisation judgement,
    # and the right person to make it is a toxicologist. What this rule guarantees is
    # that the hazard is printed on every run instead of being discovered by whoever
    # pools the column.
    scales = {}
    for m in meas:
        scales.setdefault((m["readout_name"], m["readout_unit"]), set()).add(m["source_ref"])
    multi = {k: v for k, v in scales.items() if len(v) > 2 and k[1].startswith("score_")}
    for (name, unit), refs in sorted(multi.items()):
        warn(f"readout '{name}' with unit '{unit}' spans {len(refs)} sources — "
             f"confirm they are the same instrument before pooling: "
             f"{sorted(refs)[:5]}")

    # --- the hydrocephalus endpoint tiers ---------------------------------
    # Ventricular enlargement, a raised pressure, an optic-disc sign, an ependymal
    # mechanism, a background rate and a therapeutic reduction are six different
    # claims. A tier on a row that bears on none of them would mean the derivation
    # has drifted.
    for m in meas:
        t, dom = m["hydroceph_tier"], m["endpoint_domain"]
        if t and dom not in ("hydrocephalus", "clinical_neuro_ae"):
            err(f"{m['measurement_id']}: hydroceph_tier={t} on endpoint_domain={dom}")
        if dom == "hydrocephalus" and not t:
            err(f"{m['measurement_id']}: endpoint_domain=hydrocephalus with no "
                f"hydroceph_tier")

    # --- trial keys must say how they were established --------------------
    for m in meas:
        mid, k, basis = m["measurement_id"], m["trial_key"], m["trial_key_basis"]
        if m["evidence_class"] == "human_trial_registry" and basis != "registry_posting":
            err(f"{mid}: a registry-posted row must carry "
                f"trial_key_basis=registry_posting, not {basis!r}")
        if basis == "publication_only" and not k.startswith("PUB:"):
            err(f"{mid}: trial_key_basis=publication_only but trial_key={k!r}")
        if basis in ("registry_posting", "named_in_source") and not NCT_RE.match(k):
            err(f"{mid}: trial_key_basis={basis} but trial_key={k!r} is not a "
                f"registry identifier")
        if basis == "not_a_trial" and k:
            err(f"{mid}: trial_key={k!r} on a row that is not trial-derived")

    # --- one observation, one row ------------------------------------------
    # Two extraction lanes read the same ClinicalTrials.gov posting under two
    # source_id conventions and both copies survived semantic de-duplication,
    # because they encoded the same count differently (2_of_40 against 5.0%).
    # The identity that catches it is the observation, not the value: one trial,
    # one compound, one endpoint, one term, one seriousness table.
    lanes = {}
    for m in meas:
        if not m["trial_key"].startswith("NCT"):
            continue
        t = m["source_table"].lower()
        bucket = ("serious" if "seriousevents" in t or "serious adverse event" in t
                  else "nonserious" if "otherevents" in t or "not including serious" in t
                  else "unspecified")
        lane = ("ctgov_api_sweep" if m["source_id"].startswith("CT_NCT")
                else "ctgov_curated" if m["source_id"].startswith("CNSSRC_CTG_")
                else "other")
        key = (m["trial_key"], m["oligo_id"], m["endpoint_domain"],
               re.sub(r"[^a-z0-9]", "", m["readout_name"].lower()), bucket)
        lanes.setdefault(key, {}).setdefault(lane, []).append(m["measurement_id"])
    for key, by_lane in sorted(lanes.items()):
        if len(by_lane) > 1:
            err(f"one observation extracted in {len(by_lane)} lanes: {key} -> "
                f"{dict(by_lane)}; adjudicate it in dedupe_cross_lane_cns.py")

    # --- mortality invariant ----------------------------------------------
    # Death is grade 3 under the rubric, without exception and without
    # interpretation. This is the one grading rule that needs no judgement, so it
    # is worth asserting: any drift here means a grading pass has gone wrong
    # somewhere less obvious too.
    for m in meas:
        if not re.search(r"mortalit|death", m["readout_name"], re.I):
            continue
        v = m["readout_value"].strip()
        killed = re.match(r"^\s*([0-9.]+)\s*[/_]\s*of?\s*[_]?\s*([0-9.]+)", v) or \
            re.match(r"^\s*([0-9.]+)[/_]([0-9.]+)", v)
        if not killed:
            continue
        try:
            n = float(killed.group(1))
        except ValueError:
            continue
        if n > 0 and m["neurotox_grade"] != "3":
            err(f"{m['measurement_id']}: {n:g} death(s) recorded but "
                f"neurotox_grade={m['neurotox_grade']}; death is grade 3")
        if n == 0 and m["neurotox_grade"] == "3":
            warn(f"{m['measurement_id']}: zero deaths recorded but graded 3 — "
                 f"verify the grade rests on something other than this readout")

    # --- ordinal-score plausibility ---------------------------------------
    # A group mean of n integer scores must be a multiple of 1/n. Behavioural
    # rows on ordinal scales are typically n=3-6 animals, so a value like 4.1 is
    # arithmetically impossible and betrays a bar-height estimate read off a plot
    # rather than the plotted per-animal points. This is a cheap check that
    # catches a whole class of silently-wrong digitised values.
    # Scoped to values the curator says were read off a figure. Applying it to
    # every ordinal score would fire on exactly-transcribed spreadsheet values and
    # on ordinary 2-dp rounding, and a check that cries wolf is a check people
    # learn to ignore. The tolerance likewise allows for a value reported to two
    # decimal places rather than demanding exact rational equality.
    for m in meas:
        if not m["readout_unit"].startswith("score_0_to"):
            continue
        if not re.search(r"digitis|digitiz|read from|bar height|estimated from",
                         m["notes"] or "", re.I):
            continue
        v = m["readout_value"]
        if not v or v == TBD:
            continue
        try:
            x = float(v)
        except ValueError:
            continue
        if x == int(x):
            continue
        if not any(abs(x - round(x * k) / k) <= 0.005 for k in range(2, 13)):
            warn(f"{m['measurement_id']}: digitised ordinal score {x} is not a "
                 f"multiple of 1/n for any n<=12 — impossible as a group mean of "
                 f"integer scores, so it was read from bar height rather than from "
                 f"the plotted per-animal points")

    # --- sequence sanity --------------------------------------------------
    seq_re = re.compile(r"^[ACGTUacgtu]+$")
    filled = 0
    for o in oligos:
        s = (o["sequence_5to3"] or "").strip()
        if not s or s == TBD:
            continue
        filled += 1
        if not seq_re.match(s):
            err(f"{o['oligo_id']}: sequence_5to3 contains non-IUPAC characters")
            continue
        ln = o["length_nt"]
        if ln and ln not in (TBD, "NA"):
            try:
                if int(ln) != len(s):
                    warn(f"{o['oligo_id']}: length_nt={ln} but sequence is {len(s)} nt "
                         f"(check for 3'-caps/overhangs; explain in notes)")
            except ValueError:
                pass

    # --- summary ----------------------------------------------------------
    print(f"cns_oligos.csv        : {len(oligos)} oligos")
    print(f"cns_measurements.csv  : {len(meas)} measurements")
    print(f"sequences filled      : {filled}/{len(oligos)}")
    print("grade distribution    : " + " ".join(
        f"{g}:{sum(1 for m in meas if m['neurotox_grade'] == g)}" for g in "0123"))
    print("study types           : " + " ".join(
        f"{k}:{v}" for k, v in Counter(m["study_type"] for m in meas).most_common()))
    print("endpoint domains      : " + " ".join(
        f"{k}:{v}" for k, v in Counter(m["endpoint_domain"] for m in meas).most_common()))
    print("challenge priority    : " + " ".join(
        f"{k}:{v}" for k, v in Counter(m["challenge_priority"] for m in meas).most_common()))
    report()


def report():
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
