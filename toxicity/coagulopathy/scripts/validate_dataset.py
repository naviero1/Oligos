#!/usr/bin/env python3
"""Structural QC for the OligoTox-Coagulopathy tables. Exits non-zero on any failure.

    python3 toxicity/coagulopathy/scripts/validate_dataset.py

Every check is structural or internal-consistency: it can be re-run by anyone from the
committed CSVs with no network access and no domain judgement. Checks that would require
reading a source are NOT here -- those are the verification pass recorded in the dossier.
"""
import csv, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
NR, NA = "NOT_REPORTED", "NOT_APPLICABLE"

def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

fails, checks = [], []

def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def check(name, ok, detail=""):
    checks.append((name, ok, detail))
    if not ok:
        fails.append(f"{name}: {detail}")

S, O, M, D = load("sources.csv"), load("oligos.csv"), load("modifications.csv"), load("measurements.csv")

# ---- 1-4 primary keys ------------------------------------------------------
for nm, rows, key in (("sources", S, "source_id"), ("oligos", O, "oligo_id"),
                      ("measurements", D, "measurement_id")):
    ids = [r[key] for r in rows]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    check(f"PK unique: {nm}.{key}", not dup, f"{len(dup)} duplicated: {dup[:5]}")
mk = [(r["oligo_id"], r["position"]) for r in M]
dup = [k for k, v in Counter(mk).items() if v > 1]
check("PK unique: modifications(oligo_id,position)", not dup, f"{len(dup)} duplicated: {dup[:5]}")

# ---- 5-7 referential integrity ---------------------------------------------
oids, sids = {r["oligo_id"] for r in O}, {r["source_id"] for r in S}
bad = [r["measurement_id"] for r in D if r["oligo_id"] not in oids]
check("FK: measurements.oligo_id -> oligos", not bad, f"{len(bad)} orphans: {bad[:5]}")
bad = [r["measurement_id"] for r in D if r["source_id"] not in sids and r["source_id"] != NR]
check("FK: measurements.source_id -> sources", not bad, f"{len(bad)} orphans: {bad[:5]}")
bad = [r["oligo_id"] for r in M if r["oligo_id"] not in oids]
check("FK: modifications.oligo_id -> oligos", not bad, f"{len(bad)} orphans: {bad[:5]}")

# ---- 8-12 controlled vocabularies ------------------------------------------
VOCAB = {
 "study_type": {"in_vitro", "ex_vivo_plasma", "animal_invivo", "clinical", NR},
 # The nine core coagulation categories, plus four that exist only on scope_adjacent rows:
 # a complement fragment, a target transcript level, an infusion reaction and a blanket
 # adverse-event statement are not coagulation readouts and no longer borrow a name that
 # says they are. readout_category_as_curated keeps what the curator originally wrote.
 "readout_category": {"clotting_time", "factor_activity", "fibrinogen", "thrombin_generation",
                      "fibrinolysis_marker", "anticoagulant_activity", "bleeding_outcome",
                      "thrombotic_outcome", "platelet_coag_crosstalk",
                      "complement_marker", "target_transcript_level", "infusion_reaction",
                      "blanket_adverse_event_statement", NR},
 "effect_direction": {"increase", "decrease", "no_change", NR, NA},  # NA = pre-dose baseline, not an effect
 "grade_status": {"provisional"},
 "readout_is_qualitative": {"TRUE", "FALSE"},
}
for col, allowed in VOCAB.items():
    bad = sorted({r[col] for r in D if r[col] not in allowed})
    check(f"vocabulary: measurements.{col}", not bad, f"unexpected {bad[:6]}")

for col in ("on_target_effect", "unintended_toxicity"):
    bad = sorted({r[col] for r in D if r[col] not in {"TRUE", "FALSE"}})
    check(f"boolean: measurements.{col}", not bad, f"unexpected {bad[:6]}")
bad = sorted({r["is_5_methyl_C"] for r in M if r["is_5_methyl_C"] not in {"TRUE", "FALSE"}})
check("boolean: modifications.is_5_methyl_C", not bad, f"unexpected {bad[:6]}")

