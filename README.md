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




## Roadmap

### v0.9.0 (pre-release)
- Deterministic encode/decode; frame I/O + per-frame CRC32; footer v42.
- Compressors: zstd / LZ4 / zlib; optional delta/mapping.
- Docs: README, `docs/LabReport.md`, OS matrix.
- CI (basis): determinism, truncation/corruption, streaming.

### v1.0.0 (stable)
- OS-matrix breder: Windows CMD smoke, macOS soak; eerste ARM64 build/run.
- Plugins: AES Secure release; Polyglot (Python/Node.js/Go stable); SelfTune 5-in-1 public (lab-getest).
- Artefacts: fixed workloads + CSV/JSONL in `benchmarks/`; golden vectors.

### Post-1.0
- Prebuilt binaries per OS/CPU (gesigneerd waar nodig), SBOM/attestations.
- Verdere bindings (Java, C#) en integraties (Kafka, S3/Azure, SIEM).
- Android/iOS native runs; SelfTune-profielen en overhead-budgets.
- Governance: LTS-schema, compat-matrix per release.




## Community & Governance

- **Issues / Discussions** — Support, Q&A, designvoorstellen, OS-readiness rapporten.
- **Contributing** — Zie `CONTRIBUTING.md` (workflow, tests, code style, commit conventies).
- **Code of Conduct** — Zie `CODE_OF_CONDUCT.md`.
- **Security** — Responsible disclosure in `SECURITY.md` (contact + eventueel PGP).

### Maintainers & rollen (aanbevolen)
- **Core**: 2–3 maintainers (triage, reviews, releases, docs).
- **Plugins**: 1–2 per plugin (AES, Polyglot, SelfTune).
- **Moderation/CI (optioneel)**: 1–2 voor Discussions/CI.

### Good first issues (suggesties)
- Windows **CMD** smoke (`smoke.cmd`); macOS **soak**; **ARM64** native run.
- RISC-V optioneel; Android NDK/JNI eerste load.




## Licensing & Trademark

### Free Base Tier (OSS) — first 6 months from 2025-10-01
- **All features are free** during the launch period (until **2026-04-01**).
- **OS (official):** Linux x86_64, Windows 10/11 x86_64, macOS x86_64/arm64
- **Languages (Polyglot):** Python, JavaScript/Node.js, Go
- **Security:** AES-256 GCM/CTR (basic), scrypt KDF, AAD  
- Community support; monthly OSS releases

### After the free period
- We announce ≥30 days in advance which features remain free vs. move to Enterprise/Pro.
- **PAXECT Core remains open-source and maintained** under Apache-2.0.

### Enterprise/Pro (may apply after the free period)
- **Performance & Ops:** SelfTune 5-in-1 (guard, overhead, logging, smoothing, auto-learning)
- **Security & Compliance:** HSM/KMS integratie, FIPS modes, compliance/audit logging
- **Languages:** Java (JNI), C#/.NET (P/Invoke); possible “enhanced” features for Python/Node/Go
- **Delivery:** signed builds, SBOM/attestations, LTS maintenance, SLA support
- **Integrations:** Kafka, S3/Azure Blob, SIEM export (Splunk/ELK), policy hooks

### Legal
- **License:** Apache License 2.0 (`LICENSE`, `NOTICE`)  
- **Trademarks:** use of the “PAXECT” name and logo is governed by `TRADEMARKS.md` (no confusing branding).  
- **Commercial modules:** optional Enterprise/Pro features may be offered under separate terms.




## Privacy & Security

- **Privacy-first:** no telemetry, no external uploads; local by default.
- **Security scope (Core):** integrity + determinism (per-frame CRC32, strict parsing, fail-hard).
- **Confidentiality (opt-in):** via AES Secure Plugin (AES-256 GCM/CTR, scrypt KDF, AAD).
- **Docs:** see `docs/PRIVACY.md` and `SECURITY.md`.

> Verify runs via checksums and footer/flags; store logs/CSV artefacts for audits.



## Disclaimer & Liability

This software is provided “as is”, without warranty of any kind, express or implied.  
The owner, maintainers, and contributors shall not be liable for any direct, indirect, incidental, special, or consequential damages arising from the use of this software.  
See `LICENSE` (Apache-2.0) for details.



## Contact

Questions or collaboration: **contact@paxect.io**  
Issues: https://github.com/PAXECT-Interface/PAXECT---Core/issues  
Discussions: https://github.com/PAXECT-Interface/PAXECT---Core/discussions









