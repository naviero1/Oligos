#!/usr/bin/env python3
"""Build the Phase 2 dataset release workbook from the canonical CSVs.

    python3 toxicity/coagulopathy/scripts/build_release_xlsx.py

The Challenge asks for the dataset as "a data dictionary and schema documenting all
metadata, and access to the raw data ... by including a data file in Excel (or similar
format)". This produces that single file. The CSVs in data/ remain canonical; this
workbook is generated from them and is never hand-edited.

Summary figures are written as VALUES, not formulas. The sibling CNS release used live
COUNTA/COUNTIF formulas, which read back as empty cells in any tool that does not
recalculate on open (pandas.read_excel among them). Values avoid that trap; the numbers are
recomputed here on every build, so they cannot drift from the data.
"""
import csv, os, sys
from collections import Counter

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("openpyxl is required:  pip install openpyxl")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "OligoTox-Coagulopathy_Dataset.xlsx")

HDR = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="1F3864")
TITLE = Font(bold=True, size=13)


def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sheet(wb, name, rows, freeze="A2"):
    ws = wb.create_sheet(name)
    if not rows:
        return ws
    cols = list(rows[0].keys())
    ws.append(cols)
    for c in range(1, len(cols) + 1):
        ws.cell(1, c).font = HDR
        ws.cell(1, c).fill = FILL
    for r in rows:
        ws.append([r.get(c, "") for c in cols])
    for i, c in enumerate(cols, 1):
        w = max(len(c), *(len(str(r.get(c, ""))[:60]) for r in rows[:400])) + 2
        ws.column_dimensions[get_column_letter(i)].width = min(w, 60)
    ws.freeze_panes = freeze
    ws.auto_filter.ref = ws.dimensions
    return ws


def _runs(pairs):
    """Compact a per-position attribute into runs: [(1,'2\'-MOE'),...] -> "1-5:2'-MOE; 6-15:DNA"."""
    if not pairs:
        return "NOT_REPORTED"
    out, start, prev_pos, prev_val = [], pairs[0][0], pairs[0][0], pairs[0][1]
    for pos, val in pairs[1:]:
        if val != prev_val or pos != prev_pos + 1:
            out.append(f"{start}-{prev_pos}:{prev_val}" if start != prev_pos else f"{start}:{prev_val}")
            start, prev_val = pos, val
        prev_pos = pos
    out.append(f"{start}-{prev_pos}:{prev_val}" if start != prev_pos else f"{start}:{prev_val}")
    return "; ".join(out)


def sequence_status(o):
    """Why a compound has no sequence -- so a gap is actionable rather than blank.

    'published' means this release carries it. The other four say what kind of gap it is,
    which is the difference between a compound whose sequence CANNOT exist as one string
    and one that simply has not been recovered yet."""
    if o["sequence_base"] not in ("NOT_REPORTED", "NOT_APPLICABLE", ""):
        return "published"
    if o["oligo_class"] == "polydisperse_ssDNA":
        return "not_applicable_polydisperse_mixture"
    if o["modality"] == "double_stranded_siRNA" or "duplex" in str(o["sequence_note"]).lower() \
       or "sense" in str(o["sequence_note"]).lower():
        return "not_applicable_duplex_two_strands"
    if "pprov" in str(o["max_phase"]) or "arket" in str(o["max_phase"]):
        return "recoverable_from_WHO_INN_nomenclature"
    return "not_published_by_source"

def modification_maps(M):
    """Per-oligo compact chemistry maps, built from the per-position table."""
    by = {}
    for r in M:
        by.setdefault(r["oligo_id"], []).append(r)
    out = {}
    for oid, rows in by.items():
        rows = sorted(rows, key=lambda r: int(r["position"]) if str(r["position"]).isdigit() else 0)
        out[oid] = {
            "sugar_map": _runs([(int(r["position"]), r["sugar_mod"]) for r in rows if str(r["position"]).isdigit()]),
            "backbone_map": _runs([(int(r["position"]), r["backbone_linkage_3p"]) for r in rows if str(r["position"]).isdigit()]),
            "n_positions": len(rows),
            "per_position": " ".join(f"{r['position']}{r['nucleobase']}({r['sugar_mod']}/{r['backbone_linkage_3p']})" for r in rows),
        }
    return out


def toxicity_rollup(D):
    """Per-oligo toxicity summary. worst_grade is the maximum ASSIGNED grade; an oligo whose
    rows are all ungraded gets NOT_REPORTED, never 0 -- absence of a grade is not safety."""
    by = {}
    for r in D:
        by.setdefault(r["oligo_id"], []).append(r)
    out = {}
    for oid, rows in by.items():
        gr = [int(r["coag_tox_grade"]) for r in rows if r["coag_tox_grade"] in ("0", "1", "2", "3")]
        sev = [r["severity_stated_by_source"] for r in rows
               if r["severity_stated_by_source"] not in ("NOT_REPORTED", "NOT_APPLICABLE", "")]
        sg = [r["source_stated_grade"] for r in rows if r["source_stated_grade"] != "NOT_APPLICABLE"]
        out[oid] = {
            "worst_coag_tox_grade": str(max(gr)) if gr else "NOT_REPORTED",
            "grade_distribution_0_1_2_3": "/".join(str(sum(1 for g in gr if g == k)) for k in range(4)) if gr else "NOT_REPORTED",
            "n_graded_rows": len(gr),
            "n_rows_flagged_grade_caveat": sum(1 for r in rows if r["grade_caveat"] == "within_reference_range_resolution"),
            "max_source_stated_grade": max(sg) if sg else "NOT_APPLICABLE",
            "severity_in_source_words": (sev[0][:300] if sev else "NOT_REPORTED"),
            "n_human_rows": sum(1 for r in rows if r["species_class"] == "human"),
            "n_animal_rows": sum(1 for r in rows if r["species_class"] == "animal"),
            "on_target_rows": sum(1 for r in rows if r["on_target_effect"] == "TRUE"),
            "unintended_toxicity_rows": sum(1 for r in rows if r["unintended_toxicity"] == "TRUE"),
        }
    return out


