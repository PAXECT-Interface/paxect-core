mkdir -p ~/paxect-core/scripts/demos
cat > ~/paxect-core/scripts/demos/README.md <<'MD'
# PAXECT Core — Demo Suite (International)

All demo scripts below are **self-contained**, **safe to run**, and fully **deterministic**.  
They showcase PAXECT Core and connected plugins under real conditions across systems, channels, and hops.

Each script prints progress steps, SHA-256 hashes, and integrity checks — to verify **bit-identical round-trips** and **cross-OS reproducibility**.

---

## Demo Overview

| # | Script | Purpose / Proof |
|:-:|:--|:--|
| 00 | `00_env_check.sh` | Environment sanity (paxect CLI present, core importable). |
| 01 | `01_quickstart_smoke.sh` | Quickstart round-trip — deterministic encode/decode. |
| 02 | `02_determinism_roundtrip.sh` | Double-encode proof — identical container hashes. |
| 03 | `03_perf_baseline.sh` | Raw mapping performance baseline (fast). |
| 04 | `04_strict_parser.sh` | Negative tests (corruption, MAGIC/version, truncation). |
| 05 | `05_mixed_industry_smoke.sh` | Core + Link flow (gateway → exchange → workstation). |
| 06 | `06_cross_os_verify.sh` | Cross-OS reproducibility (Windows · Linux · macOS). |
| 07 | `07_soundwave_multichannel_os.sh` | Multi-channel containers across OS boundaries. |
| 08 | `08_industry_robotics_os_bridge.sh` | Multi-hop industry bridge (EDGE → OT → ROS → Linux). |

---

## How to Run

```bash
# Environment
bash scripts/demos/00_env_check.sh

# Quick tests
bash scripts/demos/01_quickstart_smoke.sh
bash scripts/demos/02_determinism_roundtrip.sh

# Heavier (local)
bash scripts/demos/03_perf_baseline.sh 200
bash scripts/demos/04_strict_parser.sh
bash scripts/demos/05_mixed_industry_smoke.sh
bash scripts/demos/06_cross_os_verify.sh
bash scripts/demos/07_soundwave_multichannel_os.sh 4 8
bash scripts/demos/08_industry_robotics_os_bridge.sh 4 8
