import json
from pathlib import Path

from normalize import normalize_record
from validate import validate_record
from anomaly_detector import detect_price_anomalies
from schema_guard import check_schema
from heal_rules import should_trigger_healing
from heal_call import call_self_healing
from self_healing_service import (
    load_state,
    mark_healing_required,
    reset_to_idle
)


# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REJECTED_DIR = BASE_DIR / "data" / "rejected"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# THREE DATA SOURCES
# ==================================================

SOURCES = {
    "DeoDap": "deodap.json",
    "TradeIndia": "tradeindia.json",
    "Meesho": "meesho.json"
}


# ==================================================
# LOAD JSON FILE
# ==================================================

def load_json_file(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==================================================
# EXTRACT RECORDS FROM DIFFERENT JSON STRUCTURES
# ==================================================

def get_records(data):

    # JSON is directly a list
    if isinstance(data, list):
        return data

    # JSON is an object
    if isinstance(data, dict):

        # Common container names
        for key in ["data", "results", "records", "items"]:

            if isinstance(data.get(key), list):
                return data[key]

        # Treat the object itself as one record
        return [data]

    return []


# ==================================================
# DUPLICATE URL CHECK
# ==================================================

def check_duplicate_urls(records):

    seen_urls = set()
    duplicates = []

    for record in records:

        url = record.get("url")

        # Ignore records without URLs
        if not url:
            continue

        if url in seen_urls:

            duplicates.append(record)

        else:

            seen_urls.add(url)

    return duplicates


# ==================================================
# MAIN PIPELINE
# ==================================================

def main():

    print("=" * 60)
    print("SUPPLY WEBSHIELD - DATA INGESTION PIPELINE")
    print("=" * 60)

    print("\nProject folder:")
    print(BASE_DIR)

    print("\nRaw data folder:")
    print(RAW_DIR)

    # --------------------------------------------------
    # CHECK RAW FOLDER
    # --------------------------------------------------

    if not RAW_DIR.exists():

        print("\nERROR: data/raw folder does not exist.")
        print(f"Expected location: {RAW_DIR}")

        return

    # --------------------------------------------------
    # DATA CONTAINERS
    # --------------------------------------------------

    unified_data = []
    rejected_data = []

    source_stats = {}

    total_schema_warnings = 0

    # ==================================================
    # PROCESS EACH SOURCE
    # ==================================================

    for source, filename in SOURCES.items():

        print("\n" + "-" * 60)
        print(f"Processing source: {source}")

        file_path = RAW_DIR / filename

        print(f"Looking for: {file_path}")

        # --------------------------------------------------
        # CHECK FILE
        # --------------------------------------------------

        if not file_path.exists():

            print(f"WARNING: {filename} not found.")
            continue

        print("File found.")

        # --------------------------------------------------
        # LOAD FILE
        # --------------------------------------------------

        try:

            raw_data = load_json_file(file_path)

        except json.JSONDecodeError:

            print("ERROR: Invalid JSON file.")
            continue

        except Exception as error:

            print(f"ERROR loading file: {error}")
            continue

        # --------------------------------------------------
        # GET RECORDS
        # --------------------------------------------------

        records = get_records(raw_data)

        print(f"Records found: {len(records)}")

        # --------------------------------------------------
        # INITIALIZE SOURCE STATISTICS
        # --------------------------------------------------

        source_stats[source] = {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "schema_warnings": 0
        }

        # ==================================================
        # PROCESS EACH RECORD
        # ==================================================

        for record in records:

            # Ignore non-dictionary records
            if not isinstance(record, dict):

                continue

            # ----------------------------------------------
            # COUNT TOTAL
            # ----------------------------------------------

            source_stats[source]["total"] += 1

            # ----------------------------------------------
            # NORMALIZE
            # ----------------------------------------------

            normalized = normalize_record(
                record,
                source
            )

            # ----------------------------------------------
            # SCHEMA CHECK
            # ----------------------------------------------

            schema_issues = check_schema(normalized)

            if schema_issues:

                source_stats[source]["schema_warnings"] += 1
                total_schema_warnings += 1

                print("\n⚠️ SCHEMA WARNING")
                print(f"Source: {source}")

                for issue in schema_issues:

                    print(f"  - {issue}")

            # ----------------------------------------------
            # VALIDATE
            # ----------------------------------------------

            valid, issues = validate_record(
                normalized
            )

            # ----------------------------------------------
            # VALID RECORD
            # ----------------------------------------------

            if valid:

                unified_data.append(
                    normalized
                )

                source_stats[source]["valid"] += 1

            # ----------------------------------------------
            # INVALID RECORD
            # ----------------------------------------------

            else:

                rejected_data.append({
                    "record": normalized,
                    "issues": issues
                })

                source_stats[source]["invalid"] += 1

                print("\n⚠️ INVALID RECORD")

                print(
                    f"Source: {source}"
                )

                print(
                    f"Product: "
                    f"{normalized.get('product')}"
                )

                print("Problems:")

                for issue in issues:

                    print(
                        f"  - {issue}"
                    )

    # ==================================================
    # DUPLICATE CHECK
    # ==================================================

    duplicates = check_duplicate_urls(
        unified_data
    )

    print("\n")
    print("=" * 60)
    print("DUPLICATE CHECK")
    print("=" * 60)

    if duplicates:

        print(
            f"Duplicate URLs found: "
            f"{len(duplicates)}"
        )

    else:

        print("Duplicate URLs found: 0")

    # ==================================================
    # PRICE ANOMALY DETECTION
    # ==================================================

    print("\n")
    print("=" * 60)
    print("PRICE ANOMALY DETECTION")
    print("=" * 60)

    price_anomalies = detect_price_anomalies(
        unified_data
    )

    print(
        f"Price anomalies detected: "
        f"{len(price_anomalies)}"
    )

    for anomaly in price_anomalies:

        print("\n⚠️ PRICE ANOMALY")

        print(
            f"Source: "
            f"{anomaly.get('source')}"
        )

        print(
            f"Product: "
            f"{anomaly.get('product')}"
        )

        print(
            f"Price: "
            f"{anomaly.get('price')}"
        )

        print(
            f"Source median: "
            f"{anomaly.get('median_source_price')}"
        )

        print(
            f"Reason: "
            f"{anomaly.get('reason')}"
        )

        # ==================================================
# SELF-HEALING DECISION
# ==================================================

    print("\n")
    print("=" * 60)
    print("SELF-HEALING CHECK")
    print("=" * 60)

# Check every scraper independently.
# A failure in one source should not be hidden
# by healthy records from other sources.

    source_healing_results = {}

    for source, stats in source_stats.items():

        source_total = stats["total"]
        source_invalid = stats["invalid"]
        source_schema_warnings = stats["schema_warnings"]

        source_healing_needed, source_healing_reason = (
            should_trigger_healing(
            source_total,
            source_invalid,
            source_schema_warnings,
            0
        )
    )

        source_healing_results[source] = {
        "needed": source_healing_needed,
        "reason": source_healing_reason,
        "total_records": source_total,
        "invalid_records": source_invalid,
        "schema_warnings": source_schema_warnings
    }

        print(f"\nSource: {source}")
        print(
        f"Total records: {source_total}"
    )
        print(
        f"Invalid records: {source_invalid}"
    )

        if source_healing_needed:

            print("⚠️ HEALING REQUIRED")
            print(
            f"Reason: {source_healing_reason}"
        )

        else:

            print("✅ HEALTHY")
            print(
            f"Reason: {source_healing_reason}"
        )


# Find sources that require healing

    failed_sources = [
        source
        for source, result
        in source_healing_results.items()
        if result["needed"]
]


# Overall pipeline decision

    healing_needed = len(failed_sources) > 0

    if healing_needed:

        failed_source = failed_sources[0]

        healing_reason = (
            source_healing_results[
            failed_source
        ]["reason"]
    )

    else:

        failed_source = None

    healing_reason = (
        "All scraper sources appear healthy."
    )


# Overall statistics are still preserved
# for the scraper health report.

    total_records = sum(
    stats["total"]
    for stats in source_stats.values()
)

    invalid_records = sum(
    stats["invalid"]
    for stats in source_stats.values()
)

    schema_warning_count = sum(
    stats["schema_warnings"]
    for stats in source_stats.values()
)
    # ==================================================
# SELF-HEALING STATE
# ==================================================

    if healing_needed:

        print("\n⚠️ SELF-HEALING REQUIRED")
        print(f"Failed source: {failed_source}")
        print(f"Reason: {healing_reason}")

    # Load existing healing state before creating
    # another Bright Data repair request.
        existing_state = load_state()

    # If healing is already in progress, do not
    # trigger Bright Data repeatedly.
        active_healing_states = [
        "healing_required",
        "repair_requested",
        "repair_ready"
    ]

        if existing_state.get("status") in active_healing_states:

            print(
            "\nSelf-healing workflow already active."
        )

            print(
            f"Current status: "
            f"{existing_state.get('status')}"
        )

            healing_state = existing_state

        else:

        # Record that healing is required.
            healing_state = mark_healing_required(
            reason=healing_reason,
            source=failed_source
        )

            print("\nSelf-healing state recorded.")

            print(
            "Starting Bright Data "
            "self-healing workflow..."
        )

        # Trigger the real Bright Data
        # self-healing controller.
            result = call_self_healing(
            healing_reason
        )

        # Reload state because the controller may
        # have updated it to repair_requested or
        # repair_ready.
            healing_state = load_state()

            print("\nSelf-healing trigger result:")
            print(result)

    else:

        print("\n✅ SCRAPER HEALTHY")
        print(f"Reason: {healing_reason}")

        existing_state = load_state()

    # Preserve a successful healing state so the
    # dashboard can show that recovery occurred.
        if existing_state.get("status") == "healed":

            healing_state = existing_state

        else:

            healing_state = reset_to_idle()


    print("\nSelf-healing state:")

    print(
    json.dumps(
        healing_state,
        indent=2,
        ensure_ascii=False
    )
)
        # ==================================================
    # SAVE SCRAPER HEALTH REPORT
    # ==================================================

    health_report = {
        "status": "healing_required" if healing_needed else "healthy",
        "reason": healing_reason,

        "total_records": total_records,
        "valid_records": len(unified_data),
        "invalid_records": invalid_records,

        "schema_warnings": schema_warning_count,
        "duplicate_urls": len(duplicates),
        "price_anomalies": len(price_anomalies),

        "self_healing": {
    "needed": healing_needed,
    "reason": healing_reason,
    "status": healing_state["status"],
    "source": healing_state["source"],
    "healing_started_at": healing_state["healing_started_at"],
    "repair_ready_at": healing_state["repair_ready_at"],
    "healed_at": healing_state["healed_at"],
    "self_healed_count": healing_state["self_healed_count"]
},

        "sources": source_stats
    }

    health_file = (
        PROCESSED_DIR /
        "scraper_health.json"
    )

    with open(
        health_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            health_report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nScraper health report:")
    print(health_file)
     

     
    # ==================================================
    # SAVE ANOMALY REPORT
    # ==================================================

    anomaly_file = (
        REJECTED_DIR /
        "price_anomalies.json"
    )

    with open(
        anomaly_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            price_anomalies,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        "\nAnomaly report:"
    )

    print(anomaly_file)

    # ==================================================
    # SAVE VALID / TRUSTED DATA
    # ==================================================

    output_file = (
        PROCESSED_DIR /
        "unified_supply_data.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            unified_data,
            file,
            indent=2,
            ensure_ascii=False
        )

    # ==================================================
    # SAVE INVALID DATA
    # ==================================================

    rejected_file = (
        REJECTED_DIR /
        "invalid_records.json"
    )

    with open(
        rejected_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            rejected_data,
            file,
            indent=2,
            ensure_ascii=False
        )

    # ==================================================
    # SOURCE STATISTICS
    # ==================================================

    print("\n")
    print("=" * 60)
    print("SOURCE STATISTICS")
    print("=" * 60)

    for source, stats in source_stats.items():

        print(f"\n{source}")

        print(
            f"  Total           : "
            f"{stats['total']}"
        )

        print(
            f"  Valid           : "
            f"{stats['valid']}"
        )

        print(
            f"  Invalid         : "
            f"{stats['invalid']}"
        )

        print(
            f"  Schema warnings : "
            f"{stats['schema_warnings']}"
        )

    # ==================================================
    # FINAL REPORT
    # ==================================================

    print("\n")
    print("=" * 60)
    print("INTEGRATION COMPLETE")
    print("=" * 60)

    print(
        f"Sources processed : "
        f"{len(source_stats)}"
    )

    print(
        f"Trusted records   : "
        f"{len(unified_data)}"
    )

    print(
        f"Rejected records  : "
        f"{len(rejected_data)}"
    )

    print(
        f"Duplicate URLs    : "
        f"{len(duplicates)}"
    )

    print(
        f"Schema warnings   : "
        f"{total_schema_warnings}"
    )

    print(
        f"Price anomalies   : "
        f"{len(price_anomalies)}"
    )

    print("\nTrusted data:")
    print(output_file)

    print("\nRejected data:")
    print(rejected_file)

    print("\nAnomaly report:")
    print(anomaly_file)

    print("=" * 60)


# ==================================================
# PROGRAM ENTRY POINT
# ==================================================

if __name__ == "__main__":

    main()