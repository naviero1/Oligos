#!/usr/bin/env python3
"""Attribution audit: does the cited evidence actually support the row's attribution?

    python3 toxicity/coagulopathy/scripts/audit_attribution.py
    data/measurements.csv -> data/attribution_audit.csv

Why this exists. `verify_against_sources.py` locates every numeric value in the cited
document: 2,019 of 2,019. That is a FABRICATION check. It proves the number is printed in
the source. It does NOT prove the number belongs to the compound, arm, dose and timepoint
the row assigns it to -- and in a regulatory review covering six trials of one drug, which
is most of the human evidence here, a value can be located and still be attached to the
wrong arm. The first Beebop reply reported "2,019/2,019 verified" without that
qualification; Beebop was right to isolate it (2026-10-02, proposal 5).

This audit is deliberately narrow: the 353 participant rows flagged unintended_toxicity,
the subset any reader would treat as the harm signal. For each row it asks three
mechanical questions and records the answer per row, so the weak ones are addressable
instead of merely admitted:

  locus_named     -- does source_locus name a table, figure, section or page, so a reader
                     can go to the place the value came from?
  arm_identified  -- does the row's own quote name the arm or the compound it is assigned to?
  dose_or_n_shown -- does the quote carry the dose or the denominator the row claims?

A row is ATTRIBUTION_SUPPORTED only with a named locus AND an identified arm. Nothing here
changes a value or a label; it reports what the cited evidence does and does not establish.
"""
import csv, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "measurements.csv")
OUT = os.path.join(ROOT, "data", "attribution_audit.csv")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"

LOCUS = re.compile(r"table|figure|fig\.|section|annex|appendix|\bp\.?\s?\d|page|paragraph|"
                   r"§|\d+\.\d+|results|adverse event|listing|exhibit|module", re.I)
ARM = re.compile(r"placebo|\barm\b|\bgroup\b|cohort|treated|receiving|\bvs\b|versus|"
                 r"randomi[sz]ed|pooled|comparator|control", re.I)


def tokens(*vals):
    return " ".join(str(v or "") for v in vals)


def main():
    rows = list(csv.DictReader(open(SRC, newline="", encoding="utf-8")))
    oligos = {o["oligo_id"]: o for o in
              csv.DictReader(open(os.path.join(ROOT, "data", "oligos.csv"), newline="", encoding="utf-8"))}
    target = [r for r in rows
              if r["human_system_subtype"] == "participant" and r["unintended_toxicity"] == "TRUE"]
    out = []
    for r in target:
        quote = tokens(r["verbatim_quote"], r["notes"], r["control_description"])
        name = oligos.get(r["oligo_id"], {}).get("oligo_name", "")
        aliases = [a.strip() for a in oligos.get(r["oligo_id"], {}).get("aliases", "").split(";") if a.strip()]
        locus_named = bool(LOCUS.search(r["source_locus"] or ""))
        arm = bool(ARM.search(quote)) or any(
            x and len(x) > 3 and x.lower() in quote.lower() for x in [name] + aliases)
        dose = r["dose_value"]
        dose_shown = bool(dose and dose not in (NR, NA) and re.search(
            r"\b" + re.escape(str(dose).split(".")[0]) + r"\b", quote))
        n = r["n_subjects"]
        n_shown = bool(n and n not in (NR, NA) and re.search(
            r"\b" + re.escape(str(n).split(".")[0]) + r"\b", quote))
        verdict = ("ATTRIBUTION_SUPPORTED" if (locus_named and arm) else
                   "ATTRIBUTION_WEAK_locus_only" if locus_named else
                   "ATTRIBUTION_WEAK_arm_only" if arm else
                   "ATTRIBUTION_UNSUPPORTED")
        out.append({
            "measurement_id": r["measurement_id"],
            "study_id": r["study_id"],
            "study_id_basis": r["study_id_basis"],
            "oligo_id": r["oligo_id"],
            "source_id": r["source_id"],
            "readout_category": r["readout_category"],
            "readout_name": r["readout_name"],
            "evidence_class": r["evidence_class"],
            "grade_authority": r["grade_authority"],
            "locus_named": str(locus_named).upper(),
            "arm_identified": str(arm).upper(),
            "dose_shown_in_quote": str(dose_shown).upper(),
            "n_shown_in_quote": str(n_shown).upper(),
            "verdict": verdict,
            "source_locus": (r["source_locus"] or NR)[:300],
        })
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)

    c = Counter(x["verdict"] for x in out)
    print(f"  attribution audit over {len(out)} participant rows flagged unintended_toxicity")
    for k, v in c.most_common():
        print(f"    {v:4d}  {k}")
    linked = sum(1 for x in out if x["study_id"].startswith("COG-STU"))
    print(f"    {linked}/{len(out)} of the audited rows are linked to a single trial")
    print(f"  -> data/attribution_audit.csv")
    # The audit reports; it does not gate the build. A weak attribution is a research task,
    # not a broken table.
    return 0


if __name__ == "__main__":
    sys.exit(main())
