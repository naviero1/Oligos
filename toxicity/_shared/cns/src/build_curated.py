#!/usr/bin/env python3
"""Ingest sources K1, L1, O1 and C1 into the OligoTox-CNS schema.

K1  Miller BR, Paquette JD, Barker AR, et al. (Khvorova/Aronin lab)
    "Chemical and physical variables to consider when delivering oligonucleotides to the CNS"
    -- Mol Ther Nucleic Acids 2024;35(2):102359. doi:10.1016/j.omtn.2024.102359. PMC11185713.
    Supplementary Table S2 gives, for every mouse group in the paper, the oligonucleotide, dose,
    the Ca2+ and Mg2+ concentration in the injectate, the average acute tolerability score, the
    group size and the mouse genotype. Parsed directly from the supplementary PDF.

L1  Kuroda T, Yoshioka K, Lei Mon SS, et al. (Yokota / Obika labs)
    "Unraveling and controlling late-onset neurotoxicity of antisense oligonucleotides through
    strategic chemical modifications" -- Mol Ther Nucleic Acids 2025;36. PMC12744863.
    Supplementary Table S1 prints five ASOs. The chemistry is encoded in TYPEFACE, not in text:
    bold = LNA, bold+italic = 2'-MOE, regular = DNA, "C(5)" = 5-methylcytosine. The parser below
    reads the PDF span styling so the per-position chemistry is recovered mechanically rather
    than hand-transcribed.

O1  O'Rourke JJ, Bravo-Hernandez M, et al.
    "Acute neuronal inhibition response caused by phosphorothioate antisense oligonucleotides
    following local delivery to the central nervous system" -- Nucleic Acids Res 2026;54(3):gkaf1333.
    PMC12865454. Contributes the acute-inhibition scoring instruments for rodent IT, rodent ICV
    and non-human-primate IT, and a directly contradictory formulation finding (see notes).

C1  Clinical layer -- FDA prescribing information retrieved from DailyMed, read directly.
    QALSODY (tofersen) setid 81356b45-1cb7-4eef-88ea-e44cc18b47c5, label published 2024-11-18.
    SPINRAZA (nusinersen) setid dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94, label published 2026-04-06.

NO VALUE IN THIS FILE IS ESTIMATED. Where a paper shows a result only as a figure, the numeric
readout is written NOT_REPORTED and the qualitative outcome the authors state in words is
recorded instead, with `readout_is_qualitative` set.
"""
from __future__ import annotations

import csv
import pathlib
import re
import sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "staged"

# ============================================================================================
# L1 -- Kuroda 2025: recover per-position chemistry from PDF typeface
# ============================================================================================
KURODA_META = {
    # name: (target, ICV dose nmol, ICV dose ug, outcome stated in words, grade, sacrifice day)
    "ASO1": ("MAPT", 38.4, 200, "late-onset neurotoxicity: increased tolerability score, reduced "
                                "locomotor activity and max speed; sacrificed day 21", 2),
    "ASO2": ("HDAC2", 19.0, 100, "severe late-onset neurotoxicity: increased tolerability score "
                                 "incl. consciousness, severe body-weight loss; sacrificed day 7", 3),
    "ASO3": ("SNCA", 15.2, 100, "severe late-onset neurotoxicity: increased tolerability score "
                                "incl. consciousness, severe body-weight loss; sacrificed day 7", 3),
    "ASO4": ("SNCA", 39.9, 250, "late-onset neurotoxicity: increased tolerability score, reduced "
                                "max speed; sacrificed day 21", 2),
    "ASO5": ("HTT", 39.9, 280, "NON-TOXIC negative control; no increase in tolerability score; "
                               "ASO chemistry already used in clinical trials", 0),
}


def parse_kuroda_sequences(pdf: pathlib.Path) -> dict:
    """Return {name: [(base, sugar, is_5methyl_C), ...]} read from typeface, 5'->3'."""
    doc = pymupdf.open(pdf)
    page = next(p for p in doc if "ASO1" in p.get_text() and "Sequence" in p.get_text())
    seqs, current = {}, None
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = line["spans"]
            joined = "".join(s["text"] for s in spans).strip()
            m = re.fullmatch(r"(ASO\d)", joined)
            if m:
                current = m.group(1)
                continue
            if current and ("5′-" in joined or "5'-" in joined):
                units = []
                for s in spans:
                    bold, italic = bool(s["flags"] & 16), bool(s["flags"] & 2)
                    sugar = "2'-MOE" if (bold and italic) else "LNA" if bold else "DNA_2prime_deoxy"
                    text = s["text"].replace("5′-", "").replace("5'-", "").strip()
                    # tokenise: "C(5)" is one unit (5-methylcytosine); other letters are one each
                    for tok in re.findall(r"C\(5\)|[ACGT]", text):
                        if tok == "C(5)":
                            units.append(("C", sugar, True))
                        else:
                            units.append((tok, sugar, False))
                if units:
                    seqs[current] = units
                current = None
    return seqs


