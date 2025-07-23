import streamlit as st
import pandas as pd
import altair as alt
from utils.data import load_data

st.set_page_config(page_title="Role Comparison", layout="wide")

def main():
    st.title("⚖️ Compare Roles")
    df = load_data()

    roles = sorted(df["Role"].unique())
    role_sel = st.multiselect("Select roles to compare", roles, default=roles[:3])

    if not role_sel:
        st.warning("Pick at least one role.")
        return

    cmp_df = df[df["Role"].isin(role_sel)].groupby(["Role"], as_index=False).agg(
        avg_salary=("Salary", "mean"),
        min_salary=("Salary", "min"),
        max_salary=("Salary", "max"),
        count=("Salary", "count"),
    )
    st.dataframe(cmp_df)

    chart = alt.Chart(cmp_df).mark_bar().encode(
        x=alt.X("avg_salary:Q", title="Average Salary"),
        y=alt.Y("Role:N", sort='-x'),
        tooltip=['Role', 'avg_salary', 'min_salary', 'max_salary', 'count']
    )
    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
