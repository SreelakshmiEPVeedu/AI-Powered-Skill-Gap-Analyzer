# auth.py
import streamlit as st
from backend.database import Database

#to check if the username and password exits in the database
def authenticate_user(username, password):   
    try:
        #returns a user - (userid,username,password), if not exists return None
        user = st.session_state.db.get_user(username) 
        if user and user[2] == password: #if username and password exists
            #save the data in session_state 
            st.session_state.user_id = user[0]   
            st.session_state.username = username
            print(f"🔐 User authenticated: {username}, ID: {user[0]}")
            return True
        print(f"❌ Authentication failed for: {username}")
        return False
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

#register for new user
def register_user(username, password):
    #funtion add_user() present in the database file
    return st.session_state.db.add_user(username, password) 