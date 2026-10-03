#!/usr/bin/env python3
"""Audit the rights position of every row that PHYSICALLY SHIPS in submission/.

Crank's delegation asks this endpoint to "audit the 984 of 1,959 rows shipping
inside submission/ under non-redistributable terms". The 984 figure is confirmed
as the LEGACY `redistribution` column's `summary_stat` count -- but that column
was a blanket tag meaning "a number extracted from a paper", not a per-licence
determination. The publisher-declared audit in curation/rights/rights_audit.csv
supersedes it. This script restates the position per shipped artifact, and emits
the two exclusion lists Beebop's Tier 0 crosswalk needs.

Per SCIENTIFIC_RULES.md the two questions are kept SEPARATE:
  (1) source-file republication -- may the PDF/zip itself be redistributed?
  (2) extracted-data reuse      -- may the numbers, with citation, be released?
This script answers (2), which is what the workbook and the CSVs contain. It
makes NO withdrawal: output is a proposed-hold list for Oscar.

Also emits licence_class, and the ND-derived row list, because NoDerivatives is
the clause that actually bites a restructured dataset.

Usage:  python3 scripts/rights_by_artifact.py
"""
import csv, os, re, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
RIGHTS = os.path.join(ENDPOINT, "curation", "rights")


def rd(p):
    with open(p, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))


# Per-regulator classes. Correction 2026-10-03: this script previously collapsed
# every regulator document into "public_domain_us_federal". That is wrong, and
# Crank's delegation item 12 states why: "regulator document = government work =
# public domain" reaches US FEDERAL AGENCIES ONLY. EMA permits commercial reuse
# WITH ATTRIBUTION -- a licence with a condition, not public domain. 216 rows in
# this endpoint were mis-tagged. TGA forbids redistribution without written
# approval and PMDA is All Rights Reserved; this endpoint has zero of either,
# verified, but the classes exist so a future row cannot be mis-filed silently.
def regulator_of(ref):
    r = (ref or "").upper()
    if any(k in r for k in ("EMEA", "EPAR", "SMPC")) or "EMA/" in r or r.startswith("EMA "):
        return "EMA"
    if any(k in r for k in ("FDA", "NDA ", "DAILYMED", "_SPL_", "ACCESSDATA")):
        return "FDA_US"
    if "CLINICALTRIALS" in r or "NCT0" in r or "NCT1" in r:
        return "CTGOV_US"
    if re.match(r"^\s*US\s?[\d,/]{6,}", r):
        return "USPTO"
    if "TGA" in r: return "TGA_AU"
    if "PMDA" in r: return "PMDA_JP"
    return ""


REGULATOR_CLASS = {
    "FDA_US":   ("public_domain_us_federal",
                 "US federal agency work; no copyright attaches"),
    "CTGOV_US": ("public_domain_us_federal",
                 "NIH/NLM posted results; US federal agency work"),
    "USPTO":    ("public_domain_uspto_patent",
                 "published US patent text is a US government publication; the applicant's "
                 "disclosure is public by design"),
    "EMA":      ("ema_reuse_with_attribution",
                 "EMA permits reuse INCLUDING commercial use, conditional on attribution. "
                 "NOT public domain -- attribution is a condition, so it is a licence"),
    "TGA_AU":   ("tga_redistribution_prohibited",
                 "TGA forbids redistribution without written approval"),
    "PMDA_JP":  ("pmda_all_rights_reserved",
                 "PMDA material is All Rights Reserved"),
}


def licence_class(tier, lic, ref=""):
    reg = regulator_of(ref)
    if reg in REGULATOR_CLASS:
        return REGULATOR_CLASS[reg][0]
    l = (lic or "").lower()
    if tier.startswith("A_"): return "public_domain_us_federal"
    if "nd" in l.split("-"): return "cc_nd_derivatives_restricted"
    if "nc" in l.split("-"): return "cc_nc_noncommercial"
    if l.startswith("cc"): return "cc_permissive"
    if tier.startswith("B_"): return "open_access_licence_unstated"
    return "closed_no_open_licence"


def main():
    M = rd(os.path.join(DATA, "measurements.csv"))
    R = {r["source_ref"]: r for r in rd(os.path.join(RIGHTS, "rights_audit.csv"))}

    rows = []
    for m in M:
        r = R.get(m["source_ref"], {})
        tier = r.get("rights_tier", "D_unresolved")
        lic = r.get("declared_licence", "")
        rows.append({
            "measurement_id": m["measurement_id"], "oligo_id": m["oligo_id"],
            "subject_class": m["subject_class"], "source_ref": m["source_ref"][:110],
            "legacy_redistribution": m["redistribution"],
            "rights_tier": tier, "declared_licence": lic,
            "licence_class": licence_class(tier, lic, m["source_ref"]),
            "regulator": regulator_of(m["source_ref"]),
            "licence_basis": REGULATOR_CLASS.get(regulator_of(m["source_ref"]), ("", ""))[1],
            "journal": r.get("journal", ""),
            "extracted_data_release": ("permitted" if tier.startswith(("A_", "B_"))
                                       else "DECISION_REQUIRED"),
            "proposed_hold": ("no" if tier.startswith(("A_", "B_")) else "PROPOSED_HOLD"),
            "hold_reason": ("" if tier.startswith(("A_", "B_"))
                            else "no open licence declared by the publisher; extracted values are "
                                 "facts rather than expression, but the release of facts from a "
                                 "closed-access source is Oscar's call, not this pipeline's"),
        })

    with open(os.path.join(RIGHTS, "shipped_row_rights.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    # exclusion lists for the crosswalk's regeneration switch
    nd = [r for r in rows if r["licence_class"] in
          ("cc_nd_derivatives_restricted", "tga_redistribution_prohibited",
           "pmda_all_rights_reserved")]
    hold = [r for r in rows if r["proposed_hold"] == "PROPOSED_HOLD"]
    for name, sub in (("exclude_nd_derived_rows.csv", nd),
                      ("proposed_hold_rows.csv", hold)):
        with open(os.path.join(RIGHTS, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(sub)

    cls = collections.Counter(r["licence_class"] for r in rows)
    print(f"rows physically shipping in submission/ (workbook + merged view): {len(rows)}\n")
    print("licence_class distribution:")
    for k, v in cls.most_common(): print(f"  {v:5d}  {k}")
    print(f"\nextracted-data release permitted on publisher-declared terms : "
          f"{sum(1 for r in rows if r['extracted_data_release']=='permitted')}")
    print(f"PROPOSED HOLD (decision required, zero automatic withdrawals)  : {len(hold)}")
    print(f"ND-derived rows (NoDerivatives clause)                        : {len(nd)}")
    print(f"\nlegacy column said summary_stat = "
          f"{sum(1 for m in M if m['redistribution']=='summary_stat')} "
          f"-- superseded; it was a blanket tag, not a licence determination")
    print("\nproposed holds by source:")
    for k, v in collections.Counter(r["source_ref"][:72] for r in hold).most_common():
        print(f"  {v:4d}  {k}")
    print("\n  -> curation/rights/shipped_row_rights.csv")
    print("  -> curation/rights/proposed_hold_rows.csv")
    print("  -> curation/rights/exclude_nd_derived_rows.csv")


if __name__ == "__main__":
    main()
