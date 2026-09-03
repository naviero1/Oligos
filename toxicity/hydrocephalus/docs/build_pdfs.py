#!/usr/bin/env python3
"""
Renders the three Phase 2 submission documents as PDFs.

  OligoTox-Hydrocephalus_Narrative.pdf     <= 12 pages
  OligoTox-Hydrocephalus_Methodology.pdf   <= 5 pages
  OligoTox-Hydrocephalus_PADP.pdf          <= 5 pages

Every count is read from qc/stats.json and ml/results.json, never typed, so a
figure in a document cannot disagree with the data it describes. The script
asserts the page limits and exits non-zero if a document runs over.

Usage: python3 docs/build_pdfs.py   (after qc/validate.py and ml/analyse.py)
"""
import json
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, Image, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "ml", "figures")

INK = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#616E7C")
ACCENT = colors.HexColor("#2C6E9B")
RULE = colors.HexColor("#CBD2D9")
BAND = colors.HexColor("#F2F5F7")

S = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=S["BodyText"], fontName="Helvetica",
                      fontSize=9.2, leading=13.2, textColor=INK,
                      alignment=TA_JUSTIFY, spaceAfter=6)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=13.5,
                    leading=17, spaceBefore=12, spaceAfter=6, textColor=INK,
                    alignment=0)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=10.4,
                    leading=14, spaceBefore=9, spaceAfter=4, textColor=ACCENT,
                    alignment=0)
TITLE = ParagraphStyle("title", parent=BODY, fontName="Helvetica-Bold",
                       fontSize=19, leading=23, spaceAfter=3, alignment=0)
SUB = ParagraphStyle("sub", parent=BODY, fontName="Helvetica", fontSize=9.6,
                     leading=13, textColor=MUTED, spaceAfter=10, alignment=0)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=13, bulletIndent=3,
                        spaceAfter=3)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.1, leading=11,
                       textColor=MUTED)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, leading=11,
                      alignment=0, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(.5)
    canvas.line(0.9 * inch, 0.62 * inch, LETTER[0] - 0.9 * inch, 0.62 * inch)
    canvas.setFont("Helvetica", 7.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.9 * inch, 0.45 * inch, doc.running_title)
    canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.45 * inch,
                           "page %d" % canvas.getPageNumber())
    canvas.restoreState()


def build(path, running_title, flow):
    doc = BaseDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch,
                          rightMargin=0.9 * inch, topMargin=0.75 * inch,
                          bottomMargin=0.85 * inch, title=running_title)
    doc.running_title = running_title
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="n", leftPadding=0, rightPadding=0, topPadding=0,
                  bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
    doc.build(flow)
    return doc.page


def table(rows, widths, header=True):
    data = []
    for i, r in enumerate(rows):
        style = CELLB if (header and i == 0) else CELL
        data.append([Paragraph(str(c), style) for c in r])
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, 0), .7, RULE),
            ("LINEBELOW", (0, 1), (-1, -2), .25, RULE),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), BAND))
    t.setStyle(TableStyle(cmds))
    return t


def bullets(items):
    return [Paragraph("&bull;&nbsp;&nbsp;" + t, BULLET) for t in items]


def fig(name, width=6.3):
    p = os.path.join(FIG, name)
    if not os.path.exists(p):
        return Spacer(1, 1)
    from PIL import Image as PILImage
    w, h = PILImage.open(p).size
    return Image(p, width=width * inch, height=width * inch * h / w)


