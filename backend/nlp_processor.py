# backend/nlp_processor.py

import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
import re

class NLPProcessor:
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Skill keywords
        self.skill_keywords = {
            "python", "java", "javascript", "sql", "react", "node.js", "aws", "docker", 
            "kubernetes", "machine learning", "ml", "ai", "data analysis", "html", "css",
            "git", "github", "agile", "scrum", "communication", "teamwork", "leadership"
        }
    
    def extract_skills(self, text: str):
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = set()
        
        # Direct keyword matching
        for skill in self.skill_keywords:
            if skill in text_lower:
                found_skills.add(skill)
        
        # Look for skills in context
        doc = self.nlp(text_lower)
        for token in doc:
            if token.text in self.skill_keywords:
                found_skills.add(token.text)
        
        return list(found_skills)
    
    def analyze_sentiment(self, text: str):
        return self.sentiment_analyzer.polarity_scores(text)
    
    def get_embeddings(self, texts):
        if not texts:
            return None
        return self.embedding_model.encode(texts, convert_to_numpy=True)
