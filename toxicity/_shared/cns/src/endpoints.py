#!/usr/bin/env python3
"""Endpoint allocation for the CNS work: which measurement belongs to which toxicity.

The CNS sources were curated as one corpus, but they do not describe one toxicity. This module
is the single place that decides which endpoint each measurement belongs to, so the decision is
stated once and every consumer inherits it.

Why the split exists
--------------------
`toxicity/` files work by the toxicity endpoint it belongs to, one folder and one dossier each.
A single "CNS" folder would have mixed four different endpoint buckets in one place, three of
which are not the same toxicity at all. Each endpoint therefore owns its own `data/`, and this
module writes them.

The rule, in priority order
---------------------------
1. `hydrocephalus`            -- the readout names hydrocephalus. A listed endpoint.
2. `chronic-neurotoxicity`    -- `tox_axis = late_onset_neurodegeneration`, i.e. onset >= 3 days.
                                 A listed endpoint.
2b. `chronic-neurotoxicity`   -- also every human clinical row: trial adverse events are
                                 collected across chronic exposure (months of repeat dosing), so
                                 they are the human arm of this listed endpoint.
3. `acute-neurotoxicity`      -- everything else: the acute axes only (onset minutes to ~1 h, plus
                                 the in vitro neuronal-excitability readout). NOT a listed endpoint -- the Challenge brief
                                 deprioritises acute neurotoxicity, "specifically alterations of
                                 neuronal electrical activity". It gets a folder because the data
                                 exists and must be filed somewhere honest, not because the brief
                                 asks for it.

Shared oligonucleotides
-----------------------
An oligonucleotide is an entity, not an endpoint: the same compound can carry measurements on
more than one axis. `oligos.csv` and `modifications.csv` in an endpoint folder therefore hold
every compound that endpoint measures, which means a compound measured on two axes appears in
both folders. Exactly one compound does so in this release (nusinersen: one hydrocephalus row,
three other clinical rows). Measurement rows are never duplicated -- each belongs to one
endpoint and appears in one folder.
"""
from __future__ import annotations

import collections
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent      # _shared/cns
TOXICITY = ROOT.parent.parent                              # toxicity/

ENDPOINTS = ["acute-neurotoxicity", "chronic-neurotoxicity", "hydrocephalus"]

LISTED_IN_BRIEF = {"chronic-neurotoxicity": True, "hydrocephalus": True,
                   "acute-neurotoxicity": False}

TABLES = ["oligos", "measurements", "modifications", "sources"]

# A source can be registered without contributing a single row -- O1 supplies the acute-inhibition
# scoring instruments documented in docs/SCORING_INSTRUMENTS.md and a formulation finding that
# contradicts K1, but no per-oligo measurement. Splitting purely by the rows a source reaches
# would silently drop it from every endpoint's sources.csv, so zero-row sources are attributed
# explicitly to the endpoint they inform.
ZERO_ROW_SOURCE_ENDPOINT = {"O1": "acute-neurotoxicity"}

# The same trap one level down. A published oligonucleotide can be fully characterised -- name,
# sequence, chemistry, per-position modification map -- and still carry no measurement, because
# the source screened it but printed its result only in a figure with no per-compound value. An
# earlier revision allocated oligos purely by the measurements that reach them, which silently
# dropped 21 such compounds, 18 of them sequence-resolved and all of them human. Those are the
# rows this module exists to publish, so a measurement-less oligo is now filed with the endpoint
# its own source predominantly serves, and assemble.py asserts that the split loses none.

# --- human vs animal ---------------------------------------------------------------------
# The Challenge brief singles out datasets "based on in vitro human systems or able to
# extrapolate data between in vitro human systems and animal data". That makes the human/animal
# boundary a first-class axis, not a detail, so it is split out explicitly rather than left to be
# reconstructed from study_type + species.
#
# Four classes, and the second is the point: `human_invitro` is the class the brief prioritises.
# It was empty in the first release, and naming the empty class is what made that visible in the
# data rather than only in a caveat. It is no longer empty.
# --- is this compound a control? -------------------------------------------------------------
# The Challenge scores this twice: the narrative must open with "the dataset(s) generated, and
# positive/negative controls included", and the 20-point Experimental design criterion names
# "relevant positive/negative control oligos" explicitly. The information was present but not
# queryable -- 13 compounds carried the authors' own "Control" designation inside
# dataset_split_asPublished, a column meant for train/test splits, while the control compounds of
# three other sources were marked only in free prose. A reviewer could not filter for them.
#
# Derived ONLY from an explicit designation by the source. A compound is a test compound unless
# its source says otherwise; nothing is inferred from a name resembling "control".
CONTROL_ROLES = {"negative_control", "positive_control", "vehicle", "test_compound"}


