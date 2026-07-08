# AI Product Ops Intern Take-Home Assignment Guide

## 1. What This Assignment Is About

This take-home assignment is for an **AI Product Ops Intern** role at **Composio**.

Composio builds integrations that let AI agents use other software tools. For example, an AI agent might need to send a Slack message, create a HubSpot contact, read a Notion page, fetch Stripe payments, or open a GitHub issue. Before Composio builds support for an app, they need to understand whether that app has a useful API and whether developers can access it easily.

The assignment asks you to research **100 apps** and figure out how suitable each app is for becoming an **AI-agent-callable toolkit**.

The important part is not only collecting data. The real goal is to show that you can:

- Research APIs accurately.
- Use automation or agents to scale research.
- Find patterns across many apps.
- Verify your results honestly.
- Present everything clearly in one case-study page.

## 2. What You Need To Research For Each App

For every app in the list, you need to capture these fields:

| Field | What It Means |
|---|---|
| Category | The type of product, such as CRM, support, finance, ecommerce, or developer tooling. |
| What it does | A one-line explanation of the product. |
| Auth methods | How developers authenticate: OAuth2, API key, basic auth, bearer token, custom token, partner auth, etc. |
| Self-serve or gated | Whether a developer can sign up and get API credentials on their own, or whether access needs paid plans, admin approval, partnerships, or sales contact. |
| API surface | Whether the app has REST API, GraphQL API, SDKs, webhooks, MCP server, or only limited/no public API. |
| Buildability verdict | Whether Composio could build an AI-agent toolkit for it today. |
| Main blocker | The main reason it may be hard: gated API, paid plan, no public docs, unstable docs, narrow API, enterprise approval, etc. |
| Evidence | The official docs URL, developer portal, help article, or public documentation that supports your answer. |

## 3. What The Reviewer Actually Wants

The assignment says: **"Find the patterns. Do not just produce 100 rows."**

That means your final work should not only be a spreadsheet-style table. You should explain what the 100 apps reveal as a group.

Examples of useful patterns:

- Which auth method appears most often?
- Which categories are easiest to integrate?
- Which categories are mostly gated?
- Which apps are fast wins for Composio?
- Which apps require outreach or partnerships?
- Which apps already have MCP support?
- Which APIs are broad enough for useful agent actions?
- Which apps only have narrow APIs that are less useful?

Your final page should make the conclusion obvious quickly. A reviewer should understand the main findings in about **two minutes**.

## 4. You Must Use An Agent Or Script

The assignment explicitly asks you to do this **with an agent, not fully by hand**.

That means you should build some kind of automated research pipeline. It can be simple, but it should be real.

Possible pipeline:

1. Store the 100 apps in a structured file such as CSV, JSON, or YAML.
2. Use a script or agent to search official documentation pages.
3. Extract likely auth methods, API type, self-serve status, and evidence links.
4. Save the results into a structured output file.
5. Run verification checks on a sample.
6. Manually review errors and improve the pipeline.
7. Generate a final HTML case study from the results.

Using Composio's SDK or MCP would fit the spirit of the role, but the assignment allows a script or pipeline too.

When checking MCP support, be careful with wording. If you cannot find an official MCP server from the company or project, record **"No official MCP found"** instead of assuming one exists. If you find a community MCP server, label it as **"third-party/community MCP"**.

## 5. Verification Is Very Important

The assignment says accuracy matters most. So you should not pretend the agent is perfect.

You should sample part of the 100 apps and manually check the agent's answers against real docs.

A good verification section could include:

- Sample size, such as 20 out of 100 apps.
- What was checked: auth, self-serve status, API surface, evidence URL.
- First-pass accuracy, using your actual measured value. For example only: "72% correct before verification."
- Final accuracy after fixing errors, using your actual measured value. For example only: "91% correct on the checked sample."

