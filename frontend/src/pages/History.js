import { useEffect, useState } from "react";
import api from "../services/api";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/history")
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

        {history.length === 0 ? (
          <p className="no-history">No user history found</p>
        ) : (
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
