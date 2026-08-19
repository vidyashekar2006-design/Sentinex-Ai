from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="SupplyShield AI API",
    description="Backend API for SupplyShield AI supply-chain intelligence platform",
    version="1.0.0"
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SupplyShield AI Backend is running",
        "status": "online"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# --------------------------------------------------
# OVERALL RISK
# --------------------------------------------------

@app.get("/api/risk")
def get_risk():

    return {
        "overall_risk": 74,
        "risk_level": "HIGH",
        "disruption_probability": 0.88,
        "supplier_risk": 0.79,
        "market_anomaly": 0.72,
        "webshield_risk": 0.84,

        "alerts": [
            "Factory disruption detected",
            "Component prices increased",
            "Supplier sentiment deteriorated"
        ]
    }


# --------------------------------------------------
# SUPPLIERS
# --------------------------------------------------

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
            }
        ]
    }


# --------------------------------------------------
# WEBSHIELD
# --------------------------------------------------

@app.get("/api/webshield")
def get_webshield():

    return {
        "suspicious_listings": 6,
        "price_anomalies": 9,
        "counterfeit_risks": 4,
        "supplier_web_alerts": 7
    }


# --------------------------------------------------
# SCRAPER HEALTH
# --------------------------------------------------

@app.get("/api/scraper-health")
def scraper_health():

    return {
        "total_sources": 10,
        "healthy": 8,
        "failed": 2,
        "self_healed": 2
    }