def control_role_of(oligo) -> str:
    klass = (oligo.get("oligo_class") or "").lower()
    notes = (oligo.get("notes") or "").lower()
    split = (oligo.get("dataset_split_asPublished") or "").strip().lower()
    if "vehicle" in klass:
        return "vehicle"
    # H1 publishes its own Control designation in the split column; the HV sources mark theirs in
    # the oligo_class text and with an explicit "designated control compound" note.
    if split == "control":
        return "negative_control"
    if notes.startswith("designated control compound"):
        return "negative_control"
    if "negative control" in klass or "non-targeting" in klass or "scrambled" in klass:
        return "negative_control"
    return "test_compound"


# --- which measuring instrument produced this row? -------------------------------------------
# Four distinct instruments in this module share the unit label "score_0_to_20", across two
# species and two routes of administration: Hagedorn's mouse ICV acute tolerability scale,
# Miller's mouse ICV scale, Kuroda's mouse ICV late-onset scale, and Kuroda's rat INTRATHECAL
# late-onset scale. Grouping by readout_unit silently pools all four. readout_name distinguishes
# them, but only if a consumer knows to use it -- so the instrument is named explicitly here.
#
# Whether any two of these scales are mutually comparable is a scientific question, not a schema
# one. This column lets the question be asked; it does not answer it. docs/SCORING_INSTRUMENTS.md
# holds the scale definitions.
INSTRUMENTS = {
    "INS-01": ("rat primary cortical neuron spontaneous calcium oscillation",
               "pct_of_untreated_control", "rat", "in_culture_medium", "H1"),
    "INS-02": ("Hagedorn 0-20 acute tolerability score, mouse ICV",
               "score_0_to_20", "mouse", "intracerebroventricular", "H1"),
    "INS-03": ("Miller 0-20 average acute tolerability score, mouse ICV",
               "score_0_to_20", "mouse", "intracerebroventricular", "K1"),
    "INS-04": ("Kuroda 0-20 late-onset tolerability score, mouse ICV",
               "score_0_to_20", "mouse", "intracerebroventricular", "L1"),
    "INS-05": ("Kuroda rat-modified late-onset tolerability score, rat intrathecal",
               "score_0_to_20", "rat", "intrathecal", "L1"),
    "INS-06": ("ClinicalTrials.gov posted MedDRA adverse-event incidence, per arm",
               "pct_of_arm", "human", "intrathecal_or_intracerebroventricular", "CT1"),
    "INS-07": ("FDA label adverse-reaction incidence / warnings statement",
               "various", "human", "intrathecal", "C1"),
    "INS-08": ("human neural culture or organoid injury readout (viability, apoptosis, neurite)",
               "various", "human", "in_culture_medium", "HV1/HV2/HV3"),
    "INS-09": ("human neural culture CONTEXT readout (uptake, off-target expression) -- not injury",
               "various", "human", "in_culture_medium", "HV1/HV2/HV3"),
}


def instrument_of(measurement) -> str:
    src, name = measurement["source_id"], measurement["readout_name"]
    if src == "H1":
        return "INS-02" if "tolerability" in name else "INS-01"
    if src == "K1":
        return "INS-03"
    if src == "L1":
        return "INS-05" if name.endswith("_rat") else "INS-04"
    if src == "CT1":
        return "INS-06"
    if src == "C1":
        return "INS-07"
    if src.startswith("HV"):
        return "INS-08" if measurement["readout_is_toxicity"] == "TRUE" else "INS-09"
    return "NOT_REPORTED"


# --- can the SOURCE support calling this outcome chronic? ------------------------------------
# Beebop asked for a chronic-qualification rubric over the clinical rows. Building one turned out
# to be impossible from the source, and that is the finding rather than a failure to deliver.
#
# Every key in a ClinicalTrials.gov adverse-event record was enumerated across all 29 retrieved
# files. An event carries exactly: term, organSystem, assessmentType, sourceVocabulary, an
# occasional free-text note, and stats{groupId, numAffected, numAtRisk, numEvents}. There is no
# onset, no duration, no persistence, no resolution and no time-to-event field at any level. The
# module's timeFrame is a collection window for the whole table, not a property of an event.
#
# So no per-event chronic/acute split is derivable from the registry at any level of effort, and
# saying so is more useful than a rubric that would silently manufacture one.
CHRONIC_QUALIFICATIONS = {"chronic_supported_by_source", "acute_by_design",
                          "not_derivable_from_source"}


def chronic_qualification_of(measurement) -> str:
    if measurement["study_type"] == "clinical":
        return "not_derivable_from_source"
    if measurement["tox_axis"] == "late_onset_neurodegeneration":
        # L1 observes onset from day 3, with sacrifice at days 7-21; the source states the timing.
        return "chronic_supported_by_source"
    return "acute_by_design"


