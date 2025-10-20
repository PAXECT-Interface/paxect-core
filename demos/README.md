[![Star](https://img.shields.io/badge/⭐%20Star-this%20repo-orange)](../../stargazers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](../LICENSE)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](../../actions)
[![CodeQL](https://img.shields.io/badge/CodeQL-active-lightgrey.svg)](../../actions)
[![Issues](https://img.shields.io/badge/Issues-open-blue)](../../issues)
[![Discussions](https://img.shields.io/badge/Discuss-join-blue)](../../discussions)
[![Security](https://img.shields.io/badge/Security-responsible%20disclosure-informational)](../SECURITY.md)
[![Python](https://img.shields.io/badge/Python-3.12+-informational)](#)


---

#  **PAXECT Core — Deterministic Data Containers for Secure Pipelines**

>  Enterprise-grade container engine for reproducible, cross-platform pipelines.
> 100 % offline · Deterministic results · Built-in integrity verification (CRC32 + SHA-256).
> Hardened for **Linux**, **macOS**, **Windows**, **Android (Termux)**, and **iOS (Pyto)**.

---

##  Overview

**PAXECT Core** is the foundation of the PAXECT ecosystem — a deterministic, streaming container runtime
designed for **data reproducibility**, **offline operation**, and **enterprise compliance**.

Key features:

* Multi-channel Zstandard containers (1–8 channels)
* Automatic tuning (RAM / CPU aware)
* Frame-level CRC32 + footer SHA-256 verification
* Deterministic metadata, no timestamps
* Self-recovering decode engine (error isolation)
* Cross-OS identical output (bit-perfect)

---

##  Quick Setup

```bash
git clone https://github.com/paxect/paxect-core.git
cd paxect-core/demos

python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install zstandard psutil
```

>  **Windows tip:** Use `py -3` or `python` instead of `python3`.

---

##  Repository Layout

```text
paxect-core/
├── paxect_core.py                # Main deterministic container engine
└── demos/
    ├── demo_00_env_check.py
    ├── demo_01_quickstart_smoke.py
    ├── demo_02_determinism_roundtrip.py
    ├── demo_03_perf_baseline.py
    ├── demo_04_strict_parser.py
    ├── demo_05_mixed_industry_smoke.py
    ├── demo_06_cross_os_verify.py
    ├── demo_07_multichannel_os.py
    ├── demo_08_industry_bridge.py
    ├── demo_09_universal_smoke.py
    ├── demo_10_universal_core_only.py
    ├── demo_11_fail_and_recover.py
    └── demo_12_stress_test_core.py
```

---

##  Demo Overview

|  #  | Script                        | Description / Proof                                 |
| :-: | :---------------------------- | :-------------------------------------------------- |
|  00 | `00_env_check.py`             | Environment sanity — verify Python, deps, constants |
|  01 | `01_quickstart_smoke.py`      | Quick encode→decode sanity (bit-identical)          |
|  02 | `02_determinism_roundtrip.py` | Double encode proof (SHA-256 match)                 |
|  03 | `03_perf_baseline.py`         | Throughput baseline                                 |
|  04 | `04_strict_parser.py`         | Corruption / MAGIC / version test                   |
|  05 | `05_mixed_industry_smoke.py`  | Gateway→exchange→workstation flow                   |
|  06 | `06_cross_os_verify.py`       | Cross-OS reproducibility                            |
|  07 | `07_multichannel_os.py`       | Auto-mode (1–8 channels)                            |
|  08 | `08_industry_bridge.py`       | Streaming stdin/stdout bridge                       |
|  09 | `09_universal_smoke.py`       | Regression + corruption mix                         |
|  10 | `10_universal_core_only.py`   | Direct Core API validation                          |
|  11 | `11_fail_and_recover.py`      | Corrupted container → detect & recover              |
|  12 | `12_stress_test_core.py`      | 1-minute deterministic stress test                  |

---

## ▶️ Run Any Demo

```bash
python demos/demo_01_quickstart_smoke.py
```

Each script:

* Prints progress + SHA-256 verification
* Cleans up temporary files
* Exits with deterministic codes (`0–4`)

---

## 🔁 Run the Full Suite

### Linux / macOS

```bash
#!/usr/bin/env bash
set -euo pipefail
LOG="paxect_demo_run_$(date -u +%Y%m%d_%H%M%S).log"
echo "=== PAXECT Core Demo Suite — $(date -u) ===" | tee "$LOG"
for demo in {00..12}; do
  for f in ${demo}_*.py; do
    echo "──────────────────────────────" | tee -a "$LOG"
    echo "[RUN] python $f" | tee -a "$LOG"
    python "$f" 2>&1 | tee -a "$LOG"
  done
done
echo "[DONE] All PAXECT Core demos completed ✅" | tee -a "$LOG"
```

### Windows (PowerShell)

```powershell
$Log = "paxect_demo_run_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date)
"=== PAXECT Core Demo Suite — $(Get-Date -Format u) ===" | Tee-Object $Log
$Demos = 0..12 | ForEach-Object { "{0:D2}" -f $_ }
foreach ($d in $Demos) {
  $files = Get-ChildItem "$d*_*.py"
  foreach ($f in $files) {
    "[RUN] python $($f.Name)" | Tee-Object $Log -Append
    python $f.FullName 2>&1 | Tee-Object $Log -Append
  }
}
"[DONE] All PAXECT Core demos completed ✅" | Tee-Object $Log -Append
```

---

##  Verification Model

Each `.freq` container embeds:

* CRC32 per frame
* SHA-256 footer (total payload integrity)
* Header Version 42 (backward compatible)
* Deterministic metadata (no timestamps)
* Fail-safe exit codes → `0=OK`, `2=verify fail`, `3=I/O`, `4=structure`

---

##  Reliability Summary

| Test                     | Duration |       Cycles      |         Errors        | Reliability |
| :----------------------- | :------- | :---------------: | :-------------------: | :---------: |
| Demo 11 – Fail & Recover | Instant  |   2 decode tests  | 1 detected / 0 missed |    100 %    |
| Demo 12 – Stress Test    | 60 s     | ≈ 700 round-trips |           0           |    100 %    |

---

## ✅ Validation Status

All 12 demos passed deterministically on **Ubuntu 24.04 LTS (x86_64)**
with **Python 3.12.3 / GCC 13.3.0**,
reproduced bit-identically across **Linux**, **macOS**, and **Windows**.

This suite is the **official enterprise validation harness** for PAXECT Core.

---


##  Support

For validation, integration help, or CI assistance:
📧 **[PAXECT-Team@outlook.com](mailto:PAXECT-Team@outlook.com)**




---

##  License

All test utilities and scripts are released under the same license as the core engine:
**Apache 2.0 License** — © 2025 PAXECT Systems. All rights reserved.








