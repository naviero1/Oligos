#!/usr/bin/env python3
"""Derive the evidence taxonomy the CNS corpus needs to be counted honestly.

Adds six derived columns to the corpus measurement table. Nothing here reads a
new document: every value is computed from columns the rows already carry, so the
pass is reproducible, reversible (delete the columns and re-run) and cannot
introduce a fact that no source supports.

WHY EACH COLUMN EXISTS

`evidence_class` — `study_type` conflates things that must be counted apart. It
    has three values (clinical / animal_invivo / in_vitro), so a rat cortical
    culture and a patient-derived iPSC neuron are both "in_vitro", and a
    registry-posted trial table, a label's pooled safety summary and a single
    case report are all "clinical". A human-first presentation is impossible on
    that column. `evidence_class` splits it along the two axes that matter —
    human versus animal, and what kind of observation it is — so "no animal row
    contributes to a human total" becomes a predicate rather than a promise.

`trial_key` / `trial_key_basis` — measurement rows are not trials. One trial can
    reach this corpus as a registry posting, a publication and a label summary,
    and a trial with five arms contributes five rows. Counting trials needs a key
    that collapses those, and a record of HOW the key was established, because a
    registry identifier read off the posted record and one transcribed from a
    paper's registration sentence are not equally strong. No identifier is ever
    invented: a row whose source names no registry entry gets a publication-
    anchored key and is excluded from verified trial totals.

`ascertainment` — a grade of 0 can mean four different things: an assay measured
    no effect; a safety table reported the event with a zero count; a table with
    a frequency cut-off did not list the term; or the document never assessed the
    endpoint at all. Only the first two are negatives. Without this column all
    four look identical to a model.

`negative_eligible` — the single predicate that follows from `ascertainment`, so
    the eligible-negative count is reproducible instead of argued.

`event_cluster` — ClinicalTrials.gov posts serious and non-serious events in
    separate tables and the same participant may appear in both. Both counts are
    real and both are kept, but they are not independent events; rows sharing a
    cluster carry OVERLAP POTENTIAL, not demonstrated double reporting: a trial
    can genuinely report one serious and one non-serious event of the same term
    in the same arm, in different participants. Establishing that the same
    participant episode was counted twice needs source-level participant
    identifiers, which posted results do not provide. Beebop's 2026-10-02
    review made this point and it is correct.

Usage:  python toxicity/scripts/classify_evidence_cns.py [--check]
        --check  recompute and report disagreement with what is on disk
"""
import csv
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TOXDIR = os.path.dirname(HERE)
CORPUS = os.path.join(TOXDIR, "notes", "cns", "corpus", "cns_measurements.csv")

NEW_COLS = ["evidence_class", "trial_key", "trial_key_basis",
            "ascertainment", "negative_eligible", "event_cluster",
            "hydroceph_tier"]

NCT = re.compile(r"NCT\d{8}")


def norm(s):
    return re.sub(r"\s+", " ", ("" if s is None else str(s)).strip())


def low(s):
    return norm(s).lower()


def blob(r):
    """Everything the row says about its own provenance and comparison."""
    return low(" ".join([r.get("notes", ""), r.get("source_table", ""),
                         r.get("effect_vs_control", ""), r.get("readout_name", "")]))


