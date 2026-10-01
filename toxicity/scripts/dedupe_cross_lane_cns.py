#!/usr/bin/env python3
"""Remove observations extracted twice, once per extraction lane.

WHY THIS EXISTS, AND WHY IT IS NOT IN THE ASSEMBLER

`assemble_cns.py` already de-duplicates, on a semantic key built from the row's
own values (oligo, model, region, delivery, dose, readout, duration). That key
cannot catch the duplication handled here, because the two copies DISAGREE ON
THEIR VALUES while describing one observation:

    CMS1300  CNSSRC_CTG_NCT04089566  'CSF pressure increased'  2_of_40  n_of_N
    CMS1450  CT_NCT04089566          'CSF pressure increased'  5.0      pct_incidence

2/40 IS 5.0%. One number, two encodings, two lanes: the curated ClinicalTrials.gov
hand-extraction and the ClinicalTrials.gov API sweep read the same posted table.
The semantic key sees two different readout_values and keeps both.

What does identify them is the OBSERVATION, not the value: one trial, one
compound, one endpoint, one adverse-event term, one arm, one seriousness table.
That is the key below.

The pass runs AFTER assembly, on the corpus CSV, and never renumbers. Ids are
issued sequentially by the assembler (`CMS%04d`), so deleting inside it would
shift every later id and invalidate every verification record and cross-reference
written against them. A gap in the id sequence is the correct outcome of a
deletion; a silent renumbering is not.

Each decision below is keyed on CONTENT rather than on a measurement_id, so it
survives re-assembly, and records which copy was kept and why.

Usage:  python toxicity/scripts/dedupe_cross_lane_cns.py [--dry-run]
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
CORPUS = os.path.join(TOXDIR, "notes", "cns", "corpus", "cns_measurements.csv")

NCT = re.compile(r"NCT\d{8}")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", ("" if s is None else str(s)).lower())


def trial_of(row):
    m = NCT.search(row.get("source_ref", "") or "")
    return m.group(0) if m else ""


def seriousness(row):
    """Which ClinicalTrials.gov adverse-event table a row came from.

    The posted AE module reports serious and non-serious events in SEPARATE
    arrays, and the same participant can appear in both. Two rows differing only
    in this are two different reported counts, not a duplicate, so it belongs in
    the identity key rather than being ignored.
    """
    t = (row.get("source_table", "") or "").lower()
    if "seriousevents" in t or "serious adverse event" in t:
        return "serious"
    if "otherevents" in t or "not including serious" in t:
        return "nonserious"
    return "unspecified"


def lane(row):
    """The extraction lane, read off the source_id convention it was filed under."""
    sid = row.get("source_id", "") or ""
    if sid.startswith("CT_NCT"):
        return "ctgov_api_sweep"
    if sid.startswith("CNSSRC_CTG_"):
        return "ctgov_curated"
    return "other"


# ---------------------------------------------------------------------------
# The adjudicated duplicates. Both were found by grouping the corpus on
# (trial, oligo, endpoint_domain, normalised readout) and then reading every
# group with rows from more than one lane. Only these two survived that reading:
# every other multi-row group is a distinct arm, dose, timepoint, or the
# serious/non-serious pair described above.
#
# D1. DEVOTE (NCT04089566) Part C, 50/28 mg nusinersen, 'CSF pressure increased'.
#     KEEP CMS1300 (curated lane). It carries the denominator as posted (2/40)
#     rather than a derived percentage, and its notes carry the ascertainment
#     evidence that matters for this row - that the DEVOTE AE table has
#     frequencyThreshold=0, so a zero in it is a true zero and not a reporting
#     artefact. The API copy carries neither.
#     A verifier had already spotted this pair and wrote it into CMS1450's notes
#     ("of which this is a duplicate under the other source_id convention"), but
#     nothing acted on it. This is that action.
#
# D2. GENERATION HD1 (NCT03342053) Monthly arm, 'Cerebral ventricle dilatation'.
#     KEEP CMS1272 (curated lane). 2/23 = 8.7%, the same non-serious event.
#     The curated lane additionally holds the matched bimonthly comparator
#     (CMS1271, 0/23), which is what makes the monthly/bimonthly contrast
#     readable; the API copy is the monthly arm alone.
# ---------------------------------------------------------------------------
DROP = [
    {
        "id": "D1",
        "trial": "NCT04089566",
        "oligo_id": "CNS012",
        "endpoint_domain": "hydrocephalus",
        "readout": "csfpressureincreased",
        "seriousness": "nonserious",
        "drop_lane": "ctgov_api_sweep",
        "keep": "the curated copy, which carries the posted denominator and the "
                "frequency-threshold evidence",
    },
    {
        "id": "D2",
        "trial": "NCT03342053",
        "oligo_id": "CNS014",
        "endpoint_domain": "hydrocephalus",
        "readout": "cerebralventricledilatation",
        "seriousness": "nonserious",
        "arm_contains": "monthly",
        "arm_excludes": "bimonthly",
        "drop_lane": "ctgov_api_sweep",
        "keep": "the curated copy, which is paired with its bimonthly comparator row",
    },
]


def matches(row, d):
    if trial_of(row) != d["trial"]:
        return False
    if row.get("oligo_id") != d["oligo_id"]:
        return False
    if row.get("endpoint_domain") != d["endpoint_domain"]:
        return False
    if norm(row.get("readout_name")) != d["readout"]:
        return False
    if seriousness(row) != d["seriousness"]:
        return False
    if lane(row) != d["drop_lane"]:
        return False
    arm = (row.get("source_table", "") or "").lower()
    if "arm_excludes" in d and d["arm_excludes"] in arm:
        return False
    if "arm_contains" in d and d["arm_contains"] not in arm:
        return False
    return True


def scan(rows):
    """Report every group of rows that could be one observation counted twice.

    Returned so the caller can fail if a NEW cross-lane group appears that no
    decision above covers - the point being that the next such duplicate is
    surfaced rather than silently shipped.
    """
    groups = {}
    for r in rows:
        t = trial_of(r)
        if not t:
            continue
        k = (t, r.get("oligo_id"), r.get("endpoint_domain"),
             norm(r.get("readout_name")), seriousness(r))
        groups.setdefault(k, []).append(r)
    return {k: v for k, v in groups.items()
            if len({lane(x) for x in v}) > 1}


def main():
    dry = "--dry-run" in sys.argv
    with open(CORPUS, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols, rows = rdr.fieldnames, list(rdr)

    kept, removed = [], []
    for r in rows:
        hit = next((d for d in DROP if matches(r, d)), None)
        if hit:
            removed.append((hit, r))
        else:
            kept.append(r)

    for d, r in removed:
        print("%s  drop %s  %s / %s / %s  (%s %s)  -- keeping %s"
              % (d["id"], r["measurement_id"], d["trial"], r["oligo_id"],
                 r["readout_name"], r["readout_value"], r["readout_unit"], d["keep"]))
    if not removed:
        print("no rows matched the adjudicated duplicates "
              "(already removed, or the corpus was rebuilt without them)")

    leftover = scan(kept)
    if leftover:
        print("\nERROR: %d cross-lane group(s) remain unadjudicated:" % len(leftover))
        for k, v in sorted(leftover.items()):
            print("  %s" % (k,))
            for x in v:
                print("     %s  %s  %s %s" % (x["measurement_id"], x["source_id"],
                                              x["readout_value"], x["readout_unit"]))
        raise SystemExit("add a decision to DROP, or record why the group is legitimate")

    print("\n%d rows in, %d removed, %d out" % (len(rows), len(removed), len(kept)))
    if dry:
        print("--dry-run: nothing written")
        return
    if removed:
        with open(CORPUS, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(kept)
        print("wrote %s" % os.path.relpath(CORPUS, os.path.dirname(TOXDIR)))


if __name__ == "__main__":
    main()
