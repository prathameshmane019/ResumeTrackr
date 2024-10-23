# app/config/settings.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API Settings
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))

# Upload Settings
UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR', 'uploads'))
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 5 * 1024 * 1024))  # 5MB default
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', '.pdf,.doc,.docx').split(',')

# Create uploads directory if it doesn't exist
UPLOAD_PATH = BASE_DIR / UPLOAD_DIR
UPLOAD_PATH.mkdir(exist_ok=True)

# app/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.settings import UPLOAD_PATH, ALLOWED_EXTENSIONS
from app.utils.text_extractor import extract_text_from_file
from app.utils.resume_analyzer import ResumeAnalyzer
from app.utils.keyword_matcher import KeywordMatcher
from app.models.analysis import ResumeAnalysis
import os
import uuid

app = FastAPI(title="Resume Scorer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_PATH)), name="uploads")

@app.post("/api/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(None)
):
    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Save file with unique name
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_PATH / f"{file_id}{file_ext}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from file
        resume_text = extract_text_from_file(file_path)
        
        # Initialize analyzers
        resume_analyzer = ResumeAnalyzer()
        keyword_matcher = KeywordMatcher()
        
        # Perform analysis
        base_analysis = resume_analyzer.analyze(resume_text)
        
        # Add keyword matching if job description is provided
        if job_description:
            keyword_analysis = keyword_matcher.calculate_similarity(
                resume_text, 
                job_description
            )
            analysis = {**base_analysis, **keyword_analysis}
        else:
            analysis = base_analysis
            analysis["keywordMatch"] = 0
            analysis["matches"] = []
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return ResumeAnalysis(**analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}