#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Demo 00 - Environment Check
Verifies Python version, repository layout, and module importability
for PAXECT Core Plugin. Fully deterministic - no network or randomness.
"""

import os
import sys
import hashlib
import importlib.util

print("[PAXECT Demo 00] Environment Check")
print("-" * 60)

# ---- Python version ----
print(f"Python version: {sys.version.split()[0]}")
if sys.version_info < (3, 8):
    print("[Error] Python 3.8 or higher required.")
    sys.exit(1)

# ---- Auto-locate project root ----
script_dir = os.path.abspath(os.path.dirname(__file__))
top_candidates = [
    script_dir,                            # current dir
    os.path.abspath(os.path.join(script_dir, os.pardir)),  # parent
    os.getcwd(),                           # working dir
]
found = None
for path in top_candidates:
    if all(os.path.exists(os.path.join(path, f)) for f in ["paxect_core.py", "paxect_core_plugin.py"]):
        found = path
        break

if not found:
    print("[Error] Could not locate paxect_core.py and paxect_core_plugin.py in expected locations.")
    sys.exit(1)

print(f"Project root: {found}")

# ---- Plugin SHA-256 ----
plugin_path = os.path.join(found, "paxect_core_plugin.py")
with open(plugin_path, "rb") as f:
    data = f.read()
sha256 = hashlib.sha256(data).hexdigest()
print(f"paxect_core_plugin.py SHA-256: {sha256}")

# ---- Import check ----
sys.path.insert(0, found)
for mod in ("paxect_core_plugin", "paxect_core"):
    try:
        importlib.import_module(mod)
        print(f"[OK] Module {mod} imported successfully.")
    except Exception as e:
        print(f"[Error] Could not import {mod}: {e}")
        sys.exit(1)

print("\n✅ Environment check passed - system ready for PAXECT Core Demos.")
