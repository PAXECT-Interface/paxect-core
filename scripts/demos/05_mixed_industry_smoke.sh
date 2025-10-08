#!/usr/bin/env bash
set -euo pipefail

echo "[1/6] Create temporary EXCHANGE layout (INBOX/EXCHANGE/OUTBOX)…"
BASE="$(mktemp -d)"; trap 'rm -rf "$BASE"' EXIT
IN="$BASE/INBOX"; X="$BASE/EXCHANGE"; OUT="$BASE/OUTBOX"
mkdir -p "$IN" "$X" "$OUT"
echo "      BASE = $BASE"

echo "[2/6] Produce a realistic payload (128 KiB)…"
dd if=/dev/urandom of="$IN/payload.bin" bs=128K count=1 status=none
printf "      payload.bin = %s bytes\n" "$(stat -c '%s' "$IN/payload.bin")"

echo "[3/6] Encode on 'producer/gateway' → .freq in EXCHANGE…"
paxect encode < "$IN/payload.bin" > "$X/payload.freq"
printf "      payload.freq = %s bytes (SHA256=%s)\n" "$(stat -c '%s' "$X/payload.freq")" "$(sha256sum "$X/payload.freq" | awk '{print $1}')"

echo "[4/6] (Simulated) Link step — move/copy EXCHANGE → workstation…"
# If paxect_link_plugin exposes a function, we could call it; here we just simulate a handoff.
cp -f "$X/payload.freq" "$OUT/payload.freq"

echo "[5/6] Decode on 'workstation' → OUTBOX…"
paxect decode < "$OUT/payload.freq" > "$OUT/payload.out"
printf "      payload.out = %s bytes\n" "$(stat -c '%s' "$OUT/payload.out")"

echo "[6/6] Verify end-to-end determinism (byte-identical)…"
if cmp -s "$IN/payload.bin" "$OUT/payload.out"; then
  echo "✅ End-to-end OK (INBOX → EXCHANGE → OUTBOX is bit-identical)"
else
  echo "❌ End-to-end mismatch"; exit 1
fi

echo "ℹ️ For real watchers/services (systemd/Windows Service), use the PAXECT-Link repo."
