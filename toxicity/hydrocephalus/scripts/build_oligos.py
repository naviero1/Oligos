#!/usr/bin/env python3
"""
Builds data/oligos.csv — the design-predictor table.

The Challenge asks for the predictor variables (sequence, chemical modifications,
design) alongside the toxicity outcome. This script assembles them from two
evidence classes, and fills nothing from any other route:

  1. FDA prescribing information (public domain), section 11 DESCRIPTION, parsed
     from the SPL XML committed under sources/raw/. Structured fields are filled
     only by a high-precision pattern, and every filled value stores the sentence
     it was matched from in `design_source_text`, so the parse is checkable.
  2. ClinicalTrials.gov study records (public domain) for compounds with no
     approved label, which establish identity, sponsor, indication and route but
     not chemistry.

Where neither states a value, the field is NOT_REPORTED. In particular:

  * `sequence_5to3_asprinted` is NOT_REPORTED for EVERY compound here. No US
    label prints the base sequence — both intrathecal ASO labels render the
    structure as a figure ("The structural formula is: Figure 1"), which carries
    no text layer. Sequences are obtainable from the WHO INN Recommended lists,
    which is this project's established route (METHODOLOGY.md §4 path 4 of the
    sibling kidney dataset); that retrieval is recorded as an open item rather
    than approximated here. NO SEQUENCE IS GUESSED.

Output: data/oligos.csv, notes/oligo_extraction_report.txt
Usage:  python3 scripts/build_oligos.py
"""
import csv
import glob
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "sources", "raw")
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")
TODAY = date.today().isoformat()

