#!/usr/bin/env python3
"""A worked baseline: predict in vivo CNS tolerability from sequence alone, using only the
released CSVs.

    python3 src/baseline_model.py

This exists so that the narrative document's claim -- that the dataset is sufficient to train a
useful predictor -- is demonstrated rather than asserted. It deliberately uses the source's own
train/test split (`dataset_split_asPublished`), so the held-out set is the one the original
authors held out: the 19 STC1-targeting ASOs, a different target gene from the 1,806 MAPT/control
ASOs used for fitting. That is a genuine generalisation test, not a random split.

Three models are compared on the same held-out set:
  1. the linear model published by Hagedorn et al., transcribed from their Supplementary Methods
  2. the measured in vitro calcium-oscillation score, used directly as a predictor
  3. a logistic regression fitted here on richer sequence features from oligos.csv

Label: acute tolerability score > 4, i.e. the authors' own "not suitable for further
development" line.
"""
from __future__ import annotations

import csv
import json
import pathlib
import statistics as st
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import endpoints

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

FEATURES = ["length_nt", "gc_content_pct", "n_A", "n_C", "n_G", "n_T",
            "longest_g_run", "g_free_3prime_len", "n_lna", "gap_length_nt",
            "flank5_len_nt", "flank3_len_nt"]


def load():
    oligos = {o["oligo_id"]: o for o in endpoints.load_all("oligos")}
    meas = endpoints.load_all("measurements")
    ans = {m["oligo_id"]: float(m["readout_value"]) for m in meas
           if m["readout_name"] == "acute_tolerability_score_ANS"}
    cao = {m["oligo_id"]: float(m["readout_value"]) for m in meas
           if m["readout_name"].startswith("spontaneous_calcium")}
    rows = []
    for oid, score in ans.items():
        o = oligos[oid]
        # The 12-feature vector needs a defined DNA gap length, which mixmers do not have.
        # Those rows are still kept: the sequence-only comparisons below use all of them, and
        # only the fitted logistic regression is restricted to the complete-feature subset.
        feat_ok = all(o[f] not in ("", "NOT_REPORTED", "NOT_APPLICABLE") for f in FEATURES)
        rows.append({"oid": oid, "split": o["dataset_split_asPublished"],
                     "y": 1 if score > 4 else 0, "ans": score,
                     "cao": cao.get(oid), "feat_ok": feat_ok,
                     "x": [float(o[f]) for f in FEATURES] if feat_ok else None,
                     "seq": o["sequence_base"]})
    return rows


def published_score(seq: str) -> float:
    s = seq.lower()
    pos = [i for i, ch in enumerate(s) if ch == "g"]
    g3 = 20 if not pos else min(20, len(s) - 1 - max(pos))
    return (136.0430 - 3.1263 * s.count("a") - 5.1100 * s.count("c")
            - 4.7217 * s.count("t") - 10.1264 * s.count("g") + 1.3577 * g3)


def auc(scores, labels):
    """Rank-based AUC. `scores` should be higher = more likely positive."""
    pairs = sorted(zip(scores, labels))
    ranks, i = {}, 0
    vals = [p[0] for p in pairs]
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[i]:
            j += 1
        for k in range(i, j + 1):
            ranks[k] = (i + j) / 2 + 1
        i = j + 1
    pos = [ranks[k] for k, (_, lab) in enumerate(pairs) if lab == 1]
    n1, n0 = len(pos), len(pairs) - len(pos)
    if n1 == 0 or n0 == 0:
        return float("nan")
    return (sum(pos) - n1 * (n1 + 1) / 2) / (n1 * n0)


def fit_logistic(X, y, epochs=4000, lr=0.08, l2=1e-3):
    """Plain gradient-descent logistic regression on standardised features -- no dependency
    beyond the standard library, so this runs anywhere the dataset does."""
    n, d = len(X), len(X[0])
    mu = [st.mean(col) for col in zip(*X)]
    sd = [st.pstdev(col) or 1.0 for col in zip(*X)]
    Z = [[(v - mu[j]) / sd[j] for j, v in enumerate(row)] for row in X]
    w, b = [0.0] * d, 0.0
    for _ in range(epochs):
        gw, gb = [0.0] * d, 0.0
        for zi, yi in zip(Z, y):
            z = b + sum(wj * zj for wj, zj in zip(w, zi))
            p = 1 / (1 + pow(2.718281828459045, -max(-30, min(30, z))))
            e = p - yi
            for j in range(d):
                gw[j] += e * zi[j]
            gb += e
        w = [wj - lr * (gw[j] / n + l2 * wj) for j, wj in enumerate(w)]
        b -= lr * gb / n
    return (w, b, mu, sd)


