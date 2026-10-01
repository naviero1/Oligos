#!/usr/bin/env python3
"""Reconcile the branch dataset against the scientist-governed package v0.9.

Beebop's Priority 2 asks for a crosswalk of retained / duplicate / conflicting /
newly-proposed / excluded records that preserves the scientist's adjudications.
The governing rule implemented here: the scientist package is AUTHORITATIVE on
disposition and model eligibility. This script never lets a HOLD or EXCLUDE
record silently become model-eligible, and never overwrites a scientist value
with a branch value -- a disagreement is recorded as a conflict, not resolved.

Also ports the scientist's per-residue Position_Chemistry (831 rows) into the
dataset's modification_map column, which was TBD for 257 of 259 oligos.

Writes:  data/oligos.csv (extended in place)
         curation/scientist_v09/crosswalk.csv
         curation/scientist_v09/conflicts.csv
"""
import csv, os, re, collections, itertools

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
SCI = os.path.join(ENDPOINT, "curation", "scientist_v09")

def rd(p):
    with open(p, newline="") as f: return list(csv.DictReader(f))

# ---- normalisation ---------------------------------------------------------
def nseq(s):
    s = re.sub(r"[^ACGTUacgtu]", "", s or "").upper().replace("U", "T")
    return s

def nname(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

# ---- load ------------------------------------------------------------------
oligos = rd(os.path.join(DATA, "oligos.csv"))
master = rd(os.path.join(SCI, "Oligo_Sequence_Master.csv"))
adjud  = {r["Sequence_Record_ID"]: r for r in rd(os.path.join(SCI, "Scientist_Adjudication.csv"))}
fams   = {r["Sequence_Record_ID"]: r for r in rd(os.path.join(SCI, "Sequence_Family_Groups.csv"))}
chars  = {r["Sequence_Record_ID"]: r for r in rd(os.path.join(SCI, "Oligo_Characterization.csv"))}
poschem = rd(os.path.join(SCI, "Position_Chemistry.csv"))

# ---- branch lookup tables --------------------------------------------------
by_seq = collections.defaultdict(list)
by_nm  = collections.defaultdict(list)
for o in oligos:
    s = nseq(o["sequence_5to3"])
    if len(s) >= 8: by_seq[s].append(o)
    for nm in [o["oligo_name"]] + (o["aliases"] or "").split(";"):
        if nname(nm): by_nm[nname(nm)].append(o)

# ---- per-residue modification map ------------------------------------------
SUGAR = {"2′-O-methoxyethyl": "e", "2'-O-methoxyethyl": "e",
         "2′-O-methyl": "m", "2'-O-methyl": "m",
         "2′-deoxy": "d", "2'-deoxy": "d",
         "LNA": "l", "constrained ethyl (cEt)": "k"}
LINK = {"PS": "*", "PO": "-", "TERMINAL": ""}

def build_map(rows):
    """rows = Position_Chemistry rows for one sequence record, any order."""
    rows = sorted(rows, key=lambda r: int(r["Position_1based"]))
    out, unknown = [], set()
    for i, r in enumerate(rows):
        sg = SUGAR.get(r["Sugar_Modification"].strip())
        if sg is None:
            unknown.add(r["Sugar_Modification"]); sg = "?"
        res = f"{sg}{r['Base'].strip()}"
        if "5-methylcytosine" in (r["Base_Modification"] or ""): res += "(5m)"
        link = LINK.get(r["Linkage_to_Next"].strip(), "?") if i < len(rows) - 1 else ""
        out.append(res + link)
    return "".join(out), unknown

maps, ps_counts = {}, {}
for sid, rows in itertools.groupby(sorted(poschem, key=lambda r: r["Sequence_Record_ID"]),
                                     key=lambda r: r["Sequence_Record_ID"]):
    rows = list(rows)
    m, unk = build_map(rows)
    maps[sid] = m
    ps_counts[sid] = sum(1 for r in rows if r["Linkage_to_Next"].strip() == "PS")
    if unk: print(f"  ! unmapped sugar vocabulary for {sid}: {unk}")

# ---- crosswalk -------------------------------------------------------------
NEW_COLS = ["scientist_record_id", "scientist_disposition", "clinical_model_eligibility",
            "mechanistic_model_eligibility", "exact_sequence_group", "scaffold_family",
            "publication_group", "matched_pair_id", "modification_map_notation",
            "characterization_source"]
for o in oligos:
    for c in NEW_COLS: o.setdefault(c, "")
    if not o["modification_map_notation"] and o["modification_map"] not in ("", "TBD"):
        o["modification_map_notation"] = "source_verbatim"

xwalk, conflicts, recoveries = [], [], []
matched_oids = set()

# ---- branch-wide exact-sequence groups -------------------------------------
# German's leakage audit covers 12 records inside the 45-record scientist set.
# The same hazard exists dataset-wide: 35 distinct sequences are shared by 2-8
# separate oligo records here. Grouping must therefore be computed over ALL
# oligos, not only the adjudicated ones, or an outer split still leaks.
import hashlib
for o in oligos:
    s_ = nseq(o["sequence_5to3"])
    if len(s_) >= 8 and len(by_seq[s_]) > 1:
        o["exact_sequence_group"] = "EXACT-" + hashlib.sha1(s_.encode()).hexdigest()[:10].upper()
    elif len(s_) >= 8:
        o["exact_sequence_group"] = "SINGLETON-" + o["oligo_id"]
    else:
        o["exact_sequence_group"] = "NO_SEQUENCE-" + o["oligo_id"]

def ps_load(m):
    """Scientist-stated phosphorothioate linkage count, or None."""
    t = (m.get("PS_Load") or "").strip()
    mm = re.search(r"\d+", t)
    if not mm: return None
    n = int(mm.group())
    if re.search(r"\bnone\b|phosphodiester", t, re.I) and n == 0: return 0
    return n

def sids_in(text):
    """DOI / PMID / PMC identifiers mentioned in a free-text field."""
    t = (text or "").lower()
    out = set(re.findall(r"10\.\d{4,9}/[^\s;,()\]]+", t))
    out |= {"pmid" + x for x in re.findall(r"pmid[:\s]*(\d{6,8})", t)}
    out |= set(re.findall(r"pmc\d{6,8}", t))
    out |= {"pmid" + x for x in re.findall(r"^(\d{8})_", t)}
    return out

def toks(s):
    return set(re.findall(r"\d{4,7}", s or ""))

def chem_tag(s):
    s = (s or "").upper()
    return ("LNA" in s, s.endswith("-PO") or "_PO" in s or " PO" in s,
            "THIO" in s or s.endswith("-PS") or "_PS" in s)

def resolve(m, cands):
    """Narrow candidates to one. Chemistry VETOES a name match: bare compound
    names such as "ODN 2395" are shared by a phosphorothioate and an
    isosequential phosphodiester record, and name matching alone picks the
    wrong one -- it selected the ps_count=0 negative control for a full-PS
    scientist record. So the stated PS load filters the pool before any
    name rule runs."""
    cname = m["Canonical_Name"]
    aliases = [a for a in (m["Alias_or_Study_ID"] or "").replace("/", ";").split(";") if a.strip()]
    uniq = {c["oligo_id"]: c for c in cands}
    cands = list(uniq.values())

    psl, vetoed = ps_load(m), []
    if psl is not None and len(cands) > 1:
        keep = []
        for c in cands:
            bps = (c["ps_count"] or "").strip()
            if bps.isdigit() and int(bps) != psl: vetoed.append(c["oligo_id"])
            else: keep.append(c)
        if keep: cands = keep

    tag = "_chem_vetoed:" + ",".join(vetoed) if vetoed else ""
    if len(cands) == 1: return cands[0], "single_candidate" + tag
    hit = [c for c in cands if nname(c["oligo_name"]) == nname(cname)]
    if len(hit) == 1: return hit[0], "sequence+exact_name" + tag
    hit = [c for c in cands if nname(cname) in {nname(a) for a in (c["aliases"] or "").split(";")}
           or any(nname(a) == nname(c["oligo_name"]) for a in aliases)]
    if len(hit) == 1: return hit[0], "sequence+alias"
    t = toks(cname) | set().union(*[toks(a) for a in aliases]) if aliases else toks(cname)
    if t:
        hit = [c for c in cands if t & (toks(c["oligo_name"]) | toks(c["aliases"]))]
        if len(hit) == 1: return hit[0], "sequence+isis_number"
    want_lna = "LNA" in cname.upper()
    hit = [c for c in cands
           if ("LNA" in (c["oligo_name"] + " " + (c["aliases"] or "")).upper()) == want_lna]
    if len(hit) == 1: return hit[0], "sequence+LNA_token" + tag
    want = chem_tag(cname)
    hit = [c for c in cands if chem_tag(c["oligo_name"]) == want]
    if len(hit) == 1: return hit[0], "sequence+chemistry_token" + tag
    sset = sids_in(m.get("Citation", "")) | sids_in(m.get("Source_File_or_Recovery", ""))
    if sset:
        hit = [c for c in cands if sset & sids_in(c["design_source"])]
        if len(hit) == 1: return hit[0], "sequence+source_overlap" + tag
    return None, "unresolved" + tag

for m in master:
    sid, cname = m["Sequence_Record_ID"], m["Canonical_Name"]
    sq = nseq(m["Sequence_5to3"])
    cands, basis = [], ""
    if len(sq) >= 8 and by_seq.get(sq):
        cands, basis = by_seq[sq], "exact_sequence"
    else:
        for nm in [cname] + (m["Alias_or_Study_ID"] or "").replace("/", ";").split(";"):
            if nname(nm) and by_nm.get(nname(nm)):
                cands, basis = by_nm[nname(nm)], "name_or_alias"; break

    a, f, ch = adjud.get(sid, {}), fams.get(sid, {}), chars.get(sid, {})
    disp = (a.get("Current_Scientist_Disposition") or "").strip()
    clin = (a.get("Can_Enter_Final_Clinical_Model") or "").strip()
    mech = (a.get("Can_Enter_Mechanistic_Model") or "").strip()

    o, how = (None, "no_candidate") if not cands else resolve(m, cands)
    if o is None:
        status = ("newly_proposed_by_scientist_absent_from_branch" if not cands
                  else "ambiguous_unresolved_requires_scientist_review")
        oid = ";".join(sorted({c["oligo_id"] for c in cands}))
        if cands:
            conflicts.append({"kind": "ambiguous_identity", "scientist_record_id": sid,
                              "compound": cname, "oligo_id": oid, "scientist_value": m["Sequence_5to3"],
                              "branch_value": ", ".join(sorted({c["oligo_name"] for c in cands})),
                              "resolution": "UNRESOLVED - scientist must pick the intended record"})
    else:
        status, oid = "retained_matched", o["oligo_id"]
        basis = f"{basis} ({how})"
        matched_oids.add(oid)
        o["scientist_record_id"] = sid
        o["scientist_disposition"] = disp
        o["clinical_model_eligibility"] = clin or "NO"
        o["mechanistic_model_eligibility"] = mech or "NO"
        if f.get("Exact_Sequence_Group"):
            o["exact_sequence_group"] = f["Exact_Sequence_Group"]   # scientist label wins
        o["scaffold_family"] = f.get("Scaffold_Family", "")
        o["publication_group"] = f.get("Publication_Group", "")
        o["matched_pair_id"] = f.get("Matched_Sequence_Pair_ID", "")
        if len(sq) >= 8:
            bseq = nseq(o["sequence_5to3"])
            if len(bseq) < 8:
                # branch had TBD / no usable sequence -> recover it from the
                # scientist package rather than calling it a conflict.
                o["sequence_5to3"] = m["Sequence_5to3"]
                o["design_source"] = ((o["design_source"] + ";") if o["design_source"] not in ("", "TBD") else "") \
                                     + f"scientist_v0.9 Oligo_Sequence_Master ({sid})"
                recoveries.append({"kind": "sequence_recovered", "scientist_record_id": sid,
                                   "compound": cname, "oligo_id": oid,
                                   "value": m["Sequence_5to3"],
                                   "basis": (m.get("Sequence_Status") or "").strip()})
            elif bseq != sq:
                conflicts.append({"kind": "sequence", "scientist_record_id": sid, "compound": cname,
                                  "oligo_id": oid, "scientist_value": m["Sequence_5to3"],
                                  "branch_value": o["sequence_5to3"],
                                  "resolution": "UNRESOLVED - scientist review required"})
        if sid in maps:
            if o["modification_map"] in ("", "TBD"):
                o["modification_map"] = maps[sid]
                o["modification_map_notation"] = "rocksteady_v1"
                o["characterization_source"] = f"scientist_v0.9 Position_Chemistry ({sid})"
            elif o["modification_map"] != maps[sid] and o["modification_map_notation"] != "rocksteady_v1":
                conflicts.append({"kind": "modification_map", "scientist_record_id": sid,
                                  "compound": cname, "oligo_id": oid,
                                  "scientist_value": maps[sid], "branch_value": o["modification_map"],
                                  "resolution": "branch value kept (source-verbatim); scientist review required"})
        bps = (o["ps_count"] or "").strip()
        if sid in ps_counts and bps.isdigit() and int(bps) != ps_counts[sid]:
            conflicts.append({"kind": "ps_count", "scientist_record_id": sid, "compound": cname,
                              "oligo_id": oid, "scientist_value": str(ps_counts[sid]),
                              "branch_value": bps,
                              "resolution": "branch value kept; scientist review required"})
        pur = (ch.get("Purity_Percent") or "").strip()
        if pur and pur.upper() != "NOT REPORTED IN CURRENT CORPUS":
            conflicts.append({"kind": "purity_available_in_scientist_package", "scientist_record_id": sid,
                              "compound": cname, "oligo_id": oid, "scientist_value": pur,
                              "branch_value": o["purity_pct"], "resolution": "PORT CANDIDATE"})

    xwalk.append({"scientist_record_id": sid, "canonical_name": cname,
                  "scientist_sequence": m["Sequence_5to3"], "match_basis": basis,
                  "branch_oligo_id": oid, "crosswalk_status": status,
                  "scientist_disposition": disp, "clinical_model_eligibility": clin,
                  "mechanistic_model_eligibility": mech,
                  "exact_sequence_group": f.get("Exact_Sequence_Group", ""),
                  "position_chemistry_rows": str(len([r for r in poschem if r["Sequence_Record_ID"] == sid])),
                  "purity_in_scientist_package": (ch.get("Purity_Percent") or "").strip(),
                  "scientist_required_action": (a.get("Blocking_Action") or m.get("Required_Next_Action") or "").strip()})

# ---- propagate scientist group labels across the whole sequence group -----
# A scientist label must cover EVERY branch record sharing that sequence. When
# only the adjudicated member carried it, the group fragmented (TOLG242 kept a
# derived label while TOLG243/244 took EXACT-ODN2395-PS-PO), and an outer split
# could then place isosequential records in different folds -- exactly the
# leakage the grouping exists to prevent.
seq_label = {}
for o in oligos:
    s_ = nseq(o["sequence_5to3"])
    if len(s_) >= 8 and o["scientist_record_id"] and not o["exact_sequence_group"].startswith(("EXACT-", "SINGLETON-", "NO_SEQUENCE-")):
        seq_label[s_] = o["exact_sequence_group"]
    elif len(s_) >= 8 and o["scientist_record_id"] and o["exact_sequence_group"].startswith("EXACT-") \
         and fams.get(o["scientist_record_id"], {}).get("Exact_Sequence_Group"):
        seq_label[s_] = fams[o["scientist_record_id"]]["Exact_Sequence_Group"]
propagated = 0
for o in oligos:
    s_ = nseq(o["sequence_5to3"])
    if s_ in seq_label and o["exact_sequence_group"] != seq_label[s_]:
        o["exact_sequence_group"] = seq_label[s_]; propagated += 1
print(f"group labels propagated to unadjudicated isosequential records: {propagated}")

# branch records with NO scientist disposition -> explicitly not model-eligible
for o in oligos:
    if not o["scientist_record_id"]:
        o["scientist_disposition"] = "NOT_ADJUDICATED"
        o["clinical_model_eligibility"] = "NO"
        o["mechanistic_model_eligibility"] = "NO"

# ---- write -----------------------------------------------------------------
cols = list(oligos[0].keys())
with open(os.path.join(DATA, "oligos.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(oligos)
with open(os.path.join(SCI, "crosswalk.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(xwalk[0].keys())); w.writeheader(); w.writerows(xwalk)
with open(os.path.join(SCI, "recoveries.csv"), "w", newline="") as f:
    fn = ["kind","scientist_record_id","compound","oligo_id","value","basis"]
    w = csv.DictWriter(f, fieldnames=fn); w.writeheader(); w.writerows(recoveries)
with open(os.path.join(SCI, "conflicts.csv"), "w", newline="") as f:
    fn = ["kind","scientist_record_id","compound","oligo_id","scientist_value","branch_value","resolution"]
    w = csv.DictWriter(f, fieldnames=fn); w.writeheader(); w.writerows(conflicts)

st = collections.Counter(x["crosswalk_status"] for x in xwalk)
print(f"\nscientist records:              {len(master)}")
for k, v in st.most_common(): print(f"  {v:3d}  {k}")
print(f"\nbranch oligos:                  {len(oligos)}")
print(f"  {len(matched_oids):3d}  carry a scientist disposition")
print(f"  {len(oligos)-len(matched_oids):3d}  NOT_ADJUDICATED -> model-ineligible by default")
print(f"\nmodification_map populated:     {sum(1 for o in oligos if o['modification_map'] not in ('','TBD'))} / {len(oligos)}")
print(f"recoveries from scientist pkg:  {len(recoveries)}")
for k, v in collections.Counter(c["kind"] for c in recoveries).most_common(): print(f"  {v:3d}  {k}")
print(f"conflicts recorded:             {len(conflicts)}")
for k, v in collections.Counter(c["kind"] for c in conflicts).most_common(): print(f"  {v:3d}  {k}")
ce = collections.Counter(o["clinical_model_eligibility"] for o in oligos)
me = collections.Counter(o["mechanistic_model_eligibility"] for o in oligos)
g = collections.Counter(o["exact_sequence_group"] for o in oligos)
shared = {k: v for k, v in g.items() if v > 1}
print(f"\nexact-sequence groups with >1 record: {len(shared)} groups covering {sum(shared.values())} oligos")
print("clinical_model_eligibility:", dict(ce))
print("mechanistic_model_eligibility:", dict(me))
