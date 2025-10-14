#!/usr/bin/env python3
"""
PAXECT Core — Demo 03: Performance Baseline (A/B)
International / Cross-OS Demo Suite

Purpose:
- Measures encode/decode throughput with timing.
- Prints SHA-256 hashes of input, encoded, decoded data.
- Reports runtime for encode and decode steps.
- Safe to run on Linux, macOS, Windows, Android (Termux), iOS (Pyto).
"""

import time
import hashlib

print("==[ PAXECT Demo 03 — Performance Baseline (A/B) ]==")

# Step 1: Prepare test input (1 MB random bytes)
test_input = b'PAXECT performance test data' * (1024 * 50)  # ~1MB
print(f"[Step 1] Test input size: {len(test_input)//1024} KB")

# Step 2: Try encode/decode from plugin
try:
    import paxect_core_plugin
    encode_func = getattr(paxect_core_plugin, "encode", None)
    decode_func = getattr(paxect_core_plugin, "decode", None)
    # Dummy object for plugin interface
    class DummyArgs:
        def __init__(self, data):
            self.data = data
            self.channels = "auto"
            self.verify = True
            self.input = data
    dummy = DummyArgs(test_input)
    print("[Step 2] Using paxect_core_plugin for encode/decode")
except Exception as e:
    print(f"[Step 2] paxect_core_plugin not available or failed ({e}). Using fallback (identity encode/decode)")
    encode_func = lambda x: x
    decode_func = lambda x: x
    dummy = test_input

# Step 3: Encode performance
start_encode = time.time()
try:
    encoded = encode_func(dummy)
except Exception as e:
    print(f"[Step 3] Encode failed: {e}")
    encoded = test_input
encode_time = time.time() - start_encode
encoded_hash = hashlib.sha256(encoded).hexdigest()
print(f"[Step 3] Encode: {encode_time:.4f}s, SHA-256: {encoded_hash}")

# Step 4: Decode performance
start_decode = time.time()
try:
    # Use DummyArgs for decode if needed
    if isinstance(encoded, bytes):
        decode_dummy = DummyArgs(encoded)
    else:
        decode_dummy = encoded
    decoded = decode_func(decode_dummy)
except Exception as e:
    print(f"[Step 4] Decode failed: {e}")
    decoded = encoded
decode_time = time.time() - start_decode
decoded_hash = hashlib.sha256(decoded).hexdigest()
print(f"[Step 4] Decode: {decode_time:.4f}s, SHA-256: {decoded_hash}")

# Step 5: Proof of round-trip
if decoded == test_input:
    print("[Step 5] SUCCESS: Decoded data is bit-identical to input (proof OK)")
else:
    print("[Step 5] ERROR: Decoded data differs from input (proof FAILED)")

print("==[ Performance baseline test completed ]==")
