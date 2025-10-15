#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 08: Industry Bridge (Streaming Pipeline)
#
# Purpose:
#   Validate stdin/stdout streaming encode/decode.
#   Simulates an industrial data pipeline using PAXECT Core as a bridge.
#
# Usage:
#   python3 08_industry_bridge.py
# ------------------------------------------------------------------------------

import subprocess
import os
import sys
import hashlib

print("[08] PAXECT Core — Industry Bridge (Streaming Pipeline)\n")

SRC_FILE = "bridge_input.bin"
OUT_FILE = "bridge_output.bin"

def create_input():
    print("→ Creating 2 MB input sample...")
    with open(SRC_FILE, "wb") as f:
        for i in range(2 * 1024 * 1024):
            f.write(bytes([(i * 23 + 11) % 256]))

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_pipeline():
    print("→ Running encode → decode pipeline via stdin/stdout...")
    # The encoded stream is piped directly into decode using subprocess pipes
    enc = subprocess.Popen(
        [sys.executable, "paxect_core.py", "encode", "-i", "-", "-o", "-", "--channels", "2", "--frame", "131072", "--level", "4", "--verify"],
        stdin=open(SRC_FILE, "rb"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    dec = subprocess.Popen(
        [sys.executable, "paxect_core.py", "decode", "-i", "-", "-o", OUT_FILE, "--verify"],
        stdin=enc.stdout,
        stderr=subprocess.PIPE
    )
    enc.stdout.close()
    _, enc_err = enc.communicate()
    dec_out, dec_err = dec.communicate()

    if enc.returncode != 0:
        print("   ❌ Encode failed:", enc_err.decode())
        sys.exit(enc.returncode)
    if dec.returncode != 0:
        print("   ❌ Decode failed:", dec_err.decode())
        sys.exit(dec.returncode)

def verify():
    print("→ Verifying roundtrip integrity...")
    a = sha256sum(SRC_FILE)
    b = sha256sum(OUT_FILE)
    if a == b:
        print("   ✅ Streamed roundtrip verified — hashes match.")
    else:
        print("   ❌ Hash mismatch in pipeline data!")
        sys.exit(2)

def cleanup():
    for f in [SRC_FILE, OUT_FILE]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    try:
        create_input()
        run_pipeline()
        verify()
        print("\n[08] Industry Bridge (Streaming Pipeline) completed successfully ✅\n")
    except KeyboardInterrupt:
        print("\n[08] Aborted by user.")
    finally:
        cleanup()