Important: do not use example accuracy numbers in the final report. Measure the real sample results and report those numbers.
- Examples of mistakes the agent made.
- What verification loop improved the result.

Being honest about misses is a strength here. If an app is gated or unclear, say that clearly.

## 6. Final Deliverable

You need to submit:

1. A **live link** to a deployed HTML page or case study.
2. A **source repo link** with the research agent/script.
3. A short **README** explaining how to run the research agent.

The HTML page should include:

- Headline findings at the top.
- Pattern summary.
- Matrix or table of the 100 apps.
- Explanation of the research agent.
- Verification results.
- Evidence links.
- Honest notes about uncertain or gated apps.

## 7. Suggested Final Page Structure

Your final HTML case study could be structured like this:

1. **Headline**
   - Example: "Most requested agent integrations are buildable, but fintech and ads are heavily gated."

2. **Executive Summary**
   - 4-6 short bullets with the biggest findings.

3. **Pattern Dashboard**
   - Auth method distribution.
   - Self-serve vs gated count.
   - Buildable vs blocked count.
   - Category-level buildability.

4. **Easy Wins vs Outreach Needed**
   - Easy wins: apps with public docs, self-serve credentials, broad REST/GraphQL APIs.
   - Outreach needed: partner-gated, enterprise-only, unclear public API, or paid-only API access.

5. **Research Table**
   - All 100 apps with category, auth, API surface, buildability, blocker, and evidence URL.

6. **Agent Workflow**
   - What the agent/script did.
   - What sources it used.
   - Where a human had to step in.

7. **Verification**
   - Sampling method.
   - Accuracy before and after fixes.
   - Examples of corrected mistakes.

8. **Links**
   - Live page.
   - Source repo.
   - Data file.
   - Agent script.

## 8. Split The Work Into Three Parts

You can divide the assignment into **three separate workstreams** and combine them at the end into one final HTML case study.

This is a good approach because the assignment has three different kinds of work:

- Researching the 100 apps.
- Finding patterns and insights.
- Building the final page and proof of process.

Each part can be done separately, but all three should use the same shared data file so the final result is consistent.

### Part 1: Research And Data Collection

**Goal:** Build the raw research dataset for all 100 apps.

This part focuses on collecting accurate facts.

Tasks:

1. Create a structured data file, such as `apps_research.csv` or `apps_research.json`.
2. Add all 100 apps with their category and starting link.
3. For each app, research:
   - What the app does.
   - Auth method.
   - Self-serve or gated access.
   - API surface.
   - Existing MCP support, if any.
   - Buildability verdict.
   - Main blocker.
   - Evidence URL.
4. Prefer official docs, developer portals, API references, and help-center pages.
5. Mark confidence as high, medium, or low.

Source priority:

1. Official developer documentation.
2. Official API reference.
3. Official help center or support article.
4. Official company blog or changelog, if necessary.
5. Third-party blogs only when no official source exists, and mark confidence lower.

Confidence rules:

| Confidence | When To Use It |
|---|---|
| High | Official docs clearly confirm auth, API surface, access model, and evidence URL. |
| Medium | Official docs confirm most fields, but one field needs interpretation or is incomplete. |
| Low | Documentation is missing, unclear, outdated, third-party-only, or access is heavily gated. |

Output of Part 1:

- A complete dataset with 100 researched rows.
- Evidence links for each app.
- Notes for unclear or gated apps.

### Part 2: Agent, Automation And Verification

**Goal:** Show that the research was done with an agent or script, then verify that it is accurate.

This part proves that you did not manually fill a table without process.

Tasks:

1. Build a research script or agent that can process the app list.
2. Make the agent search official docs and extract likely answers.
3. Save the output into the shared dataset.
4. Run a verification sample, such as 15-25 apps.
5. Manually cross-check the sample against real documentation.
6. Record mistakes and corrections.
7. Calculate first-pass and final accuracy.

Output of Part 2:

