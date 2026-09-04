#!/usr/bin/env python3
"""Download the article of record for every source the module reads.

    python3 src/fetch_papers.py            # fetch what is missing, verify everything
    python3 src/fetch_papers.py --force    # re-fetch even files already on disk

Writes to sources/papers/, which is gitignored: these are large binaries and the build does not
read them. The build reads the supplementary tables under each source's own folder, which ARE
committed. This script exists so the full-text articles can be reconstituted on demand, and so
the folder's README cannot claim a provenance the files do not have.

Two checks, because neither alone is enough:

  * the bytes must start %PDF-. A 200 response is not evidence of a PDF -- PMC answers a direct
    binary request with an HTML challenge page under HTTP 200, and a pipeline that trusts the
    status code writes that page to disk and calls it a paper.
  * the first two pages must contain a phrase unique to the expected article. Europe PMC has
    been observed returning one article's files for another's request, and a size check would
    not catch it.

Only open-access and public-domain material is fetched. Three sources the research read -- an
NEJM correspondence item and two Roche conference decks -- are copyrighted and not licensed for
redistribution; they are named in sources/papers/README.md so a reader can obtain their own
copy, and are deliberately absent here.
"""
from __future__ import annotations

import pathlib
import re
import sys
import urllib.error
import urllib.request

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "sources" / "papers"
UA = {"User-Agent": "Mozilla/5.0 (OligoTox-CNS provenance archive)"}

# (stem, retrieval route, identifier, a phrase that must appear in the first two pages)
PAPERS = [
    ("H1_Hagedorn2022_NucleicAcidTher", "pmc", "PMC9221153",
     "acute neurotoxicity of antisense oligonucleotides"),
    ("K1_Miller2024_MTNA_journal", "pmc", "PMC11567125",
     "preventing acute neurotoxicity"),
    ("K1_Miller2024_bioRxiv_preprint", "pmc", "PMC11185713",
     "preventing acute neurotoxicity"),
    ("L1_Kuroda2025_MTNA", "pmc", "PMC12744863",
     "late-onset neurotoxicity"),
    ("HV1_Buijsen2024_Biomedicines", "pmc", "PMC11428300",
     "calcium-enhanced medium"),
    ("HV2_Chen2024_Nature", "pmc", "PMC11043036",
     "timothy syndrome"),
    ("HV3_Woffindale2026_MTNA", "pmc", "PMC12925542",
     "multigene silencing"),
    ("O1_ORourke2026_NAR", "pmc", "PMC12865454",
     "gkaf1333"),
    ("B1_BravoHernandez2026_NAR", "pmc", "PMC12867516",
     "gkag057"),
    ("C1_QALSODY_tofersen_FDA_PI", "dailymed",
     "81356b45-1cb7-4eef-88ea-e44cc18b47c5", "qalsody"),
    ("C1_SPINRAZA_nusinersen_FDA_PI", "dailymed",
     "dd70cd5f-b0fc-4ba4-a5ea-89a34778bd94", "spinraza"),
]

ROUTES = {
    "pmc": ["https://europepmc.org/articles/{id}?pdf=render",
            "https://www.ebi.ac.uk/europepmc/webservices/rest/{id}/fullTextPDF"],
    "dailymed": ["https://dailymed.nlm.nih.gov/dailymed/downloadpdffile.cfm?setId={id}&type=display",
                 "https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?setid={id}&type=pdf"],
}


def verify(path: pathlib.Path, phrase: str) -> tuple[bool, str]:
    """The file must be a PDF, and it must be the RIGHT PDF."""
    if path.read_bytes()[:5] != b"%PDF-":
        return False, "not a PDF"
    doc = pymupdf.open(path)
    head = "".join(doc[i].get_text() for i in range(min(2, len(doc))))
    # OUP's typesetting letter-spaces its titles ("A cut e neuronal"), so compare with
    # whitespace collapsed out entirely rather than normalised to single spaces.
    flat = re.sub(r"\s+", "", head).lower()
    if re.sub(r"\s+", "", phrase).lower() not in flat:
        return False, f"wrong article: {phrase!r} not in first 2 pages"
    return True, f"{len(doc)} pages"


def main(argv: list[str]) -> int:
    force = "--force" in argv
    OUT.mkdir(parents=True, exist_ok=True)
    failed = []
    for stem, route, ident, phrase in PAPERS:
        suffix = ident if route == "pmc" else ident[:8]
        path = OUT / f"{stem}_{suffix}.pdf"
        if path.exists() and not force:
            ok, why = verify(path, phrase)
            print(f"  {'have  ' if ok else 'BAD   '}{path.name}  ({why})")
            if not ok:
                failed.append(path.name)
            continue
        for url in ROUTES[route]:
            try:
                body = urllib.request.urlopen(
                    urllib.request.Request(url.format(id=ident), headers=UA), timeout=180).read()
            except (urllib.error.URLError, OSError) as exc:
                print(f"  ..    {stem}: {type(exc).__name__}")
                continue
            if body[:5] != b"%PDF-":
                print(f"  ..    {stem}: {len(body):,} bytes, not a PDF")
                continue
            path.write_bytes(body)
            ok, why = verify(path, phrase)
            if ok:
                print(f"  OK    {path.name}  ({len(body):,} bytes, {why})")
                break
            path.unlink()
            print(f"  ..    {stem}: {why}")
        else:
            print(f"  FAIL  {stem} -- no route returned the expected article")
            failed.append(stem)

    print(f"\n{len(PAPERS) - len(failed)}/{len(PAPERS)} papers present and verified")
    if failed:
        print("missing or wrong: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
