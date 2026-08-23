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
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ShieldAlert,
} from "lucide-react";

import ScraperHealth from "./components/ScraperHealth";
import SupplierRisk from "./components/SupplierRisk";
import RiskOverview from "./components/RiskOverview";
import WebShield from "./components/WebShield";

// =========================================================
// TYPES
// =========================================================

interface Supplier {
  name: string;
  risk: number;
  status: string;
}

interface RiskData {
  overall_risk: number;
  risk_level: string;
  disruption_probability: number;
  supplier_risk: number;
  market_anomaly: number;
  webshield_risk: number;
}

interface WebShieldData {
  suspicious_listings: number;
  price_anomalies: number;
  counterfeit_risks: number;
  supplier_web_alerts: number;
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
    self_healing?: {
    status: string;
    source: string | null;
    reason: string | null;
    healing_started_at: string | null;
    repair_ready_at: string | null;
    healed_at: string | null;
    self_healed_count: number;
  };
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
  const [showIntro, setShowIntro] = useState(true);

useEffect(() => {
  const timer = setTimeout(() => {
    setShowIntro(false);
  }, 7000);

  return () => clearTimeout(timer);
}, []);

  const [sidebarOpen, setSidebarOpen] =
    useState(false);

  const [notificationOpen, setNotificationOpen] =
    useState(false);

  const [activePage, setActivePage] =
    useState("Dashboard");

  const [scraper, setScraper] =
    useState<ScraperData | null>(null);

  const [risk, setRisk] =
    useState<RiskData | null>(null);

  const [webshield, setWebshield] =
    useState<WebShieldData | null>(null);

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

self_healing:
  scraperData?.self_healing
    ? {
        status:
          typeof scraperData.self_healing.status === "string"
            ? scraperData.self_healing.status
            : "idle",

        source:
          scraperData.self_healing.source ?? null,

        reason:
          scraperData.self_healing.reason ?? null,

        healing_started_at:
          scraperData.self_healing.healing_started_at ?? null,

        repair_ready_at:
          scraperData.self_healing.repair_ready_at ?? null,

        healed_at:
          scraperData.self_healing.healed_at ?? null,

        self_healed_count:
          Number(
            scraperData.self_healing.self_healed_count ?? 0
          ),
      }
    : undefined,
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

        if (riskResponse.ok) {
          const riskData =
            await riskResponse.json();

          setRisk({
            overall_risk:
              Number(
                riskData?.overall_risk ?? 0
              ),

            risk_level:
              typeof riskData?.risk_level ===
              "string"
                ? riskData.risk_level
                : "UNKNOWN",

            disruption_probability:
              Number(
                riskData?.disruption_probability ??
                  0
              ),

            supplier_risk:
              Number(
                riskData?.supplier_risk ?? 0
              ),

            market_anomaly:
              Number(
                riskData?.market_anomaly ?? 0
              ),

            webshield_risk:
              Number(
                riskData?.webshield_risk ?? 0
              ),
          });
        } else {
          console.warn(
            "Risk API unavailable"
          );

          setRisk(null);
        }

        // -------------------------------------------------
        // WEBSHIELD API
        // -------------------------------------------------

