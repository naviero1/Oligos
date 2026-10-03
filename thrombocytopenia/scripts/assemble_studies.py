#!/usr/bin/env python3
"""Assemble data/studies.csv — the human evidence at TRIAL grain.

This is Beebop's Priority 1. The dataset holds 1,002 human clinical measurement
ROWS; this file says how many actual studies sit underneath them, and of those,
how many can carry a defensible platelet claim.

WHY A SINGLE "TRIAL COUNT" IS NOT PUBLISHED
  A completeness critic reviewing the resolved registry established that
  "how many human trials does this dataset contain?" has no single honest
  answer, and it is right. 52 records are typed `registered_trial`, but 17 of
  them carry no measurement rows at all -- they are trial-grain ANCHORS,
  identified so that pooled data can be attributed, not trials this dataset has
  data for. So this script publishes a LADDER of counts, each separately
  defined, and refuses to collapse it into one headline number.

THE NESTING PROBLEM, AND WHY `pool_memberships` IS MULTI-VALUED
  Pooled analyses contain trials that are ALSO recorded here individually. The
  resolution agents' `constituent_of` field was single-valued and overloaded --
  used both for "member of this pool" and "extension of this parent trial" --
  so wherever a trial fed two pools, one edge was silently dropped, and no edge
  type could cross between cluster files at all. Traversing it under-counted
  volanesorsen by four trials and inotersen by two.
  Here, `parent_study_id` carries the extension-of relation and
  `pool_memberships` carries every pool membership, semicolon separated, across
  files. The memberships in POOL_MEMBERSHIP below were each established by
  arithmetic agreement on arm sizes, not by name similarity; the evidence is
  recorded per edge and printed into the ledger.

Writes: data/studies.csv
        data/study_nesting_ledger.csv   every declared overlap, with its evidence
        data/study_counts.csv           the count ladder
"""
import csv, glob, json, os, re, collections

ENDPOINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ENDPOINT, "data")
STUD = os.path.join(ENDPOINT, "curation", "studies")

# ---------------------------------------------------------------------------
# Harmonised registry_id vocabulary. The seven agents wrote five different
# things for "no registry record exists", and NOT_REGISTERED was doing double
# duty for "registration is impossible for this unit type" and "registration
# was sought and provably absent" -- destroying a distinction the resolution
# work had taken care to preserve.
NOT_APPLICABLE = "NOT_APPLICABLE"      # pooled analysis / label summary: no registration possible
NOT_REGISTERED = "NOT_REGISTERED"      # a trial that provably carries no registration
TBD = "TBD"                            # not established either way
NON_TRIAL_UNITS = {"pooled_analysis", "label_summary", "observational_cohort",
                   "spontaneous_report_series"}

def harmonise_registry_id(raw, unit_type):
    s = (raw or "").strip()
    # Unit type is checked FIRST. A pooled analysis often lists its constituent
    # NCTs in this field as prose; extracting one of them as the pool's OWN
    # registry id made the custirsen meta-analysis claim NCT01188187, which the
    # SYNERGY trial record also legitimately holds, and the double-counting gate
    # correctly rejected the build.
    if unit_type in NON_TRIAL_UNITS:
        ncts = re.findall(r"\bNCT\d{8}\b", s)
        note = ("constituent registry ids named in the source: " + ", ".join(ncts)) if ncts else (s if len(s) > 40 else "")
        return NOT_APPLICABLE, note
    nct = re.search(r"\bNCT\d{8}\b", s)
    if nct:
        return nct.group(), ""
    eudract = re.search(r"\b\d{4}-\d{6}-\d{2}\b", s)
    if eudract and "eudract" in s.lower():
        return "EudraCT " + eudract.group(), ""
    prospero = re.search(r"\bCRD\d{11}\b", s)
    if prospero:
        return NOT_APPLICABLE, "PROSPERO " + prospero.group()
    if unit_type in NON_TRIAL_UNITS:
        return NOT_APPLICABLE, s if len(s) > 40 else ""
    if re.fullmatch(r"NOT[_ ]REGISTERED", s, re.I):
        return NOT_REGISTERED, ""
    if not s or re.fullmatch(r"TBD|NOT[_ ]APPLICABLE.*", s, re.I):
        return TBD, s if len(s) > 40 else ""
    return TBD, s

