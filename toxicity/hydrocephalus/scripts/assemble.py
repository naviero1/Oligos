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
import re
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
        citation=("Lovett A, Chary S, Babu S, et al. Serious Neurologic Adverse Events "
                  "in Tofersen Clinical Trials for Amyotrophic Lateral Sclerosis. "
                  "Muscle Nerve. 2025;71:1006-1015."),
        first_author="Lovett A", year="2025", journal="Muscle & Nerve",
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
        citation=("Wang Q, Xia X, Zhang H, et al. Targeting modulation of the choroid "
                  "plexus blood-CSF barrier and CSF hypersecretion via lipid "
                  "nanoparticle-mediated co-delivery of siRNA and resveratrol. "
                  "Nat Commun. 2025;16:6389."),
        first_author="Wang Q", year="2025", journal="Nature Communications",
        doi="10.1038/s41467-025-61543-1", pmid="40640139", pmcid="PMC12246246",
        nct_id="", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC12246246/",
        access="open_access", license="CC BY-NC-ND 4.0",
        redistribution="summary_stat_only", evidence_tier="primary_fulltext",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("Supplies the only published sequences in this release (four SPAK siRNA "
               "duplexes, Methods/Materials) and the only protective-direction rows.")),
    "AQP4_siRNA_hydrocephalus_2018_MedSciMonit": dict(
        # DOI CORRECTION. This entry recorded 10.12659/MSM.907186, which resolves
        # to nothing: Crossref returns 404 for it. The article's own PMC XML, the
        # publisher PDF's running header and Crossref all give 10.12659/MSM.906936
        # for volume 24, pages 4204-4212. The locator check now resolves DOIs as
        # well as URLs, so a citation cannot again carry a DOI that goes nowhere.
        citation=("Guo J, Mi X, Zhan R, Li M, Wei L, Sun J. Aquaporin 4 Silencing "
                  "Aggravates Hydrocephalus Induced by Injection of Autologous Blood "
                  "in Rats. Med Sci Monit. 2018;24:4204-4212."),
        first_author="Guo J", year="2018", journal="Medical Science Monitor",
        doi="10.12659/MSM.906936", pmid="29921834", pmcid="PMC6042309",
        nct_id="", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC6042309/",
        access="open_access", license="CC BY-NC", redistribution="cc_by_nc",
        evidence_tier="primary_fulltext",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("Toxic-direction nonclinical rows, and the dataset's only DESIGNED "
               "negative control (a scrambled non-targeting siRNA).")),
})


# Sources that carry measurement or modification rows but whose citation details
# lived only in their builder's module header, never reaching this registry. A
# row whose provenance is a comment in a script is not a cited row: qc/validate.py
# now refuses any source that resolves to the fallback stub.
SOURCE_META.update({
    "Gai2_antisense_ependymal_2007_BMCNeurosci": dict(
        citation=("M\u00f6nkk\u00f6nen KS, Hakum\u00e4ki JM, Hirst RA, et al. "
                  "Intracerebroventricular antisense knockdown of G-alpha-i2 results "
                  "in ciliary stasis and ventricular dilatation in the rat. "
                  "BMC Neurosci. 2007;8:26."),
        first_author="M\u00f6nkk\u00f6nen KS", year="2007", journal="BMC Neuroscience",
        doi="10.1186/1471-2202-8-26", pmid="17430589", pmcid="PMC1855344", nct_id="",
        url="https://pmc.ncbi.nlm.nih.gov/articles/PMC1855344/",
        access="open_access", license="CC BY 2.0", redistribution="cc_by",
        evidence_tier="primary_fulltext",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("The only source measuring one oligonucleotide BOTH in vitro (ciliary "
               "beat frequency in cultured ependymal cells) and in vivo (MRI "
               "ventricular volume), which is the extrapolation the Phase 2 brief "
               "calls a particular interest. Supplies three published sequences "
               "including two designed controls, and the only stated purity value in "
               "the release (HPLC-purified, 90-97%).")),
    "Nakayama_2026_NatMed_KCNT1": dict(
        citation=("Nakayama T, El Achkar CM, Burbano LE, et al. Antisense "
                  "oligonucleotide-mediated knockdown therapy in two infants with "
                  "severe KCNT1 epileptic encephalopathy. Nat Med. 2026;32:1411."),
        first_author="Nakayama T", year="2026", journal="Nature Medicine",
        doi="10.1038/s41591-026-04314-9", pmid="41981306", pmcid="PMC13099374",
        nct_id="", url="https://pmc.ncbi.nlm.nih.gov/articles/PMC13099374/",
        access="open_access", license="CC BY-NC-ND 4.0",
        redistribution="summary_stat_only", evidence_tier="case_report",
        retrieved_via="Europe PMC REST fullTextXML endpoint",
        notes=("The SECOND independent drug-attributed signal, and the reason this "
               "release does not call hydrocephalus a tominersen-specific finding: a "
               "different ASO (valeriasen/KT777), a different target, indication and "
               "age group, and both treated infants developed the endpoint. ND "
               "licence term: summary statistics only.")),
})

