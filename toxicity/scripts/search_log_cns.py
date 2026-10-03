#!/usr/bin/env python3
"""Run the 20-resource search-coverage sweep and log what each actually returned.

Beebop's 2026-10-02 request requires a log with "one entry for each resource",
recording "actual query terms, search date, relevant result identifiers, no
useful result, access barrier, or a justified lack of endpoint applicability",
and is explicit that blocked services must NOT be marked successfully searched.

So this script queries every resource that exposes a programmatic interface and
records the HTTP outcome verbatim. Resources with no API - the four AI discovery
products, and two toxicology portals that gate downloads behind an interactive
session - are recorded with the barrier observed, never as searched.

THE GAPS BEING SEARCHED FOR. Queries are written against the four open gaps, not
as a generic literature sweep, because the request ranks opportunities "by
qualified human outcomes and characterization gained, not raw cell/row volume":

  G1  sequences and per-position chemistry for the 26 human-laboratory molecules
      that have none
  G2  purity or analytical identity for ANY molecule in the corpus - currently
      0 of 592
  G3  one construct measured in both a human neural system and an animal in-vivo
      CNS study - currently 0
  G4  the tofersen supplementary appendix and protocol

Usage:  python toxicity/scripts/search_log_cns.py --date YYYY-MM-DD
        (the date is passed in, not read from the clock, so a re-run reproduces)
"""
import csv
import json
import os
import subprocess
import sys
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
OUT = os.path.join(TOXDIR, "chronic-neurotoxicity.search-log-2026-10-02.csv")

COLS = ["n", "resource", "url", "interface", "gap", "query_terms", "search_date",
        "http_outcome", "result_count", "result_identifiers", "finding",
        "barrier", "searched"]


def get(url, timeout=45):
    """One HTTP GET, reporting the outcome rather than raising."""
    r = subprocess.run(
        ["curl", "-sS", "-m", str(timeout), "-w", "\n__HTTP__%{http_code}",
         "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120 Safari/537.36", url],
        capture_output=True, text=True)
    body = r.stdout
    code = ""
    if "__HTTP__" in body:
        body, _, code = body.rpartition("__HTTP__")
    if r.returncode != 0:
        return None, "curl exit %d: %s" % (r.returncode, (r.stderr or "").strip()[:90])
    return body, "HTTP %s" % (code.strip() or "?")


def jget(url, retries=2):
    """GET + parse JSON, retrying a rate limit politely before giving up.

    Returns (parsed, outcome, ok). `ok` is False for ANY non-200, so a rate
    limited or erroring service can never be logged as successfully searched.
    The request is explicit that blocked services must not be marked searched,
    and the first run of this script got that wrong: it treated "some JSON
    parsed" as "searched" and logged two HTTP 429s as successful.
    """
    outcome = "not attempted"
    for attempt in range(retries + 1):
        body, outcome = get(url)
        if body is None:
            return None, outcome, False
        if outcome.strip() != "HTTP 200":
            if "429" in outcome and attempt < retries:
                time.sleep(6 * (attempt + 1))
                continue
            return None, outcome, False
        try:
            return json.loads(body), outcome, True
        except Exception:
            return None, outcome + " (non-JSON body, %d bytes)" % len(body), False
    return None, outcome, False


