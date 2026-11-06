"""Minimal example: run the nonprofit-jobs-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keywords": "fundraising",
    "countries": ["GB", "US", "AU", "ES"],
    "maxItems": 50,
    "includeDescriptions": False,
}

run = client.actor("bibian/nonprofit-jobs-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    print(f"{item['title']} | {item.get('companyName')} | {item.get('locationLabel')} | {item.get('source')}")
print(f"{count} results")
