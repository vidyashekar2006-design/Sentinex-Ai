import { useCallback, useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import RiskOverview from "./components/RiskOverview";
import RiskChart from "./components/RiskChart";
import SupplierRisk from "./components/SupplierRisk";
import Alerts from "./components/Alerts";
import WebShield from "./components/WebShield";
import ScraperHealth from "./components/ScraperHealth";

// =========================================================
// TYPES
// =========================================================

interface RiskData {
  overall_risk: number;
  risk_level: string;
  disruption_probability: number;
  supplier_risk: number;
  market_anomaly: number;
  webshield_risk: number;
  alerts: string[];

  records_processed?: number;
  high_risk_records?: number;
  medium_risk_records?: number;
  low_risk_records?: number;
}

interface Supplier {
  name: string;
  risk: number;
  status: string;
}

interface WebShieldData {
  suspicious_listings: number;
  price_anomalies: number;
  counterfeit_risks: number;
  supplier_web_alerts: number;
  average_webshield_risk?: number;
}

interface ScraperData {
  total_sources: number;
  healthy: number;
  failed: number;
  self_healed: number;
  records_processed?: number;
  status?: string;
}

// =========================================================
// API CONFIGURATION
// =========================================================
//
// LOCAL:
// VITE_API_BASE_URL=http://localhost:8000
//
// LIVE:
// VITE_API_BASE_URL=https://your-backend-url.onrender.com
//
// =========================================================

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";

// =========================================================
// APP
// =========================================================

function App() {
  // =======================================================
  // NAVIGATION
  // =======================================================

  const [activePage, setActivePage] =
    useState("Dashboard");

  // =======================================================
  // API DATA
  // =======================================================

  const [risk, setRisk] =
    useState<RiskData | null>(null);

  const [suppliers, setSuppliers] =
    useState<Supplier[]>([]);

  const [webshield, setWebshield] =
    useState<WebShieldData | null>(null);

  const [scraper, setScraper] =
    useState<ScraperData | null>(null);

  // =======================================================
  // UI STATE
  // =======================================================

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [lastUpdated, setLastUpdated] =
    useState<Date | null>(null);

  // =======================================================
  // FETCH DASHBOARD DATA
  // =======================================================

  const fetchDashboardData = useCallback(
    async () => {
      try {
        setLoading(true);
        setError("");

        // ---------------------------------------------------
        // API REQUESTS
        // ---------------------------------------------------

        const [
          riskResponse,
          supplierResponse,
          webshieldResponse,
          scraperResponse,
        ] = await Promise.all([
          fetch(`${API_BASE_URL}/api/risk`),

          fetch(`${API_BASE_URL}/api/suppliers`),

          fetch(`${API_BASE_URL}/api/webshield`),

          fetch(`${API_BASE_URL}/api/scraper-health`),
        ]);

        // ---------------------------------------------------
        // CHECK RESPONSES
        // ---------------------------------------------------

        if (!riskResponse.ok) {
          throw new Error(
            `Risk API failed: ${riskResponse.status}`
          );
        }

        if (!supplierResponse.ok) {
          throw new Error(
            `Supplier API failed: ${supplierResponse.status}`
          );
        }

        if (!webshieldResponse.ok) {
          throw new Error(
            `WebShield API failed: ${webshieldResponse.status}`
          );
        }

        if (!scraperResponse.ok) {
          throw new Error(
            `Scraper API failed: ${scraperResponse.status}`
          );
        }

        // ---------------------------------------------------
        // PARSE JSON
        // ---------------------------------------------------

        const riskData: RiskData =
          await riskResponse.json();

        const supplierData =
          await supplierResponse.json();

        const webshieldData: WebShieldData =
          await webshieldResponse.json();

        const scraperData: ScraperData =
          await scraperResponse.json();

        // ---------------------------------------------------
        // UPDATE STATE
        // ---------------------------------------------------

        setRisk(riskData);

        setSuppliers(
          Array.isArray(supplierData.suppliers)
            ? supplierData.suppliers
            : []
        );

        setWebshield(webshieldData);

        setScraper(scraperData);

        setLastUpdated(new Date());

        console.log(
          "SupplyShield dashboard data loaded successfully."
        );

        console.log(
          "API:",
          API_BASE_URL
        );
      } catch (err) {
        console.error(
          "SupplyShield API Error:",
          err
        );

        setError(
          "Unable to connect to the SupplyShield backend. Make sure FastAPI is running and the API URL is correct."
        );
      } finally {
        setLoading(false);
      }
    },
    []
  );

  // =======================================================
  // INITIAL LOAD
  // =======================================================

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  // =======================================================
  // LOADING SCREEN
  // =======================================================

  if (loading && !risk) {
    return (
      <div className="loading-screen">

        <div className="loading-logo">
          🛡️
        </div>

        <h1>
          SupplyShield AI
        </h1>

        <p>
          Loading supply chain intelligence...
        </p>

        <div className="loading-spinner"></div>

      </div>
    );
  }

  // =======================================================
  // ERROR SCREEN
  // =======================================================

  if (error && !risk) {
    return (
      <div className="loading-screen">

        <div className="error-icon">
          !
        </div>

        <h1>
          SupplyShield AI
        </h1>

        <p>
          {error}
        </p>

        <button
          className="retry-button"
          onClick={fetchDashboardData}
        >
          Try Again
        </button>

      </div>
    );
  }

  // =======================================================
  // SAFETY CHECK
  // =======================================================

  if (
    !risk ||
    !webshield ||
    !scraper
  ) {
    return null;
  }

  // =======================================================
  // MAIN DASHBOARD
  // =======================================================

  return (
    <div className="app-shell">

      {/* =================================================
          SIDEBAR
          ================================================= */}

      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      {/* =================================================
          MAIN AREA
          ================================================= */}

      <div className="main-area">

        {/* =================================================
            HEADER
            ================================================= */}

        <Header
          onRefresh={fetchDashboardData}
          loading={loading}
        />

        {/* =================================================
            CONTENT
            ================================================= */}

        <main className="dashboard-content">

          {/* =================================================
              PAGE HEADING
              ================================================= */}

          <div className="page-heading">

            <div>

              <span className="eyebrow">
                SUPPLY CHAIN INTELLIGENCE
              </span>

              <h1>
                {activePage}
              </h1>

              <p>
                Monitor, predict and respond to
                supply chain disruptions.
              </p>

            </div>

            {/* =================================================
                LIVE STATUS
                ================================================= */}

            <div className="live-indicator">

              <span></span>

              Live Data

            </div>

          </div>

          {/* =================================================
              LAST UPDATED
              ================================================= */}

          {lastUpdated && (
            <div
              style={{
                marginBottom: "18px",
                color: "#64748b",
                fontSize: "11px",
              }}
            >
              Last updated:{" "}

              {lastUpdated.toLocaleTimeString()}
            </div>
          )}

          {/* =================================================
              DASHBOARD
              ================================================= */}

          {activePage === "Dashboard" && (
            <>

              {/* RISK OVERVIEW */}

              <RiskOverview
                risk={risk}
              />

              {/* RISK + SUPPLIER */}

              <div className="dashboard-grid">

                <RiskChart
                  risk={risk.overall_risk}
                />

                <SupplierRisk
                  suppliers={suppliers}
                />

              </div>

              {/* ALERTS + WEBSHIELD */}

              <div className="dashboard-grid">

                <Alerts
                  alerts={risk.alerts}
                />

                <WebShield
                  data={webshield}
                />

              </div>

              {/* SCRAPER HEALTH */}

              <ScraperHealth
                data={scraper}
              />

            </>
          )}

          {/* =================================================
              RISK INTELLIGENCE
              ================================================= */}

          {activePage === "Risk Intelligence" && (
            <>

              <RiskOverview
                risk={risk}
              />

              <div className="dashboard-grid">

                <RiskChart
                  risk={risk.overall_risk}
                />

                <Alerts
                  alerts={risk.alerts}
                />

              </div>

            </>
          )}

          {/* =================================================
              SUPPLIERS
              ================================================= */}

          {activePage === "Suppliers" && (
            <SupplierRisk
              suppliers={suppliers}
            />
          )}

          {/* =================================================
              WEBSHIELD
              ================================================= */}

          {activePage === "WebShield" && (
            <WebShield
              data={webshield}
            />
          )}

          {/* =================================================
              SCRAPER HEALTH
              ================================================= */}

          {activePage === "Scraper Health" && (
            <ScraperHealth
              data={scraper}
            />
          )}

          {/* =================================================
              ALERTS
              ================================================= */}

          {activePage === "Alerts" && (
            <Alerts
              alerts={risk.alerts}
            />
          )}

        </main>

      </div>

    </div>
  );
}

export default App;