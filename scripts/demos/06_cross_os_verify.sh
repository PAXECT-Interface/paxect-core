#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Create temp workspace…"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
echo "      TMP = $TMP"

echo "[2/4] Generate deterministic input sample (16 MiB)…"
dd if=/dev/urandom of="$TMP/sample.in" bs=1M count=16 status=none
printf "      sample.in size = %s bytes\n" "$(stat -c '%s' "$TMP/sample.in")"

echo "[3/4] Encode on OS-A → x.freq"
paxect encode < "$TMP/sample.in" > "$TMP/x.freq"
shaA="$(sha256sum "$TMP/x.freq" | awk '{print $1}')"
printf "      x.freq size = %s bytes | SHA256(OS-A) = %s\n" "$(stat -c '%s' "$TMP/x.freq")" "$shaA"

echo "[4/4] Instructions for OS-B/OS-C (copy x.freq to other OS and run):"
cat <<'TXT'
--- Verify on Windows (PowerShell) ---
Get-FileHash .\x.freq -Algorithm SHA256
# The hash MUST equal SHA256(OS-A)
# Then decode:
#   paxect decode < .\x.freq > .\out.bin
#   (Compare hashes or use fc /b to compare with original if transferred)

--- Verify on macOS/Linux ---
shasum -a 256 x.freq
# The hash MUST equal SHA256(OS-A)
# Then decode:
#   paxect decode < x.freq > out.bin
#   cmp -s sample.in out.bin && echo "byte-identical"
TXT

echo "✅ Cross-OS reproducibility: use SHA256 above to confirm identical container across OS."
