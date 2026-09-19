#!/bin/sh
# Serve Nordstern locally. Both pages also open fine over file:// — every
# artifact is a <script> tag rather than a fetch() for exactly that reason,
# including the snapshot series — so this is here for consistency with the rest
# of the family, and for when the payload outgrows a single file and the pages
# start fetching per-record JSON.
#
#   web/index.html   the map   — charts, all derived, every figure a query link
#   web/query.html   the tool  — the query language over the whole register

cd "$(dirname "$0")" || exit 1
PORT="${1:-8000}"
echo "Nordstern:  http://localhost:$PORT/web/          (the map)"
echo "            http://localhost:$PORT/web/query.html (the tool)"
exec python3 -m http.server "$PORT"
