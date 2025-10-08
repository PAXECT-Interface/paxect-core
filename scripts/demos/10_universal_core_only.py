#!/usr/bin/env python3
"""
PAXECT — Universal Core-Only Demo (Linux · macOS · Windows · Android · iOS)
Adapts to different paxect_core Python APIs. No 'paxect' CLI required.

Proofs:
- Quick round-trip (bit-identical)
- Determinism: two encodes -> identical container SHA-256
"""
import hashlib, secrets, tempfile, sys, os, inspect
from types import SimpleNamespace as NS

# 1) Import Python binding
try:
    import paxect_core as px
except Exception as e:
    print("❌ Could not import paxect_core:", e, file=sys.stderr)
    sys.exit(1)

def DBG(*a):
    if os.environ.get("PAXECT_DEBUG") == "1":
        print(*a)

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

# 2) ArgProxy: levert gevraagde velden on-the-fly
class ArgProxy:
    """
    Levert:
      - channels / n_channels → 'auto' (of 1 indien numeriek gevraagd)
      - flags/mode/version/container_version → veilige defaults
      - alles wat lijkt op bytes/data/buf/raw/input → payload
      - overige velden → None
    """
    def __init__(self, payload: bytes):
        self._payload = payload
    def __getattr__(self, name: str):
        low = name.lower()
        if low in ("channels",):
            return "auto"
        if low in ("n_channels", "nchannels"):
            return 1
        if low in ("flags","mode","version"):
            return 0
        if low in ("container_version", "containerver", "ver"):
            return 42
        # alle varianten die naar bytes kunnen verwijzen
        bytey = ("data","in_bytes","raw","bytes","payload","buffer","buf","input")
        if low in bytey or "byte" in low or "buf" in low or low.startswith("in_"):
            return self._payload
        return None