- Agent/script code.
- README explaining how to run it.
- Verification notes.
- Accuracy summary.
- Examples of mistakes and fixes.

### Part 3: Patterns, Story And Final HTML Page

**Goal:** Turn the research into a clear case study that a reviewer can understand quickly.

This part is about product thinking and presentation.

Tasks:

1. Analyze the final dataset.
2. Count auth methods across all apps.
3. Count self-serve vs gated apps.
4. Group buildability by category.
5. Identify easy wins.
6. Identify apps needing outreach or partnerships.
7. Write the headline insight.
8. Build a single HTML page with:
   - Summary findings.
   - Pattern dashboard.
   - Category matrix.
   - Full research table.
   - Agent workflow.
   - Verification proof.

Output of Part 3:

- Final HTML case study.
- Visual summaries or tables.
- Clear recommendations.
- Deployed live link.

### Final Combine Step

At the end, combine the three parts into one complete submission.

Final combined deliverables:

| Combined Item | Comes From |
|---|---|
| `apps_research.csv` or `apps_research.json` | Part 1 |
| Research agent/script | Part 2 |
| Verification report | Part 2 |
| Final HTML case study | Part 3 |
| README | Parts 1, 2, and 3 |
| Live deployed link | Part 3 |
| Source repo link | All parts |

The final submission should feel like one polished project, even though the work was split into three parts.

Recommended folder structure:

```text
assignment-project/
  data/
    apps_seed.csv
    apps_research.csv
    verification_sample.csv
  scripts/
    research_agent.py
    verify_results.py
    build_case_study.py
  public/
    index.html
  README.md
```

Simple workflow:

```text
Part 1 creates the dataset
        ->
Part 2 improves and verifies the dataset
        ->
Part 3 turns the verified dataset into the final HTML case study
```

Automation pipeline diagram:

```text
apps.csv
   |
   v
Research Agent
   |
   v
Official Docs
   |
   v
Extract Data
   |
   v
Verification
   |
   v
Final Dataset
   |
   v
HTML Case Study
```
## 9. The 100 Apps And Starting Links

These are the apps from the assignment, grouped by category. The links below are starting points for research. For final evidence, prefer official developer documentation whenever possible.

### 1. CRM And Sales

| # | App | Starting Link |
|---:|---|---|
| 1 | Salesforce | <https://www.salesforce.com> |
| 2 | HubSpot | <https://www.hubspot.com> |
| 3 | Pipedrive | <https://www.pipedrive.com> |
| 4 | Attio | <https://www.attio.com> |
| 5 | Twenty | <https://twenty.com> |
| 6 | Podio | <https://www.podio.com> |
| 7 | Zoho CRM | <https://www.zoho.com/crm> |
| 8 | Close | <https://www.close.com> |
| 9 | Copper | <https://www.copper.com> |
| 10 | DealCloud | <https://api.docs.dealcloud.com> |

### 2. Support And Helpdesk

| # | App | Starting Link |
|---:|---|---|
| 11 | Zendesk | <https://www.zendesk.com> |
| 12 | Intercom | <https://www.intercom.com> |
| 13 | Freshdesk | <https://www.freshdesk.com> |
| 14 | Front | <https://www.front.com> |
| 15 | Pylon | <https://usepylon.com> |
| 16 | LiveAgent | <https://www.liveagent.com> |
| 17 | Plain | <https://www.plain.com> |
| 18 | Help Scout | <https://www.helpscout.com> |
| 19 | Gorgias | <https://www.gorgias.com> |
| 20 | Gladly | <https://www.gladly.com> |

### 3. Communications And Messaging