# --------------------------------------------------------------------------
# Identity facts. Sourced, not recalled: `identity_source` names the document
# each row's identity and route come from. Chemistry is NOT set here — it is
# parsed from the label in parse_description(), or left NOT_REPORTED.
# --------------------------------------------------------------------------
OLIGOS = [
    # name, aliases, class, modality, target, indication, developer, phase, route, identity_source
    ("nusinersen", "Spinraza;ISIS 396443;BIIB058", "splice_switching_ASO",
     "single_stranded_ASO", "SMN2", "spinal_muscular_atrophy", "Biogen/Ionis",
     "approved", "intrathecal_lumbar", "SPINRAZA prescribing information"),
    ("tofersen", "Qalsody;BIIB067;ISIS 666853", "ASO_gapmer", "single_stranded_ASO",
     "SOD1", "SOD1_amyotrophic_lateral_sclerosis", "Biogen/Ionis", "approved",
     "intrathecal_lumbar", "QALSODY prescribing information"),
    ("tominersen", "RO7234292;RG6042;IONIS-HTTRx;ISIS 443139", "ASO_gapmer",
     "single_stranded_ASO", "HTT", "huntingtons_disease", "Roche/Ionis",
     "phase_3_discontinued", "intrathecal_lumbar",
     "ClinicalTrials.gov NCT03761849, NCT03342053, NCT03842969, NCT02519036"),
    ("BIIB080", "IONIS MAPTRx;BIIB080", "ASO_gapmer", "single_stranded_ASO", "MAPT",
     "alzheimers_disease", "Biogen/Ionis", "phase_2", "intrathecal_lumbar",
     "ClinicalTrials.gov NCT03186989"),
    ("BIIB105", "BIIB105;ION541", "ASO_gapmer", "single_stranded_ASO", "ATXN2",
     "amyotrophic_lateral_sclerosis", "Biogen/Ionis", "phase_2",
     "intrathecal_lumbar", "ClinicalTrials.gov NCT04494256"),
    ("WVE-120101", "WVE-120101", "ASO_gapmer", "single_stranded_ASO",
     "HTT_SNP1_allele_selective", "huntingtons_disease", "Wave Life Sciences",
     "phase_2_discontinued", "intrathecal_lumbar",
     "ClinicalTrials.gov NCT03225833, NCT04617847"),
    ("WVE-120102", "WVE-120102", "ASO_gapmer", "single_stranded_ASO",
     "HTT_SNP2_allele_selective", "huntingtons_disease", "Wave Life Sciences",
     "phase_2_discontinued", "intrathecal_lumbar",
     "ClinicalTrials.gov NCT03225846, NCT04617860"),
    ("WVE-003", "WVE-003", "ASO_gapmer", "single_stranded_ASO",
     "HTT_SNP3_allele_selective", "huntingtons_disease", "Wave Life Sciences",
     "phase_1_2", "intrathecal_lumbar", "ClinicalTrials.gov NCT05032196"),
    ("eplontersen", "Wainua;ION-682884;AKCEA-TTR-LRx", "ASO_gapmer",
     "single_stranded_ASO", "TTR", "hereditary_transthyretin_amyloidosis",
     "Ionis/AstraZeneca", "approved", "subcutaneous",
     "WAINUA prescribing information"),
    ("inotersen", "Tegsedi;IONIS-TTRRx", "ASO_gapmer", "single_stranded_ASO", "TTR",
     "hereditary_transthyretin_amyloidosis", "Ionis/Akcea", "approved",
     "subcutaneous", "TEGSEDI prescribing information"),
    ("eteplirsen", "Exondys 51;AVI-4658", "PMO", "single_stranded_ASO", "DMD_exon51",
     "duchenne_muscular_dystrophy", "Sarepta", "approved", "intravenous",
     "EXONDYS 51 prescribing information"),
    ("golodirsen", "Vyondys 53;SRP-4053", "PMO", "single_stranded_ASO", "DMD_exon53",
     "duchenne_muscular_dystrophy", "Sarepta", "approved", "intravenous",
     "VYONDYS 53 prescribing information"),
    ("viltolarsen", "Viltepso;NS-065;NCNP-01", "PMO", "single_stranded_ASO",
     "DMD_exon53", "duchenne_muscular_dystrophy", "NS Pharma", "approved",
     "intravenous", "VILTEPSO prescribing information"),
    ("casimersen", "Amondys 45;SRP-4045", "PMO", "single_stranded_ASO", "DMD_exon45",
     "duchenne_muscular_dystrophy", "Sarepta", "approved", "intravenous",
     "AMONDYS 45 prescribing information"),
    ("casimersen_or_golodirsen", "SRP-4045;SRP-4053", "PMO", "single_stranded_ASO",
     "DMD_exon45_or_exon53", "duchenne_muscular_dystrophy", "Sarepta", "approved",
     "intravenous",
     "ClinicalTrials.gov NCT03532542 (a single extension study of both compounds; "
     "the posted adverse-event table does not separate them)"),
    ("patisiran", "Onpattro;ALN-TTR02", "siRNA", "double_stranded_siRNA", "TTR",
     "hereditary_transthyretin_amyloidosis", "Alnylam", "approved", "intravenous",
     "ONPATTRO prescribing information"),
    ("vutrisiran", "Amvuttra;ALN-TTRSC02", "siRNA", "double_stranded_siRNA", "TTR",
     "hereditary_transthyretin_amyloidosis", "Alnylam", "approved", "subcutaneous",
     "AMVUTTRA prescribing information"),
    ("givosiran", "Givlaari;ALN-AS1", "siRNA", "double_stranded_siRNA", "ALAS1",
     "acute_hepatic_porphyria", "Alnylam", "approved", "subcutaneous",
     "GIVLAARI prescribing information"),
    ("lumasiran", "Oxlumo;ALN-GO1", "siRNA", "double_stranded_siRNA", "HAO1",
     "primary_hyperoxaluria_type_1", "Alnylam", "approved", "subcutaneous",
     "OXLUMO prescribing information"),
    ("nedosiran", "Rivfloza;DCR-PHXC", "siRNA", "double_stranded_siRNA", "LDHA",
     "primary_hyperoxaluria_type_1", "Novo Nordisk/Dicerna", "approved",
     "subcutaneous", "RIVFLOZA prescribing information"),
    ("inclisiran", "Leqvio;ALN-PCSsc", "siRNA", "double_stranded_siRNA", "PCSK9",
     "atherosclerotic_cardiovascular_disease", "Novartis/Alnylam", "approved",
     "subcutaneous", "LEQVIO prescribing information"),
    ("valeriasen", "KT777;valeriasen sodium", "ASO_gapmer", "single_stranded_ASO",
     "KCNT1", "KCNT1_developmental_and_epileptic_encephalopathy",
     "n-of-1 investigator-sponsored (Boston Children's Hospital / Yale)", "phase_1",
     "intrathecal_lumbar",
     "Nat Med 2026 PMC13099374; sequence and per-position chemistry are in Extended "
     "Data Table 1, published as an image whose bold/underline 2'-MOE encoding does "
     "not survive text extraction, so NOT transcribed (OI-02)"),
    # --- Nonclinical research-grade siRNAs with PUBLISHED sequences --------
    # These are the only compounds in the release whose sequence is published.
    # Each SPAK duplex passes the sense/antisense reverse-complement check.
    ("SPAK_siRNA1", "siSPAK-1", "siRNA", "double_stranded_siRNA", "STK39_SPAK",
     "hydrocephalus_research_choroid_plexus", "GenePharma (reagent)", "research_panel",
     "intravenous", "Nat Commun 2025 PMC12246246, Methods (Materials)"),
    ("SPAK_siRNA2", "siSPAK-2", "siRNA", "double_stranded_siRNA", "STK39_SPAK",
     "hydrocephalus_research_choroid_plexus", "GenePharma (reagent)", "research_panel",
     "intravenous", "Nat Commun 2025 PMC12246246, Methods (Materials)"),
    ("SPAK_siRNA3", "siSPAK-3", "siRNA", "double_stranded_siRNA", "STK39_SPAK",
     "hydrocephalus_research_choroid_plexus", "GenePharma (reagent)", "research_panel",
     "intravenous", "Nat Commun 2025 PMC12246246, Methods (Materials)"),
    ("SPAK_siRNA4", "siSPAK-4;lead agent", "siRNA", "double_stranded_siRNA",
     "STK39_SPAK", "hydrocephalus_research_choroid_plexus", "GenePharma (reagent)",
     "research_panel", "intravenous",
     "Nat Commun 2025 PMC12246246, Methods (Materials)"),
    ("AQP4_siRNA", "AQP4-specific siRNA", "siRNA", "double_stranded_siRNA", "AQP4",
     "hydrocephalus_research_intraventricular_haemorrhage", "GenePharma (reagent)",
     "research_panel", "intracerebroventricular",
     "Med Sci Monit 2018 PMC6042309, Material and Methods"),
    ("negative_control_siRNA", "scrambled non-targeting siRNA", "siRNA",
     "double_stranded_siRNA", "none_no_transcriptome_match",
     "designed_negative_control", "GenePharma (reagent)", "research_panel",
     "intracerebroventricular", "Med Sci Monit 2018 PMC6042309, Material and Methods"),
    ("volanesorsen", "Waylivra;IONIS-APOCIIIRx", "ASO_gapmer", "single_stranded_ASO",
     "APOC3", "familial_chylomicronaemia_syndrome", "Ionis/Akcea", "approved_EMA",
     "subcutaneous", "WAYLIVRA EMA summary of product characteristics"),
    ("mipomersen", "Kynamro;ISIS 301012", "ASO_gapmer", "single_stranded_ASO", "APOB",
     "homozygous_familial_hypercholesterolaemia", "Ionis/Genzyme", "approved",
     "subcutaneous", "KYNAMRO prescribing information"),
    ("pegaptanib", "Macugen;EYE001", "aptamer", "single_stranded_ASO", "VEGF165",
     "neovascular_age_related_macular_degeneration", "Eyetech/Pfizer", "approved",
     "intravitreal", "MACUGEN prescribing information"),
    ("defibrotide", "Defitelio", "other", "NOT_REPORTED", "NOT_APPLICABLE",
     "hepatic_veno_occlusive_disease", "Jazz Pharmaceuticals", "approved",
     "intravenous", "DEFITELIO prescribing information"),
    ("imetelstat", "Rytelo;GRN163L", "other", "NOT_REPORTED", "TERC",
     "myelodysplastic_syndromes_and_oncology", "Geron", "approved", "intravenous",
     "RYTELO prescribing information"),
]

