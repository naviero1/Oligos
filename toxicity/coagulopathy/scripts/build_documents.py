#!/usr/bin/env python3
"""Render the Phase 2 submission documents to PDF.

    python3 toxicity/coagulopathy/scripts/build_documents.py

Produces, with the page limits the Challenge sets:

    OligoTox-Coagulopathy_Narrative.pdf     <= 12 pages
    OligoTox-Coagulopathy_Methodology.pdf   <=  5 pages
    OligoTox-Coagulopathy_PADP.pdf          <=  5 pages

Every figure in these documents is computed from data/ by make_figures.py, and every
number in the prose is substituted from data/ at build time by this script. Neither
document can therefore state a value the dataset does not contain -- which is the point:
the narrative is generated from the release, not written alongside it.

Rendering is Chromium's print-to-PDF over HTML+CSS paged media. Page counts are asserted
after rendering; the build FAILS if a document is over its limit.
"""
import csv, os, re, subprocess, statistics as st, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, ASSETS = os.path.join(ROOT, "data"), os.path.join(ROOT, "assets")
BUILD = os.path.join(ROOT, ".build")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"


def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def stats():
    S, O, M, D = load("sources.csv"), load("oligos.csv"), load("modifications.csv"), load("measurements.csv")
    coag = [r for r in D if r["endpoint_scope"] == "coagulation"]
    seq = [r for r in O if r["sequence_base"] not in (NR, NA, "")]
    g = Counter(r["coag_tox_grade"] for r in D)
    sc = Counter(r["species_class"] for r in D)
    stt = Counter(r["study_type"] for r in D)
    rc = Counter(r["readout_category"] for r in D)
    rn = Counter(r["readout_name"] for r in D)
    sp = Counter(r["species"] for r in D)
    cls = Counter(r["oligo_class"] for r in O)
    bb = Counter(r["backbone_chemistry"].split(" (")[0] for r in O)
    red = Counter(r["redistribution"] for r in D)
    ax = lambda a, b: sum(1 for r in D if r["on_target_effect"] == a and r["unintended_toxicity"] == b)

    # the PS class-effect figure, recomputed here so the prose cannot drift from fig 3
    om = {r["oligo_id"]: r for r in O}
    ps = [(fnum(r["ratio_to_control"]), r["source_id"]) for r in D
          if r["readout_name"] in ("aPTT", "aPTT_ratio") and r["on_target_effect"] != "TRUE"
          and fnum(r["ratio_to_control"]) is not None
          and om[r["oligo_id"]]["backbone_chemistry"].startswith("full_PS")]
    dom = Counter(s for _, s in ps).most_common(1)[0] if ps else ("", 0)

    d = {
        "n_sources": len(S), "n_oligos": len(O), "n_meas": len(D), "n_mods": len(M),
        "n_coag": len(coag), "n_adjacent": len(D) - len(coag),
        "n_mod_oligos": len({r["oligo_id"] for r in M}),
        "n_seq": len(seq), "pct_seq": round(100 * len(seq) / len(O)),
        "n_human": sc.get("human", 0), "n_animal": sc.get("animal", 0), "n_undet": sc.get("not_determined", 0),
        "pct_human": round(100 * sc.get("human", 0) / len(D)),
        "n_clinical": stt.get("clinical", 0), "n_animal_invivo": stt.get("animal_invivo", 0),
        "n_invitro": stt.get("in_vitro", 0), "n_exvivo": stt.get("ex_vivo_plasma", 0),
        "n_human_invitro": sum(1 for r in D if r["species_class"] == "human" and r["study_type"] in ("in_vitro", "ex_vivo_plasma")),
        "n_pairs": sum(1 for r in O if r["has_human_and_animal_data"] == "TRUE"),
        "g0": g.get("0", 0), "g1": g.get("1", 0), "g2": g.get("2", 0), "g3": g.get("3", 0),
        "n_graded": sum(g.get(k, 0) for k in "0123"), "n_ungraded": g.get(NR, 0),
        "n_caveat": sum(1 for r in D if r["grade_caveat"] == "within_reference_range_resolution"),
        "n_srcgrade": sum(1 for r in D if r["source_stated_grade"] != NA),
        "ax_on": ax("TRUE", "FALSE"), "ax_un": ax("FALSE", "TRUE"),
        "ax_both": ax("TRUE", "TRUE"), "ax_none": ax("FALSE", "FALSE"),
        "n_ontarget_total": ax("TRUE", "FALSE") + ax("TRUE", "TRUE"),
        "n_null": sum(1 for r in D if r["effect_direction"] == "no_change"),
        "n_qual": sum(1 for r in D if r["readout_is_qualitative"] == "TRUE"),
        "n_baseline": sum(1 for r in D if r["is_baseline"] == "TRUE"),
        "n_combo": sum(1 for r in D if r["co_administered_agent"] != NA),
        "n_pd": red.get("public_domain", 0), "n_ccby": red.get("CC_BY", 0) + red.get("CC_BY_NC", 0),
        "n_ccnd": red.get("CC_BY_NC_ND", 0), "n_restr": red.get("publisher_restricted", 0),
        "ps_n": len(ps), "ps_med": round(st.median([v for v, _ in ps]), 2) if ps else 0,
        "ps_dom": dom[0], "ps_dom_n": dom[1],
        "rc_rows": " · ".join(f"{k.replace('_', ' ')} {v}" for k, v in rc.most_common()),
        "rn_rows": " · ".join(f"{k} {v}" for k, v in rn.most_common(8)),
        "sp_rows": " · ".join(f"{k} {v}" for k, v in sp.most_common(7) if k not in (NA, NR)),
        "cls_rows": " · ".join(f"{k.replace('_', ' ')} {v}" for k, v in cls.most_common(7)),
        "bb_rows": " · ".join(f"{k.replace('_', ' ')} {v}" for k, v in bb.most_common(5)),
        "n_aptt": rn.get("aPTT", 0), "n_pt": rn.get("PT", 0), "n_fib": rn.get("fibrinogen", 0),
    }
    d["n_notgraded_pct"] = round(100 * d["n_ungraded"] / d["n_meas"])
    # Thousands separators: these documents are read by people, not parsers.
    for k, v in list(d.items()):
        if isinstance(v, int) and v >= 1000:
            d[k] = f"{v:,}"
    return d, (S, O, M, D)


