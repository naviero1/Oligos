#!/usr/bin/env python3
"""Stage the Sewing 2017 raw-data workbook as condition-level research evidence.

STAGING, NOT INGESTION
  Output goes to curation/research_staging/, NOT to data/. Nothing here enters
  the validated dataset, any label, any adjudication or any model. The research
  round authorises acquisition into clearly separate staging and nothing more.

WHY THIS FILE MATTERS
  Phase 2 singles out "datasets based on in vitro human systems". The scientist
  package's own matched mechanistic contrasts (MCON-TMB-002/003/004, the AC-series
  PS vs LNA-PS pairs) currently rest on an adjudicated 0-3 ordinal score per
  construct. This workbook carries the PER-REPLICATE measurements underneath
  those scores, with matched negative and positive activation controls in the
  same assay run. That is the input the conditionally-approved human mechanistic
  lane needs, and it is the evidence class the challenge weights highest.

WHAT IT IS NOT
  Not independent biological replication. These are the measurements the source
  publication reports; recovering them reconstructs existing records at finer
  grain. It does not externally validate anything.

EXTRACTION PHILOSOPHY
  Rather than normalise each of six heterogeneously laid out sheets into a guessed
  schema, this emits EVERY numeric cell with the context needed to audit it: the
  endpoint block it sits under, its row label, its column header, and its exact
  cell coordinate. A reader can reconstruct any figure from this and check it
  against the source. Guessing a tidy schema would lose the locus, which is the
  one thing staging must preserve.

Usage:  python3 scripts/stage_sewing2017.py <path-to-sewing2017_S1.xlsx>
"""
import csv, hashlib, json, os, re, sys

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.join(ENDPOINT, "curation", "research_staging")
os.makedirs(STAGE, exist_ok=True)

PROV = {
    "source_title": "Sewing S, Roth AG, Winter M, et al. Assessing single-stranded "
                    "oligonucleotide drug-induced effects in vitro reveals key risk factors "
                    "for thrombocytopenia.",
    "journal": "PLOS ONE", "year": 2017,
    "doi": "10.1371/journal.pone.0187574",
    "pmid": "29095938", "pmcid": "PMC5673186",
    "supplement": "S1 File (raw data workbook)",
    "retrieval_url": "https://journals.plos.org/plosone/article/file?"
                     "type=supplementary&id=10.1371/journal.pone.0187574.s001",
    "retrieved": "2026-10-02",
    "licence": "PLOS ONE publishes under CC BY 4.0 — verify on the article page before release",
    "access_barrier": "none; HTTP 200, no login, no paywall",
}

# Text that names a measured endpoint, used to label each block.
ENDPOINT_PAT = re.compile(
    r"MFI|%\s*binding|%\s*heparin|OD450|\[ATPi\]|MCP1|Stimulation Index|aggregation",
    re.I)
# Rows that define replicate/column structure.
HEADER_PAT = re.compile(r"^\s*(condition|axis label|c \[|conc\b)", re.I)
# Controls present in the same assay runs.
CONTROLS = {
    "neg ctrl": "negative_control_unstimulated",
    "adp": "positive_control_agonist",
    "trap": "positive_control_agonist",
    "+ ps": "backbone_control_phosphorothioate",
    "- ps": "backbone_control_phosphodiester",
    "pbs": "vehicle_control",
    "r848": "positive_control_TLR7_8",
    "cpg": "positive_control_TLR9",
    "poly dc": "control_poly_dC",
    "heparin": "comparator_heparin",
}
# The alternating-AC series is labelled by LENGTH in nucleotides on some sheets.
AC_BY_LEN = {10: "(AC)5", 12: "(AC)6", 14: "(AC)7", 16: "(AC)8",
             18: "(AC)9", 20: "(AC)10", 22: "(AC)11"}


def control_class(label):
    l = (label or "").strip().lower()
    for k, v in CONTROLS.items():
        if l == k or l.startswith(k):
            return v
    return ""


