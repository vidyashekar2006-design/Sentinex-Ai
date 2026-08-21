import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

COLLECTORS = {
    "meesho": os.getenv("BRIGHTDATA_MEESHO_COLLECTOR_ID"),
    "deodap": os.getenv("BRIGHTDATA_DEODAP_COLLECTOR_ID"),
    "tradeindia": os.getenv("BRIGHTDATA_TRADEINDIA_COLLECTOR_ID"),
}

INPUT_URLS = {
    "meesho": "https://www.meesho.com/search?q=home%20tools&searchType=autosuggest&searchIdentifier=text_search",

    "deodap": "https://deodap.in/pages/search?q=tools%20and%20hardware",

    "tradeindia": "https://www.tradeindia.com/seller/industrial-supplies/",
}


if not API_TOKEN:
    raise ValueError("BRIGHTDATA_API_TOKEN is missing from .env")


source = input(
    "Enter source (meesho / deodap / tradeindia): "
).strip().lower()


if source not in COLLECTORS:
    raise ValueError("Invalid source name.")


collector_id = COLLECTORS[source]
input_url = INPUT_URLS[source]


if not collector_id:
    raise ValueError(
        f"Collector ID for {source} is missing from .env"
    )


if "PASTE_YOUR" in input_url:
    raise ValueError(
        f"Input URL for {source} has not been added yet."
    )


url = "https://api.brightdata.com/dca/trigger"

headers = {
    "Authorization": f"Bearer ef4b61a2-e888-4e1b-8b39-509977b501c7",
    "Content-Type": "application/json",
}

params = {
    "collector": collector_id,
    "queue_next": "1",
}

data = [
    {
        "url": input_url
    }
]

response = requests.post(
    url,
    headers=headers,
    params=params,
    json=data
)

print("Status Code:", response.status_code)
print("Response:", response.text)