def main():
    S, O, M, D = load("sources.csv"), load("oligos.csv"), load("modifications.csv"), load("measurements.csv")
    ST = load("studies.csv") if os.path.exists(os.path.join(DATA, "studies.csv")) else []
    trials = [r for r in ST if r.get("design") == "interventional_trial"
              and str(r.get("endpoint_evaluable", "")).upper() == "TRUE"]
    # A trial total is quoted only when it can be reproduced from verified study identifiers.
    TRIALS_LABEL = len(trials) if ST else "UNESTABLISHED - no study register built yet"
    wb = Workbook()
    wb.remove(wb.active)

    # ---- README ----------------------------------------------------------
    ws = wb.create_sheet("README")
    NR = "NOT_REPORTED"
    lines = [
        ("OligoTox-Coagulopathy", TITLE),
        ("Coagulation toxicity of oligonucleotide therapeutics. NIH/NCATS Oligonucleotide Toxicity Open Data Challenge, Phase 2.", None),
        ("", None),
        ("Licence: Creative Commons Attribution 4.0 (CC BY 4.0) for the curated tables.", None),
        ("Underlying third-party full texts are referenced, not redistributed; per-row terms are in the 'redistribution' column.", None),
        ("", None),
        ("SHEETS", TITLE),
        ("Summary            headline counts, computed from the data sheets at build time", None),
        ("data_dictionary    every column in every table, with its definition", None),
        ("sources            the provenance registry - one row per source document", None),
        ("oligos             one row per oligonucleotide - the predictor variables", None),
        ("measurements       one row per measured outcome - the response variables", None),
        ("modifications      one row per NUCLEOTIDE POSITION - the per-position chemistry", None),
        ("", None),
        ("HOW THE TABLES JOIN", TITLE),
        ("measurements.oligo_id  -> oligos.oligo_id      (many measurements per oligonucleotide)", None),
        ("measurements.source_id -> sources.source_id", None),
        ("modifications.oligo_id -> oligos.oligo_id      (one row per position, 5' to 3')", None),
        ("", None),
        ("MISSING VALUES - READ THIS BEFORE ANALYSING", TITLE),
        ("NOT_REPORTED    the source does not report this value. It has NOT been estimated, imputed or filled from background knowledge.", None),
        ("NOT_APPLICABLE  the field has no meaning for this row (a dose for an in-vitro spike-in; a 5'->3' string for a duplex or a polydisperse mixture).", None),
        ("Cells are never blank and never zero-as-missing.", None),
        ("", None),
        ("TWO AXES, NOT ONE - THE MOST IMPORTANT THING ON THIS PAGE", TITLE),
        ("Most rows here are ON-TARGET anticoagulant pharmacology, not toxicity: the compounds with published clotting", None),
        ("numbers are largely the ones designed to change clotting. on_target_effect and unintended_toxicity are separate", None),
        ("flags and BOTH may be true on one row. A model trained across them without the flags learns that anticoagulants", None),
        ("prolong aPTT - true, circular, and useless for safety prediction.", None),
        ("", None),
        ("HUMAN VERSUS ANIMAL", TITLE),
        ("species_class (human / animal / not_determined) and human_system carry this distinction, NOT study_type.", None),
        ("A purified-protein assay counts as a human system when the proteins are human; species_class_basis records how", None),
        ("each row was classified.", None),
        ("", None),
        ("GRADES ARE PROVISIONAL", TITLE),
        ("coag_tox_grade is assigned mechanically from a control-referenced ratio by CTCAE v5.0 cut-offs, and only for the", None),
        ("readouts CTCAE defines. CTCAE grades against the upper limit of normal; these sources publish a control mean, so", None),
        ("grades resting on a ratio of 1.0-1.2x carry grade_caveat = within_reference_range_resolution. FILTER ON THAT", None),
        ("BEFORE TREATING GRADE 1 AS A FINDING. No grade has had subject-matter review.", None),
    ]
    for text, font in lines:
        ws.append([text])
        if font:
            ws.cell(ws.max_row, 1).font = font
    ws.column_dimensions["A"].width = 130

    # ---- Summary ---------------------------------------------------------
    ws = wb.create_sheet("Summary")
    def block(title, pairs):
        ws.append([title]); ws.cell(ws.max_row, 1).font = TITLE
        for k, v in pairs:
            ws.append([k, v])
        ws.append([])
    seq = [r for r in O if r["sequence_base"] not in (NR, "NOT_APPLICABLE", "")]
    gr = Counter(r["coag_tox_grade"] for r in D)
    sc = Counter(r["species_class"] for r in D)
    st = Counter(r["study_type"] for r in D)
    rc = Counter(r["readout_category"] for r in D)
    block("OligoTox-Coagulopathy - release summary", [("Every figure below is computed from the data sheets at build time.", "")])
    block("Counts", [("Oligonucleotides", len(O)), ("Coagulation measurements", len(D)),
                     ("Per-position modification records", len(M)),
                     ("Oligonucleotides with per-position chemistry", len({r["oligo_id"] for r in M})),
                     ("Distinct sources", len(S))])
    block("Coverage", [("Oligonucleotides with a published sequence", len(seq)),
                       ("Oligonucleotides with a reported purity VALUE", sum(1 for r in O if r["purity_pct"] not in (NR, "NOT_APPLICABLE", ""))),
                       ("Oligonucleotides with a named purity METHOD", sum(1 for r in O if r["purity_method"] not in (NR, "NOT_APPLICABLE", ""))),
                       ("Oligonucleotides with identity confirmation recorded", sum(1 for r in O if r["identity_confirmation"] not in (NR, "NOT_APPLICABLE", "")))])
    # Phase 2: datasets "able to extrapolate data between in vitro human systems and animal
    # data are of particular interest". That is a narrower thing than having any human row
    # and any animal row for the same compound, so the three forms are reported separately.
    block("HUMAN-TO-ANIMAL EXTRAPOLATION (Phase 2: 'of particular interest')", [
        ("Compounds with the SAME readout in a human in vitro system AND an animal",
         sum(1 for r in O if r["bridge_shared_readout_categories"] not in (NR, "NOT_APPLICABLE", ""))),
        ("Compounds with human in vitro data AND animal data",
         sum(1 for r in O if r["invitro_human_animal_bridge"] == "TRUE")),
        ("Compounds with participant data AND animal data",
         sum(1 for r in O if r["participant_animal_bridge"] == "TRUE")),
        ("See sheet", "bridge")])
    # Phase 2 requires the executive summary to state the controls included.
    kc = Counter(r["control_class"] for r in D)
    block("CONTROLS (Phase 2 requires these to be stated)", [
        ("Sequence-matched negative control (scrambled / reverse complement)", kc.get("sequence_control", 0)),
        ("Pharmacological positive control (heparin, enoxaparin, bivalirudin, warfarin, protamine)", kc.get("pharmacological_positive_control", 0)),
        ("Placebo", kc.get("placebo", 0)),
        ("Vehicle or buffer", kc.get("vehicle_or_buffer", 0)),
        ("Untreated or pre-dose", kc.get("untreated_or_predose", 0)),
        ("Active comparator drug", kc.get("active_comparator", 0)),
        ("Other described control", kc.get("other_described_control", 0)),
        ("No control described", kc.get("no_control_described", 0)),
        ("NOTE", "vehicle and placebo are NOT sequence controls: they do not separate a "
                 "sequence effect from a chemistry or formulation effect"),
        ("Compounds included as endpoint NEGATIVE CONTROLS",
         sum(1 for r in S if "NEGATIVE CONTROL" in str(r["citation"]).upper()))])
    block("HUMAN EVIDENCE (the primary evidence; see the human_* sheets)", [
        ("Human measurements", sc.get("human", 0)),
        ("  of which participants in clinical studies", sum(1 for r in D if r["human_system_subtype"] == "participant")),
        ("  of which primary human blood or plasma", sum(1 for r in D if r["human_system_subtype"] == "primary_blood_or_plasma")),
        ("  of which human cells or tissue", sum(1 for r in D if r["human_system_subtype"] == "cells_or_tissue")),
        ("  of which purified or recombinant human protein", sum(1 for r in D if r["human_system_subtype"] == "purified_or_recombinant_protein")),
        ("  of which unresolved human system", sum(1 for r in D if r["human_system_subtype"] == "unresolved")),
        ("Human clinical trials (verified, deduplicated)", TRIALS_LABEL),
        ("  clinical rows linked to exactly one of those trials",
         f'{sum(1 for r in D if str(r["study_id"]).startswith("COG-STU"))} of '
         f'{sum(1 for r in D if r["study_type"] == "clinical")}'),
        ("  clinical rows whose trial could not be resolved (candidate count in study_id_basis)",
         sum(1 for r in D if str(r["study_id_basis"]).startswith("ambiguous_"))),
    ])
    block("SUPPORTING ANIMAL EVIDENCE (appendix; excluded from every human total)", [
        ("Animal measurements", sc.get("animal", 0)),
        ("See sheet", "animal_appendix"),
    ])
    block("UNRESOLVED ORIGIN (neither human nor animal until a source says)", [
        ("Measurements", sc.get("not_determined", 0)),
    ])
    block("What kind of observation each row is (evidence_class)",
          [(k.replace("_", " "), v) for k, v in Counter(r["evidence_class"] for r in D).most_common()])
    block("Study type", [(k, v) for k, v in st.most_common()])
    block("Measurements in a human or human-derived system", [("human_system = TRUE", sum(1 for r in D if r["human_system"] == "TRUE"))])
    block("Readout category", [(k, v) for k, v in rc.most_common()])
    block("Severity grade (provisional)", [
        ("grade 0 - no coagulation signal", gr.get("0", 0)),
        ("grade 1 - mild", gr.get("1", 0)),
        ("grade 2 - moderate", gr.get("2", 0)),
        ("grade 3 - severe", gr.get("3", 0)),
        ("ungraded (no published criterion applies; reason in grade_basis)", gr.get(NR, 0)),
        ("of the graded rows, flagged within_reference_range_resolution", sum(1 for r in D if r["grade_caveat"] == "within_reference_range_resolution"))])
    block("Axis", [("on-target pharmacology only", sum(1 for r in D if r["on_target_effect"] == "TRUE" and r["unintended_toxicity"] == "FALSE")),
                   ("unintended toxicity only", sum(1 for r in D if r["on_target_effect"] == "FALSE" and r["unintended_toxicity"] == "TRUE")),
                   ("both", sum(1 for r in D if r["on_target_effect"] == "TRUE" and r["unintended_toxicity"] == "TRUE")),
                   ("neither (context rows)", sum(1 for r in D if r["on_target_effect"] == "FALSE" and r["unintended_toxicity"] == "FALSE"))])
    hum_rows = [r for r in D if r["species_class"] == "human"]
    hum_oligos = {r["oligo_id"] for r in hum_rows}
    block("The human subset (see the human_measurements sheet)", [
        ("Human measurements", len(hum_rows)),
        ("Compounds measured in humans", len(hum_oligos)),
        ("…of which a published sequence is held", sum(1 for i in hum_oligos
            if next(r for r in O if r["oligo_id"] == i)["sequence_base"] not in (NR, "NOT_APPLICABLE", ""))),
        ("…of which per-position chemistry is held", len(hum_oligos & {r["oligo_id"] for r in M})),
        ("Human rows carrying a sequence", sum(1 for r in hum_rows
            if next(o for o in O if o["oligo_id"] == r["oligo_id"])["sequence_base"] not in (NR, "NOT_APPLICABLE", ""))),
        ("Human rows carrying an assigned grade", sum(1 for r in hum_rows if r["coag_tox_grade"] != NR)),
    ])
    block("Redistribution", [(k, v) for k, v in Counter(r["redistribution"] for r in D).most_common()])
    ws.column_dimensions["A"].width = 66
    ws.column_dimensions["B"].width = 16

    # ---- data_dictionary -------------------------------------------------
    dd = []
    _reg = list(csv.DictReader(open(os.path.join(ROOT, "data", "studies.csv"), newline="", encoding="utf-8"))) if ST else []
    _poolp = os.path.join(ROOT, "data", "pooled_analyses.csv")
    _pool = list(csv.DictReader(open(_poolp, newline="", encoding="utf-8"))) if os.path.exists(_poolp) else []
    _audp = os.path.join(ROOT, "data", "attribution_audit.csv")
    _aud = list(csv.DictReader(open(_audp, newline="", encoding="utf-8"))) if os.path.exists(_audp) else []
    for tbl, rows in (("sources", S), ("oligos", O), ("measurements", D), ("modifications", M),
                      ("studies", _reg), ("pooled_analyses", _pool), ("attribution_audit", _aud)):
        for c in (rows[0].keys() if rows else []):
            dd.append({"table": tbl, "column": c, "definition": DEFS.get((tbl, c), DEFS.get(("*", c), "see schema.md"))})
    # Phase 2 requires "a data dictionary and schema documenting all metadata". A column with
    # no definition is a gap in a required deliverable, so the build refuses to produce one.
    undoc = [f'{d["table"]}.{d["column"]}' for d in dd if d["definition"] == "see schema.md"]
    if undoc:
        sys.exit(f"  data_dictionary: {len(undoc)} columns have no definition: {undoc[:12]}")
    sheet(wb, "data_dictionary", dd)

    sheet(wb, "sources", S)
    sheet(wb, "oligos", O)
    sheet(wb, "measurements", D)
    sheet(wb, "modifications", M)


    # ---- human_measurements ------------------------------------------------
    # Every human row, with the compound's sequence and the toxicity score carried onto it,
    # so the most important subset of the dataset is usable without a join.
    mm, tx = modification_maps(M), toxicity_rollup(D)
    om = {r["oligo_id"]: r for r in O}
    OLIGO_COLS = ["oligo_name", "aliases", "oligo_class", "target_gene", "indication",
                  "developer", "max_phase", "length_nt", "sequence_5to3_asprinted",
                  "sequence_base", "sequence_note", "terminal_modification", "sequence_locus",
                  "backbone_chemistry", "sugar_modifications", "gapmer_design", "conjugate",
                  "ps_count", "purity_pct", "purity_method", "identity_confirmation"]
    hum = []
    for r in D:
        if r["species_class"] != "human":
            continue
        o = om[r["oligo_id"]]
        row = {"measurement_id": r["measurement_id"], "oligo_id": r["oligo_id"]}
        row.update({c: o[c] for c in OLIGO_COLS})
        m = mm.get(r["oligo_id"], {})
        row["sugar_modification_map"] = m.get("sugar_map", "NOT_REPORTED")
        row["backbone_linkage_map"] = m.get("backbone_map", "NOT_REPORTED")
        row["n_modification_positions"] = m.get("n_positions", 0)
        row["sequence_status"] = sequence_status(o)
        row.update({c: r[c] for c in D[0] if c not in ("measurement_id", "oligo_id")})
        hum.append(row)
    sheet(wb, "human_measurements", hum)

    # ---- German's analysis -------------------------------------------------
    # One row per compound: the oligo, its sequence, the modification to that sequence, and
    # its toxicity. Nothing else.
    ga = []
    for o in sorted(O, key=lambda r: r["oligo_id"]):
        m, t = mm.get(o["oligo_id"], {}), tx.get(o["oligo_id"], {})
        ga.append({
            "oligo_id": o["oligo_id"], "oligo_name": o["oligo_name"], "aliases": o["aliases"],
            "oligo_class": o["oligo_class"], "target_gene": o["target_gene"],
            "max_phase": o["max_phase"], "developer": o["developer"],
            "length_nt": o["length_nt"],
            "sequence_5to3_asprinted": o["sequence_5to3_asprinted"],
            "sequence_base": o["sequence_base"],
            "sequence_note": o["sequence_note"],
            "sequence_status": sequence_status(o),
            "terminal_modification": o["terminal_modification"],
            "backbone_chemistry": o["backbone_chemistry"],
            "sugar_modifications": o["sugar_modifications"],
            "gapmer_design": o["gapmer_design"], "conjugate": o["conjugate"], "ps_count": o["ps_count"],
            "sugar_modification_map": m.get("sugar_map", "NOT_REPORTED"),
            "backbone_linkage_map": m.get("backbone_map", "NOT_REPORTED"),
            "per_position_chemistry": m.get("per_position", "NOT_REPORTED"),
            "n_modification_positions": m.get("n_positions", 0),
            "worst_coag_tox_grade": t.get("worst_coag_tox_grade", "NOT_REPORTED"),
            "grade_distribution_0_1_2_3": t.get("grade_distribution_0_1_2_3", "NOT_REPORTED"),
            "n_graded_rows": t.get("n_graded_rows", 0),
            "n_rows_flagged_grade_caveat": t.get("n_rows_flagged_grade_caveat", 0),
            "max_source_stated_grade": t.get("max_source_stated_grade", "NOT_APPLICABLE"),
            "severity_in_source_words": t.get("severity_in_source_words", "NOT_REPORTED"),
            "n_measurements": o["n_measurements"],
            "n_human_rows": t.get("n_human_rows", 0), "n_animal_rows": t.get("n_animal_rows", 0),
            "on_target_rows": t.get("on_target_rows", 0),
            "unintended_toxicity_rows": t.get("unintended_toxicity_rows", 0),
            "has_human_and_animal_data": o["has_human_and_animal_data"],
            "source_ids": o["source_ids"],
        })
    sheet(wb, "German's analysis", ga)

    # ---- human_trials ------------------------------------------------------
    # The deduplicated study register. Headline trials first, then every other study record
    # that was identified and deliberately NOT counted as a trial, with the reason visible.
    if ST:
        ordered = sorted(ST, key=lambda r: (r.get("headline_trial") != "TRUE",
                                            r.get("design", ""),
                                            r.get("registry_id", "")))
        sheet(wb, "human_trials", ordered)

    # ---- pooled analyses ---------------------------------------------------
    # A pooled regulatory safety table is real evidence, but its participants overlap the
    # trials it pools, so it is published here rather than inside the trial register. This
    # is the table whose protocol enumerations used to chain whole drug programmes into one
    # "trial" and drive the headline count down to 30.
    _pp = os.path.join(ROOT, "data", "pooled_analyses.csv")
    if os.path.exists(_pp):
        sheet(wb, "pooled_analyses", list(csv.DictReader(open(_pp, newline="", encoding="utf-8"))))

    # ---- bridge ------------------------------------------------------------
    br = [r for r in O if r["invitro_human_animal_bridge"] == "TRUE"
          or r["participant_animal_bridge"] == "TRUE"]
    if br:
        sheet(wb, "bridge", [{
            "oligo_id": r["oligo_id"], "oligo_name": r["oligo_name"],
            "oligo_class": r["oligo_class"], "modality": r["modality"],
            "target_gene": r["target_gene"],
            "sequence_5to3_asprinted": r["sequence_5to3_asprinted"],
            "backbone_chemistry": r["backbone_chemistry"],
            "sugar_modifications": r["sugar_modifications"],
            "bridge_shared_readout_categories": r["bridge_shared_readout_categories"],
            "invitro_human_animal_bridge": r["invitro_human_animal_bridge"],
            "participant_animal_bridge": r["participant_animal_bridge"],
            "n_invitro_human_measurements": r["n_invitro_human_measurements"],
            "n_human_measurements": r["n_human_measurements"],
            "n_animal_measurements": r["n_animal_measurements"],
            "purity_pct": r["purity_pct"], "purity_method": r["purity_method"],
            "source_ids": r["source_ids"],
        } for r in sorted(br, key=lambda r: (r["bridge_shared_readout_categories"] in (NR, "NOT_APPLICABLE"), r["oligo_id"]))])

    # ---- attribution audit -------------------------------------------------
    # Locating a number in the cited document proves it is printed there, not that it belongs
    # to the arm the row assigns it to. This sheet reports that distinction per row.
    _ap = os.path.join(ROOT, "data", "attribution_audit.csv")
    if os.path.exists(_ap):
        sheet(wb, "attribution_audit", list(csv.DictReader(open(_ap, newline="", encoding="utf-8"))))

    # ---- animal appendix ---------------------------------------------------
    # Animal evidence is retained in full -- nothing is deleted -- but it is moved out of the
    # human-facing sheets and named as supporting, so it cannot be read into a human total.
    ani = [r for r in D if r["species_class"] == "animal"]
    sheet(wb, "animal_appendix", ani)

    # ---- unresolved origin -------------------------------------------------
    und = [r for r in D if r["species_class"] == "not_determined"]
    if und:
        sheet(wb, "unresolved_origin", und)

    # Human-first sheet order. The full measurements table stays in the workbook -- no source
    # data is removed -- but the human views come first and the animal appendix last.
    want = ["README", "Summary", "human_trials", "human_measurements", "German's analysis",
            "bridge", "attribution_audit", "pooled_analyses",
            "data_dictionary", "sources", "oligos", "modifications", "measurements",
            "unresolved_origin", "animal_appendix"]
    order = [n for n in want if n in wb.sheetnames] + [n for n in wb.sheetnames if n not in want]
    wb._sheets = [wb[n] for n in order]

    wb.save(OUT)
    print(f"  wrote {os.path.relpath(OUT, ROOT)}")
    print(f"    {len(S)} sources · {len(O)} oligos · {len(D)} measurements · {len(M)} modification rows")
    print(f"    data_dictionary: {len(dd)} columns documented")
    seq_ok = sum(1 for r in hum if r["sequence_base"] not in ("NOT_REPORTED", "NOT_APPLICABLE", ""))
    gr_ok = sum(1 for r in hum if r["coag_tox_grade"] != "NOT_REPORTED")
    print(f"    human_measurements: {len(hum)} rows — {seq_ok} carry a sequence, {gr_ok} carry a grade")
    print(f"    German's analysis:  {len(ga)} compounds — "
          f"{sum(1 for r in ga if r['sequence_base'] not in ('NOT_REPORTED','NOT_APPLICABLE',''))} with a sequence, "
          f"{sum(1 for r in ga if r['n_modification_positions'])} with per-position chemistry")