# ---------------------------------------------------------------------------
# What kind of human evidence each clinical source is.
#
# Read off each source's own `source_ref` and `source_table` during curation, not
# inferred from the publisher. The distinctions that drive the tiers:
#   - a REGISTRY POSTING carries arms and denominators at the grain of this
#     dataset, and is the only class that can establish a trial by itself;
#   - a PUBLICATION reports a trial but its registry identity has to be
#     established separately before the trial can be counted;
#   - a SPONSOR COMMUNICATION (slide deck, press release) reports trial data with
#     no peer review and no posted table behind it;
#   - a LABEL or EPAR pools a whole programme, so it is never one trial;
#   - a POSTMARKETING SIGNAL record has no exposure denominator at all;
#   - a CASE REPORT is one patient, however serious;
#   - an OBSERVATIONAL cohort measures exposed humans outside a trial;
#   - a CLASS REVIEW aggregates other people's compounds.
# An unlisted clinical source_id is a hard error rather than a default, so a new
# source cannot be silently counted in the wrong tier.
# ---------------------------------------------------------------------------
CLINICAL_CLASS = {
    # -- peer-reviewed reports of interventional trials -----------------------
    "CP_TABRIZI2019": "human_trial_publication",
    "CP_MILLER2026_JAMANEUROL": "human_trial_publication",
    "CP_MUMMERY2023_NATMED": "human_trial_publication",
    "CP_FINKEL2017_ENDEAR": "human_trial_publication",
    "CP_MERCURI2018_CHERISH": "human_trial_publication",
    "CP_DEVOTE_NATMED2026": "human_trial_publication",
    "CP_DEVOTE_PARTA_JND2023": "human_trial_publication",
    "CP_KCNT1_NATMED2026": "human_trial_publication",
    "CP_LAUX2026_NEJM": "human_trial_publication",
    "CP_SHNEIDER2025_LANCET": "human_trial_publication",
    "CP_VANDENBERG2024_LANCETNEUROL": "human_trial_publication",
    "CP_MABROUK2026_NATMED": "human_trial_publication",
    "CP_BIIB080_NATAGING2026": "human_trial_publication",
    "CP_HIPP2025_NATMED": "human_trial_publication",
    "CP_KIM2019_NEJM": "human_trial_publication",
    "CP_LOVETT2025_MUSNERVE": "human_trial_publication",
    "CNSSRC_MUSCLENERVE2025_TOFERSEN": "human_trial_publication",
    # -- sponsor / conference / press communications of trial data ------------
    "CP_CHDI2021_SCHOBEL": "human_trial_sponsor",
    "CNSSRC_CHDI2021_SCHOBEL": "human_trial_sponsor",
    "CP_CHDI2022_BOAK": "human_trial_sponsor",
    "CP_CHDI2023_MCCOLGAN": "human_trial_sponsor",
    "CP_HDBUZZ_GENHD2_2026": "human_trial_sponsor",
    "CP_BIOGEN_PR_20240516": "human_trial_sponsor",
    "CP_IONIS_PR_HALOS_20240722": "human_trial_sponsor",
    "CP_IONIS_PR_ZILG_20250922": "human_trial_sponsor",
    # -- labels, SmPCs, EPARs: pooled across a programme ----------------------
    "CNSSRC_QALSODY_EPAR": "human_label_pooled",
    "CNSSRC_SPINRAZA_SMPC": "human_label_pooled",
    "CNSSRC_SPINRAZA_USPI": "human_label_pooled",
    "CNSSRC_SPINRAZA_EMA_VAR0038": "human_label_pooled",
    # -- postmarketing signal assessments: no exposure denominator -----------
    "R7": "human_postmarketing",
    "R8": "human_postmarketing",
    # -- individual cases and case series ------------------------------------
    "CNSSRC_JND2023_ICH_ARACHNOIDCYST": "human_case_report",
    "CNSSRC_TOZAWA2020": "human_case_report",
    "CNSSRC_STOKER2021": "human_case_report",
    "CNSSRC_BECKER2021": "human_case_report",
    "CP_JNEUROL2024_MYELITIS": "human_case_report",
    "CP_JNEUROL2025_MTX": "human_case_report",
    "CNSSRC_SPINRAZA_DHPC2018": "human_case_report",
    "CP_N1C_NAR2025": "human_case_report",
    # -- observational cohorts in exposed humans -----------------------------
    "HB_GROULX2024": "human_observational",
    "HB_LAN2026": "human_observational",
    "HB_VISCIDI2021": "human_observational",
    # -- cross-compound reviews and atlases ----------------------------------
    "SafeSense2026": "human_class_review",
    "CP_BIODRUGS2022_HD_ASO_REVIEW": "human_class_review",
}

