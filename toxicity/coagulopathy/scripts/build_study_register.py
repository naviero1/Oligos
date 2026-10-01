#!/usr/bin/env python3
"""Build the deduplicated human study register.

    python3 toxicity/coagulopathy/scripts/build_study_register.py
    sources/study_register_raw.json  ->  data/studies.csv

Why this exists. `study_type=clinical` gives 749 MEASUREMENT ROWS. That is not 749 trials:
the same study is reported by its registry record, its publication, its regulatory
assessment and its product label, pooled analyses re-report trials already counted, and
spontaneous-reporting extracts are not studies at all. This register counts each study once.

THE HEADLINE RULE, applied strictly. A study enters the headline trial total only when
  (a) design == interventional_trial,
  (b) it reports a coagulation endpoint (endpoint_evaluable), and
  (c) it carries a verifiable identity -- a registry number, a trial acronym, or a sponsor
      protocol code -- so that the count is reproducible from identifiers and the study can
      be deduplicated against its other appearances.
A trial with no identifier of any kind cannot be shown to be distinct from one already
counted, so it is registered and excluded from the headline rather than quietly added.
Pooled analyses, labels, regulatory summaries, case reports, observational studies,
healthy-volunteer laboratory work and spontaneous reporting never enter the trial total.
"""
import csv, json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "sources", "study_register_raw.json")
OUT = os.path.join(ROOT, "data", "studies.csv")
NR = "NOT_REPORTED"

TRIAL_DESIGNS = {"interventional_trial"}
NON_STUDY = {"spontaneous_reporting", "product_label", "regulatory_summary", "not_a_human_study"}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def clean_registry(s):
    m = re.search(r"(NCT\d{8}|EUDRACT[\s-]?[\d-]{8,}|ISRCTN\d+|JAPICCTI[-\s]?\d+|EU[\s-]?CT[\s-]?[\d-]+)",
                  str(s or ""), re.I)
    return re.sub(r"[\s-]+", "", m.group(1)).upper() if m else ""


# ---- protocol tokens ---------------------------------------------------------------
# Documents gloss the same protocol differently: "ISIS 420915-CS3" in an FDA review and
# "ISIS 420915-CS3 (\"CS3\")" in an EMA report. Matching whole normalised strings misses that,
# so each record yields a SET of protocol tokens and two records merge when they share one.
_FULL = re.compile(r"(ISIS[\s-]*\d{5,6}[\s-]*CS\d+|ALN[\s-]*AT3SC[\s-]*\d+|OGX[\s-]*\d+[\s-]*\d*|"
                   r"[A-Z]{3}\d{5}|LTE\d{5}|EFC\d{5}|TDR\d{5}|POP\d{5}|ACT\d{5})", re.I)
_BARE = re.compile(r"\bCS\s?(\d{1,2})\b", re.I)

_JUNK = re.compile(r"notreported|notapplicable|none|^na$|pooled|integrated|overall|metaanalys|combinedanalys|phase\d*only")

def usable_label(s):
    """A label is an identifier only if it actually identifies a study.

    Agents wrote fields like 'NOT_REPORTED (pooled Phase 3 FCS safety analysis)'. Normalising
    that produced a long unique-looking string that matched across documents and chained two
    different drug programmes into one cluster. A label is rejected when it carries a
    not-reported marker, describes a pooled/integrated analysis, or is long enough to be a
    sentence rather than a name."""
    n = norm(s)
    if not n or len(n) > 40 or _JUNK.search(n):
        return ""
    return n

def protocol_tokens(r):
    """(strong, weak). Strong tokens identify a protocol on their own. Weak tokens -- a bare
    'CS3' -- recur across unrelated programmes, so they may only merge records that also
    agree on compound."""
    blob = f"{r.get('sponsor_protocol','')} {r.get('trial_acronym','')}"
    strong = {re.sub(r"[^A-Z0-9]", "", m.upper()) for m in _FULL.findall(blob)}
    weak = {"CS" + m for m in _BARE.findall(blob)}
    return strong, weak


def compound_key(r):
    c = " ".join(sorted(str(x) for x in (r.get("compounds") or []) if not str(x).startswith("COG-OLG")))
    c = norm(c)
    for fam in ("fitusiran", "inotersen", "mipomersen", "volanesorsen", "donidalorsen",
                "olezarsen", "eplontersen", "nusinersen", "tofersen", "imetelstat",
                "custirsen", "defibrotide", "pegnivacogin", "inclisiran", "vutrisiran",
                "fesomersen", "ionisfxirx", "isis416858", "alicaforsen", "apatorsen"):
        if fam in c:
            return fam
    return c[:24]

def best(vals):
    """Most informative non-empty value: the longest that is not a placeholder."""
    v = [str(x).strip() for x in vals if str(x).strip() and str(x).strip() not in (NR, "NOT_APPLICABLE", "None")]
    return max(v, key=len) if v else NR


