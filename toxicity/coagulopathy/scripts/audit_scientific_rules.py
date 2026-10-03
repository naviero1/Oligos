#!/usr/bin/env python3
"""Audit this endpoint against SCIENTIFIC_RULES.md §B, §C and §G.

    python3 toxicity/coagulopathy/scripts/audit_scientific_rules.py
    -> research/2026-10-03/schema_coverage_vs_SCIENTIFIC_RULES.csv

Why this exists. German's scientific framework became visible to this session on 2026-10-03.
It names a minimum schema (§C), a required unit of observation (§B) and grouping columns that
"must exist from the start" (§G). This audit states, field by field, what this endpoint has,
what it has under a different name, and what is absent — with the populated count, because a
column that exists and is empty is not coverage.

It reports. It changes nothing: §C says dropping a field because an endpoint finds it
inconvenient "is a question for German", and adding schema columns is gated on the Tier 0
crosswalk. The output is the input to that crosswalk, not a substitute for it.

Status vocabulary:
  present             a column of that name exists
  present_renamed     the field exists under a different name, given in `our_column`
  partial             part of the field's meaning is captured, and what is missing is stated
  absent              no column carries it
"""
import csv, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "research", "2026-10-03")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"


def load(n):
    p = os.path.join(DATA, n)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8"))) if os.path.exists(p) else []


# (German's field, group, status, our column or '', table, note)
FIELDS = [
    # --- identity and chemistry -------------------------------------------------------
    ("sequence_5to3", "identity", "present_renamed", "sequence_5to3_asprinted", "oligos",
     "also sequence_base with chemistry stripped, and length_nt_from_sequence computed from it"),
    ("strand_role", "identity", "absent", "", "oligos",
     "NOT MODELLED. modality distinguishes single_stranded_ASO / double_stranded_siRNA / aptamer, "
     "but a duplex is held as ONE row with one sequence field: the antisense and sense strands "
     "cannot be addressed separately and the complement is unrepresentable, not NOT_REPORTED"),
    ("duplex_partner_id", "identity", "absent", "", "oligos",
     "NOT MODELLED. follows from strand_role: there is no second strand row to point at"),
    ("backbone_by_linkage", "identity", "present_renamed", "backbone_linkage_3p", "modifications",
     "per position, linkage 3' of each residue; molecule-level backbone_chemistry is the "
     "secondary derived flag, which is the ordering §C requires"),
    ("sugar_mod_by_position", "identity", "present_renamed", "sugar_mod", "modifications", "per position"),
    ("base_mod_by_position", "identity", "partial", "is_5_methyl_C", "modifications",
     "only 5-methyl-C is captured, as a boolean. Any other base modification has nowhere to go"),
    ("terminal_modifications", "identity", "present_renamed", "terminal_modification", "oligos",
     "held at oligo level because a terminal residue has no position in a 5'->3' base string"),
    ("gap_length_nt", "identity", "partial", "gapmer_design", "oligos",
     "free text such as '5-10-5' rather than an integer gap length; machine-readable gap length absent"),
    # --- characterization -------------------------------------------------------------
    ("purity_pct", "characterization", "present", "purity_pct", "oligos",
     "plus purity_batches holding every value against its lot, and purity_pct_basis separating "
     "tested_batch from drug_substance_specification"),
    ("identity_method", "characterization", "present_renamed", "identity_confirmation", "oligos",
     "plus identity_methods_regulatory for values recovered from a regulatory quality section"),
    ("endotoxin_level", "characterization", "absent", "", "oligos",
     "NOT MODELLED. endotoxin limits appear in the EPAR quality sections we hold and were not extracted"),
    # --- exposure and system ----------------------------------------------------------
    ("formulation", "exposure", "partial", "delivery_method", "measurements",
     "delivery_method mixes route and vehicle; formulation is not a separate field"),
    ("delivery_agent", "exposure", "partial", "delivery_method", "measurements",
     "LNP / GalNAc / naked is partly inferable from delivery_method and oligos.conjugate, not a field"),
    ("anticoagulant", "exposure", "absent", "", "measurements",
     "NOT MODELLED, and this one bites HERE specifically: citrate vs heparin vs hirudin changes "
     "a clotting-time readout directly. Some rows name it inside system_model free text"),
    ("dose_value", "exposure", "present", "dose_value", "measurements", ""),
    ("dose_unit", "exposure", "present", "dose_unit", "measurements", ""),
    ("exposure_time_h", "exposure", "partial", "exposure_duration", "measurements",
     "free text with mixed units ('26 weeks', '4 h'), not normalised to hours; timepoint is separate"),
    ("cell_system", "exposure", "present_renamed", "system_model", "measurements",
     "plus matrix (plasma / whole_blood / serum / in_vivo / purified_system)"),
    ("cell_subset", "exposure", "absent", "", "measurements", "NOT MODELLED"),
    ("species", "exposure", "present", "species", "measurements",
     "plus species_class (human/animal/not_determined) and species_class_basis, because a "
     "purified human protein assay carries species=NOT_APPLICABLE while being a human system"),
    ("donor_id", "exposure", "absent", "", "measurements",
     "NOT MODELLED. donor-level replication cannot be distinguished from technical replication"),
    ("donor_class", "exposure", "absent", "", "measurements",
     "NOT MODELLED. healthy volunteer vs patient is only in population text on the study register"),
    ("sample_state", "exposure", "absent", "", "measurements",
     "NOT MODELLED. fresh / frozen / pooled is not captured; pooled plasma is named in free text only"),
    # --- outcome and adjudication -----------------------------------------------------
    ("endpoint_name", "outcome", "present_renamed", "readout_name", "measurements",
     "plus readout_category, and readout_category_as_curated where the scope rule replaced it"),
    ("raw_value", "outcome", "present_renamed", "readout_value", "measurements",
     "plus control_value, ratio_to_control and ratio_basis"),
    ("raw_unit", "outcome", "present_renamed", "readout_unit", "measurements", ""),
    ("author_interpretation", "outcome", "present_renamed", "severity_stated_by_source", "measurements",
     "plus source_stated_grade where the source graded severity itself"),
    ("curator_label", "outcome", "present_renamed", "coag_tox_grade", "measurements",
     "plus grade_basis, grade_authority, grade_status and is_validated_clinical_grade. "
     "SEE THE FLAG ON §E BELOW: the grade is derived from CTCAE cut-offs, which §E prohibits "
     "for in-vitro fold-change bins"),
    ("immunomodulatory_direction", "outcome", "present_renamed", "effect_direction", "measurements",
     "increase / decrease / no_change; the immune-specific sense of the field does not apply here"),
    ("receptor_pathway", "outcome", "absent", "", "measurements",
     "NOT MODELLED as a field. GPVI, PF4 and contact-pathway mechanisms appear in notes free text"),
    ("mechanism_evidence_type", "outcome", "absent", "", "measurements", "NOT MODELLED"),
    ("clinical_anchor", "outcome", "partial", "study_id", "measurements",
     "study_id links a clinical row to a register trial for 424 of 749 rows; it is a trial link, "
     "not the clinical-anchor concept of §C"),
    ("evidence_confidence", "outcome", "partial", "evidence_class", "measurements",
     "evidence_class says what KIND of observation a row is, with evidence_class_basis and "
     "evidence_class_review_status. It is not a confidence score and no GOLD/SILVER/BRONZE tier exists"),
    # --- grouping, §G -----------------------------------------------------------------
    ("sequence_family_group", "grouping", "absent", "", "oligos",
     "ABSENT AND REQUIRED FROM THE START by §G. Grouped splits by sequence family are "
     "impossible without it. A candidate grouping can be computed but §G also forbids merging "
     "chemically distinct constructs, so the adjudication is German's"),
    ("paper_group", "grouping", "absent", "", "measurements",
     "ABSENT AS A COLUMN, but source_id is a faithful proxy: every row carries exactly one "
     "source, so leave-one-paper-out is computable today by grouping on source_id"),
]


