#!/usr/bin/env python3
"""Build the deduplicated human study register.

    python3 toxicity/coagulopathy/scripts/build_study_register.py
    sources/study_register_raw.json  ->  data/studies.csv + data/pooled_analyses.csv

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
Labels, regulatory summaries, case reports, observational studies, healthy-volunteer
laboratory work and spontaneous reporting never enter the trial total.

POOLED ANALYSES ARE NOT TRIALS, AND THEY ARE NOT IDENTIFIERS EITHER. The first version of
this register reported 30 headline trials. That was an under-count caused by this file.
A pooled-analysis record carries a protocol field that ENUMERATES the trials it pools --
"pooled FCS safety set (CS6 + CS7)", "Pool 2 (integrated long-term safety pool: CS2 + CS3
+ CS5 + CS7)", "All Volanesorsen Treated Patients (CS1 + CS13 + ...)". Every code in those
strings used to be emitted as an identity token, so a single pooled record unioned an
entire development programme into one "trial". Worse, a record naming a comparator or
prior therapy ("olezarsen; volanesorsen as prior therapy") carried both compound keys and
bridged two different drug programmes: nine volanesorsen trials and one olezarsen trial
ended up in COG-STU001, and eplontersen ended up inside inotersen's CS2.

Three changes close that:
  1. Pooled records are partitioned out before clustering and published separately in
     data/pooled_analyses.csv with the member protocols they name. They remain evidence --
     a regulatory pooled safety table is real -- but a pooled number must never be
     attributed to a single trial.
  2. A bare protocol code ("CS7") is qualified by the SPONSOR COMPOUND NUMBER, taken from
     the record's own protocol string or, where that is bare, from the subject programme of
     the source document. ISIS 304801-CS7 and ISIS 678354-CS7 are different trials.
  3. Over-merge is a QC failure, not a comment. Two registry numbers FROM THE SAME REGISTRY
     in one cluster, or two compound families, fails validation. Two numbers from DIFFERENT
     registries do not: one trial legitimately holds both an NCT and a EudraCT number, so
     that is recorded as an alias and flagged for linkage review (Beebop, 2026-10-02).
"""
import csv, json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "sources", "study_register_raw.json")
OUT = os.path.join(ROOT, "data", "studies.csv")
OUT_POOL = os.path.join(ROOT, "data", "pooled_analyses.csv")
NR = "NOT_REPORTED"

TRIAL_DESIGNS = {"interventional_trial"}
NON_STUDY = {"spontaneous_reporting", "product_label", "regulatory_summary", "not_a_human_study"}

FAMILIES = ("fitusiran", "inotersen", "mipomersen", "volanesorsen", "donidalorsen",
            "olezarsen", "eplontersen", "nusinersen", "tofersen", "imetelstat",
            "custirsen", "defibrotide", "pegnivacogin", "inclisiran", "vutrisiran",
            "fesomersen", "ionisfxirx", "isis416858", "alicaforsen", "apatorsen")

# One STUDY under two sponsor codes. Declared explicitly, with the evidence that reconciles
# them, so the over-merge rule below can stay a hard failure for everything else. This pair
# is reconciled by the FDA reviewer's own annotation: the filing checklist records the
# mipomersen-warfarin drug-drug-interaction study as MIPO2900509 while the Clinical Summary
# calls it MIPO2900210 (COG-S088/S089/S091, Table 4 'Overview of Clinical Pharmacology
# studies'). Any further entry here needs the same kind of in-source reconciliation.
PROGRAMME_ALIAS = {"MIPO2900509": "MIPO2900210"}

