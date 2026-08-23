from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import sqlite3
import os


# =========================================================
# SUPPLYSHIELD AI - FASTAPI BACKEND
# =========================================================
#
# Integrates:
#   Member 1 -> Supply-WebShield / Scraper
#   Member 2 -> SQLite / Risk Engine
#   Frontend  -> React dashboard
#
# =========================================================


app = FastAPI(
    title="SupplyShield AI API",
    description="Backend API for SupplyShield AI supply-chain intelligence platform",
    version="1.0.0"
)


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "member2",
    "database",
    "supplyshield.db"
)


def get_db_connection():
    """
    Create a connection to the Member 2 SQLite database.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",

    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",

    "https://supply-shield-ai-sand.vercel.app",
    "https://sentinex-ai.vercel.app",
],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "SupplyShield AI Backend is running",
        "status": "online",
        "version": "1.0.0",
        "database": "Member 2 SQLite",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "backend": "online",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# =========================================================
# DATABASE STATUS
# =========================================================

@app.get("/api/database")
def database_status():

    try:

        conn = get_db_connection()

        record_count = conn.execute(
            "SELECT COUNT(*) FROM integrated_risk"
        ).fetchone()[0]

        conn.close()

        return {
            "database": "connected",
            "database_file": DATABASE_PATH,
            "integrated_risk_records": record_count
        }

    except Exception as e:

        return {
            "database": "error",
            "error": str(e)
        }


# =========================================================
# SYSTEM STATUS
# =========================================================

@app.get("/api/status")
@app.get("/api/system-status")
def system_status():

    database = "offline"

    try:

        conn = get_db_connection()

        conn.execute(
            "SELECT 1 FROM integrated_risk LIMIT 1"
        )

        conn.close()

        database = "online"

    except Exception:

        database = "offline"

    return {

        "backend": "online",

        "risk_engine": "online",

        "supplier_service": "online",

        "webshield": "online",

        "market_intelligence": "online",

        "scraper": "online",

        "database": database,

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }


# =========================================================
# OVERALL RISK
# =========================================================

@app.get("/api/risk")
def get_risk():

    conn = get_db_connection()

    summary = conn.execute("""
        SELECT

            AVG(unified_risk) AS overall_risk,

            AVG(supply_chain_risk) AS supply_chain_risk,

            AVG(webshield_risk) AS webshield_risk,

            AVG(anomaly_risk) AS anomaly_risk,

            AVG(market_risk) AS market_risk,

            COUNT(*) AS records_processed

        FROM integrated_risk
    """).fetchone()

    # -----------------------------------------------------
    # Risk category counts
    # -----------------------------------------------------

    high_risk = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE unified_risk >= 70
    """).fetchone()[0]

    medium_risk = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE unified_risk >= 40
        AND unified_risk < 70
    """).fetchone()[0]

    low_risk = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE unified_risk < 40
    """).fetchone()[0]

    # -----------------------------------------------------
    # Generate alerts
    # -----------------------------------------------------

    alerts = []

    price_anomaly_count = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE price_anomaly > 0
    """).fetchone()[0]

    supplier_risk_count = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE seller_risk > 0
    """).fetchone()[0]

    anomaly_count = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE anomaly_risk > 0
    """).fetchone()[0]

    if price_anomaly_count > 0:

        alerts.append(
            "Price anomaly detected"
        )

    if supplier_risk_count > 0:

        alerts.append(
            "Supplier identity information missing"
        )

    if anomaly_count > 0:

        alerts.append(
            "Availability risk signal detected"
        )

    conn.close()

    # -----------------------------------------------------
    # Calculate values
    # -----------------------------------------------------

    overall_risk = round(
        summary["overall_risk"] or 0,
        2
    )

    supplier_risk = round(
        summary["supply_chain_risk"] or 0,
        2
    )

    webshield_risk = round(
        summary["webshield_risk"] or 0,
        2
    )

    market_anomaly = round(
        summary["market_risk"] or 0,
        2
    )

    anomaly_risk = round(
        summary["anomaly_risk"] or 0,
        2
    )

    # -----------------------------------------------------
    # Risk level
    # -----------------------------------------------------

    if overall_risk >= 70:

        risk_level = "HIGH"

    elif overall_risk >= 40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {

        "overall_risk": overall_risk,

        "risk_level": risk_level,

        "disruption_probability": round(
            anomaly_risk / 100,
            2
        ),

        "supplier_risk": supplier_risk,

        "market_anomaly": market_anomaly,

        "webshield_risk": webshield_risk,

        "alerts": alerts,

        "records_processed":
            summary["records_processed"],

        "high_risk_records":
            high_risk,

        "medium_risk_records":
            medium_risk,

        "low_risk_records":
            low_risk
    }


# =========================================================
# SUPPLIERS
# =========================================================

@app.get("/api/suppliers")
def get_suppliers():

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT

            COALESCE(
                NULLIF(supplier, ''),
                company
            ) AS supplier_name,

            AVG(unified_risk) AS risk

        FROM integrated_risk

        GROUP BY

            COALESCE(
                NULLIF(supplier, ''),
                company
            )

        ORDER BY risk DESC

        LIMIT 20
    """).fetchall()

    conn.close()

    suppliers = []

    for row in rows:

        risk = round(
            row["risk"] or 0,
            2
        )

        if risk >= 70:

            status = "HIGH"

        elif risk >= 40:

            status = "MEDIUM"

        else:

            status = "LOW"

        suppliers.append({

            "name":
                row["supplier_name"]
                or "Unknown Supplier",

            "risk": risk,

            "status": status
        })

    return {
        "suppliers": suppliers
    }


