from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
import json


# ============================================================
# SUPPLYSHIELD AI - REAL MEMBER 1 SCRAPER HEALTH SERVICE
# ============================================================
#
# This service reads the actual outputs produced by:
#
# member1/supply-webshield/main.py
#
# It does NOT create fake scraper statistics.
#
# Sources:
#   - DeoDap
#   - TradeIndia
#   - Meesho
#
# ============================================================


# ============================================================
# PROJECT PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]

PROJECT_ROOT = BACKEND_DIR.parent

MEMBER1_DIR = (
    PROJECT_ROOT
    / "member1"
    / "supply-webshield"
)

RAW_DIR = MEMBER1_DIR / "data" / "raw"

PROCESSED_DIR = MEMBER1_DIR / "data" / "processed"

REJECTED_DIR = MEMBER1_DIR / "data" / "rejected"


UNIFIED_DATA_FILE = (
    PROCESSED_DIR
    / "unified_supply_data.json"
)

INVALID_DATA_FILE = (
    REJECTED_DIR
    / "invalid_records.json"
)

PRICE_ANOMALY_FILE = (
    REJECTED_DIR
    / "price_anomalies.json"
)

SELF_HEALING_STATUS_FILE = (
    PROCESSED_DIR
    / "self_healing_status.json"
)


# ============================================================
# REAL MEMBER 1 SOURCES
# ============================================================

SCRAPER_SOURCES = [
    {
        "name": "DeoDap",
        "file": "deodap.json",
    },
    {
        "name": "TradeIndia",
        "file": "tradeindia.json",
    },
    {
        "name": "Meesho",
        "file": "meesho.json",
    },
]


# ============================================================
# JSON HELPERS
# ============================================================

def load_json(path: Path, default):

    try:

        if not path.exists():
            return default

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return default


# ============================================================
# GET RECORDS FROM DIFFERENT JSON STRUCTURES
# ============================================================

def extract_records(data):

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        for key in [
            "data",
            "results",
            "records",
            "items"
        ]:

            value = data.get(key)

            if isinstance(value, list):
                return value

        return [data]

    return []


# ============================================================
# LOAD MEMBER 1 OUTPUTS
# ============================================================

def load_unified_data() -> List[Dict]:

    data = load_json(
        UNIFIED_DATA_FILE,
        []
    )

    return extract_records(data)


def load_invalid_data() -> List[Dict]:

    data = load_json(
        INVALID_DATA_FILE,
        []
    )

    return extract_records(data)


def load_price_anomalies() -> List[Dict]:

    data = load_json(
        PRICE_ANOMALY_FILE,
        []
    )

    return extract_records(data)

def load_self_healing_status() -> Dict:
    """
    Load the real persistent self-healing state
    produced by Member 1.
    """

    data = load_json(
        SELF_HEALING_STATUS_FILE,
        {}
    )

    if not isinstance(data, dict):
        return {}

    return data

    # ============================================================
# APPLY SELF-HEALING STATE TO SOURCE HEALTH
# ============================================================

def apply_self_healing_state(
    sources: List[Dict],
    self_healing_state: Dict
) -> List[Dict]:

    healing_status = str(
        self_healing_state.get(
            "status",
            "idle"
        )
    ).lower()

    affected_source = self_healing_state.get(
        "source"
    )

    if not affected_source:
        return sources

    for source in sources:

        if (
            source["name"].lower()
            ==
            str(affected_source).lower()
        ):

            # ------------------------------------------------
            # FAILURE / HEALING IN PROGRESS
            # ------------------------------------------------

            if healing_status in [
                "failed",
                "failure",
                "healing",
                "repairing"
            ]:

                source["status"] = "failed"

            # ------------------------------------------------
            # HEALED
            # ------------------------------------------------

            elif healing_status == "healed":

                source["status"] = "healthy"

    return sources


# ============================================================
# COUNT SOURCE RECORDS
# ============================================================

def count_source_records(
    source_name: str,
    records: List[Dict]
) -> int:

    count = 0

    for record in records:

        if not isinstance(record, dict):
            continue

        if record.get("source") == source_name:

            count += 1

    return count


# ============================================================
# COUNT INVALID SOURCE RECORDS
# ============================================================

def count_invalid_source_records(
    source_name: str,
    records: List[Dict]
) -> int:

    count = 0

    for item in records:

        if not isinstance(item, dict):
            continue

        # Member 1 stores invalid records like:
        #
        # {
        #     "record": {...},
        #     "issues": [...]
        # }

        record = item.get(
            "record",
            item
        )

        if not isinstance(record, dict):
            continue

        if record.get("source") == source_name:

            count += 1

    return count


