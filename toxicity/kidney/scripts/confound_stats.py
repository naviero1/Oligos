#!/usr/bin/env python3
"""Compute the provenance/outcome confound. Computed, never asserted.

History, because it matters for how this is read. The first version of this analysis
claimed the confound "weakened 3.7x" after three label-derived rows were added. An
adversarial review showed that was self-refuting twice over:

  1. "3.7x" was a P-VALUE RATIO, not an effect size.
  2. The replacement -- a risk difference moving 57.9 -> 50.0 pp -- moved for exactly
     and only the reason the p-ratio was disqualified: three rows entering the
     anchored arm's DENOMINATOR. The unverified arm is bit-identical before and
     after (0 of 20 reach grade >= 2 both ways), so no new information about the
     association was added at all.
  3. Worse, those three rows (MSR160/162/164) are reclassified by this same release
     as asserted_negative_regulatory -- NOT measured negatives -- and gated out of
     modelling. A weakening claim resting on rows the release declares unfit is not
     a finding.

So the honest report is NO MEASURABLE WEAKENING, and the confound is reported on
rows that pass negative_eligibility rather than on raw grades.

Usage:  python scripts/confound_stats.py
"""
import csv, os
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = [r for r in csv.DictReader(open(os.path.join(ROOT, "data", "measurements.csv"), newline=""))
     if r["study_type"] == "clinical"]

def fisher_one_sided(a, b, c, d):
    def p(a, b, c, d):
        return comb(a + b, a) * comb(c + d, c) / comb(a + b + c + d, a + c)
    tot = 0.0
    for i in range(0, min(a + b, a + c) + 1):
        j, k = a + b - i, a + c - i
        l = c + d - k
        if j < 0 or k < 0 or l < 0:
            continue
        if i <= a:
            tot += p(i, j, k, l)
    return tot

def table(rows, label):
    ws = [r for r in rows if r["source_id"] == "WS"]
    an = [r for r in rows if r["source_id"] != "WS"]
    a = sum(1 for r in ws if r["nephrotox_grade"] in "23"); b = len(ws) - a
    c = sum(1 for r in an if r["nephrotox_grade"] in "23"); d = len(an) - c
    if not (a + b) or not (c + d):
        print(f"\n{label}: insufficient rows"); return
    rd = c / (c + d) - a / (a + b)
    print(f"\n{label}")
    print(f"  unverified (WS)  {a:>3} of {a+b:<3} reach grade>=2   {a/(a+b):>6.1%}")
    print(f"  anchor-sourced   {c:>3} of {c+d:<3} reach grade>=2   {c/(c+d):>6.1%}")
    print(f"  risk difference  {rd:>6.1%}        one-sided Fisher p = {fisher_one_sided(a,b,c,d):.3g}")

print("PROVENANCE / OUTCOME CONFOUND -- clinical rows")
table(m, "[A] all clinical rows (raw grades, as previously reported)")

ELIG = ("positive_finding", "confirmed_negative")
table([r for r in m if r["negative_eligibility"] in ELIG],
      "[B] rows that pass negative_eligibility (the defensible view)")

excl = [r for r in m if r["negative_eligibility"] not in ELIG]
print(f"\n[A] minus [B] = {len(excl)} rows excluded as ineligible negatives: "
      f"{', '.join(r['measurement_id'] for r in excl)}")
print("\nNO MEASURABLE WEAKENING is claimed. The three rows previously credited with")
print("weakening the confound are themselves gated out as ineligible negatives, and the")
print("unverified arm is unchanged at 0 of 20. Any apparent movement is denominator change.")
