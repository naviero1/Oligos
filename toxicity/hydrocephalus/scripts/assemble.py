#!/usr/bin/env python3
"""
Assembles the canonical OligoTox-Hydrocephalus tables from the four extraction
components, assigns stable primary keys, and writes the provenance registry and
the derived analysis-ready join.

Reads   data/_ctgov_measurements.csv       (deterministic, scripts/extract_ctgov.py)
        data/_faers_measurements.csv       (deterministic, scripts/extract_faers.py)
        data/_label_measurements.csv       (deterministic, scripts/extract_labels.py)
        data/_literature_measurements.csv  (curated,       scripts/build_literature.py)
        data/oligos.csv                    (               scripts/build_oligos.py)

Writes  data/measurements.csv              canonical, one row per measurement
        data/sources.csv                   provenance registry
        data/hydrocephalus_merged.csv      GENERATED denormalized join

The merged file is derived and must never be hand-edited; regenerate it by
re-running this script.

Usage: python3 scripts/assemble.py
"""
import csv
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
TODAY = date.today().isoformat()

# Human and animal evidence must be separable in ONE operation, not by knowing
# which study_type values happen to imply a human subject. subject_class is
# derived deterministically from (species, study_type) by subject_class_for()
# below, and qc/validate.py re-derives it and fails if any stored value differs.
#
# The Challenge brief singles out "datasets based on in vitro human systems or
# able to extrapolate data between in vitro human systems and animal data" as of
# particular interest, so the vocabulary keeps the in vivo / in vitro axis
# separate from the human / animal axis rather than collapsing them.
SUBJECT_CLASSES = {"human_in_vivo", "human_in_vitro", "human_population",
                   "animal_in_vivo", "animal_in_vitro", "not_applicable"}


def subject_class_for(species, study_type):
    if study_type == "background_epidemiology":
        # A population incidence rate. Human subjects, but no individual dosed
        # and no per-subject observation: it is not a trial and must not be
        # pooled with one.
        return "human_population"
    if species == "human":
        return "human_in_vitro" if study_type == "in_vitro" else "human_in_vivo"
    if species in ("mouse", "rat", "monkey", "pig"):
        return "animal_in_vitro" if study_type == "in_vitro" else "animal_in_vivo"
    return "not_applicable"


MEASUREMENT_COLS = [
    "measurement_id", "oligo_id", "oligo_name", "source_id",
    "study_type", "species", "subject_class", "strain", "system_model",
    "is_human_system",
    "indication_population", "arm_label", "arm_description", "arm_role",
    "cns_compartment", "delivery_route", "dose_value", "dose_unit", "dose_regimen",
    "exposure_duration", "timepoint",
    "endpoint_tier", "readout_category", "readout_name", "readout_term_verbatim",
    "readout_value", "readout_unit", "readout_is_qualitative",
    "n_affected", "n_at_risk", "comparator_arm", "n_affected_comparator",
    "n_at_risk_comparator", "statistic", "effect_direction", "effect_vs_control",
    "seriousness", "assessment_type", "organ_system", "source_vocabulary",
    "hydroceph_grade", "grade_basis", "grade_status",
    "ascertainment", "ascertainment_basis",
    "attribution_as_stated", "attribution_evidence", "tox_axis", "event_cluster_id",
    "source_ref", "source_location", "redistribution", "notes",
]

COMPONENTS = [
    ("_ctgov_measurements.csv", "registry_results"),
    ("_ctgov_outcome_measurements.csv", "registry_results"),
    ("_faers_measurements.csv", "pharmacovigilance_api"),
    ("_label_measurements.csv", "regulatory_primary"),
    ("_literature_measurements.csv", "primary_fulltext"),
    ("_nonclinical_measurements.csv", "primary_fulltext"),
]

