import os
import time
import requests
from dotenv import load_dotenv

from self_healing_service import (
    mark_repair_requested,
    mark_repair_ready
)

load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")
COLLECTOR_ID = os.getenv("BRIGHTDATA_MEESHO_COLLECTOR_ID")

if not API_TOKEN:
    raise ValueError("BRIGHTDATA_API_TOKEN is missing from .env")

if not COLLECTOR_ID:
    raise ValueError("BRIGHTDATA_MEESHO_COLLECTOR_ID is missing from .env")


HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


def start_refactor(prompt):
    """Start a Bright Data self-healing/refactor job."""

    url = (
        f"https://api.brightdata.com/dca/collectors/"
        f"{COLLECTOR_ID}/refactor_template"
    )

    response = requests.post(
        url,
        headers=HEADERS,
        json={"prompt": prompt},
        timeout=60,
    )

    print("Refactor Status Code:", response.status_code)
    print("Refactor Response:", response.text)

    response.raise_for_status()

    mark_repair_requested()

    return response


def check_progress():
    """Check the current refactor job."""

    url = (
        f"https://api.brightdata.com/dca/collectors/"
        f"{COLLECTOR_ID}/refactor_template/progress"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=60,
    )

    print("\nProgress Status:", response.status_code)
    print("Progress Response:", response.text)

    if response.status_code != 200:
        return None

    try:
        return response.json()
    except ValueError:
        print("Progress response was not valid JSON.")
        return None


def wait_for_refactor():
    """Wait until Bright Data reaches the approval stage."""

    while True:

        progress = check_progress()

        if not progress:
            print("Could not read refactor progress.")
            return False

        status = progress.get("status")
        step = progress.get("step")

        print(f"Current status: {status}")
        print(f"Current step: {step}")

        if status == "pending_answer":
            print("\n✅ Refactor is ready for approval.")
            mark_repair_ready()
            return True

        if status == "error":
            print("\n❌ Bright Data reported an error.")
            return False

        print("Still processing... waiting 10 seconds.")
        time.sleep(10)


def main():

    print("=" * 60)
    print("SUPPLY WEBSHIELD - SELF HEALING CONTROLLER")
    print("=" * 60)

    print(f"\nCollector: {COLLECTOR_ID}")

    prompt = input(
        "\nDescribe the scraper problem: "
    ).strip()

    if not prompt:
        print("ERROR: Heal prompt cannot be empty.")
        return

    print("\nStarting Bright Data self-healing...")

    try:
        start_refactor(prompt)

    except requests.HTTPError as error:

        print("\n❌ Refactor request failed.")
        print(error)

        if "another refactor job is still in progress" in str(error):
            print(
                "\nAn existing refactor is already running."
                "\nDo NOT start another one."
                "\nOpen Bright Data Studio and finish the existing repair."
            )

        return

    except requests.RequestException as error:

        print("\n❌ Network/API error:")
        print(error)
        return

    ready = wait_for_refactor()

    if not ready:
        return

    print("\n" + "=" * 60)
    print("ACTION REQUIRED")
    print("=" * 60)

    print(
        "\nBright Data has generated a repair."
        "\nOpen the collector in Bright Data Studio."
        "\nReview the refactor changes."
        "\nAccept the changes if the repair is correct."
    )

    print(
        "\nAfter accepting the repair, run the scraper again."
    )
def run_self_healing(prompt):
    """
    Start Bright Data self-healing and wait until
    the repair is ready for manual approval.
    """

    print("\n" + "=" * 60)
    print("STARTING SELF-HEALING")
    print("=" * 60)

    print(f"Problem: {prompt}")

    try:
        start_refactor(prompt)
    except requests.HTTPError as error:
        print("\n❌ Refactor request failed.")
        print(error)
        return False

    return wait_for_refactor()    


if __name__ == "__main__":
    main()