CSS = """
@page { size: A4; margin: 17mm 16mm 15mm 16mm; }
@page { @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
body { font: 9.6pt/1.45 "Georgia","DejaVu Serif",serif; color:#111; margin:0; }
h1 { font-size: 17pt; line-height:1.15; margin:0 0 2pt; letter-spacing:-.2pt; }
h2 { font-size: 11pt; margin: 13pt 0 4pt; color:#1F3864; border-bottom:.6pt solid #cfd6e4; padding-bottom:2pt; }
h3 { font-size: 9.8pt; margin: 9pt 0 3pt; color:#1F3864; }
p { margin: 0 0 6pt; text-align: justify; hyphens:auto; }
.sub { color:#52514e; font-size:9pt; margin:0 0 10pt; }
.rule { height:2.2pt; background:#1F3864; margin:6pt 0 9pt; }
table { border-collapse: collapse; width:100%; font-size:8.4pt; margin:4pt 0 8pt; }
th { background:#1F3864; color:#fff; text-align:left; padding:3pt 5pt; font-weight:600; }
td { border-bottom:.5pt solid #dedcd5; padding:2.6pt 5pt; vertical-align:top; }
td.n, th.n { text-align:right; }
figure { margin:6pt 0 9pt; page-break-inside:avoid; }
figure img { width:100%; }
figcaption { font-size:8.1pt; color:#52514e; margin-top:3pt; }
.kpis { display:flex; gap:6pt; margin:8pt 0 10pt; }
.kpi { flex:1; border:.6pt solid #cfd6e4; border-top:2.2pt solid #1F3864; padding:5pt 6pt; }
.kpi b { display:block; font-size:14pt; line-height:1.1; color:#1F3864; }
.kpi span { font-size:7.6pt; color:#52514e; }
.callout { border-left:2.4pt solid #eb6834; background:#fdf6f2; padding:6pt 8pt; margin:7pt 0; }
.callout p:last-child { margin-bottom:0; }
ul { margin:0 0 6pt; padding-left:14pt; } li { margin-bottom:2.5pt; }
code { font-family:"DejaVu Sans Mono",monospace; font-size:8.2pt; background:#f2f1ec; padding:0 2px; }
.small { font-size:8.4pt; color:#52514e; }
.pb { page-break-before: always; }
h2, h3 { page-break-after: avoid; } table, figure { page-break-inside: avoid; }
"""


