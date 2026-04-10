# Orchestrates everything
# scrape.py → get URLs
# transform.py → extract titles
# build_data_structures() → structure data

import os
import csv

from src.scrape import get_recipe_urls
from src.transform import extract_titles, extract_raw_titles, build_data_structures
from src.load import save_to_csv, save_raw_titles_to_csv

def main():
    # Get recipe URLs
    recipe_urls = get_recipe_urls()
    print(f"Fetched {len(recipe_urls)} URLs.")

    if not recipe_urls:
        print("No URLs fetched. Exiting pipeline.")
        return

    # Extract recipe titles
    titles = extract_titles(recipe_urls)
    print(f"Extracted {len(titles)} recipe titles.")

    raw_titles = extract_raw_titles(recipe_urls)
    print(f"Extracted {len(raw_titles)} raw recipe titles.")


    # Create structured data
    dicts, db_rows = build_data_structures(titles)

    # Check output
    print(f"Dictionary format: {dicts[:10]}")
    print(f"Database format: {db_rows[:10]}")

    # Save recipe titles to CSV file
    output_path = os.path.join("data", "processed", "recipes.csv")
    save_to_csv(dicts, output_path)
    print(f"Saved data to {output_path}")
    
    output_path = os.path.join("data", "raw", "recipes.csv")
    save_raw_titles_to_csv(raw_titles, output_path)
    print(f"Saved raw data to {output_path}")


if __name__ == "__main__":
    main()