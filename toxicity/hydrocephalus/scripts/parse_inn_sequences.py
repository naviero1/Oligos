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
    # --- single-strand ASOs added after the Phase 2 re-read -------------
    "apatorsen":     (72, "WHO Drug Information, Recommended INN List 72"),
    "alicaforsen":   (79, "WHO Drug Information, Recommended INN List 79"),
    "danvatirsen":   (79, "WHO Drug Information, Recommended INN List 79"),
    "bepirovirsen":  (85, "WHO Drug Information, Recommended INN List 85"),
    "donidalorsen":  (86, "WHO Drug Information, Recommended INN List 86"),
    "olezarsen":     (87, "WHO Drug Information, Recommended INN List 87"),
    "sepofarsen":    (83, "WHO Drug Information, Recommended INN List 83"),
    "ultevursen":    (89, "WHO Drug Information, Recommended INN List 89"),
    # --- duplex siRNAs: the INN entry names BOTH strands ----------------
    "patisiran":     (71, "WHO Drug Information, Recommended INN List 71"),
    "fitusiran":     (75, "WHO Drug Information, Recommended INN List 75"),
    "givosiran":     (76, "WHO Drug Information, Recommended INN List 76"),
    "inclisiran":    (76, "WHO Drug Information, Recommended INN List 76"),
    "lumasiran":     (79, "WHO Drug Information, Recommended INN List 79"),
    "vutrisiran":    (81, "WHO Drug Information, Recommended INN List 81"),
    "nedosiran":     (85, "WHO Drug Information, Recommended INN List 85"),
    # --- morpholinos: the INN entry PRINTS the base sequence ------------
    "golodirsen":    (77, "WHO Drug Information, Recommended INN List 77"),
    "casimersen":    (77, "WHO Drug Information, Recommended INN List 77"),
    "viltolarsen":   (80, "WHO Drug Information, Recommended INN List 80"),
    "eteplirsen":    (87, "WHO Drug Information, Recommended INN List 87"),
}

# Independent evidence the parse must agree with. None where the label is silent.
EXPECTED = {
    "nusinersen": dict(length=18, ps=17, po=0, formula_p=17,
                       basis="label molecular formula C234H323N61O128P17S17"),
    "tofersen":   dict(length=20, ps=15, po=4, formula_p=19,
                       basis="label states 20-mer, 15 phosphorothioate and 4 "
                             "phosphate diesters, C230H317N72O123P19S15"),
}

BASES = [("uridylyl", "U"), ("uridylate", "U"), ("uridine", "U"),
         ("cytidylyl", "C"), ("cytidylate", "C"), ("cytidine", "C"),
         ("adenylyl", "A"), ("adenylate", "A"), ("adenosine", "A"),
         ("guanylyl", "G"), ("guanylate", "G"), ("guanosine", "G"),
         ("thymidylyl", "T"), ("thymidylate", "T"), ("thymidine", "T")]
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


COMPLEMENT = {"A": "U", "U": "A", "G": "C", "C": "G"}


def entry_text(pdf_path, compound):
    """The English INN entry, whitespace stripped.

    A WHO page prints the Latin name, then the English entry, then French and
    Spanish. The anchor is "<name>um<name>": Latin immediately followed by the
    English heading. The entry ends at the next occurrence of the name (the
    French heading) or at a translation marker.

    Scans the WHOLE document, not one page: the vutrisiran entry runs across a
    page break, and a per-page reader silently returned a truncated entry whose
    second strand was missing -- which the parser then reported as a 1-nt
    sequence rather than as a failure.
    """
    doc = fitz.open(pdf_path)
    try:
        flat = re.sub(r"\s+", "", "".join(pg.get_text() for pg in doc))
    finally:
        doc.close()
    low = flat.lower()
    anchor = low.find(compound + "um" + compound)
    if anchor < 0:
        hits = [m.start() for m in re.finditer(re.escape(compound), low)]
        if len(hits) < 2:
            return None
        start = hits[1] + len(compound)
    else:
        start = anchor + len(compound) * 2 + 2
    rest = flat[start:]
    # Prefer a TRANSLATION marker as the boundary. Using the compound name cut
    # fitusiran, givosiran and inclisiran in half -- the name recurs inside the
    # English entry, so the second strand of each duplex was silently dropped.
    end = None
    for marker in ("tout-", "todo-", "petitarn", "petitarninterferent", "pequeño"):
        i = rest.lower().find(marker, 40)
        if i >= 0 and (end is None or i < end):
            end = i
    if end is None:
        i = rest.lower().find(compound, 40)
        end = i if i >= 0 else len(rest)
    body = rest[:end]
    return body if len(body) > 60 else None