# ---------------------------------------------------------------------------
# Declared nesting. Each edge was established by exact or near-exact agreement
# on arm sizes between a pooled source's own table and an individually recorded
# trial -- never by compound-name similarity, which produced four false
# overlap claims in the agents' own notes.
POOL_MEMBERSHIP = [
    ("bepirovirsen-ISIS505358-CS1", "crooke2017-ISDB-2moe-integrated-analysis",
     "Crooke 2017 Table 1 ISIS 505358: 1 trial, 28 total, 21 ASO. This record: 28 randomised 3:1 "
     "active:placebo = 21 active / 7 placebo. Both columns match exactly."),
    ("ISIS546254-CS1", "crooke2017-ISDB-2moe-integrated-analysis",
     "Crooke 2017 Table 1 ISIS 546254: 1 trial, 49 total, 37 ASO. This record: SAD 12+4, MAD 25+8 "
     "= 37 active / 12 placebo / 49 total. Both columns match exactly."),
    ("volanesorsen-CS2", "crooke2017-ISDB-2moe-integrated-analysis",
     "Crooke 2017 Table 1 ISIS 304801: 3 trials, 136 total, 99 ASO. CS1 (25+8) + CS4 (10+5) + CS2 "
     "(64+24) = 136 total and 99 active, reproducing both columns exactly. NOTE this also "
     "DISPROVES the assumption that Crooke 2017 pools APPROACH/COMPASS/CS7: 136 subjects cannot "
     "contain CS6 (67) and CS16 (114)."),
    ("inotersen-CS1-phase1-healthy-volunteers", "crooke2017-ISDB-2moe-integrated-analysis",
     "Crooke 2017 Table 1 ISIS 420915: 1 trial, 65 total, 51 ASO. With only one ISIS 420915 trial "
     "in the database and NEURO-TTR enrolling 173, the pooled trial CANNOT be NEURO-TTR; it is the "
     "phase 1 healthy-volunteer study."),
    ("ISIS404173-CS2", "crooke2017-ISDB-2moe-integrated-analysis",
     "Crooke 2017 Table 1 ISIS 404173: 2 trials, 140 total, 98 ASO. This record (92 enrolled / 62 "
     "active) is one of the two. Membership certain, arithmetic not exact because the second "
     "trial is unidentified."),
    ("isis104838-CS7-RA-phase2", "crooke2017-ISDB-2moe-integrated-analysis",
     "Crooke 2017 Table 1 ISIS 104838: 5 trials, 281 total, 212 ASO. This record is one member."),
    ("ISIS104838-phase1-TNFalpha", "crooke2017-ISDB-2moe-integrated-analysis",
     "Second ISIS 104838 member of the same 5-trial block. Cross-cluster duplicate that neither "
     "resolution agent flagged."),
    ("ISIS757456-CS1", "crooke2019-galnac3-integrated-hv",
     "Crooke 2019 Table 1, 7th ASO (ISIS 757456 AGT-L): 12 placebo / 29 active / 41 total. This "
     "record: SAD 29 active + 12 placebo across 5 cohorts = 41. Exact match on all three numbers."),
]
# Trials enumerated inside the Vermeer 2026 meta-analysis AND recorded here
# individually, each matched on treated/placebo arm sizes.
VERMEER = "vermeer2026-aso-adverse-event-meta"
for key, ev in [
    ("inotersen-CS2-NEURO-TTR", "Vermeer Table 1 study 8 (ref 28, Benson 2018): 112 treated / 60 placebo"),
    ("volanesorsen-CS6", "Vermeer Table 1 study 98 (ref 118, Witztum 2019): 33 / 33"),
    ("volanesorsen-CS16", "Vermeer Table 1 study 35 (ref 55, Gouni-Berthold): 75 / 38"),
    ("volanesorsen-CS2", "Vermeer Table 1 study 30 (ref 50, Gaudet): 41 / 16"),
    ("nusinersen-CS3B-ENDEAR", "Vermeer Table 1 study 26 (ref 46, Finkel 2017 ENDEAR): 80 / 41"),
    ("nusinersen-CS4-CHERISH", "Vermeer Table 1 study 55 (ref 75, Mercuri 2018 CHERISH): 84 / 42"),
    ("tofersen-233AS101-VALOR", "Vermeer Table 1 study 56 (ref 76, Miller 2022): 38 / 12"),
    ("eplontersen-ION682884-CS1", "Vermeer Table 1 study 90 (ref 110, Viney): 39 active / 6 pooled placebo"),
    ("ISIS757456-CS1", "Vermeer Table 1 study 59 (ref 79, Morgan abstract): placebo 16 = CS1 12+4"),
    ("mipomersen-301012-CS5-HoFH", "Vermeer Table 1 study 68 (ref 88, Raal 2010): 34/17 = 51"),
    ("mipomersen-MIPO3500108-severe-HC", "Vermeer Table 1 study 52 (ref 72, McGowan 2012): 39/19 = 58"),
    ("mipomersen-301012-CS7-HeFH-CAD", "Vermeer Table 1 study 81 (ref 101, Stein 2012): 83/41 = 124"),
    ("mipomersen-301012-CS12-high-risk-HC", "Vermeer Table 1 study 87 (ref 107, Thomas 2013): 105/52 = 157 vs 158 registered"),
    ("mipomersen-MIPO3801011-FOCUS-FH-1year", "Vermeer Table 1 study 71 (ref 91, Reeskamp): 207/103 = 310 vs 309 registered — independent corroboration of an identification otherwise resting on a conference abstract"),
    ("mipomersen-301012-CS6-OLE", "Vermeer Table 1 study 78 (ref 98, Santos, open-label): 141 vs 143/144"),
]:
    POOL_MEMBERSHIP.append((key, VERMEER, ev))