# FDA labels and EU SmPCs entered under short regulatory ids. Rx and the EPAR
# pool a whole development programme, so none of them is one trial.
LABEL_ID = re.compile(r"^R\d+$")

# Display order. Human evidence first, in descending strength of the human
# claim it supports; animal evidence last, as supporting material.
CLASS_ORDER = [
    "human_trial_registry",
    "human_trial_publication",
    "human_trial_sponsor",
    "human_laboratory",
    "human_label_pooled",
    "human_postmarketing",
    "human_case_report",
    "human_observational",
    "human_background_epi",
    "human_class_review",
    "animal_invivo",
    "animal_laboratory",
]
HUMAN_TRIAL_TIER = {"human_trial_registry", "human_trial_publication",
                    "human_trial_sponsor"}
HUMAN = {c for c in CLASS_ORDER if c.startswith("human")}


def evidence_class(r):
    st, sp = low(r.get("study_type")), low(r.get("species"))
    if st != "clinical":
        if st == "animal_invivo":
            return "animal_invivo"
        return "human_laboratory" if sp == "human" else "animal_laboratory"
    if sp != "human":
        raise SystemExit("ERROR: clinical row %s has species=%r"
                         % (r.get("measurement_id"), r.get("species")))
    sid = norm(r.get("source_id"))
    if sid.startswith("CT_NCT") or sid.startswith("CNSSRC_CTG_NCT"):
        return "human_trial_registry"
    # CLINICAL_CLASS is consulted BEFORE the label pattern: R7 and R8 are a PSUSA
    # conclusion and a PRAC agenda item, which share the `R<n>` shape the labels
    # use but are pharmacovigilance signal records with no exposure denominator.
    if sid in CLINICAL_CLASS:
        cls = CLINICAL_CLASS[sid]
        # A cohort row measuring humans with NO oligonucleotide exposure is
        # background disease epidemiology, not evidence about a compound. Only
        # the row itself says which it is.
        if cls == "human_observational" and "no_oligo_exposure" in low(r.get("readout_name")):
            return "human_background_epi"
        return cls
    if LABEL_ID.match(sid):
        return "human_label_pooled"
    raise SystemExit(
        "ERROR: clinical source_id %r (row %s) is not classified. Add it to "
        "CLINICAL_CLASS with the class its own source_ref/source_table supports."
        % (sid, r.get("measurement_id")))


def trial_key(r, cls):
    """A key that collapses every representation of one trial, or nothing.

    Never invents an identifier. Three bases, in descending strength:
      registry_posting — the row IS a posted registry record;
      named_in_source  — the row's own source fields name exactly one registry
                         entry, so the link is transcribed rather than recalled;
      publication_only — a trial report with no registry entry named anywhere in
                         the row. Keyed on the publication so its rows still
                         collapse, and excluded from verified trial totals.
    """
    if cls not in HUMAN_TRIAL_TIER:
        return "", "not_a_trial"
    direct = NCT.search(norm(r.get("source_ref")))
    if direct:
        return direct.group(0), "registry_posting"
    found = set(NCT.findall(" ".join([norm(r.get("notes")),
                                      norm(r.get("source_table")),
                                      norm(r.get("source_ref"))])))
    # More than one registry entry named in one row means the row cannot be
    # attributed to a single trial without reading the source again. Left
    # unkeyed on purpose rather than guessed at.
    if len(found) == 1:
        return found.pop(), "named_in_source"
    return "PUB:%s" % norm(r.get("source_id")), "publication_only"


