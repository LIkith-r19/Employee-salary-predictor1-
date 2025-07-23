
import streamlit as st

def local_css():
    st.markdown(
        '''
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton > button {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 10px;
            box-shadow: 0 0 10px #00e6e6;
            transition: 0.3s ease-in-out;
            font-size: 16px;
        }
        .stButton > button:hover {
            box-shadow: 0 0 20px #00e6e6;
            transform: scale(1.05);
        }
        </style>
        ''',
        unsafe_allow_html=True
    )
    