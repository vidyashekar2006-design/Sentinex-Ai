import {
  ShieldCheck,
  AlertOctagon,
  Tag,
  PackageX,
} from "lucide-react";

interface WebShieldData {
  suspicious_listings: number;
  price_anomalies: number;
  counterfeit_risks: number;
  supplier_web_alerts: number;
}

interface Props {
  data: WebShieldData;
}

function WebShield({ data }: Props) {

  const items = [
    {
      title: "Suspicious Listings",
      value: data.suspicious_listings,
      icon: ShieldCheck,
    },
    {
      title: "Price Anomalies",
      value: data.price_anomalies,
      icon: Tag,
    },
    {
      title: "Counterfeit Risks",
      value: data.counterfeit_risks,
      icon: PackageX,
    },
    {
      title: "Supplier Web Alerts",
      value: data.supplier_web_alerts,
      icon: AlertOctagon,
    },
  ];

  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <h3>WebShield Intelligence</h3>
          <p>Web-based supply chain threat monitoring</p>
        </div>

        <ShieldCheck size={20} />

      </div>

      <div className="webshield-grid">

        {items.map((item) => {

          const Icon = item.icon;

          return (
            <div
              className="webshield-item"
              key={item.title}
            >

              <div className="webshield-icon">
                <Icon size={20} />
              </div>

              <div>

                <span>
                  {item.title}
                </span>

                <strong>
                  {item.value}
                </strong>

              </div>

            </div>
          );
        })}

      </div>

    </div>
  );
}

export default WebShield;