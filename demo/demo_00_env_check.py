#!/usr/bin/env python3
"""
PAXECT Core — Demo 00: Environment Sanity Check
International / Cross-OS Demo Suite

Purpose:
- Verifies that Python is installed and working.
- Verifies that paxect_core and paxect_core_plugin are importable.
- Prints Python version and plugin version (if available).
- Safe to run on Linux, macOS, Windows, Android (Termux), iOS (Pyto).
"""

import sys
import hashlib

print("==[ PAXECT Demo 00 — Environment Sanity Check ]==")

# Print Python version
print(f"[Step 1] Python version: {sys.version}")

# Try to import paxect_core
try:
    import paxect_core
    print("[Step 2] paxect_core imported successfully!")
    paxect_version = getattr(paxect_core, '__version__', 'unknown')
    print(f"[Step 3] paxect_core version: {paxect_version}")
except Exception as e:
    print("[ERROR] Could not import paxect_core!")
    print(e)
    sys.exit(1)

# Try to import paxect_core_plugin
try:
    import paxect_core_plugin
    print("[Step 4] paxect_core_plugin imported successfully!")
    plugin_version = getattr(paxect_core_plugin, '__version__', 'unknown')
    print(f"[Step 5] paxect_core_plugin version: {plugin_version}")
except Exception as e:
    print("[WARNING] Could not import paxect_core_plugin (optional).")
    print(e)

# Print hash of Python version string
python_ver_hash = hashlib.sha256(sys.version.encode()).hexdigest()
print(f"[Step 6] SHA-256 of Python version string: {python_ver_hash}")

# Done
print("==[ Environment check completed successfully ]==")
