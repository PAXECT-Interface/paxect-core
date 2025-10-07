
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
