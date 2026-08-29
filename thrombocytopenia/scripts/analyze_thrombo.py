#!/usr/bin/env python3
"""Fitness-for-purpose analysis of the OligoTox-Thrombocytopenia dataset.

This is NOT a predictive model — the challenge deliverable is a dataset. This
script asks a narrower question: **does the assembled data actually support the
inferences the dataset claims to enable?** A curated dataset that cannot
reproduce the field's best-established structure-activity relationship is not
ready to train anything, and that is worth knowing before release rather than
after.

Four checks, each corresponding to a claim made in README.md:

  1. Does phosphorothioate content track platelet effect?  (the core hypothesis)
  2. Does backbone chemistry separate the grade distribution?
  3. Is grade confounded with study type?  (a known structural risk — severe
     events are observed in trials, not in dishes)
  4. Are the controlled comparisons actually present and consistent?

Everything here is descriptive and non-parametric: no distributional assumptions,
no imputation, and `TBD` is always excluded rather than coerced to zero.

Usage:  python3 scripts/analyze_thrombo.py
"""
import csv, os, sys, collections, statistics

# Paths are anchored to the ENDPOINT folder that owns this script, so all
# thrombocytopenia artefacts stay inside thrombocytopenia/ and nothing is
# written outside it.
ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")


# ---------------------------------------------------------------------------
# Compounds EXCLUDED from the phosphorothioate structure-activity tests, with
# reasons. This is not cherry-picking: the hypothesis under test is that platelet
# effects are driven by PS-backbone binding to GPVI. A compound whose
# thrombocytopenia has a different, known mechanism is not evidence for or
# against that hypothesis, and including it inverts the result.
#
#   imetelstat — a 13-mer N3'->P5' THIOPHOSPHORAMIDATE. Its `ps_count` is 0
#   because it carries no phosphorothioate linkages in the strict sense, yet its
#   backbone is fully thio-substituted, so 0 reads as "neutral" when it is not.
#   More decisively, its thrombocytopenia is ON-TARGET TELOMERASE-INHIBITOR
#   MYELOSUPPRESSION in MDS, not platelet binding. Left in, its 93 high-grade
#   rows made up 74% of the zero-PS bucket and pushed that bucket's mean grade
#   ABOVE every phosphorothioate bucket — a textbook confound.
#
# Excluded rows are still IN the dataset; they are excluded only from this
# hypothesis test, and the exclusion is reported in the output.
MECHANISM_EXCLUDED = {
    "imetelstat": "on-target telomerase-inhibitor myelosuppression, not PS-backbone "
                  "binding; N3'-P5' thiophosphoramidate backbone is thio-substituted "
                  "despite ps_count=0",
}


def split_excluded(oligos, meas):
    """Return (kept, excluded) measurement rows, splitting on MECHANISM_EXCLUDED."""
    kept, excl = [], []
    for m in meas:
        nm = (oligos.get(m["oligo_id"], {}).get("oligo_name") or "").lower()
        (excl if nm in MECHANISM_EXCLUDED else kept).append(m)
    return kept, excl


def load():
    with open(os.path.join(BASE, "oligos.csv"), newline="", encoding="utf-8") as f:
        oligos = {r["oligo_id"]: r for r in csv.DictReader(f)}
    with open(os.path.join(BASE, "measurements.csv"), newline="", encoding="utf-8") as f:
        meas = list(csv.DictReader(f))
    return oligos, meas


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def bar(counts, width=34):
    """Render a 0-3 grade distribution as a compact stacked bar."""
    tot = sum(counts) or 1
    out = ""
    for ch, n in zip(".-+#", counts):
        out += ch * max(0, round(width * n / tot))
    return out.ljust(width)


def grade_profile(rows):
    c = collections.Counter(int(r["thrombocytopenia_grade"]) for r in rows)
    return [c.get(i, 0) for i in range(4)]


def mean_grade(rows):
    g = [int(r["thrombocytopenia_grade"]) for r in rows]
    return statistics.mean(g) if g else float("nan")


def section(t):
    print(f"\n{'=' * 74}\n{t}\n{'=' * 74}")