# ---------------------------------------------------------------------------
# Evaluability downgrades. `platelet_endpoint_evaluable = yes` must mean the
# endpoint was ASSESSED under a defined exposure and observation window. These
# records asserted yes on a basis that does not demonstrate it.
DOWNGRADE = {
    "ISIS757456-CS2": ("no", "Basis is one Discussion sentence ('no evidence of ... decreases in "
        "platelet count') with no value, threshold, denominator or sampling schedule. The record's "
        "own notes concede no platelet numbers are tabulated anywhere in the paper or supplement. "
        "This is the fabricated-negative pattern METHODOLOGY.md forbids; ISIS757456-CS1 was typed "
        "'partial' on the SAME sentence from the same paper."),
    "ISIS757456-CS3": ("no", "Same single Discussion sentence as CS2, same absence of any platelet "
        "value, threshold or denominator."),
    "fesomersen-ION957943-CS1": ("partial", "Basis quoted from US 2021/0355497 A1 Examples 4-5, "
        "which the record's own verification_locus states could not be retrieved. The quotation is "
        "carried from the curated input row, not read from a source."),
    "imetelstat-pool-ER-all-studies": ("partial", "Justified as 'assessed by construction'. An "
        "exposure-response model with n_enrolled and n_analyzed_platelet both TBD is not evidence "
        "that the endpoint was ascertained in a defined population."),
    "isis104838-CS7-RA-phase2": ("partial", "Basis is Crooke 2017 Figure 1, a graph. All four "
        "readout values are TBD and the paper prints no numeric platelet value or group n."),
    "ISIS3521-yuen1999-phase1": ("partial", "Grade derives from the words 'dose-limiting toxicity', "
        "not from a measurement; no platelet value exists and n_analyzed_platelet is the treated "
        "denominator relabelled."),
    "bepirovirsen-BClear-209668": ("partial", "Sole source is one sentence inside the Vermeer "
        "meta-analysis citing its own reference 158; Yuen 2022 was never fetched. The record admits "
        "the 229 denominator could not be placed."),
    "SPC5001-901-FIH": ("no", "The record's own notes disprove its row: tracing the review-table "
        "claim to van Poelgeest 2015 showed the trial never reports a platelet result and never "
        "mentions platelets."),
}

# Units where a platelet CHANGE is the intended pharmacology or the treated
# disease, so a grade must never be harvested as oligonucleotide toxicity.
# Aligns with the scientist package control classes
# THERAPEUTIC_CORRECTION_OR_PRESERVATION and SUPPORT_ONLY_INTENDED_COAG.
INTENDED_PHARMACOLOGY = {
    "ARC1779-010b-vwd2b-72h": "Platelets ROSE 40 -> 146 x10^9/L. That is ARC1779's intended effect "
        "in type 2B von Willebrand disease, not a toxicity signal.",
    "ARC1779-1779-06-001-phase1-HV": "Anti-vWF aptamer, outside the antisense class hypothesis.",
    "imetelstat-CP14B015": "Essential thrombocythaemia / polycythaemia vera — a THROMBOCYTOSIS "
        "population in which platelet reduction is the therapeutic goal.",
    "fesomersen-ION957943-CS1": "FXI-targeting antithrombotic; anticoagulant effect is intended.",
}

ROW_DISAVOWED = {"SPC5001-901-FIH": "TMSR1750"}