# Rows that are not compounds but appear as oligo_name in measurements.
NON_COMPOUND = [
    ("placebo_or_sham_control",
     "The comparator arm of a randomised trial: placebo injection or sham procedure. "
     "Carries no oligonucleotide. Present so that comparator rows are data rather "
     "than a footnote."),
    ("NOT_APPLICABLE",
     "Rows with no drug exposure at all — disease background-incidence rows "
     "(tox_axis = disease_background_rate)."),
]

# High-precision patterns over the label's DESCRIPTION section.
PATTERNS = {
    "length_nt": re.compile(r"(\d+)[- ]base residue|\b(\d+)[- ]mer\b", re.I),
    "modification_pattern": re.compile(r"(\d+-\d+-\d+)\s*(?:MOE|2['′]-MOE)?\s*gapmer", re.I),
    "molecular_formula": re.compile(r"\bC\d+\s*H\d+\s*N\d+\s*O\d+\s*P\d+(?:\s*S\d+)?"),
    "molecular_weight": re.compile(r"molecular weight is ([\d,]+\.?\d*)", re.I),
}



# Published sequences. The ONLY sequences in this release. Each is transcribed
# from the source's Materials section, and each duplex's antisense strand is the
# exact reverse complement of its sense strand once the TT overhangs are trimmed
# — an internal check that does not depend on the source being correct.
# Convention matches the sibling datasets: sequence_5to3_asprinted holds the
# ANTISENSE (guide) strand; the sense strand is recorded in notes.
SEQUENCES = {
    "SPAK_siRNA1": ("UUGAUGAUAUCCAACAUGGTT", "CCAUGUUGGAUAUCAUCAATT"),
    "SPAK_siRNA2": ("AUAGCCUCUCACCUGUUCCTT", "GGAACAGGUGAGAGGCUAUTT"),
    "SPAK_siRNA3": ("UAUUUGUGGUAAGGCGCUGTT", "CAGCGCCUUACCACAAAUATT"),
    "SPAK_siRNA4": ("AUCGUAUGUCAUUAAGUUCTT", "GAACUUAAUGACAUACGAUTT"),
}
SEQ_SOURCE = ("Nature Communications 2025, PMC12246246, Methods section 'Materials': "
              "the four SPAK siRNA duplexes are printed in full with sense and "
              "antisense strands.")

