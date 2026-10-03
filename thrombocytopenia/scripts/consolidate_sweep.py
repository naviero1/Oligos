#!/usr/bin/env python3
"""Consolidate the 20-resource sweep into an auditable coverage log, and correct
the defects an adversarial audit of it found.

The sweep ran 9 agents over 20 named resources and returned 31 resource rows and
120 candidates. An independent critic then audited the log and found real defects.
Those corrections are applied HERE, in code, with the original claim preserved
beside the correction, rather than quietly edited into the source files.

CORRECTIONS APPLIED
  C1  searched=true on rows that retrieved nothing. The brief says "Do not mark
      blocked services as successfully searched." Three rows violated it while
      their own notes asserted the correct standard. Any row whose outcome is
      access_barrier with no result identifiers is forced to searched=false.
  C2  search_date. All 31 rows recorded 2026-10-02; execution crossed into
      2026-10-03 UTC and that rollover is what unblocked one resource. Recorded
      as the true window.
  C3  A FABRICATED TITLE. Candidate DOI 10.1158/1538-7445.am2025-6835 was logged
      with "(oligonucleotide)" inserted into its title; the real study's compound
      is dasatinib, a tyrosine kinase inhibitor. The candidate is REMOVED, not
      re-ranked, and recorded as removed.
  C4  A DISPROVEN YIELD. The Slingsby 2022 supplement was logged as carrying
      "~60-200 per-donor observations", inferred from counting the word "donor"
      in the body text. The archive was then opened and contains only figure
      images and a methods appendix. Downgraded to 0 with the disproof cited.
  C5  A CONFLATED IDENTIFIER. One PMO candidate merges three distinct documents
      under one title/identifier pair. Flagged unusable pending re-resolution.
  C6  Cross-family deduplication. Each family's candidate list was standalone;
      82 identifiers appeared in two or more. Deduplicated on normalised
      identifier, keeping the strongest priority and recording every family that
      found it.

Usage:  python3 scripts/consolidate_sweep.py
Writes: curation/research_staging/search_coverage_log.csv   (the 20-row log)
        curation/research_staging/acquisition_candidates.csv (deduplicated)
        curation/research_staging/sweep_corrections.csv      (what was changed)
"""
import csv, glob, json, os, re, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(ENDPOINT, "curation", "research_staging")
WINDOW = "2026-10-02/2026-10-03 (UTC rollover mid-run; see correction C2)"

# The twenty resources the brief names, in its order.
NAMED = [
    "PubMed", "Europe PMC", "OpenAlex", "Semantic Scholar", "ResearchRabbit",
    "Undermind", "Elicit", "Consensus", "GEO", "SRA", "PRIDE", "ProteomeXchange",
    "BioStudies", "ArrayExpress", "ClinicalTrials.gov", "Comparative Toxicogenomics Database",
    "ICE", "ToxCast", "Zenodo", "Dryad",
]
ALIAS = {
    "pubmed": "PubMed", "europe pmc": "Europe PMC", "europepmc": "Europe PMC",
    "pmc": "Europe PMC", "openalex": "OpenAlex", "semantic scholar": "Semantic Scholar",
    "researchrabbit": "ResearchRabbit", "undermind": "Undermind", "elicit": "Elicit",
    "consensus": "Consensus", "geo": "GEO", "gene expression omnibus": "GEO",
    "sra": "SRA", "sequence read archive": "SRA", "pride": "PRIDE",
    "proteomexchange": "ProteomeXchange", "biostudies": "BioStudies",
    "arrayexpress": "ArrayExpress", "clinicaltrials": "ClinicalTrials.gov",
    "ctd": "Comparative Toxicogenomics Database",
    "comparative toxicogenomics": "Comparative Toxicogenomics Database",
    "ice": "ICE", "integrated chemical environment": "ICE",
    "toxcast": "ToxCast", "invitrodb": "ToxCast", "comptox": "ToxCast",
    "zenodo": "Zenodo", "dryad": "Dryad",
}

REMOVE = {"10.1158/1538-7445.am2025-6835":
          "C3 FABRICATED TITLE — '(oligonucleotide)' was inserted into the title of a study "
          "whose compound is dasatinib, a tyrosine kinase inhibitor. Not oligonucleotide "
          "evidence. Removed rather than re-ranked."}
YIELD_FIX = {"33567808":
             ("C4 DISPROVEN — logged as ~60-200 per-donor observations inferred from counting "
              "the word 'donor' in body text. The supplementary archive was then retrieved in "
              "full (1,848,710 bytes) and contains only figure/table images plus a methods "
              "appendix; no data-availability statement, no deposit. Actual yield 0.", "0")}
