#!/usr/bin/env python3
"""Merge every staged per-source table into the released OligoTox-CNS dataset.

Reads   data/staged/*_oligos.csv, *_measurements.csv, *_modifications.csv
Writes  one data/ per toxicity endpoint, under toxicity/<endpoint>/data/ --
        acute-neurotoxicity, chronic-neurotoxicity and hydrocephalus.

The endpoint folders are the source of truth; there is deliberately no combined master table,
so a folder cannot drift from one. src/endpoints.py owns the allocation rule and the union
loader that consumers use when they need the whole CNS picture.

The canonical column order defined here IS the schema; docs/DATA_DICTIONARY.md is generated
from the same definitions by src/make_docs.py, so the two can never drift apart.

Missing-value policy (see OPEN_ITEMS.md OI-02/OI-03):
  NOT_REPORTED     the source does not report this value
  NOT_APPLICABLE   the field has no meaning for this row (e.g. gap length of a vehicle control)
  (empty)          the field is not applicable to this table's row type
Nothing is ever estimated, interpolated or filled from background knowledge.
"""
from __future__ import annotations

import csv
import pathlib
import sys

import endpoints

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGED = ROOT / "data" / "staged"
DATA = ROOT / "data"

# ------------------------------------------------------------------ canonical schemas
OLIGO_COLUMNS = [
    ("oligo_id", "Primary key. Stable identifier, prefixed with the source id."),
    ("oligo_name", "Human-readable name."),
    ("aliases", "Other names, semicolon separated."),
    ("oligo_class", "ASO_gapmer | ASO_mixmer | splice_switching_ASO | siRNA | divalent_siRNA | vehicle_control | other"),
    ("modality", "single_stranded_ASO | double_stranded_siRNA | vehicle"),
    ("target_gene", "Intended target gene symbol, or none_no_transcriptome_match for scrambles."),
    ("target_transcript", "Target transcript where stated."),
    ("indication", "Disease or research context."),
    ("developer", "Originating organisation."),
    ("max_phase", "Highest development phase reached, or research_panel."),
    ("length_nt", "Length in nucleotides."),
    ("sequence_5to3_asprinted", "Sequence EXACTLY as printed by the source, preserving any case convention that encodes chemistry."),
    ("sequence_base", "Nucleobase sequence, upper case, chemistry stripped."),
    ("backbone_chemistry", "full_PS | mixed_PO_PS | no_PS | NOT_REPORTED"),
    ("backbone_linkage_positions", "Per-linkage backbone description where derivable."),
    ("sugar_modifications", "Sugar chemistry summary."),
    ("modification_pattern", "The design motif in the source's own terms, e.g. 3-10-3_LNA_gapmer."),
    ("modification_positions", "Per-position chemistry, 5'->3', as position:base:sugar[:base-mod] tokens. THE CHALLENGE'S 'location of all chemical modifications' FIELD."),
    ("modification_position_basis", "position_resolved_from_source | position_resolved_from_source_typeface | derived_from_motif | NOT_REPORTED"),
    ("n_lna", "Count of LNA sugars."),
    ("n_moe", "Count of 2'-MOE sugars."),
    ("n_dna", "Count of 2'-deoxy (DNA) sugars."),
    ("n_5methyl_C", "Count of 5-methylcytosine bases where the source marks them."),
    ("gap_length_nt", "DNA gap length for gapmers."),
    ("flank5_len_nt", "5' wing length."),
    ("flank3_len_nt", "3' wing length."),
    ("gapmer_shape", "gapmer | mixmer | NOT_APPLICABLE"),
    ("conjugate", "Conjugated moiety, or none."),
    ("ps_linkage_count", "Number of phosphorothioate linkages."),
    ("n_A", "Adenine count."), ("n_C", "Cytosine count."),
    ("n_G", "Guanine count."), ("n_T", "Thymine count."),
    ("gc_content_pct", "G+C percentage."),
    ("longest_g_run", "Longest consecutive run of G."),
    ("g_free_3prime_len", "Nucleotides from the 3' end containing no G (capped at 20; 20 if no G). Hagedorn's published predictor term."),
    ("purity_pct", "Reported purity percentage, or NOT_REPORTED. See OPEN_ITEMS OI-02."),
    ("purity_method", "Purification method, verbatim from the source's Methods, or NOT_REPORTED."),
    ("identity_confirmation", "How identity was confirmed (e.g. RP-UPLC-MS), verbatim, or NOT_REPORTED."),
    ("synthesis_platform", "Synthesiser/chemistry platform, or NOT_REPORTED."),
    ("formulation", "Vehicle the oligo was dosed in."),
    ("dataset_split_asPublished", "The source's own train/test/validate/control label, where it has one."),
    ("source_id", "Foreign key to sources.csv."),
    ("source_location", "Exact table/figure within the source."),
    ("notes", "Free text."),
]

