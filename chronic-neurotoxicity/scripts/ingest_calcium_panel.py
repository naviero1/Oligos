#!/usr/bin/env python3
"""Ingest the paired IN VITRO arm of the Hagedorn 2022 ASO panel.

Why this lane exists separately from the in-vivo rows
-----------------------------------------------------
Hagedorn et al. 2022 (Nucleic Acid Ther 32:151-162, doi:10.1089/nat.2021.0071,
PMC9221153, **CC-BY 4.0**) report two measurements on the same molecules:

  * an acute tolerability score in mice after ICV dosing (already ingested by the
    nonclinical lane), and
  * a spontaneous calcium-oscillation score in rat primary cortical neurons.

The pairing is the point. The challenge asks for data that can "bridge the
differences between predictions that are primarily based on data from
animal-based studies to data collected by in vitro systems", and this panel gives
an in-vitro and an in-vivo readout on *the same compounds with published
sequences* — matched pairs, not two unrelated collections.

Scope decision, made deliberately
---------------------------------
Supplementary Table S1 carries calcium-oscillation scores for **1,825** ASOs but
in-vivo scores for only **181**. Only those 181 are ingested here, so every row
added is half of a matched pair.

The remaining ~1,644 cell-only compounds are NOT ingested, and that is a
judgement, not an oversight. The challenge brief says submissions focused on
"acute neurotoxicity, specifically alterations of neuronal electrical activity"
are a lower priority, and a spontaneous-calcium-oscillation assay is exactly
that readout. Ingesting all 1,825 would have made the deprioritised endpoint
three-quarters of the dataset while adding no new molecules to the paired set.
They remain freely available in the cited CC-BY supplement for anyone who wants
them.

Assay, as described in the paper's Methods
------------------------------------------
Primary cortical neurons from E19 Sprague-Dawley rat embryos, 384-well FLIPR,
ASO added directly to the medium (no transfection reagent) at a final
concentration of 25 uM - chosen by the authors as within the range of CSF
concentrations expected in the first hour after a 100 ug ICV dose. Baseline read
100 s, then 200 s after addition, then a further 300 s read. The score sums
1-second reads whose signal increase exceeds 50% of the mean control amplitude,
expressed as **percent of control**. Reduced oscillations track acute
neurotoxicity: the paper's toxic exemplar ASO produced fewer oscillations and its
safe exemplar produced more.

Grade mapping (curator-defined, stated on every row)
----------------------------------------------------
    >= 80% of control ...... grade 0   (no meaningful reduction)
    50 to < 80% ............ grade 1   (mild reduction)
    < 50% .................. grade 2   (marked reduction)
    > 100% (increase) ...... grade 0   (the paper associates INCREASED
                                        oscillations with its safe exemplar and
                                        makes no toxicity claim for increases)

Capped at grade 2 on purpose. Grade 3 in this schema requires degeneration,
paralysis, intervention, death or dose-limiting toxicity, and a single in vitro
activity marker cannot establish any of those - the same cap the patents lane
applied to marker-only readouts.

Usage:  python scripts/ingest_calcium_panel.py
"""
import json
import os

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, "sources", "cns",
                    "hagedorn2022_NAT_SupplTableS1_148ASO_ICV_mouse_tolerability.xlsx")
NONCLIN = os.path.join(ROOT, "notes", "cns", "extractions", "nonclinical.json")
OUT = os.path.join(ROOT, "notes", "cns", "extractions", "invitro_calcium.json")

SOURCE_REF = "doi:10.1089/nat.2021.0071"
GRADE_NOTE = ("grade_provisional;curator mapping of the paper's calcium-oscillation "
              "score (percent of control): >=80 => 0, 50-<80 => 1, <50 => 2; "
              "increases above control => 0 since the paper associates increased "
              "oscillations with its safe exemplar; capped at 2 because one in vitro "
              "activity marker cannot establish the grade-3 criteria")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def grade(score):
    if score > 100:
        return 0
    if score >= 80:
        return 0
    if score >= 50:
        return 1
    return 2


def direction(score):
    if score > 105:
        return "increase"
    if score < 95:
        return "decrease"
    return "no_change"


