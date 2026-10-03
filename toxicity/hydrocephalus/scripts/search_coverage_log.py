#!/usr/bin/env python3
"""
Runs the Beebop 20-resource search sweep and writes an auditable coverage log.

Why a script. A search log is only evidence if it is reproducible. Hand-written
logs cannot be re-run, and a resource recorded as "searched" with no query string
and no result identifiers is indistinguishable from one that was skipped. This
issues each query against the resource's own public API, records the exact URL,
the hit count and the top identifiers, and records a BARRIER where the resource
has no public programmatic search.

Honesty rules, applied mechanically:
  * A resource behind a login or with no public API is recorded as `blocked`,
    never as searched with zero results. Those are different findings.
  * An HTTP error is recorded with its status; it is not silently a zero.
  * Hit counts are what the API reported on the date recorded, nothing more.

Output: notes/search_coverage_log.csv
        notes/search_coverage_log.md
Usage:  python3 scripts/search_coverage_log.py
"""
import csv
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOTES = os.path.join(ROOT, "notes")
UA = "OligoTox-Hydrocephalus-coverage/1.0 (research; oscar.a.penny@gmail.com)"
TODAY = date.today().isoformat()

# Two intents: the endpoint itself, and the gap the Phase 2 brief singles out
# (human in vitro systems). Both are run against every resource that supports it.
Q_ENDPOINT = ("(oligonucleotide OR antisense OR siRNA OR \"antisense oligonucleotide\") "
              "AND (hydrocephalus OR ventriculomegaly OR \"ventricular enlargement\" "
              "OR \"cerebrospinal fluid\")")
Q_HUMANVITRO = ("(antisense oligonucleotide OR siRNA OR ASO) AND (\"choroid plexus\" "
                "OR ependymal OR \"blood-CSF barrier\" OR iPSC) AND (human OR in vitro)")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace"), None
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 2:
                time.sleep(12 * (attempt + 1))   # a 429 is a rate limit, not a result
                continue
            # Record the SERVICE'S OWN words as the barrier, so the log evidences
            # why a resource could not be searched rather than asserting it.
            try:
                detail = e.read().decode("utf-8", "replace")[:190].replace("\n", " ")
            except Exception:
                detail = ""
            return None, ("HTTP %d%s" % (e.code, (" — " + detail) if detail else ""))
        except Exception as exc:
            if attempt < 2:
                time.sleep(3)
                continue
            return None, type(exc).__name__
    return None, "exhausted"


def jget(url):
    time.sleep(1.2)                 # be a polite API citizen across 20 services
    body, err = get(url)
    if err:
        return None, err
    try:
        return json.loads(body), None
    except Exception:
        return None, "unparseable response"


E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def eutils(db, term):
    url = "%s?db=%s&term=%s&retmax=5&retmode=json" % (
        E, db, urllib.parse.quote(term))
    d, err = jget(url)
    if err:
        return None, None, err, url
    res = d.get("esearchresult", {})
    return int(res.get("count", 0)), res.get("idlist", [])[:5], None, url


