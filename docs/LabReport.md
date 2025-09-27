# PAXECT Lab Report

This document summarizes robustness, stress, and OS readiness tests.

## Q-series (Robustness)
| Test | Description | Result |
|------|-------------|--------|
| Q1   | 50× 1 GB encode/decode | OK |
| Q2   | Parallel: two large files | OK |
| Q3   | Fuzz corruption | OK (detected) |
| Q4   | Truncation | OK (detected) |
| Q5   | Streaming 2 GB (stdin/stdout) | OK |
| Q6   | Filenames/permissions (Unicode/ro) | OK |
| Q7   | Low-mem (64–128 MB) | OK |
| Q8   | Determinism | OK (bit-identical) |
| Q9   | RC vs final (golden vector) | OK |
| Q10  | Cross-OS decode | Partial |
| Q11  | Long-run (hours) | OK |
| Q12  | Mixed workload | OK |
| Q13  | Fault injection (abort) | OK |

## S-series (Industry/Stress)
| Test | Description | Result |
|------|-------------|--------|
| U1   | 6 GB roundtrip | OK |
| S1   | Low-mem soak 500× @ ~96 MB | Retry planned |
| S2   | 1000 mini-files | OK |
| S3   | Mixed (commands+logs+fw) | OK |
| S4   | Power/net cut | OK (detected) |
| S5   | Parallel streams (multi-channel) | OK |

## OS Update Workloads
- Linux & Windows “fake update” payloads (1–2 GB) → bit-identical roundtrip.

## Artifacts
- CSV/JSONL under `benchmarks/` (times, ratios, checksums).
- Commands/scripts: `./smoke.sh`, `./run_smoke_mac.command`, `.\smoke.ps1`, `smoke.cmd`, `./smoke_bsd.sh`.