MEASUREMENT_COLUMNS = [
    ("measurement_id", "Primary key."),
    ("oligo_id", "Foreign key to oligos.csv."),
    ("source_id", "Foreign key to sources.csv."),
    ("study_type", "in_vitro | animal_invivo | clinical | ex_vivo"),
    ("species", "human | mouse | rat | monkey | multi_species"),
    ("strain", "Strain, sex and age where stated."),
    ("system_model", "The experimental system and instrument."),
    ("is_human_system", "TRUE if the measurement was made in a human or in human-derived cells. The challenge prioritises these."),
    ("cns_region", "CNS compartment measured."),
    ("delivery_route", "intracerebroventricular | intrathecal | in_culture_medium | ..."),
    ("dose_value", "Dose or concentration."),
    ("dose_unit", "Unit of dose_value."),
    ("dose_value_secondary", "Second dose expression where the source gives one."),
    ("dose_unit_secondary", "Unit of dose_value_secondary."),
    ("formulation_ca_mM", "Ca2+ in the injectate (mM). An experimental variable in source K1."),
    ("formulation_mg_mM", "Mg2+ in the injectate (mM). An experimental variable in source K1."),
    ("exposure_duration", "Duration of exposure."),
    ("timepoint", "When the readout was taken."),
    ("readout_category", "behavioural | electrophysiology_calcium | histopathology | injury_biomarker | functional | viability | accumulation | clinical_cns_outcome"),
    ("readout_name", "Name of the specific readout."),
    ("readout_value", "The value EXACTLY as reported, or NOT_REPORTED."),
    ("readout_is_qualitative", "TRUE where the source reports the result only in words or only as a figure."),
    ("readout_unit", "Unit of readout_value."),
    ("n_per_group", "Group size as stated."),
    ("statistic", "Dispersion/significance as stated."),
    ("effect_direction", "increase | decrease | no_change"),
    ("effect_vs_control", "The comparison as stated, including the comparator value."),
    ("cns_tox_grade", "Ordinal severity 0-3. Blank where the readout is continuous and not graded."),
    ("grade_basis", "The exact rule that produced the grade."),
    ("grade_status", "provisional | expert_confirmed | not_graded"),
    ("tox_axis", "acute_behavioural | acute_neuronal_excitability | late_onset_neurodegeneration | clinical_neuroinflammatory | clinical_serious_neurological | clinical_cns_tolerability"),
    ("is_cns_specific", "TRUE for every row in this dataset."),
    ("source_ref", "Citation key."),
    ("source_location", "Exact table/figure within the source."),
    ("redistribution", "cc_by | cc_by_nc | public_domain | summary_stat_only"),
    ("notes", "Free text."),
]

MODIFICATION_COLUMNS = [
    ("oligo_id", "Foreign key to oligos.csv."),
    ("position_5to3", "1-based position from the 5' end."),
    ("nucleobase", "A | C | G | T"),
    ("sugar_chemistry", "LNA | 2'-MOE | DNA_2prime_deoxy"),
    ("base_modification", "5-methylcytosine | none"),
    ("linkage_3prime", "Linkage to the next nucleotide, or terminal_none at the 3' end."),
    ("basis", "How the position was established."),
    ("source_id", "Foreign key to sources.csv."),
]

