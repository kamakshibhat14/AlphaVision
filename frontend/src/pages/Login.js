import { useState } from "react";
import api from "../services/api";
import "../styles/main.css";
import { useNavigate } from "react-router-dom";


function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await api.post("/login", { email, password });
      alert(res.data.message);
      navigate("/detect");
    } catch (err) {
      alert(err.response?.data?.error || "Login failed");
    }

  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="login-overlay">
          <h1>Manage Your Recognition</h1>
          <p>
            Secure alphabet recognition system with real-time detection and
            history tracking.
          </p>
        </div>
      </div>


      {/* RIGHT SECTION */}
      <div className="login-right">
        <div className="login-card">
          <h2>Sign In</h2>

          <input
            type="text"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button onClick={handleLogin}>Login</button>

          <p className="login-hint">
            New user?{" "}
            <span
              style={{ color: "#6366f1", cursor: "pointer" }}
              onClick={() => navigate("/signup")}
            >
              Create account
            </span>
          </p>

        </div>
      </div>
    </div>
  );
}

export default Login;