# EMA Summaries of Product Characteristics (Annex I of the EPAR product
# information). Included because the EU and US regulators reached materially
# different positions on the same molecules. EMA reuse terms were not established
# in this session, so redistribution stays `verify` rather than assumed open.
_EMA_SMPC = {
    "EMA_SmPC_Spinraza": ("Spinraza", "nusinersen", "spinraza",
                          "first authorised 30 May 2017, latest renewal 31 January 2022"),
    "EMA_SmPC_Qalsody": ("Qalsody", "tofersen", "qalsody",
                         "first authorised 29 May 2024"),
    "EMA_SmPC_Tegsedi": ("Tegsedi", "inotersen", "tegsedi",
                         "first authorised 06 July 2018, latest renewal 24 March 2023"),
}
for _key, (_brand, _inn, _slug, _auth) in _EMA_SMPC.items():
    SOURCE_META[_key] = dict(
        citation=("European Medicines Agency. %s (%s) EPAR product information, "
                  "Annex I Summary of Product Characteristics (%s)."
                  % (_brand, _inn, _auth)),
        first_author="NOT_APPLICABLE", year="NOT_REPORTED",
        journal="EMA European Public Assessment Report", doi="", pmid="", pmcid="",
        nct_id="",
        url="https://www.ema.europa.eu/en/documents/product-information/"
            "%s-epar-product-information_en.pdf" % _slug,
        access="open_access",
        license="EMA publication; reuse terms not established in this session",
        redistribution="verify", evidence_tier="regulatory_primary",
        retrieved_via=("ema.europa.eu EPAR product-information PDF, text extracted "
                       "and swept section by section"),
        notes=("EU label, quoted verbatim with its Annex I section number. The EPAR "
               "landing page is https://www.ema.europa.eu/en/medicines/human/EPAR/%s "
               "and the PDF is revised in place, so the retrieval date fixes which "
               "revision was read." % _slug))


_LABEL_VERSIONS = None


