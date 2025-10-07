# PAXECT Core — Demo Suite (International)

All demo scripts below are **self-contained**, **safe to run**, and fully **deterministic**.  
They showcase PAXECT Core and connected plugins under realistic conditions across systems, channels, and hops.

Each demo prints progress steps, SHA-256 hashes, and integrity checks — to verify **bit-identical round-trips** and **cross-OS reproducibility**.

---

## Demo Overview

| #  | Script                                 | Purpose / Proof                                                                 |
|:--:|:---------------------------------------|:---------------------------------------------------------------------------------|
| 00 | `00_env_check.sh`                      | Environment sanity (CLI present, `paxect_core` importable).                     |
| 01 | `01_quickstart_smoke.sh`               | Quickstart round-trip — deterministic encode/decode (bit-identical).            |
| 02 | `02_determinism_roundtrip.sh`          | Double-encode proof — identical `.freq` SHA-256; decode back bit-identical.     |
| 03 | `03_perf_baseline.sh`                  | Raw mapping performance baseline (timed encode/decode throughput).              |
| 04 | `04_strict_parser.sh`                  | Negative tests: corruption, MAGIC/version flip, truncation → clean failures.    |
| 05 | `05_mixed_industry_smoke.sh`           | Core + Link flow simulation (gateway → exchange → workstation) — E2E OK.        |
| 06 | `06_cross_os_verify.sh`                | Cross-OS reproducibility: identical container hash on Windows/macOS/Linux.      |
| 07 | `07_soundwave_multichannel_os.sh`      | Multi-channel containers across OS boundaries — per-channel bit-identical.      |
| 08 | `08_industry_robotics_os_bridge.sh`    | Multi-hop industry bridge (EDGE → OT → ROS → Linux) — no hash drift, E2E OK.    |
| 09 | `09_universal_smoke.py`                | **3-in-1 universal** demo (Linux · macOS · Windows) via Python only.            |

---

## How to Run

```bash
# 0) Environment sanity
bash scripts/demos/00_env_check.sh

# 1–2) Core determinism
bash scripts/demos/01_quickstart_smoke.sh
bash scripts/demos/02_determinism_roundtrip.sh

# 3) Performance (adjust size, e.g. 200–500 MiB)
bash scripts/demos/03_perf_baseline.sh 200

# 4) Strict parser (negative cases must fail or produce non-identical output)
bash scripts/demos/04_strict_parser.sh

# 5) Mixed industry (Core + Link simulated)
bash scripts/demos/05_mixed_industry_smoke.sh

# 6) Cross-OS verify (copy x.freq to other OS and compare SHA-256)
bash scripts/demos/06_cross_os_verify.sh

# 7) Soundwave multi-channel
bash scripts/demos/07_soundwave_multichannel_os.sh 4 8

# 8) Industry & Robotics OS bridge (multi-hop)
bash scripts/demos/08_industry_robotics_os_bridge.sh 4 8

# 9) Universal (3-in-1) — runs the same on Linux/macOS/Windows
python3 scripts/demos/09_universal_smoke.


> **Heavy demos (03, 07, 08)** generate large temporary files under `/tmp`.  
> They clean up automatically.

---

## Requirements
- Linux, macOS, or Windows (PowerShell/WSL ok)
- Python **3.12+** for core bindings and the universal demo (#09)
- `paxect` CLI available in your `PATH`

---

## Notes
- All log output is **English** for international readability.
- Every container is verified via **CRC32** and **SHA-256**.
- To automate multi-OS transfers and watchers in production, see **PAXECT-Link**.
- For CI, run **#09 (universal)** on a **3-OS matrix** to demonstrate cross-platform success.
