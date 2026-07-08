# Multi-Stage OOP Agent Architecture Plan

This document outlines the class-based redesign of the research pipeline into modular, single-responsibility agents, orchestrated by a central controller.

```
                  ┌──────────────────────┐
                  │     MasterAgent      │
                  │   (orchestrator)     │
                  └──────────┬───────────┘
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     ResearchAgent   VerificationAgent  AnalyticsAgent
                                              │
                                              ▼
                                         ReportAgent
```

---

## 1. Agent Specifications

### 🤖 ResearchAgent
* **File:** `scripts/research_agent.py`
* **Inputs:** Raw app list from JSON/CSV database.
* **Responsibilities:**
  - `run_research_loop()`: Queries official documentation pathways using search engines.
  - `check_link(url)`: Performs concurrent pings to validate URLs and prevent broken/outdated links.
  - `save_database()`: Preserves database entries to `apps_research.json` and updates CSV targets.

### ✅ VerificationAgent
* **File:** `scripts/verify_results.py`
* **Inputs:** Checked sample database (`data/verification_sample.csv`).
* **Responsibilities:**
  - `calculate_metrics()`: Manually audits the sample set.
  - Computes first-pass and final calibrated accuracies.
  - Logs exact mismatch errors to `data/verification_metrics.json`.

### 📊 AnalyticsAgent
* **File:** `scripts/build_case_study.py` (Class implementation)
* **Inputs:** Unified researched database (`apps_research.json`) & verification metrics.
* **Responsibilities:**
  - Aggregates auth methods, self-serve access, buildability, and blocker status count distributions.
  - Normalizes fields to resolve label mismatches.
  - Renders inline dynamic SVGs (e.g., self-serve donut chart).

### 💻 ReportAgent
* **File:** `scripts/build_case_study.py` (Class implementation)
* **Inputs:** Structured aggregation map compiled by `AnalyticsAgent`.
* **Responsibilities:**
  - Compiles layout templates, dynamic SVG charts, and the 100-app paginated client database.
  - Overwrites the final case study site at `public/index.html`.

### 👑 MasterAgent (Orchestrator)
* **File:** `scripts/orchestrator.py`
* **Inputs:** Command line arguments (`--run-all`, `--research`, `--verify`, `--report`).
* **Responsibilities:**
  - Imports all sub-agents.
  - Sets file path configurations globally.
  - Orchestrates execution order and prints system logs.

---

## 2. Benefits of this Architecture
- **OOP Compliance:** Avoids global state mutations and wraps operational scripts in clean, instantiation-friendly Python classes.
- **System Thinking Representation:** Demonstrates structural and system design capabilities to recruiters.
- **Execution Speed:** Retains ultra-fast execution time (< 3 seconds total run-time) with zero external LLM dependencies.
