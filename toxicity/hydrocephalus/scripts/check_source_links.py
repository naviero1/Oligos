#!/usr/bin/env python3
"""
Resolves every URL and every DOI in data/sources.csv and records the status.

Why this exists. A provenance register is only as good as its locators. Five
sources in this release carried no citation and no URL at all until the register
was audited, and sixteen more pointed at a bare hostname
(`https://dailymed.nlm.nih.gov/dailymed/`) that names the database but not the
document. Both defects are now blocked by qc/validate.py; this script closes the
remaining gap by checking that the locators actually RESOLVE, so a reader is not
handed a well-formed dead link.

What a status means here:
  200            the locator resolves
  3xx            resolves after a redirect; the final URL is recorded
  403 / 429      the host answered but refused this request (bot filtering or
                 rate limiting). NOT evidence the document is missing, and
                 recorded as `blocked` rather than `dead`.
  404 / other    recorded as `dead` and reported; the citation must be fixed.

DOIs are checked too, and separately, because a URL check does not cover them:
the AQP4 source carried DOI 10.12659/MSM.907186 for two releases while its `url`
column pointed at a perfectly good PMC page, so the URL sweep passed and the
dead DOI went unnoticed. It resolves to nothing; the article's real DOI is
10.12659/MSM.906936. A DOI is resolved through the Crossref works API, which
answers with the registered metadata or a 404, and the returned title is stored
so a DOI pointing at the WRONG paper is visible as well as a DOI pointing at no
paper.

Results are cached in notes/link_check.json and reused, so re-running is cheap
and the check does not hammer the hosts.

Output: notes/link_check.json
Usage:  python3 scripts/check_source_links.py [--recheck]
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")
OUT = os.path.join(NOTES, "link_check.json")

UA = ("Mozilla/5.0 (compatible; OligoTox-Hydrocephalus-provenance-check/1.0; "
      "+https://clinicaltrials.gov)")


def classify(status):
    if status is None:
        return "unreachable"
    if 200 <= status < 300:
        return "ok"
    if 300 <= status < 400:
        return "redirect"
    if status in (401, 403, 405, 429):
        return "blocked"
    return "dead"


def probe(url):
    """Return (status, final_url). Tries HEAD, falls back to a ranged GET for
    hosts that reject HEAD, and backs off once on a 429."""
    for method, attempt in (("HEAD", 0), ("GET", 0), ("GET", 1)):
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", UA)
        if method == "GET":
            req.add_header("Range", "bytes=0-2047")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.url
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(8)
                continue
            if e.code in (403, 405, 501) and method == "HEAD":
                continue
            return e.code, url
        except Exception:
            if method == "HEAD":
                continue
            time.sleep(2)
    return None, url


def resolve_doi(doi):
    """Resolve a DOI through the Crossref works API. Stores the registered title
    so a DOI that resolves to the WRONG paper is visible, not just a dead one."""
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/.")
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept", "application/json")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                msg = json.load(r).get("message", {})
            title = (msg.get("title") or [""])[0]
            return dict(status=200, verdict="ok", title=title[:200],
                        container=(msg.get("container-title") or [""])[0][:120],
                        volume=msg.get("volume", ""), page=msg.get("page", ""),
                        checked=date.today().isoformat())
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 2:
                time.sleep(5)
                continue
            return dict(status=e.code, verdict=("dead" if e.code == 404 else
                                                classify(e.code)), title="",
                        checked=date.today().isoformat())
        except Exception:
            if attempt < 2:
                time.sleep(3)
                continue
    return dict(status=None, verdict="unreachable", title="",
                checked=date.today().isoformat())


def main():
    recheck = "--recheck" in sys.argv
    cache = {}
    if os.path.exists(OUT) and not recheck:
        cache = json.load(open(OUT)).get("results", {})

    urls = []
    for r in csv.DictReader(open(os.path.join(DATA, "sources.csv"))):
        u = (r["url"] or "").strip()
        if u and u not in urls:
            urls.append(u)

    todo = [u for u in urls if u not in cache]
    print("%d distinct URLs in the source register; %d to check"
          % (len(urls), len(todo)))
    for i, u in enumerate(todo, 1):
        status, final = probe(u)
        cache[u] = dict(status=status, verdict=classify(status),
                        final_url=(final if final != u else ""),
                        checked=date.today().isoformat())
        if i % 20 == 0 or cache[u]["verdict"] in ("dead", "unreachable"):
            print("  %4d/%d  %-9s %s" % (i, len(todo), cache[u]["verdict"], u[:96]))
        time.sleep(0.25)

    # ---- DOIs, resolved through Crossref -----------------------------------
    dois = []
    for r in csv.DictReader(open(os.path.join(DATA, "sources.csv"))):
        d = (r["doi"] or "").strip()
        if d and d not in dois:
            dois.append(d)
    doi_cache = {}
    if os.path.exists(OUT) and not recheck:
        doi_cache = json.load(open(OUT)).get("dois", {})
    todo_doi = [d for d in dois if d not in doi_cache]
    print("%d distinct DOIs; %d to resolve" % (len(dois), len(todo_doi)))
    for d in todo_doi:
        doi_cache[d] = resolve_doi(d)
        if doi_cache[d]["verdict"] != "ok":
            print("  %-9s %s" % (doi_cache[d]["verdict"], d))
        time.sleep(0.4)
    doi_results = {d: doi_cache[d] for d in dois if d in doi_cache}

    results = {u: cache[u] for u in urls if u in cache}
    tally = {}
    for v in results.values():
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
    doi_tally = {}
    for v in doi_results.values():
        doi_tally[v["verdict"]] = doi_tally.get(v["verdict"], 0) + 1
    payload = dict(checked_on=date.today().isoformat(), n_urls=len(results),
                   tally=tally, n_dois=len(doi_results), doi_tally=doi_tally,
                   results=results, dois=doi_results)
    os.makedirs(NOTES, exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)

    print("\nURLs: " + json.dumps(tally) + "\nDOIs: " + json.dumps(doi_tally))
    bad_doi = [d for d, v in doi_results.items() if v["verdict"] != "ok"]
    if bad_doi:
        print("\nDOIS THAT DID NOT RESOLVE (%d):" % len(bad_doi))
        for d in bad_doi:
            print("  %s  %s" % (d, doi_results[d].get("status")))
    dead = [u for u, v in results.items() if v["verdict"] in ("dead", "unreachable")]
    if dead:
        print("\nLOCATORS THAT DID NOT RESOLVE (%d):" % len(dead))
        for u in dead:
            print("  %s  %s" % (results[u]["status"], u))
    print("\nwrote %s" % OUT)


if __name__ == "__main__":
    main()
