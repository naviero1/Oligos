#!/usr/bin/env bash
# Full ingestion round for the OligoTox-Thrombocytopenia dataset.
#
# Harvest completed workflow agents -> merge every lane -> assemble the canonical
# CSVs (applying verification verdicts, deduping, assigning stable keys) -> gate on
# QC -> regenerate the derived analysis view and the generated README sections.
#
# Safe to re-run at any point: assembly deduplicates measurements on their natural
# key, so harvesting the same agent twice does not double-count, and every output
# is rebuilt from the lane files rather than appended to.
#
# QC gates the round: if it fails, the derived view and docs are NOT regenerated,
# so a broken dataset cannot quietly ship with fresh-looking documentation.
#
# Usage:  scripts/ingest_thrombo.sh [scratch_dir] [workflow_journal]

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRATCH="${1:-/tmp/claude-0/-home-user-Claude-Works/189fa036-08d6-5409-99b8-7265f67bf20d/scratchpad}"
JOURNAL="${2:-}"

cd "$REPO"

echo "== 1. harvest completed workflow agents =="
if [[ -n "$JOURNAL" && -f "$JOURNAL" ]]; then
  python3 scripts/harvest_workflow.py "$JOURNAL" "$SCRATCH/workflow_harvest.json"
else
  echo "   (no workflow journal given — using existing $SCRATCH/workflow_harvest.json if present)"
fi

echo
echo "== 2. merge lanes =="
LANES=()
for f in labels_lane.json lane_preclinical_negatives.json lane_patents_panels.json \
         lane_crooke2017.json lane_patents2_reviews.json workflow_harvest.json; do
  [[ -f "$SCRATCH/$f" ]] && LANES+=("$SCRATCH/$f")
done
if [[ ${#LANES[@]} -eq 0 ]]; then
  echo "no lane files found in $SCRATCH — nothing to ingest" >&2
  exit 1
fi
python3 scripts/merge_lane_files.py "$SCRATCH/merged.json" "${LANES[@]}"

echo
echo "== 3. assemble (first pass) =="
python3 scripts/assemble_thrombo.py "$SCRATCH/merged.json"

# The kidney enrichment lane is built FROM the assembled oligos.csv, so it can only
# be generated after a first pass; a second assembly then folds it in.
echo
echo "== 4. enrich from the sister kidney dataset and re-assemble =="
python3 scripts/enrich_from_kidney.py > "$SCRATCH/kidney_lane.json"
python3 scripts/merge_lane_files.py "$SCRATCH/merged_final.json" \
    "${LANES[@]}" "$SCRATCH/kidney_lane.json" >/dev/null
python3 scripts/assemble_thrombo.py "$SCRATCH/merged_final.json"

# Re-assembly renumbers measurement_ids, so verification markers written into the
# previous CSV are gone by this point. The committed verdicts carry a natural key
# drawn from row content, so they survive that renumbering and are re-applied here
# automatically — otherwise every ingestion round would silently discard the
# verification work and the dataset would quietly regress to "unverified".
echo
echo "== 5. re-apply committed verification verdicts =="
VERDICTS=(thrombocytopenia/curation/verdicts/*.json)
if [[ -e "${VERDICTS[0]}" ]]; then
  python3 scripts/apply_verdicts.py "${VERDICTS[@]}"
else
  echo "   (no verdict files committed yet — all rows will read as unverified)"
fi

echo
echo "== 6. QC (gates the round) =="
python3 scripts/qc_thrombo.py

echo
echo "== 7. rebuild derived view + generated docs =="
python3 scripts/build_merged_thrombo.py
python3 scripts/refresh_docs.py

echo
echo "ingestion round complete."