# =========================================================
# WEBSHIELD
# =========================================================

@app.get("/api/webshield")
def get_webshield():

    conn = get_db_connection()

    suspicious_listings = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE webshield_risk > 40
    """).fetchone()[0]

    price_anomalies = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE price_anomaly > 0
    """).fetchone()[0]

    counterfeit_risks = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE counterfeit_risk > 0
    """).fetchone()[0]

    supplier_web_alerts = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE seller_risk > 0
    """).fetchone()[0]

    average_webshield = conn.execute("""
        SELECT AVG(webshield_risk)

        FROM integrated_risk
    """).fetchone()[0]

    conn.close()

    return {

        "suspicious_listings":
            suspicious_listings,

        "price_anomalies":
            price_anomalies,

        "counterfeit_risks":
            counterfeit_risks,

        "supplier_web_alerts":
            supplier_web_alerts,

        "average_webshield_risk":
            round(
                average_webshield or 0,
                2
            )
    }


# =========================================================
# SCRAPER HEALTH
# =========================================================
#
# IMPORTANT:
#
# This endpoint reads REAL Member 1 data from:
#
# member1/
#   supply-webshield/
#       data/
#           raw/
#           processed/
#           rejected/
#
# It does NOT create fake scraper statistics.
#
# =========================================================

@app.get("/api/scraper-health")
def scraper_health():

    try:

        from services.scraper_service import (
            get_scraper_health
        )

        health = get_scraper_health()

        return health

    except Exception as error:

        print(
            f"[SCRAPER HEALTH ERROR] {error}"
        )

        return {

            "total_sources": 0,

            "healthy": 0,

            "failed": 0,

            "self_healed": 0,

            "success_rate": 0,

            "total_records": 0,

            "valid_records": 0,

            "invalid_records": 0,

            "price_anomalies": 0,

            "last_run": None,

            "status": "unavailable",

            "data_source":
                "Member 1 Supply-WebShield pipeline",

            "sources": [],

            "error": str(error)
        }


# =========================================================
# SCRAPER SOURCES
# =========================================================