# ---------------------------------------------------------------------------
# Ascertainment evidence, matched against what the row itself records.
# ---------------------------------------------------------------------------
# The readout IS the absence of a warning from a label. A label's silence is an
# editorial and regulatory fact about the document, not a measurement of a
# patient, and it carries no denominator.
ABSENCE_OF_WARNING = re.compile(r"warning_absent_from_label|none_reported_in_label")
# The readout records that the document reports no CNS endpoint at all. An
# endpoint that was never assessed cannot be a negative result for it. One of
# these rows states this outright in its own notes: "carcinogenicity studies have
# not been conducted ... no CNS or neurobehavioral endpoint is reported".
NOT_ASSESSED = re.compile(r"none_reported_in_nonclinical")
# The source states that it reported EVERY event, with no frequency cut-off, so
# the term's absence is a true zero.
EXHAUSTIVE = re.compile(r"frequencythreshold\s*=\s*0|no frequency cut-?off"
                        r"|all adverse events are reported|whole section read"
                        r"|both read in full|prints no adverse-reaction table"
                        r"|complete posted ae tables|full table inspected")
# The source states the endpoint was looked for and not found.
ASSESSED_NONE = re.compile(
    r"\bnoael\b|no adverse findings|was well tolerated"
    r"|no (?:participant|patient|subject|animal)s? (?:in [^.]{0,40})?(?:had|has|showed|"
    r"developed|reported|experienced)[^.]{0,40}(?:no |zero |evidence of )?"
    r"|no evidence of|none (?:were )?(?:reported|observed|detected|seen)"
    r"|no (?:treatment-related |drug-related )?(?:cns|neuro\w*) (?:finding|effect|signal)s?")
# The table only lists terms at or above a frequency cut-off, so absence of the
# term may be a reporting artefact rather than a zero.
THRESHOLDED = re.compile(r"[>≥]=?\s*\d+\s*%|at least \d+\s*%|threshold of \d+\s*%"
                         r"|frequencythreshold\s*=\s*[1-9]")
# A denominator is present in the row's own comparison or notes.
DENOM = re.compile(r"\b\d+\s*(?:_| )?of(?:_| )\s*\d+\b|\b\d+\s*/\s*\d+\b|\bn\s*=\s*\d+")

# The readout_value is itself a zero — no event, no change, nothing measured
# above background — as opposed to a number that happens to be unremarkable.
ZERO_VALUE = re.compile(r"^0(?:\.0+)?$|^0_of_\d+$|^0/\d+$", re.I)
# A zero that carries its own denominator, i.e. the source printed the term
# against a stated roster and the count was nought.
ZERO_WITH_DENOM = re.compile(r"^0_of_\d+$|^0/\d+$", re.I)
# The row states what it was compared against. A quantity reported against a
# named comparator is a measurement even where the arm sizes are not repeated in
# this row - "-2.6 percentage points vs placebo" is a measured contrast.
COMPARATOR = re.compile(r"v(?:s|ersus)\.?[ _]+(?:placebo|control|comparator|sham"
                        r"|untreated|baseline|wt|wild)|placebo[- ]controlled"
                        r"|[_ ]vs[_ ]|vs_control")
HAS_NUMBER = re.compile(r"-?\d")

MEASURED = "measured"
ASSESSED_NO_EFFECT = "assessed_no_effect"
EXPLICIT_ZERO = "explicit_zero_with_denominator"
THRESHOLD_ZERO = "threshold_limited_zero"
NOT_ASSESSED_IN_SOURCE = "not_assessed_in_source"
ABSENCE_LABEL = "absence_of_label_warning"
REPORTED_EVENT = "reported_event"
REVIEW = "review_required"

# Which ascertainment categories let a grade-0 row stand as a negative. The set is
# short on purpose: everything else is an absence in a document, and an absence in
# a document is not a measurement.
NEGATIVE_ELIGIBLE = {MEASURED, ASSESSED_NO_EFFECT, EXPLICIT_ZERO}


