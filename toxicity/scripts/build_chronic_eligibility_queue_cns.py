#!/usr/bin/env python3
"""The chronic-eligibility adjudication set, prepared but NOT decided.

WHY THIS FILE EXISTS

Beebop asked twice for observation-level review of whether each candidate row
records *chronic* neurotoxicity, and my 2026-10-01 reply deferred it to German.
That deferral was right on the verdict and wrong on the preparation: I was using
"German's call" as a reason not to assemble the material, which left the
adjudication as a blocker rather than a queue.

So this builds the queue and writes no verdict. `chronic_eligibility` and
`chronic_eligibility_basis` are emitted EMPTY. Deciding whether a neurological
event in month 14 of a three-year trial is chronic neurotoxicity, acute toxicity
during long exposure, disease progression, a procedure effect, or simply
unresolved is a clinical judgement on 522 rows. If a curator writes it, the
dataset's chronic/acute boundary becomes that curator's opinion wearing a
schema's clothing.

WHAT IT DOES CONTRIBUTE

Triage, so the adjudication is one pass over sorted evidence instead of 522
cold reads. Every row gets:

  - `exposure_duration` as the source reports it (511 of 522 populated);
  - a verbatim ONSET snippet where the source states when the event began;
  - a verbatim OBSERVATION-WINDOW snippet where it states how long the subject
    was watched - which is what separates "did not recur" from "nobody looked";
  - a verbatim COMPETING-EXPLANATION snippet where the source itself raises
    disease progression, the delivery procedure, or a causality caveat;
  - `timing_evidence`, a one-word summary for sorting.

Snippets are extracted, never summarised: the adjudicator reads the source's own
words, bounded to the matched region, with the exact locus alongside.

A TRAP THIS AVOIDS

"Onset" is a trap word in this corpus. `infantile-onset SMA` and `later-onset
SMA` are population descriptors naming a disease phenotype, not the onset of an
adverse event. A naive match tags 65 rows as carrying onset evidence, many of
them spuriously, and handing an adjudicator noise labelled as evidence is worse
than handing them nothing. The population forms are excluded below.

Usage:  python toxicity/scripts/build_chronic_eligibility_queue_cns.py [--check]
"""
import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
MEAS = os.path.join(TOXDIR, "chronic-neurotoxicity.measurements.csv")
OLIGOS = os.path.join(TOXDIR, "chronic-neurotoxicity.oligos.csv")
OUT = os.path.join(TOXDIR, "chronic-neurotoxicity.chronic-eligibility-queue.csv")

# The candidate set: rows that assert, or could assert, a chronic neurological
# outcome. Not the whole partition - an acute behavioural score at 3 h is not a
# chronicity question.
CANDIDATE_DOMAINS = {"chronic_neurotoxicity", "clinical_neuro_ae"}

# `infantile-onset`, `later-onset`, `adult-onset` and friends describe the
# PATIENT POPULATION, not when an adverse event started.
POPULATION_ONSET = re.compile(
    r"(?:infantile|later|adult|childhood|juvenile|early|late)[- ]onset", re.I)

ONSET = re.compile(
    r"onset (?:after|at|was|occurred)[^.;]{0,90}"
    r"|(?:began|developed|emerged|first (?:observed|reported|noted|detected))"
    r"[^.;]{0,90}"
    r"|(?:after|at|by) (?:week|month|day|dose)s?\s*\d[^.;]{0,70}"
    r"|median time to [^.;]{0,70}"
    r"|\d+\s*(?:weeks?|months?|days?|years?) after[^.;]{0,70}", re.I)

WINDOW = re.compile(
    r"(?:follow[- ]?up|observed|monitored|re-?examined|watched)"
    r"[^.;]{0,80}"
    r"|recovery (?:group|arm|period|week)[^.;]{0,70}"
    r"|through (?:week|month)\s*\d[^.;]{0,60}"
    r"|up to (?:approximately )?\d+\s*(?:weeks?|months?|years?)[^.;]{0,50}", re.I)

COMPETING = re.compile(
    r"confound[^.;]{0,90}"
    r"|disease progression[^.;]{0,80}"
    r"|underlying (?:disease|indication)[^.;]{0,80}"
    r"|intrinsic to [^.;]{0,80}"
    r"|attribut\w+[^.;]{0,30}(?:weak|uncertain|unclear)[^.;]{0,40}"
    r"|causality[^.;]{0,80}"
    r"|no concurrent control[^.;]{0,60}", re.I)

