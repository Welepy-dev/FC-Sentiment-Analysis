"""
Scrape ALL English reviews for a Steam app.

Paginates through the appreviews endpoint using the cursor field until
no more reviews are returned. Waits 3 seconds between requests to avoid
triggering rate limiting / bot detection.

Usage:
    python scrape_steam_reviews.py
"""

import requests
import json
import time

APP_ID = 3405690
OUTPUT_FILE = "reviews.json"
NUM_PER_PAGE = 100
REQUEST_DELAY_SECONDS = 3


def get_reviews_page(app_id, cursor="*", num_per_page=100):
    url = f"https://store.steampowered.com/appreviews/{app_id}"
    params = {
        "json": 1,
        "filter": "recent",        # paginates more reliably than filter=all for exhaustive scraping
        "language": "english",
        "review_type": "all",
        "purchase_type": "all",
        "num_per_page": num_per_page,
        "cursor": cursor,
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()


def scrape_all_reviews(app_id, num_per_page=100, delay=3, max_pages=1000):
    all_reviews = []
    cursor = "*"
    seen_cursors = set()
    page = 0

    while page < max_pages:
        page += 1
        data = get_reviews_page(app_id, cursor=cursor, num_per_page=num_per_page)

        if data.get("success") != 1:
            print(f"Request failed on page {page}: {data}")
            break

        reviews = data.get("reviews", [])
        if not reviews:
            print(f"No more reviews returned on page {page}. Stopping.")
            break

        all_reviews.extend(reviews)
        print(f"Page {page}: fetched {len(reviews)} reviews (total so far: {len(all_reviews)})")

        new_cursor = data.get("cursor")
        if not new_cursor or new_cursor in seen_cursors:
            print("Cursor did not advance. Reached end of results.")
            break
        seen_cursors.add(new_cursor)
        cursor = new_cursor

        # NOTE: we do NOT stop on partial pages -- Steam's API sometimes
        # returns fewer than num_per_page results even when more reviews
        # remain. Only an empty `reviews` list or a repeated cursor means
        # we're actually done.

        time.sleep(delay)

    return all_reviews


if __name__ == "__main__":
    reviews = scrape_all_reviews(APP_ID, num_per_page=NUM_PER_PAGE, delay=REQUEST_DELAY_SECONDS)

    print(f"\nDone. Total reviews fetched: {len(reviews)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT_FILE}")