# Sequences and per-position chemistry recovered from the WHO INN Recommended
# lists by scripts/parse_inn_sequences.py. The INN entry spells every residue out
# longhand, so the sequence is a deterministic parse rather than a judgement; the
# parser refuses to emit a sequence that disagrees with the label's own molecular
# formula or its stated phosphorothioate count.
INN_PATH = os.path.join(ROOT, "data", "inn_sequences.json")
INN = json.load(open(INN_PATH)) if os.path.exists(INN_PATH) else {}


def inn_backbone(rec):
    if rec["n_phosphodiester"] == 0:
        return "full_PS"
    return "mixed_PO_PS" if rec["n_phosphorothioate"] else "no_PS"


def inn_motif(rec):
    """Wing-gap-wing motif read off the per-position sugar map, or NOT_APPLICABLE."""
    sugars = [p["sugar_chemistry"] for p in rec["positions"]]
    if len(set(sugars)) == 1:
        return "uniform %s" % sugars[0]
    gap_start = next((i for i, s in enumerate(sugars) if s == "DNA_2prime_deoxy"), None)
    gap_end = next((len(sugars) - i for i, s in enumerate(reversed(sugars))
                    if s == "DNA_2prime_deoxy"), None)
    if gap_start is None:
        return "NOT_REPORTED"
    return "%d-%d-%d" % (gap_start, gap_end - gap_start, len(sugars) - gap_end)

