#!/usr/bin/env python3
"""Per-source rights audit for Phase 2 prize eligibility.

WHY
  Phase 2: "Only open datasets that are or will be made publicly available will
  be considered for a prize", and access terms must allow open public access
  "such as through a creative commons license". The dataset's per-row
  `redistribution` column currently marks 984 of 1,959 rows `summary_stat`,
  which reads as "half this dataset cannot be released openly".

  That figure looks like a CLASSIFICATION artefact rather than a rights ceiling.
  `summary_stat` was applied as a blanket category meaning "a number extracted
  from a paper", not as a per-licence determination -- and several of the
  largest contributors are open-access articles sitting in PubMed Central. This
  script replaces the blanket with evidence: it resolves every source carrying
  `summary_stat` rows against the Europe PMC REST API and records the licence
  and open-access status the publisher actually declares.

WHAT IT DOES NOT DO
  It does not make the legal call and it does not rewrite the dataset. It emits
  the evidence and a tiering so that the decision Oscar has to make is a small,
  well-posed one instead of a blanket 984-row question.

Usage:  python3 scripts/rights_audit.py
Writes: curation/rights/rights_audit.csv
"""
import csv, json, os, re, subprocess, collections, time

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
OUT = os.path.join(ENDPOINT, "curation", "rights")
os.makedirs(OUT, exist_ok=True)
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def ids(ref):
    """Pull the strongest available identifier out of a source_ref string."""
    out = {}
    m = re.search(r"PMC(\d{6,8})", ref)
    if m: out["pmcid"] = "PMC" + m.group(1)
    m = re.search(r"PMID[:\s]*(\d{6,8})", ref, re.I)
    if m: out["pmid"] = m.group(1)
    m = re.search(r"\b10\.\d{4,9}/[^\s;,()\]]+", ref)
    if m: out["doi"] = m.group(0).rstrip(".,;")
    return out


def epmc(q):
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", "30", "-G", EPMC,
                            "--data-urlencode", f"query={q}",
                            "--data-urlencode", "format=json",
                            "--data-urlencode", "resultType=core"],
                           capture_output=True, text=True, timeout=45)
        res = json.loads(r.stdout).get("resultList", {}).get("result", [])
        return res[0] if res else None
    except Exception:
        return None


def lookup(ref):
    i = ids(ref)
    for q in ([f'PMCID:{i["pmcid"]}'] if "pmcid" in i else []) + \
             ([f'EXT_ID:{i["pmid"]}'] if "pmid" in i else []) + \
             ([f'DOI:"{i["doi"]}"'] if "doi" in i else []):
        r = epmc(q)
        if r: return r, q
    return None, ""


# ---- rights tiering -------------------------------------------------------
# Tier is about whether the EXTRACTED NUMERICAL VALUES can ship in an openly
# licensed dataset, not about redistributing the article PDF.
def tier(rec, legacy):
    if legacy == "public_domain":
        return "A_public_domain", "US Government work; no copyright attaches"
    lic = (rec or {}).get("license", "") or ""
    oa = (rec or {}).get("isOpenAccess", "") or ""
    lic_l = lic.lower()
    if lic_l.startswith("cc"):
        nc = "nc" in lic_l
        return ("B_cc_licensed",
                f"publisher-declared {lic.upper()}"
                + ("; NON-COMMERCIAL clause applies to reuse" if nc else ""))
    if oa == "Y":
        return "B_open_access_unspecified_licence", "Europe PMC isOpenAccess=Y, licence string absent"
    if rec is None:
        return "D_unresolved", "not resolved in Europe PMC; identifier may be wrong or record absent"
    return "C_closed_access", "no open licence declared; extracted values are facts, not expression"


def main():
    with open(os.path.join(DATA, "measurements.csv"), newline="", encoding="utf-8") as f:
        M = list(csv.DictReader(f))
    by = collections.defaultdict(lambda: collections.Counter())
    cls = {}
    for m in M:
        by[m["source_ref"]][m["redistribution"]] += 1
        cls[m["source_ref"]] = m["source_id"]

    rows, seen = [], 0
    targets = sorted(by.items(), key=lambda kv: -sum(kv[1].values()))
    print(f"resolving {len(targets)} source documents against Europe PMC ...\n")
    for ref, c in targets:
        legacy = c.most_common(1)[0][0]
        rec, q = lookup(ref)
        t, why = tier(rec, legacy)
        n = sum(c.values())
        seen += n
        rows.append({
            "source_ref": ref, "n_rows": n,
            "legacy_redistribution": legacy,
            "rights_tier": t, "basis": why,
            "declared_licence": (rec or {}).get("license", ""),
            "is_open_access": (rec or {}).get("isOpenAccess", ""),
            "in_pmc": "Y" if (rec or {}).get("pmcid") else "",
            "journal": ((rec or {}).get("journalInfo", {}) or {}).get("journal", {}).get("title", ""),
            "title": ((rec or {}).get("title", "") or "")[:140],
            "resolved_by": q,
        })
        print(f"  {n:5d}  {t:34s} {(rec or {}).get('license','-') or '-':14s} {ref[:62]}")
        time.sleep(0.2)

    with open(os.path.join(OUT, "rights_audit.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print("\n" + "=" * 78)
    agg = collections.Counter()
    for r in rows: agg[r["rights_tier"]] += r["n_rows"]
    for k in sorted(agg): print(f"  {agg[k]:5d} rows  {k}")
    openable = sum(v for k, v in agg.items() if k.startswith(("A_", "B_")))
    print(f"\n  openly releasable on publisher-declared terms : {openable} / {seen} "
          f"({100*openable//max(seen,1)}%)")
    closed = agg.get("C_closed_access", 0) + agg.get("D_unresolved", 0)
    print(f"  needs a decision                              : {closed} / {seen} "
          f"({100*closed//max(seen,1)}%)")
    nc = sum(r["n_rows"] for r in rows if "nc" in (r["declared_licence"] or "").lower())
    print(f"  carries a NON-COMMERCIAL clause               : {nc}")
    print(f"\n  (legacy column said {sum(1 for m in M if m['redistribution']=='summary_stat')} "
          f"rows were summary_stat)")
    print("  -> curation/rights/rights_audit.csv")


if __name__ == "__main__":
    main()
