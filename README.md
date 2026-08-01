# myBCA Review Scraper

Pull myBCA app reviews from the Play Store + App Store and merge them into one CSV.

| Store | App ID | Data source |
|---|---|---|
| Play Store | `com.bca.mybca.omni.android` | `google-play-scraper` |
| App Store | `1440241902` | Apple's official RSS feed (no extra library) |

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install google-play-scraper pandas
```

## Usage

Run the script with the venv's Python — no need to activate the venv first:

```bash
.venv/bin/python scrape_reviews.py                                # 200 reviews per store -> Review_myBCA.csv
.venv/bin/python scrape_reviews.py --count 500                    # more reviews
.venv/bin/python scrape_reviews.py --score 1 --out complaints.csv # 1-star only (Play Store)
```

| Flag | Default | Description |
|---|---|---|
| `--count` | `200` | number of reviews **per store** |
| `--score` | – | filter by rating 1–5, Play Store only |
| `--out` | `Review_myBCA.csv` | output file |

Flags can be combined, e.g. `--count 500 --score 1 --out complaints.csv`.

On finish it prints the review count per store and the output path.

**Refreshing the data:** just run the script again. It overwrites `--out` in
place, so rename or move the old CSV first if you want to keep it.

## Output

Columns: `Tanggal`, `Username`, `Rating`, `Isi_Ulasan`, `Sumber`

## Notes

- App Store caps out around 500 reviews (Apple's RSS is limited to 10 pages × 50). Play Store is uncapped.
- Reviews come from the Indonesian storefront (`lang=id`, `country=id`).
- Tests: `.venv/bin/python test_scrape_reviews.py`