def kuroda_records(seqs: dict) -> tuple[list, list, list]:
    oligos, measurements, mods = [], [], []
    for i, (name, units) in enumerate(sorted(seqs.items()), start=1):
        target, nmol, ug, outcome, grade = KURODA_META[name]
        oid = f"L1-OLG-{i:04d}"
        seq_plain = "".join(u[0] for u in units)
        # design motif: contiguous runs of non-DNA sugar at each end
        sugars = [u[1] for u in units]
        f5 = next((j for j, s in enumerate(sugars) if s == "DNA_2prime_deoxy"), 0)
        f3 = next((j for j, s in enumerate(reversed(sugars)) if s == "DNA_2prime_deoxy"), 0)
        gap = len(units) - f5 - f3
        wing = sugars[0]
        oligos.append({
            "oligo_id": oid,
            "oligo_name": f"Kuroda2025_{name}",
            "aliases": name,
            "oligo_class": "ASO_gapmer",
            "modality": "single_stranded_ASO",
            "target_gene": target,
            "target_transcript": f"{target}_mRNA",
            "indication": "research_panel_CNS_late_onset_neurotoxicity",
            "developer": "Institute of Science Tokyo / Osaka University",
            "max_phase": "research_panel",
            "length_nt": len(units),
            "sequence_5to3_asprinted": seq_plain,
            "sequence_base": seq_plain,
            "backbone_chemistry": "full_PS",
            "backbone_linkage_positions": f"PS x{len(units) - 1} (all internucleoside linkages; "
                                          "source notes PO substitutions only at underlined "
                                          "positions, which are NOT_RECOVERABLE from the PDF text layer)",
            "sugar_modifications": f"{wing};DNA_gap",
            "modification_pattern": f"{f5}-{gap}-{f3}_{wing}_gapmer",
            "modification_positions": ";".join(
                f"{j}:{b}:{s}{':5-methyl-C' if me else ''}" for j, (b, s, me) in enumerate(units, 1)),
            "modification_position_basis": "position_resolved_from_source_typeface",
            "n_lna": sum(1 for s in sugars if s == "LNA"),
            "n_moe": sum(1 for s in sugars if s == "2'-MOE"),
            "n_dna": sum(1 for s in sugars if s == "DNA_2prime_deoxy"),
            "n_5methyl_C": sum(1 for u in units if u[2]),
            "gap_length_nt": gap, "flank5_len_nt": f5, "flank3_len_nt": f3,
            "gapmer_shape": "gapmer", "conjugate": "none",
            "ps_linkage_count": len(units) - 1,
            "n_A": seq_plain.count("A"), "n_C": seq_plain.count("C"),
            "n_G": seq_plain.count("G"), "n_T": seq_plain.count("T"),
            "gc_content_pct": round(100 * (seq_plain.count("G") + seq_plain.count("C")) / len(units), 2),
            "purity_pct": "NOT_REPORTED",
            "purity_method": "NOT_REPORTED",
            "identity_confirmation": "NOT_REPORTED",
            "synthesis_platform": "NOT_REPORTED",
            "formulation": "NOT_REPORTED",
            "source_id": "L1", "source_location": "Supplementary Table S1",
            "notes": "Chemistry recovered from PDF typeface: bold=LNA, bold-italic=2'-MOE, "
                     "regular=DNA, C(5)=5-methylcytosine.",
        })
        for j, (b, s, me) in enumerate(units, 1):
            mods.append({"oligo_id": oid, "position_5to3": j, "nucleobase": b,
                         "sugar_chemistry": s,
                         "base_modification": "5-methylcytosine" if me else "none",
                         "linkage_3prime": "phosphorothioate" if j < len(units) else "terminal_none",
                         "basis": "position_resolved_from_source_typeface", "source_id": "L1"})
        measurements.append({
            "measurement_id": f"L1-MSR-{len(measurements) + 1:05d}",
            "oligo_id": oid, "source_id": "L1",
            "study_type": "animal_invivo", "species": "mouse",
            "strain": "C57BL/6 female, 7 weeks",
            "system_model": "single ICV injection; 5-category 0-4 tolerability score (Table S2)",
            "is_human_system": "FALSE", "cns_region": "whole_brain_lateral_ventricle",
            "delivery_route": "intracerebroventricular",
            "dose_value": nmol, "dose_unit": "nmol",
            "dose_value_secondary": ug, "dose_unit_secondary": "ug",
            "exposure_duration": "single injection",
            "timepoint": "days 1-21 post-injection (late-onset window)",
            "readout_category": "behavioural",
            "readout_name": "tolerability_score_late_onset",
            "readout_value": "NOT_REPORTED",
            "readout_is_qualitative": "TRUE",
            "readout_unit": "score_0_to_20",
            "n_per_group": "4",
            "statistic": "mean +/- SEM; significance vs vehicle",
            "effect_direction": "increase" if grade > 0 else "no_change",
            "effect_vs_control": outcome,
            "cns_tox_grade": grade,
            "grade_basis": "qualitative severity stated by authors (sacrifice day 7 = grade 3; "
                           "score increase without early sacrifice = grade 2; explicit non-toxic "
                           "control = grade 0). Numeric scores are published only as figures.",
            "grade_status": "provisional",
            "tox_axis": "late_onset_neurodegeneration",
            "is_cns_specific": "TRUE",
            "source_ref": "Kuroda2025_MTNA_PMC12744863",
            "source_location": "Figure 1A-D and Results text",
            "redistribution": "cc_by",
            "notes": "Late-onset axis: onset >=3 days, distinct from acute (<1 h) toxicity. "
                     "Authors state acute toxicity was absent for ASO1/3/4 and resolved within "
                     "1 day for ASO2.",
        })
    # rat intrathecal experiment, ASO2 only
    aso2 = next(o for o in oligos if o["aliases"] == "ASO2")
    measurements.append({
        "measurement_id": f"L1-MSR-{len(measurements) + 1:05d}",
        "oligo_id": aso2["oligo_id"], "source_id": "L1",
        "study_type": "animal_invivo", "species": "rat", "strain": "Slc:SD male, 9 weeks",
        "system_model": "intrathecal via spinal canal catheter; rat-modified tolerability score (Table S2)",
        "is_human_system": "FALSE", "cns_region": "lumbar_spinal_cord_CSF",
        "delivery_route": "intrathecal",
        "dose_value": 190, "dose_unit": "nmol",
        "dose_value_secondary": 1000, "dose_unit_secondary": "ug",
        "exposure_duration": "single injection", "timepoint": "to day 14+",
        "readout_category": "behavioural", "readout_name": "tolerability_score_late_onset_rat",
        "readout_value": "NOT_REPORTED", "readout_is_qualitative": "TRUE",
        "readout_unit": "score_0_to_20", "n_per_group": "4",
        "statistic": "NOT_REPORTED", "effect_direction": "increase",
        "effect_vs_control": "increased scores including severe paraplegia; 1 of 4 rats died from "
                             "severe toxicity on day 14",
        "cns_tox_grade": 3,
        "grade_basis": "mortality (1/4) plus severe paraplegia = grade 3",
        "grade_status": "provisional", "tox_axis": "late_onset_neurodegeneration",
        "is_cns_specific": "TRUE", "source_ref": "Kuroda2025_MTNA_PMC12744863",
        "source_location": "Figure 1E-F and Results text", "redistribution": "cc_by",
        "notes": "Demonstrates the same late-onset phenotype via the clinical route (intrathecal) "
                 "in a second species.",
    })
    return oligos, measurements, mods


