[![Star](https://img.shields.io/badge/⭐%20Star-this%20repo-orange)](../../stargazers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](../LICENSE)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](../../actions)
[![CodeQL](https://img.shields.io/badge/CodeQL-active-lightgrey.svg)](../../actions)
[![Issues](https://img.shields.io/badge/Issues-open-blue)](../../issues)
[![Discussions](https://img.shields.io/badge/Discuss-join-blue)](../../discussions)
[![Security](https://img.shields.io/badge/Security-responsible%20disclosure-informational)](../SECURITY.md)
[![Python](https://img.shields.io/badge/Python-3.12+-informational)](#)

---
# 🧠 PAXECT Core — Enterprise Demo Suite (Deterministic · CRC32+SHA-256 · Cross-OS · Offline)

> 💬 *Validated demo collection for deterministic verification, reproducibility, and cross-OS integrity.*  
> Each demo is self-contained, safe to run, and deterministic across **Linux**, **macOS**, **Windows**, **Android (Termux)**, and **iOS (Pyto)**.

---

### 🔗 Navigation
← [Back to PAXECT Core Overview](../README.md) · [Report Issue](https://github.com/paxect/paxect-core/issues) · [License](../LICENSE)

---

## ⚙️ Purpose
This suite validates the **PAXECT Core** engine:

- Determinism (identical output per run)
- Cross-OS reproducibility
- Integrity (**CRC32 per frame + SHA-256 footer**)
- Multi-channel performance
- Streamed pipelines and strict parser behavior

Each demo prints progress, SHA-256 hashes, exit codes, and a validation summary.

---

## 🚀 Quick Setup

```bash
# Clone the PAXECT Core repository
git clone https://github.com/paxect/paxect-core.git
cd paxect-core/demos

# (Optional) create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install zstandard psutil
````

> Windows tip: vervang `python3` door `py -3` of `python` afhankelijk van je omgeving.

---

## 🧩 Demo Overview

|  #  | Script                        | Description / Proof                                                                |
| :-: | :---------------------------- | :--------------------------------------------------------------------------------- |
|  00 | `00_env_check.py`             | Environment sanity — verify Python version, dependencies, and container constants. |
|  01 | `01_quickstart_smoke.py`      | Quickstart round-trip — deterministic encode/decode (bit-identical).               |
|  02 | `02_determinism_roundtrip.py` | Double-encode proof — identical `.freq` SHA-256; bit-exact decode.                 |
|  03 | `03_perf_baseline.py`         | Performance baseline — timed encode/decode throughput.                             |
|  04 | `04_strict_parser.py`         | Negative tests — corruption, MAGIC/version flip, truncation → clean failure.       |
|  05 | `05_mixed_industry_smoke.py`  | Mixed-mode flow simulation (gateway → exchange → workstation).                     |
|  06 | `06_cross_os_verify.py`       | Cross-OS reproducibility — identical container hash across platforms.              |
|  07 | `07_multichannel_os.py`       | Multi-channel and auto-mode verification (1–8 channels).                           |
|  08 | `08_industry_bridge.py`       | Streaming bridge (stdin/stdout) — multi-hop pipeline test.                         |
|  09 | `09_universal_smoke.py`       | Universal regression — determinism + corruption + stream tests.                    |
|  10 | `10_universal_core_only.py`   | Core-only API validation — direct Python calls (BytesIO).                          |

---

## 💻 Run Any Demo

```bash
python 00_env_check.py
python 01_quickstart_smoke.py
python 02_determinism_roundtrip.py
python 03_perf_baseline.py
python 04_strict_parser.py
python 05_mixed_industry_smoke.py
python 06_cross_os_verify.py
python 07_multichannel_os.py
python 08_industry_bridge.py
python 09_universal_smoke.py
python 10_universal_core_only.py
```

Each script:

* Prints progress and SHA-256 verification
* Cleans up temporary files automatically
* Exits with deterministic codes (**0–4**)

---

## 🧱 Run the Full Suite (Automation)

### 🐧 Linux / macOS (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail
LOG="paxect_demo_run_$(date -u +%Y%m%d_%H%M%S).log"

echo "=== PAXECT Core Demo Suite — $(date -u) ===" | tee "$LOG"
for demo in {00..10}; do
  for f in ${demo}_*.py; do
    echo "────────────────────────────────────────" | tee -a "$LOG"
    echo "[RUN] python $f" | tee -a "$LOG"
    python "$f" 2>&1 | tee -a "$LOG"
  done
done
echo "[DONE] All PAXECT Core demos completed ✅" | tee -a "$LOG"
```

### 🪟 Windows (PowerShell)

```powershell
$Log = "paxect_demo_run_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date)
"=== PAXECT Core Demo Suite — $(Get-Date -Format u) ===" | Tee-Object $Log
$Demos = 0..10 | ForEach-Object { "{0:D2}" -f $_ }
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

## 💡 Individual vs Full Suite

| Mode                | When to Use                               | User       | Benefits                                    |
| ------------------- | ----------------------------------------- | ---------- | ------------------------------------------- |
| **Individual Demo** | Development, debugging, or learning       | Developers | Quick, focused feedback                     |
| **Full Suite Run**  | CI/CD, nightly builds, regression testing | QA/DevOps  | Complete reproducibility proof across OS/hw |

**Recommendation**

1. Run individual demos during development.
2. Use the full suite for pre-release validation.
3. Integrate into CI pipelines for cross-OS verification.

---

## 🧾 Verification Model {#verification-model}

Each `.freq` container includes:

* **CRC32** per frame
* **SHA-256** footer (total payload integrity)
* **Version 42** header (backward compatible)
* Deterministic metadata (no timestamps)
* Fail-safe exit codes: **0=OK**, **2=verify fail**, **3=I/O error**, **4=structural error**

---

## 🏁 Validation Status

✅ All 10 demos verified successfully on **Ubuntu 24.04 LTS (x86_64)** with **Python 3.12.3 / GCC 13.3.0**.
Results reproduced across **Linux, macOS, Windows** (bit-identical outputs).

This suite serves as the **official validation harness** for PAXECT Core.

---

## 📜 License

Apache 2.0 — see [LICENSE](../LICENSE).

---

## 📫 Support

For validation, integration help, or CI assistance:
📧 **[contact@paxect.io](mailto:contact@paxect.io)**

```

Wil je dat ik ook meteen een **mini “Badges” blok** erboven zet (CI status, License, CodeQL) voor extra trust/SEO?
```


