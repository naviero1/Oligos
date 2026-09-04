#!/usr/bin/env python3
"""
Downloads the open-access PDF of every paper cited in data/sources.csv.

Why a script and not a list of links. The register already names each paper and
links it; what a reader actually needs to check the curation is the paper itself,
and the link that resolves to a landing page is not the file. This fetches the
file, verifies it really is a PDF rather than a bot-filter page, and records the
SHA256 and page count of what arrived, so a later download can be shown to be the
same document.

Every paper here is open access. Their licences differ and the difference matters
for what a redistributor may do:

  CC BY 2.0 / CC BY 4.0     reproduce freely, with attribution
  CC BY-NC                  reproduce with attribution, non-commercial only
  CC BY-NC-ND               reproduce VERBATIM with attribution, non-commercial;
                            the ND term forbids derivatives, not copies

So the PDFs may be downloaded and read by anyone, and redistributed unmodified
for non-commercial use. They are deliberately NOT committed to this repository:
the release's own per-source `redistribution` convention marks the ND papers
`summary_stat_only`, and shipping the full publisher PDF alongside rows governed
by that term would contradict it. `papers/` is git-ignored; run this script to
populate it.

Route: europepmc.org/articles/<PMCID>?pdf=render, which serves the publisher PDF
for the PMC open-access subset. Falls back to the PMC article PDF endpoint.

Output: papers/<first_author>_<year>_<PMCID>.pdf
        papers/MANIFEST.md   (citation, licence, link, SHA256, pages, bytes)
Usage:  python3 scripts/fetch_papers.py
"""
import csv
import hashlib
import os
import re
import sys
import unicodedata
import time
import urllib.error
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "papers")

UA = "Mozilla/5.0 (X11; Linux x86_64) OligoTox-Hydrocephalus-provenance/1.0"

# What each licence permits, stated in the manifest so a reader does not have to
# look it up to know whether they may pass the file on.
RIGHTS = {
    "CC BY 2.0": "Reproduce and redistribute freely, with attribution.",
    "CC BY 4.0": "Reproduce and redistribute freely, with attribution.",
    "CC BY-NC": "Reproduce with attribution; non-commercial use only.",
    "CC BY-NC-ND": ("Reproduce VERBATIM with attribution, non-commercial only. "
                    "The ND term forbids derivative works, not unmodified copies."),
    "CC BY-NC-ND 4.0": ("Reproduce VERBATIM with attribution, non-commercial only. "
                        "The ND term forbids derivative works, not unmodified copies."),
}


def slug(text):
    """ASCII-safe filename part. Accents are folded rather than replaced with
    underscores, so Monkkonen does not come out as M_nkk_nen."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_") or "unknown"


def get(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept", "application/pdf,*/*")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 2:
                time.sleep(4 * (attempt + 1))
                continue
            return None, "HTTP %d" % e.code
        except Exception as exc:
            if attempt < 2:
                time.sleep(3)
                continue
            return None, str(exc)
    return None, "exhausted"


def page_count(blob):
    """Page count without a PDF library, for the integrity line in the manifest."""
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz
        except ImportError:
            return len(re.findall(rb"/Type\s*/Page[^s]", blob)) or None
    try:
        with fitz.open(stream=blob, filetype="pdf") as d:
            return d.page_count
    except Exception:
        return None


def main():
    os.makedirs(OUT, exist_ok=True)
    papers = [r for r in csv.DictReader(open(os.path.join(DATA, "sources.csv")))
              if r["pmcid"]]
    papers.sort(key=lambda r: (r["year"], r["first_author"]))
    print("%d cited papers with a PMCID\n" % len(papers))

    manifest, failed = [], []
    for r in papers:
        pmcid = r["pmcid"]
        name = "%s_%s_%s.pdf" % (slug(r["first_author"].split()[0]
                                      if r["first_author"] not in
                                      ("NOT_REPORTED", "NOT_APPLICABLE", "")
                                      else r["journal"]),
                                 r["year"], pmcid)
        path = os.path.join(OUT, name)
        if os.path.exists(path):
            blob = open(path, "rb").read()
            ctype = "cached"
        else:
            blob, ctype = None, ""
            for url in ("https://europepmc.org/articles/%s?pdf=render" % pmcid,
                        "https://pmc.ncbi.nlm.nih.gov/articles/%s/pdf/" % pmcid):
                blob, ctype = get(url)
                # A bot-filter page is HTML with a 200; check the magic bytes,
                # not the status code.
                if blob and blob[:5] == b"%PDF-":
                    break
                blob = None
                time.sleep(1)
            if not blob:
                print("  FAILED  %-14s %s" % (pmcid, ctype))
                failed.append((pmcid, r["citation"], ctype))
                continue
            with open(path, "wb") as fh:
                fh.write(blob)
            time.sleep(1)

        pages = page_count(blob)
        sha = hashlib.sha256(blob).hexdigest()
        manifest.append(dict(r, file=name, sha256=sha, pages=pages,
                             bytes=len(blob)))
        print("  ok      %-14s %-38s %s pages, %.1f MB"
              % (pmcid, name, pages, len(blob) / 1e6))

    lines = ["# Cited papers — downloaded full text", "",
             "Every paper cited in `data/sources.csv`, fetched by "
             "`scripts/fetch_papers.py` on %s." % date.today().isoformat(), "",
             "These files are **not committed**: `papers/` is git-ignored. Two of "
             "the papers here carry an ND licence term and the release marks their "
             "rows `summary_stat_only`, so shipping the publisher PDF in the "
             "repository would contradict the dataset's own redistribution "
             "convention. Run the script to populate this directory.", "",
             "The SHA256 of each file is recorded so a later download can be shown "
             "to be the same document.", ""]
    for m in manifest:
        lines += [
            "## %s" % m["citation"], "",
            "- **File** `%s` — %s pages, %.1f MB" % (m["file"], m["pages"],
                                                          m["bytes"] / 1e6),
            "- **Journal** %s, %s" % (m["journal"], m["year"]),
            "- **Identifiers** DOI %s · PMID %s · %s"
            % (m["doi"] or "—", m["pmid"] or "—", m["pmcid"]),
            "- **Link** %s" % m["url"],
            "- **Licence** %s — %s" % (m["license"],
                                            RIGHTS.get(m["license"],
                                                       "resolve with the publisher")),
            "- **Used here for** %s" % (m["notes"] or "see data/sources.csv"),
            "- **Rows it supports** %s measurement, per `data/sources.csv`"
            % m["n_measurements"],
            "- **SHA256** `%s`" % m["sha256"], ""]
    if failed:
        lines += ["## Not retrieved", ""]
        lines += ["- %s (%s) — %s" % (c, p, why) for p, c, why in failed]
        lines += [""]

    with open(os.path.join(OUT, "MANIFEST.md"), "w") as fh:
        fh.write("\n".join(lines))

    print("\n%d downloaded, %d failed — wrote papers/MANIFEST.md"
          % (len(manifest), len(failed)))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
