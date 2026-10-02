#!/usr/bin/env python3
"""Give each acute-neurotoxicity instrument its own unit string.

THE DEFECT

485 rows carried `readout_unit = score_0_to_7`. Five sources use that string, and
their own notes define THREE DIFFERENT INSTRUMENTS:

  US10968453B2 / US9605263B2 / US9683235B2
      "rat functional observational battery, 7 regions (tail, hind paws, hind
       legs, hind end, front posture, fore paws, head), 0/1 each, summed 0-7"
      A COUNT of affected regions.

  doi:10.1093/nar/gkaf1333
      "Rodent intrathecal acute-inhibition scale: 0 bright/alert/responsive;
       1 tail without tone; 2 drooping hind end or abnormal hindlimb gait;
       3 hind limbs cannot support weight; ... 6 forelimbs immobile"
      An ORDINAL SEVERITY RANK, not a count.

  doi:10.1093/nar/gkag057
      "Acute neuronal activation (aA) response: shaking, muscle twitching,
       cramping, hyperactivity, hyperreactivity, vocalisation, tremors,
       convulsions and seizures, peaking ~15 min after intrathecal [dosing]"
      The OPPOSITE PHENOTYPE, on a different observation window.

Pooling the column averages a paralysed animal with a seizing one. The Phase 2
judging criteria score "consistency with FAIR data principles" and whether
"researchers would have any concerns or hesitation in making use of this
dataset"; one unit string naming three instruments fails interoperability, and a
consumer who groups on it gets nonsense.

WHAT THIS PASS DOES, AND WHAT IT REFUSES TO DO

It SEPARATES. It does not merge, re-grade, or decide whether the three may ever
be pooled - that is German's call and nothing needs it answered to keep them
apart. Separation is the safe direction: it can be undone by a consumer who
later learns two instruments are equivalent, while a silent merge cannot be
undone at all.

The direction of the phenotype is written into the unit name rather than added as
a separate column, because a sparse column is easy to drop in an export and the
unit string is what a consumer groups on. The observation window needs no new
field: `exposure_duration` already separates `3h`, `8wk`, `0-15min_post_single_dose`
and `0-120min_post_dose`.

Every mapping below is read from the cited source's own transcribed definition in
the affected rows' `notes`. No instrument is inferred from a title or a range.

Usage:  python toxicity/scripts/disambiguate_scales_cns.py [--check]
"""
import csv
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
CORPUS = os.path.join(TOXDIR, "notes", "cns", "corpus", "cns_measurements.csv")

AMBIGUOUS = "score_0_to_7"

# source_ref -> the instrument that source's own notes describe.
INSTRUMENT = {
    "US10968453B2": "score_0_to_7_fob7_regional_sum",
    "US9605263B2": "score_0_to_7_fob7_regional_sum",
    "US9683235B2": "score_0_to_7_fob7_regional_sum",
    "doi:10.1093/nar/gkaf1333": "score_0_to_7_ordinal_inhibition_ladder",
    "doi:10.1093/nar/gkag057": "score_0_to_7_acute_activation",
}


def main():
    check = "--check" in sys.argv
    with open(CORPUS, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols, rows = list(rdr.fieldnames), list(rdr)

    done = Counter(r["readout_unit"] for r in rows
                   if r["readout_unit"].startswith(AMBIGUOUS + "_"))
    todo = [r for r in rows if r["readout_unit"] == AMBIGUOUS]

    unmapped = sorted({r["source_ref"] for r in todo} - set(INSTRUMENT))
    if unmapped:
        raise SystemExit(
            "ERROR: %d source(s) use %r with no instrument mapping: %s\n"
            "Read that source's own scale definition and add it to INSTRUMENT "
            "rather than letting a new instrument inherit an existing name."
            % (len(unmapped), AMBIGUOUS, unmapped))

    changed = Counter()
    for r in todo:
        new = INSTRUMENT[r["source_ref"]]
        r["readout_unit"] = new
        changed[new] += 1

    if done and not todo:
        print("already disambiguated:")
        for k, v in done.most_common():
            print("  %-42s %4d" % (k, v))
    for k, v in changed.most_common():
        print("  %-42s %4d rows" % (k, v))
    print("\n%d row(s) still carry the ambiguous %r" % (
        sum(1 for r in rows if r["readout_unit"] == AMBIGUOUS), AMBIGUOUS))

    if check:
        if todo:
            raise SystemExit("ERROR: %d row(s) still ambiguous — re-run without "
                             "--check" % len(todo))
        print("--check: no ambiguous scale units remain")
        return
    if not todo:
        return
    with open(CORPUS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("wrote %s" % os.path.relpath(CORPUS, os.path.dirname(TOXDIR)))


if __name__ == "__main__":
    main()