def _encode_via_variants(raw: bytes) -> bytes:
    last = None

    # 0) encode_bytes(bytes)?
    if hasattr(px, "encode_bytes"):
        try:
            DBG("[encode] encode_bytes(bytes)")
            return px.encode_bytes(raw)
        except Exception as e:
            DBG("[encode] encode_bytes failed:", type(e).__name__, e)
            last = e

    # 1) encode(ArgProxy)
    try:
        DBG("[encode] encode(ArgProxy)")
        return px.encode(ArgProxy(raw))
    except Exception as e:
        DBG("[encode] encode(ArgProxy) failed:", type(e).__name__, e)
        last = e

    # 2) Keyword-naam afleiden uit signature (args/obj/request/options/cfg/etc.)
    try:
        sig = inspect.signature(px.encode)
        param_names = [p.name for p in sig.parameters.values() if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
    except Exception:
        param_names = []
    # voorkeurs-volgorde
    preferred = ["args","obj","request","options","cfg","config","params","a","x"]
    ordered = preferred + [n for n in param_names if n not in preferred and n not in ("self",)]
    tried = set()
    for pname in ordered:
        if not pname or pname in tried: 
            continue
        tried.add(pname)
        try:
            DBG(f"[encode] encode({pname}=ArgProxy)")
            return px.encode(**{pname: ArgProxy(raw)})
        except Exception as e:
            DBG(f"[encode] encode({pname}=ArgProxy) failed:", type(e).__name__, e)
            last = e

    # 3) Fallback: encode(SimpleNamespace) met brede set velden
    ns_all = NS(channels="auto", flags=0,
                data=raw, in_bytes=raw, raw=raw, bytes=raw,
                payload=raw, buffer=raw, buf=raw, input=raw,
                n_channels=1, mode=0, version=0, container_version=42)
    try:
        DBG("[encode] encode(NS all-payload)")
        return px.encode(ns_all)
    except Exception as e:
        DBG("[encode] encode(NS all-payload) failed:", type(e).__name__, e)
        last = e

    # 4) Laatste kans: encode(bytes)
    try:
        DBG("[encode] encode(bytes)")
        return px.encode(raw)
    except Exception as e:
        DBG("[encode] encode(bytes) failed:", type(e).__name__, e)
        last = e

    raise RuntimeError(f"encode failed across patterns: {type(last).__name__}: {last}")

def _decode_via_variants(freq: bytes) -> bytes:
    last = None

    if hasattr(px, "decode_bytes"):
        try:
            DBG("[decode] decode_bytes(bytes)")
            return px.decode_bytes(freq)
        except Exception as e:
            DBG("[decode] decode_bytes failed:", type(e).__name__, e)
            last = e

    try:
        DBG("[decode] decode(ArgProxy)")
        return px.decode(ArgProxy(freq))
    except Exception as e:
        DBG("[decode] decode(ArgProxy) failed:", type(e).__name__, e)
        last = e

    try:
        sig = inspect.signature(px.decode)
        param_names = [p.name for p in sig.parameters.values() if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
    except Exception:
        param_names = []
    preferred = ["args","obj","request","options","cfg","config","params","a","x"]
    ordered = preferred + [n for n in param_names if n not in preferred and n not in ("self",)]
    tried = set()
    for pname in ordered:
        if not pname or pname in tried:
            continue
        tried.add(pname)
        try:
            DBG(f"[decode] decode({pname}=ArgProxy)")
            return px.decode(**{pname: ArgProxy(freq)})
        except Exception as e:
            DBG(f"[decode] decode({pname}=ArgProxy) failed:", type(e).__name__, e)
            last = e

    ns_all = NS(channels="auto", flags=0,
                data=freq, in_bytes=freq, raw=freq, bytes=freq,
                payload=freq, buffer=freq, buf=freq, input=freq,
                n_channels=1, mode=0, version=0, container_version=42)
    try:
        DBG("[decode] decode(NS all-payload)")
        return px.decode(ns_all)
    except Exception as e:
        DBG("[decode] decode(NS all-payload) failed:", type(e).__name__, e)
        last = e

    try:
        DBG("[decode] decode(bytes)")
        return px.decode(freq)
    except Exception as e:
        DBG("[decode] decode(bytes) failed:", type(e).__name__, e)
        last = e

    raise RuntimeError(f"decode failed across patterns: {type(last).__name__}: {last}")

def quick_roundtrip():
    print("[1/2] Quick round-trip (core only)…")
    raw = secrets.token_bytes(256 * 1024)  # 256 KiB
    freq = _encode_via_variants(raw)
    out  = _decode_via_variants(freq)
    if raw != out:
        sys.exit("❌ Mismatch — output differs from input")
    print("✅ Deterministic round-trip")
    print("   SHA256(in)    =", sha256_bytes(raw))
    print("   SHA256(.freq) =", sha256_bytes(freq))
    print("   SHA256(out)   =", sha256_bytes(out))

def determinism_double_encode():
    print("[2/2] Determinism: two encodes -> identical container hash…")
    raw = secrets.token_bytes(4 * 1024 * 1024)  # 4 MiB
    a = _encode_via_variants(raw)
    b = _encode_via_variants(raw)
    shaA = sha256_bytes(a)
    shaB = sha256_bytes(b)
    print("      a.freq SHA256 =", shaA, f"(size={len(a)})")
    print("      b.freq SHA256 =", shaB, f"(size={len(b)})")
    if shaA != shaB:
        sys.exit("❌ Non-deterministic container hashes")
    out = _decode_via_variants(a)
    if out != raw:
        sys.exit("❌ Mismatch after decode")
    print("✅ Deterministic containers match; bit-identical round-trip confirmed")

def main():
    print("PAXECT — Universal Core-Only Demo")
    with tempfile.TemporaryDirectory() as tmp:
        print(f"[tmp] {tmp}")
        quick_roundtrip()
        determinism_double_encode()
    print("ℹ️ Done. No CLI required; works anywhere Python can import paxect_core.")

if __name__ == "__main__":
    main()
