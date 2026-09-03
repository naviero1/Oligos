#!/usr/bin/env python3
"""Render the narrative's figures from data/. Every value is computed here, so no figure
can state a number the dataset does not contain.

    python3 toxicity/coagulopathy/scripts/make_figures.py   ->  assets/*.svg
"""
import csv, os, re, statistics as st
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, ASSETS = os.path.join(ROOT, "data"), os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# Validated categorical palette (light mode), assigned in fixed slot order.
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#dedcd5"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.5,
    "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "svg.fonttype": "none",
})


def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def finish(fig, name):
    p = os.path.join(ASSETS, name)
    fig.savefig(p, format="svg", bbox_inches="tight", transparent=False)
    plt.close(fig)
    print(f"    {name}")


def fig_composition(D):
    """Human vs animal by study design. Two series -> legend + direct labels."""
    order = ["clinical", "animal_invivo", "in_vitro", "ex_vivo_plasma"]
    label = {"clinical": "Clinical", "animal_invivo": "Animal in vivo",
             "in_vitro": "In vitro", "ex_vivo_plasma": "Ex vivo plasma"}
    hum = [sum(1 for r in D if r["study_type"] == s and r["species_class"] == "human") for s in order]
    ani = [sum(1 for r in D if r["study_type"] == s and r["species_class"] == "animal") for s in order]
    y = range(len(order))
    fig, ax = plt.subplots(figsize=(6.4, 2.5))
    h = 0.36
    ax.barh([i + h / 2 + 0.01 for i in y], hum, height=h, color=S1, label="Human system")
    ax.barh([i - h / 2 - 0.01 for i in y], ani, height=h, color=S2, label="Animal system")
    for i, (a, b) in enumerate(zip(hum, ani)):
        if a: ax.text(a + 14, i + h / 2 + 0.01, str(a), va="center", fontsize=8, color=INK)
        if b: ax.text(b + 14, i - h / 2 - 0.01, str(b), va="center", fontsize=8, color=INK)
    ax.set_yticks(list(y)); ax.set_yticklabels([label[s] for s in order])
    ax.set_xlabel("measurements"); ax.set_xlim(0, max(hum + ani) * 1.16)
    ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    finish(fig, "fig1-composition.svg")


def fig_axes(D):
    """The on-target / unintended split. One series -> no legend."""
    cats = [("On-target\npharmacology only", "TRUE", "FALSE"),
            ("Unintended\ntoxicity only", "FALSE", "TRUE"),
            ("Both", "TRUE", "TRUE"),
            ("Neither\n(context rows)", "FALSE", "FALSE")]
    vals = [sum(1 for r in D if r["on_target_effect"] == a and r["unintended_toxicity"] == b)
            for _, a, b in cats]
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    ax.bar([c[0] for c in cats], vals, color=S1, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v + max(vals) * 0.03, str(v), ha="center", fontsize=8.5, color=INK)
    ax.set_ylabel("measurements"); ax.set_ylim(0, max(vals) * 1.18)
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    finish(fig, "fig2-axes.svg")


def fig_backbone(D, O):
    """aPTT prolongation among rows that are NOT on-target pharmacology.

    Only one backbone class reaches a usable n, so this is a distribution, not a
    comparison -- and the figure is drawn to make its own weakness visible: the points
    are split by whether they come from the single source that dominates the set."""
    om = {r["oligo_id"]: r for r in O}
    pts = []
    for r in D:
        if r["readout_name"] not in ("aPTT", "aPTT_ratio") or r["on_target_effect"] == "TRUE":
            continue
        v = fnum(r["ratio_to_control"])
        if v is None:
            continue
        bb = om[r["oligo_id"]]["backbone_chemistry"].split(" (")[0]
        if bb == "full_PS":
            pts.append((v, r["source_id"]))
    if len(pts) < 5:
        return None
    dom = Counter(s for _, s in pts).most_common(1)[0][0]
    a = [v for v, s in pts if s == dom]
    b = [v for v, s in pts if s != dom]
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    for vals, colr, yy, lab in ((a, S1, 0.10, f"one source ({dom}), n={len(a)}"),
                                (b, S2, -0.10, f"all other sources, n={len(b)}")):
        if not vals:
            continue
        ax.scatter(vals, [yy + (j % 7 - 3) * 0.012 for j in range(len(vals))],
                   s=16, color=colr, alpha=0.6, linewidths=0, label=lab)
    med = st.median([v for v, _ in pts])
    ax.plot([med, med], [-0.28, 0.28], color=INK, lw=1.6, solid_capstyle="round")
    ax.text(med, 0.33, f"median {med:.2f}", color=INK, fontsize=7.5, ha="center")
    ax.axvline(1.0, color=MUTED, lw=0.9, ls=":")
    ax.text(1.0, -0.34, " no change", color=MUTED, fontsize=7.5, va="bottom")
    ax.set_yticks([]); ax.set_ylim(-0.42, 0.46)
    ax.set_xlabel("aPTT, ratio to matched control  —  full-PS compounds, unintended-toxicity rows only")
    ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", ncol=2,
              bbox_to_anchor=(0.0, 1.22))
    finish(fig, "fig3-backbone.svg")
    return {"n": len(pts), "median": med, "dominant_source": dom, "n_dominant": len(a)}


def fig_grades(D):
    """Grade distribution, separating grades that rest on a near-unity ratio."""
    solid, caveat = [], []
    for gcode in ("0", "1", "2", "3"):
        rows = [r for r in D if r["coag_tox_grade"] == gcode]
        c = sum(1 for r in rows if r["grade_caveat"] == "within_reference_range_resolution")
        caveat.append(c); solid.append(len(rows) - c)
    x = ["grade 0", "grade 1", "grade 2", "grade 3"]
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    b1 = ax.bar(x, solid, color=S1, width=0.55, label="grade rests on a ratio > 1.2× control")
    ax.bar(x, caveat, bottom=solid, color=S3, width=0.55,
           label="flagged within_reference_range_resolution (1.0–1.2×)")
    for i, (a, b) in enumerate(zip(solid, caveat)):
        if a + b:
            ax.text(i, a + b + max(s + c for s, c in zip(solid, caveat)) * 0.03,
                    str(a + b), ha="center", fontsize=8.5, color=INK)
    ax.set_ylabel("measurements")
    ax.set_ylim(0, max(s + c for s, c in zip(solid, caveat)) * 1.2)
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    finish(fig, "fig4-grades.svg")


def main():
    D, O = load("measurements.csv"), load("oligos.csv")
    print("  figures:")
    fig_composition(D)
    fig_axes(D)
    fig_backbone(D, O)
    fig_grades(D)


if __name__ == "__main__":
    main()