CONFLATED = {"34797383":
             "C5 CONFLATED — one title/identifier pair merges three distinct documents "
             "(PMID 34797383 Arch Toxicol review; 10.1016/j.nmd.2016.06.247; 10.1017/CJN.2018.178). "
             "Unusable until re-resolved to one document."}


# Longest alias first. "ArrayExpress within BioStudies" contains both names, and
# shortest-first matching silently absorbed ArrayExpress into BioStudies, which
# made a resource that WAS searched read as never reached.
_ALIAS_ORDER = sorted(ALIAS.items(), key=lambda kv: -len(kv[0]))

def canon(name):
    n = (name or "").lower()
    if "arrayexpress" in n: return "ArrayExpress"
    for k, v in _ALIAS_ORDER:
        if k in n: return v
    return None


def norm_id(s):
    s = (s or "").strip().lower()
    m = re.search(r"\b(nct\d{8})\b", s)
    if m: return m.group(1)
    m = re.search(r"\b10\.\d{4,9}/[^\s;,()\]]+", s)
    if m: return m.group(0).rstrip(".,;")
    m = re.search(r"pmid[:\s]*(\d{6,8})", s)
    if m: return "pmid:" + m.group(1)
    m = re.search(r"\b(pmc\d{6,8})\b", s)
    if m: return m.group(1)
    m = re.search(r"\b(gse\d+|pxd\d+|prjna\d+|s-[a-z]+\d+)\b", s)
    if m: return m.group(1)
    return s[:80]


