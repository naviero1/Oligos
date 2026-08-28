#!/usr/bin/env python3
"""Assemble the canonical OligoTox-Thrombocytopenia CSVs from curation-agent output.

Input is a JSON file with the shape produced by the curation workflow:

    {"lanes": [
        {"lane": "<lane key>",
         "oligos":       [ {<oligos.csv fields, keyed by oligo_name>}, ... ],
         "measurements": [ {<measurements.csv fields, oligo_name as FK>}, ... ],
         "verified":     {"verdicts": [
             {"oligo_name":..., "readout_name":..., "verdict":"CONFIRMED|CORRECTED|REJECTED",
              "reason":..., "corrections":[{"field":..., "corrected_value":...}]}, ...]}},
        ...]}

What it does, in order:
  1. Applies the adversarial verifier's verdicts — REJECTED rows are DROPPED,
     CORRECTED rows have the named fields overwritten.
  2. Deduplicates oligos on a normalized `oligo_name`, merging field-by-field and
     preferring a real value over "TBD" (never overwriting one real value with another;
     conflicts are reported).
  3. Deduplicates measurements on the natural key
     (oligo, study_type, system_model, dose, readout_name, source_ref, source_table).
  4. Assigns stable primary keys TOLG### / TMSR### in deterministic sorted order.
  5. Writes thrombocytopenia/data/oligos.csv and measurements.csv.

Rows referencing an oligo that no agent described are NOT silently dropped: a stub
oligo row is created with TBD design fields so referential integrity holds and the
gap is visible rather than hidden.

Usage:  python3 scripts/assemble_thrombo.py <curation_output.json>
"""
import csv, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "thrombocytopenia", "data")

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt",
              "backbone_chemistry", "sugar_modifications", "gapmer_design",
              "conjugate", "ps_count", "sequence_5to3", "design_source", "notes"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "tissue", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "readout_category", "readout_name", "readout_value",
             "readout_unit", "effect_direction", "effect_vs_control",
             "thrombocytopenia_grade", "is_platelet_specific", "source_id",
             "source_ref", "source_table", "redistribution", "notes"]

EMPTY = {"", None, "TBD", "NA", "n/a", "N/A", "null", "None", "unknown"}


def norm_name(n):
    """Normalize an oligo name to a join key: case- and punctuation-insensitive."""
    return re.sub(r"[^a-z0-9]", "", (n or "").lower())


def clean(v):
    if v is None:
        return "TBD"
    s = str(v).strip().replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s)
    return s if s else "TBD"


def apply_verdicts(lane):
    """Drop REJECTED rows and apply CORRECTED field overwrites. Returns (rows, stats)."""
    meas = lane.get("measurements") or []
    verified = lane.get("verified") or {}
    verdicts = verified.get("verdicts") or []

    # index verdicts by (normalized oligo, readout_name) — the verifier's addressing scheme
    vindex = {}
    for v in verdicts:
        vindex.setdefault((norm_name(v.get("oligo_name")),
                           clean(v.get("readout_name")).lower()), []).append(v)

    kept, stats = [], collections.Counter()
    for row in meas:
        key = (norm_name(row.get("oligo_name")), clean(row.get("readout_name")).lower())
        vs = vindex.get(key) or []
        verdict = None
        for v in vs:
            # consume each verdict once, so N identical rows map to N verdicts
            if not v.get("_used"):
                v["_used"] = True
                verdict = v
                break
        if verdict is None:
            stats["unverified"] += 1
            kept.append(row)
            continue
        d = verdict.get("verdict")
        if d == "REJECTED":
            stats["rejected"] += 1
            continue
        if d == "CORRECTED":
            for c in verdict.get("corrections") or []:
                f = c.get("field")
                if f in MEAS_COLS or f == "oligo_name":
                    row[f] = c.get("corrected_value")
            note = clean(row.get("notes"))
            reason = clean(verdict.get("reason"))[:160]
            row["notes"] = (note if note != "TBD" else "") + f";verifier_corrected:{reason}"
            stats["corrected"] += 1
        else:
            stats["confirmed"] += 1
        kept.append(row)
    return kept, stats


