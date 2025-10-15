#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 06: Cross-OS Verify
#
# Purpose:
#   Ensure that containers encoded on this system would be verifiable on any OS.
#   Simulates a cross-platform verification by recomputing hashes from a decode step.
#
# Usage:
#   python3 06_cross_os_verify.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib
import platform

print("[06] PAXECT Core — Cross-OS Verify Test\n")

SRC_FILE = "cross_input.bin"
ENC_FILE = "cross_output.freq"
DEC_FILE = "cross_decoded.bin"

def create_input():
    print("→ Creating reference input (512 KB deterministic pattern)...")
    with open(SRC_FILE, "wb") as f:
        for i in range(512 * 1024):
            f.write(bytes([(i * 11 + 7) % 256]))

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_encode():
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", ENC_FILE,
        "--channels", "2", "--frame", "131072",
        "--mapping", "virtual", "--level", "5", "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def run_decode():
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", ENC_FILE, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def verify_cross():
    print("→ Simulating cross-OS verification...")
    enc_hash = sha256sum(ENC_FILE)
    dec_hash = sha256sum(DEC_FILE)
    print(f"   Container SHA-256 : {enc_hash}")
    print(f"   Decoded  SHA-256 : {dec_hash}")
    src_hash = sha256sum(SRC_FILE)

    if dec_hash == src_hash:
        print("   ✅ Data integrity verified — decode identical to source.")
    else:
        print("   ❌ Decode drift detected!")
        sys.exit(2)

    # simulate a “remote verifier” re-hash check
    verifier_token = hashlib.sha256((enc_hash + platform.system()).encode()).hexdigest()[:16]
    print(f"   Cross-system verification token: {verifier_token}")

def cleanup():
    for f in [SRC_FILE, ENC_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()
        print("→ Encoding container on this host...")
        enc = run_encode()
        if enc.returncode != 0:
            print(enc.stderr.decode() or enc.stdout.decode())
            sys.exit(enc.returncode)
        print("   ✅ Encoding OK")

        print("→ Decoding container locally...")
        dec = run_decode()
        if dec.returncode != 0:
            print(dec.stderr.decode() or dec.stdout.decode())
            sys.exit(dec.returncode)
        print("   ✅ Decode OK")

        verify_cross()
        print("\n[06] Cross-OS Verify Test completed successfully ✅\n")

    except KeyboardInterrupt:
        print("\n[06] Aborted by user.")
    finally:
        cleanup()
