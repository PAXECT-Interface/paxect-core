# PAXECT — Reliable Data Exchange Across Operating Systems and Programming Languages

PAXECT is an open-source platform for deterministic, secure transport and archiving of technical data (files, streams, logs, telemetry, updates) in complex, multi-platform environments. It provides a stable container format (`.freq`), a plug-and-play extension model (encryption, language bindings, performance tuning), and a privacy-first architecture with no telemetry or external data flows.

PAXECT enables reproducible exchange across operating systems (Windows, Linux, macOS, BSD, ARM/embedded, mobile) and integrates with programming languages including Python, JavaScript/Node.js, Rust, Go, Java, C#, PHP, and Ruby.

---

## Important Notice: Free Launch Period

All PAXECT features — including Enterprise/Pro features — are **free for the first 6 months after launch**.

- **Launch date:** 2025-10-01  
- **Free period ends:** 2026-04-01

At least **30 days before** the end date we will publish whether the free period is extended or which features become paid (Enterprise/Pro).  
**The open-source Core will remain open-source and maintained** under Apache-2.0.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Build](https://github.com/PAXECT-Interface/PAXECT---Core/actions/workflows/ci.yml/badge.svg)](../../actions)
[![CodeQL](https://github.com/PAXECT-Interface/PAXECT---Core/actions/workflows/codeql.yml/badge.svg)](../../actions)
[![Discussions](https://img.shields.io/github/discussions/PAXECT-Interface/PAXECT---Core)](../../discussions)



## Table of Contents
- [Core Values](#core-values)
- [Why PAXECT](#why-paxect)
- [Use Cases](#use-cases)
- [Compatibility](#compatibility)
- [Installation & Usage (Quickstart)](#installation--usage-quickstart)
- [Plugins & Extension Points](#plugins--extension-points)
- [Roadmap](#roadmap)
- [Community & Governance](#community--governance)
- [Licensing & Trademark](#licensing--trademark)
- [Privacy & Security](#privacy--security)
- [Disclaimer & Liability](#disclaimer--liability)
- [Contact](#contact)





## Core Values
- **Deterministic** — Same input + configuration ⇒ bit-identical output (audit/compliance/regression).
- **Multi-OS & multi-language** — Native support across OS families with broad language bindings.
- **Extensible** — Plug-and-play modules for encryption, observability, performance, and extra bindings.
- **Privacy & security** — No tracking or cloud dependency; optional AES-based encryption; explicit integrity checks.
- **Transparency** — Apache-2.0 licensing, public roadmap, compatibility matrix, and benchmarks. **Zero AI.**

-
-
- ## Why PAXECT

- **Reliable in heterogeneous environments** — consistent containers across Linux/Windows/macOS/BSD/embedded.
- **Audit-ready & reproducible** — deterministic processing (bit-identical with same input/config) for compliance and QA.
- **Fast integration** — stable `.freq` wire format plus plug-and-play plugins (encryption, language bindings, tuning).
- **Operational confidence** — strict integrity checks (per-frame CRC), fail-hard on truncation/corruption, clear exit behavior.
- **Privacy-first** — no telemetry or external uploads; optional AES-based confidentiality via plugin (opt-in).




## Compatibility

### Operating systems (status)
| OS family               | Status     | Notes                                                    |
|-------------------------|------------|----------------------------------------------------------|
| Linux (x86_64)          | Tested     | Ubuntu 20.04/22.04; kernel 6.x; soak/benchmarks complete |
| Windows 10/11 (x86_64)  | Tested     | PowerShell smoke OK; update payloads bit-identical       |
| macOS (x86_64/arm64)    | Partial    | Decode OK; full soak planned                             |
| BSD (Free/Open)         | Partial    | Smoke OK                                                 |
| Embedded Linux / RTOS   | Concept    | Same API/FFI; hardware runs welcome                      |
| Android (NDK/JNI)       | OS-ready   | Not yet tested                                           |
| iOS (C/Swift bridge)    | OS-ready   | Not yet tested                                           |

> Full details and logs: see `docs/LabReport.md`.

### CPU architectures
- **x86_64**: primary test target  
- **ARMv7**: smoke via QEMU-chroot OK  
- **ARM64**: planned (native builds/tests)  
- **RISC-V**: optional; same flow as ARM

### Languages (via Polyglot)
Bindings available for **Python, JavaScript/Node.js, Go, C/C++, Java, C#, PHP, Ruby, Rust**.  
> Availability may vary by edition; see **[Licensing & Trademark](#licensing--trademark)**.

### Container format
- Stable **`.freq`** (version **42**)  
- **Frame-based** I/O with per-frame **CRC32**  
- Fixed **footer/metadata**; strict parsing  
- **Deterministic decode**, platform/endianness-agnostic





## Installation & Usage (Quickstart)

### Prerequisites
- **OS:** Linux, Windows, macOS (see matrix above)
- **CPU:** x86_64 tested; ARMv7 smoke OK; ARM64 planned
- **I/O & storage:** enough disk for inputs + temporary frames

### Install (high level)
- **Core library:** build/install the platform library (`.so`/`.dll`/`.dylib`)
- **Bindings (Polyglot):** choose your language binding (Python / Node.js / Go, etc.)
- **Smoke run:** encode → decode; verify checksums, per-frame CRC, footer (version 42)

### Use (conceptual)
- **Encode (input → `.freq`):** frame data, optional delta/mapping, compress (zstd/LZ4/zlib), CRC per frame, write footer (v42)
- **Decode (`.freq` → output):** parse footer, validate CRC, optional decrypt (AES plugin), decompress, reconstruct bytes
- **Streaming:** stdin/stdout supported; bounded peak memory via frames
- **Multi-channel:** process multiple channels in parallel with channel isolation

### Failure & exit behavior
- CRC mismatch, truncation, invalid metadata ⇒ **hard fail** (no partial output)
- If encryption is enabled: wrong key/tag/AAD ⇒ **strict fail**

### Verification & audit
- Compare input/output checksums; inspect footer/flags
- Keep logs/CSV artifacts for benchmarks and regressions (`docs/LabReport.md`)




## Plugins & Extension Points

### Official plugins
| Plugin                   | Scope                          | Highlights                                        | Repository |
|--------------------------|--------------------------------|---------------------------------------------------|------------|
| PAXECT AES Secure Plugin | Confidentiality & authenticity | AES-256 GCM/CTR, scrypt KDF, AAD, strict fail     | https://github.com/PAXECT-Interface/paxect-aes-plugin |
| PAXECT Polyglot Plugin   | Language bindings              | Python, Node.js, Go, C/C++, Java, C#, PHP, Ruby…  | https://github.com/PAXECT-Interface/paxect-polyglot-plugin |
| PAXECT SelfTune 5-in-1   | Performance & observability    | Guard, overhead control, logging, smoothing, auto-learning | https://github.com/PAXECT-Interface/paxect-selftune-5in1 |

### Plug-and-play model
- **Optional & decoupled:** Core werkt zonder plugins; plugins voegen functies toe zonder Core te wijzigen.  
- **Activation per run:** via config/flag of via de binding-API.  
- **Determinism unchanged:** containers blijven v42-conform; reproduceerbaarheid blijft intact.  
- **Overhead:** uit = geen overhead; aan = alleen geselecteerde plugin(s).

### Extension points
- **Pre-processing hooks:** mapping/delta vóór compressie (deterministisch).  
- **Container transforms:** encryptie/integriteit op containerniveau (AES-plugin).  
- **I/O adapters:** extra sources/sinks naast file en stdin/stdout.








