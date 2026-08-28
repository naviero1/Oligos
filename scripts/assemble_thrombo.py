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

# Controlled-vocabulary near-misses. Extraction agents occasionally mistype an enum
# value ("public_documain"), and a single bad cell fails QC for the whole dataset.
# These are corrected here and every correction is REPORTED — the point is to fix
# unambiguous typos without hiding them. Anything not listed still reaches
# qc_thrombo.py and still fails, which is what should happen to a value whose
# intended meaning is not obvious.
VOCAB_FIXES = {
    "redistribution": {
        "public_documain": "public_domain", "public domain": "public_domain",
        "publicdomain": "public_domain", "public_domian": "public_domain",
        "cc-by": "cc_by", "ccby": "cc_by", "cc by": "cc_by",
        "summary_stats": "summary_stat", "summary stat": "summary_stat",
        "derived_features": "derived_features_only",
    },
    "is_platelet_specific": {"true": "TRUE", "false": "FALSE",
                             "True": "TRUE", "False": "FALSE"},
    "effect_direction": {"increased": "increase", "decreased": "decrease",
                         "unchanged": "no_change", "none": "no_change"},
    "study_type": {"invitro": "in_vitro", "in vitro": "in_vitro",
                   "exvivo": "ex_vivo", "ex vivo": "ex_vivo",
                   "animal_in_vivo": "animal_invivo", "in_vivo": "animal_invivo"},
}


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


# `max_phase` is by definition the MAXIMUM development stage a compound reached,
# so two sources disagreeing is usually not a conflict at all — it is one source
# being older. Crooke 2017 lists inotersen as phase 1 because it predates the 2018
# approval. Taking the later stage is the semantically correct merge; "keep first"
# would silently under-report every compound that advanced after its oldest source.
PHASE_RANK = {
    "TBD": -1, "research_panel": 0, "preclinical": 1, "phase_1": 2, "phase_2": 3,
    "phase_2_discontinued": 3, "phase_3": 4, "phase_3_discontinued": 4,
    "approved_EMA": 5, "approved": 6, "class_review": 0,
}


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
            if col == "max_phase":
                if PHASE_RANK.get(s, -1) > PHASE_RANK.get(d, -1):
                    dst[col] = s
                continue
            if col in ("aliases", "notes", "design_source", "sugar_modifications"):
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

    # --- handle oligos that no surviving measurement references ------------------
    # Two very different cases hide here, and collapsing them loses real data:
    #
    #  (a) A bare stub — no sequence, no design source. Nothing to learn from and
    #      nothing to predict; dropped.
    #  (b) A fully curated compound with a sourced sequence and design metadata that
    #      simply has no *individual* outcome row, because its source reported a
    #      POOLED outcome across a cohort (e.g. the 16 named ASOs in the Crooke
    #      pooled safety database, whose outcomes are recorded against the
    #      "2'-MOE ASO class pool" pseudo-oligo). These are kept: the sequences are
    #      hard-won, independently length-validated predictors, and the identity of
    #      the compounds making up a pooled cohort is itself information. A modeller
    #      wanting only rows with outcomes gets them from the join, for free.
    #
    # Both counts are reported; qc_thrombo surfaces the kept ones as a warning.
    referenced = {norm_name(m.get("oligo_name")) for m in deduped}
    unreferenced = sorted(k for k in oligo_by_key if k not in referenced)
    dropped_names, kept_unref = [], []
    for k in unreferenced:
        row = oligo_by_key[k]
        substantive = (row.get("sequence_5to3") not in EMPTY
                       or row.get("design_source") not in EMPTY)
        if substantive:
            note = row.get("notes", "")
            row["notes"] = ((note if note not in EMPTY else "")
                            + ";no_individual_measurement_row"
                            + ";outcome_reported_only_at_cohort_level_by_its_source")
            kept_unref.append(row["oligo_name"])
            all_stats["oligo_kept_no_measurements"] += 1
        else:
            dropped_names.append(row["oligo_name"])
            all_stats["oligo_dropped_empty_stub"] += 1
            del oligo_by_key[k]

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

    vocab_fixed = []
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
            for col, fixes in VOCAB_FIXES.items():
                v = row.get(col)
                if v in fixes:
                    vocab_fixed.append(f"{col}: {v!r} -> {fixes[v]!r}")
                    row[col] = fixes[v]
            row["measurement_id"] = f"TMSR{i:03d}"
            row["oligo_id"] = keymap.get(norm_name(m.get("oligo_name")), "TBD")
            if row["source_id"] in EMPTY:
                row["source_id"] = m.get("_lane", "TBD")
            w.writerow(row)

    print(f"oligos.csv        {len(ordered)} rows")
    print(f"measurements.csv  {len(deduped)} rows")
    print("verdicts:", dict(all_stats))
    if dropped_names:
        print(f"dropped {len(dropped_names)} empty stub oligo(s): {dropped_names[:8]}")
    if vocab_fixed:
        import collections as _c
        cnt = _c.Counter(vocab_fixed)
        print(f"corrected {len(vocab_fixed)} controlled-vocabulary typo(s):")
        for k, n in cnt.most_common(10):
            print(f"    {k}  (x{n})")
    if kept_unref:
        print(f"kept {len(kept_unref)} curated oligo(s) with no individual measurement "
              f"(pooled-cohort outcomes): {kept_unref[:8]}")
    if conflicts:
        print(f"\n{len(conflicts)} merge conflict(s) needing review:")
        for c in conflicts[:25]:
            print("  ", c)


if __name__ == "__main__":
    main()
