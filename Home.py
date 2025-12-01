# pages/2_Skill_Analysis_and_Reports.py

import streamlit as st
import plotly.express as px
import pandas as pd
from backend.report_generator import ReportGenerator
from backend.calculations import Calculations
from helpers import initialize_session_state
from datetime import datetime

initialize_session_state()

def create_skill_match_chart(skill_analysis):
    high_match = skill_analysis['high_match_count']
    partial_match = skill_analysis['partial_match_count']
    missing = skill_analysis['missing_count']
    fig = px.pie(
        values=[high_match, partial_match, missing],
        names=['High Match', 'Partial Match', 'Missing Skills'],
        title='Skill Match Distribution',
        color_discrete_map={'High Match': '#28a745', 'Partial Match': '#ffc107', 'Missing Skills': '#dc3545'}
    )
    return fig

def display_skill_table(skills, skill_type):
    if not skills:
        st.info(f"No {skill_type.replace('_', ' ').lower()} found.")
        return
    data = []
    for skill in skills:
        if skill_type == "matched_skills":
            data.append({
                "Job Skill": skill['job_skill'],
                "Your Skill": skill['resume_skill'],
                "Match Score": f"{skill['similarity']:.2f}",
                
            })
        elif skill_type == "partial_matches":
            data.append({
                "Job Skill": skill['job_skill'],
                "Your Skill": skill['resume_skill'],
                "Match Score": f"{skill['similarity']:.2f}",
              
            })
        else:
            data.append({
                "Job Skill": skill['skill'],
                "Your Skill": "Not Found",
                "Match Score": f"{skill['similarity']:.2f}",
                
            })
    
    df = pd.DataFrame(data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Job Skill": st.column_config.TextColumn(width="large"),
            "Your Skill": st.column_config.TextColumn(width="large"),
            "Match Score": st.column_config.ProgressColumn(
                width="medium",
                min_value=0,
                max_value=1,
                format="%.2f"
            ),
            "Status": st.column_config.TextColumn(width="medium")
        }
    )

def display_skill_summary(skill_analysis):
    calculations = Calculations()
    
    st.subheader("📋 Skill Analysis Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_skills = (skill_analysis['high_match_count'] + 
                       skill_analysis['partial_match_count'] + 
                       skill_analysis['missing_count'])
        st.metric("Total Skills Required", total_skills)
    with col2:
        skill_gap = calculations.calculate_skill_gap(skill_analysis)
        st.metric("Skill Gap", f"{skill_gap:.1f}%")
    with col3:
        coverage = calculations.calculate_skill_coverage(skill_analysis)
        st.metric("Skill Coverage", f"{coverage:.1f}%")
    with col4:
        match_rate = skill_analysis['overall_match']
        st.metric("Match Rate", f"{match_rate:.1f}%")

def main():
    calculations = Calculations()
    with st.sidebar:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.rerun()
    st.markdown('<h2 class="sub-header">🔍 Skill Analysis & Report</h2>', unsafe_allow_html=True)
    if not st.session_state.resume_data or not st.session_state.job_desc_data:
        st.warning("⚠️ Please upload both resume and job description first.")
        return
    if st.session_state.nlp_processor is None:
        try:
            from backend.nlp_processor import NLPProcessor
            from backend.skill_analyzer import SkillAnalyzer
            st.session_state.nlp_processor = NLPProcessor()
            st.session_state.skill_analyzer = SkillAnalyzer(st.session_state.nlp_processor)
        except Exception as e:
            st.error(f"Error initializing NLP components: {e}")
            return
    if st.button("🔍 Run Skill Gap Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing documents..."):
            try:
                st.session_state.analysis_results = st.session_state.skill_analyzer.analyze_skill_gap(
                    st.session_state.resume_data['text'],
                    st.session_state.job_desc_data['text']
                )
                st.success("✅ Analysis completed successfully!")
                    
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                return
    if not st.session_state.analysis_results:
        st.info("👆 Click the button above to run the skill gap analysis")
        return
    
    analysis = st.session_state.analysis_results
    skill_analysis = analysis["skill_analysis"]
    skill_gap = calculations.calculate_skill_gap(skill_analysis)
    skill_coverage = calculations.calculate_skill_coverage(skill_analysis)
    st.subheader("🎯 Overall Assessment")
    
    compatibility_score = analysis['compatibility_score']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Compatibility", f"{compatibility_score:.1f}%")
    
    with col2:
        st.metric("Skill Gap", f"{skill_gap:.1f}%")
    
    with col3:
        st.metric("Skill Coverage", f"{skill_coverage:.1f}%")
 
    assessment_message = calculations.get_assessment_message(compatibility_score)
    if compatibility_score >= 80:
        st.success(assessment_message)
    elif compatibility_score >= 60:
        st.info(assessment_message)
    elif compatibility_score >= 40:
        st.warning(assessment_message)
    else:
        st.error(assessment_message)
  
    display_skill_summary(skill_analysis)
    
    st.subheader("📈 Visual Analysis")
    
    fig = create_skill_match_chart(skill_analysis)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔎 Detailed Skill Analysis")
    
    with st.expander(f"✅ High Matches ({skill_analysis['high_match_count']} skills)", expanded=True):
        st.write("**Skills where you have strong matching experience:**")
        display_skill_table(skill_analysis['matched_skills'], "matched_skills")
    
    with st.expander(f"⚠️ Partial Matches ({skill_analysis['partial_match_count']} skills)"):
        st.write("**Skills where you have some experience but could improve:**")
        display_skill_table(skill_analysis['partial_matches'], "partial_matches")
    
    with st.expander(f"❌ Missing Skills ({skill_analysis['missing_count']} skills)"):
        st.write("**Skills required for the job that are missing from your resume:**")
        display_skill_table(skill_analysis['missing_skills'], "missing_skills")
    
    st.subheader("📄 Download Report")
    st.info("📝 Download the pdf for future reference as the data will be lost when you refresh or logout")
    if st.session_state.analysis_results:
        if st.button("Generate PDF Report", type="primary"):
            with st.spinner("Creating report..."):
                try:
                    report_generator = ReportGenerator()
                    pdf_data = report_generator.generate_pdf_report(st.session_state.analysis_results)
                    
                    st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=f"skill_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                    
                    st.success("PDF ready for download!")
                    
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
