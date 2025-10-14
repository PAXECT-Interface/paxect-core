#!/usr/bin/env python3
"""
PAXECT Core — Demo 04: Strict Parser Negative Tests
International / Cross-OS Demo Suite

Purpose:
- Tests plugin robustness against corruption, magic/version flip, truncation.
- Expects clean failure (exception or error message) — no crash.
- Prints progress, SHA-256, and outcomes.
"""

import hashlib

print("==[ PAXECT Demo 04 — Strict Parser Negative Tests ]==")

# Step 1: Prepare valid input and corrupted variants
valid_input = b"PAXECT strict parser test data"
corrupted_input = b"xxxxxx" + valid_input[6:]  # Corrupt MAGIC
version_flipped = b"PAXECTv2" + valid_input[8:]  # Version flip
truncated_input = valid_input[:10]  # Truncated file

print(f"[Step 1] Valid input SHA-256: {hashlib.sha256(valid_input).hexdigest()}")
print(f"[Step 1] Corrupted MAGIC SHA-256: {hashlib.sha256(corrupted_input).hexdigest()}")
print(f"[Step 1] Version flip SHA-256: {hashlib.sha256(version_flipped).hexdigest()}")
print(f"[Step 1] Truncated input SHA-256: {hashlib.sha256(truncated_input).hexdigest()}")

# Step 2: Setup decode function and dummy args
try:
    import paxect_core_plugin
    decode_func = getattr(paxect_core_plugin, "decode", None)
    class DummyArgs:
        def __init__(self, data):
            self.data = data
            self.input = data
            self.channels = "auto"
            self.verify = True
    print("[Step 2] Using paxect_core_plugin for decode")
except Exception as e:
    print(f"[Step 2] paxect_core_plugin not available ({e}). Using fallback (identity decode)")
    decode_func = lambda x: x.data if hasattr(x, "data") else x
    DummyArgs = lambda data: data

# Step 3: Negative test — Corrupted MAGIC
try:
    result = decode_func(DummyArgs(corrupted_input))
    print("[Step 3] ERROR: Corrupted MAGIC decoded successfully (should fail)")
except Exception as e:
    print(f"[Step 3] SUCCESS: Corrupted MAGIC failed as expected ({e})")

# Step 4: Negative test — Version flip
try:
    result = decode_func(DummyArgs(version_flipped))
    print("[Step 4] ERROR: Version flip decoded successfully (should fail)")
except Exception as e:
    print(f"[Step 4] SUCCESS: Version flip failed as expected ({e})")

# Step 5: Negative test — Truncated input
try:
    result = decode_func(DummyArgs(truncated_input))
    print("[Step 5] ERROR: Truncated input decoded successfully (should fail)")
except Exception as e:
    print(f"[Step 5] SUCCESS: Truncated input failed as expected ({e})")

print("==[ Strict parser negative tests completed ]==")
