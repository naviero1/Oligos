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
3. `acute-neurotoxicity`      -- everything else: the acute axes (onset minutes to ~1 h, plus the
                                 in vitro neuronal-excitability readout) and the general clinical
                                 CNS adverse events. NOT a listed endpoint -- the Challenge brief
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


def endpoint_of(measurement: dict) -> str:
    """The one endpoint a measurement row belongs to. See the module docstring for the rule."""
    if measurement["readout_name"].startswith("hydrocephalus"):
        return "hydrocephalus"
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
        counts[ep] = {"oligos": len(eps_oligos), "measurements": len(meas),
                      "modifications": len(eps_mods), "sources": len(eps_sources)}
    return counts
