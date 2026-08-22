import os
import time
import requests
from dotenv import load_dotenv


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")
COLLECTOR_ID = os.getenv("BRIGHTDATA_MEESHO_COLLECTOR_ID")


if not API_TOKEN:
    raise ValueError("BRIGHTDATA_API_TOKEN is missing from .env")

if not COLLECTOR_ID:
    raise ValueError("BRIGHTDATA_MEESHO_COLLECTOR_ID is missing from .env")


# ==========================================
# 2. GET THE HEALING PROMPT
# ==========================================

prompt = input("Describe the scraper problem: ").strip()

if not prompt:
    raise ValueError("Heal prompt cannot be empty")

if len(prompt) > 1000:
    raise ValueError("Heal prompt must be 1000 characters or less")


# ==========================================
# 3. TRIGGER SELF-HEALING
# ==========================================

refactor_url = (
    f"https://api.brightdata.com/dca/collectors/"
    f"{COLLECTOR_ID}/refactor_template"
)

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

refactor_data = {
    "prompt": prompt
}

print("\nStarting self-healing...")

response = requests.post(
    refactor_url,
    headers=headers,
    json=refactor_data
)

print("Trigger Status:", response.status_code)
print("Trigger Response:", response.text)


if response.status_code != 200:
    raise RuntimeError(
        "Failed to trigger Bright Data self-healing."
    )


# ==========================================
# 4. POLL SELF-HEALING PROGRESS
# ==========================================

progress_url = (
    f"https://api.brightdata.com/dca/collectors/"
    f"{COLLECTOR_ID}/refactor_template/progress"
)

print("\nWaiting for Bright Data to finish the refactor...")


while True:

    progress_response = requests.get(
        progress_url,
        headers={
            "Authorization": f"Bearer {API_TOKEN}"
        }
    )

    print("\nProgress Status:", progress_response.status_code)
    print("Progress Response:", progress_response.text)

    if progress_response.status_code != 200:
        raise RuntimeError(
            "Could not retrieve self-healing progress."
        )

    try:
        progress_data = progress_response.json()

    except ValueError:
        raise RuntimeError(
            "Bright Data returned an invalid JSON response."
        )

    status = progress_data.get("status")
    step = progress_data.get("step")

    print("Current status:", status)
    print("Current step:", step)

    # --------------------------------------
    # READY FOR APPROVAL
    # --------------------------------------

    if status == "pending_answer":

        print("\n✅ Refactor is ready for approval!")

        preview = progress_data.get("preview_result")

        if preview:
            print("\nPreview result:")
            print(preview)

        break

    # --------------------------------------
    # ERROR
    # --------------------------------------

    if status == "error":

        print("\n❌ Bright Data reported an error.")

        print(
            "Full progress response:",
            progress_response.text
        )

        raise RuntimeError(
            "Self-healing failed."
        )

    # --------------------------------------
    # STILL RUNNING
    # --------------------------------------

    print("Waiting 10 seconds...")

    time.sleep(10)


# ==========================================
# 5. APPROVE / RESUME THE HEALING JOB
# ==========================================

resume_url = (
    f"https://api.brightdata.com/dca/collectors/"
    f"{COLLECTOR_ID}/resume_automation_job"
)

print("\nApproving the proposed refactor...")


resume_response = requests.post(
    resume_url,
    headers={
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
)

print("Approval Status:", resume_response.status_code)
print("Approval Response:", resume_response.text)


if resume_response.status_code != 200:
    raise RuntimeError(
        "Failed to approve/resume the self-healing job."
    )


print("\n🎉 Self-healing workflow completed successfully!")