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
    """Nucleobase sequence with U collapsed to T, everything else dropped.

    THIS IS A LEAKAGE-GROUPING KEY, NOT AN IDENTITY KEY. Collapsing U to T makes
    an siRNA and an ASO of the same base sequence compare equal, and they are not
    the same construct. Beebop's 2026-10-02 review asked for the two to be
    separated and the thrombocytopenia request raised the same normalisation as a
    question; both are right. Use it only to keep related molecules in the same
    train/test fold - never to assert that two records are the same compound.
    """
    return re.sub(r"[^ACGT]", "", (s or "").upper().replace("U", "T"))


# The chemistry that distinguishes two molecules sharing a base sequence. Phase 2
# asks for "the location of all chemical modifications in each oligo", and the
# announcement's own framing is that sequence alone is insufficient: sugar, base
# and linkage position, strand identity, conjugates and formulation can separate
# constructs that read identically as text.
CHEM_FIELDS = ("backbone_chemistry", "sugar_modifications", "gapmer_design",
               "conjugate", "ps_count", "length_nt", "oligo_class")


def chem_key(o):
    """Exact-construct key: base sequence AND the recorded chemistry.

    Returns None where the sequence or any chemistry field is unknown, because an
    exact-identity claim cannot rest on blanks. A record that cannot be keyed is
    reported as unkeyable rather than silently matched or silently dropped.
    """
    seq = canon(o.get("sequence_5to3"))
    if len(seq) < 12:
        return None
    vals = []
    for f in CHEM_FIELDS:
        v = (o.get(f) or "").strip()
        if v in ("", "TBD", "NA"):
            return None
        vals.append(v.lower())
    # RNA/DNA is not collapsed here: the un-normalised text is part of the key.
    raw = re.sub(r"[^A-Z]", "", (o.get("sequence_5to3") or "").upper())
    return (raw, tuple(vals))


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

    # --- exact construct identity, chemistry included ---------------------
    print("\npairs by EXACT CONSTRUCT (same base sequence AND same recorded "
          "chemistry)")
    by_chem = defaultdict(set)
    unkeyable = set()
    for oid in set().union(*members.values()):
        k = chem_key(oligos.get(oid, {}))
        if k is None:
            unkeyable.add(oid)
        else:
            by_chem[k].add(oid)
    exact = 0
    for k, ids in by_chem.items():
        if len(ids) < 2:
            continue
        bands_hit = {b for b in order for i in ids if i in members[b]}
        if len(bands_hit) > 1:
            exact += 1
            print("  %s... %s across %s" % (k[0][:22], sorted(ids), sorted(bands_hit)))
    if not exact:
        print("  none. No two records with FULL chemistry recorded and an "
              "identical construct sit in different system bands.")
    print("  records that cannot be keyed exactly (sequence or chemistry "
          "incomplete): %d of %d" % (len(unkeyable), len(set().union(*members.values()))))
    print("  -> an exact-identity claim is impossible for those, and this is the "
          "characterization gap, not a matching failure.")

    print("\nLEAKAGE GROUPS by base sequence (U collapsed to T) — NOT identity "
          "claims")
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
    print("  These groups exist to keep related molecules in one train/test fold. "
          "They do NOT\n  establish that the grouped constructs are "
          "experimentally interchangeable.")

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