def main():
    raw = json.load(open(RAW))["raw_records"]

    # ---- identity: union-find over registry number, acronym and protocol tokens -------
    parent = list(range(len(raw)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_reg, by_acr, by_strong, by_weak = {}, {}, {}, {}
    for i, r in enumerate(raw):
        reg = clean_registry(r.get("registry_id"))
        if reg:
            by_reg.setdefault(reg, []).append(i)
        acr = usable_label(r.get("trial_acronym"))
        if acr:
            by_acr.setdefault(acr, []).append(i)
        strong, weak = protocol_tokens(r)
        for t in strong:
            by_strong.setdefault(t, []).append(i)
        for t in weak:
            by_weak.setdefault((compound_key(r), t), []).append(i)

    for idx in list(by_reg.values()) + list(by_acr.values()) + list(by_strong.values()) + list(by_weak.values()):
        for j in idx[1:]:
            union(idx[0], j)

    merged = defaultdict(list)
    for i, r in enumerate(raw):
        merged[find(i)].append(r)
    folded = len(raw) - len(merged)

    rows = []
    for n, (k, rs) in enumerate(sorted(merged.items(), key=lambda x: -len(x[1])), 1):
        designs = {r.get("design", "") for r in rs}
        # A study reported as a trial in one document and summarised in another is a trial.
        design = "interventional_trial" if "interventional_trial" in designs else best(list(designs))
        reg = best([clean_registry(r.get("registry_id")) for r in rs])
        acr = best([r.get("trial_acronym") for r in rs])
        prot = best([r.get("sponsor_protocol") for r in rs])
        has_tok = any(protocol_tokens(r)[0] for r in rs)
        pooled_only = (not any(clean_registry(r.get("registry_id")) for r in rs)
                       and not has_tok
                       and not any(usable_label(r.get("trial_acronym")) for r in rs))
        identity = ("registry_number" if reg != NR else
                    "pooled_or_unnamed_descriptor" if pooled_only else
                    "trial_acronym" if usable_label(acr) else
                    "sponsor_protocol" if (prot != NR and has_tok) else
                    "sponsor_protocol_unqualified" if prot != NR else "no_identifier")
        evaluable = any(bool(r.get("endpoint_evaluable")) for r in rs)
        headline = (design in TRIAL_DESIGNS and evaluable
                    and identity in ("registry_number", "trial_acronym", "sponsor_protocol"))
        eps = sorted({e for r in rs for e in (r.get("coagulation_endpoints") or [])})
        cmp_ = sorted({c for r in rs for c in (r.get("compounds") or []) if not c.startswith("COG-OLG")})
        olg = sorted({c for r in rs for c in (r.get("compounds") or []) if c.startswith("COG-OLG")})
        rows.append({
            "study_id": "COG-STU%03d" % n,
            "design": design,
            "identity_basis": identity,
            "registry_id": reg,
            "trial_acronym": acr,
            "sponsor_protocol": prot,
            "phase": best([r.get("phase") for r in rs]),
            "headline_trial": "TRUE" if headline else "FALSE",
            "endpoint_evaluable": "TRUE" if evaluable else "FALSE",
            "coagulation_endpoints": "; ".join(eps) if eps else NR,
            "compounds": "; ".join(cmp_) if cmp_ else NR,
            "oligo_ids": "; ".join(olg) if olg else NR,
            "enrolled": best([r.get("enrolled") for r in rs]),
            "analysed": best([r.get("analysed") for r in rs]),
            "population": best([r.get("population") for r in rs]),
            "n_source_records": len(rs),
            "source_ids": "; ".join(sorted({r.get("source_id", "") for r in rs})),
            "designs_reported": "; ".join(sorted(designs)),
            "evidence_quote": best([r.get("evidence_quote") for r in rs])[:1200],
            "locus": best([r.get("locus") for r in rs])[:400],
            "duplicate_of_hint": best([r.get("duplicate_of_hint") for r in rs])[:600],
            # Clustering is heuristic. A group built from many source records may be one
            # heavily-reported trial or an over-merge, and the difference is a scientific
            # judgement, so it is flagged for review rather than silently trusted.
            "review_flag": ("large_cluster_verify_not_an_over_merge" if len(rs) > 8 else
                            "design_disagreement_between_sources" if len(designs) > 1 else ""),
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    head = [r for r in rows if r["headline_trial"] == "TRUE"]
    from collections import Counter
    print(f"  raw records {len(raw)} -> {len(rows)} distinct studies ({folded} duplicate appearances merged)")
    print(f"  by design: {dict(Counter(r['design'] for r in rows))}")
    print(f"  identity:  {dict(Counter(r['identity_basis'] for r in rows))}")
    print(f"\n  HEADLINE human interventional trials with a coagulation endpoint: {len(head)}")
    print(f"    of which identified by registry number: {sum(1 for r in head if r['identity_basis']=='registry_number')}")
    flagged = [r for r in rows if r["headline_trial"] == "TRUE" and r["review_flag"]]
    print(f"    flagged for manual verification before quoting: {len(flagged)}"
          f" ({', '.join(r['study_id'] for r in flagged)})")
    excl = [r for r in rows if r["design"] == "interventional_trial" and r["headline_trial"] == "FALSE"]
    print(f"  trials registered but EXCLUDED from the headline: {len(excl)}"
          f"  ({sum(1 for r in excl if r['identity_basis']=='no_identifier')} unidentifiable,"
          f" {sum(1 for r in excl if r['endpoint_evaluable']=='FALSE')} no coagulation endpoint)")


if __name__ == "__main__":
    main()