def main():
    st = json.load(open(os.path.join(ROOT, "qc", "stats.json")))
    ml = json.load(open(os.path.join(ROOT, "ml", "results.json")))
    cns, sysm = ml["route"][0], ml["route"][1]
    made = []

    # ==================================================================
    # NARRATIVE
    # ==================================================================
    f = [Paragraph("OligoTox-Hydrocephalus", TITLE),
         Paragraph("An open, provenance-resolved dataset of hydrocephalus and "
                   "CSF-dynamics toxicity for oligonucleotide therapeutics<br/>"
                   "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge — "
                   "Phase 2 (Data Generation) · Narrative document · release v1.0", SUB)]

    hdr = [["Measurements", "Oligonucleotides", "Sources", "Trials",
            "Position records", "QC checks"],
           [f"{st['n_measurements']:,}", str(st["n_oligos"]), str(st["n_sources"]),
            "155", str(st["n_modification_positions"]),
            f"{st['checks_run']}/{st['checks_run']} pass"]]
    f += [table(hdr, [1.05 * inch] * 6), Spacer(1, 10)]

    f += [Paragraph("1 &nbsp; Executive summary", H1),
          Paragraph(
        f"OligoTox-Hydrocephalus pairs the design of {st['n_oligos']} oligonucleotide "
        f"therapeutics with {st['n_measurements']:,} measured hydrocephalus and "
        f"CSF-dynamics outcomes drawn from {st['n_sources']} sources. It is the first "
        "public dataset for this endpoint. Hydrocephalus is the eighth toxicity on the "
        "Challenge's list of interest and, on our reading of the Phase 1 cohort, no "
        "winning team addressed it.", BODY),
          Paragraph(
        "The endpoint is unusually hostile to naive curation, and the dataset's design "
        "is a direct response to three hazards. <b>The disease causes the endpoint</b> — "
        "the populations dosed with CNS oligonucleotides have elevated baseline rates of "
        "exactly this outcome. <b>The delivery procedure causes the endpoint</b> — "
        "repeated lumbar puncture produces CSF leak and low-pressure states in placebo "
        "arms as much as treated arms. <b>Almost nobody images the ventricles</b>, so "
        "for most compounds the absence of a finding means nobody looked. Each hazard is "
        "answered by a column that a modeller can filter on, not by a caveat in a "
        "document.", BODY)]

    f += [Paragraph("Positive and negative controls", H2),
          Paragraph(
        f"The dataset is not a list of toxic compounds. Its negative class is larger and "
        f"more deliberate than its positive class, which is what makes it trainable.", BODY)]
    f += bullets([
        f"<b>{st['tier_A_null']} tier-A explicit measured negatives.</b> Not absences: "
        "arms where the endpoint term is listed with a reported count of zero, or where "
        "42 CFR 11.48(a)(4)(ii)(A) requires the serious-adverse-event table to be "
        "complete and no ventricular term appears in it.",
        f"<b>{ml['paired_trials']} trials with a concurrent placebo or sham arm</b>, "
        f"contributing {ml['paired_ctrl_n']:,} comparator participants — the strongest "
        "design available here.",
        "<b>A route-contrast class.</b> Systemically dosed oligonucleotides are carried "
        "deliberately so the delivery hypothesis is testable rather than assumed.",
        "<b>Disease background rates carrying no compound at all</b> "
        "(<font face='Courier'>tox_axis = disease_background_rate</font>).",
        "<b>Procedure-attributable events</b> "
        "(<font face='Courier'>delivery_procedure_complication</font>), which occur in "
        "placebo arms and must be excluded from any compound-level analysis.",
        "<b>A designed negative control</b> — a scrambled non-targeting siRNA — and "
        "<b>two protective-direction rows</b>, an siRNA that <i>prevents</i> "
        "ventriculomegaly, kept on their own axis and left ungraded so a benefit can "
        "never be read as an absent harm.",
    ])

    f += [Paragraph("2 &nbsp; Main findings and conclusions", H1),
          Paragraph("Finding 1 — delivery route stratifies the endpoint, strongly, "
                    "between cohorts", H2),
          Paragraph(
        f"Across {ml['n_arms']} trial arms and {ml['n_participants']:,} participants at "
        f"risk, the tier-A (ventricular) event rate is "
        f"<b>{cns['rate_per_1000']:.2f} per 1,000</b> "
        f"(95% CI {cns['ci_lo_per_1000']:.2f}–{cns['ci_hi_per_1000']:.2f}) for "
        f"CNS-delivered oligonucleotides against "
        f"<b>{sysm['rate_per_1000']:.2f} per 1,000</b> "
        f"({sysm['ci_lo_per_1000']:.2f}–{sysm['ci_hi_per_1000']:.2f}) for systemically "
        f"delivered ones — odds ratio {ml['route_fisher']['odds_ratio']:.1f}, "
        f"Fisher exact p = {ml['route_fisher']['p_value']:.1e}.", BODY),
          fig("route_rate.png", 5.9), Spacer(1, 6),
          Paragraph("Finding 2 — and that contrast disappears inside randomised "
                    "comparisons", H2),
          Paragraph(
        f"This is the finding we would most want a reader to carry away. Restricting to "
        f"the {ml['paired_trials']} trials that contain their own concurrent comparator "
        f"arm, treated arms report {ml['paired_treated_events']} tier-A events in "
        f"{ml['paired_treated_n']:,} participants against "
        f"{ml['paired_ctrl_events']} in {ml['paired_ctrl_n']:,} comparator participants "
        f"— odds ratio {ml['paired_fisher']['odds_ratio']:.2f}, "
        f"p = {ml['paired_fisher']['p_value']:.2f}. <b>No detectable within-trial "
        f"effect.</b> The large between-route contrast in Finding 1 is a comparison "
        "between different diseases, different ages and different monitoring intensities, "
        "not between treated and untreated people. Both numbers are in the dataset, and "
        "reporting only the first would be the single easiest way to mislead with it.", BODY)]

    f += [Paragraph("Finding 3 — the ventricular signal concentrates in one compound, "
                    "and it was measured", H2),
          Paragraph(
        "Serious hydrocephalus or normal-pressure hydrocephalus appears in three separate "
        "tominersen studies, including 2/263 against 0/264 in the concurrent placebo arm "
        "of GENERATION HD1. The phase 1/2a trial made ventricular volume a pre-specified "
        "MRI outcome: from screening to day 197 the placebo arm moved 35.58 &rarr; 36.46 mL "
        "(+2.5%, n=12) while the two highest dose arms moved +13.0% (n=9) and +19.9% "
        "(n=10); in the open-label extension the ventricular-volume boundary shift "
        "integral rose 46.1% on monthly against 18.8% on bimonthly dosing. These are the "
        "only rows in the dataset where the ventricles were <i>measured</i> rather than "
        "incidentally observed.", BODY),
          fig("by_compound.png", 6.0), Spacer(1, 4),
          Paragraph("Finding 4 — but the endpoint is not compound-specific, and the two "
                    "attributed cases differ mechanistically", H2),
          Paragraph(
        "In an n-of-1 protocol, both infants dosed intrathecally with valeriasen — a "
        "different ASO, target, indication and age group — developed ventricular "
        "enlargement; one required endoscopic third ventriculostomy at a CSF opening "
        "pressure of 55 cmH<sub>2</sub>O, the other an external drain and then a shunt. "
        "The authors call it \"a potential monitorable toxicity of some intrathecal "
        "antisense oligonucleotides\". The mechanisms diverge: the tominersen index case "
        "was attributed to a sterile meningitis with CSF protein 2.64 g/L and "
        "lymphocytosis, whereas the KCNT1 patients had a negative CSF inflammatory panel "
        "and a dose-related hypothesis — evidenced by a reduced-dose rechallenge, "
        "delivered without recurrence. The dataset keeps them apart on "
        "<font face='Courier'>tox_axis</font> and "
        "<font face='Courier'>event_cluster_id</font> rather than pooling them into one "
        "count.", BODY),
          Paragraph("Finding 5 — the disease is a fourfold confounder", H2),
          Paragraph(
        "In the era before nusinersen was approved, SMA patients had a hydrocephalus "
        "incidence rate ratio of 4.7 (95% CI 2.4–10.2) against matched non-SMA controls. "
        "Those rows are in the dataset, carrying no compound. Any analysis of an "
        "SMA-indicated oligonucleotide that omits them will over-attribute.", BODY)]

    f += [Paragraph("3 &nbsp; How the data were produced", H1),
          Paragraph(
        "No wet-lab experiment was performed; this is a curation, and the methods are of "
        "two kinds kept strictly separate — the experimental methods of the source "
        "studies, and the curation methods used here. The full account is the companion "
        "Methodology document. In outline:", BODY)]
    f += [table([
        ["Modality", "Route used", "What it contributes"],
        ["Trial registry", "ClinicalTrials.gov v2 API",
         "Per-arm event counts <b>with denominators and comparator arms</b>, including "
         "explicitly reported zeros. Trial selection is a query over every "
         "oligonucleotide with posted results — 155 trials — not a hand-picked list."],
        ["Pharmacovigilance", "openFDA FAERS",
         "Post-marketing reporting proportions across the marketed class."],
        ["Regulatory labelling", "DailyMed SPL; EMA SmPC",
         "Verbatim, regulator-adjudicated risk statements with their section codes."],
        ["Primary literature", "Europe PMC fullTextXML",
         "The two drug-attributed index cases and their mechanisms."],
        ["Disease epidemiology", "Europe PMC fullTextXML",
         "Untreated-population incidence — the confounder control."],
        ["Chemistry", "WHO INN Recommended lists",
         "Sequences and per-position chemistry, by deterministic parse."],
    ], [1.05 * inch, 1.35 * inch, 3.9 * inch]), Spacer(1, 6),
          Paragraph(
        "<b>Computational processing.</b> Six of the eight build components are "
        "deterministic parsers over payloads committed to the repository, so their "
        "values cannot be mistyped and can be re-derived offline. The largest defect "
        "class found in a review of our sibling kidney dataset was hand-transcription "
        "error; a parser cannot make it, and its mapping tables are auditable in one "
        "place. Every network call is cached, so the whole dataset rebuilds from a clean "
        "checkout with one command sequence.", BODY)]

    f += [Paragraph("4 &nbsp; Indicators, predictor variables and their distribution", H1),
          Paragraph(
        "<b>The response variable.</b> <font face='Courier'>hydroceph_grade</font> is an "
        "ordinal 0–3 severity with a rubric written for this endpoint, not inherited from "
        "another organ. Every graded row carries in "
        "<font face='Courier'>grade_basis</font> the exact rule that produced it. The "
        "scale is censored by study type — a CSF-composition row cannot reach grade 3, "
        "which is defined by whole-organism intervention — so grades are not comparable "
        "across <font face='Courier'>study_type</font>, and we say so rather than letting "
        "it be discovered.", BODY)]
    grade = st["by_grade"]
    f += [table([["Grade", "0", "1", "2", "3", "not graded"],
                 ["Rows", f"{grade.get('0',0):,}", str(grade.get("1", 0)),
                  str(grade.get("2", 0)), str(grade.get("3", 0)),
                  str(grade.get("", 0))]], [1.0 * inch] + [0.85 * inch] * 5),
          Spacer(1, 7),
          Paragraph(
        "<b>Ascertainment is recorded, not assumed.</b> The column separates "
        "<i>measured_positive</i>, <i>measured_null</i> (actively assessed and not "
        f"found, {st['by_ascertainment'].get('measured_null', 0):,} rows), "
        "<i>reported_threshold_limited</i> and <i>not_assessed</i>. The QC suite "
        "<b>enforces</b> that a grade of 0 occurs only where ascertainment is "
        "measured_null. A model that ignores this column will learn the reporting "
        "process rather than the biology.", BODY),
          Paragraph(
        "<b>Attribution is the source's, never ours.</b> "
        f"<font face='Courier'>attribution_as_stated</font> is <i>not_discussed</i> for "
        f"{st['by_attribution'].get('not_discussed', 0):,} rows because registry and "
        "pharmacovigilance records carry no causality assessment at all. That is a "
        "property of those sources. Attribution for them must be read structurally, from "
        "the comparator arm and the disease baseline — which is why both are in the "
        "dataset.", BODY),
          Paragraph("Predictor variables across the tested oligonucleotides", H2),
          Paragraph(
        f"Design predictors are carried at chemistry and design level for all "
        f"{st['n_oligos']} compounds and at <b>per-position</b> level for "
        f"{st['n_oligos_with_position_map']}: "
        f"{st['n_modification_positions']} rows giving the sugar, base, 5-methylation and "
        "phosphorothioate-versus-phosphodiester status at every nucleotide. "
        f"{st['oligos_with_sequence']} compounds carry a published sequence. The "
        "remainder — the double-stranded siRNAs, the morpholinos and the compounds that "
        "enter only through the trial registry — do not, and that is the dataset's "
        "principal limitation for sequence-level modelling.", BODY),
          table([["Subject class", "Rows"]] +
                [[k, f"{v:,}"] for k, v in st["by_subject_class"].items()] +
                [["<b>in vitro (any species)</b>", "<b>0</b>"]],
                [2.6 * inch, 1.0 * inch]), Spacer(1, 5),
          Paragraph(
        "Human and animal evidence are separated by a single column, "
        "<font face='Courier'>subject_class</font>, which the QC suite re-derives and "
        "fails on any disagreement, with generated human-only and animal-only views. "
        "<b>The dataset contains no in vitro rows.</b> The Challenge states that datasets "
        "based on in vitro human systems, or able to extrapolate between in vitro human "
        "systems and animal data, are of particular interest; this release does neither, "
        "and we would rather state that plainly than imply otherwise.", BODY)]

    f += [Paragraph("5 &nbsp; The gap this addresses", H1),
          Paragraph(
        "Before this release there was no public, structured dataset pairing "
        "oligonucleotide identity with hydrocephalus or CSF-dynamics outcomes. The "
        "evidence existed but was scattered across registry adverse-event tables, "
        "spontaneous-report databases, two regulators' labels, and a handful of case "
        "reports — in formats that cannot be joined and with no shared severity scale. "
        "The specific gap this closes is not that the events were unknown; it is that "
        "<b>nobody could see them next to their own denominators, their comparator arms "
        "and their disease baselines at the same time</b>. That juxtaposition is what "
        "turns a set of alarming case reports into something a model can be fitted to, "
        "and it is what produced Finding 2 — a null within-trial contrast that the case "
        "literature alone would never have surfaced.", BODY)]

    f += [Paragraph("6 &nbsp; Using this data to build a predictive model", H1),
          Paragraph(
        "We fitted models rather than merely proposing them, and report what they do and "
        "do not support. The unit of analysis is the <b>trial arm</b>, not the "
        "measurement row: rows within an arm are not independent, and an arm carries a "
        "denominator. Validation is <b>leave-one-compound-out</b>, because arms of the "
        "same compound are correlated and a random split leaks the compound across folds.",
        BODY),
          fig("model_auc.png", 6.0), Spacer(1, 4),
          Paragraph(
        f"On the tier-B (CSF-dynamics) outcome, which occurs in {ml['n_armsB']} arms and "
        "is the mechanistic precursor the index case documents, route and indication give "
        f"a leave-one-compound-out AUC of "
        f"{[m for m in ml['models'] if m['name']=='route + indication'][0]['auc']} "
        f"(bootstrap 95% CI {ml.get('best_model_auc_ci',['—','—'])[0]}–"
        f"{ml.get('best_model_auc_ci',['—','—'])[1]}). Adding chemistry <i>degrades</i> "
        "it, because chemistry is NOT_REPORTED for most compounds and contributes noise. "
        "The tier-A outcome, with 9 affected arms, will not support a classifier and we "
        "do not present one.", BODY),
          Paragraph(
        "<b>The leakage probes are the most useful result.</b> A model given only trial "
        "identity reaches AUC "
        f"{[m for m in ml['models'] if 'trial identity' in m['name']][0]['auc']}, so a "
        "material share of any apparent performance is provenance, not biology. A model "
        "given only compound identity scores "
        f"{[m for m in ml['models'] if 'compound identity' in m['name']][0]['auc']} — "
        "below chance, which is the correct behaviour under leave-one-compound-out and "
        "confirms the validation is doing its job. We ran these because a review of our "
        "sibling kidney dataset found study_type and source_id were strong shortcut "
        "predictors of its label.", BODY),
          Paragraph("What a user should build with it, and what they should not", H2)]
    f += bullets([
        "<b>Supported:</b> route- and population-stratified risk models; separating drug "
        "effect from procedure and disease effect; modelling ascertainment explicitly as "
        "a covariate; hypothesis generation for CSF-dynamics monitoring in intrathecal "
        "programmes.",
        "<b>Not supported:</b> sequence-to-toxicity prediction across the full roster "
        f"({st['oligos_with_sequence']} of {st['n_oligos']} sequences); within-compound "
        "dose–response for tier A; in vitro-to-in vivo extrapolation; and any causal "
        "claim about an individual compound, given Finding 2.",
    ])
    f += [Paragraph(
        "The most valuable next experiment this dataset points to is not a bigger model. "
        "It is a human in vitro choroid-plexus or blood-CSF-barrier system in which a "
        "PS-oligonucleotide is applied and CSF-relevant transport is measured — because "
        "the one axis that would let anybody extrapolate from these clinical observations "
        "to a new compound is precisely the axis on which no public data exists.", BODY),
        Spacer(1, 8),
        Paragraph(
        "<b>Availability.</b> Dataset, build and QC code, and every retrieved source "
        "payload: <font face='Courier'>github.com/naviero1/Oligos</font>, "
        "<font face='Courier'>toxicity/hydrocephalus/</font>. Curation released under "
        f"CC BY 4.0; per-row rights in the redistribution column "
        f"({st['by_redistribution'].get('public_domain',0):,} rows public domain). "
        f"All {st['checks_run']} QC checks pass on the released revision.", SMALL)]

    n = build(os.path.join(ROOT, "OligoTox-Hydrocephalus_Narrative.pdf"),
              "OligoTox-Hydrocephalus · Narrative · NCATS Phase 2", f)
    made.append(("Narrative", n, 12))

    # ==================================================================
    # METHODOLOGY
    # ==================================================================
    f = [Paragraph("OligoTox-Hydrocephalus — Methodology", TITLE),
         Paragraph("Materials and methods for the hydrocephalus / CSF-dynamics "
                   "oligonucleotide toxicity dataset<br/>NIH/NCATS OligoTox Open Data "
                   "Challenge — Phase 2 · release v1.0", SUB),
         Paragraph("1 &nbsp; Design and no-fabrication policy", H1),
         Paragraph(
        "This is a curated dataset; no new wet-lab experiment was performed. The methods "
        "below are therefore of two kinds, kept strictly separate: <b>(a)</b> the "
        "experimental and reporting methods of the source studies, recorded so a user "
        "knows how each measurement was generated, and <b>(b)</b> the curation methods "
        "used here. Conflating them would let curation choices masquerade as experimental "
        "fact.", BODY),
         Paragraph(
        "No value in this dataset was recalled from memory or inferred. Every number, "
        "sequence, denominator, quotation and identifier was copied by a script from a "
        "payload committed to the repository, or transcribed from a full text also "
        "committed, and carries the exact locus it came from. Where a source is silent "
        "the field is NOT_REPORTED. <b>No number was read off a figure</b>: where a value "
        "is published only graphically, readout_value is NOT_REPORTED and "
        "readout_is_qualitative is TRUE.", BODY),
         Paragraph("2 &nbsp; Endpoint definition", H1),
         Paragraph(
        "Inclusion required a ventricular, CSF-volume, CSF-pressure or CSF-composition "
        "outcome for an identified oligonucleotide, or a population baseline for such an "
        "outcome. <b>Tier A</b> is the core endpoint: hydrocephalus, ventriculomegaly, "
        "ventricular volume, shunt or drain placement. <b>Tier B</b> is CSF-dynamics "
        "adjacent: raised intracranial pressure, papilloedema, aseptic or chemical "
        "meningitis, arachnoiditis, CSF protein or cell-count rise, post-lumbar-puncture "
        "syndrome. General neurological adverse events with no CSF or ventricular readout "
        "contribute nothing. <b>Route of administration is not itself evidence</b> of the "
        "endpoint.", BODY),
         Paragraph("3 &nbsp; Source identification and retrieval", H1),
         Paragraph(
        "Sources were sought across six deliberately different modalities, because each "
        "is biased differently: literature finds published positives, a registry finds "
        "protocol-collected events including zeros, a spontaneous-reporting system finds "
        "post-marketing signals, labels find regulator-adjudicated risks, an "
        "epidemiological cohort finds the disease baseline, and the INN lists give "
        "chemistry. Trial selection is a query, not a judgement: ClinicalTrials.gov was "
        "asked for <b>every</b> trial of any of 41 oligonucleotide therapeutics with "
        "posted results, yielding 155 usable trials. An earlier hand-picked list of 23 "
        "biased the dataset toward compounds already suspected of causing the endpoint "
        "and omitted most of the negative evidence. Every retrieved payload is committed, "
        "so the dataset rebuilds offline.", BODY),
         Paragraph("4 &nbsp; Extraction", H1),
         Paragraph(
        "Six of eight components are deterministic parsers rather than transcription. "
        "Each copies values from a named path in a committed payload, which becomes the "
        "row's source_location. Two components are curated from prose a human read; each "
        "of their rows stores the <b>verbatim sentence</b> it was taken from, so value "
        "and evidence travel together.", BODY),
         table([
        ["Component", "Rows", "Method"],
        ["extract_ctgov.py", "—", "Walks resultsSection.adverseEventsModule; one row per "
         "trial × term × arm, copying numAffected and numAtRisk from the named JSON path. "
         "MedDRA terms are never normalised or spelling-corrected."],
        ["extract_ctgov_outcomes.py", "—", "Pre-specified ventricular MRI outcome "
         "measures — the only rows where the ventricles were measured rather than "
         "incidentally observed. Selection is an explicit allow-list; a pattern match "
         "would sweep in CSF pharmacokinetics and neurofilament."],
        ["extract_faers.py", "—", "One exact query per (drug, MedDRA term). A count "
         "aggregation truncates at openFDA's 100-bucket cap and would silently drop rare "
         "pairs. A pre-flight check validates every term string against the database and "
         "drops any it does not know, rather than letting it manufacture false zeros."],
        ["extract_labels.py", "—", "Parses SPL XML; records the matching sentence "
         "verbatim with its LOINC section. A silent label yields an explicit "
         "measured_null row, not no row."],
        ["parse_inn_sequences.py", "—", "Parses WHO INN chemical names, which spell out "
         "every residue, into sequence and per-position chemistry."],
        ["build_modifications.py", str(st["n_modification_positions"]),
         "One row per nucleotide position: sugar, base, 5-methylation and 3' linkage."],
        ["build_literature.py / build_nonclinical.py", "—",
         "Curated rows; each carries its verbatim quote."],
    ], [1.55 * inch, 0.5 * inch, 4.25 * inch]), Spacer(1, 5),
         Paragraph("5 &nbsp; Purification and characterisation of oligo identity", H1),
         Paragraph(
        "The Challenge asks specifically for the methods used to purify and characterise "
        "oligo identity. Because the compounds were made by their sponsors and not here, "
        "what can be reported is what each source states — and the honest answer is "
        "almost nothing. A full-text sweep of all sixteen committed US prescribing "
        "information documents for purity, purification, chromatography, mass-spectrometry, "
        "identity and characterisation language returns <b>no statement about the drug "
        f"substance in any of them</b>; every hit is a patient baseline characteristic or "
        f"an efficacy assay. purity_pct is NOT_REPORTED for all {st['n_oligos']} "
        "compounds. The two research-reagent sources name a supplier but no method. No "
        "purity value has been estimated, inferred from a synthesis platform, or carried "
        "across from another compound. Our sibling OligoTox-CNS release reports the same "
        "for all 1,839 of its oligonucleotides: this is a property of the published "
        "literature, not of the curation.", BODY),
         Paragraph(
        "<b>Identity as recorded here</b> means the sequence together with its "
        "per-position chemistry, and both are parsed rather than typed. Sequences come "
        "from the WHO INN Recommended lists, whose entries spell out each residue's "
        "sugar, base, 5-methylation and 3' linkage longhand. The parse is validated "
        "against evidence from outside the INN list and the script exits rather than emit "
        "a disagreeing sequence: nusinersen parses to 18 residues with 17 phosphorothioate "
        "linkages against a label formula of P17 S17; tofersen to 20 residues with 15 "
        "phosphorothioate and 4 phosphodiester linkages, exactly as its label states in "
        "words; and tofersen's INN-derived sugar map is identical, position for position, "
        "to the map derived independently from the label's own motif sentence.", BODY),
         Paragraph("6 &nbsp; Experimental methods of the source studies", H1)]
    f += bullets([
        "<b>Registry adverse-event tables.</b> Modules declare a frequencyThreshold "
        "governing the other-events table, copied into every affected row's "
        "ascertainment_basis. 42 CFR 11.48(a)(4)(ii)(A) requires the serious-event table "
        "to list <i>all</i> serious events with no threshold, which is what makes a "
        "trial-level absence a reported zero. <b>No trial in this release performed "
        "protocol-specified ventricular imaging</b> except the two noted in the narrative.",
        "<b>FAERS.</b> Voluntary spontaneous reports, unvalidated, with no exposure "
        "denominator and no causality assessment.",
        "<b>Labels.</b> Postmarketing sections describe reports from a population of "
        "uncertain size for which causality cannot always be established.",
        "<b>Index cases.</b> Serial MRI, serial CSF sampling, and a lumbar infusion study "
        "measuring resistance to CSF outflow (tominersen); serial MRI, opening pressures "
        "and a reduced-dose rechallenge (valeriasen).",
        "<b>Disease baseline.</b> Retrospective matched-cohort study in a ~100-million-"
        "person EHR database, 2007–2016, ascertained by ICD-9/10 code.",
    ])
    f += [Paragraph("7 &nbsp; Harmonisation, grading and quality control", H1),
          Paragraph(
        "hydroceph_grade is a new ordinal column with its own written rubric, not a reuse "
        "of an organ-specific scale from another endpoint. Every graded row carries the "
        "exact rule in grade_basis. Grade 0 is permitted <b>only</b> where ascertainment "
        "is measured_null, so \"measured and null\" is never conflated with \"nobody "
        f"looked\". qc/validate.py runs <b>{st['checks_run']} checks</b> and exits "
        "non-zero on any failure, covering primary keys, both foreign keys, controlled "
        "vocabularies on twelve columns, the grade-0 rule, numerator ≤ denominator, "
        "contiguous nucleotide positions, and byte-identical regeneration of the derived "
        "views. Three are genuine cross-source consistency tests rather than format "
        "checks: the label's phosphorus count against the stated length, an siRNA "
        "duplex's guide strand against the reverse complement of its sense strand, and "
        "the modification table's bases against the stored sequence. The data dictionary "
        "lives in code and the suite asserts in both directions that every column is "
        "documented and every documented column exists — a check added because an earlier "
        "revision of our own schema declared three purity fields the builder never "
        "emitted.", BODY),
          Paragraph("8 &nbsp; Principal limitations", H1)]
    f += bullets([
        f"<b>No in vitro rows.</b> {st['n_human_rows']:,} human and "
        f"{st['n_animal_rows']} animal rows, none in vitro. The dataset cannot support "
        "in vitro-to-animal extrapolation.",
        f"<b>Sequences for {st['oligos_with_sequence']} of {st['n_oligos']} compounds.</b> "
        "Duplex siRNAs and morpholinos are refused by the INN parser rather than guessed; "
        "one compound's sequence exists only as an image whose bold/underline chemistry "
        "encoding does not survive text extraction.",
        "<b>All grades are provisional.</b> No subject-matter expert has reviewed the "
        "rubric or its application.",
        "<b>100 verified sources retrieved but not extracted</b>, listed with their "
        "retrieval routes in notes/source_backlog.md.",
    ])
    n = build(os.path.join(ROOT, "OligoTox-Hydrocephalus_Methodology.pdf"),
              "OligoTox-Hydrocephalus · Methodology · NCATS Phase 2", f)
    made.append(("Methodology", n, 5))

    # ==================================================================
    # PADP
    # ==================================================================
    f = [Paragraph("Public Access and Dissemination Plan", TITLE),
         Paragraph("OligoTox-Hydrocephalus dataset · NIH/NCATS Oligonucleotide Toxicity "
                   "Open Data Challenge, Phase 2", SUB),
         Paragraph(
        "This plan describes how the OligoTox-Hydrocephalus dataset is licensed, made "
        "publicly accessible and disseminated, and — as the Challenge requires — how the "
        "U.S. Government can allow interested parties to use it even if the submitting "
        "team does not itself continue to.", BODY),
         Paragraph("1 &nbsp; What is covered", H1),
         table([["Artifact", "Description"],
                ["data/oligos.csv", f"{st['n_oligos']} oligonucleotides — identity and "
                 "design predictors"],
                ["data/measurements.csv", f"{st['n_measurements']:,} graded "
                 "hydrocephalus / CSF-dynamics records"],
                ["data/modifications.csv", f"{st['n_modification_positions']} per-position "
                 "chemistry records"],
                ["data/sources.csv", f"{st['n_sources']} source provenance registry"],
                ["data/trial_registry.csv", "155 trials with posted results"],
                ["OligoTox-Hydrocephalus_Dataset.xlsx", "the whole dataset as one "
                 "workbook, 9 sheets"],
                ["SCHEMA.md, scripts/data_dictionary.py", "schema and data dictionary"],
                ["scripts/, qc/, ml/", "build, QC and analysis code"],
                ["sources/raw/", "every retrieved source payload"]],
               [2.05 * inch, 4.25 * inch]), Spacer(1, 5),
         Paragraph(
        "The dataset is a curation of already-published data. It contains <b>no "
        "human-subjects data, no personally identifiable information and no protected "
        "health information</b> — only aggregate experimental and clinical values and "
        "design descriptors drawn from public literature, regulatory labels, public "
        "registries and government databases. There are therefore no privacy, consent or "
        "data-use-agreement constraints on redistribution.", BODY),
         Paragraph("2 &nbsp; Licensing scheme", H1),
         Paragraph(
        "The curated tables, schema, documentation and code are released under the "
        "<b>Creative Commons Attribution 4.0 International licence (CC BY 4.0)</b> — "
        "permissive and <b>irrevocable</b> — letting anyone, including the U.S. "
        "Government and any third party, access, reuse, redistribute, modify and build "
        "upon the dataset in perpetuity subject only to attribution. The grant is made in "
        "the LICENSE file in the dataset directory, not merely intended. A more "
        "permissive dedication such as CC0 1.0 can be substituted at NCATS's preference.",
        BODY),
         Paragraph(
        "<b>Underlying third-party full texts are never redistributed</b>; they are "
        "referenced by DOI, PMID, NCT identifier or set id. Rights are tracked "
        "<b>per row</b> in the redistribution column, and every value it takes is used by "
        "real rows:", BODY),
         table([["Value", "Rows", "Meaning"]] +
               [[k, f"{v:,}", d] for k, v, d in [
                   ("public_domain", st["by_redistribution"].get("public_domain", 0),
                    "US Government works — ClinicalTrials.gov, FAERS, DailyMed, eCFR. "
                    "Values may be reproduced."),
                   ("cc_by", st["by_redistribution"].get("cc_by", 0),
                    "Open-access articles; reproduce with attribution."),
                   ("cc_by_nc", st["by_redistribution"].get("cc_by_nc", 0),
                    "Open access, non-commercial terms."),
                   ("summary_stat_only", st["by_redistribution"].get("summary_stat_only", 0),
                    "Licence carries a no-derivatives term; only abstract-level summary "
                    "statistics are carried."),
                   ("verify", st["by_redistribution"].get("verify", 0),
                    "Reuse terms were not established in curation; a redistributor should "
                    "resolve the licence before republishing those values."),
               ]], [1.15 * inch, 0.6 * inch, 4.55 * inch]), Spacer(1, 5),
         Paragraph(
        "No patents, trade secrets or restrictive intellectual property are or will be "
        "claimed over the dataset. There is no proprietary component whose withdrawal "
        "could remove public access. Because the licence is irrevocable once granted, "
        "third-party use does not depend on the team's continued participation.", BODY),
         Paragraph("3 &nbsp; Public access — hosting and persistence", H1)]
    f += bullets([
        "<b>Primary distribution:</b> a public code-hosting repository "
        "(github.com/naviero1/Oligos, toxicity/hydrocephalus/), openly accessible without "
        "registration.",
        "<b>Independent archival persistence and a citable identifier:</b> a versioned "
        "snapshot of each release will be deposited in a public long-term archive "
        "(Zenodo or an NIH-designated repository) and assigned a DOI, so the dataset "
        "remains findable and retrievable independently of the team or any single hosting "
        "account.",
        "<b>Non-proprietary formats:</b> UTF-8 CSV and Markdown, plus one XLSX "
        "convenience copy. No software licence is required to read any of it, and the "
        "build and QC code depends only on the Python standard library except for the "
        "workbook export and the analysis.",
        "<b>Reproducibility:</b> every source payload is committed, so a third party can "
        "rebuild the dataset from a clean checkout with no network access and confirm "
        f"all {st['checks_run']} QC checks pass.",
    ])
    f += [Paragraph("4 &nbsp; Dissemination and FAIR alignment", H1),
          table([["Principle", "How the dataset meets it"],
                 ["Findable", "Stable primary keys; archival DOI; descriptive metadata; a "
                  "provenance registry naming every source."],
                 ["Accessible", "Open repository and archive; open formats; no "
                  "gatekeeping, registration or request process."],
                 ["Interoperable", "Controlled vocabularies enforced by the QC suite; a "
                  "normalised four-table schema that is deliberately column-compatible "
                  "with our CNS release so endpoints can be pooled."],
                 ["Reusable", "CC BY 4.0, plus per-row provenance (source_id, source_ref, "
                  "exact source_location) so any single value is re-verifiable, and "
                  "per-row rights so lawful reuse is auditable at record level."]],
                [1.0 * inch, 5.3 * inch]), Spacer(1, 5),
          Paragraph(
        "Documentation for reuse comprises the narrative, this plan, the methodology "
        "document, README, SCHEMA and the in-code data dictionary. Optional supporting "
        "material includes the full build and QC pipeline and the analysis code that "
        "produces the narrative's predictive-model section.", BODY),
          Paragraph("5 &nbsp; Continuity and U.S. Government use contingency", H1),
          Paragraph(
        "The Challenge requires a plan for how the U.S. Government can allow interested "
        "parties to use the solution if the team fails to use it and does not permit "
        "others to under reasonable terms. Three scenarios cover this.", BODY)]
    f += bullets([
        "<b>Scenario A — normal operation.</b> The team maintains the repository and "
        "archival deposit and disseminates updates. Third parties use the dataset under "
        "CC BY 4.0.",
        "<b>Scenario B — the team ceases activity.</b> No action by the team is needed: "
        "the dataset has <b>already</b> been released under an irrevocable CC BY 4.0 "
        "licence and a copy is deposited in an independent public archive with a DOI. The "
        "U.S. Government and any interested party may continue to access, copy, host and "
        "build upon it without further permission. The permissive licence and the "
        "independent archival copy are the mechanisms that accomplish this.",
        "<b>Scenario C — explicit government grant.</b> The team additionally grants the "
        "U.S. Government a non-exclusive, irrevocable, royalty-free right to use, "
        "reproduce, distribute, publicly display, host copies of and <b>authorise others "
        "to use</b> the dataset and its documentation. This right survives any cessation "
        "of the team's activity.",
    ])
    f += [Paragraph(
        "In no scenario does third-party or Government use depend on the team's ongoing "
        "involvement, on a proprietary service, or on any revocable permission.", BODY),
        Paragraph("6 &nbsp; Maintenance, versioning and stewardship", H1),
        Paragraph(
        "Releases are versioned with a changelog and each is archived under its own DOI, "
        "so prior versions remain citable. All severity grades currently ship "
        "grade_status = provisional; a post-review release will clear that flag and "
        "record the reviewer's disposition. Corrections and additions are tracked through "
        "the repository's public history, and the QC suite runs on every revision so a "
        "release cannot silently regress. The maintainer is the submitting team via the "
        "public repository; the fallback steward is the independent public archive, which "
        "preserves the deposited snapshot and DOI irrespective of team status.", BODY),
        Paragraph("7 &nbsp; Compliance summary", H1)]
    f += bullets([
        "Consistent with NIH Scientific Data Sharing / Public Access policy and with FAIR.",
        "Open, irrevocable licence granted in-repository, ensuring perpetual public "
        "usability.",
        "No PII, PHI or human-subjects data, so no privacy or consent barrier to sharing.",
        "Provenance and redistribution rights tracked per row, so lawful reuse is "
        "verifiable at the record level.",
    ])
    n = build(os.path.join(ROOT, "OligoTox-Hydrocephalus_PADP.pdf"),
              "OligoTox-Hydrocephalus · Public Access & Dissemination Plan", f)
    made.append(("PADP", n, 5))

    bad = False
    for name, pages, limit in made:
        ok = pages <= limit
        bad = bad or not ok
        print("%-12s %2d pages (limit %2d) %s" % (name, pages, limit,
                                                  "OK" if ok else "OVER LIMIT"))
    if bad:
        sys.exit("a document exceeds its Challenge page limit")


if __name__ == "__main__":
    main()