# Provenance registry entries. Each source_key used by any component gets one.
SOURCE_META = {
    "FAERS_openFDA": dict(
        citation=("FDA Adverse Event Reporting System (FAERS), queried through the "
                  "openFDA drug/event API"),
        first_author="NOT_APPLICABLE", year="2026", journal="NOT_APPLICABLE",
        doi="", pmid="", pmcid="", nct_id="", url="https://api.fda.gov/drug/event.json",
        access="api", license="US Government work / public domain",
        redistribution="public_domain", evidence_tier="pharmacovigilance_api",
        retrieved_via="openFDA REST API, one exact query per (drug, MedDRA term) pair",
        notes=("Spontaneous reports. Counts are reports, not patients, and carry no "
               "exposure denominator. No disproportionality statistic is computed here.")),
    "Stoker_2021_MovDisord": dict(
        citation=("Stoker TB, Andresen KER, Barker RA. Hydrocephalus Complicating "
                  "Intrathecal Antisense Oligonucleotide Therapy for Huntington's "
                  "Disease. Mov Disord. 2021;36(1):263-264."),
        first_author="Stoker TB", year="2021", journal="Movement Disorders",
        doi="10.1002/mds.28359", pmid="33125799", pmcid="PMC7894279", nct_id="",
        url="https://pmc.ncbi.nlm.nih.gov/articles/PMC7894279/",
        access="open_access", license="CC BY 4.0", redistribution="cc_by",
        evidence_tier="case_report",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("The index case for this endpoint: communicating hydrocephalus after "
               "intrathecal tominersen, attributed by the authors to a drug-induced "
               "sterile meningitis, resolved by ventriculoperitoneal shunting.")),
    "Viscidi_2021_OJRD": dict(
        citation=("Viscidi E, Wang N, Juneja M, et al. The incidence of hydrocephalus "
                  "among patients with and without spinal muscular atrophy (SMA): "
                  "Results from a US electronic health records study. Orphanet J Rare "
                  "Dis. 2021;16:207."),
        first_author="Viscidi E", year="2021", journal="Orphanet Journal of Rare Diseases",
        doi="10.1186/s13023-021-01822-4", pmid="33962637", pmcid="PMC8105953",
        nct_id="", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC8105953/",
        access="open_access", license="CC BY 4.0", redistribution="cc_by",
        evidence_tier="epidemiology",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("THE CONFOUNDER CONTROL. Disease background rate of hydrocephalus in SMA "
               "over a study window that ends at nusinersen approval, so it is "
               "uncontaminated by the drug.")),
    "Tofersen_seriousAE_2025_MuscleNerve": dict(
        citation=("Serious Neurologic Adverse Events in Tofersen Clinical Trials for "
                  "Amyotrophic Lateral Sclerosis. Muscle Nerve. 2025."),
        first_author="NOT_REPORTED", year="2025", journal="Muscle & Nerve",
        doi="10.1002/mus.28372", pmid="40017137", pmcid="PMC12060635", nct_id="",
        url="https://pmc.ncbi.nlm.nih.gov/articles/PMC12060635/",
        access="open_access", license="CC BY-NC-ND",
        redistribution="summary_stat_only", evidence_tier="primary_fulltext",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("ND licence term: only abstract-level summary statistics are carried; "
               "no underlying table is reproduced.")),
}


SOURCE_META.update({
    "Choroid_plexus_siSPAK_LNP_2025_NatCommun": dict(
        citation=("Targeting modulation of the choroid plexus blood-CSF barrier and CSF "
                  "hypersecretion via lipid nanoparticle-mediated co-delivery of SPAK "
                  "siRNA and resveratrol. Nat Commun. 2025;16."),
        first_author="NOT_REPORTED", year="2025", journal="Nature Communications",
        doi="10.1038/s41467-025-61543-1", pmid="40640139", pmcid="PMC12246246",
        nct_id="", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC12246246/",
        access="open_access", license="CC BY-NC-ND 4.0",
        redistribution="summary_stat_only", evidence_tier="primary_fulltext",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("Supplies the only published sequences in this release (four SPAK siRNA "
               "duplexes, Methods/Materials) and the only protective-direction rows.")),
    "AQP4_siRNA_hydrocephalus_2018_MedSciMonit": dict(
        citation=("Aquaporin 4 Silencing Aggravates Hydrocephalus Induced by Injection "
                  "of Autologous Blood in Rats. Med Sci Monit. 2018;24."),
        first_author="NOT_REPORTED", year="2018", journal="Medical Science Monitor",
        doi="10.12659/MSM.907186", pmid="29921834", pmcid="PMC6042309",
        nct_id="", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC6042309/",
        access="open_access", license="CC BY-NC", redistribution="cc_by_nc",
        evidence_tier="primary_fulltext",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("Toxic-direction nonclinical rows, and the dataset's only DESIGNED "
               "negative control (a scrambled non-targeting siRNA).")),
})


