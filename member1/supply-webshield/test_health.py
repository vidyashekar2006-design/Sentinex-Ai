import json

from validator.health import calculate_field_health
from validator.breakage import detect_breakage
from validator.recovery import (
    compare_health,
    recovery_successful
)


FIELDS = [
    "current_price",
    "brand",
    "availability",
    "product_page_url"
]


# ----------------------------------------
# Load yesterday's scrape
# ----------------------------------------

with open(
    "data/croma_products_2026-08-17.json",
    "r",
    encoding="utf-8"
) as file:

    yesterday_products = json.load(file)


# ----------------------------------------
# Load today's scrape
# ----------------------------------------

with open(
    "data/croma_products_2026-08-18.json",
    "r",
    encoding="utf-8"
) as file:

    today_products = json.load(file)


# ----------------------------------------
# Calculate health
# ----------------------------------------

yesterday_health = calculate_field_health(
    yesterday_products,
    FIELDS
)

today_health = calculate_field_health(
    today_products,
    FIELDS
)


# ----------------------------------------
# Display results
# ----------------------------------------

print("\n===== YESTERDAY =====")

for field, value in yesterday_health.items():
    print(f"{field}: {value}%")


print("\n===== TODAY =====")

for field, value in today_health.items():
    print(f"{field}: {value}%")


# ----------------------------------------
# Detect possible breakage
# ----------------------------------------

breakages = detect_breakage(
    yesterday_health,
    today_health,
    threshold=30
)


print("\n===== BREAKAGE DETECTION =====")

if breakages:

    print("🚨 POSSIBLE SCRAPER BREAKAGE")

    for field, details in breakages.items():

        print(f"\nField: {field}")
        print(f"Previous: {details['previous']}%")
        print(f"Current: {details['current']}%")
        print(f"Drop: {details['drop']}%")

else:

    print("🟢 No significant scraper breakage detected")


# ----------------------------------------
# Recovery comparison
# ----------------------------------------

recovery_results = compare_health(
    yesterday_health,
    today_health
)


print("\n===== RECOVERY COMPARISON =====")

for field, data in recovery_results.items():

    print(f"\nField: {field}")
    print(f"Baseline: {data['baseline']}%")
    print(f"Current: {data['current']}%")
    print(f"Recovery: {data['recovery']}%")


# ----------------------------------------
# Recovery status
# ----------------------------------------

success = recovery_successful(
    recovery_results
)


print("\n===== STATUS =====")

if success:

    print("🟢 DATA HEALTH IS GOOD")

else:

    print("🔴 DATA HEALTH IS BELOW EXPECTED LEVEL")