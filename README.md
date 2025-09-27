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

- ## Why PAXECT

- **Reliable in heterogeneous environments** — consistent containers across Linux/Windows/macOS/BSD/embedded.
- **Audit-ready & reproducible** — deterministic processing (bit-identical with same input/config) for compliance and QA.
- **Fast integration** — stable `.freq` wire format plus plug-and-play plugins (encryption, language bindings, tuning).
- **Operational confidence** — strict integrity checks (per-frame CRC), fail-hard on truncation/corruption, clear exit behavior.
- **Privacy-first** — no telemetry or external uploads; optional AES-based confidentiality via plugin (opt-in).





