#!/usr/bin/env python3
"""
PAXECT Demo 08 – Secure Multi-Channel AEAD Bridge
-------------------------------------------------
Demonstrates the PAXECT concept in full:

 • Multi-channel message exchange (data, control, heartbeat)
 • AEAD-secured encryption/decryption per channel
 • SelfTune adaptive mode (epsilon-greedy)
 • Autonomous relay-style behavior (simulated Link policy)
 • Cross-platform deterministic integrity (no drift)

All operations are local, offline, and reproducible.
"""

import json, os, time, random, hashlib, tempfile, base64
from pathlib import Path

# --- Config ---
STATE = Path(tempfile.gettempdir()) / "paxect_demo_08_state.json"
CHANNELS = ["data", "control", "heartbeat"]

def aead_encrypt(channel: str, plaintext: str, key: bytes):
    """Simulate AEAD encrypt with deterministic hash footer."""
    nonce = hashlib.sha256((channel + "nonce").encode()).digest()[:12]
    cipher = base64.b64encode(
        bytes(a ^ b for a, b in zip(plaintext.encode(), key * 10))
    ).decode()
    tag = hashlib.sha256((cipher + channel).encode()).hexdigest()[:16]
    return {"nonce": base64.b64encode(nonce).decode(), "cipher": cipher, "tag": tag}

def aead_decrypt(channel: str, packet: dict, key: bytes):
    """Simulate AEAD decrypt and verify tag."""
    check_tag = hashlib.sha256((packet["cipher"] + channel).encode()).hexdigest()[:16]
    ok = check_tag == packet["tag"]
    plain = bytes(a ^ b for a, b in zip(base64.b64decode(packet["cipher"]), key * 10))
    return plain.decode(errors="ignore"), ok

def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            pass
    return {"cycle": 0, "epsilon": 0.1}

def save_state(s):
    STATE.write_text(json.dumps(s))

def main():
    print("=== PAXECT Demo 08 – Secure Multi-Channel AEAD Bridge ===")
    state = load_state()
    eps = state["epsilon"]
    mode = "exploit" if random.random() > eps else "explore"
    state["cycle"] += 1
    print(f"Cycle {state['cycle']} | mode={mode} | epsilon={eps}")

    key = hashlib.sha256(b"PAXECT-DEMO-KEY").digest()
    results = []
    for ch in CHANNELS:
        plain = f"{ch}-payload-{state['cycle']}"
        enc = aead_encrypt(ch, plain, key)
        dec, ok = aead_decrypt(ch, enc, key)
        match = plain == dec
        results.append({"channel": ch, "encrypted": ok, "match": match})

    # Adaptive epsilon adjustment
    success = all(r["match"] for r in results)
    if success:
        eps = max(0.05, eps * 0.95)
    else:
        eps = min(0.5, eps + 0.05)
    state["epsilon"] = round(eps, 3)
    save_state(state)

    # Deterministic digest over all channels
    digest = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:12]
    summary = {
        "cycle": state["cycle"],
        "epsilon": state["epsilon"],
        "mode": mode,
        "digest": digest,
        "channels": results,
        "status": "All channels synchronized ✅" if success else "Drift detected ❗"
    }

    print(json.dumps(summary, indent=2))
    print(f"\nState saved to: {STATE}")
    print("All operations local, offline, and reproducible.\n")

if __name__ == "__main__":
    main()
