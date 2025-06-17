import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ai_summary import generate_mock_summary  # Correct path assuming you’re in HavenAI root

st.set_page_config(page_title="HavenAI", layout="wide")

# Sidebar
with st.sidebar:
    st.markdown("### 🌙 Theme")
    st.radio("Theme", ["Dark", "Light"], index=0)
    st.markdown("### 🌐 Language / 言語 / Idioma / 语言")
    st.selectbox("Language", ["English", "日本語", "Español", "中文"], index=0)

st.title("🔐 HavenAI - AI-Powered Log Analyzer")
st.markdown("Upload logs. Get instant threat insights. No cloud required.")

uploaded_file = st.file_uploader("📤 Upload your log file (CSV format)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        st.markdown(
            "<div style='background-color: #2e7d32; color: white; padding: 12px; border-radius: 6px;'>✅ Log file uploaded successfully!</div>",
            unsafe_allow_html=True,
        )

        st.subheader("📄 Preview of Uploaded Logs")
        st.dataframe(df.head())

        if "event_type" in df.columns:
            st.subheader("📊 Event Type Breakdown")
            event_counts = df["event_type"].value_counts()
            st.bar_chart(event_counts)
        else:
            st.warning("⚠️ No 'event_type' column found in uploaded file.")

        if "source_ip" in df.columns:
            st.subheader("🌐 Top Source IPs")
            top_ips = df["source_ip"].value_counts().head(10)
            st.write(top_ips)

        st.subheader("🤖 AI Summary (Demo Mode)")
        with st.expander("Show AI-generated insights"):
            summary = generate_mock_summary(df)
            st.markdown(summary)

        st.subheader("📥 Export")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned CSV", csv, file_name="processed_log.csv")

    except Exception as e:
        st.error(f"🚫 Error processing file: {e}")
else:
    st.info("Upload a CSV log file to begin.")
