#!/usr/bin/env python3
"""Source-verified corrections to the OligoTox-Kidney canonical tables.

Two classes of fix, both carried over from the companion CNS round where each
caught a real defect. Neither invents a value: one rewrites a reference into a
resolvable form, the other reads a right out of the document that grants it.

Idempotent — safe to re-run.

Usage:  python scripts/corrections_kidney.py [--dry-run]
"""
import csv
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEAS = os.path.join(ROOT, "data", "measurements.csv")
LICENCES = os.path.join(ROOT, "toxicity", "notes", "kidney", "source_licences.json")

# ---------------------------------------------------------------------------
# K1. Make every source reference RESOLVABLE.
#
# References were stored as human-readable slugs — `Moisan2017_PMC5363415`,
# `vanPoelgeest2013_10.1111_bcp.12738`, `NEJM2018_NEJMoa1716793`. They carry a
# real identifier inside, but not in a form anything can follow, so a reader
# cannot re-verify a row in one lookup and the same document can appear under
# several spellings. Each `;`-separated component is rewritten to its canonical
# identifier where one is embedded, and left alone where none is. The multi-source
# structure is preserved rather than collapsed, because a row citing both a label
# and a review genuinely rests on both, and the reference as originally written is
# kept in `notes`.
# ---------------------------------------------------------------------------
# NB: \b is wrong here. These identifiers are embedded in underscore-joined
# slugs (`Moisan2017_PMC5363415`), and `_` is a word character, so there is no
# word boundary between it and `PMC` — a \b-anchored pattern silently matches
# nothing and the whole canonicalisation quietly no-ops. Anchor on "not preceded
# by an alphanumeric" instead, which treats `_` as the separator it is.
NOTALNUM_B = r"(?<![A-Za-z0-9])"
NOTALNUM_A = r"(?![A-Za-z0-9])"
PMC_RE = re.compile(NOTALNUM_B + r"PMC(\d{6,8})" + NOTALNUM_A, re.I)
PMID_RE = re.compile(NOTALNUM_B + r"PMID[:_ ]?(\d{6,9})" + NOTALNUM_A, re.I)
PAT_RE = re.compile(NOTALNUM_B + r"US\s?(\d{7,8})\s?([AB]\d?)?" + NOTALNUM_A, re.I)
NCT_RE = re.compile(NOTALNUM_B + r"(NCT\d{8})" + NOTALNUM_A, re.I)
# DOIs were slugified with the '/' replaced by '_', e.g. 10.1111_bcp.12738
DOI_SLUG_RE = re.compile(NOTALNUM_B + r"(10\.\d{4,9})[_/]([A-Za-z0-9][^\s;]*)")
# NEJM article ids are not DOIs but map onto one deterministically.
NEJM_RE = re.compile(NOTALNUM_B + r"(NEJM(?:oa|ra|c|e|p)\d{6,7})" + NOTALNUM_A)


def canon_component(c):
    c = c.strip()
    if not c:
        return c
    m = NCT_RE.search(c)
    if m:
        return m.group(1).upper()
    m = PAT_RE.search(c)
    if m:
        return "US" + m.group(1) + (m.group(2) or "").upper()
    m = DOI_SLUG_RE.search(c)
    if m:
        return "doi:%s/%s" % (m.group(1), m.group(2).rstrip(".,;"))
    m = NEJM_RE.search(c)
    if m:
        return "doi:10.1056/" + m.group(1)
    m = PMC_RE.search(c)
    if m:
        return "PMC" + m.group(1)
    m = PMID_RE.search(c)
    if m:
        return "PMID:" + m.group(1)
    return c


def canon_ref(ref):
    parts = [canon_component(p) for p in str(ref or "").split(";")]
    seen, out = set(), []
    for p in parts:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return ";".join(out)


# ---------------------------------------------------------------------------
# K2. Assert redistribution from the licence the source actually grants.
#
# 64 of 111 rows were `summary_stat` by assumption. Several cite plain CC-BY
# articles, which expressly permit reproducing raw values with attribution — a
# materially stronger right, and the one that lets a whole per-oligo panel be
# republished verbatim. It is tracked separately rather than conservatively
# flattened. CC-BY-NC and CC-BY-ND sources are deliberately NOT upgraded:
# republishing their tables inside a CC-BY dataset would conflict with the
# non-commercial and no-derivatives terms.
# ---------------------------------------------------------------------------
def main():
    dry = "--dry-run" in sys.argv
    lic = {k: v for k, v in json.load(open(LICENCES, encoding="utf-8")).items()
           if not k.startswith("_")}

    with open(MEAS, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        cols = list(rows[0].keys())

    stats = Counter()
    for r in rows:
        original = (r["source_ref"] or "").strip()
        canon = canon_ref(original)
        if canon != original and "source_ref_as_cited=" not in (r["notes"] or ""):
            r["source_ref"] = canon
            r["notes"] = (r["notes"] + ";" if r["notes"] else "") + \
                "source_ref_as_cited=" + original
            stats["K1_source_ref_canonicalised"] += 1

        # rights: a row inherits cc_by only if EVERY licence-bearing source it
        # cites is plain CC-BY. A row resting partly on a non-commercial source
        # cannot be republished under CC-BY terms.
        pmcs = PMC_RE.findall(r["source_ref"] + " " + (r["notes"] or ""))
        known = [lic.get("PMC" + p) for p in pmcs if lic.get("PMC" + p)]
        if known and all(k == "by" for k in known) and \
                r["redistribution"] in ("summary_stat", "derived_features_only",
                                        "verify"):
            r["redistribution"] = "cc_by"
            r["notes"] += ";redistribution_upgraded_to_cc_by_from_source_licence_statement"
            stats["K2_rights_upgraded_to_cc_by"] += 1

    if not dry:
        with open(MEAS, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)

    for k in sorted(stats):
        print("%-34s %d rows" % (k, stats[k]))
    if not stats:
        print("no rows matched - corrections already applied?")
    if dry:
        print("(dry run - nothing written)")


if __name__ == "__main__":
    main()
