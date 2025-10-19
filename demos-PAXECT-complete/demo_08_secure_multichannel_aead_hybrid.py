#!/usr/bin/env python3
"""
PAXECT Demo 08 – Secure Multi-Channel AEAD-Hybrid Bridge
--------------------------------------------------------
Adds hybrid key-wrap simulation to the AEAD multi-channel demo.
Shows both symmetric AEAD encryption and asymmetric key wrapping.
"""

import json, hashlib, base64, random, tempfile, time
from pathlib import Path

STATE = Path(tempfile.gettempdir()) / "paxect_demo_08_state.json"
CHANNELS = ["data", "control", "heartbeat"]

# --- Simulated hybrid keypair (deterministic for demo) ---
PRIVATE_KEY = hashlib.sha256(b"PAXECT-PRIVATE").digest()
PUBLIC_KEY  = hashlib.sha256(b"PAXECT-PUBLIC").digest()

def hybrid_wrap_key(sym_key: bytes) -> str:
    """Simulate public-key wrapping."""
    wrapped = bytes(a ^ b for a, b in zip(sym_key, PUBLIC_KEY))
    return base64.b64encode(wrapped).decode()

def hybrid_unwrap_key(wrapped_b64: str) -> bytes:
    """Simulate private-key unwrapping."""
    wrapped = base64.b64decode(wrapped_b64)
    unwrapped = bytes(a ^ b for a, b in zip(wrapped, PUBLIC_KEY))
    return unwrapped

def aead_encrypt(channel: str, plaintext: str, key: bytes):
    nonce = hashlib.sha256((channel + "nonce").encode()).digest()[:12]
    cipher = base64.b64encode(bytes(a ^ b for a, b in zip(plaintext.encode(), key*10))).decode()
    tag = hashlib.sha256((cipher + channel).encode()).hexdigest()[:16]
    return {"nonce": base64.b64encode(nonce).decode(), "cipher": cipher, "tag": tag}

def aead_decrypt(channel: str, packet: dict, key: bytes):
    check = hashlib.sha256((packet["cipher"] + channel).encode()).hexdigest()[:16]
    ok = check == packet["tag"]
    plain = bytes(a ^ b for a, b in zip(base64.b64decode(packet["cipher"]), key*10))
    return plain.decode(errors="ignore"), ok

def main():
    print("=== PAXECT Demo 08 – Secure Multi-Channel AEAD-Hybrid Bridge ===")
    state = json.loads(STATE.read_text()) if STATE.exists() else {"cycle":0,"epsilon":0.1}
    eps = state["epsilon"]
    mode = "exploit" if random.random() > eps else "explore"
    state["cycle"] += 1
    print(f"Cycle {state['cycle']} | mode={mode} | epsilon={eps}")

    results = []
    for ch in CHANNELS:
        # generate per-channel symmetric key
        sym_key = hashlib.sha256(f"{ch}-key-{state['cycle']}".encode()).digest()
        wrapped = hybrid_wrap_key(sym_key)
        unwrapped = hybrid_unwrap_key(wrapped)
        enc = aead_encrypt(ch, f"{ch}-payload-{state['cycle']}", unwrapped)
        dec, ok = aead_decrypt(ch, enc, unwrapped)
        match = dec == f"{ch}-payload-{state['cycle']}"
        results.append({
            "channel": ch,
            "wrapped_key_len": len(wrapped),
            "aead_ok": ok,
            "match": match
        })

    # update epsilon adaptively
    success = all(r["match"] for r in results)
    eps = round(max(0.05, eps*0.95) if success else min(0.5, eps+0.05),3)
    state["epsilon"] = eps
    STATE.write_text(json.dumps(state))

    digest = hashlib.sha256(json.dumps(results,sort_keys=True).encode()).hexdigest()[:12]
    summary = {
        "cycle": state["cycle"],
        "epsilon": eps,
        "mode": mode,
        "digest": digest,
        "channels": results,
        "status": "All hybrid channels synchronized ✅" if success else "Drift detected ❗"
    }
    print(json.dumps(summary, indent=2))
    print(f"\nState saved to: {STATE}")
    print("Hybrid key-wrap + AEAD integrity complete.\n")

if __name__ == "__main__":
    main()
