import json
from pathlib import Path

import pandas as pd


RAW_FILE = Path("raw/reviews.json")
OUTPUT_FILE = Path("processed/reviews.csv")


def load_reviews(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def preprocess(reviews: list[dict]) -> pd.DataFrame:
    rows = []

    for review in reviews:
        text = review.get("review", "").strip()

        # Ignore reviews without text
        if not text:
            continue

        rows.append({
            "recommendation_id": review["recommendationid"],
            "review": text,
            "voted_up": review["voted_up"],
            "votes_up": review["votes_up"],
            "weighted_vote_score": review["weighted_vote_score"],
            "timestamp_created": review["timestamp_created"],
            "steam_purchase": review["steam_purchase"],
            "received_for_free": review["received_for_free"],
            "refunded": review["refunded"],
            "written_during_early_access": review["written_during_early_access"],
            "primarily_steam_deck": review["primarily_steam_deck"],
            "playtime_at_review": review["author"]["playtime_at_review"],
        })

    return pd.DataFrame(rows)


def main():
    reviews = load_reviews(RAW_FILE)

    print(f"Loaded {len(reviews):,} reviews")

    df = preprocess(reviews)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Processed {len(df):,} reviews")
    print(f"Removed {len(reviews) - len(df):,} empty reviews")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
