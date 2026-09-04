#!/usr/bin/env python3
"""Render the Phase 2 markdown deliverables to PDF.

The Challenge requires the narrative, methodology and PADP as PDFs with page
limits, so this exists to produce the actual submission artefacts rather than
leaving them as repository markdown. No pandoc/wkhtmltopdf/LibreOffice is
available in this environment, so it renders directly with ReportLab.

Handles the subset of markdown these documents actually use: ATX headings,
paragraphs, bullet and numbered lists, pipe tables, block quotes, horizontal
rules, fenced code blocks, and inline bold / italic / code. Anything unhandled
degrades to plain text rather than leaking syntax into the page.

Usage:  python scripts/md_to_pdf.py FILE.md [FILE.md ...]
"""
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, KeepTogether,
                                ListFlowable, ListItem, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)

INK = colors.HexColor("#1a1a1a")
ACCENT = colors.HexColor("#1F3864")
MUTED = colors.HexColor("#666666")
RULE = colors.HexColor("#D9D9D9")
BAND = colors.HexColor("#F2F5FA")

SS = getSampleStyleSheet()
def style(name, **kw):
    base = dict(name=name, fontName="Helvetica", fontSize=9.3, leading=13.4,
                textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(**base)

S = {
    "title": style("t", fontName="Helvetica-Bold", fontSize=19, leading=23,
                   textColor=ACCENT, spaceAfter=2),
    "h1": style("h1", fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                textColor=ACCENT, spaceBefore=15, spaceAfter=5),
    "h2": style("h2", fontName="Helvetica-Bold", fontSize=11, leading=14.5,
                textColor=ACCENT, spaceBefore=11, spaceAfter=4),
    "h3": style("h3", fontName="Helvetica-BoldOblique", fontSize=9.8, leading=13,
                spaceBefore=8, spaceAfter=3),
    "body": style("body", spaceAfter=5),
    "quote": style("quote", leftIndent=10, textColor=MUTED,
                   fontName="Helvetica-Oblique", spaceAfter=5),
    "li": style("li", spaceAfter=2.5),
    "cell": style("cell", fontSize=8.1, leading=10.4),
    "cellh": style("cellh", fontSize=8.1, leading=10.4, fontName="Helvetica-Bold",
                   textColor=colors.white),
    "sub": style("sub", fontSize=8.6, leading=11.4, textColor=MUTED, spaceAfter=7),
}


def inline(t):
    """Markdown inline -> ReportLab markup, escaping XML first."""
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8.4">\1</font>', t)
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)          # keep label, drop URL
    return t.replace("—", "&#8212;").replace("→", "&#8594;")


