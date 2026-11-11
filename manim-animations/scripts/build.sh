#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
    exec "$ROOT/.venv/bin/python" "$ROOT/scripts/render.py" "$@"
fi
exec python3 "$ROOT/scripts/render.py" "$@"
