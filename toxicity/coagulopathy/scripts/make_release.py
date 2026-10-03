#!/usr/bin/env python3
"""Build the whole coagulopathy release, in order, from a clean checkout.

    python3 toxicity/coagulopathy/scripts/make_release.py

    sources/extraction/*.json          (committed extraction records)
        -> data/*.csv                  build_dataset.py
        -> 55 structural checks        validate_dataset.py      [fails the build]
        -> values vs source documents  verify_against_sources.py[fails the build]
        -> assets/*.svg                make_figures.py
        -> the three submission PDFs   build_documents.py       [enforces page limits]
        -> the release workbook        build_release_xlsx.py
        -> SOURCES.md                  build_sources_md.py

No network access is required at any step. Any failing step stops the release.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [("build_study_register.py", "deduplicated human study register"),
         ("build_dataset.py", "assemble the tables"),
         ("validate_dataset.py", "structural QC"),
         ("verify_against_sources.py", "values against their sources"),
         ("audit_attribution.py", "attribution audit of the harm-flagged participant rows"),
         ("make_figures.py", "figures"),
         ("build_documents.py", "narrative, methodology, PADP"),
         ("check_doc_numbers.py", "document figures against the data"),
         ("build_release_xlsx.py", "release workbook"),
         ("build_sources_pdf.py", "sources & provenance document"),
         ("build_download_manifest.py", "download manifest + fetch script"),
         ("build_sources_md.py", "source registry"),
         ("build_release_manifest.py", "release manifest (binds everything to one commit)")]

for script, what in STEPS:
    print(f"\n== {what} ({script})")
    r = subprocess.run([sys.executable, os.path.join(HERE, script)])
    if r.returncode != 0:
        sys.exit(f"\nRELEASE FAILED at {script}")
print("\nRelease built and checked.")
