#!/usr/bin/env bash
set -euo pipefail
# PAXECT — Soundwave Multi-Channel Demo (Cross-OS verification)
# This demo creates N independent channels, encodes each to its own .freq,
# verifies deterministic hashes locally, and prints clear cross-OS verify steps.

CHAN="${1:-4}"         # number of channels (e.g., 2/4/8)
SZ_MB="${2:-8}"        # MiB per channel payload (e.g., 8)
echo "[1/7] Setup…"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
echo "      TMP            = $TMP"
echo "      Channels       = $CHAN"
echo "      Size per chan  = ${SZ_MB} MiB"

echo "[2/7] Generate per-channel inputs…"
for i in $(seq 1 "$CHAN"); do
  dd if=/dev/urandom of="$TMP/in_ch${i}.bin" bs=1M count="$SZ_MB" status=none
done
ls -1 "$TMP"/in_ch*.bin | sed 's/^/      /'

echo "[3/7] Encode each channel → x_ch#.freq (deterministic)…"
for i in $(seq 1 "$CHAN"); do
  paxect encode < "$TMP/in_ch${i}.bin" > "$TMP/x_ch${i}.freq"
done

echo "[4/7] Compute .freq hashes (baseline on this OS)…"
for i in $(seq 1 "$CHAN"); do
  size=$(stat -c '%s' "$TMP/x_ch${i}.freq")
  sha=$(sha256sum "$TMP/x_ch${i}.freq" | awk '{print $1}')
  printf "      ch%-2d  size=%-10s  SHA256=%s\n" "$i" "$size" "$sha"
done

echo "[5/7] Decode and prove bit-identical per channel…"
ok=1
for i in $(seq 1 "$CHAN"); do
  paxect decode < "$TMP/x_ch${i}.freq" > "$TMP/out_ch${i}.bin"
  if cmp -s "$TMP/in_ch${i}.bin" "$TMP/out_ch${i}.bin"; then
    echo "      ✅ ch${i}: bit-identical"
  else
    echo "      ❌ ch${i}: mismatch"; ok=0
  fi
done
[ "$ok" -eq 1 ] || { echo "❌ Round-trip mismatch"; exit 1; }
echo "      All channels OK."

echo "[6/7] Cross-OS verification instructions"
cat <<'TXT'
--- Verify on Windows (PowerShell) ---
# For each channel file (x_ch1.freq, x_ch2.freq, …):
Get-FileHash .\x_ch1.freq -Algorithm SHA256
# The hash MUST match the one printed on OS-A.
# Then:
paxect decode < .\x_ch1.freq > .\out_ch1.bin
# (Optional) Compare with original if transferred.

--- Verify on macOS/Linux ---
# For each channel file:
shasum -a 256 x_ch1.freq
# The hash MUST match OS-A.
paxect decode < x_ch1.freq > out_ch1.bin
# Compare:
#   cmp -s in_ch1.bin out_ch1.bin && echo "byte-identical"
TXT

echo "[7/7] Summary"
echo "✅ Multi-channel deterministic containers produced and verified locally."
echo "✅ Use the printed SHA256 values to confirm identical containers across OS."