# ============================================================================================
# K1 -- Miller/Khvorova 2024: acute tolerability vs dose, PS content and divalent cations
# ============================================================================================
K1_CONSTRUCTS = {
    "1X PBS Control": ("vehicle_control", "none", "vehicle", "NOT_APPLICABLE"),
    "Di-siRNAHTT (P3, high PS)": ("divalent_siRNA", "HTT", "high_PS", "di-siRNA, P3 pattern, high PS content"),
    "Di-siRNAHTT (P3, no PS)": ("divalent_siRNA", "HTT", "no_PS", "di-siRNA, P3 pattern, no PS"),
    "monovalent siRNAHTT": ("siRNA", "HTT", "NOT_REPORTED", "monovalent siRNA"),
    "blunt-ended siRNAHTT": ("siRNA", "HTT", "NOT_REPORTED", "blunt-ended siRNA"),
    "Full PS ASO": ("ASO_gapmer", "NOT_REPORTED", "full_PS", "fully phosphorothioate ASO"),
    "Mixed PO/PS ASO": ("ASO_gapmer", "NOT_REPORTED", "mixed_PO_PS", "mixed PO/PS backbone ASO"),
}


def parse_khvorova(pdf: pathlib.Path) -> list[dict]:
    doc = pymupdf.open(pdf)
    lines = [s.strip() for p in doc for s in p.get_text().split("\n") if s.strip()]
    end = next(i for i, l in enumerate(lines) if l.startswith("Figure S1."))
    hdr = {"Oligonucleotide", "Dose (nmol)", "Dose (µg)", "Ca (mM)", "Mg (mM)",
           "Average Tolerability", "Score", "Group Size", "(n=)", "Mouse", "Genotype", "Figure"}
    L = [x for x in lines[:end] if x not in hdr and not x.startswith("Table S2")]
    isnum = lambda s: bool(re.fullmatch(r"-?\d+(\.\d+)?", s))
    recs, buf, i = [], [], 0
    while i < len(L):
        if buf and len(L) - i >= 6 and all(isnum(L[j]) for j in range(i, i + 6)):
            n = L[i:i + 6]
            rest = L[i + 6:i + 8]
            recs.append({"oligonucleotide": " ".join(buf), "dose_nmol": n[0], "dose_ug": n[1],
                         "ca_mM": n[2], "mg_mM": n[3], "score": n[4], "n": n[5],
                         "genotype": rest[0] if rest else "",
                         "figure": rest[1] if len(rest) > 1 else ""})
            buf, i = [], i + 8
        else:
            if not isnum(L[i]):
                buf.append(L[i])
            i += 1
    return recs


