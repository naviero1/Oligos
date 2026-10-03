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

# SUPERSEDED. These are the LEGACY redistribution tags carried on the measurement rows.
# They were a coarse curation shorthand, never a licence determination, and two of them were
# actively wrong: "public_domain" lumped EMA and USPTO material in with US federal works, and
# "summary_stat" asserted a fair-use position this project is not in a position to assert.
# Retained here only so the legacy column remains readable; the live classification is
# licence_class in curation/rights/shipped_row_rights.csv, built per publisher and per regulator.
LEGACY_RIGHTS = {
    "public_domain": ("public_domain", "legacy tag — mixed US federal, EMA and USPTO material"),
    "cc_by": ("cc_by", "legacy tag — Creative Commons Attribution asserted"),
    "summary_stat": ("summary_stat", "legacy blanket tag — NOT a licence determination"),
    "derived_features_only": ("derived_features_only", "legacy tag — derived features only"),
    "verify": ("verify", "legacy tag — rights not yet settled"),
}

# The live classification: one class per publisher-declared licence or per regulator, because
# "regulator document = public domain" is true of US federal agencies and FALSE of the others.
LC_SHORT = {
    "public_domain_us_federal": "US fed PD",
    "public_domain_uspto_patent": "patent PD",
    "ema_reuse_with_attribution": "EMA attrib",
    "cc_permissive": "CC-BY/CC0",
    "cc_nc_noncommercial": "CC-NC",
    "cc_nd_derivatives_restricted": "CC-ND",
    "closed_no_open_licence": "HOLD",
}

LICENCE_CLASS = [
    ("public_domain_us_federal", "US federal agency work",
     "No copyright under 17 U.S.C. §105. Reproducible without restriction."),
    ("public_domain_uspto_patent", "Granted US patent text",
     "Patent specifications are published without copyright restriction. Reproducible; the "
     "patent CLAIMS remain enforceable as patent rights, which is a separate matter from copying."),
    ("ema_reuse_with_attribution", "EMA document",
     "NOT US public domain. EMA permits reuse, including commercial reuse, WITH attribution."),
    ("cc_permissive", "CC-BY / CC0 article",
     "Publisher-declared permissive licence. Values reproducible with attribution."),
    ("cc_nc_noncommercial", "CC-BY-NC article",
     "NonCommercial clause. Whether a prize submission is a commercial use is UNSETTLED and is "
     "not ours to decide; flagged, not assumed either way."),
    ("cc_nd_derivatives_restricted", "CC-BY-ND article",
     "NoDerivatives clause. Excluded from derived outputs."),
    ("closed_no_open_licence", "No open licence located",
     "PROPOSED HOLD pending the data owner's ruling. Zero rows withdrawn and zero rows cleared "
     "by this curation effort."),
]


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


def build_inventory():
    """Compute the source inventory from the committed data.

    This used to read a JSON file written into a scratch directory by a separate
    step. That made the sources document silently stale whenever the dataset
    moved without that step rerunning -- and it broke outright when the scratch
    directory went away. The inventory is now derived from
    data/measurements.csv on every build, so it cannot disagree with the dataset
    it claims to document.
    """
    path = os.path.join(BASE, "measurements.csv")
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    inv = {}
    for r in rows:
        ref = r["source_ref"]
        v = inv.setdefault(ref, {"n": 0, "human": 0, "animal": 0, "redist": set(),
                                 "clinical": 0, "lab": 0, "oligos": set(), "loci": set()})
        v["n"] += 1
        sc = r.get("subject_class") or ""
        if sc.startswith("human"):
            v["human"] += 1
            if sc == "human_clinical": v["clinical"] += 1
            else: v["lab"] += 1
        elif sc.startswith("animal"):
            v["animal"] += 1
        if r.get("redistribution"): v["redist"].add(r["redistribution"])
        if r.get("source_table"): v["loci"].add(r["source_table"])
        v["oligos"].add(r["oligo_id"])
    for v in inv.values():
        v["redist"] = sorted(v["redist"])
        v["oligos"] = len(v["oligos"])
        v["loci"] = sorted(v["loci"])
    return inv


