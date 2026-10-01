#!/usr/bin/env python3
"""Which molecules are actually studied in more than one kind of system.

The challenge asks for data that can "bridge the differences between predictions
that are primarily based on data from animal-based studies to data collected by in
vitro human-based systems". A dataset can only support that claim for a molecule
measured in BOTH kinds of system, so the claim has to be computed, not asserted.

It is computed two ways, because an oligo_id is a curation artefact: by identity
(the same oligo_id carries rows of both kinds) and by sequence (two records under
different ids whose canonical nucleobase sequence is identical). Sequence matching
needs >=12 nt to mean anything, and a record with no published sequence can only
ever match by identity - which is itself a finding, since most of this corpus's
human-laboratory compounds have no published sequence.

Usage:  python toxicity/scripts/cross_system_pairs_cns.py
"""
import csv
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
ENDPOINTS = ["chronic-neurotoxicity", "hydrocephalus"]

BANDS = {
    "human_laboratory": "human laboratory (in vitro / ex vivo)",
    "animal_invivo": "animal in vivo",
    "animal_laboratory": "animal laboratory (in vitro)",
    "human_clinical": "human clinical (trial, label, case, cohort)",
}


def canon(s):
    """Nucleobase sequence, RNA and DNA comparable, everything else dropped."""
    return re.sub(r"[^ACGT]", "", (s or "").upper().replace("U", "T"))


def band(cls):
    if cls in ("human_laboratory", "animal_invivo", "animal_laboratory"):
        return cls
    return "human_clinical" if cls.startswith("human_") else None


def main():
    rows, oligos = [], {}
    for ep in ENDPOINTS:
        rows += list(csv.DictReader(
            open(os.path.join(TOXDIR, "%s.measurements.csv" % ep),
                 newline="", encoding="utf-8")))
        for o in csv.DictReader(open(os.path.join(TOXDIR, "%s.oligos.csv" % ep),
                                     newline="", encoding="utf-8")):
            oligos.setdefault(o["oligo_id"], o)

    members = defaultdict(set)          # band -> {oligo_id}
    for r in rows:
        b = band(r["evidence_class"])
        if b:
            members[b].add(r["oligo_id"])

    print("molecules per system band (not additive — a molecule can be in several)")
    for b, label in BANDS.items():
        ids = members[b]
        seq = sum(1 for o in ids if len(canon(oligos.get(o, {}).get("sequence_5to3"))) >= 12)
        print("  %-44s %4d molecules, %4d with a published sequence"
              % (label, len(ids), seq))

    print("\npairs by IDENTITY (one oligo_id carries rows of both kinds)")
    order = ["human_laboratory", "animal_invivo", "animal_laboratory", "human_clinical"]
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            shared = sorted(members[a] & members[b])
            print("  %-26s x %-26s %3d  %s"
                  % (a, b, len(shared),
                     ", ".join("%s %s" % (s, oligos.get(s, {}).get("oligo_name", ""))
                               for s in shared[:4])))

    print("\npairs by SEQUENCE (different ids, identical nucleobase sequence)")
    by_seq = defaultdict(set)
    for oid in set().union(*members.values()):
        s = canon(oligos.get(oid, {}).get("sequence_5to3"))
        if len(s) >= 12:
            by_seq[s].add(oid)
    found = 0
    for s, ids in by_seq.items():
        if len(ids) < 2:
            continue
        bands_hit = {b for b in order for i in ids if i in members[b]}
        if len(bands_hit) > 1:
            found += 1
            print("  %s... %s across %s" % (s[:24], sorted(ids), sorted(bands_hit)))
    if not found:
        print("  none. Every sequence-identical record pair sits inside one band.")

    # The bridge the dataset can actually claim: molecules with evidence in two
    # bands counted by identity OR sequence, since the same molecule curated twice
    # carries two ids. This is the number that may be quoted; the matched panel
    # below is not it.
    print("\nmolecules bridging two bands, identity and sequence combined")
    groups = []
    for s, ids in by_seq.items():
        if len(ids) > 1:
            groups.append(set(ids))
    def bands_of(oid):
        return {b for b in order if oid in members[b]}
    def bridge(a, b):
        hit = {o for o in members[a] & members[b]}
        for g in groups:
            if any(a in bands_of(o) for o in g) and any(b in bands_of(o) for o in g):
                hit |= g
        return sorted(o for o in hit if bands_of(o) & {a, b})
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            br = bridge(a, b)
            if br:
                print("  %-26s x %-26s %3d molecule-record(s)" % (a, b, len(br)))

    # The pairing the documentation used to call a human bridge. Stated here with
    # the species of BOTH arms so it cannot be misread again.
    print("\nthe large matched panel, by species of each arm")
    panel = [r for r in rows if "2021.0071" in r["source_ref"]]
    pairs = defaultdict(set)
    for r in panel:
        pairs[(r["evidence_class"], r["species"], r["readout_category"])].add(r["oligo_id"])
    for k, v in sorted(pairs.items()):
        print("  %-18s %-7s %-18s %4d rows, %4d molecules"
              % (k[0], k[1], k[2], sum(1 for r in panel
                                       if (r["evidence_class"], r["species"],
                                           r["readout_category"]) == k), len(v)))
    both = set.intersection(*pairs.values()) if len(pairs) > 1 else set()
    print("  molecules present in BOTH arms of that panel: %d" % len(both))
    print("  species of the two arms: %s" % sorted({k[1] for k in pairs}))


if __name__ == "__main__":
    main()
