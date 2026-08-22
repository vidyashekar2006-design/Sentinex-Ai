import {
  Activity,
  CheckCircle2,
  XCircle,
  RotateCcw,
  Database,
  AlertTriangle,
  TrendingUp,
} from "lucide-react";

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

interface Props {
  data: ScraperData;
}

function ScraperHealth({ data }: Props) {
  const healthPercentage =
    data.total_sources > 0
      ? (data.healthy / data.total_sources) * 100
      : 0;

  const formattedLastRun = data.last_run
    ? new Date(data.last_run).toLocaleString()
    : "No run information";

  return (
    <div className="panel">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="panel-header">

        <div>
          <h3>Scraper Health</h3>

          <p>
            Self-healing web data infrastructure
          </p>
        </div>

        <Activity size={20} />

      </div>


      {/* =====================================================
          HEALTH OVERVIEW
      ===================================================== */}

      <div className="health-score">

        <div className="health-circle">

          <strong>
            {healthPercentage.toFixed(0)}%
          </strong>

          <span>
            Healthy
          </span>

        </div>


        <div className="health-stats">

          {/* HEALTHY */}

          <div>
            <CheckCircle2 size={18} />

            <span>
              Healthy
            </span>

            <strong>
              {data.healthy}
            </strong>
          </div>


          {/* FAILED */}

          <div>
            <XCircle size={18} />

            <span>
              Failed
            </span>

            <strong>
              {data.failed}
            </strong>
          </div>


          {/* SELF HEALED */}

          <div>
            <RotateCcw size={18} />

            <span>
              Self-Healed
            </span>

            <strong>
              {data.self_healed}
            </strong>
          </div>

        </div>

      </div>


      {/* =====================================================
          PIPELINE METRICS
      ===================================================== */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(3, minmax(0, 1fr))",
          gap: "12px",
          marginTop: "20px",
        }}
      >

        {/* SUCCESS RATE */}

        <div className="metric-card">

          <TrendingUp size={18} />

          <span>
            Success Rate
          </span>

          <strong>
            {data.success_rate.toFixed(2)}%
          </strong>

        </div>


        {/* RECORDS */}

        <div className="metric-card">

          <Database size={18} />

          <span>
            Records
          </span>

          <strong>
            {data.total_records}
          </strong>

        </div>


        {/* ANOMALIES */}

        <div className="metric-card">

          <AlertTriangle size={18} />

          <span>
            Price Anomalies
          </span>

          <strong>
            {data.price_anomalies}
          </strong>

        </div>

      </div>


      {/* =====================================================
          DATA QUALITY
      ===================================================== */}

      <div
        style={{
          marginTop: "18px",
          padding: "16px",
          borderRadius: "12px",
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}
      >

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "12px",
          }}
        >

          <span>
            Data Quality
          </span>

          <strong>
            {data.valid_records} / {data.total_records}
          </strong>

        </div>


        <div
          style={{
            height: "7px",
            borderRadius: "10px",
            background: "rgba(255,255,255,0.08)",
            overflow: "hidden",
          }}
        >

          <div
            style={{
              width:
                data.total_records > 0
                  ? `${(
                      (data.valid_records /
                        data.total_records) *
                      100
                    ).toFixed(2)}%`
                  : "0%",
              height: "100%",
              borderRadius: "10px",
              background:
                "linear-gradient(90deg, #22c55e, #4ade80)",
              transition: "width 0.5s ease",
            }}
          />

        </div>


        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: "8px",
            fontSize: "12px",
            opacity: 0.7,
          }}
        >

          <span>
            Valid: {data.valid_records}
          </span>

          <span>
            Invalid: {data.invalid_records}
          </span>

        </div>

      </div>


      {/* =====================================================
          SOURCE STATUS
      ===================================================== */}

      {data.sources && data.sources.length > 0 && (

        <div
          style={{
            marginTop: "20px",
          }}
        >

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "12px",
            }}
          >

            <div>

              <strong>
                Source Network
              </strong>

              <p
                style={{
                  margin: "4px 0 0",
                  fontSize: "12px",
                  opacity: 0.65,
                }}
              >
                Live Member 1 pipeline sources
              </p>

            </div>

            <span
              style={{
                fontSize: "12px",
                opacity: 0.7,
              }}
            >
              {data.total_sources} sources
            </span>

          </div>


          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "8px",
            }}
          >

            {data.sources.map((source) => (

              <div
                key={source.name}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "12px 14px",
                  borderRadius: "10px",
                  background:
                    "rgba(255,255,255,0.025)",
                  border:
                    "1px solid rgba(255,255,255,0.06)",
                }}
              >

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                  }}
                >

                  {source.status === "healthy" ? (
                    <CheckCircle2
                      size={17}
                    />
                  ) : (
                    <XCircle
                      size={17}
                    />
                  )}

                  <div>

                    <strong>
                      {source.name}
                    </strong>

                    <div
                      style={{
                        fontSize: "11px",
                        opacity: 0.55,
                        marginTop: "3px",
                      }}
                    >
                      {source.records} records
                    </div>

                  </div>

                </div>


                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    fontSize: "12px",
                  }}
                >

                  <span>
                    {source.price_anomalies} anomalies
                  </span>

                  <span
                    style={{
                      textTransform: "uppercase",
                      fontWeight: 600,
                    }}
                  >
                    {source.status}
                  </span>

                </div>

              </div>

            ))}

          </div>

        </div>

      )}


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <div
        style={{
          marginTop: "18px",
          paddingTop: "14px",
          borderTop:
            "1px solid rgba(255,255,255,0.07)",
          display: "flex",
          justifyContent: "space-between",
          gap: "15px",
          flexWrap: "wrap",
          fontSize: "11px",
          opacity: 0.6,
        }}
      >

        <span>
          Status: {data.status.toUpperCase()}
        </span>

        <span>
          Last run: {formattedLastRun}
        </span>

        <span>
          {data.data_source ||
            "Member 1 Supply-WebShield"}
        </span>

      </div>

    </div>
  );
}

export default ScraperHealth;