def revcomp(seq):
    return "".join(COMPLEMENT.get(b, "N") for b in reversed(seq.replace("T", "U")))


def parse_duplex(entry, compound):
    """Both strands of an siRNA, from one INN entry.

    The entry reads "RNA duplex of <strand1> with <strand2>". The two strands are
    written in OPPOSITE directions: strand 1 uses (3'->5') linkages, so reading it
    left to right runs 5'->3'; strand 2 uses (5'->3') linkages, so reading it left
    to right runs 3'->5' and the parsed residues must be REVERSED to put the
    strand in 5'->3' orientation. Getting that backwards silently yields a
    plausible but wrong antisense strand, which is exactly why the
    reverse-complement check below is a hard failure rather than a warning.
    """
    m = re.search(r"duplexwith", entry, re.I) or re.search(
        r"(?:idine|osine|ydine|ylate)with", entry, re.I)
    if not m:
        raise ValueError("duplex entry has no joiner between the two strands")
    cut = m.start() if m.group(0).lower() == "duplexwith" else m.end() - 4
    first, second = entry[:cut], entry[m.end():]

    sense = parse(first, rna_default=True)
    anti = parse(re.sub(r"\(5'%s3'\)" % ARROW, "(3'%s5')" % ARROW, second),
                 rna_default=True)
    anti = list(reversed(anti))
    for i, pos in enumerate(anti, 1):
        pos["position_5to3"] = i
    # Reversing the residue order also moves each 3' linkage: after reversal a
    # residue carries the linkage that belonged to its new 3' neighbour.
    links = [p["linkage_3prime"] for p in anti]
    for i, pos in enumerate(anti):
        pos["linkage_3prime"] = (links[i + 1] if i + 1 < len(links)
                                 else "terminal_none")

    s_seq = "".join(p["nucleobase"] for p in sense)
    a_seq = "".join(p["nucleobase"] for p in anti)
    # Standard siRNA: 2-nt 3' overhangs that do not pair; the cores must be
    # exact reverse complements. This check depends on no source being correct,
    # so it catches a transcription or orientation error the entry alone cannot.
    # siRNA overhang conventions differ by sponsor: patisiran is 21+21 with a
    # 2-nt 3' overhang on BOTH strands (19-bp core), while the Alnylam GalNAc
    # designs are 21+23, where the antisense is the full reverse complement of
    # the sense plus a 2-nt 3' overhang. A single hard-coded trim rejects one or
    # the other, so try the known alignments and record which one matched.
    su = s_seq.replace("T", "U")
    au = a_seq.replace("T", "U")
    alignments = [
        ("21+23: antisense = revcomp(sense) + 2-nt 3' overhang", su, au[:len(su)]),
        ("2-nt 3' overhang on both strands", su[:-2], au[:len(su) - 2]),
        ("blunt", su, au),
    ]
    for label, cs, ca in alignments:
        if len(cs) == len(ca) and len(cs) >= 15 and revcomp(ca) == cs:
            return sense, anti, label
    raise ValueError("duplex cores are not reverse complements under any known "
                     "overhang convention (sense %s / antisense %s)"
                     % (s_seq, a_seq))


def parse_morpholino(entry, compound):
    """A phosphorodiamidate morpholino oligomer.

    The INN entry PRINTS the sequence as a hyphenated base run, e.g.
    (G-T-T-G-C-C-T-C-C-G-G-T-T-C-T-G-A-A-G-G-T-G-T-T-C). An earlier release
    excluded this whole class on the grounds that length was 'ambiguous from the
    molecular formula' — true, but irrelevant: the length never had to be
    derived, because the entry states the sequence outright.

    Every residue is a morpholino with a phosphorodiamidate linkage; the entry
    says so once for the whole chain ("azanediyl-P-(dimethylamino)...").
    """
    runs = re.findall(r"\(([ACGTU](?:-?[ACGTU]){5,})\)", entry)
    if not runs:
        raise ValueError("no printed base run found in the morpholino entry")
    bases = list(max(runs, key=len).replace("-", ""))
    n = len(bases)
    out = []
    for i, b in enumerate(bases, 1):
        out.append(dict(
            position_5to3=i, nucleobase=b, sugar_chemistry="morpholino",
            base_modification="none",
            linkage_3prime=("terminal_none" if i == n else "phosphorodiamidate")))
    fm = re.search(r"C\d+H\d+N\d+O\d+P(\d+)", entry)
    note = "no molecular formula in entry"
    if fm:
        pcount = int(fm.group(1))
        if pcount not in (n, n - 1):
            raise ValueError("printed sequence is %d nt but the formula gives P%d; "
                             "expected P=n or n-1" % (n, pcount))
        note = ("formula P%d agrees with %d nt (P=n means a 5'-piperazine bearing "
                "an extra phosphorus; P=n-1 means none)" % (pcount, n))
    return out, note


