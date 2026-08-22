import {
  AlertTriangle,
  TrendingUp,
  Users,
  Globe,
} from "lucide-react";

interface RiskData {
  overall_risk: number;
  risk_level: string;
  disruption_probability: number;
  supplier_risk: number;
  market_anomaly: number;
  webshield_risk: number;
}

interface Props {
  risk: RiskData;
}

function RiskOverview({ risk }: Props) {

  const metrics = [
    {
      title: "Overall Risk",
      value: `${risk.overall_risk.toFixed(2)}%`,
      icon: AlertTriangle,
      description: risk.risk_level,
      className:
        risk.overall_risk >= 70
          ? "danger"
          : risk.overall_risk >= 40
          ? "warning"
          : "success",
    },

    {
      title: "Disruption Probability",
      value: `${(
        risk.disruption_probability * 100
      ).toFixed(0)}%`,
      icon: TrendingUp,
      description: "Supply disruption",
      className:
        risk.disruption_probability >= 0.7
          ? "danger"
          : risk.disruption_probability >= 0.4
          ? "warning"
          : "success",
    },

    {
      title: "Supplier Risk",
      value: `${risk.supplier_risk.toFixed(2)}%`,
      icon: Users,
      description: "Supplier exposure",
      className:
        risk.supplier_risk >= 70
          ? "danger"
          : risk.supplier_risk >= 40
          ? "warning"
          : "success",
    },

    {
      title: "WebShield Risk",
      value: `${risk.webshield_risk.toFixed(2)}%`,
      icon: Globe,
      description: "Web intelligence",
      className:
        risk.webshield_risk >= 70
          ? "danger"
          : risk.webshield_risk >= 40
          ? "warning"
          : "success",
    },
  ];

  return (
    <div className="metric-grid">

      {metrics.map((metric) => {

        const Icon = metric.icon;

        return (
          <div
            className={`metric-card ${metric.className}`}
            key={metric.title}
          >

            <div className="metric-top">

              <span>
                {metric.title}
              </span>

              <div className="metric-icon">
                <Icon size={20} />
              </div>

            </div>

            <div className="metric-value">
              {metric.value}
            </div>

            <div className="metric-description">
              {metric.description}
            </div>

          </div>
        );
      })}

    </div>
  );
}

export default RiskOverview;