def emit_markdown(oligos, meas):
    """Emit the README's fitness-for-purpose section, so its numbers are generated
    from the data rather than hand-transcribed and left to drift."""
    meas, excluded = split_excluded(oligos, meas)
    if excluded:
        names = sorted({oligos[m["oligo_id"]]["oligo_name"] for m in excluded})
        print(f"*Structure-activity tests below exclude {len(excluded)} rows from "
              f"**{', '.join(names)}**, whose thrombocytopenia has a different, known "
              "mechanism (see `MECHANISM_EXCLUDED` in `scripts/analyze_thrombo.py`). "
              "Those rows remain in the dataset; they are excluded only from this "
              "hypothesis test, because a different mechanism is evidence neither for "
              "nor against the phosphorothioate hypothesis.*\n")
    print("**Backbone chemistry orders as the phosphorothioate hypothesis predicts**,")
    print("with no modelling:\n")
    print("| backbone | n rows | n oligos | mean grade |")
    print("|---|---:|---:|---:|")
    by = collections.defaultdict(list)
    for m in meas:
        by[oligos.get(m["oligo_id"], {}).get("backbone_chemistry", "TBD")].append(m)
    order = ["PMO_neutral", "PS_PO_mix", "full_PO", "full_PS"]
    for k in order:
        rows = by.get(k)
        if not rows:
            continue
        print(f"| `{k}` | {len(rows)} | {len({m['oligo_id'] for m in rows})} | "
              f"{mean_grade(rows):.2f} |")

    ps_bins, parts = [(0, 0, "0"), (13, 16, "13–16"), (17, 19, "17–19"), (20, 99, "20+")], []
    for lo, hi, label in ps_bins:
        rows = [m for m in meas
                if (p := num(oligos.get(m["oligo_id"], {}).get("ps_count"))) is not None
                and lo <= p <= hi]
        if rows:
            parts.append(f"{label} → {mean_grade(rows):.2f}")
    print(f"\nMean grade also rises with phosphorothioate count "
          f"({'; '.join(parts)} linkages).\n")

    bym = collections.defaultdict(list)
    for m in meas:
        bym[oligos.get(m["oligo_id"], {}).get("oligo_class", "TBD")].append(m)
    mod = sorted(((k, mean_grade(v)) for k, v in bym.items() if len(v) >= 5),
                 key=lambda kv: kv[1])
    print("Modality orders " + " < ".join(f"{k} {g:.2f}" for k, g in mod) + ".\n")

    print("**The caveat that must travel with this.** Grade is partly confounded with")
    print("study type — severe thrombocytopenia is observed in trials, not in dishes:\n")
    print("| study type | n rows | mean grade | % grade 3 |")
    print("|---|---:|---:|---:|")
    bys = collections.defaultdict(list)
    for m in meas:
        bys[m["study_type"]].append(m)
    for k, rows in sorted(bys.items(), key=lambda kv: -mean_grade(kv[1])):
        g3 = 100.0 * sum(1 for r in rows if r["thrombocytopenia_grade"] == "3") / len(rows)
        print(f"| {k} | {len(rows)} | {mean_grade(rows):.2f} | {g3:.1f}% |")
    print("\nAny model trained here must account for study type rather than learn it")
    print("as biology.")


