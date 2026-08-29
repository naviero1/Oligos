#!/usr/bin/env python3
"""
Parses WHO INN Recommended-list chemical names into sequences and per-position
chemistry.

Why this is a parse and not a transcription. A WHO INN entry for an
oligonucleotide spells out every residue longhand — its sugar, its base, any
5-methylation, and whether the linkage to the next residue is a phosphorothioate
or a plain phosphodiester:

    all-P-ambo-2'-O-(2-methoxyethyl)-5-methyl-P-thiocytidylyl-(3'->5')-
    2'-O-(2-methoxyethyl)adenylyl-(3'->5')-...

so the sequence and the modification map are recovered deterministically rather
than judged. This is the route the sibling kidney dataset established (its
METHODOLOGY §4 path 4) and it is the only route by which a marketed
oligonucleotide's sequence enters this dataset: no US label prints one.

The `P-thio` prefix belongs to the residue whose 3'->5' linkage it describes, so
a residue written without it carries a phosphodiester at its 3' end. A bare
`thymidylyl` with no sugar prefix is 2'-deoxy by definition.

VALIDATION. The parse is checked against evidence that does not come from the INN
list, and the script fails rather than emitting a sequence that disagrees:
  * parsed length must equal the length independently derived from the label's
    molecular formula (nusinersen P17 -> 18) or stated by it (tofersen 20-mer);
  * parsed phosphorothioate and phosphodiester counts must equal the label's own
    statement where it makes one (tofersen: 15 PS and 4 PO of 19);
  * parsed residue count minus one must equal the phosphorus count in the
    label's molecular formula.

Output: data/inn_sequences.json  (consumed by build_oligos.py and
        build_modifications.py)
        notes/inn_parse_report.txt
Usage:  python3 scripts/parse_inn_sequences.py
"""
import json
import os
import re
import sys

try:
    import pymupdf as fitz
except ImportError:                                    # older wheels
    import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INN = os.path.join(ROOT, "sources", "raw", "inn")
DATA = os.path.join(ROOT, "data")
NOTES = os.path.join(ROOT, "notes")

# compound -> (Recommended INN list number, WHO Drug Information citation)
COMPOUNDS = {
    "nusinersen":    (74, "WHO Drug Information Vol. 29, No. 3, 2015, Recommended INN List 74"),
    "inotersen":     (77, "WHO Drug Information, Recommended INN List 77"),
    "tofersen":      (81, "WHO Drug Information, Recommended INN List 81"),
    "tominersen":    (83, "WHO Drug Information, Recommended INN List 83"),
    "eplontersen":   (85, "WHO Drug Information, Recommended INN List 85"),
    "zorevunersen":  (87, "WHO Drug Information, Recommended INN List 87"),
    "elsunersen":    (92, "WHO Drug Information, Recommended INN List 92"),
    "volanesorsen":  (75, "WHO Drug Information, Recommended INN List 75"),
    # Present in the downloaded lists but NOT parsed here, deliberately:
    #   patisiran rl71, givosiran rl76, inclisiran rl76, lumasiran rl79,
    #   vutrisiran rl81, nedosiran rl85  — double-stranded siRNAs. The INN entry
    #     names both strands; recovering them needs a strand convention and a
    #     duplex reverse-complement check this parser has not been validated for.
    #   golodirsen rl77, casimersen rl77, viltolarsen rl80, eteplirsen rl87 —
    #     morpholinos, whose nomenclature this parser does not implement.
    # The duplex guard below makes the first class fail loudly rather than
    # silently returning one strand. See METHODOLOGY.md OI-02.
}

# Independent evidence the parse must agree with. None where the label is silent.
EXPECTED = {
    "nusinersen": dict(length=18, ps=17, po=0, formula_p=17,
                       basis="label molecular formula C234H323N61O128P17S17"),
    "tofersen":   dict(length=20, ps=15, po=4, formula_p=19,
                       basis="label states 20-mer, 15 phosphorothioate and 4 "
                             "phosphate diesters, C230H317N72O123P19S15"),
}

BASES = [("uridylyl", "U"), ("uridine", "U"), ("cytidylyl", "C"), ("cytidine", "C"),
         ("adenylyl", "A"), ("adenosine", "A"), ("guanylyl", "G"), ("guanosine", "G"),
         ("thymidylyl", "T"), ("thymidine", "T")]
ARROW = "→"


