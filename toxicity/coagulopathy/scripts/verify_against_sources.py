#!/usr/bin/env python3
"""Anti-fabrication check: every numeric readout must occur in its own source document.

    python3 toxicity/coagulopathy/scripts/verify_against_sources.py

validate_dataset.py proves the tables are internally consistent. This proves they are
consistent with the SOURCES: for each non-qualitative measurement, the printed number is
searched for in the retrieved document that row cites. It is a text-presence test, not a
semantic one -- it cannot tell whether a number was read from the right table cell, only
that the dataset did not invent it. Semantic checking is the verification pass recorded
in the dossier.

Exits non-zero if any value cannot be located.
"""
import csv, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "sources", "documents")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"
NUM = re.compile(r"^\s*[<>~≈]?\s*(-?[\d,]+(?:\.\d+)?)")

def normalise(s):
    """Fold the unicode a publisher uses for maths into ASCII before comparing.
    U+2212 MINUS, the en/em dashes and NBSP all appear in these sources and all break a
    naive string search."""
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("−", "-"), ("–", "-"), ("—", "-"), (" ", " "),
                 ("′", "'"), ("’", "'")):
        s = s.replace(a, b)
    return s

_cache = {}
def doctext(fn):
    if fn in _cache:
        return _cache[fn]
    p = os.path.join(DOCS, fn)
    t = ""
    if os.path.exists(p):
        raw = open(p, "rb").read().decode("utf-8", "ignore")
        # Strip markup ONLY for markup files. A patent .txt legitimately contains '<' and
        # '>', and a tag regex over it deletes whole tables -- which once made this very
        # check report 120 false fabrications.
        if fn.lower().endswith((".xml", ".html", ".htm")):
            raw = re.sub(r"<[^<>]{0,400}?>", " ", raw)
        t = re.sub(r"\s+", " ", normalise(raw))
    _cache[fn] = t
    return t

def main():
    S = {r["source_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "sources.csv")))}
    D = list(csv.DictReader(open(os.path.join(ROOT, "data", "measurements.csv"))))
    res, absent, nofile = Counter(), [], defaultdict(int)

    for r in D:
        if r["readout_is_qualitative"] == "TRUE" or r["readout_value"] in (NR, NA):
            res["skipped_qualitative_or_no_value"] += 1
            continue
        src = S.get(r["source_id"])
        fn = (src or {}).get("document_file", NR)
        t = doctext(fn) if fn not in (NR, "") else ""
        if not t:
            res["skipped_no_local_document"] += 1
            nofile[fn] += 1
            continue
        m = NUM.match(normalise(str(r["readout_value"])))
        if not m:
            res["skipped_value_not_numeric"] += 1
            continue
        v = m.group(1)
        if v in t or v.lstrip("-") in t:
            res["verified_present_in_source"] += 1
        else:
            res["ABSENT"] += 1
            absent.append((r["measurement_id"], r["source_id"], v, r["readout_name"]))

    for k, v in res.most_common():
        print(f"  {v:>5}  {k}")
    if nofile:
        print("\n  documents not held locally (rows skipped, not failed):")
        for fn, n in nofile.items():
            print(f"    {n:>4} rows cite {fn}")
    if absent:
        print(f"\n  {len(absent)} values NOT found in their cited source:")
        for a in absent[:20]:
            print("   ", a)
        sys.exit(1)
    checked = res["verified_present_in_source"]
    print(f"\n{checked}/{checked} checkable numeric values located in their cited source document")

    # ---- purity and characterisation evidence ------------------------------------------
    # The characterisation recovered from the regulatory quality sections was checked by an
    # independent agent pass at extraction time; this makes the same check part of the
    # deterministic build, so the evidence stays verifiable on every rebuild rather than
    # resting on a one-off review. Each quote must appear in its cited file, and each purity
    # value must be printed there.
    opath = os.path.join(ROOT, "data", "oligos.csv")
    srcs = {r["source_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "sources.csv"),
                                                          newline="", encoding="utf-8"))}
    pres = Counter()
    pbad = []
    _cpath = os.path.join(ROOT, "sources", "characterisation.json")
    _orig_purity_quote = {}
    if os.path.exists(_cpath):
        for _r in json.load(open(_cpath, encoding="utf-8"))["records"]:
            _q = str(_r.get("verbatim_quote", "") or "")
            if _q and _r.get("oligo_id") not in _orig_purity_quote:
                _orig_purity_quote[_r.get("oligo_id")] = _q
    for o in csv.DictReader(open(opath, newline="", encoding="utf-8")):
        sid = o.get("purity_source_id", "")
        quote = o.get("purity_evidence_quote", "")
        # A quote withheld for licence reasons is not published, but it still has to be
        # verifiable on every build, so verification reads the ORIGINAL from the curation
        # input we hold rather than the redacted column. Withholding protects the publisher;
        # it must not weaken the check.
        if str(quote).startswith("WITHHELD_SOURCE_LICENCE_RESTRICTED"):
            quote = _orig_purity_quote.get(o["oligo_id"], "")
            if not quote:
                pres["withheld_and_original_unavailable"] += 1
                continue
        if sid in ("", NR, "NOT_APPLICABLE") or quote in ("", NR, "NOT_APPLICABLE"):
            continue
        fn = srcs.get(sid, {}).get("document_file", "")
        t = doctext(fn)
        if t is None:
            pres["document_not_held"] += 1
            continue
        # The stored quote is faithful to the file's bytes, so a quote taken from an SPL
        # or JATS document can itself contain tags. doctext() strips markup from markup
        # files, so the quote must be stripped the same way or a faithful quote fails.
        q = quote
        if fn.lower().endswith((".xml", ".html", ".htm")):
            q = re.sub(r"<[^<>]{0,400}?>", " ", q)
        q = re.sub(r"\s+", " ", normalise(q)).strip()
        if q[:300] in normalise(t):
            pres["quote_located"] += 1
        else:
            pres["QUOTE_ABSENT"] += 1
            pbad.append((o["oligo_id"], sid, quote[:80]))
        for entry in str(o.get("purity_batches", "")).split(";"):
            m = re.search(r"(\d{1,3}(?:\.\d+)?)%", entry)
            if not m:
                continue
            if m.group(1) in t:
                pres["purity_value_located"] += 1
            else:
                pres["PURITY_VALUE_ABSENT"] += 1
                pbad.append((o["oligo_id"], sid, "purity " + m.group(1)))
    if pres:
        print("\n  purity / characterisation evidence:")
        for k, v in pres.most_common():
            print(f"  {v:>5}  {k}")
    if pbad:
        print(f"\n  {len(pbad)} purity items NOT found in their cited source:")
        for a in pbad[:15]:
            print("   ", a)
        sys.exit(1)

if __name__ == "__main__":
    main()
