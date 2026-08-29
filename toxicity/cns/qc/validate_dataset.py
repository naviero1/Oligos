#!/usr/bin/env python3
"""Structural and integrity checks on the released OligoTox-CNS dataset.

    python3 qc/validate_dataset.py            # human-readable report
    python3 qc/validate_dataset.py --json     # machine-readable, for the docs generator

Exit code 0 = every check passes. Non-zero = at least one FAIL.

The point of this file is that no claim made in the narrative or methodology PDFs about the
dataset's integrity is asserted by hand: each is a named check here that either passes or does not.
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

MISSING_TOKENS = {"NOT_REPORTED", "NOT_APPLICABLE", "NOT_RECOVERABLE", ""}

VOCAB = {
    "study_type": {"in_vitro", "animal_invivo", "clinical", "ex_vivo"},
    "is_human_system": {"TRUE", "FALSE"},
    "is_cns_specific": {"TRUE"},
    "grade_status": {"provisional", "expert_confirmed", "not_graded"},
    "effect_direction": {"increase", "decrease", "no_change"},
    "redistribution": {"cc_by", "cc_by_nc", "public_domain", "summary_stat_only"},
    "readout_is_qualitative": {"TRUE", "FALSE", ""},
}

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))


def load(name: str) -> list[dict]:
    with (DATA / f"{name}.csv").open() as fh:
        return list(csv.DictReader(fh))


def main(as_json: bool = False) -> int:
    oligos = load("oligos")
    meas = load("measurements")
    mods = load("modifications")
    srcs = load("sources")

    oids = [o["oligo_id"] for o in oligos]
    oid_set = set(oids)
    src_ids = {s["source_id"] for s in srcs}

    # ---- keys ---------------------------------------------------------------------------
    check("oligo_id is unique", len(oids) == len(oid_set),
          f"{len(oids)} rows, {len(oid_set)} distinct")
    mids = [m["measurement_id"] for m in meas]
    check("measurement_id is unique", len(mids) == len(set(mids)),
          f"{len(mids)} rows, {len(set(mids))} distinct")

    # ---- referential integrity ----------------------------------------------------------
    orphan_m = [m["measurement_id"] for m in meas if m["oligo_id"] not in oid_set]
    check("every measurement points to a real oligo", not orphan_m, f"{len(orphan_m)} orphans")
    orphan_mod = {m["oligo_id"] for m in mods if m["oligo_id"] not in oid_set}
    check("every modification row points to a real oligo", not orphan_mod,
          f"{len(orphan_mod)} orphan oligo_ids")
    bad_src = ({o["source_id"] for o in oligos} | {m["source_id"] for m in meas}) - src_ids
    check("every source_id is registered in sources.csv", not bad_src, f"unknown: {sorted(bad_src)}")
    unmeasured = oid_set - {m["oligo_id"] for m in meas}
    check("every oligo has at least one measurement", not unmeasured,
          f"{len(unmeasured)} oligos with no measurement")

    # ---- controlled vocabulary ----------------------------------------------------------
    for col, allowed in VOCAB.items():
        bad = collections.Counter(m[col] for m in meas if col in meas[0] and m[col] not in allowed)
        check(f"controlled vocabulary: measurements.{col}", not bad, f"unexpected: {dict(bad)}")

    grades = [m["cns_tox_grade"] for m in meas if m["cns_tox_grade"] != ""]
    bad_g = [g for g in grades if g not in {"0", "1", "2", "3"}]
    check("cns_tox_grade is within 0-3", not bad_g, f"{len(bad_g)} out of range")

    # ---- grading discipline -------------------------------------------------------------
    ungraded_basis = [m["measurement_id"] for m in meas
                      if m["cns_tox_grade"] != "" and not m["grade_basis"].strip()]
    check("every grade states the rule that produced it", not ungraded_basis,
          f"{len(ungraded_basis)} graded rows with empty grade_basis")
    unstated = [m["measurement_id"] for m in meas if m["grade_status"] == ""]
    check("every measurement declares a grade_status", not unstated, f"{len(unstated)} blank")

    # ---- provenance: no number without a source cell ------------------------------------
    numeric = re.compile(r"^-?\d+(\.\d+)?$")
    no_loc = [m["measurement_id"] for m in meas
              if numeric.match(m["readout_value"] or "") and not m["source_location"].strip()]
    check("every numeric readout names its source table/figure", not no_loc,
          f"{len(no_loc)} numeric readouts with no source_location")
    no_ref = [m["measurement_id"] for m in meas if not m["source_ref"].strip()]
    check("every measurement carries a citation key", not no_ref, f"{len(no_ref)} blank")
    o_no_loc = [o["oligo_id"] for o in oligos if not o["source_location"].strip()]
    check("every oligo names its source table", not o_no_loc, f"{len(o_no_loc)} blank")

    # ---- sequence self-consistency ------------------------------------------------------
    seq_len_bad, base_bad = [], []
    for o in oligos:
        seq = o["sequence_base"]
        if seq in MISSING_TOKENS:
            continue
        if o["length_nt"] not in MISSING_TOKENS and int(o["length_nt"]) != len(seq):
            seq_len_bad.append(o["oligo_id"])
        for base, col in (("A", "n_A"), ("C", "n_C"), ("G", "n_G"), ("T", "n_T")):
            if o[col] not in MISSING_TOKENS and int(o[col]) != seq.count(base):
                base_bad.append((o["oligo_id"], col))
    check("length_nt equals the actual sequence length", not seq_len_bad,
          f"{len(seq_len_bad)} mismatches")
    check("base counts equal the actual sequence composition", not base_bad,
          f"{len(base_bad)} mismatches")

    alphabet = {c for o in oligos if o["sequence_base"] not in MISSING_TOKENS
                for c in o["sequence_base"]}
    check("sequence_base uses only A/C/G/T", alphabet <= set("ACGT"),
          f"alphabet: {sorted(alphabet)}")

    # ---- modification table consistency -------------------------------------------------
    by_oligo = collections.defaultdict(list)
    for m in mods:
        by_oligo[m["oligo_id"]].append(int(m["position_5to3"]))
    pos_bad, count_bad, base_mismatch = [], [], []
    seq_of = {o["oligo_id"]: o["sequence_base"] for o in oligos}
    len_of = {o["oligo_id"]: o["length_nt"] for o in oligos}
    for oid, positions in by_oligo.items():
        if sorted(positions) != list(range(1, len(positions) + 1)):
            pos_bad.append(oid)
        if len_of.get(oid) not in MISSING_TOKENS and int(len_of[oid]) != len(positions):
            count_bad.append(oid)
    for m in mods:
        seq = seq_of.get(m["oligo_id"], "")
        i = int(m["position_5to3"])
        if seq not in MISSING_TOKENS and i <= len(seq) and seq[i - 1] != m["nucleobase"]:
            base_mismatch.append(m["oligo_id"])
    check("modification positions are contiguous 1..n", not pos_bad, f"{len(pos_bad)} oligos")
    check("modification row count equals oligo length", not count_bad, f"{len(count_bad)} oligos")
    check("modification nucleobase matches the sequence at that position", not base_mismatch,
          f"{len(set(base_mismatch))} oligos")

    covered = set(by_oligo)
    should = {o["oligo_id"] for o in oligos
              if o["modification_position_basis"].startswith("position_resolved")}
    check("every position-resolved oligo has a full modification table", should <= covered,
          f"{len(should - covered)} missing")

    # ---- report -------------------------------------------------------------------------
    passed = sum(1 for _, ok, _ in results if ok)
    summary = {
        "n_oligos": len(oligos), "n_measurements": len(meas),
        "n_modification_rows": len(mods), "n_sources": len(srcs),
        "checks_total": len(results), "checks_passed": passed,
        "checks_failed": len(results) - passed,
        "sequences_present": sum(1 for o in oligos if o["sequence_base"] not in MISSING_TOKENS),
        "position_resolved_oligos": len(should),
        "human_system_measurements": sum(1 for m in meas if m["is_human_system"] == "TRUE"),
        "grade_distribution": dict(sorted(collections.Counter(
            m["cns_tox_grade"] for m in meas if m["cns_tox_grade"] != "").items())),
        "study_type_distribution": dict(collections.Counter(m["study_type"] for m in meas)),
        "tox_axis_distribution": dict(collections.Counter(m["tox_axis"] for m in meas)),
        "species_distribution": dict(collections.Counter(m["species"] for m in meas)),
        "redistribution_distribution": dict(collections.Counter(m["redistribution"] for m in meas)),
    }
    # missingness on the challenge-mandated fields
    summary["missingness"] = {
        col: sum(1 for o in oligos if o[col] in MISSING_TOKENS)
        for col in ("sequence_base", "modification_positions", "purity_pct", "purity_method",
                    "identity_confirmation")
    }

    if as_json:
        print(json.dumps({"summary": summary,
                          "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in results]},
                         indent=2))
        return 0 if passed == len(results) else 1

    width = max(len(n) for n, _, _ in results)
    print("OligoTox-CNS dataset validation\n" + "=" * 78)
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<{width}}  {detail}")
    print("-" * 78)
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("-" * 78)
    if passed == len(results):
        print(f"PASS — {passed}/{len(results)} checks passed.")
        return 0
    print(f"FAIL — {len(results) - passed} of {len(results)} checks failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main("--json" in sys.argv))