def name_for(pdf_path, compound):
    """Return the English INN chemical name, whitespace stripped."""
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        if compound not in text.lower():
            continue
        flat = re.sub(r"\s+", "", text)
        start = flat.lower().find("all-p-ambo")
        if start < 0:
            continue
        # The English name ends at the terminal residue; the French entry follows.
        tail = flat[start:]
        end = re.search(r"(?:idine|osine|ydine)", tail)
        if not end:
            continue
        chain = tail[:end.end()]
        remainder = tail[end.end():]
        # A duplex entry continues with a SECOND ENGLISH CHAIN after the first
        # terminal residue. The French and Spanish translations also follow on
        # this page and are full of linkages, so the window must stop at
        # whichever translation marker comes first ("tout-" / "todo-") before
        # any linkages are counted. Refuse a duplex rather than silently
        # returning one strand of it.
        stop = len(remainder)
        for marker in ("tout-", "todo-", "tout‑", "todo‑"):
            i = remainder.lower().find(marker)
            if 0 <= i < stop:
                stop = i
        english_tail = remainder[:stop]
        if english_tail.count("(3'%s5')" % ARROW) >= 2:
            raise ValueError("entry names more than one strand (%d further "
                             "linkages in the English entry after the first "
                             "terminal residue); duplex parsing is not implemented"
                             % english_tail.count("(3'%s5')" % ARROW))
        return chain
    return None


def parse(name):
    """Return a list of per-position dicts, 5'->3'."""
    body = re.sub(r"^all-P-ambo-", "", name, flags=re.I)
    tokens = body.split("-(3'%s5')-" % ARROW)
    out = []
    for i, tok in enumerate(tokens):
        low = tok.lower()
        base = next((b for stem, b in BASES if stem in low), None)
        if base is None:
            raise ValueError("no base stem in residue %d: %r" % (i + 1, tok))
        if "2'-o-(2-methoxyethyl)" in low:
            sugar = "2'-MOE"
        elif "2'-deoxy" in low:
            sugar = "DNA_2prime_deoxy"
        elif "2'-o-methyl" in low:
            sugar = "2'-OMe"
        elif "thymidyl" in low or "thymidine" in low:
            sugar = "DNA_2prime_deoxy"        # thymidine is deoxy by definition
        else:
            raise ValueError("no sugar in residue %d: %r" % (i + 1, tok))
        thio = "p-thio" in low
        methyl = bool(re.search(r"5-methyl", low))
        last = (i == len(tokens) - 1)
        out.append(dict(
            position_5to3=i + 1, nucleobase=base, sugar_chemistry=sugar,
            base_modification=(("5-methylcytosine" if base == "C" else
                                "5-methyluracil" if base == "U" else "5-methyl")
                               if methyl else "none"),
            linkage_3prime=("terminal_none" if last else
                            "phosphorothioate" if thio else "phosphodiester")))
    return out


def main():
    results, report = {}, []
    for compound, (listno, citation) in COMPOUNDS.items():
        pdf = os.path.join(INN, "rl%d.pdf" % listno)
        if not os.path.exists(pdf):
            report.append("%-14s SKIPPED — %s not downloaded" % (compound, pdf))
            continue
        try:
            name = name_for(pdf, compound)
        except ValueError as exc:
            report.append("%-14s REFUSED — %s" % (compound, exc))
            continue
        if not name:
            report.append("%-14s FAILED — no English chemical name found in rl%d"
                          % (compound, listno))
            continue
        try:
            positions = parse(name)
        except ValueError as exc:
            report.append("%-14s FAILED — %s" % (compound, exc))
            continue

        seq = "".join(p["nucleobase"] for p in positions)
        ps = sum(1 for p in positions if p["linkage_3prime"] == "phosphorothioate")
        po = sum(1 for p in positions if p["linkage_3prime"] == "phosphodiester")

        exp = EXPECTED.get(compound)
        if exp:
            problems = []
            if len(positions) != exp["length"]:
                problems.append("length %d != expected %d" % (len(positions), exp["length"]))
            if ps != exp["ps"]:
                problems.append("PS %d != expected %d" % (ps, exp["ps"]))
            if po != exp["po"]:
                problems.append("PO %d != expected %d" % (po, exp["po"]))
            if len(positions) - 1 != exp["formula_p"]:
                problems.append("n-1 (%d) != formula P count %d"
                                % (len(positions) - 1, exp["formula_p"]))
            if problems:
                sys.exit("INN parse for %s disagrees with the label (%s): %s"
                         % (compound, exp["basis"], "; ".join(problems)))
            report.append("%-14s %2d nt  PS %2d  PO %d  VALIDATED against %s"
                          % (compound, len(positions), ps, po, exp["basis"]))
        else:
            report.append("%-14s %2d nt  PS %2d  PO %d  (no independent check available)"
                          % (compound, len(positions), ps, po))

        results[compound] = dict(
            sequence_base=seq, length_nt=len(positions), n_phosphorothioate=ps,
            n_phosphodiester=po, positions=positions,
            inn_list=listno, citation=citation,
            source_location="Recommended INN List %d, entry '%s', English chemical "
                            "name" % (listno, compound),
            chemical_name=name)
        report.append("%-14s %s" % ("", seq))

    with open(os.path.join(DATA, "inn_sequences.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    with open(os.path.join(NOTES, "inn_parse_report.txt"), "w") as fh:
        fh.write("WHO INN chemical-name parse\n" + "=" * 66 + "\n")
        fh.write("\n".join(report) + "\n")
    print("parsed %d compounds -> data/inn_sequences.json" % len(results))
    print("\n".join(report))


if __name__ == "__main__":
    main()
