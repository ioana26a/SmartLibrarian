import json

# Load the summaries from the JSON file
with open("data/book_summaries.json", "r", encoding="utf-8") as f:
    summaries = json.load(f)

def get_summary_by_title(title: str) -> str:
    """
    Returns the summary for a given book title.
    """
    normalized_title = title.strip()

    if normalized_title in summaries:
        return summaries[normalized_title].get("summary", "No detailed summary available.")
    else:
        return f"No summary found for the book '{title}'."
    

def get_all_titles():
    return list(summaries.keys())
