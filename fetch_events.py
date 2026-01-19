#!/usr/bin/env python3
"""
Fetch events data from Hasura endpoint and save to data.json.
"""

import json
import ssl
import urllib.request
import urllib.error
from pathlib import Path

HASURA_ENDPOINT = "https://hasura.bi.status.im/api/rest/circle/events"
OUTPUT_FILE = Path(__file__).parent / "data.json"


def fetch_events():
    """Fetch events from Hasura endpoint."""
    req = urllib.request.Request(
        HASURA_ENDPOINT,
        headers={"Accept": "application/json"}
    )

    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
                return json.loads(response.read().decode("utf-8"))
        raise


def save_data(data):
    """Save data to JSON file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {OUTPUT_FILE}")


def main():
    try:
        print(f"Fetching events from {HASURA_ENDPOINT}...")
        data = fetch_events()
        save_data(data)
        print("Done!")
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
