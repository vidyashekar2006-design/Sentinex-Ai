from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime


# =========================================================
# SUPPLYSHIELD AI - FASTAPI BACKEND
# =========================================================

app = FastAPI(
    title="SupplyShield AI API",
    description="Backend API for SupplyShield AI supply-chain intelligence platform",
    version="1.0.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # Vite frontend
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",

        # 127.0.0.1 versions
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
# SYSTEM STATUS
# =========================================================

@app.get("/api/status")
def system_status():

    return {
        "backend": "online",
        "risk_engine": "online",
        "supplier_service": "online",
        "webshield": "online",
        "market_intelligence": "online",
        "scraper": "online",
        "database": "development-mode",
        "timestamp": datetime.utcnow().isoformat()
    }


# =========================================================
# OVERALL RISK
# =========================================================

@app.get("/api/risk")
def get_risk():

    return {
        "overall_risk": 68,
        "risk_level": "MEDIUM",

        "disruption_probability": 0.88,

        "supplier_risk": 0.70,

        "market_anomaly": 0.72,

        "webshield_risk": 0.40,

        "alerts": [
            "Factory disruption detected",
            "Component prices increased",
            "Supplier sentiment deteriorated"
        ]
    }


# =========================================================
# SUPPLIERS
# =========================================================

@app.get("/api/suppliers")
def get_suppliers():

    return {
        "suppliers": [
            {
                "name": "ABC Electronics",
                "risk": 91,
                "status": "HIGH"
            },
            {
                "name": "XYZ Components",
                "risk": 73,
                "status": "MEDIUM"
            },
            {
                "name": "DEF Industries",
                "risk": 48,
                "status": "LOW"
            },
            {
                "name": "Global Parts Ltd",
                "risk": 66,
                "status": "MEDIUM"
            },
            {
                "name": "Prime Components",
                "risk": 57,
                "status": "MEDIUM"
            }
        ]
    }


# =========================================================
# WEBSHIELD
# =========================================================

@app.get("/api/webshield")
def get_webshield():

    return {
        "suspicious_listings": 6,
        "price_anomalies": 9,
        "counterfeit_risks": 4,
        "supplier_web_alerts": 7
    }


# =========================================================
# SCRAPER HEALTH
# =========================================================

@app.get("/api/scraper-health")
def scraper_health():

    return {
        "total_sources": 10,
        "healthy": 8,
        "failed": 2,
        "self_healed": 2
    }


# =========================================================
# MARKET INTELLIGENCE
# =========================================================

@app.get("/api/market")
def market_intelligence():

    return {
        "market_anomaly": 72,
        "price_change": 18.4,
        "demand_change": 12.7,
        "volatility": 64,
        "trend": "increasing",
        "status": "warning"
    }


# =========================================================
# ALERTS
# =========================================================

@app.get("/api/alerts")
def get_alerts():

    return {
        "total": 3,
        "critical": 1,
        "warning": 2,

        "alerts": [
            {
                "message": "Factory disruption detected",
                "severity": "HIGH",
                "category": "Supply"
            },
            {
                "message": "Component prices increased",
                "severity": "MEDIUM",
                "category": "Market"
            },
            {
                "message": "Supplier sentiment deteriorated",
                "severity": "MEDIUM",
                "category": "Supplier"
            }
        ]
    }


# =========================================================
# RISK TREND
# =========================================================

@app.get("/api/risk-trend")
def risk_trend():

    return {
        "labels": [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ],

        "values": [
            52,
            57,
            61,
            59,
            65,
            71,
            68
        ]
    }


# =========================================================
# SUPPLIER SUMMARY
# =========================================================

@app.get("/api/supplier-summary")
def supplier_summary():

    return {
        "total_suppliers": 5,
        "high_risk": 1,
        "medium_risk": 3,
        "low_risk": 1,
        "average_risk": 67
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
    print("CORS           : ENABLED")
    print("=" * 60)
    print("")