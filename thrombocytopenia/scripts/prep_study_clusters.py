#!/usr/bin/env python3
"""Assign a stable source_uid to every distinct source document and slice the
human clinical evidence into per-compound clusters for trial-level resolution.

Fixes a provenance defect found 2026-09-30: `source_id` is NOT unique per
source. Three source_id values each stand for up to 8 genuinely different
papers (85 rows), so any study registry keyed on source_id would silently
merge distinct trials. The stable key is the (source_id, source_ref) pair.
"""
import csv, json, os, re, hashlib, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
OUT = os.path.join(ENDPOINT, "curation", "studies")
os.makedirs(OUT, exist_ok=True)

M = list(csv.DictReader(open(os.path.join(DATA, "measurements.csv"))))
O = {r["oligo_id"]: r for r in csv.DictReader(open(os.path.join(DATA, "oligos.csv")))}

# ---- stable source_uid -----------------------------------------------------
def uid(source_id, source_ref):
    h = hashlib.sha1(f"{source_id}||{source_ref}".encode()).hexdigest()[:6].upper()
    return f"SRC-{h}"

pairs = sorted({(m["source_id"], m["source_ref"]) for m in M})
SRC = {p: uid(*p) for p in pairs}

# ---- cluster assignment ----------------------------------------------------
# Ordered rules: first match wins. Keyed on source_ref text (the reliable field).
CLUSTERS = [
    ("crooke2017_pooled", [r"PMID 28145801", r"CROOKE2017"]),
    ("volanesorsen",      [r"004538", r"WAYLIVRA", r"Waylivra", r"NEJMoa1715944", r"31390500",
                           r"PMC6386089", r"mt\.2016\.136", r"cvaa077", r"32243492"]),
    ("inotersen",         [r"211172", r"004782", r"Tegsedi", r"TEGSEDI", r"NEJMoa1716793", r"29972757"]),
    ("imetelstat",        [r"217779", r"RYTELO"]),
    ("oncology_aso",      [r"NCT00138658", r"NCT00327340", r"CCR-22-2483", r"37364001",
                           r"OTT\.S33077", r"bcp\.12633", r"MD\.0000000000014254"]),
    ("other_regulatory",  [r"214012", r"LEQVIO", r"210922", r"215515", r"AMVUTTRA", r"Qalsody",
                           r"006072", r"Spinraza", r"SPINRAZA", r"004312", r"Onpattro", r"004699",
                           r"Amvuttra", r"005852", r"TRYNGOLZA", r"olezarsen"]),
]

def cluster_of(ref):
    for name, pats in CLUSTERS:
        for p in pats:
            if re.search(p, ref):
                return name
    return "literature_misc"

# ---- emit source inventory -------------------------------------------------
inv = []
for (sid, ref) in pairs:
    rows = [m for m in M if m["source_id"] == sid and m["source_ref"] == ref]
    cls = collections.Counter(r["subject_class"] for r in rows)
    inv.append({
        "source_uid": SRC[(sid, ref)], "legacy_source_id": sid, "source_ref": ref,
        "cluster": cluster_of(ref), "n_rows": len(rows),
        "n_human_clinical": cls.get("human_clinical", 0),
        "n_human_lab": cls.get("human_in_vitro", 0) + cls.get("human_ex_vivo", 0),
        "n_animal": sum(v for k, v in cls.items() if k.startswith("animal")),
        "subject_classes": ";".join(f"{k}={v}" for k, v in sorted(cls.items())),
    })
with open(os.path.join(DATA, "sources_inventory.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(inv[0].keys())); w.writeheader(); w.writerows(inv)

collide = collections.defaultdict(set)
for (sid, ref) in pairs: collide[sid].add(ref)
n_coll = sum(1 for v in collide.values() if len(v) > 1)
print(f"source documents (stable uid):      {len(pairs)}")
print(f"legacy source_id values:            {len(collide)}")
print(f"  ... of which collide (>1 doc):    {n_coll}")

# ---- slice clinical clusters for agent resolution --------------------------
hc = [m for m in M if m["subject_class"] == "human_clinical"]
buckets = collections.defaultdict(list)
for m in hc:
    buckets[cluster_of(m["source_ref"])].append(m)

KEEP = ["measurement_id","oligo_id","study_type","system_model","tissue","delivery_method",
        "dose_or_conc_value","dose_or_conc_unit","exposure_duration","readout_category",
        "readout_name","readout_value","readout_unit","effect_direction","effect_vs_control",
        "thrombocytopenia_grade","source_id","source_ref","source_table","notes"]

print(f"\nhuman_clinical rows: {len(hc)}  ->  {len(buckets)} clusters")
for name in sorted(buckets, key=lambda k: -len(buckets[k])):
    rows = buckets[name]
    oids = sorted({r["oligo_id"] for r in rows})
    payload = {
        "cluster": name, "n_rows": len(rows),
        "compounds": [{"oligo_id": o, "oligo_name": O.get(o, {}).get("oligo_name", "?"),
                       "sequence_5to3": O.get(o, {}).get("sequence_5to3", ""),
                       "max_phase": O.get(o, {}).get("max_phase", "")} for o in oids],
        "source_documents": sorted({
            f"{SRC[(r['source_id'], r['source_ref'])]} :: {r['source_ref']}" for r in rows}),
        "rows": [{**{k: r[k] for k in KEEP},
                  "source_uid": SRC[(r["source_id"], r["source_ref"])]} for r in rows],
    }
    p = os.path.join(OUT, f"cluster_{name}.json")
    json.dump(payload, open(p, "w"), indent=1)
    print(f"  {len(rows):4d} rows  {len(oids):3d} cpd  {len(payload['source_documents']):2d} docs  {name}")

# ---- human laboratory evidence (separate: not trials) ----------------------
lab = [m for m in M if m["subject_class"] in ("human_in_vitro", "human_ex_vivo")]
json.dump({"n_rows": len(lab),
           "source_documents": sorted({f"{SRC[(r['source_id'],r['source_ref'])]} :: {r['source_ref']}" for r in lab}),
           "rows": [{**{k: r[k] for k in KEEP}, "subject_class": r["subject_class"],
                     "species": r["species"], "system_model": r["system_model"],
                     "source_uid": SRC[(r["source_id"], r["source_ref"])]} for r in lab]},
          open(os.path.join(OUT, "human_lab_evidence.json"), "w"), indent=1)
print(f"\nhuman laboratory / ex-vivo rows (NOT trials): {len(lab)}")

# ---- unresolved ------------------------------------------------------------
un = [m for m in M if m["subject_class"] in ("unspecified", "multi_species")]
json.dump([{k: m[k] for k in KEEP + ["subject_class", "species"]} for m in un],
          open(os.path.join(OUT, "unresolved_rows.json"), "w"), indent=1)
print(f"unresolved (unspecified / multi_species):    {len(un)}")
