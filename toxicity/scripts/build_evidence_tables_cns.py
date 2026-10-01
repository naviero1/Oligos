#!/usr/bin/env python3
"""Write the human-first evidence tables into the CNS dossiers, in place.

Every other generated table in this project is produced by a script and then
TRANSCRIBED into a document, with a checker to catch the transcription going
wrong. That checker exists because the transcription did go wrong once. This
script removes the step instead of guarding it: it writes between markers in the
dossier itself, so the numbers in the prose are the numbers in the data by
construction.

    <!-- BEGIN generated:evidence -->   ... replaced on every run ...
    <!-- END generated:evidence -->

What the tables encode:

  Human evidence comes first and animal evidence last, because Phase 2 asks for
  human-relevant data and a reader should not have to filter 1,863 animal rows to
  find 530 human ones. The bands are ordered by the strength of the human claim
  each supports, not by row count.

  Trials are counted from the trial register, never from rows. A trial with five
  dose arms contributes five rows and remains one trial; a trial reported by a
  registry posting AND a paper AND a label is still one trial.

  Molecule counts are deliberately NOT summed down the column. One molecule can
  carry rows in several bands, so the column does not add up, and a total would be
  wrong rather than merely unhelpful.

Usage:  python toxicity/scripts/build_evidence_tables_cns.py [--check]
"""
import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
ENDPOINTS = ["chronic-neurotoxicity", "hydrocephalus"]
BEGIN = "<!-- BEGIN generated:evidence -->"
END = "<!-- END generated:evidence -->"

# Display order and the one-line gloss each band carries in the table. The gloss
# is what stops a reader treating a label's pooled safety summary as a trial.
BANDS = [
    ("human_trial_registry", "Human trial — registry-posted results",
     "arms and denominators as posted"),
    ("human_trial_publication", "Human trial — peer-reviewed report",
     "registry identity verified separately; see the register"),
    ("human_trial_sponsor", "Human trial — sponsor or conference report",
     "no posted table, no peer review"),
    ("human_laboratory", "**Human laboratory** — in vitro / ex vivo",
     "patient-derived iPSC neurons, organoids, microglia, whole blood"),
    ("human_label_pooled", "Human — label / SmPC / EPAR, pooled",
     "pools a development programme; never one trial"),
    ("human_postmarketing", "Human — postmarketing signal assessment",
     "no exposure denominator"),
    ("human_case_report", "Human — case report or case series",
     "one patient each, however serious"),
    ("human_observational", "Human — observational cohort, exposed",
     "outside a trial protocol"),
    ("human_background_epi", "Human — disease background, unexposed",
     "no oligonucleotide given; a baseline rate, not an effect"),
    ("human_class_review", "Human — cross-compound review or atlas",
     "aggregates other studies' compounds"),
    ("animal_invivo", "Animal in vivo", "supporting material"),
    ("animal_laboratory", "Animal laboratory — in vitro", "supporting material"),
]
HUMAN = [b for b, _, _ in BANDS if b.startswith("human")]
TRIAL_TIER = ["human_trial_registry", "human_trial_publication", "human_trial_sponsor"]

# Why a grade-0 row is not a negative. The tier reasons come first, because they
# override a sound ascertainment: a row can be perfectly well measured and still
# not be a negative for the compound that was given.
INELIGIBLE_GLOSS = {
    "therapeutic_reduction": "the compound REDUCED the endpoint — measured, but an "
                             "efficacy result, not evidence the compound is non-toxic",
    "disease_background": "measured in patients given no oligonucleotide — a "
                          "baseline rate, not a negative for any compound",
    "threshold_limited_zero": "the table lists only terms above a frequency "
                              "cut-off, so the term's absence may be a reporting artefact",
    "not_assessed_in_source": "the source does not report this endpoint at all",
    "absence_of_label_warning": "the finding is a warning *not appearing* in a "
                                "label, which is a fact about the document",
    "review_required": "no ascertainment basis could be established from the "
                       "row's own source fields",
}


TIER_GLOSS = [
    ("ventricular_enlargement", "ventricular volume, ventriculomegaly, hydrocephalus "
                                "incidence, macrocephaly — the endpoint itself"),
    ("pressure_or_composition", "raised intracranial or CSF opening pressure, CSF "
                                "volume, outflow resistance, DTI-ALPS — supports a "
                                "mechanism, is not a confirmed hydrocephalus event"),
    ("related_clinical_sign", "papilloedema and optic findings — a pressure sign, "
                              "recorded separately because the two dissociate"),
    ("procedure_or_mechanism", "ependymal damage, cilia loss, meningitis, "
                               "arachnoiditis — mechanism and procedure effects"),
    ("disease_background", "measured in patients given no oligonucleotide: a "
                           "baseline rate, never an effect of a compound"),
    ("therapeutic_reduction", "the compound REDUCED the endpoint — an efficacy "
                              "result, not a toxicity negative"),
]


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt(n):
    return "{:,}".format(n)