def ascertainment(r, cls):
    name, b = low(r.get("readout_name")), blob(r)
    grade = norm(r.get("neurotox_grade"))
    zero = grade == "0"

    if ABSENCE_OF_WARNING.search(name):
        return ABSENCE_LABEL
    if NOT_ASSESSED.search(name):
        return NOT_ASSESSED_IN_SOURCE

    if cls not in HUMAN:
        # A laboratory assay or an animal study produced a value for this
        # readout. Whether the value is an effect or not, it was measured.
        return MEASURED if not zero else (
            ASSESSED_NO_EFFECT if ASSESSED_NONE.search(b) else MEASURED)
    if cls == "human_laboratory":
        return MEASURED if not zero else (
            ASSESSED_NO_EFFECT if ASSESSED_NONE.search(b) else MEASURED)

    # Human non-laboratory evidence.
    if not zero:
        return REPORTED_EVENT
    if cls == "human_postmarketing":
        # Spontaneous reporting has no exposure denominator, so it can never
        # supply a measured negative, whatever the row's grade.
        return NOT_ASSESSED_IN_SOURCE

    # What the row actually holds decides which question to ask. A grade-0 row
    # is NOT automatically an absence: a trial that reported dizziness in 4/72
    # on drug against 3/36 on placebo measured the endpoint and found no excess.
    # That is a measurement, and only rows whose value IS an absence need the
    # ascertainment analysis below.
    val = norm(r.get("readout_value"))
    if val in ("", "TBD", "NA"):
        return REVIEW
    if not ZERO_VALUE.match(val):
        if DENOM.search(b):
            return MEASURED
        # No arm sizes in the row, but a number reported against a named
        # comparator is still a measured contrast. A qualitative claim - "reduction
        # relative to placebo; magnitude not given" - is not, and falls through.
        if HAS_NUMBER.search(val) and COMPARATOR.search(b):
            return MEASURED
        return REVIEW

    # The value is a zero.
    if THRESHOLDED.search(b) and not ZERO_WITH_DENOM.match(val):
        return THRESHOLD_ZERO
    if ZERO_WITH_DENOM.match(val) or DENOM.search(b):
        # "0_of_147", or a bare 0 whose comparison spells the rosters out
        # ("0.0pct_vs_0.3pct_control (0/781 vs 2/778)"), is the source reporting
        # the term against a stated roster. A table that only prints terms above a
        # frequency cut-off never prints a zero row at all, so a zero WITH its
        # denominator is an exhaustive report for that term.
        return EXPLICIT_ZERO
    if EXHAUSTIVE.search(b) and DENOM.search(b):
        return EXPLICIT_ZERO
    if ASSESSED_NONE.search(b) and DENOM.search(b):
        return ASSESSED_NO_EFFECT
    if THRESHOLDED.search(b):
        return THRESHOLD_ZERO
    return REVIEW



# ---------------------------------------------------------------------------
# Hydrocephalus is not one endpoint, and the rows that bear on it are not
# interchangeable. Ventricular enlargement measured on protocol imaging, a raised
# opening pressure, an optic-disc sign, ependymal cilia failing in culture, a
# background rate in unexposed patients and an ASO that REDUCES hydrocephalus in a
# disease model are six different kinds of claim. `endpoint_domain` cannot carry
# that: it has one `hydrocephalus` value, and in this corpus its use drifted by
# extraction lane - 10 papilloedema rows sit under `hydrocephalus` and 4 under
# `clinical_neuro_ae`, including two readings of the SAME trial under two lanes.
#
# `hydroceph_tier` is derived from the readout instead, so it is lane-independent
# and consistent by construction. The curated `endpoint_domain` is left alone: this
# column adds a distinction rather than overwriting a judgement.
# ---------------------------------------------------------------------------
TIERS = [
    # A disease-background row measures humans given no oligonucleotide. It is a
    # baseline rate, and it is checked first because it must never be read as an
    # effect of a compound.
    ("disease_background", re.compile(r"no_oligo_exposure|_mixed_DMT_not_stratified")),
    # The compound REDUCED the endpoint. Checked before the enlargement tier, since
    # the readout name is the same one.
    ("therapeutic_reduction", None),          # decided on effect_direction, below
    # Ventricular enlargement measured as such: volume, dilatation,
    # ventriculomegaly, a hydrocephalus diagnosis. NOT macrocephaly - see below.
    ("ventricular_enlargement", re.compile(
        r"ventricul|ventricle|hydroceph|arachnoid_space|brain_volume"
        r"|macrostructural")),
    ("pressure_or_composition", re.compile(
        r"intracranial_pressure|csf_pressure|csf_outflow|csf_volume|alps_index"
        r"|opening_pressure")),
    ("procedure_or_mechanism", re.compile(
        r"ependymal|cilia|ciliary|meningitis|arachnoiditis|myelitis")),
    # A surrogate SIGN of raised volume or pressure, not a measurement of it.
    # `acquired_macrocephaly` is a MedDRA adverse-event term from a serious-AE
    # table - head circumference crossing a percentile in an infant, with no
    # imaging reported in the source. It is highly suggestive and it is not
    # ventricular enlargement, exactly as papilloedema is not. Beebop's
    # 2026-10-02 review asked for this audit; the source table settles it.
    # Whether infant macrocephaly should count as a direct hydrocephalus endpoint
    # is a clinical judgement reserved for German.
    ("related_clinical_sign", re.compile(
        r"papill|optic|vision|visual|macrocephal")),
]


