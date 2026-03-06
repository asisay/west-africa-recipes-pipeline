import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

"""
1. Get the sitemap
2. Extract all recipe URLs
3. Visit each recipe page
4. Extract structured recipe data
5. Save to JSON/CSV/database
"""
# This sitemaps blocks requests that look like they come from bots. Send a browser-like User-Agent header
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

def main():
    # Sitemap URL of the website to scrape
    sitemap_url = "https://www.africanbites.com/sitemap_index.xml"
    # sitemap_url = "https://www.africanbites.com/post-sitemap.xml"

    # Send an HTTP GET request to the website with header
    # This make the server thinks the request is coming from a normal browser instead of a bot
    index_response = requests.get(sitemap_url, headers=headers)

    print(index_response.status_code) # expect 200; 403 - blocked; 503 - rate limited
    print(index_response.text[:500])

    soup = BeautifulSoup(index_response.content, "xml")

    indexes = [loc.text for loc in soup.find_all("loc") if "post-sitemap" in loc.text]

    print(len(indexes))
    print(indexes[:5])

    recipe_urls = get_recipe_urls(indexes)
    # Scrape each recipe page to get title and ingredients
    recipes = scrape_recipe_url(recipe_urls)

    df = pd.DataFrame(recipes)
    print(df)

    return df


def get_recipe_urls(indexes):
    for post_sitemap in indexes:
        post_response = requests.get(post_sitemap, headers=headers)
        post_soup = BeautifulSoup(post_response.content, "xml")
        recipe_urls = [loc.text for loc in post_soup.find_all("loc") if "/wp-content/" not in loc.text]
        print(f"Found {len(recipe_urls)} recipes")
        print(recipe_urls[:5])
    
    return recipe_urls


def scrape_recipe_url(recipe_urls):
    recipes = []
    for url in recipe_urls[:20]:   # remove [:20] to scrape all
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        # Get recipe title
        title = soup.find("h1").text.strip()

        # Get all recipe ingredients
        ingredients = [i.text.strip() for i in soup.select(".wprm-recipe-ingredient")]

        recipes.append({
            "title": title,
            "url": url,
            "ingredients": ingredients
        })

        time.sleep(1)

    return recipes


if __name__ == "__main__":
    out = main()