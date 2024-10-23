from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import spacy
import re

class KeywordMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer()

    def extract_keywords(self, text: str) -> List[str]:
        doc = self.nlp(text.lower())
        keywords = []
        
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] or token.ent_type_ in ['SKILL', 'ORG', 'PRODUCT']:
                keywords.append(token.text)
                
        return list(set(keywords))

    def calculate_similarity(self, resume_text: str, job_description: str) -> Dict:
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_description)
        
        # Calculate TF-IDF similarity
        tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_description])
        cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        
        # Calculate keyword matches
        matches = []
        matched_keywords = set()
        
        for job_keyword in job_keywords:
            count = sum(1 for resume_keyword in resume_keywords 
                       if job_keyword in resume_keyword.lower())
            if count > 0:
                matches.append({"keyword": job_keyword, "count": count})
                matched_keywords.add(job_keyword)
        
        # Calculate match percentage
        match_percentage = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        
        # Combine TF-IDF similarity and keyword match percentage
        overall_match = (cosine_sim * 0.5 + (match_percentage / 100) * 0.5) * 100
        
        return {
            "matches": matches,
            "keywordMatch": round(overall_match, 2)
        }