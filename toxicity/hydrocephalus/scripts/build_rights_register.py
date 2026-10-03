#!/usr/bin/env python3
"""
Source-level rights register for the hydrocephalus endpoint.

Layer 1 of Crank's project-wide rights proposal (CRANK_PROPOSAL_RIGHTS_TAGGING_
2026-10-03.md §2): one row per source, carrying what was OBSERVED about its terms
and what disposition is PROPOSED. Row-level tags are derived from this by a join
and are not written by hand.

Deliberately NOT written into data/. Adding a rights column to measurements.csv
is an ingestion step and ingestion is gated on the Tier 0 crosswalk, so this lands
in notes/ as a proposal that the crosswalk can consume.

Three things this file must never do, per §5 of that proposal and §A of
SCIENTIFIC_RULES.md:
  * assert legal clearance -- it records an observation and a proposal;
  * resolve a conflict -- where no licence is declared, the row says so;
  * invent evidence -- licence_evidence quotes data/sources.csv and names the
    column it came from. Where terms were never examined, it says that too,
    which is why this register carries a fifth tier Crank's four do not have.

Usage: python3 scripts/build_rights_register.py
"""
import collections
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Observed licence string -> (tier, source-file republication, extracted-data
# reuse proposal, basis). The tiers are Crank's A/B/C/D plus U.
#
# U IS A PROPOSED ADDITION, and the reason matters. Crank's tier D is "nothing
# stated by the publisher at all" -- an examined source with no terms. Sixteen
# sources here were never examined for terms: data/sources.csv records "reuse
# terms not established in this session". Calling that D would assert that the
# publisher declares nothing, which is a claim about WHO and the EMA that no one
# here checked. U keeps the two apart until someone opens the terms page.
TIERS = {
    "US Government work / public domain": (
        "A", "YES", "RELEASE",
        "17 U.S.C. 105: a work of the US federal government carries no copyright."),
    "CC BY 4.0": (
        "B", "YES", "RELEASE", "CC BY permits reuse with attribution."),
    "CC BY 2.0": (
        "B", "YES", "RELEASE", "CC BY permits reuse with attribution."),
    "CC BY-NC": (
        "C", "CONDITIONAL_NON_COMMERCIAL", "DECISION_REQUIRED",
        "NC restricts commercial reuse. Terms exist and restrict."),
    "CC BY-NC-ND": (
        "C", "CONDITIONAL_NON_COMMERCIAL_NO_DERIVATIVES", "DECISION_REQUIRED",
        "NC restricts commercial reuse; ND forbids derivatives of the work. "
        "Measured values are facts, not the work -- but that basis is Oscar's "
        "to adopt, not this script's to assume."),
    "CC BY-NC-ND 4.0": (
        "C", "CONDITIONAL_NON_COMMERCIAL_NO_DERIVATIVES", "DECISION_REQUIRED",
        "NC restricts commercial reuse; ND forbids derivatives of the work. "
        "Measured values are facts, not the work -- but that basis is Oscar's "
        "to adopt, not this script's to assume."),
}
UNEXAMINED = ("U", "UNKNOWN", "DECISION_REQUIRED",
              "The publisher's terms were NOT examined in this session. This is "
              "not a finding that no licence is declared.")

COLS = ["source_ref", "citation_short", "declared_licence", "licence_evidence",
        "rights_tier", "source_file_redistribution", "extracted_data_reuse",
        "extracted_data_release", "hold_reason", "is_open_access", "in_pmc",
        "regulator", "n_measurements", "resolved_by", "resolved_date"]


def main():
    src = list(csv.DictReader(open(os.path.join(ROOT, "data", "sources.csv"))))
    out, unmapped = [], set()
    for r in src:
        lic = (r["license"] or "").strip()
        if lic in TIERS:
            tier, filerd, release, basis = TIERS[lic]
            evidence = ("data/sources.csv license = %r, recorded from %s on %s"
                        % (lic, r["access"] or "NOT_REPORTED",
                           r["retrieved_date"] or "NOT_REPORTED"))
        elif "not established in this session" in lic:
            tier, filerd, release, basis = UNEXAMINED
            evidence = ("data/sources.csv license = %r -- an explicit record "
                        "that terms were not checked, not a record of absence"
                        % lic)
        else:
            unmapped.add(lic)
            tier, filerd, release, basis = ("U", "UNKNOWN", "DECISION_REQUIRED",
                                            "Licence string not in the mapping.")
            evidence = "data/sources.csv license = %r (unmapped)" % lic
        out.append(dict(
            source_ref=r["source_key"] or r["source_id"],
            citation_short=(r["citation"] or "")[:110],
            declared_licence=lic or "",
            licence_evidence=evidence,
            rights_tier=tier,
            source_file_redistribution=filerd,
            # The two axes stay separate (proposal §4): whether the SOURCE
            # DOCUMENT may be republished is a different question from whether
            # MEASURED VALUES may be released, and they have different answers.
            extracted_data_reuse=basis,
            extracted_data_release=release,
            hold_reason=("" if release == "RELEASE"
                         else "awaiting Oscar's ruling on the basis; see "
                              "CRANK_PROPOSAL_RIGHTS_TAGGING_2026-10-03.md"),
            is_open_access=("YES" if r["pmcid"] else "NOT_ESTABLISHED"),
            in_pmc=("YES" if r["pmcid"] else "NO"),
            regulator=("YES" if r["evidence_tier"] in
                       ("regulatory_primary", "registry_results",
                        "pharmacovigilance_api") else "NO"),
            n_measurements=r["n_measurements"],
            resolved_by="rocksteady-hydrocephalus (agent); NOT legal clearance",
            resolved_date="2026-10-03",
        ))

    if unmapped:
        raise SystemExit("licence strings with no mapping: %s" % sorted(unmapped))

    path = os.path.join(ROOT, "notes", "rights_register_source.csv")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)

    by_tier = collections.Counter(r["rights_tier"] for r in out)
    rows_by_tier = collections.Counter()
    for r in out:
        rows_by_tier[r["rights_tier"]] += int(r["n_measurements"] or 0)
    print("wrote %s" % path)
    print("%d sources" % len(out))
    for tier in "ABCDU":
        if by_tier[tier]:
            print("  tier %s  %3d sources  %5d measurement rows"
                  % (tier, by_tier[tier], rows_by_tier[tier]))
    print("  release proposal: %s"
          % dict(collections.Counter(r["extracted_data_release"] for r in out)))


if __name__ == "__main__":
    main()
