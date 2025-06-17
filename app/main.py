import streamlit as st

# ✅ Must be first Streamlit command
st.set_page_config(page_title="HavenAI", layout="wide")

# 🛠 Standard imports
import os
import sys
import pandas as pd

# 🛠 Fix import path for local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ai_summary import generate_mock_summary
from app.threat_scoring import compute_threat_scores
from app.export_report import build_threat_report
from app.i18n import t, LANGUAGES

# -----------------------------
# 🌗 Theme Toggle
# -----------------------------
theme_choice = st.sidebar.radio("🌓 Theme", ["Dark", "Light"])
if theme_choice == "Light":
    st.markdown("""
        <style>
            body, .stApp { background-color: #ffffff; color: #000000; }
            .block-container { color: #000000; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body, .stApp { background-color: #0E1117; color: #FAFAFA; }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# 🌍 Language Selection
# -----------------------------
lang = st.sidebar.selectbox(
    "🌍 Language / 言語 / Idioma / 语言",
    LANGUAGES.keys(),
    format_func=lambda x: LANGUAGES[x]
)

# -----------------------------
# 🧠 HavenAI App Body
# -----------------------------
st.title(t("title", lang))
st.markdown("Upload logs. Get instant threat insights. No cloud required.")

# 📤 File Upload
uploaded_file = st.file_uploader(t("upload_prompt", lang), type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Log file uploaded successfully!")

        # 📄 Preview Logs
        st.subheader("📄 Preview of Uploaded Logs")
        st.dataframe(df.head())

        # 📊 Event Type Breakdown
        st.subheader("📊 Event Type Breakdown")
        if "event_type" in df.columns:
            st.bar_chart(df["event_type"].value_counts())
        else:
            st.warning("⚠️ No 'event_type' column found.")

        # 🌐 Top IPs
        if "source_ip" in df.columns:
            st.subheader("🌐 Top Source IPs")
            st.write(df["source_ip"].value_counts().head(10))

        # 🧠 AI Summary
        st.subheader("🧠 AI Log Summary (Demo Mode)")
        if st.button(t("ai_summary_btn", lang)):
            with st.spinner("Generating..."):
                summary = generate_mock_summary(df)
                st.success("AI Summary Complete:")
                st.markdown(summary)

        # 🚨 Threat Scoring
        st.subheader("⚠️ Threat Scoring")
        if st.button(t("threat_score_btn", lang)):
            with st.spinner("Analyzing..."):
                df_scored, error = compute_threat_scores(df)
                if error:
                    st.error(error)
                else:
                    st.success("Threat scoring complete. Anomalies detected:")
                    st.dataframe(df_scored[df_scored["threat_score"] == "Anomalous"].head(10))
                    df = df_scored

        # 📥 Export CSV
        st.subheader("📥 Export")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(t("download_csv", lang), csv, file_name="processed_log.csv")

        # 📄 Report Export
        st.subheader("📄 Export Threat Report")
        if st.button(t("generate_report", lang)):
            with st.spinner("Creating report..."):
                ai_summary = generate_mock_summary(df)
                report = build_threat_report(df, ai_summary)
                st.download_button("Download AI Threat Report (.txt)", report, file_name="havenai_report.txt")

    except Exception as e:
        st.error(f"🚫 Error reading file: {e}")
else:
    st.info("📎 Please upload a CSV log file to begin.")
