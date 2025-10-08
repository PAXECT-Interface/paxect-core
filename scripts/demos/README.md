# PAXECT Core — Demo Suite (International · Cross-OS)

All demo scripts below are **self-contained**, **safe to run**, and fully **deterministic**.  
They showcase **PAXECT Core** and connected plugins under real-world conditions across  
**Linux**, **macOS**, **Windows**, **Android (Termux)**, and **iOS (Pyto)**.

Each demo prints progress steps, **SHA-256 hashes**, and integrity checks  
to verify **bit-identical round-trips** and **cross-OS reproducibility**.

---

## Demo Overview

| #  | Script | Purpose / Proof |
|:--:|:--|:--|
| 00 | `00_env_check.py` | Environment sanity — verify Python + `paxect_core` importability. |
| 01 | `01_quickstart_smoke.sh` | Quickstart round-trip — deterministic encode/decode (bit-identical). |
| 02 | `02_determinism_roundtrip.sh` | Double-encode proof — identical `.freq` SHA-256; decode back bit-identical. |
| 03 | `03_perf_baseline.sh` | Performance baseline — timed encode/decode throughput. |
| 04 | `04_strict_parser.sh` | Negative tests — corruption, MAGIC/version flip, truncation → clean failure. |
| 05 | `05_mixed_industry_smoke.sh` | Core + Link flow simulation (gateway → exchange → workstation) — E2E OK. |
| 06 | `06_cross_os_verify.sh` | Cross-OS reproducibility — identical container hash across Windows/macOS/Linux. |
| 07 | `07_soundwave_multichannel_os.sh` | Multi-channel containers across OS boundaries — per-channel bit-identical. |
| 08 | `08_industry_robotics_os_bridge.sh` | Multi-hop industry bridge (EDGE → OT → ROS → Linux) — no hash drift, E2E OK. |
| 09 | `09_universal_smoke.py` | Full 3-in-1 universal demo — runs identically on Linux·macOS·Windows·Android·iOS. |
| 10 | `10_universal_core_only.py` | Core-only test — verifies the bare PAXECT kernel (soundwave mapping + CRC32) without plugins. |

---

## How to Run (Cross-Platform)

All demos are written in **pure Python 3.12+** (or POSIX shell for .sh versions)  
and run identically on **Linux**, **macOS**, **Windows (WSL / PowerShell)**,  
**Android (Termux)**, and **iOS (Pyto)**.

Run any demo:

```bash
python3 scripts/demos/00_env_check.py
bash scripts/demos/01_quickstart_smoke.sh
python3 scripts/demos/10_universal_core_only.py









