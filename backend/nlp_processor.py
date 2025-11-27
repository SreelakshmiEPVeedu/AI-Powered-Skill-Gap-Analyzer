# backend/nlp_processor.py
import spacy   # for nlp tasks
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  
from transformers import AutoTokenizer, AutoModel    # loads bert model
import numpy as np  # for numerical operations
from typing import List, Dict, Any

class NLPProcessor:
    #Handle all NLP processing tasks using spaCy and BERT
    
    def __init__(self):   # class constructor
        self.nlp = self._load_spacy_model()  # loads spacy model
        self.sentiment_analyzer = SentimentIntensityAnalyzer()  # Initializes VADER sentiment analyzer
        self.tokenizer, self.model = self._load_bert_model()  # Loads BERT tokenizer + model
        
        # Enhanced skill patterns for pattern matching 
        self.skill_patterns = [
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust",
            "sql", "r", "matlab", "scala", "perl", "html", "css", "sass", "less",
            
            # Frameworks & Libraries
            "react", "angular", "vue", "django", "flask", "spring", "laravel", "express", "node.js", "react native",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",
            
            # Tools & Platforms
            "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "git", "github", "gitlab", "jira", "confluence",
            "tableau", "power bi", "snowflake", "redshift", "mongodb", "mysql", "postgresql", "redis", "elasticsearch",
            
            # Methodologies
            "agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "bdd", "machine learning", "deep learning",
            "data analysis", "data visualization", "statistical analysis", "natural language processing",
            
            # Soft Skills
            "communication", "teamwork", "leadership", "problem solving", "critical thinking", "time management",
            "project management", "collaboration", "adaptability", "creativity", "analytical skills"
        ]
    
    def _load_spacy_model(self):
        #Load spaCy model
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded successfully")
            return nlp
        except OSError:
            raise Exception("Please install the spaCy English model: python -m spacy download en_core_web_sm")
    
    def _load_bert_model(self):
        """Load BERT model for embeddings
        This loads tokenizer → converts text → BERT tokens then model → generates embeddings"""
        try:
            tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            print("✅ BERT model loaded successfully")
            return tokenizer, model
        except Exception as e:
            print(f"⚠️ Could not load BERT model: {e}. Using fallback methods.")
            return None, None
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using multiple methods"""
        if not text:
            return []
            
        skills = set() 
        text_lower = text.lower() # converting to lowercase
        
        # Method 1: Pattern matching
        # checks if any known skill exists in the text
        for pattern in self.skill_patterns:
            if pattern in text_lower:
                skills.add(pattern)
        
        # Method 2: spaCy NER
        # identifies the named entities
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "TECHNOLOGY"]:
                skills.add(ent.text.lower())
        
        return list(skills)
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        #Analyze sentiment of text using VADER
        if not text:
            return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        return self.sentiment_analyzer.polarity_scores(text)
    
    def get_embeddings(self, texts: List[str]) -> Any:
        #Get BERT embeddings for texts without PyTorch dependency
        if self.tokenizer is None or self.model is None:
            return None

        try:
            # Tokenize texts with explicit settings
            inputs = self.tokenizer(
                texts, 
                padding=True, 
                truncation=True, 
                return_tensors="np",
                max_length=512,
                stride=128,  # Add stride for better handling of long texts
                return_overflowing_tokens=False,
                return_offsets_mapping=False
            )

            # Get embeddings with more explicit pooling
            outputs = self.model(**inputs)

            # Use more robust pooling - mean of last hidden state
            last_hidden_state = outputs.last_hidden_state
            attention_mask = inputs.get('attention_mask', None)

            if attention_mask is not None:
                # Use attention mask for better mean calculation
                input_mask_expanded = np.expand_dims(attention_mask, -1)
                sum_embeddings = np.sum(last_hidden_state * input_mask_expanded, axis=1)
                sum_mask = np.clip(input_mask_expanded.sum(axis=1), 1e-9, None)
                embeddings = sum_embeddings / sum_mask
            else:
                # Simple mean pooling
                embeddings = last_hidden_state.mean(axis=1)

            return embeddings

        except Exception as e:
            print(f"Error generating BERT embeddings: {e}")
            return None