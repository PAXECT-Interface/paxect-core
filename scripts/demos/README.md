# 🧪 PAXECT Core — Demo Suite (International · Cross-OS)

All demo scripts below are **self-contained**, **safe to run**, and fully **deterministic**.  
They showcase **PAXECT Core** and connected plugins under real-world conditions across  
**Linux**, **macOS**, **Windows**, **Android (Termux)**, and **iOS (Pyto)**.

Each demo prints progress steps, **SHA-256 hashes**, and integrity checks  
to verify **bit-identical round-trips** and **cross-OS reproducibility**.

---

## 🧭 Demo Overview

| # | Script | Purpose / Proof |
|:-:|:--|:--|
| 00 | `00_env_check.py` | Environment sanity — verify Python + `paxect_core` importability. |
| 01 | `01_quickstart_roundtrip.py` | Quickstart round-trip — deterministic encode/decode (bit-identical). |
| 02 | `02_determinism_double_encode.py` | Double-encode proof — identical `.freq` SHA-256; decode back bit-identical. |
| 03 | `03_perf_baseline.py` | Performance baseline — timed encode/decode throughput. |
| 04 | `04_strict_parser.py` | Negative tests — corruption, MAGIC/version flip, truncation → clean failure. |
| 05 | `05_mixed_industry_smoke.py` | Core + Link flow simulation (gateway → exchange → workstation) — E2E OK. |
| 06 | `06_cross_os_verify.py` | Cross-OS reproducibility — identical container hash across Windows/macOS/Linux. |
| 07 | `07_multichannel_bridge.py` | Multi-channel container test across OS boundaries — per-channel bit-identical. |
| 08 | `08_industry_robotics_bridge.py` | Multi-hop industry bridge (EDGE → OT → ROS → Linux) — no hash drift, E2E OK. |
| 09 | `09_universal_total.py` | Full 3-in-1 universal demo — runs identically on Linux · macOS · Windows · Android · iOS. |

---

## ▶️ How to Run (Cross-Platform)

All demos are written in **pure Python 3.12+** and require **no shell scripts**.  
They run identically on **Linux**, **macOS**, **Windows (WSL / PowerShell)**,  
**Android (Termux)**, and **iOS (Pyto)**.

Run any demo:
```bash
python3 scripts/demos/XX_demo_name.py

Examples

python3 scripts/demos/00_env_check.py
python3 scripts/demos/01_quickstart_roundtrip.py
python3 scripts/demos/09_universal_total.py

Each demo prints its own status, progress, and SHA-256 summary.
Large demos automatically clean up temporary files under the system temp folder.



🧩 Requirements

Python 3.12 or later

paxect_core module importable

Optional: paxect CLI in PATH (for CLI comparison)

No extra dependencies required


🌍 Notes

All output is in English for international readability.

Every container is verified via CRC32 + SHA-256.

For automation and real transfers, see PAXECT-Link.

For CI, run demo #09 on a 3-OS matrix to prove cross-platform determinis