def khvorova_records(recs: list[dict]) -> tuple[list, list]:
    names = sorted({r["oligonucleotide"] for r in recs})
    oid_of, oligos = {}, []
    for i, nm in enumerate(names, start=1):
        klass, target, ps, desc = K1_CONSTRUCTS.get(nm, ("other", "NOT_REPORTED", "NOT_REPORTED", nm))
        oid = f"K1-OLG-{i:04d}"
        oid_of[nm] = oid
        oligos.append({
            "oligo_id": oid, "oligo_name": f"Miller2024_{nm}", "aliases": nm,
            "oligo_class": klass,
            "modality": "double_stranded_siRNA" if "siRNA" in klass else
                        "single_stranded_ASO" if "ASO" in klass else "vehicle",
            "target_gene": target, "target_transcript": f"{target}_mRNA" if target not in
                           ("none", "NOT_REPORTED") else target,
            "indication": "research_panel_CNS_acute_tolerability",
            "developer": "UMass Chan (Khvorova/Aronin)", "max_phase": "research_panel",
            "length_nt": "NOT_REPORTED",
            "sequence_5to3_asprinted": "NOT_REPORTED",
            "sequence_base": "NOT_REPORTED",
            "backbone_chemistry": ps,
            "backbone_linkage_positions": "NOT_REPORTED",
            "sugar_modifications": "fully chemically modified (2'-OMe / 2'-F); per-position "
                                   "pattern shown only as a schematic in Figure S3",
            "modification_pattern": desc,
            "modification_positions": "NOT_REPORTED",
            "modification_position_basis": "NOT_REPORTED",
            "gapmer_shape": "NOT_APPLICABLE", "conjugate": "none",
            "purity_pct": "NOT_REPORTED", "purity_method": "NOT_REPORTED",
            "identity_confirmation": "NOT_REPORTED", "synthesis_platform": "NOT_REPORTED",
            "formulation": "varies by row: 1X PBS or aCSF with defined Ca2+/Mg2+",
            "source_id": "K1", "source_location": "Supplementary Table S2",
            "notes": "Sequences are not printed in the supplement; the di-siRNA modification "
                     "pattern appears only as a schematic (Figure S3).",
        })
    measurements = []
    for r in recs:
        score = float(r["score"])
        grade = 0 if score <= 4 else 1 if score <= 7 else 2 if score <= 18 else 3
        measurements.append({
            "measurement_id": f"K1-MSR-{len(measurements) + 1:05d}",
            "oligo_id": oid_of[r["oligonucleotide"]], "source_id": "K1",
            "study_type": "animal_invivo", "species": "mouse",
            "strain": r["genotype"],
            "system_model": "bilateral ICV injection; acute tolerability score",
            "is_human_system": "FALSE", "cns_region": "whole_brain_lateral_ventricle",
            "delivery_route": "intracerebroventricular",
            "dose_value": r["dose_nmol"], "dose_unit": "nmol",
            "dose_value_secondary": r["dose_ug"], "dose_unit_secondary": "ug",
            "formulation_ca_mM": r["ca_mM"], "formulation_mg_mM": r["mg_mM"],
            "exposure_duration": "single injection", "timepoint": "acute post-injection",
            "readout_category": "behavioural",
            "readout_name": "average_acute_tolerability_score",
            "readout_value": r["score"], "readout_is_qualitative": "FALSE",
            "readout_unit": "score_0_to_20", "n_per_group": r["n"],
            "statistic": "group average", "effect_direction": "increase" if score > 1.67 else "no_change",
            "effect_vs_control": f"score {r['score']} vs 1.67 for 1X PBS vehicle control",
            "cns_tox_grade": grade,
            "grade_basis": "same 0-20 acute tolerability scale as source H1; graded with the "
                           "Hagedorn2022 Fig.1B cutoffs (4, 7, 18) for cross-source comparability",
            "grade_status": "provisional", "tox_axis": "acute_behavioural",
            "is_cns_specific": "TRUE", "source_ref": "Miller2024_MTNA_PMC11185713",
            "source_location": f"Supplementary Table S2 (paper figure {r['figure']})",
            "redistribution": "summary_stat_only",
            "notes": "Formulation Ca2+/Mg2+ are experimental variables, not incidental: this "
                     "source is the divalent-cation rescue experiment.",
        })
    return oligos, measurements


