#!/usr/bin/env python3
"""Port the verified characterization recoveries into oligos.csv.

WHAT THIS PORTS, AND WHAT IT REFUSES TO
  Two verification agents read regulatory CMC sections, WHO INN documents, FDA
  labels and EPARs for the compounds carrying human clinical evidence. They
  produced three kinds of result, handled differently here:

  1. RECOVERIES with no contradiction -> written. A sequence, per-residue map or
     purity METHOD for a field that was TBD, where the agent's own
     `disagreement_with_dataset` says there is no conflict.
  2. CONTRADICTIONS of an existing value -> NEVER written. Logged to
     curation/scientist_v09/conflicts.csv for scientific adjudication. Several
     are backed by atom arithmetic from a published molecular formula and are
     almost certainly right, but overwriting a curated value on an agent's
     say-so is exactly the behaviour the governance rules forbid.
  3. A value this pipeline itself got wrong -> reverted to TBD. One case: the
     eplontersen map (see below).

PURITY: METHOD YES, VALUE NO
  The reviewer challenged the earlier claim that purity is "structurally
  unavailable", and the challenge is PARTLY UPHELD. Regulatory CMC sections do
  state the purity specification PARAMETER and the ANALYTICAL METHOD, and those
  are recovered here for 14 compounds. They do not state the numeric acceptance
  criterion: FDA withholds it under FOIA Exemption 4 as Confidential Commercial
  Information with citable page-count stamps (nusinersen NDA 209531, "136
  Page(s) has been Withheld in Full as b4"; defibrotide NDA 208114, 125 pages;
  pegaptanib NDA 21-756, 56 then 46 pages; imetelstat NDA 217779 releases 24 of
  156 and the withheld section is exactly "Characterization of Drug Substance
  and Impurities"), and the 1998 fomivirsen specification pages are physically
  removed from the scanned review. So `purity_pct` stays TBD for all 259
  compounds and `purity_method` becomes populated. That is a real, evidenced
  answer rather than either a guess or a shrug.

THE ONE REVERT
  `modification_map` for eplontersen (TOLG061) was composed BY THIS PIPELINE
  from the scientist package's position chemistry, which records 19
  phosphorothioate linkages for it -- byte-identical to inotersen, with which
  eplontersen shares a nucleobase sequence. Eplontersen is the GalNAc3
  LICA/LRx conjugate and carries a MIXED backbone; the row's own
  `backbone_chemistry` column already read `PS_PO_mix`, so the composed map
  contradicted its own record. It is reverted to TBD rather than replaced with
  the agent's proposed map, because the underlying scientist data is what needs
  correcting and that is German's call. QC gate 4c now rejects any map that
  disagrees with its backbone column.

Usage:  python3 scripts/port_characterization.py
"""
import csv, json, os, re

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
STUD = os.path.join(ENDPOINT, "curation", "studies")
SCI = os.path.join(ENDPOINT, "curation", "scientist_v09")

MAPTOK = re.compile(r"([emdlk])([ACGTU])(\(5m\))?([*-]?)")
NO_CONFLICT_PREFIXES = ("NO CONTRADICTION", "NO CHEMISTRY CONTRADICTION", "MINOR/COSMETIC")
TBD = ("", "TBD", "NA", "NOT_REPORTED")

# Reverts this pipeline owes: a value it wrote that contradicts its own record.
REVERT_MAP = {"TOLG061": "composed from scientist position chemistry that propagated inotersen's "
                         "all-PS backbone; contradicts this row's own backbone_chemistry=PS_PO_mix"}