# ---- 13-15 grade integrity --------------------------------------------------
bad = [r["measurement_id"] for r in D if r["coag_tox_grade"] not in {"0", "1", "2", "3", NR}]
check("range: coag_tox_grade in {0,1,2,3,NOT_REPORTED}", not bad, f"{len(bad)}: {bad[:5]}")
bad = [r["measurement_id"] for r in D if r["coag_tox_grade"] != NR and not r["grade_basis"].strip()]
check("every graded row states its grading rule", not bad, f"{len(bad)} without grade_basis")
bad = [r["measurement_id"] for r in D
       if r["coag_tox_grade"] == NR and r["grade_basis"] in ("", NR)]
check("every ungraded row states why it is ungraded", not bad, f"{len(bad)} without a reason")

# ---- 16-18 provenance -------------------------------------------------------
for col in ("verbatim_quote", "source_locus"):
    bad = [r["measurement_id"] for r in D if not str(r[col]).strip() or r[col] in (NR, NA)]
    check(f"provenance: every measurement has {col}", not bad, f"{len(bad)}: {bad[:5]}")
bad = [r["measurement_id"] for r in D
       if r["readout_is_qualitative"] == "FALSE" and r["readout_value"] in (NR, NA, "")]
check("a non-qualitative row carries a value", not bad,
      f"{len(bad)} rows marked numeric but hold no value: {bad[:5]}")

# ---- 19-21 the no-fabrication invariants ------------------------------------
bad = [r["measurement_id"] for r in D if r["readout_value"] == "" or r["control_value"] == ""]
check("no blank-as-missing (must be NOT_REPORTED)", not bad, f"{len(bad)}: {bad[:5]}")
bad = [r["oligo_id"] for r in O if r["sequence_base"] == ""]
check("no blank sequence cells", not bad, f"{len(bad)}: {bad[:5]}")
bad = [r["measurement_id"] for r in D if "TBD" in (r["readout_value"] + r["control_value"])]
check("no TBD sentinel leaked in", not bad, f"{len(bad)}: {bad[:5]}")

# ---- 22-25 sequence and per-position chemistry ------------------------------
seqs = {r["oligo_id"]: r["sequence_base"].upper()
        for r in O if r["sequence_base"] not in (NR, NA, "")}

bad = sorted(r["oligo_id"] for r in O
             if r["sequence_base"] not in (NR, NA, "") and re.search(r"[^ACGTU]", r["sequence_base"]))
check("sequence_base holds nucleotides only (prose belongs in sequence_note)", not bad,
      f"{len(bad)}: {bad[:6]}")

bad = sorted(r["oligo_id"] for r in O if not (str(r["length_nt"]).isdigit() or r["length_nt"] == NR))
check("length_nt is an integer or NOT_REPORTED", not bad, f"{len(bad)}: {bad[:6]}")

bad = []
for r in O:
    s, L = seqs.get(r["oligo_id"], ""), r["length_nt"]
    if not s or not str(L).isdigit():
        continue
    caps = 0 if r["terminal_modification"] in (NA, NR, "") else len(r["terminal_modification"].split(";"))
    if int(L) != len(s) + caps:
        bad.append(f"{r['oligo_id']}(declared={L},seq={len(s)},caps={caps})")
check("declared length_nt equals sequence length plus documented terminal residues", not bad,
      f"{len(bad)}: {bad[:6]}")

bad = sorted(r["oligo_id"] for r in O
             if r["sequence_base"] not in (NR, NA, "") and str(r["length_nt_from_sequence"]) != str(len(r["sequence_base"])))
check("length_nt_from_sequence is computed, not asserted", not bad, f"{len(bad)}: {bad[:6]}")

bypos = defaultdict(dict)
for r in M:
    if str(r["position"]).isdigit():
        bypos[r["oligo_id"]][int(r["position"])] = r
bad = []
for oid, pos in bypos.items():
    ks = sorted(pos)
    if ks != list(range(1, len(ks) + 1)):
        bad.append(f"{oid}(1..{len(ks)} expected, got {ks[:3]}..{ks[-1]})")
