#!/usr/bin/env bash
set -euo pipefail

echo "[1/6] Create temporary workspace…"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
echo "      TMP = $TMP"

echo "[2/6] Generate random test input (8 MiB)…"
dd if=/dev/urandom of="$TMP/in.bin" bs=1M count=8 status=none
printf "      in.bin size  = %s bytes\n" "$(stat -c '%s' "$TMP/in.bin")"

echo "[3/6] Encode attempt A…"
paxect encode < "$TMP/in.bin" > "$TMP/a.freq"
shaA="$(sha256sum "$TMP/a.freq" | awk '{print $1}')"
printf "      a.freq SHA256 = %s (size=%s)\n" "$shaA" "$(stat -c '%s' "$TMP/a.freq")"

echo "[4/6] Encode attempt B…"
paxect encode < "$TMP/in.bin" > "$TMP/b.freq"
shaB="$(sha256sum "$TMP/b.freq" | awk '{print $1}')"
printf "      b.freq SHA256 = %s (size=%s)\n" "$shaB" "$(stat -c '%s' "$TMP/b.freq")"

echo "[5/6] Compare container hashes (determinism)…"
if [ "$shaA" = "$shaB" ]; then
  echo "✅ Deterministic containers match"
else
  echo "❌ Container hash differs (non-deterministic)"; exit 1
fi

echo "[6/6] Decode and verify original bytes…"
paxect decode < "$TMP/a.freq" > "$TMP/out.bin"
if cmp -s "$TMP/in.bin" "$TMP/out.bin"; then
  sha_in="$(sha256sum "$TMP/in.bin"  | awk '{print $1}')"
  sha_out="$(sha256sum "$TMP/out.bin" | awk '{print $1}')"
  echo "✅ Bit-identical round-trip confirmed"
  echo "   SHA256(in)  = $sha_in"
  echo "   SHA256(out) = $sha_out"
else
  echo "❌ Mismatch — output differs from input"; exit 1
fi

echo "ℹ️ Done. Temporary files are cleaned up."
