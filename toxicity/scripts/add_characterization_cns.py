#!/usr/bin/env python3
"""Tested-material characterization columns for the CNS oligo table.

WHY THESE COLUMNS EXIST, AND WHY THEY ARE MOSTLY EMPTY

The NIH/NCATS Phase 2 announcement makes this content mandatory, not optional.
The dataset "must contain the sequences of all oligos tested, as well as the
location of all chemical modifications in each oligo, DATA ON THE PURITY AND
CHARACTERIZATION OF EACH, and any additional metadata", and the methodology
document "should include the methods used to purify and characterize oligo
identity". The same announcement warns that "submission packages that are
missing listed materials may not be judged".

This corpus had no such columns at all. An earlier reply argued that a field is
pointless until there is evidence to put in it. That was wrong twice over: three
sibling datasets in this repository already carry these fields and populate them,
and a reader cannot otherwise tell "no purity was published" from "nobody
looked". Explicit missingness is the deliverable; an absent column is not.

THE DISTINCTION THIS PASS IS BUILT AROUND

Beebop's 2026-10-02 review rejected the obvious shortcut - filling analytical
identity from `design_source` - and was right to. `design_source` records where a
SEQUENCE was read from. That is reference identity: the designed molecule as some
document printed it. It says nothing about the vial that was actually dosed.
Conflating the two would manufacture the appearance of characterization, which is
worse than recording none. So:

    sequence_provenance    where the sequence text came from        (derivable)
    identity_confirmation  analysis of the TESTED MATERIAL          (not derivable)
    purity_method          how the tested material was purified     (not derivable)
    purity_pct             the purity value reported for it         (not derivable)

Only the first is computable from what this corpus holds. The other three are
`NOT_REPORTED` for every compound, because a full-text search of every row's
notes and source locus for purity values, purification methods (HPLC, UPLC, AEX,
mass spectrometry, desalting, salt exchange, phosphoramidite synthesis) and
identity-confirmation statements returns **zero hits across all 2,538
measurement rows and 592 oligo records**. That is the finding, and it is now
countable instead of invisible.

`NOT_APPLICABLE` is kept distinct from `NOT_REPORTED`: seven records are
class-level or cohort-level aggregates rather than molecules, and asking for the
purity of "the ASO class" is a category error, not a gap.

HOW A VALUE MAY EVER ENTER

Through `REPORTED` below, keyed on content, with the source locus required. The
table is empty. It must stay empty until someone reads a document that states a
value - the same no-fabrication rule that governs every other column here.

Usage:  python toxicity/scripts/add_characterization_cns.py [--check]
"""
import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
OLIGOS = os.path.join(TOXDIR, "notes", "cns", "corpus", "cns_oligos.csv")

NEW_COLS = ["sequence_provenance", "purity_pct", "purity_method",
            "identity_confirmation"]

NOT_REPORTED = "NOT_REPORTED"
NOT_APPLICABLE = "NOT_APPLICABLE"

# ---------------------------------------------------------------------------
# Reported tested-material characterization, read from a document.
#
# EMPTY ON PURPOSE. Keyed on oligo_id, each entry requiring the value, the
# document it was read from, and the exact locus inside it. Adding a row here is
# the only way a purity or identity value enters this dataset.
#
# Known leads, recorded so the next pass does not start from nothing:
#   - doi:10.1089/nat.2021.0071 (Hagedorn) supplies 181 molecules here. A sibling
#     lineage reports that this paper states a purification method and an
#     RP-UPLC-MS identity confirmation for its panel. NOT transcribed here:
#     second-hand report of another extraction is not a document read during this
#     curation. It is in the acquisition plan.
#   - Patent sequence listings (253 molecules) print designed sequences, not
#     batch certificates of analysis, so they are unlikely to close this.
# ---------------------------------------------------------------------------
REPORTED = {
    # "CNS###": {"purity_pct": "...", "purity_method": "...",
    #            "identity_confirmation": "...", "source": "...", "locus": "..."},
}

# A record that is not a molecule. `max_phase=class_review` marks a class-level
# or cohort-level aggregate - a safety database, an adverse-event atlas, a
# disease-background comparator - for which per-batch characterization is
# undefined rather than missing.
NON_COMPOUND_PHASE = "class_review"

