#!/usr/bin/env python3
"""One row per human trial, built from the measurement rows that cite it.

A measurement is not a trial. GENERATION HD1 reaches this corpus as a registry
posting, two publications and a sponsor slide deck, and it contributes 32 rows
because it reported several terms across several arms. Counting rows, or counting
source documents, would say "32 trials" or "4 trials" where the answer is one.

What this script does is collapse rows onto `trial_key` and report the four
quantities that are genuinely different from each other:

    verified trials        a registry identifier the SOURCE supplies
    pending candidates     trial reports whose registry entry no source here names
    endpoint-evaluable     the subset contributing a usable graded outcome
    unique compounds       molecules, which are fewer than trials and not additive

No identifier is invented. A trial whose registry entry is not named in any row
that cites it stays in the pending register, which is excluded from the verified
total. That is the honest state of the evidence, not a gap to be filled from
recall: linking a publication to a registry number from memory would be a
fabricated trial identifier, which is the one thing this dataset must not contain.

Outputs, per endpoint, beside that endpoint's other files:
    <endpoint>.trials.csv          verified trials, one row each
    <endpoint>.trials-pending.csv  trial reports with no source-named registry entry

Usage:  python toxicity/scripts/build_trial_register_cns.py [--check]
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)

ENDPOINTS = ["chronic-neurotoxicity", "hydrocephalus"]
TRIAL_TIER = {"human_trial_registry", "human_trial_publication", "human_trial_sponsor"}

# A trial is endpoint-evaluable when at least one of its rows carries an outcome a
# model could use: a value that is not a placeholder, and a grade. A registry
# record that exists but posted nothing usable is identified, not evaluable - the
# distinction Beebop's proposal turns on, and the reason coverage cannot be
# claimed from a registry listing alone.
PLACEHOLDER = {"", "TBD", "NA"}

# Said by the source itself, not inferred: a roll-over or extension protocol
# re-enrols participants from its parent study, so its participants overlap and
# its events are not independent of the parent's.
EXTENSION = re.compile(r"roll[- ]?over|open[- ]label extension|\bOLE\b|extension study"
                       r"|extension protocol|long[- ]term extension|\bLTE\b", re.I)

COLS = ["trial_key", "registry_id", "identity_basis", "compounds", "oligo_ids",
        "indication", "delivery_routes", "measurement_rows", "arms_represented",
        "evidence_classes", "source_ids", "endpoint_evaluable", "evaluable_basis",
        "exposure_as_reported", "participant_overlap", "also_in_endpoint"]


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(p, cols, rows):
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def arm_of(row):
    """The arm or cohort a row reports, as the source names it.

    Used only to count how many arms a trial contributes, so that a five-arm
    dose-ranging study is not mistaken for five studies.
    """
    t = (row.get("source_table") or "").strip()
    m = re.search(r"arm=([^|]+)$", t)
    if m:
        return m.group(1).strip()
    m = re.search(r"(?:arm|group|cohort)\s*'([^']+)'", t)
    if m:
        return m.group(1).strip()
    m = re.search(r",\s*([^,]{3,60}?\barm)\s*$", t)
    if m:
        return m.group(1).strip()
    return t[-40:] or "unspecified"


def uniq(vals):
    out = []
    for v in vals:
        v = (v or "").strip()
        if v and v not in out:
            out.append(v)
    return out


def build(endpoint, oligos_by_id, trials_elsewhere):
    rows = read(os.path.join(TOXDIR, "%s.measurements.csv" % endpoint))
    tier = [r for r in rows if r["evidence_class"] in TRIAL_TIER]
    groups = defaultdict(list)
    for r in tier:
        groups[r["trial_key"]].append(r)

    verified, pending = [], []
    for key, rs in sorted(groups.items()):
        bases = uniq(r["trial_key_basis"] for r in rs)
        # registry_posting outranks named_in_source where both occur for one trial:
        # the posted record is the stronger identity.
        basis = ("registry_posting" if "registry_posting" in bases
                 else "named_in_source" if "named_in_source" in bases
                 else "publication_only")
        usable = [r for r in rs
                  if r["readout_value"] not in PLACEHOLDER
                  and r["neurotox_grade"] in {"0", "1", "2", "3"}]
        oids = uniq(r["oligo_id"] for r in rs)
        texts = " ".join(r["notes"] + " " + r["exposure_duration"] + " "
                         + r["system_model"] for r in rs)
        ext = EXTENSION.search(texts)
        rec = {
            "trial_key": key,
            "registry_id": key if key.startswith("NCT") else "",
            "identity_basis": basis,
            "compounds": "; ".join(uniq(oligos_by_id.get(o, {}).get("oligo_name", o)
                                        for o in oids)),
            "oligo_ids": "; ".join(oids),
            "indication": "; ".join(uniq(oligos_by_id.get(o, {}).get("indication", "")
                                         for o in oids))[:160],
            "delivery_routes": "; ".join(uniq(r["delivery_method"] for r in rs)),
            "measurement_rows": len(rs),
            "arms_represented": len({arm_of(r) for r in rs}),
            "evidence_classes": "; ".join(sorted({r["evidence_class"] for r in rs})),
            "source_ids": "; ".join(uniq(r["source_id"] for r in rs)),
            "endpoint_evaluable": "TRUE" if usable else "FALSE",
            "evaluable_basis": ("%d of %d rows carry a value and a grade"
                                % (len(usable), len(rs))) if usable
                               else "identified only: no row carries both a value "
                                    "and a grade",
            "exposure_as_reported": "; ".join(uniq(r["exposure_duration"] for r in rs))[:200],
            "participant_overlap": ("source describes an extension/roll-over "
                                    "protocol: %s" % ext.group(0)) if ext else "",
            "also_in_endpoint": "; ".join(sorted(trials_elsewhere.get(key, set()))),
        }
        (verified if basis != "publication_only" else pending).append(rec)
    return verified, pending, tier


def main():
    check = "--check" in sys.argv
    oligos_by_id = {}
    for ep in ENDPOINTS:
        for o in read(os.path.join(TOXDIR, "%s.oligos.csv" % ep)):
            oligos_by_id.setdefault(o["oligo_id"], o)

    # Which trial keys appear under more than one endpoint. The measurement rows
    # partition, so no row is counted twice, but a trial can legitimately supply
    # a hydrocephalus row and a neuroinflammation row. A consolidated submission
    # that adds the two registers together would then double-count the TRIAL, and
    # this column is what stops it.
    where = defaultdict(set)
    for ep in ENDPOINTS:
        for r in read(os.path.join(TOXDIR, "%s.measurements.csv" % ep)):
            if r["evidence_class"] in TRIAL_TIER and r["trial_key"]:
                where[r["trial_key"]].add(ep)
    elsewhere = {k: v for k, v in where.items() if len(v) > 1}

    all_verified = set()
    for ep in ENDPOINTS:
        others = {k: (v - {ep}) for k, v in elsewhere.items()}
        verified, pending, tier = build(ep, oligos_by_id, others)
        vp = os.path.join(TOXDIR, "%s.trials.csv" % ep)
        pp = os.path.join(TOXDIR, "%s.trials-pending.csv" % ep)
        evaluable = [r for r in verified if r["endpoint_evaluable"] == "TRUE"]
        compounds = {o for r in verified for o in r["oligo_ids"].split("; ") if o}
        all_verified |= {r["trial_key"] for r in verified}
        print("%s" % ep)
        print("   verified unique human trials          %4d" % len(verified))
        print("     of which endpoint-evaluable         %4d" % len(evaluable))
        print("     flagged as extension/roll-over      %4d"
              % sum(1 for r in verified if r["participant_overlap"]))
        print("     also appearing under another endpoint %2d"
              % sum(1 for r in verified if r["also_in_endpoint"]))
        print("   pending candidates (no registry id)   %4d" % len(pending))
        print("   human trial-derived measurement rows  %4d" % len(tier))
        print("   unique compounds in verified trials   %4d" % len(compounds))
        if check:
            for p, want in ((vp, verified), (pp, pending)):
                got = len(read(p)) if os.path.exists(p) else -1
                if got != len(want):
                    raise SystemExit("ERROR: %s holds %d rows, expected %d"
                                     % (os.path.basename(p), got, len(want)))
            print("   --check: registers on disk match\n")
        else:
            write(vp, COLS, verified)
            write(pp, COLS, pending)
            print("   wrote %s + %s\n" % (os.path.basename(vp), os.path.basename(pp)))

    both = sorted(k for k in all_verified if k in elsewhere)
    print("CNS-wide: %d distinct verified trials across both endpoints — NOT the sum "
          "of the two registers, because %d verified trial(s) appear in both:"
          % (len(all_verified), len(both)))
    print("   %s" % ", ".join(both))


if __name__ == "__main__":
    main()