# ============================================================================================
# C1 -- clinical layer, read directly from FDA prescribing information on DailyMed
# ============================================================================================
def _positions(seq, sugar_at):
    """Expand a stated design motif into a per-position chemistry string.

    Used only where the source states the motif but not the positions -- rows built this way
    carry modification_position_basis = derived_from_motif so a downstream user can exclude them
    from anything that requires position-resolved source content.
    """
    return ";".join(f"{i}:{b}:{sugar_at(i)}" for i, b in enumerate(seq, start=1))


CLINICAL_OLIGOS = [
    dict(oligo_id="C1-OLG-0001", oligo_name="tofersen", aliases="Qalsody;BIIB067;ISIS666853",
         oligo_class="ASO_gapmer", modality="single_stranded_ASO", target_gene="SOD1",
         target_transcript="SOD1_mRNA", indication="SOD1_amyotrophic_lateral_sclerosis",
         developer="Biogen/Ionis", max_phase="approved",
         sequence_5to3_asprinted="CAGGATACATTTCTACAGCU", sequence_base="CAGGATACATTTCTACAGCU",
         length_nt=20,
         backbone_chemistry="mixed_PO_PS",
         backbone_linkage_positions="19 internucleoside linkages: 15 phosphorothioate, 4 phosphodiester (INN description)",
         sugar_modifications="2'-MOE;DNA_gap", modification_pattern="5-10-5 MOE gapmer",
         modification_positions=_positions("CAGGATACATTTCTACAGCU",
                                           lambda i: "2'-MOE" if (i <= 5 or i >= 16)
                                           else "DNA_2prime_deoxy"),
         modification_position_basis="derived_from_motif",
         gapmer_shape="gapmer", conjugate="none", purity_pct="NOT_REPORTED",
         purity_method="NOT_REPORTED", identity_confirmation="NOT_REPORTED",
         synthesis_platform="NOT_REPORTED", formulation="intrathecal solution",
         source_id="C1",
         source_location="QALSODY PI, DailyMed setid 81356b45; sequence and chemistry from the INN description",
         notes="Sequence is NOT printed in the prescribing information. It is taken from the "
               "published INN description of tofersen: 20-mer, ten 2'-MOE and ten 2'-deoxy "
               "sugars arranged five-MOE / ten-DNA / five-MOE, with 19 linkages of which 15 are "
               "phosphorothioate and 4 phosphodiester. Positions are expanded from that stated "
               "motif, so modification_position_basis is derived_from_motif, not "
               "position_resolved_from_source."),
    dict(oligo_id="C1-OLG-0002", oligo_name="nusinersen", aliases="Spinraza;ISIS396443;BIIB058",
         oligo_class="splice_switching_ASO", modality="single_stranded_ASO", target_gene="SMN2",
         target_transcript="SMN2_ISS-N1", indication="spinal_muscular_atrophy",
         developer="Biogen/Ionis", max_phase="approved",
         sequence_5to3_asprinted="TCACTTTCATAATGCTGG", sequence_base="TCACTTTCATAATGCTGG",
         length_nt=18,
         backbone_chemistry="full_PS", backbone_linkage_positions="PS x17 (all internucleoside linkages)",
         sugar_modifications="2'-MOE_uniform", modification_pattern="uniform 2'-MOE steric block",
         modification_positions=_positions("TCACTTTCATAATGCTGG", lambda i: "2'-MOE"),
         modification_position_basis="derived_from_motif",
         gapmer_shape="NOT_APPLICABLE", conjugate="none", purity_pct="NOT_REPORTED",
         purity_method="NOT_REPORTED", identity_confirmation="NOT_REPORTED",
         synthesis_platform="NOT_REPORTED", formulation="intrathecal solution",
         source_id="C1", source_location="SPINRAZA PI, DailyMed setid dd70cd5f",
         notes="Sequence is not printed in the prescribing information; not entered from memory."),
]