# Where a sequence text came from, in the order tested. Order matters: a patent
# identifier is decided before the generic DOI pattern, and a supplement before
# the main text, because the more specific locus is the truer provenance.
PROVENANCE = [
    ("patent_sequence_listing", re.compile(r"\bUS\d{7,8}[AB]\d?", re.I)),
    ("publication_supplement", re.compile(
        r"suppl|table\s*s\d|mmc\d|supporting information|extended data", re.I)),
    ("who_inn_nomenclature", re.compile(
        r"\bINN\b|nomenclature|chemical name|longhand", re.I)),
    ("regulatory_document", re.compile(
        r"\bFDA\b|\bEMA\b|EPAR|SmPC|DailyMed|prescribing information|label", re.I)),
    ("publication_main_text", re.compile(
        r"^\s*(?:doi:|10\.\d{4})|\bPMID\b|\bPMC\d|figure|\bet al\b", re.I)),
    ("registry_metadata", re.compile(r"ClinicalTrials\.gov|\bNCT\d{8}", re.I)),
]


def canon_seq(s):
    return re.sub(r"[^ACGT]", "", (s or "").upper().replace("U", "T"))


def has_sequence(row):
    return len(canon_seq(row.get("sequence_5to3"))) >= 12


def sequence_provenance(row):
    """Where this record's sequence text came from, or why there is none."""
    if row.get("max_phase") == NON_COMPOUND_PHASE:
        return NOT_APPLICABLE
    if not has_sequence(row):
        # No sequence, so nothing has a provenance. Distinct from "we have a
        # sequence but did not record where it came from".
        return NOT_APPLICABLE
    ds = (row.get("design_source") or "").strip()
    if ds in ("", "TBD", "NA"):
        return NOT_REPORTED
    for name, rx in PROVENANCE:
        if rx.search(ds):
            return name
    return NOT_REPORTED


def characterization(row):
    """Purity and tested-batch identity: reported value, N/A, or NOT_REPORTED."""
    oid = row["oligo_id"]
    if row.get("max_phase") == NON_COMPOUND_PHASE:
        return NOT_APPLICABLE, NOT_APPLICABLE, NOT_APPLICABLE
    r = REPORTED.get(oid)
    if r:
        for req in ("source", "locus"):
            if not r.get(req):
                raise SystemExit("ERROR: REPORTED[%s] has no %s. A characterization "
                                 "value needs the document and the exact locus it "
                                 "was read from." % (oid, req))
        return (r.get("purity_pct", NOT_REPORTED),
                r.get("purity_method", NOT_REPORTED),
                r.get("identity_confirmation", NOT_REPORTED))
    return NOT_REPORTED, NOT_REPORTED, NOT_REPORTED


def main():
    check = "--check" in sys.argv
    with open(OLIGOS, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols, rows = list(rdr.fieldnames), list(rdr)

    before = {r["oligo_id"]: {c: r.get(c) for c in NEW_COLS} for r in rows}
    for r in rows:
        r["sequence_provenance"] = sequence_provenance(r)
        p, meth, ident = characterization(r)
        r["purity_pct"], r["purity_method"], r["identity_confirmation"] = p, meth, ident

    out_cols = cols + [c for c in NEW_COLS if c not in cols]

    for col in NEW_COLS:
        print("%s" % col)
        for k, v in Counter(r[col] for r in rows).most_common():
            print("  %-28s %4d" % (k, v))
    blank = [r["oligo_id"] for r in rows for c in NEW_COLS if not r[c].strip()]
    if blank:
        raise SystemExit("ERROR: %d blank characterization value(s): %s"
                         % (len(blank), blank[:5]))
    print("\nreported characterization values: %d of %d molecules"
          % (len(REPORTED), len(rows)))
    print("  (zero is the verified state of this corpus, not an omission: a "
          "full-text search\n   of every row's notes and source locus for purity "
          "values, purification methods\n   and identity-confirmation statements "
          "returns no hits)")

    if check:
        drift = [m for m, old in before.items()
                 if any(old[c] is not None for c in NEW_COLS)
                 and old != {c: next(r[c] for r in rows if r["oligo_id"] == m)
                             for c in NEW_COLS}]
        if drift:
            raise SystemExit("\nERROR: %d record(s) disagree with disk: %s"
                             % (len(drift), drift[:5]))
        print("\n--check: on-disk characterization matches")
        return

    with open(OLIGOS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        w.writerows(rows)
    print("\nwrote %s (%d columns)"
          % (os.path.relpath(OLIGOS, os.path.dirname(TOXDIR)), len(out_cols)))


if __name__ == "__main__":
    main()
