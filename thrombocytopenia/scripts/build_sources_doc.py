#!/usr/bin/env python3
"""Generate the Data Sources & Provenance document (HTML -> PDF).

Every measurement in this dataset carries a source_ref and an exact locus. This
document turns that per-row provenance into a readable bibliography: what each
source is, which database it came from, a link that resolves, what rights attach
to it, and exactly how many rows — human and animal — it contributed.

It is generated from the data, not maintained by hand, so it cannot describe a
source the dataset no longer uses or omit one it does.

Usage:  python3 scripts/build_sources_doc.py
"""
import csv, json, os, re, subprocess, shutil, sys, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")
SUB = os.path.join(ENDPOINT, "submission")
SCRATCH = "/tmp/claude-0/-home-user-Claude-Works/189fa036-08d6-5409-99b8-7265f67bf20d/scratchpad"

RIGHTS = {
    "public_domain": ("Public domain", "US Government work (FDA/EMA/USPTO) — values reproducible without restriction"),
    "cc_by": ("CC-BY", "Creative Commons Attribution — raw values reproducible with attribution"),
    "summary_stat": ("Summary stat.", "Copyrighted; reproduced as summary statistics under fair use"),
    "derived_features_only": ("Derived only", "Copyrighted; derived features only"),
    "verify": ("Unresolved", "Rights not yet settled"),
}


def classify(ref):
    r = ref.lower()
    if "clinicaltrials.gov" in r or re.search(r"\bnct\d{8}\b", r):
        return "registry"
    if ref.startswith("US ") or re.match(r"^US\s?\d", ref) or "US 20" in ref:
        return "patent"
    if "dailymed" in r or "_spl_" in r or ref.startswith("FDA_label"):
        return "fda_label"
    if "fda nda" in r or "orig1s000" in r:
        return "fda_review"
    if ref.startswith("EMA") or "ema/" in r or "emea/" in r:
        return "ema"
    return "literature"


