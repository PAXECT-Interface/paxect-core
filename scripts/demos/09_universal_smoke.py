#!/usr/bin/env python3
"""
PAXECT — Universal Smoke Demo (Linux · macOS · Windows)
- Quick round-trip (bit-identical)
- Determinism: two encodes -> identical .freq SHA256

Requirements:
- Python 3.8+ (works on 3.12+ too)
- 'paxect' CLI available in PATH
"""
import hashlib, os, secrets, shutil, subprocess, sys, tempfile

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def size(path: str) -> int:
    return os.path.getsize(path)

def run_cli(argv, stdin_path, stdout_path):
    with open(stdin_path, "rb") as fin, open(stdout_path, "wb") as fout:
        proc = subprocess.run(argv, stdin=fin, stdout=fout)
        if proc.returncode != 0:
            raise RuntimeError(f"command failed: {' '.join(argv)} (rc={proc.returncode})")

def check_cli():
    exe = shutil.which("paxect")
    if not exe:
        print("❌ paxect CLI not found in PATH", file=sys.stderr)
        sys.exit(1)
    print(f"[env] paxect = {exe}")

def quick_roundtrip(tmpdir: str, kib: int = 256):
    print("[1/2] Quick round-trip…")
    inp = os.path.join(tmpdir, "in.bin")
    xfq = os.path.join(tmpdir, "x.freq")
    out = os.path.join(tmpdir, "out.bin")

    data = secrets.token_bytes(kib * 1024)
    with open(inp, "wb") as f: f.write(data)

    print(f"      in.bin  = {size(inp)} bytes")
    run_cli(["paxect", "encode"], inp, xfq)
    print(f"      x.freq  = {size(xfq)} bytes")
    run_cli(["paxect", "decode"], xfq, out)
    print(f"      out.bin = {size(out)} bytes")

    s_in, s_fr, s_out = sha256(inp), sha256(xfq), sha256(out)
    if s_in != s_out:
        raise SystemExit("❌ Mismatch — output differs from input")
    print("✅ Deterministic round-trip")
    print(f"   SHA256(in)    = {s_in}")
    print(f"   SHA256(.freq) = {s_fr}")
    print(f"   SHA256(out)   = {s_out}")

def determinism_double_encode(tmpdir: str, mib: int = 8):
    print("[2/2] Determinism: two encodes -> identical container hash…")
    inp = os.path.join(tmpdir, "in.bin")
    a = os.path.join(tmpdir, "a.freq")
    b = os.path.join(tmpdir, "b.freq")
    out = os.path.join(tmpdir, "out.bin")

    data = secrets.token_bytes(mib * 1024 * 1024)
    with open(inp, "wb") as f: f.write(data)

    run_cli(["paxect", "encode"], inp, a)
    run_cli(["paxect", "encode"], inp, b)
    shaA, shaB = sha256(a), sha256(b)
    print(f"      a.freq SHA256 = {shaA} (size={size(a)})")
    print(f"      b.freq SHA256 = {shaB} (size={size(b)})")

    if shaA != shaB:
        raise SystemExit("❌ Non-deterministic container hashes")

    run_cli(["paxect", "decode"], a, out)
    s_in, s_out = sha256(inp), sha256(out)
    if s_in != s_out:
        raise SystemExit("❌ Mismatch — output differs from input")
    print("✅ Deterministic containers match; bit-identical round-trip confirmed")

def main():
    print("PAXECT — Universal Smoke Demo (Linux · macOS · Windows)")
    check_cli()
    with tempfile.TemporaryDirectory() as tmp:
        print(f"[tmp] {tmp}")
        quick_roundtrip(tmp, kib=256)
        determinism_double_encode(tmp, mib=8)
    print("ℹ️ Done. Temporary files were cleaned up.")

if __name__ == "__main__":
    main()
