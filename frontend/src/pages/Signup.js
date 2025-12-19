import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]).{6,}$/;
  const [passwordError, setPasswordError] = useState("");

  const handleSignup = async () => {
    if (!passwordRegex.test(password)) {
      setPasswordError(
        "Password must contain letters, numbers, and special characters"
      );
      return;
    }
  
    setPasswordError("");
    
    try {
      await api.post("/signup", { email, password });
      alert("Signup successful. Please login.");
      navigate("/");
    } catch (err) {
      alert(err.response?.data?.message || "Signup failed");
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

  <div className="login-right">
        <div className="login-card">
        <h2>Create Account</h2>

        <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
        />

        {passwordError && (
          <p style={{ color: "red", fontSize: "13px", marginTop: "8px" }}>
            ! {passwordError}
          </p>
        )}

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
