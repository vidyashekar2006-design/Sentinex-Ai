from datetime import datetime
from typing import List, Dict


# ============================================================
# SUPPLYSHIELD AI - SELF-HEALING SCRAPER SERVICE
# ============================================================

# Simulated public web sources.
# Later these can be replaced with Bright Data scraper
# results or other permitted public sources.

SCRAPER_SOURCES = [
    {
        "name": "Supplier News Feed",
        "url": "https://example.com/supplier-news",
        "status": "healthy"
    },
    {
        "name": "Market Price Feed",
        "url": "https://example.com/market-prices",
        "status": "healthy"
    },
    {
        "name": "Industry News Feed",
        "url": "https://example.com/industry-news",
        "status": "healthy"
    },
    {
        "name": "Supply Chain News",
        "url": "https://example.com/supply-chain",
        "status": "healthy"
    },
    {
        "name": "Manufacturing Feed",
        "url": "https://example.com/manufacturing",
        "status": "healthy"
    },
    {
        "name": "Commodity Feed",
        "url": "https://example.com/commodity",
        "status": "healthy"
    },
    {
        "name": "Logistics Feed",
        "url": "https://example.com/logistics",
        "status": "healthy"
    },
    {
        "name": "Technology Supply Feed",
        "url": "https://example.com/technology",
        "status": "healthy"
    },
    {
        "name": "Global Trade Feed",
        "url": "https://example.com/global-trade",
        "status": "failed"
    },
    {
        "name": "Economic News Feed",
        "url": "https://example.com/economy",
        "status": "failed"
    }
]


# ============================================================
# SCRAPER STATE
# ============================================================

SCRAPER_STATE = {
    "total_sources": 10,
    "healthy": 8,
    "failed": 2,
    "self_healed": 2,
    "total_attempts": 12,
    "successful_requests": 10,
    "last_run": datetime.utcnow().isoformat(),
    "status": "healthy"
}


# ============================================================
# GET SOURCES
# ============================================================

def get_scraper_sources() -> List[Dict]:

    return SCRAPER_SOURCES


# ============================================================
# CALCULATE SUCCESS RATE
# ============================================================

def calculate_success_rate() -> float:

    total_attempts = SCRAPER_STATE["total_attempts"]

    successful_requests = (
        SCRAPER_STATE["successful_requests"]
    )

    if total_attempts == 0:
        return 0.0

    return round(
        (successful_requests / total_attempts) * 100,
        2
    )


# ============================================================
# GET SCRAPER HEALTH
# ============================================================

def get_scraper_health() -> Dict:

    success_rate = calculate_success_rate()

    return {
        "total_sources": SCRAPER_STATE["total_sources"],
        "healthy": SCRAPER_STATE["healthy"],
        "failed": SCRAPER_STATE["failed"],
        "self_healed": SCRAPER_STATE["self_healed"],
        "success_rate": success_rate,
        "last_run": SCRAPER_STATE["last_run"],
        "status": SCRAPER_STATE["status"]
    }


# ============================================================
# SELF-HEAL FAILED SOURCE
# ============================================================

def self_heal_source(source_name: str) -> Dict:

    for source in SCRAPER_SOURCES:

        if source["name"] == source_name:

            if source["status"] == "healthy":

                return {
                    "source": source_name,
                    "status": "healthy",
                    "message": "Source is already healthy",
                    "healed": False
                }

            # Simulate self-healing
            source["status"] = "healthy"

            SCRAPER_STATE["failed"] -= 1

            SCRAPER_STATE["healthy"] += 1

            SCRAPER_STATE["self_healed"] += 1

            SCRAPER_STATE["successful_requests"] += 1

            SCRAPER_STATE["total_attempts"] += 1

            SCRAPER_STATE["last_run"] = (
                datetime.utcnow().isoformat()
            )

            return {
                "source": source_name,
                "status": "healthy",
                "message": "Source successfully self-healed",
                "healed": True
            }

    return {
        "source": source_name,
        "status": "not_found",
        "message": "Scraper source not found",
        "healed": False
    }


# ============================================================
# RUN SCRAPER
# ============================================================

def run_scraper() -> Dict:

    SCRAPER_STATE["last_run"] = (
        datetime.utcnow().isoformat()
    )

    return {
        "message": "Scraper execution completed",
        "status": "completed",
        "timestamp": SCRAPER_STATE["last_run"]
    }


# ============================================================
# SCRAPER SUMMARY
# ============================================================

def get_scraper_summary() -> Dict:

    health = get_scraper_health()

    return {
        "total_sources": health["total_sources"],
        "healthy": health["healthy"],
        "failed": health["failed"],
        "self_healed": health["self_healed"],
        "success_rate": health["success_rate"],
        "status": health["status"],
        "last_run": health["last_run"]
    }