#!/usr/bin/env python3
"""Divide every curated corpus into one self-contained dataset per toxicity.

The rule this encodes, and the reason the two halves behave differently:

  MEASUREMENTS DIVIDE.  A measurement is an observation of one toxicity, so the
  rows partition — disjoint and exhaustive. Nothing is double-counted, and the
  per-endpoint row counts sum to the corpus total. The script fails loudly if
  they ever stop summing.

  OLIGOS DUPLICATE.  An oligonucleotide is a compound identity, not an
  observation. Tofersen was studied for kidney toxicity AND for CNS toxicity, so
  it belongs in both endpoint tables. Each endpoint's oligo table is filtered to
  the molecules its own measurements reference, and a molecule appearing in two
  tables is correct rather than a duplication bug.

  Consequence, stated because it is the easy mistake: oligo counts are NOT
  additive across endpoints. Row counts are. `molecule_crosswalk` records every
  molecule that appears under more than one toxicity so the overlap is explicit
  instead of implied.

Everything is written under `toxicity/`, named for the toxicity it belongs to.

Usage:  python toxicity/scripts/split_by_endpoint.py [--check]
        --check  verify the existing split matches the corpora, write nothing
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
ROOT = os.path.dirname(TOXDIR)


def path(*p):
    return os.path.join(ROOT, *p)


# Each corpus names its measurement/oligo tables and how its rows route to
# endpoints. A corpus serving one endpoint routes everything to it; the CNS
# corpus serves two and routes on a column it already carries, so the split is
# READ OFF THE DATA rather than inferred from anything external.
CORPORA = [
    {
        "name": "kidney",
        "oligos": path("data", "oligos.csv"),
        "measurements": path("data", "measurements.csv"),
        "route": lambda r: "kidney-nephrotoxicity",
    },
    {
        "name": "cns",
        "oligos": path("toxicity", "notes", "cns", "corpus", "cns_oligos.csv"),
        "measurements": path("toxicity", "notes", "cns", "corpus", "cns_measurements.csv"),
        "route": lambda r: ("hydrocephalus"
                            if r.get("challenge_priority") == "high_hydrocephalus"
                            else "chronic-neurotoxicity"),
    },
]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


# Cross-endpoint molecule matching reuses the assembler's identity whitelist. It
# must: a first cut here keyed on any alias token longer than three characters
# claimed that O'Rourke's "ASO1", Kuroda's "ASO1" and a Mapt gapmer called "ASO1"
# were one molecule. Those are PAPER-LOCAL labels, not identifiers, and a
# crosswalk asserting a false equivalence is worse than no crosswalk — it would
# tell a modeller to pool three unrelated compounds. Only tokens that pin a
# molecule down globally are allowed: sponsor development codes, INN stems and
# brand names.
sys.path.insert(0, HERE)
from assemble_cns import (SPONSOR_CODE, INN_STEM, BRANDS,  # noqa: E402
                          PAPER_LOCAL, key_token)


def molecule_keys(o):
    """Globally-identifying tokens for this oligo (name + aliases)."""
    keys = set()
    raw = [o.get("oligo_name", "")]
    raw += re.split(r"[;,|]", o.get("aliases", "") or "")
    for r in raw:
        t = key_token(r)
        if not t or PAPER_LOCAL.match(t):
            continue
        if SPONSOR_CODE.match(t) or INN_STEM.match(t) or t in BRANDS:
            keys.add(t)
    return keys


def canon_seq(s):
    s = (s or "").strip()
    if not s or s == "TBD":
        return ""
    return re.sub(r"[^ACGT]", "", s.upper().replace("U", "T"))


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows


def write(p, fieldnames, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def main():
    check = "--check" in sys.argv
    per_endpoint = {}          # endpoint -> {"meas": [...], "oligos": [...], "cols": (...)}
    all_oligos = {}            # (corpus, oligo_id) -> row
    endpoints_of = defaultdict(set)   # (corpus, oligo_id) -> {endpoint}

    for c in CORPORA:
        oligos = read(c["oligos"])
        meas = read(c["measurements"])
        by_id = {o["oligo_id"]: o for o in oligos}

        orphans = sorted({m["oligo_id"] for m in meas} - set(by_id))
        if orphans:
            raise SystemExit("ERROR [%s]: %d measurement(s) reference unknown "
                             "oligo_id: %s" % (c["name"], len(orphans), orphans[:5]))

        routed = 0
        for m in meas:
            ep = c["route"](m)
            slot = per_endpoint.setdefault(ep, {
                "meas": [], "oligo_ids": [], "meas_cols": list(meas[0].keys()),
                "oligo_cols": list(oligos[0].keys()), "corpus": c["name"]})
            if slot["meas_cols"] != list(meas[0].keys()):
                raise SystemExit("ERROR: endpoint %r fed by two corpora with "
                                 "different measurement columns" % ep)
            slot["meas"].append(m)
            slot["oligo_ids"].append(m["oligo_id"])
            endpoints_of[(c["name"], m["oligo_id"])].add(ep)
            routed += 1

        if routed != len(meas):
            raise SystemExit("ERROR [%s]: partition not exhaustive: %d != %d"
                             % (c["name"], routed, len(meas)))
        for oid, o in by_id.items():
            all_oligos[(c["name"], oid)] = o

    # ---- write one self-contained dataset per toxicity -------------------
    summary = []
    for ep in sorted(per_endpoint):
        slot = per_endpoint[ep]
        corpus = slot["corpus"]
        seen, used = set(), []
        for oid in slot["oligo_ids"]:          # preserve first-appearance order
            if oid not in seen:
                seen.add(oid)
                used.append(all_oligos[(corpus, oid)])
        mp = path("toxicity", "%s.measurements.csv" % ep)
        op = path("toxicity", "%s.oligos.csv" % ep)
        if check:
            got_m = len(read(mp)) if os.path.exists(mp) else -1
            got_o = len(read(op)) if os.path.exists(op) else -1
            ok = (got_m == len(slot["meas"]) and got_o == len(used))
            print("%-24s %5d meas %4d oligos  on-disk %5d/%4d  %s"
                  % (ep, len(slot["meas"]), len(used), got_m, got_o,
                     "OK" if ok else "*** STALE ***"))
            if not ok:
                summary.append(ep)
        else:
            write(mp, slot["meas_cols"], slot["meas"])
            write(op, slot["oligo_cols"], used)
            print("%-24s %5d measurements  %4d oligos" % (ep, len(slot["meas"]), len(used)))
        summary.append(None)

    if check and any(summary):
        raise SystemExit("\nERROR: split on disk is stale — re-run without --check")

    # ---- disjoint + exhaustive, asserted not assumed ---------------------
    ids = [m["measurement_id"] for s in per_endpoint.values() for m in s["meas"]]
    if len(ids) != len(set(ids)):
        raise SystemExit("ERROR: a measurement_id appears in more than one endpoint")
    corpus_total = sum(len(read(c["measurements"])) for c in CORPORA)
    if len(ids) != corpus_total:
        raise SystemExit("ERROR: %d split rows != %d corpus rows" % (len(ids), corpus_total))
    print("%-24s %5d measurements across %d endpoints — disjoint, exhaustive"
          % ("TOTAL", len(ids), len(per_endpoint)))

    # ---- the duplication ledger ------------------------------------------
    # Which molecules appear under more than one toxicity, and do the two records
    # agree where both carry a sequence? A disagreement would mean one of them is
    # the wrong molecule, which is the failure this ledger exists to surface.
    by_key = defaultdict(list)
    for (corpus, oid), eps in endpoints_of.items():
        o = all_oligos[(corpus, oid)]
        for k in molecule_keys(o):
            by_key[k].append((corpus, oid, o, frozenset(eps)))

    cross, seen_pairs = [], set()

    # Case 1 — the SAME record replicated into two endpoint tables. This is the
    # within-corpus duplication: one oligo studied for two toxicities keeps one
    # id and appears in both tables. It is the commonest form of "duplicate where
    # needed" and would be invisible if the ledger only compared distinct records.
    for (corpus, oid), eps in sorted(endpoints_of.items()):
        if len(eps) < 2:
            continue
        o = all_oligos[(corpus, oid)]
        for a, b in [(x, y) for i, x in enumerate(sorted(eps))
                     for y in sorted(eps)[i + 1:]]:
            cross.append({
                "molecule": o.get("oligo_name"),
                "relation": "replicated_same_id",
                "endpoint_a": a, "corpus_a": corpus, "oligo_id_a": oid,
                "endpoint_b": b, "corpus_b": corpus, "oligo_id_b": oid,
                "sequence_check": "same_record",
            })

    # Case 2 — the same MOLECULE curated independently under two toxicities, so it
    # carries a different id in each (inotersen is OLG001 in kidney and CNS277 in
    # CNS). Nothing links these without the crosswalk, and a model keyed on id
    # would treat one compound as two.
    for k, entries in by_key.items():
        eps = {e for _, _, _, es in entries for e in es}
        if len(eps) < 2:
            continue
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                (c1, id1, o1, e1), (c2, id2, o2, e2) = entries[i], entries[j]
                if e1 == e2:
                    continue
                pair = tuple(sorted([(c1, id1), (c2, id2)]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                s1, s2 = canon_seq(o1.get("sequence_5to3")), canon_seq(o2.get("sequence_5to3"))
                agree = ("sequences_agree" if s1 and s2 and s1 == s2 else
                         "SEQUENCE_CONFLICT" if s1 and s2 else
                         "one_side_TBD" if s1 or s2 else "both_TBD")
                cross.append({
                    "molecule": o1.get("oligo_name"),
                    "relation": "same_molecule_different_id",
                    "endpoint_a": "|".join(sorted(e1)), "corpus_a": c1, "oligo_id_a": id1,
                    "endpoint_b": "|".join(sorted(e2)), "corpus_b": c2, "oligo_id_b": id2,
                    "sequence_check": agree,
                })

    cross.sort(key=lambda r: ((r["molecule"] or "").lower(), r["relation"]))
    conflicts = [c for c in cross if c["sequence_check"] == "SEQUENCE_CONFLICT"]
    if not check:
        cw = path("toxicity", "molecule_crosswalk.csv")
        write(cw, list(cross[0].keys()) if cross else
              ["molecule", "relation", "endpoint_a", "corpus_a", "oligo_id_a",
               "endpoint_b", "corpus_b", "oligo_id_b", "sequence_check"], cross)
        print("\nmolecule crosswalk      %5d molecule(s) appear under more than one "
              "toxicity -> toxicity/molecule_crosswalk.csv" % len(cross))
    same_id = sum(1 for c in cross if c["relation"] == "replicated_same_id")
    diff_id = sum(1 for c in cross if c["relation"] == "same_molecule_different_id")
    print("  %d replicated under one id | %d same molecule under two ids"
          % (same_id, diff_id))
    # Per-toxicity copy of the ledger. Cross-cutting artifacts are duplicated into
    # every toxicity that uses them rather than shared from a common folder, so each
    # toxicity answers "which of MY molecules also appear elsewhere?" from its own
    # files, without reading another endpoint's.
    if not check:
        for ep in sorted(per_endpoint):
            rows = []
            for c in cross:
                if c["endpoint_a"] == ep:
                    other_ep, here_id, there_id = c["endpoint_b"], c["oligo_id_a"], c["oligo_id_b"]
                elif c["endpoint_b"] == ep:
                    other_ep, here_id, there_id = c["endpoint_a"], c["oligo_id_b"], c["oligo_id_a"]
                else:
                    continue
                rows.append({
                    "molecule": c["molecule"],
                    "relation": c["relation"],
                    "oligo_id_here": here_id,
                    "also_under": other_ep,
                    "oligo_id_there": there_id,
                    "sequence_check": c["sequence_check"],
                })
            rows.sort(key=lambda r: ((r["molecule"] or "").lower(), r["also_under"]))
            write(path("toxicity", "%s.shared-molecules.csv" % ep),
                  ["molecule", "relation", "oligo_id_here", "also_under",
                   "oligo_id_there", "sequence_check"], rows)
            print("  %-24s %3d of its molecules also appear under another toxicity"
                  % (ep, len(rows)))

    agree = sum(1 for c in cross if c["sequence_check"] == "sequences_agree")
    print("  sequences agree %d | one side TBD %d | both TBD %d | CONFLICTS %d"
          % (agree,
             sum(1 for c in cross if c["sequence_check"] == "one_side_TBD"),
             sum(1 for c in cross if c["sequence_check"] == "both_TBD"),
             len(conflicts)))
    for c in conflicts:
        print("  *** %s: %s (%s) vs %s (%s)" % (c["molecule"], c["oligo_id_a"],
                                                c["endpoint_a"], c["oligo_id_b"],
                                                c["endpoint_b"]))
    if conflicts:
        raise SystemExit("ERROR: a molecule carries different sequences under two "
                         "toxicities — one of them is the wrong molecule")


if __name__ == "__main__":
    main()
