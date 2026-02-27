import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import argparse
import sys
import os
import hashlib
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# --- Configuration ---

URL_REGEX = re.compile(
    r"""
    ['"] (?:https?://|//) [^\s'"]+ ['"] | 
    ['"] / [^\s'"]+ ['"]                  
    """, 
    re.VERBOSE
)

# --- Core Functions ---

def get_full_url(base_url, relative_url):
    """Joins a relative URL to the base URL, stripping quotes if present."""
    if relative_url.startswith(("'", '"')) and relative_url.endswith(("'", '"')):
        relative_url = relative_url[1:-1]
    return urljoin(base_url, relative_url)

def extract_js_links(js_content, base_url):
    """Uses regex to find potential URLs in the JavaScript content."""
    found_urls = set()
    matches = URL_REGEX.findall(js_content)
    
    for match in matches:
        absolute_url = get_full_url(base_url, match)
        parsed = urlparse(absolute_url)
        if parsed.scheme in ('http', 'https') and absolute_url not in found_urls:
            found_urls.add(absolute_url)
            
    return found_urls

def fetch_js_content(js_url):
    """Fetches the content of a single JavaScript file."""
    try:
        print(f"  -> Fetching JS: {js_url}")
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; ReconBot/1.0; +https://your.security.site)'}
        response = requests.get(js_url, timeout=10, headers=headers)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()
        if 'javascript' in content_type or 'text/plain' in content_type or len(response.text) > 0:
            return response.text
        return None
    except requests.RequestException as e:
        print(f"  -> Error fetching {js_url}: {e}")
        return None

def find_all_js_files(target_url):
    """Fetches the main page, finds all external JS file URLs."""
    print(f"🔍 Starting scrape on: {target_url}")
    js_urls = set()
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; ReconBot/1.0; +https://your.security.site)'}
        response = requests.get(target_url, timeout=10, headers=headers)
        response.raise_for_status() 
    except requests.RequestException as e:
        print(f"❌ Error fetching main page {target_url}: {e}")
        return js_urls

    soup = BeautifulSoup(response.text, 'html.parser')
    
    for script in soup.find_all('script', src=True): 
        relative_url = script['src']
        absolute_url = urljoin(target_url, relative_url)
        
        parsed = urlparse(absolute_url)
        if parsed.scheme in ('http', 'https'):
            js_urls.add(absolute_url)

    print(f"✅ Found {len(js_urls)} unique external JS files.")
    return js_urls

def process_extracted_links(urls, output_dir="screenshots"):
    """
    Visits URLs, captures status, and saves screenshots with readable URL filenames.
    """
    if not urls:
        return

    print(f"\n--- Checking Status and Taking Screenshots ({len(urls)} links) ---")
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        for url in urls:
            print(f"🌐 Visiting: {url}")
            try:
                # 1. Sanitize the URL for use as a filename
                # Removes http/https and replaces forbidden chars with underscores
                clean_name = re.sub(r'https?://', '', url)
                clean_name = re.sub(r'[^a-zA-Z0-9]', '%2F', clean_name)
                
                # Truncate if the URL is extremely long (OS filename limits are usually 255 chars)
                filename = f"{clean_name[:150]}.png"
                filepath = os.path.join(output_dir, filename)

                # 2. Navigate and capture
                response = page.goto(url, timeout=15000)
                status = response.status if response else "No Response"
                
                page.screenshot(path=filepath, full_page=False)
                print(f"  -> Status: {status} | Saved: {filename}")

            except PlaywrightTimeoutError:
                print(f"  -> Error: Connection timed out.")
            except Exception as e:
                print(f"  -> Error processing {url}: {e}")

        browser.close()

# --- Main Execution ---

def main():
    """Main function to orchestrate the scraping process."""
    parser = argparse.ArgumentParser(
        description="Ethical Security Tool: Scrapes a target URL, extracts JS files, searches for hidden URLs, and takes screenshots."
    )
    
    parser.add_argument(
        'target_url', 
        help='The full URL of the website to scrape (e.g., https://example.com).'
    )
    
    args = parser.parse_args()
    TARGET_URL = args.target_url
    
    if not TARGET_URL.startswith(('http://', 'https://')):
        print(f"❌ Error: Target URL must include the scheme (e.g., https://{TARGET_URL})")
        sys.exit(1)

    js_files = find_all_js_files(TARGET_URL)
    all_extracted_links = set()
    
    print("\n--- Extracting Links from JS Files ---")
    
    for js_url in js_files:
        js_content = fetch_js_content(js_url)
        
        if js_content:
            links_in_js = extract_js_links(js_content, js_url) 
            if links_in_js:
                print(f"  -> Found {len(links_in_js)} links in {js_url}")
                all_extracted_links.update(links_in_js)
            else:
                print(f"  -> No links found in {js_url}")
            
    print("\n--- Final List of All Extracted Links ---")
    if all_extracted_links:
        sorted_links = sorted(list(all_extracted_links))
        for link in sorted_links:
            print(link)
        print(f"\nTotal unique links found: {len(all_extracted_links)}")
        
        # Trigger the screenshot and status checking phase
        process_extracted_links(sorted_links)
    else:
        print("No links were extracted from any JavaScript files.")

if __name__ == "__main__":
    main()