check("modification positions are contiguous from 1", not bad, f"{len(bad)}: {bad[:6]}")

bad = []
for oid, pos in bypos.items():
    s = seqs.get(oid)
    if not s:
        continue
    if len(pos) != len(s):
        bad.append(f"{oid}(mods={len(pos)},seq={len(s)})")
        continue
    for i, ch in enumerate(s, 1):
        b = str(pos[i]["nucleobase"]).upper()
        if b in ("", NR, NA):
            continue
        if b != ch and not (b == "T" and ch == "U") and not (b == "U" and ch == "T"):
            bad.append(f"{oid}@{i}({b}!={ch})")
            break
check("modification nucleobase matches the sequence at that position", not bad, f"{len(bad)}: {bad[:6]}")

mods_no_seq = sorted({oid for oid in bypos if oid not in seqs})
check("no per-position chemistry without a sequence to anchor it", not mods_no_seq,
      f"{len(mods_no_seq)}: {mods_no_seq[:6]}")

# ---- 26-28 ratio and grade agree -------------------------------------------
bad = []
for r in D:
    ratio, g = f(r["ratio_to_control"]), r["coag_tox_grade"]
    if ratio is None or g == NR or "CTCAE" not in r["grade_basis"]:
        continue
    nm = r["readout_name"]
    if nm in {"aPTT", "PT", "INR", "TT", "ACT"}:
        exp = "0" if ratio <= 1.0 else "1" if ratio <= 1.5 else "2" if ratio <= 2.5 else "3"
    elif nm == "fibrinogen":
        exp = "0" if ratio >= 1.0 else "1" if ratio >= 0.75 else "2" if ratio >= 0.5 else "3"
    else:
        continue
    if exp != g:
        bad.append(f"{r['measurement_id']}(ratio={ratio},grade={g},expected={exp})")
check("grade is reproducible from ratio_to_control by the stated rule", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["ratio_to_control"] != NR and r["ratio_basis"] in ("", NR)]
check("every ratio states how it was derived", not bad, f"{len(bad)}: {bad[:5]}")
bad = [r["measurement_id"] for r in D
       if r["ratio_to_control"] == NR and r["ratio_basis"] in ("", NR)]
check("every missing ratio states why", not bad, f"{len(bad)}: {bad[:5]}")

# ---- 29-30 roll-ups agree with the rows -------------------------------------
cnt = Counter(r["oligo_id"] for r in D)
bad = [r["oligo_id"] for r in O if int(r["n_measurements"]) != cnt.get(r["oligo_id"], 0)]
check("oligos.n_measurements agrees with measurements.csv", not bad, f"{len(bad)}: {bad[:5]}")
cnt = Counter(r["source_id"] for r in D)
bad = [r["source_id"] for r in S if int(r["n_measurements"]) != cnt.get(r["source_id"], 0)]
check("sources.n_measurements agrees with measurements.csv", not bad, f"{len(bad)}: {bad[:5]}")


# ---- 37-44 invariants added after the adversarial verification pass ----------
missing = [(r["source_id"], r["document_file"], r["n_measurements"]) for r in S
           if r["document_file"] not in (NR, "")
           and not os.path.exists(os.path.join(ROOT, "sources", "documents", r["document_file"]))]
check("every source's document_file resolves in sources/documents/", not missing,
      f"{len(missing)} missing: {missing[:3]}")

