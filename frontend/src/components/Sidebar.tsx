import {
  LayoutDashboard,
  ShieldAlert,
  Users,
  Globe,
  Activity,
  Bell,
} from "lucide-react";

interface SidebarProps {
  activePage: string;
  setActivePage: (page: string) => void;
}

function Sidebar({ activePage, setActivePage }: SidebarProps) {
  const menuItems = [
    {
      name: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Risk Intelligence",
      icon: ShieldAlert,
    },
    {
      name: "Suppliers",
      icon: Users,
    },
    {
      name: "WebShield",
      icon: Globe,
    },
    {
      name: "Scraper Health",
      icon: Activity,
    },
    {
      name: "Alerts",
      icon: Bell,
    },
  ];

  return (
    <aside className="sidebar">

      <div className="logo">
        <div className="logo-icon">
          🛡
        </div>

        <div>
          <h2>SupplyShield</h2>
          <span>AI Intelligence</span>
        </div>
      </div>

      <nav>

        {menuItems.map((item) => {

          const Icon = item.icon;

          return (
            <button
              key={item.name}
              className={`nav-item ${
                activePage === item.name ? "active" : ""
              }`}
              onClick={() => setActivePage(item.name)}
            >

              <Icon size={19} />

              <span>{item.name}</span>

            </button>
          );
        })}

      </nav>

      <div className="sidebar-footer">

        <div className="system-status">
          <span className="status-dot"></span>

          <div>
            <strong>System Online</strong>
            <small>All services operational</small>
          </div>
        </div>

      </div>

    </aside>
  );
}

export default Sidebar;