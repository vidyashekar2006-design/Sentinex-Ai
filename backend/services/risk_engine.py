def calculate_overall_risk(
    disruption_probability: float,
    supplier_risk: float,
    market_anomaly: float,
    webshield_risk: float,
):
    """
    Calculate the overall SupplyShield risk score.

    All input values must be between 0 and 1.
    """

    # Keep all values inside the valid range
    disruption_probability = max(
        0, min(1, disruption_probability)
    )

    supplier_risk = max(
        0, min(1, supplier_risk)
    )

    market_anomaly = max(
        0, min(1, market_anomaly)
    )

    webshield_risk = max(
        0, min(1, webshield_risk)
    )

    # Risk weights
    disruption_weight = 0.30
    supplier_weight = 0.30
    market_weight = 0.15
    webshield_weight = 0.25

    # Calculate weighted risk
    overall_score = (
        disruption_probability * disruption_weight
        + supplier_risk * supplier_weight
        + market_anomaly * market_weight
        + webshield_risk * webshield_weight
    )

    # Convert to percentage
    overall_percentage = round(
        overall_score * 100
    )

    # Determine risk level
    if overall_percentage >= 70:
        risk_level = "HIGH"

    elif overall_percentage >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "overall_risk": overall_percentage,
        "risk_level": risk_level
    }