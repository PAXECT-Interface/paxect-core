#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# PAXECT Core — Demo 10: Universal Core-Only Test (Stable)
#
# Purpose:
#   Validate core encode/decode using direct API calls, no subprocesses.
#   Includes in-memory BytesIO bridge that resists auto-closing.
# ------------------------------------------------------------------------------

import io
import os
import sys
import hashlib
import paxect_core

print("[10] PAXECT Core — Universal Core-Only Test\n")

SRC_FILE = "core_input.bin"
ENC_FILE = "core_output.freq"
DEC_FILE = "core_decoded.bin"


# --- helpers --------------------------------------------------------------

class NoClose(io.BytesIO):
    """BytesIO subclass that ignores close() to stay open after with-blocks."""
    def close(self):
        # override to prevent paxect_core from closing the stream
        pass


def create_input():
    print("→ Creating reproducible 512 KB input sample...")
    with open(SRC_FILE, "wb") as f:
        for i in range(512 * 1024):
            f.write(bytes([(i * 29 + 17) % 256]))


def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# --- API tests ------------------------------------------------------------

def encode_via_api():
    print("→ Encoding via direct API call...")
    args = paxect_core.parse_args([
        "encode", "-i", SRC_FILE, "-o", ENC_FILE,
        "--channels", "2", "--frame", "131072",
        "--level", "5", "--verify"
    ])
    rc = paxect_core.encode(args)
    if rc != 0:
        raise RuntimeError(f"Encode failed (exit={rc})")
    print("   ✅ Encode completed OK")


def decode_via_api():
    print("→ Decoding via direct API call...")
    args = paxect_core.parse_args([
        "decode", "-i", ENC_FILE, "-o", DEC_FILE, "--verify"
    ])
    rc = paxect_core.decode(args)
    if rc != 0:
        raise RuntimeError(f"Decode failed (exit={rc})")
    print("   ✅ Decode completed OK")


def verify_integrity():
    print("→ Verifying API roundtrip integrity...")
    a = sha256sum(SRC_FILE)
    b = sha256sum(DEC_FILE)
    if a == b:
        print("   ✅ Data verified — hashes match.")
    else:
        print("   ❌ Hash mismatch!")
        sys.exit(2)


def test_in_memory():
    print("→ In-memory stream test (BytesIO)...")
    data = bytes([(i * 3 + 5) % 256 for i in range(4096)])
    src = NoClose(data)     # stays open
    out = NoClose()         # stays open
    src.seek(0)

    paxect_core._open_in = lambda _: src
    paxect_core._open_out = lambda _: out

    args = paxect_core.parse_args([
        "encode", "-i", "-", "-o", "-", "--channels", "1",
        "--frame", "4096", "--level", "3"
    ])
    rc = paxect_core.encode(args)
    if rc != 0:
        raise RuntimeError("In-memory encode failed")

    encoded = out.getvalue()
    print(f"   Encoded {len(encoded)} bytes in-memory ✅")


def cleanup():
    for f in [SRC_FILE, ENC_FILE, DEC_FILE]:
        if os.path.exists(f):
            os.remove(f)


# --- main ----------------------------------------------------------------

if __name__ == "__main__":
    try:
        create_input()
        encode_via_api()
        decode_via_api()
        verify_integrity()
        test_in_memory()
        print("\n[10] Universal Core-Only Test completed successfully ✅\n")
    except KeyboardInterrupt:
        print("\n[10] Aborted by user.")
    except Exception as e:
        print("[10] ❌ Error:", e)
        sys.exit(1)
    finally:
        cleanup()
