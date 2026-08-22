import { RefreshCw, Bell, Search } from "lucide-react";

interface HeaderProps {
  onRefresh: () => void;
  loading: boolean;
}

function Header({ onRefresh, loading }: HeaderProps) {
  return (
    <header className="topbar">

      <div className="search-box">

        <Search size={18} />

        <input
          placeholder="Search supply chain intelligence..."
        />

      </div>

      <div className="topbar-actions">

        <button
          className="icon-button"
          onClick={onRefresh}
          disabled={loading}
          title="Refresh data"
        >
          <RefreshCw
            size={19}
            className={loading ? "spin" : ""}
          />
        </button>

        <button className="icon-button">
          <Bell size={19} />
        </button>

        <div className="profile">

          <div className="avatar">
            SA
          </div>

          <div>
            <strong>Supply Admin</strong>
            <small>Administrator</small>
          </div>

        </div>

      </div>

    </header>
  );
}

export default Header;