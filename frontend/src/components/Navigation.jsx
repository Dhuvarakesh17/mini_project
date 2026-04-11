import { Link, useLocation } from "react-router-dom";

export default function Navigation() {
  const location = useLocation();

  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-logo">
          <h1 className="logo-text">❤️ Heart Risk Intelligence</h1>
        </div>
        <ul className="nav-links">
          <li>
            <Link
              to="/"
              className={`nav-link ${location.pathname === "/" ? "active" : ""}`}
            >
              Dashboard
            </Link>
          </li>
          <li>
            <Link
              to="/reports"
              className={`nav-link ${location.pathname === "/reports" ? "active" : ""}`}
            >
              Reports
            </Link>
          </li>
          <li>
            <Link
              to="/risk-factors"
              className={`nav-link ${location.pathname === "/risk-factors" ? "active" : ""}`}
            >
              Heart Risk Factors
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
