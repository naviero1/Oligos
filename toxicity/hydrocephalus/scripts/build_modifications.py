#!/usr/bin/env python3
"""
Builds data/modifications.csv — one row per NUCLEOTIDE POSITION.

The Challenge brief requires the dataset to contain "the sequences of all oligos
tested, as well as **the location of all chemical modifications in each oligo**".
A per-oligo summary such as `5-10-5_MOE_gapmer` does not satisfy that: it states
the motif, not the location. This table states the location.

Two things make it possible to fill this in even where the base sequence is not
published, and both are worth being explicit about:

  * A position's SUGAR chemistry is derivable from a label that states the motif
    in words. The tofersen label says "five MOE nucleosides at the 5' and 3'-ends
    of the molecule flanking a gap of ten 2'-deoxynucleosides" for a 20-mer —
    that fixes the sugar at all twenty positions without naming a single base.
  * A position's NUCLEOBASE is known wherever the sequence is published, even if
    the source states no modification at all.

So the table is filled per DIMENSION, not per oligo: a row may carry a known
sugar and an unknown base, or the reverse. Every unknown is NOT_REPORTED and
every filled value carries a `basis` naming how it was established.

Not covered, and why: the four morpholinos. Their labels give a molecular formula
but the phosphorus count is P = n for eteplirsen, golodirsen and casimersen and
P = n-1 for viltolarsen, because some carry a 5'-piperazine bearing an extra
phosphorus and some do not. Length is therefore ambiguous for that class, and a
per-position table cannot be built on an ambiguous length. They contribute no
rows rather than a guessed one.

Output: data/modifications.csv
Usage:  python3 scripts/build_modifications.py
        MUST run after scripts/assemble.py, which is what assigns oligo_id.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")

# Per-position sugar chemistry, stated as a rule over 1-based positions.
# Each entry: (length, sugar_fn, linkage, basis, source_id, note)
DESIGNS = {
    "tofersen": dict(
        length=20,
        sugar=lambda i, n: "2'-MOE" if (i <= 5 or i > n - 5) else "DNA_2prime_deoxy",
        linkage="NOT_REPORTED",
        basis="position_resolved_from_source_motif_statement",
        source_id="DailyMed_SPL_tofersen",
        location="SPL section 11 DESCRIPTION",
        note=("Sugar fixed at every position by the label's own words: 'The residues "
              "are arranged so that there are five MOE nucleosides at the 5' and "
              "3'-ends of the molecule flanking a gap of ten 2'-deoxynucleosides.' "
              "Linkage is NOT_REPORTED per position because the label states 15 "
              "phosphorothioate and 4 phosphate diesters of 19 without saying WHICH "
              "four are phosphate. Base modification is likewise not derivable: the "
              "label says every cytosine and uridine is 5-methylated, but the "
              "sequence is not printed, so which positions those are is unknown."),
    ),
    "nusinersen": dict(
        length=18,
        sugar=lambda i, n: "2'-MOE",
        linkage="phosphorothioate",
        basis="position_resolved_from_source_uniform_chemistry_statement",
        source_id="DailyMed_SPL_nusinersen",
        location="SPL section 11 DESCRIPTION",
        note=("Uniform chemistry, so every position is determined by one sentence: "
              "'the 2'-hydroxy groups of the ribofuranosyl rings are replaced with "
              "2'-O-2-methoxyethyl groups and the phosphate linkages are replaced "
              "with phosphorothioate linkages.' Length 18 is derived from the "
              "label's molecular formula (P17, S17); see oligos.length_nt_basis. "
              "Base identity is not printed in the label."),
    ),
}

# Oligonucleotides whose SEQUENCE is published: the nucleobase at every position
# is known even though no modification is stated.
SEQUENCED_SOURCE = "Choroid_plexus_siSPAK_LNP_2025_NatCommun"
SEQUENCED_NOTE = (
    "Nucleobase at every position read from the antisense (guide) strand printed in "
    "the source's Methods (Materials). The source states no chemical modification "
    "for these reagents, so sugar_chemistry, base_modification and linkage are "
    "NOT_REPORTED rather than assumed to be unmodified RNA. The 3'-terminal TT is "
    "printed by the source as 'TT' without stating whether it is deoxythymidine, so "
    "it is recorded as base T with the sugar unstated.")

# Compounds deliberately excluded, with the reason carried into the audit output.
EXCLUDED = {
    "eteplirsen": "morpholino; length ambiguous from formula (P = n vs n-1 across class)",
    "golodirsen": "morpholino; length ambiguous from formula",
    "viltolarsen": "morpholino; length ambiguous from formula",
    "casimersen": "morpholino; length ambiguous from formula",
    "valeriasen": ("sequence and per-position chemistry exist in the source's Extended "
                   "Data Table 1 but are published as an image whose bold/underline "
                   "2'-MOE encoding does not survive text extraction; not transcribed "
                   "(METHODOLOGY.md OI-02)"),
}


def main():
    oligos = {o["oligo_name"]: o for o in
              csv.DictReader(open(os.path.join(DATA, "oligos.csv")))}
    if not all("oligo_id" in o for o in oligos.values()):
        raise SystemExit("data/oligos.csv carries no oligo_id column — run "
                         "scripts/assemble.py first; it is what assigns the keys.")
    rows, report = [], []

    for name, d in DESIGNS.items():
        o = oligos.get(name)
        if not o:
            raise SystemExit("design given for an oligo absent from oligos.csv: " + name)
        n = d["length"]
        if o["length_nt"] != str(n):
            raise SystemExit("length disagreement for %s: oligos.csv=%s design=%d"
                             % (name, o["length_nt"], n))
        for i in range(1, n + 1):
            rows.append(dict(
                oligo_id=o["oligo_id"], oligo_name=name, strand="single_strand",
                position_5to3=i, nucleobase="NOT_REPORTED",
                sugar_chemistry=d["sugar"](i, n),
                base_modification="NOT_REPORTED",
                linkage_3prime=("terminal_none" if i == n else d["linkage"]),
                basis=d["basis"], source_id=d["source_id"],
                source_location=d["location"], notes=d["note"]))
        report.append("%-24s %2d positions, sugar resolved, base NOT_REPORTED"
                      % (name, n))

    for name, o in oligos.items():
        seq = o["sequence_5to3_asprinted"]
        if seq in ("NOT_REPORTED", "NOT_APPLICABLE") or name in DESIGNS:
            continue
        for i, base in enumerate(seq, 1):
            rows.append(dict(
                oligo_id=o["oligo_id"], oligo_name=name,
                strand="antisense_guide", position_5to3=i, nucleobase=base,
                sugar_chemistry="NOT_REPORTED", base_modification="NOT_REPORTED",
                linkage_3prime=("terminal_none" if i == len(seq) else "NOT_REPORTED"),
                basis="position_resolved_from_published_sequence",
                source_id=SEQUENCED_SOURCE,
                source_location="Methods, 'Materials'", notes=SEQUENCED_NOTE))
        report.append("%-24s %2d positions, base resolved, chemistry NOT_REPORTED"
                      % (name, len(seq)))

    for name, why in EXCLUDED.items():
        report.append("%-24s EXCLUDED — %s" % (name, why))

    cols = ["oligo_id", "oligo_name", "strand", "position_5to3", "nucleobase",
            "sugar_chemistry", "base_modification", "linkage_3prime", "basis",
            "source_id", "source_location", "notes"]
    out = os.path.join(DATA, "modifications.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(ROOT, "notes", "modifications_report.txt"), "w") as fh:
        fh.write("modifications.csv build report\n" + "=" * 60 + "\n")
        fh.write("%d position rows over %d oligonucleotides\n\n"
                 % (len(rows), len({r["oligo_id"] for r in rows})))
        fh.write("\n".join(report) + "\n")

    print("wrote %s: %d position rows over %d oligonucleotides"
          % (out, len(rows), len({r["oligo_id"] for r in rows})))
    print("\n".join(report))


if __name__ == "__main__":
    main()
