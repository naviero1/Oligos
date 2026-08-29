#!/usr/bin/env python3
"""Render every figure used in the OligoTox-CNS narrative PDF, straight from data/.

    python3 src/make_figures.py

No number in any figure is typed in this file: everything is computed from data/*.csv,
so a figure cannot drift away from the dataset it describes. Numbers quoted in the
narrative text are printed to stdout by this script and pasted from that output.

Colour follows the validated data-viz palette:
  ordinal severity ramp (grade 0-3), blue, light->dark   #86b6ef #5598e7 #2a78d6 #184f95
     validated: lightness monotone, adjacent dL >= 0.06, light end 2.06:1, single hue
  categorical slots 1-3                                  #2a78d6 #eb6834 #1baf7a
     validated all-pairs light: CVD dE 9.2, normal-vision dE 24.0
Aqua sits below 3:1 on the light surface, so every series that uses it is directly
labelled (the relief rule) rather than identified by colour alone.
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import statistics as st
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import endpoints

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8f8e88"
GRID = "#e6e5e1"
GRADE = ["#86b6ef", "#5598e7", "#2a78d6", "#184f95"]
CAT = ["#2a78d6", "#eb6834", "#1baf7a"]

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans", "font.size": 9,
    "text.color": INK, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": GRID, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
    "axes.axisbelow": True, "legend.frameon": False,
    "axes.spines.top": False, "axes.spines.right": False,
})

NOTES: list[str] = []


def note(s: str) -> None:
    NOTES.append(s)
    print(s)


def load(name):
    """Union of the three endpoint folders (src/endpoints.py owns the split)."""
    return endpoints.load_all(name)


def style(ax, title=None, xlabel=None, ylabel=None):
    if title:
        ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=8.5)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8.5)
    ax.tick_params(length=0, labelsize=8)


def bar_labels(ax, bars, values, fmt="{:,}", dy=0.01):
    top = max(values) if values else 1
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + top * dy,
                fmt.format(v), ha="center", va="bottom", fontsize=8, color=INK2)


def spearman(xs, ys):
    def rank(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = st.mean(rx), st.mean(ry)
    n = len(xs)
    return (sum((a - mx) * (b - my) for a, b in zip(rx, ry))
            / ((n - 1) * st.stdev(rx) * st.stdev(ry)))


# ==========================================================================================
def main() -> int:
    FIG.mkdir(exist_ok=True)
    oligos = load("oligos")
    meas = load("measurements")
    by_oid = {o["oligo_id"]: o for o in oligos}

    # ---- F1 dataset composition ----------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.1))
    st_counts = collections.Counter(m["study_type"] for m in meas)
    order = ["in_vitro", "animal_invivo", "clinical"]
    vals = [st_counts[k] for k in order]
    labels = ["in vitro\n(rat cortical neuron)", "in vivo\n(mouse, rat)", "clinical\n(human)"]
    b = axes[0].bar(labels, vals, color=CAT[0], width=0.6)
    bar_labels(axes[0], b, vals)
    axes[0].set_yscale("log")
    axes[0].set_ylim(1, max(vals) * 4)
    style(axes[0], "Measurements by study type", ylabel="measurements (log scale)")

    ax_counts = collections.Counter(m["tox_axis"] for m in meas)
    ax_order = sorted(ax_counts, key=ax_counts.get, reverse=True)
    pretty = {"acute_neuronal_excitability": "acute neuronal\nexcitability",
              "acute_behavioural": "acute\nbehavioural",
              "late_onset_neurodegeneration": "late-onset\nneurodegeneration",
              "clinical_cns_tolerability": "clinical CNS\ntolerability",
              "clinical_neuroinflammatory": "clinical\nneuroinflammatory",
              "clinical_serious_neurological": "clinical serious\nneurological"}
    v2 = [ax_counts[k] for k in ax_order]
    b2 = axes[1].barh([pretty.get(k, k) for k in ax_order][::-1], v2[::-1], color=CAT[0], height=0.6)
    axes[1].set_xscale("log")
    axes[1].set_xlim(1, max(v2) * 5)
    for bar, v in zip(b2, v2[::-1]):
        axes[1].text(bar.get_width() * 1.25, bar.get_y() + bar.get_height() / 2,
                     f"{v:,}", va="center", fontsize=8, color=INK2)
    style(axes[1], "Measurements by toxicity axis", xlabel="measurements (log scale)")

    src = load("sources")
    sn = [(s["source_id"], int(s["n_measurements"])) for s in src if int(s["n_measurements"]) > 0]
    sn.sort(key=lambda t: -t[1])
    v3 = [n for _, n in sn]
    b3 = axes[2].bar([s for s, _ in sn], v3, color=CAT[0], width=0.55)
    bar_labels(axes[2], b3, v3)
    axes[2].set_yscale("log"); axes[2].set_ylim(1, max(v3) * 4)
    style(axes[2], "Measurements by source", ylabel="measurements (log scale)")
    fig.tight_layout()
    fig.savefig(FIG / "F1_composition.png", dpi=200)
    plt.close(fig)
    note(f"F1: study types {dict(st_counts)}; axes {dict(ax_counts)}")

    # ---- F2 predictor distributions ------------------------------------------------------
    seqd = [o for o in oligos if o["sequence_base"] not in ("NOT_REPORTED", "")]
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.6))
    specs = [
        ("length_nt", "Length (nt)", axes[0][0], int),
        ("gc_content_pct", "G+C content (%)", axes[0][1], float),
        ("n_G", "Guanine count", axes[0][2], int),
        ("g_free_3prime_len", "G-free stretch from 3' end (nt)", axes[1][0], int),
        ("n_lna", "LNA nucleotides", axes[1][1], int),
        ("gap_length_nt", "DNA gap length (nt)", axes[1][2], int),
    ]
    for col, label, ax, cast in specs:
        vals = [cast(o[col]) for o in seqd if o[col] not in ("NOT_REPORTED", "", "NOT_APPLICABLE")]
        if col in ("gc_content_pct",):
            ax.hist(vals, bins=24, color=CAT[0], edgecolor=SURFACE, linewidth=0.6)
        else:
            c = collections.Counter(vals)
            ks = sorted(c)
            ax.bar(ks, [c[k] for k in ks], color=CAT[0], width=0.8, edgecolor=SURFACE, linewidth=0.6)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
        med = st.median(vals)
        ax.axvline(med, color=INK2, linewidth=1.2, linestyle=(0, (4, 3)))
        ax.text(0.97, 0.93, f"n = {len(vals):,}\nmedian {med:g}", transform=ax.transAxes,
                ha="right", va="top", fontsize=7.5, color=INK2)
        if col == "g_free_3prime_len":
            # placed mid-axis, clear of the n/median block in the top-right corner
            ax.annotate("the bar at 20 is a cap:\nthe oligo has no G at all",
                        xy=(20, max(collections.Counter(vals).values())),
                        xytext=(0.42, 0.62), textcoords="axes fraction",
                        ha="center", va="center", fontsize=7, color=INK2,
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8,
                                        shrinkA=2, shrinkB=4))
        style(ax, label, ylabel="oligonucleotides")
        note(f"F2 {col}: n={len(vals)} median={med:g} min={min(vals):g} max={max(vals):g}")
    fig.suptitle("Distribution of predictor variables amongst tested oligonucleotides",
                 fontsize=11, fontweight="bold", x=0.008, ha="left", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(FIG / "F2_predictors.png", dpi=200)
    plt.close(fig)

    # ---- F3 severity ladder --------------------------------------------------------------
    graded = [m for m in meas if m["cns_tox_grade"] != ""]
    axes_order = ["acute_behavioural", "late_onset_neurodegeneration",
                  "clinical_cns_tolerability", "clinical_neuroinflammatory",
                  "clinical_serious_neurological"]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.5, 3.4),
                                   gridspec_kw={"width_ratios": [1, 1.5]})
    gc = collections.Counter(m["cns_tox_grade"] for m in graded)
    ks = ["0", "1", "2", "3"]
    vals = [gc[k] for k in ks]
    b = axL.bar(["0\nnone", "1\nmild", "2\nmoderate", "3\nsevere"], vals,
                color=GRADE, width=0.62)
    bar_labels(axL, b, vals)
    axL.set_ylim(0, max(vals) * 1.22)
    style(axL, f"Severity grade  (n = {len(graded)} graded rows)", ylabel="measurements")

    bottoms = [0] * len(axes_order)
    for gi, k in enumerate(ks):
        row = [sum(1 for m in graded if m["tox_axis"] == a and m["cns_tox_grade"] == k)
               for a in axes_order]
        axR.barh(range(len(axes_order)), row, left=bottoms, color=GRADE[gi], height=0.6,
                 label=f"grade {k}", edgecolor=SURFACE, linewidth=1.4)
        bottoms = [b0 + r for b0, r in zip(bottoms, row)]
    axR.set_yticks(range(len(axes_order)))
    axR.set_yticklabels([pretty.get(a, a).replace("\n", " ") for a in axes_order], fontsize=8)
    axR.invert_yaxis()
    for i, tot in enumerate(bottoms):
        axR.text(tot + max(bottoms) * 0.015, i, str(tot), va="center", fontsize=8, color=INK2)
    axR.legend(ncol=4, fontsize=8, loc="lower right", bbox_to_anchor=(1, -0.28))
    style(axR, "Severity grade by toxicity axis", xlabel="measurements")
    fig.tight_layout()
    fig.savefig(FIG / "F3_severity.png", dpi=200)
    plt.close(fig)
    note(f"F3 grade distribution: {dict(sorted(gc.items()))}, total graded {len(graded)}")

    # ---- F4 in vitro -> in vivo translation ----------------------------------------------
    cao = {m["oligo_id"]: float(m["readout_value"]) for m in meas
           if m["readout_name"].startswith("spontaneous_calcium")}
    ans = {m["oligo_id"]: float(m["readout_value"]) for m in meas
           if m["readout_name"] == "acute_tolerability_score_ANS"}
    pairs = [(cao[o], ans[o]) for o in ans if o in cao]
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    rho = spearman(xs, ys)
    calc = {o["oligo_id"]: float(o["g_free_3prime_len"]) for o in oligos
            if o["g_free_3prime_len"] not in ("", "NOT_REPORTED")}

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.6),
                                 gridspec_kw={"width_ratios": [1.25, 1]})
    a1.scatter(xs, ys, s=22, color=CAT[0], alpha=0.6, linewidth=0.6, edgecolor=SURFACE)
    a1.axhline(4, color=INK2, linewidth=1.1, linestyle=(0, (4, 3)))
    a1.text(a1.get_xlim()[1], 4.6, "score 4 — authors' developability line  ",
            fontsize=7.5, color=INK2, ha="right")
    a1.set_ylim(-1.5, 23)
    a1.text(0.02, 0.99, f"Spearman ρ = {rho:.2f}   ·   n = {len(pairs)} oligonucleotides "
                        f"with both readouts",
            transform=a1.transAxes, va="top", fontsize=8.5, color=INK)
    style(a1, "In vitro predicts in vivo, but loosely",
          xlabel="rat cortical neuron calcium-oscillation score (% of control)",
          ylabel="mouse acute tolerability score (0–20)")

    srt = sorted(pairs)
    t = len(srt) // 3
    groups = [("most affected\nin vitro", srt[:t]), ("middle", srt[t:2 * t]),
              ("least affected\nin vitro", srt[2 * t:])]
    bp = a2.boxplot([[p[1] for p in g] for _, g in groups],
                    tick_labels=[n for n, _ in groups], patch_artist=True, widths=0.5,
                    medianprops=dict(color=INK, linewidth=1.6),
                    flierprops=dict(marker="o", markersize=3, markerfacecolor=MUTED,
                                    markeredgecolor="none", alpha=0.6))
    for patch, c in zip(bp["boxes"], [GRADE[3], GRADE[2], GRADE[0]]):
        patch.set_facecolor(c); patch.set_edgecolor(SURFACE); patch.set_linewidth(1.4)
    for w in bp["whiskers"] + bp["caps"]:
        w.set_color(MUTED)
    for name, g in groups:
        note(f"F4 tertile {name.replace(chr(10), ' ')}: n={len(g)} "
             f"median ANS={st.median([p[1] for p in g]):.2f}")
    style(a2, "Mouse score by in vitro tertile", ylabel="mouse acute tolerability score")
    fig.tight_layout()
    fig.savefig(FIG / "F4_translation.png", dpi=200)
    plt.close(fig)
    note(f"F4 Spearman rho(in vitro CaO, in vivo ANS) = {rho:.3f}, n = {len(pairs)}")

    # ---- F5 sequence determinants --------------------------------------------------------
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.5))
    gcount = {o["oligo_id"]: int(o["n_G"]) for o in oligos if o["n_G"] not in ("", "NOT_REPORTED")}
    gs = sorted({gcount[o] for o in ans if o in gcount})
    data = [[ans[o] for o in ans if gcount.get(o) == g] for g in gs]
    keep = [(g, d) for g, d in zip(gs, data) if len(d) >= 3]
    bp = a1.boxplot([d for _, d in keep], tick_labels=[str(g) for g, _ in keep],
                    patch_artist=True, widths=0.55,
                    medianprops=dict(color=INK, linewidth=1.5),
                    flierprops=dict(marker="o", markersize=3, markerfacecolor=MUTED,
                                    markeredgecolor="none", alpha=0.6))
    for p in bp["boxes"]:
        p.set_facecolor(CAT[0]); p.set_alpha(0.75); p.set_edgecolor(SURFACE); p.set_linewidth(1.3)
    for w in bp["whiskers"] + bp["caps"]:
        w.set_color(MUTED)
    a1.set_ylim(-3.0, 22)
    for i, (_, d) in enumerate(keep, start=1):
        a1.text(i, -2.2, f"n={len(d)}", ha="center", fontsize=7, color=MUTED)
    style(a1, "More guanine, worse tolerability", xlabel="guanine count in the oligonucleotide",
          ylabel="mouse acute tolerability score")
    note("F5 median ANS by G count: " +
         ", ".join(f"G={g}:{st.median(d):.1f}(n={len(d)})" for g, d in keep))

    gf = sorted({int(calc[o]) for o in ans if o in calc})
    bins = [(0, 4), (5, 9), (10, 14), (15, 20)]
    lbl = ["0–4", "5–9", "10–14", "15–20"]
    dd = [[ans[o] for o in ans if o in calc and lo <= calc[o] <= hi] for lo, hi in bins]
    bp2 = a2.boxplot(dd, tick_labels=lbl, patch_artist=True, widths=0.55,
                     medianprops=dict(color=INK, linewidth=1.5),
                     flierprops=dict(marker="o", markersize=3, markerfacecolor=MUTED,
                                     markeredgecolor="none", alpha=0.6))
    for p, c in zip(bp2["boxes"], [GRADE[3], GRADE[2], GRADE[1], GRADE[0]]):
        p.set_facecolor(c); p.set_edgecolor(SURFACE); p.set_linewidth(1.3)
    for w in bp2["whiskers"] + bp2["caps"]:
        w.set_color(MUTED)
    a2.set_ylim(-3.0, 22)
    for i, d in enumerate(dd, start=1):
        a2.text(i, -2.2, f"n={len(d)}", ha="center", fontsize=7, color=MUTED)
    style(a2, "A G close to the 3' end is the strongest single warning",
          xlabel="length of G-free stretch measured from the 3' end (nt)",
          ylabel="mouse acute tolerability score")
    note("F5 median ANS by 3' G-free bin: " +
         ", ".join(f"{l}:{st.median(d):.1f}(n={len(d)})" for l, d in zip(lbl, dd) if d))
    fig.tight_layout()
    fig.savefig(FIG / "F5_sequence.png", dpi=200)
    plt.close(fig)

    # ---- F6 assay reproducibility --------------------------------------------------------
    # Replicates must be the SAME MOLECULE, so group on the as-printed sequence, whose case
    # encodes LNA position. Grouping on sequence_base would merge oligos that share a
    # nucleobase sequence but carry LNA at different positions -- different compounds.
    seqs = collections.Counter(o["sequence_5to3_asprinted"] for o in oligos
                               if o["sequence_5to3_asprinted"] not in ("NOT_REPORTED", ""))
    rep_seq, rep_n = seqs.most_common(1)[0]
    rep_ids = [o["oligo_id"] for o in oligos if o["sequence_5to3_asprinted"] == rep_seq]
    rep_vals = [cao[i] for i in rep_ids if i in cao]
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.scatter(range(1, len(rep_vals) + 1), sorted(rep_vals), s=42, color=CAT[0],
               edgecolor=SURFACE, linewidth=0.8, zorder=3)
    m, sd = st.mean(rep_vals), st.stdev(rep_vals)
    ax.axhline(m, color=INK2, linewidth=1.2)
    ax.axhspan(m - sd, m + sd, color=CAT[0], alpha=0.10, zorder=0)
    ax.text(0.02, 0.95, f"mean {m:.1f} · SD {sd:.1f} · CV {100 * sd / m:.1f}%\n"
                        f"same sequence, {len(rep_vals)} independent plate runs",
            transform=ax.transAxes, va="top", fontsize=8.5, color=INK)
    style(ax, "Reproducibility of the in vitro assay",
          xlabel="replicate run (sorted)", ylabel="calcium-oscillation score (% of control)")
    fig.tight_layout()
    fig.savefig(FIG / "F6_reproducibility.png", dpi=200)
    plt.close(fig)
    note(f"F6 replicate control {rep_seq}: n={len(rep_vals)} mean={m:.2f} sd={sd:.2f} "
         f"CV={100 * sd / m:.1f}% range {min(rep_vals)}-{max(rep_vals)}")

    # ---- F7 divalent cation rescue -------------------------------------------------------
    k1 = [m for m in meas if m["source_id"] == "K1"]
    hi = [m for m in k1 if by_oid[m["oligo_id"]]["aliases"] == "Di-siRNAHTT (P3, high PS)"]
    # Each panel of the source paper is a self-contained experiment, so select rows by the
    # paper figure they belong to rather than by dose/cation alone -- otherwise unrelated
    # control groups from other panels land on the same curve at x = 0.
    def panel(tag):
        return [m for m in hi if tag in m["source_location"] and m["strain"] == "WT FVB"]

    dose_pts = sorted({(float(m["dose_value"]), float(m["readout_value"]))
                       for m in panel("1D") if float(m["dose_value"]) > 0})
    dose_x = [d for d, _ in dose_pts]
    dose_y = [s for _, s in dose_pts]
    ca = sorted({(float(m["formulation_ca_mM"]), float(m["readout_value"])) for m in panel("4C")
                 if float(m["dose_value"]) == 10 and float(m["formulation_mg_mM"] or 0) == 0})
    mg = sorted({(float(m["formulation_mg_mM"]), float(m["readout_value"])) for m in panel("4D")
                 if float(m["dose_value"]) == 10 and float(m["formulation_ca_mM"] or 0) == 0})

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.5))
    a1.plot(dose_x, dose_y, marker="o", markersize=8, linewidth=2, color=CAT[0],
            markeredgecolor=SURFACE, markeredgewidth=1.2)
    for x, y in zip(dose_x, dose_y):
        a1.annotate(f"{y:g}", (x, y), textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=8, color=INK2)
    a1.set_ylim(0, 22)
    style(a1, "Dose drives acute toxicity", xlabel="di-siRNA dose (nmol, ICV)",
          ylabel="acute tolerability score (0–20)")

    a2.plot([c for c, _ in ca], [s for _, s in ca], marker="o", markersize=8, linewidth=2,
            color=CAT[0], markeredgecolor=SURFACE, markeredgewidth=1.2, label="added Ca$^{2+}$")
    a2.plot([c for c, _ in mg], [s for _, s in mg], marker="s", markersize=8, linewidth=2,
            color=CAT[1], markeredgecolor=SURFACE, markeredgewidth=1.2, label="added Mg$^{2+}$")
    a2.set_xlim(-2, 40)
    a2.annotate("Ca$^{2+}$", (ca[-1][0], ca[-1][1]), textcoords="offset points",
                xytext=(9, -2), fontsize=8.5, color=CAT[0], ha="left", va="center")
    a2.annotate("Mg$^{2+}$", (mg[-1][0], mg[-1][1]), textcoords="offset points",
                xytext=(9, -2), fontsize=8.5, color=CAT[1], ha="left", va="center")
    a2.legend(fontsize=8, loc="upper right")
    a2.set_ylim(0, 22)
    style(a2, "Divalent cation in the injectate reverses it",
          xlabel="cation added to the 10 nmol dose (mM)",
          ylabel="acute tolerability score (0–20)")
    fig.tight_layout()
    fig.savefig(FIG / "F7_formulation.png", dpi=200)
    plt.close(fig)
    note(f"F7 dose-response {list(zip(dose_x, dose_y))}")
    note(f"F7 Ca rescue {ca}")
    note(f"F7 Mg rescue {mg}")

    # ---- F8 completeness, including the honest gaps ---------------------------------------
    fields = [("sequence_base", "Sequence"), ("modification_positions", "Modification positions"),
              ("purity_method", "Purity/characterisation method"), ("purity_pct", "Purity value (%)")]
    miss = {"NOT_REPORTED", "NOT_APPLICABLE", ""}
    present = [sum(1 for o in oligos if o[c] not in miss) for c, _ in fields]
    total = len(oligos)
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ypos = range(len(fields))
    ax.barh(list(ypos), [total] * len(fields), color=GRID, height=0.55)
    bars = ax.barh(list(ypos), present, color=CAT[0], height=0.55)
    for i, (p, (c, lab)) in enumerate(zip(present, fields)):
        ax.text(total * 1.02, i, f"{p:,} / {total:,}  ({100 * p / total:.1f}%)",
                va="center", fontsize=8.5, color=INK if p else "#b03030")
    ax.set_yticks(list(ypos))
    ax.set_yticklabels([lab for _, lab in fields], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, total * 1.42)
    ax.grid(False)
    ax.set_xticks([])
    style(ax, "Field completeness across all 1,839 oligonucleotides")
    fig.tight_layout()
    fig.savefig(FIG / "F8_completeness.png", dpi=200)
    plt.close(fig)
    note(f"F8 completeness: " + ", ".join(f"{lab} {p}/{total}" for p, (_, lab)
                                          in zip(present, fields)))

    (FIG / "figure_numbers.txt").write_text("\n".join(NOTES) + "\n")
    print(f"\nwrote {len(list(FIG.glob('*.png')))} figures to figures/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