def source_meta_for(key):
    if key in SOURCE_META:
        return SOURCE_META[key]
    if key.startswith("NCT"):
        return dict(
            citation="ClinicalTrials.gov study record %s, including posted results" % key,
            first_author="NOT_APPLICABLE", year="NOT_REPORTED",
            journal="NOT_APPLICABLE", doi="", pmid="", pmcid="", nct_id=key,
            url="https://clinicaltrials.gov/study/%s" % key,
            access="public_domain", license="US Government work / public domain",
            redistribution="public_domain", evidence_tier="registry_results",
            retrieved_via="ClinicalTrials.gov v2 API, /api/v2/studies/%s" % key,
            notes=("Adverse-event module gives per-arm counts with denominators, "
                   "including explicitly reported zeros."))
    if key.startswith("WHO_INN_List_"):
        n = key.rsplit("_", 1)[1]
        return dict(
            citation="WHO Drug Information, Recommended International Nonproprietary "
                     "Names (INN) List %s" % n,
            first_author="NOT_APPLICABLE", year="NOT_REPORTED",
            journal="WHO Drug Information", doi="", pmid="", pmcid="", nct_id="",
            url="https://cdn.who.int/media/docs/default-source/"
                "international-nonproprietary-names-(inn)/rl%s.pdf" % n,
            access="open_access", license="WHO publication; reuse terms not "
                                          "established in this session",
            redistribution="verify", evidence_tier="regulatory_primary",
            retrieved_via="cdn.who.int Recommended INN list PDF, parsed by "
                          "scripts/parse_inn_sequences.py",
            notes="Supplies sequence and per-position chemistry by deterministic "
                  "parse of the INN chemical name. No measurement row derives from "
                  "this source.")
    if key.startswith("DailyMed_SPL_"):
        drug = key[len("DailyMed_SPL_"):]
        return dict(
            citation="FDA prescribing information for %s (Structured Product Label)" % drug,
            first_author="NOT_APPLICABLE", year="NOT_REPORTED",
            journal="NOT_APPLICABLE", doi="", pmid="", pmcid="", nct_id="",
            url="https://dailymed.nlm.nih.gov/dailymed/",
            access="public_domain", license="US Government work / public domain",
            redistribution="public_domain", evidence_tier="regulatory_primary",
            retrieved_via="DailyMed v2 API, spls/<setid>.xml",
            notes="Label text quoted verbatim with its LOINC-coded section.")
    return dict(citation=key, first_author="NOT_REPORTED", year="NOT_REPORTED",
                journal="NOT_APPLICABLE", doi="", pmid="", pmcid="", nct_id="",
                url="", access="NOT_REPORTED", license="NOT_REPORTED",
                redistribution="verify", evidence_tier="NOT_REPORTED",
                retrieved_via="NOT_REPORTED", notes="")


