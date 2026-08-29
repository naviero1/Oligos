#!/usr/bin/env python3
"""Ingest source H1 — Hagedorn et al. 2022, Supplementary Table S1 — into the OligoTox-CNS schema.

Source
------
Hagedorn PH, Brown JM, Easton A, Pierdomenico M, Jones K, Olson RE, Mercer SE, Li D, Loy J,
Hog AM, Jensen ML, Gill M, Cacace AM. "Acute Neurotoxicity of Antisense Oligonucleotides After
Intracerebroventricular Injection Into Mouse Brain Can Be Predicted from Sequence Features."
Nucleic Acid Ther. 2022 Jun;32(3):151-162. doi:10.1089/nat.2021.0071. PMID 35166597. PMC9221153.
Licence: CC BY 4.0 -> the supplementary table may be redistributed with attribution.

Why this source anchors the module
----------------------------------
Supplementary Table S1 pairs, for 1,825 oligonucleotides:
  * the full sequence, with LNA position encoded by upper case and DNA by lower case
    ("Sequences are shown with LNA-modified nucleotides in upper case bold and DNA nucleotides
     in lower case. All ASOs are with full phosphorothioate backbones." -- Table 1 legend)
  * a measured in vitro readout  (calcium-oscillation score, rat primary cortical neurons)
  * for 181 of them, a measured in vivo readout (mouse acute tolerability score, 0-20)

Nothing here is inferred. Every column written below is either copied from the table, or is a
deterministic function of the printed sequence string (base counts, run lengths, gap geometry),
which is stated as such in `modification_position_basis` and in the data dictionary.

Grading
-------
The 0-3 `cns_tox_grade` is NOT invented. It uses the cut-offs the authors themselves defined:

    "Based on inspection of the cumulative distribution of tolerability scores (Fig. 1B), we
     divided ASO into those with mild, moderate, marked, and severe tolerability signs using
     score cutoffs at 4, 7, and 18. We judged that only ASOs with no or mild tolerability signs
     ... were suitable for further development. The remaining 40% of all ASOs, with moderate to
     severe tolerability signs, were judged as having an acute neurotoxic potential too high for
     further development."

so that grade <= 1 reproduces the authors' "suitable for further development" class exactly.
"""
from __future__ import annotations

import csv
import pathlib
import re
import sys

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUPP = ROOT / "sources" / "H1_Hagedorn2022" / "Suppl_TableS1.xlsx"
OUT = ROOT / "data" / "staged"

SOURCE_ID = "H1"
SOURCE_REF = "Hagedorn2022_NAT_10.1089/nat.2021.0071"

# --- the authors' own cut-offs (Fig. 1B) -------------------------------------------------
# ANS == 0            -> no observable signs
# 0  < ANS <= 4       -> "mild"      | authors: suitable for further development
# 4  < ANS <= 7       -> "moderate"  | authors: too high for further development
# 7  < ANS            -> "marked"/"severe" (their further cut-off at 18 separates these two)
GRADE_BANDS = [(0.0, 0, "ANS=0 (no observable signs)"),
               (4.0, 1, "0<ANS<=4 mild (Hagedorn2022 Fig.1B cutoff 4)"),
               (7.0, 2, "4<ANS<=7 moderate (Hagedorn2022 Fig.1B cutoff 7)"),
               (float("inf"), 3, "ANS>7 marked/severe (Hagedorn2022 Fig.1B cutoffs 7,18)")]


def grade_ans(ans: float) -> tuple[int, str]:
    for hi, g, basis in GRADE_BANDS:
        if ans <= hi:
            return g, basis
    raise AssertionError("unreachable")


def g_free_3prime(seq: str) -> int:
    """Nucleotides from the 3'-end containing no G. Capped at 20, and 20 if the ASO has no G --
    this is the authors' own definition, transcribed from their published R function."""
    s = seq.lower()
    pos = [i for i, ch in enumerate(s) if ch == "g"]
    if not pos:
        return 20
    return min(20, len(s) - 1 - max(pos))


def longest_run(seq: str, base: str) -> int:
    runs = re.findall(f"{base}+", seq.lower())
    return max((len(r) for r in runs), default=0)


def published_score(seq: str) -> float:
    """The authors' trained linear model, transcribed verbatim from Supplementary Methods."""
    s = seq.lower()
    return round(136.0430
                 - 3.1263 * s.count("a")
                 - 5.1100 * s.count("c")
                 - 4.7217 * s.count("t")
                 - 10.1264 * s.count("g")
                 + 1.3577 * g_free_3prime(seq), 1)


