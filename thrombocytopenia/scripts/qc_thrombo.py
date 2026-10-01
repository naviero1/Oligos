#!/usr/bin/env python3
"""Quality-control validator for the OligoTox-Thrombocytopenia dataset.

Runs the checks documented in thrombocytopenia/METHODOLOGY.md §Quality control:
  - schema conformance   (column set + controlled-vocabulary enums)
  - referential integrity (measurements.oligo_id -> oligos.oligo_id, no orphans)
  - primary-key uniqueness
  - range checks         (thrombocytopenia_grade in 0..3, booleans TRUE/FALSE)
  - provenance completeness (every row has source_id + source_ref + source_table)
  - sequence policy      (only A/C/G/T/U characters, case-insensitive, or TBD)

Exits non-zero if any hard check fails, so it can gate a commit.

Usage:  python3 scripts/qc_thrombo.py
"""
import csv, os, re, sys, collections

# Paths are anchored to the ENDPOINT folder that owns this script, so all
# thrombocytopenia artefacts stay inside thrombocytopenia/ and nothing is
# written outside it.
ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ENDPOINT, "data")

OLIGO_COLS = ["oligo_id", "oligo_name", "aliases", "oligo_class", "target_gene",
              "indication", "developer", "max_phase", "length_nt",
              "backbone_chemistry", "sugar_modifications", "gapmer_design",
              "conjugate", "ps_count", "sequence_5to3", "modification_map",
              "purity_pct", "purity_method", "design_source", "notes",
              # --- scientific governance, ported from the scientist package v0.9 ---
              # Beebop P2 acceptance: "Every model-eligible row traces to a current
              # scientific disposition." These columns carry that trace, plus the
              # leakage grouping the scientist package requires for any split.
              "scientist_record_id", "scientist_disposition",
              "clinical_model_eligibility", "mechanistic_model_eligibility",
              "exact_sequence_group", "scaffold_family", "publication_group",
              "matched_pair_id", "modification_map_notation", "characterization_source"]

MEAS_COLS = ["measurement_id", "oligo_id", "study_type", "species", "system_model",
             "tissue", "delivery_method", "dose_or_conc_value", "dose_or_conc_unit",
             "exposure_duration", "readout_category", "readout_name", "readout_value",
             "readout_unit", "effect_direction", "effect_vs_control",
             "thrombocytopenia_grade", "is_platelet_specific", "subject_class",
             "source_id", "source_ref", "source_table", "redistribution", "notes"]

ENUMS = {
    "oligo_class": {"ASO_gapmer", "siRNA", "GalNAc_siRNA", "splice_switching_ASO",
                    "PMO", "aptamer", "other"},
    # "NA" = no internucleotide linkage exists (mononucleotide controls used as
    # negative comparators in the PF4/aptamer work) - distinct from "TBD" (unknown).
    "backbone_chemistry": {"full_PS", "PS_PO_mix", "full_PO", "PMO_neutral",
                           "mixed", "NA", "TBD"},
    "conjugate": {"none", "GalNAc", "lipid", "peptide", "PEG", "other", "TBD"},
    "max_phase": {"approved", "approved_EMA", "phase_3", "phase_3_discontinued",
                  "phase_2", "phase_2_discontinued", "phase_1", "preclinical",
                  "research_panel", "class_review", "TBD"},
    "study_type": {"in_vitro", "ex_vivo", "animal_invivo", "clinical"},
    # minipig: the Gottingen minipig is an established regulatory tox species and
    # appears here with its own GPVI/PF4 ontogeny data.
    "species": {"human", "monkey", "rat", "mouse", "dog", "minipig",
                "multi_species", "NA", "TBD"},
    "delivery_method": {"direct_addition", "gymnotic_free_uptake", "transfection",
                        "conjugate_mediated", "systemic_dose", "intrathecal",
                        "intravitreal", "oral", "subcutaneous", "TBD"},
    "dose_or_conc_unit": {"uM", "nM", "ug/mL", "mg/kg", "mg", "fold_Cmax", "NA", "TBD"},
    "readout_category": {"platelet_count", "platelet_activation", "platelet_aggregation",
                         "platelet_binding", "megakaryocyte", "immunogenicity",
                         "clinical_outcome", "histopathology", "viability", "coagulation"},
    "effect_direction": {"increase", "decrease", "no_change", "TBD"},
    "is_platelet_specific": {"TRUE", "FALSE"},
    "redistribution": {"public_domain", "cc_by", "derived_features_only",
                       "summary_stat", "verify"},
    "subject_class": {"human_clinical", "human_ex_vivo", "human_in_vitro", "human_other",
                      "animal_in_vivo", "animal_ex_vivo", "animal_in_vitro", "animal_other",
                      "multi_species", "unspecified"},
}

