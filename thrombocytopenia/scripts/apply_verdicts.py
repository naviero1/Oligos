#!/usr/bin/env python3
"""Apply adversarial-verification verdicts to the assembled measurements.csv.

Verifiers address rows by `measurement_id`, but those IDs are assigned by sort
order at assembly time and therefore SHIFT whenever rows are added. Applying a
verdict blindly by ID against a re-assembled table would silently correct or
delete the wrong row — a worse outcome than not verifying at all.

So every verdict is matched by ID *and then confirmed* against the row's
oligo_name and readout_name. A verdict whose ID no longer points at the row the
verifier described is REFUSED, counted, and reported, never guessed at.

  CONFIRMED  -> row untouched, marked verified in notes
  CORRECTED  -> named fields overwritten, reason appended to notes
  REJECTED   -> row DELETED

Usage:
  python3 scripts/apply_verdicts.py verdicts1.json [verdicts2.json ...]
  python3 scripts/apply_verdicts.py --dry-run verdicts1.json
"""
import csv, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEAS = os.path.join(ROOT, "thrombocytopenia", "data", "measurements.csv")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)

    with open(MEAS, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols, rows = rdr.fieldnames, list(rdr)
    by_id = {r["measurement_id"]: r for r in rows}

    # Natural-key index, so verdicts survive the renumbering that a re-assembly
    # causes. freeze_verdicts.py stamps this key onto each verdict; when present
    # it is preferred over the volatile measurement_id.
    onames = {}
    opath = os.path.join(os.path.dirname(MEAS), "oligos.csv")
    with open(opath, newline="", encoding="utf-8") as f:
        onames = {r["oligo_id"]: r["oligo_name"] for r in csv.DictReader(f)}

    def nkey(r):
        return "|".join([norm(onames.get(r["oligo_id"], "")), norm(r.get("source_ref")),
                         norm(r.get("source_table")), norm(r.get("readout_name")),
                         norm(r.get("dose_or_conc_value"))])

    by_nk = {}
    for r in rows:
        by_nk.setdefault(nkey(r), []).append(r)

    verdicts = []
    for p in args:
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print(f"  SKIP {p}: {e}")
            continue
        v = d.get("verdicts") or []
        verdicts.extend(v)
        print(f"  loaded {len(v):>4} verdict(s) from {os.path.basename(p)}")
        if d.get("coverage"):
            print(f"        coverage: {str(d['coverage'])[:150]}")

    stats = collections.Counter()
    drop, mismatches = set(), []
    for v in verdicts:
        mid = v.get("measurement_id")
        row = None
        if v.get("natural_key"):
            cands = by_nk.get(v["natural_key"]) or []
            if len(cands) == 1:
                row = cands[0]
                stats["matched_by_natural_key"] += 1
            elif len(cands) > 1:
                stats["ambiguous_natural_key"] += 1
                continue
        if row is None:
            row = by_id.get(mid)
            if row is not None:
                stats["matched_by_id"] += 1
        if not row:
            stats["not_found"] += 1
            continue
        # ID stability guard: the row must still be the one the verifier described
        if (norm(v.get("oligo_name")) and norm(v.get("oligo_name")) != norm(row["oligo_id"])
                and norm(v.get("readout_name")) != norm(row["readout_name"])):
            stats["refused_id_mismatch"] += 1
            mismatches.append(f"{mid}: verdict says {v.get('readout_name')!r}, "
                              f"row has {row['readout_name']!r}")
            continue
        d = (v.get("verdict") or "").upper()
        if d == "REJECTED":
            drop.add(row["measurement_id"])
            stats["rejected"] += 1
        elif d == "CORRECTED":
            for c in v.get("corrections") or []:
                f_ = c.get("field")
                if f_ in cols:
                    row[f_] = c.get("corrected_value")
            row["notes"] = (row.get("notes", "") +
                            f";verifier_corrected:{str(v.get('reason'))[:150]}")
            stats["corrected"] += 1
        elif d == "CONFIRMED":
            row["notes"] = row.get("notes", "") + ";verified_against_source"
            stats["confirmed"] += 1
        else:
            stats["unknown_verdict"] += 1

    kept = [r for r in rows if r["measurement_id"] not in drop]
    print(f"\nverdicts: {dict(stats)}")
    if mismatches:
        print(f"REFUSED {len(mismatches)} verdict(s) whose id no longer matches the row "
              f"(dataset was re-assembled after verification):")
        for x in mismatches[:8]:
            print("   ", x)
    print(f"rows: {len(rows)} -> {len(kept)}")

    if dry:
        print("\n(dry run — nothing written)")
        return
    with open(MEAS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(kept)
    print(f"wrote {MEAS}")
    print("NOTE: measurement_ids are NOT renumbered here, so ids stay aligned with "
          "the verdicts just applied. Re-run assemble only when ingesting new lanes.")


if __name__ == "__main__":
    main()
