#!/usr/bin/env python3
"""
Enumerates every registered trial of an oligonucleotide therapeutic that has
POSTED RESULTS, and writes data/trial_registry.csv.

Why this exists. The first version of the ClinicalTrials.gov component carried a
hand-written map of 23 trials — the ones that turned up while chasing the
hydrocephalus signal. That biases the dataset toward the compounds already
suspected of causing the endpoint, and it silently omits the negative evidence
that makes the positives interpretable. This script instead asks the registry for
ALL of them, so trial selection is a query rather than a judgement.

Route is taken from the trial's OWN text (intervention and arm descriptions),
not assumed from the compound, and the matched sentence is stored in
`route_evidence` so the assignment is checkable. Where the record does not state
a route, the field is NOT_REPORTED.

Non-oligonucleotides that match a drug-name query are excluded by name with the
reason recorded, never silently dropped.

Output: data/trial_registry.csv
        sources/raw/ctgov_<NCT>.json for every trial with results
        notes/trial_discovery_report.txt
Usage:  python3 scripts/discover_ctgov_trials.py
"""
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "sources", "raw")
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")
API = "https://clinicaltrials.gov/api/v2/studies"

# Oligonucleotide therapeutics to enumerate. Aliases are folded to one canonical
# name so a trial found under two names is one row.
DRUGS = {
    "nusinersen": ["nusinersen"], "tofersen": ["tofersen"],
    "tominersen": ["tominersen"], "eplontersen": ["eplontersen", "ION-682884"],
    "inotersen": ["inotersen"], "eteplirsen": ["eteplirsen"],
    "golodirsen": ["golodirsen"], "viltolarsen": ["viltolarsen"],
    "casimersen": ["casimersen"], "patisiran": ["patisiran"],
    "vutrisiran": ["vutrisiran"], "givosiran": ["givosiran"],
    "lumasiran": ["lumasiran"], "nedosiran": ["nedosiran"],
    "inclisiran": ["inclisiran"], "volanesorsen": ["volanesorsen"],
    "mipomersen": ["mipomersen"], "pegaptanib": ["pegaptanib"],
    "defibrotide": ["defibrotide"], "imetelstat": ["imetelstat"],
    "fomivirsen": ["fomivirsen"], "zorevunersen": ["zorevunersen"],
    "elsunersen": ["elsunersen"], "BIIB080": ["BIIB080", "IONIS-MAPTRx"],
    "BIIB105": ["BIIB105"], "WVE-120101": ["WVE-120101"],
    "WVE-120102": ["WVE-120102"], "WVE-003": ["WVE-003"],
    "olezarsen": ["olezarsen"], "donidalorsen": ["donidalorsen"],
    "fitusiran": ["fitusiran"], "bepirovirsen": ["bepirovirsen"],
    "apatorsen": ["apatorsen"], "custirsen": ["custirsen"],
    "danvatirsen": ["danvatirsen"], "trabedersen": ["trabedersen"],
    "alicaforsen": ["alicaforsen"],
    # Development codes folded to the INN so one compound is one row:
    "sepofarsen": ["sepofarsen", "QR-110"],
    "ultevursen": ["ultevursen", "QR-421a"],
}

# Matched by a drug query but NOT an oligonucleotide. Recorded, not silently dropped.
NOT_OLIGONUCLEOTIDE = {
    "imlifidase": "an IgG-degrading endopeptidase (enzyme), not an oligonucleotide",
}

ROUTE_PATTERNS = [
    ("intrathecal_lumbar", r"intrathecal|intra-thecal|lumbar puncture|\bIT\s+(?:dose|injection|administration)"),
    ("intracerebroventricular", r"intracerebroventricular|intraventricular|\bICV\b"),
    ("intravitreal", r"intravitreal|intra-vitreal|intravitreous"),
    ("subcutaneous", r"subcutaneous|subcutaneously|\bSC\b|\bSQ\b"),
    ("intravenous", r"intravenous|intravenously|\bIV\b|infusion"),
    ("oral", r"\boral(?:ly)?\b|by mouth"),
    ("topical_enema", r"\benema\b|rectal"),
]


def fetch(url, cache):
    path = os.path.join(RAW, cache)
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                payload = json.load(r)
            with open(path, "w") as fh:
                json.dump(payload, fh)
            time.sleep(0.15)
            return payload
        except Exception:
            time.sleep(2 ** attempt)
    return None


