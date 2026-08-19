import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="SupplyShield AI",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# API HELPER
# ============================================================

def get_api_data(endpoint):
    """
    Fetch data from the FastAPI backend.
    """

    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to the SupplyShield backend. "
            "Make sure FastAPI is running on port 8000."
        )
        return None

    except requests.exceptions.Timeout:
        st.error("❌ Backend request timed out.")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Backend request failed: {e}")
        return None

    except ValueError:
        st.error("❌ Backend returned invalid JSON.")
        return None


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ SupplyShield AI")

st.subheader("AI-Powered Supply Chain Intelligence")

st.write(
    "Monitor suppliers, detect disruptions, "
    "and identify supply-chain risks."
)

st.divider()


# ============================================================
# LOAD BACKEND DATA
# ============================================================

risk_data = get_api_data("/api/risk")
supplier_data = get_api_data("/api/suppliers")
webshield_data = get_api_data("/api/webshield")
scraper_data = get_api_data("/api/scraper-health")


# ============================================================
# OVERALL RISK
# ============================================================

st.header("🚨 Overall Supply Chain Risk")

if risk_data:

    # Try common field names
    risk_score = (
        risk_data.get("overall_risk")
        or risk_data.get("risk_score")
        or risk_data.get("risk")
        or 0
    )

    try:
        risk_score = float(risk_score)
    except (ValueError, TypeError):
        risk_score = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall Risk",
            f"{risk_score:.0f}/100"
        )

    with col2:

        if risk_score >= 70:
            risk_status = "🔴 HIGH"
        elif risk_score >= 40:
            risk_status = "🟠 MEDIUM"
        else:
            risk_status = "🟢 LOW"

        st.metric(
            "Risk Level",
            risk_status
        )

    with col3:

        st.metric(
            "API Status",
            "🟢 Connected"
        )

else:

    st.warning("No risk data available.")


st.divider()


# ============================================================
# SCRAPER HEALTH
# ============================================================

st.header("🕷️ Scraper Health")

if scraper_data:

    total_sources = scraper_data.get("total_sources", 0)
    healthy = scraper_data.get("healthy", 0)
    failed = scraper_data.get("failed", 0)
    self_healed = scraper_data.get("self_healed", 0)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Sources",
            total_sources
        )

    with col2:
        st.metric(
            "Healthy",
            healthy
        )

    with col3:
        st.metric(
            "Failed",
            failed
        )

    with col4:
        st.metric(
            "Self-Healed",
            self_healed
        )

else:

    st.warning("No scraper health data available.")


st.divider()


# ============================================================
# SUPPLIERS
# ============================================================

st.header("🏭 Supplier Risk")

if supplier_data:

    # Handle different possible API response structures
    if isinstance(supplier_data, dict):

        if "suppliers" in supplier_data:
            suppliers = supplier_data["suppliers"]

        elif "data" in supplier_data:
            suppliers = supplier_data["data"]

        else:
            suppliers = supplier_data

    elif isinstance(supplier_data, list):

        suppliers = supplier_data

    else:

        suppliers = []

    # Convert to dataframe
    if isinstance(suppliers, list) and suppliers:

        df_suppliers = pd.DataFrame(suppliers)

        st.dataframe(
            df_suppliers,
            use_container_width=True
        )

        # Try to find useful risk columns
        risk_column = None

        for column in [
            "risk",
            "risk_score",
            "supplier_risk",
            "score"
        ]:

            if column in df_suppliers.columns:
                risk_column = column
                break

        # Try to find supplier name column
        name_column = None

        for column in [
            "supplier",
            "supplier_name",
            "name",
            "company"
        ]:

            if column in df_suppliers.columns:
                name_column = column
                break

        # Create chart if possible
        if risk_column and name_column:

            st.subheader("Supplier Risk Comparison")

            chart = px.bar(
                df_suppliers,
                x=name_column,
                y=risk_column,
                title="Supplier Risk Scores"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )

    else:

        st.info("No supplier records available.")

else:

    st.warning("Supplier API returned no data.")


st.divider()


# ============================================================
# WEBSHIELD
# ============================================================

st.header("🛡️ WebShield Alerts")

if webshield_data:

    # Display the complete WebShield response
    if isinstance(webshield_data, dict):

        col1, col2, col3, col4 = st.columns(4)

        suspicious = (
            webshield_data.get("suspicious_listings")
            or webshield_data.get("suspicious")
            or 0
        )

        price_anomalies = (
            webshield_data.get("price_anomalies")
            or webshield_data.get("price_anomaly")
            or 0
        )

        counterfeit = (
            webshield_data.get("counterfeit_risks")
            or webshield_data.get("counterfeit")
            or 0
        )

        supplier_alerts = (
            webshield_data.get("supplier_web_alerts")
            or webshield_data.get("supplier_web_alerts")
            or webshield_data.get("supplier_alerts")
            or 0
        )

        with col1:
            st.metric(
                "Suspicious Listings",
                suspicious
            )

        with col2:
            st.metric(
                "Price Anomalies",
                price_anomalies
            )

        with col3:
            st.metric(
                "Counterfeit Risks",
                counterfeit
            )

        with col4:
            st.metric(
                "Supplier Web Alerts",
                supplier_alerts
            )

        st.subheader("WebShield API Response")

        st.json(webshield_data)

    else:

        st.write(webshield_data)

else:

    st.warning("No WebShield data available.")


st.divider()


# ============================================================
# RAW API DATA
# ============================================================

with st.expander("🔧 Developer / API Data"):

    st.subheader("Risk API")

    if risk_data:
        st.json(risk_data)

    st.subheader("Supplier API")

    if supplier_data:
        st.json(supplier_data)

    st.subheader("WebShield API")

    if webshield_data:
        st.json(webshield_data)

    st.subheader("Scraper Health API")

    if scraper_data:
        st.json(scraper_data)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SupplyShield AI — Detect the disruption before it reaches your supply chain."
)