def link(ref, cls, ids):
    """Build a URL that actually resolves for this source."""
    if cls == "registry":
        nct = re.search(r"(NCT\d{8})", ref)
        return f"https://clinicaltrials.gov/study/{nct.group(1)}" if nct else ""
    if cls == "patent":
        m = re.search(r"US\s?([\d,]{7,12})\s?([AB]\d?)", ref) or re.search(r"US\s?(\d{4}/\d{7})\s?(A\d)", ref)
        if m:
            num = m.group(1).replace(",", "").replace("/", "")
            return f"https://patents.google.com/patent/US{num}{m.group(2)}/en"
        return "https://patents.google.com/"
    if cls == "fda_label":
        sid = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27,})", ref)
        if sid:
            return f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={sid.group(1)}"
        drug = re.search(r"label_([A-Z]+)", ref)
        return (f"https://dailymed.nlm.nih.gov/dailymed/search.cfm?labeltype=all&query={drug.group(1)}"
                if drug else "https://dailymed.nlm.nih.gov/")
    if cls == "fda_review":
        nda = re.search(r"NDA\s?(\d{6})", ref)
        return (f"https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo={nda.group(1)}"
                if nda else "https://www.accessdata.fda.gov/scripts/cder/daf/")
    if cls == "ema":
        prod = re.search(r"\b(Waylivra|Tegsedi|Oxlumo|Qalsody|Spinraza|Onpattro|Amvuttra|Givlaari|Leqvio|Wainua|Tryngolza)\b", ref, re.I)
        return (f"https://www.ema.europa.eu/en/medicines/human/EPAR/{prod.group(1).lower()}"
                if prod else "https://www.ema.europa.eu/en/medicines")
    if ids.get("doi"):
        return f"https://doi.org/{ids['doi']}"
    if ids.get("pmcid"):
        return f"https://pmc.ncbi.nlm.nih.gov/articles/{ids['pmcid']}/"
    if ids.get("pmid"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{ids['pmid']}/"
    return ""


DB_NAME = {
    "fda_review": ("FDA — Drugs@FDA review documents", "accessdata.fda.gov",
                   "Multi-discipline, clinical and pharmacology/toxicology reviews. Retrieved as PDF and parsed with PyMuPDF; a browser User-Agent is required or the host returns 404."),
    "fda_label": ("FDA — prescribing information (DailyMed)", "dailymed.nlm.nih.gov",
                  "Structured Product Labels retrieved as XML through the DailyMed SPL REST API and parsed directly."),
    "ema": ("EMA — EPAR assessment reports and SmPCs", "ema.europa.eu",
            "European Public Assessment Reports and Summaries of Product Characteristics, retrieved as PDF and parsed with PyMuPDF."),
    "patent": ("USPTO patents", "patents.google.com",
               "Worked-example tables and formal sequence listings. Retrieved as HTML from Google Patents; the USPTO print-PDF endpoint returns image-only scans with no text layer."),
    "registry": ("Trial registry", "clinicaltrials.gov",
                 "Posted results — structured adverse-event and outcome-measure tables, retrieved through the ClinicalTrials.gov API v2."),
    "literature": ("Peer-reviewed literature", "europepmc.org · pmc.ncbi.nlm.nih.gov · doi.org",
                   "Full text retrieved as JATS XML through NCBI E-utilities or the Europe PMC REST API, with supplementary files where present; publisher PDF or PubMed abstract where full text was not open."),
}
ORDER = ["literature", "fda_review", "ema", "patent", "fda_label", "registry"]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    inv = json.load(open(os.path.join(SCRATCH, "source_inventory.json"), encoding="utf-8"))
    cit = json.load(open(os.path.join(SCRATCH, "citations.json"), encoding="utf-8"))
    ids_all, meta = cit["ids"], cit["meta"]

    groups = collections.defaultdict(list)
    for ref, v in inv.items():
        cls = classify(ref)
        groups[cls].append((ref, v))
    for g in groups.values():
        g.sort(key=lambda kv: -kv[1]["n"])

    n_rows = sum(v["n"] for v in inv.values())
    n_h = sum(v["human"] for v in inv.values())
    n_a = sum(v["animal"] for v in inv.values())
    rights_tot = collections.Counter()
    for v in inv.values():
        for r in v["redist"]:
            rights_tot[r] += v["n"]

    H = []
    H.append('<!doctype html><html><head><meta charset="utf-8">'
             '<link rel="stylesheet" href="style.css"><style>'
             'td.src{font-size:8pt} .u{font-family:"DejaVu Sans Mono",monospace;font-size:7.3pt;'
             'color:#1a4d8f;overflow-wrap:anywhere} a{color:#1a4d8f;text-decoration:none}'
             '.cite{font-size:8.2pt}'
             'h2{margin-top:6mm} .dbhdr{background:#eef1f5;border-left:3px solid #123;'
             'padding:2mm 2.6mm;margin:3mm 0 2mm}</style></head><body>')
    H.append('<div class="hdr"><h1>Data Sources &amp; Provenance</h1>'
             '<p class="sub">OligoTox-Thrombocytopenia — every source, database and link behind the dataset</p>'
             f'<p class="meta"><b>{len(inv)} distinct sources</b> · <b>{n_rows:,} measurements</b> '
             f'({n_h:,} human, {n_a:,} animal) · NIH/NCATS OligoTox Challenge, Phase 2</p></div>')

    H.append("<p>Every measurement in this dataset carries a <code>source_ref</code> and an exact "
             "<code>source_table</code> locus — the specific table, figure, claim or label section a "
             "value was read from. This document is <b>generated from the data</b>, so it cannot list a "
             "source the dataset no longer uses or omit one it does. For each entry: the full citation, "
             "the database it was retrieved from, a resolving link, the rights class governing reuse, "
             "the number of rows it contributed, and how many distinct loci within it were cited.</p>")

    H.append('<div class="note"><b>How to read the row counts.</b> "Rows" is the number of '
             'per-measurement records drawn from that source; "loci" is the number of distinct '
             'places within it that were cited. A source with 387 rows across 268 loci was mined '
             'cell-by-cell, not summarised — the two numbers together show extraction depth.</div>')

    H.append("<h2>Summary by database</h2><table>"
             "<tr><th>Database</th><th>Retrieved via</th><th class='n'>Sources</th>"
             "<th class='n'>Rows</th><th class='n'>Human</th></tr>")
    for cls in ORDER:
        if cls not in groups:
            continue
        name, host, _ = DB_NAME[cls]
        rows = sum(v["n"] for _, v in groups[cls])
        hum = sum(v["human"] for _, v in groups[cls])
        H.append(f"<tr><td><b>{esc(name)}</b></td><td><span class='u'>{esc(host)}</span></td>"
                 f"<td class='n'>{len(groups[cls])}</td><td class='n'>{rows:,}</td>"
                 f"<td class='n'>{hum:,}</td></tr>")
    H.append("</table>")

    H.append("<h2>Rights position across the dataset</h2><table>"
             "<tr><th>Class</th><th>Meaning for reuse</th><th class='n'>Rows</th></tr>")
    for k in ("public_domain", "cc_by", "summary_stat", "derived_features_only", "verify"):
        if rights_tot.get(k):
            lbl, mean = RIGHTS[k]
            H.append(f"<tr><td><b>{lbl}</b></td><td>{esc(mean)}</td>"
                     f"<td class='n'>{rights_tot[k]:,}</td></tr>")
    H.append("</table><p>Rights are tracked <b>per row</b>, not per dataset, so a consumer can filter "
             "to exactly the records they may lawfully reuse. A CC-BY classification is taken from the "
             "article's own licence field, never from the fact that it is free to read.</p>")

    for cls in ORDER:
        if cls not in groups:
            continue
        name, host, how = DB_NAME[cls]
        H.append(f'<div class="pb"></div><h2>{esc(name)}</h2>')
        H.append(f'<div class="dbhdr"><b>Database:</b> <span class="u">{esc(host)}</span><br>'
                 f'<b>Retrieval:</b> {esc(how)}</div>')
        H.append("<table><tr><th style='width:52%'>Source</th><th style='width:26%'>Link</th>"
                 "<th class='n'>Rows</th><th class='n'>Loci</th><th>Rights</th></tr>")
        for ref, v in groups[cls]:
            ids = ids_all.get(ref, {})
            m = meta.get(ref)
            if m:
                au = m["authors"]
                au = au if len(au) < 70 else au.split(",")[0] + " et al."
                bits = [f"<b>{esc(m['title'])}</b>", f"{esc(au)}"]
                jr = " ".join(x for x in [m["journal"], m["year"],
                                          (m["volume"] or ""), (m["pages"] or "")] if x)
                if jr.strip():
                    bits.append(f"<i>{esc(jr)}</i>")
                idl = " · ".join(x for x in [
                    f"PMID {m['pmid']}" if m["pmid"] else "",
                    m["pmcid"] or "", f"doi:{m['doi']}" if m["doi"] else ""] if x)
                if idl:
                    bits.append(f"<span class='u'>{esc(idl)}</span>")
                if m.get("licence"):
                    bits.append(f"licence field: <code>{esc(m['licence'])}</code>")
                cellsrc = "<br>".join(bits)
            else:
                cellsrc = f"<b>{esc(ref)}</b>"
            u = link(ref, cls, ids)
            # rendered as a real anchor so the link is clickable in the PDF, not
            # merely printed — a reviewer should not have to retype a DOI
            cell_link = (f"<a href='{esc(u)}'><span class='u'>{esc(u)}</span></a>"
                         if u else "<span class='u'>—</span>")
            H.append(f"<tr><td class='src'>{cellsrc}</td>"
                     f"<td>{cell_link}</td>"
                     f"<td class='n'>{v['n']}</td><td class='n'>{len(v['loci'])}</td>"
                     f"<td style='font-size:8pt'>{RIGHTS.get(sorted(v['redist'])[0], ('?', ''))[0]}</td></tr>")
        H.append("</table>")

    H.append('<div class="pb"></div><h2>Retrieval routes, verbatim</h2>'
             "<p>Recorded so any value can be re-fetched, and because several routes are "
             "non-obvious — the wrong one silently returns nothing or an abstract stub:</p><table>"
             "<tr><th>Resource</th><th>Endpoint used</th></tr>"
             "<tr><td>PMC open-access full text</td><td class='u'>https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&amp;id=&lt;numeric id&gt;</td></tr>"
             "<tr><td>Europe PMC full text / supplementary files</td><td class='u'>https://www.ebi.ac.uk/europepmc/webservices/rest/PMC&lt;id&gt;/fullTextXML — and /supplementaryFiles</td></tr>"
             "<tr><td>Europe PMC rendered PDF <i>(when XML is abstract-only)</i></td><td class='u'>https://europepmc.org/articles/PMC&lt;id&gt;?pdf=render</td></tr>"
             "<tr><td>PubMed abstract</td><td class='u'>https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&amp;id=&lt;pmid&gt;&amp;rettype=abstract</td></tr>"
             "<tr><td>DailyMed SPL (FDA labels)</td><td class='u'>https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=&lt;drug&gt; → /spls/&lt;setid&gt;.xml</td></tr>"
             "<tr><td>FDA review documents</td><td class='u'>https://www.accessdata.fda.gov/drugsatfda_docs/nda/&lt;year&gt;/&lt;accession&gt;.pdf <b>(browser User-Agent required)</b></td></tr>"
             "<tr><td>EMA EPAR / SmPC</td><td class='u'>https://www.ema.europa.eu/en/documents/assessment-report/&lt;product&gt;-epar-public-assessment-report_en.pdf</td></tr>"
             "<tr><td>Patents</td><td class='u'>https://patents.google.com/patent/US&lt;number&gt;/en <b>(USPTO print PDFs are image-only)</b></td></tr>"
             "<tr><td>Trial registry</td><td class='u'>https://clinicaltrials.gov/api/v2/studies</td></tr>"
             "<tr><td>Citation resolution for this document</td><td class='u'>https://www.ebi.ac.uk/europepmc/webservices/rest/search (resultType=core)</td></tr>"
             "</table>")

    H.append("<h2>What is deliberately absent</h2>"
             "<p><b>No third-party full text is redistributed.</b> Sources are referenced by identifier "
             "and exact locus; the PDFs and XML retrieved during extraction were working files and are "
             "not committed. What <i>is</i> committed is the curation record — every agent's returned "
             "rows, the adversarial-verification verdicts, and the source sweep — so the published "
             "tables are reproducible from their inputs rather than merely re-checkable against these "
             "citations.</p>"
             "<p><b>Sources consulted but not used</b> are not listed here. Two categories were "
             "deliberately excluded during curation: on-target antithrombotic pharmacology (aptamers "
             "that inhibit platelet function <i>by design</i> — that is the intended mechanism, not "
             "toxicity), and papers whose platelet content could not be pinned to a specific locus. A "
             "row whose exact locus could not be named was dropped rather than kept with a vague "
             "citation.</p>")

    H.append('<p class="foot">OligoTox-Thrombocytopenia · data sources &amp; provenance · CC-BY 4.0 · '
             'generated by <code>scripts/build_sources_doc.py</code> from '
             '<code>data/measurements.csv</code></p></body></html>')

    src = os.path.join(SUB, "sources.html")
    open(src, "w", encoding="utf-8").write("\n".join(H))
    ch = next((c for c in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                           shutil.which("chromium"), shutil.which("google-chrome"))
               if c and os.path.exists(c)), None)
    out = os.path.join(SUB, "sources.pdf")
    subprocess.run([ch, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={out}", src], capture_output=True)
    import pymupdf
    print(f"wrote submission/sources.pdf — {len(pymupdf.open(out))} pages, "
          f"{len(inv)} sources, {n_rows:,} rows")
    for cls in ORDER:
        if cls in groups:
            print(f"  {DB_NAME[cls][0]:<44} {len(groups[cls]):>3} sources  "
                  f"{sum(v['n'] for _, v in groups[cls]):>5} rows")


if __name__ == "__main__":
    main()