def _label_version(drug):
    """(setid, published_date) for a drug, read from the label component's own
    source_ref. Parsed rather than typed so the citation cannot drift from the
    document the extractor actually read."""
    global _LABEL_VERSIONS
    if _LABEL_VERSIONS is None:
        _LABEL_VERSIONS = {}
        path = os.path.join(DATA, "_label_measurements.csv")
        if os.path.exists(path):
            for r in csv.DictReader(open(path)):
                m = re.match(r"DailyMed setid ([0-9a-f-]+), label published (.+)$",
                             r.get("source_ref", "") or "")
                if m:
                    _LABEL_VERSIONS.setdefault(r.get("oligo_name", ""), m.groups())
    return _LABEL_VERSIONS.get(drug, (None, None))


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
        # A generic dailymed.nlm.nih.gov link does not identify WHICH label was
        # read, and a US label is revised in place. The setid and publication date
        # recorded by the extractor on every label row make the citation resolve to
        # one specific document version.
        setid, published = _label_version(drug)
        url = ("https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=%s" % setid
               if setid else "https://dailymed.nlm.nih.gov/dailymed/")
        return dict(
            citation=("FDA prescribing information for %s (DailyMed Structured "
                      "Product Label, setid %s, published %s)"
                      % (drug, setid or "NOT_REPORTED", published or "NOT_REPORTED")),
            first_author="NOT_APPLICABLE", year="NOT_REPORTED",
            journal="NOT_APPLICABLE", doi="", pmid="", pmcid="", nct_id="",
            url=url,
            access="public_domain", license="US Government work / public domain",
            redistribution="public_domain", evidence_tier="regulatory_primary",
            retrieved_via=("DailyMed v2 API, GET /dailymed/services/v2/spls/%s.xml"
                           % (setid or "<setid>")),
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
    # The human subset is the dataset's most important slice, so it is enriched:
    # every row carries the compound's SEQUENCE and design alongside its toxicity
    # grade, so a reader never has to join back to oligos.csv to see them.
    obyid = {o["oligo_id"]: o for o in oligos}
    ENRICH = ["sequence_5to3_asprinted", "sequence_base", "length_nt",
              "backbone_chemistry", "sugar_modifications", "modification_pattern",
              "oligo_class", "target_gene", "conjugate", "purity_pct",
              "sequence_source"]
    view_cols = MEASUREMENT_COLS + ["oligo__" + c for c in ENRICH]
    for fname, keep in splits.items():
        subset = []
        for r in rows:
            if not keep(r):
                continue
            o = obyid.get(r["oligo_id"], {})
            row = dict(r)
            for c in ENRICH:
                row["oligo__" + c] = o.get(c, "NOT_APPLICABLE")
            subset.append(row)
        with open(os.path.join(DATA, fname), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=view_cols)
            w.writeheader()
            w.writerows(subset)
        with_seq = sum(1 for r in subset if r["oligo__sequence_5to3_asprinted"]
                       not in ("NOT_REPORTED", "NOT_APPLICABLE"))
        print("%-30s %4d rows (GENERATED view; %d carry a sequence)"
              % ("data/" + fname, len(subset), with_seq))

    # ---- German's analysis: one row per compound ---------------------------
    # Requested slice: oligo, its sequence, the modification to that sequence,
    # and its toxicity. One row per compound, so it reads as a compound-level
    # summary rather than a measurement list.
    mods = []
    mpath = os.path.join(DATA, "modifications.csv")
    if os.path.exists(mpath):
        with open(mpath) as fh:
            mods = list(csv.DictReader(fh))
    bymod = {}
    for r in mods:
        bymod.setdefault(r["oligo_id"], []).append(r)

    ga = []
    for o in oligos:
        if o["oligo_name"] in ("placebo_or_sham_control", "NOT_APPLICABLE"):
            continue
        mine = [r for r in rows if r["oligo_id"] == o["oligo_id"]]
        graded = [int(r["hydroceph_grade"]) for r in mine if r["hydroceph_grade"]]
        pos = sorted(bymod.get(o["oligo_id"], []),
                     key=lambda r: int(r["position_5to3"]))
        sugar_map = "".join({"2'-MOE": "M", "DNA_2prime_deoxy": "d", "LNA": "L",
                             "2'-OMe": "o", "morpholino": "P"}.get(
                                 r["sugar_chemistry"], "?") for r in pos)
        link_map = "".join({"phosphorothioate": "S", "phosphodiester": "o",
                            "terminal_none": "."}.get(
                                r["linkage_3prime"], "?") for r in pos)
        methyl_map = "".join("m" if r["base_modification"].startswith("5-methyl")
                             else "-" for r in pos)
        tierA_pos = sum(1 for r in mine if r["endpoint_tier"] == "A"
                        and r["ascertainment"] == "measured_positive")
        ga.append(dict(
            oligo_id=o["oligo_id"], oligo_name=o["oligo_name"],
            oligo_class=o["oligo_class"], target_gene=o["target_gene"],
            route_of_administration=o["route_of_administration"],
            length_nt=o["length_nt"],
            sequence_5to3=o["sequence_5to3_asprinted"],
            sequence_base=o["sequence_base"],
            sequence_source=o["sequence_source"][:200],
            backbone_chemistry=o["backbone_chemistry"],
            sugar_modifications=o["sugar_modifications"],
            modification_pattern=o["modification_pattern"],
            per_position_sugar_map=sugar_map or "NOT_REPORTED",
            per_position_linkage_map=link_map or "NOT_REPORTED",
            per_position_5methyl_map=methyl_map or "NOT_REPORTED",
            n_positions_mapped=len(pos),
            purity_pct=o["purity_pct"],
            max_hydroceph_grade=(max(graded) if graded else ""),
            n_measurements=len(mine),
            n_tierA_positive=tierA_pos,
            n_tierA_measured_null=sum(1 for r in mine if r["endpoint_tier"] == "A"
                                      and r["ascertainment"] == "measured_null"),
            any_human_evidence=("TRUE" if any(r["subject_class"].startswith("human")
                                              for r in mine) else "FALSE"),
            tox_axes=";".join(sorted({r["tox_axis"] for r in mine})) or "none",
        ))
    ga.sort(key=lambda r: (-(r["max_hydroceph_grade"] or 0), -r["n_tierA_positive"],
                           r["oligo_name"]))
    gpath = os.path.join(DATA, "germans_analysis.csv")
    with open(gpath, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ga[0].keys()))
        w.writeheader()
        w.writerows(ga)
    print("%-30s %4d compounds (GENERATED view; %d with a sequence)"
          % ("data/germans_analysis.csv", len(ga),
             sum(1 for r in ga if r["sequence_5to3"]
                 not in ("NOT_REPORTED", "NOT_APPLICABLE"))))

    print("data/oligos.csv        %4d rows" % len(oligos))
    print("data/measurements.csv  %4d rows x %d cols" % (len(rows), len(MEASUREMENT_COLS)))
    print("data/sources.csv       %4d rows" % len(src_rows))
    print("data/hydrocephalus_merged.csv %4d rows x %d cols (GENERATED)"
          % (len(rows), len(merged_cols)))


if __name__ == "__main__":
    main()
