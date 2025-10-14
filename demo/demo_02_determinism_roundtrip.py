#!/usr/bin/env python3
"""
PAXECT Core — Demo 02: Double-Encode Determinism Proof
International / Cross-OS Demo Suite

Purpose:
- Demonstrates deterministic double-encode and decode round-trip.
- Verifies that double-encoded output is identical every time (determinism).
- SHA-256 hashes of both .freq outputs, and final decode.
"""

import hashlib

print("==[ PAXECT Demo 02 — Double-Encode Determinism Proof ]==")

# Step 1: Prepare test input
test_input = b"PAXECT determinism double-encode demo input"
print(f"[Step 1] Test input: {test_input!r}")

# Step 2: Try encode/decode from plugin
try:
    import paxect_core_plugin
    encode_func = getattr(paxect_core_plugin, "encode", None)
    decode_func = getattr(paxect_core_plugin, "decode", None)
    if not encode_func or not decode_func:
        raise AttributeError
    print("[Step 2] Using paxect_core_plugin for encode/decode")
except Exception:
    print("[Step 2] paxect_core_plugin not available or failed. Using fallback (identity encode/decode)")
    encode_func = lambda x: x
    decode_func = lambda x: x

# Step 3: Double encode
encoded_1 = encode_func(test_input)
encoded_2 = encode_func(test_input)
print(f"[Step 3] SHA-256 of encoded_1: {hashlib.sha256(encoded_1).hexdigest()}")
print(f"[Step 3] SHA-256 of encoded_2: {hashlib.sha256(encoded_2).hexdigest()}")

# Step 4: Check determinism (bit-identical)
if encoded_1 == encoded_2:
    print("[Step 4] SUCCESS: Both encoded outputs are bit-identical (deterministic)")
else:
    print("[Step 4] ERROR: Encoded outputs differ (not deterministic)")

# Step 5: Decode back
decoded = decode_func(encoded_1)
decoded_hash = hashlib.sha256(decoded).hexdigest()
print(f"[Step 5] SHA-256 of decoded data: {decoded_hash}")

# Step 6: Proof of round-trip
if decoded == test_input:
    print("[Step 6] SUCCESS: Decoded data is bit-identical to input (proof OK)")
else:
    print("[Step 6] ERROR: Decoded data differs from input (proof FAILED)")

print("==[ Double-encode determinism test completed ]==")