def construct_of(label):
    """Map a row label to the construct it denotes, where unambiguous."""
    l = (label or "").strip()
    if re.fullmatch(r"\d{2}", l) and int(l) in AC_BY_LEN:
        return AC_BY_LEN[int(l)], f"length {l} nt of the alternating-AC series"
    m = re.match(r"AC\s*\(?(\d{1,2})\)?\s*(\+?\s*LNA)?", l, re.I)
    if m:
        base = f"(AC){m.group(1)}"
        return (base + (" + LNA" if m.group(2) else ""), "named in the source sheet")
    if re.search(r"ODN\s*2395", l, re.I):
        return ("ODN 2395 Thio" if re.search(r"thio", l, re.I) else "ODN 2395"), "named in the source sheet"
    return "", ""


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src or not os.path.exists(src):
        sys.exit("usage: stage_sewing2017.py <path-to-sewing2017_S1.xlsx>")
    import openpyxl

    raw = open(src, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    fn = "sewing2017_pone.0187574_S1.xlsx"
    with open(os.path.join(STAGE, fn), "wb") as f:
        f.write(raw)

    wb = openpyxl.load_workbook(src, data_only=True)
    rows, sheets = [], []

    for ws in wb.worksheets:
        grid = {}
        for r in ws.iter_rows():
            for c in r:
                if c.value is not None:
                    grid[(c.row, c.column)] = c.value

        # rows that look like structural headers, and the replicate labels on them
        header_rows = {}
        for (rr, cc), v in grid.items():
            if isinstance(v, str) and HEADER_PAT.match(v):
                labels = {}
                for (r2, c2), v2 in grid.items():
                    if r2 == rr and c2 > cc:
                        labels[c2] = v2
                if labels:
                    header_rows[rr] = labels

        # text cells naming an endpoint, as block anchors
        anchors = sorted([(rr, cc, v) for (rr, cc), v in grid.items()
                          if isinstance(v, str) and ENDPOINT_PAT.search(v)])

        n_sheet = 0
        for (rr, cc), v in sorted(grid.items()):
            if not isinstance(v, (int, float)):
                continue
            # nearest endpoint anchor at or above this row
            block = ""
            for (ar, ac, av) in anchors:
                if ar <= rr:
                    block = str(av).strip()
                else:
                    break
            # row label: nearest text cell to the left on this row
            row_label = ""
            for c2 in range(cc - 1, 0, -1):
                x = grid.get((rr, c2))
                if isinstance(x, str) and x.strip():
                    row_label = x.strip(); break
                if isinstance(x, (int, float)) and c2 == 1:
                    row_label = str(x); break
            if not row_label:
                x = grid.get((rr, 1))
                if x is not None:
                    row_label = str(x).strip()
            # column header: the replicate/series label from the nearest header row above
            col_header, hdr_row = "", None
            for hr in sorted(header_rows):
                if hr <= rr:
                    hdr_row = hr
            if hdr_row is not None:
                col_header = str(header_rows[hdr_row].get(cc, "")).strip()
            construct, basis = construct_of(row_label)
            # Side-by-side block layout: several sheets put two constructs in one
            # row band, e.g. "A42=AC(8) ... I42=AC(8) + LNA", with data rows
            # beneath BOTH. A left-scan on the data row finds nothing for the
            # right-hand block, which silently dropped AC(9) + LNA -- one of the
            # three matched contrasts this file exists to support. So when the row
            # label does not resolve to a construct, climb upward through this
            # column band for the nearest text cell that does.
            if not construct:
                best = None
                for c2 in (cc, cc - 1, cc - 2):
                    if c2 < 1: continue
                    for r2 in range(rr - 1, max(0, rr - 14), -1):
                        x = grid.get((r2, c2))
                        if isinstance(x, str) and x.strip():
                            cand, _ = construct_of(x)
                            if cand:
                                d = rr - r2
                                if best is None or d < best[0]:
                                    best = (d, cand, f"block header {chr(64+c2)}{r2} "
                                                     f"in a side-by-side layout")
                            break
                if best:
                    construct, basis = best[1], best[2]
            rows.append({
                "staging_id": f"SEW-{len(rows)+1:05d}",
                "source_sheet": ws.title,
                "source_cell": f"{ws.title}!{chr(64+cc) if cc<=26 else ''}{rr}"
                               if cc <= 26 else f"{ws.title}!R{rr}C{cc}",
                "endpoint_block": block,
                "row_label": row_label,
                "column_header": col_header,
                "replicate_or_series": col_header,
                "value": v,
                "construct_named": construct,
                "construct_basis": basis,
                "control_class": control_class(row_label),
                "assay_context": f"{ws.title} / {block}" if block else ws.title,
                "human_system": "human platelets / PRP / whole blood (per source methods)",
                "qualification": "STAGED RAW VALUE — not validated, not adjudicated, "
                                 "not entered in the dataset",
            })
            n_sheet += 1
        sheets.append({"sheet": ws.title, "numeric_cells_staged": n_sheet,
                       "endpoint_blocks": sorted({str(a[2]).strip() for a in anchors})})

    cols = list(rows[0].keys())
    with open(os.path.join(STAGE, "sewing2017_condition_level.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

    manifest = {
        **PROV, "staged_filename": fn, "sha256": sha, "bytes": len(raw),
        "sheets": sheets, "total_values_staged": len(rows),
        "controls_present": sorted({r["control_class"] for r in rows if r["control_class"]}),
        "constructs_named": sorted({r["construct_named"] for r in rows if r["construct_named"]}),
        "scope_note": "Staged for research review only. Does not enter data/, any label, "
                      "any scientific adjudication or any model. Recovering these values "
                      "reconstructs the source publication's own measurements at finer "
                      "grain; it is NOT independent biological replication.",
    }
    with open(os.path.join(STAGE, "sewing2017_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)

    print(f"staged {len(rows)} numerical observations -> curation/research_staging/")
    print(f"  file   {fn}  ({len(raw)} bytes)\n  sha256 {sha}")
    for s in sheets:
        print(f"  {s['sheet']:10s} {s['numeric_cells_staged']:5d} values   blocks: "
              f"{', '.join(s['endpoint_blocks'][:4])}")
    print(f"\n  controls present : {', '.join(manifest['controls_present'])}")
    print(f"  constructs named : {', '.join(manifest['constructs_named'])}")


if __name__ == "__main__":
    main()
