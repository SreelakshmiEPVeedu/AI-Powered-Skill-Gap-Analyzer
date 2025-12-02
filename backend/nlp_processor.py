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
    # Programming Languages
    "python", "python3", "django", "flask", "numpy", "pandas", "tensorflow", "pytorch",
    "java", "spring", "spring boot", "hibernate", "j2ee", "jsp", "servlet",
    "javascript", "typescript", "es6", "react", "angular", "vue", "vue.js", "node.js", 
    "express.js", "next.js", "redux", "jquery", "ajax",
    "c++", "c#", ".net", "asp.net", "core", "mvc",
    "php", "laravel", "symfony", "codeigniter", "wordpress",
    "ruby", "rails", "ruby on rails", "sinatra",
    "go", "golang", "rust", "swift", "kotlin", "dart", "flutter",
    
    # Databases
    "sql", "mysql", "postgresql", "postgres", "oracle", "sql server", "mongodb",
    "nosql", "redis", "cassandra", "dynamodb", "elasticsearch", "firebase",
    "pl/sql", "t-sql", "database design", "data modeling",
    
    # Cloud & DevOps
    "aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudformation",
    "azure", "microsoft azure", "google cloud", "gcp", "cloud computing",
    "docker", "kubernetes", "k8s", "jenkins", "ansible", "terraform", "ci/cd",
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    
    # Web Technologies
    "html", "html5", "css", "css3", "sass", "scss", "less", "bootstrap",
    "tailwind", "responsive design", "webpack", "babel", "npm", "yarn",
    
    # Data Science & AI
    "machine learning", "ml", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "openai", "chatgpt",
    "data science", "data analysis", "data analytics", "big data", "hadoop",
    "spark", "tableau", "power bi", "excel", "statistics", "matplotlib",
    "seaborn", "scikit-learn", "keras", "artificial intelligence", "ai",
    
    # Testing
    "testing", "unit testing", "integration testing", "selenium", "jest",
    "mocha", "chai", "cypress", "testng", "junit", "pytest",
    
    # Methodologies & Practices
    "agile", "scrum", "kanban", "waterfall", "devops", "lean",
    "tdd", "test driven development", "bdd", "behavior driven development",
    "microservices", "rest", "restful", "api", "graphql", "soap",
    "oauth", "jwt", "authentication", "authorization",
    
    # Mobile Development
    "android", "ios", "react native", "xamarin", "ionic", "mobile development",
    
    # Operating Systems
    "linux", "unix", "windows", "macos", "shell scripting", "bash", "powershell",
    
    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving", "critical thinking",
    "time management", "project management", "team management", "mentoring",
    "presentation", "public speaking", "negotiation", "conflict resolution",
    "adaptability", "creativity", "analytical skills", "attention to detail",
    
    # Business & Tools
    "photoshop", "illustrator", "figma", "sketch", "adobe xd",
    "word", "excel", "powerpoint", "outlook", "sharepoint",
    "salesforce", "sap", "oracle ebs", "erp", "crm",
    
    # Specialized Domains
    "blockchain", "ethereum", "solidity", "smart contracts",
    "iot", "internet of things", "cybersecurity", "ethical hacking",
    "game development", "unity", "unreal engine", "ar/vr",
    "embedded systems", "arduino", "raspberry pi",
    
    # Finance & Accounting
    "accounting", "finance", "quickbooks", "xero", "taxation",
    
    # Marketing
    "digital marketing", "seo", "search engine optimization", "sem",
    "social media marketing", "content marketing", "email marketing",
    "google analytics", "adwords", "facebook ads",
    
    # Languages
    "english", "spanish", "french", "german", "chinese", "japanese",
    "hindi", "multilingual"
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

