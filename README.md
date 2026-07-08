# Composio AI Product Ops Intern Assignment - Complete Deliverables

This repository contains the dynamic research agent pipeline, verification tooling, compiled datasets, and the interactive case study web page for the take-home assignment.

---

## Folder Structure

```text
assignment-project/
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
  public/
    index.html                # Compiled premium interactive dashboard
  README.md                   # Complete repository instructions (this file)
  work_done.md                # Summary of accomplishments
```

---

## Deliverables & Key Stats

- **100 Researched Apps**: Every app has 15 fields audited, including descriptions, authentication methods, self-serve credentials access, and Model Context Protocol (MCP) server support.
- **Calibrated Confidence Rating**: High (83) / Medium (17) / Low (0). No blank values remain.
- **Model Context Protocol (MCP)**: Identified 10 platforms with official hosted/local MCP servers (including *Salesforce, Plain, Slack, Twilio, Otter AI, Consensus, Higgsfield, and Grain*) and verified community-maintained packages.
- **Aesthetic Case Study Dashboard**: Fully responsive dark-themed dashboard at `public/index.html` featuring interactive text search, category/verdict dropdown filters, buildability matrices, and detailed audit mistake logs.
- **Verification Audit**: Analyzed a random 20-app sample.
  - **First-pass Accuracy**: 40.0%
  - **Final Accuracy (After Calibration Loop)**: 100.0%

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
To analyze the verification sample, calculate accuracy metrics, and generate the metrics JSON payload:
```bash
python scripts/verify_results.py
```

### 4. Compile the HTML Case Study Dashboard
To read the compiled datasets and verification metrics, and regenerate the interactive dashboard webpage at `public/index.html`:
```bash
python scripts/build_case_study.py
```
After running, simply open `public/index.html` in any web browser to view the interactive dashboard.
