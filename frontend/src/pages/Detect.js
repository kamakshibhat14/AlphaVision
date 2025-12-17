import { useState } from "react";
import api from "../services/api";

function Detect() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const detect = async () => {
    if (!file) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    const res = await api.post("/detect", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      withCredentials: true,   // ⭐ THIS LINE FIXES 401
    });

    setResult(res.data.detected_alphabet);
  };

  return (
    <div className="page-center">
      <div className="card detect-card">
        <h2>Upload Image</h2>

        <input type="file" onChange={(e) => {
          setFile(e.target.files[0]);
          setResult("");
        }} />

        <button onClick={detect}>Detect Alphabet</button>

        {result && (
          <div className="detect-result-box">
            <span>Detected Alphabet:</span>
            <strong>{result}</strong>
          </div>
        )}
      </div>
    </div>
  );
}

export default Detect;