def merge_oligo(dst, src, conflicts):
    """Merge src into dst field-by-field, preferring real values over TBD."""
    for col in OLIGO_COLS:
        if col in ("oligo_id",):
            continue
        s = clean(src.get(col))
        d = clean(dst.get(col))
        if s in EMPTY:
            continue
        if d in EMPTY:
            dst[col] = s
        elif d != s:
            if col in ("aliases", "notes", "design_source"):
                parts = [p for p in (d.split(";") + s.split(";")) if p and p not in EMPTY]
                dst[col] = ";".join(dict.fromkeys(parts))
            elif col == "sequence_5to3":
                # never silently pick a winner between two different sequences
                conflicts.append(f"{dst['oligo_name']}: sequence conflict {d!r} vs {s!r}")
            else:
                conflicts.append(f"{dst['oligo_name']}.{col}: {d!r} vs {s!r} (kept first)")
    return dst


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        payload = json.load(f)

    lanes = payload.get("lanes") or []
    all_stats = collections.Counter()
    oligo_by_key, conflicts = {}, []
    meas_rows = []

    for lane in lanes:
        lname = lane.get("lane", "?")
        for o in lane.get("oligos") or []:
            k = norm_name(o.get("oligo_name"))
            if not k:
                continue
            row = {c: clean(o.get(c)) for c in OLIGO_COLS if c != "oligo_id"}
            row["oligo_name"] = clean(o.get("oligo_name"))
            if k in oligo_by_key:
                merge_oligo(oligo_by_key[k], row, conflicts)
            else:
                oligo_by_key[k] = row

        kept, stats = apply_verdicts(lane)
        all_stats.update(stats)
        for m in kept:
            m["_lane"] = lname
            meas_rows.append(m)

    # --- deduplicate measurements on their natural key --------------------------
    seen, deduped = {}, []
    for m in meas_rows:
        nk = (norm_name(m.get("oligo_name")),
              clean(m.get("study_type")).lower(),
              clean(m.get("system_model")).lower(),
              clean(m.get("dose_or_conc_value")).lower(),
              clean(m.get("readout_name")).lower(),
              clean(m.get("source_ref")).lower(),
              clean(m.get("source_table")).lower())
        if nk in seen:
            all_stats["duplicate_dropped"] += 1
            continue
        seen[nk] = True
        deduped.append(m)

    # --- stub any oligo referenced by a measurement but never described ---------
    for m in deduped:
        k = norm_name(m.get("oligo_name"))
        if k and k not in oligo_by_key:
            oligo_by_key[k] = {c: "TBD" for c in OLIGO_COLS if c != "oligo_id"}
            oligo_by_key[k]["oligo_name"] = clean(m.get("oligo_name"))
            oligo_by_key[k]["notes"] = "stub;design_metadata_not_yet_curated"
            all_stats["stub_oligos"] += 1

    # --- assign stable IDs (deterministic: sorted by name) -----------------------
    ordered = sorted(oligo_by_key.items(), key=lambda kv: kv[1]["oligo_name"].lower())
    for i, (k, row) in enumerate(ordered, start=1):
        row["oligo_id"] = f"TOLG{i:03d}"
    keymap = {k: row["oligo_id"] for k, row in ordered}

    # measurements sorted by oligo then source then readout for stable IDs
    deduped.sort(key=lambda m: (keymap.get(norm_name(m.get("oligo_name")), "ZZZ"),
                                clean(m.get("source_ref")).lower(),
                                clean(m.get("source_table")).lower(),
                                clean(m.get("readout_name")).lower()))

    os.makedirs(BASE, exist_ok=True)
    with open(os.path.join(BASE, "oligos.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OLIGO_COLS)
        w.writeheader()
        for _, row in ordered:
            w.writerow({c: row.get(c, "TBD") for c in OLIGO_COLS})

    with open(os.path.join(BASE, "measurements.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MEAS_COLS)
        w.writeheader()
        for i, m in enumerate(deduped, start=1):
            row = {c: clean(m.get(c)) for c in MEAS_COLS}
            row["measurement_id"] = f"TMSR{i:03d}"
            row["oligo_id"] = keymap.get(norm_name(m.get("oligo_name")), "TBD")
            if row["source_id"] in EMPTY:
                row["source_id"] = m.get("_lane", "TBD")
            w.writerow(row)

    print(f"oligos.csv        {len(ordered)} rows")
    print(f"measurements.csv  {len(deduped)} rows")
    print("verdicts:", dict(all_stats))
    if conflicts:
        print(f"\n{len(conflicts)} merge conflict(s) needing review:")
        for c in conflicts[:25]:
            print("  ", c)


if __name__ == "__main__":
    main()