# Registry-verified crosswalk between a registry number and the sponsor's own protocol code.
# Checked against the ClinicalTrials.gov API (v2, 2026-10-02): each NCT record's
# orgStudyIdInfo.id and acronym were read and matched to the code the source documents use.
# Without this, one trial documented by its protocol code in a regulatory review and by its
# NCT number in a publication stays split -- ATLAS-A/B was counted twice.
#   NCT03417102 orgStudyId EFC14768 acronym ATLAS-INH
#   NCT03417245 orgStudyId EFC14769 acronym (none in registry; sponsor writes ATLAS-A/B)
#   NCT03549871 orgStudyId EFC15110 acronym ATLAS-PPX
#   NCT03754790 orgStudyId LTE15174 acronym ATLAS-OLE
REGISTRY_PROTOCOL = {
    "EFC14768": "NCT03417102",
    "EFC14769": "NCT03417245",
    "EFC15110": "NCT03549871",
    "LTE15174": "NCT03754790",
}

# One compound under two names is one family. IONIS-FXIRx IS ISIS 416858 (and BAY 2306001).
FAMILY_ALIAS = {"isis416858": "ionisfxirx"}

# A compound named as a comparator, an active reference, a prior therapy or a positive
# control is not the subject of the trial. Counting it as a second programme would read a
# two-arm trial as an over-merge: eplontersen's ION-682884-CS3 carries inotersen as its
# concurrent active reference arm, and that is one trial, correctly recorded.
_NOT_SUBJECT = re.compile(r"comparator|reference arm|active reference|prior therapy|"
                          r"prior treatment|prior prophylaxis|positive control|placebo|"
                          r"external control|on-demand|bypassing agent|BPA|"
                          r"clotting factor concentrate|CFC", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def clean_registry(s):
    m = re.search(r"(NCT\d{8}|EUDRACT[\s-]?[\d-]{8,}|ISRCTN\d+|JAPICCTI[-\s]?\d+|EU[\s-]?CT[\s-]?[\d-]+)",
                  str(s or ""), re.I)
    return re.sub(r"[\s-]+", "", m.group(1)).upper() if m else ""


def registry_family(reg):
    """Which registry a number belongs to. Two numbers from different registries are an
    alias of one trial; two from the same registry are two trials."""
    for fam in ("NCT", "EUDRACT", "ISRCTN", "JAPICCTI", "EUCT"):
        if reg.startswith(fam):
            return fam
    return "OTHER"


# ---- pooled-analysis detection ----------------------------------------------------
# A pooled record is one whose own design says so, or whose protocol/acronym field reads as
# an enumeration of other studies rather than as one study's identifier.
_POOL_WORD = re.compile(r"pool|integrated\s+(?:set|safety|placebo|long)|integrated\s*$|"
                        r"\bcombined\b|overall\s+\w+\s+(?:safety\s+)?database|"
                        r"\ball\b[^.]{0,40}\btreated\b|treated set|"
                        r"longitudinal safety set|safety database|meta[- ]?analys", re.I)
_POOL_PLUS = re.compile(r"(?:CS|MIPO|ISIS|ION|EFC|LTE|TDR)[\s-]?\d+[^+]{0,24}\+|"
                        r"\+[^+]{0,24}(?:CS|MIPO|ISIS|ION|EFC|LTE|TDR)[\s-]?\d+", re.I)


def is_pooled(r):
    if r.get("design") == "pooled_analysis":
        return True
    blob = f"{r.get('sponsor_protocol','')} {r.get('trial_acronym','')}"
    return bool(_POOL_WORD.search(blob) or _POOL_PLUS.search(blob))


# ---- identity tokens ---------------------------------------------------------------
# Documents gloss the same protocol differently: "ISIS 420915-CS3" in an FDA review and
# "ISIS 420915-CS3 (\"CS3\")" in an EMA report. Matching whole normalised strings misses
# that, so each record yields a SET of tokens and two records merge when they share one.
_FULL = re.compile(r"(ISIS[\s-]*\d{5,6}[\s-]*CS\d+|ION[\s-]*\d{6}[\s-]*CS\d+|"
                   r"ALN[\s-]*AT3SC[\s-]*\d+|OGX[\s-]*\d+[\s-]*\d*|"
                   r"[A-Z]{3}\d{5}|LTE\d{5}|EFC\d{5}|TDR\d{5}|POP\d{5}|ACT\d{5})", re.I)
_BARE = re.compile(r"\bCS\s?(\d{1,2})\b", re.I)
_PROG = re.compile(r"\b(ISIS|ION|AKCEA|ALN[\s-]?AT3SC|OGX|MIPO)[\s-]?(\d{4,8})", re.I)

_JUNK = re.compile(r"notreported|notapplicable|none|^na$|pooled|integrated|overall|"
                   r"metaanalys|combinedanalys|phase\d*only|^pool\d*$")


_ACR_HEAD = re.compile(r"^\s*([A-Za-z][A-Za-z0-9]*(?:[-/][A-Za-z0-9]+){0,3})")


def acronym_head(s):
    """The acronym itself, without the document's annotation of it. Agents recorded
    'ATLAS-A/B (also written ATLAS-AB)' in one source and 'ATLAS-A/B' in another; comparing
    the whole annotated string left one trial counted twice."""
    m = _ACR_HEAD.match(str(s or ""))
    return m.group(1) if m else ""


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
    head = norm(acronym_head(s))
    # A one- or two-letter head is not a name; keep the full label in that case.
    return head if len(head) >= 4 and not _JUNK.search(head) else n


def strong_tokens(r):
    blob = f"{r.get('sponsor_protocol','')} {r.get('trial_acronym','')}"
    return {re.sub(r"[^A-Z0-9]", "", m.upper()) for m in _FULL.findall(blob)}


def bare_tokens(r):
    blob = f"{r.get('sponsor_protocol','')} {r.get('trial_acronym','')}"
    return {"CS" + m for m in _BARE.findall(blob)}


def own_programme(r):
    """The sponsor's compound number as written in this record's protocol field."""
    m = _PROG.search(str(r.get("sponsor_protocol") or ""))
    if m:
        return re.sub(r"[^A-Z0-9]", "", (m.group(1) + m.group(2)).upper())
    return ""


def family(r, subject_only=False):
    """Drug families named by the record. Used for QC, never for merging: a record that
    names a comparator carries two families, which is exactly how two programmes got
    bridged into one cluster. With subject_only, comparator/prior-therapy/control
    compounds are excluded, leaving the drugs the trial was actually testing."""
    fams = set()
    for c in (r.get("compounds") or []):
        if subject_only and _NOT_SUBJECT.search(str(c)):
            continue
        n = norm(c)
        for f in FAMILIES:
            if f in n:
                fams.add(FAMILY_ALIAS.get(f, f))
    return fams


# Crank 2026-10-03, applied to the register as well as to measurements: a quote whose source
# licence does not permit republication is withheld and hashed rather than printed. A study
# cluster can draw on several sources, so a quote is kept only when EVERY source behind the
# cluster permits it -- a mixed cluster is withheld, because the quote cannot be attributed
# to the permissive half.
QUOTE_LICENCE_PERMITS_REPUBLICATION = {"public_domain", "CC_BY"}


def quote_rights(quote, source_ids, red):
    import hashlib
    q = str(quote or "")
    h = "sha256:" + hashlib.sha256(re.sub(r"\s+", " ", q).strip().encode("utf-8")).hexdigest()
    if not q.strip() or q.strip() == NR:
        return q, NR, "0", NR
    licences = {red.get(s.strip(), NR) for s in source_ids if s.strip()}
    if licences and licences <= QUOTE_LICENCE_PERMITS_REPUBLICATION:
        return q, h, str(len(q.split())), "quoted_in_full_source_licence_permits_republication"
    return ("WITHHELD_SOURCE_LICENCE_RESTRICTED - verify against the source at `locus` and "
            "compare evidence_quote_sha256."), h, str(len(q.split())), "withheld_source_licence_restricted"


def best(vals):
    """Most informative non-empty value: the longest that is not a placeholder."""
    v = [str(x).strip() for x in vals if str(x).strip() and str(x).strip() not in (NR, "NOT_APPLICABLE", "None")]
    return max(v, key=len) if v else NR


def main():
    raw = json.load(open(RAW))["raw_records"]
    _sp = os.path.join(ROOT, "data", "sources.csv")
    red = ({r["source_id"]: r.get("redistribution", NR)
            for r in csv.DictReader(open(_sp, newline="", encoding="utf-8"))}
           if os.path.exists(_sp) else {})
    pooled = [r for r in raw if is_pooled(r)]
    trial = [r for r in raw if not is_pooled(r)]

    # ---- the subject programme of each source document -----------------------------
    # A Waylivra assessment report writes "CS7" bare; its subject programme is ISIS 304801.
    src_prog = {}
    for sid, group in defaultdict(list, {k: [r for r in trial if r.get("source_id") == k]
                                         for k in {r.get("source_id") for r in trial}}).items():
        c = Counter(p for p in (own_programme(r) for r in group) if p)
        src_prog[sid] = c.most_common(1)[0][0] if c else ""

    def programme(r):
        return own_programme(r) or src_prog.get(r.get("source_id"), "") or "UNKNOWN"

    # ---- identity: union-find over registry number, acronym and protocol tokens -----
    parent = list(range(len(trial)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    by_reg, by_acr, by_strong, by_bare = {}, {}, {}, {}
    for i, r in enumerate(trial):
        reg = clean_registry(r.get("registry_id"))
        if reg:
            by_reg.setdefault(reg, []).append(i)
        acr = usable_label(r.get("trial_acronym"))
        if acr:
            by_acr.setdefault((programme(r), acr), []).append(i)
        for t in strong_tokens(r):
            by_strong.setdefault(t, []).append(i)
            # a registry-verified protocol code is the same identity as its registry number
            if t in REGISTRY_PROTOCOL:
                by_reg.setdefault(REGISTRY_PROTOCOL[t], []).append(i)
        prog = programme(r)
        for t in bare_tokens(r):
            # Qualified by the sponsor compound number, not by compound name. Where no
            # programme can be established -- neither the record's protocol nor its source
            # document names one -- a bare "CS2" identifies nothing and must not merge:
            # unqualified, it put nusinersen and volanesorsen in one cluster.
            if prog != "UNKNOWN":
                by_bare.setdefault((prog, t), []).append(i)

    for idx in list(by_reg.values()) + list(by_acr.values()) + list(by_strong.values()) + list(by_bare.values()):
        for j in idx[1:]:
            union(idx[0], j)

    merged = defaultdict(list)
    for i, r in enumerate(trial):
        merged[find(i)].append(r)
    folded = len(trial) - len(merged)

    rows = []
    for n, (k, rs) in enumerate(sorted(merged.items(), key=lambda x: -len(x[1])), 1):
        designs = {r.get("design", "") for r in rs}
        # A study reported as a trial in one document and summarised in another is a trial.
        # Pooled analyses can no longer reach this line, which is what used to promote them.
        design = "interventional_trial" if "interventional_trial" in designs else best(list(designs))
        regs = sorted({x for x in (clean_registry(r.get("registry_id")) for r in rs) if x})
        reg = regs[0] if regs else NR
        acr = best([r.get("trial_acronym") for r in rs])
        prot = best([r.get("sponsor_protocol") for r in rs])
        has_tok = any(strong_tokens(r) or bare_tokens(r) for r in rs)
        identity = ("registry_number" if regs else
                    "trial_acronym" if any(usable_label(r.get("trial_acronym")) for r in rs) else
                    "sponsor_protocol" if (prot != NR and has_tok) else
                    "sponsor_protocol_unqualified" if prot != NR else "no_identifier")
        evaluable = any(bool(r.get("endpoint_evaluable")) for r in rs)
        headline = (design in TRIAL_DESIGNS and evaluable
                    and identity in ("registry_number", "trial_acronym", "sponsor_protocol"))
        eps = sorted({e for r in rs for e in (r.get("coagulation_endpoints") or [])})
        cmp_ = sorted({c for r in rs for c in (r.get("compounds") or []) if not c.startswith("COG-OLG")})
        # The id is embedded in the compound string ("fitusiran (COG-OLG060)"), so it must be
        # extracted, not filtered. Filtering on startswith() found 5 of 30; this finds 24.
        olg = sorted({m for r in rs for c in (r.get("compounds") or [])
                      for m in re.findall(r"COG-OLG\d+", str(c))})
        fams = sorted(set().union(*[family(r) for r in rs]) if rs else [])
        subj = sorted(set().union(*[family(r, subject_only=True) for r in rs]) if rs else [])
        progs = sorted({programme(r) for r in rs} - {"UNKNOWN"})
        canon = sorted({PROGRAMME_ALIAS.get(p, p) for p in progs})
        same_registry_clash = len({registry_family(x) for x in regs}) < len(regs)

        flags = []
        if same_registry_clash:
            flags.append("OVER_MERGE_two_registry_numbers_same_registry")
        if len(canon) > 1:
            flags.append("OVER_MERGE_two_sponsor_programmes")
        if len(rs) > 1 and len(subj) > 1:
            # Two drugs under test in one cluster built from several documents. Could be a
            # genuine multi-arm trial; could be a bridge. Scientific call, so it is flagged.
            flags.append("two_subject_compounds_verify")
        if len(regs) > 1 and not same_registry_clash:
            # One trial, two registries. Beebop 2026-10-02: review the linkage, do not reject.
            flags.append("registry_alias_verify_linkage")
        if len(rs) > 8:
            flags.append("large_cluster_verify_not_an_over_merge")
        if len(designs) > 1:
            flags.append("design_disagreement_between_sources")

        rows.append({
            "study_id": "COG-STU%03d" % n,
            "design": design,
            "design_basis": "unanimous" if len(designs) == 1 else "mixed: " + "; ".join(sorted(designs)),
            "identity_basis": identity,
            "registry_id": reg,
            "registry_ids_all": "; ".join(regs) if regs else NR,
            "sponsor_programme": "; ".join(progs) if progs else NR,
            "compound_families": "; ".join(fams) if fams else NR,
            "subject_compound_families": "; ".join(subj) if subj else NR,
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
            "evidence_quote": quote_rights(best([r.get("evidence_quote") for r in rs])[:1200],
                                           {r.get("source_id", "") for r in rs}, red)[0],
            "evidence_quote_sha256": quote_rights(best([r.get("evidence_quote") for r in rs])[:1200],
                                                  {r.get("source_id", "") for r in rs}, red)[1],
            "evidence_quote_word_count": quote_rights(best([r.get("evidence_quote") for r in rs])[:1200],
                                                      {r.get("source_id", "") for r in rs}, red)[2],
            "evidence_quote_status": quote_rights(best([r.get("evidence_quote") for r in rs])[:1200],
                                                  {r.get("source_id", "") for r in rs}, red)[3],
            "locus": best([r.get("locus") for r in rs])[:400],
            "duplicate_of_hint": best([r.get("duplicate_of_hint") for r in rs])[:600],
            "review_flag": "; ".join(flags),
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    # ---- pooled analyses, published separately --------------------------------------
    # Kept as evidence (a regulatory pooled safety table is real) but never as a trial and
    # never as an identifier. member_protocols records which trials each pool re-reports, so
    # a pooled number can be traced instead of being attributed to one study.
    prows, seen = [], {}
    for r in sorted(pooled, key=lambda r: str(r.get("sponsor_protocol") or "")):
        prot = str(r.get("sponsor_protocol") or NR)
        fams = sorted(family(r))
        key = (tuple(fams), norm(prot)[:60], r.get("source_id"))
        if key in seen:
            continue
        seen[key] = 1
        members = sorted(strong_tokens(r) | bare_tokens(r))
        prows.append({
            "pool_id": "COG-POOL%03d" % (len(prows) + 1),
            "source_id": r.get("source_id", NR),
            "pool_descriptor": prot,
            "member_protocols": "; ".join(members) if members else NR,
            "n_member_protocols_named": len(members),
            "compound_families": "; ".join(fams) if fams else NR,
            "subject_compound_families": "; ".join(subj) if subj else NR,
            "compounds": "; ".join(sorted(str(c) for c in (r.get("compounds") or []))) or NR,
            "oligo_ids": "; ".join(sorted({m for c in (r.get("compounds") or [])
                                           for m in re.findall(r"COG-OLG\d+", str(c))})) or NR,
            "endpoint_evaluable": "TRUE" if r.get("endpoint_evaluable") else "FALSE",
            "coagulation_endpoints": "; ".join(r.get("coagulation_endpoints") or []) or NR,
            "enrolled": str(r.get("enrolled") or NR)[:400],
            "analysed": str(r.get("analysed") or NR)[:400],
            "population": str(r.get("population") or NR)[:300],
            "evidence_quote": quote_rights(str(r.get("evidence_quote") or NR)[:1200],
                                           {r.get("source_id", "")}, red)[0],
            "evidence_quote_sha256": quote_rights(str(r.get("evidence_quote") or NR)[:1200],
                                                  {r.get("source_id", "")}, red)[1],
            "evidence_quote_status": quote_rights(str(r.get("evidence_quote") or NR)[:1200],
                                                  {r.get("source_id", "")}, red)[3],
            "locus": str(r.get("locus") or NR)[:400],
            "counting_rule": "NOT a trial; never added to the human-trial total; its "
                             "participants overlap the member protocols named above",
        })
    with open(OUT_POOL, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(prows[0].keys()))
        w.writeheader(); w.writerows(prows)

    head = [r for r in rows if r["headline_trial"] == "TRUE"]
    print(f"  raw records {len(raw)}: {len(trial)} study records + {len(pooled)} pooled-analysis records")
    print(f"  pooled analyses published separately: {len(prows)} distinct "
          f"(data/pooled_analyses.csv) -- excluded from identity and from every trial count")
    print(f"  {len(trial)} study records -> {len(rows)} distinct studies ({folded} duplicate appearances merged)")
    print(f"  by design: {dict(Counter(r['design'] for r in rows))}")
    print(f"  identity:  {dict(Counter(r['identity_basis'] for r in rows))}")
    print(f"\n  HEADLINE human interventional trials with a coagulation endpoint: {len(head)}")
    print(f"    of which identified by registry number: {sum(1 for r in head if r['identity_basis']=='registry_number')}")
    bad = [r for r in rows if "OVER_MERGE" in r["review_flag"]]
    print(f"    clusters failing the over-merge check: {len(bad)}"
          + (f" ({', '.join(r['study_id'] for r in bad)})" if bad else ""))
    alias = [r for r in rows if "registry_alias" in r["review_flag"]]
    print(f"    registry aliases to verify (one trial, two registries): {len(alias)}")
    flagged = [r for r in head if r["review_flag"]]
    print(f"    flagged for manual verification before quoting: {len(flagged)}")
    excl = [r for r in rows if r["design"] == "interventional_trial" and r["headline_trial"] == "FALSE"]
    print(f"  trials registered but EXCLUDED from the headline: {len(excl)}"
          f"  ({sum(1 for r in excl if r['identity_basis']=='no_identifier')} unidentifiable,"
          f" {sum(1 for r in excl if r['endpoint_evaluable']=='FALSE')} no coagulation endpoint)")


if __name__ == "__main__":
    main()