COLS = ["study_id", "study_key", "cluster", "registry_id", "registry_id_note",
        "sponsor_protocol_id", "study_name", "evidence_unit_type", "design", "phase",
        "compound", "oligo_id", "indication", "population",
        "n_enrolled_numeric", "n_enrolled_note",
        "n_analyzed_platelet_numeric", "n_analyzed_platelet_note",
        "route", "dose_regimen", "duration",
        "platelet_endpoint_evaluable", "platelet_endpoint_evaluable_original",
        "evaluability_adjustment_reason", "platelet_endpoint_basis",
        "parent_study_id", "pool_memberships", "constituents_identifiable",
        "intended_pharmacology", "intended_pharmacology_reason",
        "disavowed_measurement_ids", "n_measurement_rows", "measurement_ids",
        "source_uids", "eligibility_decision", "eligibility_reason",
        "verification_locus", "confidence", "notes"]


def numeric(v):
    """Pull a leading integer out of a prose denominator; '' when ambiguous.
    Six of seven agents wrote free prose here (one field runs 802 characters),
    so no numeric column could be extracted from the registry as delivered."""
    s = str(v or "").strip()
    if not s or s.upper().startswith("TBD"):
        return "", s
    m = re.match(r"^\s*([\d,]{1,7})\b", s)
    if not m:
        return "", s
    n = m.group(1).replace(",", "")
    return n, ("" if s == m.group(1) else s)


