import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import mysql.connector

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)
st.sidebar.title("Welcome to Whatsapp Chat Analyzer, Register from Here")

def add_details(username,useremail,password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatanalyzer"
    )
    mycursor = mydb.cursor()

    sql = "INSERT into userdata (username,useremail,password) VALUES (%s,%s,%s)"
    val=(username,useremail,password)
    mycursor.execute(sql,val)
    mydb.commit()

    

def main():
    st.title("Registration")

    username = st.text_input("Username:")
    useremail = st.text_input("Email:")
    password = st.text_input("Password:", type="password")
    register_button = st.button("Resgister")
    
    if register_button:
        add_details(username,useremail,password)
        st.success("Logged in successfully!")
        switch_page("login")





if __name__ == "__main__":
    main()


