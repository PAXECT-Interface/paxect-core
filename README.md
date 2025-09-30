# PAXECT — Betrouwbare data-uitwisseling over besturingssystemen en programmeertalen
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Build](https://github.com/PAXECT-Interface/PAXECT---Core/actions/workflows/ci.yml/badge.svg)](../../actions)
[![CodeQL](https://github.com/PAXECT-Interface/PAXECT---Core/actions/workflows/codeql.yml/badge.svg)](../../actions)
[![Discussions](https://img.shields.io/github/discussions/PAXECT-Interface/PAXECT---Core)](../../discussions)

PAXECT is een open-source platform voor **deterministisch** en **veilig** transport/archivering van technische data
(bestanden, streams, logs, telemetrie, updates) in multi-platform omgevingen. Het levert een stabiel containerformaat
**`.freq`**, een **plug-and-play** extensiemodel (encryptie, taal-bindings, performance-tuning) en een **privacy-first**
architectuur (geen telemetry, geen externe datastromen). **Zero AI.**

> **Lanceringsperiode (gratis)**: alle features (incl. Enterprise/Pro) zijn gratis t/m **2026-04-01**.  
> De Core blijft daarna open-source (Apache-2.0) en onderhouden.

---

## Kerneigenschappen
- **Deterministisch** — zelfde input + configuratie ⇒ bit-identieke output (audit/compliance/regressie).
- **Multi-OS & polyglot** — Windows, Linux, macOS; bindings voor Python, Node.js, Go (meer via plugins).
- **Integriteit eerst** — frame-I/O met **CRC32 per frame** en strikte parsing (fail-hard bij fouten).
- **Uitbreidbaar** — encryptie, bindings en tuning als optionele plugins (zonder wijzigingen in Core).
- **Privacy by default** — lokale uitvoering; geen tracking/telemetry.

---

## Supportmatrix (basismodel)
| Domein       | Officieel (OSS)                                       | Notities / Volledige matrix |
|--------------|--------------------------------------------------------|-----------------------------|
| **OS**       | Linux x86_64 · Windows 10/11 x86_64 · macOS x86_64/arm64 | Zie `docs/LabReport.md`     |
| **Talen**    | Python · JavaScript/Node.js · Go                       | Extra via Polyglot-plugin   |
| **CPU**      | x86_64 (getest) · ARMv7 (smoke) · ARM64 (gepland)      | RISC-V optioneel            |

**Container:** `.freq` (v42) · CRC32 per frame · vaste footer/metadata · deterministische decode.

---

## Snel starten
1. **Installeer Core** voor jouw OS/CPU (`.so/.dll/.dylib`).  
2. **Kies een binding** (Python / Node.js / Go via Polyglot).  
3. **Smoke-run:** encode → decode; verifieer CRC/footer (v42).  
   → Zie **Installatie & Gebruik** hieronder en `docs/LabReport.md`.

---

## Plugins (officieel)
| Plugin              | Scope                          | Highlights                                               | Repo |
|---------------------|--------------------------------|----------------------------------------------------------|------|
| **AES Secure**      | Vertrouwelijkheid & integriteit| AES-256 GCM/CTR, scrypt KDF, AAD, strikt falen           | https://github.com/PAXECT-Interface/paxect-aes-plugin |
| **Polyglot**        | Taal-bindings                  | Python, Node.js, Go; extra talen via enterprise          | https://github.com/PAXECT-Interface/paxect-polyglot-plugin |
| **SelfTune 5-in-1** | Performance & observability    | Guard, overhead-controle, logging, smoothing, auto-learning | https://github.com/PAXECT-Interface/paxect-selftune-5in1 |

**Plug-and-play:** Core draait zonder plugins; per run inschakelen via config/flag of binding-API. Determinisme blijft gelijk.

![PAXECT Architecture](paxect_architecture_v6.svg)





---

## Installatie & Gebruik (Quickstart)
- **Vereisten:** Linux/Windows/macOS; x86_64; voldoende schijfruimte voor input + tijdelijke frames.  
- **Encode (→ `.freq`):** framen → (optioneel) delta/mapping → compressie (zstd/LZ4/zlib) → CRC per frame → footer (v42).  
- **Decode (van `.freq`):** footer parsen → CRC valideren → (optioneel) decrypt → decompresseren → bytes reconstrueren.  
- **Streaming:** stdin/stdout met begrensd geheugen; onderbrekingen worden gedetecteerd.  
- **Foutgedrag:** CRC-mismatch / truncatie / ongeldige metadata ⇒ hard fail (geen gedeeltelijke output).

---

## Roadmap (hoogover)
- **v0.9.0:** deterministische Core; zstd/LZ4/zlib; LabReport; basis-CI (determinisme/streaming/corruptie).  
- **v1.0.0:** bredere OS-matrix (Windows CMD, macOS soak), eerste ARM64 build; AES-release; Polyglot stable; SelfTune public.  
- **Na 1.0:** prebuilt binaries, SBOM/attestations, extra bindings/integraties (Kafka/S3/SIEM), LTS.

---

## Governance, Security & Privacy
- **Licentie:** Apache-2.0 (`LICENSE`, `NOTICE`) · **Merken:** zie `TRADEMARKS.md`.  
- **Bijdragen & Gedragscode:** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`. **Security:** `SECURITY.md`.  
- **Privacy:** geen telemetry of externe uploads; lokaal by default. Zie `docs/PRIVACY.md`.



**Vragen of verzoeken? Mail ons of open een GitHub issue!**

---

## Contact
**contact@paxect.io** · Issues: https://github.com/PAXECT-Interface/PAXECT---Core/issues · Discussions: https://github.com/PAXECT-Interface/PAXECT---Core/discussions










