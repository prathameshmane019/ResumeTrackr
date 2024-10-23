from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict
import logging
from app.utils.text_extractor import extract_text_from_file
from app.utils.resume_analyzer import ResumeAnalyzer
from app.utils.keyword_matcher import KeywordMatcher

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordMatch(BaseModel):
    keyword: str
    count: int

class AnalysisResult(BaseModel):
    total_score: float
    keyword_match: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    matched_keywords: List[KeywordMatch] = Field(default_factory=list)

@app.post("/analyze-resume", response_model=AnalysisResult)
async def analyze_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    logger.info("Received a request to analyze the resume.")

    try:
        resume_text = await extract_text_from_file(file)
        logger.info("Extracted text from resume.")
        
        resume_analyzer = ResumeAnalyzer()
        keyword_matcher = KeywordMatcher()

        analysis_result = resume_analyzer.analyze(resume_text)
        keyword_analysis = keyword_matcher.calculate_similarity(resume_text, job_description)

        total_score = analysis_result["score"] * 0.7 + keyword_analysis["keywordMatch"] * 0.3

        result = AnalysisResult(
            total_score=round(total_score, 2),
            keyword_match=keyword_analysis["keywordMatch"],
            strengths=analysis_result["strengths"],
            weaknesses=analysis_result["weaknesses"],
            suggestions=analysis_result["suggestions"],
            matched_keywords=[KeywordMatch(keyword=k["keyword"], count=k["count"]) for k in keyword_analysis["matches"]]
        )

        logger.info("Resume analysis completed successfully.")
        return result

    except ValueError as ve:
        logger.error(f"Error during resume analysis: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during resume analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"}, status_code=200)