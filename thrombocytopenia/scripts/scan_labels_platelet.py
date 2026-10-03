#!/usr/bin/env python3
"""Sweep FDA prescribing information (DailyMed SPL) for every approved
oligonucleotide therapeutic and report its platelet / thrombocytopenia content.

Why this exists: negative controls are the hardest class to populate in a
toxicity dataset, because a compound with no platelet signal usually generates no
publication. Regulatory labels are the exception — safety monitoring is reported
whether or not it was eventful — so a systematic label sweep is the most reliable
way to source well-evidenced grade-0 rows alongside the positives.

Output is a per-drug report of every sentence mentioning platelets or
thrombocytopenia, with its label context, for hand-curation into the schema.
A drug whose current label contains NO platelet sentence is reported explicitly
as such: that absence is itself evidence, but it must be recorded as
"not mentioned in label" and graded only against a source that actually reports
platelet monitoring — never assumed to be a measured zero.

Usage:  python3 scripts/scan_labels_platelet.py [outfile.json]
"""
import json, re, ssl, sys, time, urllib.parse, urllib.request

CA = "/root/.ccr/ca-bundle.crt"
try:
    CTX = ssl.create_default_context(cafile=CA)
except Exception:
    CTX = ssl.create_default_context()

API = "https://dailymed.nlm.nih.gov/dailymed/services/v2"

# Approved / late-stage oligonucleotide therapeutics, by modality.
DRUGS = [
    # 2'-MOE PS ASO gapmers — the class with the platelet signal
    ("inotersen", "ASO_gapmer"), ("mipomersen", "ASO_gapmer"),
    ("eplontersen", "ASO_gapmer"), ("olezarsen", "ASO_gapmer"),
    ("volanesorsen", "ASO_gapmer"),
    # splice-switching / steric block
    ("nusinersen", "splice_switching_ASO"), ("tofersen", "splice_switching_ASO"),
    # PMO — neutral backbone, expected negative
    ("eteplirsen", "PMO"), ("golodirsen", "PMO"),
    ("viltolarsen", "PMO"), ("casimersen", "PMO"),
    # siRNA / GalNAc-siRNA — expected negative
    ("patisiran", "siRNA"), ("givosiran", "GalNAc_siRNA"),
    ("lumasiran", "GalNAc_siRNA"), ("inclisiran", "GalNAc_siRNA"),
    ("vutrisiran", "GalNAc_siRNA"), ("nedosiran", "GalNAc_siRNA"),
    # aptamer / other nucleic-acid drugs with known platelet biology
    ("pegaptanib", "aptamer"), ("defibrotide", "other"), ("imetelstat", "other"),
    ("fomivirsen", "other"),
]

KW = re.compile(r"(thrombocytopeni|platelet|thrombocyt)", re.I)
# label section headings we want to attribute a hit to
SEC = re.compile(r"(BOXED WARNING|WARNING[S]?(?: AND PRECAUTIONS)?|ADVERSE REACTIONS|"
                 r"CONTRAINDICATIONS|CLINICAL PHARMACOLOGY|NONCLINICAL TOXICOLOGY|"
                 r"DOSAGE AND ADMINISTRATION|USE IN SPECIFIC POPULATIONS)", re.I)


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": "OligoTox-Thrombo/1.0 (research)"})
    data = urllib.request.urlopen(req, context=CTX, timeout=45).read()
    return data if raw else data.decode("utf-8", "replace")


def strip_xml(x):
    x = re.sub(r"<[^>]+>", " ", x)
    return re.sub(r"\s+", " ", x)


def scan(drug):
    """Return {setid, title, hits:[sentence...]} for a drug, or an error marker."""
    try:
        j = json.loads(get(f"{API}/spls.json?drug_name={urllib.parse.quote(drug)}"))
    except Exception as e:
        return {"drug": drug, "error": f"lookup failed: {e}"}
    data = j.get("data") or []
    if not data:
        return {"drug": drug, "error": "no SPL found (may not be FDA-approved)"}
    # prefer the highest spl_version (most current label)
    entry = sorted(data, key=lambda d: d.get("spl_version", 0), reverse=True)[0]
    setid = entry["setid"]
    try:
        text = strip_xml(get(f"{API}/spls/{setid}.xml"))
    except Exception as e:
        return {"drug": drug, "setid": setid, "error": f"fetch failed: {e}"}

    sentences = re.split(r"(?<=[.:;])\s+", text)
    hits, seen = [], set()
    for i, s in enumerate(sentences):
        if not KW.search(s):
            continue
        s = s.strip()
        if len(s) < 25 or s in seen:
            continue
        seen.add(s)
        # nearest preceding section heading, for source_table attribution
        ctx = ""
        for back in range(i, max(-1, i - 40), -1):
            m = SEC.search(sentences[back])
            if m:
                ctx = m.group(0).upper()
                break
        hits.append({"section": ctx, "text": s[:600]})
    return {"drug": drug, "setid": setid, "title": entry.get("title"),
            "spl_version": entry.get("spl_version"),
            "published": entry.get("published_date"),
            "n_hits": len(hits), "hits": hits[:40]}


def main():
    out = []
    for drug, cls in DRUGS:
        r = scan(drug)
        r["oligo_class"] = cls
        out.append(r)
        if "error" in r:
            print(f"  {drug:<14} {cls:<22} !! {r['error']}")
        else:
            flag = "PLATELET CONTENT" if r["n_hits"] else "no platelet mention"
            print(f"  {drug:<14} {cls:<22} {r['n_hits']:>3} hits   {flag}")
        time.sleep(0.4)  # be polite to DailyMed

    path = sys.argv[1] if len(sys.argv) > 1 else "label_platelet_scan.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")
    print("NOTE: 'no platelet mention' is NOT itself a measured grade-0. It means the "
          "label does not discuss platelets; a grade-0 row still requires a source that "
          "reports platelet monitoring having been done.")


if __name__ == "__main__":
    main()
