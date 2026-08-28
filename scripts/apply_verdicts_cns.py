#!/usr/bin/env python3
"""Apply adversarial-verification verdicts back into the lane extraction JSONs.

Corrections are written to the LANE files under `notes/cns/extractions/`, not to
the assembled CSVs, because the lane files are the source of truth: the CSVs are
regenerated from them by `scripts/assemble_cns.py`. Editing the CSVs directly
would be silently undone by the next assembly.

Why verdicts are re-keyed rather than applied by measurement_id
--------------------------------------------------------------
`measurement_id` is assigned at assembly time from the sorted, de-duplicated set
of lane rows. Adding a lane therefore renumbers everything after it, and the
verification batches were exported from an earlier assembly. Applying a verdict
by its `CMS####` would silently write a correction onto an unrelated row — the
worst possible failure for a process whose entire purpose is correctness.

So every verdict is re-keyed on the CONTENT of the row it was written against, as
captured in the batch export: canonical source reference, exact source locus,
readout name, and the oligo's name. A verdict that does not match exactly one
current row is REPORTED AND SKIPPED, never guessed at.

Usage:  python scripts/apply_verdicts_cns.py [--dry-run]
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT_DIR = os.path.join(ROOT, "notes", "cns", "extractions")
VERIFY_DIR = os.path.join(ROOT, "notes", "cns", "verify")

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from assemble_cns import canon_source_ref, norm  # noqa: E402

# Fields a verifier is allowed to correct. Deliberately excludes provenance
# columns: if a verifier believes the source itself is wrong, that is a REFUTED
# row to be dropped or re-extracted, not a citation to be rewritten.
CORRECTABLE = {"readout_value", "readout_unit", "effect_direction",
               "effect_vs_control", "neurotox_grade", "reversibility",
               "endpoint_domain", "challenge_priority", "readout_category",
               "redistribution", "dose_or_conc_value", "dose_or_conc_unit",
               "species", "cns_region", "exposure_duration", "system_model",
               "is_cns_specific"}


import qc_cns  # noqa: E402  (reuse the single definition of the vocabularies)


def valid_correction(field, value):
    """Is this correction a VALUE, or is it a verifier's prose recommendation?

    Verifiers legitimately write things like
        "neurotox_grade": "2 unless source_ref is amended to co-cite ..."
    which is a useful recommendation and a catastrophic cell value. Anything that
    does not conform to the column's own type or vocabulary is refused here and
    recorded as an advisory note instead, so a reviewer still sees the argument
    without the CSV acquiring a sentence where a grade belongs.
    """
    v = norm(value)
    if not v:
        return False
    if field == "neurotox_grade":
        return v in {"0", "1", "2", "3"}
    if field in ("dose_or_conc_value", "readout_value") and field == "dose_or_conc_value":
        if v == "TBD":
            return True
        try:
            float(v)
            return True
        except ValueError:
            return False
    allowed = qc_cns.ENUMS.get(field)
    if allowed is not None:
        return v in allowed
    # free-text columns: refuse anything that reads like advice rather than a value
    return not re.search(r"\b(unless|should|consider|or declare|de-duplicate|"
                         r"until the|recommend|drop or)\b", v, re.I)


def row_key(m, oligo_name):
    """Content identity of a measurement, used to re-key verdicts onto lane rows.

    Source, locus, readout name and oligo alone are not enough: a dose-response
    series shares all four across its arms, so a verdict about one arm would match
    several rows. Value and dose disambiguate them.
    """
    return (canon_source_ref(m.get("source_ref")).lower(),
            re.sub(r"\s+", " ", norm(m.get("source_table"))).lower()[:120],
            re.sub(r"\s+", "_", norm(m.get("readout_name")).lower()),
            norm(oligo_name).lower(),
            norm(m.get("readout_value")).lower(),
            norm(m.get("dose_or_conc_value")).lower())


def main():
    dry = "--dry-run" in sys.argv

    # ---- batch exports: measurement_id -> the row as verified -------------
    batch_rows = {}
    for p in glob.glob(os.path.join(VERIFY_DIR, "batch_*.json")):
        for r in json.load(open(p, encoding="utf-8")):
            batch_rows[r["measurement_id"]] = r
    if not batch_rows:
        raise SystemExit("no batch_*.json exports found in %s" % VERIFY_DIR)

    # ---- lane rows, indexed by content key --------------------------------
    lanes = {}
    index = defaultdict(list)
    for p in sorted(glob.glob(os.path.join(EXTRACT_DIR, "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        lane = d.get("lane") or os.path.splitext(os.path.basename(p))[0]
        lanes[lane] = (p, d)
        names = {o["oligo_id"]: o.get("oligo_name", "") for o in d.get("oligos", [])}
        for m in d.get("measurements", []):
            index[row_key(m, names.get(m.get("oligo_id"), ""))].append((lane, m))

    # ---- apply ------------------------------------------------------------
    stats = Counter()
    applied, skipped = [], []
    for p in sorted(glob.glob(os.path.join(VERIFY_DIR, "verdict_*.json"))):
        v = json.load(open(p, encoding="utf-8"))
        for verdict in v.get("verdicts", []):
            mid = verdict.get("measurement_id")
            stats["verdicts"] += 1
            stats["verdict:" + str(verdict.get("verdict"))] += 1
            raw_corr = {k: val for k, val in (verdict.get("correction") or {}).items()
                        if k in CORRECTABLE and str(val).strip() != ""}
            corr = {k: v for k, v in raw_corr.items() if valid_correction(k, v)}
            advisory = {k: v for k, v in raw_corr.items() if k not in corr}
            if advisory:
                stats["advisory_not_applied"] += len(advisory)
            note_only = verdict.get("verdict") in ("CONFIRMED", "CONFIRMED_MINOR") \
                and not corr
            if note_only:
                continue
            src = batch_rows.get(mid)
            if src is None:
                skipped.append((mid, "verdict id not present in any batch export"))
                stats["skipped"] += 1
                continue
            k = row_key(src, (src.get("_oligo") or {}).get("oligo_name", ""))
            hits = index.get(k, [])
            if len(hits) != 1:
                skipped.append((mid, "re-key matched %d rows (need exactly 1)"
                                % len(hits)))
                stats["skipped"] += 1
                continue
            lane, m = hits[0]
            changed = []
            for field, val in corr.items():
                old = norm(m.get(field))
                if old != norm(val):
                    m[field] = val
                    changed.append("%s:%s->%s" % (field, old, val))
            tag = "VERIFIED[%s]" % verdict.get("verdict")
            if advisory:
                tag += " ;; ADVISORY(not applied, not a value): " + "; ".join(
                    "%s=%s" % (k, re.sub(r"\s+", " ", str(v))[:160])
                    for k, v in advisory.items())
            if verdict.get("problem"):
                tag += " " + re.sub(r"\s+", " ", str(verdict["problem"]))[:240]
            m["notes"] = norm(m.get("notes")) + " ;; " + tag
            if changed:
                m["notes"] += " ;; corrected(" + ";".join(changed) + ")"
                stats["rows_corrected"] += 1
            else:
                stats["rows_annotated_only"] += 1
            applied.append((mid, lane, verdict.get("verdict"), changed))

    if not dry:
        for lane, (p, d) in lanes.items():
            json.dump(d, open(p, "w", encoding="utf-8"), indent=1)

    print("verdicts read        : %d" % stats["verdicts"])
    for k in sorted(stats):
        if k.startswith("verdict:"):
            print("  %-22s %d" % (k[8:], stats[k]))
    print("rows corrected       : %d" % stats["rows_corrected"])
    print("rows annotated only  : %d" % stats["rows_annotated_only"])
    print("advisory not applied : %d (prose, not a value - kept in notes)"
          % stats["advisory_not_applied"])
    print("verdicts skipped     : %d" % stats["skipped"])
    for mid, why in skipped[:15]:
        print("   SKIP %s: %s" % (mid, why))
    print()
    for mid, lane, vd, changed in applied:
        if changed:
            print("  %-10s [%s] %-16s %s" % (mid, lane, vd, "; ".join(changed)))
    if dry:
        print("\n(dry run - nothing written)")


if __name__ == "__main__":
    main()
