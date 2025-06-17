import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Relative import since you're running from HavenAI root
from app.ai_summary import generate_mock_summary

# Set page configuration
st.set_page_config(page_title="HavenAI", layout="wide")

# Sidebar
with st.sidebar:
    st.markdown("### 🌙 Theme")
    selected_theme = st.radio("Theme", ["Dark", "Light"], index=0)
    
    st.markdown("### 🌐 Language / 言語 / Idioma / 语言")
    st.selectbox("Language", ["English", "日本語", "Español", "中文"], index=0)

# Apply theme via custom background colors for plots
if selected_theme == "Dark":
    background_color = "#0E1117"
    font_color = "#FFFFFF"
    plot_bar_color = "#64b5f6"
else:
    background_color = "#FFFFFF"
    font_color = "#000000"
    plot_bar_color = "#1976d2"

# Title and description
st.title("🔐 HavenAI - AI-Powered Log Analyzer")
st.markdown("Upload logs. Get instant threat insights. No cloud required.")

# File uploader
uploaded_file = st.file_uploader("📤 Upload your log file (CSV format)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Success message
        st.markdown(
            f"<div style='background-color: #2e7d32; color: white; padding: 12px; border-radius: 6px;'>✅ Log file uploaded successfully!</div>",
            unsafe_allow_html=True,
        )

        # Preview
        st.subheader("📄 Preview of Uploaded Logs")
        st.dataframe(df.head(10), use_container_width=True)

        # Event breakdown chart
        st.subheader("📊 Event Type Breakdown")
        if "event_type" in df.columns:
            event_counts = df["event_type"].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(6, 3))
            event_counts.plot(kind="bar", ax=ax, color=plot_bar_color)
            ax.set_xlabel("Event Type", fontsize=10, color=font_color)
            ax.set_ylabel("Count", fontsize=10, color=font_color)
            ax.tick_params(axis="x", labelsize=9, rotation=0, colors=font_color)
            ax.tick_params(axis="y", labelsize=9, colors=font_color)
            fig.patch.set_facecolor(background_color)
            ax.set_facecolor(background_color)
            fig.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("⚠️ No 'event_type' column found in uploaded file.")

        # Top source IPs
        if "source_ip" in df.columns:
            st.subheader("🌐 Top Source IPs")
            top_ips = df["source_ip"].value_counts().head(10)
            st.dataframe(top_ips, use_container_width=True)

        # AI Summary (Demo)
        st.subheader("🤖 AI Summary (Demo Mode)")
        with st.expander("Show AI-generated insights"):
            summary = generate_mock_summary(df)
            st.markdown(summary)

        # Download
        st.subheader("📥 Export")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned CSV", csv, file_name="processed_log.csv")

    except Exception as e:
        st.error(f"🚫 Error processing file: {e}")
else:
    st.info("Upload a CSV log file to begin.")
