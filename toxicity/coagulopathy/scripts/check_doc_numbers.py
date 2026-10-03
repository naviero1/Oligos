#!/usr/bin/env python3
"""Fail the release if a document asserts a count the data does not support.

    python3 toxicity/coagulopathy/scripts/check_doc_numbers.py

Why this exists. On 2026-10-03 five documents -- METHODOLOGY.md, PADP.md, README.md,
STATUS.md and schema.md -- still asserted "213 oligonucleotides, 2,388 measurements, 941
per-position modification records" against an actual 218 / 2,685 / 1,039, and the
methodology's distribution table named a `study_type` value that had been renamed for
encoding a species. Those numbers were typed by hand into prose and nothing re-checked
them, so every rebuild of the dataset silently widened the gap between the dataset and the
documents that describe it. A submission whose narrative contradicts its own tables is
worse than one that says less.

Two defences, because they catch different mistakes:

  1. SUPERSEDED VALUES. Each count that has ever been published is listed with the value
     that replaced it. If a superseded number reappears next to its own noun, the build
     fails and names the file and line. This catches a stale paragraph that nobody
     remembered to update.
  2. LIVE VALUES. Each current count must appear at least once, in the thousands-separated
     form a reader sees. This catches a document that quietly dropped a required figure.

The right long-term fix is a marker, not a check: METHODOLOGY.md and PADP.md now carry
`<!--N:key-->` placeholders that build_documents.py fills from the tables at build time, so
their numbers cannot drift at all. README.md, STATUS.md and schema.md are read directly on
GitHub rather than rendered, so they keep literal numbers and this check guards them.
"""
import csv, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
# SOURCES.md was missing from this list on 2026-10-03, which is why its header shipped
# "75 sources - 2388 measurements" against an actual 100 and 2,685 until Crank caught it.
# A guard with an incomplete file list is a guard that reports clean while the defect ships.
DOCS = ["METHODOLOGY.md", "PADP.md", "README.md", "STATUS.md", "schema.md", "coagulopathy.md",
        "SOURCES.md", "ROCKSTEADY_RESEARCH_REPORT_2026-10-02.md"]
# Dated correspondence is an archive of what was said on a date, not a current claim, so it
# is out of scope here and carries a superseded-figures banner instead. Checking it would
# force either rewriting history or exempting whole files from the guard.
ARCHIVE = ["ROCKSTEADY_REVIEW_REPLY_2026-10-01.md", "ROCKSTEADY_RESPONSE_TO_BEEBOP.md"]


def load(n):
    p = os.path.join(DATA, n)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []


def main():
    O, D, M, S = load("oligos.csv"), load("measurements.csv"), load("modifications.csv"), load("sources.csv")
    ST = load("studies.csv")
    head = [r for r in ST if r.get("headline_trial") == "TRUE"]

    live = {
        "oligonucleotides": len(O),
        "measurements": len(D),
        "modification records": len(M),
        "sources": len(S),
        "headline trials": len(head),
        "compounds with per-position chemistry": len({m["oligo_id"] for m in M}),
    }
    # value that is current -> values it replaced, with the noun they sit beside
    # Every value that has ever been published for one of these counts. Crank's 2026-10-03
    # delegation named four this guard did not know about -- the source count, the
    # modification-record count over its oligo count, and the published-sequence count --
    # which is the difference between a guard that catches a class of defect and one that
    # catches the three instances somebody happened to remember.
    superseded = {
        "oligonucleotides|compounds": (len(O), [213]),
        "measurements|rows": (len(D), [2388]),
        "modification": (len(M), [941]),
        "sources?": (len(S), [75]),
        "trials": (len(head), [30, 65]),
        "oligos": (len({m["oligo_id"] for m in M}), [47]),
    }

    fails = []
    for doc in DOCS:
        p = os.path.join(ROOT, doc)
        if not os.path.exists(p):
            continue
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            # a line that is explicitly about the history of a corrected number is allowed to
            # name the old one; it is the retraction, not a stale claim.
            if re.search(r"retract|superseded|was an under-count|previously|replaces|until 2026|"
                         r"corrected|was wrong|had drifted|earlier release|stale", line, re.I):
                continue
            for nouns, (now, old) in superseded.items():
                for o in old:
                    pat = r"\b" + f"{o:,}".replace(",", "[,]?") + r"\b[^.|]{0,60}?\b(" + nouns + r")\b"
                    if re.search(pat, line, re.I) and str(now) not in line:
                        fails.append(f"{doc}:{i}: superseded count {o:,} beside '{nouns}' "
                                     f"(current value is {now:,})\n      {line.strip()[:150]}")

    missing = []
    joined = "\n".join(open(os.path.join(ROOT, d), encoding="utf-8").read()
                       for d in DOCS if os.path.exists(os.path.join(ROOT, d)))
    for label, v in live.items():
        if f"{v:,}" not in joined and str(v) not in joined:
            missing.append(f"no document states the current {label} count ({v:,})")

    for a in ARCHIVE:
        q = os.path.join(ROOT, a)
        if os.path.exists(q) and "Superseded figures" not in open(q, encoding="utf-8").read():
            fails.append(f"{a}: dated correspondence carries no superseded-figures banner")

    for f in fails:
        print(f"  FAIL  {f}")
    for m in missing:
        print(f"  WARN  {m}")
    if fails:
        sys.exit(f"\n  {len(fails)} document figures contradict the data -- fix them before release")
    print(f"  document figures agree with the data "
          f"({len(O)} compounds · {len(D):,} measurements · {len(M):,} modification records · "
          f"{len(head)} headline trials)")


if __name__ == "__main__":
    main()
