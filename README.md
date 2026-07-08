# Composio AI Product Ops Evaluation Case Study

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![GitHub Actions CI/CD](https://img.shields.io/badge/github--actions-active-green.svg)](https://github.com/features/actions)
[![GitHub Pages](https://img.shields.io/badge/github--pages-deployed-brightgreen.svg)](https://pages.github.com/)

An automated research pipeline for evaluating and prioritizing 100 software applications as agent-callable toolkits for Composio. This project combines automated documentation analysis, verification workflows, structured datasets, and an interactive HTML case study to support integration prioritization for AI agents.

---

## 🏗️ Pipeline Architecture

The pipeline uses a multi-stage workflow where each component has a single, isolated responsibility:

```
100 Seed Apps (CSV)
      │
      ▼
[Research Agent] (DDG Search Loops & Multithreaded URL Pings)
      │
      ▼
Research Database (JSON/CSV)
      │
      ▼
[Verification Agent] (Sample Audit, Mismatch Logging, & Fix Calibration)
      │
      ▼
Verified Datasets
      │
      ▼
[Analytics Agent] (Field Normalization & Chart Aggregation)
      │
      ▼
[Report Agent] (Case Study Builder)
      │
      ▼
Interactive HTML Dashboard
```

---

## 🛠️ Technology Stack & AI Tooling

In accordance with the guidelines, AI assistance (Claude / ChatGPT) and automated tools were used to build this pipeline:
- **Programming Language:** Python 3.10
- **AI Tooling:** Claude (API verification helper & code structure design)
- **CI/CD & Hosting:** GitHub Actions & GitHub Pages
- **Frontend Stack:** Vanilla HTML5, CSS3 (Light Mint Grid System), and JavaScript (dynamic client-side search, filtering, and pagination)
- **Data Serialization:** JSON and CSV

---

## 📁 File Structure & Data Roles

```text
assignment-project/
  .github/
    workflows/
      deploy.yml              # GitHub Actions deployment workflow (GitHub Pages)
  data/
    apps_seed.csv             # 100 apps with category & starting urls
    apps_research.json        # Dynamic researched JSON database (Primary research database)
    apps_research.csv         # Tabular CSV representation (Tabular analysis)
    verification_sample.csv   # QA audit sample (20 checked apps)
    verification_metrics.json # Programmatic accuracy stats computed by the verification script
  scripts/
    research_agent.py         # Research agent with search loops & link verification
    verify_results.py         # QA validation tool (calculates accuracy scores & tracks fixes)
    build_case_study.py       # Compiler to build the case-study HTML webpage
    orchestrator.py           # Research Pipeline Orchestrator (runs full pipeline or single stages)
  public/
    index.html                # Interactive HTML case study dashboard (Reviewer presentation)
  README.md                   # Complete repository instructions (this file)
  work_done.md                # Summary of accomplishments
  agent_architecture_plan.md  # Detailed architecture document for the OOP agent design
```

* **JSON (`data/apps_research.json`)**: Acts as the primary research database containing 16 detailed fields for all 100 apps.
* **CSV (`data/apps_research.csv`)**: A tabular export enabling instant spreadsheet analysis.
* **HTML (`public/index.html`)**: The presentation layer rendered for review.

---

## 🔍 Research Sources
To ensure credibility and prevent hallucinations, information was fetched and verified against these sources:
* Official developer documentation portals
* Official API references and specification tables
* Official help centers and merchant support pages
* Public SDK packages (e.g., NPM registries, GitHub CLI repos)

---

## 📊 Key Stats & Verification Metrics

- **100 Researched Apps**: 100% evaluated across category, description, authentication methods, self-serve access, API surface, and Model Context Protocol (MCP) server support.
- **Model Context Protocol (MCP)**: Identified 14 official MCP signals and 4 third-party/community MCP signals.
- **Verification Audit (20-App Sample)**:
  - **First-pass Accuracy**: 40.0%  
    *(Why: Initial extraction intentionally captured raw, unverified search candidate fields, containing outdated homepage URLs or generic placeholders.)*
  - **Final Accuracy on Checked Sample**: 100.0%  
    *(Why: The verification loop corrected missing API subpaths, calibrated confidence metrics, and logged corrections to `data/verification_metrics.json`.)*

---

## ⚙️ Setup & Reproducibility

Ensure you have Python installed on your system.

### Running the Orchestrator (Recommended)
You can run the entire pipeline or execute specific stages using the central Research Pipeline Orchestrator:
* **Run the full pipeline** (Research -> Verify -> Analytics & Compile):
  ```bash
  python scripts/orchestrator.py --run-all
  ```
* **Run only the Research stage (link validation)**:
  ```bash
  python scripts/orchestrator.py --research
  ```
* **Run only the QA Verification stage**:
  ```bash
  python scripts/orchestrator.py --verify
  ```
* **Run only the HTML Case Study compilation**:
  ```bash
  python scripts/orchestrator.py --report
  ```

---

## 🚀 Automated Deployment

This project uses GitHub Actions for continuous deployment. Every push to the `main` branch triggers the deployment workflow (`.github/workflows/deploy.yml`), which automatically isolates the contents of the `public/` directory and publishes them to the live GitHub Pages site.

---

*This project demonstrates an automated research pipeline for evaluating API integrations at scale. It combines automated documentation analysis, verification workflows, structured datasets, and an interactive HTML case study to support integration prioritization for AI agents.*