def main():
    members = collections.defaultdict(list)
    evidence = {}
    for key, pool, ev in POOL_MEMBERSHIP:
        members[key].append(pool)
        evidence[(key, pool)] = ev

    rows, seen_keys, nesting = [], {}, []
    n = 0
    for path in sorted(glob.glob(os.path.join(STUD, "registry_*.json"))):
        cluster = os.path.basename(path)[len("registry_"):-len(".json")]
        d = json.load(open(path))
        for s in d.get("studies", []):
            n += 1
            key = (s.get("study_key") or f"unkeyed-{n}").strip()
            ut = (s.get("evidence_unit_type") or "").strip()
            rid, rnote = harmonise_registry_id(s.get("registry_id"), ut)
            ev_orig = (s.get("platelet_endpoint_evaluable") or "").strip()
            ev_new, reason = DOWNGRADE.get(key, (ev_orig, ""))
            mids = [m for m in (s.get("measurement_ids") or []) if m]
            ne, nen = numeric(s.get("n_enrolled"))
            na, nan = numeric(s.get("n_analyzed_platelet"))
            pools = members.get(key, [])
            for p in pools:
                nesting.append({"study_key": key, "nested_in": p,
                                "relation": "member_of_pooled_analysis",
                                "evidence": evidence[(key, p)]})
            parent = (s.get("constituent_of") or "").strip()
            # constituent_of was overloaded; keep it as parent ONLY where it is
            # not itself a pool this record is declared a member of.
            if parent in pools:
                parent = ""
            rows.append({
                "study_id": f"THR-STU-{n:03d}", "study_key": key, "cluster": cluster,
                "registry_id": rid, "registry_id_note": rnote,
                "sponsor_protocol_id": s.get("sponsor_protocol_id", ""),
                "study_name": s.get("study_name", ""), "evidence_unit_type": ut,
                "design": s.get("design", ""), "phase": s.get("phase", ""),
                "compound": s.get("compound", ""), "oligo_id": s.get("oligo_id", ""),
                "indication": s.get("indication", ""), "population": s.get("population", ""),
                "n_enrolled_numeric": ne, "n_enrolled_note": nen,
                "n_analyzed_platelet_numeric": na, "n_analyzed_platelet_note": nan,
                "route": s.get("route", ""), "dose_regimen": s.get("dose_regimen", ""),
                "duration": s.get("duration", ""),
                "platelet_endpoint_evaluable": ev_new,
                "platelet_endpoint_evaluable_original": ev_orig,
                "evaluability_adjustment_reason": reason,
                "platelet_endpoint_basis": s.get("platelet_endpoint_basis", ""),
                "parent_study_id": parent, "pool_memberships": ";".join(pools),
                "constituents_identifiable": s.get("constituents_identifiable", ""),
                "intended_pharmacology": "yes" if key in INTENDED_PHARMACOLOGY else "no",
                "intended_pharmacology_reason": INTENDED_PHARMACOLOGY.get(key, ""),
                "disavowed_measurement_ids": ROW_DISAVOWED.get(key, ""),
                "n_measurement_rows": len(mids), "measurement_ids": ";".join(mids),
                "source_uids": ";".join(s.get("source_uids") or []),
                "eligibility_decision": "included",
                "eligibility_reason": "", "verification_locus": s.get("verification_locus", ""),
                "confidence": s.get("confidence", ""), "notes": s.get("notes", "")})
            seen_keys.setdefault(key, []).append(rows[-1]["study_id"])

    # duplicate study_key across files => same unit resolved twice
    for key, ids in seen_keys.items():
        if len(ids) > 1:
            for r in rows:
                if r["study_key"] == key and r["study_id"] != ids[0]:
                    r["eligibility_decision"] = "excluded_duplicate"
                    r["eligibility_reason"] = f"same study_key already recorded as {ids[0]}"

    with open(os.path.join(DATA, "studies.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(DATA, "study_nesting_ledger.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["study_key", "nested_in", "relation", "evidence"])
        w.writeheader(); w.writerows(nesting)

    # ---- the count ladder ---------------------------------------------------
    inc = [r for r in rows if r["eligibility_decision"] == "included"]
    trials = [r for r in inc if r["evidence_unit_type"] in ("registered_trial", "unregistered_trial")]
    reg = [r for r in trials if r["registry_id"].startswith(("NCT", "EudraCT"))]
    with_rows = [r for r in trials if r["n_measurement_rows"] > 0]
    evaluable = [r for r in with_rows if r["platelet_endpoint_evaluable"] == "yes"]
    tox = [r for r in evaluable if r["intended_pharmacology"] == "no"]
    pooled = [r for r in inc if r["evidence_unit_type"] == "pooled_analysis"]
    nested = {e["study_key"] for e in nesting}
    ladder = [
        ("evidence units resolved", len(rows),
         "every unit the 1,002 human clinical rows resolve to, of any type"),
        ("... TYPED as a trial", len(trials),
         "registered_trial + unregistered_trial. A TYPE, not a qualification. These are NOT "
         "qualified trials and must never be reported as such."),
        ("... with a verified registry identifier", len(reg), "NCT or EudraCT confirmed against the registry"),
        ("... WITH MEASUREMENTS", len(with_rows),
         "carrying at least one measurement row. THE REST ARE TRIAL-GRAIN ANCHORS, not trials "
         "this dataset holds data for."),
        ("... platelet endpoint evaluable", len(evaluable),
         "endpoint demonstrably assessed under a defined exposure and observation window"),
        ("... classified as a platelet-toxicity claim", len(tox),
         "endpoint evaluable AND not intended pharmacology. A CURATOR CLASSIFICATION, superseded "
         "by the audited figure below."),
        ("pooled analyses (NOT trials)", len(pooled), "integrated analyses, meta-analyses, label pools"),
        ("trials declared nested inside a pooled analysis", len(nested),
         "these subjects are counted inside a pool as well; NEVER sum a pool with its members"),
        ("unique compounds across included units", len({r["oligo_id"] for r in inc if r["oligo_id"]}), ""),
        ("participants", 0,
         "NOT SUMMABLE. Denominators overlap across nested pools and strata; summing them "
         "double-counts. Use a single stratum's denominator and say which."),
    ]
    # The audited rung belongs IN the ladder: a reader must not have to open a
    # second file to learn that the curator classification was superseded.
    apath = os.path.join(DATA, "toxicity_denominator_audit.csv")
    if os.path.exists(apath):
        with open(apath, newline="", encoding="utf-8") as af:
            AUD = list(csv.DictReader(af))
        n_aud = sum(1 for r in AUD if r.get("audit_verdict") == "SURVIVES_ALL_FOUR")
        ladder.insert(6, ("... PASSING THIS ENDPOINT'S FOUR-TEST AUDIT", n_aud,
                          "monitoring QUOTED (not absence reported) + dose and duration stated + "
                          "platelet-specific at-risk denominator + retrievable locus. THIS IS THE "
                          "FIGURE TO QUOTE. It is this endpoint's own audit, NOT qualification "
                          "against the project sign-off gates, which is the scientist's "
                          "determination and has not been made."))

    with open(os.path.join(DATA, "study_counts.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["measure", "n", "definition"]); w.writerows(ladder)

    print(f"studies.csv: {len(rows)} units ({len(inc)} included)")
    for a, b, c in ladder:
        print(f"  {b:>5}  {a}")
    print(f"\nnesting ledger: {len(nesting)} declared overlaps covering {len(nested)} trials")
    print(f"evaluability downgraded: {sum(1 for r in rows if r['evaluability_adjustment_reason'])}")
    print(f"intended-pharmacology flagged: {sum(1 for r in rows if r['intended_pharmacology']=='yes')}")
    unmatched = [k for k in members if k not in seen_keys]
    if unmatched:
        print(f"\n! declared nesting for {len(unmatched)} study_key(s) not found in the registry:")
        for k in unmatched: print(f"    {k}")


if __name__ == "__main__":
    main()