# ============================================================
# COUNT SOURCE ANOMALIES
# ============================================================

def count_source_anomalies(
    source_name: str,
    anomalies: List[Dict]
) -> int:

    count = 0

    for anomaly in anomalies:

        if not isinstance(anomaly, dict):
            continue

        if anomaly.get("source") == source_name:

            count += 1

    return count


# ============================================================
# GET SOURCE STATUS
# ============================================================

def get_source_status(
    source_name: str,
    total: int,
    valid: int,
    invalid: int,
    anomalies: int
) -> str:

    # No records means the source could not currently
    # provide usable data.

    if total == 0:

        return "failed"

    # Invalid records are allowed, but if everything
    # from a source was rejected, mark it failed.

    if valid == 0 and invalid > 0:

        return "failed"

    # Anomalies do not automatically mean scraper failure.
    #
    # They are data-quality / market signals.

    return "healthy"


# ============================================================
# GET SCRAPER SOURCES
# ============================================================

def get_scraper_sources() -> List[Dict]:

    unified_data = load_unified_data()

    invalid_data = load_invalid_data()

    anomalies = load_price_anomalies()

    sources = []

    for source in SCRAPER_SOURCES:

        name = source["name"]

        raw_file = (
            RAW_DIR
            / source["file"]
        )

        total = len(
            extract_records(
                load_json(
                    raw_file,
                    []
                )
            )
        )

        valid = count_source_records(
            name,
            unified_data
        )

        invalid = count_invalid_source_records(
            name,
            invalid_data
        )

        source_anomalies = count_source_anomalies(
            name,
            anomalies
        )

        status = get_source_status(
            name,
            total,
            valid,
            invalid,
            source_anomalies
        )

        sources.append({

            "name": name,

            "status": status,

            "records": total,

            "valid": valid,

            "invalid": invalid,

            "schema_warnings": 0,

            "price_anomalies": source_anomalies,

            "data_source": "Member 1 pipeline",

            "file": source["file"],

        })

    return sources


# ============================================================
# CALCULATE HEALTH
# ============================================================

def get_scraper_health() -> Dict:

    # -----------------------------------------------------
    # LOAD SCRAPER SOURCES
    # -----------------------------------------------------

    sources = get_scraper_sources()

    # -----------------------------------------------------
    # LOAD REAL SELF-HEALING STATE
    # -----------------------------------------------------

    self_healing_state = load_self_healing_status()

    healing_status = str(
        self_healing_state.get(
            "status",
            "idle"
        )
    ).lower()

    healing_source = self_healing_state.get(
        "source"
    )

    # -----------------------------------------------------
    # APPLY FAILURE / HEALING STATE
    # -----------------------------------------------------

    if (
        healing_source
        and healing_status in [
            "healing_required",
            "repair_requested",
            "repair_ready",
            "failed",
            "failure",
            "healing",
            "repairing"
        ]
    ):

        for source in sources:

            if (
                source["name"].lower()
                == str(healing_source).lower()
            ):

                source["status"] = "failed"

    # -----------------------------------------------------
    # CALCULATE SOURCE COUNTS
    # -----------------------------------------------------

    total_sources = len(sources)

    healthy = sum(
        1
        for source in sources
        if source["status"] == "healthy"
    )

    failed = sum(
        1
        for source in sources
        if source["status"] == "failed"
    )

    total_records = sum(
        source["records"]
        for source in sources
    )

    total_valid = sum(
        source["valid"]
        for source in sources
    )

    total_invalid = sum(
        source["invalid"]
        for source in sources
    )

    total_anomalies = sum(
        source["price_anomalies"]
        for source in sources
    )

    # -----------------------------------------------------
    # CALCULATE SUCCESS RATE
    # -----------------------------------------------------

    if total_records > 0:

        success_rate = round(
            (
                total_valid
                / total_records
            ) * 100,
            2
        )

    else:

        success_rate = 0.0

    # -----------------------------------------------------
    # CALCULATE OVERALL STATUS
    # -----------------------------------------------------

    if failed == 0 and total_sources > 0:

        overall_status = "healthy"

    elif healthy > 0:

        overall_status = "degraded"

    else:

        overall_status = "failed"

    # -----------------------------------------------------
    # SELF-HEALED COUNT
    # -----------------------------------------------------

    self_healed = self_healing_state.get(
        "self_healed_count",
        0
    )

    if not isinstance(self_healed, int):

        self_healed = 0

    # -----------------------------------------------------
    # LAST RUN TIMESTAMP
    # -----------------------------------------------------

    last_run = get_last_run_timestamp()

    # -----------------------------------------------------
    # RETURN HEALTH DATA
    # -----------------------------------------------------

    return {

        "total_sources": total_sources,

        "healthy": healthy,

        "failed": failed,

        "self_healed": self_healed,

        "self_healing": {

            "status": self_healing_state.get(
                "status",
                "idle"
            ),

            "source": self_healing_state.get(
                "source"
            ),

            "reason": self_healing_state.get(
                "reason"
            ),

            "healing_started_at": self_healing_state.get(
                "healing_started_at"
            ),

            "repair_ready_at": self_healing_state.get(
                "repair_ready_at"
            ),

            "healed_at": self_healing_state.get(
                "healed_at"
            ),

            "self_healed_count": self_healed,

        },

        "success_rate": success_rate,

        "total_records": total_records,

        "valid_records": total_valid,

        "invalid_records": total_invalid,

        "price_anomalies": total_anomalies,

        "last_run": last_run,

        "status": overall_status,

        "data_source": "Member 1 Supply-WebShield pipeline",

        "sources": sources,

    }



