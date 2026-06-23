#!/usr/bin/env bash
#
# update_definitions.sh — Refresh the live API pages from the current source.
#
# Use this after a SOURCE change (edited docstrings or signatures) when the nav LAYOUT
# is unchanged. It re-extracts the API and regenerates the per-method and free-function
# pages straight into the live docs/api, in place — these carry no hand-authored prose,
# so they are always safe to overwrite. Class index.md pages are NOT written here: they
# may hold hand-curated prose/examples, so regenerating them goes through a staging tree
# (see below), never straight over the live docs. Section overviews and hand-authored
# constant pages are likewise left untouched.
#
# To regenerate class indexes (a docstring/signature change you want reflected on the
# index, or a nav LAYOUT change — new/renamed sections, a moved or merged library), use
# rebuild_layout.sh: it stages a full rebuild (indexes included) under _outline for
# review and diff before you promote it, so live prose is never destroyed.
#
#   ./update_definitions.sh                  # methods (default): per-method/function pages
#   ./update_definitions.sh methods+classes  # also overwrite live class indexes (rarely
#                                            # wanted — discards any hand-authored prose)
#
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"
SRC="$REPO_ROOT/src"
MKDOCS="$REPO_ROOT/mkdocs.yml"
DOCS="$REPO_ROOT/docs"
API_DATA="$SCRIPTS_DIR/_api_data"
MODE="${1:-methods}"

# extract_api writes _api_data/ relative to the cwd; style_api writes pages under the
# docs root (the nav targets carry the leading "api/").
cd "$SCRIPTS_DIR"

echo "1/2  Extracting API from $SRC"
rm -f "$API_DATA"/*.json
python3 extract_api.py "$SRC" >/dev/null

echo "2/2  Regenerating ($MODE) into $DOCS/api"
python3 style_api.py "$MKDOCS" "$API_DATA" "$DOCS" "$MODE"
