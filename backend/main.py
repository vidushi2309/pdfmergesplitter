from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader, PdfWriter
import shutil
from pathlib import Path

app = FastAPI()

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with a specific URL in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/split-pdf/")
async def split_pdf(file: UploadFile = File(...), pages: str = Form(...)):
    """Splits a PDF based on selected page numbers."""
    pdf_path = UPLOAD_DIR / file.filename
    with pdf_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    selected_pages = list(map(int, pages.split(',')))
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page_num in selected_pages:
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    output_path = UPLOAD_DIR / f"split_{file.filename}"
    with output_path.open("wb") as output_pdf:
        writer.write(output_pdf)
    
    return {"message": "PDF split successfully", "download_url": f"/download/{output_path.name}"}

@app.post("/merge-pdf/")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    """Merges multiple PDFs into one and returns the file for download."""
    writer = PdfWriter()
    output_path = UPLOAD_DIR / "merged.pdf"
    
    for file in files:
        pdf_path = UPLOAD_DIR / file.filename
        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
    
    with output_path.open("wb") as merged_pdf:
        writer.write(merged_pdf)
    
    return {"message": "PDFs merged successfully", "download_url": f"/download/{output_path.name}"}


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Endpoint to download processed PDFs."""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}

@app.get("/")
def home():
    return {"message": "Welcome to the PDF Splitter/Merger API"}
