from backend.models.webshield import WebShieldData


# ============================================================
# WEBSHIELD DATA
# ============================================================

WEBSHIELD_DATA = WebShieldData(
    suspicious_listings=6,
    price_anomalies=9,
    counterfeit_risks=4,
    supplier_web_alerts=7
)


# ============================================================
# GET WEBSHIELD DATA
# ============================================================

def get_webshield_data() -> WebShieldData:
    """
    Return the current WebShield intelligence data.
    """

    return WEBSHIELD_DATA


# ============================================================
# CALCULATE WEBSHIELD RISK
# ============================================================

def calculate_webshield_risk() -> int:
    """
    Calculate WebShield risk as a percentage.

    Risk sources:
        - Suspicious listings
        - Price anomalies
        - Counterfeit risks
        - Supplier web alerts
    """

    data = WEBSHIELD_DATA

    # --------------------------------------------------------
    # Normalize individual signals
    # --------------------------------------------------------

    suspicious_score = min(
        data.suspicious_listings / 20,
        1.0
    )

    price_score = min(
        data.price_anomalies / 20,
        1.0
    )

    counterfeit_score = min(
        data.counterfeit_risks / 10,
        1.0
    )

    supplier_alert_score = min(
        data.supplier_web_alerts / 15,
        1.0
    )

    # --------------------------------------------------------
    # Weighted WebShield Risk
    # --------------------------------------------------------

    risk_score = (
        suspicious_score * 0.25
        + price_score * 0.25
        + counterfeit_score * 0.30
        + supplier_alert_score * 0.20
    )

    # Convert to percentage
    risk_percentage = round(
        risk_score * 100
    )

    return risk_percentage


# ============================================================
# WEBSHIELD RISK LEVEL
# ============================================================

def get_webshield_risk_level(risk: int) -> str:
    """
    Determine WebShield risk level.
    """

    if risk >= 70:
        return "HIGH"

    elif risk >= 40:
        return "MEDIUM"

    else:
        return "LOW"


# ============================================================
# WEBSHIELD SUMMARY
# ============================================================

def get_webshield_summary() -> dict:
    """
    Return complete WebShield summary.
    """

    data = WEBSHIELD_DATA

    risk = calculate_webshield_risk()

    risk_level = get_webshield_risk_level(
        risk
    )

    total_alerts = (
        data.suspicious_listings
        + data.price_anomalies
        + data.counterfeit_risks
        + data.supplier_web_alerts
    )

    return {
        "risk": risk,
        "risk_level": risk_level,
        "total_alerts": total_alerts
    }