def incidence_is_zero_of(measurement) -> str:
    """TRUE where the row records that the event did not occur in that arm."""
    n = (measurement.get("n_per_group") or "").strip()
    return "TRUE" if n.startswith("0/") else "FALSE"


# --- does this readout measure injury at all? ------------------------------------------------
# Kept here, next to the endpoint and subject-class rules, because it is the same kind of thing:
# a property of a row derived by one documented rule rather than asserted by whoever built it.
#
# The distinction is not pedantic. A delivery measure (how much compound entered the cell) and an
# off-target expression measure (what the transcriptome did) are legitimate, valuable context --
# and neither is harm. Grading them produces a toxicity value the source never reported.
INJURY_CATEGORIES = {"viability", "apoptosis", "histopathology", "injury_biomarker",
                     "morphological", "behavioural", "electrophysiology_calcium",
                     "functional", "clinical_cns_outcome"}
CONTEXT_CATEGORIES = {"accumulation", "off_target_expression"}
READOUT_CATEGORIES = INJURY_CATEGORIES | CONTEXT_CATEGORIES


def readout_is_toxicity_of(measurement) -> str:
    return "TRUE" if measurement["readout_category"] in INJURY_CATEGORIES else "FALSE"


SUBJECT_CLASSES = ["human_clinical", "human_invitro", "animal_invivo", "animal_invitro"]

SUBJECT_GROUP = {"human_clinical": "human", "human_invitro": "human",
                 "animal_invivo": "animal", "animal_invitro": "animal"}


def subject_class_of(measurement: dict) -> str:
    """Which subject class a measurement belongs to. Derived from the row, never hand-assigned."""
    human = measurement.get("is_human_system") == "TRUE" or measurement.get("species") == "human"
    if measurement["study_type"] == "clinical":
        return "human_clinical" if human else "animal_invivo"
    if measurement["study_type"] == "in_vitro":
        return "human_invitro" if human else "animal_invitro"
    return "animal_invivo"


def subject_group_of(measurement: dict) -> str:
    """`human` or `animal` -- the coarse split the brief cares about."""
    return SUBJECT_GROUP[subject_class_of(measurement)]


HYDROCEPHALUS_RE = re.compile(r"hydroceph", re.I)


def endpoint_of(measurement: dict) -> str:
    """The one endpoint a measurement row belongs to. See the module docstring for the rule.

    The hydrocephalus test is a case-insensitive substring, not a prefix: clinical-registry terms
    arrive as MedDRA strings such as "Hydrocephalus" and "Normal pressure hydrocephalus", and a
    prefix match on lower case would have silently filed both under acute neurotoxicity.
    """
    if HYDROCEPHALUS_RE.search(measurement["readout_name"]):
        return "hydrocephalus"
    if measurement["study_type"] == "clinical":
        # Human clinical rows are adverse events collected across the whole trial exposure --
        # months to years of repeat intrathecal dosing -- so they are the human evidence for
        # CHRONIC neurotoxicity, which is on the brief's endpoint list.
        #
        # Caveat, recorded rather than glossed: it is the EXPOSURE that is chronic, not
        # necessarily each event. A single "headache" term may describe an acute reaction to one
        # dose. The registry does not publish time-to-onset per event, so a finer split would be
        # our inference rather than the source's statement. Filter on source_id CT1/C1 or on
        # study_type to isolate these rows.
        return "chronic-neurotoxicity"
    if measurement["tox_axis"] == "late_onset_neurodegeneration":
        return "chronic-neurotoxicity"
    return "acute-neurotoxicity"


def data_dir(endpoint: str) -> pathlib.Path:
    return TOXICITY / endpoint / "data"


def read(endpoint: str, table: str) -> list[dict]:
    p = data_dir(endpoint) / f"{table}.csv"
    if not p.exists():
        return []
    with p.open(newline="") as fh:
        return list(csv.DictReader(fh))


def read_group(endpoint: str, group: str) -> list[dict]:
    """One endpoint's human-only or animal-only measurement file."""
    p = data_dir(endpoint) / f"measurements_{group}.csv"
    if not p.exists():
        return []
    with p.open(newline="") as fh:
        return list(csv.DictReader(fh))


def load_all(table: str) -> list[dict]:
    """Every row of `table` across all three endpoint folders, in endpoint order.

    Consumers that need the whole CNS picture -- the QC suite, the figures, the submission
    documents -- read through here rather than from a fourth combined copy, so the endpoint
    folders stay the single source of truth and cannot drift from a master table.
    """
    rows = []
    seen = set()
    for ep in ENDPOINTS:
        for r in read(ep, table):
            key = r.get("measurement_id") or r.get("oligo_id", "") + r.get("position_5to3", "") \
                  or r.get("source_id")
            if table in ("oligos", "modifications", "sources"):
                # these are entity tables and may legitimately repeat across endpoints
                k = (table, key)
                if k in seen:
                    continue
                seen.add(k)
            rows.append(r)
    return rows


