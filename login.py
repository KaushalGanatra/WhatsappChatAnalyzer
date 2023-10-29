import streamlit as st
from streamlit_extras.switch_page_button import switch_page

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

# Function to check if the user is logged in
def is_user_logged_in(username, password):
    # Add your authentication logic here
    # For simplicity, let's assume the username is "user" and the password is "password"
    return username == "user" and password == "password"

# Main Streamlit app
def main():
    st.title("Whatsapp Chat Analyzer Login")
    
    # Add login form to the main page
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    login_button = st.button("Login")
    
    if login_button:
        st.write(username,password)
        if is_user_logged_in(username, password):
            st.success("Logged in successfully!")
            
            switch_page("app")
        else:
            st.error("Incorrect username or password.")





if __name__ == "__main__":
    main()
