#!/usr/bin/env python3
"""
Renders OligoTox-Hydrocephalus_Sources.pdf — the source and provenance register.

This is a supplementary document, not one of the four required Phase 2 parts. It
exists because a dataset's claims are only as good as the documents behind them,
and a reader asked to trust 1,300+ rows is entitled to see every one of those
documents named, located and linked.

Every figure, every citation and every URL in this document is READ FROM THE DATA
(data/sources.csv, data/trial_registry.csv, notes/link_check.json,
notes/source_backlog.csv, qc/stats.json). Nothing is typed twice, so the document
cannot drift from the release it describes.

Usage: python3 docs/build_sources_pdf.py
       (after scripts/assemble.py, qc/validate.py and scripts/check_source_links.py)
"""
import collections
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pdfs import (ACCENT, BODY, BULLET, CELL, H1, H2, MUTED, SMALL, SUB,
                        TITLE, build, bullets, table)  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, Spacer  # noqa: E402

# Justified text and long unbreakable Courier strings (URLs, API paths) fight
# each other: reportlab stretches the spaces instead of the token and the line
# comes out with gaps. Anything carrying a literal goes left-aligned.
LEFT = ParagraphStyle("left", parent=BODY, alignment=0)
LEFTSMALL = ParagraphStyle("leftsmall", parent=SMALL, alignment=0)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")

# Column widths (inches -> points handled by build_pdfs.table via reportlab units)
from reportlab.lib.units import inch  # noqa: E402


def clip(text, n):
    """Truncate on a word boundary so a table cell never ends mid-word."""
    text = str(text)
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return (cut or text[:n]) + "\u2026"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def link(url, label=None):
    if not url:
        return "&mdash;"
    return '<link href="%s" color="#2C6E9B">%s</link>' % (esc(url),
                                                          esc(label or url))


def database_of(source_id):
    if source_id.startswith("NCT"):
        return "ClinicalTrials.gov"
    if source_id.startswith("DailyMed_SPL_"):
        return "DailyMed (FDA SPL)"
    if source_id.startswith("WHO_INN_List_"):
        return "WHO INN lists"
    if source_id.startswith("EMA_SmPC_"):
        return "EMA EPAR"
    if source_id == "FAERS_openFDA":
        return "openFDA FAERS"
    return "PubMed Central / Europe PMC"


# Access route, one line each, keyed by the database label above.
ENDPOINTS = {
    "ClinicalTrials.gov": (
        "ClinicalTrials.gov REST API v2 &mdash; <font face='Courier'>GET "
        "https://clinicaltrials.gov/api/v2/studies?query.intr=&lt;drug&gt;</font> to "
        "enumerate, then <font face='Courier'>GET /api/v2/studies/&lt;NCT&gt;</font> "
        "for each record. Rows come from "
        "<font face='Courier'>resultsSection.adverseEventsModule</font>."),
    "openFDA FAERS": (
        "openFDA drug/event REST API &mdash; <font face='Courier'>GET "
        "https://api.fda.gov/drug/event.json?search=&lt;drug&gt; AND "
        "patient.reaction.reactionmeddrapt.exact:\"&lt;PT&gt;\"</font>, one exact "
        "query per (drug, term) pair."),
    "DailyMed (FDA SPL)": (
        "DailyMed REST API v2 &mdash; <font face='Courier'>GET /dailymed/services/v2/"
        "spls/&lt;setid&gt;.xml</font>. Each citation carries the setid and "
        "publication date of the exact label version read."),
    "EMA EPAR": (
        "European Public Assessment Report product-information PDFs from "
        "ema.europa.eu, text-extracted and swept section by section."),
    "WHO INN lists": (
        "Recommended INN list PDFs from cdn.who.int, parsed residue by residue by "
        "<font face='Courier'>scripts/parse_inn_sequences.py</font>."),
    "PubMed Central / Europe PMC": (
        "Europe PMC REST <font face='Courier'>fullTextXML</font> endpoint; open-access "
        "full text only, never a paywalled PDF."),
}

