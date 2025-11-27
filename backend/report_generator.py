# backend/report_generator.py
import io
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportGenerator:
    
    def __init__(self):
        #creates a collection of predefined text styles
        self.styles = getSampleStyleSheet() 
    #function to calculate skill_gap
    def _calculate_skill_gap(self, skill_analysis: Dict[str, Any]) -> float:
        #formula to calculate skill_gap
        '''Scoring Logic:
        Missing skills: Full weight (1.0) - completely absent
        Partial matches: Half weight (0.5) - partially present
        Matched skills: Zero weight - fully present
        Scoring formula used:
        Total Required Skills = matched_skills + partial_matches + missing_skills
        Weighted Gap = (missing_skills × 1.0) + (partial_matches × 0.5)
        Skill Gap % = (Weighted Gap / Total Required Skills) × 100'''
        total_required = len(skill_analysis['matched_skills']) + len(skill_analysis['partial_matches']) + len(skill_analysis['missing_skills'])
        if total_required == 0:
            return 0
        
        missing_skills_weight = len(skill_analysis['missing_skills'])
        partial_matches_weight = len(skill_analysis['partial_matches']) * 0.5
        
        skill_gap = ((missing_skills_weight + partial_matches_weight) / total_required) * 100
        return skill_gap
    #function to generate pdf report
    def generate_pdf_report(self, analysis_results: Dict[str, Any]) -> bytes:
       
        buffer = io.BytesIO() #Creates an in-memory binary stream
        #SimpleDocTemplate: Main PDF container with A4 size and margins
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=40, bottomMargin=40)
        story = []  #List that accumulates all PDF elements in order
        #Extracts key metrics for the report display
        skill_analysis = analysis_results["skill_analysis"]
        compatibility_score = analysis_results['compatibility_score']
        skill_gap = self._calculate_skill_gap(skill_analysis)
        skill_coverage = 100 - skill_gap
        
        # Title
        title = Paragraph("Skill Gap Analysis Report", self.styles['Title'])
        story.append(title)
        story.append(Spacer(1, 10)) #Spacer: Adds vertical space (1 inch width, 10 points height)
        
        # Date
        #add timestamp for report validity tracking
        date_str = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['Normal'])
        story.append(date_str) 
        story.append(Spacer(1, 20))
        
        # Overall Assessment
        story.append(Paragraph("<b>Overall Assessment</b>", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Main metrics table
        metrics_data = [
            ['Overall Compatibility', f"{compatibility_score:.1f}%"],
            ['Skill Gap', f"{skill_gap:.1f}%"],
            ['Skill Coverage', f"{skill_coverage:.1f}%"]
        ]
        #tables setting
        metrics_table = Table(metrics_data, colWidths=[200, 100])
        metrics_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 10))
        
        # Assessment message
        if compatibility_score >= 80:
            assessment = "✅ Excellent Match! Your skills are very well aligned with the job requirements."
        elif compatibility_score >= 60:
            assessment = "👍 Good Match! Your skills match well with some areas for improvement."
        elif compatibility_score >= 40:
            assessment = "⚠️ Moderate Match. There are significant skill gaps to address."
        else:
            assessment = "❌ Poor Match. Consider developing more relevant skills."
        
        story.append(Paragraph(assessment, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
  
        story.append(Paragraph("<b>Skill Analysis Summary</b>", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        total_skills = skill_analysis['high_match_count'] + skill_analysis['partial_match_count'] + skill_analysis['missing_count']
        
        summary_data = [
            ['Total Skills Required', str(total_skills)],
            ['Skill Gap', f"{skill_gap:.1f}%"],
            ['Skill Coverage', f"{skill_coverage:.1f}%"],
            ['Match Rate', f"{skill_analysis['overall_match']:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 100])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        
        story.append(Paragraph("<b>Skill Breakdown</b>", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        breakdown_data = [
            ['Category', 'Count'],
            ['High Matches', str(skill_analysis['high_match_count'])],
            ['Partial Matches', str(skill_analysis['partial_match_count'])],
            ['Missing Skills', str(skill_analysis['missing_count'])]
        ]
        
        breakdown_table = Table(breakdown_data, colWidths=[150, 80])
        breakdown_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, 1), colors.lightgreen),
            ('BACKGROUND', (0, 2), (0, 2), colors.lightyellow),
            ('BACKGROUND', (0, 3), (0, 3), colors.pink),
        ]))
        
        story.append(breakdown_table)
        story.append(Spacer(1, 20))
        
      
        col1 = []
        col2 = []
        
        
        if skill_analysis['matched_skills']:
            col1.append(Paragraph("<b>✅ Your Strong Skills:</b>", self.styles['Normal']))
            for skill in skill_analysis['matched_skills'][:10]:
                col1.append(Paragraph(f"• {skill['job_skill']}", self.styles['Normal']))
            col1.append(Spacer(1, 10))
        
    
        if skill_analysis['missing_skills']:
            col2.append(Paragraph("<b>❌ Skills to Learn:</b>", self.styles['Normal']))
            for skill in skill_analysis['missing_skills'][:10]:
                col2.append(Paragraph(f"• {skill['skill']}", self.styles['Normal']))
            col2.append(Spacer(1, 10))
        
    
        if col1 or col2:
            from reportlab.platypus import KeepTogether
            skills_data = [[col1, col2]] if col1 and col2 else [[col1]] if col1 else [[col2]]
            skills_table = Table(skills_data, colWidths=[250, 250])
            skills_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(skills_table)
            story.append(Spacer(1, 15))
        

        story.append(Paragraph("<b>💡 Recommendations</b>", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        if skill_analysis['missing_skills']:
            recommendations = [
                "Focus on learning the missing skills listed above",
                "Take online courses or work on practical projects",
                "Build a portfolio to showcase your new skills",
                "Network with professionals who have these skills"
            ]
        else:
            recommendations = [
                "Highlight your strong skills in job applications",
                "Prepare specific examples for interview questions",
                "Continue learning to stay current in your field",
                "Consider mentoring others in your strong areas"
            ]
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
     
        story.append(Spacer(1, 20))
        footer = Paragraph("Generated by Skill Gap Analyzer", self.styles['Italic'])
        story.append(footer)
        #creates the page
        doc.build(story)  # Writes PDF data, position moves to end  
        buffer.seek(0)     # Reset position to start          
        return buffer.getvalue()    # Reads entire PDF content from beginning