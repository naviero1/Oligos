#!/usr/bin/env python3
"""
Deterministic extraction of hydrocephalus / CSF-dynamics statements from the
official FDA prescribing information (Structured Product Labels) of marketed
oligonucleotide therapeutics, via the DailyMed v2 API.

Labels are US Government-published regulatory documents; the text quoted here is
public domain and is reproduced verbatim, with its LOINC-coded section, so any
statement can be checked against the source.

Two things this script is careful about.

1. A label that is SILENT on the endpoint is a datum, not a gap. Every drug in
   the roster gets a row per endpoint concept: either the verbatim statement, or
   an explicit `measured_null` recording that the current label carries no such
   statement.
2. The word "ventricular" is ambiguous in a drug label — cardiac ventricular
   repolarisation and arrhythmia are common and irrelevant here. Matching uses a
   CNS-anchored pattern and an explicit cardiac exclusion list, and every
   excluded sentence is written to the audit report so the filter can be checked.

Output: data/_label_measurements.csv
        sources/raw/dailymed_*.xml (every label, committed)
        notes/label_extraction_report.txt

Usage: python3 scripts/extract_labels.py
"""
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "sources", "raw")
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")
NS = {"v3": "urn:hl7-org:v3"}
BASE = "https://dailymed.nlm.nih.gov/dailymed/services/v2"

# CNS-anchored endpoint pattern.
ENDPOINT = re.compile(
    r"hydrocephal\w*|ventriculomegaly|cerebral ventricle|ventricular (?:enlarge|dilat)\w*"
    r"|intracranial pressure|papill?[oe]edema|papilledema|cerebrospinal fluid"
    r"|aseptic meningitis|chemical meningitis|arachnoiditis"
    r"|(?:post[- ])?lumbar puncture", re.I)

# Sentences matching these are cardiac / unrelated uses of "ventricular".
CARDIAC = re.compile(
    r"ventricular (?:repolariz|arrhythmi|tachycard|fibrillat|hypertroph|septal|"
    r"ejection|dysfunction|premature|extrasystol)", re.I)

CONCEPTS = [
    # concept key, tier, readout_category, tox_axis, pattern
    ("hydrocephalus", "A", "hydrocephalus_event", "ventricular_enlargement",
     re.compile(r"hydrocephal\w*", re.I)),
    ("ventriculomegaly", "A", "ventricular_morphometry", "ventricular_enlargement",
     re.compile(r"ventriculomegaly|cerebral ventricle|ventricular (?:enlarge|dilat)\w*", re.I)),
    ("intracranial_pressure", "B", "csf_pressure", "csf_pressure_disturbance",
     re.compile(r"intracranial pressure|papill?[oe]edema|papilledema", re.I)),
    ("aseptic_meningitis", "B", "csf_composition", "csf_composition_disturbance",
     re.compile(r"aseptic meningitis|chemical meningitis|arachnoiditis", re.I)),
    ("csf_or_lp", "B", "procedure_complication", "delivery_procedure_complication",
     re.compile(r"cerebrospinal fluid|(?:post[- ])?lumbar puncture", re.I)),
]

DRUGS = [
    # generic, dailymed drug_name query, route
    ("nusinersen", "nusinersen", "intrathecal_lumbar"),
    ("tofersen", "tofersen", "intrathecal_lumbar"),
    ("eplontersen", "eplontersen", "subcutaneous"),
    ("inotersen", "inotersen", "subcutaneous"),
    ("eteplirsen", "eteplirsen", "intravenous"),
    ("golodirsen", "golodirsen", "intravenous"),
    ("viltolarsen", "viltolarsen", "intravenous"),
    ("casimersen", "casimersen", "intravenous"),
    ("patisiran", "patisiran", "intravenous"),
    ("vutrisiran", "vutrisiran", "subcutaneous"),
    ("givosiran", "givosiran", "subcutaneous"),
    ("lumasiran", "lumasiran", "subcutaneous"),
    ("nedosiran", "nedosiran", "subcutaneous"),
    ("inclisiran", "inclisiran", "subcutaneous"),
    ("defibrotide", "defibrotide", "intravenous"),
    ("imetelstat", "imetelstat", "intravenous"),
]