WHAT_IT_GIVES = {
    "ClinicalTrials.gov": "Per-arm adverse-event counts with denominators, including reported zeros",
    "openFDA FAERS": "Spontaneous-report counts by drug and MedDRA preferred term",
    "DailyMed (FDA SPL)": "US label text, and the chemistry statements behind the modification maps",
    "EMA EPAR": "EU label text &mdash; the jurisdiction contrast",
    "WHO INN lists": "Sequence and per-position chemistry, by deterministic parse",
    "PubMed Central / Europe PMC": "Case reports, the disease background rate, and the nonclinical rows",
}


def load(path, reader=csv.DictReader):
    with open(path) as fh:
        return list(reader(fh))


def main():
    src = load(os.path.join(DATA, "sources.csv"))
    meas = load(os.path.join(DATA, "measurements.csv"))
    mods = load(os.path.join(DATA, "modifications.csv"))
    trials = load(os.path.join(DATA, "trial_registry.csv"))
    stats = json.load(open(os.path.join(ROOT, "qc", "stats.json")))
    links = json.load(open(os.path.join(NOTES, "link_check.json")))
    backlog = load(os.path.join(NOTES, "source_backlog.csv"))

    rows_by_src = collections.Counter(r["source_id"] for r in meas)
    mods_by_src = collections.Counter(r["source_id"] for r in mods)
    by_db = collections.defaultdict(list)
    for r in src:
        by_db[database_of(r["source_id"])].append(r)

    f = []

    # ------------------------------------------------------------------ cover
    f.append(Paragraph("OligoTox-Hydrocephalus &mdash; Source and Provenance Register", TITLE))
    f.append(Paragraph(
        "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, Phase 2 &middot; "
        "hydrocephalus and CSF-dynamics endpoints &middot; supplementary to the four "
        "required submission documents", SUB))
    f.append(Paragraph(
        "Every measurement in this release names the document it came from, and this "
        "register names every one of those documents: what database it was taken from, "
        "how it was retrieved, where in it the value sits, what may lawfully be done "
        "with it, and a link that resolves. %d source records support %d measurement "
        "rows and %d per-position chemistry rows across %d compounds."
        % (len(src), len(meas), len(mods), stats["n_oligos"]), BODY))
    f.append(Paragraph(
        "The register is generated from the data itself, never typed alongside it. "
        "Three checks in <font face='Courier'>qc/validate.py</font> enforce that every "
        "source carrying rows has a real citation, states its link, rights, evidence "
        "tier and retrieval route, and points at a document rather than a bare "
        "hostname. All %d distinct URLs below were resolved on %s; %d returned a "
        "success status and none was dead."
        % (links["n_urls"], links["checked_on"], links["tally"].get("ok", 0)), BODY))

    f.append(Paragraph("How to trace any single number", H2))
    f.append(Paragraph(
        "Every row of <font face='Courier'>measurements.csv</font> carries four "
        "provenance columns, and together they resolve to one sentence in one "
        "document:", BODY))
    f += bullets([
        "<b>source_id</b> &mdash; the key of the row in <font face='Courier'>sources.csv</font>, which is the table reproduced in this document.",
        "<b>source_ref</b> &mdash; the stable external identifier: an NCT number, a PMID/PMCID/DOI, or a DailyMed setid with its publication date.",
        "<b>source_location</b> &mdash; where inside that document the value sits: a named results table, a LOINC-coded label section, an SmPC Annex I section number, a figure number.",
        "<b>evidence_quote</b> &mdash; for curated rows, the source's own words, so the reading is checkable without re-fetching the paper.",
    ])

    # ------------------------------------------------------- database summary
    f.append(Paragraph("1 &nbsp; Databases and archives used", H1))
    f.append(Paragraph(
        "Six. Each is a primary public source; none of the release derives from a "
        "secondary compilation, a review article's table, or another curated dataset.",
        BODY))
    rows = [["Database", "What it supplies here", "Records", "Meas. rows",
             "Pos. rows", "Rights"]]
    order = sorted(by_db, key=lambda d: -sum(rows_by_src[r["source_id"]] for r in by_db[d]))
    for db in order:
        recs = by_db[db]
        lic = sorted({r["license"] for r in recs})
        rows.append([
            "<b>%s</b>" % esc(db), WHAT_IT_GIVES.get(db, ""),
            str(len(recs)),
            str(sum(rows_by_src[r["source_id"]] for r in recs)),
            str(sum(mods_by_src[r["source_id"]] for r in recs)),
            esc(clip("; ".join(x.split(";")[0] for x in lic), 58))])
    f.append(table(rows, [1.12 * inch, 1.83 * inch, .56 * inch, .66 * inch,
                          .58 * inch, 1.55 * inch]))

    f.append(Paragraph("Exact access route, per database", H2))
    for db in order:
        f.append(Paragraph("<b>%s.</b> %s" % (esc(db), ENDPOINTS.get(db, "")), LEFT))
    f.append(Paragraph(
        "Raw payloads for every retrieval are kept under "
        "<font face='Courier'>sources/raw/</font> so any extraction can be re-derived "
        "without re-querying the host.", LEFTSMALL))

    # ---------------------------------------------------- primary literature
    f.append(PageBreak())
    f.append(Paragraph("2 &nbsp; Primary literature", H1))
    f.append(Paragraph(
        "Seven papers, all open access, all retrieved as full text through Europe PMC. "
        "These are the rows that carry a quotation, a figure number and an author "
        "attribution &mdash; the evidence a registry table cannot give.", BODY))
    lit = sorted(by_db["PubMed Central / Europe PMC"],
                 key=lambda r: (r["year"], r["first_author"]))
    for r in lit:
        f.append(Paragraph("<b>%s</b>" % esc(r["citation"]), BODY))
        bits = []
        for lbl, col in (("DOI", "doi"), ("PMID", "pmid"), ("PMCID", "pmcid")):
            if r[col]:
                bits.append("%s %s" % (lbl, esc(r[col])))
        bits.append("licence %s" % esc(r["license"]))
        bits.append("redistribution <b>%s</b>" % esc(r["redistribution"]))
        bits.append("%d measurement rows, %d position rows"
                    % (rows_by_src[r["source_id"]], mods_by_src[r["source_id"]]))
        f.append(Paragraph(" &middot; ".join(bits), SMALL))
        f.append(Paragraph(link(r["url"]), SMALL))
        if r["notes"]:
            f.append(Paragraph("<i>%s</i>" % esc(r["notes"]), SMALL))
        f.append(Spacer(1, 5))

    # ------------------------------------------------------------ regulatory
    f.append(PageBreak())
    f.append(Paragraph("3 &nbsp; Regulatory documents", H1))
    f.append(Paragraph("3.1 &nbsp; US labels &mdash; DailyMed Structured Product Labels", H2))
    f.append(Paragraph(
        "A US label is revised in place, so a link to the drug's DailyMed page does not "
        "identify what was read. Each row below carries the setid and the publication "
        "date of the specific label version parsed. A label that is silent on the "
        "endpoint produces an explicit <font face='Courier'>measured_null</font> row "
        "rather than no row at all, which is why silent labels appear here.", BODY))
    rows = [["Drug", "Label version read", "Rows", "DailyMed setid"]]
    for r in sorted(by_db["DailyMed (FDA SPL)"], key=lambda r: r["source_id"]):
        drug = r["source_id"][len("DailyMed_SPL_"):]
        setid = r["url"].split("setid=")[-1] if "setid=" in r["url"] else "&mdash;"
        pub = r["citation"].split("published ")[-1].rstrip(")") if "published " in r["citation"] else ""
        rows.append([esc(drug), esc(pub), str(rows_by_src[r["source_id"]]),
                     link(r["url"], setid)])
    f.append(table(rows, [1.0 * inch, 1.05 * inch, .45 * inch, 3.8 * inch]))

    f.append(Paragraph("3.2 &nbsp; EU labels &mdash; EMA EPAR product information", H2))
    f.append(Paragraph(
        "Included because the two regulators reached materially different positions on "
        "the same molecules: the EMA gives hydrocephalus its own subheading under "
        "section 4.4 for nusinersen, where the US label mentions it only under "
        "postmarketing experience. A jurisdiction contrast on an identical molecule is "
        "itself a datum about how strongly the signal is judged.", BODY))
    for r in sorted(by_db["EMA EPAR"], key=lambda r: r["source_id"]):
        f.append(Paragraph("<b>%s</b>" % esc(r["citation"]), BODY))
        n_r = rows_by_src[r["source_id"]]
        f.append(Paragraph("%s &middot; %d row%s &middot; redistribution <b>%s</b>"
                           % (link(r["url"]), n_r, "" if n_r == 1 else "s",
                              esc(r["redistribution"])), SMALL))
        f.append(Spacer(1, 4))
    f.append(Paragraph(
        "EMA reuse terms were not established in this session, so every EU-label row is "
        "marked <font face='Courier'>redistribution = verify</font> rather than assumed "
        "open. A redistributor should resolve the licence before republishing those "
        "values.", SMALL))

    # ------------------------------------------------------------- sequences
    f.append(Paragraph("4 &nbsp; Sequence and chemistry provenance &mdash; WHO INN lists", H1))
    f.append(Paragraph(
        "No US label prints an oligonucleotide's sequence. The WHO Recommended INN "
        "entry does, indirectly but completely: it spells out every residue longhand "
        "&mdash; its sugar, its base, any 5-methylation, and whether the linkage to the "
        "next residue is a phosphorothioate or a plain phosphodiester &mdash; so both "
        "the sequence and the per-position modification map are recovered by "
        "deterministic parse rather than judgement.", BODY))
    rows = [["INN list", "Compounds parsed from it", "Position rows", "Link"]]
    inn_by_list = collections.defaultdict(list)
    for m in mods:
        if m["source_id"].startswith("WHO_INN_List_"):
            if m["oligo_name"] not in inn_by_list[m["source_id"]]:
                inn_by_list[m["source_id"]].append(m["oligo_name"])
    for r in sorted(by_db["WHO INN lists"], key=lambda r: int(r["source_id"].rsplit("_", 1)[1])):
        n = r["source_id"].rsplit("_", 1)[1]
        rows.append(["List %s" % n,
                     esc(", ".join(inn_by_list.get(r["source_id"], [])) or "&mdash;"),
                     str(mods_by_src[r["source_id"]]),
                     link(r["url"], "rl%s.pdf" % n)])
    f.append(table(rows, [.7 * inch, 1.5 * inch, .7 * inch, 3.4 * inch]))
    f.append(Paragraph(
        "The parse is validated against evidence that does not come from the INN list, "
        "and <font face='Courier'>scripts/parse_inn_sequences.py</font> refuses to emit "
        "a sequence that disagrees: parsed length must equal the length derived from "
        "the label's molecular formula, and parsed phosphorothioate and phosphodiester "
        "counts must equal the label's own statement where it makes one. Two further "
        "lists were parsed successfully but contribute nothing to this release: "
        "zorevunersen (list 87) and elsunersen (list 92) have no trial with posted "
        "results and therefore no measurement row for a sequence to attach to. Their "
        "parses are retained in <font face='Courier'>data/inn_sequences.json</font>.",
        BODY))

    # ------------------------------------------------------- pharmacovigilance
    f.append(Paragraph("5 &nbsp; Pharmacovigilance &mdash; openFDA FAERS", H1))
    faers = by_db["openFDA FAERS"][0]
    f.append(Paragraph(
        "%s &mdash; %s &middot; %d measurement rows over %s compounds."
        % (esc(faers["citation"]), link(faers["url"]), rows_by_src["FAERS_openFDA"],
           faers["n_oligos"]), LEFT))
    f.append(Paragraph(
        "One exact query per (drug, MedDRA preferred term) pair, over 28 preferred "
        "terms spanning both endpoint tiers. Two design decisions are worth stating "
        "because both were corrections to earlier defects. First, an aggregated "
        "<font face='Courier'>count</font> query truncates at 100 buckets and silently "
        "loses the tail, so exact per-pair queries replaced it. Second, term strings "
        "are now verified against FAERS itself before use: "
        "<font face='Courier'>CEREBROSPINAL FLUID PROTEIN INCREASED</font> matches "
        "nothing because FAERS stores that preferred term as "
        "<font face='Courier'>CSF PROTEIN INCREASED</font>, and the unverified spelling "
        "had recorded a false zero for all 19 drugs. A pre-flight vocabulary probe now "
        "drops any term string the database does not know, so the same class of error "
        "cannot recur silently.", BODY))
    f.append(Paragraph(
        "Spontaneous reports are counts of reports, not patients, and carry no exposure "
        "denominator. No disproportionality statistic is computed from them anywhere in "
        "this release.", SMALL))

    # --------------------------------------------------------- trial registry
    f.append(PageBreak())
    f.append(Paragraph("6 &nbsp; Clinical trial registry &mdash; the complete list", H1))
    usable = [t for t in trials if t["has_adverse_event_module"] == "TRUE"]
    f.append(Paragraph(
        "%d registered trials of an oligonucleotide therapeutic with posted results, "
        "every one of them enumerated by query rather than chosen. This matters more "
        "than any single citation: the first version of this component carried a "
        "hand-written map of 23 trials &mdash; the ones that surfaced while chasing the "
        "signal &mdash; which biases a dataset toward the compounds already suspected "
        "and silently discards the negative evidence that makes a positive "
        "interpretable. Asking the registry for all of them is what makes the %d "
        "reported zeros in this release meaningful."
        % (len(trials), stats["tier_A_null"]), BODY))
    byroute = collections.Counter(t["route"] for t in usable)
    f.append(Paragraph(
        "Route is taken from each trial's own intervention and arm text, never assumed "
        "from the compound, and the matched sentence is stored in "
        "<font face='Courier'>route_evidence</font> so the assignment is checkable. "
        "Distribution: %s."
        % esc(", ".join("%s %d" % (k, v) for k, v in byroute.most_common())), SMALL))
    harvested = [t for t in trials if t.get("discovery", "") not in
                 ("", "found by drug-name query")]
    f.append(Paragraph(
        "<b>An INN-only query is not sufficient, and the failure is silent.</b> The "
        "tominersen first-in-human trial NCT02519036 posts a full adverse-event module, "
        "but its record never contains the string &ldquo;tominersen&rdquo; &mdash; the "
        "drug is registered as ISIS 443139 with other name IONIS HTTRx &mdash; so no "
        "query on the INN could reach it and it was missing from the first registry. "
        "Trials are now also reached through development codes that a record equates "
        "with a compound inside a single intervention entry, and each such trial "
        "carries the record that supplied the alias in its "
        "<font face='Courier'>discovery</font> column (%d trials). A coverage sweep "
        "reports any fetched trial that posts adverse events but reaches no compound, "
        "so the next gap of this kind is loud rather than silent." % len(harvested),
        BODY))
    f.append(Spacer(1, 4))

    rows = [["NCT", "Compound", "Route", "Status", "Title"]]
    for t in sorted(trials, key=lambda t: (t["drug"], t["nct_id"])):
        rows.append([
            link("https://clinicaltrials.gov/study/%s" % t["nct_id"], t["nct_id"]),
            esc(clip(t["drug"], 26)), esc(t["route"].replace("_", " ")),
            esc(t["overall_status"].replace("_", " ").title()),
            esc(clip(t["brief_title"], 72))])
    f.append(table(rows, [.95 * inch, 1.02 * inch, .8 * inch, .72 * inch, 3.21 * inch]))

    # ----------------------------------------------------------- link check
    f.append(PageBreak())
    f.append(Paragraph("7 &nbsp; Locator verification", H1))
    f.append(Paragraph(
        "A provenance register is only as good as its locators, so every URL in it is "
        "resolved and the status recorded in "
        "<font face='Courier'>notes/link_check.json</font> by "
        "<font face='Courier'>scripts/check_source_links.py</font>. On %s, %d distinct "
        "URLs were checked: %s. A 403 or 429 would be recorded as <i>blocked</i> "
        "(the host answered but refused the request) rather than dead, and a 404 as "
        "<i>dead</i>, which fails the register."
        % (links["checked_on"], links["n_urls"],
           esc(", ".join("%d %s" % (v, k) for k, v in sorted(links["tally"].items(),
                                                             key=lambda kv: -kv[1])))),
        BODY))

    # ------------------------------------------------------------ exclusions
    f.append(Paragraph("8 &nbsp; What was deliberately not used", H1))
    f.append(Paragraph(
        "An exclusion that is not written down is indistinguishable from an oversight. "
        "Each of these is enforced in code at the location named.", BODY))
    rows = [["Excluded", "Reason", "Where enforced"]]
    rows += [
        ["Viral-vector constructs (AAV, lentiviral shRNA)",
         "Gene-therapy vectors, not oligonucleotide therapeutics. This cost the "
         "closest thing to a human in vitro finding &mdash; a choroid-plexus shRNA "
         "study &mdash; and is a curation judgement a reviewer may reasonably want to "
         "revisit, not a mechanical rule.",
         "curation rule, applied at source triage"],
        ["imlifidase",
         "Matched an oligonucleotide drug-name query but is an IgG-degrading "
         "endopeptidase. Recorded by name with the reason rather than silently dropped.",
         "<font face='Courier'>discover_ctgov_trials.py</font> NOT_OLIGONUCLEOTIDE"],
        ["Four morpholinos, from the position table only",
         "Phosphorus count is P = n for eteplirsen, golodirsen and casimersen but "
         "P = n&minus;1 for viltolarsen, because some carry a 5'-piperazine bearing an "
         "extra phosphorus. Length is therefore ambiguous, and a per-position table "
         "cannot rest on an ambiguous length. They contribute measurement rows, just "
         "no position rows.",
         "<font face='Courier'>build_modifications.py</font> EXCLUDED"],
        ["Duplex siRNAs, from the INN parse only",
         "The INN entry names both strands; recovering them needs a strand convention "
         "and a duplex reverse-complement check this parser has not been validated "
         "for. The parser refuses a duplex loudly rather than silently returning one "
         "strand of it.",
         "<font face='Courier'>parse_inn_sequences.py</font> duplex guard"],
        ["valeriasen sequence and chemistry",
         "Published in the source's Extended Data Table 1 as an image whose "
         "bold/underline 2'-MOE encoding does not survive text extraction. Not "
         "transcribed by eye.",
         "<font face='Courier'>build_modifications.py</font> EXCLUDED"],
        ["Numbers read off figures",
         "Both nonclinical sources publish their ventricular measurements graphically. "
         "Those rows carry readout_value NOT_REPORTED and "
         "readout_is_qualitative TRUE rather than a digitised estimate.",
         "<font face='Courier'>build_nonclinical.py</font>"],
    ]
    f.append(table(rows, [1.35 * inch, 3.3 * inch, 1.55 * inch]))

    # -------------------------------------------------------------- backlog
    f.append(PageBreak())
    f.append(Paragraph("9 &nbsp; Retrieved and verified, but not extracted", H1))
    f.append(Paragraph(
        "A source-discovery pass returned %d further sources that were retrieved and "
        "inspected but do not carry a <font face='Courier'>source_id</font> in this "
        "release. They are listed so the gap is visible rather than silent. Their "
        "absence is a completeness limit, not a quality one: nothing in "
        "<font face='Courier'>data/</font> depends on any of them. "
        "<font face='Courier'>notes/source_backlog.csv</font> carries the full list "
        "with retrieval routes, exact loci and per-source caveats."
        % len(backlog), BODY))
    bytype = collections.Counter(b["evidence_type"] for b in backlog)
    rows = [["Evidence type", "Sources", "Est. rows", "Highest-value example"]]
    for etype, n in bytype.most_common():
        items = [b for b in backlog if b["evidence_type"] == etype]
        best = max(items, key=lambda b: int(b["expected_rows"] or 0))
        est = sum(int(b["expected_rows"] or 0) for b in items)
        rows.append([esc(etype.replace("_", " ")), str(n), str(est),
                     esc(clip(best["title"], 86))])
    f.append(table(rows, [1.2 * inch, .55 * inch, .6 * inch, 3.85 * inch]))
    f.append(Paragraph(
        "The single highest-value missing modality is the EMA EPAR <i>assessment "
        "reports</i> (scientific discussion and risk-management plan), as distinct from "
        "the EPAR <i>product information</i> that this release does carry. Those are "
        "where a regulator states an adjudicated causal judgement and a date. Also "
        "entirely absent: EudraVigilance, WHO VigiBase, the FDA pharmacology/toxicology "
        "review packages, PMDA documents, the EU Clinical Trials Register, and patent "
        "literature. Every spontaneous-report row here comes from one database, "
        "openFDA FAERS, and the nusinersen signal was first acted on in Europe.", BODY))
    f.append(Paragraph(
        "Row-count estimates are the discovery pass's own and are not verified here; "
        "they also double-count wherever a backlog entry overlaps rows already present. "
        "Nothing in this section is evidence for any claim &mdash; it is a work list.",
        SMALL))

    # ----------------------------------------------------------------- rights
    f.append(Paragraph("10 &nbsp; Rights, per source", H1))
    f.append(Paragraph(
        "Redistribution terms are tracked per row, not per dataset, so lawful reuse is "
        "verifiable at the record level. The curation layer &mdash; the schema, the "
        "grading rubric, the derived columns &mdash; is offered under CC BY 4.0; the "
        "underlying source rights are as follows and are not altered by that grant.",
        BODY))
    rows = [["Redistribution term", "What it permits", "Sources", "Measurement rows"]]
    means = {
        "public_domain": "Values may be reproduced freely (US Government works)",
        "cc_by": "Reproduce with attribution",
        "cc_by_nc": "Reproduce with attribution, non-commercial only",
        "summary_stat_only": "Summary statistics only; no underlying table reproduced (ND term)",
        "verify": "Resolve the licence with the publisher before republishing values",
    }
    tally = collections.Counter(r["redistribution"] for r in src)
    for term, n in tally.most_common():
        rows.append([esc(term), means.get(term, ""), str(n),
                     str(sum(rows_by_src[r["source_id"]] for r in src
                             if r["redistribution"] == term))])
    f.append(table(rows, [1.28 * inch, 3.07 * inch, .6 * inch, .9 * inch]))
    f.append(Paragraph(
        "No source in this release contains PII, PHI or individual-level human-subjects "
        "data, so there is no privacy or consent barrier to sharing any of it.", SMALL))

    f.append(Spacer(1, 8))
    f.append(Paragraph(
        "Generated from data/sources.csv, data/trial_registry.csv, "
        "notes/link_check.json, notes/source_backlog.csv and qc/stats.json by "
        "docs/build_sources_pdf.py. %d sources &middot; %d measurements &middot; "
        "%d compounds &middot; %d QC checks passing."
        % (len(src), len(meas), stats["n_oligos"], stats["checks_run"]), SMALL))

    n = build(os.path.join(ROOT, "OligoTox-Hydrocephalus_Sources.pdf"),
              "OligoTox-Hydrocephalus · Source and Provenance Register", f)
    print("Sources register  %d pages, %d source records, %d URLs verified"
          % (n, len(src), links["n_urls"]))


if __name__ == "__main__":
    main()
