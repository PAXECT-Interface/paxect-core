#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 01: Quickstart Smoke Test
#
# Purpose:
#   Run a minimal encode → decode → verify cycle using the PAXECT Core blueprint.
#   Confirms container creation, integrity validation, and return codes.
#
# Usage:
#   python3 01_quickstart_smoke.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib

print("[01] PAXECT Core — Quickstart Smoke Test\n")

SRC_FILE = "test_input.bin"
ENC_FILE = "test_output.freq"
DEC_FILE = "test_decoded.bin"

def create_sample_file():
    print("→ Creating sample input file...")
    with open(SRC_FILE, "wb") as f:
        f.write(os.urandom(256 * 1024))  # 256 KB random test data

def run_encode():
    print("→ Encoding sample file...")
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", ENC_FILE,
        "--channels", "1", "--frame", "65536",
        "--level", "3", "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def run_decode():
    print("→ Decoding back to raw data...")
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", ENC_FILE, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_roundtrip():
    print("→ Verifying integrity...")
    orig = sha256sum(SRC_FILE)
    decomp = sha256sum(DEC_FILE)
    if orig == decomp:
        print("   ✅ Roundtrip verified — hashes match.")
    else:
        print("   ❌ Hash mismatch!")
        print("     Original:", orig)
        print("     Decoded :", decomp)
        sys.exit(2)

def cleanup():
    for f in [SRC_FILE, ENC_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_sample_file()
        enc = run_encode()
        print("   Encode exit code:", enc.returncode)
        if enc.returncode != 0:
            print(enc.stderr.decode() or enc.stdout.decode())
            sys.exit(enc.returncode)

        dec = run_decode()
        print("   Decode exit code:", dec.returncode)
        if dec.returncode != 0:
            print(dec.stderr.decode() or dec.stdout.decode())
            sys.exit(dec.returncode)

        verify_roundtrip()
        print("\n[01] Quickstart Smoke Test completed successfully ✅\n")

    except KeyboardInterrupt:
        print("\n[01] Aborted by user.")
    finally:
        cleanup()
