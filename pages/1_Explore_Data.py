import streamlit as st
import pandas as pd
import altair as alt
from utils.data import load_data, load_or_train

st.set_page_config(page_title="Explore Data", layout="wide")

def main():
    st.title("📊 Explore Dataset")
    df = load_data()
    pipe, _, metrics = load_or_train()

    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]} | **Model R²:** {metrics['r2']:.4f}")

    st.dataframe(df)

    # Salary distribution
    st.subheader("Salary Distribution")
    chart = alt.Chart(df).mark_bar().encode(
        alt.X("Salary:Q", bin=alt.Bin(maxbins=40)),
        y='count()',
        tooltip=['count()']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

    # Salary by Role
    st.subheader("Average Salary by Role")
    role_df = df.groupby("Role", as_index=False)["Salary"].mean().sort_values("Salary", ascending=False)
    chart2 = alt.Chart(role_df).mark_bar().encode(
        x=alt.X("Salary:Q"),
        y=alt.Y("Role:N", sort='-x'),
        tooltip=['Role', 'Salary']
    )
    st.altair_chart(chart2, use_container_width=True)

    # Salary by Location
    st.subheader("Average Salary by Location")
    loc_df = df.groupby("Location", as_index=False)["Salary"].mean().sort_values("Salary", ascending=False)
    chart3 = alt.Chart(loc_df).mark_bar().encode(
        x=alt.X("Salary:Q"),
        y=alt.Y("Location:N", sort='-x'),
        tooltip=['Location', 'Salary']
    )
    st.altair_chart(chart3, use_container_width=True)

if __name__ == "__main__":
    main()
