#!/usr/bin/env bash
# Render a quick preview and open the result. Override quality with -q h.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/scripts/build.sh" -q l --preview "$@"
