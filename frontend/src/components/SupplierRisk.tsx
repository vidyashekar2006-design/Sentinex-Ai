import { Users } from "lucide-react";

interface Supplier {
  name: string;
  risk: number;
  status: string;
}

interface Props {
  suppliers: Supplier[];
}

function SupplierRisk({ suppliers }: Props) {

  return (
    <div className="panel">

      <div className="panel-header">

        <div>
          <h3>Supplier Risk</h3>
          <p>Current supplier exposure</p>
        </div>

        <Users size={20} />

      </div>

      <div className="supplier-table">

        {suppliers.map((supplier) => (

          <div
            className="supplier-row"
            key={supplier.name}
          >

            <div className="supplier-info">

              <div className="supplier-avatar">
                {supplier.name.charAt(0)}
              </div>

              <div>
                <strong>{supplier.name}</strong>

                <span
                  className={`badge ${supplier.status.toLowerCase()}`}
                >
                  {supplier.status}
                </span>
              </div>

            </div>

            <div className="supplier-risk">

              <div className="progress">

                <div
                  className={`progress-fill ${supplier.status.toLowerCase()}`}
                  style={{
                    width: `${supplier.risk}%`,
                  }}
                />

              </div>

              <strong>
                {supplier.risk}%
              </strong>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

export default SupplierRisk;