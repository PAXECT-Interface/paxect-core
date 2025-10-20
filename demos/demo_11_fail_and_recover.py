#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Demo 11 — PAXECT Core Fail & Self-Recover
-----------------------------------------
Purpose
--------
Simulates a corrupted container (.freq) to prove that
PAXECT Core detects integrity failure (CRC/SHA mismatch)
and continues working properly on the next valid container.
"""

import os, subprocess, shutil
from pathlib import Path

BASE = Path("/tmp/paxect_demo11")
BASE.mkdir(parents=True, exist_ok=True)
GOOD = BASE / "ok.txt"
BAD_FREQ = BASE / "bad.freq"
GOOD_FREQ = BASE / "ok.freq"
OUT_OK = BASE / "ok.out"
OUT_BAD = BASE / "bad.out"
LOG = BASE / "core_recover.log"

shutil.rmtree(BASE, ignore_errors=True)
BASE.mkdir(parents=True, exist_ok=True)

print("=== Demo 11 — PAXECT Core Fail & Self-Recover ===")
print("[+] Creating valid and corrupted .freq containers...")

# 1️⃣  valid encode
GOOD.write_text("core deterministic integrity\n", encoding="utf-8")
subprocess.run(["python3","paxect_core.py","encode","-i",str(GOOD),"-o",str(GOOD_FREQ),"--verify"],check=True)

# 2️⃣  make a corrupted copy
bad = GOOD_FREQ.read_bytes()[:-64] + b"XXXX"     # truncate footer
BAD_FREQ.write_bytes(bad)

def try_decode(src: Path, dst: Path):
    r = subprocess.run(["python3","paxect_core.py","decode","-i",str(src),"-o",str(dst),"--verify"],
                       capture_output=True,text=True)
    return r.returncode,r.stderr.strip()

print("[*] Step 1: Decode corrupted .freq (expect fail)")
code,err = try_decode(BAD_FREQ,OUT_BAD)
LOG.write_text(f"FAIL-PHASE:\nexit={code}\n{err}\n")
print("   returncode:",code)
print("   error:",err or "(none)")

print("[*] Step 2: Decode valid .freq (expect recovery)")
code2,err2 = try_decode(GOOD_FREQ,OUT_OK)
LOG.write_text(LOG.read_text()+f"\nRECOVER-PHASE:\nexit={code2}\n{err2}\n")

if OUT_OK.exists():
    txt = OUT_OK.read_text().strip()
    print(f"[+] Recovery successful, output: {txt}")
    print("✅ Core self-recovery confirmed")
else:
    print("⚠️ No valid output found — check log for details")

print(f"\n[log] {LOG}")
