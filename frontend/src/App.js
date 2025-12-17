import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Detect from "./pages/Detect";
import History from "./pages/History";
import Navbar from "./components/Navbar";
import Signup from "./pages/Signup";

import "./styles/main.css";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <BrowserRouter>
      <div className="app-layout">
        {loggedIn && <Navbar setLoggedIn={setLoggedIn} />}

        <div className="content-wrapper">
          <Routes>
            <Route
              path="/"
              element={
                loggedIn ? (
                  <Navigate to="/detect" />
                ) : (
                  <Login onLogin={setLoggedIn} />
                )
              }
            />
            <Route path="/signup" element={<Signup />} />


            <Route
              path="/detect"
              element={loggedIn ? <Detect /> : <Navigate to="/" />}
            />


            <Route
              path="/history"
              element={loggedIn ? <History /> : <Navigate to="/" />}
            />
          </Routes>
        </div>

        {loggedIn && (
          <footer className="footer">
            © 2025 Alphabet Recognition System
          </footer>
        )}
      </div>
    </BrowserRouter>
  );
}

export default App;