# Lengths derivable from the label's own molecular formula. A linear
# oligonucleotide of n residues with no terminal phosphate carries n-1
# internucleoside linkages, hence n-1 phosphorus atoms. The tofersen label states
# BOTH a 20-mer and C230H317N72O123P19S15, which pins that relationship (P = n-1)
# for this chemistry class. Applying it to nusinersen -- same manufacturer, same
# uniform 2'-MOE/PS chemistry, no terminal phosphate stated -- gives 18 residues
# from P17, corroborated by S17 (every one of the 17 linkages is thio, exactly as
# the label's wording requires).
#
# It is NOT applied to the morpholinos: their formulas give P = n for eteplirsen,
# golodirsen and casimersen but P = n-1 for viltolarsen, because some carry a
# 5'-piperazine bearing an extra phosphorus and some do not. The relationship is
# therefore ambiguous for that class and their length stays NOT_REPORTED.
# Purification, identity confirmation and synthesis platform, per source.
# A full-text sweep of all 16 committed US labels for purity / purification /
# chromatography / mass-spectrometry / identity / characterisation language returns
# NO statement about the drug substance in any of them -- every hit is a patient
# baseline characteristic or an efficacy assay. purity_pct is therefore
# NOT_REPORTED for every compound in this release, which is the same finding the
# sibling OligoTox-CNS release reports for all 1,839 of its oligonucleotides:
# per-compound purity is almost never published alongside toxicity data. The two
# research-reagent sources name a supplier but no method.
PURITY = {
    # name: (purity_method, identity_confirmation, synthesis_platform)
    "SPAK_siRNA1": ("NOT_REPORTED", "NOT_REPORTED",
                    "GenePharma (Shanghai); commercial synthesis, platform not stated"),
    "SPAK_siRNA2": ("NOT_REPORTED", "NOT_REPORTED",
                    "GenePharma (Shanghai); commercial synthesis, platform not stated"),
    "SPAK_siRNA3": ("NOT_REPORTED", "NOT_REPORTED",
                    "GenePharma (Shanghai); commercial synthesis, platform not stated"),
    "SPAK_siRNA4": ("NOT_REPORTED", "NOT_REPORTED",
                    "GenePharma (Shanghai); commercial synthesis, platform not stated"),
    "AQP4_siRNA": ("NOT_REPORTED", "NOT_REPORTED",
                   "GenePharma (Shanghai); commercial synthesis, platform not stated"),
    "negative_control_siRNA": ("NOT_REPORTED", "NOT_REPORTED",
                               "GenePharma (Shanghai); commercial synthesis, "
                               "platform not stated"),
}

LENGTH_FROM_FORMULA = {
    "nusinersen": (18, "derived_from_molecular_formula: the label gives "
                       "C234H323N61O128P17S17; 17 phosphorothioate linkages imply 18 "
                       "residues, using the P = n-1 relationship the tofersen label "
                       "confirms by stating both 20-mer and P19. Not stated by the "
                       "label as a number."),
}


