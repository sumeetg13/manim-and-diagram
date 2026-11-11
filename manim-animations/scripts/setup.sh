#!/usr/bin/env bash
# Create a project-local environment. Native libraries must be installed first.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v pkg-config >/dev/null 2>&1 || ! pkg-config --exists cairo pangocairo; then
    echo "Cairo, Pango, and pkg-config are required. Install them, then rerun this script."
    if [[ "$(uname -s)" == "Darwin" ]]; then
        echo "  brew install python@3.13 cairo pango pkg-config"
    else
        echo "  sudo apt-get install python3-dev python3-venv build-essential pkg-config libcairo2-dev libpango1.0-dev"
    fi
    exit 1
fi

PYTHON_BIN="${PYTHON:-}"
if [[ -z "$PYTHON_BIN" ]]; then
    for candidate in python3.13 python3.12 python3.14 python3.11 python3; do
        if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
            PYTHON_BIN="$(command -v "$candidate")"
            break
        fi
    done
fi
if [[ -z "$PYTHON_BIN" ]] || ! "$PYTHON_BIN" -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
    echo "Python 3.11+ is required. Set PYTHON=/path/to/python3.13 if needed."
    exit 1
fi

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
    "$PYTHON_BIN" -m venv "$ROOT/.venv"
fi
"$ROOT/.venv/bin/python" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Existing .venv needs Python 3.11+; move it aside and rerun setup.")'
"$ROOT/.venv/bin/python" -m pip install --upgrade pip
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements.txt"
"$ROOT/.venv/bin/python" -m manim --version
echo "Setup complete. Try: ./scripts/run.sh fourier"