def hydroceph_tier(r, asc):
    """Which kind of hydrocephalus claim a row makes, or blank if it makes none."""
    if norm(r.get("endpoint_domain")) not in ("hydrocephalus", "clinical_neuro_ae"):
        return ""
    name = low(r.get("readout_name"))
    if norm(r.get("endpoint_domain")) == "clinical_neuro_ae" \
            and not re.search(r"papill|optic|hydroceph|ventricul|intracranial", name):
        return ""
    for tier, pat in TIERS:
        if tier == "therapeutic_reduction":
            # A grade-0 row whose direction is a FALL in the endpoint, in a disease
            # model, is the compound working - not a measurement of its toxicity.
            if (low(r.get("effect_direction")) == "decrease"
                    and norm(r.get("neurotox_grade")) == "0"
                    and re.search(r"hydroceph|ventricul", name)):
                return tier
            continue
        if pat and pat.search(name):
            return tier
    return "related_clinical_sign"


def negative_eligible(r, asc, tier=""):
    if norm(r.get("neurotox_grade")) != "0":
        return "NA"
    # A grade of 0 reached because the compound IMPROVED the endpoint is not
    # evidence that the compound is non-toxic. It is an efficacy result in a
    # disease model, and counting it as a negative control would teach a model
    # that this molecule is safe on the strength of it working.
    if tier == "therapeutic_reduction":
        return "FALSE"
    # A background rate in patients given no oligonucleotide is not a negative
    # for any compound either.
    if tier == "disease_background":
        return "FALSE"
    return "TRUE" if asc in NEGATIVE_ELIGIBLE else "FALSE"


def event_cluster(r, tkey):
    """One reported episode, however many severity tables list it.

    Only defined where it can be: a registry posting that splits one arm's
    events into a serious and a non-serious table. Elsewhere blank rather than
    a key that means nothing.
    """
    t = low(r.get("source_table"))
    if not tkey.startswith("NCT"):
        return ""
    if not ("seriousevents" in t or "otherevents" in t
            or "not including serious" in t or "serious adverse event" in t):
        return ""
    arm = ""
    m = re.search(r"arm=([^|]+)$", norm(r.get("source_table")))
    if m:
        arm = m.group(1)
    else:
        m = re.search(r",\s*([^,]*arm)\s*$", norm(r.get("source_table")))
        arm = m.group(1) if m else ""
    key = re.sub(r"[^a-z0-9]", "", low(arm))
    if not key:
        return ""
    return "%s|%s|%s" % (tkey, key, re.sub(r"[^a-z0-9]", "", low(r.get("readout_name"))))


