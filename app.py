import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from utils.ui import local_css

from utils.data import load_data, load_or_train
from utils.db import init_db, insert_record
from utils.pdf_utils import generate_salary_pdf

# Ensure DB exists
init_db()

st.set_page_config(page_title="Smart Salary AI", layout="wide")
local_css()


st.title("💼 Smart Salary AI - Employee Salary Prediction")

# Load data / model
pipe, preprocessor, metrics = load_or_train()
df = load_data()
r2 = metrics['r2']

st.sidebar.header("Enter Employee Details")

# Use original categorical values from df for better UX
education = st.sidebar.selectbox("Education", sorted(df["Education"].unique()))
experience = st.sidebar.slider("Experience (years)", int(df["Experience"].min()), int(df["Experience"].max()), int(df["Experience"].median()))
role = st.sidebar.selectbox("Role", sorted(df["Role"].unique()))
department = st.sidebar.selectbox("Department", sorted(df["Department"].unique()))
location = st.sidebar.selectbox("Location", sorted(df["Location"].unique()))

user_input = {
    "Education": education,
    "Experience": experience,
    "Role": role,
    "Department": department,
    "Location": location,
}

input_df = pd.DataFrame([user_input])

predict_col, pdf_col = st.columns([2,1])

with predict_col:
    predict_btn = st.container()
    with predict_btn:
        glow = st.empty()
        # Add class so CSS glow applies
        with st.container():
            pred_clicked = st.button("Predict Salary", key="predict_salary", type="primary", help="Click to predict salary", use_container_width=True)

if pred_clicked:
    predicted_salary = pipe.predict(input_df)[0]
    st.markdown(f"<h2>🤑 Predicted Salary: ₹{int(predicted_salary):,}</h2>", unsafe_allow_html=True)
    st.success(f"Model R² Score: {r2:.4f}")
    insert_record(education, experience, role, department, location, predicted_salary, r2)

    # Comparison text
    role_avg = df[df["Role"]==role]["Salary"].mean()
    loc_avg = df[df["Location"]==location]["Salary"].mean()
    delta_role = predicted_salary - role_avg
    delta_loc = predicted_salary - loc_avg
    cmp_lines = [
        f"Avg salary for {role}: ₹{int(role_avg):,}",
        f"Avg salary for {location}: ₹{int(loc_avg):,}",
        f"Difference vs role avg: ₹{int(delta_role):,}",
        f"Difference vs location avg: ₹{int(delta_loc):,}",
    ]
    cmp_text = "\n".join(cmp_lines)

    # Simple suggestions
    sugg_lines = []
    if predicted_salary < 0.8 * role_avg:
        sugg_lines.append("Your predicted salary is below the typical range for this role. Consider negotiation or upskilling.")
    if experience < 3:
        sugg_lines.append("Early career: focus on foundational skills & certifications.")
    elif experience < 7:
        sugg_lines.append("Mid-level: specialize in in-demand tech (ML, Cloud, Data Eng).")
    else:
        sugg_lines.append("Senior: highlight leadership & cross-functional impact to increase pay.")
    if not sugg_lines:
        sugg_lines.append("You are well-positioned—track market salaries and negotiate at review time.")
    suggestions_text = "\n".join(sugg_lines)

    # Offer PDF
    with pdf_col:
        if st.button("Download PDF Report", key="pdf_btn"):
            out_path = Path("salary_report.pdf")
            generate_salary_pdf(out_path, user_input, predicted_salary, r2, cmp_text, suggestions_text)
            with open(out_path, "rb") as f:
                st.download_button(
                    label="⬇️ Save Salary Report PDF",
                    data=f,
                    file_name="salary_report.pdf",
                    mime="application/pdf",
                )

# Quick dashboard below
st.markdown("---")
st.subheader("📊 Quick Insights")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Dataset Rows", value=len(df))
with col2:
    st.metric("Unique Roles", value=df["Role"].nunique())
with col3:
    st.metric("Model R²", value=f"{r2:.4f}")

# Salary Distribution
st.markdown("### Salary Distribution")
st.bar_chart(df["Salary"])

# Pie chart by Role (counts)
st.markdown("### Role Distribution")
role_counts = df["Role"].value_counts()
st.pyplot(role_counts.plot.pie(autopct='%1.1f%%').figure)
