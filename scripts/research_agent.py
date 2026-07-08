import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor


class ResearchAgent:
  """Queries documentation pathways, validates URLs, and persists the app database."""

  def __init__(self, json_path=None, csv_path=None):
    self.json_path = json_path or os.path.join('data', 'apps_research.json')
    self.csv_path = csv_path or os.path.join('data', 'apps_research.csv')

  def load_database(self):
    """Loads the researched database from JSON."""
    if not os.path.exists(self.json_path):
      print(f"Error: Database file {self.json_path} not found.")
      sys.exit(1)
    with open(self.json_path, 'r', encoding='utf-8-sig') as f:
      return json.load(f)

  def save_database(self, db):
    """Preserves database entries to JSON and updates the CSV copy."""
    os.makedirs(os.path.dirname(self.json_path) or '.', exist_ok=True)

    with open(self.json_path, 'w', encoding='utf-8-sig') as f:
      json.dump(db, f, indent=4, ensure_ascii=False)

    if db:
      headers = list(db[0].keys())
      with open(self.csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(db)
    print("Agent Action: Database saved successfully in JSON and CSV formats.")

  def check_link(self, url, timeout=3):
    """Performs a concurrent ping to validate a single URL."""
    first_url = url.split(',')[0].strip()
    try:
      req = urllib.request.Request(
        first_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
      )
      with urllib.request.urlopen(req, timeout=timeout) as response:
        code = response.getcode()
        if code in [200, 301, 302, 201, 204]:
          return True
    except Exception:
      pass
    return False

  def validate_all_evidence_links(self, db):
    """Validates evidence URLs using ThreadPoolExecutor for fast execution."""
    print("Agent Action: Programmatically validating all 100 app evidence links...")
    links = [app.get("docs_url", app.get("website", "")) for app in db]

    with ThreadPoolExecutor(max_workers=20) as executor:
      results = list(executor.map(self.check_link, links))

    passed = sum(1 for r in results if r)
    print(f"Agent Verification Report: {passed}/{len(db)} links successfully verified/pinged.")
    return results

  def _search_ddg(self, query):
    """Performs a live DuckDuckGo HTML search and parses external links."""
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(
      url,
      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    )
    try:
      with urllib.request.urlopen(req, timeout=6) as response:
        html = response.read().decode('utf-8')
        hrefs = re.findall(r'href="([^"]+)"', html)
        clean_links = []
        for h in hrefs:
          if 'uddg=' in h:
            h = urllib.parse.unquote(h.split('uddg=')[1].split('&')[0])
          if h.startswith('http') and 'duckduckgo.com' not in h:
            if h not in clean_links:
              clean_links.append(h)
        return clean_links
    except Exception:
      return []

  def run_research_loop(self, db=None):
    """Queries official documentation pathways using search engines."""
    if db is None:
      db = self.load_database()

    print("=== Starting Automated Research Loop for All 100 Apps ===")
    total = len(db)

    for index, app in enumerate(db):
      app_name = app.get("app_name")
      print(f"\n[{index+1}/{total}] Researching '{app_name}'...")

      query = f"{app_name} developer API documentation"
      links = self._search_ddg(query)

      if links:
        print(" -> Found candidate documentation URLs:")
        for link in links[:3]:
          print(f"    - {link}")

        current_docs = app.get("docs_url", "")
        current_website = app.get("website", "")

        if not current_docs or current_docs.strip() == current_website.strip():
          for link in links:
            if any(k in link.lower() for k in ['dev', 'api', 'doc', 'github']):
              app["docs_url"] = link
              app["evidence_urls"] = link
              print(f" -> Auto-enriched evidence URL to: {link}")
              break
      else:
        print(" -> Search query yielded no results (rate limit or connection time-out).")

      time.sleep(1.5)

    self.save_database(db)
    print("\n=== Automated Research Loop Completed ===")

  def audit(self):
    """Default behavior: validate links and save the database."""
    db = self.load_database()
    self.validate_all_evidence_links(db)
    self.save_database(db)


def main():
  parser = argparse.ArgumentParser(description="Composio AI Product Ops Research Agent")
  parser.add_argument('--audit', action='store_true', help='Validate all evidence URLs using multithreaded ping checks')
  parser.add_argument('--app', type=str, help='Print detailed research data for a specific app')
  parser.add_argument('--update-field', nargs=3, metavar=('ID', 'FIELD', 'VALUE'), help='Programmatically update a field in the database')
  parser.add_argument('--research-loop', action='store_true', help='Execute an automated search loop across all 100 apps')

  args = parser.parse_args()
  agent = ResearchAgent()
  db = agent.load_database()

  if args.update_field:
    app_id = int(args.update_field[0])
    field = args.update_field[1]
    value = args.update_field[2]

    found = False
    for app in db:
      if app.get("id") == app_id:
        if field in app:
          app[field] = value
          found = True
          break
        print(f"Error: Field '{field}' does not exist in schema.")
        sys.exit(1)
    if not found:
      print(f"Error: App with ID {app_id} not found.")
      sys.exit(1)

    agent.save_database(db)
    print(f"Success: Updated App {app_id} field '{field}' to '{value}'.")

  elif args.app:
    app_name = args.app.lower()
    matches = [app for app in db if app_name in app.get("app_name", "").lower()]
    if not matches:
      print(f"No apps found matching: {args.app}")
    for match in matches:
      print(json.dumps(match, indent=4))

  elif args.research_loop:
    agent.run_research_loop(db)

  elif args.audit:
    agent.validate_all_evidence_links(db)

  else:
    agent.audit()


if __name__ == '__main__':
  main()
