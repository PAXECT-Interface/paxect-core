#!/usr/bin/env bash
set -euo pipefail

SZ_MB="${1:-200}"   # choose 200–500 MB for a meaningful run
echo "[1/6] Create temporary workspace…"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
echo "      TMP = $TMP"

echo "[2/6] Generate random test input (${SZ_MB} MiB)…"
dd if=/dev/urandom of="$TMP/in.bin" bs=1M count="$SZ_MB" status=none
printf "      in.bin size = %s bytes\n" "$(stat -c '%s' "$TMP/in.bin")"

echo "[3/6] Encode → .freq (timed)…"
ENC_T=$(/usr/bin/time -f %e -o "$TMP/enc.t" bash -c 'paxect encode < "$0" > "$1"' "$TMP/in.bin" "$TMP/x.freq" 2>/dev/null; cat "$TMP/enc.t")
printf "      x.freq size = %s bytes (t_enc=%ss)\n" "$(stat -c '%s' "$TMP/x.freq")" "$ENC_T"

echo "[4/6] Decode → raw (timed)…"
DEC_T=$(/usr/bin/time -f %e -o "$TMP/dec.t" bash -c 'paxect decode < "$0" > "$1"' "$TMP/x.freq" "$TMP/out.bin" 2>/dev/null; cat "$TMP/dec.t")
printf "      out.bin size = %s bytes (t_dec=%ss)\n" "$(stat -c '%s' "$TMP/out.bin")" "$DEC_T"

echo "[5/6] Verify bit-identical…"
if cmp -s "$TMP/in.bin" "$TMP/out.bin"; then
  echo "✅ Bit-identical (input == output)"
else
  echo "❌ Mismatch — output differs from input"; exit 1
fi

echo "[6/6] Compute throughput…"
ENC_MBPS=$(awk -v s="$SZ_MB" -v t="$ENC_T" 'BEGIN{if(t>0) printf "%.1f", s/t; else print "inf"}')
DEC_MBPS=$(awk -v s="$SZ_MB" -v t="$DEC_T" 'BEGIN{if(t>0) printf "%.1f", s/t; else print "inf"}')
echo "📊 Encode: ~${ENC_MBPS} MB/s | Decode: ~${DEC_MBPS} MB/s"

echo "ℹ️ Tip: if you hit an input limit, export e.g. PAXECT_MAX_INPUT_MB=$((SZ_MB+64)) and retry."
