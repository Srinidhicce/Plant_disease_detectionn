import React, { useState } from "react";
import axios from "axios";
import "./style.css";

function UploadImage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) setPreviewUrl(URL.createObjectURL(selectedFile));
  };

const handleSubmit = async () => {
  if (!file) return alert("Please select an image first!");
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await axios.post("http://127.0.0.1:5000/api/leaf-predict", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    // Set the result from the backend response
    setResult({
      prediction: res.data.disease, // Disease name from the response
      remedy: res.data.remedy,
      imageUrl: res.data.imageUrl
    });
  } catch (err) {
    console.error(err);
    alert("Error uploading image or predicting disease");
  }
};


  return (
    <div className="prediction-container">
      <h2>Leaf Disease Detection</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Upload & Predict</button>

      {previewUrl && (
        <div className="prediction-image-preview">
          <img src={previewUrl} alt="Preview" />
        </div>
      )}

      {result && (
        <div className="prediction-result-box">
          <h3>Disease: {result.prediction}</h3>
          <p><strong>Remedy:</strong> {result.remedy}</p>
          <img
            src={`http://127.0.0.1:5000${result.imageUrl}`}
            alt="Result"
            className="result-image"
          />
        </div>
      )}
    </div>
  );
}

export default UploadImage;
