from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sqlite3
import os
import json


# =========================================================
# SUPPLYSHIELD AI - FASTAPI BACKEND
# DATABASE INTEGRATION
# =========================================================

app = FastAPI(
    title="SupplyShield AI API",
    description="Backend API for SupplyShield AI supply-chain intelligence platform",
    version="1.0.0"
)



# =========================================================
# SCRAPER HEALTH FILE
# =========================================================

SCRAPER_HEALTH_FILE = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "data",
    "processed",
    "scraper health.json"
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
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "backend": "online",
        "timestamp": datetime.utcnow().isoformat()
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

        "timestamp": datetime.utcnow().isoformat()
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


    # Risk category counts

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


    # Generate alerts from database

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


    # Risk level

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

@app.get("/api/scraper-health")
def scraper_health():

    try:

        with open(
            SCRAPER_HEALTH_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except FileNotFoundError:

        return {
            "status": "error",
            "message": "Scraper health file not found",
            "file": SCRAPER_HEALTH_FILE
        }

    except json.JSONDecodeError:

        return {
            "status": "error",
            "message": "Scraper health JSON is invalid"
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }

# =========================================================
# SCRAPER SOURCES
# =========================================================

@app.get("/api/scraper-sources")
def scraper_sources():

    conn = get_db_connection()


    rows = conn.execute("""
        SELECT

            source,

            COUNT(*) AS records

        FROM integrated_risk

        GROUP BY source

        ORDER BY records DESC
    """).fetchall()


    conn.close()


    sources = []


    for row in rows:

        sources.append({

            "source":
                row["source"],

            "records":
                row["records"],

            "status":
                "healthy"
        })


    return {

        "sources": sources

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


    # If only one processing date exists,
    # return that date instead of fake weekly data.

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

    print("Database Path  :", DATABASE_PATH)

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