def map_is_valid(mm, o):
    """A map is portable only if it parses as rocksteady_v1 AND agrees with the
    row's own backbone_chemistry and ps_count. Validating BEFORE writing is the
    point: without it the port wrote the agents' status strings
    ("NOT_APPLICABLE", "NOTATION EXTENSION REQUIRED - ...") into the map column,
    where the hyphens were then counted as phosphodiester linkages, and it wrote
    tofersen's 15-PS map onto a row still carrying ps_count=19 -- turning the
    agent's flagged disagreement into a silent contradiction.
    Returns (ok, reason)."""
    if not mm or mm.upper().startswith(("TBD", "NOT_APPLICABLE", "NOTATION", "NOT ", "N/A")):
        return False, "not a composed map (status string or TBD)"
    toks = MAPTOK.findall(mm)
    if not toks or sum(len("".join(t)) for t in toks) != len(mm):
        return False, f"does not fully parse under rocksteady_v1: {mm[:60]!r}"
    n_ps, n_po = mm.count("*"), mm.count("-")
    bb = (o.get("backbone_chemistry") or "").strip()
    if bb == "full_PS" and n_po:
        return False, f"backbone_chemistry=full_PS but map has {n_po} PO linkage(s)"
    if bb == "full_PO" and n_ps:
        return False, f"backbone_chemistry=full_PO but map has {n_ps} PS linkage(s)"
    if bb == "PS_PO_mix" and not (n_ps and n_po):
        return False, f"backbone_chemistry=PS_PO_mix but map has {n_ps} PS / {n_po} PO"
    pc = (o.get("ps_count") or "").strip()
    if pc.isdigit() and int(pc) != n_ps:
        return False, f"row ps_count={pc} but map has {n_ps} PS linkage(s)"
    sq = re.sub(r"[^ACGTU]", "", (o.get("sequence_5to3") or "").upper()).replace("U", "T")
    bases = "".join(t[1] for t in toks).replace("U", "T")
    if len(sq) >= 8 and sq != bases:
        return False, f"map bases {bases!r} != sequence_5to3 {sq!r}"
    return True, ""


def rd(p):
    with open(p, newline="", encoding="utf-8") as f: return list(csv.DictReader(f))


