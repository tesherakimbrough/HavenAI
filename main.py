import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from ai_summary import generate_mock_summary  # Adjust if your import path is different

# Set Streamlit config
st.set_page_config(page_title="HavenAI", layout="wide")

# Sidebar Theme + Language Toggle
with st.sidebar:
    st.markdown("### 🌙 Theme")
    selected_theme = st.radio("Theme", ["Dark", "Light"], index=0)

    st.markdown("### 🌐 Language / 言語 / Idioma / 语言")
    st.selectbox("Language", ["English", "日本語", "Español", "中文"], index=0)

# Apply dynamic styling based on theme
if selected_theme == "Dark":
    bg_color = "#0e1117"
    text_color = "#FFFFFF"
    accent_color = "#1f77b4"
    mpl.style.use("dark_background")
    df_style = {"backgroundColor": "#0e1117", "color": "#FFFFFF"}
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    accent_color = "#007ACC"
    mpl.style.use("default")
    df_style = {"backgroundColor": "#FFFFFF", "color": "#000000"}

# Inject CSS styling
st.markdown(
    f"""
    <style>
        body, .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stButton>button {{
            background-color: {accent_color};
            color: white;
            border-radius: 8px;
            padding: 6px 16px;
            font-weight: bold;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title & Subtitle
st.title("🔐 HavenAI - AI-Powered Log Analyzer")
st.markdown("Upload logs. Get instant threat insights. No cloud required.")

# Upload CSV log file
uploaded_file = st.file_uploader("📤 Upload your log file (CSV format)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Success message
        st.markdown(
            f"<div style='background-color: #2e7d32; color: white; padding: 12px; border-radius: 6px;'>✅ Log file uploaded successfully!</div>",
            unsafe_allow_html=True,
        )

        # Preview logs
        st.subheader("📄 Preview of Uploaded Logs")
        st.dataframe(df.style.set_properties(**df_style))

        # Event Breakdown
        st.subheader("📊 Event Type Breakdown")
        if "event_type" in df.columns:
            event_counts = df["event_type"].value_counts()
            fig, ax = plt.subplots()
            event_counts.plot(kind="bar", color=accent_color, ax=ax)
            ax.set_ylabel("Count")
            ax.set_title("Event Types")
            st.pyplot(fig)
        else:
            st.warning("⚠️ No 'event_type' column found in uploaded file.")

        # Top Source IPs
        if "source_ip" in df.columns:
            st.subheader("🌐 Top Source IPs")
            top_ips = df["source_ip"].value_counts().head(10)
            st.bar_chart(top_ips)
        
        # AI Summary
        st.subheader("🤖 AI Summary (Demo Mode)")
        with st.expander("Show AI-generated insights"):
            summary = generate_mock_summary(df)
            st.markdown(summary)

        # Download Processed CSV
        st.subheader("📥 Export")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Processed CSV", csv, file_name="processed_log.csv")

    except Exception as e:
        st.error(f"🚫 Error processing file: {e}")
else:
    st.info("Upload a CSV log file to begin.")
