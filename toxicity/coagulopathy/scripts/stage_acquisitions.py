#!/usr/bin/env python3
"""Acquire the critical open-access records into research staging.

    python3 toxicity/coagulopathy/scripts/stage_acquisitions.py
    -> research/2026-10-03/staging/ + staging_manifest.csv

Authorisation. Crank's 2026-10-03 delegation sets the standing rule: "acquisition and
description run in parallel. Ingestion, promotion and release are gated." Beebop's
2026-10-02 research request authorises obtaining "legally accessible articles/supplements/raw
files into clearly separate research staging" and requires that staged files preserve
"checksums, source URLs, original filenames, file/sheet inventories and provenance". This
script does exactly that and no more: files land in research/, never in data/, and nothing
is extracted from them here. Ingestion remains gated.

Only open-access records are fetched, and openness is read from the Europe PMC record rather
than assumed -- an earlier session offered fullTextXML for non-open records and collected
five confident 404s. A record that is not open is reported as not fetched, with the licence
field that says so. No paywall is circumvented, no login is used, nothing is purchased.
"""
import csv, hashlib, json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "research", "2026-10-03", "staging")
MAN = os.path.join(ROOT, "research", "2026-10-03", "staging_manifest.csv")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"

# The critical and high-priority entries of the 2026-10-02 acquisition plan that this
# endpoint does not already hold. PMC13009829 is deliberately absent: it is already in the
# corpus as COG-S023, which the plan recorded as UNKNOWN.
TARGETS = [
    {"pmcid": "PMC8804562", "pmid": "33567808", "rank": 1,
     "what": "2'MOE ASOs activate human platelets through GPVI; per-compound GPVI KD, 7-donor variance",
     "gap": "human_in_vitro_assay"},
    {"pmcid": "PMC5673186", "pmid": "29107969", "rank": 2,
     "what": "Single-stranded oligo effects in vitro; length and PS-linkage count as covariates (panel is in the SI)",
     "gap": "sequence_or_chemistry"},
    {"pmcid": "PMC9718591", "pmid": "35977698", "rank": 3,
     "what": "Donidalorsen coagulation and fibrinolysis panel; 22 HAE patients x 13 assays",
     "gap": "human_trial_endpoint"},
    {"pmcid": "PMC10143489", "pmid": "37111598", "rank": 5,
     "what": "ASO platelet activation in Gottingen minipig; per-position chemistry for 7 constructs plus cross-species map",
     "gap": "human_animal_bridge"},
    {"pmcid": "PMC4322051", "pmid": "25646267", "rank": 7,
     "what": "Phosphorothioate backbone as the platelet-activating moiety; human GPVI-deficient platelets as a genetic negative control",
     "gap": "human_in_vitro_assay"},
]


def get(url, out_path=None, tries=3):
    for i in range(tries):
        r = subprocess.run(["curl", "-sSL", "--max-time", "120", "-w", "%{http_code}",
                            "-o", out_path or "/dev/stdout", url],
                           capture_output=True, text=True)
        code = (r.stdout or "").strip()[-3:]
        if code.startswith("2"):
            return True, code
        time.sleep(2 ** i)
    return False, code


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for t in TARGETS:
        rec = dict(t)
        rec.update({"retrieved": "2026-10-03", "staged_file": "", "sha256": "", "bytes": "",
                    "licence": "", "is_open_access": "", "source_url": "", "outcome": ""})

        # openness is READ, not assumed
        meta = os.path.join(OUT, f"_{t['pmcid']}.meta.json")
        ok, code = get(f"{EPMC}/search?query=PMCID:{t['pmcid']}&resultType=core&format=json", meta)
        lic = oa = ""
        if ok and os.path.exists(meta):
            try:
                res = (json.load(open(meta)).get("resultList", {}).get("result") or [{}])[0]
                lic, oa = str(res.get("license") or ""), str(res.get("isOpenAccess") or "")
                rec["licence"], rec["is_open_access"] = lic or "not_stated", oa
            except Exception as e:
                rec["licence"] = f"metadata_unparsed:{e}"
            os.remove(meta)
        else:
            rec["licence"] = f"metadata_fetch_failed_http_{code}"

        if oa != "Y":
            rec["outcome"] = ("NOT FETCHED - Europe PMC does not mark this record open access "
                              f"(isOpenAccess={oa or 'unknown'}, licence={lic or 'not stated'}). "
                              "No paywall was circumvented and no login was used.")
            rows.append(rec)
            print(f"  {t['pmcid']}  SKIPPED (not open access)")
            continue

        url = f"{EPMC}/{t['pmcid']}/fullTextXML"
        dest = os.path.join(OUT, f"{t['pmcid']}.xml")
        ok, code = get(url, dest)
        if ok and os.path.exists(dest) and os.path.getsize(dest) > 2000:
            b = open(dest, "rb").read()
            rec.update({"staged_file": os.path.relpath(dest, ROOT),
                        "sha256": hashlib.sha256(b).hexdigest(),
                        "bytes": str(len(b)), "source_url": url,
                        "outcome": "staged"})
            print(f"  {t['pmcid']}  staged {len(b):,} bytes  licence={lic}")
        else:
            if os.path.exists(dest):
                os.remove(dest)
            rec["outcome"] = f"FETCH FAILED http_{code} from {url}"
            print(f"  {t['pmcid']}  FAILED http {code}")
        rows.append(rec)

    with open(MAN, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    n = sum(1 for r in rows if r["outcome"] == "staged")
    print(f"\n  {n} of {len(rows)} staged into research/2026-10-03/staging/")
    print(f"  manifest: research/2026-10-03/staging_manifest.csv")
    print("  NOTHING INGESTED. data/ is untouched; ingestion is gated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
