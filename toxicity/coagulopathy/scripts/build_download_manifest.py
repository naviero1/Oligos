#!/usr/bin/env python3
"""Build the download manifest and fetch script for the original source documents.

    python3 toxicity/coagulopathy/scripts/build_download_manifest.py

    -> sources/DOWNLOAD_MANIFEST.csv     one row per source: where the original lives
    -> scripts/fetch_original_papers.sh  one command to download the fetchable ones

Why this exists rather than a folder of PDFs: what the release holds in
sources/documents/ is the machine-readable text or XML each row was extracted from, not
the publisher's formatted PDF. And 24 of the 100 sources are publisher-restricted, so
their full texts are cited, not redistributed. The manifest points at the original in
every case; the script fetches the ones that can be fetched without a subscription.
"""
import csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_sources_pdf import parse_ids, classify, RX  # one identifier parser, not two

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CSV = os.path.join(ROOT, "sources", "DOWNLOAD_MANIFEST.csv")
OUT_SH = os.path.join(ROOT, "scripts", "fetch_original_papers.sh")

FREE = {"public_domain", "CC_BY", "CC_BY_NC", "CC_BY_NC_ND"}


def rows():
    S = list(csv.DictReader(open(os.path.join(ROOT, "data", "sources.csv"), newline="", encoding="utf-8")))
    out = []
    for r in S:
        ids = parse_ids(r["identifier"] + " " + r["citation"])
        db = classify(r, ids)
        landing = direct = ""
        note = ""
        if ids.get("patent"):
            direct = f"https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/{ids['patent']}"
            landing = f"https://patents.google.com/patent/US{ids['patent']}"
            note = "US patent - public domain, direct PDF."
        elif ids.get("setid") and db == "DailyMed":
            direct = f"https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid={ids['setid']}&type=pdf"
            landing = f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={ids['setid']}"
            note = "US prescribing information - public domain, direct PDF."
        elif ids.get("pmcid"):
            landing = f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{ids['pmcid']}/"
            if r["redistribution"] in FREE:
                # Europe PMC serves fullTextXML for the OPEN-ACCESS subset only. Offering it
                # for a restricted record produces a confident 404, so it is offered only
                # where the licence says the record is open.
                direct = f"https://www.ebi.ac.uk/europepmc/webservices/rest/PMC{ids['pmcid']}/fullTextXML"
                note = "Open access - full text retrievable as XML; the publisher PDF is on the landing page."
            else:
                note = ("Publisher-restricted or licence unresolved - NOT programmatically fetchable. "
                        "Open the landing page with your institutional access.")
        elif ids.get("nda") or db == "Drugs@FDA":
            n = ids.get("nda", "")
            landing = (f"https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo={n}"
                       if n else "https://www.accessdata.fda.gov/scripts/cder/daf/")
            note = ("FDA review package - public domain. Open the application, then the "
                    "'Approval History, Letters, Reviews' tab and take the named review.")
        elif db == "EMA":
            landing = "https://www.ema.europa.eu/en/medicines"
            note = ("EMA assessment report - search the product name, then 'Assessment report'. "
                    "Free to download; reuse permitted with acknowledgement.")
        elif ids.get("pmid"):
            landing = f"https://pubmed.ncbi.nlm.nih.gov/{ids['pmid']}/"
            note = "Abstract only in this release; use the landing page for the full text."
        elif ids.get("nct"):
            landing = f"https://clinicaltrials.gov/study/{ids['nct']}"
            direct = f"https://clinicaltrials.gov/api/v2/studies/{ids['nct']}"
            note = "Registry record incl. posted results - public domain."
        elif db == "openFDA":
            landing = "https://open.fda.gov/apis/drug/event/"
            note = "Query output, not a paper. Reproduce with the query recorded in the row's notes."
        if ids.get("doi") and not landing:
            landing = f"https://doi.org/{ids['doi']}"
        out.append({
            "source_id": r["source_id"],
            "citation": r["citation"],
            "database": db,
            "landing_url": landing,
            "direct_download_url": direct,
            "doi": ids.get("doi", ""),
            "pmcid": ("PMC" + ids["pmcid"]) if ids.get("pmcid") else "",
            "pmid": ids.get("pmid", ""),
            "licence": r["licence"],
            "redistribution": r["redistribution"],
            "we_may_redistribute": "yes" if r["redistribution"] in FREE else "no",
            "local_extracted_copy": f"sources/documents/{r['document_file']}",
            "n_measurements": r["n_measurements"],
            "access_note": note,
        })
    return out


def main():
    R = rows()
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(R[0].keys()))
        w.writeheader(); w.writerows(R)

    fetch = [r for r in R if r["direct_download_url"]]
    L = ["#!/usr/bin/env bash",
         "# Download the original source documents that can be fetched without a subscription.",
         "#",
         "#   bash toxicity/coagulopathy/scripts/fetch_original_papers.sh [OUTDIR]",
         "#",
         "# Default OUTDIR is toxicity/coagulopathy/originals/ (git-ignored).",
         "# Sources with no direct URL -- FDA review packages, EMA assessment reports, and every",
         "# publisher-restricted paper -- are NOT fetched here: open the landing_url in",
         "# sources/DOWNLOAD_MANIFEST.csv, which for restricted papers is where your",
         "# institutional access applies.",
         "set -uo pipefail",
         'OUT="${1:-$(dirname "$0")/../originals}"',
         'mkdir -p "$OUT"',
         'ok=0; fail=0',
         'get() {  # get <name> <url>',
         '  if [ -s "$OUT/$1" ]; then echo "  have  $1"; return; fi',
         '  if curl -fsSL --max-time 180 -A "OligoTox-Coagulopathy/1.0" -o "$OUT/$1" "$2"; then',
         '    echo "  got   $1"; ok=$((ok+1))',
         '  else',
         '    echo "  FAIL  $1  <- $2"; rm -f "$OUT/$1"; fail=$((fail+1))',
         '  fi',
         '}',
         f'echo "Fetching {len(fetch)} original documents into $OUT"']
    for r in fetch:
        ext = ".pdf" if "downloadPdf" in r["direct_download_url"] or "type=pdf" in r["direct_download_url"] \
              else (".json" if "clinicaltrials" in r["direct_download_url"] else ".xml")
        name = f'{r["source_id"]}_{re.sub(r"[^A-Za-z0-9]+", "-", r["citation"])[:60].strip("-")}{ext}'
        L.append(f'get "{name}" "{r["direct_download_url"]}"')
    L += ['echo', 'echo "downloaded $ok, failed $fail"',
          'echo "Everything else: see sources/DOWNLOAD_MANIFEST.csv (landing_url)."']
    with open(OUT_SH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    os.chmod(OUT_SH, 0o755)

    from collections import Counter
    print(f"  wrote sources/DOWNLOAD_MANIFEST.csv        {len(R)} sources")
    print(f"  wrote scripts/fetch_original_papers.sh     {len(fetch)} directly fetchable")
    print(f"    redistributable by us: {sum(1 for r in R if r['we_may_redistribute']=='yes')}"
          f" / restricted: {sum(1 for r in R if r['we_may_redistribute']=='no')}")
    print("    by database:", dict(Counter(r["database"] for r in R)))


if __name__ == "__main__":
    main()
