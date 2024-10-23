import spacy
from typing import Dict, List
import re

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def analyze(self, text: str) -> Dict:
        doc = self.nlp(text)
        
        scores = {
            "action_verbs": self._analyze_action_verbs(doc),
            "quantified_achievements": self._analyze_quantified_achievements(text),
            "structure": self._analyze_structure(text),
            "technical_skills": self._analyze_technical_skills(doc),
            "education": self._analyze_education(text)
        }
        
        strengths = []
        weaknesses = []
        suggestions = []
        
        total_score = sum(scores.values())
        
        if scores["action_verbs"] >= 15:
            strengths.append("Strong use of action verbs")
        else:
            weaknesses.append("Limited use of action verbs")
            suggestions.append("Use more powerful action verbs to describe your achievements")
            
        if scores["quantified_achievements"] >= 15:
            strengths.append("Good quantification of achievements")
        else:
            weaknesses.append("Limited quantification of achievements")
            suggestions.append("Add more specific numbers and metrics to demonstrate impact")
            
        if scores["structure"] >= 15:
            strengths.append("Well-structured resume")
        else:
            weaknesses.append("Improve resume structure")
            suggestions.append("Organize your resume into clear sections (e.g., Summary, Experience, Skills, Education)")
            
        if scores["technical_skills"] >= 15:
            strengths.append("Strong technical skills section")
        else:
            weaknesses.append("Limited technical skills mentioned")
            suggestions.append("Highlight more relevant technical skills for the position")
            
        if scores["education"] >= 15:
            strengths.append("Clear education section")
        else:
            weaknesses.append("Education section needs improvement")
            suggestions.append("Ensure your education details are clearly presented")
        
        return {
            "score": round(total_score / 5, 2),  # Average score out of 20
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions
        }
        
    def _analyze_action_verbs(self, doc) -> float:
        action_verbs = ["achieved", "improved", "developed", "managed", "created", "implemented", "led", "increased", "reduced", "negotiated"]
        count = sum(1 for token in doc if token.lemma_.lower() in action_verbs)
        return min(count * 2, 20)  # Max 20 points
        
    def _analyze_quantified_achievements(self, text: str) -> float:
        number_pattern = r'\d+%|\d+\s(?:percent|million|billion|thousand)'
        quantities = re.findall(number_pattern, text, re.IGNORECASE)
        return min(len(quantities) * 4, 20)  # Max 20 points
        
    def _analyze_structure(self, text: str) -> float:
        sections = ["summary", "experience", "education", "skills", "projects"]
        found_sections = sum(1 for section in sections if section in text.lower())
        return min(found_sections * 4, 20)  # Max 20 points
        
    def _analyze_technical_skills(self, doc) -> float:
        technical_terms = set(["python", "javascript", "java", "sql", "aws", "docker", "kubernetes", "react", "angular", "vue", "node.js", "mongodb", "postgresql"])
        found_terms = sum(1 for token in doc if token.text.lower() in technical_terms)
        return min(found_terms * 2, 20)  # Max 20 points
        
    def _analyze_education(self, text: str) -> float:
        education_keywords = ["degree", "university", "bachelor", "master", "phd", "diploma", "certificate"]
        found_keywords = sum(1 for keyword in education_keywords if keyword in text.lower())
        return min(found_keywords * 3, 20)  # Max 20 points