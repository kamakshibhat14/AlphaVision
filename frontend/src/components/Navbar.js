import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Navbar({ setLoggedIn }) {
  const navigate = useNavigate();

  const logout = async () => {
    await api.post("/logout");
    setLoggedIn(false);
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
          <img src="/apple-touch-icon.png" alt="AV Logo" className="nav-logo-img" />
          <span>AlphaVision</span>
      </div>


      <ul className="navbar-menu">
        <li>
          <Link to="/detect">Detect</Link>
        </li>
        <li>
          <Link to="/history">History</Link>
        </li>
        <li>
          <button className="nav-logout" onClick={logout}>
            Logout
          </button>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
