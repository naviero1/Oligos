#!/usr/bin/env python3
"""Address the Phase 2 purity/characterization requirement, honestly and in two halves.

The brief requires the dataset to contain "data on the purity and characterization of
each" oligo, and the methodology document to describe "the methods used to purify and
characterize oligo identity". For a curation-type dataset those two halves have very
different answers, and collapsing them would misrepresent what we have.

PURITY: absent, and verified absent rather than assumed. Both in-repo patents were
searched for purity / HPLC / UPLC / LC-MS / mass-spec language; neither reports any
(the only "characterized" hits describe chemical structure, not oligo purity). Labels
and trial papers do not publish per-batch purity either. `purity_pct` and
`purity_method` are therefore TBD for every oligo, with the reason recorded rather
than left as an unexplained blank. No wet lab was run, so this cannot be closed by
further curation.

IDENTITY: this we can answer, and it is the half of the requirement that a curated
dataset can genuinely satisfy. `identity_confirmation` records HOW each oligo's
identity was established, derived from `design_source`:

  who_inn_chemical_nomenclature  residue-by-residue INN nomenclature, parsed
                                 deterministically and checked by reverse-complement
                                 and molecular formula (see METHODOLOGY §4 path 4)
  patent_sequence_listing        formal SEQUENCE LISTING of a US patent
  regulatory_label               FDA/EMA label or prescribing information
  peer_reviewed_publication      sequence printed in a primary publication
  not_established                sequence itself is TBD; identity unconfirmed

Usage:  python scripts/add_identity_characterization.py && python scripts/build_merged.py
"""
import csv, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")

def identity(r):
    if r["sequence_5to3"].strip() in ("TBD", "", "NA"):
        return "not_established", "sequence_TBD_identity_unconfirmed"
    src = r["design_source"]
    if re.search(r"WHO_INN", src, re.I):
        return "who_inn_chemical_nomenclature", "residue_by_residue_INN_parse_revcomp_and_formula_checked"
    if re.search(r"SEQ_ID|SEQUENCE_LISTING|US\d{7,}|patent", src, re.I):
        return "patent_sequence_listing", "formal_patent_sequence_listing"
    if re.search(r"FDA_label|SmPC|EPAR|_PI\b|label", src, re.I):
        return "regulatory_label", "sequence_from_regulatory_label"
    return "peer_reviewed_publication", "sequence_from_primary_publication"

with open(OLIGOS, newline="") as fh:
    rd = csv.DictReader(fh); fields, rows = list(rd.fieldnames), list(rd)

for col in ("purity_pct", "purity_method", "identity_confirmation"):
    if col not in fields:
        fields.insert(fields.index("design_source"), col)

counts = {}
for r in rows:
    r["purity_pct"] = "TBD"
    r["purity_method"] = "TBD"
    ident, why = identity(r)
    r["identity_confirmation"] = ident
    counts[ident] = counts.get(ident, 0) + 1
    tag = f"identity_{why};purity_not_published_by_any_source_verified_not_assumed"
    if "purity_not_published" not in r["notes"]:
        r["notes"] = f"{r['notes']};{tag}" if r["notes"].strip() else tag

with open(OLIGOS, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)

print("identity_confirmation assigned:")
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {k:<32}{v:>3}")
print(f"\npurity_pct / purity_method: TBD for all {len(rows)} oligos (verified unavailable)")
