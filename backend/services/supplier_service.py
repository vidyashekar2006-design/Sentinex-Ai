from backend.models.supplier import Supplier


# ============================================================
# SUPPLIER DATA
# ============================================================

SUPPLIERS = [
    Supplier(
        name="ABC Electronics",
        risk=91,
        status="HIGH",
        delivery_delay=8.5,
        price_change=18.0,
        sentiment_score=0.28,
        disruption_history=0.82
    ),

    Supplier(
        name="XYZ Components",
        risk=73,
        status="MEDIUM",
        delivery_delay=5.2,
        price_change=11.0,
        sentiment_score=0.46,
        disruption_history=0.61
    ),

    Supplier(
        name="DEF Industries",
        risk=48,
        status="LOW",
        delivery_delay=2.1,
        price_change=4.0,
        sentiment_score=0.74,
        disruption_history=0.32
    ),

    Supplier(
        name="Global Parts Ltd",
        risk=66,
        status="MEDIUM",
        delivery_delay=4.7,
        price_change=9.0,
        sentiment_score=0.53,
        disruption_history=0.55
    )
]


# ============================================================
# GET ALL SUPPLIERS
# ============================================================

def get_all_suppliers():
    return SUPPLIERS


# ============================================================
# GET SUPPLIER BY NAME
# ============================================================

def get_supplier_by_name(name: str):

    for supplier in SUPPLIERS:

        if supplier.name.lower() == name.lower():
            return supplier

    return None


# ============================================================
# CALCULATE AVERAGE SUPPLIER RISK
# ============================================================

def calculate_average_supplier_risk():

    if not SUPPLIERS:
        return 0

    total_risk = sum(
        supplier.risk
        for supplier in SUPPLIERS
    )

    return round(
        total_risk / len(SUPPLIERS)
    )


# ============================================================
# SUPPLIER SUMMARY
# ============================================================

def get_supplier_summary():

    average_risk = calculate_average_supplier_risk()

    high_risk = sum(
        1
        for supplier in SUPPLIERS
        if supplier.status == "HIGH"
    )

    medium_risk = sum(
        1
        for supplier in SUPPLIERS
        if supplier.status == "MEDIUM"
    )

    low_risk = sum(
        1
        for supplier in SUPPLIERS
        if supplier.status == "LOW"
    )

    return {
        "total_suppliers": len(SUPPLIERS),
        "average_risk": average_risk,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }