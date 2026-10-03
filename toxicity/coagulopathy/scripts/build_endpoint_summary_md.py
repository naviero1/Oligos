#!/usr/bin/env python3
"""Regenerate the two summary tables in coagulopathy.md from the data.

    python3 toxicity/coagulopathy/scripts/build_endpoint_summary_md.py

Why this exists. On 2026-10-03 Crank's answer 3 refused to generalise
`check_doc_numbers.py` until its matcher was fixed, because the pattern required
number-then-noun and could not cross a markdown pipe: "in a table the noun precedes the
number. It therefore misses stale figures in table form, including ones live in
coagulopathy.md right now." That was exactly right, and the cost was this file's entire
headline table -- 213 oligos, 2,388 measurement rows, 867 graded, 1,521 ungraded, QC 45/45
and 1,876 verified values, every one of them stale, with the guard reporting clean. One of
its distribution rows still named `ex vivo human plasma`, a `study_type` value renamed
because it encoded a species.

Hand-typed tables drift. These two are generated between markers, like SOURCES.md's header,
so the summary of the endpoint cannot disagree with the endpoint.
"""
import csv, os, re, subprocess, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "coagulopathy.md")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"


def load(n):
    p = os.path.join(ROOT, "data", n)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []


def main():
    O, D, M, S = load("oligos.csv"), load("measurements.csv"), load("modifications.csv"), load("sources.csv")
    ST = load("studies.csv")
    head = [r for r in ST if r.get("headline_trial") == "TRUE"]
    nf = lambda v: v and v not in (NR, NA, "")

    qc = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "validate_dataset.py")],
                        capture_output=True, text=True)
    m = re.search(r"(\d+)/(\d+) checks pass", qc.stdout or "")
    checks = f"{m.group(1)} / {m.group(2)} pass" if m else "see validate_dataset.py"

    ver = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "verify_against_sources.py")],
                         capture_output=True, text=True)
    vm = re.search(r"(\d[\d,]*)/(\d[\d,]*) checkable numeric values", ver.stdout or "")
    vals = f"{vm.group(1)} / {vm.group(2)}" if vm else "see verify_against_sources.py"

    g = Counter(r["coag_tox_grade"] for r in D)
    graded = sum(g.get(k, 0) for k in "0123")
    seq = sum(1 for o in O if nf(o["sequence_base"]))

    t1 = [
        "| | Value | Source of the figure |",
        "|---|---|---|",
        f"| Unique oligonucleotides | {len(O):,} | `data/oligos.csv` ({len(O)} x {len(O[0])}) |",
        f"| Measurement rows | {len(D):,} | `data/measurements.csv` ({len(D)} x {len(D[0])}) |",
        f"| Per-position modification records | {len(M):,} over {len({r['oligo_id'] for r in M})} oligonucleotides | `data/modifications.csv` |",
        f"| Source documents | {len(S)}, all with the cited document committed | `data/sources.csv`, `sources/documents/` |",
        f"| Sequences published | {seq} of {len(O)} | `sequence_base` not `NOT_REPORTED`/`NOT_APPLICABLE` |",
        f"| Verified human interventional trials | {len(head)} ({sum(1 for r in head if r['identity_basis']=='registry_number')} registry-identified) | `data/studies.csv`, `headline_trial` |",
        f"| Graded rows | {graded:,} (0/1/2/3 = {g.get('0',0)}/{g.get('1',0)}/{g.get('2',0)}/{g.get('3',0)}) | `coag_tox_grade`; {g.get(NR,0):,} ungraded, each with a stated reason |",
        f"| Structural QC | {checks} | `scripts/validate_dataset.py`, exits non-zero on failure |",
        f"| Numeric values found in their cited source | {vals} | `scripts/verify_against_sources.py` |",
    ]

    def dist(label, counter, n=9, sep=" · "):
        items = [f"{k.replace('_',' ')} {v:,}" for k, v in counter.most_common(n) if k not in (NA,)]
        return f"| {label} | {sep.join(items)} |"

    ax = lambda a, b: sum(1 for r in D if r["on_target_effect"] == a and r["unintended_toxicity"] == b)
    t2 = [
        "| Axis | Distribution |",
        "|---|---|",
        dist("Study type", Counter(r["study_type"] for r in D)),
        dist("Species", Counter(r["species"] for r in D), 8),
        dist("System origin", Counter(r["species_class"] for r in D)),
        dist("Human system subtype", Counter(r["human_system_subtype"] for r in D)),
        dist("Readout category", Counter(r["readout_category"] for r in D)),
        dist("Effect direction", Counter(r["effect_direction"] for r in D)),
        dist("Evidence class", Counter(r["evidence_class"] for r in D)),
        dist("Control class", Counter(r["control_class"] for r in D)),
        f"| Axis flags | on-target only {ax('TRUE','FALSE'):,} · unintended only {ax('FALSE','TRUE'):,} · both {ax('TRUE','TRUE'):,} · neither {ax('FALSE','FALSE'):,} |",
        dist("Redistribution", Counter(r["redistribution"] for r in D)),
    ]

    txt = open(DOC, encoding="utf-8").read()
    for marker, block in (("SUMMARY_TABLE", t1), ("DISTRIBUTION_TABLE", t2)):
        pat = re.compile(r"<!--BEGIN:" + marker + r"-->.*?<!--END:" + marker + r"-->", re.S)
        new = f"<!--BEGIN:{marker}-->\n" + "\n".join(block) + f"\n<!--END:{marker}-->"
        if pat.search(txt):
            txt = pat.sub(new, txt)
        else:
            print(f"  WARNING: marker {marker} not present in coagulopathy.md; nothing replaced")
    open(DOC, "w", encoding="utf-8").write(txt)
    print(f"  regenerated coagulopathy.md summary tables: {len(O)} oligos · {len(D):,} rows · "
          f"{len(head)} trials · QC {checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