def block(ep):
    meas = read(os.path.join(TOXDIR, "%s.measurements.csv" % ep))
    trials = read(os.path.join(TOXDIR, "%s.trials.csv" % ep))
    pending = read(os.path.join(TOXDIR, "%s.trials-pending.csv" % ep))
    cc = Counter(r["evidence_class"] for r in meas)
    human = sum(v for k, v in cc.items() if k in HUMAN)
    animal = len(meas) - human

    L = [BEGIN, ""]
    L.append("| Evidence class | Rows | Molecules | Sources | What it is |")
    L.append("|---|---:|---:|---:|---|")
    for key, label, gloss in BANDS:
        if not cc[key]:
            continue
        rs = [r for r in meas if r["evidence_class"] == key]
        L.append("| %s | %s | %d | %d | %s |"
                 % (label, fmt(len(rs)), len({r["oligo_id"] for r in rs}),
                    len({r["source_id"] for r in rs}), gloss))
    L.append("| **Human — all classes** | **%s** | — | — | %.0f%% of the endpoint |"
             % (fmt(human), 100.0 * human / len(meas)))
    L.append("| **Animal — all classes** | **%s** | — | — | %.0f%%, supporting material |"
             % (fmt(animal), 100.0 * animal / len(meas)))
    L.append("")
    L.append("Molecule counts do **not** sum down that column: one molecule can "
             "carry rows in several bands. Row counts do sum.")
    L.append("")

    # --- trials -----------------------------------------------------------
    trial_rows = sum(cc[k] for k in TRIAL_TIER)
    evaluable = [t for t in trials if t["endpoint_evaluable"] == "TRUE"]
    compounds = {o for t in trials for o in t["oligo_ids"].split("; ") if o}
    shared = [t for t in trials if t["also_in_endpoint"]]
    ext = [t for t in trials if t["participant_overlap"]]
    L.append("**Human clinical trials, counted as trials.** From "
             "[`%s.trials.csv`](./%s.trials.csv), one row per trial, never per "
             "measurement." % (ep, ep))
    L.append("")
    L.append("| | Count |")
    L.append("|---|---:|")
    L.append("| Verified unique human trials | **%d** |" % len(trials))
    L.append("| …with an endpoint-evaluable outcome | %d |" % len(evaluable))
    L.append("| …flagged by their own source as an extension or roll-over protocol | %d |"
             % len(ext))
    L.append("| …also contributing rows to the other CNS endpoint | %d |" % len(shared))
    L.append("| Pending candidates — a trial report naming no registry entry | %d |"
             % len(pending))
    L.append("| Human trial-derived measurement rows | %s |" % fmt(trial_rows))
    L.append("| Unique compounds across the verified trials | %d |" % len(compounds))
    L.append("| Human laboratory / ex-vivo measurement rows | %s |"
             % fmt(cc["human_laboratory"]))
    L.append("")
    if not cc["human_laboratory"]:
        L.append("The human-laboratory row is **zero, and stated rather than hidden**: "
                 "no in vitro or ex vivo human experiment in this corpus measures this "
                 "endpoint. Nothing was reclassified to fill it.")
        L.append("")
    L.append("Pending candidates are excluded from the verified total on purpose. "
             "A publication reporting a trial establishes the trial, but its registry "
             "identifier has to come from a document — supplying one from recall "
             "would be exactly the fabricated trial identifier this dataset refuses "
             "to contain.")
    L.append("")

    # --- negatives --------------------------------------------------------
    zero = [r for r in meas if r["neurotox_grade"] == "0"]
    elig = [r for r in zero if r["negative_eligible"] == "TRUE"]
    inel = [r for r in zero if r["negative_eligible"] == "FALSE"]
    tiers = Counter(r["hydroceph_tier"] for r in meas if r["hydroceph_tier"])
    if tiers:
        L.append("**Which hydrocephalus claim each row makes.** The endpoint is not "
                 "one thing, and `endpoint_domain` cannot carry the distinction — it "
                 "has a single `hydrocephalus` value, and its use in this corpus "
                 "drifted by extraction lane. `hydroceph_tier` is derived from the "
                 "readout instead, so it is lane-independent.")
        L.append("")
        L.append("| Tier | Rows | What it is |")
        L.append("|---|---:|---|")
        for key, gloss in TIER_GLOSS:
            if tiers[key]:
                L.append("| `%s` | %d | %s |" % (key, tiers[key], gloss))
        L.append("")

    L.append("**Which zeros are negatives.** A grade of 0 means four different "
             "things, and only two of them are a measured negative.")
    L.append("")
    L.append("| | Rows |")
    L.append("|---|---:|")
    L.append("| Grade-0 rows | %s |" % fmt(len(zero)))
    L.append("| …eligible as a measured negative (`negative_eligible=TRUE`) | %s |"
             % fmt(len(elig)))
    L.append("| …**not** eligible | %s |" % fmt(len(inel)))
    L.append("")
    if inel:
        L.append("The ineligible rows are kept, with their evidence, and excluded "
                 "from negative counts by one predicate:")
        L.append("")
        def why(r):
            # The tier overrides the ascertainment where it applies, so it is the
            # reason to report.
            if r["hydroceph_tier"] in ("therapeutic_reduction", "disease_background"):
                return r["hydroceph_tier"]
            return r["ascertainment"]
        for k, v in Counter(why(r) for r in inel).most_common():
            L.append("- `%s` — %d row(s): %s" % (k, v, INELIGIBLE_GLOSS.get(k, "")))
        L.append("")
    L.append(END)
    return "\n".join(L)


def main():
    check = "--check" in sys.argv
    stale = []
    for ep in ENDPOINTS:
        want = block(ep)
        for doc in ("%s.md" % ep,):
            path = os.path.join(TOXDIR, doc)
            text = open(path, encoding="utf-8").read()
            if BEGIN not in text or END not in text:
                raise SystemExit("ERROR: %s has no generated:evidence markers" % doc)
            new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: want,
                         text, flags=re.S)
            if new == text:
                print("%-26s up to date" % doc)
                continue
            if check:
                stale.append(doc)
                print("%-26s *** STALE ***" % doc)
            else:
                open(path, "w", encoding="utf-8").write(new)
                print("%-26s rewritten" % doc)
    if check and stale:
        raise SystemExit("\nERROR: %d document(s) stale — re-run without --check"
                         % len(stale))


if __name__ == "__main__":
    main()
