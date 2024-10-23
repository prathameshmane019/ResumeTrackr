from pydantic import BaseModel
from typing import List, Dict

class KeywordMatch(BaseModel):
    keyword: str
    count: int

class ResumeAnalysis(BaseModel):
    score: float
    overallScore: float
    keywordMatch: float
    matches: List[KeywordMatch]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
