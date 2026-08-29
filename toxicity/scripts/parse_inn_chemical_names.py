#!/usr/bin/env python3
"""Deterministic parser for WHO INN longhand oligonucleotide chemical names.

Rules implemented (per METHODOLOGY.md section 4 path 4):
  * a strand written with (3'->5') linkages is listed 5'->3'  -> emit as-is
  * a strand written with (5'->3') linkages is listed 3'->5'  -> emit REVERSED
  * every residue token must yield exactly one nucleobase, else hard error
    (this is what catches PDF line-break damage instead of silently
     mis-parsing it)
Nucleobase letters: 5-methyluridine/thymidine -> T, uridine -> U,
cytidine/5-methylcytidine -> C, adenine -> A, guanine -> G.
"""
import re
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "cns")     # archived WHO INN PDFs
TXT = os.path.join(SRC, "_inn_txt_cache")      # PyMuPDF text cache (built on demand)
# Linkage arrows. Note WHO text contains occasional typos with a missing
# opening parenthesis (e.g. mivelsiran "P-thiouridylyl5'->3')"), so the
# opening bracket is optional. Non-canonical linkages ((5'->2'), (3'->3'))
# appear around glycol-nucleic-acid (GNA) residues and are matched too, but
# they do NOT vote on strand direction.
ARROW = re.compile(r"\(?\s*[235]'\s*(?:→|->)\s*[235]'\s*\)")
ARROW_DIR = re.compile(r"\(?\s*([235]')\s*(?:→|->)\s*([235]')\s*\)")
PAGE_JUNK = re.compile(
    r"^(===PAGE \d+===|\d{1,4}|Recommended\s+INN.*|Proposed\s+INN.*|"
    r"WHO Drug Information.*|.*Vol\.\s*\d+,\s*No\.\s*\d+.*)$")
ACCENT = re.compile(r"[éèêàáâíóúñüçö]")
FORMULA = re.compile(r"\bC\d+H\d+[A-Za-z0-9]*?P\d+[A-Za-z0-9]*\b")


def load(list_no):
    """Text of Recommended INN List <list_no>, extracted from the archived PDF."""
    os.makedirs(TXT, exist_ok=True)
    cache = os.path.join(TXT, f"rl{list_no}.txt")
    if not os.path.exists(cache):
        import glob
        import pymupdf
        hits = glob.glob(os.path.join(
            SRC, f"WHO_INN_RecommendedList{list_no}_*.pdf"))
        if not hits:
            raise LookupError(
                f"no archived PDF for Recommended INN List {list_no} in {SRC}. "
                f"Fetch it from https://cdn.who.int/media/docs/default-source/"
                f"international-nonproprietary-names-(inn)/rl{list_no}.pdf")
        doc = pymupdf.open(hits[0])
        with open(cache, "w") as fh:
            fh.write("\n".join(p.get_text() for p in doc))
        doc.close()
    with open(cache) as fh:
        return fh.read().split("\n")


def entry_block(lines, name, extra_lines=200):
    """Return (english_chemical_name_text, raw_region_text) for one INN."""
    latin = f"{name}um"
    idx = None
    for i, ln in enumerate(lines):
        if ln.strip() == latin:
            idx = i
            break
    if idx is None:
        raise LookupError(f"{latin} not found")
    start = None
    for i in range(idx + 1, min(idx + 12, len(lines))):
        if lines[i].strip() == name:
            start = i + 1
            break
    if start is None:
        raise LookupError(f"English name line for {name} not found")

    body = []
    for ln in lines[start:start + extra_lines]:
        s = ln.strip()
        if not s:
            continue
        if ACCENT.search(s):          # French / Spanish block begins
            break
        if s == name:                 # repeat of the name = next language
            break
        if re.fullmatch(r"[a-z]+um", s) and s != latin:   # next INN entry
            break
        if PAGE_JUNK.match(s):        # page break header/footer inside a name
            continue
        body.append(s)

    joined = ""
    for s in body:
        if joined and not joined.endswith("-") and not s[0] in "-()]},":
            joined += " "
        joined += s

    # Scope the molecular formula to THIS entry: the block runs from this
    # entry's latin name up to the next entry's latin name.
    end = idx + extra_lines * 3
    for i in range(start, min(idx + extra_lines * 3, len(lines))):
        s = lines[i].strip()
        if re.fullmatch(r"[a-z]+um", s) and s != latin:
            end = i
            break
    region = "\n".join(lines[idx:end])
    return joined, region


BASES = [
    ("thymidyl", "T"), ("thymidine", "T"), ("thymidylate", "T"),
    ("uridyl", "U"), ("uridine", "U"), ("uridylate", "U"),
    ("cytidyl", "C"), ("cytidine", "C"), ("cytidylate", "C"),
    ("adenyl", "A"), ("adenosine", "A"),
    ("guanyl", "G"), ("guanosine", "G"),
]


def base_of(tok):
    hits = set()
    t = re.sub(r"\s+", "", tok.lower())
    for key, b in BASES:
        if key in t:
            hits.add(b)
    if len(hits) != 1:
        raise ValueError(f"ambiguous/no base in residue token: {tok!r} -> {hits}")
    b = hits.pop()
    if b == "U" and "5-methyl" in t:
        b = "T"          # 5-methyluridine == thymine base
    return b


