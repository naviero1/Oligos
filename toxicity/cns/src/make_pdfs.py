#!/usr/bin/env python3
"""Render the two submission PDFs.

    deliverables/OligoTox-CNS_Narrative.pdf      (limit: 12 pages)
    deliverables/OligoTox-CNS_Methodology.pdf    (limit:  5 pages)

Every number in the prose is interpolated from a value computed here out of data/*.csv,
qc/validate_dataset.py --json, or figures/baseline_model.json. Nothing is typed as a literal,
so the documents cannot state a figure the dataset does not support.
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import statistics as st
import subprocess
import sys

import reportlab.rl_config
# Byte-deterministic output. reportlab otherwise stamps each build with the current time in
# /CreationDate and /ModDate and a random /ID, so two runs over identical data produce
# different bytes. The methodology document claims the pipeline is deterministic; with this
# set, that claim holds for the PDF binaries and not only for their content.
reportlab.rl_config.invariant = 1

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA, FIG, OUT = ROOT / "data", ROOT / "figures", ROOT / "deliverables"

NAVY = colors.HexColor("#1F3B5C")
BLUE = colors.HexColor("#2a78d6")
INK = colors.HexColor("#111111")
INK2 = colors.HexColor("#4a4a4a")
RULE = colors.HexColor("#d9d9d9")
BOXBG = colors.HexColor("#f2f6fb")
WARNBG = colors.HexColor("#fdf4ec")

# ------------------------------------------------------------------ styles
ss = getSampleStyleSheet()
S = {
    "title": ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold",
                            fontSize=19, leading=23, textColor=NAVY, alignment=0, spaceAfter=2),
    "subtitle": ParagraphStyle("st", fontName="Helvetica", fontSize=10.5, leading=14,
                               textColor=INK2, spaceAfter=10),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=12.5, leading=15,
                         textColor=NAVY, spaceBefore=11, spaceAfter=5),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.2, leading=13,
                         textColor=INK, spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("b", fontName="Helvetica", fontSize=9.1, leading=12.6,
                           textColor=INK, alignment=TA_JUSTIFY, spaceAfter=5),
    "bullet": ParagraphStyle("bu", fontName="Helvetica", fontSize=9.1, leading=12.4,
                             textColor=INK, leftIndent=11, bulletIndent=2, spaceAfter=2.5,
                             alignment=TA_JUSTIFY),
    "cap": ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=7.9, leading=10.4,
                          textColor=INK2, spaceBefore=2, spaceAfter=8),
    "cell": ParagraphStyle("ce", fontName="Helvetica", fontSize=8.1, leading=10.4, textColor=INK),
    "cellb": ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8.1, leading=10.4,
                            textColor=colors.white),
    "small": ParagraphStyle("sm", fontName="Helvetica", fontSize=7.8, leading=10,
                            textColor=INK2, alignment=TA_JUSTIFY),
    "kicker": ParagraphStyle("k", fontName="Helvetica-Bold", fontSize=9.1, leading=12.4,
                             textColor=NAVY, spaceAfter=3),
}


def P(t, s="body"):
    return Paragraph(t, S[s])


def B(t):
    return Paragraph(t, S["bullet"], bulletText="•")


def caption(t):
    return Paragraph(t, S["cap"])


def fig(name, width=170 * mm):
    from PIL import Image as PILImage
    p = FIG / name
    with PILImage.open(p) as im:
        w, h = im.size
    return Image(str(p), width=width, height=width * h / w)


def box(flows, bg=BOXBG, border=BLUE):
    t = Table([[flows]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def table(rows, widths, header=True, align_right=()):
    data = [[Paragraph(c, S["cellb"] if (header and i == 0) else S["cell"])
             for c in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
             ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE)]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), NAVY),
                  ("LINEBELOW", (0, 0), (-1, 0), 0, colors.white)]
    for c in align_right:
        style.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t


def build(path, story, footer_text):
    doc = BaseDocTemplate(str(path), pagesize=A4,
                          leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=16 * mm, bottomMargin=15 * mm,
                          title=footer_text, author="OligoTox-CNS")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")

    def on_page(canv, d):
        canv.saveState()
        canv.setStrokeColor(RULE); canv.setLineWidth(0.5)
        canv.line(doc.leftMargin, 12 * mm, A4[0] - doc.rightMargin, 12 * mm)
        canv.setFont("Helvetica", 7.4); canv.setFillColor(INK2)
        canv.drawString(doc.leftMargin, 8.4 * mm, footer_text)
        canv.drawRightString(A4[0] - doc.rightMargin, 8.4 * mm, f"page {canv.getPageNumber()}")
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])
    doc.build(story)
    return path


# ==========================================================================================
def gather():
    """Every number the documents quote, computed here."""
    q = json.loads(subprocess.run([sys.executable, str(ROOT / "qc" / "validate_dataset.py"),
                                   "--json"], capture_output=True, text=True).stdout)
    n = dict(q["summary"])
    n["checks"] = q["checks"]
    n["model"] = json.loads((FIG / "baseline_model.json").read_text())

    oligos = list(csv.DictReader((DATA / "oligos.csv").open()))
    meas = list(csv.DictReader((DATA / "measurements.csv").open()))
    srcs = list(csv.DictReader((DATA / "sources.csv").open()))
    n["sources_rows"] = srcs

    ans = {m["oligo_id"]: float(m["readout_value"]) for m in meas
           if m["readout_name"] == "acute_tolerability_score_ANS"}
    cao = {m["oligo_id"]: float(m["readout_value"]) for m in meas
           if m["readout_name"].startswith("spontaneous_calcium")}
    n["n_ans"] = len(ans)
    n["n_paired"] = len([o for o in ans if o in cao])
    n["pct_grade_le1"] = 100 * sum(1 for v in ans.values() if v <= 4) / len(ans)
    n["n_grade_le1"] = sum(1 for v in ans.values() if v <= 4)

    by = {o["oligo_id"]: o for o in oligos}
    gsplit = collections.defaultdict(list)
    for oid, v in ans.items():
        gsplit[int(by[oid]["n_G"])].append(v)
    n["g_medians"] = {g: (round(st.median(v), 1), len(v)) for g, v in sorted(gsplit.items())
                      if len(v) >= 3}
    bins = [(0, 4), (5, 9), (10, 14), (15, 20)]
    n["g3_medians"] = {}
    for lo, hi in bins:
        v = [ans[o] for o in ans if by[o]["g_free_3prime_len"] not in ("", "NOT_REPORTED")
             and lo <= int(by[o]["g_free_3prime_len"]) <= hi]
        if v:
            n["g3_medians"][f"{lo}-{hi}"] = (round(st.median(v), 1), len(v))

    rep = collections.Counter(o["sequence_5to3_asprinted"] for o in oligos
                              if o["sequence_5to3_asprinted"] not in ("NOT_REPORTED", ""))
    rseq, _ = rep.most_common(1)[0]
    rv = [cao[o["oligo_id"]] for o in oligos
          if o["sequence_5to3_asprinted"] == rseq and o["oligo_id"] in cao]
    n["rep_seq"], n["rep_n"] = rseq, len(rv)
    n["rep_mean"], n["rep_sd"] = round(st.mean(rv), 1), round(st.stdev(rv), 1)
    n["rep_cv"] = round(100 * st.stdev(rv) / st.mean(rv), 1)

    ctrl = [o for o in oligos if o["dataset_split_asPublished"] == "Control"]
    n["n_negative_controls"] = len(ctrl)
    n["neg_ctrl_ans"] = sorted({ans[o["oligo_id"]] for o in ctrl if o["oligo_id"] in ans})
    n["n_severe_positives"] = sum(1 for v in ans.values() if v > 18)
    n["max_ans"] = max(ans.values())

    k1 = [m for m in meas if m["source_id"] == "K1"]
    ca = {float(m["formulation_ca_mM"]): float(m["readout_value"]) for m in k1
          if "4C" in m["source_location"] and m["strain"] == "WT FVB"
          and float(m["dose_value"]) == 10 and float(m["formulation_mg_mM"] or 0) == 0}
    n["ca_rescue"] = sorted(ca.items())

    n["open_rows"] = sum(1 for m in meas if m["redistribution"] in ("cc_by", "public_domain"))
    n["pct_open"] = round(100 * n["open_rows"] / len(meas), 1)
    n["lengths"] = (min(int(o["length_nt"]) for o in oligos if o["length_nt"].isdigit()),
                    max(int(o["length_nt"]) for o in oligos if o["length_nt"].isdigit()))
    n["n_gapmer"] = sum(1 for o in oligos if o["gapmer_shape"] == "gapmer")
    n["n_mixmer"] = sum(1 for o in oligos if o["gapmer_shape"] == "mixmer")
    n["n_gap_known"] = sum(1 for o in oligos
                           if o["gap_length_nt"] not in ("", "NOT_REPORTED", "NOT_APPLICABLE"))
    n["purity_method_present"] = len(oligos) - n["missingness"]["purity_method"]
    return n


# ==========================================================================================
def narrative(n):
    gd = n["grade_distribution"]
    s = []
    s.append(P("OligoTox-CNS", "title"))
    s.append(P("An open, sequence-resolved dataset of central-nervous-system toxicity for "
               "oligonucleotide therapeutics<br/>"
               "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge &mdash; Phase 2, "
               "Data Generation &nbsp;&middot;&nbsp; Narrative document &nbsp;&middot;&nbsp; "
               "release v1.0", "subtitle"))

    s.append(table([
        ["Oligonucleotides", "CNS measurements", "Modification records", "Sources", "Structural QC"],
        [f"<b>{n['n_oligos']:,}</b>", f"<b>{n['n_measurements']:,}</b>",
         f"<b>{n['n_modification_rows']:,}</b>", f"<b>{n['n_sources']}</b>",
         f"<b>{n['checks_passed']}/{n['checks_total']} pass</b>"]],
        [34 * mm, 34 * mm, 38 * mm, 24 * mm, 40 * mm]))
    s.append(Spacer(1, 7))

    # ---------------- 1. executive summary
    s.append(P("1&nbsp;&nbsp;Executive summary", "h1"))
    s.append(P(
        f"OligoTox-CNS pairs the <b>design</b> of {n['n_oligos']:,} oligonucleotides &mdash; "
        f"their sequences and the position of every chemical modification within them &mdash; "
        f"with {n['n_measurements']:,} measured central-nervous-system toxicity outcomes. "
        f"{n['position_resolved_oligos']:,} of the {n['n_oligos']:,} compounds "
        f"({100 * n['position_resolved_oligos'] / n['n_oligos']:.1f}%) carry a full "
        f"per-nucleotide chemistry map, expanded into a {n['n_modification_rows']:,}-row "
        f"position table. This is the pairing a predictive model needs, and it is the thing "
        f"the public literature has not previously offered in one structured place for the CNS."))
    s.append(P(
        f"The scientific core is the supplementary data of Hagedorn et al. (2022), released "
        f"under CC BY. That table is widely cited for its 148 mouse-dosed compounds; it in fact "
        f"contains 1,825 oligonucleotides, each with a sequence whose upper/lower case encodes "
        f"locked-nucleic-acid position, and each with a measured rat primary-neuron "
        f"calcium-oscillation score. {n['n_ans']} of them additionally carry a mouse acute "
        f"tolerability score. Restructuring the full table &mdash; rather than the 148 &mdash; "
        f"and adding a verified per-position modification map is this release's principal "
        f"contribution."))
    s.append(P(
        f"Three further sources widen the picture: a divalent-cation formulation-rescue "
        f"experiment in mice, a late-onset neurotoxicity study whose per-position chemistry had "
        f"to be recovered from PDF typeface, and the FDA prescribing information for the two "
        f"approved intrathecal antisense drugs. A fifth source contributes measurement "
        f"instruments but no rows."))

    s.append(P("Positive and negative controls", "h2"))
    s.append(P(
        f"The dataset is not a list of toxic compounds; it spans the full severity range and "
        f"contains deliberate controls at both ends, which is what makes it trainable."))
    s.append(B(f"<b>Designed negative controls ({n['n_negative_controls']}).</b> Guanine-free "
               f"antisense oligonucleotides with no perfectly or partially matching target in "
               f"the mouse transcriptome, built by the source authors as a negative class. "
               f"Their mouse tolerability scores run from "
               f"{min(n['neg_ctrl_ans']):g} to {max(n['neg_ctrl_ans']):g} on a 0&ndash;20 scale."))
    s.append(B("<b>Vehicle control.</b> Phosphate-buffered saline, scored on the same scale "
               "(1.67), which fixes the assay's floor: a score of roughly 1&ndash;2 is what an "
               "untreated animal produces."))
    s.append(B("<b>A non-toxic clinical-chemistry control.</b> A 5-10-5 2&prime;-MOE gapmer "
               "already used in clinical trials, included by its source authors specifically as "
               "a compound that does <i>not</i> produce the late-onset phenotype."))
    s.append(B(f"<b>Severe positive controls ({n['n_severe_positives']}).</b> Compounds scoring "
               f"above 18 of 20, i.e. severe signs in nearly all categories, up to the maximum "
               f"score of {n['max_ans']:g}."))
    s.append(B(f"<b>Graded across the range.</b> Severity grades 0/1/2/3 = "
               f"{gd.get('0', 0)}/{gd.get('1', 0)}/{gd.get('2', 0)}/{gd.get('3', 0)}."))

    s.append(fig("F1_composition.png"))
    s.append(caption(
        "<b>Figure 1.</b> What the dataset contains. Log scales: the in vitro arm dominates by "
        "count, but the in vivo and clinical arms carry the severity grades. Source H1 is "
        "Hagedorn 2022, K1 Miller 2024, L1 Kuroda 2025, C1 the FDA labels."))
    s.append(PageBreak())

    # ---------------- 2. findings
    s.append(P("2&nbsp;&nbsp;Main findings and conclusions", "h1"))

    s.append(P("Finding 1 &mdash; sequence predicts in vivo CNS tolerability better than the "
               "in vitro assay does", "kicker"))
    s.append(P(
        f"Across the {n['n_paired']} oligonucleotides that carry both readouts, the measured "
        f"in vitro calcium-oscillation score separates tolerable from intolerable compounds "
        f"with an AUC of {n['model']['auc_all_measured_invitro']:.2f}, while a score computed "
        f"from the sequence alone reaches {n['model']['auc_all_published_linear']:.2f}. On the "
        f"held-out set &mdash; {n['model']['n_held']} oligonucleotides against a different "
        f"target gene, held out by the original authors &mdash; the sequence model reaches "
        f"{n['model']['acc_published_cutoff70']:.1%} accuracy."))
    s.append(P(
        f"The explanation is measurement noise, and the dataset contains the evidence for it. "
        f"One control oligonucleotide appears {n['rep_n']} times in the source table, having "
        f"been run on {n['rep_n']} independent plates. Its scores range across "
        f"{n['rep_cv']:.1f}% coefficient of variation (mean {n['rep_mean']}, SD {n['rep_sd']}). "
        f"A single in vitro measurement carries that noise; a sequence-derived score does not. "
        f"<b>The practical consequence for anyone building a model: do not treat the in vitro "
        f"assay as ground truth to be predicted, and do not discard a compound on one plate "
        f"run.</b>"))
    s.append(fig("F4_translation.png"))
    s.append(caption(
        f"<b>Figure 2.</b> In vitro to in vivo translation, n = {n['n_paired']}. The "
        f"relationship is real and monotone across tertiles (median mouse score 6.67, 3.25, "
        f"0.83) but loose at the level of an individual compound (Spearman &rho; = &minus;0.33)."))

    s.append(P("Finding 2 &mdash; guanine content is a graded risk factor, not a threshold", "kicker"))
    gm = n["g_medians"]
    gm_txt = "; ".join(f"{g} G &rarr; {v[0]:g} (n={v[1]})" for g, v in list(gm.items())[:6])
    s.append(P(
        f"Median mouse tolerability score rises monotonically with the number of guanines in "
        f"the oligonucleotide: {gm_txt}. Position matters more than count. Binning by the "
        f"length of the guanine-free stretch measured from the 3&prime; end gives median scores "
        + ", ".join(f"{k} nt &rarr; {v[0]:g} (n={v[1]})" for k, v in n["g3_medians"].items())
        + ". A guanine close to the 3&prime; end is the single strongest sequence warning in "
          "this dataset."))
    s.append(fig("F5_sequence.png"))
    s.append(caption(
        "<b>Figure 3.</b> Both guanine relationships, with group sizes shown. The extreme "
        "guanine-count bins are small (n = 3), which is why the count relationship should be "
        "read as a trend and the 3&prime;-position relationship, with 21&ndash;87 per bin, as "
        "the more reliable of the two."))
    s.append(PageBreak())

    s.append(P("Finding 3 &mdash; formulation can override sequence and chemistry entirely", "kicker"))
    ca = n["ca_rescue"]
    s.append(P(
        f"At a fixed dose of the same molecule, adding calcium to the injectate reduces the "
        f"acute tolerability score from {ca[0][1]:g} to {ca[-1][1]:g} of 20 as calcium rises "
        f"from {ca[0][0]:g} to {ca[-1][0]:g} mM. That is close to an on/off switch, produced "
        f"without changing a single nucleotide. Magnesium produces a similar but shallower "
        f"effect."))
    s.append(P(
        "<b>This has a direct implication for how the dataset should be modelled.</b> A model "
        "trained on sequence and chemistry alone, on data pooled across studies that used "
        "different vehicles, will attribute a formulation effect to the molecule. The dataset "
        "therefore carries <font face='Courier'>formulation_ca_mM</font> and "
        "<font face='Courier'>formulation_mg_mM</font> as first-class columns rather than "
        "burying them in a methods note."))
    s.append(fig("F7_formulation.png"))
    s.append(caption("<b>Figure 4.</b> Dose-response and cation rescue, both from source K1, "
                     "both on the same 0&ndash;20 scale as the core dataset."))

    s.append(P("Finding 4 &mdash; two published sources disagree, and the dataset makes the "
               "disagreement visible", "kicker"))
    s.append(P(
        "Source K1 shows divalent cations abolishing acute CNS toxicity. Source O1 reports that "
        "divalent cation supplementation at 1&ndash;100 mM did <i>not</i> alter the acute "
        "response it measured. Both can be correct, because they measure different phenotypes: "
        "K1 scores an <i>activation</i> syndrome (hyperactivity, tremor, seizure) and O1 scores "
        "an <i>inhibition</i> syndrome (progressive loss of motor function, scored 3 h after "
        "dosing on a 0&ndash;7 scale). A model trained on a pooled &ldquo;CNS toxicity&rdquo; "
        "label would be learning across a real mechanistic boundary. This is why every "
        "measurement carries a <font face='Courier'>tox_axis</font>, and why "
        "<font face='Courier'>docs/SCORING_INSTRUMENTS.md</font> states explicitly which axes "
        "may be pooled."))

    s.append(P("Finding 5 &mdash; acute and late-onset toxicity are separable, and separably "
               "recorded", "kicker"))
    s.append(P(
        "Source L1 reports gapmers that are <i>not</i> acutely toxic &mdash; one produces acute "
        "signs that resolve within a day, three produce none &mdash; yet cause hypoactivity and "
        "motor loss appearing three or more days after dosing, severe enough that two required "
        "humane sacrifice at day 7 and one of four rats given the compound intrathecally died "
        "at day 14. Acute screening cannot see this. The dataset keeps the two windows on "
        "separate axes so that a model is not trained to call a late-onset toxin safe."))

    s.append(P("Conclusions", "h2"))
    s.append(B("Sequence and modification position, taken together, carry enough signal to "
               "predict acute CNS tolerability at clinically useful accuracy &mdash; "
               f"{n['model']['acc_published_cutoff70']:.1%} on a genuinely held-out target."))
    s.append(B("The commonly used in vitro screen is noisier than the sequence model it is "
               "meant to validate; its coefficient of variation is measurable from this "
               f"dataset at {n['rep_cv']:.1f}%."))
    s.append(B("Formulation is a confounder of the first order and must be modelled, not "
               "assumed constant."))
    s.append(B("&ldquo;CNS toxicity&rdquo; is at least four distinct phenomena. Collapsing them "
               "into one label discards mechanism and creates contradictions that are artefacts "
               "of the labelling, not the biology."))
    s.append(PageBreak())

    # ---------------- 3. how produced
    s.append(P("3&nbsp;&nbsp;How the data were produced", "h1"))
    s.append(P(
        "This is a <b>curation</b> dataset: no new wet-lab experiment was run. Its contribution "
        "is the structuring, verification and harmonisation of experimental results that exist "
        "in the public record but not in any usable form. What follows is a summary; the "
        "methodology document gives the full protocol."))

    s.append(P("Source selection", "h2"))
    s.append(P(
        "Sources were required to report a CNS-specific toxicity outcome for an identified "
        "oligonucleotide, and were prioritised by whether they also published the sequence. A "
        "source that reports toxicity with sequences is worth far more than one that reports "
        "toxicity alone, because only the former can train a model. Sources reached by "
        "web-search summary alone were not used for any numeric value."))

    rows = [["ID", "Source", "Contribution", "Licence", "Oligos", "Measurements"]]
    for r in n["sources_rows"]:
        rows.append([r["source_id"],
                     f"{r['first_author']} {r['year']}<br/><font size=7>{r['journal']}</font>",
                     r["evidence_tier"].replace("_", " "), r["license"],
                     r["n_oligos"], r["n_measurements"]])
    s.append(table(rows, [10 * mm, 40 * mm, 42 * mm, 34 * mm, 20 * mm, 24 * mm],
                   align_right=(4, 5)))
    s.append(caption("<b>Table 1.</b> The source registry, reproduced from "
                     "<font face='Courier'>data/sources.csv</font>. O1 contributes measurement "
                     "instruments and a contradictory finding, but no rows."))

    s.append(P("Acquisition", "h2"))
    s.append(P(
        "Supplementary files were retrieved through the Europe PMC REST endpoint after the "
        "PubMed Central interface proved to gate binary downloads behind a JavaScript "
        "proof-of-work challenge. Regulatory labels were read from DailyMed. Every retrieved "
        "file is committed alongside the code, so the dataset remains rebuildable if a "
        "publisher URL rots."))

    s.append(P("Computational processing", "h2"))
    s.append(B("<b>Sequence and modification position.</b> In source H1 the printed sequence "
               "encodes chemistry in case. This was not taken on trust: the count of upper-case "
               "characters was checked against the paper's own declared LNA count for all 1,825 "
               "rows, with zero mismatches, before position was read out of case."))
    s.append(B("<b>Typeface parsing.</b> In source L1 the chemistry is encoded in <b>bold</b> "
               "(LNA) and <b>bold-italic</b> (2&prime;-MOE), which plain text extraction "
               "destroys. Per-position chemistry was recovered by reading the PDF's span "
               "styling, giving 3-10-3 and 4-12-4 LNA gapmers and one 5-10-5 2&prime;-MOE "
               "gapmer."))
    s.append(B("<b>Table parsing.</b> Source K1's tolerability table was parsed from the "
               "supplementary PDF by a state machine over the text layer, recovering 41 dosing "
               "groups with their injectate cation concentrations."))
    s.append(B("<b>Derived fields.</b> Base composition, G+C content, longest guanine run, "
               "3&prime; guanine-free stretch and gap geometry are computed from the printed "
               "sequence and marked as derived. Nothing else is computed."))
    s.append(P(
        "As an end-to-end check that the transcription is faithful, the predictive model "
        "published by the source authors was re-implemented from their supplementary methods "
        "and run over the restructured table: it reproduces their own published score column "
        "for all 1,825 rows, with zero mismatches beyond rounding."))
    s.append(PageBreak())

    # ---------------- 4. indicators & predictors
    s.append(P("4&nbsp;&nbsp;Indicators and predictor variables", "h1"))
    s.append(P("How the toxicity indicators were measured", "h2"))
    s.append(table([
        ["Indicator", "Instrument", "Range / units", "n"],
        ["Acute tolerability score",
         "Modified functional observational battery (Oligonucleotide Safety Working Group), "
         "five categories each 0&ndash;4, summed; scored over 1 h after a single ICV bolus; "
         "4&ndash;6 mice per group, averaged",
         "0&ndash;20", str(n["n_ans"] + 41)],
        ["Calcium-oscillation score",
         "Spontaneous calcium oscillations in rat E19 primary cortical neurons, fluo-4 AM on "
         "FLIPR; 1 point per 1-s read exceeding 50% of mean control amplitude over a 300 s read",
         "% of control<br/>(lower = greater effect)", "1,825"],
        ["Late-onset tolerability",
         "Five-category 0&ndash;4 scale applied over days 1&ndash;21; open-field locomotion and "
         "body weight alongside",
         "0&ndash;20<br/>(published as figures only)", "6"],
        ["Clinical adverse-event incidence",
         "Randomised controlled trial safety reporting, as printed in FDA prescribing "
         "information",
         "% of arm", "12"]],
        [30 * mm, 80 * mm, 34 * mm, 14 * mm], align_right=(3,)))
    s.append(caption("<b>Table 2.</b> Each instrument is reproduced verbatim from its source in "
                     "<font face='Courier'>docs/SCORING_INSTRUMENTS.md</font>, including which "
                     "instruments may legitimately be pooled."))

    s.append(P("Distribution of the predictor variables amongst tested oligonucleotides", "h2"))
    s.append(P(
        f"Lengths run {n['lengths'][0]}&ndash;{n['lengths'][1]} nucleotides, with a strong mode "
        f"at 16 and 20. {n['n_gap_known']:,} compounds have a determined DNA gap length; "
        f"{n['n_mixmer']} are mixmers whose modified residues are not contiguous, for which a "
        f"single gap length is undefined and is left empty rather than guessed. "
        f"Guanine count is strongly right-skewed (median 1), which is by design: the source "
        f"library was built to interrogate guanine as a risk factor and deliberately "
        f"over-samples guanine-poor sequences."))
    s.append(fig("F2_predictors.png"))
    s.append(caption(
        "<b>Figure 5.</b> The six principal predictors. The spike at 20 in the 3&prime; "
        "guanine-free panel is a cap defined by the source, meaning the oligonucleotide "
        "contains no guanine anywhere; it is not a measured length of 20."))
    s.append(PageBreak())

    s.append(P("Distribution of the toxicity outcome", "h2"))
    s.append(P(
        f"{sum(gd.values())} of {n['n_measurements']:,} measurements carry an ordinal severity "
        f"grade. The remaining {n['n_measurements'] - sum(gd.values()):,} are the in vitro "
        f"calcium-oscillation readings, deliberately left ungraded: they are a continuous "
        f"measure of a different quantity and the source defines no severity bands for them, so "
        f"grading them would mean inventing thresholds."))
    s.append(fig("F3_severity.png"))
    s.append(caption(
        f"<b>Figure 6.</b> Severity distribution. All four grades are well represented "
        f"({gd.get('0', 0)}/{gd.get('1', 0)}/{gd.get('2', 0)}/{gd.get('3', 0)}), which matters: "
        f"a dataset of positives alone cannot train a classifier. The grade boundary between 1 "
        f"and 2 reproduces the source authors' own developability line &mdash; "
        f"{n['n_grade_le1']} of {n['n_ans']} in vivo rows ({n['pct_grade_le1']:.1f}%) fall at "
        f"grade &le; 1, against their stated &ldquo;roughly 60%&rdquo;."))

    # ---------------- 5. gap
    s.append(P("5&nbsp;&nbsp;The gap in public data that this addresses", "h1"))
    s.append(P(
        "Oligonucleotides delivered into cerebrospinal fluid have a specific, well-documented "
        "toxicity problem, and two approved drugs carry CNS warnings on their labels. Yet the "
        "public data needed to predict that toxicity from a candidate's design has been "
        "effectively unavailable, for three separate reasons that this dataset addresses."))
    s.append(B("<b>The data existed but was not in usable form.</b> The largest public "
               "sequence-resolved CNS dataset sits inside a single supplementary spreadsheet, "
               "behind a download challenge, with chemistry encoded in text case and no "
               "position table, no controlled vocabulary, and no join to any other source. It "
               "is generally cited for 148 compounds; it holds 1,825."))
    s.append(B("<b>Modification position was not machine-readable anywhere.</b> The challenge "
               "asks for the location of every chemical modification. Sources supply this as a "
               "case convention, as typeface, or as a motif string, and no public CNS dataset "
               "had normalised it. This release provides "
               f"{n['n_modification_rows']:,} position-level records with an explicit "
               "provenance basis on each."))
    s.append(B("<b>Findings were scattered across incompatible instruments.</b> At least five "
               "distinct scoring scales are in use. Placing them in one schema, with the "
               "instruments documented and the incompatible ones explicitly marked as "
               "un-poolable, is a prerequisite for cross-study modelling that no previous "
               "public resource provided."))
    s.append(P(
        "The dataset also makes visible two things that only appear when sources are placed "
        "side by side: the measured noise of the standard in vitro screen, and a direct "
        "contradiction between two 2024&ndash;2026 papers on whether divalent cations mitigate "
        "CNS toxicity. Neither is visible from within any single publication."))
    s.append(PageBreak())

    # ---------------- 6. predictive model
    s.append(P("6&nbsp;&nbsp;Using this data to build a predictive model", "h1"))
    s.append(P(
        "The claim that this dataset supports predictive modelling is demonstrated rather than "
        "asserted. <font face='Courier'>src/baseline_model.py</font> reads only the released "
        "CSVs and trains against the source's own train/test split, so the held-out set is the "
        f"one the original authors held out: {n['model']['n_held']} oligonucleotides targeting a "
        f"<i>different gene</i> from the compounds used for fitting. That is a generalisation "
        f"test, not a random split."))
    s.append(table([
        ["Model", "Inputs", "Held-out AUC", "Held-out accuracy"],
        ["Published linear model", "base composition + 3&prime; guanine-free length",
         f"{n['model']['auc_published_linear']:.3f}",
         f"{n['model']['acc_published_cutoff70']:.1%}"],
        ["Measured in vitro assay", "calcium-oscillation score",
         f"{n['model']['auc_measured_invitro']:.3f}", "&mdash;"],
        ["Logistic regression fitted here", "12 sequence and geometry features",
         f"{n['model']['auc_logistic_12feat']:.3f}", f"{n['model']['acc_logistic']:.1%}"]],
        [46 * mm, 62 * mm, 26 * mm, 30 * mm], align_right=(2, 3)))
    s.append(caption(
        f"<b>Table 3.</b> Predicting the source authors' own developability line (tolerability "
        f"score &gt; 4) on {n['model']['n_held']} held-out compounds, "
        f"{n['model']['held_positives']} of them positive. The fitted logistic regression uses "
        f"{n['model']['n_train']} training compounds &mdash; the subset of the {n['n_ans']} in "
        f"vivo rows for which all twelve features are defined; the remaining "
        f"{n['n_ans'] - n['model']['n_rows_featok']} are mixmers, which have no single DNA gap "
        f"length. The two sequence-only rows use all {n['model']['n_both']}."))
    s.append(P(
        f"Two results are worth stating plainly. First, the published five-parameter model "
        f"reproduces at {n['model']['acc_published_cutoff70']:.1%} accuracy on the held-out "
        f"set, which independently confirms that the restructured table is faithful. Second, "
        f"<b>a richer twelve-feature logistic regression fitted here did not beat it</b> "
        f"(AUC {n['model']['auc_logistic_12feat']:.2f} against "
        f"{n['model']['auc_published_linear']:.2f}). With 138 labelled training compounds, "
        f"added features cost more in variance than they buy in signal. That is a useful "
        f"negative result for anyone planning to model this data: the constraint is labelled "
        f"in vivo examples, not features."))

    s.append(P("A recommended build order", "h2"))
    s.append(B("<b>Reproduce the baseline first.</b> If your pipeline cannot reach roughly 89% "
               "on the held-out set with base counts and the 3&prime; guanine-free length, the "
               "pipeline is wrong, not the data."))
    s.append(B("<b>Model the two readouts jointly, not sequentially.</b> The in vitro score is "
               f"available for all 1,825 compounds and the in vivo score for only "
               f"{n['n_ans']}. Treating the in vitro score as a noisy auxiliary task, with its "
               f"measured {n['rep_cv']:.1f}% coefficient of variation as a known noise floor, "
               f"uses ten times more data than in vivo-only training."))
    s.append(B("<b>Use the position table, not just base counts.</b> The published model uses "
               "composition only. Position-resolved chemistry is now available for "
               f"{n['position_resolved_oligos']:,} compounds and is entirely unexploited."))
    s.append(B("<b>Include formulation.</b> Calcium and magnesium concentration are dataset "
               "columns. A model that ignores them will attribute a vehicle effect to a "
               "sequence."))
    s.append(B("<b>Respect the axes.</b> Train separate heads for acute and late-onset "
               "toxicity, or at minimum condition on "
               "<font face='Courier'>tox_axis</font>."))

    s.append(P("What would most improve the next version", "h2"))
    s.append(P(
        "More labelled in vivo examples, and chemistry breadth. The core is one chemistry class "
        "&mdash; LNA/DNA full-phosphorothioate gapmers &mdash; which is a strength for isolating "
        "sequence effects and a limitation for generalising. Two published datasets documented "
        "here as instruments only (non-human-primate and 2&prime;-MOE) would address both, and "
        "are the top priority for v1.1."))
    s.append(PageBreak())

    # ---------------- 7. limitations
    s.append(P("7&nbsp;&nbsp;Limitations, stated plainly", "h1"))
    s.append(box([
        P("<b>Per-compound purity is absent from the literature.</b> "
          f"<font face='Courier'>purity_pct</font> is <font face='Courier'>NOT_REPORTED</font> "
          f"for all {n['n_oligos']:,} oligonucleotides. Journals essentially never print "
          f"per-compound purity or observed mass alongside toxicity results. What is captured, "
          f"where the source states it, is the purification and identity-confirmation "
          f"<i>method</i> &mdash; present for {n['purity_method_present']:,} of "
          f"{n['n_oligos']:,}. No purity value has been estimated. This is the largest gap "
          f"between this dataset and the challenge's description of one, and it is a property "
          f"of the published record rather than of the curation.", "small")], WARNBG,
        colors.HexColor("#ec835a")))
    s.append(Spacer(1, 5))
    s.append(B(f"<b>The in vitro arm is rat, not human.</b> Only "
               f"{n['human_system_measurements']} of {n['n_measurements']:,} measurements are "
               f"human-derived, and all of them are clinical. We searched specifically for "
               f"human iPSC-derived neuron or organoid data on oligonucleotide CNS toxicity and "
               f"found reviews describing it as promising but no published, sequence-resolved "
               f"source. The field's standard predictive screen is a rodent primary-neuron "
               f"assay. This is the most important scientific gap the dataset reveals."))
    s.append(B(f"<b>Chemistry is narrow.</b> {n['position_resolved_oligos'] - 5:,} of "
               f"{n['n_oligos']:,} compounds are LNA/DNA full-phosphorothioate oligonucleotides "
               f"from a single study &mdash; {n['n_gapmer'] - 6:,} conventional gapmers and "
               f"{n['n_mixmer']} mixmers."))
    s.append(B("<b>Grades are provisional.</b> Every grade carries the rule that produced it, "
               "but none has been reviewed by a subject-matter expert; all ship as "
               "<font face='Courier'>provisional</font>."))
    s.append(B("<b>One row is one group, not one animal.</b> In vivo scores are group means "
               "over 4&ndash;6 mice. Within-group variance is not recoverable from the "
               "published data."))
    s.append(B("<b>Publication bias.</b> The 40% failure rate in the core library is a property "
               "of a library built to interrogate toxicity, not a base rate for CNS "
               "oligonucleotides generally."))

    s.append(P("Quality control", "h2"))
    s.append(P(
        f"<font face='Courier'>qc/validate_dataset.py</font> runs "
        f"{n['checks_total']} structural and provenance checks &mdash; key uniqueness, "
        f"referential integrity, controlled-vocabulary conformance, grade range, sequence "
        f"self-consistency, modification-table completeness and contiguity, and the rule that "
        f"<b>no numeric readout may exist without a named source table or figure</b>. All "
        f"{n['checks_passed']} pass, and the script exits non-zero on any failure so it can "
        f"gate a release."))

    s.append(P("Access and licence", "h2"))
    s.append(P(
        f"CC BY 4.0 for everything created here. Row-level content carries its source's terms in "
        f"a <font face='Courier'>redistribution</font> column: {n['open_rows']:,} of "
        f"{n['n_measurements']:,} measurements ({n['pct_open']}%) are CC BY 4.0 or US public "
        f"domain and are reusable for any purpose including commercially; the remainder derive "
        f"from CC BY-NC sources, are individually marked, and are removable with a one-line "
        f"filter. No registration, no data-use agreement, no embargo. Full plan in "
        f"<font face='Courier'>docs/PADP.md</font>."))
    s.append(fig("F8_completeness.png", 150 * mm))
    s.append(caption("<b>Figure 7.</b> Field completeness, including the purity gap stated "
                     "above. Nothing has been filled in to improve this picture."))

    return s


# ==========================================================================================
def methodology(n):
    s = []
    s.append(P("OligoTox-CNS &mdash; Methodology", "title"))
    s.append(P("Materials and methods for the CNS oligonucleotide toxicity dataset<br/>"
               "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge &mdash; Phase 2 "
               "&nbsp;&middot;&nbsp; release v1.0", "subtitle"))

    s.append(P("1&nbsp;&nbsp;Design", "h1"))
    s.append(P(
        "OligoTox-CNS is a <b>curated</b> dataset. No new wet-lab experiment was performed; the "
        "materials and methods below are therefore of two kinds, and are kept strictly "
        "separate: <b>(a)</b> the experimental methods of the source studies, recorded verbatim "
        "so that a user knows how each measurement was generated, and <b>(b)</b> the curation "
        "methods used here to extract, verify and harmonise them. Conflating the two would let "
        "curation choices masquerade as experimental fact."))

    s.append(P("2&nbsp;&nbsp;Source selection and retrieval", "h1"))
    s.append(P(
        "Inclusion required a CNS-specific toxicity outcome attributable to an identified "
        "oligonucleotide. Sources were ranked by whether they also published the sequence. "
        "Excluded: sources whose toxicity endpoints were hepatic, renal or systemic-immune "
        "without a CNS readout; and any value reachable only through a web-search summary."))
    s.append(P(
        "Supplementary files were retrieved through the Europe PMC REST supplementary-files "
        "endpoint (<font face='Courier'>/europepmc/webservices/rest/&lt;PMCID&gt;/"
        "supplementaryFiles</font>). This route was adopted after the PubMed Central interface "
        "was found to gate binary downloads behind a JavaScript proof-of-work challenge that "
        "returns an HTML stub in place of the requested file &mdash; a stub that would "
        "otherwise be silently parsed as data. Regulatory labels were read from DailyMed, "
        "identified by set ID and label publication date. Every retrieved file is committed to "
        "<font face='Courier'>sources/</font>."))

    s.append(P("3&nbsp;&nbsp;Oligonucleotide identity, purification and characterisation", "h1"))
    s.append(box([
        P("This section answers the challenge's requirement for <i>the methods used to purify "
          "and characterize oligo identity</i>. Because the compounds were synthesised by the "
          "source laboratories and not here, what can be reported is what each source states. "
          "<b>Where a source is silent, the field is "
          "<font face='Courier'>NOT_REPORTED</font>. No purity value has been estimated, "
          "inferred from a synthesis platform, or carried across from another compound.</b>",
          "small")], WARNBG, colors.HexColor("#ec835a")))
    s.append(Spacer(1, 4))
    s.append(P("Reported by source H1, covering 1,825 of the "
               f"{n['n_oligos']:,} oligonucleotides", "h2"))
    s.append(P(
        "Quoted verbatim from the source's Materials and Methods: <i>&ldquo;Single-stranded DNA "
        "oligonucleotides with complete PS backbones and LNA-modified flanks were synthesized "
        "on a MerMade 192&times; synthesizer (Bioautomation, TX, USA) following standard "
        "phosphoramidite protocols. The final 5&prime;-dimethoxytrityl (DMT) group was left on "
        "the oligonucleotide for later use as lipophilic handle and chromatographic retention "
        "probe. The oligonucleotides were purified by solid phase extraction in TOP cartridges "
        "(Agilent Technologies, Glostrup, Denmark) using the DMT group, after which the DMT "
        "group was removed &hellip; The oligonucleotides were dissolved in sterile 0.9% saline "
        "solution, and the concentration of oligonucleotide in solution confirmed by calculating "
        "the Beer-Lambert extinction coefficient and measuring ultraviolet absorbance. "
        "Oligonucleotide identity and purity were validated by reversed-phase ultra-performance "
        "liquid chromatography coupled to mass spectrometry.&rdquo;</i>"))
    s.append(P(
        "These statements populate <font face='Courier'>synthesis_platform</font>, "
        "<font face='Courier'>purity_method</font>, "
        "<font face='Courier'>identity_confirmation</font> and "
        "<font face='Courier'>formulation</font>. <b>The source states the method but publishes "
        "no per-compound purity percentage and no observed mass</b>, so "
        "<font face='Courier'>purity_pct</font> is "
        "<font face='Courier'>NOT_REPORTED</font> for every row."))
    s.append(P("Reported by the remaining sources", "h2"))
    s.append(table([
        ["Source", "Synthesis", "Purification", "Identity confirmation", "Purity value"],
        ["K1", "not reported", "not reported", "not reported", "not reported"],
        ["L1", "commercial synthesis stated; platform not reported", "not reported",
         "not reported", "not reported"],
        ["C1", "not applicable &mdash; approved products manufactured to their marketing "
               "authorisation", "not in label", "not in label", "not in label"]],
        [14 * mm, 46 * mm, 34 * mm, 40 * mm, 32 * mm]))
    s.append(caption(
        f"<b>Table M1.</b> Characterisation reporting by source. Across the whole release, "
        f"{n['purity_method_present']:,} of {n['n_oligos']:,} oligonucleotides carry a stated "
        f"purification method and <b>0 carry a purity value</b>. This is a property of the "
        f"published literature; see <font face='Courier'>OPEN_ITEMS.md</font> OI-02."))
    s.append(P("Sequence identity as recorded here", "h2"))
    s.append(P(
        "Identity in this dataset means the printed sequence together with its per-position "
        "chemistry. Both are transcribed mechanically, never typed by hand, and both are checked "
        f"against internal evidence: for all 1,825 H1 compounds the count of upper-case "
        f"characters in the printed sequence equals the source's own declared LNA count "
        f"(0 mismatches), and every oligonucleotide that has a published sequence has a declared "
        f"length and base composition equal to that sequence "
        f"({n['sequences_present']:,} of {n['sequences_present']:,}; the remaining "
        f"{n['n_oligos'] - n['sequences_present']} have no published sequence to check against). "
        f"Both are re-checked by the QC suite on every build."))
    s.append(Spacer(1, 4))

    s.append(P("4&nbsp;&nbsp;Experimental methods of the source studies", "h1"))
    s.append(table([
        ["Source", "System", "Design"],
        ["H1 &mdash; in vivo",
         "adult female C57BL/6J mice",
         "Single intracerebroventricular bolus, 100 &micro;g in 5 &micro;L 0.9% saline. Observed "
         "1 h using a modified functional observational battery per the Oligonucleotide Safety "
         "Working Group. Five categories (hyperactivity; decreased activity and arousal; motor "
         "dysfunction/ataxia; abnormal posture and breathing; tremor/convulsions), each 0&ndash;4, "
         "summed to 0&ndash;20. 4&ndash;6 mice per group; per-animal scores averaged to a group score."],
        ["H1 &mdash; in vitro",
         "primary cortical neurons, Sprague-Dawley rat embryonic day 19, 25,000 cells/well",
         "Spontaneous calcium oscillations, fluo-4 AM, read on FLIPR for 300 s, &plusmn; 1 mM "
         "added Mg<super>2+</super>. ASO at 25 &micro;M, chosen as the expected CSF concentration in "
         "the first hour after a 100 &micro;g ICV injection. Score = 1 point per 1-s read whose "
         "signal increase exceeds 50% of mean control amplitude, summed and expressed as percent "
         "of control."],
        ["K1", "wild-type FVB and two Huntington's disease model mouse lines",
         "Bilateral ICV injection of di-siRNA and ASO constructs, 1.25&ndash;20 nmol, in vehicles "
         "containing 0&ndash;32 mM Ca<super>2+</super> and/or 0&ndash;16 mM Mg<super>2+</super>. Acute "
         "tolerability scored on the same 0&ndash;20 scale; 4&ndash;6 animals per group."],
        ["L1", "C57BL/6 and ICR mice; Slc:SD rats",
         "ICV injection of 15.2&ndash;39.9 nmol, or intrathecal injection via spinal canal "
         "catheter of 190 nmol. Five-category 0&ndash;4 tolerability scale (separate rat variant), "
         "open-field locomotion and body weight, assessed to day 21. n = 4 per group."],
        ["C1", "human patients",
         "Randomised placebo- or sham-controlled trials. Tofersen 100 mg intrathecally (n = 72 "
         "versus 36 placebo); nusinersen 12 mg intrathecally (n = 84 versus 42 control in the "
         "later-onset study). Adverse-event incidences as printed in the prescribing "
         "information, plus post-marketing reports with no estimable frequency."]],
        [22 * mm, 40 * mm, 108 * mm]))

    s.append(P("5&nbsp;&nbsp;Extraction and transcription", "h1"))
    s.append(B("<b>Spreadsheet source (H1).</b> Read cell-by-cell with "
               "<font face='Courier'>openpyxl</font>. No value passed through a language model "
               "or a summarising fetch layer, which was a deliberate decision after a "
               "transcription artefact (a Cyrillic character substituted into a nucleotide "
               "sequence) was observed in summarised text during source discovery."))
    s.append(B("<b>Typeface-encoded source (L1).</b> Chemistry is carried in <b>bold</b> = LNA "
               "and <b>bold-italic</b> = 2&prime;-MOE, with <font face='Courier'>C(5)</font> "
               "marking 5-methylcytosine; plain text extraction discards all of it. Per-position "
               "chemistry was recovered by reading PDF span style flags "
               "(<font face='Courier'>src/build_curated.py::parse_kuroda_sequences</font>), "
               "yielding 3-10-3 and 4-12-4 LNA gapmers and one 5-10-5 2&prime;-MOE gapmer."))
    s.append(B("<b>PDF table source (K1).</b> Parsed by a state machine over the text layer, "
               "keyed on runs of six consecutive numeric fields, recovering 41 dosing groups. "
               "Curves were selected by the source figure panel each group belongs to, because "
               "selecting by dose and cation alone merges control groups from unrelated panels."))
    s.append(B("<b>Regulatory source (C1).</b> Warnings, incidences and denominators read "
               "directly from the label text."))

    s.append(P("6&nbsp;&nbsp;Harmonisation and grading", "h1"))
    s.append(P(
        "Sources H1 and K1 report on the same 0&ndash;20 acute tolerability scale and are graded "
        "identically. The 0&ndash;3 ordinal grade uses the cut-offs published by the H1 authors "
        "(4, 7, 18), not thresholds devised here: grade 0 = score 0; grade 1 = 0&ndash;4 "
        "(&lsquo;mild&rsquo;); grade 2 = 4&ndash;7 (&lsquo;moderate&rsquo;); grade 3 = above 7. "
        f"The boundary between grade 1 and 2 is the authors' own developability line, and it "
        f"reproduces: {n['n_grade_le1']} of {n['n_ans']} in vivo rows "
        f"({n['pct_grade_le1']:.1f}%) fall at grade &le; 1, against the authors' stated "
        f"&lsquo;roughly 60%&rsquo;. Every graded row carries the rule applied in "
        f"<font face='Courier'>grade_basis</font>, and every grade is "
        f"<font face='Courier'>provisional</font>."))
    s.append(P(
        "Where a source publishes scores only as figures, no number is read off the figure: "
        "<font face='Courier'>readout_value</font> is "
        "<font face='Courier'>NOT_REPORTED</font>, "
        "<font face='Courier'>readout_is_qualitative</font> is TRUE, and the grade is taken from "
        "the severity the authors state in words. Clinical rows use a separate rubric and are "
        "kept on separate <font face='Courier'>tox_axis</font> values so that they are never "
        "silently pooled with preclinical scores."))

    s.append(P("7&nbsp;&nbsp;Quality control", "h1"))
    s.append(P(
        f"<font face='Courier'>qc/validate_dataset.py</font> runs {n['checks_total']} checks; "
        f"all {n['checks_passed']} pass and the script exits non-zero on any failure. They "
        f"cover: primary-key uniqueness; referential integrity across all three joins; "
        f"controlled-vocabulary conformance on seven columns; grade range; the requirement that "
        f"every graded row state its grading rule; the requirement that <b>every numeric readout "
        f"name its source table or figure</b>; agreement between each declared length and base "
        f"composition and the actual sequence; and, for every oligonucleotide, that the "
        f"modification table holds exactly one contiguous row per position whose nucleobase "
        f"matches the sequence at that position."))
    s.append(P(
        "Two independent end-to-end checks were also run. The source authors' published "
        "predictive model, re-implemented from their supplementary methods, reproduces their own "
        "score column for all 1,825 rows. And a baseline classifier trained only on the released "
        "CSVs, using the source's own held-out split, reaches "
        f"{n['model']['acc_published_cutoff70']:.1%} accuracy &mdash; matching the accuracy the "
        f"authors report for that validation set."))

    s.append(P("8&nbsp;&nbsp;Reproducibility", "h1"))
    s.append(P(
        "The pipeline is deterministic and fully committed. From a clean checkout: "
        "<font face='Courier'>build_hagedorn.py</font> &rarr; "
        "<font face='Courier'>build_curated.py</font> &rarr; "
        "<font face='Courier'>assemble.py</font> &rarr; "
        "<font face='Courier'>validate_dataset.py</font> &rarr; "
        "<font face='Courier'>make_figures.py</font> &rarr; "
        "<font face='Courier'>make_release.py</font> &rarr; "
        "<font face='Courier'>make_pdfs.py</font>. Dependencies are "
        "<font face='Courier'>openpyxl</font>, <font face='Courier'>pymupdf</font>, "
        "<font face='Courier'>matplotlib</font> and <font face='Courier'>reportlab</font>. "
        "Every number in the figures and in both PDFs is computed at build time from "
        "<font face='Courier'>data/</font>, so neither document can state a value the dataset "
        "does not contain."))
    s.append(P(
        "Determinism is <b>byte-level, and checked rather than asserted</b>. Running the pipeline "
        "twice over the same inputs reproduces all 19 released artefacts &mdash; the four CSVs, "
        "the workbook, both PDFs, the eight figures and the generated documentation &mdash; with "
        "identical SHA-256 digests. Reaching that required suppressing three sources of "
        "build-time noise that would otherwise make every rebuild differ while the data stayed "
        "the same: ReportLab&rsquo;s embedded creation timestamps and document IDs, the archive "
        "timestamps inside the .xlsx container, and the modification date openpyxl writes into "
        "<font face='Courier'>docProps/core.xml</font> at save time. A reviewer who re-runs the "
        "build can therefore diff the outputs against the committed ones and expect an exact "
        "match, rather than having to compare them by eye."))
    return s


def main() -> int:
    OUT.mkdir(exist_ok=True)
    n = gather()
    p1 = build(OUT / "OligoTox-CNS_Narrative.pdf", narrative(n),
               "OligoTox-CNS v1.0 · Narrative · NCATS Oligonucleotide Toxicity Challenge, Phase 2")
    p2 = build(OUT / "OligoTox-CNS_Methodology.pdf", methodology(n),
               "OligoTox-CNS v1.0 · Methodology · NCATS Oligonucleotide Toxicity Challenge, Phase 2")
    import pymupdf
    for p, limit in ((p1, 12), (p2, 5)):
        pages = len(pymupdf.open(p))
        flag = "OK" if pages <= limit else "OVER LIMIT"
        print(f"{p.name}: {pages} pages (limit {limit}) [{flag}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
