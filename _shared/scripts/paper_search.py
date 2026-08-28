#!/usr/bin/env python3
"""Native paper search + open-access full-text retrieval — no MCP server required.

This environment's egress allowlist reaches the major scholarly APIs directly
(OpenAlex, Europe PMC, Crossref, NCBI PubMed/PMC, Semantic Scholar, bioRxiv),
which is what paper-search-MCP servers wrap. This helper hits them directly, so
paper discovery and OA full-text work in-session without any MCP setup.

Reachable (verified): OpenAlex, Crossref, Europe PMC, NCBI E-utilities (PubMed +
PMC full text), Semantic Scholar (rate-limited without a key), Google Patents,
WHO INN. Blocked: arXiv API host, DrugBank.

Usage:
  python scripts/paper_search.py "oligonucleotide nephrotoxicity proximal tubule"
  python scripts/paper_search.py --pmc PMC6796739          # dump OA full text
  python scripts/paper_search.py --pubmed "ASO kidney injury biomarker"

Intended uses for this dataset: verify the WS-tagged rows against their primary
PMC sources, and discover additional kidney-toxicity records. NOT a fabrication
shortcut — sequences/values are still only filled from an explicit, cited source.
"""
import sys, json, ssl, urllib.request, urllib.parse

CA = "/root/.ccr/ca-bundle.crt"
try:
    CTX = ssl.create_default_context(cafile=CA)
except Exception:
    CTX = ssl.create_default_context()

def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "OligoTox-Kidney/1.0 (research)"})
    return urllib.request.urlopen(req, context=CTX, timeout=30).read().decode("utf-8", "replace")

def search_europepmc(query, n=8):
    q = urllib.parse.quote(query)
    url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}"
           f"&format=json&pageSize={n}&resultType=core")
    out = []
    for r in json.loads(_get(url)).get("resultList", {}).get("result", []):
        out.append({"id": r.get("id"), "pmid": r.get("pmid"), "pmcid": r.get("pmcid"),
                    "year": r.get("pubYear"), "oa": r.get("isOpenAccess"),
                    "title": (r.get("title") or "").strip(), "journal": r.get("journalTitle")})
    return out

def search_openalex(query, n=8):
    q = urllib.parse.quote(query)
    url = f"https://api.openalex.org/works?search={q}&per-page={n}"
    out = []
    for w in json.loads(_get(url)).get("results", []):
        out.append({"doi": w.get("doi"), "year": w.get("publication_year"),
                    "title": w.get("title"),
                    "oa": (w.get("open_access") or {}).get("is_oa")})
    return out

def search_pubmed(query, n=8):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    ids = json.loads(_get(f"{base}/esearch.fcgi?db=pubmed&retmode=json&retmax={n}"
                          f"&sort=relevance&term={urllib.parse.quote(query)}")
                     )["esearchresult"]["idlist"]
    if not ids:
        return []
    summ = json.loads(_get(f"{base}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids)}"))["result"]
    return [{"pmid": u, "year": summ[u].get("pubdate", "")[:4],
             "title": summ[u].get("title"), "journal": summ[u].get("source")}
            for u in summ["uids"]]

def fetch_pmc_fulltext(pmcid):
    """Return OA full-text XML for a PMC id (accepts 'PMC6796739' or '6796739')."""
    num = pmcid.upper().replace("PMC", "")
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    return _get(f"{base}/efetch.fcgi?db=pmc&id={num}")

def _print(rows):
    for r in rows:
        ids = " ".join(f"{k}={v}" for k, v in r.items() if k in ("pmid", "pmcid", "doi") and v)
        print(f"  [{r.get('year','----')}] {(r.get('title') or '')[:88]}")
        if ids:
            print(f"        {ids}  oa={r.get('oa')}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(0)
    if a[0] == "--pmc":
        xml = fetch_pmc_fulltext(a[1])
        print(f"{a[1]}: {len(xml)} chars of full-text XML")
    elif a[0] == "--pubmed":
        _print(search_pubmed(" ".join(a[1:])))
    else:
        q = " ".join(a)
        print("== Europe PMC =="); _print(search_europepmc(q))
        print("== OpenAlex ==");   _print(search_openalex(q))