def write_split(oligos: list[dict], measurements: list[dict], modifications: list[dict],
                sources: list[dict], columns: dict, trials: list[dict] | None = None) -> dict:
    """Partition the assembled tables into one `data/` per endpoint. Returns per-endpoint counts."""
    by_ep: dict[str, list[dict]] = {ep: [] for ep in ENDPOINTS}
    for m in measurements:
        by_ep[endpoint_of(m)].append(m)

    oligo_by_id = {o["oligo_id"]: o for o in oligos}
    mods_by_oligo: dict[str, list[dict]] = {}
    for md in modifications:
        mods_by_oligo.setdefault(md["oligo_id"], []).append(md)
    source_by_id = {s["source_id"]: s for s in sources}

    # An oligo with at least one measurement belongs to the endpoints its measurements reach.
    # One with none belongs to the endpoint where its source contributes most measurements --
    # deterministic, with an alphabetical tie-break and a documented fallback -- so that no
    # characterised compound falls out of the release.
    src_weight: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for ep, meas in by_ep.items():
        for m in meas:
            src_weight[m["source_id"]][ep] += 1
    measured = {m["oligo_id"] for m in measurements}
    homeless: dict[str, list[str]] = {ep: [] for ep in ENDPOINTS}
    for oid, o in oligo_by_id.items():
        if oid in measured:
            continue
        w = src_weight.get(o["source_id"])
        ep = (min(sorted(w.items()), key=lambda kv: (-kv[1], kv[0]))[0] if w
              else ZERO_ROW_SOURCE_ENDPOINT.get(o["source_id"], ENDPOINTS[0]))
        homeless[ep].append(oid)

    counts = {}
    for ep, meas in by_ep.items():
        oids = [oid for oid in oligo_by_id
                if oid in {m["oligo_id"] for m in meas} or oid in homeless[ep]]
        oids.sort()
        eps_oligos = [oligo_by_id[o] for o in oids]
        eps_mods = [md for o in oids for md in mods_by_oligo.get(o, [])]
        sids = sorted({m["source_id"] for m in meas} | {o["source_id"] for o in eps_oligos}
                      | {sid for sid, e in ZERO_ROW_SOURCE_ENDPOINT.items() if e == ep})
        eps_sources = [source_by_id[s] for s in sids if s in source_by_id]

        d = data_dir(ep)
        d.mkdir(parents=True, exist_ok=True)
        # Each endpoint folder carries the trials its OWN rows came from, with the shared
        # trial_key, and with n_cns_measurements recounted for this endpoint only. A trial that
        # feeds two endpoints appears in both files under one key -- which is the point: it is
        # how a consolidated submission can tell that it is one trial, not two.
        here = {re.match(r"(NCT\d+)", m["source_location"]).group(1)
                for m in meas if m["source_id"] == "CT1" and re.match(r"(NCT\d+)", m["source_location"])}
        eps_trials = []
        for tr in (trials or []):
            if tr["trial_key"] in here:
                n = sum(1 for m in meas if m["source_id"] == "CT1"
                        and m["source_location"].startswith(tr["trial_key"]))
                eps_trials.append(dict(tr, n_cns_measurements=n,
                                       endpoint_evaluable="TRUE" if n else "FALSE"))
        eps_trials.sort(key=lambda r: r["trial_key"])

        for table, rows in (("oligos", eps_oligos), ("measurements", meas),
                            ("modifications", eps_mods), ("sources", eps_sources),
                            ("trials", eps_trials)):
            cols = columns[table]
            with (d / f"{table}.csv").open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=cols)
                w.writeheader()
                w.writerows(rows)

        # human vs animal, as separate files under the endpoint's data/. Written even when a
        # group is empty, with a header row, so "this endpoint has no human data" is a file you
        # can open rather than an absence you have to notice.
        mcols = columns["measurements"]
        for group in ("human", "animal"):
            sub = [m for m in meas if subject_group_of(m) == group]
            with (d / f"measurements_{group}.csv").open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=mcols)
                w.writeheader()
                w.writerows(sub)
            counts.setdefault(ep, {})[f"{group}_rows"] = len(sub)
        counts[ep].update({"trials": len(eps_trials),
                           "oligos": len(eps_oligos), "measurements": len(meas),
                           "modifications": len(eps_mods), "sources": len(eps_sources)})
    return counts