def main():
    wb = openpyxl.load_workbook(XLSX)
    rows = list(wb["S1"].iter_rows(values_only=True))
    hdr = rows[0]
    iSeq = hdr.index("Sequence")
    iTgt = hdr.index("Target")
    iLen = hdr.index("Length")
    iLNA = hdr.index("Number_LNA")
    iCaO = hdr.index("Measured_CaO_score_cells")
    iMice = hdr.index("Acute_tolerance_score_mice")

    # The in-vivo arm is already curated; reuse its names and sequences verbatim so
    # the assembler's name+sequence rule attaches these rows to the existing oligos
    # instead of creating a second copy of the panel.
    nc = json.load(open(NONCLIN, encoding="utf-8"))
    by_seq = {}
    for o in nc["oligos"]:
        s = (o.get("sequence_5to3") or "").strip()
        if s and s != "TBD" and SOURCE_REF.split(":")[1] in (o.get("design_source") or ""):
            by_seq[s.upper()] = o

    oligos, meas, unmatched = [], [], 0
    n = 0
    for r in rows[1:]:
        if num(r[iMice]) is None:          # in-vivo arm absent -> not a matched pair
            continue
        cao = num(r[iCaO])
        if cao is None:
            continue
        seq = str(r[iSeq]).strip()
        src = by_seq.get(seq.upper())
        if src is None:
            unmatched += 1
            continue
        n += 1
        oid = "TMP_cao_%d" % n
        oligos.append({
            "oligo_id": oid,
            "oligo_name": src["oligo_name"],
            "aliases": src.get("aliases", "NA"),
            "oligo_class": src.get("oligo_class", "ASO_gapmer"),
            "target_gene": src.get("target_gene", str(r[iTgt])),
            "indication": src.get("indication", "research_tool"),
            "developer": src.get("developer", "TBD"),
            "max_phase": "research_panel",
            "length_nt": src.get("length_nt", str(r[iLen])),
            "backbone_chemistry": src.get("backbone_chemistry", "full_PS"),
            "sugar_modifications": src.get("sugar_modifications", "LNA;DNA_gap"),
            "gapmer_design": src.get("gapmer_design", "NA"),
            "conjugate": src.get("conjugate", "none"),
            "ps_count": src.get("ps_count", "TBD"),
            "sequence_5to3": seq,
            "design_source": src.get("design_source", ""),
            "notes": ("paired in-vitro arm of the same panel; number_LNA=%s; "
                      "in-vivo mouse ICV acute tolerability score for this same "
                      "molecule = %s (see the animal row)" % (r[iLNA], r[iMice])),
        })
        meas.append({
            "measurement_id": "TMP_cao_m%d" % n,
            "oligo_id": oid,
            "study_type": "in_vitro",
            "species": "rat",
            "system_model": "primary_cortical_neuron",
            "cns_region": "cortex",
            "delivery_method": "gymnotic_free_uptake",
            "dose_or_conc_value": 25,
            "dose_or_conc_unit": "uM",
            "exposure_duration": "500s_FLIPR_read",
            "endpoint_domain": "acute_neurotoxicity",
            # A spontaneous-calcium-oscillation assay measures neuronal network
            # activity, which is the readout class the challenge brief explicitly
            # deprioritises. Flagged so it is filterable rather than buried.
            "challenge_priority": "low_acute_electrophysiology",
            "readout_category": "electrophysiology",
            "readout_name": "spontaneous_calcium_oscillation_score",
            "readout_value": cao,
            "readout_unit": "% of control",
            "effect_direction": direction(cao),
            "effect_vs_control": "%.2f%% of vehicle control" % cao,
            "neurotox_grade": grade(cao),
            "reversibility": "not_assessed",
            "is_cns_specific": "TRUE",
            "source_id": "HAG2022_INVITRO",
            "source_ref": SOURCE_REF,
            "source_table": "Supplementary Table S1, column Measured_CaO_score_cells",
            "redistribution": "cc_by",
            "notes": GRADE_NOTE + (";paired with the in-vivo mouse ICV acute "
                                   "tolerability score of %s for the same molecule"
                                   % r[iMice]),
        })

    json.dump({
        "lane": "invitro_calcium",
        "oligos": oligos,
        "measurements": meas,
        "extraction_notes": __doc__ + (
            "\n\nRun result: %d matched-pair rows written; %d in-vivo-scored rows "
            "had no sequence match in the already-curated in-vivo arm and were "
            "skipped rather than guessed." % (len(meas), unmatched)),
    }, open(OUT, "w", encoding="utf-8"), indent=1)

    print("wrote %s: %d oligos, %d measurements (%d unmatched, skipped)"
          % (OUT, len(oligos), len(meas), unmatched))


if __name__ == "__main__":
    main()
