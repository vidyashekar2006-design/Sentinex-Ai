from backend.models.market import MarketData


# ============================================================
# MARKET INTELLIGENCE DATA
# ============================================================

MARKET_DATA = MarketData(
    component_price_change=0.68,
    demand_change=0.55,
    supply_pressure=0.76,
    market_anomalies=8
)


# ============================================================
# GET MARKET DATA
# ============================================================

def get_market_data() -> MarketData:
    """
    Return current market intelligence data.
    """

    return MARKET_DATA


# ============================================================
# CALCULATE MARKET RISK
# ============================================================

def calculate_market_risk() -> int:
    """
    Calculate market risk as a percentage.
    """

    data = MARKET_DATA

    # --------------------------------------------------------
    # Normalize market anomaly count
    # --------------------------------------------------------

    anomaly_score = min(
        data.market_anomalies / 20,
        1.0
    )

    # --------------------------------------------------------
    # Weighted market risk
    # --------------------------------------------------------

    risk_score = (
        data.component_price_change * 0.30
        + data.demand_change * 0.20
        + data.supply_pressure * 0.30
        + anomaly_score * 0.20
    )

    risk_percentage = round(
        risk_score * 100
    )

    return risk_percentage


# ============================================================
# MARKET RISK LEVEL
# ============================================================

def get_market_risk_level(risk: int) -> str:

    if risk >= 70:
        return "HIGH"

    elif risk >= 40:
        return "MEDIUM"

    else:
        return "LOW"


# ============================================================
# MARKET SUMMARY
# ============================================================

def get_market_summary() -> dict:

    data = MARKET_DATA

    risk = calculate_market_risk()

    risk_level = get_market_risk_level(
        risk
    )

    return {
        "risk": risk,
        "risk_level": risk_level,
        "component_price_change": data.component_price_change,
        "demand_change": data.demand_change,
        "supply_pressure": data.supply_pressure,
        "market_anomalies": data.market_anomalies
    }