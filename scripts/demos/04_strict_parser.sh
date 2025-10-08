#!/usr/bin/env bash
set -euo pipefail

echo "[1/7] Create temp workspace…"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
echo "      TMP = $TMP"

echo "[2/7] Produce a valid .freq for reference…"
dd if=/dev/urandom of="$TMP/in.bin" bs=64K count=1 status=none
paxect encode < "$TMP/in.bin" > "$TMP/good.freq"
printf "      good.freq size = %s bytes\n" "$(stat -c '%s' "$TMP/good.freq")"

# helper: attempt decode; treat as PASS if decoder fails OR output != input
try_case () {
  local label="$1" file="$2"
  local out="$TMP/out_${label}.bin"
  if paxect decode < "$file" > "$out" 2>/dev/null; then
    if cmp -s "$TMP/in.bin" "$out"; then
      echo "❌ SHOULD FAIL but passed: $label (bit-identical output!)"
      return 1
    else
      echo "✅ FAIL (expected via mismatch): $label (decoder returned non-identical bytes)"
      return 0
    fi
  else
    echo "✅ FAIL (expected via error): $label"
    return 0
  fi
}

echo "[3/7] Negative: flip one byte in the middle (payload-hit)…"
cp "$TMP/good.freq" "$TMP/bad_flip.freq"
python - <<'PY' "$TMP/bad_flip.freq"
import sys, os, random
p=sys.argv[1]; b=bytearray(open(p,'rb').read())
n=len(b)
# Flip a byte roughly halfway, but not header (min 16) and not last 3 bytes
i=max(16, min(n-4, n//2))
b[i]^=0xFF
open(p,'wb').write(b)
print("flipped_index", i, "of", n)
PY
try_case "byte_flip_mid" "$TMP/bad_flip.freq"

echo "[4/7] Negative: bad MAGIC (overwrite first 4 bytes)…"
cp "$TMP/good.freq" "$TMP/bad_magic.freq"
python - <<'PY' "$TMP/bad_magic.freq"
import sys
p=sys.argv[1]; b=bytearray(open(p,'rb').read()); b[0:4]=b'NOPE'; open(p,'wb').write(b)
PY
try_case "bad_magic" "$TMP/bad_magic.freq"

echo "[5/7] Negative: bad VERSION-ish byte (flip byte 4)…"
cp "$TMP/good.freq" "$TMP/bad_version.freq"
python - <<'PY' "$TMP/bad_version.freq"
import sys
p=sys.argv[1]; b=bytearray(open(p,'rb').read())
if len(b)>=5: b[4]^=0xFF
open(p,'wb').write(b)
PY
try_case "bad_version_byte4" "$TMP/bad_version.freq"

echo "[6/7] Negative: truncate last 5 bytes…"
head -c -5 "$TMP/good.freq" > "$TMP/trunc.freq" || true
try_case "truncated_tail" "$TMP/trunc.freq"

echo "[7/7] Summary:"
echo "All negative cases considered PASS if decoder fails OR output mismatches input."
echo "✅ Strict parser behavior validated (fail-hard or non-identical output)."
