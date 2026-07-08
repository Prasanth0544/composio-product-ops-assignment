# Composio AI Product Ops Intern Assignment - Complete Deliverables

This repository contains the dynamic research agent pipeline, verification tooling, compiled datasets, and the interactive case study web page for the take-home assignment.

---

## Folder Structure

```text
assignment-project/
  .github/
    workflows/
      deploy.yml              # GitHub Actions deployment workflow (GitHub Pages)
  data/
    apps_seed.csv             # 100 apps with category & starting urls
    apps_research.json        # Dynamic researched JSON database (100 apps)
    apps_research.csv         # Tabular CSV representation of the dataset
    verification_sample.csv   # QA audit sample (20 checked apps)
    verification_metrics.json # Programmatic accuracy stats computed by the verification script
  scripts/
    research_agent.py         # Dynamic CLI research agent with link verification
    verify_results.py         # QA validation tool (calculates accuracy scores & tracks fixes)
    build_case_study.py       # Compiler to build the case-study HTML webpage
    orchestrator.py           # Master Agent orchestrator (runs full pipeline or single stages)
  public/
    index.html                # Compiled premium interactive dashboard
  README.md                   # Complete repository instructions (this file)
  work_done.md                # Summary of accomplishments
  agent_architecture_plan.md  # Detailed architecture document for the OOP agent design
```

---

## Deliverables & Key Stats

- **100 Researched Apps**: Every app has 15 fields audited, including descriptions, authentication methods, self-serve credentials access, and Model Context Protocol (MCP) server support.
- **Calibrated Confidence Rating**: High (80) / Medium (20) / Low (0). No blank values remain.
- **Model Context Protocol (MCP)**: Identified 14 official MCP signals and 4 third-party/community MCP signals. Official labels are reserved for company or project-controlled evidence; reference/community servers are labeled separately.
- **Light Mint Case Study Dashboard**: Fully responsive light mint themed dashboard at `public/index.html` featuring interactive text search, category/verdict dropdown filters, buildability matrices, detailed audit mistake logs, **paginated 10-row views**, and a **Key Takeaways summary**.
- **Automated Deployments**: Integrates `.github/workflows/deploy.yml` to automatically build and deploy changes to GitHub Pages (`gh-pages` branch) on every push.
- **Verification Audit**: Analyzed a random 20-app sample.
  - **First-pass Accuracy**: 40.0%
  - **Final Accuracy On Checked Sample (After Calibration Loop)**: 100.0%

---

## Setup & Running the Scripts Locally

Ensure you have Python installed on your system.

### 1. Run the Link Audit & Regenerate Databases
To run the multithreaded link check across all 100 apps and synchronize the JSON and CSV databases:
```bash
python scripts/research_agent.py
```

### 2. Search or Update Specific Apps (CLI Agent)
To search for a specific app's checked attributes:
```bash
python scripts/research_agent.py --app Salesforce
```

To programmatically update a specific field in the JSON/CSV database (e.g., updating ID 50's confidence to 'High'):
```bash
python scripts/research_agent.py --update-field 50 confidence High
```

### 3. Compute QA Verification Accuracy
To analyze the 20-app verification sample, calculate sample accuracy metrics, and generate the metrics JSON payload:
```bash
python scripts/verify_results.py
```

### 4. Compile the HTML Case Study Dashboard
To read the compiled datasets and verification metrics, and regenerate the interactive dashboard webpage at `public/index.html`:
```bash
python scripts/build_case_study.py
```

### 5. Run the Integrated Master Agent Orchestrator (New)
You can run the entire OOP multi-stage pipeline or trigger specific stages sequentially using the central orchestrator:
* **Run full pipeline** (Research -> Verify -> Analytics & Compile):
  ```bash
  python scripts/orchestrator.py --run-all
  ```
* **Run only the Research stage**:
  ```bash
  python scripts/orchestrator.py --research
  ```
* **Run only the Verification stage**:
  ```bash
  python scripts/orchestrator.py --verify
  ```
* **Run only the Analytics & Report compilation stage**:
  ```bash
  python scripts/orchestrator.py --report
  ```

After running, simply open `public/index.html` in any web browser to view the interactive dashboard.
