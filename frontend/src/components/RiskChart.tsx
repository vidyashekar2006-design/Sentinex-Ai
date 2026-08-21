import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface Props {
  risk: number;
}

function RiskChart({ risk }: Props) {

  const data = [
    { name: "Mon", risk: Math.max(risk - 18, 0) },
    { name: "Tue", risk: Math.max(risk - 10, 0) },
    { name: "Wed", risk: Math.max(risk - 14, 0) },
    { name: "Thu", risk: Math.max(risk - 5, 0) },
    { name: "Fri", risk },
  ];

  return (
    <div className="panel chart-panel">

      <div className="panel-header">

        <div>
          <h3>Risk Trend</h3>
          <p>Recent supply chain risk movement</p>
        </div>

      </div>

      <div className="chart-container">

        <ResponsiveContainer width="100%" height="100%">

          <LineChart data={data}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="name" />

            <YAxis domain={[0, 100]} />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="risk"
              strokeWidth={3}
              dot={{ r: 5 }}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default RiskChart;