@app.get("/api/scraper-sources")
def scraper_sources():

    try:

        from backend.services.scraper_service import (
            get_scraper_sources
        )

        sources = get_scraper_sources()

        return {
            "sources": sources
        }

    except Exception as error:

        print(
            f"[SCRAPER SOURCES ERROR] {error}"
        )

        return {

            "sources": [],

            "error": str(error)
        }


# =========================================================
# SCRAPER SUMMARY
# =========================================================

@app.get("/api/scraper-summary")
def scraper_summary():

    try:

        from backend.services.scraper_service import (
            get_scraper_summary
        )

        return get_scraper_summary()

    except Exception as error:

        print(
            f"[SCRAPER SUMMARY ERROR] {error}"
        )

        return {

            "total_sources": 0,

            "healthy": 0,

            "failed": 0,

            "self_healed": 0,

            "success_rate": 0,

            "total_records": 0,

            "valid_records": 0,

            "invalid_records": 0,

            "price_anomalies": 0,

            "status": "unavailable",

            "sources": [],

            "error": str(error)
        }


# =========================================================
# RUN SCRAPER
# =========================================================

@app.post("/api/run-scraper")
def run_scraper():

    try:

        from backend.services.scraper_service import (
            run_scraper
        )

        return run_scraper()

    except Exception as error:

        print(
            f"[RUN SCRAPER ERROR] {error}"
        )

        return {

            "status": "error",

            "message":
                "Unable to read Member 1 scraper pipeline",

            "error": str(error)
        }


# =========================================================
# SELF-HEAL SOURCE
# =========================================================

@app.post("/api/self-heal/{source_name}")
def self_heal(source_name: str):

    try:

        from backend.services.scraper_service import (
            self_heal_source
        )

        return self_heal_source(
            source_name
        )

    except Exception as error:

        print(
            f"[SELF HEAL ERROR] {error}"
        )

        return {

            "source": source_name,

            "status": "error",

            "message":
                "Unable to communicate with Member 1 self-healing service",

            "healed": False,

            "error": str(error)
        }


# =========================================================
# MARKET INTELLIGENCE
# =========================================================

@app.get("/api/market")
def market_intelligence():

    conn = get_db_connection()

    row = conn.execute("""
        SELECT

            AVG(market_risk) AS market_risk,

            AVG(price_anomaly) AS price_anomaly,

            AVG(unified_risk) AS overall_risk

        FROM integrated_risk
    """).fetchone()

    conn.close()

    market_risk = round(
        row["market_risk"] or 0,
        2
    )

    price_anomaly = round(
        row["price_anomaly"] or 0,
        2
    )

    if market_risk >= 70:

        status = "critical"

    elif market_risk >= 40:

        status = "warning"

    else:

        status = "normal"

    return {

        "market_anomaly":
            market_risk,

        "price_change":
            price_anomaly,

        "demand_change":
            0,

        "volatility":
            market_risk,

        "trend":
            "increasing"
            if market_risk > 40
            else "stable",

        "status":
            status
    }


# =========================================================
# ALERTS
# =========================================================

@app.get("/api/alerts")
def get_alerts():

    conn = get_db_connection()

    price_count = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE price_anomaly > 0
    """).fetchone()[0]

    counterfeit_count = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE counterfeit_risk > 0
    """).fetchone()[0]

    anomaly_count = conn.execute("""
        SELECT COUNT(*)

        FROM integrated_risk

        WHERE anomaly_risk > 0
    """).fetchone()[0]

    conn.close()

    alerts = []

    if price_count > 0:

        alerts.append({

            "message":
                "Price anomaly detected",

            "severity":
                "MEDIUM",

            "category":
                "Market"
        })

    if counterfeit_count > 0:

        alerts.append({

            "message":
                "Potential counterfeit risk detected",

            "severity":
                "HIGH",

            "category":
                "WebShield"
        })

    if anomaly_count > 0:

        alerts.append({

            "message":
                "Anomalous supply-chain behaviour detected",

            "severity":
                "MEDIUM",

            "category":
                "Supply"
        })

    high_count = sum(
        1
        for alert in alerts
        if alert["severity"] == "HIGH"
    )

    warning_count = sum(
        1
        for alert in alerts
        if alert["severity"] == "MEDIUM"
    )

    return {

        "total":
            len(alerts),

        "critical":
            high_count,

        "warning":
            warning_count,

        "alerts":
            alerts
    }


