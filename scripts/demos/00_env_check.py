#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAXECT Core Demo 00 — Environment Check
Cross-platform validation for Linux, macOS, Windows, Android (Termux), and iOS (Pyto)
"""

import sys
import platform

print("PAXECT — Demo 00: Environment Check\n")

try:
    import paxect_core
    print("paxect_core module import: OK")
except ImportError:
    print("paxect_core module import: FAILED")
    sys.exit(1)

print(f"Python version : {sys.version.split()[0]}")
print(f"Operating system: {platform.system()} ({platform.machine()})")

print("\nEnvironment verification: SUCCESS")