def main():
    inv = build_inventory()
    cpath = os.path.join(SCRATCH, "citations.json")
    if os.path.exists(cpath):
        cit = json.load(open(cpath, encoding="utf-8"))
        ids_all, meta = cit["ids"], cit["meta"]
    else:
        # Citation enrichment is optional decoration; the document must build
        # from the dataset alone rather than fail when a cache is absent.
        ids_all, meta = {}, {}

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

    # Rights: read the live per-row classification rather than the legacy tag. An earlier version
    # of this page published the legacy tag as a rights position, which asserted a fair-use
    # determination and treated EMA and USPTO material as US public domain. Both were wrong.
    lc = collections.Counter()
    src_lc = collections.defaultdict(collections.Counter)
    lcpath = os.path.join(ENDPOINT, "curation", "rights", "shipped_row_rights.csv")
    if os.path.exists(lcpath):
        with open(lcpath, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                lc[r["licence_class"]] += 1
                src_lc[r["source_ref"]][r["licence_class"]] += 1

    def lc_of(ref):
        """The live licence class for one source. A source's rows all share a publisher, so
        this is normally unanimous; if it is not, say so rather than pick a winner."""
        c = src_lc.get(ref)
        if not c:
            return "?"
        if len(c) == 1:
            return LC_SHORT.get(next(iter(c)), next(iter(c)))
        return "mixed"

    H.append("<h2>Rights position across the dataset</h2>")
    H.append("<p><b>Two separate questions, and this page answers only the second.</b> "
             "(1) May the <i>source file</i> be republished? (2) May the <i>facts extracted from it</i> "
             "be reused? A measured value read out of a copyrighted table is not the table. This "
             "classification is about extracted-fact reuse; nothing here licenses republication of a "
             "source document.</p>")
    if lc:
        H.append("<table><tr><th>Class</th><th>What it is</th><th>Position on extracted-fact reuse</th>"
                 "<th class='n'>Rows</th></tr>")
        for key, what, meaning in LICENCE_CLASS:
            if lc.get(key):
                H.append(f"<tr><td><b>{esc(key)}</b></td><td>{esc(what)}</td>"
                         f"<td>{esc(meaning)}</td><td class='n'>{lc[key]:,}</td></tr>")
        H.append("</table>")
        rel = sum(v for k, v in lc.items() if k != "closed_no_open_licence")
        hold = lc.get("closed_no_open_licence", 0)
        H.append(f"<p><b>{rel:,} rows</b> carry a publisher-declared or regulator-stated position "
                 f"permitting extracted-data release. <b>{hold:,} rows</b> are on "
                 f"<b>PROPOSED HOLD</b>: no open licence was located, and the ruling belongs to the "
                 f"data owner. <b>Zero rows withdrawn, zero rows cleared</b> by this curation effort "
                 f"— the holds are proposed, not applied.</p>")
    H.append("<p><b>This ledger is a project classification, not legal clearance.</b> It records what "
             "each publisher or regulator declares, with the basis, so the position is auditable "
             "rather than asserted. A permissive classification is taken from the article's own "
             "licence field, never from the fact that it is free to read. Rights are tracked "
             "<b>per row</b>, so a consumer can filter to the records matching their own "
             "determination. The per-regulator split matters: <b>regulator document = government work "
             "= public domain reaches US federal agencies only.</b> EMA permits reuse with "
             "attribution, and other national regulators are more restrictive still — one forbids "
             "redistribution without written approval and another reserves all rights. "
             "Full per-row ledger: <code>curation/rights/shipped_row_rights.csv</code>.</p>")

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
                     f"<td style='font-size:8pt'>{esc(lc_of(ref))}</td></tr>")
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
    # Write the acquisition tally so METHODOLOGY can quote it instead of quoting the
    # retired legacy rights tags, which conflated FDA, EMA and USPTO material.
    tally = os.path.join(ENDPOINT, "data", "source_class_counts.csv")
    with open(tally, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_class", "label", "n_sources", "n_rows"])
        for cls in ORDER:
            if cls in groups:
                w.writerow([cls, DB_NAME[cls][0], len(groups[cls]),
                            sum(v["n"] for _, v in groups[cls])])
    for cls in ORDER:
        if cls in groups:
            print(f"  {DB_NAME[cls][0]:<44} {len(groups[cls]):>3} sources  "
                  f"{sum(v['n'] for _, v in groups[cls]):>5} rows")
    print(f"  -> {os.path.relpath(tally, ENDPOINT)}")


if __name__ == "__main__":
    main()
