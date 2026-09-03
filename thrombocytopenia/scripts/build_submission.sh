#!/usr/bin/env bash
# Render the Phase 2 submission PDFs from their HTML sources.
#
# Headless Chromium is used rather than a LaTeX or Word toolchain so the documents
# rebuild anywhere the repository is checked out, with no proprietary dependency —
# the same openness the dataset itself claims.
#
# Page limits are enforced here, not left to a reviewer: the script fails if a
# document exceeds the limit the announcement sets.
set -euo pipefail

S_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUB="$(dirname "$S_DIR")/submission"
CHROME="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
[[ -x "$CHROME" ]] || CHROME="$(command -v chromium || command -v google-chrome)"

declare -A LIMIT=( [narrative]=12 [methodology]=5 [padp]=5 )
fail=0
for doc in narrative methodology padp; do
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
      --print-to-pdf="$SUB/$doc.pdf" "$SUB/$doc.html" 2>/dev/null
  n=$(python3 -c "import pymupdf,sys;print(len(pymupdf.open('$SUB/$doc.pdf')))")
  lim=${LIMIT[$doc]}
  if (( n > lim )); then
    echo "  FAIL $doc.pdf: $n pages exceeds the $lim-page limit"; fail=1
  else
    echo "  ok   $doc.pdf: $n / $lim pages"
  fi
done
exit $fail
