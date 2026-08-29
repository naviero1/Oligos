#!/usr/bin/env python3
"""
Deterministic extraction of hydrocephalus / CSF-dynamics pharmacovigilance rows
from the FDA Adverse Event Reporting System via the openFDA API.

Query strategy. openFDA caps a `count` aggregation at 100 buckets without an API
key, so counting reaction terms per drug would silently truncate. This script
inverts the query: for each reaction term of interest it counts reports **by
drug**, which puts every oligonucleotide in one bucket list, and separately
retrieves each drug's total report count as the denominator.

What these rows are and are not. FAERS is a spontaneous, voluntary reporting
system. A count is a number of REPORTS, not a number of patients and not an
incidence: there is no exposure denominator, reporting is biased by publicity,
indication and time on market, and a report is not evidence of causation. The
denominator recorded here (`n_at_risk`) is the drug's total FAERS report count,
so the ratio is a *reporting proportion within the drug's own reports* and
nothing more. This script deliberately computes no PRR, ROR or signal score —
see SCHEMA.md §"Deliberate limits of this schema".

Output: data/_faers_measurements.csv
        sources/raw/faers_*.json (every payload, committed)
        notes/faers_extraction_report.txt

Usage: python3 scripts/extract_faers.py
"""
import csv
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "sources", "raw")
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")
API = "https://api.fda.gov/drug/event.json"

# --------------------------------------------------------------------------
# Reaction terms. Spellings are MedDRA preferred terms exactly as FAERS stores
# them, confirmed by a vocabulary probe rather than assumed.
# --------------------------------------------------------------------------
TERMS = [
    # term, tier, readout_category, tox_axis
    ("HYDROCEPHALUS", "A", "hydrocephalus_event", "ventricular_enlargement"),
    ("NORMAL PRESSURE HYDROCEPHALUS", "A", "hydrocephalus_event", "ventricular_enlargement"),
    ("COMMUNICATING HYDROCEPHALUS", "A", "hydrocephalus_event", "ventricular_enlargement"),
    ("CONGENITAL HYDROCEPHALUS", "A", "hydrocephalus_event", "ventricular_enlargement"),
    ("VENTRICULOMEGALY", "A", "ventricular_morphometry", "ventricular_enlargement"),
    ("CEREBRAL VENTRICLE DILATATION", "A", "ventricular_morphometry", "ventricular_enlargement"),
    ("INTRACRANIAL PRESSURE INCREASED", "B", "csf_pressure", "csf_pressure_disturbance"),
    ("PAPILLOEDEMA", "B", "csf_pressure", "csf_pressure_disturbance"),
    ("MENINGITIS ASEPTIC", "B", "csf_composition", "csf_composition_disturbance"),
    ("MENINGITIS CHEMICAL", "B", "csf_composition", "csf_composition_disturbance"),
    ("ARACHNOIDITIS", "B", "csf_dynamics", "csf_composition_disturbance"),
    ("CEREBROSPINAL FLUID LEAKAGE", "B", "csf_dynamics", "delivery_procedure_complication"),
    ("CEREBROSPINAL FLUID PROTEIN INCREASED", "B", "csf_composition", "csf_composition_disturbance"),
    ("POST LUMBAR PUNCTURE SYNDROME", "B", "procedure_complication", "delivery_procedure_complication"),
]

