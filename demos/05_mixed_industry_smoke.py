#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 05: Mixed Industry Smoke Test
#
# Purpose:
#   Stress-test the PAXECT Core container under mixed configurations.
#   Runs multiple encode/decode cycles with varying frame sizes, channels, and mappings.
#
# Usage:
#   python3 05_mixed_industry_smoke.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import random
import hashlib

print("[05] PAXECT Core — Mixed Industry Smoke Test\n")

SRC_FILE = "mix_input.bin"
DEC_FILE = "mix_output.bin"

CONFIGS = [
    {"channels": "1", "frame": "65536",    "mapping": "virtual", "level": "3"},
    {"channels": "2", "frame": "131072",   "mapping": "u16",     "level": "5"},
    {"channels": "4", "frame": "262144",   "mapping": "virtual", "level": "7"},
    {"channels": "auto", "frame": "524288","mapping": "u16",     "level": "9"},
]

def create_input():
    print("→ Generating 1 MB patterned input...")
    with open(SRC_FILE, "wb") as f:
        for i in range(1024 * 1024):
            f.write(bytes([(i * 37) % 256]))  # reproducible pattern

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_encode(cfg, out_file):
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", out_file,
        "--channels", cfg["channels"],
        "--frame", cfg["frame"],
        "--mapping", cfg["mapping"],
        "--level", cfg["level"],
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def run_decode(enc_file):
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", enc_file, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def test_cycle(cfg, idx):
    enc_name = f"mix_test_{idx}.freq"
    print(f"\n→ Test #{idx+1}: channels={cfg['channels']}, frame={cfg['frame']}, "
          f"mapping={cfg['mapping']}, level={cfg['level']}")
    enc = run_encode(cfg, enc_name)
    if enc.returncode != 0:
        print("   ❌ Encode failed:", enc.stderr.decode() or enc.stdout.decode())
        sys.exit(enc.returncode)

    dec = run_decode(enc_name)
    if dec.returncode != 0:
        print("   ❌ Decode failed:", dec.stderr.decode() or dec.stdout.decode())
        sys.exit(dec.returncode)

    # Verify hashes
    a = sha256sum(SRC_FILE)
    b = sha256sum(DEC_FILE)
    if a == b:
        print("   ✅ Roundtrip verified — hashes match.")
    else:
        print("   ❌ Hash mismatch!")
        sys.exit(2)

    # Optional deterministic consistency check
    h_enc = sha256sum(enc_name)
    print(f"   Container hash: {h_enc[:16]}…")

def cleanup():
    for f in os.listdir("."):
        if f.startswith("mix_test_") or f in [SRC_FILE, DEC_FILE]:
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()
        for i, cfg in enumerate(CONFIGS):
            test_cycle(cfg, i)
        print("\n[05] Mixed Industry Smoke Test completed successfully ✅\n")
    except KeyboardInterrupt:
        print("\n[05] Aborted by user.")
    finally:
        cleanup()