def dig(j, *path, **kw):
    """Walk a JSON shape that may be a dict or a list, without assuming."""
    default = kw.get("default")
    cur = j
    for k in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def main():
    date = "unset"
    if "--date" in sys.argv:
        date = sys.argv[sys.argv.index("--date") + 1]
    rows = []

    def rec(n, resource, url, interface, gap, q, outcome, count, ids, finding,
            barrier, searched):
        rows.append(dict(n=n, resource=resource, url=url, interface=interface,
                         gap=gap, query_terms=q, search_date=date,
                         http_outcome=outcome, result_count=count,
                         result_identifiers=ids, finding=finding,
                         barrier=barrier, searched=searched))
        print("%2d %-26s %-10s %-9s %s" % (n, resource[:26], outcome[:10],
                                           searched, finding[:66]))

    # ---- 1 PubMed (E-utilities) -----------------------------------------
    q = ('("antisense oligonucleotide"[tiab] OR ASO[tiab]) AND '
         '(purity[tiab] OR "mass spectrometry"[tiab] OR HPLC[tiab]) AND '
         '(neuro*[tiab] OR CNS[tiab])')
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&"
         "retmode=json&retmax=20&term=" + urllib.parse.quote(q))
    j, o, ok = jget(u)
    ids = dig(j, "esearchresult", "idlist", default=[])
    cnt = dig(j, "esearchresult", "count", default="")
    rec(1, "PubMed", "https://pubmed.ncbi.nlm.nih.gov/", "E-utilities API", "G2",
        q, o, cnt, ";".join(ids[:12]),
        "%s PMIDs match oligo + analytical-characterization + CNS terms"
        % (cnt or "?") if j else "query did not return JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 2 Europe PMC ----------------------------------------------------
    q = ('(ABSTRACT:"antisense oligonucleotide" OR ABSTRACT:ASO) AND '
         '(ABSTRACT:"iPSC" OR ABSTRACT:"induced pluripotent") AND '
         'ABSTRACT:neuro* AND (ABSTRACT:toxicity OR ABSTRACT:tolerability) AND '
         'OPEN_ACCESS:Y')
    u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&"
         "pageSize=25&query=" + urllib.parse.quote(q))
    j, o, ok = jget(u)
    res = dig(j, "resultList", "result", default=[])
    rec(2, "Europe PMC", "https://europepmc.org/", "REST API", "G1,G3", q, o,
        dig(j, "hitCount", default=""),
        ";".join(r.get("pmcid") or r.get("pmid") or "" for r in res[:12]),
        "%s open-access hits pairing human iPSC neural systems with oligo "
        "toxicity; fullTextXML is retrievable for PMC records"
        % dig(j, "hitCount", default="?") if j else "no JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 3 OpenAlex -------------------------------------------------------
    q = "antisense oligonucleotide neurotoxicity induced pluripotent neuron"
    u = ("https://api.openalex.org/works?per-page=20&filter=is_oa:true&search="
         + urllib.parse.quote(q))
    j, o, ok = jget(u)
    res = dig(j, "results", default=[])
    rec(3, "OpenAlex", "https://openalex.org/", "REST API", "G1,G3", q, o,
        dig(j, "meta", "count", default=""),
        ";".join((w.get("doi") or "").replace("https://doi.org/", "")
                 for w in res[:10]),
        "%s open-access works; used for citation expansion, not as primary "
        "evidence" % dig(j, "meta", "count", default="?") if j else "no JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 4 Semantic Scholar ----------------------------------------------
    q = "oligonucleotide purity characterization mass spectrometry intrathecal"
    u = ("https://api.semanticscholar.org/graph/v1/paper/search?limit=15&"
         "fields=externalIds,title,isOpenAccess&query=" + urllib.parse.quote(q))
    j, o, ok = jget(u)
    res = dig(j, "data", default=[])
    rec(4, "Semantic Scholar", "https://www.semanticscholar.org/",
        "Graph API (unauthenticated)", "G2", q, o, dig(j, "total", default=""),
        ";".join((p.get("externalIds") or {}).get("DOI") or "" for p in res[:10]),
        "%s hits" % dig(j, "total", default="?") if j
        else "unauthenticated Graph API rate-limited or unavailable",
        "" if j else "API key required for reliable access; not a paywall",
        "yes" if ok else "no")
    time.sleep(1)

    # ---- 5-8 the four AI discovery products ------------------------------
    for n, name, url in ((5, "ResearchRabbit", "https://www.researchrabbit.ai/"),
                         (6, "Undermind", "https://www.undermind.ai/"),
                         (7, "Elicit", "https://elicit.com/"),
                         (8, "Consensus", "https://consensus.app/")):
        body, o = get(url, timeout=25)
        rec(n, name, url, "interactive web app, no public search API", "G1,G3",
            "not issued - no programmatic query interface", o, "", "",
            "Landing page reachable; search requires an authenticated "
            "interactive session. No query was issued, so this resource is NOT "
            "recorded as searched. These are discovery aids, not primary "
            "evidence, and a subscription to one does not unlock publisher "
            "content.",
            "account/login required for search; no API. Not a paywall.", "no")
        time.sleep(1)

    # ---- 9 GEO ------------------------------------------------------------
    q = "antisense oligonucleotide AND neuron AND (iPSC OR cortical)"
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&"
         "retmode=json&retmax=20&term=" + urllib.parse.quote(q))
    j, o, ok = jget(u)
    ids = dig(j, "esearchresult", "idlist", default=[])
    cnt = dig(j, "esearchresult", "count", default="")
    rec(9, "GEO", "https://www.ncbi.nlm.nih.gov/geo/", "E-utilities API", "G1,G3",
        q, o, cnt, ";".join(ids[:10]),
        "%s GEO series match. Caveat carried from the compendium: a transcriptome "
        "of treated cells is not the administered construct's sequence."
        % (cnt or "?") if j else "no JSON", "" if j else "see http_outcome",
        "yes" if ok else "no")
    time.sleep(1)

    # ---- 10 SRA -----------------------------------------------------------
    q = "antisense oligonucleotide neurotoxicity"
    u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=sra&"
         "retmode=json&retmax=10&term=" + urllib.parse.quote(q))
    j, o, ok = jget(u)
    cnt = dig(j, "esearchresult", "count", default="")
    rec(10, "SRA", "https://www.ncbi.nlm.nih.gov/sra", "E-utilities API", "G1",
        q, o, cnt,
        ";".join(dig(j, "esearchresult", "idlist", default=[])[:8]),
        "%s runs. Low applicability to this endpoint: sequenced biological "
        "samples are not the administered oligonucleotide, so SRA cannot close "
        "a construct-sequence gap." % (cnt or "?") if j else "no JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 11 PRIDE ----------------------------------------------------------
    u = ("https://www.ebi.ac.uk/pride/ws/archive/v2/search/projects?"
         "keyword=antisense%20oligonucleotide&pageSize=20&page=0")
    j, o, ok = jget(u)
    pride = dig(j, "_embedded", "compactprojects", default=None)
    if not isinstance(pride, list):
        pride = j if isinstance(j, list) else []
    n_hits = len(pride)
    rec(11, "PRIDE", "https://www.ebi.ac.uk/pride/", "REST API v2", "G1", 
        "keyword=antisense oligonucleotide", o, n_hits,
        ";".join(p.get("accession", "") for p in pride[:8] if isinstance(p, dict)),
        "Proteomics deposits; relevant only for protein-level neuro markers, "
        "not for construct sequence or purity.",
        "" if j else "endpoint returned non-JSON or was unavailable",
        "yes" if ok else "no")
    time.sleep(1)

    # ---- 12 ProteomeXchange ------------------------------------------------
    u = ("https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets?"
         "keywords=antisense%20oligonucleotide&pageSize=20")
    j, o, ok = jget(u)
    rec(12, "ProteomeXchange",
        "https://www.proteomexchange.org/", "PROXI API", "G1",
        "keywords=antisense oligonucleotide", o,
        len(j) if isinstance(j, list) else "",
        ";".join(d.get("identifier", "") for d in (j if isinstance(j, list) else [])[:8])
        if isinstance(j, list) else "",
        "Aggregates PRIDE and others - deduplicate against resource 11 before "
        "counting any deposit twice.",
        "" if isinstance(j, list) else "non-JSON or unavailable",
        "yes" if (ok and isinstance(j, list)) else "no")
    time.sleep(1)

    # ---- 13 BioStudies ------------------------------------------------------
    u = ("https://www.ebi.ac.uk/biostudies/api/v1/search?query="
         + urllib.parse.quote("antisense oligonucleotide neurotoxicity") + "&pageSize=20")
    j, o, ok = jget(u)
    rec(13, "BioStudies", "https://www.ebi.ac.uk/biostudies/", "REST API", "G1,G3",
        "antisense oligonucleotide neurotoxicity", o,
        dig(j, "totalHits", default=""),
        ";".join(h.get("accession", "") for h in dig(j, "hits", default=[])[:8]),
        "%s hits" % dig(j, "totalHits", default="?") if j else "no JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 14 ArrayExpress (within BioStudies) --------------------------------
    u = ("https://www.ebi.ac.uk/biostudies/api/v1/arrayexpress/search?query="
         + urllib.parse.quote("antisense oligonucleotide neuron") + "&pageSize=20")
    j, o, ok = jget(u)
    rec(14, "ArrayExpress (BioStudies)",
        "https://www.ebi.ac.uk/biostudies/arrayexpress", "REST API", "G1,G3",
        "antisense oligonucleotide neuron", o, dig(j, "totalHits", default=""),
        ";".join(h.get("accession", "") for h in dig(j, "hits", default=[])[:8]),
        "Collection within resource 13; deduplicate against it.",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 15 ClinicalTrials.gov ---------------------------------------------
    u = ("https://clinicaltrials.gov/api/v2/studies?format=json&pageSize=30&"
         "query.cond=" + urllib.parse.quote("hydrocephalus OR neurotoxicity") +
         "&query.intr=" + urllib.parse.quote("antisense oligonucleotide"))
    j, o, ok = jget(u)
    st = dig(j, "studies", default=[])
    def nct(s):
        return (s.get("protocolSection", {}).get("identificationModule", {})
                 .get("nctId", ""))
    rec(15, "ClinicalTrials.gov", "https://clinicaltrials.gov/", "API v2",
        "G3,G4", "cond=hydrocephalus OR neurotoxicity; intr=antisense "
        "oligonucleotide", o, dig(j, "totalCount", default=len(st)),
        ";".join(nct(s) for s in st[:14]),
        "Registration alone does not establish an observed toxicity outcome - "
        "only the posted results module does.",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 16 Comparative Toxicogenomics Database ----------------------------
    body, o = get("https://ctdbase.org/", timeout=25)
    rec(16, "Comparative Toxicogenomics DB", "https://ctdbase.org/",
        "batch-query web form; no documented open REST search", "G3",
        "not issued - no programmatic query interface verified", o, "", "",
        "CTD curates chemical-gene-disease relationships that are contextual or "
        "inferred. Those cannot replace observed, sequence-linked experimental "
        "outcomes, which is what this endpoint needs, so applicability is low "
        "independently of access.",
        "no verified open search API; batch query is interactive", "no")
    time.sleep(1)

    # ---- 17 ICE -------------------------------------------------------------
    body, o = get("https://ice.ntp.niehs.nih.gov/", timeout=25)
    rec(17, "ICE", "https://ice.ntp.niehs.nih.gov/",
        "interactive portal; bulk download requires a session", "G2",
        "not issued - no programmatic query interface", o, "", "",
        "ICE aggregates curated in-vitro assay data dominated by small "
        "molecules. No oligonucleotide-specific characterization expected; "
        "recorded as reachable but not searched.",
        "interactive session required for data download", "no")
    time.sleep(1)

    # ---- 18 ToxCast ----------------------------------------------------------
    body, o = get("https://www.epa.gov/comptox-tools/exploring-toxcast-data",
                  timeout=25)
    rec(18, "ToxCast", "https://www.epa.gov/comptox-tools/exploring-toxcast-data",
        "documentation page; data via CompTox dashboard/downloads", "G2",
        "not issued - no programmatic query interface from this page", o, "", "",
        "Broad chemical-assay screening is not a therapeutic-oligonucleotide "
        "toxicity dataset; ToxCast's chemical library does not carry "
        "therapeutic ASOs. Justified low applicability.",
        "data behind dashboard/bulk download, not a search API", "no")
    time.sleep(1)

    # ---- 19 Zenodo -----------------------------------------------------------
    u = ("https://zenodo.org/api/records?size=20&q="
         + urllib.parse.quote('"antisense oligonucleotide" AND (neurotoxicity OR neuron)'))
    j, o, ok = jget(u)
    hits = dig(j, "hits", "hits", default=[])
    rec(19, "Zenodo", "https://zenodo.org/", "REST API", "G1,G3",
        '"antisense oligonucleotide" AND (neurotoxicity OR neuron)', o,
        dig(j, "hits", "total", default=""),
        ";".join(str(h.get("doi", "")) for h in hits[:8]),
        "%s records" % dig(j, "hits", "total", default="?") if j else "no JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")
    time.sleep(1)

    # ---- 20 Dryad ------------------------------------------------------------
    u = ("https://datadryad.org/api/v2/search?per_page=20&q="
         + urllib.parse.quote("antisense oligonucleotide neuron"))
    j, o, ok = jget(u)
    emb = dig(j, "_embedded", "stash:datasets", default=[])
    rec(20, "Dryad", "https://datadryad.org/", "REST API v2", "G1,G3",
        "antisense oligonucleotide neuron", o, dig(j, "total", default=len(emb)),
        ";".join(d.get("identifier", "") for d in emb[:8]),
        "%s datasets" % dig(j, "total", default="?") if j else "no JSON",
        "" if j else "see http_outcome", "yes" if ok else "no")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    searched = sum(1 for r in rows if r["searched"] == "yes")
    print("\n%d resources logged; %d actually searched, %d recorded as NOT "
          "searched with the barrier named" % (len(rows), searched, len(rows) - searched))
    print("wrote %s" % os.path.relpath(OUT, os.path.dirname(TOXDIR)))


if __name__ == "__main__":
    main()
