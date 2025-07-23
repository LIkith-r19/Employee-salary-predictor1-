import streamlit as st
import pandas as pd
from utils.data import load_data

st.set_page_config(page_title="Career Suggestions", layout="wide")

def career_rules(education, experience, role, avg_role_salary, user_salary=None):
    suggestions = []
    if user_salary is not None and user_salary < 0.8 * avg_role_salary:
        suggestions.append("Your predicted salary is below the typical range for this role. Consider upskilling or negotiation.")
    if experience < 3:
        suggestions.append("Early career: build foundational skills, take certifications, and contribute to open-source.")
    elif experience < 7:
        suggestions.append("Mid-level: target specialization (e.g., ML, cloud), pursue advanced courses, mentor juniors.")
    else:
        suggestions.append("Senior: focus on leadership, architecture, and cross-functional impact to command higher pay.")
    if education.lower() in ["high school", "diploma"]:
        suggestions.append("Higher degree or professional certification could significantly increase earning potential.")
    if not suggestions:
        suggestions.append("You are well-positioned. Keep tracking market salaries and negotiate during reviews.")
    return suggestions

def main():
    st.title("🚀 Career Suggestions")
    df = load_data()

    edu = st.selectbox("Education", sorted(df["Education"].unique()))
    role = st.selectbox("Role", sorted(df["Role"].unique()))
    dept = st.selectbox("Department", sorted(df["Department"].unique()))
    loc = st.selectbox("Location", sorted(df["Location"].unique()))
    exp = st.slider("Experience (years)", 0, 40, 2)

    avg_role_salary = df[df["Role"]==role]["Salary"].mean()
    user_salary = st.number_input("Optional: Enter your current or predicted salary (₹)", min_value=0, value=0)

    if st.button("Get Suggestions"):
        sugg = career_rules(edu, exp, role, avg_role_salary, user_salary if user_salary>0 else None)
        st.subheader("Recommendations")
        for s in sugg:
            st.markdown(f"- {s}")
        st.info(f"Average salary for {role}: ₹{int(avg_role_salary):,}")

if __name__ == "__main__":
    main()
