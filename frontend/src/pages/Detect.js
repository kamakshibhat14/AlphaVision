import { useState } from "react";
import api from "../services/api";

function Detect() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const detect = async () => {
    if (!file) {
      alert("Please select an image");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("image", file);

      const res = await api.post("/detect", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(res.data.detected_alphabet);
      setError("");
    } catch (err) {
      if (err.response?.status === 401) {
        setError("❌ Please login first");
      } else {
        setError("❌ Detection failed");
      }
    }
  };

  return (
    <div className="page-center">
      <div className="card">
        <h2>Upload Image</h2>

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={detect}>Detect Alphabet</button>

        {result && (
          <div className="result">
            Detected Alphabet: <strong>{result}</strong>
          </div>
        )}

        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </div>
  );
}

export default Detect;
