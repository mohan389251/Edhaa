
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Insurer Risk Scoring Tool", layout="centered")

st.title("🏥 Life Insurance Risk Scoring - Edhaa MVP")

# Applicant input form
with st.form("risk_form"):
    st.subheader("Applicant Information")

    name = st.text_input("Applicant Name")
    age = st.number_input("Age", min_value=0, max_value=100)
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
    bmi = weight / ((height / 100) ** 2) if height else 0
    st.text(f"BMI: {bmi:.2f}")

    tobacco = st.selectbox("Tobacco Use", ["No", "Yes"])
    alcohol = st.selectbox("Alcohol Use", ["No/Occasional", "Frequent"])
    bp = st.selectbox("Blood Pressure Category", ["<130/85", "130-139/85-89", "≥140/90"])
    glucose = st.selectbox("Blood Glucose (mg/dL)", ["<140", "140–199", "≥200"])
    hb = st.selectbox("Hemoglobin", ["Normal", "Low"])
    creatinine = st.selectbox("Creatinine", ["<=1.2", ">1.2"])
    cholesterol = st.selectbox("Cholesterol", ["<200", "≥200"])

    submitted = st.form_submit_button("Calculate Risk")

if submitted:
    # Scoring logic
    score = 0
    if age > 50:
        score += 2
    elif age >= 35:
        score += 1
    if bmi >= 30:
        score += 2
    elif bmi >= 25:
        score += 1
    score += {"<130/85": 0, "130-139/85-89": 1, "≥140/90": 2}[bp]
    score += {"<140": 0, "140–199": 1, "≥200": 2}[glucose]
    score += {"Normal": 0, "Low": 1}[hb]
    score += {"<=1.2": 0, ">1.2": 2}[creatinine]
    score += {"<200": 0, "≥200": 2}[cholesterol]
    score += {"No": 0, "Yes": 2}[tobacco]
    score += {"No/Occasional": 0, "Frequent": 1}[alcohol]

    if score <= 3:
        risk_level = "Low Risk"
    elif score <= 6:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    # Display results
    st.success(f"✅ Total Risk Score: {score} — {risk_level}")
    st.write("### Summary")
    st.write({
        "Name": name,
        "Age": age,
        "BMI": f"{bmi:.2f}",
        "BP": bp,
        "Glucose": glucose,
        "Hemoglobin": hb,
        "Creatinine": creatinine,
        "Cholesterol": cholesterol,
        "Tobacco": tobacco,
        "Alcohol": alcohol,
        "Score": score,
        "Risk Level": risk_level,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Save record
    record = pd.DataFrame([{
        "Name": name,
        "Age": age,
        "BMI": f"{bmi:.2f}",
        "BP": bp,
        "Glucose": glucose,
        "Hemoglobin": hb,
        "Creatinine": creatinine,
        "Cholesterol": cholesterol,
        "Tobacco": tobacco,
        "Alcohol": alcohol,
        "Score": score,
        "Risk Level": risk_level,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    try:
        existing = pd.read_csv("saved_scores.csv")
        combined = pd.concat([existing, record], ignore_index=True)
    except:
        combined = record
    combined.to_csv("saved_scores.csv", index=False)
    st.success("✅ Record saved successfully.")
