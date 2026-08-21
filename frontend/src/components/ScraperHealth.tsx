import {
  Activity,
  CheckCircle2,
  XCircle,
  RotateCcw,
} from "lucide-react";

interface ScraperData {
  total_sources: number;
  healthy: number;
  failed: number;
  self_healed: number;
}

interface Props {
  data: ScraperData;
}

function ScraperHealth({ data }: Props) {

  const healthPercentage =
    (data.healthy / data.total_sources) * 100;

  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <h3>Scraper Health</h3>
          <p>Self-healing web data infrastructure</p>
        </div>

        <Activity size={20} />

      </div>

      <div className="health-score">

        <div className="health-circle">

          <strong>
            {healthPercentage.toFixed(0)}%
          </strong>

          <span>Healthy</span>

        </div>

        <div className="health-stats">

          <div>
            <CheckCircle2 size={18} />
            <span>Healthy</span>
            <strong>{data.healthy}</strong>
          </div>

          <div>
            <XCircle size={18} />
            <span>Failed</span>
            <strong>{data.failed}</strong>
          </div>

          <div>
            <RotateCcw size={18} />
            <span>Self-Healed</span>
            <strong>{data.self_healed}</strong>
          </div>

        </div>

      </div>

    </div>
  );
}

export default ScraperHealth;