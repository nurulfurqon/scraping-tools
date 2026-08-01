from scrape_reviews import parse_apple_feed

FEED = {
    "feed": {
        "entry": [
            {"im:name": {"label": "myBCA"}},  # metadata entry, must be dropped
            {
                "updated": {"label": "2026-07-30T10:00:00-07:00"},
                "author": {"name": {"label": "budi"}},
                "im:rating": {"label": "2"},
                "content": {"label": "sering error"},
            },
        ]
    }
}

rows = parse_apple_feed(FEED)
assert len(rows) == 1, rows
assert rows[0]["Rating"] == 2 and rows[0]["Username"] == "budi"
assert parse_apple_feed({"feed": {}}) == []
assert len(parse_apple_feed({"feed": {"entry": FEED["feed"]["entry"][1]}})) == 1
print("ok")
