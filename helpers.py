# helpers.py

import streamlit as st
from backend.database import Database

def initialize_session_state():
    """Initialize session state variables"""
    if 'db' not in st.session_state:
        st.session_state.db = Database()  #for database
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None   #reseume data
    if 'job_desc_data' not in st.session_state:
        st.session_state.job_desc_data = None  #for job_description
    if 'analysis_results' not in st.session_state: 
        st.session_state.analysis_results = None   #for analysis_results
    if 'nlp_processor' not in st.session_state:   
        st.session_state.nlp_processor = None    #for nlp_processor
    if 'skill_analyzer' not in st.session_state:
        st.session_state.skill_analyzer = None    #for skill_analyzer
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False     #for authentication
    if 'username' not in st.session_state:
        st.session_state.username = None      #for username
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None         #for user_id
