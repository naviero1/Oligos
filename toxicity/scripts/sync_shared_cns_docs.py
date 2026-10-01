#!/usr/bin/env python3
"""Keep the duplicated CNS documents identical, and say so at the top of each.

The CNS curation covered both named CNS endpoints as one corpus, so six of its
documents describe the whole corpus rather than either partition. The chosen
layout is that each toxicity is self-contained — a shared document is COPIED into
every toxicity that relies on it rather than referenced out of a common folder.

Copies drift. They drifted the first time a generator wrote only the master copy
and the duplicate kept a stale row count. This script is what makes the layout
safe: one master, one derived copy, a banner that names both, and a `--check` mode
so a stale duplicate is a failure rather than a surprise.

Master is the `chronic-neurotoxicity.*` copy, for no better reason than that it is
the larger partition; the content is identical either way.

Usage:  python toxicity/scripts/sync_shared_cns_docs.py [--check]
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)

MASTER, COPY = "chronic-neurotoxicity", "hydrocephalus"
SHARED = ["corpus-overview", "methodology", "next-steps", "schema", "sources",
          "verification"]

BANNER = """> **Shared CNS-corpus document, duplicated here.** The CNS curation covered both
> named CNS endpoints as one corpus, so this document describes the whole corpus
> ({corpus:,} measurements), not the {part:,}-row {copy} partition alone. It is copied into each
> toxicity that relies on it rather than shared from a common folder, so every
> toxicity is self-contained. The counterpart copy is `{master}.{stem}.md`.
> Both copies are written by `scripts/sync_shared_cns_docs.py`; edit the master.

"""


def nrows(p):
    with open(p, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def main():
    check = "--check" in sys.argv
    corpus = nrows(os.path.join(TOXDIR, "notes", "cns", "corpus", "cns_measurements.csv"))
    part = nrows(os.path.join(TOXDIR, "%s.measurements.csv" % COPY))
    stale = []
    for stem in SHARED:
        mp = os.path.join(TOXDIR, "%s.%s.md" % (MASTER, stem))
        cp = os.path.join(TOXDIR, "%s.%s.md" % (COPY, stem))
        if not os.path.exists(mp):
            print("%-22s master missing — skipped" % stem)
            continue
        body = open(mp, encoding="utf-8").read()
        # A master that itself carries a banner would double it on the next run.
        body = re.sub(r"\A(?:> .*\n)+\n", "", body)
        want = BANNER.format(corpus=corpus, part=part, copy=COPY, master=MASTER,
                             stem=stem) + body
        got = open(cp, encoding="utf-8").read() if os.path.exists(cp) else None
        if got == want:
            print("%-22s in sync" % stem)
            continue
        if check:
            stale.append(stem)
            print("%-22s *** STALE ***" % stem)
        else:
            open(cp, "w", encoding="utf-8").write(want)
            print("%-22s rewritten from master" % stem)
    if check and stale:
        raise SystemExit("\nERROR: %d duplicate(s) stale — re-run without --check: %s"
                         % (len(stale), ", ".join(stale)))


if __name__ == "__main__":
    main()
