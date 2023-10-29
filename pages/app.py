import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import preprocessor as prep

st.set_page_config(initial_sidebar_state="expanded")

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.sidebar.title("Welcome User to,")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = prep.preprocess(data)
    st.write(df)
    



