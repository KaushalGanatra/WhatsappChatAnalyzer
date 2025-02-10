import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import mysql.connector

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)
st.sidebar.title("Welcome to Whatsapp Chat Analyzer")

with st.sidebar:
    st.write("if you are a new user, Register from here")
    register_button = st.button("Register")

    if register_button:
        switch_page("Register")

def is_user_logged_in(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatanalyzer"
    )
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT password from user where username=%s", (username,))
    res = mycursor.fetchone()
    mydb.close()
    
    if res and res[0] == password:
        return True
    else:
        return False

def main():
    st.title("Whatsapp Chat Analyzer Login")
    
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    login_button = st.button("Login")
    
    if login_button:
        if is_user_logged_in(username, password):
            st.success("Logged in successfully!")
            switch_page("app")
        else:
            st.error("Incorrect username or password.")

if __name__ == "__main__":
    main()
