#!/usr/bin/env python3
"""Inventory every file in research staging with its checksum and provenance.

The research round requires: "Preserve checksums, source URLs, original
filenames, file/sheet inventories and provenance for staged files." Bulk
third-party content is not committed (see the staging .gitignore), so this
inventory is the committed record that makes any of it re-fetchable and
verifiable.
"""
import csv, hashlib, json, os, re

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(ENDPOINT, "curation", "research_staging")

# Retrieval URLs for files whose origin is recoverable from the filename.
KNOWN = {
    "sewing2017_pone.0187574_S1.xlsx":
        "https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0187574.s001",
}
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/{kind}"


def guess_url(fn):
    if fn in KNOWN: return KNOWN[fn]
    m = re.search(r"(PMC\d{6,8})", fn, re.I)
    if m:
        kind = "supplementaryFiles" if "suppl" in fn.lower() else "fullTextXML"
        return EPMC.format(pmcid=m.group(1).upper(), kind=kind)
    if "suppl" in fn.lower() or "fulltext" in fn.lower():
        return "Europe PMC REST (see the sweep coverage log for the exact query and pmcid)"
    return ""


def main():
    rows = []
    for fn in sorted(os.listdir(STAGE)):
        p = os.path.join(STAGE, fn)
        if not os.path.isfile(p) or fn in (".gitignore",):
            continue
        b = open(p, "rb").read()
        inner = ""
        if fn.endswith(".zip"):
            try:
                import zipfile
                with zipfile.ZipFile(p) as z:
                    inner = ";".join(f"{i.filename}({i.file_size})" for i in z.infolist()[:14])
            except Exception as e:
                inner = f"unreadable zip: {e}"
        elif fn.endswith(".xlsx"):
            try:
                import openpyxl
                wb = openpyxl.load_workbook(p, read_only=True)
                inner = ";".join(wb.sheetnames)
            except Exception as e:
                inner = f"unreadable xlsx: {e}"
        rows.append({
            "filename": fn, "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest(),
            "retrieval_url": guess_url(fn),
            "committed": "yes" if (fn.endswith((".csv", ".json", ".md"))
                                   or fn == "sewing2017_pone.0187574_S1.xlsx") else "no",
            "inner_inventory": inner[:400],
        })
    with open(os.path.join(STAGE, "staged_inventory.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    tot = sum(r["bytes"] for r in rows)
    print(f"staged_inventory.csv — {len(rows)} files, {tot/1e6:.1f} MB total")
    for r in rows:
        print(f"  {r['bytes']:>9d}  {'C' if r['committed']=='yes' else '-'}  {r['filename']}")


if __name__ == "__main__":
    main()