def gap_geometry(seq: str) -> tuple[str, int, int, int, str]:
    """Return (design_label, flank5, gap, flank3, shape). Upper case == LNA, lower == DNA."""
    m = re.fullmatch(r"([A-Z]+)([a-z]+)([A-Z]+)", seq)
    if m:
        f5, gap, f3 = len(m.group(1)), len(m.group(2)), len(m.group(3))
        return f"{f5}-{gap}-{f3}_LNA_gapmer", f5, gap, f3, "gapmer"
    # not a clean flank-gap-flank arrangement: LNA residues are interspersed
    return "LNA_mixmer_noncontiguous_flanks", -1, -1, -1, "mixmer"


def mod_position_string(seq: str) -> str:
    """Per-position sugar chemistry, 5'->3', one token per nucleotide. Directly readable from
    the source's own case convention -- this is transcription, not inference."""
    return ";".join(f"{i}:{ch.upper()}:{'LNA' if ch.isupper() else 'DNA'}"
                    for i, ch in enumerate(seq, start=1))


def main() -> int:
    if not SUPP.exists():
        print(f"missing source file: {SUPP}", file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.load_workbook(SUPP, read_only=True, data_only=True)
    rows = list(wb["S1"].iter_rows(values_only=True))
    hdr = list(rows[0])
    data = [r for r in rows[1:] if r and r[0]]
    col = {name: hdr.index(name) for name in hdr}

    oligos, measurements, modifications = [], [], []
    model_mismatch = 0

    for n, r in enumerate(data, start=1):
        seq = r[col["Sequence"]]
        oid = f"H1-OLG-{n:04d}"
        design, f5, gap, f3, shape = gap_geometry(seq)
        base = seq.upper()
        n_lna = sum(1 for ch in seq if ch.isupper())

        # cross-check the printed helper columns against the printed sequence
        assert len(seq) == r[col["Length"]], f"{oid} length mismatch"
        assert n_lna == r[col["Number_LNA"]], f"{oid} LNA count mismatch"
        if abs(published_score(seq) - r[col["Calculated_score"]]) > 0.11:
            model_mismatch += 1

        oligos.append({
            "oligo_id": oid,
            "oligo_name": f"Hagedorn2022_{r[col['Set']]}_{n:04d}",
            "aliases": r[col["ID in figure"]] or "",
            "oligo_class": "ASO_gapmer" if shape == "gapmer" else "ASO_mixmer",
            "modality": "single_stranded_ASO",
            "target_gene": {"Tau": "MAPT", "STC1": "STC1", "None": "none_no_transcriptome_match"}
                           .get(r[col["Target"]], r[col["Target"]]),
            "target_transcript": "MAPT_pre_mRNA" if r[col["Target"]] == "Tau" else r[col["Target"]],
            "indication": "research_panel_CNS_neurotoxicity",
            "developer": "Roche/Bristol Myers Squibb",
            "max_phase": "research_panel",
            "length_nt": len(seq),
            "sequence_5to3_asprinted": seq,
            "sequence_base": base,
            "backbone_chemistry": "full_PS",
            "backbone_linkage_positions": f"PS x{len(seq) - 1} (all internucleoside linkages)",
            "sugar_modifications": "LNA;DNA_gap",
            "modification_pattern": design,
            "modification_positions": mod_position_string(seq),
            "modification_position_basis": "position_resolved_from_source",
            "n_lna": n_lna,
            "n_dna": len(seq) - n_lna,
            "gap_length_nt": gap if gap >= 0 else "",
            "flank5_len_nt": f5 if f5 >= 0 else "",
            "flank3_len_nt": f3 if f3 >= 0 else "",
            "gapmer_shape": shape,
            "conjugate": "none",
            "ps_linkage_count": len(seq) - 1,
            "n_A": base.count("A"), "n_C": base.count("C"),
            "n_G": base.count("G"), "n_T": base.count("T"),
            "gc_content_pct": round(100 * (base.count("G") + base.count("C")) / len(seq), 2),
            "longest_g_run": longest_run(seq, "g"),
            "g_free_3prime_len": g_free_3prime(seq),
            # -- purity / characterisation: method stated by the source, values not published --
            "purity_pct": "NOT_REPORTED",
            "purity_method": "DMT-on solid-phase extraction (Agilent TOP cartridges); identity and "
                             "purity validated by reversed-phase UPLC coupled to mass spectrometry",
            "identity_confirmation": "RP-UPLC-MS; concentration confirmed by UV absorbance with "
                                     "calculated Beer-Lambert extinction coefficient",
            "synthesis_platform": "MerMade 192X synthesiser, standard phosphoramidite protocols",
            "formulation": "sterile 0.9% saline",
            "dataset_split_asPublished": r[col["Set"]],
            "source_id": SOURCE_ID,
            "source_location": "Supplementary Table S1",
            "notes": "",
        })

        # ---- per-position modification long table -------------------------------------
        for i, ch in enumerate(seq, start=1):
            modifications.append({
                "oligo_id": oid,
                "position_5to3": i,
                "nucleobase": ch.upper(),
                "sugar_chemistry": "LNA" if ch.isupper() else "DNA_2prime_deoxy",
                "linkage_3prime": "phosphorothioate" if i < len(seq) else "terminal_none",
                "basis": "position_resolved_from_source",
                "source_id": SOURCE_ID,
            })

        # ---- measurement 1: in vitro calcium oscillation (every oligo) ------------------
        cao = r[col["Measured_CaO_score_cells"]]
        measurements.append({
            "measurement_id": f"H1-MSR-{len(measurements) + 1:05d}",
            "oligo_id": oid, "source_id": SOURCE_ID,
            "study_type": "in_vitro",
            "species": "rat", "strain": "Sprague-Dawley (embryonic day 19)",
            "system_model": "primary cortical neuron culture, FLIPR calcium imaging (fluo-4 AM)",
            "is_human_system": "FALSE",
            "cns_region": "cortex",
            "delivery_route": "in_culture_medium",
            "dose_value": 25, "dose_unit": "uM",
            "exposure_duration": "300 s read",
            "timepoint": "300 s FLIPR read",
            "readout_category": "electrophysiology_calcium",
            "readout_name": "spontaneous_calcium_oscillation_score_pct_of_control",
            "readout_value": cao, "readout_unit": "pct_of_untreated_control",
            "n_per_group": "NOT_REPORTED_per_oligo",
            "statistic": "NOT_REPORTED_per_oligo",
            "effect_direction": "decrease" if cao < 100 else "increase" if cao > 100 else "no_change",
            "effect_vs_control": f"{cao}% of untreated control amplitude-derived score",
            "cns_tox_grade": "", "grade_basis": "in_vitro_continuous_readout_not_graded",
            "grade_status": "not_graded",
            "tox_axis": "acute_neuronal_excitability",
            "is_cns_specific": "TRUE",
            "source_ref": SOURCE_REF,
            "source_location": "Supplementary Table S1, column Measured_CaO_score_cells",
            "redistribution": "cc_by",
            "notes": "Lower score = fewer/smaller oscillations = greater in vitro effect. "
                     "Scoring: 1 point per 1 s read with signal increase >50% of mean control "
                     "amplitude, summed over 300 s, expressed as % of control.",
        })

        # ---- measurement 2: in vivo mouse acute tolerability (181 oligos) ---------------
        ans = r[col["Acute_tolerance_score_mice"]]
        if isinstance(ans, (int, float)):
            g, basis = grade_ans(float(ans))
            measurements.append({
                "measurement_id": f"H1-MSR-{len(measurements) + 1:05d}",
                "oligo_id": oid, "source_id": SOURCE_ID,
                "study_type": "animal_invivo",
                "species": "mouse", "strain": "C57BL/6J adult female",
                "system_model": "single ICV bolus, modified functional observational battery "
                                "(Oligonucleotide Safety Working Group recommendation)",
                "is_human_system": "FALSE",
                "cns_region": "whole_brain_lateral_ventricle",
                "delivery_route": "intracerebroventricular",
                "dose_value": 100, "dose_unit": "ug",
                "exposure_duration": "single bolus",
                "timepoint": "0-1 h post-injection",
                "readout_category": "behavioural",
                "readout_name": "acute_tolerability_score_ANS",
                "readout_value": ans, "readout_unit": "score_0_to_20",
                "n_per_group": "4-6 mice per treatment group",
                "statistic": "group mean of per-mouse scores",
                "effect_direction": "increase" if ans > 0 else "no_change",
                "effect_vs_control": f"ANS {ans} of 20 (0 = no side effects)",
                "cns_tox_grade": g, "grade_basis": basis,
                "grade_status": "provisional",
                "tox_axis": "acute_behavioural",
                "is_cns_specific": "TRUE",
                "source_ref": SOURCE_REF,
                "source_location": "Supplementary Table S1, column Acute_tolerance_score_mice",
                "redistribution": "cc_by",
                "notes": "Five categories (hyperactivity; decreased activity/arousal; motor "
                         "dysfunction/ataxia; abnormal posture and breathing; tremor/convulsions), "
                         "each 0-4, summed to 0-20.",
            })

    for name, recs in (("oligos", oligos), ("measurements", measurements),
                       ("modifications", modifications)):
        path = OUT / f"H1_{name}.csv"
        with path.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(recs[0].keys()))
            w.writeheader()
            w.writerows(recs)
        print(f"wrote {path.relative_to(ROOT)}: {len(recs)} rows x {len(recs[0])} cols")

    print(f"\npublished-model reproduction mismatches (>0.11): {model_mismatch}/{len(data)}")
    import collections
    gd = collections.Counter(m["cns_tox_grade"] for m in measurements if m["cns_tox_grade"] != "")
    print("in vivo grade distribution:", dict(sorted(gd.items())))
    print("gapmer shapes:", dict(collections.Counter(o["gapmer_shape"] for o in oligos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