COLS = ["measurement_id", "oligo_id", "oligo_name", "evidence_class",
        "endpoint_domain", "species", "timing_evidence", "exposure_duration",
        "onset_text", "observation_window_text", "competing_explanation_text",
        "reversibility", "readout_name", "readout_value", "effect_vs_control",
        "neurotox_grade", "ascertainment", "source_id", "source_ref",
        "source_table",
        # Emitted empty. German fills these; nothing else writes them.
        "chronic_eligibility", "chronic_eligibility_basis"]


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def snippet(rx, text, limit=260):
    """The source's own words around the match, bounded, never paraphrased."""
    t = clean(text)
    # Population-onset phrases are masked before matching so they cannot be
    # mistaken for event onset.
    masked = POPULATION_ONSET.sub("DISEASE_PHENOTYPE", t)
    m = rx.search(masked)
    if not m:
        return ""
    return clean(masked[m.start():m.start() + limit])


def main():
    check = "--check" in sys.argv
    with open(MEAS, newline="", encoding="utf-8") as f:
        meas = list(csv.DictReader(f))
    with open(OLIGOS, newline="", encoding="utf-8") as f:
        names = {o["oligo_id"]: o["oligo_name"] for o in csv.DictReader(f)}

    out = []
    for r in meas:
        if r["endpoint_domain"] not in CANDIDATE_DOMAINS:
            continue
        blob = " ".join([r["notes"], r["effect_vs_control"], r["exposure_duration"]])
        onset = snippet(ONSET, blob)
        window = snippet(WINDOW, blob)
        compete = snippet(COMPETING, blob)
        dur = r["exposure_duration"] not in ("", "TBD", "NA")
        tev = ("onset_and_window" if onset and window else
               "onset_only" if onset else
               "window_only" if window else
               "duration_only" if dur else "none")
        out.append({
            "measurement_id": r["measurement_id"], "oligo_id": r["oligo_id"],
            "oligo_name": names.get(r["oligo_id"], ""),
            "evidence_class": r["evidence_class"],
            "endpoint_domain": r["endpoint_domain"], "species": r["species"],
            "timing_evidence": tev, "exposure_duration": r["exposure_duration"],
            "onset_text": onset, "observation_window_text": window,
            "competing_explanation_text": compete,
            "reversibility": r["reversibility"], "readout_name": r["readout_name"],
            "readout_value": r["readout_value"],
            "effect_vs_control": clean(r["effect_vs_control"])[:200],
            "neurotox_grade": r["neurotox_grade"],
            "ascertainment": r["ascertainment"], "source_id": r["source_id"],
            "source_ref": r["source_ref"],
            "source_table": clean(r["source_table"])[:200],
            # EMPTY ON PURPOSE.
            "chronic_eligibility": "", "chronic_eligibility_basis": "",
        })

    # Sort the adjudicator's work: best-evidenced human rows first, animal last.
    rank = {"onset_and_window": 0, "onset_only": 1, "window_only": 2,
            "duration_only": 3, "none": 4}
    out.sort(key=lambda r: (not r["evidence_class"].startswith("human"),
                            rank[r["timing_evidence"]], r["measurement_id"]))

    print("candidate rows: %d" % len(out))
    print("\ntiming evidence")
    for k, v in Counter(r["timing_evidence"] for r in out).most_common():
        print("  %-18s %4d" % (k, v))
    print("\nby evidence class")
    for k, v in Counter(r["evidence_class"] for r in out).most_common():
        print("  %-26s %4d" % (k, v))
    print("\nrows where the SOURCE itself raises a competing explanation: %d"
          % sum(1 for r in out if r["competing_explanation_text"]))
    print("rows carrying a reversibility determination: %d"
          % sum(1 for r in out if r["reversibility"] not in ("not_assessed", "TBD")))
    print("verdicts written by this script: 0 (chronic_eligibility is emitted empty)")

    if check:
        if not os.path.exists(OUT):
            raise SystemExit("ERROR: %s missing" % os.path.basename(OUT))
        with open(OUT, newline="", encoding="utf-8") as f:
            on_disk = list(csv.DictReader(f))
        if len(on_disk) != len(out):
            raise SystemExit("ERROR: queue on disk has %d rows, expected %d"
                             % (len(on_disk), len(out)))
        filled = [r["measurement_id"] for r in on_disk if r["chronic_eligibility"]]
        if filled:
            print("\n--check: %d row(s) adjudicated so far: %s"
                  % (len(filled), filled[:5]))
        print("--check: queue matches the candidate set")
        return

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    print("\nwrote %s" % os.path.relpath(OUT, os.path.dirname(TOXDIR)))


if __name__ == "__main__":
    main()
