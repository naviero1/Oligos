#!/usr/bin/env python3
"""
Resolves every URL in data/sources.csv and records the HTTP status.

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

    results = {u: cache[u] for u in urls if u in cache}
    tally = {}
    for v in results.values():
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
    payload = dict(checked_on=date.today().isoformat(), n_urls=len(results),
                   tally=tally, results=results)
    os.makedirs(NOTES, exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)

    print("\n" + json.dumps(tally, indent=2))
    dead = [u for u, v in results.items() if v["verdict"] in ("dead", "unreachable")]
    if dead:
        print("\nLOCATORS THAT DID NOT RESOLVE (%d):" % len(dead))
        for u in dead:
            print("  %s  %s" % (results[u]["status"], u))
    print("\nwrote %s" % OUT)


if __name__ == "__main__":
    main()
