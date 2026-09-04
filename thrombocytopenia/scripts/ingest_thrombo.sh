#!/usr/bin/env bash
# Full ingestion round for the OligoTox-Thrombocytopenia dataset.
#
# Harvest completed workflow agents -> merge every lane -> assemble the canonical
# CSVs (applying verification verdicts, deduping, assigning stable keys) -> re-apply
# the committed verdicts -> gate on QC -> regenerate the derived view and the
# generated README sections.
#
# EVERYTHING THIS SCRIPT WRITES STAYS INSIDE thrombocytopenia/. The only path it
# reads outside the endpoint is the sister kidney dataset's oligos.csv, via
# enrich_from_kidney.py, and that is read-only.
#
# Safe to re-run at any point: assembly deduplicates measurements on their natural
# key, so harvesting the same agent twice does not double-count, and every output
# is rebuilt from the lane files rather than appended to.
#
# QC gates the round: if it fails, the derived view and docs are NOT regenerated,
# so a broken dataset cannot quietly ship with fresh-looking documentation.
#
# Usage:  thrombocytopenia/scripts/ingest_thrombo.sh [scratch_dir] [workflow_journal]

set -euo pipefail

S_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # thrombocytopenia/scripts
ENDPOINT="$(dirname "$S_DIR")"                          # thrombocytopenia
CURATION="$ENDPOINT/curation"
SCRATCH="${1:-${TMPDIR:-/tmp}/oligotox-thrombo-ingest}"
JOURNAL="${2:-}"
mkdir -p "$SCRATCH"

echo "== 1. harvest completed workflow agents =="
if [[ -n "$JOURNAL" && -f "$JOURNAL" ]]; then
  python3 "$S_DIR/harvest_workflow.py" "$JOURNAL" "$CURATION/lanes/workflow_harvest.json"
else
  echo "   (no workflow journal given — using the committed lanes as they stand)"
fi

echo
echo "== 2. merge lanes =="
shopt -s nullglob
LANES=("$CURATION"/lanes/*.json)
shopt -u nullglob
if [[ ${#LANES[@]} -eq 0 ]]; then
  echo "no lane files in $CURATION/lanes — nothing to ingest" >&2
  exit 1
fi
python3 "$S_DIR/merge_lane_files.py" "$SCRATCH/merged.json" "${LANES[@]}"

echo
echo "== 3. assemble (first pass) =="
python3 "$S_DIR/assemble_thrombo.py" "$SCRATCH/merged.json"

# The kidney enrichment lane is built FROM the assembled oligos.csv, so it can only
# be generated after a first pass; a second assembly then folds it in. It reads the
# sister dataset and writes only into this endpoint.
echo
echo "== 4. enrich from the sister kidney dataset and re-assemble =="
python3 "$S_DIR/enrich_from_kidney.py" > "$SCRATCH/kidney_lane.json"
python3 "$S_DIR/merge_lane_files.py" "$SCRATCH/merged_final.json" \
    "${LANES[@]}" "$SCRATCH/kidney_lane.json" >/dev/null
python3 "$S_DIR/assemble_thrombo.py" "$SCRATCH/merged_final.json"

# Re-assembly renumbers measurement_ids, so verification markers written into the
# previous CSV are gone by this point. The committed verdicts carry a natural key
# drawn from row content, so they survive that renumbering and are re-applied here
# automatically — otherwise every ingestion round would silently discard the
# verification work and the dataset would quietly regress to "unverified".
echo
echo "== 5. re-apply committed verification verdicts =="
shopt -s nullglob
VERDICTS=("$CURATION"/verdicts/*.json)
shopt -u nullglob
if [[ ${#VERDICTS[@]} -gt 0 ]]; then
  python3 "$S_DIR/apply_verdicts.py" "${VERDICTS[@]}"
else
  echo "   (no verdict files committed yet — all rows will read as unverified)"
fi

echo
echo "== 6. QC (gates the round) =="
python3 "$S_DIR/qc_thrombo.py"

# Two datasets in this repository share compounds, and design metadata is
# deliberately read across from the sister nephrotoxicity set. An OUTCOME crossing
# over would be a silent scientific error that schema validation cannot see, so
# endpoint alignment is proven on every round rather than assumed.
echo
echo "== 7. endpoint-alignment audit (no cross-toxicity contamination) =="
python3 "$S_DIR/audit_endpoint.py"

echo
echo "== 8. rebuild derived view + generated docs =="
python3 "$S_DIR/build_merged_thrombo.py"
python3 "$S_DIR/refresh_docs.py"
python3 "$S_DIR/split_human_animal.py"

# The submission artefacts are generated from the data too, so a round that changes
# the dataset cannot leave a stale workbook or a PDF quoting last round's counts.
echo
echo "== 9. regenerate submission artefacts =="
python3 "$S_DIR/build_workbook.py"
python3 "$S_DIR/render_submission.py"
python3 "$S_DIR/build_sources_doc.py"

echo
echo "ingestion round complete."
