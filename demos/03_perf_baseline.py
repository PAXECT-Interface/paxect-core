#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 03: Performance Baseline
#
# Purpose:
#   Benchmark encode and decode throughput for the PAXECT Core container engine.
#   Reports MB/s for both directions on a reproducible dataset.
#
# Usage:
#   python3 03_perf_baseline.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import time
import hashlib

print("[03] PAXECT Core — Performance Baseline\n")

SRC_FILE = "perf_input.bin"
ENC_FILE = "perf_output.freq"
DEC_FILE = "perf_decoded.bin"

DATA_MB = 8  # size of sample file (in MB)

def create_input():
    print(f"→ Creating {DATA_MB} MB input file...")
    block = bytes([x % 256 for x in range(1024)])
    with open(SRC_FILE, "wb") as f:
        for _ in range(DATA_MB * 1024):  # MB * 1024 KB
            f.write(block)

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

def run_encode():
    print("→ Encoding...")
    cmd = [
        sys.executable, "paxect_core.py",
        "encode", "-i", SRC_FILE, "-o", ENC_FILE,
        "--channels", "auto", "--frame", "1048576",
        "--level", "5", "--verify"
    ]
    return run_and_time(cmd)

def run_decode():
    print("→ Decoding...")
    cmd = [
        sys.executable, "paxect_core.py",
        "decode", "-i", ENC_FILE, "-o", DEC_FILE,
        "--verify"
    ]
    return run_and_time(cmd)

def throughput(bytes_, seconds_):
    return (bytes_ / (1024 * 1024)) / seconds_ if seconds_ > 0 else 0

def verify():
    print("→ Verifying integrity...")
    a = sha256sum(SRC_FILE)
    b = sha256sum(DEC_FILE)
    if a == b:
        print("   ✅ Data verified — hashes match.")
    else:
        print("   ❌ Hash mismatch!")
        sys.exit(2)

def cleanup():
    for f in [SRC_FILE, ENC_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()

        enc_proc, enc_time = run_encode()
        if enc_proc.returncode != 0:
            print(enc_proc.stderr.decode() or enc_proc.stdout.decode())
            sys.exit(enc_proc.returncode)
        enc_size = os.path.getsize(ENC_FILE)
        print(f"   Encode: {enc_size/1_048_576:.2f} MB written in {enc_time:.2f}s "
              f"({throughput(DATA_MB*1024*1024, enc_time):.1f} MB/s)")

        dec_proc, dec_time = run_decode()
        if dec_proc.returncode != 0:
            print(dec_proc.stderr.decode() or dec_proc.stdout.decode())
            sys.exit(dec_proc.returncode)
        print(f"   Decode completed in {dec_time:.2f}s "
              f"({throughput(DATA_MB*1024*1024, dec_time):.1f} MB/s)")

        verify()
        print("\n[03] Performance Baseline completed successfully ✅\n")

    except KeyboardInterrupt:
        print("\n[03] Aborted by user.")
    finally:
        cleanup()