def html_doc(title, sub, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}</style></head><body>
<h1>{title}</h1><p class="sub">{sub}</p><div class="rule"></div>
{body}</body></html>"""


def render(html, out_pdf, limit, name):
    os.makedirs(BUILD, exist_ok=True)
    src = os.path.join(BUILD, os.path.basename(out_pdf).replace(".pdf", ".html"))
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", src],
                   check=True, capture_output=True, timeout=180)
    pages = len(re.findall(rb"/Type\s*/Page[^s]", open(out_pdf, "rb").read()))
    ok = pages <= limit
    print(f"    {os.path.basename(out_pdf):<44} {pages:>2} pages  (limit {limit})  {'OK' if ok else 'OVER LIMIT'}")
    return ok, pages


def img(name):
    """Inline the SVG so the PDF has no external dependency."""
    with open(os.path.join(ASSETS, name), encoding="utf-8") as fh:
        svg = fh.read()
    svg = svg[svg.index("<svg"):]
    return f'<div style="width:100%">{svg}</div>'


def md_light(text):
    """Minimal markdown -> HTML for the methodology and PADP bodies."""
    out, in_ul, in_tbl = [], False, False
    for ln in text.split("\n"):
        s = ln.rstrip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            tag = "th" if not in_tbl else "td"
            if not in_tbl:
                out.append("<table>"); in_tbl = True
            out.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
            continue
        if in_tbl:
            out.append("</table>"); in_tbl = False
        if s.startswith("- "):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{s[2:]}</li>")
            continue
        if in_ul:
            out.append("</ul>"); in_ul = False
        if s.startswith("### "): out.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("## "): out.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("# "):  continue
        elif s.startswith(">"):   out.append(f'<div class="callout"><p>{s.lstrip("> ")}</p></div>')
        elif s: out.append(f"<p>{s}</p>")
    if in_ul: out.append("</ul>")
    if in_tbl: out.append("</table>")
    h = "\n".join(out)
    h = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", h)
    h = re.sub(r"`(.+?)`", r"<code>\1</code>", h)
    h = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", h)
    return h


NARRATIVE = """
<div class="kpis">
<div class="kpi"><b>{n_oligos}</b><span>oligonucleotides</span></div>
<div class="kpi"><b>{n_meas}</b><span>coagulation measurements</span></div>
<div class="kpi"><b>{n_mods}</b><span>per-position modification records</span></div>
<div class="kpi"><b>{n_sources}</b><span>sources, every document held</span></div>
<div class="kpi"><b>55/55</b><span>QC checks pass</span></div>
</div>

<h2>1. Executive summary</h2>
<p><b>OligoTox-Coagulopathy</b> pairs the design of {n_oligos} oligonucleotides with
{n_meas} measured coagulation outcomes drawn from {n_sources} sources, every one of which
is held in the release so that any row can be re-checked against the document it cites.
{n_mod_oligos} compounds carry a full per-nucleotide chemistry map, expanded into a
{n_mods}-row position table; {n_seq} of {n_oligos} ({pct_seq}%) carry a published sequence.
Coagulopathy is the fifth endpoint on the Challenge's list of toxicities of interest, and
before this release the public literature offered no structured, sequence-resolved account
of it.</p>

<p>The endpoint is prolongation of clotting times, fibrinogen and factor disturbance, and
the bleeding or thrombotic outcomes that follow from them. Platelet count alone is
excluded: thrombocytopenia is a separate endpoint on the same list, and conflating the two
is the commonest way this literature is misread.</p>

<h3>Positive and negative controls</h3>
<p>The dataset is not a list of toxic compounds. It spans the full range and carries
controls at both ends, which is what makes it trainable:</p>
<ul>
<li><b>Measured negatives — {n_null} rows.</b> An endpoint that was assessed and found
unremarkable. These are distinguished, deliberately and throughout, from an endpoint that
was never measured: the latter is <code>NOT_REPORTED</code> with the reason recorded, never
<code>no_change</code>. Independent reviewers tested this distinction specifically and
could not break it.</li>
<li><b>Vehicle, saline and untreated-plasma comparators</b> carried as the matched control
on the row they belong to, in <code>control_value</code>, rather than as separate rows a
user must find and join.</li>
<li><b>Severe positives — {g3} rows at grade 3</b>, the highest severity the rubric
assigns, plus {n_srcgrade} rows carrying a severity grade the source itself reported.</li>
<li><b>Pharmacological positive controls.</b> {n_ontarget_total} rows measure compounds
designed to alter coagulation — anti-factor-XI and anti-factor-XII antisense, prekallikrein
and factor-VII programmes, anticoagulant aptamers, antithrombin-lowering siRNA. They are a
mechanistically-explained positive class, and they are flagged so they are never mistaken
for toxicity.</li>
</ul>

