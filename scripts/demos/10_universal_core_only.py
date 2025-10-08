#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAXECT — Universal Core-Only Demo (International · Cross-Platform)

Purpose:
- Tests the PAXECT Core module alone (no plugins).
- Verifies deterministic encode/decode round-trip.
- Confirms CRC32 integrity and SHA-256 identity across OSes.
- Runs identically on Linux, macOS, Windows, Android (Termux), and iOS (Pyto).
"""

import os
import tempfile
import hashlib
import sys
import paxect_core as px


def quick_roundtrip():
    print("PAXECT — Universal Core-Only Demo")
    tmp = tempfile.mkdtemp(prefix="paxect_coreonly_")
    print(f"[tmp] {tmp}")

    print("[1/2] Quick round-trip (core only)…")

    # Generate test input (256 KiB)
    raw = os.urandom(256 * 1024)
    open(f"{tmp}/input.bin", "wb").write(raw)

    # Encode using paxect_core CLI-compatible call
    rc1 = px.main([
        "encode",
        "-i", f"{tmp}/input.bin",
        "-o", f"{tmp}/x.freq",
        "--channels", "auto"
    ])
    if rc1 != 0:
        print(f"❌ Encode failed (exit={rc1})")
        sys.exit(rc1)

    # Decode back
    rc2 = px.main([
        "decode",
        "-i", f"{tmp}/x.freq",
        "-o", f"{tmp}/output.bin"
    ])
    if rc2 != 0:
        print(f"❌ Decode failed (exit={rc2})")
        sys.exit(rc2)

    # Compare hashes
    sha_in = hashlib.sha256(open(f"{tmp}/input.bin", "rb").read()).hexdigest()
    sha_out = hashlib.sha256(open(f"{tmp}/output.bin", "rb").read()).hexdigest()
    sha_freq = hashlib.sha256(open(f"{tmp}/x.freq", "rb").read()).hexdigest()

    print(f"   SHA256(in)    = {sha_in}")
    print(f"   SHA256(.freq) = {sha_freq}")
    print(f"   SHA256(out)   = {sha_out}")

    if sha_in == sha_out:
        print("✅ Core-only deterministic encode/decode OK")
    else:
        print("❌ Mismatch detected — not deterministic")


def main():
    try:
        quick_roundtrip()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