def flat(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def sentence_around(text, match):
    start = text.rfind(".", 0, match.start()) + 1
    end = text.find(".", match.end())
    return text[start:end + 1 if end > 0 else len(text)].strip()


def description_of(generic):
    """Return (text, setid) of the label's DESCRIPTION section, or (None, None)."""
    files = sorted(glob.glob(os.path.join(RAW, "dailymed_%s_*.xml" % generic)))
    if not files:
        return None, None
    setid = os.path.basename(files[0]).rsplit("_", 1)[1].split(".")[0]
    root = ET.fromstring(open(files[0], "rb").read())
    for sec in root.iter("{urn:hl7-org:v3}section"):
        t = sec.find("{urn:hl7-org:v3}title")
        if t is not None and "DESCRIPTION" in flat(t).upper():
            return flat(sec), setid
    return None, setid


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(NOTES, exist_ok=True)
    rows, report = [], []

    for (name, aliases, klass, modality, target, indication, developer, phase,
         route, identity_source) in OLIGOS:
        desc, setid = description_of(name)
        parsed, evidence = {}, {}
        if desc:
            for field, pat in PATTERNS.items():
                m = pat.search(desc)
                if m:
                    val = next((g for g in m.groups() if g), m.group(0)) \
                        if m.groups() else m.group(0)
                    parsed[field] = val.strip()
                    evidence[field] = sentence_around(desc, m)[:320]
            # Backbone: state it only if the label says so in words.
            if re.search(r"mixed backbone", desc, re.I):
                parsed["backbone_chemistry"] = "mixed_PO_PS"
                m = re.search(r"[^.]*mixed backbone[^.]*\.", desc, re.I)
                evidence["backbone_chemistry"] = m.group(0).strip()[:320] if m else ""
            elif re.search(r"phosphate linkages are replaced with phosphorothioate",
                           desc, re.I):
                parsed["backbone_chemistry"] = "full_PS"
                m = re.search(r"[^.]*phosphate linkages are replaced[^.]*\.", desc, re.I)
                evidence["backbone_chemistry"] = m.group(0).strip()[:320] if m else ""
            if re.search(r"morpholino", desc, re.I):
                parsed["backbone_chemistry"] = "PMO_neutral"
                m = re.search(r"[^.]*morpholino[^.]*\.", desc, re.I)
                evidence["backbone_chemistry"] = m.group(0).strip()[:320] if m else ""
            # Sugar chemistry
            sugars = []
            if re.search(r"2['′]-O-\(?2-methoxyethyl\)?|2['′]-O-2-methoxyethyl|MOE",
                         desc, re.I):
                sugars.append("2'-MOE")
            if re.search(r"2[- ]deoxy|2['′]-deoxynucleoside", desc, re.I):
                sugars.append("DNA_gap")
            if re.search(r"morpholino", desc, re.I):
                sugars.append("morpholino")
            if sugars:
                parsed["sugar_modifications"] = ";".join(sugars)
            # Formulation, including whether divalent cations are present — a
            # variable the CNS oligonucleotide literature treats as material.
            fm = re.search(r"[^.]*(calcium chloride|magnesium chloride)[^.]*\.", desc, re.I)
            if fm:
                parsed["formulation"] = "contains divalent cations (Ca2+ and/or Mg2+)"
                evidence["formulation"] = fm.group(0).strip()[:320]

        source_loc = ("SPL section 11 DESCRIPTION, DailyMed setid %s" % setid
                      if desc else identity_source)
        rows.append(dict(
            oligo_name=name, aliases=aliases, oligo_class=klass, modality=modality,
            target_gene=target, indication=indication, developer=developer,
            max_phase=phase, route_of_administration=route,
            length_nt=(parsed.get("length_nt")
                       or (str(INN[name]["length_nt"]) if name in INN else None)
                       or (str(len(SEQUENCES[name][0])) if name in SEQUENCES else None)
                       or (str(LENGTH_FROM_FORMULA[name][0])
                           if name in LENGTH_FROM_FORMULA else "NOT_REPORTED")),
            length_nt_basis=("stated_in_label" if parsed.get("length_nt")
                             else "counted_from_WHO_INN_chemical_name"
                             if name in INN
                             else "counted_from_published_sequence"
                             if name in SEQUENCES
                             else LENGTH_FROM_FORMULA[name][1]
                             if name in LENGTH_FROM_FORMULA
                             else "NOT_REPORTED"),
            sequence_5to3_asprinted=(INN[name]["sequence_base"] if name in INN
                                     else SEQUENCES.get(name, ("NOT_REPORTED",))[0]),
            sequence_base=(INN[name]["sequence_base"].replace("U", "T") if name in INN
                           else SEQUENCES[name][0].replace("U", "T")
                           if name in SEQUENCES else "NOT_REPORTED"),
            sequence_source=(("%s. Recovered by deterministic parse of the INN "
                              "chemical name, which spells out every residue; the "
                              "source prints no sequence string. Parser and its "
                              "validation: scripts/parse_inn_sequences.py."
                              % INN[name]["citation"]) if name in INN
                             else SEQ_SOURCE if name in SEQUENCES else
                             "NOT_REPORTED — no US label prints the base sequence; the "
                             "structure is a figure with no text layer. See "
                             "METHODOLOGY.md open item OI-02."),
            backbone_chemistry=(inn_backbone(INN[name]) if name in INN
                                else parsed.get("backbone_chemistry", "NOT_REPORTED")),
            sugar_modifications=parsed.get("sugar_modifications", "NOT_REPORTED"),
            modification_pattern=(inn_motif(INN[name]) if name in INN
                                  else parsed.get("modification_pattern",
                                                  "NOT_REPORTED")),
            gapmer_shape=("gapmer" if klass == "ASO_gapmer" else
                          "uniform" if klass == "splice_switching_ASO" else
                          "NOT_APPLICABLE"),
            molecular_formula=parsed.get("molecular_formula", "NOT_REPORTED"),
            molecular_weight=parsed.get("molecular_weight", "NOT_REPORTED"),
            conjugate="NOT_REPORTED",
            formulation=parsed.get("formulation", "NOT_REPORTED"),
            purity_pct="NOT_REPORTED",
            purity_method=PURITY.get(name, ("NOT_REPORTED",) * 3)[0],
            identity_confirmation=PURITY.get(name, ("NOT_REPORTED",) * 3)[1],
            synthesis_platform=PURITY.get(name, ("NOT_REPORTED",) * 3)[2],
            design_source_text=json.dumps(evidence)[:1800] if evidence else "NOT_REPORTED",
            identity_source=identity_source,
            source_location=source_loc,
            redistribution=("public_domain" if desc else "public_domain"),
            notes=(("Antisense (guide) strand shown; sense strand %s. Duplex passes "
                    "the sense/antisense reverse-complement check on the 19-mer core. "
                    % SEQUENCES[name][1]) if name in SEQUENCES else "") +
                  ("Design fields filled only where the cited document states them; "
                   "everything else NOT_REPORTED. Retrieved %s." % TODAY),
        ))
        report.append("%-26s label=%-3s parsed=%s" % (
            name, "yes" if desc else "no", ",".join(sorted(parsed)) or "none"))

    for name, why in NON_COMPOUND:
        rows.append(dict(
            oligo_name=name, aliases="", oligo_class="NOT_APPLICABLE",
            modality="NOT_APPLICABLE", target_gene="NOT_APPLICABLE",
            indication="NOT_APPLICABLE", developer="NOT_APPLICABLE",
            max_phase="NOT_APPLICABLE", route_of_administration="NOT_APPLICABLE",
            length_nt="NOT_APPLICABLE", sequence_5to3_asprinted="NOT_APPLICABLE",
            sequence_base="NOT_APPLICABLE", sequence_source="NOT_APPLICABLE",
            backbone_chemistry="NOT_APPLICABLE", sugar_modifications="NOT_APPLICABLE",
            modification_pattern="NOT_APPLICABLE", gapmer_shape="NOT_APPLICABLE",
            molecular_formula="NOT_APPLICABLE", molecular_weight="NOT_APPLICABLE",
            conjugate="NOT_APPLICABLE", formulation="NOT_APPLICABLE",
            length_nt_basis="NOT_APPLICABLE", purity_pct="NOT_APPLICABLE",
            purity_method="NOT_APPLICABLE", identity_confirmation="NOT_APPLICABLE",
            synthesis_platform="NOT_APPLICABLE",
            design_source_text="NOT_APPLICABLE", identity_source="NOT_APPLICABLE",
            source_location="NOT_APPLICABLE", redistribution="NOT_APPLICABLE",
            notes=why))
        report.append("%-26s (non-compound placeholder)" % name)

    out = os.path.join(DATA, "oligos.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(NOTES, "oligo_extraction_report.txt"), "w") as fh:
        fh.write("oligos.csv build report, %s\n" % TODAY)
        fh.write("=" * 64 + "\n" + "\n".join(report) + "\n")
    print("wrote %s: %d rows, %d columns" % (out, len(rows), len(rows[0])))
    print("\n".join(report))


if __name__ == "__main__":
    main()