def sugar_of(tok):
    # PDF line-joining can inject stray spaces inside a residue name
    # (e.g. "2'- O-(2-methoxyethyl) -5-methyl-..."), so match space-free.
    t = re.sub(r"\s+", "", tok.lower())
    if "dihydroxypropyl" in t:
        return "GNA"
    if "phosphonoethen" in t:
        return "VP-OMe"      # 5'-(E)-vinylphosphonate on a 2'-O-methyl sugar
    if "hexadecyl" in t:
        return "C16"         # 2'-O-hexadecyl lipid anchor
    if "2'-o-(2-methoxyethyl" in t:
        return "MOE"
    if "2'-deoxy-2'-fluoro" in t:
        return "2'F"
    if "2'-o,4'-c" in t or "bicyclo" in t:
        return "BNA"
    if "2'-o-methyl" in t:
        return "OMe"
    if "morpholin" in t:
        return "PMO"
    if "2'-deoxy" in t or "thymidyl" in t or "thymidine" in t:
        return "DNA"
    return "RNA"


# A second strand is introduced by "and" or by "duplex with".
STRAND_SEP = re.compile(r"\s+(?:and|duplex\s+with)\s+")


def parse_strands(chem):
    """Split the chemical name into strands; return list of dicts."""
    dirs = [(m.group(1), m.group(2)) for m in ARROW_DIR.finditer(chem)]
    frags = ARROW.split(chem)
    if len(frags) != len(dirs) + 1:
        raise ValueError(f"arrow/fragment mismatch: {len(frags)} vs {len(dirs)}+1")

    # locate strand boundaries: the fragment joining two strands contains
    # " and " / " duplex with "
    strands, cur_res, cur_dirs = [], [], []
    for i, frag in enumerate(frags):
        f = frag.strip().strip("-")
        boundary = STRAND_SEP.split(f, maxsplit=1)
        if len(boundary) == 2:
            cur_res.append(boundary[0])
            strands.append((cur_res, cur_dirs))
            cur_res, cur_dirs = [boundary[1]], []
        else:
            cur_res.append(f)
        if i < len(dirs):
            cur_dirs.append(dirs[i])
    strands.append((cur_res, cur_dirs))

    out = []
    for res, ds in strands:
        # Only canonical 3'->5' / 5'->3' linkages vote on listing direction.
        # (5'->2') and (3'->3') flank glycol-nucleic-acid (GNA) residues.
        canon = [a for a, b in ds if {a, b} == {"3'", "5'"}]
        if not canon:
            direction = "3'"      # single residue; irrelevant
        else:
            if len(set(canon)) != 1:
                raise ValueError(f"mixed linkage directions in one strand: {set(canon)}")
            direction = canon[0]
        bases = [base_of(r) for r in res]
        sugars = [sugar_of(r) for r in res]
        ps = sum(1 for r in res if "p-thio" in r.lower())
        listed = "".join(bases)
        if direction == "3'":
            seq, listed_dir = listed, "listed 5'->3' (3'->5' linkages)"
            sug = sugars
        else:
            seq, listed_dir = listed[::-1], "listed 3'->5' (5'->3' linkages) - REVERSED"
            sug = sugars[::-1]
        out.append({
            "seq_5to3": seq,
            "n": len(res),
            "ps_linkages": ps,
            "sugars_5to3": sug,
            "direction_note": listed_dir,
            "residues_as_listed": res,
        })
    return out


def revcomp(s):
    m = {"A": "U", "U": "A", "T": "A", "G": "C", "C": "G"}
    return "".join(m[c] for c in reversed(s))


def report(list_no, name):
    lines = load(list_no)
    chem, region = entry_block(lines, name)
    forms = FORMULA.findall(region)
    print(f"\n===== {name}  (WHO Recommended INN List {list_no}) =====")
    strands = parse_strands(chem)
    for i, s in enumerate(strands, 1):
        print(f"  strand {i}: {s['n']} nt  PS={s['ps_linkages']}  {s['direction_note']}")
        print(f"    5'->3' : {s['seq_5to3']}")
        print(f"    sugars : {'-'.join(s['sugars_5to3'])}")
    if len(strands) == 2:
        a, b = strands[0]["seq_5to3"], strands[1]["seq_5to3"]
        print(f"    revcomp(sense)= {revcomp(a)}")
        print(f"    guide        = {b}")
    print(f"  formulas seen nearby: {sorted(set(forms))[:6]}")
    return strands, chem, forms


VALIDATION = {          # already in data/oligos.csv - must reproduce exactly
    "inotersen":  (77, 0, "TCTTGGTTACATGAAATCCC"),
    "nusinersen": (74, 0, "TCACTTTCATAATGCTGG"),
    "givosiran":  (76, 1, "UAAGAUGAGACACUCUUUCUGGU"),
    "inclisiran": (76, 1, "ACAAAAGCAAAACAGGUCUAGAA"),
    "vutrisiran": (81, 1, "UCUUGGUUACAUGAAAUCCCAUC"),
}


def self_test():
    """Reproduce five known sequences before trusting any new one."""
    ok = True
    for nm, (ln, si, want) in VALIDATION.items():
        got = parse_strands(entry_block(load(ln), nm)[0])[si]["seq_5to3"]
        good = got == want
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {nm:<12}{got}")
    print("self-test:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--self-test":
        raise SystemExit(0 if self_test() else 1)
    for arg in sys.argv[1:]:
        ln, nm = arg.split(":")
        report(int(ln), nm)
