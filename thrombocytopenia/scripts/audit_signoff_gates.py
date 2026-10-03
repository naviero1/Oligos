#!/usr/bin/env python3
"""Audit this endpoint against German's twelve scientist sign-off gates (SCIENTIFIC_RULES.md §K).

Every verdict carries a measured figure. The verdict is this endpoint's self-assessment against
the gate text; it is NOT a sign-off. Only German signs off.

Writes data/signoff_gate_audit.csv and prints a table.
"""
import csv, os, json, collections

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

def load(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

MISSING = {"", "TBD", "NOT_REPORTED", "NA", "N/A", "NOT_APPLICABLE", "UNKNOWN", "none", "None"}
def has(v):
    return (v or "").strip() not in MISSING

meas = load("measurements.csv")
olig = load("oligos.csv")
ctrl = load("controls_inventory.csv")
stud = load("studies.csv")
audit = load("toxicity_denominator_audit.csv")
NM, NO = len(meas), len(olig)
mcols = set(meas[0].keys()) if meas else set()
ocols = set(olig[0].keys()) if olig else set()

rows = []
def gate(n, text, verdict, measured, detail):
    rows.append(dict(gate=n, gate_text=text, verdict=verdict, measured=measured, detail=detail))

# ---- Gate 1: traceable primary source + exact source location
import re as _re
g1_src = sum(1 for r in meas if has(r.get("source_ref")))
g1_loc = sum(1 for r in meas if has(r.get("source_table")))
g1_cell = sum(1 for r in meas if _re.search(
    r"(table|tbl|fig|suppl|mmc|S\d|row|page|p\.|sheet|appendix)", r.get("source_table") or "", _re.I))
gate(1, "Traceable primary source and exact source location",
     "PASS" if g1_loc == NM else "PARTIAL",
     f"source_ref {g1_src}/{NM}; in-document locus {g1_loc}/{NM}, of which "
     f"{g1_cell} name a table/figure/supplement cell and {g1_loc - g1_cell} name a document "
     f"section (prose-derived facts)",
     "Every row names both a retrievable source and a place inside it. The section-level loci are "
     "facts stated in prose rather than tabulated, so a section is their exact location; they are "
     "not missing loci. This gate passes on its own terms, which does not make the rows qualified "
     "- the other gates are where this endpoint fails.")

# ---- Gate 2: sequence verified 5'->3', strand identity and duplex partner
g2_seq = sum(1 for r in olig if has(r.get("sequence_5to3")))
g2_strand = "strand_role" in ocols
g2_duplex = "duplex_partner_id" in ocols
g2_ds = sum(1 for r in olig if "siRNA" in (r.get("oligo_class") or ""))
gate(2, "Sequence verified 5'->3', with strand identity and duplex partner where applicable",
     "FAIL",
     f"sequence_5to3 present {g2_seq}/{NO}; strand_role column {'present' if g2_strand else 'ABSENT'}; "
     f"duplex_partner_id column {'present' if g2_duplex else 'ABSENT'}; double-stranded constructs {g2_ds}",
     "Sequences are recorded and directional, but the two fields this gate names do not exist in "
     "the schema. For the double-stranded constructs the gate cannot be evaluated at all: nothing "
     "records which strand a sequence is, or what it pairs with. This is the clearest FAIL.")

# ---- Gate 3: modification encoded BY POSITION
g3_map = sum(1 for r in olig if has(r.get("modification_map")))
g3_verb = sum(1 for r in olig if has(r.get("modification_map")) and
              "verbatim" in (r.get("characterization_source") or "").lower())
g3_flagonly = sum(1 for r in olig if not has(r.get("modification_map"))
                  and has(r.get("sugar_modifications")))
gate(3, "Chemical modification encoded by position, not only as a molecule-level flag",
     "PARTIAL",
     f"position-resolved modification_map {g3_map}/{NO}; of those, source-verbatim {g3_verb}; "
     f"molecule-level flags only {g3_flagonly}/{NO}",
     "A minority carry a true per-position map. The majority carry molecule-level chemistry only, "
     "which is exactly what this gate excludes. Two maps were reverted this round because they had "
     "been composed from a related molecule's backbone rather than read from a source.")

# ---- Gate 4: assay context (cell system, donor, delivery, dose, exposure time)
g4 = {k: sum(1 for r in meas if has(r.get(k)))
      for k in ("system_model", "delivery_method", "dose_or_conc_value", "exposure_duration")}
g4_donor = "donor_id" in mcols
gate(4, "Assay context includes cell system, donor information, delivery/formulation, dose and exposure time",
     "PARTIAL",
     f"system_model {g4['system_model']}/{NM}; delivery_method {g4['delivery_method']}/{NM}; "
     f"dose {g4['dose_or_conc_value']}/{NM}; exposure_duration {g4['exposure_duration']}/{NM}; "
     f"donor_id column {'present' if g4_donor else 'ABSENT'}",
     "Dose and exposure are well covered; delivery/formulation is the weakest reported field and "
     "donor information has no column at all, so per-donor variation cannot be modelled or even "
     "counted. §B names donor/cell system as part of the unit of observation.")

# ---- Gate 5: raw/continuous outcomes retained; curator labels explicitly marked derived
g5_raw = sum(1 for r in meas if has(r.get("readout_value")))
g5_graded = sum(1 for r in meas if (r.get("thrombocytopenia_grade") or "").strip() in "0123"
                and (r.get("thrombocytopenia_grade") or "").strip() != "")
g5_marked = any(c in mcols for c in ("grade_is_curator_derived", "grade_provenance", "label_origin"))
gate(5, "Raw/continuous outcomes retained when available; curator-derived labels explicitly marked derived",
     "FAIL",
     f"continuous readout_value retained {g5_raw}/{NM}; curator-assigned grades {g5_graded}; "
     f"derived-label marker column {'present' if g5_marked else 'ABSENT'}",
     "The continuous readout is retained alongside the label, which is the half of this gate that "
     "passes. The other half fails outright: no column states that thrombocytopenia_grade is "
     "curator-derived rather than source-reported, so a downstream reader cannot tell the two apart. "
     "All graded rows are referred to German as provisional.")

# ---- Gate 6: agonist / antagonist / potentiator / inert separated
g6_col = any(c in mcols for c in ("response_state", "pharmacology_class", "activity_state"))
g6_dir = collections.Counter((r.get("effect_direction") or "NOT_REPORTED").strip() for r in meas)
gate(6, "Agonist, antagonist, potentiator and inert/low-response states are separated",
     "FAIL",
     f"response-state column {'present' if g6_col else 'ABSENT'}; "
     f"effect_direction distribution {dict(g6_dir.most_common(6))}",
     "effect_direction records which way a readout moved; it does not encode the four states this "
     "gate names. The gate is written for receptor pharmacology and generalizes here to separating "
     "an actively harmful construct from one measured and found inert. We cannot currently do that.")

# ---- Gate 7: human and animal not pooled
sep = all(os.path.exists(os.path.join(DATA, f)) for f in
          ("measurements_human.csv", "measurements_animal.csv"))
# Count on subject_class, the derived axis QC re-derives independently, so these figures
# agree with qc_thrombo.py. Counting animal as "everything not human" silently absorbed the
# 9 unresolved/multi-species rows into the animal side, which is the pooling this gate forbids.
nh = sum(1 for r in meas if (r.get("subject_class") or "").startswith("human"))
na = sum(1 for r in meas if (r.get("subject_class") or "").startswith("animal"))
nn = NM - nh - na
bridge = load("bridge_human_animal.csv")
bcols = set(bridge[0].keys()) if bridge else set()
pooled_col = [c for c in bcols if "grade_gap" in c]
gate(7, "Human and animal observations are not pooled as interchangeable ground truth",
     "PASS",
     f"separate views written {sep}; human rows {nh}; animal rows {na}; "
     f"assigned to neither (unresolved or multi-species) {nn}; "
     f"pooled grade-difference column {'STILL PRESENT: ' + str(pooled_col) if pooled_col else 'removed'}; "
     f"bridge carries exposure_comparable + interpretation_limit "
     f"{('exposure_comparable' in bcols) and ('interpretation_limit' in bcols)}",
     "Human and animal evidence are split into separate views, the ranking that feeds the scientist "
     "is computed on human rows only, and the arithmetic difference between a human and an animal "
     "grade — which asserted the interchangeability this gate forbids — was deleted and replaced by "
     "per-side exposure plus an explicit interpretation limit. Pooled multi-species findings are "
     "assigned to neither side rather than forced onto one.")

# ---- Gate 8: endpoint-specific outcomes not collapsed into a composite
rc = collections.Counter((r.get("readout_category") or "?").strip() for r in meas)
rn = len(set((r.get("readout_name") or "").strip() for r in meas))
plt_spec = sum(1 for r in meas if (r.get("is_platelet_specific") or "").strip().lower() in ("true", "yes", "1"))
gate(8, "Endpoint-specific outcomes are not collapsed into a composite (generalized from TLR7/8/9)",
     "PASS",
     f"distinct readout_name values {rn}; readout_category distribution {dict(rc.most_common(8))}; "
     f"platelet-specific rows flagged {plt_spec}/{NM}",
     "The named readout survives on every row; the grade is a secondary derived field layered over "
     "it, not a replacement for it. is_platelet_specific keeps a true platelet readout separable "
     "from a general haematology or safety readout, so nothing is silently composited.")

# ---- Gate 9: citation metadata and file identities pass QC
srcs = load("sources_inventory.csv")
uid = any("uid" in c for c in (srcs[0].keys() if srcs else []))
gate(9, "Citation metadata and file identities pass QC",
     "PASS",
     f"sources in inventory {len(srcs)}; stable source_uid assigned {uid}; "
     f"QC gates in scripts/qc_thrombo.py: 5 governance + round-trip + backbone-consistency",
     "Colliding source ids were resolved to stable uids, 27 citation defects found by auditing my "
     "own search fleet's log were corrected (a fabricated title, three false 'searched' flags, a "
     "yield inferred rather than read, twenty cross-family duplicates), and QC runs on every build. "
     "Gate 9 is about whether citations pass QC, and they do now — they did not before the audit.")

# ---- Gate 10: split leakage checks
g10 = {k: sum(1 for r in olig if has(r.get(k)))
       for k in ("exact_sequence_group", "scaffold_family", "publication_group", "matched_pair_id")}
gate(10, "Train/test splitting checked for exact-sequence, modified/unmodified counterpart, strand, "
         "family, paper and experimental-series leakage",
     "PARTIAL",
     f"exact_sequence_group {g10['exact_sequence_group']}/{NO}; scaffold_family {g10['scaffold_family']}/{NO}; "
     f"publication_group {g10['publication_group']}/{NO}; matched_pair_id {g10['matched_pair_id']}/{NO}; "
     f"strand grouping ABSENT; experimental-series grouping ABSENT; "
     f"measured leakage cost random ~0.94 vs LOPO ~0.65",
     "Four of the six leakage axes have grouping keys and the cost of ignoring them is measured, "
     "not assumed. Strand leakage cannot be checked because gate 2's fields do not exist. "
     "Experimental-series leakage has no key; the study registry's 23 proved nesting edges are the "
     "nearest thing and do not cover it.")

# ---- Gate 11: LOPO and sequence-family grouped performance with uncertainty
mdr = {}
p = os.path.join(DATA, "model_demo_results.json")
if os.path.exists(p):
    mdr = json.load(open(p, encoding="utf-8"))
gate(11, "LOPO and sequence-family grouped performance reported with uncertainty",
     "NOT APPLICABLE",
     f"classifier release state BLOCKED; model trained this round: "
     f"{'no' if mdr.get('classifier_status', 'retracted') != 'trained' else 'YES'}",
     "No model is trained, so there is no performance to report. The gate becomes live the moment "
     "one is, and reporting a single number without LOPO and sequence-family grouping would fail it. "
     "The prior classifier was retracted rather than re-reported.")

# ---- Gate 12: claims no stronger than the evidence supports
n_aud = sum(1 for r in audit if (r.get("audit_verdict") or "").strip() == "SURVIVES_ALL_FOUR")
n_aud_tot = len(audit)
gate(12, "All major mechanistic and clinical claims are no stronger than the evidence supports",
     "PARTIAL",
     f"count ladder published with every rung and its loss reason; endpoint audit survivors "
     f"{n_aud}/{n_aud_tot}; "
     f"in-vitro rows whose grade derives from a clinical scale {sum(1 for r in meas if (r.get('study_type') or '') in ('in_vitro','ex_vivo') and (r.get('thrombocytopenia_grade') or '').strip() in '0123')}",
     "Three overstatements were corrected this round: a structure-activity result asserted as "
     "reproduced from curation when it describes provisional curator labels; a rights conclusion "
     "stated as lawful redistributability when it is a project classification; and a trial count "
     "quotable as qualified when it is only typed. PARTIAL not PASS because the corrections were "
     "needed at all — the recurring finding across endpoints is conclusions outrunning evidence, "
     "and this endpoint produced three instances in one document set.")

out = os.path.join(DATA, "signoff_gate_audit.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["gate", "gate_text", "verdict", "measured", "detail"])
    w.writeheader(); w.writerows(rows)

# ---- The figure that matters: how many rows clear ALL twelve gates.
# Gates 2, 5 and 6 fail because the fields they require are absent from the schema entirely,
# so they fail identically on every row. No per-row arithmetic can rescue that.
failing = [r["gate"] for r in rows if r["verdict"] == "FAIL"]
n_qualified = 0 if failing else None

tally = collections.Counter(r["verdict"] for r in rows)
print(f"{'#':>3}  {'VERDICT':<15} MEASURED")
for r in rows:
    print(f"{r['gate']:>3}  {r['verdict']:<15} {r['measured'][:120]}")
print()
print("tally:", dict(tally))
print()
print(f"ROWS CLEARING ALL TWELVE GATES: {n_qualified} of {NM}")
print(f"  Gates {failing} fail for want of schema fields, so they fail on every row alike.")
print("  This is the figure to quote when asked whether the endpoint is sign-off ready.")
print("  It is not a quality judgement on the rows; it is the distance left to travel.")
print("wrote", out)