SOURCES = [
    dict(source_id="H1", source_key="Hagedorn_2022",
         citation="Hagedorn PH, Brown JM, Easton A, Pierdomenico M, Jones K, Olson RE, Mercer SE, "
                  "Li D, Loy J, Hog AM, Jensen ML, Gill M, Cacace AM. Acute Neurotoxicity of "
                  "Antisense Oligonucleotides After Intracerebroventricular Injection Into Mouse "
                  "Brain Can Be Predicted from Sequence Features. Nucleic Acid Ther. "
                  "2022 Jun;32(3):151-162.",
         first_author="Hagedorn PH", year="2022", journal="Nucleic Acid Therapeutics",
         doi="10.1089/nat.2021.0071", pmid="35166597", pmcid="PMC9221153",
         url="https://pmc.ncbi.nlm.nih.gov/articles/PMC9221153/",
         access="open_access", license="CC BY 4.0", redistribution="cc_by",
         evidence_tier="primary_supplementary_data",
         retrieved_via="Europe PMC supplementaryFiles REST endpoint",
         notes="Supplementary Table S1. Sequence case encodes LNA (upper) vs DNA (lower); "
               "all backbones full PS."),
    dict(source_id="K1", source_key="Miller_2024",
         citation="Miller BR, Paquette JD, Barker AR, et al. Chemical and physical variables "
                  "influencing the acute tolerability of oligonucleotides delivered to the CNS. "
                  "Mol Ther Nucleic Acids. 2024;35(2):102359.",
         first_author="Miller BR", year="2024", journal="Molecular Therapy Nucleic Acids",
         doi="10.1016/j.omtn.2024.102359", pmid="", pmcid="PMC11185713",
         url="https://pmc.ncbi.nlm.nih.gov/articles/PMC11185713/",
         access="open_access", license="CC BY-NC", redistribution="cc_by_nc",
         evidence_tier="primary_supplementary_data",
         retrieved_via="Europe PMC supplementaryFiles REST endpoint",
         notes="Supplementary Table S2: per-group acute tolerability scores with injectate "
               "Ca2+/Mg2+ as experimental variables."),
    dict(source_id="L1", source_key="Kuroda_2025",
         citation="Kuroda T, Yoshioka K, Lei Mon SS, Katsuyama M, Sato K, Isogai E, "
                  "Yoshida-Tanaka K, Iwata-Hara R, Yamaguchi T, Obika S, Yokota T. Unraveling and "
                  "controlling late-onset neurotoxicity of antisense oligonucleotides through "
                  "strategic chemical modifications. Mol Ther Nucleic Acids. 2025;36.",
         first_author="Kuroda T", year="2025", journal="Molecular Therapy Nucleic Acids",
         doi="10.1016/j.omtn.2025.102692", pmid="", pmcid="PMC12744863",
         url="https://pmc.ncbi.nlm.nih.gov/articles/PMC12744863/",
         access="open_access", license="CC BY-NC", redistribution="cc_by_nc",
         evidence_tier="primary_supplementary_data",
         retrieved_via="Europe PMC supplementaryFiles REST endpoint",
         notes="Supplementary Table S1 encodes chemistry in typeface; recovered by parsing PDF "
               "span styling. Behavioural scores are published only as figures."),
    dict(source_id="C1", source_key="FDA_PI_DailyMed",
         citation="QALSODY (tofersen) prescribing information, Biogen Inc., DailyMed setid "
                  "81356b45-1cb7-4eef-88ea-e44cc18b47c5, published 2024-11-18. SPINRAZA "
                  "(nusinersen) prescribing information, Biogen Inc., DailyMed setid "
                  "dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94, published 2026-04-06.",
         first_author="US FDA / Biogen Inc.", year="2024/2026", journal="FDA prescribing information",
         doi="", pmid="", pmcid="",
         url="https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=81356b45-1cb7-4eef-88ea-e44cc18b47c5",
         access="public_domain", license="US Government work / public domain",
         redistribution="public_domain", evidence_tier="regulatory_primary",
         retrieved_via="DailyMed, read directly",
         notes="Human clinical CNS adverse-event anchors for the two approved intrathecal ASOs."),
    dict(source_id="O1", source_key="ORourke_2026",
         citation="O'Rourke JJ, Bravo-Hernandez M, et al. Acute neuronal inhibition response "
                  "caused by phosphorothioate antisense oligonucleotides following local delivery "
                  "to the central nervous system. Nucleic Acids Res. 2026;54(3):gkaf1333.",
         first_author="O'Rourke JJ", year="2026", journal="Nucleic Acids Research",
         doi="10.1093/nar/gkaf1333", pmid="41494985", pmcid="PMC12865454",
         url="https://academic.oup.com/nar/article/54/3/gkaf1333/8415850",
         access="open_access", license="CC BY-NC", redistribution="cc_by_nc",
         evidence_tier="primary_fulltext_instruments_only",
         retrieved_via="Europe PMC supplementaryFiles REST endpoint",
         notes="Contributes measurement INSTRUMENTS (rodent IT, rodent ICV and NHP IT acute "
               "inhibition scales) documented in docs/SCORING_INSTRUMENTS.md, and the finding "
               "that divalent cations do NOT mitigate acute INHIBITION -- which stands in "
               "tension with source K1's rescue of acute ACTIVATION. No per-oligo rows "
               "extracted: the supplement does not print per-ASO sequences with scores."),
]