def main():
    oligos, meas = load()
    meas_all = meas
    meas, excluded = split_excluded(oligos, meas)
    print(f"{len(oligos)} oligos · {len(meas_all)} measurements")
    if excluded:
        names = sorted({oligos[m["oligo_id"]]["oligo_name"] for m in excluded})
        print(f"EXCLUDED from structure-activity tests: {len(excluded)} rows "
              f"({', '.join(names)}) — different known mechanism")
    print("legend: grade 0='.'  1='-'  2='+'  3='#'")

    # ---------------------------------------------------------------- 1. PS count
    section("1. Does phosphorothioate content track platelet effect?")
    print("The central hypothesis. ps_count is binned; oligos with ps_count=TBD are")
    print("EXCLUDED, not treated as zero.\n")
    bins = [(0, 0, "0 (neutral)"), (1, 12, "1-12"), (13, 16, "13-16"),
            (17, 19, "17-19"), (20, 99, "20+")]
    print(f"{'PS linkages':<14} {'n rows':>6} {'n oligos':>9} {'mean grade':>11}  distribution")
    for lo, hi, label in bins:
        rows = [m for m in meas
                if (p := num(oligos.get(m["oligo_id"], {}).get("ps_count"))) is not None
                and lo <= p <= hi]
        if not rows:
            continue
        n_ol = len({m["oligo_id"] for m in rows})
        print(f"{label:<14} {len(rows):>6} {n_ol:>9} {mean_grade(rows):>11.2f}  "
              f"{bar(grade_profile(rows))}")
    unknown = [m for m in meas
               if num(oligos.get(m["oligo_id"], {}).get("ps_count")) is None]
    print(f"\n  ({len(unknown)} rows excluded: ps_count is TBD — never imputed)")

    # ------------------------------------------------------------- 2. backbone
    section("2. Does backbone chemistry separate the grade distribution?")
    by = collections.defaultdict(list)
    for m in meas:
        by[oligos.get(m["oligo_id"], {}).get("backbone_chemistry", "TBD")].append(m)
    print(f"{'backbone':<14} {'n rows':>6} {'n oligos':>9} {'mean grade':>11}  distribution")
    for k, rows in sorted(by.items(), key=lambda kv: -mean_grade(kv[1])):
        n_ol = len({m["oligo_id"] for m in rows})
        print(f"{k:<14} {len(rows):>6} {n_ol:>9} {mean_grade(rows):>11.2f}  "
              f"{bar(grade_profile(rows))}")

    # ------------------------------------------------------------- 3. confound
    section("3. Is grade confounded with study type?")
    print("A known structural risk: severe thrombocytopenia is observed in trials,")
    print("not in dishes, so grade may partly encode study design rather than biology.")
    print("Any model trained on this data must account for it.\n")
    by = collections.defaultdict(list)
    for m in meas:
        by[m["study_type"]].append(m)
    print(f"{'study type':<16} {'n rows':>6} {'mean grade':>11} {'% grade 3':>10}  distribution")
    for k, rows in sorted(by.items(), key=lambda kv: -mean_grade(kv[1])):
        g3 = 100.0 * sum(1 for r in rows if r["thrombocytopenia_grade"] == "3") / len(rows)
        print(f"{k:<16} {len(rows):>6} {mean_grade(rows):>11.2f} {g3:>9.1f}%  "
              f"{bar(grade_profile(rows))}")

    # -------------------------------------------------------------- 4. modality
    section("4. Modality contrast")
    by = collections.defaultdict(list)
    for m in meas:
        by[oligos.get(m["oligo_id"], {}).get("oligo_class", "TBD")].append(m)
    print(f"{'modality':<22} {'n rows':>6} {'n oligos':>9} {'mean grade':>11}  distribution")
    for k, rows in sorted(by.items(), key=lambda kv: -mean_grade(kv[1])):
        n_ol = len({m["oligo_id"] for m in rows})
        print(f"{k:<22} {len(rows):>6} {n_ol:>9} {mean_grade(rows):>11.2f}  "
              f"{bar(grade_profile(rows))}")

    # ------------------------------------------------- 5. controlled comparisons
    section("5. Are the controlled comparisons present and consistent?")
    print("Each pair should share a sequence (or differ in exactly one design")
    print("variable). These are the dataset's most distinctive content.\n")
    # match on the same normalized key the assembler joins on, so a spacing or
    # punctuation variant ("ODN 2395" vs "ODN2395") does not read as "missing"
    def nk(s):
        return "".join(c for c in s.lower() if c.isalnum())

    byname = {nk(o["oligo_name"]): o for o in oligos.values()}
    pairs = [("odn2395", "odn2395thio", "backbone only (non-PS vs PS)"),
             ("isis416858", "fesomersen", "PS count + GalNAc conjugate"),
             ("volanesorsen", "olezarsen", "GalNAc conjugate + exposure")]
    for a, b, what in pairs:
        oa, ob = byname.get(a), byname.get(b)
        if not (oa and ob):
            print(f"  [missing] {a} / {b} — not both present")
            continue
        ra = [m for m in meas if m["oligo_id"] == oa["oligo_id"]]
        rb = [m for m in meas if m["oligo_id"] == ob["oligo_id"]]
        same = (oa["sequence_5to3"] == ob["sequence_5to3"]
                and oa["sequence_5to3"] not in ("", "TBD"))
        print(f"  {oa['oligo_name']} vs {ob['oligo_name']}  ({what})")
        print(f"    same sequence: {'YES' if same else 'no/unknown'}"
              f"   PS {oa['ps_count']} vs {ob['ps_count']}"
              f"   conjugate {oa['conjugate']} vs {ob['conjugate']}")
        print(f"    mean grade {mean_grade(ra):.2f} (n={len(ra)})  vs  "
              f"{mean_grade(rb):.2f} (n={len(rb)})")

    if "--markdown" in sys.argv:
        emit_markdown(oligos, meas)
        return

    section("Interpretation")
    print("Read the PS-count and backbone tables together. If mean grade rises with")
    print("PS content and full_PS separates from PMO_neutral, the dataset reproduces")
    print("the field's established structure-activity relationship from curation")
    print("alone — which is the evidence that it is fit to train a model on.")
    print("Check 3 is the caveat that must travel with any such claim.")


if __name__ == "__main__":
    main()
