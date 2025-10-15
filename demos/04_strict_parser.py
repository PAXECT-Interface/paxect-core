#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 04: Strict Parser Validation
#
# Purpose:
#   Validate error detection in container parsing.
#   Ensures integrity checks trigger correct exit codes on corrupted input.
#
# Usage:
#   python3 04_strict_parser.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib
import random

print("[04] PAXECT Core — Strict Parser Validation\n")

SRC_FILE = "strict_input.bin"
ENC_FILE = "strict_ok.freq"
CORRUPT_FILE = "strict_corrupt.freq"
DEC_FILE = "strict_out.bin"

def create_input():
    print("→ Creating test input...")
    with open(SRC_FILE, "wb") as f:
        f.write(os.urandom(512 * 1024))  # 512 KB random data

def run_encode():
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", ENC_FILE,
        "--channels", "1", "--frame", "65536",
        "--level", "5", "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def corrupt_container():
    print("→ Corrupting encoded container...")
    data = bytearray(open(ENC_FILE, "rb").read())
    pos = random.randint(32, len(data) - 64)
    data[pos] ^= 0xFF  # flip a random byte
    with open(CORRUPT_FILE, "wb") as f:
        f.write(data)
    print(f"   Corruption injected at byte offset {pos}")

def run_decode(file):
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", file, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_exitcode(proc, expected):
    if proc.returncode == expected:
        print(f"   ✅ Expected exit code {expected} confirmed.")
    else:
        print(f"   ❌ Unexpected exit code! Got {proc.returncode}, expected {expected}")
        sys.exit(4)

def cleanup():
    for f in [SRC_FILE, ENC_FILE, CORRUPT_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()

        print("→ Encoding baseline container...")
        enc = run_encode()
        if enc.returncode != 0:
            print(enc.stderr.decode() or enc.stdout.decode())
            sys.exit(enc.returncode)
        print("   ✅ Encoding completed OK")

        print("→ Decoding baseline to verify reference...")
        dec_ok = run_decode(ENC_FILE)
        verify_exitcode(dec_ok, 0)

        print("→ Creating corrupted copy for parser test...")
        corrupt_container()

        print("→ Decoding corrupted container...")
        dec_bad = run_decode(CORRUPT_FILE)
        if dec_bad.returncode in (2, 3, 4):
            print(f"   ✅ Parser correctly failed with code {dec_bad.returncode}")
        else:
            print(f"   ❌ Parser did not detect corruption (code {dec_bad.returncode})")
            sys.exit(4)

        print("\n[04] Strict Parser Validation completed successfully ✅\n")

    except KeyboardInterrupt:
        print("\n[04] Aborted by user.")
    finally:
        cleanup()
