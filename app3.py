import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import random
from fpdf import FPDF

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Smart Livestock AI",
    layout="wide",
    page_icon="🐄"
)

# ---------------- PROFESSIONAL STYLE ----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f0fff4, #ecfdf5); }
.hero-section { 
    background: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)),
    url('https://images.unsplash.com/photo-1500595046743-cd271d694d30?q=80&w=2070&auto=format&fit=crop');
    background-size: cover; background-position: center; padding: 100px 60px; border-radius: 25px;
    margin-bottom: 40px; border: 1px solid rgba(255,255,255,0.4); backdrop-filter: blur(12px);
}
.main-title { font-size:52px; font-weight:700; color:#064e3b; line-height:1.1; }
.sub-title { font-size:18px; color:#065f46; }
.feature-box { background: rgba(255,255,255,0.65); backdrop-filter: blur(12px); padding:40px; border-radius:20px; border:1px solid rgba(255,255,255,0.4); box-shadow:0 8px 20px rgba(0,0,0,0.05); }
.feature-label { color:#16a34a; font-weight:700; font-size:12px; letter-spacing:1px; }
.stButton>button { background: rgba(34,197,94,0.85) !important; color:white !important; border-radius:12px; border:1px solid rgba(255,255,255,0.4); backdrop-filter:blur(10px); padding:12px 24px; font-weight:600; transition: all 0.3s ease; }
.stButton>button:hover { background: rgba(22,163,74,0.95) !important; transform:translateY(-3px); box-shadow:0 8px 20px rgba(34,197,94,0.3); }
section[data-testid="stSidebar"] { background: rgba(255,255,255,0.7); backdrop-filter: blur(16px); border-right: 1px solid rgba(255,255,255,0.4); }
div[role="radiogroup"] > label { background: rgba(34,197,94,0.12); padding:12px; border-radius:12px; margin-bottom:8px; transition: all 0.2s ease; }
div[role="radiogroup"] > label:hover { background: rgba(34,197,94,0.25); }
div[role="radiogroup"] input:checked + div { color:#065f46 !important; font-weight:700; }
[data-testid="metric-container"] { background: rgba(255,255,255,0.65); border-radius:15px; padding:15px; backdrop-filter: blur(10px); border:1px solid rgba(255,255,255,0.4); }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state: st.session_state.page = "home"
if "role" not in st.session_state: st.session_state.role = None
if "otp" not in st.session_state: st.session_state.otp = None

role = st.session_state.get("role", None)
page = st.session_state.get("nav", "Prediction")  

# ---------------- LOAD MODEL ----------------
model = joblib.load("best_livestock_model0.pkl")
label_encoder = joblib.load("label_encoder0.pkl")
encoders = joblib.load("feature_encoders.pkl")

# ---------------- LOAD DATASET ----------------
DATA = "animal_disease.csv"
data = pd.read_csv(DATA) if os.path.exists(DATA) else None

# ---------------- COMMON DATA ----------------
symptoms = [
    "loss of appetite","depression","painless lumps",
    "swelling in limb","crackling sound",
    "fever","nasal discharge","difficulty breathing"
]

medicine = {
    "anthrax":"Penicillin or Oxytetracycline",
    "blackleg":"Penicillin + Anti-inflammatory",
    "pneumonia":"Amoxicillin",
    "lumpy virus":"Supportive therapy",
    "foot and mouth":"Supportive care + vaccination",
    "healthy":"No medicine required"
}

precautions = {
    "anthrax":"Isolate immediately",
    "blackleg":"Disinfect area",
    "pneumonia":"Keep warm shelter",
    "lumpy virus":"Control insects",
    "foot and mouth":"Isolate + disinfect area",
    "healthy":"Maintain hygiene"
}

# =====================================================
# HOME PAGE
# =====================================================
if st.session_state.page == "home":
    st.markdown("""
        <div class="hero-section">
            <div class="feature-label">Future of Agriculture</div>
            <h1 class="main-title">Precision Livestock <br>Management & AI</h1>
            <p class="sub-title">
            Utilizing machine learning and real-time data analytics to ensure the health,
            productivity, and sustainability of your herd.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="feature-box"><div class="feature-label">01. Predictive</div><h3 style="color:#1e293b;">Disease Diagnosis</h3><p style="color:#64748b;">Advanced algorithms detect symptoms early.</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="feature-box"><div class="feature-label">02. Analytical</div><h3 style="color:#1e293b;">Vital Monitoring</h3><p style="color:#64748b;">Track temperature and health indicators.</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="feature-box"><div class="feature-label">03. Automated</div><h3 style="color:#1e293b;">Health Management</h3><p style="color:#64748b;">Digital records and AI treatment guidance.</p></div>', unsafe_allow_html=True)

    st.write("### Select User Type")
    c1, c2, c3 = st.columns(3)
    if c1.button("👨‍🌾 Farmer", use_container_width=True):
        st.session_state.role = "farmer"; st.session_state.page="login"; st.rerun()
    if c2.button("🩺 Doctor", use_container_width=True):
        st.session_state.role = "doctor"; st.session_state.page="login"; st.rerun()
    if c3.button("🔬 Researcher", use_container_width=True):
        st.session_state.role = "researcher"; st.session_state.page="login"; st.rerun()

    st.markdown("<p style='text-align:center;color:#94a3b8;font-size:12px;'>INDUSTRIAL AI SYSTEM • VERSION 2.0</p>", unsafe_allow_html=True)

# =====================================================
# LOGIN PAGE
# =====================================================
elif st.session_state.page == "login":
    st.title("Login Verification")
    st.info(f"Logging in as: {st.session_state.role.title()}")
    user = st.text_input("Enter Phone or Email")
    if st.button("Send OTP"):
        st.session_state.otp = str(random.randint(1000,9999))
        st.success(f"Demo OTP: {st.session_state.otp}")
    otp = st.text_input("Enter OTP")
    if st.button("Verify Login"):
        if otp == st.session_state.otp: st.session_state.page="dashboard"; st.rerun()
        else: st.error("Invalid OTP")
    if st.button("Back"): st.session_state.page="home"; st.rerun()

# =====================================================
# DASHBOARD (ALL ROLES)
# =====================================================
elif st.session_state.page == "dashboard":

    role = st.session_state.get("role", None)
    page = st.session_state.get("nav", "Prediction")

    st.success("AI Model Active • Real-time Monitoring Enabled")
    c1, c2, c3 = st.columns(3)
    c1.metric("Animals Checked Today", 12)
    c2.metric("High Risk Cases", 3)
    c3.metric("Model Accuracy", "92%")

    with st.sidebar:
        if st.button("Prediction", use_container_width=True):
            st.session_state.nav = "Prediction"; st.rerun()
        if st.button("Analytics", use_container_width=True):
            st.session_state.nav = "Analytics"; st.rerun()
        if st.button("Logout", use_container_width=True):
            st.session_state.page = "home"; st.rerun()

    page = st.session_state.get("nav", "Prediction")

    # ---------------- FARMER DASHBOARD ----------------
    if role == "farmer":
        st.header("👨‍🌾 Farmer Dashboard")
        if page=="Prediction":
            animal = st.selectbox("Animal", ["cow","buffalo","sheep","goat"])
            temp = st.slider("Temperature",95.0,110.0,102.0)
            s1 = st.selectbox("Symptom 1", symptoms)
            s2 = st.selectbox("Symptom 2", symptoms)
            s3 = st.selectbox("Symptom 3", symptoms)

            if st.button("Predict Disease"):
                df = pd.DataFrame([{"Animal":animal,"Age":5,"Temperature":temp,"Symptom 1":s1,"Symptom 2":s2,"Symptom 3":s3}])
                for col in encoders:
                    df[col] = df[col].apply(lambda x: x if x in encoders[col].classes_ else encoders[col].classes_[0])
                    df[col] = encoders[col].transform(df[col])
                df = df[model.feature_names_in_]
                probs = model.predict_proba(df)[0]
                disease = label_encoder.inverse_transform([np.argmax(probs)])[0]
                risk = int(max(probs)*100)

                st.success("Predicted Disease: "+disease)
                st.metric("Animal Health Score", f"{100-risk}%")
                if risk>75: st.error("🔴 High Risk — Immediate care required")
                elif risk>40: st.warning("🟡 Moderate Risk — Monitor closely")
                else: st.success("🟢 Low Risk — Stable condition")
                st.info("Medicine: "+medicine.get(disease,"Consult veterinarian"))
                st.warning("Precaution: "+precautions.get(disease,"Isolate animal and monitor"))

                if disease != "healthy": st.warning("💉 Vaccination recommended within 30 days")
                else: st.success("Maintain regular vaccination schedule")

                record = pd.DataFrame([{"Animal":animal,"Temperature":temp,"Symptom 1":s1,"Symptom 2":s2,"Symptom 3":s3,"Prediction":disease,"Risk":risk}])
                record.to_csv("history.csv",mode="a",header=not os.path.exists("history.csv"),index=False)

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial","B",16)
                pdf.cell(0,10,"Animal Health Prediction Report",ln=True,align="C")
                pdf.ln(10)
                pdf.set_font("Arial","",12)
                pdf.cell(0,8,f"Animal: {animal}",ln=True)
                pdf.cell(0,8,f"Temperature: {temp}",ln=True)
                pdf.cell(0,8,f"Symptom 1: {s1}",ln=True)
                pdf.cell(0,8,f"Symptom 2: {s2}",ln=True)
                pdf.cell(0,8,f"Symptom 3: {s3}",ln=True)
                pdf.cell(0,8,f"Predicted Disease: {disease}",ln=True)
                pdf.cell(0,8,f"Risk Level: {risk}%",ln=True)
                pdf.cell(0,8,f"Medicine: {medicine.get(disease,'Consult vet')}",ln=True)
                pdf.cell(0,8,f"Precaution: {precautions.get(disease,'Monitor')}",ln=True)
                pdf_file="prediction_report.pdf"
                pdf.output(pdf_file)
                with open(pdf_file,"rb") as f:
                    st.download_button("Download Prediction PDF",f,"prediction_report.pdf","application/pdf")

        elif page=="Analytics":
            st.subheader("Animal Health Records")
            if os.path.exists("history.csv"):
                df_hist=pd.read_csv("history.csv")
                edited_df=st.data_editor(df_hist,num_rows="dynamic",use_container_width=True)
                if st.button("Save Changes"): edited_df.to_csv("history.csv",index=False); st.success("Records updated successfully"); st.rerun()
                st.subheader("Risk Distribution"); st.bar_chart(edited_df["Risk"])
                st.subheader("Cases by Animal"); st.bar_chart(edited_df["Animal"].value_counts())
                st.download_button("Download Records CSV",edited_df.to_csv(index=False),"animal_health_records.csv","text/csv")
            else: st.info("No records available yet.")

    # ---------------- DOCTOR DASHBOARD ----------------
    elif role == "doctor":
        st.header("🩺 Doctor Clinical Dashboard")
        if page=="Prediction":
            animal = st.selectbox("Animal", ["cow","buffalo","sheep","goat"], key="doc_animal")
            temp = st.slider("Temperature", 95.0, 110.0, 102.0, key="doc_temp")
            s1 = st.selectbox("Primary Symptom", symptoms, key="doc_s1")
            s2 = st.selectbox("Secondary Symptom", symptoms, key="doc_s2")
            s3 = st.selectbox("Additional Symptom", symptoms, key="doc_s3")

            if st.button("Run Diagnosis", key="doc_run"):
                df = pd.DataFrame([{"Animal":animal,"Age":6,"Temperature":temp,"Symptom 1":s1,"Symptom 2":s2,"Symptom 3":s3}])
                df.to_csv("clinical_cases.csv",mode="a",header=not os.path.exists("clinical_cases.csv"),index=False)
                for col in encoders:
                    df[col] = df[col].apply(lambda x: x if x in encoders[col].classes_ else encoders[col].classes_[0])
                    df[col] = encoders[col].transform(df[col])
                df = df[model.feature_names_in_]
                probs = model.predict_proba(df)[0]
                disease = label_encoder.inverse_transform([np.argmax(probs)])[0]
                risk = int(max(probs)*100)

                st.error("Diagnosis: " + disease.upper())
                st.subheader("Case Severity")
                if risk>75: st.error("Emergency Case")
                elif risk>40: st.warning("Needs Monitoring")
                else: st.success("Stable Condition")

                st.subheader("Prediction Probabilities")
                st.table(pd.DataFrame({"Disease": label_encoder.classes_, "Probability": probs}).sort_values("Probability", ascending=False))
                st.subheader("Treatment Protocol")
                st.success(medicine.get(disease,"Consult veterinarian"))
                st.write("Precautions:", precautions.get(disease,"Isolate animal and monitor"))

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial","B",16)
                pdf.cell(0,10,"Clinical Prediction Report",ln=True,align="C")
                pdf.ln(10)
                pdf.set_font("Arial","",12)
                pdf.cell(0,8,f"Animal: {animal}",ln=True)
                pdf.cell(0,8,f"Temperature: {temp}",ln=True)
                pdf.cell(0,8,f"Symptom 1: {s1}",ln=True)
                pdf.cell(0,8,f"Symptom 2: {s2}",ln=True)
                pdf.cell(0,8,f"Symptom 3: {s3}",ln=True)
                pdf.cell(0,8,f"Predicted Disease: {disease}",ln=True)
                pdf.cell(0,8,f"Risk Level: {risk}%",ln=True)
                pdf.cell(0,8,f"Treatment: {medicine.get(disease,'Consult vet')}",ln=True)
                pdf.cell(0,8,f"Precaution: {precautions.get(disease,'Monitor')}",ln=True)
                pdf_file="doctor_prediction_report.pdf"
                pdf.output(pdf_file)
                with open(pdf_file,"rb") as f:
                    st.download_button("Download Prediction PDF",f,pdf_file,"application/pdf")

        elif page=="Analytics":
            st.subheader("Clinical Case History")
            if os.path.exists("clinical_cases.csv"):
                df_cases = pd.read_csv("clinical_cases.csv")
                st.dataframe(df_cases)
                st.subheader("Cases by Animal")
                st.bar_chart(df_cases["Animal"].value_counts())
                if "Temperature" in df_cases.columns:
                    st.subheader("Temperature Trend")
                    st.line_chart(df_cases["Temperature"])
            else:
                st.info("No clinical cases recorded yet.")

    # ---------------- RESEARCHER DASHBOARD ----------------
    elif role == "researcher":
        st.header("🔬 Research Dashboard")
        if data is None:
            st.error("Dataset not found")
        else:
            if page=="Analytics":
                st.subheader("Dataset Preview")
                st.dataframe(data.head())
                st.subheader("Statistical Summary")
                st.write(data.describe())
                st.subheader("Disease Distribution")
                st.bar_chart(data["Disease"].value_counts())
                st.subheader("Cases by Animal")
                st.bar_chart(data.groupby("Animal")["Disease"].count())
                if "Temperature" in data.columns:
                    st.subheader("Temperature Trend")
                    st.line_chart(data["Temperature"])
                animal_filter = st.selectbox("Filter by Animal", data["Animal"].unique(), key="researcher_filter")
                st.subheader("Filtered Dataset")
                st.dataframe(data[data["Animal"]==animal_filter])
                top_disease = data["Disease"].value_counts().idxmax()
                top_animal = data["Animal"].value_counts().idxmax()
                st.info(f"Most common disease: {top_disease}")
                st.info(f"Most affected animal: {top_animal}")
                if "Temperature" in data.columns:
                                        avg_temp = round(data["Temperature"].mean(),2)
                                        st.info(f"Average recorded temperature: {avg_temp}")

            # ✅ NEW — RESEARCHER CODING PLAYGROUND
            elif page == "Prediction":
                st.subheader("Research Coding Playground")

                st.info("Dataset is preloaded as: data\nModel is loaded as: model\nLabel encoder: label_encoder")

                default_code = """# Example: View dataset
st.write(data.head())

# Example: Train quick model
from sklearn.ensemble import RandomForestClassifier

df = data.copy()

X = df.drop("Disease", axis=1)
y = df["Disease"]

for col in encoders:
    X[col] = encoders[col].transform(X[col])

model_rf = RandomForestClassifier()
model_rf.fit(X, y)

st.success("Model trained successfully")
"""

                user_code = st.text_area("Write your analysis code", default_code, height=300)

                if st.button("Run Code"):
                    try:
                        exec(user_code)
                    except Exception as e:
                        st.error(str(e))