# --------------------------------------------------------------------------
# Oligonucleotide therapeutics. `route` is the approved/clinical route and is
# the variable the route-contrast control turns on.
# --------------------------------------------------------------------------
DRUGS = [
    # generic, brand aliases (upper case as FAERS stores medicinalproduct), route
    ("nusinersen", ["SPINRAZA"], "intrathecal_lumbar"),
    ("tofersen", ["QALSODY"], "intrathecal_lumbar"),
    ("tominersen", ["TOMINERSEN", "RO7234292", "RG6042"], "intrathecal_lumbar"),
    ("eplontersen", ["WAINUA"], "subcutaneous"),
    ("inotersen", ["TEGSEDI"], "subcutaneous"),
    ("eteplirsen", ["EXONDYS 51", "EXONDYS"], "intravenous"),
    ("golodirsen", ["VYONDYS 53", "VYONDYS"], "intravenous"),
    ("viltolarsen", ["VILTEPSO"], "intravenous"),
    ("casimersen", ["AMONDYS 45", "AMONDYS"], "intravenous"),
    ("patisiran", ["ONPATTRO"], "intravenous"),
    ("vutrisiran", ["AMVUTTRA"], "subcutaneous"),
    ("givosiran", ["GIVLAARI"], "subcutaneous"),
    ("lumasiran", ["OXLUMO"], "subcutaneous"),
    ("nedosiran", ["RIVFLOZA"], "subcutaneous"),
    ("inclisiran", ["LEQVIO"], "subcutaneous"),
    ("volanesorsen", ["WAYLIVRA"], "subcutaneous"),
    ("mipomersen", ["KYNAMRO"], "subcutaneous"),
    ("pegaptanib", ["MACUGEN"], "intravitreal"),
    ("defibrotide", ["DEFITELIO"], "intravenous"),
    ("imetelstat", ["RYTELO"], "intravenous"),
    ("fomivirsen", ["VITRAVENE"], "intravitreal"),
]


def fetch(params, cache_name):
    """GET with an on-disk cache so a re-run costs no API quota."""
    path = os.path.join(RAW, cache_name)
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    url = API + "?" + urllib.parse.urlencode(params)
    payload = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=90) as resp:
                payload = json.load(resp)
            break
        except urllib.error.HTTPError as exc:
            # openFDA returns 404 with a NOT_FOUND error body when a search matches
            # nothing. That is a real zero, not a failure, and must be recorded.
            body = exc.read().decode("utf-8", "replace")
            try:
                payload = json.loads(body)
            except ValueError:
                payload = {"error": {"code": "HTTP_%s" % exc.code,
                                     "message": body[:200]}}
            if exc.code == 404:
                break            # genuine "no matching records"
            if exc.code not in (429, 500, 502, 503, 504):
                break
            time.sleep(2 ** attempt)
        except Exception as exc:                     # transient transport failure
            payload = {"error": {"code": "TRANSPORT",
                                 "message": type(exc).__name__ + ": " + str(exc)[:150]}}
            time.sleep(2 ** attempt)
    if payload is None or payload.get("error", {}).get("code") == "TRANSPORT":
        # Do NOT cache a transport failure as if it were a zero.
        raise RuntimeError("openFDA unreachable after retries: %s" % cache_name)
    with open(path, "w") as fh:
        json.dump(payload, fh)
    time.sleep(1.0)   # stay well inside the unauthenticated rate limit
    return payload


def drug_clause(generic, brands):
    parts = ['patient.drug.openfda.generic_name:"%s"' % generic]
    parts += ['patient.drug.medicinalproduct:"%s"' % b for b in brands]
    return "(" + " OR ".join(parts) + ")"


