from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from PyPDF2 import PdfReader
import io

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Update if frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded files
uploaded_files: Dict[str, bytes] = {}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Sanitize filename
        sanitized_filename = file.filename.strip()
        content = await file.read()
        uploaded_files[sanitized_filename] = content
        return {"filename": sanitized_filename, "message": "File uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/summarize/")
async def summarize_file(filename: str):
    # Log available files
    print(f"Available files: {list(uploaded_files.keys())}")

    # Check if file exists
    if filename not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found!")

    file_content = uploaded_files[filename]
    try:
        # Attempt to extract text from PDF
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            raise ValueError("No text found in the PDF. It may be an image-based PDF.")

        # Summarize text (mock example)
        summary = text[:500]  # Return the first 500 characters as a summary
        return {"filename": filename, "summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
