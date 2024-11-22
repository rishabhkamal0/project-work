import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(`File uploaded: ${res.data.filename}`);
    } catch (err) {
      console.error(err);
      alert("Failed to upload file.");
    }
  };

  const handleSummarize = async () => {
    if (!file) {
      alert("Please upload a file first!");
      return;
    }

    console.log("Requesting summary for:", file.name);

    try {
      const res = await axios.get("http://127.0.0.1:8000/summarize/", {
        params: { filename: file.name },
      });
      setSummary(res.data.summary);
    } catch (err) {
      console.error(err);
      alert("Failed to summarize file.");
    }
  };

  return (
    <div>
      <h1>File Upload and Summarization</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload File</button>
      <button onClick={handleSummarize}>Summarize File</button>
      <div>
        <h2>Summary:</h2>
        <p>{summary}</p>
      </div>
    </div>
  );
};

export default FileUpload;
