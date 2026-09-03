#!/usr/bin/env python3
"""
Predictive analysis of the hydrocephalus endpoint.

This script is deliberately conservative about what it claims. The endpoint is
rare: 9 of 526 trial arms report a tier-A (ventricular) event. Nine events will
not support a sequence-to-toxicity classifier, and presenting one would be
misleading. What the data does support is:

  1. Risk stratification by DELIVERY ROUTE, with exact confidence intervals and
     an exact test, at both arm and participant level.
  2. A modellable secondary outcome — tier B, CSF-dynamics disturbance — which
     occurs in 78 arms and is the mechanistic precursor the index case
     documents.
  3. A LEAKAGE TEST that quantifies how much of any apparent performance comes
     from provenance rather than biology. This is run because a review of the
     sibling kidney dataset found study_type and source_id were strong shortcut
     predictors of its label, and the same hazard applies here.

Validation is leave-one-COMPOUND-out, not random k-fold: arms of the same
compound are correlated, so a random split leaks the compound across folds and
inflates the score.

Outputs: ml/ML_REPORT.md, ml/results.json, ml/figures/*.png
Usage:   python3 ml/analyse.py   (after ml/build_analysis_set.py)
"""
import json
import os
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

INK, MUTED, ACCENT, WARN = "#1F2933", "#7B8794", "#2C6E9B", "#B4551F"


def wilson(k, n):
    if n == 0:
        return (0.0, 0.0)
    lo, hi = stats.binomtest(k, n).proportion_ci(confidence_level=0.95,
                                                 method="wilson")
    return lo, hi