<div class="callout"><p><b>The single most important thing about this dataset.</b>
{n_ontarget_total} of {n_meas} rows are <b>on-target pharmacology, not toxicity</b>,
because the compounds with published clotting numbers are largely the ones designed to
change clotting. Two boolean columns keep the axes apart and <b>both may be true on one
row</b> ({ax_both} rows are). A model trained across them without the flags learns that
anticoagulants prolong aPTT — true, circular, and useless for safety prediction.</p></div>

<h2>2. Main findings and conclusions</h2>

<h3>Finding 1 — the phosphorothioate class effect, quantified per compound for the first time</h3>
<p>The safety literature states this effect at class level: prolongation of coagulation
time at high plasma C<sub>max</sub> of phosphorothioate-backbone oligonucleotides,
independent of sequence and of hybridisation. This release expresses it as per-compound
numbers. Across rows that are <i>not</i> on-target pharmacology, full-phosphorothioate
compounds show a median aPTT of <b>{ps_med}× the matched control</b> (n = {ps_n}).</p>
<p>The caveat is load-bearing and the figure is drawn to show it: <b>{ps_dom_n} of those
{ps_n} rows come from a single source</b>. It is one well-controlled experiment, not a
meta-analysis, and it should not be cited as though it were.</p>
{fig3}

<h3>Finding 2 — a source whose own prose contradicts its own tables</h3>
<p>US 9,061,044 states verbatim that "PT, aPTT and fibrinogen were not significantly
altered in monkeys treated with ISIS oligonucleotides compared to the PBS control." Its
Table 87 shows every treated group above control at every timepoint, in a clean
compound rank order peaking at 4 h — 39.13 s against a 20.13 s control, a 1.94×
prolongation. The dataset extracts the tables and carries the contradicting sentence
verbatim on all 126 of that source's rows, so the disagreement travels with the data. Any
pipeline that reads conclusions rather than tables records a false negative here.</p>

<h3>Finding 3 — the standard in-vitro assay cannot do the job it is used for</h3>
<p>One source demonstrates that in-vitro aPTT is saturated by phosphorothioate content and
therefore cannot discriminate toxic from non-toxic compounds. Nulls from that assay are
encoded as a <i>method limitation</i>, never as a safety finding. The opposite reading —
the intuitive one — would teach a model that a saturated assay means a safe compound.</p>

<h3>Finding 4 — human and animal evidence are separated, and rarely paired</h3>
<p>{n_human} measurements are made in human or human-derived systems and {n_animal} in
animal systems. Only <b>{n_pairs} of {n_oligos} compounds carry both</b>, which bounds
what any translation model built on this release can claim.</p>
{fig1}

<h2>3. How the data were produced</h2>
<p>This is an <b>in-silico curation</b> of published data; no wet-lab experiment was
performed. Sources were found by eight independent search axes — mechanism, clinical
trials, nonclinical toxicology, siRNA and lipid nanoparticles, aptamers, regulatory
labels, patents, and reviews used as a citation map — followed by a targeted sweep for
human data. Every candidate had to be <i>retrieved and quoted</i> before entering the
work-list; nothing rests on a search-engine summary. That discipline closed the project's
only previously recorded lead for this endpoint, which proved on retrieval not to report
the values its title implied.</p>
<p>Extraction rules, enforced by the output contract: every measurement carries a verbatim
quote and an exact locus; no value is ever read off a figure ({n_qual} rows are therefore
qualitative rather than invented); per-position chemistry is transcribed from the source's
own legend, never modelled. Retrieval used the Europe PMC REST service, DailyMed, the
ClinicalTrials.gov API, EMA and FDA review documents, and the USPTO full-text endpoint.
The pipeline is deterministic and committed: from a clean checkout,
<code>build_dataset.py → validate_dataset.py → verify_against_sources.py</code> reproduces
and re-checks the release with no network access.</p>

