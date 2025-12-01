# backend/calculations.py

class Calculations:
    
    @staticmethod
    def calculate_skill_gap(skill_analysis):
        total_required = skill_analysis['high_match_count'] + \
                        skill_analysis['partial_match_count'] + \
                        skill_analysis['missing_count']
        
        if total_required == 0:
            return 0
        
        gap = (skill_analysis['missing_count'] + 
               skill_analysis['partial_match_count'] * 0.5) / total_required * 100
        return gap
    
    @staticmethod
    def calculate_compatibility_score(skill_analysis, resume_sentiment, job_desc_sentiment):
        # Simplified - just use skill match
        return skill_analysis['overall_match']
    
    @staticmethod
    def calculate_skill_coverage(skill_analysis):
        return 100 - Calculations.calculate_skill_gap(skill_analysis)
    
    @staticmethod
    def get_assessment_message(compatibility_score: float):
        if compatibility_score >= 80:
            return "🎉 **Excellent Match!** Your skills strongly align with the job requirements."
        elif compatibility_score >= 60:
            return "👍 **Good Match!** You have most required skills with minor gaps."
        elif compatibility_score >= 40:
            return "⚠️ **Moderate Match.** You have some key skills but significant gaps to address."
        else:
            return "❌ **Poor Match.** Consider developing more relevant skills for this role."
