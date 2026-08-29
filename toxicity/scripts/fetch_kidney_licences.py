#!/usr/bin/env python3
"""Regenerate notes/kidney/source_licences.json from the sources themselves.

Redistribution rights are asserted from the licence statement inside each cited
document, not assumed from the journal or publisher. This walks every PMC id
referenced by data/measurements.csv, reads the Creative Commons licence out of
the article's own full text, and writes the map that
scripts/corrections_kidney.py consumes.

Only plain CC-BY permits reproducing raw values inside a CC-BY dataset; CC-BY-NC
and CC-BY-ND do not, and are recorded as such so the distinction is auditable
rather than a judgement made once and forgotten.

Usage:  python scripts/fetch_kidney_licences.py
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEAS = os.path.join(ROOT, "data", "measurements.csv")
OUT = os.path.join(ROOT, "toxicity", "notes", "kidney", "source_licences.json")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
PMC_RE = re.compile(r"(?<![A-Za-z0-9])PMC(\d{6,8})(?![A-Za-z0-9])", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")


def licence(pmcid):
    """Return the CC licence code, trying the full-text XML then the article page."""
    for url in ("https://www.ebi.ac.uk/europepmc/webservices/rest/%s/fullTextXML" % pmcid,
                "https://pmc.ncbi.nlm.nih.gov/articles/%s/" % pmcid):
        try:
            text = fetch(url)
        except Exception:
            continue
        codes = sorted({a.lower() for a, _ in re.findall(
            r"creativecommons\.org/licenses/([a-z\-]+)/([0-9.]+)", text)})
        if codes:
            return "/".join(codes)
        if re.search(r"creativecommons\.org/publicdomain|\bCC0\b", text):
            return "cc0_or_public_domain"
    return "no_cc_statement"


def main():
    with open(MEAS, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ids = sorted({"PMC" + p for r in rows
                  for p in PMC_RE.findall(r["source_ref"] + " " + (r["notes"] or ""))})
    out = {"_note": ("Creative Commons licence read from each source's own licence "
                     "statement via the Europe PMC full-text XML, falling back to the "
                     "PMC article page. Only plain CC-BY permits reproducing raw "
                     "values in a CC-BY dataset; CC-BY-NC and CC-BY-ND do not, so "
                     "those stay at summary_stat. Regenerate with "
                     "scripts/fetch_kidney_licences.py.")}
    for pmcid in ids:
        out[pmcid] = licence(pmcid)
        print("%-12s %s" % (pmcid, out[pmcid]))
        time.sleep(0.4)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print("\nwrote %s: %d sources" % (OUT, len(ids)))


if __name__ == "__main__":
    sys.exit(main())