def main():
    # ---- oligo ids -------------------------------------------------------
    oligos = list(csv.DictReader(open(os.path.join(DATA, "oligos.csv"))))
    oligos.sort(key=lambda o: o["oligo_name"].lower())
    for i, o in enumerate(oligos, 1):
        o["oligo_id"] = "HYD-OLG-%04d" % i
    by_name = {o["oligo_name"]: o["oligo_id"] for o in oligos}
    cols = ["oligo_id"] + [c for c in oligos[0] if c != "oligo_id"]
    with open(os.path.join(DATA, "oligos.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(oligos)

    # ---- measurements ----------------------------------------------------
    rows, unknown = [], set()
    for fname, _tier in COMPONENTS:
        path = os.path.join(DATA, fname)
        if not os.path.exists(path):
            raise SystemExit("missing component: %s (run its build script first)" % fname)
        for src in csv.DictReader(open(path)):
            out = {c: src.get(c, "") for c in MEASUREMENT_COLS}
            name = src.get("oligo_name", "")
            if name not in by_name:
                unknown.add(name)
            out["oligo_name"] = name
            out["oligo_id"] = by_name.get(name, "UNMAPPED")
            out["source_id"] = src.get("source_key", "")
            for col in MEASUREMENT_COLS:
                if out[col] == "" and col not in ("hydroceph_grade", "event_cluster_id",
                                                  "dose_value", "dose_unit",
                                                  "dose_regimen"):
                    out[col] = "NOT_REPORTED"
            for col in ("dose_value", "dose_unit", "dose_regimen"):
                if out[col] == "":
                    out[col] = "NOT_REPORTED"
            if out["event_cluster_id"] == "":
                out["event_cluster_id"] = "NOT_APPLICABLE"
            rows.append(out)

    if unknown:
        raise SystemExit("oligo_name values absent from oligos.csv: %s" % sorted(unknown))

    for r in rows:
        r["subject_class"] = subject_class_for(r["species"], r["study_type"])
        if r["subject_class"] not in SUBJECT_CLASSES:
            raise SystemExit("unmapped subject_class for species=%r study_type=%r"
                             % (r["species"], r["study_type"]))

    for i, r in enumerate(rows, 1):
        r["measurement_id"] = "HYD-MSR-%05d" % i

    with open(os.path.join(DATA, "measurements.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=MEASUREMENT_COLS)
        w.writeheader()
        w.writerows(rows)

    # ---- sources registry ------------------------------------------------
    mod_path = os.path.join(DATA, "modifications.csv")
    mod_keys = set()
    if os.path.exists(mod_path):
        with open(mod_path) as fh:
            mod_keys = {r["source_id"] for r in csv.DictReader(fh)}
    keys = sorted({r["source_id"] for r in rows} | mod_keys)
    src_cols = ["source_id", "source_key", "citation", "first_author", "year",
                "journal", "doi", "pmid", "pmcid", "nct_id", "url", "access",
                "license", "redistribution", "evidence_tier", "retrieved_via",
                "retrieved_date", "n_oligos", "n_measurements", "notes"]
    src_rows = []
    for key in keys:
        meta = source_meta_for(key)
        mine = [r for r in rows if r["source_id"] == key]
        src_rows.append(dict(
            source_id=key, source_key=key, retrieved_date=TODAY,
            n_oligos=len({r["oligo_id"] for r in mine
                          if r["oligo_name"] not in ("NOT_APPLICABLE",
                                                     "placebo_or_sham_control")}),
            n_measurements=len(mine), **meta))
    with open(os.path.join(DATA, "sources.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=src_cols)
        w.writeheader()
        w.writerows(src_rows)

    # ---- derived merged view --------------------------------------------
    obyid = {o["oligo_id"]: o for o in oligos}
    ocols = [c for c in oligos[0] if c not in ("oligo_id", "oligo_name")]
    merged_cols = MEASUREMENT_COLS + ["oligo__" + c for c in ocols]
    with open(os.path.join(DATA, "hydrocephalus_merged.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=merged_cols)
        w.writeheader()
        for r in rows:
            o = obyid.get(r["oligo_id"], {})
            m = dict(r)
            for c in ocols:
                m["oligo__" + c] = o.get(c, "NOT_APPLICABLE")
            w.writerow(m)

    # ---- split views: human evidence and animal evidence ------------------
    # Generated, never hand-edited. They are filters over measurements.csv, kept
    # as files because "divide the human trials from the animal trials" should be
    # one command for a downstream user, not a lookup in the schema.
    splits = {
        "measurements_human.csv": lambda r: r["subject_class"].startswith("human"),
        "measurements_animal.csv": lambda r: r["subject_class"].startswith("animal"),
    }
    for fname, keep in splits.items():
        subset = [r for r in rows if keep(r)]
        with open(os.path.join(DATA, fname), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=MEASUREMENT_COLS)
            w.writeheader()
            w.writerows(subset)
        print("%-30s %4d rows (GENERATED view)" % ("data/" + fname, len(subset)))

    print("data/oligos.csv        %4d rows" % len(oligos))
    print("data/measurements.csv  %4d rows x %d cols" % (len(rows), len(MEASUREMENT_COLS)))
    print("data/sources.csv       %4d rows" % len(src_rows))
    print("data/hydrocephalus_merged.csv %4d rows x %d cols (GENERATED)"
          % (len(rows), len(merged_cols)))


if __name__ == "__main__":
    main()
