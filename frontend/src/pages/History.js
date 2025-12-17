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

        {/* Loading */}
        {loading && <p>Loading history...</p>}

        {/* No history */}
        {!loading && history.length === 0 && (
          <p style={{ textAlign: "center", marginTop: "20px", color: "#888" }}>
            No user history found
          </p>
        )}

        {/* History Table */}
        {!loading && history.length > 0 && (
          <table className="history-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Image Name</th>
                <th>Detected Alphabet</th>
                <th>Date & Time</th>
              </tr>
            </thead>

            <tbody>
              {history.map((h, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{h.image_name}</td>
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