| # | App | Starting Link |
|---:|---|---|
| 21 | Slack | <https://www.slack.com> |
| 22 | Twilio | <https://www.twilio.com> |
| 23 | Zoho Cliq | <https://www.zoho.com/cliq> |
| 24 | Lark / Larksuite | <https://open.larksuite.com> |
| 25 | Pumble | <https://pumble.com> |
| 26 | Discord | <https://discord.com> |
| 27 | Telegram | <https://core.telegram.org> |
| 28 | WhatsApp Business | <https://developers.facebook.com/docs/whatsapp> |
| 29 | Aircall | <https://aircall.io> |
| 30 | Vonage | <https://developer.vonage.com> |

### 4. Marketing, Ads, Email And Social

| # | App | Starting Link |
|---:|---|---|
| 31 | Google Ads | <https://developers.google.com/google-ads> |
| 32 | Meta Ads | <https://developers.facebook.com/docs/marketing-apis> |
| 33 | LinkedIn Ads | <https://learn.microsoft.com/linkedin/marketing> |
| 34 | GoHighLevel | <https://highlevel.stoplight.io> |
| 35 | Mailchimp | <https://mailchimp.com/developer> |
| 36 | Klaviyo | <https://developers.klaviyo.com> |
| 37 | systeme.io | <https://systeme.io> |
| 38 | Pinterest | <https://developers.pinterest.com> |
| 39 | Threads | <https://developers.facebook.com/docs/threads> |
| 40 | SendGrid | <https://sendgrid.com> |

### 5. Ecommerce

| # | App | Starting Link |
|---:|---|---|
| 41 | Shopify | <https://shopify.dev> |
| 42 | WooCommerce | <https://woocommerce.com/document/woocommerce-rest-api> |
| 43 | BigCommerce | <https://developer.bigcommerce.com> |
| 44 | Salesforce Commerce Cloud | <https://developer.salesforce.com/docs/commerce> |
| 45 | Magento / Adobe Commerce | <https://developer.adobe.com/commerce> |
| 46 | Squarespace | <https://developers.squarespace.com> |
| 47 | Ecwid | <https://api-docs.ecwid.com> |
| 48 | Gumroad | <https://gumroad.com/api> |
| 49 | Amazon Selling Partner | <https://developer-docs.amazon.com/sp-api> |
| 50 | fanbasis | <https://fanbasis.com> |

### 6. Data, SEO And Scraping

| # | App | Starting Link |
|---:|---|---|
| 51 | DataForSEO | <https://docs.dataforseo.com> |
| 52 | SE Ranking | <https://seranking.com/api> |
| 53 | Ahrefs | <https://ahrefs.com/api> |
| 54 | MrScraper | <https://docs.mrscraper.com> |
| 55 | Apify | <https://docs.apify.com> |
| 56 | Firecrawl | <https://firecrawl.dev> |
| 57 | Bright Data | <https://brightdata.com> |
| 58 | Sherlock | <https://github.com/sherlock-project/sherlock> |
| 59 | Waterfall.io | <https://waterfall.io> |
| 60 | Clay | <https://clay.com> |

### 7. Developer, Infra And Data Platforms

| # | App | Starting Link |
|---:|---|---|
| 61 | GitHub | <https://docs.github.com/rest> |
| 62 | Vercel | <https://vercel.com/docs/rest-api> |
| 63 | Netlify | <https://docs.netlify.com/api> |
| 64 | Cloudflare | <https://developers.cloudflare.com/api> |
| 65 | Supabase | <https://supabase.com/docs> |
| 66 | Neo4j | <https://neo4j.com/docs/api> |
| 67 | Snowflake | <https://docs.snowflake.com> |
| 68 | MongoDB Atlas | <https://www.mongodb.com/docs/atlas/api> |
| 69 | Datadog | <https://docs.datadoghq.com/api> |
| 70 | Sentry | <https://docs.sentry.io/api> |

### 8. Productivity And Project Management