def read(pattern: str) -> list[dict]:
    rows = []
    for p in sorted(STAGED.glob(pattern)):
        with p.open() as fh:
            rows.extend(csv.DictReader(fh))
    return rows


def normalise(rows: list[dict], columns: list[tuple[str, str]]) -> list[dict]:
    names = [c for c, _ in columns]
    out = []
    for r in rows:
        extra = set(r) - set(names)
        if extra:
            raise SystemExit(f"column(s) not in canonical schema: {sorted(extra)}")
        out.append({c: r.get(c, "") for c in names})
    return out


def write(path: pathlib.Path, rows: list[dict], columns: list[tuple[str, str]]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[c for c, _ in columns])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path.relative_to(ROOT)}: {len(rows)} rows x {len(columns)} cols")


def main() -> int:
    oligos = normalise(read("*_oligos.csv"), OLIGO_COLUMNS)
    meas = normalise(read("*_measurements.csv"), MEASUREMENT_COLUMNS)
    mods = normalise(read("*_modifications.csv"), MODIFICATION_COLUMNS)

    oligos.sort(key=lambda r: r["oligo_id"])
    meas.sort(key=lambda r: r["measurement_id"])
    mods.sort(key=lambda r: (r["oligo_id"], int(r["position_5to3"])))

    # fill per-source counts on the source registry
    import collections
    no = collections.Counter(r["source_id"] for r in oligos)
    nm = collections.Counter(r["source_id"] for r in meas)
    srcs = [dict(s, n_oligos=no.get(s["source_id"], 0), n_measurements=nm.get(s["source_id"], 0))
            for s in SOURCES]

    columns = {"oligos": [c for c, _ in OLIGO_COLUMNS],
               "measurements": [c for c, _ in MEASUREMENT_COLUMNS],
               "modifications": [c for c, _ in MODIFICATION_COLUMNS],
               "sources": list(srcs[0].keys())}
    counts = endpoints.write_split(oligos, meas, mods, srcs, columns)

    print("per-endpoint data written to toxicity/<endpoint>/data/:")
    for ep in endpoints.ENDPOINTS:
        c = counts[ep]
        listed = "listed in the brief" if endpoints.LISTED_IN_BRIEF[ep] else "NOT a listed endpoint"
        print(f"  {ep:<24} oligos={c['oligos']:>5}  measurements={c['measurements']:>5}  "
              f"modifications={c['modifications']:>6}  sources={c['sources']}   ({listed})")
    total = sum(c["measurements"] for c in counts.values())
    assert total == len(meas), f"split lost rows: {total} != {len(meas)}"
    print(f"  {'TOTAL':<24} measurements={total} (every assembled row allocated exactly once)")

    print("\nper-source contribution:")
    for s in srcs:
        print(f"  {s['source_id']} {s['source_key']:<18} oligos={s['n_oligos']:>5}  "
              f"measurements={s['n_measurements']:>5}  licence={s['license']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
