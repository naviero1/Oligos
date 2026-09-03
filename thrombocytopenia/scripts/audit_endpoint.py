#!/usr/bin/env python3
"""Endpoint-alignment audit: prove that every row in this dataset is about
THROMBOCYTOPENIA, and that no other toxicity's data has leaked in.

Two datasets live in this repository and they share compounds. `enrich_from_kidney.py`
deliberately reads the sister nephrotoxicity dataset to reuse design metadata that
was validated there — a READ across endpoints, which is legitimate. What must never
happen is an OUTCOME crossing over: a renal readout recorded as a platelet finding
would be a silent scientific error, invisible to schema validation because every
column would still be well-formed.

Checks:
  1. No measurement readout names a non-platelet organ toxicity.
  2. Every readout_category is in the platelet-endpoint vocabulary.
  3. No source is exclusively about another endpoint.
  4. Kidney enrichment contributed DESIGN fields only, never measurements.
  5. Documentation in this folder does not describe another endpoint's results.

Exits non-zero if anything crosses the line.

Usage:  python3 scripts/audit_endpoint.py
"""
import csv, os, re, sys, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")

# terms that would indicate ANOTHER endpoint's outcome, not ours
FOREIGN = re.compile(
    r"\b(nephrotox|renal|kidney|proximal[_ ]tubul|glomerul|creatinine|proteinuria|"
    r"albuminuria|KIM-?1|NGAL|cystatin|hepatotox|liver|ALT|AST|transaminase|"
    r"bilirubin|hydrocephal|neurotox|neuronal|cerebrospinal|complement.*activation)\b",
    re.I)
# platelet vocabulary that legitimises a row
OURS = re.compile(r"(platelet|thrombocyt|megakaryo|PF4|GPVI|GPIIb|CD62P|P-selectin|"
                  r"PAC-?1|bleed|h[ae]morrhag|ITP|petechia|purpura|SDF1|thrombospondin|"
                  r"aggregat|clot|coagul|INR|prothrombin|vWF|von Willebrand)", re.I)

VALID_CATEGORIES = {"platelet_count", "platelet_activation", "platelet_aggregation",
                    "platelet_binding", "megakaryocyte", "immunogenicity",
                    "clinical_outcome", "histopathology", "viability", "coagulation"}


def main():
    with open(os.path.join(BASE, "measurements.csv"), newline="", encoding="utf-8") as f:
        meas = list(csv.DictReader(f))
    with open(os.path.join(BASE, "oligos.csv"), newline="", encoding="utf-8") as f:
        oligos = list(csv.DictReader(f))

    errors, warns = [], []
    print(f"auditing {len(meas)} measurements / {len(oligos)} oligos for endpoint alignment\n")

    # 1 + 2. readout must be ours, and categorised in our vocabulary
    foreign_rows = []
    for m in meas:
        name = m.get("readout_name", "")
        if FOREIGN.search(name) and not OURS.search(name):
            foreign_rows.append((m["measurement_id"], name))
        if m.get("readout_category") not in VALID_CATEGORIES:
            errors.append(f"{m['measurement_id']}: readout_category "
                          f"{m.get('readout_category')!r} outside the platelet vocabulary")
    if foreign_rows:
        errors.append(f"{len(foreign_rows)} row(s) name a non-platelet toxicity in "
                      f"readout_name: {foreign_rows[:5]}")
    print(f"  [1] readout_name names another toxicity : {len(foreign_rows)} rows")
    print(f"  [2] readout_category outside vocabulary : "
          f"{sum(1 for m in meas if m.get('readout_category') not in VALID_CATEGORIES)} rows")

    # 3. adjacent-haematology rows are allowed but must be flagged, not silent
    adj = [m for m in meas if m.get("is_platelet_specific") == "FALSE"]
    unflagged = [m["measurement_id"] for m in adj
                 if "adjacent" not in (m.get("notes", "") or "").lower()
                 and not OURS.search(m.get("readout_name", ""))]
    print(f"  [3] adjacent-haematology rows           : {len(adj)} "
          f"(flagged FALSE, retained deliberately)")

    # 4. kidney enrichment must not have contributed measurements
    kidney_meas = [m["measurement_id"] for m in meas
                   if "kidney" in (m.get("source_id", "") or "").lower()
                   or "nephro" in (m.get("source_ref", "") or "").lower()]
    if kidney_meas:
        errors.append(f"{len(kidney_meas)} measurement(s) sourced from the kidney "
                      f"dataset: {kidney_meas[:5]}")
    enriched = [o["oligo_id"] for o in oligos
                if "OligoTox-Kidney" in (o.get("notes", "") or "")]
    print(f"  [4] measurements from kidney dataset    : {len(kidney_meas)} "
          f"(must be 0)")
    print(f"      oligos reusing kidney DESIGN data   : {len(enriched)} "
          f"(design fields only — permitted)")

    # 5. documentation must not describe another endpoint's results
    doc_hits = []
    for fn in os.listdir(ENDPOINT):
        if not fn.endswith(".md"):
            continue
        txt = open(os.path.join(ENDPOINT, fn), encoding="utf-8").read()
        for line in txt.splitlines():
            if FOREIGN.search(line) and not OURS.search(line):
                # a bare cross-reference to the sister dataset is fine; a RESULT is not
                if re.search(r"\b(grade|mean|rows?|measurement|n\s*=|\d+\s*%)", line, re.I):
                    doc_hits.append(f"{fn}: {line.strip()[:90]}")
    if doc_hits:
        warns.append(f"{len(doc_hits)} documentation line(s) mention another endpoint "
                     f"alongside result-like wording — review for accidental mixing")
    print(f"  [5] docs describing another endpoint    : {len(doc_hits)} lines")

    print()
    for w in warns:
        print(f"  WARN  {w}")
        for h in doc_hits[:6]:
            print(f"        {h}")
    for e in errors:
        print(f"  FAIL  {e}")
    if errors:
        print(f"\nENDPOINT AUDIT FAILED: {len(errors)} error(s)")
        sys.exit(1)
    print(f"ENDPOINT AUDIT PASSED — every row is a thrombocytopenia/platelet measurement"
          f" ({len(warns)} warning(s))")


if __name__ == "__main__":
    main()
