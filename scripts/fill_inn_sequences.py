#!/usr/bin/env python3
"""One-off backfill: nine sequences derived from WHO INN chemical nomenclature.

Each INN entry spells every residue out longhand
(2'-O-methyl-P-thiocytidylyl-(3'->5')-...), so the base sequence is a
deterministic parse rather than a judgement call. Two properties were checked
before anything was written here:

  1. Direction. INN writes one strand with (3'->5') linkages (listed 5'->3')
     and the other with (5'->3') linkages (listed 3'->5', so reversed on
     output). Getting this backwards silently yields a reversed strand. The
     parser was validated by reproducing givosiran and inclisiran -- both
     already in this table from WHO INN List 76 -- exactly.

  2. Duplex consistency. For every siRNA the stored guide strand is the exact
     reverse complement of the sense strand (ignoring 3' overhangs). This is an
     internal check that does not depend on any source being correct.

Strand convention matches the existing rows: sequence_5to3 holds the
antisense/guide strand for duplexes (the sense strand is recorded in notes),
and the single strand for ASOs/PMOs. INN lists the sense strand first -- the
strand carrying the GalNAc conjugate where one is present -- which was
confirmed against vutrisiran's already-stored guide strand.

Usage:  python scripts/fill_inn_sequences.py && python scripts/build_merged.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLIGOS = os.path.join(ROOT, "data", "oligos.csv")

# oligo_id -> (guide/single strand 5'->3', length, design_source add, notes add)
FILLS = {
    "OLG013": ("CCTCCGGTTCTGAAGGTGTTC", "21",
               "WHO_INN_List80",
               "PMO_21mer_exon53_skipping;formula_C244H381N113O88P20_P20_confirms_21nt"),
    "OLG019": ("AUGGAAUACUCUUGGUUACTT", "21",
               "WHO_INN_List71_guide_strand",
               "siRNA_duplex_21_21_dTdT_overhangs_both_strands;"
               "sense21_GUAACCAAGAGUAUUCCAUTT;revcomp_verified_core19"),
    "OLG023": ("UCUUGGUUACAUGAAAUCCCAUC", "23",
               "WHO_INN_List73_guide_strand",
               "GalNAc_siRNA_sense21_UGGGAUUUCAUGUAACCAAGA;"
               "same_base_sequence_as_vutrisiran_OLG022_differs_only_in_chemistry;"
               "revcomp_verified_core21"),
    "OLG027": ("GCCCAAGCTGGCATCCGTCA", "20",
               "WHO_INN_List79_correction_entry",
               "PS_DNA_20mer_ICAM1;formula_C192H244N75O98P19S19_P19_confirms_20nt"),
    "OLG028": ("UUGAAGUAAAUGGUGUUAACCAG", "23",
               "WHO_INN_List75_guide_strand",
               "GalNAc_siRNA_sense21_GGUUAACACCAUUUACUUCAA;revcomp_verified_core21"),
    "OLG029": ("GTCGCCCCTTCTCCCCGCAGC", "21",
               "WHO_INN_List73",
               "PS_DNA_21mer_SMAD7_antisense"),
    "OLG035": ("UAUUAUAAAAAUAUCUUGCUUUUTT", "25",
               "WHO_INN_List76_guide_strand",
               "GalNAc_siRNA_sense21_AAGCAAGAUAUUUUUAUAAUA;"
               "antisense25_carries_4nt_UUdTdT_3prime_overhang_unusual_but_per_INN;"
               "revcomp_verified_core21"),
    "OLG038": ("UGAAGGGUGAAAUAUUCUC", "19",
               "WHO_INN_List78_guide_strand",
               "blunt_19mer_siRNA_duplex_sense19_GAGAAUAUUUCACCCUUCA;"
               "revcomp_verified_exact_full_length"),
    "OLG039": ("UGUUAAACAUGCCUAAACGCU", "21",
               "WHO_INN_List88_guide_strand",
               "GalNAc_siRNA_sense21_AGCGUUUAGGCAUGUUUAACA;"
               "revcomp_verified_exact_full_length"),
}


def add(existing, extra):
    """Append to a ';'-delimited field without duplicating or leading ';'."""
    existing = (existing or "").strip()
    if not existing or existing == "TBD":
        return extra
    return existing if extra in existing else f"{existing};{extra}"


def main():
    with open(OLIGOS, newline="") as fh:
        reader = csv.DictReader(fh)
        fields, rows = reader.fieldnames, list(reader)

    changed = 0
    for r in rows:
        fill = FILLS.get(r["oligo_id"])
        if not fill:
            continue
        seq, length, src, note = fill
        if r["sequence_5to3"].strip() not in ("TBD", "", "NA"):
            print(f"  SKIP {r['oligo_id']} - already has {r['sequence_5to3']}")
            continue
        r["sequence_5to3"] = seq
        r["length_nt"] = length
        r["design_source"] = add(r["design_source"], src)
        r["notes"] = add(r["notes"], note)
        changed += 1
        print(f"  {r['oligo_id']:<8}{r['oligo_name']:<14}{seq}  ({length} nt)")

    with open(OLIGOS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\n{changed} row(s) filled")


if __name__ == "__main__":
    main()