def main():
    for d in (RAW, DATA, NOTES):
        os.makedirs(d, exist_ok=True)
    report = []
    today = date.today().isoformat()

    # ---- denominators: each drug's total FAERS report count ---------------
    totals = {}
    for generic, brands, _route in DRUGS:
        payload = fetch({"search": drug_clause(generic, brands), "limit": 1},
                        "faers_total_%s.json" % generic)
        total = (payload.get("meta", {}).get("results", {}) or {}).get("total", 0)
        totals[generic] = total
        report.append("total reports  %-14s %8d" % (generic, total))

    # ---- numerators: one EXACT query per (drug, term) ---------------------
    # An aggregation counting drugs within a term truncates at openFDA's 100-bucket
    # cap, which silently drops exactly the rare drug/term pairs this dataset is
    # about. A direct search for the pair returns meta.results.total with no cap,
    # so a zero here is a real zero.
    rows = []
    for term, tier, category, axis in TERMS:
        slug = term.lower().replace(" ", "_")
        for generic, brands, route in DRUGS:
            payload = fetch(
                {"search": '%s AND patient.reaction.reactionmeddrapt.exact:"%s"'
                           % (drug_clause(generic, brands), term),
                 "limit": 1},
                "faers_pair_%s_%s.json" % (generic, slug))
            n = (payload.get("meta", {}).get("results", {}) or {}).get("total", 0)
            total = totals.get(generic, 0)
            if total == 0:
                continue           # drug absent from FAERS entirely; no denominator
            asc = "measured_positive" if n else "measured_null"
            if n:
                grade = 3 if category == "hydrocephalus_event" else (
                    1 if category in ("ventricular_morphometry", "procedure_complication") else 2)
                basis = (
                    "Grade assigned from the MedDRA preferred term alone, per the "
                    "SCHEMA.md rubric, because a FAERS aggregate carries no clinical "
                    "narrative: hydrocephalus terms -> 3, ventricular imaging and "
                    "procedure terms -> 1, pressure/composition terms -> 2. This is a "
                    "weaker basis than a trial or case row and must not be pooled with "
                    "them without stratifying on study_type.")
            else:
                grade = 0
                basis = ("0 = no FAERS report for this drug carries this reaction term. "
                         "Absence in a spontaneous system is weak evidence; see "
                         "ascertainment_basis.")
            rows.append(dict(
                oligo_name=generic,
                source_key="FAERS_openFDA",
                study_type="pharmacovigilance",
                species="human",
                strain="NOT_APPLICABLE",
                system_model="FDA Adverse Event Reporting System, spontaneous reports",
                is_human_system="TRUE",
                indication_population="NOT_REPORTED",
                arm_label="all reports naming this drug",
                arm_description="NOT_APPLICABLE",
                arm_role="exposed",
                cns_compartment=("CSF_and_neuraxis" if route == "intrathecal_lumbar"
                                 else "NOT_APPLICABLE"),
                delivery_route=route,
                exposure_duration="NOT_REPORTED",
                timepoint="NOT_REPORTED",
                endpoint_tier=tier,
                readout_category=category,
                readout_name="faers_reports_%s" % slug,
                readout_term_verbatim=term,
                readout_value=n,
                readout_unit="reports",
                readout_is_qualitative="FALSE",
                n_affected=n,
                n_at_risk=total,
                comparator_arm="NOT_APPLICABLE",
                n_affected_comparator="NOT_APPLICABLE",
                n_at_risk_comparator="NOT_APPLICABLE",
                statistic="NOT_REPORTED",
                effect_direction=("increase" if n else "no_change"),
                seriousness="NOT_REPORTED",
                assessment_type="spontaneous_report",
                organ_system="NOT_REPORTED",
                source_vocabulary="MedDRA preferred term as stored by FAERS",
                hydroceph_grade=grade,
                grade_basis=basis,
                grade_status="provisional",
                ascertainment=asc,
                ascertainment_basis=(
                    "FAERS is a voluntary spontaneous-reporting system with no exposure "
                    "denominator. n_at_risk is the drug's TOTAL FAERS report count, so "
                    "n_affected/n_at_risk is a reporting proportion within that drug's "
                    "own reports and is not an incidence. Absence of a term reflects "
                    "reporting behaviour as much as clinical absence."),
                attribution_as_stated="not_discussed",
                attribution_evidence=(
                    "FAERS records no causality assessment. A report associates a drug "
                    "with an event; it does not attribute one to the other."),
                tox_axis=axis,
                source_ref=('openFDA drug/event: '
                            'search=patient.reaction.reactionmeddrapt.exact:"%s" '
                            'count by drug; denominator search=%s'
                            % (term, drug_clause(generic, brands))),
                source_location=("api.fda.gov/drug/event.json results[] bucket "
                                 "matching this drug name"),
                redistribution="public_domain",
                notes=("openFDA API, retrieved %s. Payloads committed under "
                       "sources/raw/faers_*.json." % today),
            ))

    out = os.path.join(DATA, "_faers_measurements.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(NOTES, "faers_extraction_report.txt"), "w") as fh:
        fh.write("openFDA FAERS extraction audit trail\nretrieved %s\n" % today)
        fh.write("=" * 60 + "\n" + "\n".join(report) + "\n")

    pos = [r for r in rows if r["ascertainment"] == "measured_positive"]
    print("wrote %s: %d rows (%d positive, %d null)" % (out, len(rows), len(pos),
                                                        len(rows) - len(pos)))
    for r in sorted(pos, key=lambda r: -int(r["n_affected"]))[:30]:
        print("   %-12s %-38s %6s / %-7s  tier %s" % (
            r["oligo_name"], r["readout_term_verbatim"], r["n_affected"],
            r["n_at_risk"], r["endpoint_tier"]))


if __name__ == "__main__":
    main()
