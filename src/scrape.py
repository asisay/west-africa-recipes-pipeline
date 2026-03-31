# Extract recipe URLs from sitemap

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

def get_recipe_urls():
    sitemap_url = "https://www.africanbites.com/sitemap_index.xml"
    recipe_urls = []
    
    # Configure the retry strategy
    retry_strategy = Retry(
        total=5, # Total number of retries
        backoff_factor=1, # Exponential backoff factor
        status_forcelist=[429, 500, 502, 503, 504], # Status codes to retry Too Many Requests, Server Errors, Bad Gateway, Service Unavailable, Gateway Timeout
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"] #
    )

    # Create an HTTPAdapter with the retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # Create a session and mount the adapter
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Send an HTTP GET request to the website with header
    # This make the server thinks the request is coming from a normal browser instead of a bot
    response = session.get(sitemap_url, headers=HEADERS, timeout=5)
    if response.status_code != 200:
        print("Failed to fetch sitemap")
        return []
    print(f"Fetched sitemap: {sitemap_url} (status {response.status_code})") # expect 200; 403 - blocked; 503 - rate limited

    soup = BeautifulSoup(response.content, "xml")

    # Step 1: find post sitemap; Get post-sitemaps that are found in sitemap index
    post_sitemap_urls = [loc.text for loc in soup.find_all("loc") if "post-sitemap" in loc.text]
    print(f"Fetched post sitemap: {post_sitemap_urls} (Number of URLs: {len(post_sitemap_urls)})")

    for post_sitemap in post_sitemap_urls:
        # Step 2: request it
        post_response = session.get(post_sitemap, headers=HEADERS, timeout=5)
        # Error handling
        if post_response.status_code != 200:
            continue

        # Step 3: extract URLs
        post_soup = BeautifulSoup(post_response.content, "xml")

        # Step 4: filter them
        # recipe_urls = [loc.text for loc in post_soup.find_all("loc") if "/wp-content/" not in loc.text] # Overwrites the list each time, so you only keep the last sitemap’s URLs.
        recipe_urls.extend(
            loc.text for loc in post_soup.find_all("loc")
            if "/wp-content/" not in loc.text
        )
    
    print(f"Found {len(recipe_urls)} recipes")
    
    return recipe_urls


if __name__ == "__main__":
    print(get_recipe_urls()[:10])