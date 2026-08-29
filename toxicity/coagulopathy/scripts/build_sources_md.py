#!/usr/bin/env python3
"""Regenerate SOURCES.md from data/sources.csv (the source of truth).

    python3 toxicity/coagulopathy/scripts/build_sources_md.py
"""
import csv, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = list(csv.DictReader(open(os.path.join(ROOT, "data", "sources.csv"))))
S.sort(key=lambda r: -int(r["n_measurements"]))
out = open(os.path.join(ROOT, "SOURCES.md")).read().split("## Registry")[0]
rows = ["## Registry\n",
        "| ID | Rows | Oligos | Source | Identifier | Redistribution |",
        "|---|---:|---:|---|---|---|"]
for r in S:
    cit = r["citation"].replace("|", "/")
    cit = (cit[:110] + "…") if len(cit) > 110 else cit
    ident = r["identifier"].replace("|", "/")
    ident = (ident[:46] + "…") if len(ident) > 46 else ident
    rows.append(f"| `{r['source_id']}` | {r['n_measurements']} | {r['n_oligos']} | {cit} | {ident} | `{r['redistribution']}` |")
tail = open(os.path.join(ROOT, "SOURCES.md")).read().split("## Not used as a source of rows")
print("regenerated registry section:", len(S), "sources")
open(os.path.join(ROOT, "SOURCES.md"), "w").write(out + "\n".join(rows) + "\n\n## Not used as a source of rows" + tail[1])