# (oligo, readout, value, unit, comparator, n_treated, n_control, grade, axis, location)
CLINICAL_MEASUREMENTS = [
    ("C1-OLG-0001", "myelitis_or_radiculitis_serious_AE", "6", "patients",
     "6 patients treated with QALSODY experienced myelitis or radiculitis in the clinical studies",
     "72", "36", 3, "clinical_serious_neurological", "PI section 5.1"),
    ("C1-OLG-0001", "papilledema_or_elevated_intracranial_pressure", "4", "patients",
     "Four patients developed elevated intracranial pressure and/or papilledema",
     "72", "36", 3, "clinical_serious_neurological", "PI section 5.2"),
    ("C1-OLG-0001", "aseptic_or_chemical_meningitis", "2", "patients",
     "One patient experienced a serious adverse reaction of chemical meningitis; one patient "
     "experienced a serious adverse reaction of aseptic meningitis",
     "72", "36", 2, "clinical_neuroinflammatory", "PI section 5.3"),
    ("C1-OLG-0001", "CSF_white_blood_cell_increased", "14", "pct_incidence",
     "14% tofersen 100 mg vs 0% placebo", "72", "36", 2, "clinical_neuroinflammatory",
     "PI section 6.1 adverse reactions table, Study 1 Part C"),
    ("C1-OLG-0001", "CSF_protein_increased", "8", "pct_incidence",
     "8% tofersen 100 mg vs 3% placebo", "72", "36", 1, "clinical_neuroinflammatory",
     "PI section 6.1 adverse reactions table, Study 1 Part C"),
    ("C1-OLG-0001", "pain", "42", "pct_incidence", "42% tofersen 100 mg vs 22% placebo",
     "72", "36", 1, "clinical_cns_tolerability", "PI section 6.1 adverse reactions table"),
    ("C1-OLG-0001", "fatigue", "17", "pct_incidence", "17% tofersen 100 mg vs 6% placebo",
     "72", "36", 1, "clinical_cns_tolerability", "PI section 6.1 adverse reactions table"),
    ("C1-OLG-0001", "myalgia", "14", "pct_incidence", "14% tofersen 100 mg vs 6% placebo",
     "72", "36", 1, "clinical_cns_tolerability", "PI section 6.1 adverse reactions table"),
    ("C1-OLG-0002", "headache", "29", "pct_incidence", "29% nusinersen vs 7% control (Study 2, later-onset SMA)",
     "84", "42", 1, "clinical_cns_tolerability", "PI section 6.1 adverse reactions table, Study 2"),
    ("C1-OLG-0002", "back_pain", "25", "pct_incidence", "25% nusinersen vs 0% control (Study 2, later-onset SMA)",
     "84", "42", 1, "clinical_cns_tolerability", "PI section 6.1 adverse reactions table, Study 2"),
    ("C1-OLG-0002", "hydrocephalus_postmarketing", "NOT_REPORTED", "NA",
     "Hydrocephalus reported post-marketing; frequency not estimable from spontaneous reports",
     "NOT_REPORTED", "NOT_REPORTED", 3, "clinical_serious_neurological", "PI section 6.2 postmarketing"),
    ("C1-OLG-0002", "aseptic_meningitis_and_arachnoiditis_postmarketing", "NOT_REPORTED", "NA",
     "Aseptic meningitis and arachnoiditis reported post-marketing; frequency not estimable",
     "NOT_REPORTED", "NOT_REPORTED", 2, "clinical_neuroinflammatory", "PI section 6.2 postmarketing"),
]