# ============================================================
# FIND LAST RUN
# ============================================================

def get_last_run_timestamp() -> str:

    timestamps = []

    files_to_check = [

        UNIFIED_DATA_FILE,

        INVALID_DATA_FILE,

        PRICE_ANOMALY_FILE,

    ]

    for file_path in files_to_check:

        try:

            if file_path.exists():

                timestamps.append(
                    datetime.fromtimestamp(
                        file_path.stat().st_mtime,
                        tz=timezone.utc
                    )
                )

        except Exception:

            pass

    if not timestamps:

        return datetime.now(
            timezone.utc
        ).isoformat()

    latest = max(timestamps)

    return latest.isoformat()


# ============================================================
# CALCULATE SUCCESS RATE
# ============================================================

def calculate_success_rate() -> float:

    health = get_scraper_health()

    return health["success_rate"]


# ============================================================
# RUN SCRAPER
# ============================================================

def run_scraper() -> Dict:

    """
    The actual Member 1 pipeline is currently executed
    separately through member1/supply-webshield/main.py.

    This endpoint therefore reports the current pipeline
    state instead of pretending to execute a scraper.
    """

    health = get_scraper_health()

    return {

        "message": (
            "Member 1 scraper pipeline output "
            "loaded successfully"
        ),

        "status": health["status"],

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "sources": health["total_sources"],

        "records": health["total_records"],

    }


# ============================================================
# SELF-HEAL SOURCE
# ============================================================

def self_heal_source(
    source_name: str
) -> Dict:

    """
    The actual Bright Data self-healing system lives
    inside Member 1.

    We do NOT simulate healing here.
    """

    sources = get_scraper_sources()

    for source in sources:

        if source["name"].lower() == source_name.lower():

            if source["status"] == "healthy":

                return {

                    "source": source_name,

                    "status": "healthy",

                    "message": (
                        "Source is currently healthy"
                    ),

                    "healed": False,

                    "data_source": (
                        "Member 1 Supply-WebShield"
                    ),

                }

            return {

                "source": source_name,

                "status": "failed",

                "message": (
                    "Source requires Member 1 "
                    "self-healing controller"
                ),

                "healed": False,

                "data_source": (
                    "Member 1 Supply-WebShield"
                ),

            }

    return {

        "source": source_name,

        "status": "not_found",

        "message": "Scraper source not found",

        "healed": False,

    }


# ============================================================
# SCRAPER SUMMARY
# ============================================================

def get_scraper_summary() -> Dict:

    health = get_scraper_health()

    return {

        "total_sources": health[
            "total_sources"
        ],

        "healthy": health[
            "healthy"
        ],

        "failed": health[
            "failed"
        ],

        "self_healed": health[
            "self_healed"
        ],

        "success_rate": health[
            "success_rate"
        ],

        "total_records": health[
            "total_records"
        ],

        "valid_records": health[
            "valid_records"
        ],

        "invalid_records": health[
            "invalid_records"
        ],

        "price_anomalies": health[
            "price_anomalies"
        ],

        "status": health[
            "status"
        ],

        "last_run": health[
            "last_run"
        ],

        "sources": health[
            "sources"
        ],

    }