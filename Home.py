# Home.py
import streamlit as st  #for frontend
from auth import authenticate_user, register_user  #for authentication
from helpers import initialize_session_state #to store data real time

#to configure the page appers on the tab
st.set_page_config(
    page_title="AI-Powered Skill Gap Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

#start of program
def main():
    initialize_session_state() 
    if not st.session_state.get("authenticated", False):  #if not logged in
        show_login_page()   #function to show login page
        return  
    show_main_app()   #function to show the main front page

def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])  #divides to 3 cloumns
    with col2:
        st.markdown('<h1 class="main-header">🔐 Resume Analyzer</h1>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:   #login form
            with st.form("login_form"):
                st.subheader("Login to Your Account")
                username = st.text_input("Username")   #takes usermane
                password = st.text_input("Password", type="password")  #takes password
                login_btn = st.form_submit_button("Login", use_container_width=True)
                if login_btn:
                    if authenticate_user(username, password):  #funtion to know if the user is present or not
                        #stores the data 
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        with tab2:  #for signup page
            with st.form("signup_form"):
                st.subheader("Create New Account")
                new_username = st.text_input("Choose Username", placeholder="Enter your username")
                new_password = st.text_input("Choose Password", type="password", placeholder="Enter your password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                signup_btn = st.form_submit_button("Create Account", use_container_width=True)
                if signup_btn:
                    #password checking conditions
                    if not new_username or not new_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_username) < 3:
                        st.error("Username must be at least 3 characters long")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        #to register as new user
                        success = register_user(new_username, new_password) 
                        if success:
                            st.success("Account created successfully! Please login with your new credentials.")
                        else:
                            st.error("User already exists!")

def show_main_app():
    with st.sidebar:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()  # This will trigger a rerun and show the login page
    
    st.markdown(
    '<h1 class="main-header" style="text-align: center;">AI-Powered Skill Gap Analyzer</h1>', 
    unsafe_allow_html=True
)
    st.markdown(f"""
    ## Welcome, {st.session_state.username}! 
    This application uses advanced Natural Language Processing (NLP) techniques to:\\
    📁 Upload your resume and job description files \\
    🔍 Analyze - Extract and compare skills using AI \\
    📊 Visualize - View skill gaps and compatibility scores \\
    📄 Export - Download detailed analysis reports \\
    """)
    st.markdown("---")
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📁 Upload Documents", use_container_width=True):
            st.switch_page("pages/1_Upload_Documents.py")
    with col2:
        if st.button("🔍 Skill Analysis", use_container_width=True):
            st.switch_page("pages/2_Skill_Analysis_and_Results.py")

if __name__ == "__main__":
    main()