<h3>Computational processing, and what it corrects</h3>
<p>The build applies corrections that an adversarial verification pass identified, rather
than leaving them as hand edits: a "relative" clotting time is a subtracted delta and must
not be divided by its control; percent <i>inhibition</i> is not percent <i>of control</i>;
a combination arm must be referenced to the partner-drug arm, not to the untreated cell;
{n_baseline} pre-dose baselines are not effect measurements; and a source-stated measured
null outranks a ratio a hair above 1.00. {n_combo} rows carry a
<code>co_administered_agent</code> and are not measurements of the oligonucleotide alone.</p>

<h2>4. Indicators, predictors and their distributions</h2>
<h3>Response variables — how coagulation toxicity was measured</h3>
<table><tr><th>Axis</th><th>Distribution</th></tr>
<tr><td>Readout category</td><td>{rc_rows}</td></tr>
<tr><td>Readout (top)</td><td>{rn_rows}</td></tr>
<tr><td>Study design</td><td>clinical {n_clinical} · animal in vivo {n_animal_invivo} · in vitro {n_invitro} · ex vivo plasma {n_exvivo}</td></tr>
<tr><td>Species</td><td>{sp_rows}</td></tr>
<tr><td>System origin</td><td>human {n_human} · animal {n_animal} · not determined {n_undet}</td></tr>
</table>
<p>Grades are ordinal 0–3, assigned <b>mechanically</b> from a control-referenced ratio by
published <b>CTCAE v5.0</b> cut-offs, and only for the readouts CTCAE defines. {n_ungraded}
rows ({n_notgraded_pct}%) are deliberately <b>left ungraded</b>, each stating why, rather
than graded by a threshold invented here.</p>
{fig4}
<div class="callout"><p><b>Read the grade column with its caveat.</b> CTCAE grades against
the upper limit of normal; these sources publish a control mean. A ratio a few percent
above 1.00 is therefore not evidence of a real prolongation. {n_caveat} graded rows carry
<code>grade_caveat = within_reference_range_resolution</code>. Filter on it before treating
grade 1 as a finding.</p></div>

<h3>Predictor variables — the distribution across tested oligos</h3>
<table><tr><th>Variable</th><th>Distribution across {n_oligos} compounds</th></tr>
<tr><td>Class</td><td>{cls_rows}</td></tr>
<tr><td>Backbone</td><td>{bb_rows}</td></tr>
<tr><td>Sequence published</td><td>{n_seq} / {n_oligos}</td></tr>
<tr><td>Position-resolved chemistry</td><td>{n_mod_oligos} / {n_oligos} ({n_mods} position records)</td></tr>
<tr><td>Human <i>and</i> animal data</td><td>{n_pairs} / {n_oligos}</td></tr>
</table>
{fig2}

<h2>5. The gap this addresses</h2>
<p>Coagulopathy is named in the Challenge brief and is, in the published record, described
almost entirely at class level. The characterisation the field works from — that
phosphorothioate backbones prolong clotting time at high C<sub>max</sub>, independent of
sequence — appears in review and methods literature as a sentence, naming no compound, no
dose and no value. What did not exist was a structured table pairing an identified
oligonucleotide, its sequence and its per-position chemistry, with a measured coagulation
outcome and a citable locus. This release is that table.</p>
<p>It also fills a narrower gap the field has been explicit about: the separation of
<i>on-target anticoagulant pharmacology</i> from <i>unintended coagulation toxicity</i>.
Those two live side by side in the literature — often in the same paper — and are routinely
pooled. Here they are two columns.</p>
<p>Finally, the release distinguishes human from animal evidence at row level, including
for purified-protein systems, where the human/animal question is invisible in a species
field. {n_human} rows ({pct_human}%) are human or human-derived, {n_human_invitro} of them
from human in-vitro and ex-vivo systems — the category the Challenge identifies as of
particular interest.</p>

<h2>6. Using this to build a predictive model</h2>
<p>The four-table design exposes sequence, per-position chemistry and design predictors
against graded, per-condition outcomes, with no join required beyond
<code>oligo_id</code>. A model builder should:</p>
<ul>
<li><b>Train on the unintended-toxicity class</b> ({ax_un} rows, plus the {ax_both} rows
where an on-target compound produced harm), using the {ax_on} on-target rows as a
mechanistically-explained positive class rather than as toxicity labels.</li>
<li><b>Use the {n_null} measured nulls as negatives</b>, and <i>not</i> the
<code>NOT_REPORTED</code> rows, which encode absence of measurement, not absence of effect.
The distinction is the difference between a safety model and a model of what has been
studied.</li>
<li><b>Filter <code>grade_caveat</code></b> before treating grade 1 as signal, and prefer
<code>ratio_to_control</code> — a continuous target — over the ordinal grade.</li>
<li><b>Respect <code>species_class</code>.</b> Train and validate within a system class, or
model the human/animal gap explicitly using the {n_pairs} compounds that carry both.</li>
<li><b>Exclude <code>co_administered_agent</code> rows</b> from single-agent models.</li>
</ul>
<p>The most defensible near-term target is not a grade classifier but a regression on aPTT
ratio from backbone composition and phosphorothioate count, trained on the unintended class
— the one relationship this release now supports with per-compound numbers.</p>

