import {
  Users,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
} from "lucide-react";

interface Supplier {
  name: string;
  risk: number;
  status: string;
}

interface Props {
  suppliers: Supplier[];
}

function SupplierRisk({ suppliers }: Props) {


  const getRiskClass = (risk: number) => {

    if (risk >= 70) {
      return "high";
    }

    if (risk >= 40) {
      return "medium";
    }

    return "low";
  };


  const getRiskIcon = (risk: number) => {

    if (risk >= 70) {
      return <ShieldAlert size={16} />;
    }

    if (risk >= 40) {
      return <AlertTriangle size={16} />;
    }

    return <ShieldCheck size={16} />;
  };


  const visibleSuppliers =
    suppliers.slice(0, 6);


  return (

    <div className="panel">

      {/* HEADER */}

      <div className="panel-header">

        <div>

          <h3>
            Supplier Risk
          </h3>

          <p>
            Current supplier exposure across the network
          </p>

        </div>


        <Users
          size={19}
          color="#2563eb"
        />

      </div>


      {/* SUPPLIER LIST */}

      <div className="supplier-table">

        {visibleSuppliers.length === 0 ? (

          <div
            style={{
              padding: "35px 10px",
              textAlign: "center",
              color: "#94a3b8",
              fontSize: "11px",
            }}
          >

            No supplier intelligence available.

          </div>

        ) : (

          visibleSuppliers.map((supplier) => {

            const risk =
              Number(supplier.risk || 0);

            const riskClass =
              getRiskClass(risk);

            const status =
              supplier.status ||
              (
                risk >= 70
                  ? "HIGH"
                  : risk >= 40
                  ? "MEDIUM"
                  : "LOW"
              );


            return (

              <div
                className="supplier-row"
                key={supplier.name}
              >

                {/* SUPPLIER */}

                <div className="supplier-info">

                  <div className="supplier-avatar">

                    {supplier.name
                      .charAt(0)
                      .toUpperCase()}

                  </div>


                  <div>

                    <strong>
                      {supplier.name}
                    </strong>


                    <span
                      className={`badge ${riskClass}`}
                    >

                      {getRiskIcon(risk)}

                      <span
                        style={{
                          marginLeft: "4px",
                        }}
                      >
                        {status}
                      </span>

                    </span>

                  </div>

                </div>


                {/* RISK */}

                <div className="supplier-risk">

                  <div className="progress">

                    <div
                      className={`progress-fill ${riskClass}`}
                      style={{
                        width:
                          `${Math.min(
                            Math.max(risk, 0),
                            100
                          )}%`,
                      }}
                    />

                  </div>


                  <strong>
                    {risk.toFixed(1)}%
                  </strong>

                </div>

              </div>

            );

          })

        )}

      </div>


      {/* FOOTER */}

      {suppliers.length > 6 && (

        <div
          style={{
            marginTop: "13px",
            paddingTop: "12px",
            borderTop: "1px solid #eef2f6",
            color: "#64748b",
            fontSize: "10px",
            display: "flex",
            justifyContent: "space-between",
          }}
        >

          <span>
            Showing top 6 suppliers
          </span>

          <strong
            style={{
              color: "#2563eb",
            }}
          >
            {suppliers.length} total
          </strong>

        </div>

      )}

    </div>
  );
}

export default SupplierRisk;