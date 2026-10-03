#!/usr/bin/env python3
"""Stage Sewing et al. 2016 (PLoS One 11:e0159431) at experiment-condition grain.

RAW TRANSFER ONLY. This script performs the transfer permitted by SCIENTIFIC_RULES.md §A:
rows move into a staging schema with source lineage preserved. It assigns no toxicity label,
imputes no missing value, manufactures no negative and resolves no scientific conflict.
Nothing it emits is ingested, promoted or released; schema is gated on the Tier 0 crosswalk
and anything scientific is gated on German.

Source:   Sewing S, Boess F, Moisan A, Bertinetti-Lapatki C, Minz T, Hedtjaern M, Tessier Y,
          Schuler F, Singer T, Roth AB. "Establishment of a Predictive In Vitro Assay for
          Assessment of the Hepatotoxic Potential of Oligonucleotide Drugs."
          PLoS One 2016;11(7):e0159431. doi:10.1371/journal.pone.0159431. PMCID PMC4956313.
Licence:  CC BY (Europe PMC `license: cc by`; article states the Creative Commons Attribution
          License permitting unrestricted use, distribution and reproduction with credit).
Read by:  Table 1 and Figure 8 read visually from the publisher's renders. Both are printed
          tables; no value here is digitised off a plot axis.

Grain emitted: oligo x dose x exposure time x cell system x species x endpoint.
Per SCIENTIFIC_RULES.md §B the canonical oligo table and the observation table stay separate.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))

DOI = "10.1371/journal.pone.0159431"
URL = "https://europepmc.org/article/MED/27442522"
LICENCE = "CC BY"
PAPER_GROUP = "sewing2016_pone0159431"

# --- Table 1, read visually from Sewing2016_Table1_sequences.tif (1572x623, 2x upscale) ---
# Notation per the table's own footnote: lowercase = DNA nucleotides; CAPITALS = beta-oxy LNA;
# mC = methylated cytosine; subscript s = phosphorothioate backbone linkage.
# Tokens below preserve that notation: "mC" = 5-methyl-C, case carries the sugar.
TABLE1 = {
    "32": ("mC A A a g g a a a c a c a mC A T", 64.0),
    "33": ("mC A A a t g c t g a a a c T A T", 59.0),
    "35": ("mC T mC a a c a t c a a g c A G T", 67.0),
    "36": ("A mC T g c t t t c c a c t mC T G", 1889.0),
    "37": ("G mC mC t c c c a g t t c c T T T", 2368.0),
    "43": ("G A T g c c t c c c a G T T", 1890.0),
    "47": ("G A c a t t g c c t mC T A", None),  # ND: group sacrificed early (severe toxicity)
}

# Independently verified character-for-character against Dieckmann 2018 Table 1 after the
# documented E -> 5-methyl-C substitution. Recorded as a sequence-level crosswalk only:
# a shared base sequence is NOT evidence of identical administered material (§G).
DIECKMANN_SEQ_MATCH = {"32": "LNA32", "33": "LNA33", "37": "LNA37", "43": "LNA43"}


def parse(tokens):
    """Return (plain_sequence, sugar_by_pos, base_mod_by_pos, wing_design)."""
    seq, sugar, basemod = [], [], []
    for t in tokens.split():
        methyl = t.startswith("m")
        letter = t[1:] if methyl else t
        seq.append(letter.upper())
        sugar.append("LNA_betaD_oxy" if letter.isupper() else "DNA")
        basemod.append("5-methyl-C" if methyl else "none")
    # wing design = leading LNA run / DNA gap / trailing LNA run
    lead = 0
    while lead < len(sugar) and sugar[lead] != "DNA":
        lead += 1
    trail = 0
    while trail < len(sugar) and sugar[len(sugar) - 1 - trail] != "DNA":
        trail += 1
    gap = len(sugar) - lead - trail
    return "".join(seq), "|".join(sugar), "|".join(basemod), f"{lead}-{gap}-{trail}", gap


# --- Figure 8, read visually from Sewing2016_Fig8_mouse_human_hepatocytes.jpg ---
# Fig 8 is a printed numeric heat-map table; every value below is printed in the source.
# Panel A: the 7 myd88 tool SSOs in HUMAN hepatocytes.
# Panel B: 2 clinical-stage SSOs in MOUSE hepatocytes. Panel C: the same 2 in HUMAN.
# "Data are means from 2 experiments in triplicates" (Fig 8 legend) -> these are MEANS.
FIG8A_LDH = {  # % of vehicle
    10:  {"32": 111, "33": 105, "35": 104, "36": 98,  "37": 124, "43": 120, "47": 105},
    30:  {"32": 113, "33": 105, "35": 107, "36": 106, "37": 150, "43": 146, "47": 107},
    100: {"32": 113, "33": 108, "35": 106, "36": 112, "37": 169, "43": 169, "47": 110},
}
FIG8A_ATP = {  # % decrease
    10:  {"32": 2,  "33": 10, "35": 14, "36": 17, "37": 44, "43": 33, "47": 5},
    30:  {"32": 8,  "33": 10, "35": 20, "36": 28, "37": 70, "43": 67, "47": 13},
    100: {"32": 15, "33": 17, "35": 27, "36": 38, "37": 87, "43": 90, "47": 26},
}
FIG8BC = {  # (panel, species): {conc: {construct: (ldh, atp)}}
    ("B", "Mus musculus"): {
        3:  {"Survivin": (171, 26), "Bcl2": (131, 28)},
        10: {"Survivin": (182, 29), "Bcl2": (142, 38)},
        30: {"Survivin": (195, 36), "Bcl2": (160, 48)},
    },
    ("C", "Homo sapiens"): {
        30:  {"Survivin": (117, 31), "Bcl2": (118, 29)},
        100: {"Survivin": (136, 38), "Bcl2": (120, 40)},
        300: {"Survivin": (158, 39), "Bcl2": (139, 48)},
    },
}

NR = "NOT_REPORTED"
QUAL = ("STAGED RAW VALUE - transferred under SCIENTIFIC_RULES.md SA; not validated, "
        "not adjudicated, not ingested, not model-eligible")

# ---------------------------------------------------------------- canonical oligo table
con_rows = []
for sso, (tokens, _alt) in TABLE1.items():
    seq, sugar, basemod, wing, gap = parse(tokens)
    assert len(seq) == len(sugar.split("|")) == len(basemod.split("|"))
    con_rows.append({
        "oligo_id": f"SEW16-SSO{sso}",
        "source_label": f"SSO {sso}",
        "sequence_5to3": seq,
        "length_nt": len(seq),
        "strand_role": "single_strand_antisense",
        "duplex_partner_id": "not_applicable",
        "backbone_by_linkage": "|".join(["phosphorothioate"] * (len(seq) - 1)),
        "sugar_mod_by_position": sugar,
        "base_mod_by_position": basemod,
        "terminal_modifications": "none_reported",
        "gap_length_nt": gap,
        "wing_design": wing,
        "purity_pct": NR,
        "identity_method": NR,
        "endotoxin_level": NR,
        "target_gene": "Myd88",
        "target_species": "Mus musculus",
        "sequence_family_group": f"myd88_tool_set_{wing}",
        "paper_group": PAPER_GROUP,
        "dieckmann2018_sequence_match": DIECKMANN_SEQ_MATCH.get(sso, "none"),
        "identity_basis": ("published sequence read visually from Table 1; NOT experimental "
                           "batch identity; sequence match to Dieckmann is sequence-level only"),
        "source_location": "Table 1",
        "source_doi": DOI,
        "source_url": URL,
        "licence": LICENCE,
    })
for name in ("Survivin", "Bcl2"):
    con_rows.append({
        "oligo_id": f"SEW16-{name}",
        "source_label": f"historical development SSO targeting {name}",
        "sequence_5to3": NR, "length_nt": NR, "strand_role": "single_strand_antisense",
        "duplex_partner_id": "not_applicable", "backbone_by_linkage": NR,
        "sugar_mod_by_position": NR, "base_mod_by_position": NR,
        "terminal_modifications": NR, "gap_length_nt": NR, "wing_design": NR,
        "purity_pct": NR, "identity_method": NR, "endotoxin_level": NR,
        "target_gene": name, "target_species": "Homo sapiens",
        "sequence_family_group": NR, "paper_group": PAPER_GROUP,
        "dieckmann2018_sequence_match": "none",
        "identity_basis": ("named by target only; no sequence published in this source, so this "
                           "construct cannot enter a sequence-linked dataset from here"),
        "source_location": "Results / Fig 8B-C", "source_doi": DOI, "source_url": URL,
        "licence": LICENCE,
    })

# ---------------------------------------------------------------- observation table
obs, n = [], 0


def add(**kw):
    global n
    n += 1
    row = {"staging_id": f"SEW16-{n:05d}", "exposure_time_h": 72,
           "delivery_agent": "none_gymnotic_free_uptake",
           "formulation": "PBS stock into serum-free William's Medium E",
           "donor_id": NR, "donor_class": NR, "replicate_structure":
           "mean of 2 independent experiments, each in triplicate",
           "curator_label": "NOT_ASSIGNED_pending_German",
           "source_doi": DOI, "source_url": URL, "licence": LICENCE, "qualification": QUAL}
    row.update(kw)
    obs.append(row)


for sso, (_tok, alt) in TABLE1.items():
    add(oligo_id=f"SEW16-SSO{sso}", endpoint_name="ALT_serum",
        raw_value=(alt if alt is not None else NR), raw_unit="U/L",
        dose_value=15, dose_unit="mg/kg per injection, 5 injections i.v. over 2 weeks",
        exposure_time_h=336, cell_system="whole animal, in vivo", species="Mus musculus",
        sample_state="serum", delivery_agent="saline, tail vein injection",
        formulation="saline",
        author_interpretation=("in vivo hepatotoxic" if (alt is None or alt > 150)
                               else "in vivo safe"),
        replicate_structure=NR,
        source_location="Table 1",
        note=("ND - no ALT determined, group sacrificed early due to severe toxicity"
              if alt is None else ""))

for conc in (10, 30, 100):
    for sso in TABLE1:
        for ep, table, unit in (("LDH_release", FIG8A_LDH, "percent_of_vehicle"),
                                ("ATP_cellular", FIG8A_ATP, "percent_decrease_vs_vehicle")):
            add(oligo_id=f"SEW16-SSO{sso}", endpoint_name=ep, raw_value=table[conc][sso],
                raw_unit=unit, dose_value=conc, dose_unit="uM",
                cell_system="cryopreserved primary hepatocytes, collagen-coated 96-well",
                species="Homo sapiens", sample_state="supernatant" if ep.startswith("LDH")
                else "cell lysate",
                author_interpretation=NR, source_location="Figure 8A", note="")

for (panel, species), block in FIG8BC.items():
    for conc, per in block.items():
        for name, (ldh, atp) in per.items():
            for ep, val, unit in (("LDH_release", ldh, "percent_of_vehicle"),
                                  ("ATP_cellular", atp, "percent_decrease_vs_vehicle")):
                add(oligo_id=f"SEW16-{name}", endpoint_name=ep, raw_value=val, raw_unit=unit,
                    dose_value=conc, dose_unit="uM",
                    cell_system=("cryopreserved primary hepatocytes" if species == "Homo sapiens"
                                 else "freshly isolated primary hepatocytes"),
                    species=species,
                    sample_state="supernatant" if ep.startswith("LDH") else "cell lysate",
                    author_interpretation=("documented pre-clinical and clinical liver effects; "
                                           "grade 3 liver enzyme increases reported in phase 1"),
                    source_location=f"Figure 8{panel}", note="")

for path, rows in (("sewing2016_constructs.csv", con_rows),
                   ("sewing2016_condition_level.csv", obs)):
    keys = list(rows[0].keys())
    for r in rows:
        for k in keys:
            r.setdefault(k, "")
    with open(os.path.join(HERE, path), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"{path}: {len(rows)} rows x {len(keys)} cols")

human = sum(1 for r in obs if r["species"] == "Homo sapiens")
print(f"  human-system observation rows: {human}")
print(f"  animal-system observation rows: {len(obs) - human}")
print(f"  constructs with a published sequence: "
      f"{sum(1 for r in con_rows if r['sequence_5to3'] != NR)}/{len(con_rows)}")
print(f"  constructs with a purity value: "
      f"{sum(1 for r in con_rows if r['purity_pct'] != NR)}/{len(con_rows)}")