# =========================================================
# RISK TREND
# =========================================================

@app.get("/api/risk-trend")
def risk_trend():

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT

            DATE(integration_timestamp) AS day,

            AVG(unified_risk) AS risk

        FROM integrated_risk

        GROUP BY DATE(integration_timestamp)

        ORDER BY day
    """).fetchall()

    conn.close()

    labels = []

    values = []

    for row in rows:

        labels.append(
            row["day"]
        )

        values.append(
            round(
                row["risk"] or 0,
                2
            )
        )

    # Do not generate fake historical data.

    if not labels:

        labels = ["Current"]

        values = [0]

    return {

        "labels":
            labels,

        "values":
            values
    }


# =========================================================
# SUPPLIER SUMMARY
# =========================================================

@app.get("/api/supplier-summary")
def supplier_summary():

    conn = get_db_connection()

    total = conn.execute("""
        SELECT COUNT(
            DISTINCT COALESCE(
                NULLIF(supplier, ''),
                company
            )
        )

        FROM integrated_risk
    """).fetchone()[0]

    high = conn.execute("""
        SELECT COUNT(*)

        FROM (

            SELECT

                COALESCE(
                    NULLIF(supplier, ''),
                    company
                ) AS supplier_name,

                AVG(unified_risk) AS risk

            FROM integrated_risk

            GROUP BY supplier_name

            HAVING AVG(unified_risk) >= 70
        )
    """).fetchone()[0]

    medium = conn.execute("""
        SELECT COUNT(*)

        FROM (

            SELECT

                COALESCE(
                    NULLIF(supplier, ''),
                    company
                ) AS supplier_name,

                AVG(unified_risk) AS risk

            FROM integrated_risk

            GROUP BY supplier_name

            HAVING AVG(unified_risk) >= 40
            AND AVG(unified_risk) < 70
        )
    """).fetchone()[0]

    low = conn.execute("""
        SELECT COUNT(*)

        FROM (

            SELECT

                COALESCE(
                    NULLIF(supplier, ''),
                    company
                ) AS supplier_name,

                AVG(unified_risk) AS risk

            FROM integrated_risk

            GROUP BY supplier_name

            HAVING AVG(unified_risk) < 40
        )
    """).fetchone()[0]

    average = conn.execute("""
        SELECT AVG(unified_risk)

        FROM integrated_risk
    """).fetchone()[0]

    conn.close()

    return {

        "total_suppliers":
            total,

        "high_risk":
            high,

        "medium_risk":
            medium,

        "low_risk":
            low,

        "average_risk":
            round(
                average or 0,
                2
            )
    }


# =========================================================
# DATABASE RECORDS
# =========================================================

@app.get("/api/records")
def get_records(limit: int = 50):

    # Protect the API from unreasonable limits.

    if limit < 1:
        limit = 1

    if limit > 500:
        limit = 500

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT *

        FROM integrated_risk

        ORDER BY integration_id DESC

        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    records = []

    for row in rows:

        records.append(
            dict(row)
        )

    return {

        "count":
            len(records),

        "records":
            records
    }


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
async def startup_event():

    print("")

    print("=" * 60)

    print("             SUPPLYSHIELD AI")

    print("=" * 60)

    print("Backend Status : ONLINE")

    print("Risk Engine    : ONLINE")

    print("Supplier API   : ONLINE")

    print("WebShield      : ONLINE")

    print("Market Intel   : ONLINE")

    print("Scraper        : ONLINE")

    print("Database       : MEMBER 2 SQLITE")

    print(
        "Database Path  :",
        DATABASE_PATH
    )

    print("CORS           : ENABLED")

    print("=" * 60)

    print("")


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
