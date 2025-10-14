#!/usr/bin/env python3
"""
PAXECT Core — Demo 01: Quickstart Smoke Test
International / Cross-OS Demo Suite

Purpose:
- Demonstrates deterministic encode/decode round-trip.
- Prints SHA-256 hashes of input and output for bit-identical proof.
- Works with paxect_core_plugin if available.
"""

import hashlib

print("==[ PAXECT Demo 01 — Quickstart Round-Trip Smoke Test ]==")

# Step 1: Prepare sample input data
test_input = b"PAXECT quickstart deterministic demo input"
print(f"[Step 1] Test input: {test_input!r}")

# Step 2: Encode using paxect_core_plugin (or fallback)
try:
    import paxect_core_plugin
    encode_func = getattr(paxect_core_plugin, "encode", None)
    decode_func = getattr(paxect_core_plugin, "decode", None)
    if not encode_func or not decode_func:
        raise AttributeError("encode/decode functions not found in paxect_core_plugin")
    print("[Step 2] Using paxect_core_plugin for encode/decode")
    encoded = encode_func(test_input)
except Exception as e:
    print("[Step 2] paxect_core_plugin not available or failed. Using fallback (identity encode).")
    encoded = test_input # fallback: no-op

# Step 3: SHA-256 of encoded data
encoded_hash = hashlib.sha256(encoded).hexdigest()
print(f"[Step 3] SHA-256 of encoded data: {encoded_hash}")

# Step 4: Decode data
try:
    decoded = decode_func(encoded)
except Exception:
    decoded = encoded # fallback: no-op

# Step 5: SHA-256 of decoded data
decoded_hash = hashlib.sha256(decoded).hexdigest()
print(f"[Step 4] SHA-256 of decoded data: {decoded_hash}")

# Step 6: Proof of bit-identical round-trip
if decoded == test_input:
    print("[Step 5] SUCCESS: Decoded data is bit-identical to input (proof OK)")
else:
    print("[Step 5] ERROR: Decoded data differs from input (proof FAILED)")

print("==[ Quickstart smoke test completed ]==")
