import {
  ShieldAlert,
  TrendingUp,
  
  Activity,
  AlertTriangle,
  CheckCircle2,
  Users,
} from "lucide-react";

interface Supplier {
  name: string;
  risk: number;
  status: string;
}

interface SupplierRiskProps {
  suppliers: Supplier[];
}

function SupplierRisk({ suppliers }: SupplierRiskProps) {
  const totalSuppliers = suppliers.length;

  const highRisk = suppliers.filter(
    (supplier) => supplier.risk >= 70
  ).length;

  const mediumRisk = suppliers.filter(
    (supplier) =>
      supplier.risk >= 40 && supplier.risk < 70
  ).length;

  const lowRisk = suppliers.filter(
    (supplier) => supplier.risk < 40
  ).length;

  const averageRisk =
    totalSuppliers > 0
      ? suppliers.reduce(
          (sum, supplier) => sum + supplier.risk,
          0
        ) / totalSuppliers
      : 0;

  const getRiskLevel = (risk: number) => {
    if (risk >= 70) return "HIGH";
    if (risk >= 40) return "MEDIUM";
    return "LOW";
  };

  const getRiskClass = (risk: number) => {
    if (risk >= 70) return "risk-high";
    if (risk >= 40) return "risk-medium";
    return "risk-low";
  };

  /*
   * Demo trend values are intentionally deterministic.
   * Replace these with /api/risk-trend data when you
   * connect the graph to the backend endpoint.
   */
  const trendData = [
    31,
    35,
    32,
    39,
    37,
    43,
    41,
    47,
    44,
    50,
    48,
    Math.max(averageRisk, 48),
  ];

  const maxTrend = Math.max(...trendData, 100);

  return (
    <div className="risk-intelligence">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="risk-page-header">

        <div>

          <div className="risk-eyebrow">
            <ShieldAlert size={15} />
            RISK INTELLIGENCE
          </div>

          <h2>
            Supplier Risk
          </h2>

          <p>
            Monitor supplier exposure, concentration
            and operational risk.
          </p>

        </div>

        <div className="risk-live-status">
          <span className="live-dot" />
          Live risk monitoring
        </div>

      </div>


      {/* =====================================================
          KPI CARDS
      ===================================================== */}

      <div className="risk-kpi-grid">

        {/* TOTAL */}

        <div className="risk-kpi-card">

          <div className="risk-kpi-top">

            <div className="risk-kpi-icon blue">
              <Users size={19} />
            </div>

            <span className="risk-kpi-label">
              TOTAL SUPPLIERS
            </span>

          </div>

          <strong>
            {totalSuppliers}
          </strong>

          <span className="risk-kpi-description">
            Suppliers monitored
          </span>

        </div>


        {/* HIGH */}

        <div className="risk-kpi-card">

          <div className="risk-kpi-top">

            <div className="risk-kpi-icon red">
              <ShieldAlert size={19} />
            </div>

            <span className="risk-kpi-label">
              HIGH RISK
            </span>

          </div>

          <strong>
            {highRisk}
          </strong>

          <span className="risk-kpi-description">
            Immediate attention
          </span>

        </div>


        {/* MEDIUM */}

        <div className="risk-kpi-card">

          <div className="risk-kpi-top">

            <div className="risk-kpi-icon orange">
              <AlertTriangle size={19} />
            </div>

            <span className="risk-kpi-label">
              MEDIUM RISK
            </span>

          </div>

          <strong>
            {mediumRisk}
          </strong>

          <span className="risk-kpi-description">
            Requires monitoring
          </span>

        </div>


        {/* AVERAGE */}

        <div className="risk-kpi-card">

          <div className="risk-kpi-top">

            <div className="risk-kpi-icon green">
              <Activity size={19} />
            </div>

            <span className="risk-kpi-label">
              AVG RISK
            </span>

          </div>

          <strong>
            {averageRisk.toFixed(1)}%
          </strong>

          <span className="risk-kpi-description">
            Network risk score
          </span>

        </div>

      </div>


      {/* =====================================================
          ANALYTICS GRID
      ===================================================== */}

      <div className="risk-analytics-grid">


        {/* =================================================
            RISK TREND
        ================================================= */}

        <div className="risk-chart-card">

          <div className="risk-card-header">

            <div>

              <span className="risk-card-eyebrow">
                NETWORK EXPOSURE
              </span>

              <h3>
                Risk Trend
              </h3>

              <p>
                Supplier risk movement over time
              </p>

            </div>

            <div className="trend-badge">

              <TrendingUp size={15} />

              <span>
                +8.4%
              </span>

            </div>

          </div>


          {/* CHART */}

          <div className="risk-chart">

            <div className="chart-y-axis">

              <span>100</span>
              <span>75</span>
              <span>50</span>
              <span>25</span>
              <span>0</span>

            </div>


            <div className="chart-area">

              <div className="chart-grid-line line-1" />
              <div className="chart-grid-line line-2" />
              <div className="chart-grid-line line-3" />
              <div className="chart-grid-line line-4" />


              <svg
                className="risk-svg"
                viewBox="0 0 1000 300"
                preserveAspectRatio="none"
              >

                <defs>

                  <linearGradient
                    id="riskGradient"
                    x1="0"
                    x2="0"
                    y1="0"
                    y2="1"
                  >

                    <stop
                      offset="0%"
                      stopColor="#2563eb"
                      stopOpacity="0.28"
                    />

                    <stop
                      offset="100%"
                      stopColor="#2563eb"
                      stopOpacity="0"
                    />

                  </linearGradient>

                </defs>


                <polygon
                  className="risk-area"
                  fill="url(#riskGradient)"
                  stroke="none"
                  points={`
                    ${trendData
                      .map((value, index) => {
                        const x =
                          (index /
                            (trendData.length - 1)) *
                          1000;

                        const y =
                          300 -
                          (value / maxTrend) *
                            250;

                        return `${x},${y}`;
                      })
                      .join(" ")}

                    1000,300
                    0,300
                  `}
                />


                <polyline
                  className="risk-line"
                  fill="none"
                  stroke="#2563eb"
                  strokeWidth={4}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  points={trendData
                    .map((value, index) => {

                      const x =
                        (index /
                          (trendData.length - 1)) *
                        1000;

                      const y =
                        300 -
                        (value / maxTrend) *
                          250;

                      return `${x},${y}`;

                    })
                    .join(" ")}
                />


                {trendData.map(
                  (value, index) => {

                    const x =
                      (index /
                        (trendData.length - 1)) *
                      1000;

                    const y =
                      300 -
                      (value / maxTrend) *
                        250;

                    return (
                      <circle
                        key={index}
                        className="risk-point"
                        fill="#ffffff"
                        stroke="#2563eb"
                        strokeWidth={4}
                        cx={x}
                        cy={y}
                        r="5"
                      />
                    );
                  }
                )}

              </svg>


              <div className="chart-x-axis">

                <span>Jan</span>
                <span>Feb</span>
                <span>Mar</span>
                <span>Apr</span>
                <span>May</span>
                <span>Jun</span>
                <span>Jul</span>
                <span>Aug</span>

              </div>

            </div>

          </div>

        </div>


        {/* =================================================
            RISK DISTRIBUTION
        ================================================= */}

        <div className="risk-distribution-card">

          <div className="risk-card-header">

            <div>

              <span className="risk-card-eyebrow">
                SUPPLIER EXPOSURE
              </span>

              <h3>
                Risk Distribution
              </h3>

            </div>

          </div>


          <div className="risk-donut-wrapper">

            <div
              className="risk-donut"
              style={{
                background: `conic-gradient(
                  #ef4444 0deg ${
                    totalSuppliers
                      ? (highRisk /
                          totalSuppliers) *
                        360
                      : 0
                  }deg,

                  #f59e0b ${
                    totalSuppliers
                      ? (highRisk /
                          totalSuppliers) *
                        360
                      : 0
                  }deg ${
                    totalSuppliers
                      ? ((highRisk +
                          mediumRisk) /
                          totalSuppliers) *
                        360
                      : 0
                  }deg,

                  #22c55e ${
                    totalSuppliers
                      ? ((highRisk +
                          mediumRisk) /
                          totalSuppliers) *
                        360
                      : 0
                  }deg 360deg
                )`,
              }}
            >

              <div className="risk-donut-inner">

                <strong>
                  {averageRisk.toFixed(0)}%
                </strong>

                <span>
                  Avg Risk
                </span>

              </div>

            </div>

          </div>


          <div className="distribution-list">

            <div>

              <span className="distribution-label">
                <i className="dot high" />
                High Risk
              </span>

              <strong>
                {highRisk}
              </strong>

            </div>


            <div>

              <span className="distribution-label">
                <i className="dot medium" />
                Medium Risk
              </span>

              <strong>
                {mediumRisk}
              </strong>

            </div>


            <div>

              <span className="distribution-label">
                <i className="dot low" />
                Low Risk
              </span>

              <strong>
                {lowRisk}
              </strong>

            </div>

          </div>

        </div>

      </div>


      {/* =====================================================
          SUPPLIER TABLE
      ===================================================== */}

      <div className="supplier-risk-table-card">

        <div className="risk-card-header">

          <div>

            <span className="risk-card-eyebrow">
              SUPPLIER NETWORK
            </span>

            <h3>
              Supplier Risk Exposure
            </h3>

            <p>
              Highest-risk suppliers requiring
              monitoring or intervention.
            </p>

          </div>

          <button className="risk-view-button">
            View all
          </button>

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


          {suppliers
            .slice()
            .sort(
              (a, b) => b.risk - a.risk
            )
            .slice(0, 6)
            .map((supplier, index) => {

              const level =
                getRiskLevel(
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
                        className={`risk-progress-fill ${getRiskClass(
                          supplier.risk
                        )}`}
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
                      className={`supplier-status ${getRiskClass(
                        supplier.risk
                      )}`}
                    >

                      {level === "HIGH" && (
                        <AlertTriangle size={13} />
                      )}

                      {level === "MEDIUM" && (
                        <Activity size={13} />
                      )}

                      {level === "LOW" && (
                        <CheckCircle2 size={13} />
                      )}

                      {level}

                    </span>

                  </div>

                </div>

              );
            })}

        </div>

      </div>


      {/* =====================================================
          RISK SIGNALS
      ===================================================== */}

      <div className="risk-signals">

        <div className="risk-signal-card">

          <div className="signal-icon red">
            <ShieldAlert size={18} />
          </div>

          <div>

            <span>
              HIGH-RISK EXPOSURE
            </span>

            <strong>
              {highRisk} suppliers
            </strong>

            <p>
              Require immediate review
            </p>

          </div>

        </div>


        <div className="risk-signal-card">

          <div className="signal-icon orange">
            <AlertTriangle size={18} />
          </div>

          <div>

            <span>
              MONITORING REQUIRED
            </span>

            <strong>
              {mediumRisk} suppliers
            </strong>

            <p>
              Showing moderate risk signals
            </p>

          </div>

        </div>


        <div className="risk-signal-card">

          <div className="signal-icon green">
            <CheckCircle2 size={18} />
          </div>

          <div>

            <span>
              LOW EXPOSURE
            </span>

            <strong>
              {lowRisk} suppliers
            </strong>

            <p>
              Currently within safe range
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default SupplierRisk;