        if (webshieldResponse.ok) {
          const webshieldData =
            await webshieldResponse.json();

          setWebshield({
            suspicious_listings:
              Number(
                webshieldData?.suspicious_listings ??
                  0
              ),

            price_anomalies:
              Number(
                webshieldData?.price_anomalies ?? 0
              ),

            counterfeit_risks:
              Number(
                webshieldData?.counterfeit_risks ??
                  0
              ),

            supplier_web_alerts:
              Number(
                webshieldData?.supplier_web_alerts ??
                  0
              ),
          });
        } else {
          console.warn(
            "WebShield API unavailable"
          );

          setWebshield(null);
        }

      } catch (err) {
        console.error(
          "Dashboard API error:",
          err
        );

        setError(
          "Unable to connect to the Sentinex AI backend."
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

  const interval = setInterval(() => {
    fetchDashboardData();
  }, 3000);

  return () => clearInterval(interval);
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

  const getSupplierRiskLevel = (
    supplier: Supplier
  ) => {
    if (supplier.status) {
      return supplier.status;
    }

    if (supplier.risk >= 70) {
      return "HIGH";
    }

    if (supplier.risk >= 40) {
      return "MEDIUM";
    }

    return "LOW";
  };

  const getSupplierRiskClass = (
    riskScore: number
  ) => {
    if (riskScore >= 70) {
      return "risk-high";
    }

    if (riskScore >= 40) {
      return "risk-medium";
    }

    return "risk-low";
  };

  // =======================================================
  // NOTIFICATIONS (derived from existing live state only)
  // =======================================================

  interface AlertItem {
    id: string;
    severity: "critical" | "warning" | "info";
    icon: typeof AlertTriangle;
    message: string;
  }

  const alerts: AlertItem[] = [];

  if (scraper && scraper.failed > 0) {
    alerts.push({
      id: "scraper-failed",
      severity: "critical",
      icon: XCircle,
      message: `${scraper.failed} scraper source${
        scraper.failed === 1 ? "" : "s"
      } failing`,
    });
  }

  if (scraper && scraper.self_healed > 0) {
    alerts.push({
      id: "scraper-self-healed",
      severity: "info",
      icon: CheckCircle2,
      message: `${scraper.self_healed} source${
        scraper.self_healed === 1 ? "" : "s"
      } self-healed`,
    });
  }

  if (webshield && webshield.supplier_web_alerts > 0) {
    alerts.push({
      id: "webshield-supplier-alerts",
      severity: "warning",
      icon: ShieldAlert,
      message: `${webshield.supplier_web_alerts} supplier web alert${
        webshield.supplier_web_alerts === 1 ? "" : "s"
      }`,
    });
  }

  if (webshield && webshield.price_anomalies > 0) {
    alerts.push({
      id: "webshield-price-anomalies",
      severity: "warning",
      icon: AlertTriangle,
      message: `${webshield.price_anomalies} price anomal${
        webshield.price_anomalies === 1 ? "y" : "ies"
      } detected`,
    });
  }

  if (webshield && webshield.suspicious_listings > 0) {
    alerts.push({
      id: "webshield-suspicious-listings",
      severity: "warning",
      icon: AlertTriangle,
      message: `${webshield.suspicious_listings} suspicious listing${
        webshield.suspicious_listings === 1 ? "" : "s"
      } detected`,
    });
  }

  if (risk && risk.risk_level === "HIGH") {
    alerts.push({
      id: "risk-high",
      severity: "critical",
      icon: AlertTriangle,
      message: "Overall risk level is HIGH",
    });
  }

  if (risk && risk.risk_level === "MEDIUM") {
    alerts.push({
      id: "risk-medium",
      severity: "warning",
      icon: AlertTriangle,
      message: "Overall risk level is MEDIUM",
    });
  }

  const toggleNotifications = () => {
    setNotificationOpen((prev) => !prev);
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
        <>

          {risk ? (
            <RiskOverview
              risk={risk}
            />
          ) : (
            <div className="dashboard-main-card">

              <div className="loading-card">

                <div className="loading-spinner">
                  <ShieldCheck size={22} />
                </div>

                <strong>
                  Loading risk intelligence
                </strong>

                <span>
                  Connecting to Sentinex AI API...
                </span>

              </div>

            </div>
          )}

          <SupplierRisk
            suppliers={suppliers}
          />

        </>
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
                  Connecting to Sentinex AI API...
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
        <div className="supplier-risk-table-card">

          <div className="risk-card-header">

            <div>

              <span className="risk-card-eyebrow">
                SUPPLIER NETWORK
              </span>

              <h3>
                Supplier Network
              </h3>

              <p>
                Live supplier risk data from the
                Sentinex AI backend.
              </p>

            </div>

            <strong>
              {suppliers.length} monitored
            </strong>

          </div>

          <div className="supplier-table">

            <div className="supplier-table-header">

              <span>
                SUPPLIER
              </span>

              <span>
                RISK SCORE
              </span>

              <span>
                STATUS
              </span>

            </div>

            {suppliers.length > 0 ? (
              suppliers
                .slice()
                .sort(
                  (a, b) => b.risk - a.risk
                )
                .map((supplier, index) => {

                  const level =
                    getSupplierRiskLevel(
                      supplier
                    );

                  const riskClass =
                    getSupplierRiskClass(
                      supplier.risk
                    );

                  return (

                    <div
                      className="supplier-row"
                      key={supplier.name}
                      style={{
                        animationDelay: `${index * 70}ms`,
                      }}
                    >

                      <div className="supplier-name">

                        <div className="supplier-avatar">
                          {supplier.name
                            .slice(0, 1)
                            .toUpperCase()}
                        </div>

                        <div>

                          <strong>
                            {supplier.name}
                          </strong>

                          <span>
                            Supplier #{index + 1}
                          </span>

                        </div>

                      </div>

                      <div className="supplier-risk-score">

                        <div className="risk-progress">

                          <div
                            className={`risk-progress-fill ${riskClass}`}
                            style={{
                              width: `${Math.min(
                                supplier.risk,
                                100
                              )}%`,
                            }}
                          />

                        </div>

                        <strong>
                          {supplier.risk.toFixed(1)}%
                        </strong>

                      </div>

                      <div>

                        <span
                          className={`supplier-status ${riskClass}`}
                        >
                          {level}
                        </span>

                      </div>

                    </div>

                  );
                })
            ) : (
              <div className="supplier-row">

                <div className="supplier-name">

                  <div className="supplier-avatar">
                    S
                  </div>

                  <div>

                    <strong>
                      No supplier records returned
                    </strong>

                    <span>
                      Waiting for backend supplier data
                    </span>

                  </div>

                </div>

                <span>
                  --
                </span>

                <span>
                  --
                </span>

              </div>
            )}

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

          {webshield ? (
            <WebShield
              data={webshield}
            />
          ) : (
            <div className="loading-card">

              <div className="loading-spinner">
                <Globe2 size={22} />
              </div>

              <strong>
                Loading WebShield intelligence
              </strong>

              <span>
                Connecting to Sentinex AI API...
              </span>

            </div>
          )}

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
                  Connecting to Sentinex AI API...
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
              Sentinex AI is continuously
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
            © 2026 Sentinex AI AI
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
  // INTRO SCREEN
  // =======================================================
  //
  // This check is placed AFTER every hook in the component
  // has already been called (all useState/useEffect/useCallback
  // calls above run unconditionally on every render), so this
  // early return is safe and will never cause a
  // "Rendered more hooks than during the previous render" error.
  //
  // It is placed BEFORE the dashboard's `return`, so the
  // dashboard shell (sidebar/topbar/content) does not render
  // into the DOM at all while the intro is showing.
  // =======================================================

  if (showIntro) {
    return (
      <div className="sentinex-intro">
        <video
  className="sentinex-intro-video"
  autoPlay
  muted
  playsInline
  preload="auto"
  onEnded={() => setShowIntro(false)}
  onError={() => {
    console.error("Intro video failed to load");
    setShowIntro(false);
  }}
>
  <source
    src="/assets/animation.mp4"
    type="video/mp4"
  />
  
  Your browser does not support this video.
</video>

        <button
          className="skip-intro"
          onClick={() => setShowIntro(false)}
        >
          Skip Intro
        </button>
      </div>
    );
  }

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
              Sentinex AI
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
              Sentinex AI monitoring services
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
                  Sentinex AI
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

            <div className="notification-wrapper">

              <button
                className="icon-button"
                aria-label={
                  alerts.length > 0
                    ? `Notifications, ${alerts.length} active alert${
                        alerts.length === 1 ? "" : "s"
                      }`
                    : "Notifications, no active alerts"
                }
                aria-expanded={notificationOpen}
                aria-haspopup="true"
                onClick={toggleNotifications}
              >

                <Bell size={19} />

                {alerts.length > 0 && (
                  <span className="notification-dot" />
                )}

              </button>

              {notificationOpen && (

                <div
                  className="notification-panel"
                  role="menu"
                >

                  <div className="notification-panel-header">

                    <strong>
                      Notifications
                    </strong>

                    <span
                      className={
                        alerts.length > 0
                          ? "notification-count notification-count-active"
                          : "notification-count"
                      }
                    >
                      {alerts.length}
                    </span>

                  </div>

                  <div className="notification-panel-body">

                    {alerts.length > 0 ? (
                      alerts.map((alert) => {

                        const AlertIcon = alert.icon;

                        return (
                          <div
                            className={`notification-item notification-${alert.severity}`}
                            key={alert.id}
                            role="menuitem"
                          >

                            <AlertIcon size={16} />

                            <span>
                              {alert.message}
                            </span>

                          </div>
                        );
                      })
                    ) : (
                      <div className="notification-item notification-healthy">

                        <CheckCircle2 size={16} />

                        <span>
                          No active alerts
                        </span>

                      </div>
                    )}

                  </div>

                </div>

              )}

            </div>

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
                  Sentinex AI
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