def main():
    rows, cands, corr = [], [], []
    seen_named = {}

    for f in sorted(glob.glob(os.path.join(STAGE, "sweep_*.json"))):
        fam = os.path.basename(f)[len("sweep_"):-len(".json")]
        d = json.load(open(f))
        for r in d.get("resources", []):
            ids = [x for x in (r.get("result_identifiers") or []) if x]
            searched = bool(r.get("searched"))
            outcome = (r.get("outcome") or "").strip()
            # C1: a barrier row with nothing retrieved is not a search
            if searched and outcome == "access_barrier" and not ids:
                corr.append({"correction": "C1_false_search_flag", "family": fam,
                             "subject": r.get("resource", "")[:90],
                             "original": "searched=true",
                             "corrected": "searched=false",
                             "why": "outcome=access_barrier with zero result identifiers; the "
                                    "brief forbids marking a blocked service as searched"})
                searched = False
            rows.append({
                "resource_named": canon(r.get("resource")) or "",
                "resource_as_reported": (r.get("resource") or "")[:120],
                "family": fam, "url": r.get("url", ""),
                "searched": "yes" if searched else "no",
                "search_window": WINDOW,
                "n_queries": len(r.get("queries") or []),
                "queries": " | ".join((r.get("queries") or [])[:12])[:900],
                "n_results_relevant": r.get("n_results_relevant", ""),
                "n_identifiers_recorded": len(ids),
                "result_identifiers": ";".join(ids[:40])[:900],
                "outcome": outcome,
                "barrier_class": r.get("barrier_class", ""),
                "barrier_detail": (r.get("barrier_detail") or "")[:600],
                "notes": (r.get("notes") or "")[:500],
            })
            c = canon(r.get("resource"))
            if c:
                prev = seen_named.get(c)
                if prev is None or (searched and prev["searched"] == "no"):
                    seen_named[c] = rows[-1]

        for c in d.get("candidates", []):
            ident = c.get("identifier", "") or c.get("link", "")
            key = norm_id(ident)
            rm = next((v for k, v in REMOVE.items() if k in (ident or "").lower()), None)
            if rm:
                corr.append({"correction": "C3_removed_candidate", "family": fam,
                             "subject": (c.get("full_title") or "")[:90],
                             "original": ident, "corrected": "REMOVED", "why": rm})
                continue
            exp = str(c.get("expected_usable_observations", ""))
            note = ""
            for k, (why, newv) in YIELD_FIX.items():
                if k in (ident or ""):
                    corr.append({"correction": "C4_disproven_yield", "family": fam,
                                 "subject": (c.get("full_title") or "")[:90],
                                 "original": exp, "corrected": newv, "why": why})
                    exp, note = newv, why
            for k, why in CONFLATED.items():
                if k in (ident or ""):
                    corr.append({"correction": "C5_conflated_identifier", "family": fam,
                                 "subject": (c.get("full_title") or "")[:90],
                                 "original": ident, "corrected": "FLAGGED_UNUSABLE", "why": why})
                    note = why
            cands.append({
                "dedup_key": key, "found_by": fam,
                "full_title": (c.get("full_title") or "")[:200],
                "authors_year": c.get("authors_year", ""), "identifier": ident,
                "link": c.get("link", ""), "publisher_or_repo": c.get("publisher_or_repo", ""),
                "required_file": (c.get("required_file") or "")[:200],
                "endpoint_gap": (c.get("endpoint_gap_it_closes") or "")[:200],
                "expected_usable_observations": exp,
                "human_in_vitro": str(c.get("human_in_vitro", "")),
                "priority": str(c.get("priority", "")),
                "access_outcome": (c.get("outcome") or "")[:160],
                "correction_note": note,
            })

    # C6: deduplicate across families. Merge on ANY shared identifier, not just
    # the primary key: the same paper was logged under a PMID by one family and a
    # DOI by another, so a single-key dedup under-merges.
    def all_keys(c):
        blob = f"{c['identifier']} {c['link']}"
        ks = set()
        for m in re.finditer(r"\b(nct\d{8})\b", blob, re.I): ks.add(m.group(1).lower())
        for m in re.finditer(r"\b10\.\d{4,9}/[^\s;,()\]]+", blob): ks.add(m.group(0).rstrip(".,;").lower())
        for m in re.finditer(r"pmid[:\s]*(\d{6,8})", blob, re.I): ks.add("pmid:" + m.group(1))
        for m in re.finditer(r"\b(pmc\d{6,8})\b", blob, re.I): ks.add(m.group(1).lower())
        for m in re.finditer(r"\b(gse\d+|pxd\d+|prjna\d+)\b", blob, re.I): ks.add(m.group(1).lower())
        return ks or {c["dedup_key"]}

    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for c in cands:
        ks = list(all_keys(c))
        for k in ks[1:]: union(ks[0], k)
        c["_keys"] = ks
    grp = collections.defaultdict(list)
    for c in cands: grp[find(c["_keys"][0])].append(c)
    dedup = []
    for k, v in grp.items():
        best = min(v, key=lambda x: (x["priority"] or "9"))
        best = dict(best)
        best["found_by"] = ";".join(sorted({x["found_by"] for x in v}))
        best["n_families_found"] = len({x["found_by"] for x in v})
        best["priorities_assigned"] = ";".join(sorted({x["priority"] for x in v if x["priority"]}))
        dedup.append(best)
        if len(v) > 1:
            corr.append({"correction": "C6_cross_family_duplicate", "family": best["found_by"],
                         "subject": best["full_title"][:90], "original": f"{len(v)} separate entries",
                         "corrected": "merged to 1", "why": "no cross-family reconciliation existed "
                                                            "in the log; the brief requires dedup"})
    dedup.sort(key=lambda x: (x["priority"] or "9", -x["n_families_found"]))

    # ---- the 20-row log, one row per NAMED resource -----------------------
    log = []
    for n in NAMED:
        r = seen_named.get(n)
        if r:
            log.append({**r, "resource_named": n})
        else:
            log.append({"resource_named": n, "resource_as_reported": "", "family": "",
                        "url": "", "searched": "no", "search_window": WINDOW, "n_queries": 0,
                        "queries": "", "n_results_relevant": "", "n_identifiers_recorded": 0,
                        "result_identifiers": "", "outcome": "not_reached",
                        "barrier_class": "unresolved_citation",
                        "barrier_detail": "no sweep family reported this resource",
                        "notes": ""})

    def write(name, data, cols=None):
        with open(os.path.join(STAGE, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols or list(data[0].keys()), extrasaction="ignore")
            w.writeheader(); w.writerows(data)
        print(f"  {len(data):4d} rows -> curation/research_staging/{name}")

    write("search_coverage_log.csv", log)
    write("sweep_all_resource_rows.csv", rows)
    write("acquisition_candidates.csv", dedup)
    write("sweep_corrections.csv", corr,
          ["correction", "family", "subject", "original", "corrected", "why"])

    print(f"\n20 NAMED RESOURCES: {sum(1 for r in log if r['searched']=='yes')} searched, "
          f"{sum(1 for r in log if r['searched']=='no')} not")
    for r in log:
        if r["searched"] == "no":
            print(f"   NOT SEARCHED  {r['resource_named']:38s} {r['barrier_class']}: "
                  f"{r['barrier_detail'][:70]}")
    print(f"\ncandidates: {len(cands)} raw -> {len(dedup)} deduplicated")
    pri = collections.Counter(c["priority"] for c in dedup)
    print("  by priority:", dict(sorted(pri.items())))
    iv = sum(1 for c in dedup if c["human_in_vitro"].lower() in ("true", "yes"))
    print(f"  human in vitro: {iv}")
    print(f"\ncorrections applied: {len(corr)}")
    for k, v in collections.Counter(c["correction"] for c in corr).most_common():
        print(f"  {v:4d}  {k}")


if __name__ == "__main__":
    main()