def strip_prefix(chain):
    """Remove an entry preamble and any 5' conjugate before the first residue.

    GalNAc-conjugated siRNAs prefix the chain with a large ligand whose name ends
    "...pyrrolidin-2-yl}methyl hydrogen"; the residues start after it. Entries may
    also open with prose ("small interfering RNA (siRNA); RNA duplex of").
    """
    for marker in ("duplexof", "duplexwith"):
        i = chain.lower().rfind(marker)
        if i >= 0:
            chain = chain[i + len(marker):]
    i = chain.lower().rfind("methylhydrogen")
    if i >= 0:
        chain = chain[i + len("methylhydrogen"):]
    return re.sub(r"^all-P-ambo-", "", chain, flags=re.I)


def parse(name, rna_default=False):
    """Return a list of per-position dicts, 5'->3'."""
    body = strip_prefix(name)
    tokens = body.split("-(3'%s5')-" % ARROW)
    out = []
    for i, tok in enumerate(tokens):
        low = tok.lower()
        base = next((b for stem, b in BASES if stem in low), None)
        if base is None:
            raise ValueError("no base stem in residue %d: %r" % (i + 1, tok))
        if "2'-o,4'-c-[(1s)-ethane-1,1-diyl]" in low or "cet" == low.strip():
            sugar = "cEt"                       # constrained ethyl (danvatirsen)
        elif "2'-deoxy-2'-fluoro" in low:
            sugar = "2'-F"
        elif "2'-o-(2-methoxyethyl)" in low:
            sugar = "2'-MOE"
        elif "2'-deoxy" in low:
            sugar = "DNA_2prime_deoxy"
        elif "2'-o-methyl" in low:
            sugar = "2'-OMe"
        elif "thymidyl" in low or "thymidine" in low:
            sugar = "DNA_2prime_deoxy"        # thymidine is deoxy by definition
        elif rna_default:
            # In an RNA duplex entry a residue written with no sugar prefix is a
            # plain ribonucleotide; only DNA/modified residues carry a prefix.
            sugar = "RNA_2prime_OH"
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
        entry = entry_text(pdf, compound)
        if not entry:
            report.append("%-14s FAILED — no English entry found in rl%d"
                          % (compound, listno))
            continue

        # Three nomenclatures, dispatched on the entry's own wording.
        kind = ("duplex" if re.search(r"duplexof|duplexwith", entry, re.I)
                else "morpholino" if re.search(r"azanediyl", entry, re.I)
                else "single_strand")
        name, anti_positions, extra_note, dup_align = entry, None, "", ""
        try:
            if kind == "duplex":
                positions, anti_positions, dup_align = parse_duplex(entry, compound)
            elif kind == "morpholino":
                positions, extra_note = parse_morpholino(entry, compound)
            else:
                name = name_for(pdf, compound)
                if not name:
                    report.append("%-14s FAILED — no chemical name in rl%d"
                                  % (compound, listno))
                    continue
                positions = parse(name)
        except ValueError as exc:
            report.append("%-14s FAILED (%s) — %s" % (compound, kind, exc))
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

        if kind == "duplex":
            a_seq = "".join(p["nucleobase"] for p in anti_positions)
            report.append("%-14s DUPLEX %d+%d nt, cores reverse-complement VERIFIED "
                          "(%s)" % (compound, len(positions), len(anti_positions),
                                    dup_align))
            report.append("%-14s   antisense %s" % ("", a_seq))
        elif kind == "morpholino":
            report.append("%-14s MORPHOLINO %d nt from the entry's printed base "
                          "run; %s" % (compound, len(positions), extra_note))

        results[compound] = dict(
            sequence_base=seq, length_nt=len(positions), n_phosphorothioate=ps,
            n_phosphodiester=po, positions=positions,
            strand_kind=kind,
            antisense_sequence_base=("".join(p["nucleobase"] for p in anti_positions)
                                     if anti_positions else None),
            antisense_positions=anti_positions,
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
