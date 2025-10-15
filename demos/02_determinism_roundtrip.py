#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 02: Determinism Roundtrip Test
#
# Purpose:
#   Verify deterministic encoding: identical input produces identical containers.
#   Confirms reproducible encode/decode integrity for CI/CD environments.
#
# Usage:
#   python3 02_determinism_roundtrip.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib

print("[02] PAXECT Core — Determinism Roundtrip Test\n")

SRC_FILE = "det_input.bin"
ENC1_FILE = "det_output_1.freq"
ENC2_FILE = "det_output_2.freq"
DEC_FILE = "det_decoded.bin"

def create_input():
    print("→ Creating deterministic input file...")
    with open(SRC_FILE, "wb") as f:
        # Fixed seed pattern for reproducibility
        for i in range(1024 * 128):  # 128 KB
            f.write(bytes([i % 256]))

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_encode(outfile):
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", outfile,
        "--channels", "1", "--frame", "65536",
        "--level", "5", "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def run_decode():
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", ENC1_FILE, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def verify_determinism():
    print("→ Comparing container hashes...")
    h1 = sha256sum(ENC1_FILE)
    h2 = sha256sum(ENC2_FILE)
    print("   hash #1:", h1)
    print("   hash #2:", h2)
    if h1 == h2:
        print("   ✅ Deterministic output confirmed.")
    else:
        print("   ❌ Non-deterministic container output!")
        sys.exit(4)

def verify_roundtrip():
    print("→ Verifying decoded integrity...")
    orig = sha256sum(SRC_FILE)
    decomp = sha256sum(DEC_FILE)
    if orig == decomp:
        print("   ✅ Roundtrip verified — hashes match.")
    else:
        print("   ❌ Hash mismatch between input and decoded data.")
        sys.exit(2)

def cleanup():
    for f in [SRC_FILE, ENC1_FILE, ENC2_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()
        print("→ Encoding first container...")
        e1 = run_encode(ENC1_FILE)
        if e1.returncode != 0:
            print(e1.stderr.decode() or e1.stdout.decode())
            sys.exit(e1.returncode)

        print("→ Encoding second container...")
        e2 = run_encode(ENC2_FILE)
        if e2.returncode != 0:
            print(e2.stderr.decode() or e2.stdout.decode())
            sys.exit(e2.returncode)

        verify_determinism()

        print("→ Decoding first container...")
        d = run_decode()
        if d.returncode != 0:
            print(d.stderr.decode() or d.stdout.decode())
            sys.exit(d.returncode)

        verify_roundtrip()

        print("\n[02] Determinism Roundtrip Test completed successfully ✅\n")

    except KeyboardInterrupt:
        print("\n[02] Aborted by user.")
    finally:
        cleanup()
