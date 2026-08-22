import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

if not API_TOKEN:
    raise ValueError("BRIGHTDATA_API_TOKEN is missing from .env")


collection_id = input("Enter collection ID: ").strip()
source = input("Enter source name: ").strip().lower()

url = "https://api.brightdata.com/dca/dataset"

headers = {
    "Authorization": f"Bearer ef4b61a2-e888-4e1b-8b39-509977b501c7 ",
}

params = {
    "id": collection_id
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

print("Status Code:", response.status_code)

if response.status_code != 200:
    print("Response:", response.text)
    raise SystemExit(1)


lines = response.text.strip().splitlines()

records = []

for line in lines:

    if not line.strip():
        continue

    try:
        record = json.loads(line)
        records.append(record)

    except json.JSONDecodeError:
        print("WARNING: Could not parse one response line.")


output_file = Path("data/raw") / f"{source}.json"

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        records,
        file,
        indent=2,
        ensure_ascii=False
    )


print("--------------------------------")
print("DATA DOWNLOAD COMPLETE")
print("--------------------------------")
print(f"Source: {source}")
print(f"Records saved: {len(records)}")
print(f"Output: {output_file}")