DEFS = {
    ("*", "oligo_id"): "Foreign key to oligos.oligo_id.",
    ("oligos", "oligo_id"): "Primary key. Stable identifier, COG-OLGnnn.",
    ("oligos", "oligo_name"): "Common or development name.",
    ("oligos", "aliases"): "Other names, semicolon separated.",
    ("oligos", "oligo_class"): "ASO_gapmer | ASO_mixmer | splice_switching_ASO | siRNA | GalNAc_siRNA | aptamer | PMO | tcDNA_ASO | CpG_ODN | polydisperse_ssDNA | other",
    ("oligos", "modality"): "single_stranded_ASO | double_stranded_siRNA | aptamer | mixture | other",
    ("oligos", "target_gene"): "Intended molecular target.",
    ("oligos", "indication"): "Disease or research context.",
    ("oligos", "developer"): "Originating organisation.",
    ("oligos", "max_phase"): "Highest development phase reached.",
    ("oligos", "length_nt"): "Length in nucleotides AS DECLARED BY THE SOURCE.",
    ("oligos", "length_nt_from_sequence"): "Length COMPUTED from sequence_base. Held separately so the declared value can be checked rather than trusted.",
    ("oligos", "sequence_5to3_asprinted"): "Sequence exactly as printed by the source, preserving any case convention that encodes chemistry.",
    ("oligos", "sequence_base"): "Nucleobases only, upper case, chemistry stripped. NOT_APPLICABLE for duplexes and polydisperse mixtures.",
    ("oligos", "sequence_note"): "Anything the source said about the sequence or length that is not itself sequence.",
    ("oligos", "terminal_modification"): "A terminal residue with no position in a 5'->3' string, e.g. a 3'-inverted dT cap.",
    ("oligos", "sequence_locus"): "Where in the document the sequence is printed.",
    ("oligos", "backbone_chemistry"): "full_PS | mixed_PO_PS | full_PO | PMO_neutral | other | NOT_REPORTED",
    ("oligos", "sugar_modifications"): "Semicolon-separated sugar chemistries.",
    ("oligos", "gapmer_design"): "Wing-gap-wing motif where applicable.",
    ("oligos", "conjugate"): "Conjugate moiety (GalNAc, PEG, cholesterol, none).",
    ("oligos", "ps_count"): "Number of phosphorothioate linkages.",
    ("oligos", "purity_pct"): "Per-compound purity. NOT_REPORTED throughout this release - see METHODOLOGY section 6.",
    ("oligos", "purity_method"): "Purification method as the source states it.",
    ("oligos", "identity_confirmation"): "Identity-confirmation method as the source states it.",
    ("oligos", "synthesis_platform"): "Synthesis platform as the source states it.",
    ("oligos", "source_ids"): "Semicolon-separated sources describing this compound.",
    ("oligos", "n_measurements"): "Measurement rows for this compound.",
    ("oligos", "n_human_measurements"): "Measurement rows in a human or human-derived system.",
    ("oligos", "n_animal_measurements"): "Measurement rows in an animal system.",
    ("oligos", "has_human_and_animal_data"): "TRUE where the compound is measured in BOTH - a human/animal translation pair.",
    ("oligos", "notes"): "Free text.",
    ("sources", "source_id"): "Primary key, COG-Snnn.",
    ("sources", "citation"): "Full citation as the document states it.",
    ("sources", "identifier"): "PMCID / PMID / DOI / US patent number / DailyMed set id.",
    ("sources", "document_file"): "File in sources/documents/ - the row's evidence is re-readable from the release.",
    ("sources", "retrieval_route"): "How the document was obtained.",
    ("sources", "licence"): "Licence as stated by the source.",
    ("sources", "redistribution"): "public_domain | CC_BY | CC_BY_NC | CC_BY_NC_ND | publisher_restricted | unresolved",
    ("sources", "extraction_bundle"): "Which extraction bundle read this source (audit trail).",
    ("sources", "n_oligos"): "Compounds described by this source.",
    ("sources", "n_measurements"): "Measurement rows from this source.",
    ("measurements", "measurement_id"): "Primary key, COG-MSRnnnn.",
    ("measurements", "source_id"): "Foreign key to sources.source_id.",
    ("measurements", "study_type"): "in_vitro | ex_vivo_plasma | animal_invivo | clinical. Carries the DESIGN only; species is carried by species_class.",
    ("measurements", "species"): "Species as the source states it, or NOT_APPLICABLE for a purified system.",
    ("measurements", "species_class"): "human | animal | not_determined. The human-versus-animal axis. A purified-protein assay is human when the proteins are human.",
    # ---- columns added in the 2026-10-03 work package -------------------------------
    # ---- purity and characterisation, recovered 2026-10-03 ---------------------------
    ("oligos", "purity_pct_basis"): "tested_batch | drug_substance_specification | publication_methods | multiple_lots_reported_with_different_values_see_purity_batches | NOT_REPORTED. A specification is not the batch used in a study and is never spread across batches.",
    ("oligos", "purity_batches"): "Every reported purity value against its lot, e.g. 'TA666853-008:90%; TA666853-001:94%'. A purity belongs to a lot, so all are kept; where lots disagree, purity_pct carries no single number.",
    ("oligos", "n_purity_batches_reported"): "How many lot-level purity values the sources report for this compound.",
    ("oligos", "purity_locus"): "Exact section or table in the cited document where the purity/characterisation evidence sits.",
    ("oligos", "purity_source_id"): "The source document the characterisation came from.",
    ("oligos", "purity_evidence_quote"): "Verbatim quote supporting the purity and characterisation fields. Every quote was string-matched against the cited file by an independent verification pass.",
    ("oligos", "purity_limits_redacted"): "TRUE where a regulatory document NAMES the purity test but withholds the numeric acceptance limit, which public EPARs routinely do. A withheld limit is recorded as a finding, never as a value.",
    ("oligos", "analytical_methods_regulatory"): "Purity/assay methods as named in a regulatory quality section (typically IP-HPLC-UV-MS). Kept separate from purity_method so publication-derived and regulatory-derived provenance stay distinguishable.",
    ("oligos", "identity_methods_regulatory"): "Identity-confirmation methods as named in a regulatory quality section - accurate mass by MS, sequence confirmation by duplex melting temperature (Tm), NMR, ESI-TOF.",
    ("oligos", "characterisation_methods"): "Other characterisation tests named: counterion by ICP-OES, water by Karl Fischer, residual solvents by GC, elemental impurities by ICP-MS, endotoxin, XRPD, TGA.",
    ("oligos", "purification_method"): "How the material was manufactured or purified, where the document states it.",
    ("oligos", "counterion"): "The salt form and how the counterion is controlled.",
    ("oligos", "impurity_classes"): "Impurity and degradant classes named in the specification.",
    ("oligos", "characterisation_basis"): "regulatory_quality_section:<source_id> where characterisation was recovered from a Quality/CMC section, else not_recovered_from_a_regulatory_quality_section.",
    # ---- quote rights (Crank's delegation, 2026-10-03) ------------------------------
    ("*", "verbatim_quote_status"): "quoted_in_full_source_licence_permits_republication | withheld_source_licence_restricted. A quote is printed only where the source licence permits republication (public_domain, CC BY). 774 of 2,685 are withheld.",
    ("*", "verbatim_quote_sha256"): "SHA-256 of the normalised quote, present whether or not the quote itself is printed. A withheld quote stays checkable: recompute the hash from the source text at source_locus and compare.",
    ("*", "verbatim_quote_word_count"): "Word count of the original quote, kept so a withheld quote's extent is still visible.",
    ("*", "purity_evidence_quote_status"): "Same rule as verbatim_quote_status, for the purity evidence.",
    ("*", "purity_evidence_quote_sha256"): "SHA-256 of the normalised purity quote; present whether or not the quote is printed.",
    ("*", "purity_evidence_quote_word_count"): "Word count of the original purity quote.",
    ("*", "evidence_quote_status"): "Same rule as verbatim_quote_status. A study cluster drawing on several sources is withheld unless EVERY source behind it permits republication, because the quote cannot be attributed to the permissive half.",
    ("*", "evidence_quote_sha256"): "SHA-256 of the normalised register quote.",
    ("*", "evidence_quote_word_count"): "Word count of the original register quote.",
    # ---- held-document recovery, 2026-10-03 -----------------------------------------
    ("oligos", "characterisation_recovery_round"): "Names the round that recovered this compound's characterisation from a document already held in the repository, so recovered-from-a-held-document is always separable from extracted-at-first-pass. NOT_APPLICABLE where nothing was recovered.",
    ("oligos", "endotoxin_level"): "Endotoxin limit or value as printed. SCIENTIFIC_RULES.md §C names this a minimum field. NOT_REPORTED for every compound, because the public documents name the test and withhold the number -- see endotoxin_level_limit_redacted.",
    ("oligos", "endotoxin_method_named"): "The bacterial-endotoxins test as the specification names it (e.g. 'bacterial endotoxins (USP<85>, Ph. Eur. 2.6.14, JP 4.01)'). Present for 10 compounds. This evidence was already captured in characterisation_methods by the previous round; the gap register had wrongly recorded endotoxin as absent for 218/218, which was true of the column and misleading about the evidence.",
    ("oligos", "molecular_weight"): "Relative molecular mass as printed, including the source's own unit -- transcribed exactly, so 'Da g/mol' appears where the document prints it. States whether it is the salt or the free acid where the source does.",
    ("oligos", "dna_content"): "DNA content as printed with its dispersion, for the two defibrotide compounds (heparin red method, 19 porcine and 9 ovine API batches).",
    ("*", "endotoxin_level_basis"): "drug_substance_specification | finished_product_specification | tested_batch | NOT_REPORTED.",
    ("*", "endotoxin_level_source_id"): "Source document the endotoxin evidence came from.",
    ("*", "endotoxin_level_locus"): "Exact section and heading of the endotoxin evidence.",
    ("*", "endotoxin_level_limit_redacted"): "TRUE where the document names the endotoxin test and withholds the numeric limit. A withheld limit is a finding, never a value, and QC fails if both are present.",
    ("*", "endotoxin_level_evidence_quote"): "Verbatim quote supporting the endotoxin record, subject to the same licence withholding as every other quote.",
    ("*", "molecular_weight_basis"): "What kind of statement the molecular weight is. NOT_REPORTED where it is a chemical-identity statement rather than a specification test or a tested batch -- which is the honest answer for most of them.",
    ("*", "molecular_weight_source_id"): "Source document the molecular weight came from.",
    ("*", "molecular_weight_locus"): "Exact section and heading of the molecular-weight statement.",
    ("*", "molecular_weight_limit_redacted"): "FALSE throughout: a molecular weight is not a limit test.",
    ("*", "molecular_weight_evidence_quote"): "Verbatim quote supporting the molecular weight.",
    ("*", "dna_content_basis"): "tested_batch for the defibrotide records: the values are batch measurements, not specifications.",
    ("*", "dna_content_source_id"): "Source document the DNA content came from.",
    ("*", "dna_content_locus"): "Exact table or section of the DNA-content measurement.",
    ("*", "dna_content_limit_redacted"): "FALSE throughout.",
    ("*", "dna_content_evidence_quote"): "Verbatim quote supporting the DNA content.",
    # ---- definitions shared by several tables (the ("*", col) fallback) --------------
    ("*", "compound_families"): "Drug families named by the record, comparators included.",
    ("*", "subject_compound_families"): "The drug families actually under test, with comparators, prior therapies, placebos and positive controls removed.",
    ("*", "compounds"): "Compounds named by the record, verbatim as the source writes them.",
    ("*", "oligo_ids"): "COG-OLG compound ids, extracted from anywhere in the compound strings.",
    ("*", "endpoint_evaluable"): "TRUE where a coagulation endpoint is reported.",
    ("*", "coagulation_endpoints"): "The coagulation endpoints reported, as named by the source.",
    ("*", "enrolled"): "Enrolment as reported, quoted; disagreeing figures are both kept.",
    ("*", "analysed"): "Analysis-set sizes as reported, quoted.",
    ("*", "population"): "Population as described by the source.",
    ("*", "evidence_quote"): "Quoted evidence supporting the row.",
    ("*", "locus"): "Where in the source document the evidence sits.",
    ("*", "measurement_id"): "Stable key of one measurement row (COG-MSR...).",
    ("*", "study_id"): "The register study (studies.csv) the row belongs to.",
    ("*", "study_id_basis"): "How the study link was established, or why it could not be.",
    ("*", "oligo_id"): "Stable key of one oligonucleotide (COG-OLG...).",
    ("*", "source_id"): "Stable key of one source document (COG-S...).",
    ("*", "readout_category"): "Which family of coagulation readout this is.",
    ("*", "readout_name"): "The readout as the source names it.",
    ("*", "evidence_class"): "What kind of observation the row is; read with species_class.",
    ("*", "grade_authority"): "Who assigned the severity grade, if anyone.",
    ("*", "source_locus"): "Exact table, figure, section or page the value came from.",
    # ---- studies (the deduplicated human study register) -----------------------------
    ("studies", "study_id"): "Register key for one distinct study, deduplicated across its registry record, publication, regulatory assessment and label.",
    ("studies", "design"): "interventional_trial | observational_study | case_report | regulatory_summary | product_label | spontaneous_reporting | healthy_volunteer_lab | not_a_human_study. Pooled analyses are NOT here: they are a separate table.",
    ("studies", "design_basis"): "unanimous where every source record agreed on the design, otherwise the set of designs reported.",
    ("studies", "identity_basis"): "What makes this study identifiable, and therefore countable: registry_number | trial_acronym | sponsor_protocol | sponsor_protocol_unqualified | no_identifier. Only the first three may enter the headline total.",
    ("studies", "registry_id"): "The primary registry number (NCT, EudraCT, ISRCTN, JAPIC, EU-CT).",
    ("studies", "registry_ids_all"): "Every registry number in the cluster. Two numbers from DIFFERENT registries are one trial registered twice; two from the same registry fail QC as an over-merge.",
    ("studies", "sponsor_programme"): "The sponsor's compound number(s) (e.g. ISIS304801, ION682884). Used to qualify bare protocol codes: ISIS 304801-CS7 and ISIS 678354-CS7 are different trials.",
    ("studies", "compound_families"): "Every drug family named by the cluster's records, comparators included.",
    ("studies", "subject_compound_families"): "The families actually under test, with comparators, prior therapies, placebos and positive controls removed.",
    ("studies", "trial_acronym"): "Trial acronym as the sources write it. Matching uses its head, so 'ATLAS-A/B (also written ATLAS-AB)' and 'ATLAS-A/B' are one name.",
    ("studies", "sponsor_protocol"): "Sponsor protocol code(s) as written, with the document's own glosses preserved.",
    ("studies", "phase"): "Trial phase as reported; disagreements between documents are preserved verbatim rather than resolved.",
    ("studies", "headline_trial"): "TRUE only where design is interventional_trial AND a coagulation endpoint is reported AND identity_basis is registry_number, trial_acronym or sponsor_protocol. Recomputable from those three columns; QC fails if it is not.",
    ("studies", "endpoint_evaluable"): "TRUE where at least one source record reports a coagulation endpoint for this study.",
    ("studies", "coagulation_endpoints"): "The coagulation endpoints reported, as named by the sources.",
    ("studies", "compounds"): "Compounds named by the cluster's records, verbatim.",
    ("studies", "oligo_ids"): "COG-OLG ids extracted from anywhere in the compound strings, including from inside a name such as 'fitusiran (COG-OLG060)'.",
    ("studies", "enrolled"): "Enrolment as reported, quoted. Figures that disagree between documents are both kept.",
    ("studies", "analysed"): "Analysis-set sizes as reported, quoted.",
    ("studies", "population"): "Study population as described by the source.",
    ("studies", "n_source_records"): "How many raw source records merged into this study. A large number may be a heavily-reported trial; the over-merge QC decides.",
    ("studies", "source_ids"): "The source documents this study was assembled from.",
    ("studies", "designs_reported"): "Every design value the source records gave.",
    ("studies", "evidence_quote"): "Quoted evidence for the study's identity and endpoint.",
    ("studies", "locus"): "Where in the source documents the identity evidence sits.",
    ("studies", "duplicate_of_hint"): "Curator note on suspected duplication with another study record.",
    ("studies", "review_flag"): "Empty where the cluster is clean. OVER_MERGE_* fails QC. registry_alias_verify_linkage, two_subject_compounds_verify, large_cluster_verify_not_an_over_merge and design_disagreement_between_sources are review items, not failures.",
    # ---- pooled_analyses --------------------------------------------------------------
    ("pooled_analyses", "pool_id"): "Key for one pooled analysis.",
    ("pooled_analyses", "source_id"): "The document reporting the pool.",
    ("pooled_analyses", "pool_descriptor"): "How the source describes the pool, verbatim (e.g. 'Pool 2 (integrated long-term safety pool: CS2 + CS3 + CS5 + CS7)').",
    ("pooled_analyses", "member_protocols"): "Protocol codes the pool names. These were previously emitted as identity tokens, which chained whole drug programmes into single 'trials' and drove the headline count down to 30.",
    ("pooled_analyses", "n_member_protocols_named"): "How many member protocols the descriptor names.",
    ("pooled_analyses", "counting_rule"): "Stated on every row: a pooled analysis is NOT a trial and is never added to the human-trial total; its participants overlap its member protocols.",
    # ---- attribution_audit ------------------------------------------------------------
    ("attribution_audit", "verdict"): "ATTRIBUTION_SUPPORTED needs a named locus AND an arm identified in the row's own quote. The weaker verdicts say which half is missing.",
    ("attribution_audit", "locus_named"): "TRUE where source_locus names a table, figure, section or page a reader can go to.",
    ("attribution_audit", "arm_identified"): "TRUE where the row's quote names the arm, group or compound the value is assigned to.",
    ("attribution_audit", "dose_shown_in_quote"): "TRUE where the dose the row claims appears in its quote.",
    ("attribution_audit", "n_shown_in_quote"): "TRUE where the denominator the row claims appears in its quote.",
    ("measurements", "endpoint_scope"): "coagulation | scope_adjacent. scope_adjacent means the readout is NOT a coagulation endpoint and is retained only because the source reports it alongside one.",
    ("measurements", "endpoint_scope_note"): "Why a scope_adjacent row is out of scope, in words.",
    ("measurements", "cross_endpoint_referral"): "For a scope_adjacent row, the Challenge endpoint the observation actually belongs to (complement-activation, cross-cutting) or none_stays_in_coagulopathy.",
    ("measurements", "readout_category_as_curated"): "The readout_category the curator originally wrote, kept where the scope rule replaced it. All six scope_adjacent rows had been given a core coagulation category: COG-MSR0345 said clotting_time for complement fragment Bb.",
    ("measurements", "evidence_class"): "What KIND of observation the row is, derived from the two flags plus readout and direction: intended_pharmacodynamic | measured_negative | unintended_lab_disturbance | outcome_not_attributed | adverse_outcome_source_attributed | baseline_reference | unattributed_lab_change | unresolved_observation. MUST be read together with species_class: these classes are species-agnostic, and the two formerly named 'clinical' were renamed because 222 of 292 rows in one of them were animal.",
    ("measurements", "evidence_class_basis"): "The rule that assigned the evidence_class, stated per row.",
    ("measurements", "evidence_class_review_status"): "Always curator_derived_unreviewed in this release. No evidence_class has been adjudicated by a subject-matter expert.",
    ("measurements", "human_system_subtype"): "For human rows only: participant | primary_blood_or_plasma | cells_or_tissue | purified_or_recombinant_protein | unresolved. A participant in a trial and a purified-protein assay are both 'human' and are not comparable evidence.",
    ("measurements", "grade_authority"): "Who assigned the severity grade: source_reported | curator_derived_research_score | both_source_reported_and_curator_derived | ungraded. Only 24 rows carry a grade a source actually reported.",
    ("measurements", "is_validated_clinical_grade"): "FALSE on every row in this release. No grade has been adjudicated against a clinical grading authority by a subject-matter expert.",
    ("measurements", "study_id"): "The register study (studies.csv) this clinical row belongs to, or NOT_RESOLVED where it cannot be pinned to exactly one. NOT_APPLICABLE on non-clinical rows. Never a guess: an arm misattribution is worse than a missing link.",
    ("measurements", "study_id_basis"): "How the study link was established: source_and_compound_unique | source_unique | registry_number_in_row | protocol_code_in_row | bare_protocol_code_in_row | ambiguous_N_candidates | no_matching_study_in_register. The ambiguous values carry the number of candidate trials.",
    ("measurements", "control_class"): "The reference this row was compared against: sequence_control | pharmacological_positive_control | placebo | vehicle_or_buffer | untreated_or_predose | active_comparator | other_described_control | no_control_described. Vehicle and placebo are NOT sequence controls - they do not separate a sequence effect from a chemistry or formulation effect, and only 8 rows in the dataset carry a sequence-matched control.",
    ("oligos", "invitro_human_animal_bridge"): "TRUE where the compound has at least one measurement in a human IN VITRO system (blood/plasma, cells/tissue or purified protein) and at least one in an animal. This is the comparison Phase 2 calls 'of particular interest'.",
    ("oligos", "participant_animal_bridge"): "TRUE where the compound has participant data and animal data. Kept separate from the in vitro bridge because they are not the same evidence.",
    ("oligos", "bridge_shared_readout_categories"): "Readout categories measured in BOTH a human in vitro system and an animal for this compound - the directly extrapolatable pairs. NOT_APPLICABLE where none is shared.",
    ("oligos", "n_invitro_human_measurements"): "Measurement rows in a human in vitro system (excludes trial participants).",
    ("sources", "licence_resolution_basis"): "How this source's licence was decided. as_extracted_from_source, or the evidence actually read - e.g. europe_pmc_rest_core_and_ncbi_oa_service_2026-10-03, statement_absent_in_held_file_and_ema_legal_notice_unreachable_2026-10-03, or a correction recorded downward.",
    ("measurements", "species_class_basis"): "How species_class was determined: the species field, the system description, or source verification.",
    ("measurements", "human_system"): "TRUE where the measurement is made in a human or human-derived system - the Challenge's 'in vitro human system' criterion.",
    ("measurements", "system_model"): "Cell line, model, subject or assay system.",
    ("measurements", "matrix"): "plasma | whole_blood | serum | in_vivo | purified_system | NOT_APPLICABLE",
    ("measurements", "delivery_method"): "Route or delivery mode.",
    ("measurements", "dose_value"): "Dose or concentration.",
    ("measurements", "dose_unit"): "Unit of dose_value.",
    ("measurements", "timepoint"): "Timepoint of the measurement.",
    ("measurements", "exposure_duration"): "Duration of exposure.",
    ("measurements", "n_subjects"): "Subjects or animals contributing. Several clinical rows are underpowered; this makes that visible.",
    ("measurements", "is_baseline"): "TRUE for a pre-dose draw. A baseline is a reference point, not an effect: it carries no grade.",
    ("measurements", "co_administered_agent"): "Partner drug in a combination arm. A row with this set is NOT a measurement of the oligonucleotide alone.",
    ("measurements", "readout_category"): "clotting_time | factor_activity | fibrinogen | thrombin_generation | fibrinolysis_marker | anticoagulant_activity | bleeding_outcome | thrombotic_outcome | platelet_coag_crosstalk",
    ("measurements", "readout_name"): "The specific assay, e.g. aPTT, PT, INR, TT, ACT, fibrinogen, D_dimer, anti_Xa, FXI_activity, antithrombin_activity.",
    ("measurements", "readout_value"): "The value EXACTLY as printed, including any +/- or range.",
    ("measurements", "readout_unit"): "Unit of readout_value.",
    ("measurements", "readout_is_qualitative"): "TRUE where the row carries no number (e.g. the value exists only in a figure panel).",
    ("measurements", "control_value"): "The matched control value as printed.",
    ("measurements", "control_description"): "What the control was.",
    ("measurements", "effect_direction"): "increase | decrease | no_change | NOT_REPORTED | NOT_APPLICABLE. no_change means a MEASURED null, never an unmentioned endpoint.",
    ("measurements", "effect_vs_control"): "Effect size as the source expresses it.",
    ("measurements", "ratio_to_control"): "Control-referenced ratio computed at build time.",
    ("measurements", "ratio_basis"): "How the ratio was derived, or why none could be.",
    ("measurements", "coag_tox_grade"): "Ordinal 0-3 by CTCAE v5.0 cut-offs, or NOT_REPORTED where no published criterion applies.",
    ("measurements", "grade_basis"): "The exact rule applied, or for an ungraded row why no rule applies.",
    ("measurements", "grade_status"): "provisional on every row - no subject-matter review has taken place.",
    ("measurements", "grade_caveat"): "within_reference_range_resolution where the grade rests on a 1.0-1.2x ratio, which normal variation cannot be excluded from.",
    ("measurements", "source_stated_grade"): "The severity grade the SOURCE itself reports. A different rule from coag_tox_grade; a severity query should read both.",
    ("measurements", "severity_stated_by_source"): "Severity in the source's own words, verbatim.",
    ("measurements", "on_target_effect"): "TRUE where the compound is DESIGNED to act on coagulation.",
    ("measurements", "unintended_toxicity"): "TRUE where the source presents the finding as an adverse or unintended effect. Both flags may be true.",
    ("*", "sequence_status"): "Why a compound has no sequence: published | not_applicable_polydisperse_mixture | not_applicable_duplex_two_strands | recoverable_from_WHO_INN_nomenclature | not_published_by_source.",
    ("*", "sugar_modification_map"): "Per-position sugar chemistry, run-length encoded, e.g. 1-5:2'-MOE; 6-15:DNA; 16-20:2'-MOE.",
    ("*", "backbone_linkage_map"): "Per-position backbone linkage, run-length encoded.",
    ("*", "per_position_chemistry"): "The full per-residue map: position, nucleobase, sugar and 3' linkage.",
    ("*", "worst_coag_tox_grade"): "Highest ASSIGNED grade across the compound's rows. NOT_REPORTED where no row could be graded -- absence of a grade is not a grade of 0.",
    ("*", "grade_distribution_0_1_2_3"): "Count of the compound's rows at each grade.",
    ("*", "severity_in_source_words"): "Severity as the source states it, verbatim.",
    ("measurements", "value_origin"): "measured_in_this_document | cited_from_another_source",
    ("measurements", "source_locus"): "Exact locus - table, figure, section, label section or page.",
    ("measurements", "redistribution"): "Inherited from the source.",
    ("measurements", "verbatim_quote"): "Text copied from the document supporting this row. Present on every row.",
    ("measurements", "notes"): "Free text, including method limitations and reporting-silence flags.",
    ("modifications", "position"): "Nucleotide position, 5' to 3', contiguous from 1.",
    ("modifications", "nucleobase"): "A | C | G | T | U. Must equal sequence_base at this position.",
    ("modifications", "sugar_mod"): "DNA | RNA | LNA | 2'-MOE | 2'-OMe | 2'-F | cEt | morpholino | tcDNA | NOT_REPORTED",
    ("modifications", "backbone_linkage_3p"): "The linkage 3' of this position: PS | PO | PN | NOT_APPLICABLE | NOT_REPORTED",
    ("modifications", "is_5_methyl_C"): "TRUE only where the source states it. FALSE means not stated.",
    ("modifications", "basis"): "How the chemistry at this position was determined, e.g. the source's own case legend quoted.",
}

if __name__ == "__main__":
    main()
