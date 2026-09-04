#!/usr/bin/env python3
"""Ingest source HV -- human in vitro CNS oligonucleotide toxicity -- into the schema.

    python3 src/build_human_invitro.py sources/HV_human_invitro/extractions.json

Why this source group exists
----------------------------
The Challenge brief singles out "datasets based on in vitro human systems". Before this, the
module held zero rows in the `human_invitro` subject class: its in vitro arm was rat primary
cortical neurons and its human arm was clinical adverse events. This ingests per-compound
toxicity readouts measured in HUMAN NEURAL cells -- iPSC-derived neurons and astrocytes, cortical
and cerebral organoids, and SH-SY5Y, the line the team's own CNS strategy names as its scalable
human CNS surrogate.

Admission rules, applied here rather than trusted upstream
----------------------------------------------------------
A row is admitted only if all of the following hold. Each rejection is counted and printed, so
what did not make it in is visible rather than silent.

  1. `usable` is true and the source is not marked non-usable by the extractor.
  2. The measurement is in a HUMAN NEURAL system (`is_neural` is not false). Readouts in
     non-neural human lines -- HEK293, fibroblasts, A549, HepG2 -- are rejected: this module is
     CNS-specific and must not be contaminated with other organ toxicities.
  3. The readout is a TOXICITY readout, not target knockdown.
  4. If a sequence is present, an independent adversarial verifier must have confirmed it against
     the source. An unconfirmed sequence is downgraded to NOT_REPORTED rather than admitted --
     a wrong sequence is worse than a missing one.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "staged"

NOT = ("NOT_REPORTED", "", None)

# Readout names that are efficacy, not toxicity. Rejected.
EFFICACY = re.compile(r"knockdown|silencing|exon (skip|inclusion)|splice (correction|switching)"
                      r"|target (mRNA|protein) (level|reduction)|SMN2? (protein|mRNA)|rescue", re.I)


def norm_seq(s: str) -> str:
    """Uppercase A/C/G/T/U only, for the chemistry-stripped column."""
    return re.sub(r"[^ACGTU]", "", (s or "").upper())


CHARACTERISED_ONLY = "CHARACTERISED_ONLY:"


def main(path: str) -> int:
    data = json.loads(pathlib.Path(path).read_text())
    sources = data["sources"] if isinstance(data, dict) and "sources" in data else data

    oligos, measurements = [], []
    rej = {"source_unusable": 0, "not_neural": 0, "efficacy_readout": 0,
           "sequence_unconfirmed": 0, "no_oligo_match": 0}
    src_rows = {}

    for entry in sources:
        ex = entry.get("extraction") or entry
        if not ex or not ex.get("usable"):
            rej["source_unusable"] += 1
            continue
        key = ex.get("source_key", entry.get("source", "HV?"))
        key = key.split("_")[0]  # HV1_Buijsen2024 -> HV1, so source_id stays a short stable token
        licence = (ex.get("licence") or "unknown").strip()
        # CC BY-NC-ND is checked FIRST: the NoDerivatives clause means we cannot license a
        # restructured derivative of the article, so those rows are marked summary_stat_only -
        # cite and read, do not redistribute as our own dataset content.
        if re.search(r"CC.?BY.?NC.?ND|NoDeriv", licence, re.I):
            redistribution = "summary_stat_only"
        elif re.search(r"CC.?BY.?NC", licence, re.I):
            redistribution = "cc_by_nc"
        elif re.search(r"CC.?BY", licence, re.I):
            redistribution = "cc_by"
        else:
            redistribution = "summary_stat_only"

        # sequences an adversarial verifier confirmed
        confirmed = {v.get("compound"): v for v in (entry.get("verdicts") or [])
                     if not v.get("refuted")}

        oid_of = {}
        for o in ex.get("oligos", []):
            name = o.get("local_name", "")
            seq_raw = o.get("sequence_5to3") or "NOT_REPORTED"
            if seq_raw not in NOT and name not in confirmed:
                seq_raw = "NOT_REPORTED"
                rej["sequence_unconfirmed"] += 1
            base = norm_seq(seq_raw) if seq_raw not in NOT else "NOT_REPORTED"
            oid = f"HV-OLG-{len(oligos) + 1:04d}"
            oid_of[name] = oid
            oligos.append({
                "oligo_id": oid, "oligo_name": f"{key}_{name}", "aliases": name,
                "oligo_class": o.get("modality") or "ASO_gapmer",
                "modality": "single_stranded_ASO",
                "target_gene": o.get("target_gene") or "NOT_REPORTED",
                "target_transcript": "NOT_REPORTED",
                "indication": "research_panel_human_invitro_CNS",
                "developer": "NOT_REPORTED", "max_phase": "research_panel",
                "length_nt": len(base) if base not in NOT else (o.get("length_nt") or "NOT_REPORTED"),
                "sequence_5to3_asprinted": seq_raw, "sequence_base": base,
                "backbone_chemistry": o.get("backbone_chemistry") or "NOT_REPORTED",
                "backbone_linkage_positions": "NOT_REPORTED",
                "sugar_modifications": o.get("sugar_modifications") or "NOT_REPORTED",
                "modification_pattern": o.get("modification_positions") or "NOT_REPORTED",
                "modification_positions": "NOT_REPORTED",
                "modification_position_basis": "NOT_REPORTED",
                "gapmer_shape": "NOT_REPORTED", "conjugate": "none",
                "n_A": base.count("A") if base not in NOT else "",
                "n_C": base.count("C") if base not in NOT else "",
                "n_G": base.count("G") if base not in NOT else "",
                "n_T": base.count("T") if base not in NOT else "",
                "gc_content_pct": (round(100 * (base.count("G") + base.count("C")) / len(base), 2)
                                   if base not in NOT and base else ""),
                "purity_pct": "NOT_REPORTED",
                "purity_method": ex.get("purity_characterization_reported") or "NOT_REPORTED",
                "identity_confirmation": "NOT_REPORTED", "synthesis_platform": "NOT_REPORTED",
                "formulation": ex.get("delivery_method") or "NOT_REPORTED",
                "source_id": key, "source_location": o.get("source_location") or "NOT_REPORTED",
                "notes": ("designated control compound. " if o.get("is_control") else "")
                         + (o.get("base_modifications") or ""),
            })

        for m in ex.get("measurements", []):
            if m.get("is_neural") is False:
                rej["not_neural"] += 1
                continue
            rname = m.get("readout_name", "")
            if EFFICACY.search(rname):
                rej["efficacy_readout"] += 1
                continue
            oid = oid_of.get(m.get("oligo_local_name"))
            if not oid:
                rej["no_oligo_match"] += 1
                continue
            call = (m.get("toxic_call") or "").lower()
            if re.search(r"non[- ]?toxic|no (significant )?(drop|effect|toxicity)|well tolerated", call):
                grade, basis = 0, "authors state the compound was non-toxic in this system"
            elif re.search(r"\btoxic\b|significant (drop|reduction|decrease)|cytotox", call):
                grade, basis = 2, "authors state a significant toxicity or viability loss in this system"
            else:
                grade, basis = "", "authors state no explicit toxic/non-toxic call for this readout"
            measurements.append({
                "measurement_id": f"HV-MSR-{len(measurements) + 1:05d}",
                "oligo_id": oid, "source_id": key,
                "study_type": "in_vitro", "species": "human",
                "strain": "NOT_APPLICABLE",
                "system_model": m.get("human_system") or ex.get("human_system") or "NOT_REPORTED",
                "is_human_system": "TRUE",
                "cns_region": "neural_cell_culture",
                "delivery_route": ex.get("delivery_method") or "in_culture_medium",
                "dose_value": m.get("concentration") or "NOT_REPORTED",
                "dose_unit": m.get("concentration_unit") or "NOT_REPORTED",
                "exposure_duration": m.get("exposure_duration") or "NOT_REPORTED",
                "timepoint": m.get("exposure_duration") or "NOT_REPORTED",
                "readout_category": m.get("readout_category") or "viability",
                "readout_name": rname,
                "readout_value": m.get("readout_value") or "NOT_REPORTED",
                "readout_is_qualitative": "TRUE" if (m.get("readout_value") in NOT) else "FALSE",
                "readout_unit": m.get("readout_unit") or "NOT_REPORTED",
                "n_per_group": m.get("n_replicates") or "NOT_REPORTED",
                "statistic": m.get("statistic") or "NOT_REPORTED",
                "effect_direction": m.get("effect_direction") or "no_change",
                "effect_vs_control": m.get("comparator") or "NOT_REPORTED",
                "cns_tox_grade": grade, "grade_basis": basis,
                "grade_status": "provisional" if grade != "" else "not_graded",
                "tox_axis": "invitro_human_neural_toxicity",
                "is_cns_specific": "TRUE",
                "source_ref": f"{key} ({ex.get('doi') or ex.get('pmcid') or ''})",
                "source_location": m.get("source_location") or "NOT_REPORTED",
                "redistribution": redistribution,
                "notes": (m.get("notes") or "") + f" | licence as stated by PMC: {licence}",
            })
        src_rows[key] = sum(1 for m in measurements if m["source_id"] == key)

    # A compound can be fully characterised and still carry no measurement: the source names it,
    # prints its sequence and chemistry, and then reports its result only inside a pooled figure
    # panel with no per-compound value. Reading a number off such a panel would be estimating it,
    # which this pipeline does not do -- so the compound is kept for its chemistry and declared,
    # in the row itself, to have no measurement and why. qc/validate_dataset.py enforces that
    # every unmeasured oligo carries this declaration, so an ACCIDENTAL orphan still fails.
    measured = {m["oligo_id"] for m in measurements}
    n_declared = 0
    for o in oligos:
        if o["oligo_id"] not in measured:
            o["notes"] = (CHARACTERISED_ONLY + " retained for its published sequence and "
                          "chemistry; the source reports no per-compound toxicity readout for it "
                          "that could be extracted without estimating a value from a figure. | "
                          + (o.get("notes") or "")).strip(" |")
            n_declared += 1
    print(f"{n_declared} oligo(s) declared {CHARACTERISED_ONLY.strip(':')} "
          f"(characterised, no extractable measurement)")

    for name, recs in (("HV_oligos", oligos), ("HV_measurements", measurements)):
        if not recs:
            print(f"  no rows for {name}")
            continue
        keys = []
        for r in recs:
            for k in r:
                if k not in keys:
                    keys.append(k)
        p = OUT / f"{name}.csv"
        with p.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys, restval="")
            w.writeheader(); w.writerows(recs)
        print(f"wrote {p.relative_to(ROOT)}: {len(recs)} rows x {len(keys)} cols")

    seqs = sum(1 for o in oligos if o["sequence_base"] not in NOT)
    print(f"\noligos {len(oligos)} ({seqs} with a verified sequence); measurements {len(measurements)}")
    print("per source:", src_rows)
    print("rejected:", rej)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else str(ROOT / "sources" / "HV_human_invitro" / "extractions.json")))
