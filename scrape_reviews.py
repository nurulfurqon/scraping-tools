"""Scrape myBCA reviews from Play Store + App Store into one CSV."""
import argparse
import json
import urllib.request

import pandas as pd
from google_play_scraper import Sort, reviews

PLAY_ID = "com.bca.mybca.omni.android"
APPLE_ID = "1440241902"
COLUMNS = ["Tanggal", "Username", "Rating", "Isi_Ulasan", "Sumber"]


def scrape_play(count, lang="id", country="id", score=None):
    result, _ = reviews(
        PLAY_ID,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count,
        filter_score_with=score,
    )
    df = pd.DataFrame(result)[["at", "userName", "score", "content"]]
    df["Sumber"] = "Play Store"
    df.columns = COLUMNS
    return df


def parse_apple_feed(feed):
    """Apple's RSS puts app metadata in entry[0]; only entries with 'im:rating' are reviews."""
    entries = feed.get("feed", {}).get("entry", [])
    if isinstance(entries, dict):  # single-review pages come back unwrapped
        entries = [entries]
    return [
        {
            "Tanggal": e["updated"]["label"],
            "Username": e["author"]["name"]["label"],
            "Rating": int(e["im:rating"]["label"]),
            "Isi_Ulasan": e["content"]["label"],
            "Sumber": "App Store",
        }
        for e in entries
        if "im:rating" in e
    ]


def scrape_appstore(count, country="id"):
    # RSS feed caps at 10 pages x 50 reviews; no auth, no extra dependency.
    rows = []
    for page in range(1, 11):
        url = (
            f"https://itunes.apple.com/{country}/rss/customerreviews"
            f"/page={page}/id={APPLE_ID}/sortby=mostrecent/json"
        )
        with urllib.request.urlopen(url, timeout=30) as r:
            page_rows = parse_apple_feed(json.load(r))
        if not page_rows:
            break
        rows += page_rows
        if len(rows) >= count:
            break
    return pd.DataFrame(rows[:count], columns=COLUMNS)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--count", type=int, default=200, help="reviews per store")
    p.add_argument("--score", type=int, help="filter Play Store by rating 1-5")
    p.add_argument("--out", default="Review_myBCA.csv")
    a = p.parse_args()

    df = pd.concat(
        [scrape_play(a.count, score=a.score), scrape_appstore(a.count)],
        ignore_index=True,
    )
    df.to_csv(a.out, index=False)
    print(df["Sumber"].value_counts().to_string())
    print(f"Selesai -> {a.out} ({len(df)} ulasan)")


if __name__ == "__main__":
    main()