def table_flowable(rows, width):
    head, body = rows[0], rows[1:]
    ncol = len(head)
    data = [[Paragraph(inline(c), S["cellh"]) for c in head]]
    for r in body:
        r = (r + [""] * ncol)[:ncol]
        data.append([Paragraph(inline(c), S["cell"]) for c in r])
    # first column usually carries the label; give it more room
    if ncol > 1:
        first = min(0.34, max(0.16, 1.6 / ncol))
        widths = [width * first] + [width * (1 - first) / (ncol - 1)] * (ncol - 1)
    else:
        widths = [width]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BAND]),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def parse(md, width):
    out, i = [], 0
    lines = md.splitlines()
    bullets, numbers = [], []

    def flush():
        nonlocal bullets, numbers
        for buf, kind, mark in ((bullets, "bullet", "•"), (numbers, "1", None)):
            if buf:
                out.append(ListFlowable(
                    [ListItem(Paragraph(inline(b), S["li"]), leftIndent=13) for b in buf],
                    bulletType=kind, bulletFontSize=7, leftIndent=13,
                    **({"start": "1"} if kind == "1" else {})))
                out.append(Spacer(1, 3))
        bullets, numbers = [], []

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if s.startswith("```"):                                     # fenced code
            flush(); i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            out.append(Preformatted("\n".join(buf),
                                    ParagraphStyle("code", fontName="Courier", fontSize=7.4,
                                                   leading=9.2, textColor=INK)))
            out.append(Spacer(1, 5)); i += 1; continue

        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                raw = lines[i].strip().strip("|")
                if not re.match(r"^[\s:|-]+$", raw):
                    rows.append([c.strip() for c in raw.split("|")])
                i += 1
            if rows:
                out.append(Spacer(1, 3)); out.append(table_flowable(rows, width)); out.append(Spacer(1, 8))
            continue

        if not s:
            flush(); i += 1; continue
        if re.match(r"^(---+|\*\*\*+|___+)$", s):
            flush(); out.append(Spacer(1, 5))
            out.append(HRFlowable(width="100%", thickness=0.5, color=RULE))
            out.append(Spacer(1, 7)); i += 1; continue

        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            flush()
            lvl, txt = len(h.group(1)), h.group(2)
            key = "title" if lvl == 1 else "h1" if lvl == 2 else "h2" if lvl == 3 else "h3"
            out.append(Paragraph(inline(txt), S[key]))
            if lvl == 1:
                out.append(HRFlowable(width="100%", thickness=1.1, color=ACCENT,
                                      spaceBefore=4, spaceAfter=8))
            i += 1; continue

        # List items wrap across source lines, and an inline span may straddle the
        # break (e.g. "**oligo x system /\n dose x readout**"). Consume continuation
        # lines into the same item, or the unmatched marker leaks into the PDF.
        def continuation(j):
            buf = []
            while j < len(lines):
                nxt = lines[j]
                if not nxt.strip():
                    break
                if not re.match(r"^\s{2,}", nxt):          # continuations are indented
                    break
                if re.match(r"^\s*([-*+]\s|\d+[.)]\s|#{1,6}\s|\||>|```)", nxt):
                    break
                buf.append(nxt.strip()); j += 1
            return buf, j

        b = re.match(r"^[-*+]\s+(.*)$", s)
        if b:
            if numbers: flush()
            more, i = continuation(i + 1)
            bullets.append(" ".join([b.group(1)] + more)); continue
        n = re.match(r"^\d+[.)]\s+(.*)$", s)
        if n:
            if bullets: flush()
            more, i = continuation(i + 1)
            numbers.append(" ".join([n.group(1)] + more)); continue

        if s.startswith(">"):
            flush()
            out.append(Paragraph(inline(s.lstrip("> ").strip()), S["quote"]))
            i += 1; continue

        flush()
        para = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|[-*+]\s|\d+[.)]\s|\||>|```|---)", lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        txt = " ".join(para)
        out.append(Paragraph(inline(txt), S["sub"] if txt.startswith("*") and txt.endswith("*") else S["body"]))

    flush()
    return out


def render(src, dst):
    md = open(src, encoding="utf-8").read()
    doc = BaseDocTemplate(dst, pagesize=A4,
                          leftMargin=2.0 * cm, rightMargin=2.0 * cm,
                          topMargin=1.7 * cm, bottomMargin=1.7 * cm,
                          title=os.path.basename(src), author="OligoTox-Kidney")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")

    def furniture(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.3)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 1.05 * cm,
                          "OligoTox-Kidney  |  NIH/NCATS OligoTox Challenge, Phase 2  |  Endpoint: nephrotoxicity")
        canvas.drawRightString(A4[0] - doc.rightMargin, 1.05 * cm, f"Page {d.page}")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(doc.leftMargin, 1.35 * cm, A4[0] - doc.rightMargin, 1.35 * cm)
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=furniture)])
    doc.build(parse(md, doc.width))
    return doc.page


if __name__ == "__main__":
    for src in sys.argv[1:]:
        dst = os.path.splitext(src)[0] + ".pdf"
        pages = render(src, dst)
        print(f"  {os.path.basename(dst):<34}{pages:>3} pages")
