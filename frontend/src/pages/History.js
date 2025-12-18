import { useEffect, useState } from "react";
import api from "../services/api";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/history", { withCredentials: true })
      .then((res) => {
        setHistory(res.data);
        setLoading(false);
      })
      .catch(() => {
        setHistory([]);
        setLoading(false);
      });
  }, []);

  return (
    <div className="page-center">
      <div className="card history-card">
        <h2>Detection History</h2>

        
        {loading && <p>Loading history...</p>}

        
        {!loading && history.length === 0 && (
          <p style={{ textAlign: "center", marginTop: "20px", color: "#888" }}>
            No user history found
          </p>
        )}

        
        {!loading && history.length > 0 && (
          <table className="history-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Image Name</th>
                <th>Detected <br /> Alpha</th>
                <th>Date & Time</th>
              </tr>
            </thead>

            <tbody>
              {history.map((h, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>
                    <a
                      href={`${api.defaults.baseURL}${h.image_url}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ textDecoration: "none", color: "#4f46e5" }}
                    >
                      <img
                        src={`${api.defaults.baseURL}${h.image_url}`}
                        alt={h.image_name}
                        style={{
                          width: "60px",
                          height: "60px",
                          objectFit: "cover",
                          borderRadius: "8px",
                          display: "block",
                          marginBottom: "6px",
                        }}
                      />
                      <span>{h.image_name}</span>
                    </a>
                  </td>

                  <td>{h.detected_alphabet}</td>
                  <td>{h.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default History;
