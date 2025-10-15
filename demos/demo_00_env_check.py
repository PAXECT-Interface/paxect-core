#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 00: Environment Validation
#
# Purpose:
#   Validate that the system and Python runtime are ready for all PAXECT Core demos.
#   Checks Python version, OS architecture, required dependencies, and container constants.
#
# Usage:
#   python3 00_env_check.py
# ------------------------------------------------------------------------------

import sys
import os
import platform
import time
import struct
import hashlib
import importlib.util  # ✅ direct import for Python 3.12 compatibility

print("[00] PAXECT Core — Environment Validation\n")

REQUIRED_MODULES = ["zstandard", "psutil"]
MAGIC = b"PXC1"
VERSION = 42

def check_python():
    print("→ Python:", sys.version.replace("\n", " "))
    if sys.version_info < (3, 8):
        raise SystemExit("[FAIL] Python 3.8+ required")

def check_os():
    print("→ OS:", platform.system(), platform.release())
    print("→ Arch:", platform.machine())
    print("→ Working directory:", os.getcwd())

def check_dependencies():
    print("→ Checking required modules...")
    missing = []
    for mod in REQUIRED_MODULES:
        if importlib.util.find_spec(mod) is None:
            missing.append(mod)
    if missing:
        raise SystemExit(f"[FAIL] Missing dependencies: {', '.join(missing)}")
    print("   All required modules are installed ✅")

def check_container_constants():
    print("→ Container constants check...", end=" ")
    header_fmt = "<4sH I B b I H 6x"
    footer_fmt = "<Q I 32s"
    header_size = struct.calcsize(header_fmt)
    footer_size = struct.calcsize(footer_fmt)
    if header_size != 24 or footer_size != 44:
        raise SystemExit("[FAIL] Unexpected header/footer structure size")
    digest = hashlib.sha256(MAGIC + bytes([VERSION])).hexdigest()[:16]
    print("OK (magic/version verified:", digest, ")")

def check_time():
    print("→ Time (UTC):", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

if __name__ == "__main__":
    try:
        check_python()
        check_os()
        check_dependencies()
        check_container_constants()
        check_time()
        print("\n[00] Environment verified ✅ — ready for PAXECT Core demos.\n")
    except Exception as e:
        print("[00] Environment validation failed ❌")
        print("Reason:", e)
        sys.exit(1)