def route_of(doc):
    """Route from the trial's own text, with the matched sentence as evidence."""
    ps = doc.get("protocolSection", {})
    chunks = []
    for iv in ps.get("armsInterventionsModule", {}).get("interventions", []):
        chunks.append("%s %s" % (iv.get("name", ""), iv.get("description", "")))
    for arm in ps.get("armsInterventionsModule", {}).get("armGroups", []):
        chunks.append(arm.get("description", "") or "")
    chunks.append(ps.get("designModule", {}).get("designInfo", {}).get("description", "") or "")
    text = " ".join(c for c in chunks if c)
    for route, pat in ROUTE_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            lo = max(0, m.start() - 90)
            return route, re.sub(r"\s+", " ", text[lo:m.end() + 90]).strip()[:220]
    return "NOT_REPORTED", "no route statement found in the trial's intervention or arm descriptions"


def main():
    for d in (RAW, DATA, NOTES):
        os.makedirs(d, exist_ok=True)
    found, report = {}, []

    for canonical, aliases in DRUGS.items():
        seen = set()
        for alias in aliases:
            url = (API + "?query.intr=" + urllib.parse.quote(alias) +
                   "&fields=NCTId,BriefTitle,HasResults,OverallStatus&pageSize=200")
            payload = fetch(url, "ctgov_query_%s.json" % re.sub(r"\W+", "_", alias))
            if not payload:
                report.append("%-14s QUERY FAILED for alias %s" % (canonical, alias))
                continue
            for st in payload.get("studies", []):
                if not st.get("hasResults"):
                    continue
                nct = st["protocolSection"]["identificationModule"]["nctId"]
                seen.add(nct)
        for nct in sorted(seen):
            found.setdefault(nct, set()).add(canonical)
        report.append("%-14s %3d trials with posted results" % (canonical, len(seen)))

    rows = []
    for nct, drugs in sorted(found.items()):
        doc = fetch(API + "/" + nct, "ctgov_%s.json" % nct)
        if not doc:
            report.append("%s FETCH FAILED" % nct)
            continue
        ps = doc.get("protocolSection", {})
        ident = ps.get("identificationModule", {})
        title = ident.get("briefTitle", "")
        conditions = "; ".join(ps.get("conditionsModule", {}).get("conditions", []))
        ivnames = " ".join(i.get("name", "") for i in
                           ps.get("armsInterventionsModule", {}).get("interventions", []))
        excluded = ""
        for name, why in NOT_OLIGONUCLEOTIDE.items():
            if name.lower() in ivnames.lower() and len(drugs) == 1 and name in drugs:
                excluded = why
        route, evidence = route_of(doc)
        has_ae = bool((doc.get("resultsSection") or {}).get("adverseEventsModule"))
        rows.append(dict(
            nct_id=nct, drug="; ".join(sorted(drugs)), route=route,
            route_evidence=evidence, has_adverse_event_module=str(has_ae).upper(),
            overall_status=ps.get("statusModule", {}).get("overallStatus", ""),
            brief_title=title[:180], conditions=conditions[:180],
            interventions=ivnames[:180], excluded_reason=excluded))

    cols = ["nct_id", "drug", "route", "route_evidence", "has_adverse_event_module",
            "overall_status", "brief_title", "conditions", "interventions",
            "excluded_reason"]
    with open(os.path.join(DATA, "trial_registry.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    usable = [r for r in rows if not r["excluded_reason"]
              and r["has_adverse_event_module"] == "TRUE"]
    byroute = {}
    for r in usable:
        byroute[r["route"]] = byroute.get(r["route"], 0) + 1
    with open(os.path.join(NOTES, "trial_discovery_report.txt"), "w") as fh:
        fh.write("ClinicalTrials.gov trial discovery\n" + "=" * 62 + "\n")
        fh.write("%d trials with posted results; %d usable (oligonucleotide, has an "
                 "adverse-event module)\n" % (len(rows), len(usable)))
        fh.write("routes among usable trials: %s\n\n" % byroute)
        fh.write("\n".join(report) + "\n")

    print("wrote data/trial_registry.csv: %d trials with results, %d usable"
          % (len(rows), len(usable)))
    print("routes among usable trials:", byroute)
    print("excluded:", sum(1 for r in rows if r["excluded_reason"]))
    print("no AE module:", sum(1 for r in rows if r["has_adverse_event_module"] != "TRUE"))


if __name__ == "__main__":
    main()
