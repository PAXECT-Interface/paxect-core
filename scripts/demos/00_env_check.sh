#!/usr/bin/env bash
# PAXECT Demo 00 — Environment sanity check
set -euo pipefail

echo "[00] Environment sanity check"

# Check that the paxect CLI exists
if ! command -v paxect >/dev/null 2>&1; then
  echo "❌ paxect CLI not in PATH"
  exit 1
else
  echo "✅ paxect CLI found"
fi

# Check that the Python core module imports
if ! python3 -c "import paxect_core" 2>/dev/null; then
  echo "❌ paxect_core not importable (check PYTHONPATH)"
  exit 1
else
  echo "✅ paxect_core import OK"
fi

echo "✅ Environment OK (paxect + paxect_core)"
