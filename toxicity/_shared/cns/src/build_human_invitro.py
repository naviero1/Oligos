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



# ---------------------------------------------------------------------------------------------
# HV3 (Woffindale 2026) prints its 23 sequences in LNA notation in supplementary Table S2:
#   +N      locked nucleic acid at that position
#   N       2'-deoxy (DNA)
#   /IDSP/  internal DSpacer -- an abasic spacer occupying a position, carrying no nucleobase
# The source states the backbone verbatim as a "fully phosphorothioated backbone", so the linkage
# is transcribed, not assumed; base modifications are recorded by the source as "None reported".
#
# The extraction already described the 3-8-3 pattern in prose and the per-position map was simply
# never expanded, leaving every human oligo in the module with zero source-resolved modification
# positions while 1,830 animal oligos had them. This parser closes that for the compounds whose
# chemistry the source actually prints.
LNA_TOKEN = re.compile(r"/IDSP/|\+([ACGTU])|([ACGTU])", re.I)


def parse_lna_notation(seq: str):
    """[(nucleobase, sugar_chemistry)] 5'->3', or None if the string is not this notation."""
    if not seq or seq in NOT:
        return None
    # Strip a 5'/3' wrapper and separators first, so the decision to parse rests on the NOTATION
    # and not on incidental punctuation. Without this the function refused HV1's sequences by
    # choking on their "5\u2032-" prefix -- the right answer for the wrong reason, which would have
    # silently dropped any LNA sequence that happened to carry the same prefix.
    s = re.sub(r"^\s*5[\u2032']?\s*-\s*|\s*-\s*3[\u2032']?\s*$", "", seq.strip())
    s = s.replace(" ", "")
    # This notation marks chemistry per position. A sequence with no "+" and no spacer is a plain
    # base string whose chemistry lives in prose (e.g. uniform 2'-MOE), and a per-position map for
    # it would be derived, not read. Those are refused here and left NOT_REPORTED.
    if "+" not in s and "/IDSP/" not in s.upper():
        return None
    pos, out = 0, []
    while pos < len(s):
        m = LNA_TOKEN.match(s, pos)
        if not m:
            if s[pos] in " -'":          # tolerate separators, never silently skip a base
                pos += 1
                continue
            return None                   # unknown token: refuse rather than guess
        if m.group(0).upper() == "/IDSP/":
            out.append(("none_abasic", "abasic_DSpacer"))
        elif m.group(1):
            out.append((m.group(1).upper(), "LNA"))
        else:
            out.append((m.group(2).upper(), "DNA_2prime_deoxy"))
        pos = m.end()
    return out or None


CHARACTERISED_ONLY = "CHARACTERISED_ONLY:"

# Which readout categories measure INJURY. Everything else is context: a delivery or uptake
# measure says how much compound got in, and an off-target expression measure says what the
# transcriptome did -- neither is harm, and neither may carry a toxicity grade.
INJURY_CATEGORIES = {"viability", "apoptosis", "histopathology", "injury_biomarker",
                     "morphological", "behavioural", "electrophysiology_calcium",
                     "functional", "clinical_cns_outcome"}

# The extractor writes category labels in prose when it is unsure, e.g.
# "off_target_safety (NOT a cytotoxicity readout - recorded as context)". That is honest, but a
# free-text value in a controlled column defeats every downstream filter, so it is mapped onto
# the vocabulary here and the qualifying prose is preserved in the row's notes by the caller.
CATEGORY_ALIASES = [
    (re.compile(r"off[_ ]?target", re.I), "off_target_expression"),
    (re.compile(r"apopto", re.I), "apoptosis"),
    (re.compile(r"morpholog|neurite", re.I), "morphological"),
    (re.compile(r"accumulat|uptake|transfection|delivery", re.I), "accumulation"),
    (re.compile(r"viabilit|cytotox", re.I), "viability"),
]


def normalise_category(raw):
    """Map an extractor's category label onto the controlled vocabulary."""
    v = (raw or "").strip()
    if not v:
        return "viability"
    if v in INJURY_CATEGORIES or v == "accumulation" or v == "off_target_expression":
        return v
    for rx, canon in CATEGORY_ALIASES:
        if rx.search(v):
            return canon
    return v  # unrecognised -> left as-is so the QC vocabulary check fails loudly



def main(path: str) -> int:
    data = json.loads(pathlib.Path(path).read_text())
    sources = data["sources"] if isinstance(data, dict) and "sources" in data else data

    oligos, measurements, mods = [], [], []
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
            backbone = o.get("backbone_chemistry") or ""
            oid = f"HV-OLG-{len(oligos) + 1:04d}"
            oid_of[name] = oid

            # Expand the source's own notation into per-position records. Only where the source
            # PRINTS the chemistry -- an unparseable or absent sequence yields nothing rather
            # than a guessed map.
            parsed = parse_lna_notation(seq_raw) if seq_raw not in NOT else None
            posmap = ""
            if parsed:
                posmap = ";".join(f"{i}:{b}:{s}" for i, (b, s) in enumerate(parsed, 1))
                ps = "phosphorothioate" if re.search(r"phosphorothioat", backbone, re.I) else "NOT_REPORTED"
                # NB: named nt_base, not base -- `base` is the chemistry-stripped sequence in
                # the enclosing scope, and shadowing it here silently truncated sequence_base to
                # the final nucleotide for all 23 compounds. Caught by the two QC checks that
                # compare the modification table against the sequence.
                for i, (nt_base, sugar) in enumerate(parsed, 1):
                    mods.append({
                        "oligo_id": oid, "position_5to3": i, "nucleobase": nt_base,
                        "sugar_chemistry": sugar, "base_modification": "",
                        "linkage_3prime": ps if i < len(parsed) else "terminal_none",
                        "basis": "position_resolved_from_source", "source_id": key,
                    })
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
                "modification_positions": posmap or "NOT_REPORTED",
                "modification_position_basis": ("position_resolved_from_source" if posmap
                                                else "NOT_REPORTED"),
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
            # readout_category is the gate, and it is checked BEFORE the prose is read.
            # An earlier revision graded on the prose alone, and a substring match on
            # "non-toxic" inside the sentence "Not a toxicity readout. ... non-toxic" put
            # cns_tox_grade=0 on a transfection-efficiency row. A delivery or
            # gene-expression measurement cannot be graded for toxicity at any value of
            # its prose, so it is never offered to the regex.
            rcat = normalise_category(m.get("readout_category"))
            call = (m.get("toxic_call") or "").lower()
            if rcat not in INJURY_CATEGORIES:
                grade, basis = "", (f"not a toxicity readout (readout_category={rcat}); "
                                    f"recorded as context, never graded")
            elif re.search(r"non[- ]?toxic|no (significant )?(drop|effect|toxicity)|well tolerated", call):
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
                "readout_category": rcat,
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
                "tox_axis": ("invitro_human_neural_toxicity" if rcat in INJURY_CATEGORIES
                             else "invitro_human_context_not_toxicity"),
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

    for name, recs in (("HV_oligos", oligos), ("HV_measurements", measurements),
                       ("HV_modifications", mods)):
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
    nmapped = len({m["oligo_id"] for m in mods})
    print(f"per-position modification records: {len(mods)} across {nmapped} oligo(s), "
          f"all position_resolved_from_source")
    print("per source:", src_rows)
    print("rejected:", rej)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else str(ROOT / "sources" / "HV_human_invitro" / "extractions.json")))
