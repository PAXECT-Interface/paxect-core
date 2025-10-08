#!/usr/bin/env bash
set -euo pipefail
# PAXECT — Industry + Robotics + Linux OS Bridge Demo (multi-hop, multi-channel)
# Replaces real daemons with simple hand-offs; compatible with any shell.
# For production watchers/services, use the PAXECT-Link repo.

CHAN="${1:-4}"         # channels (e.g., 4)
SZ_MB="${2:-8}"        # MiB per channel (e.g., 8)

echo "[1/9] Topology & workspace…"
BASE="$(mktemp -d)"; trap 'rm -rf "$BASE"' EXIT
EDGE="$BASE/EDGE_RTOS"         # Embedded/RTOS edge
OT="$BASE/OT_SCADA"            # OT/SCADA exchange (dropfolder)
ROS="$BASE/ROBOT_ROS2"         # Robotics node
WS="$BASE/LINUX_WS"            # Linux workstation
for d in "$EDGE/IN" "$EDGE/OUT" "$OT/IN" "$OT/OUT" "$ROS/IN" "$ROS/OUT" "$WS/IN" "$WS/OUT"; do
  mkdir -p "$d"
done
echo "      BASE=$BASE"
printf "      Nodes: EDGE_RTOS, OT_SCADA, ROBOT_ROS2, LINUX_WS\n"

echo "[2/9] Produce per-channel inputs on EDGE (RTOS)…"
for i in $(seq 1 "$CHAN"); do
  dd if=/dev/urandom of="$EDGE/IN/in_ch${i}.bin" bs=1M count="$SZ_MB" status=none
done
ls -1 "$EDGE/IN" | sed 's/^/      /'

echo "[3/9] EDGE encodes each channel → .freq (deterministic)…"
for i in $(seq 1 "$CHAN"); do
  paxect encode < "$EDGE/IN/in_ch${i}.bin" > "$EDGE/OUT/x_ch${i}.freq"
done

echo "[4/9] Baseline container hashes (OS-A = EDGE)…"
for i in $(seq 1 "$CHAN"); do
  size=$(stat -c '%s' "$EDGE/OUT/x_ch${i}.freq")
  sha=$(sha256sum "$EDGE/OUT/x_ch${i}.freq" | awk '{print $1}')
  printf "      EDGE ch%-2d  size=%-10s  SHA256=%s\n" "$i" "$size" "$sha"
done

echo "[5/9] Hop #1 — OT/SCADA dropfolder hand-off (simulated)…"
# In production, a link-agent/watch service would detect and move. We simulate with cp.
cp -f "$EDGE/OUT/"x_ch*.freq "$OT/IN/"

echo "[6/9] Hop #2 — OT → ROBOT (ROS2 node), verification + pass-through…"
ok=1
for i in $(seq 1 "$CHAN"); do
  # Verify container hash unchanged on ROS
  sha_edge=$(sha256sum "$EDGE/OUT/x_ch${i}.freq" | awk '{print $1}')
  sha_ros=$(sha256sum "$OT/IN/x_ch${i}.freq"   | awk '{print $1}')
  if [ "$sha_edge" != "$sha_ros" ]; then
    echo "      ❌ hash drift on ch${i} (OT input)"; ok=0
  fi
  # Simulate ROS processing: the ROS node forwards containers as-is
  cp -f "$OT/IN/x_ch${i}.freq" "$ROS/IN/x_ch${i}.freq"
done
[ "$ok" -eq 1 ] || { echo "❌ Drift detected on OT hand-off"; exit 1; }
echo "      ✅ OT hand-off verified (hashes match)"

echo "[7/9] Hop #3 — ROBOT → LINUX Workstation, verification…"
ok=1
for i in $(seq 1 "$CHAN"); do
  sha_ros=$(sha256sum "$ROS/IN/x_ch${i}.freq" | awk '{print $1}')
  cp -f "$ROS/IN/x_ch${i}.freq" "$WS/IN/x_ch${i}.freq"
  sha_ws=$(sha256sum "$WS/IN/x_ch${i}.freq"  | awk '{print $1}')
  if [ "$sha_ros" != "$sha_ws" ]; then
    echo "      ❌ hash drift on ch${i} (ROS→WS)"; ok=0
  fi
done
[ "$ok" -eq 1 ] || { echo "❌ Drift detected ROS→WS"; exit 1; }
echo "      ✅ ROS→WS hand-off verified (hashes match)"

echo "[8/9] Final decode on Linux WS → prove bit-identical per channel…"
ok=1
for i in $(seq 1 "$CHAN"); do
  paxect decode < "$WS/IN/x_ch${i}.freq" > "$WS/OUT/out_ch${i}.bin"
  if cmp -s "$EDGE/IN/in_ch${i}.bin" "$WS/OUT/out_ch${i}.bin"; then
    echo "      ✅ ch${i}: bit-identical (EDGE → OT → ROS → WS)"
  else
    echo "      ❌ ch${i}: mismatch"; ok=0
  fi
done
[ "$ok" -eq 1 ] || { echo "❌ End-to-end mismatch"; exit 1; }

echo "[9/9] Cross-OS verification notes"
cat <<'TXT'
To verify on actual different OS machines:
- Transfer the x_ch#.freq files to each OS.
- Compute SHA256 on each OS; hashes MUST match those produced at the EDGE step.
- Then decode and compare bytes (cmp/fc /b/shasum) to confirm bit-identical output.
For automated watchers/services on each hop, use PAXECT-Link (systemd/Windows Service).
TXT

echo "✅ Multi-hop, multi-channel bridge verified without hash drift."