def predict(model, X):
    w, b, mu, sd = model
    out = []
    for row in X:
        z = b + sum(wj * ((v - mu[j]) / sd[j]) for j, (wj, v) in enumerate(zip(w, row)))
        out.append(1 / (1 + pow(2.718281828459045, -max(-30, min(30, z)))))
    return out


def metrics(scores, y, thr):
    tp = sum(1 for s, t in zip(scores, y) if s >= thr and t == 1)
    tn = sum(1 for s, t in zip(scores, y) if s < thr and t == 0)
    fp = sum(1 for s, t in zip(scores, y) if s >= thr and t == 0)
    fn = sum(1 for s, t in zip(scores, y) if s < thr and t == 1)
    return {"accuracy": (tp + tn) / len(y), "tp": tp, "tn": tn, "fp": fp, "fn": fn}


def main() -> int:
    rows = load()
    train = [r for r in rows if r["split"] in ("Test", "Control", "Training") and r["feat_ok"]]
    held = [r for r in rows if r["split"] == "Validate" and r["feat_ok"]]
    print(f"rows with an in vivo score                       : {len(rows)}")
    print(f"  of which the 12-feature vector is complete     : "
          f"{sum(1 for r in rows if r['feat_ok'])}")
    print(f"  fitting set   (Test/Control/Training, MAPT + controls) : {len(train)}"
          f"   positives {sum(r['y'] for r in train)}")
    print(f"  held-out set  (Validate, STC1 -- a different target)   : {len(held)}"
          f"   positives {sum(r['y'] for r in held)}")
    print()

    yh = [r["y"] for r in held]

    # 1 -- the published linear model. Higher score = safer, so negate for AUC.
    pub = [-published_score(r["seq"]) for r in held]
    a_pub = auc(pub, yh)
    m_pub = metrics([-p for p in pub], [1 - v for v in yh], 70)  # published cutoff 70 = safe
    acc_pub = sum(1 for r in held if (published_score(r["seq"]) > 70) == (r["y"] == 0)) / len(held)

    # 2 -- the measured in vitro assay. Lower calcium score = more toxic, so negate.
    have_cao = [r for r in held if r["cao"] is not None]
    a_cao = auc([-r["cao"] for r in have_cao], [r["y"] for r in have_cao])

    # 3 -- logistic regression on richer sequence features
    model = fit_logistic([r["x"] for r in train], [r["y"] for r in train])
    ph = predict(model, [r["x"] for r in held])
    a_lr = auc(ph, yh)
    m_lr = metrics(ph, yh, 0.5)

    print("held-out performance (n = %d, positives = %d)" % (len(held), sum(yh)))
    print(f"  published linear model (sequence only) : AUC {a_pub:.3f}   "
          f"accuracy at published cutoff 70 = {acc_pub:.1%}")
    print(f"  measured in vitro calcium score        : AUC {a_cao:.3f}   (n = {len(have_cao)})")
    print(f"  logistic regression, 12 seq features   : AUC {a_lr:.3f}   "
          f"accuracy at 0.5 = {m_lr['accuracy']:.1%}   {m_lr}")
    print()

    # whole-dataset correlation, for context
    both = [r for r in rows if r["cao"] is not None]   # every in vivo row, feature-complete or not
    print(f"across all {len(both)} oligos with both readouts:")
    print(f"  AUC of the sequence model vs the ANS>4 label   : "
          f"{auc([-published_score(r['seq']) for r in both], [r['y'] for r in both]):.3f}")
    print(f"  AUC of the measured in vitro score             : "
          f"{auc([-r['cao'] for r in both], [r['y'] for r in both]):.3f}")

    out = {
        "n_rows": len(rows), "n_rows_featok": sum(1 for r in rows if r["feat_ok"]),
        "n_train": len(train), "n_held": len(held),
        "held_positives": sum(yh),
        "auc_published_linear": round(a_pub, 3),
        "acc_published_cutoff70": round(acc_pub, 6),
        "auc_measured_invitro": round(a_cao, 3),
        "auc_logistic_12feat": round(a_lr, 3),
        "acc_logistic": round(m_lr["accuracy"], 6),
        "n_both": len(both),
        "auc_all_published_linear": round(auc([-published_score(r["seq"]) for r in both],
                                              [r["y"] for r in both]), 3),
        "auc_all_measured_invitro": round(auc([-r["cao"] for r in both],
                                              [r["y"] for r in both]), 3),
    }
    (ROOT / "figures" / "baseline_model.json").write_text(json.dumps(out, indent=2))
    print("\nwrote figures/baseline_model.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
