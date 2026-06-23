#!/usr/bin/env bash
#
# rebuild_layout.sh — Rebuild the whole API reference tree from mkdocs.yml's nav.
#
# Use this after a NAV / LAYOUT change: new or renamed sections, a class or library
# moved to a different category, a library folded into another, or functions added to
# (or dropped from) a library's nav. It regenerates everything from source into a
# staging tree under _scripts (_outline/api), and does NOT touch the live docs/api, so
# the new layout can be reviewed and diffed before it goes live.
#
# Pipeline (all output stays inside _scripts):
#   1. extract_api.py        src/        -> _api_data/   (fresh API inventory)
#   2. build_outline.py      mkdocs.yml  -> _outline/    (section + leaf skeleton)
#   3. style_api.py          ...         -> _outline/    (class/method/function pages)
#   4. restore_handwritten.py            -> _outline/    (hand-authored pages, e.g. constants)
#
# Watch step 3's report for classes missing from the nav or given a flat page.
# When the staged tree looks right, promote it (this is the only step that touches the
# live docs):
#   rm -rf docs/api && mv docs/_scripts/_outline/api docs/api
#
set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"
SRC="$REPO_ROOT/src"
MKDOCS="$REPO_ROOT/mkdocs.yml"
DOCS="$REPO_ROOT/docs"
API_DATA="$SCRIPTS_DIR/_api_data"
OUTLINE="$SCRIPTS_DIR/_outline"

# extract_api and build_outline write _api_data/ and _outline/ relative to the cwd.
cd "$SCRIPTS_DIR"

echo "1/4  Extracting API from $SRC"
rm -f "$API_DATA"/*.json
python3 extract_api.py "$SRC" >/dev/null

echo "2/4  Building outline skeleton from nav"
python3 build_outline.py "$MKDOCS" >/dev/null

echo "3/4  Generating class/method/function pages"
python3 style_api.py "$MKDOCS" "$API_DATA" "$OUTLINE" methods+classes

echo "4/4  Restoring hand-authored pages (constants, etc.)"
python3 restore_handwritten.py "$MKDOCS" "$DOCS" "$OUTLINE"

echo
echo "Staged new layout at: $OUTLINE/api"
echo "Review it, then promote with:"
echo "  rm -rf \"$DOCS/api\" && mv \"$OUTLINE/api\" \"$DOCS/api\""
