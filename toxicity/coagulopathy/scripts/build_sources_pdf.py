#!/usr/bin/env python3
"""Build the source & provenance document: every source, every database, every link.

    python3 toxicity/coagulopathy/scripts/build_sources_pdf.py [--no-check]

    -> OligoTox-Coagulopathy_Sources.pdf

Identifiers are parsed out of data/sources.csv, resolved to canonical URLs at the
repository that actually holds each document, and then HTTP-checked, so the document
reports which links were confirmed to resolve rather than asserting that they do.
Pass --no-check to skip the network step (every link is then reported "not checked").
"""
import csv, os, re, sys, datetime, urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_documents import html_doc, render, ROOT  # same renderer as the other PDFs

DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "OligoTox-Coagulopathy_Sources.pdf")
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- identifier parsing
RX = {
    "pmcid": re.compile(r"\bPMC(\d{6,8})\b"),
    "pmid": re.compile(r"\bPMID:?\s*(\d{7,8})\b"),
    # Elsevier DOIs embed parentheses -- 10.1016/s0006-2952(97)00091-9 -- so ")" cannot be
    # a terminator. Take everything up to whitespace or a field separator, then trim only
    # trailing punctuation that is not part of the identifier.
    "doi": re.compile(r"\b(10\.\d{4,9}/[^\s|;\]]+)"),
    "patent": re.compile(r"\bUS\s*([\d][\d,]{5,})\s*([AB]\d?)?"),
    "setid": re.compile(r"set\s*[Ii][dD]\s*[:=]?\s*([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"),
    "nct": re.compile(r"\b(NCT\d{8})\b"),
    "ema": re.compile(r"\b(EMA/[A-Za-z0-9/]*\d{4,6}/\d{4}|EMEA/H/C/\d{6})\b"),
    "nda": re.compile(r"\bNDA\s*(\d{6})\b"),
}