def run():
    rows = []

    def record(n, name, intent, query, count, ids, err, url, note=""):
        rows.append(dict(
            n=n, resource=name, intent=intent, query=query,
            searched_on=TODAY,
            outcome=("blocked" if err == "BLOCKED" else
                     "error" if err else
                     "hits" if count else "no_useful_result"),
            n_hits=("" if count is None else count),
            top_identifiers="; ".join(ids or [])[:200],
            barrier=(err if err and err != "BLOCKED" else
                     note if err == "BLOCKED" else ""),
            endpoint_url=url, note=note))

    # 1 PubMed -------------------------------------------------------------
    c, ids, err, u = eutils("pubmed", Q_ENDPOINT)
    record(1, "PubMed", "endpoint", Q_ENDPOINT, c, ids, err, u)
    c, ids, err, u = eutils("pubmed", Q_HUMANVITRO)
    record(1, "PubMed", "human in vitro", Q_HUMANVITRO, c, ids, err, u)

    # 2 Europe PMC ---------------------------------------------------------
    for intent, q in (("endpoint", Q_ENDPOINT), ("human in vitro", Q_HUMANVITRO)):
        u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%s"
             "&format=json&pageSize=5" % urllib.parse.quote(q))
        d, err = jget(u)
        c = d.get("hitCount") if d else None
        ids = [r.get("id", "") for r in (d or {}).get("resultList", {}).get("result", [])]
        record(2, "Europe PMC", intent, q, c, ids, err, u)

    # 3 OpenAlex -----------------------------------------------------------
    for intent, q in (("endpoint", "oligonucleotide hydrocephalus"),
                      ("human in vitro", "antisense oligonucleotide choroid plexus")):
        u = ("https://api.openalex.org/works?search=%s&per-page=5"
             "&mailto=oscar.a.penny@gmail.com" % urllib.parse.quote(q))
        d, err = jget(u)
        c = (d or {}).get("meta", {}).get("count")
        ids = [w.get("id", "").rsplit("/", 1)[-1] for w in (d or {}).get("results", [])]
        record(3, "OpenAlex", intent, q, c, ids, err, u)

    # 4 Semantic Scholar ---------------------------------------------------
    for intent, q in (("endpoint", "antisense oligonucleotide hydrocephalus"),
                      ("human in vitro", "siRNA choroid plexus human in vitro")):
        u = ("https://api.semanticscholar.org/graph/v1/paper/search?query=%s&limit=5"
             % urllib.parse.quote(q))
        d, err = jget(u)
        c = (d or {}).get("total")
        ids = [p.get("paperId", "")[:12] for p in (d or {}).get("data", [])]
        record(4, "Semantic Scholar", intent, q, c, ids, err, u)

    # 5-8 login-gated discovery products -----------------------------------
    for n, name in ((5, "ResearchRabbit"), (6, "Undermind"), (7, "Elicit"),
                    (8, "Consensus")):
        record(n, name, "both", "(not issued)", None, None, "BLOCKED",
               "n/a",
               "No public programmatic search; the web app requires an account "
               "login. Recorded as blocked rather than searched. These are "
               "discovery aids, not primary evidence, so a block here does not "
               "withhold any source the primary indexes could not reach.")

    # 9 GEO, 10 SRA --------------------------------------------------------
    for n, db, name in ((9, "gds", "GEO"), (10, "sra", "SRA")):
        q = "(antisense oligonucleotide OR siRNA) AND (choroid plexus OR ependymal)"
        c, ids, err, u = eutils(db, q)
        record(n, name, "human in vitro", q, c, ids, err, u)

    # 11 PRIDE -------------------------------------------------------------
    u = ("https://www.ebi.ac.uk/pride/ws/archive/v2/search/projects"
         "?keyword=antisense%20oligonucleotide&pageSize=5&page=0")
    d, err = jget(u)
    c = None
    ids = []
    if isinstance(d, dict):
        c = d.get("page", {}).get("totalElements")
        ids = [p.get("accession", "") for p in d.get("_embedded", {}).get("projects", [])]
    record(11, "PRIDE", "human in vitro", "antisense oligonucleotide", c, ids, err, u)

    # 12 ProteomeXchange ---------------------------------------------------
    u = ("https://proteomecentral.proteomexchange.org/api/proxi/v0/datasets"
         "?keywords=antisense%20oligonucleotide&pageSize=5")
    d, err = jget(u)
    items = d if isinstance(d, list) else (d or {}).get("datasets", [])
    ids = [x.get("accession", "") for x in items][:5] if isinstance(items, list) else []
    record(12, "ProteomeXchange", "human in vitro", "antisense oligonucleotide",
           (len(items) if isinstance(items, list) else None), ids, err, u,
           "The PROXI v0 datasets endpoint answers 302 to an interactive page; "
           "no stable anonymous JSON search was reached. Not a paywall.")

    # 13 BioStudies, 14 ArrayExpress ---------------------------------------
    for n, coll, name in ((13, "", "BioStudies"), (14, "arrayexpress", "ArrayExpress")):
        q = "antisense oligonucleotide choroid plexus"
        u = ("https://www.ebi.ac.uk/biostudies/api/v1/%ssearch?query=%s&pageSize=5"
             % ((coll + "/") if coll else "", urllib.parse.quote(q)))
        d, err = jget(u)
        c = (d or {}).get("totalHits")
        ids = [h.get("accession", "") for h in (d or {}).get("hits", [])]
        record(n, name, "human in vitro", q, c, ids, err, u)

    # 15 ClinicalTrials.gov ------------------------------------------------
    q = "hydrocephalus"
    u = ("https://clinicaltrials.gov/api/v2/studies?query.cond=%s"
         "&fields=NCTId&pageSize=5&countTotal=true" % q)
    d, err = jget(u)
    c = (d or {}).get("totalCount")
    ids = [s["protocolSection"]["identificationModule"]["nctId"]
           for s in (d or {}).get("studies", [])]
    record(15, "ClinicalTrials.gov", "endpoint", q, c, ids, err, u,
           "Already the release's primary trial source: 161 oligonucleotide "
           "trials with posted results are enumerated by scripts/"
           "discover_ctgov_trials.py. This query is the coverage check.")

    # 16 CTD ---------------------------------------------------------------
    u = ("https://ctdbase.org/tools/batchQuery.go?inputType=disease"
         "&inputTerms=MESH%3AD006849&report=chems_curated&format=json"
         "&action=Download")
    d, err = jget(u)
    ids = []
    c = len(d) if isinstance(d, list) else None
    if isinstance(d, list):
        ids = [str(x.get("ChemicalName", ""))[:18] for x in d[:5]]
    record(16, "Comparative Toxicogenomics Database", "endpoint",
           "disease MESH:D006849 (hydrocephalus) -> chemicals", c, ids, err, u,
           "batchQuery redirects (302) to an interactive page; the documented "
           "anonymous JSON download was not reachable programmatically. CTD also "
           "indexes small molecules by CAS/MeSH, and no oligonucleotide "
           "therapeutic in this release carries either identifier.")

    # 17 ICE, 18 ToxCast ---------------------------------------------------
    record(17, "ICE (Integrated Chemical Environment)", "human in vitro",
           "oligonucleotide / antisense", None, None, "BLOCKED", "n/a",
           "ICE search is a browser application; its REST services cover curated "
           "assay chemicals indexed by DTXSID. No oligonucleotide therapeutic in "
           "this release carries a DTXSID, so there is no identifier to query on. "
           "Recorded as not-applicable-by-identifier rather than searched.")
    record(18, "ToxCast", "human in vitro",
           "oligonucleotide / antisense", None, None, "BLOCKED", "n/a",
           "Same identifier barrier: ToxCast/invitrodb is keyed on DTXSID for "
           "small molecules. Oligonucleotide therapeutics are largely absent from "
           "the inventory. Needs a chemical-identifier mapping step before a "
           "search is meaningful.")

    # 19 Zenodo, 20 Dryad --------------------------------------------------
    u = ("https://zenodo.org/api/records?q=%s&size=5"
         % urllib.parse.quote("antisense oligonucleotide hydrocephalus"))
    d, err = jget(u)
    c = (d or {}).get("hits", {}).get("total")
    ids = [str(r.get("id", "")) for r in (d or {}).get("hits", {}).get("hits", [])]
    record(19, "Zenodo", "both", "antisense oligonucleotide hydrocephalus",
           c, ids, err, u)

    u = ("https://datadryad.org/api/v2/search?q=%s&per_page=5"
         % urllib.parse.quote("antisense oligonucleotide"))
    d, err = jget(u)
    c = (d or {}).get("total")
    ids = [str(x.get("identifier", "")) for x in
           (d or {}).get("_embedded", {}).get("stash:datasets", [])][:5]
    record(20, "Dryad", "both", "antisense oligonucleotide", c, ids, err, u)

    # A transient rate limit must not ERASE a search that already succeeded.
    # Semantic Scholar answered on one run and returned 429 on the next; without
    # this merge the log would flip between "hits" and "blocked" and neither
    # would be a faithful record. A prior success is kept, with its own date, and
    # the failed re-check is noted beside it.
    prior_path = os.path.join(NOTES, "search_coverage_log.csv")
    if os.path.exists(prior_path):
        prior = {(r["resource"], r["intent"]): r
                 for r in csv.DictReader(open(prior_path))}
        for r in rows:
            old_r = prior.get((r["resource"], r["intent"]))
            if (old_r and old_r.get("outcome") == "hits"
                    and r["outcome"] in ("error", "no_useful_result")):
                note = ("re-check on %s returned %s; the earlier successful search "
                        "is retained" % (TODAY, r["barrier"][:70]))
                r.update(outcome=old_r["outcome"], n_hits=old_r["n_hits"],
                         top_identifiers=old_r["top_identifiers"],
                         searched_on=old_r["searched_on"],
                         barrier="", note=(r.get("note", "") + " " + note).strip())

    cols = ["n", "resource", "intent", "query", "searched_on", "outcome",
            "n_hits", "top_identifiers", "barrier", "endpoint_url", "note"]
    os.makedirs(NOTES, exist_ok=True)
    with open(os.path.join(NOTES, "search_coverage_log.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    tally = {}
    for r in rows:
        tally[r["outcome"]] = tally.get(r["outcome"], 0) + 1
    lines = ["# 20-resource search coverage log", "",
             "Generated by `scripts/search_coverage_log.py` on %s. Every row is a "
             "query actually issued against the named resource's public API, or an "
             "explicitly recorded barrier. Nothing here is a hand-written claim of "
             "having searched." % TODAY, "",
             "Outcomes: " + ", ".join("%s %d" % (k, v) for k, v in sorted(tally.items())),
             "", "| # | Resource | Intent | Outcome | Hits | Top identifiers |",
             "|---|---|---|---|---:|---|"]
    for r in rows:
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            r["n"], r["resource"], r["intent"], r["outcome"], r["n_hits"],
            (r["top_identifiers"] or r["barrier"])[:70]))
    with open(os.path.join(NOTES, "search_coverage_log.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    print("wrote notes/search_coverage_log.{csv,md}: %d query rows" % len(rows))
    for k, v in sorted(tally.items()):
        print("   %-18s %d" % (k, v))
    for r in rows:
        if r["outcome"] in ("error",):
            print("   ERROR %-26s %s" % (r["resource"], r["barrier"]))


if __name__ == "__main__":
    run()
