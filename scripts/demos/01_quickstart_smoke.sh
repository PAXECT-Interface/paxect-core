#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Create temporary workspace…"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
echo "      TMP = $TMP"

echo "[2/5] Generate random test input (256 KiB)…"
dd if=/dev/urandom of="$TMP/in.bin" bs=256K count=1 status=none
printf "      in.bin size  = %s bytes\n" "$(stat -c '%s' "$TMP/in.bin")"

echo "[3/5] Encode → create .freq container using paxect encode…"
paxect encode < "$TMP/in.bin" > "$TMP/x.freq"
printf "      x.freq size  = %s bytes\n" "$(stat -c '%s' "$TMP/x.freq")"

echo "[4/5] Decode → restore original bytes from .freq…"
paxect decode < "$TMP/x.freq" > "$TMP/out.bin"
printf "      out.bin size = %s bytes\n" "$(stat -c '%s' "$TMP/out.bin")"

echo "[5/5] Verify determinism (bit-identical round-trip)…"
if cmp -s "$TMP/in.bin" "$TMP/out.bin"; then
  sha_in=$(sha256sum "$TMP/in.bin"  | awk '{print $1}')
  sha_fr=$(sha256sum "$TMP/x.freq"  | awk '{print $1}')
  sha_out=$(sha256sum "$TMP/out.bin" | awk '{print $1}')
  echo "✅ Deterministic round-trip verified"
  echo "   SHA256(in)    = $sha_in"
  echo "   SHA256(.freq) = $sha_fr"
  echo "   SHA256(out)   = $sha_out"
else
  echo "❌ Mismatch — output differs from input"
  exit 1
fi

echo "ℹ️ Done. Temporary files are automatically cleaned up."
