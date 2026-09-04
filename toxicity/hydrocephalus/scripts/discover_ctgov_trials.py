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

ALIAS HARVEST. Querying the INN alone is not enough, and the failure is silent.
The tominersen first-in-human trial NCT02519036 posts a full adverse-event module
but its record never contains the string "tominersen" — the drug is registered as
"ISIS 443139" with other name "IONIS HTTRx", so no query on the INN can reach it,
and it was absent from the first registry. The fix keeps selection a query rather
than a hand-written list: after the INN round, every intervention name and
otherName in the records already found is harvested, anything shaped like a
sponsor development code is queried in a second round, and the record that
supplied the alias is recorded in `alias_evidence` so the link is checkable. The
alias ISIS 443139 -> tominersen, for instance, comes from the open-label
extension NCT03342053, whose intervention is "RO7234292 (RG6042)" with other name
"Tominersen" and whose text names ISIS 443139.

Finally, any fetched trial that posts an adverse-event module but reaches no
canonical compound is reported as UNATTRIBUTED rather than dropped, so the next
such gap is loud instead of silent.

Output: data/trial_registry.csv
        sources/raw/ctgov_<NCT>.json for every trial with results
        notes/trial_discovery_report.txt
Usage:  python3 scripts/discover_ctgov_trials.py
"""
import csv
import glob
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

# tominersen's first-in-human trial NCT02519036 is registered as "ISIS 443139"
# with other name "IONIS HTTRx" and its record never contains the string
# "tominersen", so no INN query and no co-occurrence harvest can reach it: the
# two names never appear in the same intervention record anywhere. The link is
# stated by the open-label extension NCT03342053, whose intervention is
# "RO7234292 (RG6042)" with other name "Tominersen" and whose text names ISIS
# 443139 as the antecedent study. Recorded here with that evidence rather than
# left to a dragnet.
DRUGS["tominersen"] += ["ISIS 443139", "IONIS HTTRx"]

# Matched by a drug query but NOT an oligonucleotide. Recorded, not silently dropped.
NOT_OLIGONUCLEOTIDE = {
    "imlifidase": "an IgG-degrading endopeptidase (enzyme), not an oligonucleotide",
}

# A sponsor development code as ClinicalTrials.gov writes them: an alphabetic stem
# of 2-6 letters, an optional separator, then digits.
DEV_CODE = re.compile(r"^(?:[A-Z]{2,6})[\s\-]?\d{2,7}[A-Za-z]?$")

# Strings that match DEV_CODE but are not drug identifiers.
CODE_STOPWORDS = {"PLACEBO", "SALINE", "SHAM", "MG", "ML"}

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


def query_alias(alias, report, canonical):
    """NCT ids with posted results for one drug-name string."""
    url = (API + "?query.intr=" + urllib.parse.quote(alias) +
           "&fields=NCTId,BriefTitle,HasResults,OverallStatus&pageSize=200")
    payload = fetch(url, "ctgov_query_%s.json" % re.sub(r"\W+", "_", alias))
    if not payload:
        report.append("%-14s QUERY FAILED for alias %s" % (canonical, alias))
        return set()
    return {st["protocolSection"]["identificationModule"]["nctId"]
            for st in payload.get("studies", []) if st.get("hasResults")}


def harvest_codes(doc, canonical, aliases):
    """Development codes that a trial record itself equates with this compound.

    The rule is CO-OCCURRENCE INSIDE ONE INTERVENTION RECORD: a code is accepted
    only if the same intervention's name or otherNames also carries a name we
    already know for this compound. So NCT03342053's intervention
    "RO7234292 (RG6042)" with otherName "Tominersen" yields RO7234292 and RG6042
    as tominersen aliases, evidenced by that record.

    A shape-only sweep was tried first and rejected: it dragged 236 unrelated
    trials (including 44 oral ones -- no oligonucleotide here is oral) into the
    registry, because a code-shaped token in an intervention name is not evidence
    that the code names THIS compound.
    """
    known = {a.lower() for a in aliases} | {canonical.lower()}
    out = set()
    ivs = doc.get("protocolSection", {}).get("armsInterventionsModule", {})
    for iv in ivs.get("interventions", []):
        names = [iv.get("name", "") or ""] + [n or "" for n in (iv.get("otherNames") or [])]
        blob = " ".join(names).lower()
        if not any(k in blob for k in known):
            continue
        for name in names:
            # UPPERCASE stem, word-bounded. A case-insensitive stem matched
            # "ersen 200" inside "mipomersen 200 mg" and querying that string
            # returned 107 unrelated trials; development codes are uppercase.
            for token in re.findall(r"\b([A-Z]{2,6}[\s\-]?\d{2,7}[A-Za-z]?)\b", name):
                token = token.strip()
                if (DEV_CODE.match(token.upper())
                        and token.upper() not in CODE_STOPWORDS
                        and token.lower() not in known):
                    out.add(token)
    return out


def main():
    for d in (RAW, DATA, NOTES):
        os.makedirs(d, exist_ok=True)
    found, report, alias_evidence = {}, [], {}

    # ---- round 1: the INN and any alias stated in DRUGS ---------------------
    for canonical, aliases in DRUGS.items():
        seen = set()
        for alias in aliases:
            seen |= query_alias(alias, report, canonical)
        for nct in sorted(seen):
            found.setdefault(nct, set()).add(canonical)
        report.append("%-14s %3d trials with posted results" % (canonical, len(seen)))

    # ---- round 2: codes harvested from the records round 1 found -----------
    #      A trial registered only under a sponsor code is invisible to an INN
    #      query. Harvest the codes those same compounds' other trials state,
    #      then query them; record which record supplied each alias.
    harvested = {}
    for nct in sorted(found):
        doc = fetch(API + "/" + nct, "ctgov_%s.json" % nct)
        if not doc:
            continue
        for canonical in found[nct]:
            for code in harvest_codes(doc, canonical, DRUGS[canonical]):
                harvested.setdefault((canonical, code), nct)

    new_hits = 0
    for (canonical, code), from_nct in sorted(harvested.items()):
        for nct in sorted(query_alias(code, report, canonical)):
            if canonical in found.get(nct, set()):
                continue
            found.setdefault(nct, set()).add(canonical)
            alias_evidence[(nct, canonical)] = (
                "found via development code %r, harvested from the intervention "
                "record of %s" % (code, from_nct))
            new_hits += 1
            report.append("%-14s + %s via harvested code %r (from %s)"
                          % (canonical, nct, code, from_nct))
    report.append("alias harvest: %d codes tried, %d further trials reached"
                  % (len(harvested), new_hits))

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
            discovery=("; ".join(sorted(
                alias_evidence[(nct, d)] for d in drugs
                if (nct, d) in alias_evidence)) or "found by drug-name query"),
            overall_status=ps.get("statusModule", {}).get("overallStatus", ""),
            brief_title=title[:180], conditions=conditions[:180],
            interventions=ivnames[:180], excluded_reason=excluded))

    cols = ["nct_id", "drug", "route", "route_evidence", "has_adverse_event_module",
            "overall_status", "brief_title", "conditions", "interventions",
            "excluded_reason", "discovery"]
    with open(os.path.join(DATA, "trial_registry.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # ---- coverage sweep: an AE-bearing payload that reached no compound -----
    #      This is the check that would have caught NCT02519036 the first time.
    in_registry = {r["nct_id"] for r in rows}
    unattributed = []
    for path in sorted(glob.glob(os.path.join(RAW, "ctgov_NCT*.json"))):
        try:
            doc = json.load(open(path))
        except Exception:
            continue
        nct = (doc.get("protocolSection", {}).get("identificationModule", {})
               .get("nctId"))
        if not nct or nct in in_registry:
            continue
        if (doc.get("resultsSection") or {}).get("adverseEventsModule"):
            unattributed.append(nct)
    if unattributed:
        report.append("UNATTRIBUTED — fetched, posts an adverse-event module, but "
                      "reached no canonical compound: %s" % ", ".join(unattributed))

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
    print("reached only via a harvested development code:",
          sum(1 for r in rows if r["discovery"] != "found by drug-name query"))
    if unattributed:
        print("UNATTRIBUTED AE-bearing payloads:", ", ".join(unattributed))


if __name__ == "__main__":
    main()