DBS = {
    "PMC":        ("PubMed Central / Europe PMC", "https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML"),
    "PubMed":     ("NCBI PubMed (abstracts)", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract"),
    "USPTO":      ("USPTO granted patents (full text)", "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<NUMBER>"),
    "DailyMed":   ("NLM DailyMed (US prescribing information, SPL)", "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/<SETID>.xml"),
    "Drugs@FDA":  ("FDA Drugs@FDA review packages", "https://www.accessdata.fda.gov/drugsatfda_docs/nda/<YEAR>/<NDA>Orig1s000<REVIEW>.pdf"),
    "EMA":        ("European Medicines Agency EPARs", "https://www.ema.europa.eu/en/medicines/human/EPAR/<product>"),
    "ClinicalTrials.gov": ("ClinicalTrials.gov registry & results", "https://clinicaltrials.gov/api/v2/studies/<NCTID>"),
    "openFDA":    ("openFDA (FAERS adverse events, SPL labels)", "https://api.fda.gov/drug/event.json?search=<query>"),
}


def classify(rec, ids):
    rr = (rec["retrieval_route"] + " " + rec["identifier"] + " " + rec["citation"]).lower()
    if ids.get("patent"):                                   return "USPTO"
    if ids.get("setid") and "openfda" not in rr:            return "DailyMed"
    if "openfda" in rr or "faers" in rr:                    return "openFDA"
    if ids.get("nda") or "drugs@fda" in rr or "accessdata" in rr: return "Drugs@FDA"
    if ids.get("ema") or "ema " in rr or "epar" in rr:      return "EMA"
    if ids.get("pmcid"):                                    return "PMC"
    if "clinicaltrials" in rr or (ids.get("nct") and not ids.get("pmid")): return "ClinicalTrials.gov"
    if ids.get("pmid"):                                     return "PubMed"
    return "other"


def parse_ids(text):
    out = {}
    for k, rx in RX.items():
        m = rx.search(text)
        if not m:
            continue
        if k == "patent":
            out[k] = m.group(1).replace(",", "")
        elif k == "doi":
            d = m.group(1).rstrip(".,;")
            while d.endswith(")") and d.count(")") > d.count("("):
                d = d[:-1].rstrip(".,;")
            out[k] = d
        else:
            out[k] = m.group(1) if m.groups() else m.group(0)
    return out


def links_for(db, ids):
    """Canonical, resolvable URLs. The first is the primary landing page for the record."""
    L = []
    if ids.get("pmcid"):
        L.append(("PMC article", f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{ids['pmcid']}/"))
    if ids.get("pmid"):
        L.append(("PubMed record", f"https://pubmed.ncbi.nlm.nih.gov/{ids['pmid']}/"))
    if ids.get("doi"):
        L.append(("DOI", f"https://doi.org/{ids['doi']}"))
    if ids.get("patent"):
        L.append(("USPTO PDF", f"https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/{ids['patent']}"))
        L.append(("Patent record", f"https://patents.google.com/patent/US{ids['patent']}"))
    if ids.get("setid"):
        L.append(("DailyMed label", f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={ids['setid']}"))
    if ids.get("nct"):
        L.append(("ClinicalTrials.gov", f"https://clinicaltrials.gov/study/{ids['nct']}"))
    if ids.get("nda"):
        L.append(("Drugs@FDA", f"https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo={ids['nda']}"))
    if db == "EMA" and not L:
        L.append(("EMA medicine page", "https://www.ema.europa.eu/en/medicines"))
    if db == "openFDA" and not L:
        L.append(("openFDA API", "https://open.fda.gov/apis/drug/event/"))
    return L


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def check(url):
    """Resolution status.

    For doi.org the right question is whether the DOI is REGISTERED, so redirects are not
    followed: a 301/302 means it resolves. Following it would report the publisher's
    bot-blocking as a broken link, which it is not."""
    import urllib.error
    hdr = {"User-Agent": "OligoTox-Coagulopathy/1.0 (provenance link check)"}
    opener = urllib.request.build_opener(_NoRedirect) if "doi.org/" in url else urllib.request.build_opener()
    try:
        with opener.open(urllib.request.Request(url, headers=hdr), timeout=25) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main():
    do_check = "--no-check" not in sys.argv
    S = list(csv.DictReader(open(os.path.join(DATA, "sources.csv"), newline="", encoding="utf-8")))
    for r in S:
        r["_ids"] = parse_ids(r["identifier"] + " " + r["citation"])
        r["_db"] = classify(r, r["_ids"])
        r["_links"] = links_for(r["_db"], r["_ids"])

    status = {}
    if do_check:
        urls = sorted({u for r in S for _, u in r["_links"]})
        print(f"  checking {len(urls)} links…")
        with ThreadPoolExecutor(max_workers=8) as ex:
            for u, st in zip(urls, ex.map(check, urls)):
                status[u] = st
        ok = sum(1 for v in status.values() if 200 <= v < 400)
        print(f"    {ok}/{len(urls)} resolved")

    def badge(u):  # noqa: E306
        if not do_check:
            return '<span class="nc">not checked</span>'
        v = status.get(u, 0)
        if 200 <= v < 400: return '<span class="ok">resolves</span>'
        if v in (401, 403): return f'<span class="warn">{v} (blocks automated agents)</span>'
        if v == 0:          return '<span class="warn">no response</span>'
        return f'<span class="warn">HTTP {v}</span>'

    bydb = defaultdict(list)
    for r in S:
        bydb[r["_db"]].append(r)
    order = [k for k in ("PMC", "PubMed", "USPTO", "Drugs@FDA", "EMA", "DailyMed",
                         "ClinicalTrials.gov", "openFDA", "other") if k in bydb]

    tot_m = sum(int(r["n_measurements"]) for r in S)
    B = []
    B.append(f'<p class="small">Generated {TODAY} from <code>data/sources.csv</code>, which is itself '
             f'generated by the build. Every row of the dataset carries a <code>source_id</code> that '
             f'resolves to an entry below.</p>')
    B.append('<div class="kpis">'
             f'<div class="kpi"><b>{len(S)}</b><span>sources</span></div>'
             f'<div class="kpi"><b>{len(order)}</b><span>databases</span></div>'
             f'<div class="kpi"><b>{tot_m:,}</b><span>measurements traced</span></div>'
             f'<div class="kpi"><b>{sum(1 for r in S if r["document_file"] not in ("NOT_REPORTED",""))}</b>'
             f'<span>documents held locally</span></div></div>')

    B.append("<h2>1. Databases and access routes</h2>")
    B.append("<p>Every document was retrieved programmatically from a public repository. No value in "
             "this dataset comes from a search-engine summary. The endpoints below are the ones "
             "actually used, not a generic citation of the resource.</p>")
    B.append('<table><tr><th>Database</th><th>What it holds</th><th>Endpoint used</th><th class="n">Sources</th><th class="n">Rows</th></tr>')
    for db in order:
        name, ep = DBS.get(db, (db, "—"))
        n = len(bydb[db]); m = sum(int(r["n_measurements"]) for r in bydb[db])
        B.append(f'<tr><td><b>{db}</b></td><td>{name}</td><td><code>{ep}</code></td>'
                 f'<td class="n">{n}</td><td class="n">{m:,}</td></tr>')
    B.append("</table>")

    B.append("<h2>2. How to check any single number</h2>")
    B.append("<p>The chain is three steps and needs nothing from us: take a row's "
             "<code>source_id</code> from <code>measurements.csv</code>; find it in the register "
             "below or in <code>sources.csv</code>; open the link, or open the copy held at "
             "<code>sources/documents/&lt;document_file&gt;</code> and search for the row's "
             "<code>verbatim_quote</code> at its <code>source_locus</code>. "
             "<code>scripts/verify_against_sources.py</code> automates exactly this for every "
             "numeric value in the release.</p>")

    if do_check:
        ok = sum(1 for v in status.values() if 200 <= v < 400)
        bad = {u: v for u, v in status.items() if not (200 <= v < 400)}
        B.append(f"<h2>3. Link check</h2><p>Every URL in this document was requested on {TODAY}: "
                 f"<b>{ok} of {len(status)} resolved</b>. DOIs are checked WITHOUT following the "
                 f"redirect, because the question is whether the DOI is registered; following it "
                 f"would report a publisher's bot-blocking as a broken link. ")
        if bad:
            gp = sum(1 for u in bad if "patents.google" in u)
            note = ("All of them are Google Patents pages returning 503 to automated clients. "
                    "The authoritative USPTO PDF link for each of those patents resolved, so no "
                    "patent is unreachable. "
                    if gp == len(bad) else
                    "They are listed with their status rather than presented as working. A 401/403 "
                    "means the publisher refuses automated clients, not that the record is missing. ")
            B.append(f"{len(bad)} did not. {note}"
                     "In every case the copy held at <code>sources/documents/</code> is the durable "
                     "route, which is why the release ships the documents rather than only citing them.</p>")
            B.append('<table><tr><th>URL</th><th class="n">Status</th></tr>')
            for u, v in sorted(bad.items(), key=lambda x: -x[1])[:40]:
                B.append(f'<tr><td><code>{u[:96]}</code></td><td class="n">{v or "no response"}</td></tr>')
            B.append("</table>")
        else:
            B.append("None failed.</p>")

    B.append('<h2>4. Source register</h2>')
    B.append("<p>Grouped by the database the document was retrieved from. "
             "<b>Rows</b> is the number of measurements in the released dataset that cite this source; "
             "<b>Oligos</b> the number of compounds it describes.</p>")
    for db in order:
        name, _ = DBS.get(db, (db, ""))
        rs = sorted(bydb[db], key=lambda r: -int(r["n_measurements"]))
        B.append(f'<h3 class="pbavoid">{db} &mdash; {name} ({len(rs)} sources)</h3>')
        for r in rs:
            cite = r["citation"].strip()
            B.append('<div class="src">')
            B.append(f'<div class="sid">{r["source_id"]} '
                     f'<span class="cnt">{int(r["n_measurements"]):,} rows &middot; {r["n_oligos"]} oligos</span></div>')
            B.append(f'<div class="cite">{cite}</div>')
            if r["_links"]:
                B.append('<div class="lnk">' + " &nbsp;·&nbsp; ".join(
                    f'{lbl}: <a href="{u}">{u}</a> {badge(u)}' for lbl, u in r["_links"]) + "</div>")
            else:
                B.append(f'<div class="lnk"><i>No resolvable public identifier; '
                         f'identified as:</i> {r["identifier"][:200]}</div>')
            B.append(f'<div class="meta">Retrieved via: {r["retrieval_route"][:190]}<br>'
                     f'Licence: {r["licence"][:150]} &nbsp;|&nbsp; '
                     f'Redistribution: <code>{r["redistribution"]}</code>')
            if r["document_file"] not in ("NOT_REPORTED", ""):
                B.append(f'<br>Local copy: <code>sources/documents/{r["document_file"]}</code>')
            B.append("</div></div>")

    extra = """
    .src { border-left:2pt solid #cfd6e4; padding:3pt 0 3pt 7pt; margin:0 0 7pt; page-break-inside:avoid; }
    .sid { font-weight:700; color:#1F3864; font-size:8.8pt; }
    .cnt { float:right; font-weight:400; color:#52514e; font-size:7.8pt; }
    .cite { font-size:8.5pt; margin:1pt 0 2pt; }
    .lnk { font-size:7.6pt; word-break:break-all; margin-bottom:2pt; }
    .lnk a { color:#2a78d6; text-decoration:none; }
    .meta { font-size:7.4pt; color:#52514e; }
    .ok { color:#1baf7a; font-weight:700; } .warn { color:#eb6834; font-weight:700; }
    .nc { color:#52514e; }
    h3.pbavoid { page-break-before:auto; }
    """
    html = html_doc("OligoTox-Coagulopathy — Sources & Provenance",
                    "Every source, the database it came from, and a resolvable link · "
                    "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, Phase 2",
                    "\n".join(B)).replace("</style>", extra + "</style>")
    render(html, OUT, 200, "sources")


if __name__ == "__main__":
    main()
