from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update if frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for files
uploaded_files: Dict[str, bytes] = {}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        uploaded_files[file.filename] = content
        return {"filename": file.filename, "message": "File uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/query/")
async def query_file(filename: str, query: str):
    if filename not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found!")
    
    # Replace this mock logic with real file processing
    content = uploaded_files[filename]
    response = f"Query '{query}' processed on file '{filename}'. File size: {len(content)} bytes."
    return {"result": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
