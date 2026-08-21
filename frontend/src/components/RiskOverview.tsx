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
      value: `${risk.overall_risk}%`,
      icon: AlertTriangle,
      description: risk.risk_level,
      className: "danger",
    },
    {
      title: "Disruption Probability",
      value: `${(risk.disruption_probability * 100).toFixed(0)}%`,
      icon: TrendingUp,
      description: "Supply disruption",
      className: "warning",
    },
    {
      title: "Supplier Risk",
      value: `${(risk.supplier_risk * 100).toFixed(0)}%`,
      icon: Users,
      description: "Supplier exposure",
      className: "warning",
    },
    {
      title: "WebShield Risk",
      value: `${(risk.webshield_risk * 100).toFixed(0)}%`,
      icon: Globe,
      description: "Web intelligence",
      className: "danger",
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

              <span>{metric.title}</span>

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