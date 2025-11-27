#backend/skill_analyzer.py
import numpy as np #packeage for numerical operations
#compute pairwise cosine similarity between vectors (embeddings)
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
from .nlp_processor import NLPProcessor

class SkillAnalyzer:
   
    
    def __init__(self, nlp_processor: NLPProcessor): #constructor 
        '''stores the passed nlp_processor instance on the object so other methods can call 
        NLP functions (like extract_skills, get_embeddings, analyze_sentiment)'''
        self.nlp = nlp_processor
    #function to analyze how well  a condidate matches a job description
    def analyze_skill_gap(self, resume_text: str, job_desc_text: str) -> Dict[str, Any]:
       
        
        resume_skills = self.nlp.extract_skills(resume_text)
        job_desc_skills = self.nlp.extract_skills(job_desc_text)
  
        resume_sentiment = self.nlp.analyze_sentiment(resume_text)
        job_desc_sentiment = self.nlp.analyze_sentiment(job_desc_text)
    
        skill_analysis = self._match_skills(resume_skills, job_desc_skills)
        
        
        compatibility_score = self._calculate_compatibility_score(skill_analysis, resume_sentiment, job_desc_sentiment)
        
        return {
            "resume_skills": resume_skills,
            "job_desc_skills": job_desc_skills,
            "resume_sentiment": resume_sentiment,
            "job_desc_sentiment": job_desc_sentiment,
            "skill_analysis": skill_analysis,
            "compatibility_score": compatibility_score
        }
    
    def _match_skills(self, resume_skills: List[str], job_desc_skills: List[str]) -> Dict[str, Any]:
        """Match skills between resume and job description"""
        if not resume_skills or not job_desc_skills:
            return {
                'matched_skills': [],
                'partial_matches': [],
                'missing_skills': job_desc_skills if job_desc_skills else [],
                'overall_match': 0,
                'similarity_matrix': np.array([]),
                'high_match_count': 0,
                'partial_match_count': 0,
                'missing_count': len(job_desc_skills) if job_desc_skills else 0
            }
        
        #Combines both lists and removes duplicates by converting to a set, then back to list
        all_skills = list(set(resume_skills + job_desc_skills))
        '''Requests vector embeddings for each skill phrase from the NLP processor. Expected: 
        a 2D array-like of shape (len(all_skills), embedding_dim) or None if embeddings not 
        available'''
        embeddings = self.nlp.get_embeddings(all_skills)
        '''Creates a mapping from skill string to its index in all_skills so we can find 
        rows/cols in the similarity matrix'''
        skill_to_idx = {skill: i for i, skill in enumerate(all_skills)}
        
    
        if embeddings is not None:
            similarity_matrix = cosine_similarity(embeddings)
        else:
            '''If embeddings is None (embedding provider not available):
            Build a fallback similarity_matrix initialized to zeros (size N x N where N = 
            number of unique skills).
            Nested loops compare every pair of skill strings:
                If strings are identical (skill1 == skill2): set similarity = 1.0.
                If one skill string is substring of the other (skill1 in skill2 or skill2 in 
                skill1): set similarity = 0.7 (heuristic for partial match).
            This fallback gives a rough similarity when embeddings are absent'''
       
            similarity_matrix = np.zeros((len(all_skills), len(all_skills)))
            for i, skill1 in enumerate(all_skills):
                for j, skill2 in enumerate(all_skills):
                    if skill1 == skill2:
                        similarity_matrix[i][j] = 1.0
                    elif skill1 in skill2 or skill2 in skill1:
                        similarity_matrix[i][j] = 0.7

        '''Initializes three lists to collect match results.
        The outer loop iterates over each job_skill (we check how well the resume covers job 
        requirements).
        job_idx = skill_to_idx[job_skill] finds the index in all_skills.
        For each job_skill, it attempts to find the best matching resume_skill by checking 
        all resume skills:
            resume_idx = skill_to_idx[resume_skill] gives the resume skill index.
            similarity = similarity_matrix[job_idx][resume_idx] reads similarity value 
            from matrix.
            Track the best_match_score and best_match_skill.
        After checking all resume skills for that job skill:
            If best_match_score > 0.8: treat it as a high match — append to matched_skills 
            with job/resume skill pairing and similarity number.
            Elif best_match_score > 0.5: treat it as a partial match — append to partial_matches.
            Else: treat it as missing — append to missing_skills with similarity (likely low or 0).
        Thresholds 0.8 and 0.5 are heuristics: they separate high vs partial vs missing matches. 
        You can tune them as needed.'''
        matched_skills = []
        missing_skills = []
        partial_matches = []
        
        for job_skill in job_desc_skills:
            job_idx = skill_to_idx[job_skill]
            best_match_score = 0
            best_match_skill = None
            
            for resume_skill in resume_skills:
                resume_idx = skill_to_idx[resume_skill]
                similarity = similarity_matrix[job_idx][resume_idx]
                
                if similarity > best_match_score:
                    best_match_score = similarity
                    best_match_skill = resume_skill
            
            if best_match_score > 0.8:  
                matched_skills.append({
                    'job_skill': job_skill,
                    'resume_skill': best_match_skill,
                    'similarity': best_match_score,
                    'match_level': 'high'
                })
            elif best_match_score > 0.5:  
                partial_matches.append({
                    'job_skill': job_skill,
                    'resume_skill': best_match_skill,
                    'similarity': best_match_score,
                    'match_level': 'partial'
                })
            else: 
                missing_skills.append({
                    'skill': job_skill,
                    'similarity': best_match_score,
                    'match_level': 'missing'
                })
        '''total_job_skills — number of skills listed in the job description.
        high_match_count and partial_match_count — counts of matched/partial items derived above.
        overall_match — combines counts into a single percentage:
            A high match counts as 1.0.
            A partial match counts as 0.5 (half weight).
            Sum weighted matches, divide by total job skills, multiply by 100 to get percent.
            If total_job_skills is 0, returns 0 to avoid division by zero.'''
 
        total_job_skills = len(job_desc_skills)
        high_match_count = len(matched_skills)
        partial_match_count = len(partial_matches)
        
        overall_match = ((high_match_count + (partial_match_count * 0.5)) / total_job_skills) * 100 if total_job_skills > 0 else 0
        
        return {
            'matched_skills': matched_skills,
            'partial_matches': partial_matches,
            'missing_skills': missing_skills,
            'overall_match': overall_match,
            'similarity_matrix': similarity_matrix,
            'high_match_count': high_match_count,
            'partial_match_count': partial_match_count,
            'missing_count': len(missing_skills)
        }
    #funtion to calculate the compatibility score
    def _calculate_compatibility_score(self, skill_analysis: Dict[str, Any], 
                                     resume_sentiment: Dict[str, float], 
                                     job_desc_sentiment: Dict[str, float]) -> float:
     
        skill_weight = 0.7
        sentiment_weight = 0.3
        #Uses the percent overall match (0–100) computed earlier as the skill component
        skill_score = skill_analysis['overall_match']
        #Computes absolute difference between the compound sentiment scores for resume and 
        # job description
        sentiment_diff = abs(resume_sentiment['compound'] - job_desc_sentiment['compound'])
        sentiment_score = max(0, 100 - (sentiment_diff * 100))
        #compatibility score calculation
        compatibility_score = (skill_score * skill_weight) + (sentiment_score * sentiment_weight)
        
        return min(100, compatibility_score)