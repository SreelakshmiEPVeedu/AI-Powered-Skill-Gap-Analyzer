# helpers.py
import streamlit as st
'''imports your custom class Database() used to store and manage user accounts or stored data'''
from backend.database import Database

def initialize_session_state():
    """Initialize session state variables"""
    # Initialize database first
    if 'db' not in st.session_state:
        st.session_state.db = Database() #for database connection
    
    # Initialize other session state variables
    if 'resume_data' not in st.session_state:  #Empty slot to store uploaded resume text later
        st.session_state.resume_data = None
    if 'job_desc_data' not in st.session_state: #holds jd from the user
        st.session_state.job_desc_data = None
        '''After NLP processing, results (scores, gaps, matching) will be saved here'''
    if 'analysis_results' not in st.session_state:   
        st.session_state.analysis_results = None
    if 'nlp_processor' not in st.session_state:
        st.session_state.nlp_processor = None
    if 'skill_analyzer' not in st.session_state: #Will store your skill-analysis logic class instance
        st.session_state.skill_analyzer = None
    if 'authenticated' not in st.session_state:     #for login purpose 
        st.session_state.authenticated = False
    if 'username' not in st.session_state:   #to check if username exists
        st.session_state.username = None
    if 'user_id' not in st.session_state:   #to check if password exists
        st.session_state.user_id = None

def get_match_class(similarity: float) -> str:
    """Get CSS class for skill match based on similarity score"""
    if similarity > 0.8:
        return "skill-match-high"
    elif similarity > 0.5:
        return "skill-match-medium"
    else:
        return "skill-match-low"