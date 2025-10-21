

<p align="center">
  <img src="docs/ChatGPT%20Image%202%20okt%202025,%2022_22_22.png" alt="PAXECT logo" width="200"/>
</p>

# Contributing Guidelines

Welcome, and thank you for your interest in contributing to **PAXECT Core**!  
Your effort helps keep the project deterministic, reproducible, and accessible across every major platform.

---

## Overview

**PAXECT Core** is part of the broader **PAXECT Interface** ecosystem.  
All contributions must remain **deterministic**, **platform-agnostic**, and **dependency-free** — no AI, telemetry, or opaque behavior.  

In short: clean code, transparent logic, reproducible results.

---

## Development Setup

1. **Fork** this repository to your own GitHub account.  
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/PAXECT-Interface/paxect-core.git
   cd paxect-core
````

3. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. **Install dependencies** (if applicable):

   ```bash
   pip install -r requirements.txt
   ```
5. **Verify determinism** before coding:

   ```bash
   python demos/demo_01_quickstart_smoke.py
   python demos/demo_02_determinism_roundtrip.py
   ```

> 🧩 Each demo should pass without drift — if not, investigate before contributing.

---

## Contribution Rules

* Keep commits focused and clear.
  Example: `fix: align CRC32 validation on Windows` or `docs: clarify checksum flow`.
* All files must include SPDX headers:

  ```python
  # SPDX-FileCopyrightText: © 2025 PAXECT
  # SPDX-License-Identifier: Apache-2.0
  ```
* Test changes on **at least two operating systems**.
* Avoid network calls, telemetry, or machine-learning logic.
* All pull requests must pass **CI + CodeQL** checks before review.

---

## Pull Request Workflow

1. Create a feature branch:

   ```bash
   git checkout -b feature/your-change
   ```
2. Make your edits and push:

   ```bash
   git push origin feature/your-change
   ```
3. Open a **Pull Request** with a short description and rationale.
4. Wait for review by maintainers — discussions are encouraged, not bureaucratic.
5. Once approved, your PR will be merged and included in the next deterministic build.

> ✨ The goal: predictable progress, not rushed merges.

---

## Communication

* **Issues:** for bug reports, improvement ideas, and reproducibility findings
* **Discussions:** for architecture, roadmap input, and plugin design
* **Security:** please see [SECURITY.md](./SECURITY.md) for responsible disclosure

---

## Thank You 💛

Every contribution — small or large — helps make **PAXECT Core** more robust, transparent, and enterprise-ready.
Your time and expertise are truly appreciated.

> Together we keep PAXECT deterministic, fair, and open for everyone.


