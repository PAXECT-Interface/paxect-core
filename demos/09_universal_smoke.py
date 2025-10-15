#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 09: Universal Smoke Test
#
# Purpose:
#   Full regression smoke: encode/decode determinism, corruption handling,
#   multi-channel verification, and streaming pipeline validation.
#
# Usage:
#   python3 09_universal_smoke.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib
import random

print("[09] PAXECT Core — Universal Smoke Test\n")

SRC_FILE = "universal_input.bin"
ENC_FILE = "universal_output.freq"
DEC_FILE = "universal_decoded.bin"

def create_input():
    print("→ Creating 1 MB reproducible input sample...")
    with open(SRC_FILE, "wb") as f:
        for i in range(1024 * 1024):
            f.write(bytes([(i * 7 + 13) % 256]))

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_encode(ch="auto", level="5"):
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", ENC_FILE,
        "--channels", str(ch), "--frame", "131072",
        "--level", str(level), "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def run_decode(input_file=ENC_FILE):
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", input_file, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def verify_integrity():
    a = sha256sum(SRC_FILE)
    b = sha256sum(DEC_FILE)
    if a == b:
        print("   ✅ Roundtrip verified — hashes match.")
    else:
        print("   ❌ Hash mismatch!"); sys.exit(2)

def test_determinism():
    print("→ Determinism check...")
    run_encode("2", "4")
    h1 = sha256sum(ENC_FILE)
    os.remove(ENC_FILE)
    run_encode("2", "4")
    h2 = sha256sum(ENC_FILE)
    if h1 == h2:
        print("   ✅ Deterministic encode confirmed.")
    else:
        print("   ❌ Non-deterministic container detected!")
        sys.exit(4)

def test_corruption():
    print("→ Corruption handling check...")
    data = bytearray(open(ENC_FILE, "rb").read())
    flip = random.randint(32, len(data) - 128)
    data[flip] ^= 0xFF
    bad_file = "universal_corrupt.freq"
    with open(bad_file, "wb") as f:
        f.write(data)
    dec = run_decode(bad_file)
    if dec.returncode in (2, 3, 4):
        print(f"   ✅ Corruption correctly detected (exit={dec.returncode}).")
    else:
        print(f"   ❌ Corruption not detected (exit={dec.returncode})!")
        sys.exit(4)
    os.remove(bad_file)

def test_streaming():
    print("→ Streaming pipeline verification...")
    cmd_enc = [
        sys.executable, "paxect_core.py",
        "encode", "-i", "-", "-o", "-", "--channels", "auto",
        "--frame", "65536", "--level", "5", "--verify"
    ]
    cmd_dec = [
        sys.executable, "paxect_core.py",
        "decode", "-i", "-", "-o", DEC_FILE, "--verify"
    ]
    enc = subprocess.Popen(cmd_enc, stdin=open(SRC_FILE, "rb"), stdout=subprocess.PIPE)
    dec = subprocess.Popen(cmd_dec, stdin=enc.stdout, stdout=subprocess.PIPE)
    enc.stdout.close()
    dec.wait()
    if dec.returncode == 0:
        print("   ✅ Streamed encode/decode pipeline OK.")
    else:
        print("   ❌ Streaming pipeline failed!"); sys.exit(3)

def cleanup():
    for f in [SRC_FILE, ENC_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()
        print("→ Encoding baseline container...")
        enc = run_encode()
        if enc.returncode != 0:
            print(enc.stderr.decode() or enc.stdout.decode()); sys.exit(enc.returncode)
        print("   ✅ Encode OK")

        print("→ Decoding baseline container...")
        dec = run_decode()
        if dec.returncode != 0:
            print(dec.stderr.decode() or dec.stdout.decode()); sys.exit(dec.returncode)
        verify_integrity()

        test_determinism()
        test_corruption()
        test_streaming()

        print("\n[09] Universal Smoke Test completed successfully ✅\n")
    except KeyboardInterrupt:
        print("\n[09] Aborted by user.")
    finally:
        cleanup()