def main():
    df = pd.read_csv(os.path.join(HERE, "analysis_set.csv"))
    R = {}

    R["n_arms"] = int(len(df))
    R["n_trials"] = int(df.nct_id.nunique())
    R["n_compounds"] = int(df.oligo_name.nunique())
    R["n_participants"] = int(df.n_at_risk.sum())
    R["n_armsA"] = int(df.tierA_event.sum())
    R["n_armsB"] = int(df.tierB_event.sum())

    # ---- 1. route stratification, arm level and participant level ----------
    def block(sub, label):
        arms, ev = len(sub), int(sub.tierA_event.sum())
        pa, pn = int(sub.tierA_affected.sum()), int(sub.n_at_risk.sum())
        lo, hi = wilson(pa, pn)
        return dict(label=label, arms=arms, arms_with_event=ev,
                    participants=pn, participants_affected=pa,
                    rate_per_1000=1000.0 * pa / pn if pn else 0.0,
                    ci_lo_per_1000=1000 * lo, ci_hi_per_1000=1000 * hi)

    cns = df[df.route_is_cns == 1]
    sys_ = df[(df.route_is_cns == 0) & (df.delivery_route != "NOT_REPORTED")]
    R["route"] = [block(cns, "CNS-delivered (intrathecal / ICV)"),
                  block(sys_, "Systemically delivered")]

    tbl = [[int(cns.tierA_affected.sum()),
            int(cns.n_at_risk.sum() - cns.tierA_affected.sum())],
           [int(sys_.tierA_affected.sum()),
            int(sys_.n_at_risk.sum() - sys_.tierA_affected.sum())]]
    odds, p = stats.fisher_exact(tbl)
    R["route_fisher"] = dict(odds_ratio=float(odds), p_value=float(p),
                             table=tbl)

    # ---- 2. per-compound observed tier-A rates -----------------------------
    g = df.groupby("oligo_name").agg(
        arms=("tierA_event", "size"), arms_with_event=("tierA_event", "sum"),
        affected=("tierA_affected", "sum"), at_risk=("n_at_risk", "sum"),
        cns=("route_is_cns", "max")).reset_index()
    g["rate_per_1000"] = 1000 * g.affected / g.at_risk
    g[["lo", "hi"]] = g.apply(
        lambda r: pd.Series([1000 * x for x in wilson(int(r.affected), int(r.at_risk))]),
        axis=1)
    R["by_compound"] = g.sort_values("rate_per_1000", ascending=False).head(14).to_dict("records")

    # ---- 3. within-trial comparator contrast -------------------------------
    # The strongest design available: treated and placebo arms of the SAME trial.
    pairs = []
    for nct, sub in df.groupby("nct_id"):
        tre, com = sub[sub.is_comparator == 0], sub[sub.is_comparator == 1]
        if len(com) == 0 or len(tre) == 0:
            continue
        pairs.append(dict(nct=nct,
                          treated_aff=int(tre.tierA_affected.sum()),
                          treated_n=int(tre.n_at_risk.sum()),
                          ctrl_aff=int(com.tierA_affected.sum()),
                          ctrl_n=int(com.n_at_risk.sum()),
                          cns=int(sub.route_is_cns.max())))
    P = pd.DataFrame(pairs)
    R["paired_trials"] = int(len(P))
    R["paired_treated_events"] = int(P.treated_aff.sum())
    R["paired_ctrl_events"] = int(P.ctrl_aff.sum())
    R["paired_treated_n"] = int(P.treated_n.sum())
    R["paired_ctrl_n"] = int(P.ctrl_n.sum())
    mt = stats.fisher_exact([[P.treated_aff.sum(), P.treated_n.sum() - P.treated_aff.sum()],
                             [P.ctrl_aff.sum(), P.ctrl_n.sum() - P.ctrl_aff.sum()]])
    R["paired_fisher"] = dict(odds_ratio=float(mt[0]), p_value=float(mt[1]))

    # ---- 4. modellable outcome: tier B, with honest validation -------------
    def design(frame, cols):
        X = pd.get_dummies(frame[cols].astype(str), drop_first=False)
        return X.astype(float), list(X.columns)

    def loco(frame, y, cols):
        """Leave-one-compound-out CV. Random folds would leak the compound."""
        preds, truth = [], []
        for comp in frame.oligo_name.unique():
            te = frame.oligo_name == comp
            tr = ~te
            if y[tr].nunique() < 2 or te.sum() == 0:
                continue
            Xtr, names = design(frame[tr], cols)
            Xte, _ = design(frame[te], cols)
            Xte = Xte.reindex(columns=names, fill_value=0.0)
            mdl = LogisticRegression(max_iter=2000, class_weight="balanced", C=1.0)
            mdl.fit(Xtr, y[tr])
            preds.extend(mdl.predict_proba(Xte)[:, 1])
            truth.extend(y[te].tolist())
        if len(set(truth)) < 2:
            return None, len(truth)
        return roc_auc_score(truth, preds), len(truth)

    yB = df.tierB_event
    models = {
        "route only": ["delivery_route"],
        "route + indication": ["delivery_route", "indication"],
        "route + indication + chemistry": ["delivery_route", "indication",
                                           "oligo_class", "backbone_chemistry"],
        "LEAKAGE PROBE: trial identity only": ["nct_id"],
        "LEAKAGE PROBE: compound identity only": ["oligo_name"],
    }
    R["models"] = []
    for name, cols in models.items():
        auc, n = loco(df, yB, cols)
        R["models"].append(dict(name=name, features=cols,
                                auc=None if auc is None else round(float(auc), 3),
                                n_scored=n))

    # bootstrap CI for the best legitimate model
    best = ["delivery_route", "indication"]
    aucs = []
    rng = np.random.default_rng(0)
    for _ in range(300):
        idx = rng.choice(len(df), len(df), replace=True)
        sub = df.iloc[idx].reset_index(drop=True)
        a, _n = loco(sub, sub.tierB_event, best)
        if a is not None:
            aucs.append(a)
    if aucs:
        R["best_model_auc_ci"] = [round(float(np.percentile(aucs, 2.5)), 3),
                                  round(float(np.percentile(aucs, 97.5)), 3)]

    # ---- figures -----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    lab = [b["label"].replace(" (", "\n(") for b in R["route"]]
    val = [b["rate_per_1000"] for b in R["route"]]
    err = [[b["rate_per_1000"] - b["ci_lo_per_1000"] for b in R["route"]],
           [b["ci_hi_per_1000"] - b["rate_per_1000"] for b in R["route"]]]
    ax.barh(lab, val, color=[ACCENT, MUTED], height=.5)
    ax.errorbar(val, lab, xerr=err, fmt="none", ecolor=INK, capsize=4, lw=1.2)
    for i, b in enumerate(R["route"]):
        ax.text(b["ci_hi_per_1000"] + max(val) * .03, i,
                "%d/%s" % (b["participants_affected"], f"{b['participants']:,}"),
                va="center", fontsize=9, color=INK)
    ax.set_xlabel("Tier-A (ventricular) events per 1,000 participants at risk\n"
                  "bars are 95% Wilson intervals", fontsize=9)
    ax.set_title("Route stratifies the ventricular endpoint", fontsize=11,
                 color=INK, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "route_rate.png"), dpi=200)
    plt.close(fig)

    top = pd.DataFrame(R["by_compound"]).head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    cols = [ACCENT if c else MUTED for c in top.cns]
    ax.barh(top.oligo_name, top.rate_per_1000, color=cols, height=.6)
    ax.errorbar(top.rate_per_1000, top.oligo_name,
                xerr=[top.rate_per_1000 - top.lo, top.hi - top.rate_per_1000],
                fmt="none", ecolor=INK, capsize=3, lw=1)
    ax.set_xlabel("Tier-A events per 1,000 participants (95% Wilson)", fontsize=9)
    ax.set_title("Per-compound observed rate — blue = CNS-delivered",
                 fontsize=11, color=INK, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "by_compound.png"), dpi=200)
    plt.close(fig)

    mods = [m for m in R["models"] if m["auc"] is not None]
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    names = [m["name"] for m in mods][::-1]
    vals = [m["auc"] for m in mods][::-1]
    cols = [WARN if "LEAKAGE" in n else ACCENT for n in names]
    ax.barh(names, vals, color=cols, height=.55)
    ax.axvline(.5, color=MUTED, ls="--", lw=1)
    for i, v in enumerate(vals):
        ax.text(v + .01, i, "%.2f" % v, va="center", fontsize=9, color=INK)
    ax.set_xlim(0, 1); ax.set_xlabel("Leave-one-compound-out AUC, tier-B outcome",
                                     fontsize=9)
    ax.set_title("Orange bars are provenance leakage probes, not models",
                 fontsize=11, color=INK, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "model_auc.png"), dpi=200)
    plt.close(fig)

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(R, fh, indent=1, default=str)

    print("arms %(n_arms)d | trials %(n_trials)d | compounds %(n_compounds)d | "
          "participants %(n_participants)d" % R)
    print("tier-A arms %(n_armsA)d | tier-B arms %(n_armsB)d" % R)
    for b in R["route"]:
        print("  %-38s %d/%d = %.2f per 1,000 (%.2f-%.2f)"
              % (b["label"], b["participants_affected"], b["participants"],
                 b["rate_per_1000"], b["ci_lo_per_1000"], b["ci_hi_per_1000"]))
    print("  Fisher OR %.2f, p = %.3g" % (R["route_fisher"]["odds_ratio"],
                                          R["route_fisher"]["p_value"]))
    print("  within-trial: treated %d/%d vs comparator %d/%d, OR %.2f p=%.3g"
          % (R["paired_treated_events"], R["paired_treated_n"],
             R["paired_ctrl_events"], R["paired_ctrl_n"],
             R["paired_fisher"]["odds_ratio"], R["paired_fisher"]["p_value"]))
    for m in R["models"]:
        print("  %-40s AUC %s (n=%d)" % (m["name"], m["auc"], m["n_scored"]))


if __name__ == "__main__":
    main()
