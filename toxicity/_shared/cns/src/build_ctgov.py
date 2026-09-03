#!/usr/bin/env python3
"""Ingest source CT1 -- ClinicalTrials.gov posted results -- into the OligoTox-CNS schema.

Why this source matters
-----------------------
Before it, the module held 12 human measurements against 2,053 animal ones, and the Challenge
brief singles out human data. Registry results postings carry the full MedDRA adverse-event
tables that journal papers summarise away: every term, every arm, with BOTH a numerator and a
denominator. That is quantitative human clinical data with the comparator arm attached.

It also supplies the first quantitative hydrocephalus rows in the module. The hydrocephalus
dossier previously recorded one row whose value was NOT_REPORTED because the source was a
post-marketing label entry with no denominator; three tominersen trials report hydrocephalus with
per-arm counts.

Retrieval
---------
Via the API, not the web page: clinicaltrials.gov/study/<NCT>?tab=results is a client-side
application whose HTML contains none of the adverse-event text, so scraping it silently returns
nothing. The data lives at https://clinicaltrials.gov/api/v2/studies/<NCT> under
resultsSection.adverseEventsModule. The retrieved JSON is committed under
sources/CT1_ClinicalTrialsGov/ so the build does not depend on the service staying up.

Licence: ClinicalTrials.gov is a US Government work -- public domain.

Scope
-----
Trials of oligonucleotides delivered into the CNS (intrathecal or intracerebroventricular), plus
one intratumoural CpG-ODN glioblastoma trial. Only CNS-relevant adverse events are ingested: the
whole "Nervous system disorders" organ class, plus a curated set of terms filed by MedDRA under
other organ classes that are nonetheless CNS events (post-lumbar-puncture syndrome, CSF findings,
meningitis, myelitis, papilloedema, hydrocephalus). Cardiac "ventricular" terms are excluded --
they are heart ventricles, not brain ventricles.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "CT1_ClinicalTrialsGov"
OUT = ROOT / "data" / "staged"

SOURCE_ID = "CT1"

# CNS-relevant terms that MedDRA files outside "Nervous system disorders".
CNS_ELSEWHERE = re.compile(
    r"hydroceph|intracranial pressure|papill?oedema|papilledema|meningit|myelit|radiculit"
    r"|arachnoid|lumbar puncture|cerebrospinal|\bcsf\b|pleocytosis|encephal", re.I)
# "Ventricular" in a cardiac context is the heart, not the brain.
NOT_CNS = re.compile(r"ventricular (tachycardia|extrasystole|fibrillation|arrhythm)"
                     r"|supraventricular|osteomyelitis", re.I)

# Objective CNS-injury markers -- graded 2 even when the trial did not call them serious.
OBJECTIVE_MARKER = re.compile(
    r"hydroceph|papill?oedema|papilledema|pleocytosis|csf .*increas|cerebrospinal"
    r"|intracranial pressure|meningit|myelit|radiculit|arachnoid", re.I)

HYDROCEPHALUS = re.compile(r"hydroceph", re.I)


def cns_relevant(term: str, organ: str) -> bool:
    if NOT_CNS.search(term):
        return False
    return organ == "Nervous system disorders" or bool(CNS_ELSEWHERE.search(term))


# Explicit per-trial drug assignment. Parsing the intervention strings was tried and produced
# junk identifiers ("SAD" from "SAD: 30mg WVE-003", "WVE" from "WVE-120101", and case-variant
# duplicates of nusinersen), which would have split one molecule across several oligo rows. An
# explicit table is checkable; a regex over free text is not.
TRIAL_DRUG = {
    "NCT01703988": "nusinersen", "NCT01839656": "nusinersen", "NCT02193074": "nusinersen",
    "NCT02292537": "nusinersen", "NCT02386553": "nusinersen", "NCT02462759": "nusinersen",
    "NCT02594124": "nusinersen", "NCT04089566": "nusinersen",
    "NCT02623699": "tofersen",   "NCT03070119": "tofersen",
    "NCT02519036": "tominersen", "NCT03342053": "tominersen", "NCT03761849": "tominersen",
    "NCT03842969": "tominersen", "NCT04000594": "tominersen",
    "NCT03186989": "BIIB080_MAPTRx",
    "NCT03225833": "WVE-120101", "NCT04617847": "WVE-120101",
    "NCT03225846": "WVE-120102", "NCT04617860": "WVE-120102",
    "NCT05032196": "WVE-003",
    "NCT04494256": "BIIB105",
}

# Molecules already curated from the FDA labels (source C1). Their measurements attach to the
# existing oligo rather than creating a second row for the same molecule.
EXISTING_OLIGO = {"tofersen": "C1-OLG-0001", "nusinersen": "C1-OLG-0002"}

DRUG_CLASS = {
    "nusinersen": ("splice_switching_ASO", "SMN2", "2'-MOE_uniform"),
    "tofersen": ("ASO_gapmer", "SOD1", "2'-MOE;DNA_gap"),
    "tominersen": ("ASO_gapmer", "HTT", "2'-MOE;DNA_gap"),
    "BIIB080_MAPTRx": ("ASO_gapmer", "MAPT", "2'-MOE;DNA_gap"),
    "WVE-120101": ("ASO_gapmer", "HTT_SNP1", "stereopure_PN_backbone"),
    "WVE-120102": ("ASO_gapmer", "HTT_SNP2", "stereopure_PN_backbone"),
    "WVE-003": ("ASO_gapmer", "HTT_SNP3", "stereopure_PN_backbone"),
    "BIIB105": ("ASO_gapmer", "ATXN2", "2'-MOE;DNA_gap"),
}


def is_comparator(title: str) -> bool:
    return bool(re.search(r"placebo|sham|untreated|vehicle", title, re.I))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    oligos, measurements = [], []
    oligo_id_of, skipped = {}, []

    for f in sorted(SRC.glob("NCT*.json")):
        d = json.loads(f.read_text())
        nct = f.stem
        ps = d.get("protocolSection", {})
        rs = d.get("resultsSection", {})
        ae = rs.get("adverseEventsModule", {})
        if not ae:
            skipped.append(nct)
            continue

        title = ps.get("identificationModule", {}).get("briefTitle", "")
        ivs = [i.get("name", "") for i in ps.get("armsInterventionsModule", {})
               .get("interventions", [])]
        drug = TRIAL_DRUG.get(nct)
        if drug is None:
            skipped.append(f"{nct} (no drug mapping)")
            continue
        cond = "; ".join(ps.get("conditionsModule", {}).get("conditions", []))

        if drug in EXISTING_OLIGO:
            oligo_id_of.setdefault(drug, EXISTING_OLIGO[drug])
        elif drug not in oligo_id_of:
            oid = f"CT1-OLG-{len(oligo_id_of) + 1:04d}"
            oligo_id_of[drug] = oid
            klass, target, sugar = DRUG_CLASS[drug]
            oligos.append({
                "oligo_id": oid, "oligo_name": drug, "aliases": "; ".join(sorted(set(ivs))),
                "oligo_class": klass,
                "modality": "single_stranded_ASO",
                "target_gene": target, "target_transcript": f"{target}_mRNA",
                "indication": cond or "NOT_REPORTED",
                "developer": ps.get("sponsorCollaboratorsModule", {})
                               .get("leadSponsor", {}).get("name", "NOT_REPORTED"),
                "max_phase": "; ".join(ps.get("designModule", {}).get("phases", [])) or "NOT_REPORTED",
                "length_nt": "NOT_REPORTED",
                "sequence_5to3_asprinted": "NOT_REPORTED", "sequence_base": "NOT_REPORTED",
                "backbone_chemistry": "NOT_REPORTED", "backbone_linkage_positions": "NOT_REPORTED",
                "sugar_modifications": sugar, "modification_pattern": "class design; not printed in the registry",
                "modification_positions": "NOT_REPORTED",
                "modification_position_basis": "NOT_REPORTED",
                "gapmer_shape": "NOT_REPORTED", "conjugate": "NOT_REPORTED",
                "purity_pct": "NOT_REPORTED", "purity_method": "NOT_REPORTED",
                "identity_confirmation": "NOT_REPORTED", "synthesis_platform": "NOT_REPORTED",
                "formulation": "NOT_REPORTED",
                "source_id": SOURCE_ID, "source_location": f"{nct} protocolSection",
                "notes": "Investigational oligonucleotide identified from the trial registry. "
                         "The registry prints no sequence or chemistry; those fields are "
                         "NOT_REPORTED rather than filled from elsewhere.",
            })

        groups = {g["id"]: g for g in ae.get("eventGroups", [])}
        for serious, bucket in ((True, "seriousEvents"), (False, "otherEvents")):
            for ev in ae.get(bucket, []):
                term, organ = ev.get("term", ""), ev.get("organSystem", "")
                if not cns_relevant(term, organ):
                    continue
                for st in ev.get("stats", []):
                    g = groups.get(st.get("groupId"), {})
                    at_risk = st.get("numAtRisk")
                    affected = st.get("numAffected")
                    if at_risk in (None, 0):
                        continue
                    pct = round(100 * affected / at_risk, 2) if affected is not None else None

                    if affected == 0:
                        grade, basis = 0, "no event in this arm (numAffected = 0)"
                    elif serious:
                        grade, basis = 3, "reported in the trial's SERIOUS adverse event table"
                    elif OBJECTIVE_MARKER.search(term):
                        grade, basis = 2, ("non-serious, but an objective CNS marker "
                                           "(CSF finding, meningeal, papilloedema or hydrocephalus)")
                    else:
                        grade, basis = 1, "non-serious symptomatic CNS adverse event"

                    hyd = bool(HYDROCEPHALUS.search(term))
                    measurements.append({
                        "measurement_id": f"CT1-MSR-{len(measurements) + 1:05d}",
                        "oligo_id": oligo_id_of[drug], "source_id": SOURCE_ID,
                        "study_type": "clinical", "species": "human",
                        "strain": "NOT_APPLICABLE",
                        "system_model": f"randomised clinical trial arm: {g.get('title','')}",
                        "is_human_system": "TRUE",
                        "cns_region": "CSF_and_neuraxis",
                        "delivery_route": "intrathecal_or_intracerebroventricular",
                        "dose_value": "NOT_REPORTED", "dose_unit": "NOT_REPORTED",
                        "exposure_duration": ae.get("timeFrame", "NOT_REPORTED"),
                        "timepoint": "trial adverse-event collection period",
                        "readout_category": "clinical_cns_outcome",
                        "readout_name": term,
                        "readout_value": pct if pct is not None else "NOT_REPORTED",
                        "readout_is_qualitative": "FALSE",
                        "readout_unit": "pct_of_arm",
                        "n_per_group": f"{affected}/{at_risk}",
                        "statistic": "count affected of count at risk; no p-value posted",
                        "effect_direction": "increase" if affected else "no_change",
                        "effect_vs_control": (f"{affected}/{at_risk} in arm "
                                              f"'{g.get('title','')}'"
                                              f"{' (comparator arm)' if is_comparator(g.get('title','')) else ''}"),
                        "cns_tox_grade": grade, "grade_basis": basis,
                        "grade_status": "provisional",
                        "tox_axis": ("clinical_serious_neurological" if (hyd or serious)
                                     else "clinical_neuroinflammatory"
                                     if OBJECTIVE_MARKER.search(term)
                                     else "clinical_cns_tolerability"),
                        "is_cns_specific": "TRUE",
                        "source_ref": f"ClinicalTrials.gov {nct}",
                        "source_location": (f"{nct} resultsSection.adverseEventsModule."
                                            f"{bucket}, term '{term}', group "
                                            f"{st.get('groupId')} ({g.get('title','')})"),
                        "redistribution": "public_domain",
                        "notes": (f"MedDRA organ class: {organ}. Trial: {title[:90]}. "
                                  f"{'Comparator arm.' if is_comparator(g.get('title','')) else 'Treated arm.'}"),
                    })

    for name, recs in (("CT1_oligos", oligos), ("CT1_measurements", measurements)):
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

    import collections
    print(f"\ntrials ingested: {len(list(SRC.glob('NCT*.json'))) - len(skipped)}; "
          f"no posted results: {len(skipped)} ({', '.join(skipped)})")
    print("oligonucleotides:", ", ".join(sorted(oligo_id_of)))
    print("grades:", dict(sorted(collections.Counter(m['cns_tox_grade'] for m in measurements).items())))
    print("axes:", dict(collections.Counter(m['tox_axis'] for m in measurements)))
    hyd = [m for m in measurements if HYDROCEPHALUS.search(m['readout_name'])]
    print(f"hydrocephalus rows: {len(hyd)} across "
          f"{len({m['source_ref'] for m in hyd})} trials")
    return 0


if __name__ == "__main__":
    sys.exit(main())