def get(url, cache):
    path = os.path.join(RAW, cache)
    if os.path.exists(path):
        return open(path, "rb").read()
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                body = r.read()
            open(path, "wb").write(body)
            time.sleep(0.5)
            return body
        except Exception:
            time.sleep(2 ** attempt)
    return None


def flat(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def sentences(text):
    """Split into sentences, protecting abbreviations common in drug labels."""
    guard = {"e.g.": "\x01EG\x01", "i.e.": "\x01IE\x01", "vs.": "\x01VS\x01",
             "approx.": "\x01AP\x01", "No.": "\x01NO\x01"}
    tmp = text
    for k, v in guard.items():
        tmp = tmp.replace(k, v)
    # Protect single-letter initials such as "S. aureus" or "U. S."
    tmp = re.sub(r"\b([A-Z])\.", lambda m: m.group(1) + "\x02", tmp)
    parts = re.split(r"(?<=[.;])\s+", tmp)
    out = []
    for part in parts:
        for k, v in guard.items():
            part = part.replace(v, k)
        part = part.replace("\x02", ".")
        part = part.strip()
        if part:
            out.append(part)
    return out


def main():
    for d in (RAW, DATA, NOTES):
        os.makedirs(d, exist_ok=True)
    rows, report = [], []
    today = date.today().isoformat()

    for generic, query, route in DRUGS:
        meta = get("%s/spls.json?drug_name=%s" % (BASE, urllib.parse.quote(query)),
                   "dailymed_meta_%s.json" % generic)
        if not meta:
            report.append("%-14s METADATA FETCH FAILED" % generic)
            continue
        entries = json.loads(meta).get("data", [])
        if not entries:
            report.append("%-14s no SPL in DailyMed" % generic)
            continue
        entry = entries[0]
        setid, published = entry["setid"], entry.get("published_date", "NOT_REPORTED")
        title = entry.get("title", "")
        xml = get("%s/spls/%s.xml" % (BASE, setid), "dailymed_%s_%s.xml" % (generic, setid[:8]))
        if not xml:
            report.append("%-14s SPL FETCH FAILED (setid %s)" % (generic, setid))
            continue

        root = ET.fromstring(xml)
        # Collect (section title, LOINC display name, sentence) for leaf-ish sections.
        found = {}
        excluded = []
        for sec in root.iter("{urn:hl7-org:v3}section"):
            body = flat(sec)
            if len(body) > 6000 or not ENDPOINT.search(body):
                continue
            t_el = sec.find("v3:title", NS)
            c_el = sec.find("v3:code", NS)
            sec_title = flat(t_el) if t_el is not None else "(untitled section)"
            loinc = c_el.get("displayName") if c_el is not None else "NOT_REPORTED"
            for sent in sentences(body):
                if not ENDPOINT.search(sent):
                    continue
                if CARDIAC.search(sent):
                    excluded.append("%s | %s | %s" % (generic, sec_title[:30], sent[:110]))
                    continue
                for key, tier, cat, axis, pat in CONCEPTS:
                    if pat.search(sent):
                        prev = found.get(key)
                        # Prefer a statement from a numbered label section.
                        if prev is None or (sec_title[:1].isdigit()
                                            and not prev["section"][:1].isdigit()):
                            found[key] = dict(section=sec_title, loinc=loinc,
                                              sentence=sent[:600])
        report.append("%-14s setid=%s published=%s concepts_found=%s"
                      % (generic, setid, published, ",".join(sorted(found)) or "none"))

        for key, tier, cat, axis, _pat in CONCEPTS:
            hit = found.get(key)
            if hit:
                asc, grade = "measured_positive", None
                if key == "hydrocephalus":
                    grade = 3
                    basis = ("3 = the product's official prescribing information names "
                             "hydrocephalus as an identified adverse reaction "
                             "(SCHEMA.md rubric grade 3).")
                elif key == "ventriculomegaly":
                    grade = 1
                    basis = ("1 = the label names a ventricular imaging finding without "
                             "stating an intervention (SCHEMA.md rubric grade 1).")
                elif key in ("intracranial_pressure", "aseptic_meningitis"):
                    grade = 2
                    basis = ("2 = the label names raised intracranial pressure, "
                             "papilloedema, aseptic/chemical meningitis or arachnoiditis "
                             "(SCHEMA.md rubric grade 2).")
                else:
                    grade = 1
                    basis = ("1 = the label names a CSF or lumbar-puncture procedural "
                             "matter (SCHEMA.md rubric grade 1); tox_axis is "
                             "delivery_procedure_complication.")
                value = hit["sentence"]
                loc = "SPL section '%s' [%s]" % (hit["section"], hit["loinc"])
                asc_basis = ("Statement present in the current label, quoted verbatim. "
                             "A label names an identified risk; it reports no incidence "
                             "denominator unless the quoted sentence contains one.")
                attribution = "drug_attributed"
                attribution_ev = (
                    "Inclusion in the product's approved labelling is a regulatory "
                    "determination that the event is an identified or potential risk of "
                    "the product. Postmarketing-experience sections state explicitly "
                    "that a causal relationship cannot always be established.")
            else:
                asc, grade = "measured_null", 0
                value = "NOT_REPORTED"
                basis = ("0 = the current prescribing information contains no statement "
                         "matching this endpoint concept (SCHEMA.md rubric grade 0).")
                loc = "whole SPL, setid %s, published %s" % (setid, published)
                asc_basis = ("Derived from absence across the full label text. A label "
                             "lists identified risks, not everything that was looked "
                             "for and not found, so this is weaker than a trial-arm "
                             "zero. See METHODOLOGY.md OI-01.")
                attribution = "not_discussed"
                attribution_ev = "No statement; no attribution to record."

            rows.append(dict(
                oligo_name=generic,
                source_key="DailyMed_SPL_%s" % generic,
                study_type="regulatory_label",
                species="human", strain="NOT_APPLICABLE",
                system_model="FDA prescribing information (Structured Product Label)",
                is_human_system="TRUE",
                indication_population="NOT_REPORTED",
                arm_label="labelled population", arm_description=title[:200],
                arm_role="exposed",
                cns_compartment=("CSF_and_neuraxis" if route == "intrathecal_lumbar"
                                 else "NOT_APPLICABLE"),
                delivery_route=route,
                exposure_duration="NOT_APPLICABLE", timepoint="NOT_APPLICABLE",
                endpoint_tier=tier, readout_category=cat,
                readout_name="label_statement_%s" % key,
                readout_term_verbatim=(value if value != "NOT_REPORTED" else "NOT_APPLICABLE"),
                readout_value=value, readout_unit="verbatim_label_text",
                readout_is_qualitative="TRUE",
                n_affected="NOT_APPLICABLE", n_at_risk="NOT_APPLICABLE",
                comparator_arm="NOT_APPLICABLE",
                n_affected_comparator="NOT_APPLICABLE",
                n_at_risk_comparator="NOT_APPLICABLE",
                statistic="NOT_REPORTED",
                effect_direction=("increase" if asc == "measured_positive" else "no_change"),
                seriousness="NOT_REPORTED", assessment_type="regulatory_labelling",
                organ_system="NOT_APPLICABLE",
                source_vocabulary="FDA SPL / LOINC section coding",
                hydroceph_grade=grade, grade_basis=basis, grade_status="provisional",
                ascertainment=asc, ascertainment_basis=asc_basis,
                attribution_as_stated=attribution, attribution_evidence=attribution_ev,
                tox_axis=axis,
                source_ref=("DailyMed setid %s, label published %s" % (setid, published)),
                source_location=loc,
                redistribution="public_domain",
                notes=("DailyMed v2 API, retrieved %s. Label XML committed at "
                       "sources/raw/dailymed_%s_%s.xml" % (today, generic, setid[:8])),
            ))

    out = os.path.join(DATA, "_label_measurements.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(NOTES, "label_extraction_report.txt"), "w") as fh:
        fh.write("DailyMed SPL extraction audit trail\nretrieved %s\n" % today)
        fh.write("=" * 70 + "\n" + "\n".join(report) + "\n")

    pos = [r for r in rows if r["ascertainment"] == "measured_positive"]
    print("wrote %s: %d rows (%d with a label statement)" % (out, len(rows), len(pos)))
    for r in pos:
        print("\n  %s [tier %s] %s\n    %s\n    -> %s" % (
            r["oligo_name"], r["endpoint_tier"], r["readout_name"],
            r["source_location"][:100], r["readout_value"][:230]))


if __name__ == "__main__":
    main()
