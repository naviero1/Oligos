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
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")
MEAS = os.path.join(ROOT, "data", "measurements.csv")

TBD = "TBD"

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
             "redistribution", "notes"]

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