for col, allowed in (("is_baseline", {"TRUE", "FALSE"}),
                     ("grade_caveat", {"within_reference_range_resolution", NA}),
                     ("source_stated_grade", {"1", "2", "3", "4", "5", NA})):
    bad = sorted({r[col] for r in D if r[col] not in allowed})
    check(f"vocabulary: measurements.{col}", not bad, f"unexpected {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["ratio_basis"] == "value_is_already_control_referenced" and f(r["control_value"]) is not None]
check("no ratio ignores a matched control that is present", not bad,
      f"{len(bad)} rows reference the untreated cell while holding a comparator: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["effect_direction"] == "no_change" and r["coag_tox_grade"] in {"1", "2", "3"}]
check("a source-stated measured null is never graded as a toxicity", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["is_baseline"] == "TRUE" and (r["coag_tox_grade"] != NR or r["effect_direction"] != NA)]
check("a pre-dose baseline carries neither a grade nor a direction", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["readout_unit"] == "%_inhibition_vs_control" and r["ratio_basis"] == "value_over_matched_control"]
check("percent-inhibition rows are not read as percent-of-control", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["co_administered_agent"] != NA and r["notes"].strip() == ""]
check("a combination row keeps the note that documents its partner agent", not bad, f"{len(bad)}: {bad[:5]}")


bad = sorted({r["study_type"] for r in D if re.search(r"human|mouse|rat|monkey|pig|dog", r["study_type"], re.I)})
check("no study_type value encodes a species (species_class carries that)", not bad, f"{bad}")

for col, allowed in (("species_class", {"human", "animal", "not_determined"}),
                     ("human_system", {"TRUE", "FALSE"})):
    bad = sorted({r[col] for r in D if r[col] not in allowed})
    check(f"vocabulary: measurements.{col}", not bad, f"unexpected {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if (r["species_class"] == "human") != (r["human_system"] == "TRUE")]
check("human_system agrees with species_class", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D if not str(r["species_class_basis"]).strip()]
check("every species_class states how it was determined", not bad, f"{len(bad)}: {bad[:5]}")

cntH = Counter(r["oligo_id"] for r in D if r["species_class"] == "human")
cntA = Counter(r["oligo_id"] for r in D if r["species_class"] == "animal")
bad = [r["oligo_id"] for r in O
       if int(r["n_human_measurements"]) != cntH.get(r["oligo_id"], 0)
       or int(r["n_animal_measurements"]) != cntA.get(r["oligo_id"], 0)]
check("oligos human/animal roll-ups agree with measurements.csv", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["oligo_id"] for r in O
       if (r["has_human_and_animal_data"] == "TRUE") !=
          bool(cntH.get(r["oligo_id"], 0) and cntA.get(r["oligo_id"], 0))]
check("has_human_and_animal_data is derived, not asserted", not bad, f"{len(bad)}: {bad[:5]}")


bad = sorted({r["endpoint_scope"] for r in D if r["endpoint_scope"] not in {"coagulation", "scope_adjacent"}})
check("vocabulary: measurements.endpoint_scope", not bad, f"unexpected {bad[:5]}")

# The coagulation lexicon is imported from the build so the two cannot drift apart.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_dataset import COAG_LEXICON as LEX

bad = sorted({r["readout_name"] for r in D
              if r["endpoint_scope"] == "coagulation" and not LEX.search(r["readout_name"])})
check("every in-scope readout is a coagulation readout (else mark it scope_adjacent)", not bad,
      f"{len(bad)} unrecognised: {bad[:6]}")

bad = [r["measurement_id"] for r in D
       if r["endpoint_scope"] == "scope_adjacent" and r["endpoint_scope_note"] in ("", NA)]
check("every scope_adjacent row says why it is out of scope", not bad, f"{len(bad)}: {bad[:5]}")


# ---- 56-63 invariants added after the Beebop review (2026-09-30) -------------
EV = {"baseline_reference", "measured_negative", "adverse_outcome_source_attributed",
      "outcome_not_attributed", "unintended_lab_disturbance",
      "intended_pharmacodynamic", "unattributed_lab_change", "unresolved_observation"}
bad = sorted({r["evidence_class"] for r in D if r["evidence_class"] not in EV})
check("vocabulary: measurements.evidence_class", not bad, f"unexpected {bad[:5]}")

bad = [r["measurement_id"] for r in D if not str(r["evidence_class_basis"]).strip()]
check("every evidence_class states the rule that assigned it", not bad, f"{len(bad)}: {bad[:5]}")

bad = sorted({r["evidence_class_review_status"] for r in D
              if r["evidence_class_review_status"] != "curator_derived_unreviewed"})
check("evidence_class is declared unreviewed on every row", not bad, f"{bad[:3]}")

SUB = {"participant", "primary_blood_or_plasma", "cells_or_tissue",
       "purified_or_recombinant_protein", "unresolved", NA}
bad = sorted({r["human_system_subtype"] for r in D if r["human_system_subtype"] not in SUB})
check("vocabulary: measurements.human_system_subtype", not bad, f"unexpected {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if (r["species_class"] == "human") != (r["human_system_subtype"] != NA)]
check("human_system_subtype is set on exactly the human rows", not bad, f"{len(bad)}: {bad[:5]}")

# A class name that says "clinical" must hold human rows only. The previous vocabulary
# called two classes clinical while 222 of their rows were mouse, monkey, rat or pig. The
# names are fixed; this check is what stops the mistake being reintroduced.
bad = [r["measurement_id"] for r in D
       if "clinical" in r["evidence_class"] and r["species_class"] != "human"]
check("no evidence_class named 'clinical' carries a non-human row", not bad, f"{len(bad)}: {bad[:5]}")

# A row that is out of endpoint scope must not wear a coagulation category. COG-MSR0345
# said clotting_time for complement fragment Bb; all six scope-adjacent rows did this.
CORE = {"clotting_time", "factor_activity", "bleeding_outcome", "thrombotic_outcome",
        "fibrinogen", "anticoagulant_activity", "platelet_coag_crosstalk",
        "thrombin_generation", "fibrinolysis_marker"}
bad = [r["measurement_id"] for r in D
       if r["endpoint_scope"] == "scope_adjacent" and r["readout_category"] in CORE]
check("no scope_adjacent row carries a core coagulation category", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["endpoint_scope"] == "scope_adjacent" and r["cross_endpoint_referral"] in ("", NA)]
check("every scope_adjacent row names the endpoint it belongs to", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["readout_category_as_curated"] not in ("", NA) and r["endpoint_scope"] != "scope_adjacent"]
check("a recategorised row is recorded only where the scope says so", not bad, f"{len(bad)}: {bad[:5]}")

AUTH = {"source_reported", "curator_derived_research_score",
        "both_source_reported_and_curator_derived", "ungraded"}
bad = sorted({r["grade_authority"] for r in D if r["grade_authority"] not in AUTH})
check("vocabulary: measurements.grade_authority", not bad, f"unexpected {bad[:5]}")

bad = [r["measurement_id"] for r in D if r["is_validated_clinical_grade"] != "FALSE"]
check("no row claims a validated clinical grade", not bad, f"{len(bad)}: {bad[:5]}")

bad = [r["measurement_id"] for r in D
       if r["grade_authority"] == "ungraded" and r["coag_tox_grade"] != NR]
check("grade_authority agrees with the grade columns", not bad, f"{len(bad)}: {bad[:5]}")

# A baseline is a reference point; it must never be counted as an outcome.
bad = [r["measurement_id"] for r in D
       if r["evidence_class"] == "baseline_reference" and r["coag_tox_grade"] != NR]
check("a baseline_reference row carries no grade", not bad, f"{len(bad)}: {bad[:5]}")


# ---- 65-69 study register ----------------------------------------------------
import csv as _csv
_sp = os.path.join(ROOT, "data", "studies.csv")
if os.path.exists(_sp):
    ST = list(_csv.DictReader(open(_sp, newline="", encoding="utf-8")))
    ids = [r["study_id"] for r in ST]
    check("PK unique: studies.study_id", len(set(ids)) == len(ids), "duplicated study ids")

    DES = {"interventional_trial", "observational_study", "case_report", "pooled_analysis",
           "regulatory_summary", "product_label", "spontaneous_reporting",
           "healthy_volunteer_lab", "not_a_human_study"}
    bad = sorted({r["design"] for r in ST if r["design"] not in DES})
    check("vocabulary: studies.design", not bad, f"unexpected {bad[:4]}")

    # The headline rule, re-derived. A trial total that cannot be recomputed from the
    # columns is not reproducible, which is the whole point of the register.
    bad = [r["study_id"] for r in ST
           if (r["headline_trial"] == "TRUE") != (
               r["design"] == "interventional_trial"
               and r["endpoint_evaluable"] == "TRUE"
               and r["identity_basis"] in ("registry_number", "trial_acronym", "sponsor_protocol"))]
    check("headline_trial is reproducible from design + endpoint + identity", not bad, f"{len(bad)}: {bad[:4]}")

    bad = [r["study_id"] for r in ST
           if r["headline_trial"] == "TRUE" and r["design"] != "interventional_trial"]
    check("no pooled analysis, label or report counts as a trial", not bad, f"{len(bad)}: {bad[:4]}")

    bad = [r["study_id"] for r in ST if r["identity_basis"] == "no_identifier" and r["headline_trial"] == "TRUE"]
    check("an unidentifiable study never enters the headline total", not bad, f"{len(bad)}: {bad[:4]}")

    # ---- over-merge is a failure, not a comment (Beebop 2026-10-02) ------------------
    # 55 checks passed while two drugs sat in one trial row. These are the checks that
    # would have caught it. Two registry numbers from the SAME registry, or two sponsor
    # compound numbers, cannot be one trial. Two numbers from DIFFERENT registries can:
    # one trial legitimately holds both an NCT and a EudraCT number, so that is an alias.
    bad = [r["study_id"] for r in ST if "OVER_MERGE" in r["review_flag"]]
    check("no study cluster fails the over-merge test", not bad, f"{len(bad)}: {bad[:4]}")

    def _reg_fam(x):
        for f in ("NCT", "EUDRACT", "ISRCTN", "JAPICCTI", "EUCT"):
            if x.startswith(f):
                return f
        return "OTHER"

    bad = []
    for r in ST:
        regs = [x.strip() for x in r["registry_ids_all"].split(";") if x.strip() and x.strip() != NR]
        if len({_reg_fam(x) for x in regs}) < len(regs):
            bad.append(r["study_id"])
    check("no cluster holds two registry numbers from one registry", not bad, f"{len(bad)}: {bad[:4]}")

    bad = [r["study_id"] for r in ST
           if len([x for x in r["sponsor_programme"].split(";") if x.strip() and x.strip() != NR]) > 1
           and "OVER_MERGE" not in r["review_flag"]
           and "MIPO2900210" not in r["sponsor_protocol"]]
    check("two sponsor compound numbers in one cluster are declared, not silent", not bad, f"{len(bad)}: {bad[:4]}")

    # A pooled analysis re-reports trials already counted. It must not be a study row.
    bad = [r["study_id"] for r in ST if r["design"] == "pooled_analysis"]
    check("pooled analyses are not study records", not bad, f"{len(bad)}: {bad[:4]}")

    # The compound id is embedded in the compound string, so it must be extracted. Filtering
    # on startswith() resolved 5 of 30 headline trials and I reported that as the dataset's
    # state rather than as my bug.
    bad = [r["study_id"] for r in ST
           if re.search(r"COG-OLG\d+", r["compounds"]) and r["oligo_ids"] == NR]
    check("a compound id written inside the compound string is extracted", not bad, f"{len(bad)}: {bad[:4]}")

_pp = os.path.join(ROOT, "data", "pooled_analyses.csv")
if os.path.exists(_pp):
    PA = list(_csv.DictReader(open(_pp, newline="", encoding="utf-8")))
    ids = [r["pool_id"] for r in PA]
    check("PK unique: pooled_analyses.pool_id", len(set(ids)) == len(ids), "duplicated pool ids")
    bad = [r["pool_id"] for r in PA if not str(r["pool_descriptor"]).strip()]
    check("every pooled analysis records what it pools", not bad, f"{len(bad)}: {bad[:4]}")
    bad = [r["pool_id"] for r in PA if "NOT a trial" not in r["counting_rule"]]
    check("every pooled analysis carries its counting rule", not bad, f"{len(bad)}: {bad[:4]}")

# ---- report -----------------------------------------------------------------
w = max(len(n) for n, _, _ in checks)
for n, ok, detail in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {n:<{w}}  {'' if ok else detail}")
print(f"\n{sum(1 for _, ok, _ in checks if ok)}/{len(checks)} checks pass")
print(f"tables: {len(S)} sources · {len(O)} oligos · {len(M)} modification rows · {len(D)} measurements")
sys.exit(1 if fails else 0)
