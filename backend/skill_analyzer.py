# backend/skill_analyzer.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SkillAnalyzer:
    
    def __init__(self, nlp_processor):
        self.nlp = nlp_processor
    
    def analyze_skill_gap(self, resume_text: str, job_desc_text: str):
        resume_skills = self.nlp.extract_skills(resume_text)
        job_desc_skills = self.nlp.extract_skills(job_desc_text)
        
        resume_sentiment = self.nlp.analyze_sentiment(resume_text)
        job_desc_sentiment = self.nlp.analyze_sentiment(job_desc_text)
        
        skill_analysis = self._match_skills(resume_skills, job_desc_skills)
        compatibility_score = self._calculate_compatibility(skill_analysis)
        
        return {
            "resume_skills": resume_skills,
            "job_desc_skills": job_desc_skills,
            "skill_analysis": skill_analysis,
            "compatibility_score": compatibility_score
        }
    
    def _match_skills(self, resume_skills, job_desc_skills):
        if not job_desc_skills:
            return {
                'matched_skills': [],
                'partial_matches': [],
                'missing_skills': [],
                'overall_match': 0,
                'high_match_count': 0,
                'partial_match_count': 0,
                'missing_count': 0
            }
        
        matched_skills = []
        partial_matches = []
        missing_skills = []
        
        # Get embeddings for all skills
        all_skills = list(set(resume_skills + job_desc_skills))
        embeddings = self.nlp.get_embeddings(all_skills)
        
        if embeddings is not None and len(all_skills) > 0:
            skill_to_idx = {skill: i for i, skill in enumerate(all_skills)}
            similarity_matrix = cosine_similarity(embeddings)
            
            for job_skill in job_desc_skills:
                job_idx = skill_to_idx.get(job_skill)
                if job_idx is None:
                    continue
                    
                best_match = None
                best_score = 0
                
                for resume_skill in resume_skills:
                    resume_idx = skill_to_idx.get(resume_skill)
                    if resume_idx is None:
                        continue
                    
                    score = similarity_matrix[job_idx][resume_idx]
                    if score > best_score:
                        best_score = score
                        best_match = resume_skill
                
                if best_score > 0.7:
                    matched_skills.append({
                        'job_skill': job_skill,
                        'resume_skill': best_match,
                        'similarity': best_score
                    })
                elif best_score > 0.3:
                    partial_matches.append({
                        'job_skill': job_skill,
                        'resume_skill': best_match,
                        'similarity': best_score
                    })
                else:
                    missing_skills.append({
                        'skill': job_skill,
                        'similarity': best_score
                    })
        else:
            # Fallback to string matching
            for job_skill in job_desc_skills:
                found = False
                for resume_skill in resume_skills:
                    if job_skill.lower() == resume_skill.lower():
                        matched_skills.append({
                            'job_skill': job_skill,
                            'resume_skill': resume_skill,
                            'similarity': 1.0
                        })
                        found = True
                        break
                    elif job_skill in resume_skill or resume_skill in job_skill:
                        partial_matches.append({
                            'job_skill': job_skill,
                            'resume_skill': resume_skill,
                            'similarity': 0.5
                        })
                        found = True
                        break
                
                if not found:
                    missing_skills.append({
                        'skill': job_skill,
                        'similarity': 0.0
                    })
        
        total_skills = len(job_desc_skills)
        if total_skills > 0:
            overall_match = (len(matched_skills) * 1.0 + len(partial_matches) * 0.5) / total_skills * 100
        else:
            overall_match = 0
        
        return {
            'matched_skills': matched_skills,
            'partial_matches': partial_matches,
            'missing_skills': missing_skills,
            'overall_match': overall_match,
            'high_match_count': len(matched_skills),
            'partial_match_count': len(partial_matches),
            'missing_count': len(missing_skills)
        }
    
    def _calculate_compatibility(self, skill_analysis):
        skill_score = skill_analysis['overall_match']
        # Simple compatibility based on skill match
        return min(100, max(0, skill_score))
