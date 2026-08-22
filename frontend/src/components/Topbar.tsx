import {
  Menu,
  ChevronRight,
  Bell,
  RefreshCw,
} from "lucide-react";

interface TopbarProps {
  activePage: string;
  refreshing: boolean;
  onMenu: () => void;
  onRefresh: () => void;
}

function Topbar({
  activePage,
  refreshing,
  onMenu,
  onRefresh,
}: TopbarProps) {
  const pageTitle =
    activePage === "Dashboard"
      ? "Supply Chain Intelligence"
      : activePage;

  return (
    <header className="topbar">
      {/* LEFT */}

      <div className="topbar-left">
        <button
          className="mobile-menu"
          onClick={onMenu}
          aria-label="Open navigation"
        >
          <Menu size={21} />
        </button>

        <div>
          <div className="breadcrumb">
            <span>Sentinex AI</span>

            <ChevronRight size={14} />

            <strong>
              {activePage}
            </strong>
          </div>

          <h1>{pageTitle}</h1>
        </div>
      </div>

      {/* RIGHT */}

      <div className="topbar-actions">
        {/* LIVE */}

        <div className="topbar-live">
          <span className="live-dot" />

          <span>Live</span>
        </div>

        {/* REFRESH */}

        <button
          className={`icon-button ${
            refreshing ? "refreshing" : ""
          }`}
          onClick={onRefresh}
          aria-label="Refresh dashboard"
          title="Refresh dashboard"
        >
          <RefreshCw size={18} />
        </button>

        {/* NOTIFICATIONS */}

        <button
          className="icon-button"
          aria-label="Notifications"
        >
          <Bell size={19} />

          <span className="notification-dot" />
        </button>

        {/* PROFILE */}

        <button className="profile-button">
          <div className="profile-avatar">
            VS
          </div>

          <div className="profile-info">
            <strong>
              Sentinex AI
            </strong>

            <span>
              Administrator
            </span>
          </div>
        </button>
      </div>
    </header>
  );
}

export default Topbar;
