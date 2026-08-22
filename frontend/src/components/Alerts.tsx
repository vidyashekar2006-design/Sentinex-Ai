import { AlertTriangle, ArrowUpRight } from "lucide-react";

interface Props {
  alerts: string[];
}

function Alerts({ alerts }: Props) {

  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <h3>Active Alerts</h3>
          <p>Recent supply chain warnings</p>
        </div>

        <span className="alert-count">
          {alerts.length}
        </span>

      </div>

      <div className="alert-list">

        {alerts.map((alert, index) => (

          <div
            className="alert-item"
            key={index}
          >

            <div className="alert-icon">
              <AlertTriangle size={18} />
            </div>

            <div className="alert-content">

              <strong>
                Supply Chain Alert
              </strong>

              <p>{alert}</p>

            </div>

            <ArrowUpRight size={18} />

          </div>

        ))}

      </div>

    </div>
  );
}

export default Alerts;