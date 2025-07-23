import streamlit as st
from utils.db import fetch_history, clear_history

st.set_page_config(page_title="Prediction History", layout="wide")

def main():
    st.title("📜 Prediction History")
    df = fetch_history()
    if df.empty:
        st.info("No predictions yet.")
        return
    st.dataframe(df)

    if st.button("Clear History"):
        clear_history()
        st.success("History cleared! Refresh to update.")

if __name__ == "__main__":
    main()
