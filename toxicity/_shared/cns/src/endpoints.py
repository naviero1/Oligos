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

# --- human vs animal ---------------------------------------------------------------------
# The Challenge brief singles out datasets "based on in vitro human systems or able to
# extrapolate data between in vitro human systems and animal data". That makes the human/animal
# boundary a first-class axis, not a detail, so it is split out explicitly rather than left to be
# reconstructed from study_type + species.
#
# Four classes, and the fourth is the point: `human_invitro` is the class the brief prioritises,
# and this dataset has ZERO rows in it. Naming the empty class makes that visible in the data
# itself instead of only in a caveat.
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
                sources: list[dict], columns: dict) -> dict:
    """Partition the assembled tables into one `data/` per endpoint. Returns per-endpoint counts."""
    by_ep: dict[str, list[dict]] = {ep: [] for ep in ENDPOINTS}
    for m in measurements:
        by_ep[endpoint_of(m)].append(m)

    oligo_by_id = {o["oligo_id"]: o for o in oligos}
    mods_by_oligo: dict[str, list[dict]] = {}
    for md in modifications:
        mods_by_oligo.setdefault(md["oligo_id"], []).append(md)
    source_by_id = {s["source_id"]: s for s in sources}

    counts = {}
    for ep, meas in by_ep.items():
        oids = [oid for oid in oligo_by_id if oid in {m["oligo_id"] for m in meas}]
        oids.sort()
        eps_oligos = [oligo_by_id[o] for o in oids]
        eps_mods = [md for o in oids for md in mods_by_oligo.get(o, [])]
        sids = sorted({m["source_id"] for m in meas} | {o["source_id"] for o in eps_oligos}
                      | {sid for sid, e in ZERO_ROW_SOURCE_ENDPOINT.items() if e == ep})
        eps_sources = [source_by_id[s] for s in sids if s in source_by_id]

        d = data_dir(ep)
        d.mkdir(parents=True, exist_ok=True)
        for table, rows in (("oligos", eps_oligos), ("measurements", meas),
                            ("modifications", eps_mods), ("sources", eps_sources)):
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
        counts[ep] = {"oligos": len(eps_oligos), "measurements": len(meas),
                      "modifications": len(eps_mods), "sources": len(eps_sources)}
    return counts
