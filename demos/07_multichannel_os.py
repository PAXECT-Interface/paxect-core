#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 07: Multi-Channel OS Test
#
# Purpose:
#   Validate multi-channel encode/decode functionality across configurations.
#   Tests both manual (1–8) and auto mode, verifying throughput and consistency.
#
# Usage:
#   python3 07_multichannel_os.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib
import time

print("[07] PAXECT Core — Multi-Channel OS Test\n")

SRC_FILE = "multi_input.bin"
DEC_FILE = "multi_output.bin"

CHANNELS = [1, 2, 4, 6, 8, "auto"]

def create_input():
    print("→ Creating 4 MB deterministic input...")
    with open(SRC_FILE, "wb") as f:
        for i in range(4 * 1024 * 1024):
            f.write(bytes([(i * 19 + 5) % 256]))

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_and_time(cmd):
    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True)
    elapsed = time.perf_counter() - start
    return proc, elapsed

def run_encode(ch):
    enc_file = f"multi_{ch}.freq"
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", enc_file,
        "--channels", str(ch),
        "--frame", "1048576",
        "--mapping", "virtual",
        "--level", "5", "--verify"
    ]
    proc, t = run_and_time(cmd)
    return enc_file, proc, t

def run_decode(enc_file):
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", enc_file, "-o", DEC_FILE,
        "--verify"
    ]
    return subprocess.run(cmd, capture_output=True)

def test_channel(ch):
    print(f"\n→ Testing channel configuration: {ch}")
    enc_file, enc_proc, enc_time = run_encode(ch)
    if enc_proc.returncode != 0:
        print("   ❌ Encode failed:", enc_proc.stderr.decode() or enc_proc.stdout.decode())
        sys.exit(enc_proc.returncode)

    enc_size = os.path.getsize(enc_file)
    enc_speed = (4 * 1024 * 1024) / (1024 * 1024) / enc_time
    print(f"   ✅ Encoded {enc_size/1_048_576:.2f} MB in {enc_time:.2f}s ({enc_speed:.1f} MB/s)")

    dec_proc = run_decode(enc_file)
    if dec_proc.returncode != 0:
        print("   ❌ Decode failed:", dec_proc.stderr.decode() or dec_proc.stdout.decode())
        sys.exit(dec_proc.returncode)

    src_hash = sha256sum(SRC_FILE)
    dec_hash = sha256sum(DEC_FILE)
    if src_hash == dec_hash:
        print("   ✅ Roundtrip integrity verified.")
    else:
        print("   ❌ Hash mismatch!")
        sys.exit(2)

    os.remove(enc_file)
    os.remove(DEC_FILE)

def cleanup():
    if os.path.exists(SRC_FILE):
        os.remove(SRC_FILE)

if __name__ == "__main__":
    try:
        create_input()
        for ch in CHANNELS:
            test_channel(ch)
        print("\n[07] Multi-Channel OS Test completed successfully ✅\n")
    except KeyboardInterrupt:
        print("\n[07] Aborted by user.")
    finally:
        cleanup()