def main():
    O, D, M = load("oligos.csv"), load("measurements.csv"), load("modifications.csv")
    tables = {"oligos": O, "measurements": D, "modifications": M}
    rows = []
    for field, group, status, ours, table, note in FIELDS:
        recs = tables.get(table, [])
        populated = ""
        if ours and recs and ours in recs[0]:
            n = sum(1 for r in recs if str(r.get(ours, "")).strip() not in ("", NR, NA))
            populated = f"{n} of {len(recs)}"
        elif ours and recs:
            status, note = "absent", (note + " [named column not found in the table]").strip()
        rows.append({
            "german_field": field, "group": group, "status": status,
            "our_column": ours or "-", "table": table,
            "populated": populated or "-", "note": note,
        })
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "schema_coverage_vs_SCIENTIFIC_RULES.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    c = Counter(r["status"] for r in rows)
    print(f"  {len(rows)} fields named in SCIENTIFIC_RULES.md §C/§G audited against this endpoint")
    for k in ("present", "present_renamed", "partial", "absent"):
        print(f"    {c.get(k, 0):2d}  {k}")
    print("  absent:", ", ".join(r["german_field"] for r in rows if r["status"] == "absent"))
    print("  partial:", ", ".join(r["german_field"] for r in rows if r["status"] == "partial"))
    print(f"  -> research/2026-10-03/schema_coverage_vs_SCIENTIFIC_RULES.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
