#!/usr/bin/env python3
"""Audit the units claimed to support a platelet-toxicity claim.

The count ladder ends at 22 units: trial-typed, carrying measurement rows,
platelet endpoint evaluable, and not intended pharmacology. Beebop's research
round asks that those 22 be audited "against exact platelet monitoring, exposure
and denominators" before any total is quoted -- correctly, because the 22 is a
CURATOR CLASSIFICATION, not an independent re-audit of each primary report.

This applies four explicit tests to each unit and reports which survive all of
them. It changes no data; it writes an audit table.

TESTS
  T1 monitoring  the platelet_endpoint_basis must QUOTE evidence that platelets
                 were measured. Language that only reports an ABSENCE ("no
                 decreases were observed", "no evidence of") does not establish
                 that the endpoint was assessed under a defined window, and is
                 the exact pattern that manufactures negatives.
  T2 exposure    dose_regimen AND duration must both be stated.
  T3 denominator n_analyzed_platelet_numeric must be present -- an at-risk
                 denominator specific to the platelet analysis.
  T4 locus       the basis must cite a retrievable locus (table, figure,
                 section, page), not a bare assertion.

Usage:  python3 scripts/audit_toxicity_denominator.py
Writes: data/toxicity_denominator_audit.csv
"""
import csv, os, re, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")

ABSENCE = re.compile(
    r"no (?:evidence|reports?|cases?|decreases?|reduction|events?|clinically)|"
    r"were not (?:observed|reported)|was not (?:observed|reported)|"
    r"did not (?:occur|show)|absence of|unremarkable|no significant change", re.I)
MEASURED = re.compile(
    r"\bplatelet count|platelet nadir|x\s*10\s*9|K/u?L|10\^9/L|per\s*u?L|"
    r"thrombocytopenia (?:grade|events?|incidence)|CTCAE|<\s*\d+\s*,?\d*\s*(?:K|x)|"
    r"\bmedian\b|\bmean\b|\bn\s*=\s*\d+|\d+\s*%|\d+\s*/\s*\d+", re.I)
LOCUS = re.compile(
    r"table|figure|fig\.|section|appendix|page\s*\d|p\.\s*\d|supplement|"
    r"module|results|listing|exhibit", re.I)


def main():
    p = os.path.join(DATA, "studies.csv")
    if not os.path.exists(p):
        raise SystemExit("data/studies.csv not built")
    with open(p, newline="", encoding="utf-8") as f:
        S = list(csv.DictReader(f))

    pool = [s for s in S
            if s["eligibility_decision"] == "included"
            and s["evidence_unit_type"] in ("registered_trial", "unregistered_trial")
            and (s["n_measurement_rows"] or "0") not in ("", "0")
            and s["platelet_endpoint_evaluable"] == "yes"
            and s["intended_pharmacology"] != "yes"]

    out = []
    for s in pool:
        basis = s.get("platelet_endpoint_basis", "") or ""
        t1_measured = bool(MEASURED.search(basis))
        t1_absence_only = bool(ABSENCE.search(basis)) and not t1_measured
        t1 = t1_measured and not t1_absence_only
        t2 = bool((s.get("dose_regimen") or "").strip()
                  and not (s.get("dose_regimen") or "").upper().startswith("TBD")
                  and (s.get("duration") or "").strip()
                  and not (s.get("duration") or "").upper().startswith("TBD"))
        t3 = bool((s.get("n_analyzed_platelet_numeric") or "").strip())
        t4 = bool(LOCUS.search(basis))
        passed = sum([t1, t2, t3, t4])
        fails = [n for n, ok in (("T1_monitoring", t1), ("T2_exposure", t2),
                                 ("T3_denominator", t3), ("T4_locus", t4)) if not ok]
        out.append({
            "study_id": s["study_id"], "study_key": s["study_key"],
            "compound": s["compound"], "registry_id": s["registry_id"],
            "n_measurement_rows": s["n_measurement_rows"],
            "T1_monitoring_quoted": "pass" if t1 else "FAIL",
            "T1_absence_language_only": "yes" if t1_absence_only else "",
            "T2_exposure_stated": "pass" if t2 else "FAIL",
            "T3_platelet_denominator": "pass" if t3 else "FAIL",
            "T4_retrievable_locus": "pass" if t4 else "FAIL",
            "tests_passed": passed,
            "audit_verdict": ("SURVIVES_ALL_FOUR" if passed == 4 else
                              "PARTIAL" if passed >= 2 else "WEAK"),
            "failed_tests": ";".join(fails),
            "n_analyzed_platelet": s.get("n_analyzed_platelet_numeric", ""),
            "basis_excerpt": basis[:220],
        })

    out.sort(key=lambda r: (-r["tests_passed"], r["compound"]))
    with open(os.path.join(DATA, "toxicity_denominator_audit.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

    agg = collections.Counter(r["audit_verdict"] for r in out)
    print(f"audited {len(out)} units claimed to support a platelet-toxicity claim\n")
    for k in ("SURVIVES_ALL_FOUR", "PARTIAL", "WEAK"):
        if agg.get(k): print(f"  {agg[k]:3d}  {k}")
    print()
    for t in ("T1_monitoring_quoted", "T2_exposure_stated",
              "T3_platelet_denominator", "T4_retrievable_locus"):
        n = sum(1 for r in out if r[t] == "pass")
        print(f"  {n:3d}/{len(out)}  {t}")
    ab = sum(1 for r in out if r["T1_absence_language_only"] == "yes")
    if ab:
        print(f"\n  !! {ab} unit(s) rest on ABSENCE language only — the manufactured-negative pattern:")
        for r in out:
            if r["T1_absence_language_only"] == "yes":
                print(f"       {r['study_id']} {r['compound'][:28]:28s} {r['basis_excerpt'][:90]}")
    print(f"\n  DEFENSIBLE DENOMINATOR after audit: {agg.get('SURVIVES_ALL_FOUR',0)} "
          f"(was reported as {len(out)})")
    print("  -> data/toxicity_denominator_audit.csv")


if __name__ == "__main__":
    main()
