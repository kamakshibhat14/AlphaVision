import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
        const res = await api.post("/signup", { email, password });
        alert(res.data.message);
        navigate("/login");
      } catch (err) {
        alert(err.response?.data?.error || "Signup failed");
      }

  };

  return (
    <div className="login-container">
  {/* LEFT SIDE IMAGE */}
  <div className="login-left">
    <div className="login-overlay">
      <h1>Manage Your Recognition</h1>
      <p>
        Secure alphabet recognition system with real-time detection and
        history tracking.
      </p>
    </div>
  </div>

  {/* RIGHT SIDE FORM */}
  <div className="login-right">
        <div className="login-card">
        <h2>Create Account</h2>

        <input
            type="email"
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

        <button onClick={handleSignup}>Sign Up</button>

        <p className="login-hint">
            Already have an account? <span onClick={() => navigate("/")}>Login</span>
        </p>
            </div>
        </div>
    </div>

  );
}

export default Signup;