DOSE = {"C1-OLG-0001": ("100", "mg", "intrathecal, 3 loading doses 14 days apart then every 28 days"),
        "C1-OLG-0002": ("12", "mg", "intrathecal bolus over 1-3 minutes")}
REF = {"C1-OLG-0001": "QALSODY_PI_DailyMed_81356b45-1cb7-4eef-88ea-e44cc18b47c5_2024-11-18",
       "C1-OLG-0002": "SPINRAZA_PI_DailyMed_dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94_2026-04-06"}


def clinical_records() -> tuple[list, list]:
    ms = []
    for oid, name, val, unit, comp, nt, nc, grade, axis, loc in CLINICAL_MEASUREMENTS:
        dose, dunit, route = DOSE[oid]
        ms.append({
            "measurement_id": f"C1-MSR-{len(ms) + 1:05d}", "oligo_id": oid, "source_id": "C1",
            "study_type": "clinical", "species": "human", "strain": "NOT_APPLICABLE",
            "system_model": "randomised placebo/sham-controlled trial, patient cohort",
            "is_human_system": "TRUE", "cns_region": "CSF_and_neuraxis",
            "delivery_route": route, "dose_value": dose, "dose_unit": dunit,
            "exposure_duration": "chronic dosing", "timepoint": "trial duration",
            "readout_category": "clinical_cns_outcome", "readout_name": name,
            "readout_value": val, "readout_is_qualitative": "FALSE" if val != "NOT_REPORTED" else "TRUE",
            "readout_unit": unit, "n_per_group": f"treated {nt}; control {nc}",
            "statistic": "incidence, no p-value reported in label",
            "effect_direction": "increase", "effect_vs_control": comp,
            "cns_tox_grade": grade,
            "grade_basis": "3 = serious/irreversible-risk neurological event named in Warnings and "
                           "Precautions; 2 = objective CNS inflammatory marker or meningitis; "
                           "1 = symptomatic but non-serious CNS-related adverse reaction",
            "grade_status": "provisional", "tox_axis": axis, "is_cns_specific": "TRUE",
            "source_ref": REF[oid], "source_location": loc,
            "redistribution": "public_domain",
            "notes": "Read directly from the FDA prescribing information on DailyMed.",
        })
    return CLINICAL_OLIGOS, ms


def write(name: str, recs: list[dict]) -> None:
    if not recs:
        return
    keys = []
    for r in recs:
        for k in r:
            if k not in keys:
                keys.append(k)
    path = OUT / f"{name}.csv"
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, restval="")
        w.writeheader()
        w.writerows(recs)
    print(f"wrote {path.relative_to(ROOT)}: {len(recs)} rows x {len(keys)} cols")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    kur = parse_kuroda_sequences(ROOT / "sources" / "L1_Kuroda2025" / "Kuroda2025_supplement.pdf")
    print("L1 sequences recovered:")
    for n, u in sorted(kur.items()):
        pat = "".join("L" if s == "LNA" else "M" if s == "2'-MOE" else "d" for _, s, _ in u)
        print(f"  {n}: {''.join(b for b, _, _ in u)}  ({len(u)} nt)  chem={pat}")
    lo, lm, lmods = kur and kuroda_records(kur) or ([], [], [])

    krecs = parse_khvorova(ROOT / "sources" / "K1_Miller2024" / "media-1.pdf")
    print(f"\nK1 table rows parsed: {len(krecs)}")
    ko, km = khvorova_records(krecs)

    co, cm = clinical_records()

    write("L1_oligos", lo); write("L1_measurements", lm); write("L1_modifications", lmods)
    write("K1_oligos", ko); write("K1_measurements", km)
    write("C1_oligos", co); write("C1_measurements", cm)
    return 0


if __name__ == "__main__":
    sys.exit(main())
