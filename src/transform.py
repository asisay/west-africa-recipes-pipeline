# Clean and deduplicate data

# Use package-relative import so module resolves when importing `src` as a package
from .scrape import get_recipe_urls


def extract_titles(recipe_urls):
    titles = []
    seen = set()
    for recipe in recipe_urls:
        title = recipe.rstrip("/").split("/")[-1] # .rstrip("/") removes trailing slash
        clean_title = title.replace("-", " ").lower()

        if clean_title not in seen:
            titles.append(clean_title)
            seen.add(clean_title)

    return titles

def extract_raw_titles(recipe_urls):
    titles = []

    for recipe in recipe_urls:
        title = recipe.rstrip("/").split("/")[-1].replace("-", " ") # .rstrip("/") removes trailing slash
        titles.append(title)

    return titles

def build_data_structures(titles):
    dictionary_format = []
    database_format = []

    for title in titles:
        dictionary_format.append({"title": title, "title_length": len(title)})
        database_format.append((title, len(title),))

    return dictionary_format, database_format

if __name__ == "__main__":
    recipe_urls = get_recipe_urls()
    titles = extract_titles(recipe_urls)
    print(f"Finished extracting recipe titles: {titles}")
    dictionary_format, database_format = build_data_structures(titles)
    print(f"Converted cleaned titles into dictionary and database formats.")
    print(f"Dictionary format: {dictionary_format} Database format: {database_format}")