SEQ_RE = re.compile(r"^[ACGTUacgtu]+$")


def load(name):
    path = os.path.join(BASE, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f)), path


def main():
    errors, warnings = [], []
    oligos, opath = load("oligos.csv")
    meas, mpath = load("measurements.csv")

    # --- column-set conformance -------------------------------------------------
    if oligos and list(oligos[0].keys()) != OLIGO_COLS:
        errors.append(f"oligos.csv column set mismatch:\n  got {list(oligos[0].keys())}")
    if meas and list(meas[0].keys()) != MEAS_COLS:
        errors.append(f"measurements.csv column set mismatch:\n  got {list(meas[0].keys())}")

    # --- primary-key uniqueness -------------------------------------------------
    for rows, key, label in ((oligos, "oligo_id", "oligos"), (meas, "measurement_id", "measurements")):
        dupes = [k for k, c in collections.Counter(r[key] for r in rows).items() if c > 1]
        if dupes:
            errors.append(f"{label}: duplicate {key}: {dupes[:5]}")

    # --- referential integrity --------------------------------------------------
    known = {o["oligo_id"] for o in oligos}
    orphans = [m["measurement_id"] for m in meas if m["oligo_id"] not in known]
    if orphans:
        errors.append(f"measurements: {len(orphans)} orphan oligo_id refs: {orphans[:5]}")
    used = {m["oligo_id"] for m in meas}
    unused = sorted(known - used)
    if unused:
        warnings.append(f"oligos with no measurement rows: {len(unused)} ({unused[:5]})")

    # --- controlled vocabularies ------------------------------------------------
    for rows, label in ((oligos, "oligos"), (meas, "measurements")):
        for r in rows:
            pk = r.get("oligo_id") or r.get("measurement_id")
            for col, allowed in ENUMS.items():
                if col in r and r[col] and r[col] not in allowed:
                    errors.append(f"{label} {pk}: {col}={r[col]!r} not in controlled vocabulary")

    # --- subject_class must AGREE with the columns it summarises ---------------
    # Re-derived here independently of the assembler, so a stale or hand-edited
    # value cannot survive: the human/animal split is a headline property of this
    # dataset and must never disagree with study_type/species.
    ANIMAL = {"monkey", "rat", "mouse", "dog", "minipig"}

    def expect(st, sp):
        st, sp = (st or "").lower(), (sp or "").lower()
        if sp == "human":
            return {"clinical": "human_clinical", "ex_vivo": "human_ex_vivo",
                    "in_vitro": "human_in_vitro"}.get(st, "human_other")
        if sp in ANIMAL:
            return {"animal_invivo": "animal_in_vivo", "ex_vivo": "animal_ex_vivo",
                    "in_vitro": "animal_in_vitro"}.get(st, "animal_other")
        return "multi_species" if sp == "multi_species" else "unspecified"

    for m in meas:
        want = expect(m.get("study_type"), m.get("species"))
        got = m.get("subject_class", "")
        if got != want:
            errors.append(f"measurements {m['measurement_id']}: subject_class={got!r} "
                          f"disagrees with study_type={m.get('study_type')!r}/"
                          f"species={m.get('species')!r} (expected {want!r})")

    # --- range checks -----------------------------------------------------------
    for m in meas:
        g = m.get("thrombocytopenia_grade", "")
        if g not in {"0", "1", "2", "3"}:
            errors.append(f"measurements {m['measurement_id']}: grade={g!r} outside 0-3")

    # --- provenance completeness ------------------------------------------------
    for m in meas:
        for col in ("source_id", "source_ref", "source_table"):
            if not m.get(col) or m[col] in {"", "TBD", "NA"}:
                errors.append(f"measurements {m['measurement_id']}: missing provenance {col}")

    # --- provenance STRENGTH (not a failure, but must stay visible) -------------
    # A row citing a paywalled paper's abstract is legitimately sourced — an
    # abstract is a specific, retrievable locus — but it is weaker evidence than a
    # numbered table and must be re-verified against full text before release.
    # Surfacing the count here stops that caveat from being buried in a notes field.
    abstract_only = [m["measurement_id"] for m in meas
                     if "abstract" in (m.get("source_table") or "").lower()]
    if abstract_only:
        warnings.append(
            f"{len(abstract_only)} row(s) cite an abstract rather than a numbered "
            f"table/figure (paywalled full text) — verify before release: "
            f"{abstract_only[:5]}")

    # --- CONTROL-ARM rows carrying a non-zero grade ----------------------------
    # These are correctly graded: the rubric grades the OBSERVED band regardless of
    # study arm, and a placebo subject whose platelets genuinely fell below 75 K/uL
    # did have that event. But a model joining grade to DESIGN FEATURES would read
    # them as the compound causing an effect at zero dose. The canonical filter is
    # `dose_or_conc_value == "0"`; surfacing the count here keeps the hazard visible
    # instead of buried in prose.
    ctrl_nonzero = [m["measurement_id"] for m in meas
                    if str(m.get("dose_or_conc_value", "")).strip() in {"0", "0.0"}
                    and m.get("thrombocytopenia_grade") not in {"0", ""}]
    if ctrl_nonzero:
        warnings.append(
            f"{len(ctrl_nonzero)} CONTROL-ARM row(s) (dose 0) carry grade > 0 — correct "
            f"per the rubric, but MODELS MUST EXCLUDE dose_or_conc_value=='0' before "
            f"joining grade to design features: {ctrl_nonzero[:5]}")

    # --- Phase 2 dataset-content requirements, reported every run --------------
    # The announcement requires the dataset file to contain "the sequences of all
    # oligos tested, as well as the location of all chemical modifications in each
    # oligo, data on the purity and characterization of each". Coverage of those
    # three is a submission-blocking property, so it is surfaced on every QC run
    # rather than discovered late. These are WARNINGS, not errors: the shortfall is
    # a genuine limitation of curating published data, not a defect to be papered
    # over, and it is documented in STATUS.md and the methodology.
    def filled(col):
        return sum(1 for o in oligos if o.get(col, "") not in ("", "TBD", "NA"))

    n = len(oligos) or 1
    for col, label in (("sequence_5to3", "sequences"),
                       ("modification_map", "per-residue modification maps"),
                       ("purity_pct", "purity values"),
                       ("purity_method", "characterization methods")):
        k = filled(col)
        if k < n:
            warnings.append(f"Phase 2 dataset requirement — {label}: {k}/{n} "
                            f"({100*k//n}%) present; the rest are TBD")

    # --- sequence policy (case-insensitive; case encodes chemistry) -------------
    for o in oligos:
        s = o.get("sequence_5to3", "")
        if s and s not in ("TBD", "NA") and not SEQ_RE.match(s):
            errors.append(f"oligos {o['oligo_id']}: sequence_5to3 has non-ACGTU chars: {s!r}")
        if s and s not in ("TBD", "NA") and o.get("length_nt", "TBD") not in ("TBD", "", str(len(s))):
            warnings.append(
                f"oligos {o['oligo_id']}: length_nt={o['length_nt']} != len(sequence)={len(s)}")

    # --- GOVERNANCE GATES -------------------------------------------------------
    # Added 2026-10-01 in response to Beebop's Priority 5, which asks for targeted
    # checks against four specific failure modes. Each is an ERROR, not a warning:
    # every one of them would put a scientifically false claim into a release.

    # (1) No reversal of a scientist decision. Model eligibility may only be
    #     non-NO where a scientist record actually grants it.
    ELIG_OK = {"NO", "", "PROVISIONAL ONLY", "PROVISIONAL COMPARATOR",
               "PROVISIONAL - POSITIVE ONLY", "TREATMENT-AWARE ONLY"}
    for o in oligos:
        ce = (o.get("clinical_model_eligibility") or "").strip()
        me = (o.get("mechanistic_model_eligibility") or "").strip()
        sid = (o.get("scientist_record_id") or "").strip()
        if ce not in ELIG_OK:
            errors.append(f"oligos {o['oligo_id']}: clinical_model_eligibility={ce!r} "
                          f"not a scientist-defined value")
        if ce not in ("NO", "") and not sid:
            errors.append(f"oligos {o['oligo_id']}: clinical_model_eligibility={ce!r} "
                          f"without a scientist_record_id — a scientist decision cannot be "
                          f"granted by this pipeline")
        if me == "YES" and not sid:
            errors.append(f"oligos {o['oligo_id']}: mechanistic_model_eligibility=YES "
                          f"without a scientist_record_id")
        if sid and not (o.get("scientist_disposition") or "").strip():
            errors.append(f"oligos {o['oligo_id']}: has scientist_record_id {sid} but no disposition")

    # (2) No unsupported negatives. The scientist package rules
    #     CLEAN_CLINICAL_NEGATIVE "NOT YET AVAILABLE" and the qualified
    #     clinical-negative count 0. Nothing in this dataset may assert one.
    NEG_WORDS = re.compile(r"clean[_ ]clinical[_ ]negative|qualified[_ ]negative|"
                           r"confirmed[_ ]negative|clinical[_ ]negative", re.I)
    for m in meas:
        blob = f"{m.get('notes','')} {m.get('readout_name','')} {m.get('effect_vs_control','')}"
        if NEG_WORDS.search(blob):
            errors.append(f"measurements {m['measurement_id']}: asserts a clinical negative "
                          f"({NEG_WORDS.search(blob).group()!r}); the scientist package records "
                          f"zero qualified clinical negatives")

    # (3) No animal leakage into the human-facing views. Any compound ranked in
    #     germans_analysis.csv above a compound WITH human evidence must itself
    #     have human evidence.
    gpath = os.path.join(BASE, "germans_analysis.csv")
    if os.path.exists(gpath):
        with open(gpath, newline="", encoding="utf-8") as f:
            g = list(csv.DictReader(f))
        seen_no = None
        for r in g:
            if r.get("has_human_evidence") == "no" and seen_no is None:
                seen_no = r.get("rank")
            elif r.get("has_human_evidence") == "yes" and seen_no is not None:
                errors.append(f"germans_analysis.csv: {r.get('oligo_name')} (rank {r.get('rank')}) "
                              f"has human evidence but ranks BELOW an animal-only compound at "
                              f"rank {seen_no} — animal data is influencing the human ranking")
                break
        for r in g:
            if r.get("has_human_evidence") == "no" and (r.get("human_clinical_max_grade")
                                                        or r.get("human_lab_max_grade")):
                errors.append(f"germans_analysis.csv: {r.get('oligo_name')} flagged no human "
                              f"evidence but carries a human grade")

    # (4) Exact-sequence group integrity. Every oligo sharing a normalised
    #     sequence must share one group label, or an outer split separates
    #     isosequential constructs and the leakage the grouping exists to
    #     prevent happens anyway.
    bysq = collections.defaultdict(set)
    for o in oligos:
        sq = re.sub(r"[^ACGTU]", "", (o.get("sequence_5to3") or "").upper()).replace("U", "T")
        if len(sq) >= 8:
            bysq[sq].add((o.get("exact_sequence_group") or "").strip())
    for sq, labels in bysq.items():
        if len(labels) > 1:
            errors.append(f"exact_sequence_group split across one sequence {sq[:20]}: {sorted(labels)}")

    # (4b) Composed modification maps must round-trip. The rocksteady_v1 notation
    #      claims to be lossless in schema.md: the base sequence must be readable
    #      back off it and ps_count must equal the number of PS linkage marks. A
    #      map that fails this is a positional-chemistry claim that cannot be
    #      checked, which is worse than TBD.
    TOK = re.compile(r"([emdlk])([ACGTU])(\(5m\))?([*-]?)")
    for o in oligos:
        if (o.get("modification_map_notation") or "") != "rocksteady_v1":
            continue
        mm = o.get("modification_map", "")
        toks = TOK.findall(mm)
        if sum(len("".join(t)) for t in toks) != len(mm):
            errors.append(f"oligos {o['oligo_id']}: modification_map does not fully parse "
                          f"under rocksteady_v1: {mm[:60]!r}")
            continue
        seq = "".join(t[1] for t in toks).replace("U", "T")
        want = re.sub(r"[^ACGTU]", "", (o.get("sequence_5to3") or "").upper()).replace("U", "T")
        if want and seq != want:
            errors.append(f"oligos {o['oligo_id']}: modification_map bases {seq!r} != "
                          f"sequence_5to3 {want!r}")
        ps = mm.count("*")
        if (o.get("ps_count") or "").isdigit() and int(o["ps_count"]) != ps:
            errors.append(f"oligos {o['oligo_id']}: ps_count={o['ps_count']} but "
                          f"modification_map has {ps} phosphorothioate linkage(s)")

    # (5) Trial double-counting, once the study registry exists.
    spath = os.path.join(BASE, "studies.csv")
    if os.path.exists(spath):
        with open(spath, newline="", encoding="utf-8") as f:
            studies = list(csv.DictReader(f))
        seen_reg = collections.defaultdict(list)
        for st in studies:
            rid = (st.get("registry_id") or "").strip().upper()
            if rid.startswith("NCT"):
                seen_reg[rid].append(st.get("study_id", "?"))
        for rid, ids in seen_reg.items():
            if len(ids) > 1:
                errors.append(f"studies.csv: registry id {rid} appears under {len(ids)} study "
                              f"records {ids} — one trial counted more than once")
        counted = [st for st in studies
                   if (st.get("evidence_unit_type") or "") == "registered_trial"
                   and (st.get("eligibility_decision") or "") == "included"]
        warnings.append(f"study registry: {len(studies)} evidence units, "
                        f"{len(counted)} counted as verified included registered trials")
    else:
        warnings.append("data/studies.csv not built yet — the headline human trial count "
                        "remains 'not yet established'; row counts must NOT be reported as trials")

    # --- report -----------------------------------------------------------------
    print(f"oligos.csv        {len(oligos):>4} rows x {len(OLIGO_COLS)} cols   {opath}")
    print(f"measurements.csv  {len(meas):>4} rows x {len(MEAS_COLS)} cols   {mpath}")
    if meas:
        gd = collections.Counter(m["thrombocytopenia_grade"] for m in meas)
        print("grade distribution 0/1/2/3 :",
              " / ".join(str(gd.get(str(i), 0)) for i in range(4)))
        print("study types                :",
              dict(collections.Counter(m["study_type"] for m in meas)))
        sc = collections.Counter(m.get("subject_class", "?") for m in meas)
        nh = sum(v for k, v in sc.items() if k.startswith("human"))
        na = sum(v for k, v in sc.items() if k.startswith("animal"))
        print(f"HUMAN / ANIMAL split       : {nh} human · {na} animal · "
              f"{len(meas) - nh - na} other")
        print("  subject_class            :", dict(sc.most_common()))
        print("platelet-specific TRUE     :",
              sum(1 for m in meas if m["is_platelet_specific"] == "TRUE"), "/", len(meas))
        print("distinct sources           :",
              len({m["source_ref"] for m in meas}))
    if oligos:
        withseq = sum(1 for o in oligos if o["sequence_5to3"] not in ("", "TBD"))
        print(f"sequences filled           : {withseq} / {len(oligos)}")
        print("oligo classes              :",
              dict(collections.Counter(o["oligo_class"] for o in oligos)))

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")

    if errors:
        print(f"\nQC FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"\nQC PASSED ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
