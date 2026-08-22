import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  LayoutDashboard,
  ShieldCheck,
  Users,
  Globe2,
  Activity,
  Bell,
  Settings,
  Menu,
  X,
  ChevronRight,
  Sparkles,
} from "lucide-react";

import ScraperHealth from "./components/ScraperHealth";
import SupplierRisk from "./components/SupplierRisk";

// =========================================================
// TYPES
// =========================================================

interface Supplier {
  name: string;
  risk: number;
  status: string;
}
interface ScraperSource {
  name: string;
  status: string;
  records: number;
  valid: number;
  invalid: number;
  schema_warnings: number;
  price_anomalies: number;
  data_source: string;
  file: string;
}

interface ScraperData {
  total_sources: number;
  healthy: number;
  failed: number;
  self_healed: number;
  success_rate: number;
  total_records: number;
  valid_records: number;
  invalid_records: number;
  price_anomalies: number;
  last_run: string | null;
  status: string;
  data_source?: string;
  sources?: ScraperSource[];
}

interface NavItem {
  label: string;
  icon: React.ReactNode;
}

// =========================================================
// NAVIGATION
// =========================================================

const navItems: NavItem[] = [
  {
    label: "Dashboard",
    icon: <LayoutDashboard size={18} />,
  },
  {
    label: "Risk Intelligence",
    icon: <ShieldCheck size={18} />,
  },
  {
    label: "Supplier Network",
    icon: <Users size={18} />,
  },
  {
    label: "WebShield",
    icon: <Globe2 size={18} />,
  },
  {
    label: "Scraper Health",
    icon: <Activity size={18} />,
  },
];

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
// If VITE_API_BASE_URL is not provided, localhost is used.
// =========================================================

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";

// =========================================================
// APP
// =========================================================

