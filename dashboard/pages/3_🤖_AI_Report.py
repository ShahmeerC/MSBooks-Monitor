import streamlit as st
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

logging_df = pd.read_csv("data/monthly_monitor_log.csv")
ai_summary = logging_df.iloc[-1]["AI Dashboard Summary"]
latest_run = logging_df.iloc[-1]["Date"]

st.set_page_config(
    page_title="AI Report — MS Books Dashboard",
    page_icon="dashboard/logos/iconremovebg.ico",
    layout="wide"
)

st.sidebar.title("MS Books")
st.sidebar.caption("Monitoring Platform")

col1, col2 = st.columns([1,8])
col1.image("dashboard/logos/logoremovebg.png", width=100)
col2.title("AI Intelligence Report")

st.subheader("Last Month's summary")

if ai_summary:
    st.write(f"Generated on: {latest_run}")
    st.markdown(ai_summary)
else:
    st.write("No AI summary available")