def main():
    oligos = rd(os.path.join(DATA, "oligos.csv"))
    byid = {o["oligo_id"]: o for o in oligos}
    conflicts = rd(os.path.join(SCI, "conflicts.csv"))
    ported = {"purity_method": 0, "modification_map": 0, "sequence_5to3": 0, "ps_count": 0}
    flagged, reverted, rejected = 0, 0, []

    # ---- reverts -----------------------------------------------------------
    for oid, why in REVERT_MAP.items():
        o = byid.get(oid)
        if o and o["modification_map"] not in TBD and o["modification_map_notation"] == "rocksteady_v1":
            conflicts.append({"kind": "modification_map_retracted", "scientist_record_id":
                              o.get("scientist_record_id", ""), "compound": o["oligo_name"],
                              "oligo_id": oid, "scientist_value": o["modification_map"],
                              "branch_value": "TBD (reverted)",
                              "resolution": f"RETRACTED BY PIPELINE — {why}. The scientist "
                                            f"package's position chemistry for this record needs "
                                            f"correction; not overwritten here."})
            o["modification_map"] = "TBD"
            o["modification_map_notation"] = ""
            o["characterization_source"] = ""
            reverted += 1

    # ---- ports and flags ---------------------------------------------------
    for fn, kind in (("characterization_regulatory_cmc.json", "cmc"),
                     ("characterization_sequence_identity.json", "seq")):
        path = os.path.join(STUD, fn)
        if not os.path.exists(path):
            print(f"  skip {fn}: not present"); continue
        for c in json.load(open(path)).get("compounds", []):
            oid = (c.get("oligo_id") or "").strip()
            o = byid.get(oid)
            if not o:
                continue
            dis = (c.get("disagreement_with_dataset") or "").strip()
            clean = dis.upper().startswith(NO_CONFLICT_PREFIXES) or not dis

            # purity METHOD is additive and never contradicts a TBD field
            pm = (c.get("purity_method") or "").strip()
            if pm and not pm.upper().startswith(("TBD", "NOT ")) and o["purity_method"] in TBD:
                o["purity_method"] = pm[:300]
                o["purity_pct"] = "TBD"   # never inferred; the numeric value is withheld
                ported["purity_method"] += 1

            if oid in REVERT_MAP:
                continue

            # A port only ever writes into a field that is TBD, so it cannot
            # overwrite a curated value and is safe even on a record that has a
            # disagreement elsewhere. Holding the whole record back because of
            # an unrelated dispute lost real recoveries: aprinocarsen's dispute
            # is about oligo_class, and it was blocking its sequence, ps_count
            # and per-residue map, all of which were TBD.
            mm = (c.get("modification_map") or "").strip()
            ok, why = map_is_valid(mm, o)
            if mm and not ok and o["modification_map"] in TBD and "status string" not in why:
                conflicts.append({"kind": "modification_map_rejected", "scientist_record_id":
                                  o.get("scientist_record_id", ""), "compound": o["oligo_name"],
                                  "oligo_id": oid, "scientist_value": mm[:160],
                                  "branch_value": f"bb={o['backbone_chemistry']} ps={o['ps_count']}",
                                  "resolution": f"NOT PORTED — {why}. Scientist adjudication "
                                                f"required; the proposed map and the row's own "
                                                f"columns cannot both be right."})
                rejected.append(oid)
            if ok and o["modification_map"] in TBD:
                o["modification_map"] = mm
                o["modification_map_notation"] = "rocksteady_v1"
                o["characterization_source"] = (c.get("sequence_source") or "")[:200] or kind
                ported["modification_map"] += 1
                # the base sequence is readable off a lossless map
                if o["sequence_5to3"] in TBD:
                    bases = "".join(t[1] for t in MAPTOK.findall(mm))
                    if len(bases) >= 8:
                        o["sequence_5to3"] = bases
                        ported["sequence_5to3"] += 1
                        if o["length_nt"] in TBD:
                            o["length_nt"] = str(len(bases))
                            ported["length_nt"] = ported.get("length_nt", 0) + 1
            pcm = re.match(r"\s*(\d{1,3})\b", str(c.get("ps_count_verified") or ""))
            if pcm and o["ps_count"] in TBD:
                o["ps_count"] = pcm.group(1)
                ported["ps_count"] += 1
            if dis and not clean:
                conflicts.append({"kind": "chemistry_disagreement", "scientist_record_id":
                                  o.get("scientist_record_id", ""), "compound": o["oligo_name"],
                                  "oligo_id": oid,
                                  "scientist_value": (c.get("modification_map") or "")[:160] or "see resolution",
                                  "branch_value": f"bb={o['backbone_chemistry']} ps={o['ps_count']} "
                                                  f"sugar={o['sugar_modifications'][:40]}",
                                  "resolution": "NOT OVERWRITTEN — scientist adjudication required. "
                                                + dis[:900]})
                flagged += 1

    with open(os.path.join(DATA, "oligos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(oligos[0].keys()))
        w.writeheader(); w.writerows(oligos)
    with open(os.path.join(SCI, "conflicts.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["kind", "scientist_record_id", "compound", "oligo_id",
                                          "scientist_value", "branch_value", "resolution"],
                           extrasaction="ignore")
        w.writeheader(); w.writerows(conflicts)

    npm = sum(1 for o in oligos if o["purity_method"] not in TBD)
    nmm = sum(1 for o in oligos if o["modification_map"] not in TBD)
    nsq = sum(1 for o in oligos if o["sequence_5to3"] not in TBD)
    print("ported:", {k: v for k, v in ported.items() if v})
    print(f"reverted (pipeline's own error): {reverted}")
    print(f"flagged for scientist adjudication, NOT overwritten: {flagged}")
    print(f"maps REJECTED as inconsistent with their own row: {len(rejected)} {rejected}")
    print(f"\npurity_method populated : {npm} / {len(oligos)}")
    print(f"purity_pct populated    : {sum(1 for o in oligos if o['purity_pct'] not in TBD)} / {len(oligos)}"
          f"   (numeric criterion withheld as Confidential Commercial Information)")
    print(f"modification_map        : {nmm} / {len(oligos)}")
    print(f"sequences               : {nsq} / {len(oligos)}")


if __name__ == "__main__":
    main()