def main():
    check = "--check" in sys.argv
    with open(CORPUS, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        cols, rows = list(rdr.fieldnames), list(rdr)

    before = {r["measurement_id"]: {c: r.get(c) for c in NEW_COLS} for r in rows}
    for r in rows:
        cls = evidence_class(r)
        tkey, basis = trial_key(r, cls)
        asc = ascertainment(r, cls)
        tier = hydroceph_tier(r, asc)
        r["evidence_class"] = cls
        r["trial_key"] = tkey
        r["trial_key_basis"] = basis
        r["ascertainment"] = asc
        r["negative_eligible"] = negative_eligible(r, asc, tier)
        r["event_cluster"] = event_cluster(r, tkey)
        r["hydroceph_tier"] = tier

    out_cols = cols + [c for c in NEW_COLS if c not in cols]

    print("evidence_class (%d rows)" % len(rows))
    cc = Counter(r["evidence_class"] for r in rows)
    for c in CLASS_ORDER:
        if cc[c]:
            band = ("HUMAN " if c in HUMAN else "animal")
            print("  %-6s %-26s %5d" % (band, c, cc[c]))
    unknown = set(cc) - set(CLASS_ORDER)
    if unknown:
        raise SystemExit("ERROR: class not in CLASS_ORDER: %s" % sorted(unknown))
    print("  %-6s %-26s %5d" % ("", "HUMAN total",
                                sum(v for k, v in cc.items() if k in HUMAN)))
    print("  %-6s %-26s %5d" % ("", "of which trial-derived",
                                sum(v for k, v in cc.items() if k in HUMAN_TRIAL_TIER)))

    print("\ntrial_key_basis")
    for k, v in Counter(r["trial_key_basis"] for r in rows).most_common():
        print("  %-20s %5d" % (k, v))
    verified = {r["trial_key"] for r in rows
                if r["trial_key_basis"] in ("registry_posting", "named_in_source")}
    pending = {r["trial_key"] for r in rows if r["trial_key_basis"] == "publication_only"}
    print("  distinct verified trial keys  %4d" % len(verified))
    print("  distinct pending (publication-only) keys %4d" % len(pending))

    print("\nascertainment")
    for k, v in Counter(r["ascertainment"] for r in rows).most_common():
        flag = "" if k in NEGATIVE_ELIGIBLE or k == REPORTED_EVENT else "   <- not negative-eligible"
        print("  %-32s %5d%s" % (k, v, flag))
    print("\nhydroceph_tier (rows bearing on the hydrocephalus endpoint)")
    for k, v in Counter(r["hydroceph_tier"] for r in rows if r["hydroceph_tier"]).most_common():
        print("  %-28s %5d" % (k, v))
    ne = Counter(r["negative_eligible"] for r in rows)
    print("\ngrade-0 rows: %d eligible as negatives, %d NOT eligible"
          % (ne["TRUE"], ne["FALSE"]))
    print("event_cluster: %d rows in %d clusters, %d clusters holding >1 row"
          % (sum(1 for r in rows if r["event_cluster"]),
             len({r["event_cluster"] for r in rows if r["event_cluster"]}),
             sum(1 for _, n in Counter(r["event_cluster"] for r in rows
                                       if r["event_cluster"]).items() if n > 1)))

    if check:
        drift = [m for m, old in before.items()
                 if any(old[c] is not None for c in NEW_COLS)
                 and old != {c: next(r[c] for r in rows if r["measurement_id"] == m)
                             for c in NEW_COLS}]
        if drift:
            raise SystemExit("\nERROR: %d row(s) disagree with disk — re-run "
                             "without --check: %s" % (len(drift), drift[:5]))
        print("\n--check: on-disk classification matches")
        return

    with open(CORPUS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        w.writerows(rows)
    print("\nwrote %s (%d columns)" % (os.path.relpath(CORPUS, os.path.dirname(TOXDIR)),
                                       len(out_cols)))


if __name__ == "__main__":
    main()