function App() {
  const [sidebarOpen, setSidebarOpen] =
    useState(false);

  const [activePage, setActivePage] =
    useState("Dashboard");

  const [scraper, setScraper] =
    useState<ScraperData | null>(null);

  const [suppliers, setSuppliers] =
    useState<Supplier[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  // =======================================================
  // FETCH DASHBOARD DATA
  // =======================================================

  const fetchDashboardData =
    useCallback(async () => {
      setLoading(true);
      setError(null);

      try {
        const [
          riskResponse,
          suppliersResponse,
          webshieldResponse,
          scraperResponse,
        ] = await Promise.all([
          fetch(
            `${API_BASE_URL}/api/risk`
          ),

          fetch(
            `${API_BASE_URL}/api/suppliers`
          ),

          fetch(
            `${API_BASE_URL}/api/webshield`
          ),

          fetch(
            `${API_BASE_URL}/api/scraper-health`
          ),
        ]);

        // -------------------------------------------------
        // SCRAPER HEALTH
        // -------------------------------------------------

        if (!scraperResponse.ok) {
          throw new Error(
            `Scraper health API failed with status ${scraperResponse.status}`
          );
        }

        const scraperData =
          await scraperResponse.json();

        /*
         * Ensure the object always has a string status.
         *
         * This also protects the frontend if the backend
         * temporarily returns an incomplete response.
         */

        const normalizedScraperData: ScraperData = {
          total_sources:
            Number(
              scraperData?.total_sources ?? 0
            ),

          healthy:
            Number(
              scraperData?.healthy ?? 0
            ),

          failed:
            Number(
              scraperData?.failed ?? 0
            ),

          self_healed:
            Number(
              scraperData?.self_healed ?? 0
            ),

          success_rate:
            Number(
              scraperData?.success_rate ?? 0
            ),

          total_records:
            Number(
              scraperData?.total_records ?? 0
            ),

          valid_records:
            Number(
              scraperData?.valid_records ?? 0
            ),

          invalid_records:
            Number(
              scraperData?.invalid_records ?? 0
            ),

          price_anomalies:
            Number(
              scraperData?.price_anomalies ?? 0
            ),

          last_run:
            scraperData?.last_run ?? null,

          // REQUIRED STRING
          status:
            typeof scraperData?.status ===
            "string"
              ? scraperData.status
              : "unknown",

          data_source:
            scraperData?.data_source,

          sources:
            Array.isArray(
              scraperData?.sources
            )
              ? scraperData.sources
              : [],
        };

        setScraper(
          normalizedScraperData
        );

        // -------------------------------------------------
        // SUPPLIERS
        // -------------------------------------------------

        if (suppliersResponse.ok) {
          const supplierData =
            await suppliersResponse.json();

          /*
           * Backend may return:
           *
           * [
           *   {...}
           * ]
           *
           * OR:
           *
           * {
           *   suppliers: [...]
           * }
           */

          if (
            Array.isArray(
              supplierData
            )
          ) {
            setSuppliers(
              supplierData
            );
          } else if (
            Array.isArray(
              supplierData?.suppliers
            )
          ) {
            setSuppliers(
              supplierData.suppliers
            );
          } else {
            setSuppliers([]);
          }
        } else {
          console.warn(
            "Supplier API unavailable"
          );
        }

        // -------------------------------------------------
        // RISK API
        // -------------------------------------------------

        if (!riskResponse.ok) {
          console.warn(
            "Risk API unavailable"
          );
        }

        // -------------------------------------------------
        // WEBSHIELD API
        // -------------------------------------------------

        if (!webshieldResponse.ok) {
          console.warn(
            "WebShield API unavailable"
          );
        }

      } catch (err) {
        console.error(
          "Dashboard API error:",
          err
        );

        setError(
          "Unable to connect to the SupplyShield backend."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  // =======================================================
  // INITIAL LOAD
  // =======================================================

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  // =======================================================
  // NAVIGATION
  // =======================================================

  const handleNavigation = (
    label: string
  ) => {
    setActivePage(label);
    setSidebarOpen(false);
  };

  // =======================================================
  // PAGE CONTENT
  // =======================================================

  const renderPageContent = () => {

    // -----------------------------------------------------
    // RISK INTELLIGENCE
    // -----------------------------------------------------

    if (
      activePage ===
      "Risk Intelligence"
    ) {
      return (
        <SupplierRisk
          suppliers={suppliers}
        />
      );
    }

    // -----------------------------------------------------
    // SCRAPER HEALTH
    // -----------------------------------------------------

    if (
      activePage ===
      "Scraper Health"
    ) {
      return (
        <div className="dashboard-grid">

          <div className="dashboard-main-card">

            {scraper ? (
              <ScraperHealth
                data={scraper}
              />
            ) : (
              <div className="loading-card">

                <div className="loading-spinner">
                  <Activity size={22} />
                </div>

                <strong>
                  Loading scraper intelligence
                </strong>

                <span>
                  Connecting to SupplyShield API...
                </span>

              </div>
            )}

          </div>

        </div>
      );
    }

    // -----------------------------------------------------
    // SUPPLIER NETWORK
    // -----------------------------------------------------

    if (
      activePage ===
      "Supplier Network"
    ) {
      return (
        <div className="dashboard-main-card">

          <div className="loading-card">

            <div className="loading-spinner">
              <Users size={22} />
            </div>

            <strong>
              Supplier Network
            </strong>

            <span>
              Supplier intelligence module
              is connected.
            </span>

          </div>

        </div>
      );
    }

    // -----------------------------------------------------
    // WEBSHIELD
    // -----------------------------------------------------

    if (
      activePage ===
      "WebShield"
    ) {
      return (
        <div className="dashboard-main-card">

          <div className="loading-card">

            <div className="loading-spinner">
              <Globe2 size={22} />
            </div>

            <strong>
              WebShield Monitoring
            </strong>

            <span>
              Web intelligence and anomaly
              monitoring is active.
            </span>

          </div>

        </div>
      );
    }

    // -----------------------------------------------------
    // DEFAULT DASHBOARD
    // -----------------------------------------------------

    return (
      <>

        {/* =================================================
            PAGE INTRO
        ================================================= */}

        <div className="page-intro">

          <div>

            <div className="eyebrow">

              <Sparkles size={14} />

              <span>
                AI-POWERED SUPPLY INTELLIGENCE
              </span>

            </div>

            <h2>
              Monitor your supply ecosystem
            </h2>

            <p>
              Real-time visibility into supplier
              risk, market intelligence and
              web data health.
            </p>

          </div>

          <div className="intro-status">

            <div className="intro-status-icon">
              <Activity size={18} />
            </div>

            <div>

              <span>
                Monitoring Status
              </span>

              <strong>
                {scraper?.status ===
                "healthy"
                  ? "All systems operational"
                  : scraper?.status ||
                    "Monitoring"}
              </strong>

            </div>

          </div>

        </div>

        {/* =================================================
            ERROR MESSAGE
        ================================================= */}

        {error && (
          <div className="dashboard-error">

            <Activity size={18} />

            <span>
              {error}
            </span>

          </div>
        )}

        {/* =================================================
            KPI STRIP
        ================================================= */}

        <div className="kpi-grid">

          {/* RISK ENGINE */}

          <div className="kpi-card">

            <div className="kpi-icon blue">
              <ShieldCheck size={20} />
            </div>

            <div>

              <span>
                Risk Engine
              </span>

              <strong>
                Active
              </strong>

            </div>

            <div className="kpi-indicator">
              <span />
            </div>

          </div>

          {/* DATA PIPELINE */}

          <div className="kpi-card">

            <div className="kpi-icon green">
              <Activity size={20} />
            </div>

            <div>

              <span>
                Data Pipeline
              </span>

              <strong>

                {loading
                  ? "Loading..."
                  : scraper?.status ===
                    "healthy"
                    ? "Operational"
                    : scraper?.status ||
                      "Operational"}

              </strong>

            </div>

            <div className="kpi-indicator">
              <span />
            </div>

          </div>

          {/* WEBSHIELD */}

          <div className="kpi-card">

            <div className="kpi-icon purple">
              <Globe2 size={20} />
            </div>

            <div>

              <span>
                WebShield
              </span>

              <strong>
                Monitoring
              </strong>

            </div>

            <div className="kpi-indicator">
              <span />
            </div>

          </div>

          {/* SUPPLIER NETWORK */}

          <div className="kpi-card">

            <div className="kpi-icon orange">
              <Users size={20} />
            </div>

            <div>

              <span>
                Supplier Network
              </span>

              <strong>

                {suppliers.length > 0
                  ? `${suppliers.length} Connected`
                  : "Connected"}

              </strong>

            </div>

            <div className="kpi-indicator">
              <span />
            </div>

          </div>

        </div>

        {/* =================================================
            DASHBOARD GRID
        ================================================= */}

        <div className="dashboard-grid">

          {/* SCRAPER HEALTH */}

          <div className="dashboard-main-card">

            {scraper ? (

              <ScraperHealth
                data={scraper}
              />

            ) : (

              <div className="loading-card">

                <div className="loading-spinner">

                  <Activity
                    size={22}
                  />

                </div>

                <strong>
                  Loading scraper intelligence
                </strong>

                <span>
                  Connecting to SupplyShield API...
                </span>

              </div>

            )}

          </div>

          {/* AI INSIGHT */}

          <div className="intelligence-card">

            <div className="intelligence-header">

              <div className="intelligence-icon">

                <Sparkles size={18} />

              </div>

              <span>
                AI INSIGHT
              </span>

            </div>

            <h3>
              Supply network
              monitoring active
            </h3>

            <p>
              SupplyShield is continuously
              monitoring your supplier ecosystem
              for anomalies, data quality issues
              and operational risk signals.
            </p>

            <div className="insight-divider" />

            <div className="insight-row">

              <span>
                Pipeline status
              </span>

              <strong>
                {scraper?.status ||
                  "Operational"}
              </strong>

            </div>

            <div className="insight-row">

              <span>
                Sources monitored
              </span>

              <strong>
                {scraper?.total_sources ??
                  "--"}
              </strong>

            </div>

            <div className="insight-row">

              <span>
                Records processed
              </span>

              <strong>
                {scraper?.total_records ??
                  "--"}
              </strong>

            </div>

            <div className="insight-row">

              <span>
                Success rate
              </span>

              <strong>
                {scraper
                  ? `${scraper.success_rate}%`
                  : "--"}
              </strong>

            </div>

            <div className="insight-footer">

              <div className="pulse-ring">
                <span />
              </div>

              <span>
                Real-time monitoring enabled
              </span>

            </div>

          </div>

        </div>

        {/* =================================================
            FOOTER
        ================================================= */}

        <footer className="dashboard-footer">

          <span>
            © 2026 SupplyShield AI
          </span>

          <span>
            Intelligent Supply Chain Risk Platform
          </span>

          <span className="footer-live">

            <span className="live-dot" />

            Systems operational

          </span>

        </footer>

      </>
    );
  };

  // =======================================================
  // RENDER
  // =======================================================

  return (
    <div className="app-shell">

      {/* =================================================
          BACKGROUND DECORATION
      ================================================= */}

      <div className="ambient-background">

        <div className="ambient-orb orb-one" />

        <div className="ambient-orb orb-two" />

        <div className="ambient-orb orb-three" />

      </div>

      {/* =================================================
          MOBILE OVERLAY
      ================================================= */}

      {sidebarOpen && (
        <div
          className="mobile-overlay"
          onClick={() =>
            setSidebarOpen(false)
          }
        />
      )}

      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside
        className={`sidebar ${
          sidebarOpen
            ? "sidebar-open"
            : ""
        }`}
      >

        {/* BRAND */}

        <div className="sidebar-brand">

          <div className="brand-logo">

            <ShieldCheck size={22} />

          </div>

          <div className="brand-text">

            <strong>
              SupplyShield
            </strong>

            <span>
              AI Intelligence
            </span>

          </div>

          <button
            className="mobile-close"
            onClick={() =>
              setSidebarOpen(false)
            }
            aria-label="Close navigation"
          >

            <X size={20} />

          </button>

        </div>

        {/* NAVIGATION */}

        <div className="sidebar-section">

          <span className="sidebar-label">
            PLATFORM
          </span>

          <nav className="sidebar-nav">

            {navItems.map(
              (item) => {

                const active =
                  activePage ===
                  item.label;

                return (

                  <button
                    key={item.label}
                    className={`nav-item ${
                      active
                        ? "nav-item-active"
                        : ""
                    }`}
                    onClick={() =>
                      handleNavigation(
                        item.label
                      )
                    }
                  >

                    <span className="nav-icon">
                      {item.icon}
                    </span>

                    <span>
                      {item.label}
                    </span>

                    {active && (
                      <ChevronRight
                        size={15}
                        className="nav-arrow"
                      />
                    )}

                  </button>

                );
              }
            )}

          </nav>

        </div>

        {/* SIDEBAR STATUS */}

        <div className="sidebar-bottom">

          <div className="system-card">

            <div className="system-card-header">

              <div className="live-dot" />

              <span>
                System Operational
              </span>

            </div>

            <p>
              SupplyShield monitoring services
              are running normally.
            </p>

            <div className="system-status-line">

              <span>
                API
              </span>

              <strong>
                Online
              </strong>

            </div>

          </div>

          <button className="sidebar-settings">

            <Settings size={17} />

            <span>
              Settings
            </span>

          </button>

        </div>

      </aside>

      {/* =================================================
          MAIN AREA
      ================================================= */}

      <main className="main-content">

        {/* =================================================
            TOPBAR
        ================================================= */}

        <header className="topbar">

          <div className="topbar-left">

            <button
              className="mobile-menu"
              onClick={() =>
                setSidebarOpen(true)
              }
              aria-label="Open navigation"
            >

              <Menu size={21} />

            </button>

            <div>

              <div className="breadcrumb">

                <span>
                  SupplyShield
                </span>

                <ChevronRight
                  size={14}
                />

                <strong>
                  {activePage}
                </strong>

              </div>

              <h1>

                {activePage ===
                "Dashboard"
                  ? "Supply Chain Intelligence"
                  : activePage}

              </h1>

            </div>

          </div>

          {/* TOPBAR ACTIONS */}

          <div className="topbar-actions">

            {/* LIVE */}

            <div className="topbar-live">

              <span className="live-dot" />

              <span>
                Live
              </span>

            </div>

            {/* NOTIFICATIONS */}

            <button
              className="icon-button"
              aria-label="Notifications"
            >

              <Bell size={19} />

              <span className="notification-dot" />

            </button>

            {/* PROFILE */}

            <button
              className="profile-button"
              aria-label="Profile"
            >

              <div className="profile-avatar">
                VS
              </div>

              <div className="profile-info">

                <strong>
                  SupplyShield
                </strong>

                <span>
                  Administrator
                </span>

              </div>

            </button>

          </div>

        </header>

        {/* =================================================
            PAGE CONTENT
        ================================================= */}

        <section className="page-content">

          {renderPageContent()}

        </section>

      </main>

    </div>
  );
}

export default App;