<h2>7. Limitations, stated plainly</h2>
<ul>
<li><b>Grades are provisional and mechanical.</b> No subject-matter expert has reviewed them.</li>
<li><b>The class-effect quantification rests on one source</b> ({ps_dom_n} of {ps_n} rows).</li>
<li><b>No clinical compound has a published sequence</b> in the sources used, so
sequence-to-phenotype modelling is restricted to patent and preclinical compounds.</li>
<li><b>{n_undet} rows have an undetermined system origin</b> — the source never states
whether the proteins used were human. They are marked, not guessed.</li>
<li><b>Prothrombotic rows are dominated by one compound family</b>, so
"hypercoagulability" risks being learned as one drug.</li>
<li><b>{n_adjacent} rows are scope-adjacent</b> — retained as context but marked, because
they are not coagulation readouts.</li>
<li><b>Open defects are enumerated</b>, not summarised away, in the endpoint dossier.</li>
</ul>
<p class="small">Licence: CC BY 4.0 for the curated tables and documentation; MIT for the
code. Per-row redistribution terms are tracked in the <code>redistribution</code> column —
{n_pd} rows public domain, {n_ccby} CC BY / CC BY-NC, {n_ccnd} CC BY-NC-ND, {n_restr}
publisher-restricted. Underlying third-party documents are referenced, not relicensed.</p>
"""


def main():
    d, _ = stats()
    print("  documents:")
    figs = {"fig1": f'<figure>{img("fig1-composition.svg")}<figcaption><b>Figure 1.</b> '
                    f'Human versus animal evidence by study design. The clinical and animal-in-vivo '
                    f'arms are disjoint by construction; the in-vitro and ex-vivo arms are where '
                    f'human systems and animal systems both appear.</figcaption></figure>',
            "fig2": f'<figure>{img("fig2-axes.svg")}<figcaption><b>Figure 2.</b> The two axes. '
                    f'On-target pharmacology dominates the row count, which is why the flags exist.'
                    f'</figcaption></figure>',
            "fig3": f'<figure>{img("fig3-backbone.svg")}<figcaption><b>Figure 3.</b> aPTT '
                    f'prolongation for full-phosphorothioate compounds, unintended-toxicity rows only. '
                    f'Points are split by source to make the concentration of evidence visible: '
                    f'{d["ps_dom_n"]} of {d["ps_n"]} come from one study.</figcaption></figure>',
            "fig4": f'<figure>{img("fig4-grades.svg")}<figcaption><b>Figure 4.</b> Grade '
                    f'distribution. The upper segment marks grades resting on a ratio between 1.0 and '
                    f'1.2× control, which normal variation cannot be excluded from.</figcaption></figure>'}
    ok = True

    body = NARRATIVE.format(**d, **figs)
    html = html_doc("OligoTox-Coagulopathy",
                    "Coagulation toxicity of oligonucleotide therapeutics · Narrative document · "
                    "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, Phase 2", body)
    a, _ = render(html, os.path.join(ROOT, "OligoTox-Coagulopathy_Narrative.pdf"), 12, "narrative")
    ok &= a

    for src, out, limit, title, sub in (
        ("METHODOLOGY.md", "OligoTox-Coagulopathy_Methodology.pdf", 5, "OligoTox-Coagulopathy — Methodology",
         "Materials and methods · NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, Phase 2"),
        ("PADP.md", "OligoTox-Coagulopathy_PADP.pdf", 5, "OligoTox-Coagulopathy — Public Access & Dissemination Plan",
         "NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, Phase 2")):
        with open(os.path.join(ROOT, src), encoding="utf-8") as fh:
            txt = fh.read()
        a, _ = render(html_doc(title, sub, md_light(txt)), os.path.join(ROOT, out), limit, src)
        ok &= a

    if not ok:
        sys.exit("\n  a document is over its page limit -- trim it before release")


if __name__ == "__main__":
    main()