| # | App | Starting Link |
|---:|---|---|
| 71 | Notion | <https://developers.notion.com> |
| 72 | Airtable | <https://airtable.com/developers> |
| 73 | Linear | <https://developers.linear.app> |
| 74 | Jira | <https://developer.atlassian.com> |
| 75 | Asana | <https://developers.asana.com> |
| 76 | Monday.com | <https://developer.monday.com> |
| 77 | ClickUp | <https://clickup.com/api> |
| 78 | Coda | <https://coda.io/developers> |
| 79 | Smartsheet | <https://www.smartsheet.com/developers> |
| 80 | Harvest | <https://help.getharvest.com/api-v2> |

### 9. Finance And Fintech

| # | App | Starting Link |
|---:|---|---|
| 81 | Stripe | <https://stripe.com/docs/api> |
| 82 | Plaid | <https://plaid.com/docs> |
| 83 | Binance | <https://binance-docs.github.io> |
| 84 | Paygent Connect | <https://paygent.com> |
| 85 | iPayX | <https://ipayx.ai/docs> |
| 86 | QuickBooks | <https://developer.intuit.com> |
| 87 | Xero | <https://developer.xero.com> |
| 88 | Brex | <https://developer.brex.com> |
| 89 | Ramp | <https://docs.ramp.com> |
| 90 | PitchBook | <https://pitchbook.com> |

### 10. AI, Research And Media-Native

| # | App | Starting Link |
|---:|---|---|
| 91 | NotebookLM / Gemini Enterprise API | <https://cloud.google.com/gemini> |
| 92 | Otter AI | <https://help.otter.ai> |
| 93 | Fathom | <https://fathom.video> |
| 94 | Consensus | <https://consensus.app> |
| 95 | Reducto | <https://reducto.ai> |
| 96 | Devin | <https://docs.devin.ai> |
| 97 | Higgsfield | <https://higgsfield.ai/cli> |
| 98 | Mermaid CLI | <https://github.com/mermaid-js/mermaid-cli> |
| 99 | YouTube Transcript | <https://transcriptapi.com> |
| 100 | Grain | <https://grain.com> |

## 10. Recommended Research Data Columns

When you start collecting the actual research, use a table or CSV with these columns:

| Column | Example |
|---|---|
| id | 1 |
| category | CRM and Sales |
| app_name | Salesforce |
| website | https://www.salesforce.com |
| docs_url | https://developer.salesforce.com/docs |
| one_line_description | Enterprise CRM and sales platform. |
| auth_methods | OAuth2, JWT bearer flow |
| credential_access | Self-serve developer account, but production org access may require admin setup |
| self_serve_status | Self-serve / gated / mixed / unclear |
| api_surface | REST, SOAP, Bulk API, Streaming API, metadata APIs |
| mcp_available | Official MCP / third-party MCP / No official MCP found / unclear |
| buildability | Easy win / buildable / buildable with caveats / blocked |
| main_blocker | Enterprise admin setup |
| evidence_urls | Official docs links |
| confidence | High / medium / low |
| verification_notes | Manually checked auth docs and API overview |

## 11. Suggested Buildability Labels

Use consistent labels so the final analysis is easy to understand.

| Label | Meaning |
|---|---|
| Easy win | Public docs, self-serve credentials, broad API, clear auth. |
| Buildable | API exists and integration is possible, but there may be setup complexity. |
| Buildable with caveats | Useful API exists, but access, plan limits, or admin permissions may slow implementation. |
| Outreach needed | Public docs are limited or access requires partnership, approval, or sales contact. |
| Not currently buildable | No clear public API or not enough evidence to build confidently. |

## 12. How To Think About The Assignment

This assignment is basically testing whether you can be both:

- **Operational:** Can you collect accurate data across many apps quickly?
- **Product-minded:** Can you turn messy research into useful decisions?

Composio does not only need a list. They need to know where to spend engineering time.

So the strongest final answer will tell them:

- "Build these first."
- "These need manual outreach."
- "These categories are high-confidence."
- "These categories are risky."
- "Here is how the agent got the data."
- "Here is how I verified it."

That is the story your final HTML page should tell.



