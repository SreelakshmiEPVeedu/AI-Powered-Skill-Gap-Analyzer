# app.py
#import necessary files
import streamlit as st  #frontend for the website
#authenticate_user() - to check login credentials
#register_user() - create new user account'''
from auth import authenticate_user, register_user
#'''a place to persist values while the user interacts with the app'''   
from helpers import initialize_session_state  

#'''st.set_page_config(...) — configures the browser tab and overall page layout:
#page_title — text shown in the browser tab.
#page_icon — emoji or icon shown in the tab.
#layout="wide" — allows the page to use more horizontal space (two-column layout friendly).
#initial_sidebar_state="expanded" — makes the sidebar open by default.'''
st.set_page_config(
    page_title="AI-Powered Skill Gap Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()  #loads css
    initialize_session_state()   #here st.session_state keys are intialized
    
    if not st.session_state.get("authenticated", False):  #checkes if the user is logged in 
        show_login_page()   #function to show the login page if not logged in - implemented below
        return
    show_main_app()  #funtion used to show the main dashboard - implemented below

def show_login_page():
    '''creates 3 column layout middle one is 2 times the width of the other 2 columns'''
    col1, col2, col3 = st.columns([1, 2, 1])
    #login form is made
    with col2:
        st.markdown('<h1 class="main-header">🔐 Resume Analyzer</h1>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            with st.form("login_form"):
                st.subheader("Login to Your Account")
                username = st.text_input("Username") #collects username
                password = st.text_input("Password", type="password") #collects password
                login_btn = st.form_submit_button("Login", use_container_width=True)
                if login_btn:    #authenticates the login details
                    if authenticate_user(username, password):   #funtion which was imported
                        st.session_state.authenticated = True
                        st.session_state.username = username 
                        st.success("Login successful!")
                        st.rerun() #to re run the app
                    else:
                        st.error("Invalid username or password")
        with tab2:
            with st.form("signup_form"):
                st.subheader("Create New Account")
                new_username = st.text_input("Choose Username", placeholder="Enter your username")
                new_password = st.text_input("Choose Password", type="password", placeholder="Enter your password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                signup_btn = st.form_submit_button("Create Account", use_container_width=True)
                if signup_btn:
                    if not new_username or not new_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_username) < 3:
                        st.error("Username must be at least 3 characters long")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        '''creates new user using the register_user() function'''
                        success, message = register_user(new_username, new_password) 
                        if success:
                            st.success("Account created successfully! Please login with your new credentials.")
                        else:
                            st.error(message)

def show_main_app():   #to show the main app
    with st.sidebar:
        #logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.rerun()
    #content displayed on home screen
    st.markdown('<h1 class="main-header">AI-Powered Skill Gap Analyzer</h1>', unsafe_allow_html=True)
    st.markdown(f"""
    ## Welcome, {st.session_state.username}! 
    This application uses advanced Natural Language Processing (NLP) techniques to:\\
    📁 Upload your resume and job description files \\
    🔍 Analyze - Extract and compare skills using AI\\
    📊 Visualize - View skill gaps and compatibility scores\\
    📄 Export - Download detailed analysis reports
    """)
    st.markdown("---")
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📁 Upload Documents", use_container_width=True, help="Upload your resume and job description"):
            st.switch_page("pages/1_Upload_Documents.py")
    with col2:
        if st.button("🔍 Skill Analysis", use_container_width=True, help="Analyze skill gaps and get recommendations"):
            st.switch_page("pages/2_Skill_Analysis_and_Results.py")

if __name__ == "__main__":
    main()