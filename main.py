import streamlit as st
import pandas as pd
import altair as alt
import os
from app.ai_summary import generate_mock_summary  # Ensure this file exists

# Page config
st.set_page_config(page_title="HavenAI", layout="wide")

# Sidebar - Theme and Language
with st.sidebar:
    st.markdown("### 🌙 Theme")
    theme = st.radio("Theme", ["Dark", "Light"], index=0)

    st.markdown("### 🌐 Language")
    language = st.selectbox("Language", ["English", "日本語", "Español", "中文"], index=0)

# Apply theme colors
bg_color = "#1e1e1e" if theme == "Dark" else "#f4f4f4"
text_color = "#ffffff" if theme == "Dark" else "#000000"

# Title
st.markdown(
    f"<h1 style='color:{text_color};'>🔐 HavenAI - AI-Powered Log Analyzer</h1>"
    "<p style='font-size:18px;'>Upload logs. Get instant threat insights. No cloud required.</p>",
    unsafe_allow_html=True
)

# Load sample or uploaded file
uploaded_file = st.file_uploader("📤 Upload your log file (CSV format)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown("<div style='background-color:#2e7d32; color:white; padding:10px; border-radius:6px;'>✅ File uploaded successfully!</div>", unsafe_allow_html=True)
else:
    sample_path = "sample_logs/example.log.csv"
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        st.info("🧪 Using sample log file: `example.log.csv`")
    else:
        st.warning("⚠️ No log file provided and no sample file found.")
        df = None

# Main content
if df is not None and not df.empty:
    st.subheader("📄 Preview of Logs")
    st.dataframe(df.head())

    # 📊 Event breakdown with Altair
    if "event_type" in df.columns:
        st.subheader("📊 Event Type Breakdown")
        event_counts = df["event_type"].value_counts().reset_index()
        event_counts.columns = ["event_type", "count"]

        chart = alt.Chart(event_counts).mark_bar().encode(
            x=alt.X("event_type:N", title="Event Type"),
            y=alt.Y("count:Q", title="Count"),
            color="event_type:N",
            tooltip=["event_type", "count"]
        ).properties(
            width=600,
            height=400,
            title="Event Frequency"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ No 'event_type' column in the log file.")

    # 🌐 Top IPs
    if "source_ip" in df.columns:
        st.subheader("🌐 Top Source IPs")
        top_ips = df["source_ip"].value_counts().head(10)
        st.write(top_ips)

    # 🤖 AI Summary (Demo mode)
    st.subheader("🤖 AI Summary (Demo Mode)")
    with st.expander("Show Insights", expanded=True):
        summary = generate_mock_summary(df)
        st.markdown(summary)

    # 📥 Export
    st.subheader("📥 Export")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Processed CSV", csv, file_name="processed_log.csv")

else:
    st.info("Please upload a CSV log file to begin.")
