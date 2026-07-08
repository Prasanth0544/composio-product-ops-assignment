import json
import csv
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import socket
import argparse
import time
import re
from concurrent.futures import ThreadPoolExecutor

JSON_PATH = os.path.join('data', 'apps_research.json')
CSV_PATH = os.path.join('data', 'apps_research.csv')

def load_database():
    """Loads the researched database from data/apps_research.json."""
    if not os.path.exists(JSON_PATH):
        print(f"Error: Database file {JSON_PATH} not found.")
        sys.exit(1)
    with open(JSON_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save_database(db):
    """Saves the database back to apps_research.json and updates the apps_research.csv copy."""
    os.makedirs('data', exist_ok=True)
    
    # Save JSON file
    with open(JSON_PATH, 'w', encoding='utf-8-sig') as f:
        json.dump(db, f, indent=4, ensure_ascii=False)
    
    # Save CSV file
    if db:
        headers = list(db[0].keys())
        with open(CSV_PATH, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(db)
    print("Agent Action: Database saved successfully in JSON and CSV formats.")

def check_link(url, timeout=3):
    """Pings a single URL to check if it returns a valid HTTP status code (200, 301, 302, etc.)."""
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

def validate_all_evidence_links(db):
    """Validates the first link of each evidence URL using ThreadPoolExecutor for fast execution."""
    print("Agent Action: Programmatically validating all 100 app evidence links...")
    links = [app.get("docs_url", app.get("website", "")) for app in db]
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_link, links))
        
    passed = sum(1 for r in results if r)
    print(f"Agent Verification Report: {passed}/{len(db)} links successfully verified/pinged.")
    return results

def search_ddg(query):
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

def run_research_loop(db):
    """Loops through all 100 apps to search for developer API references in a looped manner."""
    print("=== Starting Automated Research Loop for All 100 Apps ===")
    total = len(db)
    
    for index, app in enumerate(db):
        app_name = app.get("app_name")
        print(f"\n[{index+1}/{total}] Researching '{app_name}'...")
        
        # Query: App Developer API documentation
        query = f"{app_name} developer API documentation"
        links = search_ddg(query)
        
        if links:
            print(f" -> Found candidate documentation URLs:")
            for l in links[:3]:
                print(f"    - {l}")
            
            # Auto-enrich docs_url if it's missing or set to generic homepage
            current_docs = app.get("docs_url", "")
            current_website = app.get("website", "")
            
            if not current_docs or current_docs.strip() == current_website.strip():
                # Look for links containing 'dev', 'api', or 'doc'
                for l in links:
                    if any(k in l.lower() for k in ['dev', 'api', 'doc', 'github']):
                        app["docs_url"] = l
                        app["evidence_urls"] = l
                        print(f" -> Auto-enriched evidence URL to: {l}")
                        break
        else:
            print(" -> Search query yielded no results (rate limit or connection time-out).")
        
        # Standard delay to respect search server policies
        time.sleep(1.5)
        
    save_database(db)
    print("\n=== Automated Research Loop Completed ===")

def main():
    parser = argparse.ArgumentParser(description="Composio AI Product Ops Research Agent")
    parser.add_argument('--audit', action='store_true', help='Validate all evidence URLs using multithreaded ping checks')
    parser.add_argument('--app', type=str, help='Print detailed research data for a specific app')
    parser.add_argument('--update-field', nargs=3, metavar=('ID', 'FIELD', 'VALUE'), help='Programmatically update a field in the database')
    parser.add_argument('--research-loop', action='store_true', help='Execute an automated search loop across all 100 apps')
    
    args = parser.parse_args()
    db = load_database()
    
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
                else:
                    print(f"Error: Field '{field}' does not exist in schema.")
                    sys.exit(1)
        if not found:
            print(f"Error: App with ID {app_id} not found.")
            sys.exit(1)
            
        save_database(db)
        print(f"Success: Updated App {app_id} field '{field}' to '{value}'.")
        
    elif args.app:
        app_name = args.app.lower()
        matches = [app for app in db if app_name in app.get("app_name", "").lower()]
        if not matches:
            print(f"No apps found matching: {args.app}")
        for match in matches:
            print(json.dumps(match, indent=4))
            
    elif args.research_loop:
        run_research_loop(db)
        
    elif args.audit:
        validate_all_evidence_links(db)
        
    else:
        # Default behavior: run audit and save
        validate_all_evidence_links(db)
        save_database(db)

if __name__ == '__main__':
    main()
